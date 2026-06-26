#!/usr/bin/env python3
"""Update candidate stage in pipeline."""
import json
import os
import argparse
from datetime import datetime

RECRUITING_DIR = os.path.expanduser("~/.openclaw/workspace/memory/recruiting")
PIPELINE_FILE = os.path.join(RECRUITING_DIR, "pipeline.json")

def load_pipeline():
    if not os.path.exists(PIPELINE_FILE):
        return {"candidates": []}
    with open(PIPELINE_FILE, 'r') as f:
        return json.load(f)

def save_pipeline(data):
    os.makedirs(RECRUITING_DIR, exist_ok=True)
    with open(PIPELINE_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Update candidate stage')
    parser.add_argument('--candidate-id', required=True, help='Candidate ID')
    parser.add_argument('--stage', required=True,
                        choices=['screening', 'phone_screen', 'technical', 
                                'onsite', 'reference_check', 'offer', 'hired', 'rejected'],
                        help='New stage')
    parser.add_argument('--next-action', help='Next action required')
    parser.add_argument('--owner', help='Action owner')
    parser.add_argument('--rating', choices=['strong', 'likely', 'maybe', 'no_hire'],
                        help='Candidate rating')
    
    args = parser.parse_args()
    
    data = load_pipeline()
    
    candidate = None
    for c in data.get('candidates', []):
        if c['id'] == args.candidate_id:
            candidate = c
            break
    
    if not candidate:
        print(f"Error: Candidate {args.candidate_id} not found")
        return
    
    # Update stage history
    now = datetime.now().isoformat()
    if candidate['stage_history']:
        candidate['stage_history'][-1]['exited_at'] = now
    
    candidate['stage_history'].append({
        "stage": args.stage,
        "entered_at": now,
        "exited_at": None
    })
    
    candidate['current_stage'] = args.stage
    
    if args.next_action:
        candidate['next_action'] = args.next_action
    if args.owner:
        candidate['action_owner'] = args.owner
    if args.rating:
        candidate['rating'] = args.rating
    
    save_pipeline(data)
    
    print(f"✓ Updated candidate: {candidate['name']}")
    print(f"  New stage: {args.stage}")
    if args.rating:
        print(f"  Rating: {args.rating}")
    if args.next_action:
        print(f"  Next action: {args.next_action}")

if __name__ == '__main__':
    main()
