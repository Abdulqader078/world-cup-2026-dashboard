import requests
import urllib3
import ssl
from dotenv import load_dotenv
import os

ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

api_key = os.getenv("API_KEY")

url = "https://api.football-data.org/v4/competitions/WC/matches?season=2026"

headers ={"X-Auth-Token": api_key}

response = requests.get(url, headers=headers, verify=False)

data = response.json()
matches = data["matches"]

months = {
    '01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr',
    '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Aug',
    '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'
}

for match in matches:
    if match["homeTeam"]["name"] is not None:
        date =  match["utcDate"].split("T")[0]
        parts = date.split("-")
        day = parts[2]
        month = months[parts[1]]
        print(f'{day} {month} | {match["homeTeam"]["name"]} vs {match["awayTeam"]["name"]}')
