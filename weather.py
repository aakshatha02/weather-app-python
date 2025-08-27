import tkinter as tk
from tkinter import messagebox
import requests
from geopy.geocoders import Nominatim
import datetime

# -----------------------------
# Function to fetch weather data
# -----------------------------

def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return
    
    try:
        # Get latitude and longitude using geopy
        geolocator = Nominatim(user_agent="weather_app")
        location = geolocator.geocode(city)
        
        if location is None:
            messagebox.showerror("Error", f"City not found: {city}")
            return
        
        latitude = location.latitude
        longitude = location.longitude
        
        # Call Open-Meteo API
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
        response = requests.get(url)
        data = response.json()
        
        if "current_weather" not in data:
            messagebox.showerror("Error", "Weather data not available.")
            return
        
        weather = data["current_weather"]
        temp = weather["temperature"]
        windspeed = weather["windspeed"]
        weather_code = weather["weathercode"]
        today = datetime.datetime.now()

        # Display results
        result_label.config(
            text=f"City: {city.title()}\n"
                 f"Temperature: {temp}°C\n"
                 f"Wind Speed: {windspeed} km/h\n"
                 f"Weather Code: {weather_code}\n"
                 f"Date: {today}"
        )
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get data: {e}")

# -----------------------------
# GUI Setup
# -----------------------------
root = tk.Tk()
root.title("Weather App - Open-Meteo")
root.geometry("400x250")
root.resizable(False, False)

# Title Label
title_label = tk.Label(root, text="Weather App", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

# City Entry
city_entry = tk.Entry(root, font=("Helvetica", 14))
city_entry.pack(pady=10)
city_entry.insert(0, "Enter city name")

# Get Weather Button
get_weather_btn = tk.Button(root, text="Get Weather", font=("Helvetica", 12), command=get_weather)
get_weather_btn.pack(pady=5)

# Result Label
result_label = tk.Label(root, text="", font=("Helvetica", 12), justify="left")
result_label.pack(pady=10)

# Run the app
root.mainloop()
