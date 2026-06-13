from flask import Flask, render_template
import requests
import urllib3
import ssl
from dotenv import load_dotenv
import os


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
    for match in matches:
        if match["homeTeam"]["name"] is not None:
                if match["status"] == "FINISHED":
                    print(match["homeTeam"]["name"], match["score"]["fullTime"])
        date_parts = match["utcDate"].split("T")[0].split("-")
        formatted_date = f'{date_parts[2]} {months[date_parts[1]]}'
        fixtures.append({
                "date": formatted_date,
                "home": match["homeTeam"]["name"],
                "away": match["awayTeam"]["name"],
                "status": "Upcoming" if match["status"] == "TIMED" else match["status"],
                "home_score":match["score"]["fullTime"]["home"],
                "away_score":match["score"]["fullTime"]["away"]
            })

    return render_template('index.html', fixtures=fixtures)
if __name__ == '__main__':
    app.run(debug=True)