#!/usr/bin/env python3
"""
Enforced workflow cho xử lý task Zrise.
Chạy từng step, dừng ở approval points chờ human input.

Usage:
    python3 process_task.py --task-id 42349 --message "viết giới thiệu công ty"
    # → chạy đến bước review plan, dừng

    python3 process_task.py --task-id 42349 --approve-plan
    # → approve plan, chạy đến review result, dừng

    python3 process_task.py --task-id 42349 --approve-result
    # → approve result, writeback + timesheet + done

    python3 process_task.py --task-id 42349 --reject-plan "thêm phần về team"
    # → reject plan, AI revise, dừng lại ở review plan mới

    python3 process_task.py --task-id 42349 --reject-result "thêm ví dụ cụ thể"
    # → reject result, AI revise, dừng ở review result mới
"""
import argparse
import json
import sys
from pathlib import Path

import xmlrpc.client

ROOT = Path(__file__).resolve().parent.parent  # skills/zrise-connect/
STATE_DIR = ROOT / '.workflow-state'
STATE_DIR.mkdir(exist_ok=True)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from zrise_utils import get_openclaw_config_path


def get_state(task_id):
    path = STATE_DIR / f'{task_id}.json'
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    return None


def save_state(task_id, data):
    path = STATE_DIR / f'{task_id}.json'
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def connect():
    with open(str(get_openclaw_config_path()), 'r') as f:
        cfg = json.load(f)
    env = cfg['skills']['entries']['zrise-connect']['env']
    url = env['ZRISE_URL'].rstrip('/')
    db = env['ZRISE_DB']
    uid_str = env['ZRISE_USERNAME']
    pwd = env.get('ZRISE_API_KEY')
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common', allow_none=True)
    uid = common.authenticate(db, uid_str, pwd, {})
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object', allow_none=True)
    return url, db, uid, pwd, models


def fetch_task(models, db, uid, pwd, task_id):
    import re
    tasks = models.execute_kw(db, uid, pwd, 'project.task', 'read',
                              [[task_id]], {'fields': ['id', 'name', 'description', 'stage_id', 'project_id', 'date_deadline', 'priority']})
    if not tasks:
        return None
    t = tasks[0]
    raw_desc = t.get('description') or ''
    if not isinstance(raw_desc, str):
        raw_desc = str(raw_desc)
    desc = re.sub('<[^<]+?>', '', raw_desc)
    return {
        'task_id': t['id'],
        'name': t.get('name'),
        'description': desc[:2000] if desc else '',
        'stage': (t.get('stage_id') or [None, 'Unknown'])[1],
        'stage_id': (t.get('stage_id') or [None])[0],
        'project': (t.get('project_id') or [None, 'Unknown'])[1],
        'project_id': (t.get('project_id') or [None])[0],
        'deadline': t.get('date_deadline'),
        'priority': t.get('priority', '0'),
    }


def update_stage(models, db, uid, pwd, task_id, stage_name):
    task = fetch_task(models, db, uid, pwd, task_id)
    if not task:
        return False
    project_id = task['project_id']
    stages = models.execute_kw(db, uid, pwd, 'project.task.type', 'search_read',
                               [[('project_ids', 'in', [project_id])]],
                               {'fields': ['id', 'name']})
    for s in stages:
        if stage_name.lower() in s['name'].lower():
            models.execute_kw(db, uid, pwd, 'project.task', 'write',
                              [task_id, {'stage_id': s['id']}])
            return True
    return False


def post_comment(models, db, uid, pwd, task_id, body):
    return models.execute_kw(db, uid, pwd, 'project.task', 'message_post',
                             [[task_id]], {'body': body, 'message_type': 'comment'})


