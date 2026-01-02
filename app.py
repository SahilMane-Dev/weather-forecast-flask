from flask import Flask, render_template , request
import requests as req

app = Flask(__name__)



@app.route("/")
def home():
    return render_template("home.html" , weather=None)


@app.route("/get_weather" , methods=["GET" ,"POST"])
def get_weather():
    if request.method == "POST":
        city = request.form['city']

        geo_url = req.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1")

        geo_data = geo_url.json()

        if "results" not in geo_data:
            return render_template("home.html" , weather={"city" :"City not found !"})
        
        lat = geo_data["results"][0]["latitude"]
        lon = geo_data['results'][0]['longitude']
        city_name = geo_data['results'][0]['name']

        weather_url = req.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true")
        weather_data = weather_url.json()

        temp = weather_data["current_weather"]["temperature"]
        wind = weather_data['current_weather']['windspeed']
        code = weather_data['current_weather']['weathercode']

        condition_map = {
            0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Fog", 48: "Depositing rime fog", 51: "Drizzle: Light", 53: "Drizzle: Moderate",
            55: "Drizzle: Dense", 61: "Rain: Slight", 63: "Rain: Moderate", 65: "Rain: Heavy",
            71: "Snow fall: Slight", 73: "Snow fall: Moderate", 75: "Snow fall: Heavy",
            80: "Rain showers: Slight", 81: "Rain showers: Moderate", 82: "Rain showers: Violent"
        }

        condition = condition_map.get(code , "unknown")

        weather = {
            "city" : city_name,
            "temp" : temp,
            "wind" : wind,
            "condition" : condition
        }

        return render_template('home.html' , weather = weather)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
