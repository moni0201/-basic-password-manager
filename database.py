import json
import os

FILE_PATH = "data/passwords.json"

def load_data():
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, "w") as f:
            json.dump({}, f)

    with open(FILE_PATH, "r") as f:
        content = f.read().strip()

        if not content:
            return {}

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {}

def save_data(data):
    os.makedirs("data", exist_ok=True)

    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)