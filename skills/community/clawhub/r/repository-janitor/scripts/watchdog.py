#!/usr/bin/env python3
"""Independent scheduler health observer. No cleanup or scheduling mutations."""
import argparse
import json
from pathlib import Path
import subprocess
import time



def health(job, now_ms):
    state=job.get("state",{})
    if not job.get("enabled"): return "disabled"
    due=state.get("nextRunAtMs")
    if due and now_ms-due > 3600000: return "schedule overdue by more than one hour"
    running=state.get("runningAtMs")
    if running and now_ms-running > 900000: return "execution exceeded 15 minutes"
    last=state.get("lastRunAtMs")
    if not last or now_ms-last > 27*3600000: return "no execution in more than 27 hours"
    if state.get("lastRunStatus") in ("error","skipped"): return "last execution failed or was skipped"
    delivery=state.get("lastDeliveryStatus")
    if delivery in ("not-delivered","unknown"): return "delivery failed or unconfirmed"
    return "healthy"

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--job-id", required=True)
    parser.add_argument("--config", type=Path, required=True)
    args=parser.parse_args()
    try:
        p=subprocess.run(["openclaw","automations","get",args.job_id],capture_output=True,text=True,timeout=15)
        if p.returncode: raise ValueError("query unavailable")
        job=json.loads(p.stdout)
        if "job" in job: job=job["job"]
        status=health(job,time.time()*1000)
        config=json.loads(args.config.read_text())
        latest=Path(config["state_dir"])/"latest.json"
        if status=="healthy" and latest.exists() and json.loads(latest.read_text()).get("errors"):
            status="last audit has incomplete coverage"
    except (ValueError,KeyError,TypeError,OSError,subprocess.TimeoutExpired):
        status="scheduler metadata unavailable"
    print(json.dumps({"status":status},ensure_ascii=True))

if __name__=="__main__": main()
