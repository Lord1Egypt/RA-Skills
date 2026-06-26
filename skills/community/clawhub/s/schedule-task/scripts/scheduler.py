#!/usr/bin/env python3
"""
Task Scheduler - Manage cron jobs programmatically
"""

import os
import sys
import json
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

TASKS_FILE = os.path.expanduser("~/.config/jack-scheduler/tasks.json")


def load_tasks():
    """Load tasks from JSON file."""
    os.makedirs(os.path.dirname(TASKS_FILE), exist_ok=True)
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE) as f:
            return json.load(f)
    return []


def save_tasks(tasks):
    """Save tasks to JSON file."""
    os.makedirs(os.path.dirname(TASKS_FILE), exist_ok=True)
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)


def validate_cron(expression):
    """Validate cron expression."""
    parts = expression.split()
    if len(parts) != 5:
        return False, "Cron expression must have 5 parts"
    return True, "Valid"


def add_task(args):
    """Add a new scheduled task."""
    valid, msg = validate_cron(args.cron)
    if not valid:
        print(f"Error: {msg}")
        return 1
    
    tasks = load_tasks()
    task_id = len(tasks) + 1
    
    task = {
        'id': task_id,
        'name': args.name or f"task-{task_id}",
        'cron': args.cron,
        'command': args.command,
        'log': args.log,
        'notify': args.notify,
        'timeout': args.timeout,
        'enabled': True,
        'created': datetime.now().isoformat()
    }
    
    tasks.append(task)
    save_tasks(tasks)
    
    # Add to crontab
    add_to_crontab(task)
    
    print(f"Task {task_id} added: {args.name or args.command}")
    print(f"  Schedule: {args.cron}")
    return 0


def add_to_crontab(task):
    """Add task to system crontab."""
    try:
        # Get current crontab
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        current = result.stdout if result.returncode == 0 else ""
        
        # Add new line
        log_redirect = f" >> {task['log']} 2>&1" if task.get('log') else ""
        line = f"{task['cron']} {task['command']}{log_redirect}\n"
        
        # Write new crontab
        new_crontab = current + line
        proc = subprocess.Popen(['crontab', '-'], stdin=subprocess.PIPE)
        proc.communicate(input=new_crontab.encode())
        
    except Exception as e:
        print(f"Warning: Could not add to crontab: {e}")


def list_tasks(args):
    """List all scheduled tasks."""
    tasks = load_tasks()
    if not tasks:
        print("No tasks scheduled")
        return 0
    
    print(f"{'ID':<4} {'Name':<20} {'Schedule':<20} {'Command':<30} {'Status'}")
    print("-" * 90)
    for task in tasks:
        status = "enabled" if task.get('enabled', True) else "disabled"
        cmd = task['command'][:28] + ".." if len(task['command']) > 30 else task['command']
        print(f"{task['id']:<4} {task['name']:<20} {task['cron']:<20} {cmd:<30} {status}")
    return 0


def remove_task(args):
    """Remove a scheduled task."""
    tasks = load_tasks()
    task_id = int(args.id)
    
    tasks = [t for t in tasks if t['id'] != task_id]
    save_tasks(tasks)
    
    # Rebuild crontab
    rebuild_crontab(tasks)
    
    print(f"Task {task_id} removed")
    return 0


def rebuild_crontab(tasks):
    """Rebuild crontab from tasks."""
    try:
        lines = []
        for task in tasks:
            if task.get('enabled', True):
                log_redirect = f" >> {task['log']} 2>&1" if task.get('log') else ""
                lines.append(f"{task['cron']} {task['command']}{log_redirect}")
        
        new_crontab = "\n".join(lines) + "\n"
        if new_crontab.strip():
            proc = subprocess.Popen(['crontab', '-'], stdin=subprocess.PIPE)
            proc.communicate(input=new_crontab.encode())
    except Exception as e:
        print(f"Warning: Could not rebuild crontab: {e}")


def enable_task(args):
    """Enable a task."""
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == int(args.id):
            task['enabled'] = True
            save_tasks(tasks)
            rebuild_crontab(tasks)
            print(f"Task {args.id} enabled")
            return 0
    print(f"Task {args.id} not found")
    return 1


def disable_task(args):
    """Disable a task."""
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == int(args.id):
            task['enabled'] = False
            save_tasks(tasks)
            rebuild_crontab(tasks)
            print(f"Task {args.id} disabled")
            return 0
    print(f"Task {args.id} not found")
    return 1


def show_log(args):
    """Show task log."""
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == int(args.id):
            if task.get('log') and os.path.exists(task['log']):
                with open(task['log']) as f:
                    print(f.read())
            else:
                print("No log file")
            return 0
    print(f"Task {args.id} not found")
    return 1


def health_check(args):
    """Check task health."""
    tasks = load_tasks()
    print("Task Health Status")
    print("=" * 50)
    for task in tasks:
        status = "✓ OK" if task.get('enabled', True) else "✗ Disabled"
        print(f"{task['id']}. {task['name']}: {status}")
    return 0


def main():
    parser = argparse.ArgumentParser(description='Task Scheduler')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Add command
    parser_add = subparsers.add_parser('add', help='Add a new task')
    parser_add.add_argument('--cron', required=True, help='Cron expression')
    parser_add.add_argument('--command', required=True, help='Command to run')
    parser_add.add_argument('--name', help='Task name')
    parser_add.add_argument('--log', help='Log file path')
    parser_add.add_argument('--notify', help='Email on failure')
    parser_add.add_argument('--timeout', type=int, help='Timeout in seconds')
    
    # List command
    subparsers.add_parser('list', help='List all tasks')
    
    # Remove command
    parser_remove = subparsers.add_parser('remove', help='Remove a task')
    parser_remove.add_argument('--id', required=True, help='Task ID')
    
    # Enable command
    parser_enable = subparsers.add_parser('enable', help='Enable a task')
    parser_enable.add_argument('--id', required=True, help='Task ID')
    
    # Disable command
    parser_disable = subparsers.add_parser('disable', help='Disable a task')
    parser_disable.add_argument('--id', required=True, help='Task ID')
    
    # Log command
    parser_log = subparsers.add_parser('log', help='Show task log')
    parser_log.add_argument('--id', required=True, help='Task ID')
    
    # Health command
    subparsers.add_parser('health', help='Check task health')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    commands = {
        'add': add_task,
        'list': list_tasks,
        'remove': remove_task,
        'enable': enable_task,
        'disable': disable_task,
        'log': show_log,
        'health': health_check
    }
    
    return commands.get(args.command, lambda a: 1)(args)


if __name__ == '__main__':
    sys.exit(main())
