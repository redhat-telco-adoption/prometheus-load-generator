import os
import random
import time
import requests

# --- Configuration from Environment Variables ---
TARGET_URL = os.getenv("TARGET_URL", "http://prometheus-example-app:8080")
RPS = int(os.getenv("RPS", "10"))

# Error ratio will vary randomly between these bounds
MIN_ERROR_RATIO = float(os.getenv("MIN_ERROR_RATIO", "0.1"))  # 10%
MAX_ERROR_RATIO = float(os.getenv("MAX_ERROR_RATIO", "0.5"))  # 50%

print("🚀 Starting load generator...")
print(f"   - Target URL: {TARGET_URL}")
print(f"   - Target RPS: {RPS}")
print(f"   - Error Ratio range: {MIN_ERROR_RATIO} – {MAX_ERROR_RATIO}")

# --- Main Loop ---
while True:
    try:
        # Pick a new error ratio each iteration
        current_error_ratio = random.uniform(MIN_ERROR_RATIO, MAX_ERROR_RATIO)

        if random.random() < current_error_ratio:
            endpoint = "/err"
        else:
            endpoint = "/"

        url_to_hit = f"{TARGET_URL}{endpoint}"

        response = requests.get(url_to_hit, timeout=5)

        print(
            f"Request to {url_to_hit} | Status: {response.status_code} "
            f"| Error Ratio (this round): {current_error_ratio:.2f}"
        )

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")

    time.sleep(1 / RPS)
