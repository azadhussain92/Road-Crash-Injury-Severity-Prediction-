from flask import Flask, render_template, request, jsonify
import requests
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
import mysql.connector
from mysql.connector import Error
import random
import traceback

app = Flask(__name__)

DB_CONFIG = {
    'host': 'localhost',
    'database': 'crash_prediction',
    'user': 'root',
    'password': 'root' 
}

def connect_to_database():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
    return None

def save_crash_data(data, prediction):
    conn = connect_to_database()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS crash_records (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date_of_crash DATE,
                time_of_crash TIME,
                day_of_week VARCHAR(20),
                weather_condition VARCHAR(50),
                light_condition VARCHAR(20),
                road_surface_condition VARCHAR(50),
                speed_limit INT,
                crash_type VARCHAR(50),
                road_type VARCHAR(50),
                driver_age INT,
                driver_gender VARCHAR(20),
                seatbelt_used BOOLEAN,
                alcohol_involved BOOLEAN,
                location VARCHAR(255),
                latitude DECIMAL(10, 6),
                longitude DECIMAL(10, 6),
                severity_prediction VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        query = '''
            INSERT INTO crash_records (
                date_of_crash, time_of_crash, day_of_week, weather_condition,
                light_condition, road_surface_condition, speed_limit, crash_type,
                road_type, driver_age, driver_gender, seatbelt_used, alcohol_involved,
                location, latitude, longitude, severity_prediction
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        
        seatbelt_used = True if data.get('seatbelt_used') == 'on' else False
        alcohol_involved = True if data.get('alcohol_involved') == 'on' else False
        
        date_of_crash = None
        if data.get('date_of_crash'):
            try:
                date_of_crash = datetime.strptime(data.get('date_of_crash', ""), '%Y-%m-%d').date()
            except Exception as e:
                pass
                
        speed_limit = int(data.get('speed_limit')) if data.get('speed_limit') else 0
        driver_age = int(data.get('driver_age')) if data.get('driver_age') else 0
        
        # latitude = float(data.get('latitude')) if data.get('latitude') else None
        # longitude = float(data.get('longitude')) if data.get('longitude') else None
        try:
            latitude = float(data.get('latitude'))
        except (TypeError, ValueError):
            latitude = None
            
        try:
            longitude = float(data.get('longitude'))
        except (TypeError, ValueError):
            longitude = None

        values = (
            date_of_crash, data.get('time_of_crash'),
            data.get('day_of_week'),
            data.get('weather_condition'),
            data.get('light_condition'),
            data.get('road_surface_condition'),
            speed_limit, data.get('crash_type'),
            data.get('road_type'),
            driver_age, data.get('driver_gender'),
            seatbelt_used, alcohol_involved, data.get('location'),
            latitude, longitude, prediction
        )
        
        cursor.execute(query, values)
        conn.commit()
        return True
    except Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def create_model():
    return RandomForestClassifier(n_estimators=100, random_state=42)
model = create_model()
shared_results = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        is_api_call = request.headers.get('Content-Type') == 'application/json'
        data = request.get_json() if is_api_call else request.form.to_dict()
        required_fields = ['time_of_crash', 'day_of_week', 'weather_condition', 'light_condition']
        for field in required_fields:
            if field not in data or not data[field]:
                if is_api_call:
                    return jsonify({'error': f'Missing required field: {field}'}), 400
                return render_template('error.html', error_message=f'Missing required field: {field}')
        severity_options = ['No Injury or Minor Injury', 'Serious Injury', 'Fatal Injury']
        severity = severity_options[random.randint(0, 2)] 
        
        suggestions = {
            'No Injury or Minor Injury': 'Standard medical check-up recommended as a precaution.',
            'Serious Injury': 'Immediate medical attention required. Call emergency services.',
            'Fatal Injury': 'Emergency services required immediately. Secure the area and assist if possible.'
        }
        suggestion = suggestions.get(severity, 'Please seek appropriate medical assistance.')
        save_crash_data(data, severity)
        share_id = "".join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=10))
        
        if is_api_call:
            return jsonify({'severity': severity, 'suggestion': suggestion, 'share_id': share_id})
        return render_template('result.html', severity=severity, suggestion=suggestion, form_data=data, share_id=share_id)
        
    except Exception as e:
        traceback.print_exc()
        if is_api_call:
            return jsonify({'error': str(e)}), 500
        return render_template('error.html', error_message=str(e))

@app.route('/get_sun_data', methods=['POST'])
def get_sun_data():
    try:
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        url = f"https://api.sunrise-sunset.org/json?lat={latitude}&lng={longitude}&formatted=0"
        response = requests.get(url)
        sun_data = response.json()
        
        if sun_data.get('status') != 'OK':
            return jsonify({'error': 'Failed to fetch sunrise/sunset data'}), 500
            
        results = sun_data.get('results', {})
        sunrise = results.get('sunrise')
        sunset = results.get('sunset')
        
        light_condition = "unknown"
        crash_time = data.get('time_of_crash')
        if crash_time and sunrise and sunset:
            sunrise_time = datetime.fromisoformat(sunrise.replace('Z', '+00:00'))
            sunset_time = datetime.fromisoformat(sunset.replace('Z', '+00:00'))
            crash_hour, crash_minute = map(int, crash_time.split(':'))
            crash_obj = datetime.now().replace(hour=crash_hour, minute=crash_minute).time()
            
            if sunrise_time.time() <= crash_obj <= sunset_time.time():
                light_condition = "light"
            else:
                light_condition = "dark"
                
        return jsonify({
            'sunrise': sunrise_time.strftime('%I:%M %p') if sunrise else None,
            'sunset': sunset_time.strftime('%I:%M %p') if sunset else None,
            'light_condition': light_condition
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history')
def history():
    try:
        conn = connect_to_database()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM crash_records ORDER BY created_at DESC")
        records = cursor.fetchall()
        return render_template('history.html', records=records)
    except Exception as e:
        return render_template('error.html', error_message=str(e))
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)
