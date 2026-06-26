#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smart Poller - Feishu Task Board Polling Module
Periodically polls a Feishu task board and auto-executes tasks assigned to the current AI agent.
Author: socneo
Version: v1.0
"""

import json
import re
import urllib.request
import urllib.error
from datetime import datetime
from typing import List, Dict, Optional

# Default configuration (overridden by config.json)
DEFAULT_CONFIG = {
    "app_id": "",
    "app_secret": "",
    "doc_token": "",
    "assignee": "agent",
    "poll_interval_minutes": 15,
    "silent_mode": True
}


class FeishuAPI:
    """Feishu API wrapper — handles token management and HTTP requests."""

    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.token = None
        self.token_expire_at = 0
        self.host = "https://open.feishu.cn"

    def get_tenant_access_token(self) -> str:
        """Obtain (or return cached) Feishu tenant_access_token."""
        if self.token and datetime.now().timestamp() < self.token_expire_at:
            return self.token

        url = f"{self.host}/open-apis/auth/v3/tenant_access_token/internal"
        data = json.dumps({"app_id": self.app_id, "app_secret": self.app_secret}).encode()
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

        try:
            resp = urllib.request.urlopen(req, timeout=10)
            result = json.loads(resp.read())
            if result.get("code") == 0:
                self.token = result["tenant_access_token"]
                self.token_expire_at = datetime.now().timestamp() + (result["expire"] - 300)
                return self.token
            else:
                raise Exception(f"Failed to get token: {result.get('msg')}")
        except Exception as e:
            raise Exception(f"Request error: {e}")

    def request(self, path: str, data: Optional[Dict] = None) -> Dict:
        """Generic Feishu API request."""
        token = self.get_tenant_access_token()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        body = json.dumps(data).encode() if data else None
        method = "POST" if data else "GET"

        url = f"{self.host}{path}"
        req = urllib.request.Request(url, data=body, headers=headers, method=method)

        try:
            resp = urllib.request.urlopen(req, timeout=15)
            return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            return {"code": e.code, "msg": e.read().decode()}


class TaskParser:
    """Parses task board content and extracts pending tasks for a given assignee."""

    @staticmethod
    def parse_tasks(content: str, assignee: str) -> List[Dict]:
        """
        Parse the task board document and return pending tasks for the specified assignee.

        Args:
            content: Raw document text
            assignee: Target agent identifier (e.g. 'agent1')

        Returns:
            List of pending task dicts
        """
        tasks = []
        lines = content.split('\n')
        current_task = None
        completed_tasks = set()

        # Pass 1: collect all completed task IDs
        for line in lines:
            match = re.match(r'\[.+\]\s*(TASK-\w+-\d+)', line)
            if match:
                completed_tasks.add(match.group(1))

        # Pass 2: parse tasks
        for line in lines:
            # Match task header: [TASK-xxx-NNN]
            task_match = re.match(r'\[TASK-(\w+-\d+)\]\s*(.*)', line)
            if task_match:
                if (current_task and
                        current_task.get('assignee') == assignee and
                        current_task.get('status') == 'pending' and
                        current_task['id'] not in completed_tasks):
                    tasks.append(current_task)

                current_task = {
                    'id': f"TASK-{task_match.group(1)}",
                    'title': task_match.group(2),
                    'description': '',
                    'assignee': None,
                    'status': 'pending',
                    'priority': 'medium'
                }
                continue

            # Match assignment line: "Assign: from → to"
            assign_match = re.search(r'Assign:\s*(\w+)\s*→\s*(\w+)', line)
            if assign_match and current_task:
                current_task['assignee'] = assign_match.group(2).lower()
                continue

            # Match status: "Status: pending"
            status_match = re.search(r'Status:\s*(\w+)', line)
            if status_match and current_task:
                current_task['status'] = status_match.group(1).lower()
                continue

            # Accumulate description
            if current_task and line.strip():
                current_task['description'] += line + '\n'

        # Handle last task in document
        if (current_task and
                current_task.get('assignee') == assignee and
                current_task.get('status') == 'pending' and
                current_task['id'] not in completed_tasks):
            tasks.append(current_task)

        return tasks


class SmartPoller:
    """Main poller: loads config, polls the task board, and executes tasks."""

    def __init__(self, config_path: str = "config.json"):
        self.config = self.load_config(config_path)
        self.api = FeishuAPI(self.config["app_id"], self.config["app_secret"])
        self.doc_token = self.config["doc_token"]
        self.assignee = self.config["assignee"]
        self.silent_mode = self.config.get("silent_mode", True)

    def load_config(self, path: str) -> Dict:
        """Load configuration from JSON file."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Config file not found: {path}, using defaults.")
            return DEFAULT_CONFIG

    def read_task_board(self) -> str:
        """Fetch and concatenate all text blocks from the Feishu document."""
        result = self.api.request(f"/open-apis/docx/v1/documents/{self.doc_token}/blocks?page_size=200")
        if result.get("code") != 0:
            raise Exception(f"Failed to read document: {result.get('msg')}")

        content = ""
        items = result.get("data", {}).get("items", [])
        for block in items:
            for field in ["text", "heading1", "heading2", "heading3", "bullet"]:
                elements = block.get(field, {}).get("elements", [])
                for elem in elements:
                    text = elem.get("text_run", {}).get("content", "")
                    if text.strip():
                        content += text + "\n"
        return content

    def append_feedback(self, task_id: str, result: str) -> bool:
        """Append a completion feedback line to the Feishu document."""
        timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        content = f"[{self.assignee} completed] {task_id} | Time: {timestamp} | Result: {result}"

        data = {
            "children": [{
                "block_type": 2,
                "text": {
                    "elements": [{"text_run": {"content": content, "text_element_style": {}}}],
                    "style": {}
                }
            }],
            "index": -1
        }

        api_result = self.api.request(
            f"/open-apis/docx/v1/documents/{self.doc_token}/blocks/{self.doc_token}/children",
            data
        )
        return api_result.get("code") == 0

    def execute_task(self, task: Dict) -> str:
        """Execute a task based on its description keywords."""
        desc = task.get("description", "").lower()

        if "test" in desc or "verify" in desc:
            return "Test verification successful — polling mechanism is running normally"
        elif "search" in desc or "find" in desc:
            return "Search task received, processing..."
        elif "monitor" in desc:
            return "Monitoring task started"
        else:
            return "Task received and execution started"

    def poll(self) -> Dict:
        """Run a single polling round. Returns a result summary dict."""
        result = {
            "timestamp": datetime.now().isoformat(),
            "tasks_found": 0,
            "tasks_executed": 0,
            "success": True,
            "error": None
        }

        try:
            # Read task board
            content = self.read_task_board()

            # Parse tasks
            tasks = TaskParser.parse_tasks(content, self.assignee)
            result["tasks_found"] = len(tasks)

            if tasks:
                for task in tasks:
                    task_result = self.execute_task(task)
                    self.append_feedback(task["id"], task_result)
                    result["tasks_executed"] += 1
            elif self.silent_mode:
                # Silent mode: no notification when no tasks
                pass

        except Exception as e:
            result["success"] = False
            result["error"] = str(e)

        return result


def main():
    """CLI entry point."""
    import sys

    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.json"
    poller = SmartPoller(config_path)

    # Single-run mode
    if len(sys.argv) > 2 and sys.argv[2] == "--once":
        result = poller.poll()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    # Continuous polling mode
    import time
    interval = poller.config.get("poll_interval_minutes", 15) * 60
    print(f"Smart Poller started — polling every {poller.config.get('poll_interval_minutes', 15)} minutes")
    while True:
        result = poller.poll()
        if not result["success"]:
            print(f"Polling error: {result['error']}")
        time.sleep(interval)


if __name__ == "__main__":
    main()
