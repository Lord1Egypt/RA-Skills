# -*- coding: utf-8 -*-
import os
import json
import glob
from datetime import datetime

TEMPLATES_DIR = "/etc/compute/templates"


def run(capacity_report):
    cpu_idle = capacity_report.get("cpu_percent_idle", 0)
    mem_avail = capacity_report.get("memory_mb_available", 0)

    template_files = glob.glob(os.path.join(TEMPLATES_DIR, "*.json"))
    scheduled_tasks = []

    for tf in template_files:
        with open(tf) as f:
            spec = json.load(f)

        task_name = os.path.splitext(os.path.basename(tf))[0]
        cpu_req = spec.get("cpu_required", 0)
        mem_req = spec.get("memory_mb", 0)

        if cpu_req <= cpu_idle * 0.8 and mem_req <= mem_avail * 0.8:
            scheduled_tasks.append({
                "task_name": task_name,
                "cpu_required": cpu_req,
                "memory_mb": mem_req,
                "priority": spec.get("priority", "low"),
                "type": spec.get("type", "unknown"),
            })

    return {
        "schedule_timestamp": datetime.utcnow().isoformat(),
        "capacity": {"cpu_percent_idle": cpu_idle, "memory_mb_available": mem_avail},
        "scheduled_tasks": scheduled_tasks,
        "total_scheduled": len(scheduled_tasks),
        "status": "completed",
    }


if __name__ == "__main__":
    import sys
    report_path = sys.argv[1] if len(sys.argv) > 1 else "/tmp/capacity_report.json"
    with open(report_path) as f:
        capacity = json.load(f)
    result = run(capacity)
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
