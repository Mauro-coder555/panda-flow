# PandaFlow: Una biblioteca para limpieza y transformación de datos con Pandas

Esta biblioteca proporciona una clase `PandaFlow` que facilita la limpieza y transformación de datos utilizando la librería pandas. 

## Características principales

* **Manejo de valores nulos:**
    * Eliminar filas o columnas con valores nulos.
    * Rellenar valores nulos con un valor específico, la media, la mediana o la moda.
* **Manejo de duplicados:**
    * Eliminar duplicados.
    * Mantener el primer o último duplicado.
* **Detección e inspección de outliers:**
    * Detectar outliers utilizando diferentes métodos (IQR, desviación estándar, percentiles).
    * Inspeccionar y obtener un resumen de los outliers.
* **Manejo de outliers:**
    * Eliminar filas con outliers.
    * Reemplazar outliers con un valor específico.
    * Marcar filas con outliers.
* **Resumen de columnas:**
    * Obtener un resumen de las columnas del DataFrame, incluyendo:
        * Nombre de la columna.
        * Porcentaje de valores nulos y no nulos.
        * Cantidad de valores nulos y no nulos.
        * Tipo de datos de la columna.

## Instalación

```bash
pip install panda_flow  # El paquete se va a publicar en PyPI
```

## Ventajas de PandaFlow

### 1. **Simplificación del código**
- **Pandas:** Requiere escribir múltiples líneas de código para tareas comunes, como manejar valores nulos o duplicados. Además, a menudo es necesario recordar detalles específicos de la API de pandas.
- **PandaFlow:** Ofrece métodos directos (`handle_nulls`, `handle_duplicates`, etc.) con estrategias predefinidas, reduciendo la cantidad de código que necesitas escribir y haciendo que sea más legible.

### 2. **Estandarización de procesos**
- **Pandas:** Los usuarios necesitan implementar sus propias funciones o flujos para tareas como detectar y manejar valores atípicos.
- **PandaFlow:** Proporciona funciones estandarizadas con parámetros configurables que aseguran un flujo de trabajo consistente.

### 3. **Manejo integrado de outliers**
- **Pandas:** No incluye una solución directa para identificar y manejar valores atípicos; los usuarios deben implementar métodos basados en métricas como el rango intercuartil (IQR) o z-scores manualmente.
- **PandaFlow:** Incluye funciones integradas para detectar, eliminar, reemplazar o marcar outliers con métodos comunes, como `iqr`.

### 4. **Resúmenes detallados**
- **Pandas:** Para obtener un resumen de valores nulos, no nulos y tipos de datos, los usuarios deben escribir varias líneas de código utilizando métodos como `df.info()`, `df.isnull().sum()` y `df.dtypes`.
- **PandaFlow:** La función `summarize_columns()` genera un resumen completo en un solo paso, incluyendo métricas útiles que pandas no ofrece directamente.

### 5. **Manejo de JSON integrado**
- **Pandas:** Detectar columnas con datos en formato JSON requiere escribir lógica personalizada.
- **PandaFlow:** Proporciona un método integrado para detectar columnas con datos en formato JSON (`_detect_json_type`).

### 6. **Reducción de errores comunes**
- **Pandas:** La manipulación manual puede introducir errores al realizar operaciones repetitivas o complejas.
- **PandaFlow:** Al encapsular lógica en métodos bien probados, reduce las probabilidades de errores humanos en tareas repetitivas.

### 7. **Más accesible para principiantes**
- **Pandas:** La curva de aprendizaje puede ser pronunciada, especialmente para usuarios nuevos en manipulación de datos.
- **PandaFlow:** Simplifica la interacción al ofrecer métodos con nombres intuitivos y documentación clara.

### 8. **Flujo de trabajo más rápido**
- **Pandas:** Requiere más tiempo para implementar funciones personalizadas.
- **PandaFlow:** Los métodos prediseñados aceleran las tareas comunes, liberando tiempo para análisis más profundo.

### 9. **Extensible y adaptable**
- **Pandas:** Los usuarios a menudo necesitan modificar el código base de sus scripts para cambiar la lógica.
- **PandaFlow:** Ofrece parámetros configurables (por ejemplo, estrategias para valores nulos y duplicados) que permiten adaptar fácilmente el comportamiento a diferentes casos.

## Cómo PandaFlow aporta valor adicional

1. **Productividad aumentada:** Reduce el tiempo necesario para escribir código repetitivo y permite concentrarse en tareas de análisis más complejas.

2. **Legibilidad y mantenibilidad del código:** El código basado en PandaFlow es más limpio y comprensible, facilitando la colaboración y el mantenimiento del proyecto.

3. **Menor curva de aprendizaje para nuevos integrantes del equipo:** Las funciones abstractas y la documentación de PandaFlow hacen que sea más fácil para nuevos analistas y científicos de datos integrarse al flujo de trabajo.

4. **Facilita el prototipado rápido:** Con funciones preconstruidas, es más rápido probar diferentes enfoques en la limpieza y transformación de datos.

5. **Reutilización de lógica estandarizada:** Las funciones de PandaFlow encapsulan mejores prácticas, lo que significa que puedes confiar en que las operaciones de limpieza cumplen con estándares establecidos sin necesidad de implementarlas manualmente.


## Uso

Ejemplo básico:

```python
import pandas as pd
from panda_flow import PandaFlow

# Crear un DataFrame de ejemplo
data = {'col1': [1, 2, None, 4, 5], 
        'col2': ['a', 'b', 'c', 'b', None], 
        'col3': [10.0, 20.0, 30.0, None, 50.0]}
df = pd.DataFrame(data)

# Crear una instancia de PandaFlow
dflow = PandaFlow(df)

# Manejar valores nulos
df_clean = dflow.handle_nulls(strategy='fill', fill_value=0) 

# Manejar duplicados
df_clean = dflow.handle_duplicates(strategy='keep_first')

# Inspeccionar outliers
outlier_summary = dflow.inspect_outliers(method='iqr')
print(outlier_summary)

# Manejar outliers
df_clean = dflow.handle_outliers(method='iqr', action='replace', replacement_value=0)

# Resumen de columnas
dflow.summarize_columns()
```


# Contribución

¡Las contribuciones son bienvenidas! Si encuentras un problema o tienes una idea para una nueva funcionalidad, no dudes en abrir un issue o enviar un pull request.

# Licencia

Este proyecto está bajo la licencia MIT. Puedes ver los detalles en el archivo LICENSE.