def fill_timesheet(models, db, uid, pwd, task_id, project_id, hours, description):
    try:
        # search domain: chỉ dùng positional, không pass domain+fields riêng
        emp_ids = models.execute_kw(db, uid, pwd, 'hr.employee', 'search',
                                    [[['user_id', '=', uid]]])
        emp_id = emp_ids[0] if emp_ids else False
        from datetime import date
        models.execute_kw(db, uid, pwd, 'account.analytic.line', 'create',
                          [{'name': description, 'task_id': task_id, 'project_id': project_id,
                            'unit_amount': hours, 'date': date.today().isoformat(),
                            'user_id': uid, 'company_id': 1, 'employee_id': emp_id}])
        return True
    except Exception as e:
        print(f"⚠️ Timesheet failed: {e}")
        return False


def step_fetch(task_id, user_message):
    """Step 1: Fetch task data."""
    url, db, uid, pwd, models = connect()
    task = fetch_task(models, db, uid, pwd, task_id)
    if not task:
        print(f"❌ Task {task_id} not found")
        return None

    state = get_state(task_id) or {'task_id': task_id}
    state.update({
        'current_step': 'plan',
        'status': 'waiting_plan_approval',
        'task': task,
        'user_message': user_message,
        'workflow': 'general',
    })
    save_state(task_id, state)
    print(f"✅ Step 1: Fetched task #{task_id} — {task['name']}")
    print(f"   Stage: {task['stage']} | Project: {task['project']}")
    return state


def step_plan(task_id):
    """Step 2: AI lên plan. Ghi state, agent sẽ đọc và generate plan."""
    state = get_state(task_id)
    if not state:
        print(f"❌ No state for task {task_id}. Run without flags first.")
        return None

    state['status'] = 'waiting_plan_approval'
    state['current_step'] = 'plan'
    save_state(task_id, state)

    task = state['task']
    print(f"\n📋 Step 2: PLAN REQUIRED for task #{task_id}")
    print(f"   Name: {task['name']}")
    print(f"   Description: {task['description'][:200] or '(empty)'}")
    print(f"   User message: {state.get('user_message', '(auto)')}")
    print(f"\n⏸️ AWAITING: Agent needs to generate PLAN and write to state.")
    print(f"   After plan is ready, run: --approve-plan or --reject-plan")
    return state


def save_plan(task_id, plan_text, workflow='general'):
    """Agent calls this after generating plan."""
    state = get_state(task_id)
    if not state:
        print(f"❌ No state for task {task_id}")
        return

    state['plan'] = plan_text
    state['workflow'] = workflow
    state['status'] = 'waiting_plan_approval'
    save_state(task_id, state)

    # Post plan to Zrise
    url, db, uid, pwd, models = connect()
    body = f"<p><b>📝 Plan — AI Workflow ({workflow})</b></p><div style='margin-top:8px'>{plan_text.replace(chr(10), '<br/>')}</div>"
    post_comment(models, db, uid, pwd, task_id, body)

    # Move to In Progress
    update_stage(models, db, uid, pwd, task_id, 'In Process')

    print(f"✅ Plan saved and posted to Zrise. Stage → In Process.")
    print(f"⏸️ AWAITING: --approve-plan or --reject-plan")


def approve_plan(task_id):
    """Step 3: Human approves plan → proceed to execute."""
    state = get_state(task_id)
    if not state:
        print(f"❌ No state for task {task_id}")
        return

    state['status'] = 'plan_approved'
    state['current_step'] = 'execute'
    save_state(task_id, state)

    print(f"✅ Plan APPROVED for task #{task_id}")
    print(f"⏸️ AWAITING: Agent needs to EXECUTE task and save result.")
    print(f"   After execution, run: --approve-result or --reject-result")


def reject_plan(task_id, feedback):
    """Step 3b: Human rejects plan → AI revise."""
    state = get_state(task_id)
    if not state:
        print(f"❌ No state for task {task_id}")
        return

    state['status'] = 'plan_rejected'
    state['plan_feedback'] = feedback
    state['current_step'] = 'revise_plan'
    save_state(task_id, state)

    print(f"❌ Plan REJECTED for task #{task_id}")
    print(f"   Feedback: {feedback}")
    print(f"⏸️ AWAITING: Agent needs to REVISE plan and save again.")


