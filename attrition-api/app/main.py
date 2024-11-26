
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
        # Captura de los datos del formulario
        age = request.form.get('Age', type=int)
        BusinessTravel = request.form.get('BusinessTravel', type=int)
        Department = request.form.get('Department', type=int)
        DistanceFromHome = request.form.get('DistanceFromHome', type=int)
        Education = request.form.get('Education', type=int)
        EducationField = request.form.get('EducationField', type=int)
        Gender = request.form.get('Gender', type=int)
        MaritalStatus = request.form.get('MaritalStatus', type=int)
        NumCompaniesWorked = request.form.get('NumCompaniesWorked', type=int)
        TrainingTimesLastYear = request.form.get('TrainingTimesLastYear', type=int)
        YearsAtCompany = request.form.get('YearsAtCompany', type=int)

        # Validación de datos (si es necesario)
        required_fields = [age, BusinessTravel, Department, DistanceFromHome, Education,
                           EducationField, Gender, MaritalStatus, NumCompaniesWorked,
                           TrainingTimesLastYear, YearsAtCompany]

        if None in required_fields:
            return jsonify({'error': 'Todos los campos son obligatorios.'}), 400

        # Preparar datos de entrada
        input_data = pd.DataFrame({
            'Age': [age],
            'BusinessTravel': [BusinessTravel],
            'Department': [Department],
            'DistanceFromHome': [DistanceFromHome],
            'Education': [Education],
            'EducationField': [EducationField],
            'Gender': [Gender],
            'MaritalStatus': [MaritalStatus],
            'NumCompaniesWorked': [NumCompaniesWorked],
            'TrainingTimesLastYear': [TrainingTimesLastYear],
            'YearsAtCompany': [YearsAtCompany]
        })

        # Hacer predicción
        prediction = model.predict(input_data)
        
        if prediction[0]==1:
            resp="SI"
        else:
            resp="N0"
        
        return jsonify({'Attrition': resp})
       

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=8000)
