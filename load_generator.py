import os
import random
import time
import requests

# --- Configuration from Environment Variables ---
# The target service's URL, e.g., 'http://my-app.my-project.svc.cluster.local'
TARGET_URL = os.getenv("TARGET_URL", "http://prometheus-example-app:8080")

# Target requests per second (RPS)
RPS = int(os.getenv("RPS", "10"))

# The ratio of requests that should be sent to the /err endpoint (0.0 to 1.0)
ERROR_RATIO = float(os.getenv("ERROR_RATIO", "0.2")) 

print(f"🚀 Starting load generator...")
print(f"   - Target URL: {TARGET_URL}")
print(f"   - Target RPS: {RPS}")
print(f"   - Error Ratio: {ERROR_RATIO}")

# --- Main Loop ---
while True:
    try:
        # Decide which endpoint to hit based on the error ratio
        if random.random() < ERROR_RATIO:
            endpoint = "/err"
        else:
            endpoint = "/"

        url_to_hit = f"{TARGET_URL}{endpoint}"

        # Make the HTTP GET request
        response = requests.get(url_to_hit, timeout=5) # 5-second timeout

        print(f"Request to {url_to_hit} | Status: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")

    # Wait for a period to maintain the target RPS
    time.sleep(1 / RPS)