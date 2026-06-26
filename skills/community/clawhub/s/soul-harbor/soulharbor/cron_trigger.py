"""
Cron Job entry script
For scheduled proactive message checking
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from soulharbor.memory_system import MemorySystem
from soulharbor.proactive_trigger import ProactiveTrigger


def main():
    """Cron Job main function"""
    memory = MemorySystem()
    
    # Get all user IDs (from storage)
    # TODO: Implement user list retrieval based on actual storage
    user_ids = ["default_user"]  # Example
    
    def send_message(user_id: str, message: str):
        """Send proactive message"""
        # TODO: Integrate OpenClaw message sending interface
        print(f"[Cron] Sending to {user_id}: {message}")
    
    trigger = ProactiveTrigger(memory, send_message)
    
    # Check all users
    for user_id in user_ids:
        messages = trigger.check_and_trigger(user_id)
        for msg in messages:
            send_message(user_id, msg)


if __name__ == "__main__":
    main()
