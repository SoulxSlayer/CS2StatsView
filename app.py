from flask import Flask, request, Response, send_from_directory
from flask_cors import CORS # Handles CORS headers for you
import requests # To make HTTP requests to the Steam API

# Initialize Flask app
# static_folder='.' means Flask will look for static files (like your HTML) in the current directory.
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app) # Enable CORS for all routes on your Flask app.
          # This allows your HTML page (even if opened directly as a file or from another dev server)
          # to call your Flask proxy.

STEAM_API_BASE_URL = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/"
APP_ID = "730" # For CS:GO / CS2

# Route to serve your HTML file
@app.route('/')
def index():
    # Replace 'steam_viewer.html' if your HTML file has a different name
    return send_from_directory('.', 'steam_viewer.html')

# Route to act as a proxy for the Steam API
@app.route('/proxy_steam_stats')
def proxy_steam_stats():
    api_key = request.args.get('key')
    steam_id = request.args.get('steamid')

    if not api_key or not steam_id:
        # Return a JSON error response with a 400 Bad Request status
        return Response('{"error": "Missing API key or SteamID"}', status=400, mimetype='application/json')

    steam_api_url = f"{STEAM_API_BASE_URL}?appid={APP_ID}&key={api_key}&steamid={steam_id}"

    try:
        # Make the request to the Steam API
        steam_response = requests.get(steam_api_url, timeout=10) # Added a 10-second timeout

        # Forward Steam's response (content, status code, and content-type header)
        # to the client. This makes the proxy as transparent as possible.
        response_headers = {
            'Content-Type': steam_response.headers.get('Content-Type', 'application/json')
        }
        return Response(steam_response.content, status=steam_response.status_code, headers=response_headers)
        
    except requests.exceptions.Timeout:
        return Response('{"error": "Request to Steam API timed out"}', status=504, mimetype='application/json') # 504 Gateway Timeout
    except requests.exceptions.RequestException as e:
        # For other network-related errors during the request to Steam
        return Response(f'{{"error": "Failed to connect to Steam API", "details": "{str(e)}"}}', status=502, mimetype='application/json') # 502 Bad Gateway

if __name__ == '__main__':
    # Run the Flask development server
    # It will be accessible at http://localhost:5000
    app.run(debug=True, port=5000)