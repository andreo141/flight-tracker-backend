import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.environ.get("SKYSCANNER_API_KEY")


url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/auto-complete"

querystring = {"query":"Brussels International","market":"EU","locale":"nl-NL"}

headers = {
    "X-Rapidapi-Key": API_KEY,
    "X-Rapidapi-Host": "skyscanner80.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())
