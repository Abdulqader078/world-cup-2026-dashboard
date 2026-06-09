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

for match in matches:
    if match["homeTeam"]["name"] is not None:
        print(f'{match["homeTeam"]["name"]} vs {match["awayTeam"]["name"]}')
