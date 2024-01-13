from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import random
from datetime import datetime
import asyncio

# Importing the context manager used in fastAPI 
from contextlib import asynccontextmanager

# Dotenv loading 
import os 
import dotenv

# Json wrangling 
import json 

# Azure events 
from azure.eventhub import EventHubProducerClient, EventData

# Loading the .env file
dotenv.load_dotenv()

# Getting the credentials from the .env file
connection_str = os.environ.get("EVENT_HUB_CONNECTION_STRING")
eventhub_name = os.environ.get("EVENT_HUB_NAME")

def get_power_usage_range(hour):
    """Determines the power usage range based on the hour of the day."""
    if 22 <= hour or hour < 6:
        return (10, 60)  # Night: Lower consumption
    elif 6 <= hour < 10:
        return (100, 200)  # Morning: High consumption
    elif 10 <= hour < 18:
        return (60, 100)  # Daytime: Moderate consumption
    else:
        return (100, 200)  # Evening: High consumption again

def generate_mock_energy_data():
    """Generates a mock energy data point."""
    timestamp = datetime.now()
    hour = timestamp.hour
    power_usage_range = get_power_usage_range(hour)
    power_usage = random.uniform(*power_usage_range)  # Random power usage in the determined range
    voltage = random.uniform(110, 220)  # Random voltage
    current = power_usage / voltage  # Simple calculation for current
    return {
        "timestamp": timestamp,
        "power_usage": power_usage,
        "voltage": voltage,
        "current": current
    }

# Creating a function to stop the producer when the app is stopped
# the function return needs to return an awaitable object
async def stop_producer():    
    # Returning an awaitable empty list
    return 

@asynccontextmanager
async def lifespan(app: FastAPI):
    producer = EventHubProducerClient.from_connection_string(conn_str=connection_str, eventhub_name=eventhub_name)
    app.state.producer = producer
    yield
    await stop_producer()

# Initiating the api 
app = FastAPI(lifespan=lifespan)

@app.get("/stream_energy_data")
async def stream_energy_data():

    # Check if producer exists in app state
    if not hasattr(app.state, 'producer'):
        return {"error": "EventHubProducerClient not initialized"}

    producer = app.state.producer
    while True:
        data_point = generate_mock_energy_data()
        event_data_batch = producer.create_batch()
        event_data_batch.add(EventData(json.dumps(data_point, default=str)))
        producer.send_batch(event_data_batch)
        await asyncio.sleep(1)  # Interval between data points

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)