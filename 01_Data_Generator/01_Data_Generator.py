import json
import random
import time
from datetime import datetime
import os

# Output directory 
OUTPUT_DIR = "/Volumes/ai_logs_catalog/logs_schema/raw_logs_vol/logs"  

os.makedirs(OUTPUT_DIR, exist_ok=True)

services = ["payment-service", "order-service", "user-service", "inventory-service"]

log_levels = ["INFO", "WARN", "ERROR"]

error_messages = {
    "payment-service": [
        ("Timeout while calling payment gateway", "PAY-504"),
        ("Payment failed due to insufficient funds", "PAY-402")
    ],
    "order-service": [
        ("Order creation failed", "ORD-500"),
        ("Invalid order request", "ORD-400")
    ],
    "user-service": [
        ("User login failed", "USR-401"),
        ("Session expired", "USR-440")
    ],
    "inventory-service": [
        ("Stock not available", "INV-404"),
        ("Inventory update failed", "INV-500")
    ]
}

info_messages = {
    "payment-service": ["Payment processed successfully"],
    "order-service": ["Order created successfully"],
    "user-service": ["User logged in"],
    "inventory-service": ["Inventory updated"]
}

def generate_log(spike=False):
    service = random.choice(services)

    # Increase error probability during spike
    if spike:
        level = random.choices(["ERROR", "INFO"], weights=[0.7, 0.3])[0]
    else:
        level = random.choices(log_levels, weights=[0.1, 0.2, 0.7])[0]

    if level == "ERROR":
        message, code = random.choice(error_messages[service])
        response_time = random.randint(800, 2000)
    else:
        message = random.choice(info_messages[service])
        code = None
        response_time = random.randint(100, 500)

    log = {
        "timestamp": datetime.utcnow().isoformat(),
        "service_name": service,
        "log_level": level,
        "message": message,
        "error_code": code,
        "response_time": response_time
    }

    return log


def write_logs():
    counter = 0

    while counter < 20:
        # Create spike every 5 iterations
        spike = (counter % 5 == 0)

        logs_batch = [generate_log(spike) for _ in range(50)]

        file_name = f"log_{int(time.time())}.json"
        file_path = os.path.join(OUTPUT_DIR, file_name)

        with open(file_path, "w") as f:
            for log in logs_batch:
                f.write(json.dumps(log) + "\n")

        print(f"Written: {file_name}")

        counter += 1
        time.sleep(5)


if __name__ == "__main__":
    write_logs()