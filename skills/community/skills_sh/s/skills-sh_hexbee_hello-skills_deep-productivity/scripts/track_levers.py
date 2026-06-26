#!/usr/bin/env python3
"""
Lever-Moving Task Tracker

Track daily progress on lever-moving tasks and assess whether
you're actually moving toward your goals.
"""

import json
import os
from datetime import datetime, timedelta


class LeverTracker:
    def __init__(self, data_file="lever_tracking.json"):
        self.data_file = data_file
        self.data = self.load_data()

    def load_data(self):
        """Load tracking data from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {"tasks": [], "projects": [], "logs": []}
        return {"tasks": [], "projects": [], "logs": []}

    def save_data(self):
        """Save tracking data to file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2, default=str)

    def add_project(self, name, ten_year_goal):
        """Add a project with its alignment to 10-year goal"""
        project = {
            "id": len(self.data["projects"]) + 1,
            "name": name,
            "ten_year_goal": ten_year_goal,
            "created": datetime.now().isoformat(),
            "status": "active",
            "milestones": []
        }
        self.data["projects"].append(project)
        self.save_data()
        return project

    def add_milestone(self, project_id, one_year, one_month, one_week):
        """Add milestones to a project"""
        for project in self.data["projects"]:
            if project["id"] == project_id:
                project["milestones"] = {
                    "one_year": one_year,
                    "one_month": one_month,
                    "one_week": one_week
                }
                self.save_data()
                return True
        return False

    def log_daily_task(self, project_id, task, duration_minutes, completed=True, notes=""):
        """Log a daily lever-moving task"""
        log_entry = {
            "id": len(self.data["logs"]) + 1,
            "project_id": project_id,
            "date": datetime.now().isoformat(),
            "task": task,
            "duration_minutes": duration_minutes,
            "completed": completed,
            "notes": notes
        }
        self.data["logs"].append(log_entry)
        self.save_data()
        return log_entry

    def get_project_progress(self, project_id):
        """Calculate progress on a project"""
        project_logs = [l for l in self.data["logs"] if l["project_id"] == project_id]
        completed_tasks = [l for l in project_logs if l["completed"]]
        total_minutes = sum(l["duration_minutes"] for l in project_logs)
        completed_minutes = sum(l["duration_minutes"] for l in completed_tasks)

        return {
            "total_tasks": len(project_logs),
            "completed_tasks": len(completed_tasks),
            "total_minutes": total_minutes,
            "completed_minutes": completed_minutes,
            "completion_rate": len(completed_tasks) / len(project_logs) * 100 if project_logs else 0
        }

    def check_lever_moving(self, project_id, weeks=2):
        """Check if lever-moving tasks are actually moving the needle"""
        cutoff = datetime.now() - timedelta(weeks=weeks)
        recent_logs = [l for l in self.data["logs"]
                      if l["project_id"] == project_id
                      and datetime.fromisoformat(l["date"]) > cutoff]

        if not recent_logs:
            return {
                "status": "no_activity",
                "message": "No activity in the past 2 weeks",
                "recommendation": "Start your daily 1-hour protocol immediately"
            }

        progress = self.get_project_progress(project_id)

        if progress["completion_rate"] < 50:
            return {
                "status": "low_engagement",
                "message": f"Only {progress['completion_rate']:.0f}% completion rate",
                "recommendation": "Review your goal hierarchy—are you working on the right levers?"
            }

        if progress["total_minutes"] < 60 * 14:  # 1 hour/day for 2 weeks
            return {
                "status": "insufficient_time",
                "message": f"Only {progress['total_minutes']/60:.1f} hours logged",
                "recommendation": "You need 1 hour/day minimum. Protect your time."
            }

        return {
            "status": "on_track",
            "message": f"Good progress: {progress['completed_tasks']} tasks completed",
            "recommendation": "Keep going—you're moving the right levers"
        }

    def weekly_review(self, project_id):
        """Generate weekly review summary"""
        progress = self.get_project_progress(project_id)
        lever_status = self.check_lever_moving(project_id)

        review = {
            "date": datetime.now().isoformat(),
            "tasks_completed": progress["completed_tasks"],
            "total_hours": progress["completed_minutes"] / 60,
            "completion_rate": progress["completion_rate"],
            "lever_status": lever_status["status"]
        }

        return review


def main():
    tracker = LeverTracker()

    print("=" * 60)
    print("LEVER-MOVING TASK TRACKER")
    print("=" * 60)
    print("\nOptions:")
    print("1. Log daily task")
    print("2. View project progress")
    print("3. Check if you're moving the right levers")
    print("4. Weekly review")
    print("5. Add new project")
    print("q. Quit")

    choice = input("\n> ")

    if choice == "1":
        print("\nLogging a daily task...")
        project_id = int(input("Project ID: "))
        task = input("Task description: ")
        duration = int(input("Duration (minutes): "))
        completed_input = input("Completed? (y/n): ")
        completed = completed_input.lower() == 'y'
        notes = input("Notes (optional): ")

        log = tracker.log_daily_task(project_id, task, duration, completed, notes)
        print(f"\nLogged: {task} ({duration} min) - {'Done' if completed else 'Not done'}")

    elif choice == "2":
        print("\nProject Progress:")
        for p in tracker.data["projects"]:
            if p["status"] == "active":
                prog = tracker.get_project_progress(p["id"])
                print(f"\n{p['name']} (ID: {p['id']})")
                print(f"  Tasks: {prog['completed_tasks']}/{prog['total_tasks']} completed")
                print(f"  Hours: {prog['completed_minutes']/60:.1f}")
                print(f"  Rate: {prog['completion_rate']:.0f}%")

    elif choice == "3":
        project_id = int(input("Project ID to check: "))
        status = tracker.check_lever_moving(project_id)
        print(f"\nStatus: {status['status'].upper()}")
        print(f"Message: {status['message']}")
        print(f"Recommendation: {status['recommendation']}")

    elif choice == "4":
        project_id = int(input("Project ID for weekly review: "))
        review = tracker.weekly_review(project_id)
        print(f"\nWeekly Review for Project {project_id}:")
        print(f"  Tasks Completed: {review['tasks_completed']}")
        print(f"  Total Hours: {review['total_hours']:.1f}")
        print(f"  Completion Rate: {review['completion_rate']:.0f}%")
        print(f"  Lever Status: {review['lever_status']}")

    elif choice == "5":
        print("\nAdding new project...")
        name = input("Project name: ")
        ten_year = input("10-year goal alignment: ")
        project = tracker.add_project(name, ten_year)
        print(f"\nCreated project: {name} (ID: {project['id']})")

    elif choice.lower() == "q":
        return

    else:
        print("Invalid choice")

    tracker.save_data()


if __name__ == "__main__":
    main()
