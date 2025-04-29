from flask import Flask, render_template, request
import joblib
import numpy as np
import pandas as pd
import os

app = Flask(__name__)

# Model paths and CO2 mitigation factors
models = {
    "solar": {"file": "models/solar.pkl", "factor": 1.527},
    "wind": {"file": "models/wind.pkl", "factor": 1.569},
    "biomass": {"file": "models/biomass.pkl", "factor": 1.555},
    "hydro": {"file": "models/hydro.pkl", "factor": 1.556},
}

# Landing Page
@app.route('/')
def landing():
    return render_template('landing.html')

# Green Calculator Page
@app.route('/calculator')
def calculator():
    return render_template('index.html')
#About Page
@app.route('/about')
def about():
    return render_template('about.html')
#Factfile Page
@app.route('/facts')
def facts():
    return render_template('facts.html')

# Prediction Route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        energy_type = request.form['energy_type']

        if energy_type == 'solar':
            avg_temp = float(request.form['avg_temp_solar'])
            avg_irradiance = float(request.form['avg_irradiance'])
            peak_capacity = float(request.form['peak_capacity_solar'])
            state = request.form['state_solar']

            state_columns = ['State_Madhya Pradesh', 'State_Maharashtra', 'State_Rajasthan', 'State_Uttarakhand']
            state_vector = [1 if state == col.split('_')[1] else 0 for col in state_columns]

            input_data = np.array([[avg_temp, avg_irradiance, peak_capacity] + state_vector])

        elif energy_type == 'wind':
            wind_speed = float(request.form['wind_speed'])
            air_density = float(request.form['air_density'])
            temperature = float(request.form['temperature_wind'])
            pressure = float(request.form['pressure'])
            humidity = float(request.form['humidity'])
            installed_capacity = float(request.form['installed_capacity'])
            state = request.form['state_wind']

            state_columns = ['State_Karnataka', 'State_Maharashtra', 'State_Rajasthan', 'State_Tamil Nadu']
            state_vector = [1 if state == col.split('_')[1] else 0 for col in state_columns]

            input_data = np.array([[wind_speed, air_density, temperature, pressure, humidity, installed_capacity] + state_vector])

        elif energy_type == 'biomass':
            peak_capacity = float(request.form['peak_capacity_biomass'])
            feedstock = request.form['feedstock_type']
            moisture = float(request.form['moisture_content'])
            calorific = float(request.form['calorific_value'])
            quantity = float(request.form['feedstock_quantity'])

            input_data = pd.DataFrame([{
                'Peak Capacity (MW)': peak_capacity,
                'Type of Feedstock': feedstock,
                'Moisture Content (%)': moisture,
                'Calorific Value (kcal/kg)': calorific,
                'Feedstock Quantity Used (Tonnes/day)': quantity
            }])

        elif energy_type == 'hydro':
            head_height = float(request.form['head_height'])
            flow_rate = float(request.form['flow_rate'])
            turbine_eff = float(request.form['turbine_efficiency'])
            peak_capacity = float(request.form['peak_capacity_hydro'])
            scale = request.form['scale']

            flow_head = flow_rate * head_height
            capacity_eff = peak_capacity * turbine_eff

            input_dict = {
                'Peak Capacity (MW)': [peak_capacity],
                'Flow Rate (m³/s)': [flow_rate],
                'Head Height (m)': [head_height],
                'Turbine Efficiency (%)': [turbine_eff],
                'Flow_Head': [flow_head],
                'Capacity_Eff': [capacity_eff],
                'Scale': [scale]
            }

            input_data = pd.DataFrame(input_dict)

        else:
            return render_template("error.html", message="Invalid energy type selected.")

        model_path = models[energy_type]['file']
        co2_factor = models[energy_type]['factor']

        if not os.path.exists(model_path):
            return render_template("error.html", message=f"Model file not found for {energy_type}")

        model = joblib.load(model_path)

        prediction = model.predict(input_data)[0]
        co2_mitigated = prediction * co2_factor
        carbon_credits = co2_mitigated

        return render_template(
            'result.html',
            energy_type=energy_type.capitalize(),
            prediction=round(prediction, 2),
            co2_mitigated=round(co2_mitigated, 2),
            carbon_credits=round(carbon_credits, 2)
        )

    except Exception as e:
        return render_template("error.html", message=f"Error occurred: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
