from datetime import datetime
import json

def log_journal(entry, path="../logs/journal.log"):
    with open(path, "a") as f:
        f.write(f"[{datetime.now()}] {entry}\n")

def log_actions(actions, path="../logs/actions.json"):
    with open(path, "w") as f:
        json.dump(actions, f, indent=2)
