# Steam CS (appid: 730) Stats Viewer

A web application to view your Counter-Strike (Global Offensive / CS2 - appid 730) game statistics using the Steam Web API. This application uses a Python Flask backend to proxy requests to the Steam API, bypassing browser CORS restrictions.

![{126DA0DA-9AD5-4EF5-BAD4-3C8E098FD0E1}](https://github.com/user-attachments/assets/d659cf62-7c82-4ed7-ab7a-d99b54630851)


## Features

*   Fetches and displays player game statistics for Counter-Strike (appid: 730).
*   Shows:
    *   Player Information (SteamID, Game Name)
    *   Overall Stats (K/D, Wins, Playtime, Accuracy, etc.)
    *   Last Match Stats
    *   Detailed Weapon Stats (Kills, Shots, Hits, Accuracy per weapon)
    *   Map-specific Stats (Wins, Rounds, Win Rate per map)
    *   Miscellaneous Stats
    *   Earned Achievements
    *   GI Lesson Stats
*   Stores API Key and Steam64 ID in browser `localStorage` for convenience.
*   Responsive design with a Steam-like theme.
*   Includes Docker support for easy deployment.

## Technology Stack

*   **Frontend:** HTML, CSS, Vanilla JavaScript
*   **Backend (Proxy):** Python 3, Flask, Requests, Flask-CORS
*   **API:** Steam Web API (`ISteamUserStats/GetUserStatsForGame`)

## Prerequisites

### For Manual Setup:
*   Python 3.7+
*   pip (Python package installer)
*   A Steam Web API Key (Get one [here](https://steamcommunity.com/dev/apikey))
*   Your Steam64 ID (You can find it using sites like [SteamID.io](https://steamid.io/))
*   A modern web browser

### For Docker Setup:
*   Docker installed and running.
*   A Steam Web API Key.
*   Your Steam64 ID.

## Setup and Running

### 1. Manual Setup (Local Development)

1.  **Clone the repository (or create the files):**
    ```bash
    git clone https://github.com/SoulxSlayer/CS2StatsView/
    cd CS2StatsView
    ```
    If you don't have a repo, ensure you have `app.py`, `steam_viewer.html` (or your HTML file name), and `requirements.txt` in the same directory.

2.  **Create `requirements.txt` file with the following content:**
    ```txt
    Flask
    requests
    Flask-CORS
    ```

3.  **Create a virtual environment (recommended) and activate it:**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the Flask application:**
    The `app.py` file contains the Flask server.
    ```bash
    python app.py
    ```
    By default, it will run on `http://localhost:5000`.

6.  **Access the application:**
    Open your web browser and navigate to `http://localhost:5000`.

### 2. Docker Setup

1.  **Ensure you have the following files in your project root:**
    *   `app.py` (your Flask backend)
    *   `steam_viewer.html` (or your HTML file name, ensure it's correctly referenced in `app.py`)
    *   `requirements.txt` (as defined above)
    *   `Dockerfile` (see content below)
    *   `.dockerignore` (optional, but good practice - see content below)

2.  **Create a `Dockerfile` with the following content:**
    ```dockerfile
    # Use an official Python runtime as a parent image
    FROM python:3.9-slim

    # Set the working directory in the container
    WORKDIR /app

    # Copy the dependencies file to the working directory
    COPY requirements.txt .

    # Install any needed packages specified in requirements.txt
    # --no-cache-dir reduces image size
    RUN pip install --no-cache-dir -r requirements.txt

    # Copy the rest of the application code to the working directory
    COPY . .

    # Make port 5000 available to the world outside this container
    EXPOSE 5000

    # Define environment variable (optional, if you want to configure Flask host/port)
    # ENV FLASK_APP app.py
    # ENV FLASK_RUN_HOST 0.0.0.0

    # Run app.py when the container launches
    # Use "gunicorn" for a more production-ready setup if desired,
    # but for simplicity, Flask's dev server is fine here.
    CMD ["python", "app.py"]
    ```
    *Note: Ensure your `app.py` runs on `host='0.0.0.0'` if you want it accessible outside the Docker container's internal network. The provided `app.py` with `app.run(debug=True, port=5000)` should work, but for production, `app.run(host='0.0.0.0', port=5000)` is more explicit.* The current `app.py` should be fine.

3.  **Create a `.dockerignore` file (optional, but recommended):**
    This file tells Docker which files/folders to ignore when building the image, reducing build time and image size.
    ```
    __pycache__/
    *.pyc
    *.pyo
    *.pyd
    .Python
    env/
    venv/
    .env
    .git
    .gitignore
    README.md
    ```

4.  **Build the Docker image:**
    Open your terminal in the project root directory (where the `Dockerfile` is) and run:
    ```bash
    docker build -t steam-cs-stats-viewer .
    ```
    You can replace `steam-cs-stats-viewer` with your preferred image name.

5.  **Run the Docker container:**
    ```bash
    docker run -p 5000:5000 steam-cs-stats-viewer
    ```
    *   `-p 5000:5000`: Maps port 5000 of your host machine to port 5000 of the container.
    *   If you want to run it in detached mode (in the background): `docker run -d -p 5000:5000 steam-cs-stats-viewer`

6.  **Access the application:**
    Open your web browser and navigate to `http://localhost:5000`.

## Usage

1.  Open the application in your browser.
2.  Enter your **Steam Web API Key** in the first input field.
3.  Enter the **Steam64 ID** of the user whose stats you want to view in the second input field.
4.  Click the "Fetch Stats" button.
5.  The stats will be displayed below. Your API key and Steam64 ID will be saved in your browser's `localStorage` for future visits.

## Important Notes & Limitations

*   **CORS Proxy:** The Steam Web API does not provide CORS headers, which prevents direct calls from client-side JavaScript. This application uses a Python Flask server (`app.py`) as a proxy to make requests to the Steam API on behalf of the client.
*   **API Key Security:**
    *   The API key is entered by the user and stored in `localStorage`.
    *   When fetching stats, the key is sent from the client to your Flask proxy. The proxy then uses this key to call the Steam API.
    *   **This setup is suitable for personal use or development.** For a public-facing application, you would ideally not want the API key to ever leave a secure server environment or be transmitted from the client.
*   **Steam API Rate Limits:** Be mindful of Steam API rate limits. Excessive requests might lead to temporary blocking.
*   **Private Profiles:** Stats for users with private Steam profiles or private game details will not be accessible. The API will usually return an error or empty data.
*   **AppID:** This viewer is hardcoded for CS (appid: 730). To view stats for other games, the `appid` in `app.py` and potentially the HTML title would need to be changed, and stat parsing logic might need adjustments.

## File Structure

```
/
├── app.py              # Flask backend proxy
├── steam_viewer.html   # Frontend HTML, CSS, JS (or your HTML file name)
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration
├── .dockerignore       # Files to ignore for Docker build
└── README.md           # This file
```

## Contributing

Contributions are welcome! If you have suggestions or improvements, feel free to:
1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.

## License

This project is open-source. Feel free to use and modify it. If you plan to deploy it publicly, be mindful of Steam API Terms of Service and API key security best practices.
