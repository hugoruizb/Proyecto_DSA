
# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, jsonify
import joblib
import traceback
import pandas as pd
from sklearn.compose import ColumnTransformer

#import re


app = Flask(__name__)

model = joblib.load('./model_attrition.joblib')


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')



@app.route('/predict', methods=['POST'])
def predict():
    try:                              
        age=request.form.get('age', type=float)
        BusinessTravel=request.form.get('BusinessTravel', type=float)
        DailyRate=request.form.get('DailyRate', type=float)
        Department=request.form.get('Department', type=float)
           
        try:
            age = int(age)
            BusinessTravel=int(BusinessTravel)
            DailyRate=int(DailyRate)
            Department=int(Department)
            
        except (ValueError, TypeError):
            return jsonify({'error': 'Age y DailyRate deben ser números enteros válidos.'}), 400

                 
        input_data = pd.DataFrame({            
            'age':[age],
            'BusinessTravel':[BusinessTravel],
            'DailyRate':[DailyRate],
            'Department':[Department]})
                            
        X = input_data
                      
        prediction=model.predict(X)
        
        cols = ['Attrition']
        
        res = pd.DataFrame(prediction, columns=cols)       
        res = res.loc[:, (res != 0).all(axis=0)]
        
        table_html = res.to_html(classes='table table-striped', index=False)

        return jsonify({'Attrition': int(prediction)})
        #return render_template('table2.html', table_html=table_html)
        
                
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=8000)
