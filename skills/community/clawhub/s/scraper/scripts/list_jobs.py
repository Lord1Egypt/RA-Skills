#!/usr/bin/env python3
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_jobs

def main():
    jobs = load_jobs().get("jobs", {})
    if not jobs:
        print("No scraper jobs saved yet.")
        return

    for job_id, job in jobs.items():
        print(f"{job_id} | {job.get('title')} | {job.get('url')}")
        print(f"  {job.get('saved_to')}")
        print()

if __name__ == "__main__":
    main()
