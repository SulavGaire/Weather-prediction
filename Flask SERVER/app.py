from flask import Flask, render_template, request
import pandas as pd
import joblib

app = Flask(__name__)

# Load the trained models
temp_model = joblib.load('temp_model.pkl')
humidity_model = joblib.load('rh_model.pkl')
pressure_model = joblib.load('press_model.pkl')

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    # Get the input values from the form
    hour = int(request.form['hour'])
    dayofweek = int(request.form['dayofweek'])
    month = int(request.form['month'])
    year = int(request.form['year'])
    quarter = int(request.form['quarter'])
    dayofyear = int(request.form['dayofyear'])
    dayofmonth = int(request.form['dayofmonth'])

    # Create a DataFrame with the input values
    data = pd.DataFrame({
        'Hour': [hour],
        'Dayofweek': [dayofweek],
        'Month': [month],
        'Year': [year],
        'Quarter': [quarter],
        'Dayofyear': [dayofyear],
        'Dayofmonth': [dayofmonth]
    })

    # Make predictions using the models
    temperature = temp_model.predict(data)[0]
    humidity = humidity_model.predict(data)[0]
    pressure = pressure_model.predict(data)[0]

    # Prepare the prediction results
    results = {
        'Temperature': temperature,
        'Humidity': humidity,
        'Pressure': pressure
    }

    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
