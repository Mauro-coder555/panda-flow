import pandas as pd
import json
import tabulate

class PandaFlow:
    def __init__(self, df):
        """
        Inicializa el limpiador con un DataFrame.
        """
        if not isinstance(df, pd.DataFrame):
            raise ValueError("El objeto debe ser un DataFrame de pandas.")
        self.df = df

    def handle_nulls(self, strategy="drop", fill_value=None):
        """
        Maneja valores nulos en el DataFrame.
        
        Parameters:
        - strategy: Estrategia para manejar nulos:
            - 'drop': Eliminar filas o columnas con nulos.
            - 'fill': Rellenar con un valor específico.
            - 'mean': Rellenar con la media de cada columna (numérica).
            - 'median': Rellenar con la mediana de cada columna (numérica).
            - 'mode': Rellenar con la moda de cada columna.
        - fill_value: Valor a usar si strategy='fill'.
        
        Returns:
        - DataFrame con los nulos manejados.
        """
        if strategy == "drop":
            df = self.df.dropna()
            print("Filas con valores nulos eliminadas.")
            return df

        elif strategy == "fill":
            if fill_value is None:
                raise ValueError("Debes especificar un 'fill_value' para rellenar nulos.")
            self.df = self.df.fillna(fill_value)
            print(f"Valores nulos rellenados con: {fill_value}")

        elif strategy == "mean":
            # Validar si hay columnas numéricas
            numeric_cols = self.df.select_dtypes(include=["number"]).columns
            if numeric_cols.empty:
                raise ValueError("No hay columnas numéricas para calcular la media.")
            # Rellenar nulos con la media de cada columna numérica
            self.df[numeric_cols] = self.df[numeric_cols].fillna(self.df[numeric_cols].mean())
            print("Valores nulos rellenados con la media de las columnas numéricas.")

        elif strategy == "median":
            # Validar si hay columnas numéricas
            numeric_cols = self.df.select_dtypes(include=["number"]).columns
            if numeric_cols.empty:
                raise ValueError("No hay columnas numéricas para calcular la mediana.")
            # Rellenar nulos con la mediana de cada columna numérica
            self.df[numeric_cols] = self.df[numeric_cols].fillna(self.df[numeric_cols].median())
            print("Valores nulos rellenados con la mediana de las columnas numéricas.")

        elif strategy == "mode":
            # Rellenar nulos con la moda de cada columna
            for col in self.df.columns:
                mode_value = self.df[col].mode()
                if not mode_value.empty:
                    self.df[col] = self.df[col].fillna(mode_value[0])
                else:
                    print(f"No se encontró una moda válida para la columna '{col}'.")
            print("Valores nulos rellenados con la moda de las columnas.")

        else:
            raise ValueError("Estrategia no reconocida. Usa 'drop', 'fill', 'mean', 'median' o 'mode'.")

        return self.df

    def handle_duplicates(self, strategy="drop"):
        """
        Maneja duplicados en el DataFrame.
        
        Parameters:
        - strategy: 'drop' para eliminar duplicados,
                    'keep_first' para mantener el primer duplicado,
                    'keep_last' para mantener el último duplicado.
        """
        if strategy == "drop":
            self.df = self.df.drop_duplicates()
        elif strategy == "keep_first":
            self.df = self.df.drop_duplicates(keep="first")
        elif strategy == "keep_last":
            self.df = self.df.drop_duplicates(keep="last")
        else:
            raise ValueError("Estrategia no reconocida. Usa 'drop', 'keep_first' o 'keep_last'.")
        return self.df

    def _detect_json_type(self, column):
        """
        Detecta si el contenido de una columna es JSON y su tipo.

        Parameters:
        - column: Pandas Series (columna del DataFrame)

        Returns:
        - str indicando el tipo de JSON (o None si no es JSON).
        """
        is_json = False
        json_type = None

        for value in column.dropna():
            try:
                parsed = json.loads(value) if isinstance(value, str) else None
                if isinstance(parsed, (dict, list)):
                    is_json = True
                    json_type = "Normal JSON"
                elif isinstance(parsed, str) and "\n" in parsed:
                    is_json = True
                    json_type = "Line-by-line JSON"
                else:
                    continue
            except (TypeError, ValueError):
                continue

            if is_json:
                break

        return f"JSON ({json_type})" if is_json else None

    def inspect_outliers(self, method="iqr", threshold=1.5):
        """
        Inspecciona los valores atípicos (outliers) en el DataFrame.

        Parameters:
        - method: Método para detectar outliers:
            - 'iqr': Usar rango intercuartil (IQR).
            - 'std': Usar desviaciones estándar.
            - 'percentile': Usar percentiles (e.g., 1% y 99% como límite).
        - threshold: Umbral para identificar outliers (e.g., multiplicador del IQR o std).

        Returns:
        - DataFrame resumen con:
            - Columna.
            - Cantidad de outliers.
            - Porcentaje de outliers.
            - Rango o valores extremos.
            - Método usado.
        """
        numeric_cols = self.df.select_dtypes(include=["number"]).columns
        if numeric_cols.empty:
            raise ValueError("No hay columnas numéricas para inspeccionar valores atípicos.")
        
        summary = []

        for col in numeric_cols:
            if method == "iqr":
                q1 = self.df[col].quantile(0.25)
                q3 = self.df[col].quantile(0.75)
                iqr = q3 - q1
                lower_bound = q1 - threshold * iqr
                upper_bound = q3 + threshold * iqr
            elif method == "std":
                mean = self.df[col].mean()
                std_dev = self.df[col].std()
                lower_bound = mean - threshold * std_dev
                upper_bound = mean + threshold * std_dev
            elif method == "percentile":
                lower_bound = self.df[col].quantile(threshold / 100)
                upper_bound = self.df[col].quantile(1 - threshold / 100)
            else:
                raise ValueError("Método no reconocido. Usa 'iqr', 'std' o 'percentile'.")

            # Identificar valores atípicos
            outliers = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)]
            num_outliers = outliers.shape[0]
            percent_outliers = (num_outliers / self.df.shape[0]) * 100
            range_extremes = f"[{lower_bound}, {upper_bound}]"

            summary.append({
                "Column": col,
                "Num Outliers": num_outliers,
                "% Outliers": percent_outliers,
                "Range/Extremes": range_extremes,
                "Method": method
            })

        summary_df = pd.DataFrame(summary)
        print("Inspección de outliers completada.")
        return summary_df

    def summarize_columns(self):
        """
        Genera un resumen de las columnas del DataFrame, mostrando:
        - Nombre de las columnas
        - Porcentaje de nulos y no nulos
        - Cantidad de nulos y no nulos
        - Tipo de datos de cada columna
        """
        summary = []
        total_rows = len(self.df)

        for col in self.df.columns:
            null_count = self.df[col].isnull().sum()
            not_null_count = total_rows - null_count
            null_percent = (null_count / total_rows) * 100 if total_rows > 0 else 0
            not_null_percent = 100 - null_percent

            # Detectar si es un JSON o asignar el tipo base
            json_type = self._detect_json_type(self.df[col])
            dtype = json_type if json_type else self.df[col].dtype

            summary.append({
                "Column": col,
                "Null %": f"{null_percent:.2f}%",
                "Not Null %": f"{not_null_percent:.2f}%",
                "Null Count": null_count,
                "Not Null Count": not_null_count,
                "Type": dtype
            })

        # Mostrar la tabla con tabulate
        print(tabulate.tabulate(summary, headers="keys", tablefmt="fancy_grid"))

        

    def handle_outliers(self, method="iqr", threshold=1.5, action="remove", replacement_value=None):
        """
        Maneja valores atípicos (outliers) en el DataFrame.

        Parameters:
        - method: Método para detectar outliers:
            - 'iqr': Usar rango intercuartil (IQR).
            - 'std': Usar desviaciones estándar.
            - 'percentile': Usar percentiles (e.g., 1% y 99% como límite).
        - threshold: Umbral para identificar outliers (e.g., multiplicador del IQR o std).
        - action: Acción a tomar con los outliers:
            - 'remove': Eliminar filas con outliers.
            - 'replace': Reemplazar outliers con un valor.
            - 'mark': Agregar una columna indicando si cada fila contiene outliers.
        - replacement_value: Valor a usar si action='replace'.

        Returns:
        - DataFrame con los outliers manejados.
        """
        numeric_cols = self.df.select_dtypes(include=["number"]).columns
        if numeric_cols.empty:
            raise ValueError("No hay columnas numéricas para detectar outliers.")
        
        df_outliers = self.df.copy()

        for col in numeric_cols:
            if method == "iqr":
                q1 = self.df[col].quantile(0.25)
                q3 = self.df[col].quantile(0.75)
                iqr = q3 - q1
                lower_bound = q1 - threshold * iqr
                upper_bound = q3 + threshold * iqr
            elif method == "std":
                mean = self.df[col].mean()
                std_dev = self.df[col].std()
                lower_bound = mean - threshold * std_dev
                upper_bound = mean + threshold * std_dev
            elif method == "percentile":
                lower_bound = self.df[col].quantile(threshold / 100)
                upper_bound = self.df[col].quantile(1 - threshold / 100)
            else:
                raise ValueError("Método no reconocido. Usa 'iqr', 'std' o 'percentile'.")

            # Detectar valores atípicos
            outliers = (self.df[col] < lower_bound) | (self.df[col] > upper_bound)

            if action == "remove":
                df_outliers = df_outliers[~outliers.reindex(df_outliers.index, fill_value=False)]
            elif action == "replace":
                if replacement_value is None:
                    raise ValueError("Debes especificar un 'replacement_value' para reemplazar outliers.")
                df_outliers.loc[outliers, col] = replacement_value
            elif action == "mark":
                mark_col = f"{col}_is_outlier"
                df_outliers[mark_col] = outliers
            else:
                raise ValueError("Acción no reconocida. Usa 'remove', 'replace' o 'mark'.")

        if action == "remove":
            print("Filas con valores atípicos eliminadas.")
        elif action == "replace":
            print(f"Valores atípicos reemplazados con: {replacement_value}")
        elif action == "mark":
            print("Se agregó una columna para marcar los valores atípicos.")

        return df_outliers