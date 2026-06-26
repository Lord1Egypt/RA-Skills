#!/usr/bin/env python3
import sys
import json
import os
import requests

# --- Configuration ---
API_URL = "https://api.todoist.com/api/v2"
CONFIG_PATH = "./skills/todoist-manager/references/API_CONFIG.json"
# ---------------------

def load_config():
    try:
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
        
        todoist_token = config.get("todoist_api_token")
        sync_flag = config.get("sync_on_command", True) # Default to true if not present
        
        if not todoist_token or todoist_token == "PUT_YOUR_REAL_TOKEN_HERE_NOW":
            print("ERROR: Todoist API token not configured in API_CONFIG.json.", file=sys.stderr)
            return None, None
        return todoist_token, sync_flag
        
    except FileNotFoundError:
        print(f"ERROR: Configuration file not found at {CONFIG_PATH}", file=sys.stderr)
        return None, None
    except json.JSONDecodeError:
        print(f"ERROR: Invalid JSON format in {CONFIG_PATH}", file=sys.stderr)
        return None, None

def check_config():
    return load_config()

def get_headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

def handle_api_call(method, endpoint, token, data=None, params=None):
    url = f"{API_URL}{endpoint}"
    try:
        response = requests.request(
            method,
            url,
            headers=get_headers(token),
            json=data,
            params=params,
            timeout=10
        )
        response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
        
        if response.status_code == 204:
            return None
        return response.json()
        
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error {response.status_code}: {response.text}", file=sys.stderr)
        return {"error": f"HTTP Error {response.status_code}"}
    except requests.exceptions.RequestException as e:
        print(f"Connection Error: {e}", file=sys.stderr)
        return {"error": "Connection Error"}

def sync_data(token):
    print("--- EXECUTING TODOIST API: SYNC ---")
    endpoint = "/sync"
    sync_payload = {
        "sync_token": "*",
        "resource_types": ["all"]
    }
    
    result = handle_api_call("POST", endpoint, token, data=sync_payload)
    
    if result and "sync_token" in result:
        print(f"SUCCESS: Sync completed. New sync_token: {result.get('sync_token')}", file=sys.stderr)
    elif result:
        print(f"FAILED to sync: {result.get('error')}", file=sys.stderr)
    return 0

def add_task(content, token, project_id=None, due_date=None, priority=None):
    print("--- EXECUTING TODOIST API: ADD TASK ---")
    
    payload = {
        "content": content,
        "priority": int(priority) if priority and 1 <= int(priority) <= 4 else 4,
    }
    if project_id:
        payload["project_id"] = project_id
    if due_date:
        payload["due_string"] = due_date
        
    result = handle_api_call("POST", "/tasks", token, data=payload)
    
    if result and "error" not in result:
        print("SUCCESS: Задача добавлена.")
    elif result:
        print(f"FAILED: Не удалось добавить задачу: {result.get('error')}")
    
    return 0

def complete_task(task_id, token):
    print("--- EXECUTING TODOIST API: COMPLETE TASK ---")
    endpoint = f"/tasks/{task_id}/close"
    result = handle_api_call("POST", endpoint, token)
    
    if result is None:
        print("SUCCESS: Задача отмечена как выполненная.")
    else:
        print(f"FAILED: Не удалось отметить задачу {task_id}: {result.get('error')}")
    return 0

def delete_task(task_id, token):
    print("--- EXECUTING TODOIST API: DELETE TASK ---")
    endpoint = f"/tasks/{task_id}"
    result = handle_api_call("DELETE", endpoint, token)
    
    if result is None:
        print("SUCCESS: Задача удалена.")
    else:
        print(f"FAILED: Не удалось удалить задачу {task_id}: {result.get('error')}")
    return 0

def list_projects(token):
    print("--- EXECUTING TODOIST API: LIST PROJECTS ---")
    endpoint = "/projects"
    result = handle_api_call("GET", endpoint, token)
    
    if isinstance(result, list):
        print("SUCCESS: Список проектов получен.")
        for project in result:
             print(f"ID: {project.get('id')}, Name: {project.get('name')}")
    elif result and "error" in result:
        print(f"FAILED to list projects: {result.get('error')}", file=sys.stderr)
    return 0

def list_tasks(token):
    print("--- EXECUTING TODOIST API: LIST TASKS ---")
    endpoint = "/tasks"
    result = handle_api_call("GET", endpoint, token)
    
    if isinstance(result, list):
        print("SUCCESS: Список задач получен.")
        for task in result:
             print(f"Задача: {task.get('content')} (Проект ID: {task.get('project_id')})")
    elif result and "error" in result:
        print(f"FAILED to list tasks: {result.get('error')}", file=sys.stderr)
    return 0

def main():
    config = check_config()
    if not config:
        sys.exit(1)
    
    token, sync_flag = config

    if len(sys.argv) < 2:
        print("Usage: ./todoist_api.py <command> [args...]", file=sys.stderr)
        sys.exit(1)

    if sync_flag:
        sync_data(token)
        
    command = sys.argv[1]
    
    try:
        if command == "add_task":
            args_dict = {}
            i = 2
            while i < len(sys.argv):
                if sys.argv[i].startswith("--"):
                    key = sys.argv[i][2:]
                    if i + 1 < len(sys.argv) and not sys.argv[i+1].startswith("--"):
                        args_dict[key] = sys.argv[i+1]
                        i += 2
                    else:
                        args_dict[key] = None
                        i += 1
                else:
                    i += 1
            
            content = args_dict.get("content")
            if not content:
                print("Error: 'add_task' requires --content argument.", file=sys.stderr)
                sys.exit(1)

            add_task(
                content, token,
                project_id=args_dict.get("project_id"), 
                due_date=args_dict.get("due_date"), 
                priority=args_dict.get("priority")
            )
        elif command == "complete_task":
            task_id = next((sys.argv[i + 1] for i, x in enumerate(sys.argv) if x == "--task_id" and i + 1 < len(sys.argv)), None)
            if task_id:
                complete_task(task_id, token)
            else:
                print("Error: 'complete_task' requires --task_id argument.", file=sys.stderr)
                sys.exit(1)
        elif command == "delete_task":
            task_id = next((sys.argv[i + 1] for i, x in enumerate(sys.argv) if x == "--task_id" and i + 1 < len(sys.argv)), None)
            if task_id:
                delete_task(task_id, token)
            else:
                print("Error: 'delete_task' requires --task_id argument.", file=sys.stderr)
                sys.exit(1)
        elif command == "list_projects":
            list_projects(token)
        elif command == "list_tasks":
            list_tasks(token)
        else:
            print(f"Unknown command: '{command}'", file=sys.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"An unexpected error occurred during command execution: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()