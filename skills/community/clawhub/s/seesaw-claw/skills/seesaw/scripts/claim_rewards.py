import sys
import os
import json

# Add current dir to path to import utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import (
    send_slack_message,
    parse_args,
    load_config
)
from seesaw import SeesawClient

def main():
    args = parse_args("Claim available rewards.")
    config = load_config()
    dry_run = args.dry_run or config.get("dry_run", False)
    
    print("--- Starting Claim Rewards Workflow ---")
    if dry_run:
        print("[DRY-RUN MODE ENABLED]")
        
    client = SeesawClient()

    claimed_count = 0
    try:
        # Get challenges/tasks
        # Assuming list_challenges returns a list of objects or dict with 'items'
        challenges_resp = client.list_challenges()
        
        if isinstance(challenges_resp, dict) and 'items' in challenges_resp:
            challenges = challenges_resp['items']
        elif isinstance(challenges_resp, list):
            challenges = challenges_resp
        else:
            print(f"Unexpected challenges format: {type(challenges_resp)}")
            challenges = []
            
        print(f"Found {len(challenges)} challenges.")

        
        for challenge in challenges:
            c_id = challenge.get('id')
            title = challenge.get('title')
            status = challenge.get('status')
            
            # Debug log status
            print(f"Challenge: {title} (ID: {c_id}, Status: {status})")
            
            # Check if claimable - status values: pending, completed, claimed
            if status == 'completed': 
                print(f"Attempting to claim reward for: {title}")
                
                if not dry_run:
                    try:
                        resp = client.claim_challenge(c_id)
                        msg = f"Claimed Reward: {title}"
                        send_slack_message(msg)
                        print(msg)
                        claimed_count += 1
                    except Exception as e:
                        print(f"Failed to claim {c_id}: {e}")
                else:
                    print(f"[DRY-RUN] Would claim reward for {c_id}")
                    
    except Exception as e:
        print(f"Error checking rewards: {e}")

    if claimed_count == 0:
        print("No new rewards claimed.")

if __name__ == "__main__":
    main()
