#!/usr/bin/env python3
"""Add candidate to pipeline."""
import json
import os
import uuid
import argparse
from datetime import datetime

RECRUITING_DIR = os.path.expanduser("~/.openclaw/workspace/memory/recruiting")
PIPELINE_FILE = os.path.join(RECRUITING_DIR, "pipeline.json")

def ensure_dir():
    os.makedirs(RECRUITING_DIR, exist_ok=True)

def load_pipeline():
    if os.path.exists(PIPELINE_FILE):
        with open(PIPELINE_FILE, 'r') as f:
            return json.load(f)
    return {"candidates": []}

def save_pipeline(data):
    ensure_dir()
    with open(PIPELINE_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Add candidate to pipeline')
    parser.add_argument('--job-id', required=True, help='Job ID')
    parser.add_argument('--name', required=True, help='Candidate name')
    parser.add_argument('--email', required=True, help='Candidate email')
    parser.add_argument('--source', default='Direct', help='Application source')
    
    args = parser.parse_args()
    
    candidate_id = f"CAND-{str(uuid.uuid4())[:6].upper()}"
    
    candidate = {
        "id": candidate_id,
        "job_id": args.job_id,
        "name": args.name,
        "email": args.email,
        "source": args.source,
        "applied_at": datetime.now().isoformat(),
        "current_stage": "applied",
        "stage_history": [
            {"stage": "applied", "entered_at": datetime.now().isoformat(), "exited_at": None}
        ],
        "rating": "pending",
        "notes": ""
    }
    
    data = load_pipeline()
    data['candidates'].append(candidate)
    save_pipeline(data)
    
    print(f"✓ Candidate added: {candidate_id}")
    print(f"  Name: {args.name}")
    print(f"  Job: {args.job_id}")
    print(f"  Stage: Applied")

if __name__ == '__main__':
    main()
