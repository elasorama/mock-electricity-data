import random
from datetime import datetime
import time

# Dotenv loading 
import os 
import dotenv

# Json wrangling 
import json 

# Azure events 
from azure.eventhub import EventHubProducerClient, EventData

# Importing the logging functionality
import logging

def get_power_usage_range(hour):
    """
    Determines the power usage range based on the hour of the day.
    
    First, a random hour of day is generated. Then, based on a sine function, the power usage range is determined.
    """
    
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

def stream_energy_data(producer, continues: bool = False, time_interval: int = 1, time_generation: int = 60):
    if continues:
        while True:
            data_point = generate_mock_energy_data()
            print(data_point)
            event_data_batch = producer.create_batch()
            event_data_batch.add(EventData(json.dumps(data_point, default=str)))
            producer.send_batch(event_data_batch)
            
            # Sleep for 1 second
            time.sleep(time_interval)
    else:
        start = time.time()
        while time.time() - start < time_generation:
            data_point = generate_mock_energy_data()
            print(data_point)
            event_data_batch = producer.create_batch()
            event_data_batch.add(EventData(json.dumps(data_point, default=str)))
            producer.send_batch(event_data_batch)
            
            # Sleep for 1 second
            time.sleep(time_interval)

if __name__ == "__main__":
    # Loading the .env file
    dotenv.load_dotenv()

    # Getting the credentials from the .env file
    connection_str = os.environ.get("EVENT_HUB_CONNECTION_STRING")
    eventhub_name = os.environ.get("EVENT_HUB_NAME")

    # Creating the connection to the producer 
    producer = EventHubProducerClient.from_connection_string(connection_str, eventhub_name=eventhub_name)

    # Starting the stream
    stream_energy_data(producer)