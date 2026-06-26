#!/usr/bin/env python3
"""
Task recovery check for heartbeat - Python version
"""

import sys
import subprocess
import os
from pathlib import Path

def find_workspace_root():
    """Find workspace root directory"""
    script_dir = Path(__file__).parent
    
    # Try relative path from script location
    # scripts -> smarter-task-planner -> skills -> .openclaw -> workspace
    relative_path = script_dir.parent.parent.parent / "workspace"
    if relative_path.exists():
        return str(relative_path)
    
    # Try common locations
    potential_paths = []
    
    # Windows APPDATA
    if 'APPDATA' in os.environ:
        # Generic path without username
        appdata_root = Path(os.environ['APPDATA']).parent
        for dir_name in ['.openclaw', 'openclaw']:
            workspace_path = appdata_root / dir_name / 'workspace'
            potential_paths.append(workspace_path)
    
    # User home directory
    home = Path.home()
    potential_paths.extend([
        home / '.openclaw' / 'workspace',
        home / 'openclaw' / 'workspace',
    ])
    
    # Check all potential paths
    for path in potential_paths:
        if path.exists():
            return str(path)
    
    # Fallback to relative path (might not exist)
    return str(relative_path)

def main():
    mode = "check"
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    
    workspace_root = find_workspace_root()
    
    if not os.path.exists(workspace_root):
        print(f"ERROR: Workspace directory not found: {workspace_root}")
        print("INFO: Make sure OpenClaw is properly installed and workspace exists")
        return 1
    
    script_dir = Path(__file__).parent
    manager_script = script_dir / "task-memory-manager.py"
    
    if not manager_script.exists():
        print("ERROR: Cannot find task-memory-manager.py")
        return 1
    
    os.chdir(workspace_root)
    
    try:
        # Run scan command
        result = subprocess.run(
            ['py', str(manager_script), 'scan'],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode != 0:
            print("ERROR: Scan failed")
            return result.returncode
        
        output = result.stdout
        
        active_tasks = []
        for line in output.strip().split('\n'):
            if not line.strip():
                continue
            
            # Parse line format: task_id - status - current_step
            parts = line.split(' - ')
            if len(parts) >= 2:
                task_id = parts[0].strip()
                status = parts[1].strip()
                
                # Check for active status
                if status in ['进行中', '已暂停']:
                    active_tasks.append({
                        'task_id': task_id,
                        'status': status,
                        'current_step': parts[2].strip() if len(parts) > 2 else ''
                    })
        
        if not active_tasks:
            print("OK: No active tasks found")
            return 0
        
        print(f"INFO: Found {len(active_tasks)} active tasks:")
        for task in active_tasks:
            print(f"  - {task['task_id']} [{task['status']}]")
        
        if mode == "check":
            print("\nINFO: Use '恢复上次任务' or run: py task-memory-manager.py recovery")
        elif mode == "notify":
            print("\nINFO: Active tasks found")
            print("INFO: Use '恢复上次任务' to continue")
        elif mode == "auto-recover":
            if active_tasks:
                latest_task = active_tasks[0]['task_id']
                print(f"\nINFO: Auto-recovering: {latest_task}")
                subprocess.run([
                    'py', str(manager_script), 'load', 
                    '--task-ids', latest_task,
                    '--max-per-task', '5'
                ])
        
        return len(active_tasks)
        
    except Exception as e:
        print(f"ERROR: Execution failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())