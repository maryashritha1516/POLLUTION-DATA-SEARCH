from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

# Replace with your OpenWeather API key
API_KEY = 'ca36cd94ca163491b30c6ca720509260'

def get_coordinates_by_city(city):
    """
    Fetch latitude and longitude for a city.
    """
    try:
        geo_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
        response = requests.get(geo_url)
        if response.status_code == 200:
            data = response.json()
            return data['coord']['lat'], data['coord']['lon']
        else:
            return None, None
    except:
        return None, None

def get_pollution_data(lat, lon):
    """
    Fetch pollution data for given coordinates.
    """
    try:
        pollution_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
        response = requests.get(pollution_url)
        if response.status_code == 200:
            data = response.json()
            return data['list'][0]
        else:
            return None
    except:
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_pollution', methods=['POST'])
def get_pollution():
    input_type = request.form.get('input_type')
    if input_type == 'city':
        city = request.form.get('city')
        lat, lon = get_coordinates_by_city(city)
        if lat is None or lon is None:
            return jsonify({'error': 'City not found'})
    else:
        try:
            lat = float(request.form.get('latitude'))
            lon = float(request.form.get('longitude'))
        except ValueError:
            return jsonify({'error': 'Invalid coordinates'})

    pollution_data = get_pollution_data(lat, lon)
    if pollution_data:
        return jsonify(pollution_data)
    else:
        return jsonify({'error': 'Could not fetch pollution data'})

if __name__ == '__main__':
    app.run(debug=True)
