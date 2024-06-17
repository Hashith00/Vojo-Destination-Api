from flask import request, jsonify
from flask import Flask
import requests

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def returnHello():
    return "Hello Flask Server"

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
    

GOOGLE_API_KEY = 'AIzaSyC8XOXvvxImxyxY6dFnOKIMTlbOM3X58Yw'

@app.route('/get_place_photo', methods=['GET'])
def get_place_photo():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    
    if not latitude or not longitude:
        return jsonify({'error': 'Missing latitude or longitude'}), 400
    
    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except ValueError:
        return jsonify({'error': 'Invalid latitude or longitude'}), 400

    # Step 1: Get Place ID
    nearby_search_url = (
        f'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
        f'?location={latitude},{longitude}&radius=500&key={GOOGLE_API_KEY}'
    )
    nearby_search_response = requests.get(nearby_search_url)
    nearby_search_data = nearby_search_response.json()
    
    if not nearby_search_data['results']:
        return jsonify({'error': 'No places found near the given location'}), 404

    place_id = nearby_search_data['results'][0]['place_id']

    # Step 2: Get Photos from Place ID
    place_details_url = (
        f'https://maps.googleapis.com/maps/api/place/details/json'
        f'?place_id={place_id}&fields=photos&key={GOOGLE_API_KEY}'
    )
    place_details_response = requests.get(place_details_url)
    place_details_data = place_details_response.json()

    if 'photos' not in place_details_data['result']:
        return jsonify({'error': 'No photos found for the place'}), 404

    photo_reference = place_details_data['result']['photos'][0]['photo_reference']

    # Step 3: Get the Photo using the Photo Reference
    photo_url = (
        f'https://maps.googleapis.com/maps/api/place/photo'
        f'?maxwidth=400&photoreference={photo_reference}&key={GOOGLE_API_KEY}'
    )

    return jsonify({'photo_url': photo_url})

if __name__ == "__main__":
    app.run()