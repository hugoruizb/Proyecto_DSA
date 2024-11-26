FROM python:3.10

# Crear usuario que ejecuta la app
RUN adduser --disabled-password --gecos '' api-user

# Definir directorio de trabajo
WORKDIR /opt/attrition-api

# Instalar dependencias
COPY ./attrition-api /opt/attrition-api/
RUN pip install --upgrade pip
RUN pip install -r /opt/attrition-api/requirements.txt

# Copiar el modelo desde la carpeta correcta
COPY attrition-api/app/model_attrition.joblib /opt/attrition-api/app/model_attrition.joblib

# Hacer el directorio de trabajo ejecutable
RUN chmod +x /opt/attrition-api/run.sh
# Cambiar propiedad de la carpeta a api-user
RUN chown -R api-user:api-user ./

USER api-user
# Puerto a exponer para la api
EXPOSE 8000

# Comandos a ejecutar al correr el contenedor
CMD ["bash", "./run.sh"]
