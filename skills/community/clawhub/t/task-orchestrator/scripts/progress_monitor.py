#!/usr/bin/env python3
"""Progress Monitor - Progress Monitoring Script"""
import json
from datetime import datetime
from typing import List, Dict, Any
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    FAILED = "failed"

class ProgressMonitor:
    def __init__(self, tasks_file: str):
        self.tasks_file = tasks_file
        with open(tasks_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        self.tasks = self.data.get("tasks", [])
    
    def _save(self):
        with open(self.tasks_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def update_status(self, task_id: str, status: str, message: str = None):
        for task in self.tasks:
            if task["id"] == task_id:
                task["status"] = status
                task["updated_at"] = datetime.now().isoformat()
                if status == "in_progress":
                    task["started_at"] = datetime.now().isoformat()
                elif status in ["completed", "failed"]:
                    task["completed_at"] = datetime.now().isoformat()
                self._save()
                return True
        return False
    
    def get_progress(self) -> Dict[str, Any]:
        counts = {s.value: 0 for s in TaskStatus}
        for task in self.tasks:
            status = task.get("status", "pending")
            if status in counts:
                counts[status] += 1
        total = len(self.tasks)
        completed = counts["completed"]
        return {
            "total": total,
            "progress_percent": round(completed / total * 100, 1) if total else 0,
            "status_counts": counts,
            "is_complete": completed == total
        }
    
    def detect_anomalies(self) -> List[Dict]:
        anomalies = []
        for task in self.tasks:
            if task.get("status") == "in_progress":
                started = task.get("started_at")
                if started:
                    try:
                        elapsed = (datetime.now() - datetime.fromisoformat(started)).total_seconds() / 3600
                        est = float(task.get("estimated_time", "1h").replace("h", "") or 1)
                        if elapsed > est * 1.5:
                            anomalies.append({"task_id": task["id"], "type": "timeout", "elapsed": elapsed})
                    except: pass
            if task.get("status") == "blocked":
                anomalies.append({"task_id": task["id"], "type": "blocked"})
            if task.get("status") == "failed":
                anomalies.append({"task_id": task["id"], "type": "failed"})
        return anomalies
    
    def generate_report(self) -> str:
        progress = self.get_progress()
        c = progress["status_counts"]
        lines = [
            "═" * 40,
            f"📊 Task Progress: {progress['progress_percent']}%",
            f"  ✓ Completed: {c['completed']}  ⏳ In Progress: {c['in_progress']}",
            f"  ⏸ Pending: {c['pending']}  🚫 Blocked: {c['blocked']}  ✗ Failed: {c['failed']}",
            "═" * 40
        ]
        return "\n".join(lines)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-a', '--action', choices=['status', 'report', 'update'], default='report')
    parser.add_argument('-t', '--task-id')
    parser.add_argument('-s', '--status')
    args = parser.parse_args()
    
    monitor = ProgressMonitor(args.input)
    if args.action == 'report':
        print(monitor.generate_report())
    elif args.action == 'status':
        print(json.dumps(monitor.get_progress(), indent=2))
    elif args.action == 'update' and args.task_id and args.status:
        monitor.update_status(args.task_id, args.status)
        print(f"✓ Updated {args.task_id} -> {args.status}")