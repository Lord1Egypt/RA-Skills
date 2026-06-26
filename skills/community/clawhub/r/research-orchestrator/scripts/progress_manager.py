#!/usr/bin/env python3
"""
Progress Manager
Track and report research progress
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


class ProgressManager:
    def __init__(self, workspace=None):
        self.workspace = workspace or os.environ.get("OPENCLAW_WORKSPACE", os.getcwd())

    def create_progress(self, task_id, query):
        """Create initial progress file"""

        progress = {
            "task_id": task_id,
            "query": query,
            "status": "created",
            "current_phase": "init",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "phases": {
                "decomposition": {
                    "status": "pending",
                    "started_at": None,
                    "completed_at": None,
                },
                "research": {
                    "status": "pending",
                    "started_at": None,
                    "completed_at": None,
                    "agents": {},
                },
                "verification": {
                    "status": "pending",
                    "started_at": None,
                    "completed_at": None,
                },
                "analysis": {
                    "status": "pending",
                    "started_at": None,
                    "completed_at": None,
                },
                "reporting": {
                    "status": "pending",
                    "started_at": None,
                    "completed_at": None,
                },
            },
            "metrics": {
                "total_sources": 0,
                "total_findings": 0,
                "high_credibility_findings": 0,
                "elapsed_seconds": 0,
            },
        }

        return progress

    def update_phase(self, progress, phase, status, details=None):
        """Update phase status"""

        if phase not in progress["phases"]:
            print(f"Warning: Unknown phase {phase}")
            return progress

        progress["phases"][phase]["status"] = status
        progress["current_phase"] = phase
        progress["updated_at"] = datetime.now().isoformat()

        if status == "running":
            progress["phases"][phase]["started_at"] = datetime.now().isoformat()
            progress["status"] = "running"
        elif status == "done":
            progress["phases"][phase]["completed_at"] = datetime.now().isoformat()

        if details:
            progress["phases"][phase].update(details)

        # Check if all phases complete
        all_done = all(
            p["status"] in ["done", "skipped"] for p in progress["phases"].values()
        )
        if all_done:
            progress["status"] = "completed"

        return progress

    def update_agent(self, progress, agent_id, status, sources=0):
        """Update research agent status"""

        if "agents" not in progress["phases"]["research"]:
            progress["phases"]["research"]["agents"] = {}

        progress["phases"]["research"]["agents"][agent_id] = {
            "status": status,
            "sources": sources,
            "updated_at": datetime.now().isoformat(),
        }

        # Update total sources
        total_sources = sum(
            a.get("sources", 0)
            for a in progress["phases"]["research"]["agents"].values()
        )
        progress["metrics"]["total_sources"] = total_sources

        return progress

    def update_metrics(self, progress, metrics):
        """Update progress metrics"""

        progress["metrics"].update(metrics)
        progress["updated_at"] = datetime.now().isoformat()

        return progress

    def save_progress(self, task_dir, progress):
        """Save progress to file"""

        progress_file = f"{task_dir}/progress.json"

        with open(progress_file, "w", encoding="utf-8") as f:
            json.dump(progress, f, indent=2, ensure_ascii=False)

        return progress_file

    def load_progress(self, task_dir):
        """Load progress from file"""

        progress_file = f"{task_dir}/progress.json"

        if not os.path.exists(progress_file):
            return None

        with open(progress_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_progress_summary(self, progress, lang="en"):
        """Get formatted progress summary"""

        if lang.startswith("zh"):
            return self._get_chinese_summary(progress)
        else:
            return self._get_english_summary(progress)

    def _get_chinese_summary(self, progress):
        """Chinese progress summary"""

        status_icons = {
            "pending": "⏳",
            "running": "🔄",
            "done": "✅",
            "skipped": "⏭️",
            "failed": "❌",
        }

        summary = f"""
📊 研究进度报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🆔 任务ID: {progress["task_id"]}
📝 研究主题: {progress["query"][:50]}{"..." if len(progress["query"]) > 50 else ""}
🔄 当前状态: {progress["status"]}
📍 当前阶段: {progress["current_phase"]}

