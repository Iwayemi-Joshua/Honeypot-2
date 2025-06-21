import json
import time
from pathlib import Path

LOG_FILE = Path("attack_logs.json")
  # Corrected path

def log_attack(ip, attack_type):
    if LOG_FILE.exists():
        with open(LOG_FILE) as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append({
        "id": len(logs) + 1,
        "ip": ip,
        "type": attack_type,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    })

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)