#!/usr/bin/env python3
"""
Deep Research Orchestrator
Manages multi-agent research workflow
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


class ResearchOrchestrator:
    def __init__(self, workspace=None):
        self.workspace = workspace or os.environ.get("OPENCLAW_WORKSPACE", os.getcwd())
        self.research_dir = f"{self.workspace}/deep-research"
        self.tasks_dir = f"{self.research_dir}/tasks"
        self.output_dir = f"{self.research_dir}/output"

        # Ensure directories exist
        os.makedirs(self.tasks_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

    def create_task(self, query, output_lang="auto"):
        """Create a new research task"""

        task_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        task_dir = f"{self.tasks_dir}/{task_id}"

        # Create task structure
        os.makedirs(f"{task_dir}/research", exist_ok=True)
        os.makedirs(f"{task_dir}/analysis", exist_ok=True)
        os.makedirs(f"{task_dir}/output", exist_ok=True)

        # Task metadata
        meta = {
            "task_id": task_id,
            "query": query,
            "output_lang": output_lang,
            "status": "created",
            "created_at": datetime.now().isoformat(),
            "workspace": task_dir,
        }

        with open(f"{task_dir}/meta.json", "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)

        # Initial progress
        progress = {
            "task_id": task_id,
            "query": query,
            "status": "created",
            "current_phase": "init",
            "created_at": datetime.now().isoformat(),
            "phases": {
                "decomposition": {"status": "pending"},
                "research": {"status": "pending", "agents": {}},
                "verification": {"status": "pending"},
                "analysis": {"status": "pending"},
                "reporting": {"status": "pending"},
            },
            "total_sources": 0,
            "total_findings": 0,
        }

        with open(f"{task_dir}/progress.json", "w", encoding="utf-8") as f:
            json.dump(progress, f, indent=2, ensure_ascii=False)

        return task_id, task_dir, meta

    def update_progress(self, task_dir, phase, status, details=None):
        """Update task progress"""

        progress_file = f"{task_dir}/progress.json"

        with open(progress_file, "r", encoding="utf-8") as f:
            progress = json.load(f)

        progress["current_phase"] = phase
        progress["phases"][phase]["status"] = status
        progress["updated_at"] = datetime.now().isoformat()

        if details:
            progress["phases"][phase].update(details)

        with open(progress_file, "w", encoding="utf-8") as f:
            json.dump(progress, f, indent=2, ensure_ascii=False)

        return progress

    def get_progress(self, task_dir):
        """Get current progress"""

        progress_file = f"{task_dir}/progress.json"

        with open(progress_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def create_research_plan(self, task_dir, research_angles):
        """Create research plan from angles"""

        plan_content = "# Research Plan\n\n"
        plan_content += f"## Research Angles ({len(research_angles)} total)\n\n"

        for i, angle in enumerate(research_angles, 1):
            plan_content += f"### {i}. {angle['name']}\n"
            plan_content += f"- **Queries**: {', '.join(angle['queries'])}\n"
            plan_content += f"- **Sources**: {angle.get('sources', 'web, academic')}\n"
            plan_content += f"- **Priority**: {angle.get('priority', 'medium')}\n"
            plan_content += f"- **Output**: {angle['output_file']}\n\n"

        plan_file = f"{task_dir}/plan.md"
        with open(plan_file, "w", encoding="utf-8") as f:
            f.write(plan_content)

        return plan_file

    def create_research_agent_config(self, task_dir, angle):
        """Create configuration for a research sub-agent"""

        config = {
            "agent_id": f"research-{angle['id']}",
            "task_dir": task_dir,
            "angle": angle,
            "queries": angle["queries"],
            "output_file": f"{task_dir}/research/{angle['output_file']}",
            "created_at": datetime.now().isoformat(),
        }

        config_file = f"{task_dir}/research/{angle['id']}_config.json"
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        return config_file

    def save_research_findings(self, task_dir, angle_id, findings, sources):
        """Save research findings from a sub-agent"""

        findings_file = f"{task_dir}/research/{angle_id}.json"

        data = {
            "angle_id": angle_id,
            "findings": findings,
            "sources": sources,
            "source_count": len(sources),
            "completed_at": datetime.now().isoformat(),
        }

        with open(findings_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # Update progress
        progress = self.get_progress(task_dir)
        progress["phases"]["research"]["agents"][angle_id] = {
            "status": "done",
            "sources": len(sources),
        }
        progress["total_sources"] = sum(
            a.get("sources", 0)
            for a in progress["phases"]["research"]["agents"].values()
        )

        progress_file = f"{task_dir}/progress.json"
        with open(progress_file, "w", encoding="utf-8") as f:
            json.dump(progress, f, indent=2, ensure_ascii=False)

        return findings_file

    def generate_final_report_path(self, task_id):
        """Get path for final report"""

        md_path = f"{self.output_dir}/{task_id}/report.md"
        pdf_path = f"{self.output_dir}/{task_id}/report.pdf"

        os.makedirs(os.path.dirname(md_path), exist_ok=True)

        return md_path, pdf_path

    def list_tasks(self):
        """List all research tasks"""

        tasks = []
        if os.path.exists(self.tasks_dir):
            for task_id in os.listdir(self.tasks_dir):
                meta_file = f"{self.tasks_dir}/{task_id}/meta.json"
                if os.path.exists(meta_file):
                    with open(meta_file, "r", encoding="utf-8") as f:
                        tasks.append(json.load(f))

        return sorted(tasks, key=lambda t: t.get("created_at", ""), reverse=True)

    def get_task_status(self, task_id):
        """Get status of a specific task"""

        task_dir = f"{self.tasks_dir}/{task_id}"

        if not os.path.exists(task_dir):
            return None

        meta_file = f"{task_dir}/meta.json"
        progress_file = f"{task_dir}/progress.json"

        with open(meta_file, "r", encoding="utf-8") as f:
            meta = json.load(f)

        with open(progress_file, "r", encoding="utf-8") as f:
            progress = json.load(f)

        return {"meta": meta, "progress": progress}


def main():
    """CLI interface"""

    if len(sys.argv) < 2:
        print("Usage: python3 orchestrator.py <command> [args]")
        print("Commands:")
        print("  create <query> [lang]  - Create new research task")
        print("  status <task_id>       - Get task status")
        print("  list                   - List all tasks")
        sys.exit(1)

    command = sys.argv[1]
    orchestrator = ResearchOrchestrator()

    if command == "create":
        query = sys.argv[2] if len(sys.argv) > 2 else "Research topic"
        lang = sys.argv[3] if len(sys.argv) > 3 else "auto"
        task_id, task_dir, meta = orchestrator.create_task(query, lang)
        print(json.dumps({"task_id": task_id, "task_dir": task_dir}, indent=2))

    elif command == "status":
        task_id = sys.argv[2] if len(sys.argv) > 2 else None
        if not task_id:
            print("Error: task_id required")
            sys.exit(1)
        status = orchestrator.get_task_status(task_id)
        if status:
            print(json.dumps(status, indent=2, ensure_ascii=False))
        else:
            print(f"Task not found: {task_id}")

    elif command == "list":
        tasks = orchestrator.list_tasks()
        print(json.dumps(tasks, indent=2, ensure_ascii=False))

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