def save_result(task_id, result_text):
    """Agent calls this after executing."""
    state = get_state(task_id)
    if not state:
        print(f"❌ No state for task {task_id}")
        return

    state['result'] = result_text
    state['status'] = 'waiting_result_approval'
    save_state(task_id, state)

    print(f"✅ Result saved for task #{task_id}")
    print(f"⏸️ AWAITING: --approve-result or --reject-result")


def approve_result(task_id):
    """Step 5: Human approves result → writeback + timesheet + done."""
    state = get_state(task_id)
    if not state:
        print(f"❌ No state for task {task_id}")
        return

    url, db, uid, pwd, models = connect()
    task = fetch_task(models, db, uid, pwd, task_id)
    if not task:
        return

    # 1. Writeback result to Zrise
    result = state.get('result', '(no result)')
    body = f"<p><b>✅ Kết quả — AI Workflow ({state.get('workflow', 'general')})</b></p><div style='margin-top:8px'>{result.replace(chr(10), '<br/>')}</div>"
    post_comment(models, db, uid, pwd, task_id, body)
    print("✅ Writeback result to Zrise")

    # 2. Fill timesheet
    fill_timesheet(models, db, uid, pwd, task_id, task['project_id'], 0.5,
                   f"AI workflow: {state.get('workflow', 'general')} - Task #{task_id}")
    print("✅ Timesheet logged (0.5h)")

    # 3. Stage Done
    update_stage(models, db, uid, pwd, task_id, 'Done')
    print("✅ Stage → Done")

    state['status'] = 'completed'
    save_state(task_id, state)
    print(f"\n🎉 Task #{task_id} COMPLETED!")


def reject_result(task_id, feedback):
    """Step 5b: Human rejects result → AI revise."""
    state = get_state(task_id)
    if not state:
        print(f"❌ No state for task {task_id}")
        return

    state['status'] = 'result_rejected'
    state['result_feedback'] = feedback
    state['current_step'] = 'revise_result'
    save_state(task_id, state)

    print(f"❌ Result REJECTED for task #{task_id}")
    print(f"   Feedback: {feedback}")
    print(f"⏸️ AWAITING: Agent needs to REVISE result and save again.")


def show_status(task_id):
    state = get_state(task_id)
    if not state:
        print(f"❌ No workflow state for task {task_id}")
        return
    print(json.dumps(state, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description='Enforced Zrise task workflow')
    parser.add_argument('--task-id', type=int, required=True)
    parser.add_argument('--message', default='')
    # Control flow flags
    parser.add_argument('--save-plan', action='store_true', help='Agent: save plan to state')
    parser.add_argument('--save-result', action='store_true', help='Agent: save result to state')
    parser.add_argument('--plan-text', default='', help='Plan content (with --save-plan)')
    parser.add_argument('--result-text', default='', help='Result content (with --save-result)')
    parser.add_argument('--workflow', default='general', help='Workflow type')
    # Approval/rejection
    parser.add_argument('--approve-plan', action='store_true')
    parser.add_argument('--reject-plan', action='store_true')
    parser.add_argument('--approve-result', action='store_true')
    parser.add_argument('--reject-result', action='store_true')
    parser.add_argument('--feedback', default='')
    # Status
    parser.add_argument('--status', action='store_true', help='Show current workflow state')
    args = parser.parse_args()

    tid = args.task_id

    if args.status:
        show_status(tid)
    elif args.approve_plan:
        approve_plan(tid)
    elif args.reject_plan:
        reject_plan(tid, args.feedback)
    elif args.approve_result:
        approve_result(tid)
    elif args.reject_result:
        reject_result(tid, args.feedback)
    elif args.save_plan:
        plan = args.plan_text or sys.stdin.read() if not sys.stdin.isatty() else ''
        save_plan(tid, plan, args.workflow)
    elif args.save_result:
        result = args.result_text or sys.stdin.read() if not sys.stdin.isatty() else ''
        save_result(tid, result)
    else:
        # Start workflow: fetch + wait for plan
        step_fetch(tid, args.message)
        step_plan(tid)


if __name__ == '__main__':
    main()
