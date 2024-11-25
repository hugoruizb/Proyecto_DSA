

# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, jsonify
import joblib
import traceback
import pandas as pd

app = Flask(__name__)

# Carga del modelo
#model = joblib.load('./model_attrition.joblib')
model = joblib.load('/opt/attrition-api/app/model_attrition.joblib')

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Lista de las variables esperadas por el modelo
        expected_fields = [
            'age', 'BusinessTravel', 'Department',
            'DistanceFromHome', 'Education', 'EducationField',
            'Gender', 'MaritalStatus', 'MonthlyRate',
            'NumCompaniesWorked', 'TrainingTimesLastYear', 'YearsAtCompany'
        ]
        
        # Captura de los datos del formulario
        input_data = {}
        for field in expected_fields:
            value = request.form.get(field, type=float)
            if value is None:
                return jsonify({'error': f'El campo {field} es requerido y debe ser un número válido.'}), 400
            input_data[field] = int(value)
        
        # Preparar los datos para el modelo
        input_df = pd.DataFrame([input_data])
        
        # Realizar la predicción
        prediction = model.predict(input_df)[0]  # Obtener la primera (y única) predicción
        
        return jsonify({'Attrition': int(prediction)})
    
    except Exception as e:
        # Mostrar error en consola y responder con un mensaje
        traceback.print_exc()
        return jsonify({'error': f'Ha ocurrido un error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=8000)
