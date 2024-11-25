# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="attrition_api_project",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "flask",
        "joblib",
        "scikit-learn",  # Otras dependencias necesarias
    ],
    entry_points={
        "console_scripts": [
            "run-my-api=api_package.app:app.run",  # Define el comando para lanzar la API
        ]
    },
    description="API para predicciones con el modelo entrenado",
    #long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Tu Nombre",
    author_email="h.ruizb@uniadnes.edu.co",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
