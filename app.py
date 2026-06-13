from flask import Flask, render_template
import requests
import urllib3
import ssl
from dotenv import load_dotenv
import os
from datetime import date


app = Flask(__name__)


ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()
api_key = os.getenv("API_KEY")

@app.route('/')
def index():
    url = "https://api.football-data.org/v4/competitions/WC/matches?season=2026"
    headers = {"X-Auth-Token": api_key}
    response = requests.get(url, headers=headers, verify=False)
    data = response.json()
    matches = data["matches"]
    months = {
    "01": "Jan",
    "02": "Feb",
    "03": "Mar",
    "04": "Apr",
    "05": "May",
    "06": "Jun",
    "07": "Jul",
    "08": "Aug",
    "09": "Sep",
    "10": "Oct",
    "11": "Nov",
    "12": "Dec",
    }
    fixtures = []
    today_str = str(date.today())
    for match in matches:
        if match["homeTeam"]["name"] is not None:
            match_date = match["utcDate"].split("T")[0]
            date_parts = match["utcDate"].split("T")[0].split("-")
            formatted_date = f'{date_parts[2]} {months[date_parts[1]]}'
            raw_time = match["utcDate"].split("T")[1].split("Z")[0][:5]
            hour = int(raw_time.split(":")[0]) + 1
            minute = raw_time.split(":")[1]
            corrected_time = f'{hour:02d}:{minute}'
            fixtures.append({
                "date": formatted_date,
                "home": match["homeTeam"]["name"],
                "away": match["awayTeam"]["name"],
                "status": "Upcoming" if match["status"] == "TIMED" else match["status"],
                "home_score":match["score"]["fullTime"]["home"],
                "away_score":match["score"]["fullTime"]["away"],
                "is_today": match_date == today_str,
                "time": corrected_time,
                "home_crest": match["homeTeam"]["crest"],
                "away_crest": match["awayTeam"]["crest"]
            })

    return render_template('index.html', fixtures=fixtures)
if __name__ == '__main__':
    app.run(debug=True)