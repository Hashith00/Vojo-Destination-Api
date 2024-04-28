from flask import request, jsonify
from flask import Flask
import requests

app = Flask(__name__)

@app.route('/api', methods = ['GET'])
def returnasci():
    d = {}
    input_value  = str(request.args['query'])
    answer = str(ord(input_value))
    d['output'] = answer
    return d

@app.route('/places', methods=['GET'])
def get_nearby_places():
    try:
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')
        radius = request.args.get('radius')
        api_key = "AIzaSyC8XOXvvxImxyxY6dFnOKIMTlbOM3X58Yw"  # Replace with your API key

        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius={radius}&type=tourist_attraction&key={api_key}"
        
        response = requests.get(url)
        data = response.json()
        print(data)

        return jsonify(data)

    except Exception as e:
        print("Error fetching nearby places:", e)
        return jsonify({'error': 'Internal Server Error'}), 500


if __name__ == "__main__":
    app.run()