📋 阶段进度:
"""

        phase_names = {
            "decomposition": "任务分解",
            "research": "信息研究",
            "verification": "事实验证",
            "analysis": "深度分析",
            "reporting": "报告生成",
        }

        for phase_id, phase in progress["phases"].items():
            icon = status_icons.get(phase["status"], "❓")
            name = phase_names.get(phase_id, phase_id)

            summary += f"  {icon} {name}: {phase['status']}\n"

            # Show agent details for research phase
            if phase_id == "research" and "agents" in phase:
                for agent_id, agent in phase["agents"].items():
                    agent_icon = status_icons.get(agent["status"], "❓")
                    summary += f"      {agent_icon} {agent_id}: {agent.get('sources', 0)}个来源\n"

        summary += f"""
📊 数据统计:
  📚 总来源数: {progress["metrics"]["total_sources"]}
  🔍 总发现数: {progress["metrics"]["total_findings"]}
  ⭐ 高可信度: {progress["metrics"]["high_credibility_findings"]}
"""

        return summary

    def _get_english_summary(self, progress):
        """English progress summary"""

        status_icons = {
            "pending": "⏳",
            "running": "🔄",
            "done": "✅",
            "skipped": "⏭️",
            "failed": "❌",
        }

        summary = f"""
📊 Research Progress Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🆔 Task ID: {progress["task_id"]}
📝 Topic: {progress["query"][:50]}{"..." if len(progress["query"]) > 50 else ""}
🔄 Status: {progress["status"]}
📍 Current Phase: {progress["current_phase"]}

📋 Phase Progress:
"""

        phase_names = {
            "decomposition": "Task Decomposition",
            "research": "Information Research",
            "verification": "Fact Verification",
            "analysis": "Deep Analysis",
            "reporting": "Report Generation",
        }

        for phase_id, phase in progress["phases"].items():
            icon = status_icons.get(phase["status"], "❓")
            name = phase_names.get(phase_id, phase_id)

            summary += f"  {icon} {name}: {phase['status']}\n"

            # Show agent details for research phase
            if phase_id == "research" and "agents" in phase:
                for agent_id, agent in phase["agents"].items():
                    agent_icon = status_icons.get(agent["status"], "❓")
                    summary += f"      {agent_icon} {agent_id}: {agent.get('sources', 0)} sources\n"

        summary += f"""
📊 Metrics:
  📚 Total Sources: {progress["metrics"]["total_sources"]}
  🔍 Total Findings: {progress["metrics"]["total_findings"]}
  ⭐ High Credibility: {progress["metrics"]["high_credibility_findings"]}
"""

        return summary

    def list_active_tasks(self):
        """List all active research tasks"""

        tasks_dir = f"{self.workspace}/deep-research/tasks"
        active_tasks = []

        if not os.path.exists(tasks_dir):
            return active_tasks

        for task_id in os.listdir(tasks_dir):
            task_dir = f"{tasks_dir}/{task_id}"
            progress_file = f"{task_dir}/progress.json"

            if os.path.exists(progress_file):
                progress = self.load_progress(task_dir)
                if progress and progress["status"] not in ["completed", "failed"]:
                    active_tasks.append(
                        {
                            "task_id": task_id,
                            "query": progress.get("query", ""),
                            "status": progress["status"],
                            "current_phase": progress["current_phase"],
                        }
                    )

        return active_tasks


def main():
    """CLI interface"""

    if len(sys.argv) < 2:
        print("Usage: python3 progress_manager.py <command> [args]")
        print("Commands:")
        print("  show <task_dir> [lang] - Show progress")
        print("  list                   - List active tasks")
        sys.exit(1)

    command = sys.argv[1]
    manager = ProgressManager()

    if command == "show":
        task_dir = sys.argv[2] if len(sys.argv) > 2 else "."
        lang = sys.argv[3] if len(sys.argv) > 3 else "en"

        progress = manager.load_progress(task_dir)
        if progress:
            print(manager.get_progress_summary(progress, lang))
        else:
            print("No progress file found")

    elif command == "list":
        tasks = manager.list_active_tasks()
        print(json.dumps(tasks, indent=2, ensure_ascii=False))

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
