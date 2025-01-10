from setuptools import setup, find_packages

setup(
    name="datacleaner_light",
    version="0.1",
    description="Paquete ligero para limpieza de datos en Pandas.",
    author="Tu Nombre",
    author_email="tuemail@ejemplo.com",
    url="https://github.com/tuusuario/datacleaner_light",
    packages=find_packages(),
    install_requires=["pandas>=1.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
