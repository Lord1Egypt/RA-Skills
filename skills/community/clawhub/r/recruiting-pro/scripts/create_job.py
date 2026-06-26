#!/usr/bin/env python3
"""Create a new job posting."""
import json
import os
import uuid
import argparse
from datetime import datetime

RECRUITING_DIR = os.path.expanduser("~/.openclaw/workspace/memory/recruiting")
JOBS_FILE = os.path.join(RECRUITING_DIR, "jobs.json")

def ensure_dir():
    os.makedirs(RECRUITING_DIR, exist_ok=True)

def load_jobs():
    if os.path.exists(JOBS_FILE):
        with open(JOBS_FILE, 'r') as f:
            return json.load(f)
    return {"jobs": []}

def save_jobs(data):
    ensure_dir()
    with open(JOBS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Create job posting')
    parser.add_argument('--title', required=True, help='Job title')
    parser.add_argument('--level', choices=['junior', 'mid', 'senior', 'lead', 'exec'],
                        default='mid', help='Seniority level')
    parser.add_argument('--department', default='', help='Department')
    parser.add_argument('--location', default='Remote', help='Location')
    parser.add_argument('--type', default='Full-time', help='Employment type')
    
    args = parser.parse_args()
    
    job_id = f"JOB-{str(uuid.uuid4())[:6].upper()}"
    
    job = {
        "id": job_id,
        "title": args.title,
        "level": args.level,
        "department": args.department,
        "location": args.location,
        "employment_type": args.type,
        "status": "active",
        "created_at": datetime.now().isoformat(),
        "requirements": [],
        "responsibilities": [],
        "screening_criteria": []
    }
    
    data = load_jobs()
    data['jobs'].append(job)
    save_jobs(data)
    
    print(f"✓ Job created: {job_id}")
    print(f"  Title: {args.title}")
    print(f"  Level: {args.level}")
    print(f"  Location: {args.location}")
    print(f"\nNext steps:")
    print(f"  1. Add requirements: edit jobs.json or use --interactive")
    print(f"  2. Define screening criteria")
    print(f"  3. Post to job boards")

if __name__ == '__main__':
    main()
