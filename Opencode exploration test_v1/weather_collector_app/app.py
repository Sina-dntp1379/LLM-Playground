from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import json
import urllib.parse

WTTR_URL = "https://wttr.in/{}?format=j1"

def get_weather(city_state):
    query = city_state.replace(" ", "+")
    url = WTTR_URL.format(query)
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            curr = data["current_condition"][0]
            area = data["nearest_area"][0]
            return {
                "location": f"{area['areaName'][0]['value']}, {area['region'][0]['value']}",
                "temp_f": curr["temp_F"],
                "temp_c": curr["temp_C"],
                "condition": curr["weatherDesc"][0]["value"],
                "humidity": curr["humidity"],
                "wind": curr["windspeedMiles"],
            }
    except Exception as e:
        return {"error": str(e)}

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather Collector</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; max-width: 600px; margin: 40px auto; padding: 0 20px; }}
        label {{ display: block; margin-top: 12px; font-weight: 600; }}
        input {{ width: 100%; padding: 8px; margin-top: 4px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; }}
        button {{ margin-top: 18px; padding: 10px 24px; background: #007bff; color: #fff; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; }}
        button:hover {{ background: #0056b3; }}
        .result {{ margin-top: 24px; padding: 16px; border-radius: 8px; }}
        .result.success {{ background: #d4edda; border: 1px solid #c3e6cb; }}
        .result.error {{ background: #f8d7da; border: 1px solid #f5c6cb; }}
        .temp {{ font-size: 32px; font-weight: bold; }}
        .meta {{ margin-top: 8px; color: #555; }}
    </style>
</head>
<body>
    <h1>Weather Collector</h1>
    <form method="POST">
        <label for="city">City</label>
        <input type="text" id="city" name="city" placeholder="e.g. Ames" required>
        <label for="state">State / Region</label>
        <input type="text" id="state" name="state" placeholder="e.g. Iowa" required>
        <label for="datetime">Date & Time</label>
        <input type="text" id="datetime" name="datetime" placeholder="e.g. 2/20/2017  9:07:00 PM">
        <button type="submit">Get Temperature</button>
    </form>
    {result_html}
</body>
</html>"""

RESULT_SUCCESS = """<div class="result success">
    <div><strong>{query}</strong></div>
    <div class="temp">{temp_f}°F / {temp_c}°C</div>
    <div>{condition}</div>
    <div class="meta">Humidity: {humidity}% | Wind: {wind} mph{datetime_html}</div>
</div>"""

RESULT_ERROR = """<div class="result error"><strong>Error:</strong> {error}</div>"""

class WeatherHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(HTML.format(result_html="").encode())

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode()
        params = urllib.parse.parse_qs(body)
        city = params.get("city", [""])[0].strip()
        state = params.get("state", [""])[0].strip()
        dt = params.get("datetime", [""])[0].strip()

        if not city or not state:
            result_html = RESULT_ERROR.format(error="Please enter both city and state.")
        else:
            city_state = f"{city}, {state}"
            weather = get_weather(city_state)
            if "error" in weather:
                result_html = RESULT_ERROR.format(error=weather["error"])
            else:
                dt_html = f" | Recorded: {dt}" if dt else ""
                result_html = RESULT_SUCCESS.format(
                    query=weather["location"],
                    temp_f=weather["temp_f"],
                    temp_c=weather["temp_c"],
                    condition=weather["condition"],
                    humidity=weather["humidity"],
                    wind=weather["wind"],
                    datetime_html=dt_html,
                )

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(HTML.format(result_html=result_html).encode())

if __name__ == "__main__":
    port = 5000
    print(f"Server running at http://localhost:{port}")
    HTTPServer(("0.0.0.0", port), WeatherHandler).serve_forever()
