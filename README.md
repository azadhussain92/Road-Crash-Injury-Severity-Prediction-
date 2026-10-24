# 🚗 Road Crash Injury Severity Prediction System

## 📌 Project Overview

The Road Crash Injury Severity Prediction System is a web-based application designed to estimate road crash injury severity using information about road conditions, weather, driver details, and crash circumstances.

The system categorizes predicted injury severity into three classes: **Minor, Serious, and Fatal**. It provides a user-friendly interface for entering crash details, selecting a location on an interactive map, viewing prediction results, and reviewing previous records.

## ✨ Features

- **Modern UI:** Responsive interface with glassmorphism styling.
- **Interactive Map:** Select crash locations using Leaflet.js.
- **GPS Location:** Retrieve the user's current coordinates with permission.
- **Reverse Geocoding:** Convert geographic coordinates into a readable address using OpenStreetMap Nominatim.
- **Severity Prediction:** Display the predicted injury severity based on the application's configured prediction logic.
- **Prediction Dashboard:** Present prediction results and safety recommendations.
- **Crash History:** Store and view previous prediction records using MySQL.
- **Lighting Conditions:** Determine light conditions using available crash time and location data.
- **Database Integration:** Maintain crash details and prediction history.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| MySQL | Database management |
| HTML5 | Web page structure |
| CSS3 | Styling and responsive UI |
| JavaScript | Frontend interactions |
| Leaflet.js | Interactive maps |
| OpenStreetMap Nominatim API | Reverse geocoding |

### System Architecture Components

**1. User Input**

The user enters crash details, including date, time, weather, road conditions, speed limit, driver information, and crash location.

**2. Location Services**

Leaflet.js allows the user to select a crash location on the map. GPS coordinates and reverse geocoding provide location information when supported and permitted.

**3. Flask Backend**

Flask receives the submitted information, validates the inputs, processes the data, and executes the configured prediction logic.

**4. Injury Severity Prediction**

The prediction component estimates the severity category: Minor, Serious, or Fatal. The actual model and prediction method depend on the implementation.

**5. MySQL Database**

The application stores crash information and prediction history in the `crash_prediction` database.

**6. Results Dashboard**

The application displays the prediction result, relevant details, and available safety recommendations. Users can also review previous records.

## 🔄 System Workflow

```text
        User Opens Web Application
                   |
                   v
         Enter Crash Information
                   |
                   v
        Select Crash Location
          (Leaflet.js / GPS)
                   |
                   v
         Reverse Geocoding
       (OpenStreetMap Nominatim)
                   |
                   v
          Flask Backend
                   |
                   v
        Validate Input Data
                   |
                   v
       Injury Severity Prediction
                   |
                   v
       Minor / Serious / Fatal
                   |
                   v
        Save Record to MySQL
                   |
                   v
         Display Result Dashboard
                   |
                   v
          View Crash History
```

## 📋 Prerequisites

Install the following before running the project:

- [Python 3.x](https://www.python.org/downloads/)
- [MySQL Server](https://dev.mysql.com/downloads/mysql/)
- [MySQL Workbench](https://dev.mysql.com/downloads/workbench/)
- pip package manager
- A modern web browser

## 🚀 Installation and Setup

Install the required packages:

```bash
pip install Flask mysql-connector-python
```

If your project uses additional libraries, install them and include them in `requirements.txt`.

### 4. Configure the MySQL Database

Open MySQL Workbench and execute:

```sql
CREATE DATABASE crash_prediction;
USE crash_prediction;

CREATE TABLE crash_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date_of_crash DATE,
    time_of_crash TIME,
    day_of_week VARCHAR(20),
    weather_condition VARCHAR(50),
    light_condition VARCHAR(50),
    road_surface_condition VARCHAR(50),
    speed_limit INT,
    crash_type VARCHAR(50),
    road_type VARCHAR(50),
    driver_age INT,
    driver_gender VARCHAR(20),
    seatbelt_used VARCHAR(10),
    alcohol_involved VARCHAR(10),
    location VARCHAR(255),
    latitude FLOAT,
    longitude FLOAT,
    severity_prediction VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Make sure the table columns match the SQL queries in your Flask application.

### 5. Configure Database Credentials

Update the database configuration in `app.py`:

```python
DB_CONFIG = {
    "host": "localhost",
    "database": "crash_prediction",
    "user": "root",
    "password": "YOUR_MYSQL_PASSWORD"
}
```

Replace the placeholder with your local MySQL password. For better security, use environment variables rather than hardcoding credentials.

### 6. Run the Application

```bash
python app.py
```

Open your browser and visit:

http://127.0.0.1:5000/

## 📂 Project Structure

```text
road-crash-prediction/
│
├── app.py
├── requirements.txt
├── README.md
│
├── static/
│   └── css/
│       └── style.css
│
├── templates/
│   ├── index.html
│   ├── result.html
│   ├── history.html
│   └── error.html
```

*The structure above is a suggested layout. Keep your actual filenames and folders consistent with your code.*

## 📊 Prediction Output

The application is designed to display one of the following severity categories:

- **Minor:** The predicted injury severity is minor.
- **Serious:** The predicted injury severity is serious.
- **Fatal:** The predicted injury severity is fatal.

Actual output depends on the prediction logic, model, and input data implemented in the application.

## 🔮 Future Enhancements

- Integrate and document a validated machine learning classification model.
- Add charts to analyze historical crash records.
- Improve data validation and error handling.
- Add user authentication and role-based access.
- Build additional reports to explore crash patterns.
- Improve model evaluation using appropriate classification metrics.
