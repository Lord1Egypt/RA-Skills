#!/usr/bin/env python3
"""
Todo Batch Creator

Create multiple todos from a JSON file.
Usage: python todo_batch_create.py tasks.json [--executors user1,user2]
"""

import argparse
import subprocess
import json
import sys


def run_dws(args, execute=False):
    """Run dws command.
    
    Args:
        args: Command arguments
        execute: If True, add --yes to perform mutation. Default is False (dry-run).
    
    Safety: Defaults to dry-run mode. Must explicitly pass execute=True to mutate.
    """
    cmd = ["dws"] + args
    if execute:
        cmd.append("--yes")
    else:
        cmd.append("--dry-run")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        return False
    print(result.stdout)
    return True


def create_todo(title, executors, priority=None, due_date=None, description=None, dry_run=False):
    """Create a single todo."""
    args = [
        "todo", "task", "create",
        "--title", title,
        "--executors", executors
    ]
    
    if priority:
        args.extend(["--priority", str(priority)])
    if due_date:
        args.extend(["--due-date", due_date])
    if description:
        args.extend(["--description", description])
    
    return run_dws(args, dry_run)


def main():
    parser = argparse.ArgumentParser(description="Batch create todos from JSON")
    parser.add_argument("input_file", help="JSON file with tasks")
    parser.add_argument("--executors", help="Default executors (comma-separated)")
    parser.add_argument("--execute", action="store_true", help="Actually create todos (default is dry-run)")
    
    args = parser.parse_args()
    
    # Safety: Default to dry-run
    execute = args.execute
    
    # Load tasks
    try:
        with open(args.input_file, "r") as f:
            tasks = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {args.input_file}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Ensure tasks is a list
    if isinstance(tasks, dict):
        tasks = tasks.get("tasks", [tasks])
    
    print(f"Processing {len(tasks)} tasks...")
    
    success_count = 0
    for i, task in enumerate(tasks, 1):
        title = task.get("title")
        if not title:
            print(f"Task {i}: Missing title, skipping")
            continue
        
        executors = task.get("executors", args.executors)
        if not executors:
            print(f"Task {i}: Missing executors, skipping")
            continue
        
        priority = task.get("priority")
        due_date = task.get("due_date") or task.get("due-date")
        description = task.get("description")
        
        print(f"\n[{i}/{len(tasks)}] Creating: {title}")
        if create_todo(title, executors, priority, due_date, description, execute=execute):
            success_count += 1
    
    print(f"\nCompleted: {success_count}/{len(tasks)} tasks created")


if __name__ == "__main__":
    main()
