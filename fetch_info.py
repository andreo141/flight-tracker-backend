import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from dotenv import load_dotenv
import os

load_dotenv('.env')

API_KEY = os.environ.get("AVIATIONSTACK_API_KEY")

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set all CORS enabled origins
origins = [
  # Add more URLs if needed
    "http://localhost:5173",  # Svelte app's URL
]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True,allow_methods=["*"], allow_headers=["*"])

params = {
  'access_key': API_KEY
}

def fetch_flights():
  try:
      api_result = requests.get('http://api.aviationstack.com/v1/flights', params)
      api_result.raise_for_status()
      api_response = api_result.json()
      return api_response.get('data', [])
  except requests.RequestException as e:
      logger.error(f"Error fetching flights: {e}")
      raise HTTPException(status_code=500, detail="Error fetching flight data")

def format_flight_info(flight):
    airline_name = flight['airline']['name']
    if not airline_name:
        airline_name = 'Unknown airline'
    iata_code = flight['flight']['iata']
    departure_airport = flight['departure']['airport']
    if not departure_airport:
        departure_airport = 'unknown airport'
    departure_iata = flight['departure']['iata']
    arrival_airport = flight['arrival']['airport']
    if not arrival_airport:
        arrival_airport = 'unknown airport'
    arrival_iata = flight['arrival']['iata']

    return f'{airline_name} flight {iata_code} from {departure_airport} ({departure_iata}) to {arrival_airport} ({arrival_iata}) is in the air.'
  


@app.get("/flights")
async def get_flights():
    flights_data = fetch_flights()
    flights = [format_flight_info(flight) for flight in flights_data]
    return flights


