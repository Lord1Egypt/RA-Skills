# -*- coding: utf-8 -*-
import os
import json
from datetime import datetime

DISPATCH_DIR = "/var/log/compute/dispatched"


def is_safe_task_name(name):
    if not isinstance(name, str):
        return False
    if not name:
        return False
    return all(c.isalnum() or c in ('-', '_') for c in name)


def run(schedule_report):
    scheduled = schedule_report.get("scheduled_tasks", [])
    os.makedirs(DISPATCH_DIR, exist_ok=True)

    dispatched = []

    for task in scheduled:
        task_name = task.get("task_name", "")
        if not is_safe_task_name(task_name):
            continue

        dispatch_record = {
            "task_name": task_name,
            "dispatched_at": datetime.utcnow().isoformat(),
            "status": "dispatched",
        }

        record_path = os.path.join(DISPATCH_DIR, "{}.json".format(task_name))
        with open(record_path, "w") as f:
            json.dump(dispatch_record, f, indent=2)

        dispatched.append(task_name)

    return {
        "dispatch_timestamp": datetime.utcnow().isoformat(),
        "dispatched_tasks": dispatched,
        "dispatch_log": DISPATCH_DIR,
        "total_dispatched": len(dispatched),
        "status": "completed",
    }


if __name__ == "__main__":
    import sys
    report_path = sys.argv[1] if len(sys.argv) > 1 else "/tmp/schedule_report.json"
    with open(report_path) as f:
        schedule = json.load(f)
    result = run(schedule)
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
