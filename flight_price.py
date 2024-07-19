import requests
from datetime import date, timedelta
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from dotenv import load_dotenv
import os

load_dotenv(".env")

API_KEY = os.environ.get('SKYSCANNER_API_KEY')

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set all CORS enabled origins
origins = [
    "http://localhost:5173",
    "https://flights.andreo.dev"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tomorrow = date.today() + timedelta(days=1)
week_after_tomorrow = tomorrow + timedelta(days=7)

# Formatting both dates into the desired string format
tomorrow_dmy = tomorrow.strftime('%d-%m-%Y')
week_after_tomorrow_dmy = week_after_tomorrow.strftime('%d-%m-%Y')

def get_flight_data():


    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/search-everywhere"

    querystring = {
        "fromId": "eyJzIjoiQlJVIiwiZSI6Ijk1NTY1MDM2IiwiaCI6IjI3NTM5NTY1In0=",
        "departDate": tomorrow.isoformat(),  # Format the date as a string
        "returnDate": week_after_tomorrow.isoformat(),  # Format the date as a string
        "adults": "1",
        "cabinClass": "economy",
        "currency": "EUR",
        "market": "BE",
        "locale": "nl-NL"
    }

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "skyscanner80.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code != 200:
        logger.error(f"Failed to fetch flight data: {response.status_code}, {response.text}")
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch flight data")

    return response.json()

@app.get("/flights")
def read_flight_data():
    try:
        flight_data = get_flight_data()
        flight_data['departureDate'] = tomorrow_dmy
        flight_data['returnDate'] = week_after_tomorrow_dmy
        return flight_data
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

