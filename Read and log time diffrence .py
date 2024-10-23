import opendaq
import time
from datetime import datetime
import numpy as np
import os

def create_instance():
    """Create and return an opendaq instance."""
    return opendaq.Instance()

# Create an instance
instance = create_instance()

# Add the device and get the signal
device = instance.add_device('daq://openDAQ_08:00:27:e5:df:77')
signal = device.signals_recursive[0]

# Create a stream reader for the signal
reader = opendaq.StreamReader(signal)

# Create a TimeStreamReader using the StreamReader instance
time_reader = opendaq.TimeStreamReader(reader)

previous_timestamp = None  # Variable to hold the timestamp from the previous iteration
file_path = "data_log.txt"

# Open a file to log the values and timestamps
with open(file_path, "a") as log_file:
    # If the file is empty, add the header
    if os.stat(file_path).st_size == 0:
        log_file.write("Value, Timestamp, Time Difference (ms)\n")

    # Loop until we have some samples
    while True:
        # Read 1000 samples with timestamps
        values, timestamps = time_reader.read_with_timestamps(1000)

        # Check if arrays have data using .size
        if values.size > 0 and timestamps.size > 0:
            # Get the first value and timestamp
            first_value = values[0]
            first_timestamp = timestamps[0]

            # Convert numpy datetime64 to a Python datetime object
            first_timestamp_python = first_timestamp.astype('datetime64[ms]').astype(datetime)

            # Format the timestamp
            formatted_time = first_timestamp_python.strftime('%H:%M:%S.%f')[:-3]

            # Calculate time difference
            time_diff_ms = 0  # Initialize with 0 for the first iteration

            # If there is a previous timestamp, calculate the time difference in milliseconds
            if previous_timestamp:
                time_diff = first_timestamp_python - previous_timestamp
                time_diff_ms = int(time_diff.total_seconds() * 1000)

            # Print the first value, timestamp, and time difference
            print(f"First Value: {first_value}, Timestamp: {formatted_time}, Time Difference: {time_diff_ms} ms")

            # Log the value, timestamp, and time difference to the file
            log_file.write(f"{first_value}, {formatted_time}, {time_diff_ms}\n")

            # Update the previous timestamp to the current timestamp
            previous_timestamp = first_timestamp_python

            # Flush the file to ensure data is written
            log_file.flush()

        else:
            print("No samples available, retrying...")

        # Wait for 100 milliseconds before the next attempt
        time.sleep(0.1)

# Wait for user input to exit
input("Press any key to exit...")
