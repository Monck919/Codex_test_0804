# Codex_test_0804

A simple Flask application that fetches weather forecasts from Taiwan's Central Weather Bureau and displays them on a Bootstrap styled page.

## Setup

1. Create a `.env` file based on `.env.example` and fill in your `CWB_API_KEY`.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Open `http://localhost:5000` in your browser.

## Docker

Build and run with Docker:

```bash
docker build -t weather-app .
docker run -p 5000:5000 --env-file .env weather-app
```
