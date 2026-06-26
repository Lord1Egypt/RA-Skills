import json
import os
import logging

class StateManager:
    def __init__(self, state_path):
        self.state_path = state_path
        self.state = {}

    def load(self):
        if os.path.exists(self.state_path):
            logging.info(f"Loading state from {self.state_path}...")
            with open(self.state_path, 'r', encoding='utf-8') as f:
                self.state = json.load(f)
            return self.state
        else:
            logging.warning(f"State file not found at {self.state_path}. Starting with empty state.")
            self.state = {}
            return self.state

    def save(self):
        logging.info(f"Saving state to {self.state_path}...")
        with open(self.state_path, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, indent=4)

    def get_last_sent(self, username):
        return self.state.get(username)

    def update_state(self, username, date_str):
        self.state[username] = date_str
        self.save()
