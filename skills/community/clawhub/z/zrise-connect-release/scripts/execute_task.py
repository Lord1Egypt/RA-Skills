#!/usr/bin/env python3
"""
execute_task.py - Execute single task via selected agent

Simple workflow:
1. Fetch task from Zrise
2. Select appropriate agent (auto or manual)
3. Call selected agent
4. Agent handles everything (including spawning subagents if needed)
5. Return result

Usage:
    python3 execute_task.py --task-id 42174 --workflow simple
    python3 execute_task.py --task-id 42174 --workflow email-draft --feedback "Thêm AC rõ hơn"
    python3 execute_task.py --task-id 42174 --agent demo-be  # Manual agent selection
"""
import argparse
import json
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime, timezone

SCRIPTS_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPTS_DIR))

from zrise_utils import get_root, get_state_path, connect_zrise

ROOT = get_root()


def fetch_task_context(task_id):
    """Fetch task data from Zrise"""
    try:
        db, uid, secret, models, url = connect_zrise()
        if not models:
            return None
        
        # Fetch task
        tasks = models.execute_kw(
            db, uid, secret,
            'project.task', 'read',
            [[task_id]],
            {'fields': ['name', 'description', 'stage_id', 'project_id', 
                       'date_deadline', 'user_ids', 'priority', 'state']}
        )
        
        if not tasks:
            return None
        
        task = tasks[0]
        return {
            'task_id': task_id,
            'name': task.get('name', ''),
            'description': task.get('description', ''),
            'stage': (task.get('stage_id') or [None, ''])[1],
            'project': (task.get('project_id') or [None, ''])[1],
            'deadline': task.get('date_deadline', ''),
            'priority': task.get('priority', '0'),
            'state': task.get('state', ''),
            'link': f"{url}/web#id={task_id}&model=project.task&view_type=form"
        }
    except Exception as e:
        print(f"⚠️ Failed to fetch task: {e}", file=sys.stderr)
        return None


def build_agent_prompt(task_context, workflow, feedback):
    """Build prompt for zrise-worker agent"""
    prompt = f"""Execute task from Zrise:

**Task #{task_context['task_id']}: {task_context['name']}**

**Context:**
- Project: {task_context['project']}
- Stage: {task_context['stage']}
- State: {task_context['state']}
- Priority: {task_context['priority']}
- Deadline: {task_context['deadline']}

**Description:**
{task_context['description'] or 'No description'}

**Workflow:** {workflow}

**Link:** {task_context['link']}
"""
    
    if feedback:
        prompt += f"\n**User Feedback:**\n{feedback}"
    
    prompt += """

**Instructions:**
1. Analyze the task
2. Determine what needs to be done
3. If complex, spawn subagents (using sessions_spawn)
4. Execute the work
5. Generate output
6. Writeback to Zrise (using writeback_to_zrise.py)

**Output Format:**
Return JSON with:
- ok: true/false
- summary: what was done
- output: main output
- files_changed: list of files (if any)
"""
    
    return prompt


def call_agent(task_id, prompt, session_id, agent_id='zrise'):
    """Call selected agent"""
    try:
        # macOS xattr fix
        subprocess.run(['xattr', '-cr', str(SCRIPTS_DIR)], 
                      capture_output=True, timeout=5)
    except Exception:
        pass
    
    # Call agent
    result = subprocess.run(
        [
            'openclaw', 'agent',
            '--agent', agent_id,
            '--local',
            '--session-id', session_id,
            '--message', prompt,
        ],
        capture_output=True, text=True,
        timeout=600,  # 10 minutes
        cwd=str(ROOT),
    )
    
    return result


def main():
    parser = argparse.ArgumentParser(description='Execute task via selected agent')
    parser.add_argument('--task-id', required=True, type=int)
    parser.add_argument('--workflow', default='simple')
    parser.add_argument('--feedback', default='')
    parser.add_argument('--agent', default='', help='Manual agent selection (overrides auto-selection)')
    parser.add_argument('--list-agents', action='store_true', help='List available agents')
    args = parser.parse_args()
    
    # Fetch task context
    print(f"📋 Fetching task #{args.task_id}...")
    task_context = fetch_task_context(args.task_id)
    
    if not task_context:
        print(f"❌ Failed to fetch task #{args.task_id}")
        output = {
            'ok': False,
            'task_id': args.task_id,
            'error': 'Failed to fetch task from Zrise'
        }
        print(json.dumps(output, ensure_ascii=False))
        return 1
    
    # Check if task is done/canceled
    if task_context['state'] in ('1_done', '1_canceled'):
        print(f"⚠️ Task #{args.task_id} is already {task_context['state']}")
        output = {
            'ok': True,
            'task_id': args.task_id,
            'status': 'skipped',
            'reason': f"Task is {task_context['state']}"
        }
        print(json.dumps(output, ensure_ascii=False))
        return 0
    
    # Agent selection
    selected_agent = args.agent
    if not selected_agent:
        # Auto-select agent based on task
        print(f"🔍 Auto-selecting agent for task...")
        agent_selector = SCRIPTS_DIR / 'agent_selector.py'
        if agent_selector.exists():
            try:
                result = subprocess.run(
                    [sys.executable, str(agent_selector), 
                     '--task-id', str(args.task_id),
                     '--task-name', task_context.get('name', ''),
                     '--task-description', task_context.get('description', '')],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    selection = json.loads(result.stdout)
                    selected_agent = selection.get('agent_id', 'zrise')
                    print(f"✅ Selected agent: {selection.get('agent_name', selected_agent)} ({selection.get('selection_type', 'auto')})")
                else:
                    selected_agent = 'zrise'
                    print(f"⚠️ Agent selection failed, using default: {selected_agent}")
            except Exception as e:
                selected_agent = 'zrise'
                print(f"⚠️ Agent selection error: {e}, using default: {selected_agent}")
        else:
            selected_agent = 'zrise'
            print(f"⚠️ Agent selector not found, using default: {selected_agent}")
    
    # Build agent prompt
    prompt = build_agent_prompt(task_context, args.workflow, args.feedback)
    
    # Session ID
    session_id = f'zrise-{args.task_id}'
    
    print(f"\n{'='*60}")
    print(f"  EXECUTING TASK #{args.task_id}")
    print(f"  Agent: {selected_agent}")
    print(f"  Workflow: {args.workflow}")
    print(f"  Session: {session_id}")
    print(f"{'='*60}\n")
    
    # Call agent
    result = call_agent(args.task_id, prompt, session_id, selected_agent)
    
    # Check result
    if result.returncode != 0:
        error_msg = result.stderr[:500] if result.stderr else f'Exit code {result.returncode}'
        print(f"❌ Agent failed: {error_msg}")
        output = {
            'ok': False,
            'task_id': args.task_id,
            'error': error_msg
        }
        print(json.dumps(output, ensure_ascii=False))
        return 1
    
    # Success
    print(f"\n{'='*60}")
    print(f"  ✅ TASK COMPLETED")
    print(f"{'='*60}\n")
    
    output = {
        'ok': True,
        'task_id': args.task_id,
        'workflow': args.workflow,
        'session_id': session_id,
        'summary': f"Task #{args.task_id} executed successfully"
    }
    
    if os.environ.get('ZRISE_JSON_OUTPUT'):
        print(json.dumps(output, ensure_ascii=False))
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
