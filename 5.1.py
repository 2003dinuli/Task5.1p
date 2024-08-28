import csv
import time
from datetime import datetime
from arduino_iot_cloud import ArduinoCloudClient

DEVICE_ID = "6b32abcc-3875-48dc-a668-a519af99e5a5"
SECRET_KEY = "jXEr6J8ui#HPPQ2PmAGIrsSVl"

# CSV file name
csv_file = "gyroscope1_data.csv"

# Buffer to store data
buffer = {
    'timestamp': None,
    'xx': None,
    'yy': None,
    'zz': None
}

# Callback functions for gyroscope readings
def on_xx_changed(client, value):
    buffer['xx'] = value
    save_data_if_complete()

def on_yy_changed(client, value):
    buffer['yy'] = value
    save_data_if_complete()

def on_zz_changed(client, value):
    buffer['zz'] = value
    save_data_if_complete()

def save_data_if_complete():
    # Ensure that all values are set
    if all(val is not None for val in [buffer['xx'], buffer['yy'], buffer['zz']]):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if buffer['timestamp'] != timestamp:
            # Update timestamp in buffer
            buffer['timestamp'] = timestamp
            # Save data to CSV
            save_data(timestamp, buffer['xx'], buffer['yy'], buffer['zz'])
            # Clear buffer
            buffer['xx'] = None
            buffer['yy'] = None
            buffer['zz'] = None

# Function to save data to CSV
def save_data(timestamp, xx, yy, zz):
    with open(csv_file, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, xx, yy, zz])
        print(f"Data saved: {timestamp}, xx={xx}, yy={yy}, zz={zz}")

def main():
    print("Starting the IoT client...")

    # Instantiate Arduino cloud client
    client = ArduinoCloudClient(
        device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY
    )

    # Register with cloud variables for gyroscope axes
    client.register("xx", value=None, on_write=on_xx_changed)
    client.register("yy", value=None, on_write=on_yy_changed)
    client.register("zz", value=None, on_write=on_zz_changed)

    # Initialize CSV file with headers
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "X-axis (xx)", "Y-axis (yy)", "Z-axis (zz)"])

    # Start cloud client
    client.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Script terminated by user.")

if __name__ == "__main__":
    main()
