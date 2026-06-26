#!/usr/bin/env python3
"""
workflow_manager_ui.py — Web UI for workflow management + Zrise tasks.

KIẾN TRÚC MỚI (Lobster + registry + cron post-processing):
  - Lobster Workflow Engine: Xử lý AI + 2 approval gates (plan + result)
  - Registry/State Store: Lưu trữ kết quả trung gian trong .tasks/<task_id>/
  - Cron Post-Processing: Tự động writeback → timesheet → stage Done

Endpoints:
  Workflows:
    GET  /api/workflows              — List all workflows
    POST /api/workflows              — Create workflow
    GET  /api/workflows/:id          — Get workflow details
    PUT  /api/workflows/:id          — Update workflow
    DEL  /api/workflows/:id          — Delete workflow
    GET  /api/workflows/:id/yaml     — Get workflow YAML
  Tasks:
    GET  /api/tasks                  — List Zrise tasks for current user
    GET  /api/tasks/:id              — Get task details
    POST /api/tasks/:id/run          — Trigger Lobster workflow (fetch → analyze → plan → post plan → In Process)
    POST /api/tasks/:id/approve      — Approve workflow step (plan hoặc result, KHÔNG trực tiếp change stage)
                                       → Ghi vào .tasks/<task_id>/plan_approved hoặc result_approved
                                       → Lobster hoặc cron post-processing sẽ đọc file này để tiếp tục
"""
import argparse
import json
import os
import re
import sys
import subprocess
import threading
import time
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

SCRIPTS_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPTS_DIR))

from zrise_utils import get_root, connect_zrise

ROOT = get_root()


def _zrise_url():
    """Get Zrise base URL from config."""
    try:
        cfg = json.loads(pathlib.Path.home().joinpath('.openclaw', 'openclaw.json').read_text())
        return cfg['skills']['entries']['zrise-connect']['env']['ZRISE_URL'].rstrip('/')
    except Exception:
        return 'https://zrise.app'
WORKFLOWS_DIR = ROOT / 'workflows' / 'employee-workflows'
REGISTRY_FILE = ROOT / 'workflows' / 'registry.json'

# ── Helper functions cho kiến trúc mới (Lobster + registry + cron post-processing) ──

def fetch_task_data_from_zrise(models, db, uid, secret, task_id):
    """Lấy thông tin task từ Zrise qua XML-RPC."""
    try:
        # Lưu ý: 'stage' không phải là field trực tiếp, phải dùng 'stage_id' hoặc fetch riêng
        task_data = models.execute_kw(db, uid, secret, 'project.task', 'read', [[int(task_id)]], {'fields': ['id', 'name', 'description', 'stage_id', 'user_ids', 'priority', 'date_deadline']})
        if task_data and len(task_data) > 0:
            task = task_data[0]
            # Nếu có stage_id, lấy name của stage từ model project.task.type
            # stage_id có thể là list [id, name] hoặc int
            if 'stage_id' in task:
                stage_id_val = task['stage_id']
                if isinstance(stage_id_val, list) and len(stage_id_val) >= 2:
                    # Format: [id, name] → lấy name trực tiếp
                    task['stage'] = stage_id_val[1]
                elif isinstance(stage_id_val, int):
                    # Chỉ có id → cần fetch riêng
                    stage_data = models.execute_kw(db, uid, secret, 'project.task.type', 'read', [[stage_id_val]], {'fields': ['name']})
                    if stage_data and len(stage_data) > 0:
                        task['stage'] = stage_data[0].get('name', 'Unknown')
                    else:
                        task['stage'] = 'Unknown'
                else:
                    task['stage'] = 'Unknown'
            else:
                task['stage'] = 'Unknown'
            return task
        return {'stage': 'Unknown'}
    except Exception as e:
        print(f"Error fetching task data: {e}")
        return {'stage': 'Unknown'}

def check_if_task_has_ai_result(task_id):
    """Kiểm tra xem task đã có kết quả AI chưa (trong registry hoặc comments)."""
    # Kiểm tra trong thư mục .tasks/<task_id>/ xem có result.md hoặc result.json không
    task_dir = SCRIPTS_DIR.parent / '.tasks' / str(task_id)
    if task_dir.exists():
        result_file = task_dir / 'result.md'
        if result_file.exists() and result_file.stat().st_size > 50:
            # Có file result.md với nội dung đáng kể → đã có kết quả AI
            content = result_file.read_text(encoding='utf-8')
            # Nếu content không phải là lỗi CLI error → có kết quả AI
            if not content.strip().startswith('CLI error'):
                return True
    
    # Kiểm tra trong comments trên Zrise xem có comment nào chứa kết quả AI không
    try:
        db, uid, secret, models, url = connect_zrise()
        comments = models.execute_kw(db, uid, secret, 'project.task', 'read', [[int(task_id)]], {'fields': ['message_ids']})
        if comments and len(comments) > 0 and 'message_ids' in comments[0]:
            msg_ids = comments[0]['message_ids']
            if msg_ids:
                messages = models.execute_kw(db, uid, secret, 'mail.message', 'read', [[msg_ids]], {'fields': ['body', 'message_type']})
                if messages:
                    for msg in messages:
                        if msg.get('message_type') == 'comment' and msg.get('body'):
                            body = msg['body']
                            # Kiểm tra xem body có chứa dấu hiệu của kết quả AI không
                            if '✅ Kết quả' in body or 'AI Workflow Result' in body or 'Hoàn thành task' in body:
                                return True
    except Exception as e:
        print(f"Error checking comments: {e}")
    
    return False

def get_current_user():
    """Lấy username hiện tại từ environment hoặc config."""
    return os.environ.get('USER', os.environ.get('USERNAME', 'unknown'))

# ── Quản lý tiến trình con để tránh zombie ──
_background_procs = {}  # {pid: Popen}

def _watch_process(proc, task_id, phase):
    """Thread chạy ngầm: chờ proc xong, thu output, cập nhật session state."""
    stdout, stderr = proc.communicate()
    pid = proc.pid
    _background_procs.pop(pid, None)
    exit_code = proc.returncode
    print(f"[workflow] PID {pid} (task={task_id}, phase={phase}) exited with code {exit_code}")

    # Update session state so UI can see progress
    try:
        ctx, session_dir, ctx_path = _resolve_session_path(task_id)
        if ctx is None:
            # Create session state
            sessions_dir = ROOT / 'state' / 'zrise' / 'sessions'
            sessions_dir.mkdir(parents=True, exist_ok=True)
            ctx_path = sessions_dir / f'zrise-task-{task_id}.json'
            ctx = {'session_id': f'zrise-task-{task_id}', 'task_id': int(task_id),
                   'created_at': datetime.now(timezone.utc).isoformat()}

        # Parse pipeline output for progress
        import re as _re
        result_summary = ''
        if stdout:
            for line in stdout.decode('utf-8', errors='replace').strip().split('\n'):
                line = line.strip()
                if line.startswith('{'):
                    try:
                        evt = json.loads(line)
                        if evt.get('kind') == 'result':
                            result_summary = evt.get('result_summary', '')
                    except Exception:
                        pass

        # Map phase to step
        step_map = {'plan': 'agent_plan', 'execute': 'agent_execute', 'approve': 'agent_approve'}
        # Clear previous error before this run
        ctx.pop('error', None)
        if exit_code == 0:
            ctx['current_step'] = step_map.get(phase, phase)
            ctx['status'] = 'completed' if phase == 'approve' else 'awaiting_review'
            if result_summary:
                ctx['last_result'] = result_summary
        else:
            ctx['status'] = 'failed'
            ctx['error'] = (stderr.decode('utf-8', errors='replace') or '')[:1000]
            ctx['current_step'] = step_map.get(phase, phase)

        ctx['updated_at'] = datetime.now(timezone.utc).isoformat()
        ctx_path.write_text(json.dumps(ctx, indent=2, ensure_ascii=False), encoding='utf-8')
    except Exception as e:
        print(f"[workflow] Failed to update session state for task={task_id}: {e}")

def launch_workflow(cmd, task_id, phase, cwd, env):
    """Khởi chạy workflow trong tiến trình con + thread giám sát để tránh zombie.
    
    macOS xattr provenance fix: tự clear com.apple.provenance trên file Python
    để tránh "cannot execute" error khi subprocess gọi script.
    """
    import subprocess as _sp
    # Clear provenance xattr cho script chính và scripts/ dir
    for p in list(SCRIPTS_DIR.glob('*.py')):
        try:
            _sp.run(['xattr', '-d', 'com.apple.provenance', str(p)],
                     capture_output=True, timeout=5)
            _sp.run(['xattr', '-d', 'com.apple.quarantine', str(p)],
                     capture_output=True, timeout=5)
        except Exception:
            pass

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            cwd=cwd, env=env)
    _background_procs[proc.pid] = proc
    t = threading.Thread(target=_watch_process, args=(proc, task_id, phase), daemon=True)
    t.start()
    return proc


def get_current_user():
    return os.environ.get('OPENCLAW_USER', 'khoa')


def get_auth_token():
    token = os.environ.get('WORKFLOW_UI_TOKEN')
    if not token:
        try:
            cfg = json.loads(open(os.path.expanduser('~/.openclaw/openclaw.json')).read())
            token = cfg.get('skills', {}).get('entries', {}).get('zrise-connect', {}).get('env', {}).get('WORKFLOW_UI_TOKEN', '')
        except Exception:
            pass
    return token


def check_auth(handler):
    token = get_auth_token()
    if not token:
        return True
    auth = handler.headers.get('Authorization', '')
    return auth == f'Bearer {token}'


def load_registry():
    if not REGISTRY_FILE.exists():
        REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
        REGISTRY_FILE.write_text('{}', encoding='utf-8')
    try:
        return json.loads(REGISTRY_FILE.read_text(encoding='utf-8'))
    except Exception:
        return {}


def save_registry(registry):
    REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY_FILE.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding='utf-8')


def validate_lobster_yaml(yaml_content):
    errors = []
    stripped = '\n'.join(
        line for line in yaml_content.split('\n')
        if not line.strip().startswith('#')
    )
    if not re.search(r'^name:\s*\S+', stripped, re.MULTILINE):
        errors.append("Missing required field: 'name'")
    if not re.search(r'^steps:', stripped, re.MULTILINE):
        errors.append("Missing required field: 'steps'")
    return {'valid': len(errors) == 0, 'errors': errors}


def get_builtin_workflows():
    try:
        from workflow_registry import list_all_workflows
        all_wf = list_all_workflows()
        return {k: v for k, v in all_wf.items() if v.get('source', 'builtin') in ('builtin', None, '')}
    except Exception:
        return {}


def get_all_workflows():
    registry = load_registry()
    builtins = get_builtin_workflows()
    all_wf = {}
    for k, v in builtins.items():
        all_wf[k] = {**v, 'source': 'builtin', 'editable': False}
    for k, v in registry.items():
        all_wf[k] = {**v, 'editable': True}
    return all_wf


def fetch_zrise_tasks(limit=50, stage_filter=None):
    """Fetch tasks for current user from Zrise."""
    try:
        db, uid, secret, models, url = connect_zrise()
        domain = [('user_ids', '=', uid)]
        if stage_filter:
            domain.append(('stage_id', '=', stage_filter))

        fields = ['id', 'name', 'description', 'stage_id', 'project_id',
                  'date_deadline', 'priority', 'create_date', 'write_date']

        tasks = models.execute_kw(db, uid, secret, 'project.task', 'search_read',
            [domain], {'fields': fields, 'limit': limit, 'order': 'write_date desc'})

        # Get project stages for sequence info
        stage_map = {}
        project_ids = set()
        for t in tasks:
            pid = t.get('project_id')
            if isinstance(pid, list) and pid[0]:
                project_ids.add(pid[0])
        for pid in project_ids:
            try:
                proj = models.execute_kw(db, uid, secret, 'project.project', 'read',
                    [[pid], ['type_ids']])
                type_ids = proj[0].get('type_ids', [])
                if type_ids:
                    stages = models.execute_kw(db, uid, secret, 'project.task.type', 'read',
                        [type_ids, ['id', 'name', 'sequence']])
                    for s in stages:
                        stage_map[s['id']] = s
            except Exception:
                pass

        result = []
        for t in tasks:
            stage_id = t.get('stage_id')
            stage_name = stage_id[1] if isinstance(stage_id, list) else str(stage_id)
            stage_seq = stage_map.get(stage_id[0] if isinstance(stage_id, list) else stage_id, {}).get('sequence', 0) if isinstance(stage_id, list) else 0

            project = t.get('project_id')
            project_name = project[1] if isinstance(project, list) else str(project) if project else ''

            priority_map = {'0': 'low', '1': 'normal'}
            priority = priority_map.get(str(t.get('priority', '0')), 'normal')

            result.append({
                'id': t['id'],
                'name': t['name'],
                'stage': stage_name,
                'stage_sequence': stage_seq,
                'project': project_name,
                'priority': priority,
                'deadline': t.get('date_deadline'),
                'created': t.get('create_date'),
                'updated': t.get('write_date'),
                'url': f'{url}/web#id={t["id"]}&model=project.task&view_type=form',
            })
        return result
    except Exception as e:
        return {'error': str(e)}


def _resolve_session_path(task_id):
    """Resolve session for a given task_id.

    Supports multiple storage formats:
    1. state/zrise/sessions/{task_id}/context.json  (dir-based)
    2. state/zrise/sessions/zrise-task-{task_id}.json (flat file)
    3. state/zrise/sessions/{task_id}.json (flat file)
    Returns (ctx_dict_or_None, session_dir_or_None, ctx_path_or_None).
    """
    sessions_dir = ROOT / 'state' / 'zrise' / 'sessions'
    task_str = str(task_id)

    # Dir-based: sessions/{task_id}/context.json
    d = sessions_dir / task_str
    if d.is_dir():
        ctx_file = d / 'context.json'
        if ctx_file.exists():
            return json.loads(ctx_file.read_text(encoding='utf-8')), d, ctx_file

    # Flat file: zrise-task-{id}.json
    flat = sessions_dir / f'zrise-task-{task_str}.json'
    if flat.exists():
        return json.loads(flat.read_text(encoding='utf-8')), sessions_dir, flat

    # Flat file: {id}.json
    flat2 = sessions_dir / f'{task_str}.json'
    if flat2.exists():
        return json.loads(flat2.read_text(encoding='utf-8')), sessions_dir, flat2

    return None, None, None


def _get_task_name_from_zrise(task_id):
    """Fetch task_name from Zrise API if not in session state."""
    try:
        tasks = fetch_zrise_tasks(limit=200)
        if isinstance(tasks, list):
            t = next((t for t in tasks if t['id'] == task_id), None)
            if t:
                return t.get('name', ''), t.get('project', ''), t.get('stage', '')
    except Exception:
        pass
    return '', '', ''


def _default_timeline(task_id, status='no_session', task_name='', project='', stage=''):
    """Build default timeline response."""
    return {
        'ok': True, 'task_id': task_id, 'task_name': task_name, 'project': project, 'stage': stage,
        'workflow': '-', 'current_step': '-', 'current_phase': 'plan',
        'iteration': '0', 'total_turns': '0', 'status': status,
        'phases': [
            {'name': 'plan', 'label': '📋 Plan', 'steps': [{'id': 'agent_plan', 'icon': '🤖', 'desc': 'Agent: Fetch + Analyze + Plan', 'state': 'upcoming'}]},
            {'name': 'execute', 'label': '⚡ Execute', 'steps': [{'id': 'agent_execute', 'icon': '🧠', 'desc': 'Agent: Thực thi theo plan', 'state': 'upcoming'}]},
            {'name': 'approve', 'label': '✅ Approve', 'steps': [{'id': 'agent_approve', 'icon': '✅', 'desc': 'Agent: Mark Done + Notify', 'state': 'upcoming'}]},
        ],
        'logs': [],
    }


def get_session_timeline(task_id):
    """Get full timeline for a session with step states and logs."""
    import re as _re
    ctx, session_dir, ctx_path = _resolve_session_path(task_id)

    if ctx is None:
        # Try to get task_name from Zrise
        tn, proj, stg = _get_task_name_from_zrise(task_id)
        return _default_timeline(task_id, task_name=tn, project=proj, stage=stg)

    # Ensure task_name — fetch from Zrise if missing
    if not ctx.get('task_name'):
        tn, proj, stg = _get_task_name_from_zrise(task_id)
        if tn:
            ctx['task_name'] = tn
            if proj and not ctx.get('project'):
                ctx['project'] = proj
            if stg and not ctx.get('stage'):
                ctx['stage'] = stg
            # Persist
            if ctx_path:
                ctx_path.write_text(json.dumps(ctx, indent=2, ensure_ascii=False), encoding='utf-8')

    turns = []
    if session_dir and session_dir.is_dir():
        turns_file = session_dir / 'turns.json'
    else:
        turns_file = ROOT / 'state' / 'zrise' / 'sessions' / f'zrise-task-{task_id}-turns.json'
    if turns_file.exists():
        turns_data = json.loads(turns_file.read_text(encoding='utf-8'))
        turns = turns_data.get('turns', []) if isinstance(turns_data, dict) else (turns_data if isinstance(turns_data, list) else [])

    # Build turn logs per step
    step_logs = {}
    for turn in turns:
        sid = turn.get('step', '')
        if sid:
            step_logs.setdefault(sid, []).append({
                'role': turn.get('role', ''), 'agent': turn.get('agent', ''),
                'author': turn.get('author', ''), 'content': (turn.get('content', '') or '')[:500],
                'timestamp': turn.get('timestamp', ''),
            })

    current_step = ctx.get('current_step', '')
    workflow = ctx.get('workflow', 'general')
    stage = ctx.get('stage', '')

    # Bug 1 fix: Sync stage from Zrise API if local state is stale
    is_zrise_done = stage and any(keyword in stage.lower() for keyword in ['done', 'closed', 'completed'])
    if not is_zrise_done:
        try:
            tasks = fetch_zrise_tasks(limit=200)
            if isinstance(tasks, list):
                zrise_task = next((t for t in tasks if t['id'] == task_id), None)
                if zrise_task:
                    zstage = zrise_task.get('stage', '')
                    if any(kw in zstage.lower() for kw in ['done', 'closed', 'completed']):
                        is_zrise_done = True
                        stage = zstage
                        # Update local state
                        ctx['stage'] = stage
                        if not is_zrise_done or current_step != 'done':
                            ctx['current_step'] = 'done'
                            current_step = 'done'
                            ctx['status'] = 'completed'
                        ctx_path.write_text(json.dumps(ctx, indent=2, ensure_ascii=False), encoding='utf-8')
        except Exception:
            pass

    # Workflow phases — agent xử lý mỗi phase, không còn granular steps
    all_phases = [
        ('plan', '📋 Plan', [
            ('agent_plan', '🤖', 'Agent: Fetch + Analyze + Plan + Send Review'),
            ('awaiting_plan_approval', '⏳', 'Chờ Plan Approval'),
        ]),
        ('execute', '⚡ Execute', [
            ('agent_execute', '🧠', 'Agent: Thực thi theo plan + Writeback + Send Result'),
            ('awaiting_result_approval', '⏳', 'Chờ Result Approval'),
        ]),
        ('approve', '✅ Approve', [
            ('agent_approve', '✅', 'Agent: Mark Done + Notify'),
            ('done', '🎉', 'Task Completed'),
        ]),
    ]

    # Determine current phase
    current_phase = 'plan'
    session_status = ctx.get('status', '')
    stage = ctx.get('stage', '')

    plan_ids = [s[0] for p in all_phases for s in p[2] if p[0] == 'plan']
    exec_ids = [s[0] for p in all_phases for s in p[2] if p[0] == 'execute']
    appr_ids = [s[0] for p in all_phases for s in p[2] if p[0] == 'approve']
    if current_step in exec_ids: current_phase = 'execute'
    elif current_step in appr_ids: current_phase = 'approve'

    phase_idx = {'plan': 0, 'execute': 1, 'approve': 2}
    current_idx = phase_idx.get(current_phase, 0)
    active_found = False

    phases_out = []
    for pi, (pname, plabel, psteps) in enumerate(all_phases):
        steps_out = []
        for sid, sicon, sdesc in psteps:
            # Bug 1 fix: If Zrise indicates done/closed, all phases should be completed
            if is_zrise_done:
                state = 'completed'
            # Bug 1 fix: If step is 'done', mark as completed regardless of current_idx
            elif sid == 'done':
                state = 'completed'
            elif pi < current_idx:
                state = 'completed'
            elif pi == current_idx:
                if sid == current_step:
                    # Node hiện tại: active nếu đang processing, failed nếu lỗi
                    state = 'failed' if session_status == 'failed' else 'active'
                    active_found = True
                elif not active_found and sid in step_logs:
                    state = 'completed'
                elif not active_found:
                    state = 'pending'
                else:
                    state = 'pending'
            else:
                state = 'upcoming'
            steps_out.append({'id': sid, 'icon': sicon, 'desc': sdesc, 'state': state, 'logs': step_logs.get(sid, [])})
        phases_out.append({'name': pname, 'label': plabel, 'steps': steps_out, 'is_active': pname == current_phase})

    return {
        'ok': True, 'task_id': task_id, 'task_name': ctx.get('task_name', ''),
        'project': ctx.get('project', ''), 'workflow': workflow,
        'current_step': current_step, 'current_phase': current_phase,
        'status': ctx.get('status', 'unknown'), 'iteration': ctx.get('iteration', 1),
        'stage': ctx.get('stage', ''), 'created_at': ctx.get('created_at', ''),
        'updated_at': ctx.get('updated_at', ''), 'phases': phases_out,
        'total_turns': len(turns), 'step_logs': step_logs,
        'error': _re.sub(r'\x1b\[[0-9;]*m', '', ctx.get('error', '')) if ctx.get('error') else None,
    }


def get_monitor_data():
    """Get active sessions, running processes, and system info."""
    data = {
        'sessions': [],
        'processes': [],
        'poll_state': None,
        'timestamp': datetime.now(timezone.utc).isoformat(),
    }

    # 1. Active sessions from state/zrise/sessions/
    sessions_dir = ROOT / 'state' / 'zrise' / 'sessions'
    if sessions_dir.exists():
        for task_dir in sessions_dir.iterdir():
            if not task_dir.is_dir():
                continue
            ctx_file = task_dir / 'context.json'
            if not ctx_file.exists():
                continue
            try:
                ctx = json.loads(ctx_file.read_text(encoding='utf-8'))
                task_id = ctx.get('task_id', task_dir.name)

                # Count turns
                turns = []
                turns_file = task_dir / 'turns.json'
                if turns_file.exists():
                    turns_data = json.loads(turns_file.read_text(encoding='utf-8'))
                    turns = turns_data.get('turns', []) if isinstance(turns_data, dict) else turns_data

                # Get handoff info
                handoff = {}
                handoff_file = task_dir / 'handoff.json'
                if handoff_file.exists():
                    handoff = json.loads(handoff_file.read_text(encoding='utf-8'))

                # File timestamps
                mtime = os.path.getmtime(ctx_file)
                age_seconds = time.time() - mtime
                age_str = _human_age(age_seconds)

                # Status
                status = ctx.get('status', 'unknown')
                step = ctx.get('current_step', '')
                workflow = ctx.get('workflow', '')
                iteration = ctx.get('iteration', 1)
                last_active = datetime.fromtimestamp(mtime, tz=timezone.utc).isoformat()

                data['sessions'].append({
                    'task_id': task_id,
                    'task_name': ctx.get('task_name', ''),
                    'project': ctx.get('project', ''),
                    'stage': ctx.get('stage', ''),
                    'status': status,
                    'current_step': step,
                    'workflow': workflow,
                    'iteration': iteration,
                    'turns_count': len(turns) if isinstance(turns, list) else 0,
                    'last_active': last_active,
                    'age': age_str,
                    'age_seconds': age_seconds,
                    'has_handoff': bool(handoff),
                    'agents': list(set(t.get('agent', '') for t in turns if isinstance(turns, list) and t.get('agent'))) if isinstance(turns, list) else [],
                })
            except Exception:
                pass

    # Sort by most recent
    data['sessions'].sort(key=lambda s: s['age_seconds'] or 0)

    # 2. Running lobster processes
    try:
        result = subprocess.run(['pgrep', '-fa', 'lobster run'],
                               capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                if not line.strip():
                    continue
                # Parse: PID command args
                parts = line.strip().split(None, 1)
                if len(parts) >= 2:
                    cmd = parts[1]
                    data['processes'].append({
                        'pid': int(parts[0]),
                        'command': cmd[:200],
                        'is_lobster': True,
                    })
    except Exception:
        pass

    # Also check for python workflow processes
    try:
        result = subprocess.run(['pgrep', '-fa', 'workflow_manager'],
                               capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                if not line.strip():
                    continue
                parts = line.strip().split(None, 1)
                if len(parts) >= 2:
                    data['processes'].append({
                        'pid': int(parts[0]),
                        'command': parts[1][:200],
                        'is_lobster': False,
                    })
    except Exception:
        pass

    # 3. Poll state
    poll_file = ROOT / 'state' / 'zrise' / 'poll-state'
    if poll_file.exists():
        try:
            poll_files = list(poll_file.glob('*.json'))
            if poll_files:
                latest = max(poll_files, key=lambda f: f.stat().st_mtime)
                poll_data = json.loads(latest.read_text(encoding='utf-8'))
                data['poll_state'] = {
                    'last_poll': datetime.fromtimestamp(latest.stat().st_mtime, tz=timezone.utc).isoformat(),
                    'data': poll_data,
                }
        except Exception:
            pass

    return data


def _human_age(seconds):
    """Convert seconds to human readable age."""
    if seconds < 60:
        return f'{int(seconds)}s ago'
    elif seconds < 3600:
        return f'{int(seconds/60)}m ago'
    elif seconds < 86400:
        return f'{int(seconds/3600)}h ago'
    else:
        return f'{int(seconds/86400)}d ago'


class WorkflowAPIHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8'))

    def parse_path(self):
        parsed = urlparse(self.path)
        return parsed.path, parse_qs(parsed.query)

    def read_body(self):
        length = int(self.headers.get('Content-Length', 0))
        if length > 0:
            return json.loads(self.rfile.read(length).decode('utf-8'))
        return {}

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        self.end_headers()

    def do_GET(self):
        path, query = self.parse_path()
        if path.startswith('/api/') and not check_auth(self):
            self.send_json({'ok': False, 'error': 'Unauthorized'}, 401)
            return

        # ── Workflows ──
        if path == '/api/workflows':
            wf_dict = get_all_workflows()
            workflows = list(wf_dict.values())
            for f in ('category', 'owner', 'source'):
                if f in query:
                    workflows = [w for w in workflows if w.get(f) == query[f][0]]
            self.send_json({'ok': True, 'workflows': workflows, 'count': len(workflows)})
            return

        match = re.match(r'^/api/workflows/([^/]+)/yaml$', path)
        if match:
            wid = match.group(1)
            all_wf = get_all_workflows()
            if wid not in all_wf:
                self.send_json({'ok': False, 'error': 'Not found'}, 404)
                return
            fp = ROOT / all_wf[wid].get('file', '')
            if fp.exists():
                self.send_json({'ok': True, 'yaml': fp.read_text(encoding='utf-8'), 'source': all_wf[wid].get('source')})
            else:
                self.send_json({'ok': False, 'error': 'File not found'}, 404)
            return

        match = re.match(r'^/api/workflows/([^/]+)$', path)
        if match:
            wid = match.group(1)
            all_wf = get_all_workflows()
            if wid in all_wf:
                self.send_json({'ok': True, 'workflow': all_wf[wid]})
            else:
                self.send_json({'ok': False, 'error': 'Not found'}, 404)
            return

        # ── Tasks ──
        if path == '/api/tasks':
            limit = int(query.get('limit', ['50'])[0])
            stage = query.get('stage', [None])[0]
            result = fetch_zrise_tasks(limit=limit, stage_filter=stage)
            if isinstance(result, dict) and 'error' in result:
                self.send_json({'ok': False, 'error': result['error']}, 500)
            else:
                self.send_json({'ok': True, 'tasks': result, 'count': len(result)})
            return

        match = re.match(r'^/api/tasks/(\d+)$', path)
        if match:
            task_id = int(match.group(1))
            try:
                db, uid, secret, models, url = connect_zrise()
                task = models.execute_kw(db, uid, secret, 'project.task', 'search_read',
                    [[('id', '=', task_id)]], {'fields': ['id', 'name', 'description', 'stage_id', 'project_id',
                                        'date_deadline', 'priority', 'create_date', 'write_date'], 'limit': 1})
                if task:
                    t = task[0]
                    import re as _re
                    desc = _re.sub('<[^>]+>', '', t.get('description', ''))
                    self.send_json({'ok': True, 'task': {
                        'id': t['id'], 'name': t['name'], 'description': desc,
                        'stage': t['stage_id'][1] if isinstance(t.get('stage_id'), list) else '',
                        'project': t['project_id'][1] if isinstance(t.get('project_id'), list) else '',
                        'priority': t.get('priority', '0'),
                        'deadline': t.get('date_deadline'),
                        'url': f'{url}/web#id={t["id"]}&model=project.task&view_type=form',
                    }})
                else:
                    self.send_json({'ok': False, 'error': 'Task not found'}, 404)
            except Exception as e:
                self.send_json({'ok': False, 'error': str(e)}, 500)
            return

        # ── Monitor ──
        if path == '/api/monitor':
            data = get_monitor_data()
            self.send_json({'ok': True, **data})
            return

        # ── Session Timeline ──
        match = re.match(r'^/api/sessions/(\d+)/timeline$', path)
        if match:
            task_id = int(match.group(1))
            data = get_session_timeline(task_id)
            self.send_json(data)
            return

        # ── UI ──
        if path in ('/', '/index.html'):
            self.serve_ui()
            return

        self.send_json({'ok': False, 'error': 'Not found'}, 404)

    def do_POST(self):
        path, query = self.parse_path()
        body = self.read_body()
        if not check_auth(self):
            self.send_json({'ok': False, 'error': 'Unauthorized'}, 401)
            return

        # Create workflow
        if path == '/api/workflows':
            name = body.get('name')
            yaml_content = body.get('yaml')
            if not name or not yaml_content:
                self.send_json({'ok': False, 'error': 'Missing name or yaml'}, 400)
                return
            validation = validate_lobster_yaml(yaml_content)
            if not validation['valid']:
                self.send_json({'ok': False, 'errors': validation['errors']}, 400)
                return
            owner = get_current_user()
            safe_name = re.sub(r'[^a-z0-9-]', '-', name.lower())
            user_dir = WORKFLOWS_DIR / owner
            user_dir.mkdir(parents=True, exist_ok=True)
            filepath = user_dir / f'{safe_name}.lobster'
            filepath.write_text(yaml_content, encoding='utf-8')
            now = datetime.now(timezone.utc).isoformat()
            metadata = {
                'workflow_id': safe_name, 'name': name,
                'description': body.get('description', ''),
                'category': body.get('category', 'custom'),
                'tags': body.get('tags', []),
                'visibility': body.get('visibility', 'private'),
                'owner': owner, 'agent': body.get('agent', 'zrise-analyst'),
                'file': str(filepath.relative_to(ROOT)),
                'created_at': now, 'updated_at': now, 'version': '1.0.0',
            }
            registry = load_registry()
            registry[safe_name] = metadata
            save_registry(registry)
            self.send_json({'ok': True, 'workflow': metadata}, 201)
            return

        # Trigger workflow from timeline
        match = re.match(r'^/api/sessions/(\d+)/trigger$', path)
        if match:
            task_id = int(match.group(1))
            step_id = body.get('step', '')
            phase = body.get('phase', '')
            step = body.get('step', '')
            feedback = body.get('feedback', '')

            wf_name = body.get('workflow', 'general')
            wf_file = SCRIPTS_DIR.parent / 'workflows' / f'{wf_name}.lobster'
            if not wf_file.exists():
                # Fallback to general
                wf_file = SCRIPTS_DIR.parent / 'workflows' / 'general.lobster'
                if not wf_file.exists():
                    self.send_json({'ok': False, 'error': 'No workflow file found'}, 404)
                    return

            # Map individual steps to their parent phase (kiến trúc agent-based)
            step_to_phase = {
                'agent_plan': 'plan', 'awaiting_plan_approval': 'plan',
                'agent_execute': 'execute', 'awaiting_result_approval': 'execute',
                'agent_approve': 'approve', 'done': 'approve',
            }

            # Determine effective phase: use step mapping first, then phase directly
            effective_phase = step_to_phase.get(step) or step_to_phase.get(phase) or phase or 'plan'

            args = {'task_id': task_id, 'effective_phase': effective_phase, 'step': step}
            if effective_phase == 'plan':
                args['phase'] = 'plan'
            elif effective_phase == 'execute':
                args['phase'] = 'execute'
                args['selected_workflow'] = body.get('workflow', 'general')
                if feedback:
                    args['feedback'] = feedback
            elif effective_phase == 'approve':
                args['phase'] = 'approve'

            # ── Bootstrap session state ──
            work_item_id = f'zrise-task-{task_id}'
            sessions_dir = ROOT / 'state' / 'zrise' / 'sessions'
            sessions_dir.mkdir(parents=True, exist_ok=True)
            session_file = sessions_dir / f'{work_item_id}.json'

            ctx = {}
            if session_file.exists():
                ctx = json.loads(session_file.read_text(encoding='utf-8'))

            # Ensure session has basic fields
            ctx.setdefault('session_id', work_item_id)
            ctx.setdefault('task_id', task_id)
            if not ctx.get('created_at'):
                ctx['created_at'] = datetime.now(timezone.utc).isoformat()
            ctx['current_phase'] = effective_phase
            step_map = {'plan': 'agent_plan', 'execute': 'agent_execute', 'approve': 'agent_approve'}
            ctx['current_step'] = step_map.get(effective_phase, effective_phase)
            ctx['status'] = 'processing'
            if feedback:
                ctx['last_feedback'] = feedback
            ctx['updated_at'] = datetime.now(timezone.utc).isoformat()

            # Fetch task_name from Zrise if missing
            if not ctx.get('task_name'):
                tn, proj, stg = _get_task_name_from_zrise(task_id)
                if tn:
                    ctx['task_name'] = tn
                if proj:
                    ctx['project'] = proj
                if stg:
                    ctx['stage'] = stg

            session_file.write_text(json.dumps(ctx, indent=2, ensure_ascii=False), encoding='utf-8')

            # ── Bootstrap work-item state for pipeline ──
            work_items_dir = ROOT / 'state' / 'zrise' / 'work-items'
            work_items_dir.mkdir(parents=True, exist_ok=True)
            item_file = work_items_dir / f'{work_item_id}.json'

            if not item_file.exists():
                # Create work-item from session data + Zrise fetch
                item = {
                    'work_item_id': work_item_id,
                    'source': 'ui-trigger',
                    'event_type': 'manual_trigger',
                    'task_id': task_id,
                    'task_name': ctx.get('task_name', ''),
                    'project_name': ctx.get('project', ''),
                    'stage': ctx.get('stage', ''),
                    'link': ctx.get('link', ''),
                }
                # Enrich from Zrise if possible
                try:
                    tasks = fetch_zrise_tasks(limit=200)
                    if isinstance(tasks, list):
                        zt = next((t for t in tasks if t['id'] == task_id), None)
                        if zt:
                            item['task_name'] = item['task_name'] or zt.get('name', '')
                            item['project_name'] = item['project_name'] or ''
                            item['stage'] = item['stage'] or zt.get('stage_id', [''])[1] if isinstance(zt.get('stage_id'), list) else item['stage']
                            item['deadline'] = zt.get('date_deadline', '')
                            item['link'] = f"{_zrise_url()}/web#id={task_id}&model=project.task&view_type=form"
                except Exception:
                    pass
                item_file.write_text(json.dumps(item, indent=2, ensure_ascii=False), encoding='utf-8')

            try:
                env = {**os.environ}
                env['PYTHONPATH'] = str(SCRIPTS_DIR)
                env['PATH'] = '/opt/homebrew/bin:' + env.get('PATH', '')
                env['ZRISE_JSON_OUTPUT'] = '1'

                # Build command using run_workflow_pipeline.py with work_item_id
                workflow_name = args.get('selected_workflow', body.get('workflow', 'general'))
                cmd = [str(SCRIPTS_DIR / 'run_workflow_pipeline.py'),
                       work_item_id, workflow_name]

                proc = launch_workflow(cmd, task_id, args['phase'], str(ROOT), env)
                self.send_json({'ok': True, 'message': f'Triggered: phase={args["phase"]}', 'task_id': task_id, 'work_item_id': work_item_id, 'phase': args['phase'], 'pid': proc.pid, 'args': args})
            except FileNotFoundError:
                self.send_json({'ok': False, 'error': 'Pipeline script not found'}, 500)
            except Exception as e:
                self.send_json({'ok': False, 'error': str(e)}, 500)
            return

        # Run workflow for task
        match = re.match(r'^/api/tasks/(\d+)/run$', path)
        if match:
            task_id = int(match.group(1))
            self.send_json({'ok': True, 'message': f'Workflow triggered for task {task_id}', 'task_id': task_id, 'phase': 'plan'})
            return

        # Approve task workflow step (plan or result) - NEW ARCHITECTURE
        match = re.match(r'^/api/tasks/(\d+)/approve$', path)
        if match:
            task_id = int(match.group(1))
            try:
                # Fetch task info từ Zrise để kiểm tra trạng thái
                db, uid, secret, models, url = connect_zrise()
                task_info = fetch_task_data_from_zrise(models, db, uid, secret, task_id)
                current_stage = task_info.get('stage', 'Unknown')
                
                # Chỉ cho phép approve khi task đang ở In Process
                if current_stage != "In Process":
                    self.send_json({
                        'ok': False, 
                        'error': f'Task đang ở stage "{current_stage}". Chỉ task ở "In Process" mới có thể approve qua UI.'
                    }, 400)
                    return
                
                # Xác định loại approve: plan hoặc result
                # Người dùng có thể chỉ định qua body['approve_type'], hoặc hệ thống tự suy diễn
                approve_type = body.get('approve_type', '').lower()
                
                # Đảm bảo thư mục .tasks tồn tại
                tasks_dir = SCRIPTS_DIR.parent / '.tasks'
                tasks_dir.mkdir(parents=True, exist_ok=True)
                task_dir = tasks_dir / str(task_id)
                task_dir.mkdir(parents=True, exist_ok=True)
                
                if approve_type == 'plan':
                    # User muốn approve plan → ghi vào file để Lobster workflow biết
                    approve_file = task_dir / 'plan_approved'
                    approve_file.write_text(json.dumps({
                        'approved_by': get_current_user(),
                        'approved_at': datetime.now(timezone.utc).isoformat(),
                        'via': 'ui_manager'
                    }), encoding='utf-8')
                    
                    self.send_json({
                        'ok': True,
                        'task_id': task_id,
                        'action': 'plan_approved',
                        'message': '✅ Plan đã được approve. Lobster workflow sẽ tiếp tục sang execute phase.',
                        'next_step': 'Đợi AI hoàn thành execute, sau đó approve kết quả'
                    })
                    
                elif approve_type == 'result':
                    # User muốn approve result → ghi vào file để post-processing hệ thống biết
                    approve_file = task_dir / 'result_approved'
                    approve_file.write_text(json.dumps({
                        'approved_by': get_current_user(),
                        'approved_at': datetime.now(timezone.utc).isoformat(),
                        'via': 'ui_manager',
                        'trigger_post_processing': True
                    }), encoding='utf-8')
                    
                    self.send_json({
                        'ok': True,
                        'task_id': task_id,
                        'action': 'result_approved',
                        'message': '✅ Kết quả đã được approve. Post-processing sẽ tự động thực hiện writeback, timesheet, và chuyển stage Done.',
                        'next_step': 'Đợi cron job post-processing tự động xử lý (writeback → timesheet → Done)'
                    })
                    
                else:
                    # Tự suy diễn: nếu đã có kết quả AI trong registry/comments → approve result, ngược lại → approve plan
                    has_ai_result = check_if_task_has_ai_result(task_id)
                    
                    if has_ai_result:
                        # Có kết quả AI → approve result
                        approve_file = task_dir / 'result_approved'
                        approve_file.write_text(json.dumps({
                            'approved_by': get_current_user(),
                            'approved_at': datetime.now(timezone.utc).isoformat(),
                            'via': 'ui_manager_auto',
                            'trigger_post_processing': True
                        }), encoding='utf-8')
                        
                        self.send_json({
                            'ok': True,
                            'task_id': task_id,
                            'action': 'result_approved',
                            'message': '✅ Phát hiện kết quả AI đã hoàn thành. Kết quả được approve. Post-processing sẽ tự động xử lý.',
                            'next_step': 'Đợi cron job post-processing tự động xử lý (writeback → timesheet → Done)'
                        })
                    else:
                        # Chưa có kết quả AI → approve plan
                        approve_file = task_dir / 'plan_approved'
                        approve_file.write_text(json.dumps({
                            'approved_by': get_current_user(),
                            'approved_at': datetime.now(timezone.utc).isoformat(),
                            'via': 'ui_manager_auto'
                        }), encoding='utf-8')
                        
                        self.send_json({
                            'ok': True,
                            'task_id': task_id,
                            'action': 'plan_approved',
                            'message': '✅ Chưa phát hiện kết quả AI. Plan được approve. Lobster workflow sẽ tiếp tục sang execute phase.',
                            'next_step': 'Đợi AI hoàn thành execute, sau đó approve kết quả'
                        })
                        
            except Exception as e:
                self.send_json({'ok': False, 'error': str(e)}, 500)
            return

        self.send_json({'ok': False, 'error': 'Not found'}, 404)

    def do_PUT(self):
        path, query = self.parse_path()
        body = self.read_body()
        if not check_auth(self):
            self.send_json({'ok': False, 'error': 'Unauthorized'}, 401)
            return
        match = re.match(r'^/api/workflows/([^/]+)$', path)
        if match:
            wid = match.group(1)
            registry = load_registry()
            if wid not in registry:
                self.send_json({'ok': False, 'error': 'Not found'}, 404)
                return
            wf = registry[wid]
            if wf.get('owner') != get_current_user() and wf.get('visibility') != 'public':
                self.send_json({'ok': False, 'error': 'Permission denied'}, 403)
                return
            if 'yaml' in body:
                v = validate_lobster_yaml(body['yaml'])
                if not v['valid']:
                    self.send_json({'ok': False, 'errors': v['errors']}, 400)
                    return
                (ROOT / wf['file']).write_text(body['yaml'], encoding='utf-8')
            for k in ('name', 'description', 'category', 'tags', 'visibility', 'agent'):
                if k in body:
                    wf[k] = body[k]
            wf['updated_at'] = datetime.now(timezone.utc).isoformat()
            registry[wid] = wf
            save_registry(registry)
            self.send_json({'ok': True, 'workflow': wf})
            return
        self.send_json({'ok': False, 'error': 'Not found'}, 404)

    def do_DELETE(self):
        path, query = self.parse_path()
        if not check_auth(self):
            self.send_json({'ok': False, 'error': 'Unauthorized'}, 401)
            return
        match = re.match(r'^/api/workflows/([^/]+)$', path)
        if match:
            wid = match.group(1)
            registry = load_registry()
            if wid not in registry:
                self.send_json({'ok': False, 'error': 'Not found'}, 404)
                return
            wf = registry[wid]
            if wf.get('owner') != get_current_user():
                self.send_json({'ok': False, 'error': 'Permission denied'}, 403)
                return
            fp = ROOT / wf['file']
            if fp.exists():
                fp.unlink()
            del registry[wid]
            save_registry(registry)
            self.send_json({'ok': True, 'deleted': wid})
            return
        self.send_json({'ok': False, 'error': 'Not found'}, 404)

    def serve_ui(self):
        html = HTML_UI
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))


# ── HTML UI ────────────────────────────────────────────────

HTML_UI = r"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Zrise Workflow Manager</title>
<style>
:root {
  --bg: #1a1a2e; --bg2: #16213e; --card: #2d2d44; --card-hover: #353554;
  --border: #3a3a5c; --text: #e0e0e0; --text2: #9e9e9e; --text3: #6b6b8d;
  --accent: #ff6d5a; --accent2: #ff8a7a; --primary: #7b61ff; --primary2: #9b85ff;
  --success: #4caf50; --success-bg: #1a3a1f; --warning: #ffab40; --warning-bg: #3a2a10;
  --danger: #ff5252; --danger-bg: #3a1a1a; --blue: #42a5f5; --blue-bg: #1a2a3a;
  --radius: 12px; --shadow: 0 2px 8px rgba(0,0,0,.3);
  --node-w: 160px; --node-h: 90px; --gap: 80px;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); line-height: 1.5; overflow-x: hidden; }

/* ── Layout ── */
.app { max-width: 1600px; margin: 0 auto; padding: 16px 24px; min-height: 100vh; }
header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid var(--border); }
header h1 { font-size: 22px; font-weight: 700; color: #fff; }
header h1 span { color: var(--accent); }
.header-right { display: flex; align-items: center; gap: 16px; font-size: 13px; color: var(--text2); }

/* ── Tabs ── */
.tabs { display: flex; gap: 2px; margin-bottom: 20px; background: var(--bg2); border-radius: 10px; padding: 3px; }
.tab { flex: 1; padding: 10px 20px; border: none; background: none; border-radius: 8px; font-size: 13px; font-weight: 600; color: var(--text2); cursor: pointer; transition: all .2s; display: flex; align-items: center; justify-content: center; gap: 6px; }
.tab:hover { color: var(--text); background: rgba(255,255,255,.04); }
.tab.active { background: var(--primary); color: #fff; box-shadow: 0 2px 10px rgba(123,97,255,.4); }
.tab .count { background: rgba(255,255,255,.15); padding: 1px 7px; border-radius: 8px; font-size: 11px; }
.tab:not(.active) .count { background: rgba(255,255,255,.06); color: var(--text3); }
.tab-content { display: none; }
.tab-content.active { display: block; }

/* ── Stats ── */
.stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; margin-bottom: 20px; }
.stat-card { background: var(--card); border-radius: var(--radius); padding: 16px; border: 1px solid var(--border); }
.stat-card .label { font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: .5px; color: var(--text3); margin-bottom: 2px; }
.stat-card .value { font-size: 26px; font-weight: 700; }
.stat-card .value.v-accent { color: var(--accent); }
.stat-card .value.v-blue { color: var(--blue); }
.stat-card .value.v-green { color: var(--success); }
.stat-card .value.v-warning { color: var(--warning); }

/* ── Toolbar ── */
.toolbar { display: flex; gap: 10px; margin-bottom: 16px; align-items: center; flex-wrap: wrap; }
.search { flex: 1; min-width: 200px; padding: 9px 14px; border: 1px solid var(--border); border-radius: 8px; font-size: 13px; background: var(--card); color: var(--text); outline: none; transition: border .2s; }
.search:focus { border-color: var(--primary); }
.search::placeholder { color: var(--text3); }
.filter-select { padding: 9px 12px; border: 1px solid var(--border); border-radius: 8px; font-size: 13px; background: var(--card); color: var(--text); outline: none; }

/* ── Buttons ── */
.btn { padding: 8px 16px; border: none; border-radius: 8px; font-size: 13px; font-weight: 600; cursor: pointer; transition: all .15s; display: inline-flex; align-items: center; gap: 5px; }
.btn:active { transform: scale(.97); }
.btn-primary { background: var(--primary); color: #fff; }
.btn-primary:hover { background: var(--primary2); }
.btn-ghost { background: none; color: var(--text2); padding: 8px 12px; }
.btn-ghost:hover { background: rgba(255,255,255,.06); color: var(--text); }
.btn-danger { background: var(--danger-bg); color: var(--danger); }
.btn-danger:hover { background: var(--danger); color: #fff; }
.btn-success { background: var(--success-bg); color: var(--success); }
.btn-success:hover { background: var(--success); color: #fff; }
.btn-accent { background: var(--accent); color: #fff; }
.btn-accent:hover { background: var(--accent2); }
.btn-blue { background: var(--blue-bg); color: var(--blue); }
.btn-blue:hover { background: var(--blue); color: #fff; }
.btn-sm { padding: 5px 10px; font-size: 12px; }

/* ── Split Panel (Tasks + Workflow) ── */
.split-panel { display: flex; gap: 16px; min-height: calc(100vh - 200px); }
.panel-left { flex: 0 0 380px; min-width: 320px; display: flex; flex-direction: column; gap: 12px; }
.panel-right { flex: 1; min-width: 0; }
.panel-left.full { flex: 1 1 100%; }

/* ── Task Cards ── */
.task-list { display: flex; flex-direction: column; gap: 6px; overflow-y: auto; max-height: calc(100vh - 240px); padding-right: 4px; }
.task-list::-webkit-scrollbar { width: 4px; }
.task-list::-webkit-scrollbar-track { background: transparent; }
.task-list::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
.task-card { background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 12px 14px; cursor: pointer; transition: all .15s; }
.task-card:hover { background: var(--card-hover); border-color: var(--primary); }
.task-card.selected { border-color: var(--primary); background: rgba(123,97,255,.08); box-shadow: 0 0 0 1px var(--primary); }
.task-card.running { border-left: 3px solid var(--success); }
.task-card.dimmed { opacity: .5; }
.tc-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 8px; }
.tc-name { font-size: 13px; font-weight: 600; color: #fff; line-height: 1.3; }
.tc-sub { font-size: 11px; color: var(--text2); margin-top: 2px; }
.tc-badges { display: flex; gap: 4px; flex-shrink: 0; align-items: center; }
.tc-meta { display: flex; gap: 10px; margin-top: 6px; font-size: 11px; color: var(--text3); }

/* ── Badges ── */
.badge { display: inline-flex; align-items: center; gap: 3px; padding: 2px 8px; border-radius: 20px; font-size: 11px; font-weight: 600; }
.badge-done { background: var(--success-bg); color: var(--success); }
.badge-in-process { background: var(--blue-bg); color: var(--blue); }
.badge-todo { background: rgba(255,255,255,.06); color: var(--text2); }
.badge-high { background: var(--danger-bg); color: var(--danger); }
.badge-normal { background: rgba(255,255,255,.06); color: var(--text2); }
.badge-running { background: var(--success-bg); color: var(--success); animation: glow-green 2s infinite; }
@keyframes glow-green { 0%,100%{ box-shadow: 0 0 4px rgba(76,175,80,.3); } 50%{ box-shadow: 0 0 12px rgba(76,175,80,.5); } }
.badge-builtin { background: rgba(255,255,255,.06); color: var(--text2); }
.badge-custom { background: var(--blue-bg); color: var(--blue); }

/* ── Workflow Canvas (n8n style) ── */
.wf-canvas { position: relative; background: var(--bg2); border-radius: var(--radius); border: 1px solid var(--border); overflow: hidden; min-height: 300px; }
.wf-canvas-grid { position: absolute; inset: 0; background-image: radial-gradient(circle, var(--border) 1px, transparent 1px); background-size: 24px 24px; opacity: .5; }
.wf-header { position: relative; z-index: 2; display: flex; align-items: center; justify-content: space-between; padding: 14px 18px; border-bottom: 1px solid var(--border); background: rgba(26,26,46,.8); backdrop-filter: blur(8px); }
.wf-header-title { font-size: 14px; font-weight: 600; color: #fff; display: flex; align-items: center; gap: 8px; }
.wf-actions { display: flex; gap: 6px; flex-wrap: wrap; }
.wf-body { position: relative; z-index: 1; padding: 40px 30px; overflow-x: auto; overflow-y: auto; min-height: 400px; }

/* ── Nodes ── */
.nodes-container { display: flex; flex-direction: column; gap: 24px; }
.node-phase { display: flex; align-items: flex-start; gap: 0; }
.node-phase-label { position: absolute; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: var(--text3); top: -18px; left: 0; }
.node-row { display: flex; align-items: center; position: relative; }
.node { width: var(--node-w); min-height: var(--node-h); background: var(--card); border: 2px solid var(--border); border-radius: 14px; padding: 14px; cursor: pointer; transition: all .2s; position: relative; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; gap: 4px; }
.node:hover { border-color: var(--primary); transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,.3); }
.node-icon { font-size: 26px; line-height: 1; }
.node-name { font-size: 12px; font-weight: 600; color: var(--text); line-height: 1.2; }
.node-status { font-size: 10px; font-weight: 600; padding: 2px 8px; border-radius: 10px; margin-top: 4px; text-transform: uppercase; letter-spacing: .5px; }
.node.completed { border-color: var(--success); }
.node.completed .node-status { background: var(--success-bg); color: var(--success); }
.node.failed { border-color: #ef4444; background: rgba(239,68,68,.08); }
.node.failed .node-status { background: rgba(239,68,68,.15); color: #ef4444; }
.node.active { border-color: var(--primary); animation: node-pulse 2s infinite; }
.node.active .node-status { background: rgba(123,97,255,.2); color: var(--primary2); }
@keyframes node-pulse { 0%,100%{ box-shadow: 0 0 0 0 rgba(123,97,255,.4); } 50%{ box-shadow: 0 0 0 8px rgba(123,97,255,0); } }
.node.pending { border-color: var(--border); opacity: .4; }
.node.pending .node-status { background: rgba(255,255,255,.04); color: var(--text3); }
.node.upcoming { border-color: transparent; opacity: .2; pointer-events: none; }
.wf-error-banner { background: rgba(239,68,68,.12); border: 1px solid rgba(239,68,68,.3); border-radius: 8px; padding: 12px 16px; margin-bottom: 16px; color: #fca5a5; font-size: 13px; }
.wf-error-banner strong { color: #ef4444; }

/* Connection lines between nodes */
.node-connector { width: var(--gap);; height: 2px; position: relative; flex-shrink: 0; }
.node-connector svg { position: absolute; top: 50%; left: 0; width: 100%; height: 40px; transform: translateY(-50%); }
.node-connector svg path { fill: none; stroke: var(--border); stroke-width: 2; }
.node-connector.completed svg path { stroke: var(--success); }
.node-connector.active svg path { stroke: var(--primary); stroke-dasharray: 6 4; animation: dash-flow 1s linear infinite; }
@keyframes dash-flow { to { stroke-dashoffset: -10; } }

/* ── Node Popover ── */
.node-popover { display: none; position: fixed; z-index: 200; background: var(--card); border: 1px solid var(--primary); border-radius: 12px; padding: 16px; width: 320px; max-height: 400px; overflow-y: auto; box-shadow: 0 12px 40px rgba(0,0,0,.5); }
.node-popover.show { display: block; }
.np-header { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; }
.np-title { font-size: 14px; font-weight: 600; color: #fff; }
.np-desc { font-size: 12px; color: var(--text2); margin-bottom: 10px; }
.np-actions { display: flex; gap: 6px; margin-bottom: 10px; }
.np-logs { background: var(--bg); border-radius: 8px; padding: 10px; max-height: 200px; overflow-y: auto; }
.np-log-item { margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px solid var(--border); }
.np-log-item:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
.np-log-role { font-size: 10px; font-weight: 700; text-transform: uppercase; color: var(--primary2); }
.np-log-content { font-size: 12px; color: var(--text); white-space: pre-wrap; line-height: 1.5; margin-top: 2px; max-height: 150px; overflow-y: auto; }
.np-log-time { font-size: 10px; color: var(--text3); margin-top: 2px; }
.np-close { position: absolute; top: 8px; right: 10px; background: none; border: none; color: var(--text2); cursor: pointer; font-size: 16px; }

/* ── Empty State ── */
.empty { text-align: center; padding: 60px 20px; color: var(--text3); }
.empty-icon { font-size: 48px; margin-bottom: 12px; }
.empty-text { font-size: 15px; }

/* ── Loading ── */
.loading { text-align: center; padding: 40px; color: var(--text3); }
.spinner { width: 24px; height: 24px; border: 3px solid var(--border); border-top-color: var(--primary); border-radius: 50%; animation: spin .8s linear infinite; margin: 0 auto 12px; }
@keyframes spin { to { transform: rotate(360deg); } }

/* ── Modals ── */
.modal-overlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,.6); z-index: 100; align-items: center; justify-content: center; backdrop-filter: blur(4px); }
.modal-overlay.show { display: flex; }
.modal { background: var(--card); border-radius: 16px; width: 640px; max-width: 95vw; max-height: 90vh; overflow-y: auto; box-shadow: 0 20px 60px rgba(0,0,0,.4); border: 1px solid var(--border); }
.modal-header { padding: 20px 20px 0; display: flex; align-items: center; justify-content: space-between; }
.modal-header h2 { font-size: 18px; color: #fff; }
.modal-body { padding: 20px; }
.modal-footer { padding: 0 20px 20px; display: flex; gap: 10px; justify-content: flex-end; }

/* ── Forms ── */
.form-group { margin-bottom: 14px; }
.form-group label { display: block; font-size: 12px; font-weight: 600; margin-bottom: 4px; color: var(--text2); }
.form-group input, .form-group select { width: 100%; padding: 9px 12px; border: 1px solid var(--border); border-radius: 8px; font-size: 13px; background: var(--bg2); color: var(--text); outline: none; }
.form-group input:focus, .form-group select:focus { border-color: var(--primary); }
textarea.code { width: 100%; height: 260px; font-family: 'SF Mono', 'Fira Code', monospace; font-size: 12px; padding: 12px; border: 1px solid var(--border); border-radius: 8px; resize: vertical; outline: none; line-height: 1.5; background: var(--bg); color: var(--text); }
textarea.code:focus { border-color: var(--primary); }

/* ── Card list (workflows tab) ── */
.card-list { display: flex; flex-direction: column; gap: 8px; }
.card { background: var(--card); border-radius: var(--radius); padding: 16px; border: 1px solid var(--border); transition: all .15s; }
.card:hover { border-color: var(--primary); }
.card-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; }
.card-title { font-size: 15px; font-weight: 600; color: #fff; }
.card-subtitle { font-size: 12px; color: var(--text2); margin-top: 2px; }
.card-desc { font-size: 13px; color: var(--text2); margin-top: 6px; line-height: 1.6; }
.card-actions { display: flex; gap: 6px; flex-shrink: 0; }
.card-meta { display: flex; gap: 12px; margin-top: 8px; font-size: 11px; color: var(--text3); flex-wrap: wrap; }

a.task-link { color: var(--primary2); text-decoration: none; }
a.task-link:hover { text-decoration: underline; }

/* ── Workflow empty panel ── */
.wf-empty { display: flex; align-items: center; justify-content: center; height: 100%; min-height: 200px; color: var(--text3); flex-direction: column; gap: 8px; }
.wf-empty-icon { font-size: 48px; opacity: .3; }
.wf-empty-text { font-size: 14px; }
.wf-empty-sub { font-size: 11px; opacity: .6; }

/* ── Workflow info bar ── */
.wf-info { display: flex; gap: 16px; padding: 10px 18px; font-size: 12px; color: var(--text2); border-bottom: 1px solid var(--border); flex-wrap: wrap; }
.wf-info-item { display: flex; align-items: center; gap: 4px; }
.wf-info-item strong { color: var(--text); }

/* ── Logs in workflow ── */
.wf-logs-panel { background: var(--bg); border-top: 1px solid var(--border); max-height: 200px; overflow-y: auto; padding: 0; }
.wf-logs-panel.wf-logs-panel-open { padding: 12px 18px; }

/* ── Bug 2 fix: Logs panel styling ── */
.logs-header { transition: background .2s; }
.logs-header:hover { background: rgba(255,255,255,.02); }
#logs-content { scrollbar-width: thin; scrollbar-color: var(--border) transparent; }
#logs-content::-webkit-scrollbar { width: 4px; }
#logs-content::-webkit-scrollbar-track { background: transparent; }
#logs-content::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
.log-turn { background: var(--bg); border: 1px solid var(--border); border-radius: 6px; padding: 8px 10px; margin-bottom: 6px; font-size: 11px; line-height: 1.4; }
.log-turn:last-child { margin-bottom: 0; }
.log-turn-meta { display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px; }
.log-turn-role { font-weight: 600; color: var(--primary); }
.log-turn-time { color: var(--text3); font-size: 10px; }
.log-turn-content { color: var(--text2); white-space: pre-wrap; word-break: break-word; }

/* ── Bug 3 fix: Pulse indicator for active node ── */
.node.active::before { content: ''; position: absolute; inset: -6px; border: 2px solid var(--primary); border-radius: 12px; animation: node-pulse-outer .8s infinite; }
@keyframes node-pulse-outer { 0% { opacity: 1; transform: scale(1); } 100% { opacity: 0; transform: scale(1.3); } }

/* ── Responsive ── */
@media (max-width: 900px) {
  .split-panel { flex-direction: column; }
  .panel-left { flex: none; max-height: 40vh; }
  .panel-left.full { flex: none; }
  .task-list { max-height: 35vh; }
  .app { padding: 12px; }
  .stats { grid-template-columns: repeat(2, 1fr); }
  :root { --node-w: 130px; --node-h: 80px; --gap: 50px; }
}
@media (max-width: 600px) {
  :root { --node-w: 110px; --node-h: 70px; --gap: 30px; }
  .wf-actions { gap: 4px; }
  .btn { padding: 6px 10px; font-size: 11px; }
}

@keyframes pulse { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.5; transform: scale(0.8); } }

/* ── View Toggle ── */
.view-toggle { display: flex; background: var(--bg2); border-radius: 8px; padding: 2px; border: 1px solid var(--border); }
.view-toggle button { padding: 7px 14px; border: none; background: none; border-radius: 6px; font-size: 12px; font-weight: 600; color: var(--text2); cursor: pointer; transition: all .15s; display: flex; align-items: center; gap: 4px; }
.view-toggle button:hover { color: var(--text); }
.view-toggle button.active { background: var(--primary); color: #fff; }

/* ── Kanban Board ── */
.board-container { display: none; flex: 1; overflow-x: auto; overflow-y: auto; max-height: calc(100vh - 240px); padding-bottom: 8px; }
.board-container::-webkit-scrollbar { height: 6px; }
.board-container::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
.board-container.active { display: flex; gap: 12px; padding: 4px; }
.task-list-view.active { display: flex; flex-direction: column; }
.task-list-view { display: none; }
.task-list-view.active { display: flex; flex-direction: column; }

.kanban-col { min-width: 250px; max-width: 320px; flex: 1 1 250px; display: flex; flex-direction: column; background: var(--bg2); border-radius: 12px; border: 1px solid var(--border); overflow: hidden; max-height: 100%; }
.kanban-col-header { padding: 12px 14px; font-size: 13px; font-weight: 700; color: #fff; display: flex; align-items: center; justify-content: space-between; flex-shrink: 0; }
.kanban-col-header.stage-todo { background: rgba(66,165,245,.15); border-bottom: 2px solid var(--blue); }
.kanban-col-header.stage-in-progress { background: rgba(255,171,64,.15); border-bottom: 2px solid var(--warning); }
.kanban-col-header.stage-done { background: rgba(76,175,80,.15); border-bottom: 2px solid var(--success); }
.kanban-col-header.stage-default { background: rgba(255,255,255,.04); border-bottom: 2px solid var(--border); }
.kanban-col-count { background: rgba(255,255,255,.12); padding: 1px 8px; border-radius: 10px; font-size: 11px; font-weight: 600; }
.kanban-col-body { flex: 1; overflow-y: auto; padding: 8px; display: flex; flex-direction: column; gap: 6px; }
.kanban-col-body::-webkit-scrollbar { width: 4px; }
.kanban-col-body::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

.kanban-card { background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: 10px 12px; cursor: pointer; transition: all .15s; cursor: grab; }
.kanban-card:hover { background: var(--card-hover); border-color: var(--primary); transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,.25); }
.kanban-card.selected { border-color: var(--primary); background: rgba(123,97,255,.08); box-shadow: 0 0 0 1px var(--primary); }
.kanban-card.running { border-left: 3px solid var(--success); }
.kc-name { font-size: 12px; font-weight: 600; color: #fff; line-height: 1.3; margin-bottom: 4px; }
.kc-sub { font-size: 10px; color: var(--text2); margin-bottom: 6px; }
.kc-badges { display: flex; gap: 4px; flex-wrap: wrap; }
.kc-meta { font-size: 10px; color: var(--text3); margin-top: 4px; }
.kanban-empty { text-align: center; padding: 24px 12px; color: var(--text3); font-size: 12px; opacity: .6; }

/* Board split layout */
.split-panel.board-mode .panel-left { flex: 1 1 60%; min-width: 0; max-width: none; }
.split-panel.board-mode .panel-left.full { flex: 1 1 100%; }
</style>
</head>
<body>
<div class="app">
  <header>
    <h1>🧠 <span>Zrise</span> Workflow Manager</h1>
    <div class="header-right">
      <span>Connected as <strong id="current-user" style="color:#fff">...</strong></span>
    </div>
  </header>

  <div class="tabs">
    <button class="tab active" onclick="switchTab('tasks')">📋 Tasks <span class="count" id="tasks-count">0</span></button>
  </div>

  <!-- ═══ TASKS TAB (split panel) ═══ -->
  <div id="tab-tasks" class="tab-content active">
    <div class="stats">
      <div class="stat-card"><div class="label">Total Tasks</div><div class="value v-blue" id="stat-total">-</div></div>
      <div class="stat-card"><div class="label">In Process</div><div class="value v-blue" id="stat-in-process">-</div></div>
      <div class="stat-card"><div class="label">Todo</div><div class="value v-warning" id="stat-todo">-</div></div>
      <div class="stat-card"><div class="label">Done</div><div class="value v-green" id="stat-done">-</div></div>
    </div>
    <div class="toolbar">
      <input class="search" id="task-search" placeholder="🔍 Search tasks..." oninput="filterTasks()">
      <select class="filter-select" id="task-filter" onchange="filterTasks()">
        <option value="">All stages</option>
      </select>
      <div class="view-toggle" id="view-toggle">
        <button class="active" data-view="list" onclick="setView('list')">☰ List</button>
        <button data-view="board" onclick="setView('board')">▦ Board</button>
      </div>
      <button class="btn btn-ghost" onclick="loadTasks()">↻</button>
    </div>
    <div class="split-panel" id="tasks-split">
      <div class="panel-left" id="panel-left">
        <div id="task-list" class="task-list task-list-view active"><div class="loading"><div class="spinner"></div>Loading...</div></div>
        <div id="board-container" class="board-container"></div>
      </div>
      <div class="panel-right" id="panel-right" style="display:flex; flex-direction:column; gap:16px;">
        <div class="wf-canvas" id="workflow-canvas" style="flex:1; min-height:0; overflow-y:auto;">
          <div class="wf-canvas-grid"></div>
          <div class="wf-empty">
            <div class="wf-empty-icon">🔗</div>
            <div class="wf-empty-text">Select a task to view workflow</div>
            <div class="wf-empty-sub">Click any task on the left to open its workflow visualization</div>
          </div>
        </div>
        <!-- Bug 2 fix: Logs expandable section -->
        <div class="logs-panel" id="logs-panel" style="background:var(--card);border:1px solid var(--border);border-radius:10px;max-height:300px;display:flex;flex-direction:column;overflow:hidden;">
          <div class="logs-header" style="padding:12px 14px;border-bottom:1px solid var(--border);cursor:pointer;display:flex;align-items:center;justify-content:space-between;user-select:none;background:var(--bg2);" onclick="toggleLogsPanel()">
            <div style="display:flex;align-items:center;gap:6px;font-weight:600;color:var(--text);font-size:13px;">
              <span id="logs-toggle-icon">▼</span>
              <span>📋 Recent Logs</span>
            </div>
            <span id="logs-count" style="font-size:11px;background:rgba(255,255,255,.1);padding:2px 8px;border-radius:6px;color:var(--text3);">0 turns</span>
          </div>
          <div class="logs-content" id="logs-content" style="flex:1;overflow-y:auto;padding:10px;display:none;">
            <div style="font-size:12px;color:var(--text3);text-align:center;padding:20px;">No logs yet</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- ═══ WORKFLOWS TAB ═══ -->
  <div id="tab-workflows" class="tab-content">
    <div class="toolbar">
      <input class="search" id="wf-search" placeholder="🔍 Search workflows..." oninput="filterWorkflows()">
      <select class="filter-select" id="wf-filter" onchange="filterWorkflows()">
        <option value="">All types</option>
        <option value="builtin">Built-in</option>
        <option value="custom">Custom</option>
      </select>
      <button class="btn btn-primary" onclick="showCreateWorkflow()">+ New Workflow</button>
    </div>
    <div id="workflow-list" class="card-list"><div class="loading"><div class="spinner"></div>Loading...</div></div>
  </div>

  <!-- ═══ MONITOR TAB ═══ -->
  <div id="tab-monitor" class="tab-content">
    <div class="stats">
      <div class="stat-card"><div class="label">Active Sessions</div><div class="value v-blue" id="stat-sessions">-</div></div>
      <div class="stat-card"><div class="label">Running Processes</div><div class="value v-green" id="stat-processes">-</div></div>
      <div class="stat-card"><div class="label">Last Poll</div><div class="value" id="stat-poll" style="font-size:15px;">-</div></div>
    </div>
    <div class="toolbar">
      <button class="btn btn-primary" onclick="loadMonitor()">↻ Refresh</button>
      <button class="btn btn-ghost" id="auto-refresh-btn" onclick="toggleAutoRefresh()">▶ Auto (10s)</button>
    </div>
    <h3 style="font-size:14px;margin-bottom:10px;color:var(--text2)">📋 Active Sessions</h3>
    <div id="session-list" class="card-list"></div>
    <h3 style="font-size:14px;margin:20px 0 10px;color:var(--text2)">🔄 Running Processes</h3>
    <div id="process-list" class="card-list"></div>
  </div>
</div>

<!-- ═══ WORKFLOW EDITOR MODAL ═══ -->
<div class="modal-overlay" id="editor-modal">
  <div class="modal">
    <div class="modal-header">
      <h2 id="editor-title">New Workflow</h2>
      <button class="btn btn-ghost" onclick="hideEditor()" style="font-size:18px;padding:4px 8px;">✕</button>
    </div>
    <div class="modal-body">
      <div class="form-group"><label>Name *</label><input type="text" id="wf-name" placeholder="my-workflow"></div>
      <div class="form-group"><label>Description</label><input type="text" id="wf-desc" placeholder="What does this workflow do?"></div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">
        <div class="form-group"><label>Category</label>
          <select id="wf-category">
            <option value="custom">Custom</option><option value="analysis">Analysis</option>
            <option value="development">Development</option><option value="qa">QA/Testing</option>
            <option value="docs">Documentation</option><option value="pm">PM/Planning</option>
          </select>
        </div>
        <div class="form-group"><label>Visibility</label>
          <select id="wf-visibility">
            <option value="private">Private</option><option value="team">Team</option><option value="public">Public</option>
          </select>
        </div>
      </div>
      <div class="form-group"><label>Workflow YAML *</label>
        <textarea class="code" id="wf-yaml" placeholder="name: my-workflow&#10;steps:&#10;  - id: step1&#10;    command: echo hello"></textarea>
      </div>
    </div>
    <div class="modal-footer">
      <button class="btn btn-ghost" onclick="hideEditor()">Cancel</button>
      <button class="btn btn-primary" onclick="saveWorkflow()">💾 Save</button>
    </div>
  </div>
</div>

<!-- ═══ TASK DETAIL MODAL ═══ -->
<div class="modal-overlay" id="task-modal">
  <div class="modal">
    <div class="modal-header">
      <h2 id="task-modal-title">Task Detail</h2>
      <button class="btn btn-ghost" onclick="hideTaskModal()" style="font-size:18px;padding:4px 8px;">✕</button>
    </div>
    <div class="modal-body" id="task-modal-body"></div>
    <div class="modal-footer" id="task-modal-footer"></div>
  </div>
</div>

<!-- ═══ NODE POPOVER ═══ -->
<div class="node-popover" id="node-popover">
  <button class="np-close" onclick="hideNodePopover()">✕</button>
  <div id="np-content"></div>
</div>

<script>
let allTasks = [], allWorkflows = [], editingId = null, selectedTaskId = null;
let activeSessions = {};
let currentView = 'list'; // 'list' or 'board'
const token = localStorage.getItem('workflow_ui_token') || '';
const headers = {'Content-Type':'application/json'};
if (token) headers['Authorization'] = 'Bearer ' + token;

// ── Auth ──
async function apiFetch(url, opts={}) {
  let res = await fetch(url, {...opts, headers});
  if (res.status === 401) {
    const t = prompt('🔑 Enter workflow UI token:');
    if (t) { localStorage.setItem('workflow_ui_token', t); location.reload(); }
    throw new Error('Unauthorized');
  }
  return res;
}

// ── Tabs ──
function switchTab(tab) {
  document.querySelectorAll('.tab').forEach((t,i) => t.classList.toggle('active', ['tasks','workflows','monitor'][i]===tab));
  document.getElementById('tab-tasks').classList.toggle('active', tab==='tasks');
  document.getElementById('tab-workflows').classList.toggle('active', tab==='workflows');
  document.getElementById('tab-monitor').classList.toggle('active', tab==='monitor');
  if (tab === 'monitor') loadMonitor();
}

// ── Tasks ──
async function loadTasks() {
  try {
    const res = await apiFetch('/api/tasks');
    const data = await res.json();
    allTasks = data.tasks || [];
    document.getElementById('tasks-count').textContent = allTasks.length;
    updateTaskStats();
    renderTasks();
    populateTaskFilter();
    // Also load monitor to know active sessions
    loadActiveSessions();
  } catch(e) { document.getElementById('task-list').innerHTML = '<div class="empty"><div class="empty-icon">⚠️</div><div class="empty-text">Failed: '+e.message+'</div></div>'; }
}

async function loadActiveSessions() {
  try {
    const res = await apiFetch('/api/monitor');
    const d = await res.json();
    activeSessions = {};
    (d.sessions || []).forEach(s => { activeSessions[s.task_id] = s; });
    // Re-render if a task is selected, refresh workflow (silent refresh - don't show loading)
    if (selectedTaskId && activeSessions[selectedTaskId]) {
      loadWorkflowForTask(selectedTaskId, true); // true = silent refresh
    }
  } catch(e) {}
}

function updateTaskStats() {
  const todo = allTasks.filter(t => t.stage.toLowerCase().includes('todo') || t.stage.toLowerCase().includes('backlog') || t.stage.toLowerCase().includes('to-do') || t.stage.toLowerCase().includes('to do')).length;
  const inProcess = allTasks.filter(t => t.stage.toLowerCase().includes('in process') || t.stage.toLowerCase().includes('in progress') || t.stage.toLowerCase().includes('doing')).length;
  const done = allTasks.filter(t => t.stage.toLowerCase().includes('done') || t.stage.toLowerCase().includes('closed') || t.stage.toLowerCase().includes('completed')).length;
  document.getElementById('stat-total').textContent = allTasks.length;
  document.getElementById('stat-in-process').textContent = inProcess;
  document.getElementById('stat-todo').textContent = todo;
  document.getElementById('stat-done').textContent = done;
}

function populateTaskFilter() {
  const stages = [...new Set(allTasks.map(t => t.stage))].sort();
  const sel = document.getElementById('task-filter');
  const val = sel.value;
  sel.innerHTML = '<option value="">All stages</option>' + stages.map(s => '<option value="'+s+'">'+s+'</option>').join('');
  sel.value = val;
}

function filterTasks() {
  const q = document.getElementById('task-search').value.toLowerCase();
  const stage = document.getElementById('task-filter').value;
  const filtered = allTasks.filter(t => {
    if (stage && t.stage !== stage) return false;
    if (q && !t.name.toLowerCase().includes(q) && !t.project.toLowerCase().includes(q)) return false;
    return true;
  });
  renderTaskList(filtered);
  if (currentView === 'board') renderBoard(filtered);
}

function setView(view) {
  currentView = view;
  document.querySelectorAll('#view-toggle button').forEach(b => b.classList.toggle('active', b.dataset.view === view));
  const listEl = document.getElementById('task-list');
  const boardEl = document.getElementById('board-container');
  const split = document.getElementById('tasks-split');
  listEl.classList.toggle('active', view === 'list');
  boardEl.classList.toggle('active', view === 'board');
  split.classList.toggle('board-mode', view === 'board');
  if (view === 'board') {
    const q = document.getElementById('task-search').value.toLowerCase();
    const stage = document.getElementById('task-filter').value;
    const filtered = allTasks.filter(t => {
      if (stage && t.stage !== stage) return false;
      if (q && !t.name.toLowerCase().includes(q) && !t.project.toLowerCase().includes(q)) return false;
      return true;
    });
    renderBoard(filtered);
  }
}

function getStageGroup(stage) {
  const s = stage.toLowerCase();
  if (/^(todo|to[- ]?do|backlog|new)$/i.test(s)) return 'todo';
  if (/in[- ]?(progress|process)|doing|working/i.test(s)) return 'in-progress';
  if (/done|completed|closed|cancel/i.test(s)) return 'done';
  return 'default';
}

function getStageGroupOrder(group) {
  return {todo:0, 'in-progress':1, default:2, done:3}[group] ?? 2;
}

function renderBoard(tasks) {
  const container = document.getElementById('board-container');
  if (!tasks.length) {
    container.innerHTML = '<div class="kanban-empty" style="padding:60px;">📋 No tasks match your filter</div>';
    return;
  }
  // Group by stage
  const groups = {};
  tasks.forEach(t => {
    const stage = t.stage || 'Unknown';
    if (!groups[stage]) groups[stage] = [];
    groups[stage].push(t);
  });
  // Sort columns: todo first, in-progress, default, done last
  const stageNames = Object.keys(groups).sort((a, b) => {
    const ga = getStageGroup(a), gb = getStageGroup(b);
    if (ga !== gb) return getStageGroupOrder(ga) - getStageGroupOrder(gb);
    // Within same group, sort by avg sequence
    const avgA = groups[a].reduce((s,t) => s + (t.stage_sequence||0), 0) / groups[a].length;
    const avgB = groups[b].reduce((s,t) => s + (t.stage_sequence||0), 0) / groups[b].length;
    return avgA - avgB;
  });

  container.innerHTML = stageNames.map(stageName => {
    const group = getStageGroup(stageName);
    const stageTasks = groups[stageName];
    return '<div class="kanban-col">'
      + '<div class="kanban-col-header stage-'+group+'">'
      + '<span>'+escapeHtml(stageName)+'</span>'
      + '<span class="kanban-col-count">'+stageTasks.length+'</span>'
      + '</div>'
      + '<div class="kanban-col-body">'
      + (stageTasks.length === 0 ? '<div class="kanban-empty">No tasks</div>'
        : stageTasks.map(t => renderKanbanCard(t)).join(''))
      + '</div></div>';
  }).join('');
}

function renderKanbanCard(t) {
  const session = activeSessions[t.id];
  const isRunning = session && session.status !== 'done' && session.status !== 'completed';
  const isSelected = t.id === selectedTaskId;
  const stageClass = getStageGroup(t.stage);
  let cls = 'kanban-card';
  if (isSelected) cls += ' selected';
  if (isRunning) cls += ' running';
  const deadline = t.deadline ? '📅 ' + t.deadline.slice(0,10) : '';
  const runningBadge = isRunning ? '<span class="badge badge-running" style="font-size:10px;padding:1px 6px;">🟢</span>' : '';
  return '<div class="'+cls+'" onclick="selectTask('+t.id+')">'
    + '<div class="kc-name">#'+t.id+' '+escapeHtml(t.name)+'</div>'
    + (t.project ? '<div class="kc-sub">'+escapeHtml(t.project)+'</div>' : '')
    + '<div class="kc-badges">'
    + '<span class="badge badge-'+stageClass+'" style="font-size:10px;padding:1px 6px;">'+escapeHtml(t.stage)+'</span>'
    + runningBadge
    + '</div>'
    + (deadline ? '<div class="kc-meta">'+deadline+'</div>' : '')
    + '</div>';
}

function renderTasks() { renderTaskList(allTasks); if (currentView === 'board') renderBoard(allTasks); }

function renderTaskList(tasks) {
  const c = document.getElementById('task-list');
  if (!tasks.length) { c.innerHTML = '<div class="empty"><div class="empty-icon">📋</div><div class="empty-text">No tasks found</div></div>'; return; }
  // Sort: running sessions first, then others
  const sorted = [...tasks].sort((a, b) => {
    const aRun = activeSessions[a.id] && activeSessions[a.id].status !== 'done' ? 0 : 1;
    const bRun = activeSessions[b.id] && activeSessions[b.id].status !== 'done' ? 0 : 1;
    return aRun - bRun;
  });
  c.innerHTML = sorted.map(t => {
    const session = activeSessions[t.id];
    const isRunning = session && session.status !== 'done' && session.status !== 'completed';
    const stageClass = t.stage.toLowerCase().includes('done') || t.stage.toLowerCase().includes('closed') ? 'done'
      : t.stage.toLowerCase().includes('in process') || t.stage.toLowerCase().includes('in progress') || t.stage.toLowerCase().includes('doing') ? 'in-process' : 'todo';
    const isSelected = t.id === selectedTaskId;
    let cls = 'task-card';
    if (isSelected) cls += ' selected';
    if (isRunning) cls += ' running';
    else if (!session && !isRunning) cls += ' dimmed';
    const deadline = t.deadline ? '📅 ' + t.deadline.slice(0,10) : '';
    const updated = t.updated ? new Date(t.updated).toLocaleDateString('vi-VN') : '';
    const runningBadge = isRunning ? '<span class="badge badge-running">🟢 Running</span>' : '';
    const stepBadge = isRunning && session.current_step ? '<span class="badge" style="background:var(--blue-bg);color:var(--blue)">' + session.current_step + '</span>' : '';
    return '<div class="'+cls+'" onclick="selectTask('+t.id+')">'
      +'<div class="tc-header">'
      +'<div>'
      +'<div class="tc-name">#'+t.id+' '+escapeHtml(t.name)+'</div>'
      +'<div class="tc-sub">'+escapeHtml(t.project)+'</div>'
      +'</div>'
      +'<div class="tc-badges">'
      +'<span class="badge badge-'+stageClass+'">'+t.stage+'</span>'
      +runningBadge + stepBadge
      +'</div></div>'
      +'<div class="tc-meta">'+deadline+(deadline?' · ':'')+(updated||'')+'</div>'
      +'</div>';
  }).join('');
}

function selectTask(id) {
  selectedTaskId = id;
  renderTasks();
  loadWorkflowForTask(id);
  document.getElementById('panel-left').classList.remove('full');
}

async function loadWorkflowForTask(taskId, silentRefresh = false) {
  const canvas = document.getElementById('workflow-canvas');
  
  // Always use pulsing dot indicator - never show full loading spinner
  showRefreshIndicator();
  canvas.style.opacity = '0.7';
  canvas.style.transition = 'opacity 0.2s';
  
  try {
    const res = await apiFetch('/api/sessions/'+taskId+'/timeline');
    const d = await res.json();
    console.log('[WF] timeline response:', JSON.stringify(d).substring(0, 2000));
    if (!d.ok) {
      console.warn('[WF] timeline not ok:', d);
      canvas.style.opacity = '1';
      canvas.innerHTML = '<div class="wf-canvas-grid"></div><div class="wf-empty"><div class="wf-empty-icon">📭</div><div class="wf-empty-text">No workflow session yet</div><div class="wf-empty-sub">Task #'+taskId+' has not started a workflow</div></div>';
      showWorkflowHeader(canvas, {task_id: taskId, task_name: allTasks.find(t=>t.id===taskId)?.name || 'Task #'+taskId, workflow:'-', current_step:'-', current_phase:'plan', iteration:'0', total_turns:'0', phases:[]}, false);
      hideRefreshIndicator();
      return;
    }
    console.log('[WF] rendering canvas, phases:', d.phases?.length, 'step:', d.current_step, 'status:', d.status, 'error:', d.error);
    renderWorkflowCanvas(canvas, d, silentRefresh);
    canvas.style.opacity = '1';
    hideRefreshIndicator();
  } catch(e) {
    console.error('[WF] loadWorkflowForTask error:', e);
    canvas.style.opacity = '1';
    canvas.innerHTML = '<div class="wf-canvas-grid"></div><div class="wf-empty"><div class="wf-empty-icon">⚠️</div><div class="wf-empty-text">Error loading workflow</div><div class="wf-empty-sub">'+e.message+'</div></div>';
    hideRefreshIndicator();
  }
}

function showRefreshIndicator() {
  let indicator = document.getElementById('refresh-indicator');
  if (!indicator) {
    indicator = document.createElement('div');
    indicator.id = 'refresh-indicator';
    indicator.style.cssText = 'position:fixed;top:12px;right:12px;z-index:9999;display:flex;align-items:center;gap:6px;font-size:12px;color:var(--text3);opacity:0;transition:opacity 0.2s;';
    indicator.innerHTML = '<div style="width:8px;height:8px;border-radius:50%;background:var(--accent);animation:pulse 1s infinite;"></div><span>Updating...</span>';
    document.body.appendChild(indicator);
  }
  indicator.style.opacity = '1';
}

function hideRefreshIndicator() {
  const indicator = document.getElementById('refresh-indicator');
  if (indicator) indicator.style.opacity = '0';
}

function showWorkflowHeader(canvas, d, hasSession) {
  const existing = canvas.querySelector('.wf-header');
  if (existing) return;
  const hdr = document.createElement('div');
  hdr.className = 'wf-header';
  hdr.innerHTML = '<div class="wf-header-title">🔗 #'+d.task_id+' '+escapeHtml(d.task_name)+'</div>'
    +'<div class="wf-actions">'
    +'<button class="btn btn-accent btn-sm" onclick="triggerPhase(\'plan\')">📋 Re-plan</button>'
    +(hasSession ? '<button class="btn btn-primary btn-sm" onclick="triggerCurrent()">▶ Resume</button>' : '')
    +'<button class="btn btn-blue btn-sm" onclick="triggerPhase(\'execute\')">⚡ Execute</button>'
    +'<button class="btn btn-success btn-sm" onclick="triggerPhase(\'approve\')">✅ Approve</button>'
    +'<button class="btn btn-ghost btn-sm" onclick="loadWorkflowForTask('+d.task_id+')">↻</button>'
    +'</div>';
  canvas.appendChild(hdr);
}

function renderWorkflowCanvas(canvas, d) {
  console.log('[WF] renderWorkflowCanvas called, phases:', d?.phases?.length, 'task:', d?.task_id);
  try {
  window._tlData = d;
  // Bug 2 & 3 fix: Update logs panel and setup auto-refresh
  updateLogsPanel(d);

  // Find the canvas element, excluding the logs panel
  const canvasBody = canvas.querySelector('.wf-body') ? canvas : (() => {
    // Clear only the workflow content, not the logs panel
    const grid = canvas.querySelector('.wf-canvas-grid');
    const header = canvas.querySelector('.wf-header');
    const info = canvas.querySelector('.wf-info');
    const errBanner = canvas.querySelector('.wf-error-banner');
    const body = canvas.querySelector('.wf-body');
    const emptyState = canvas.querySelector('.wf-empty');
    [header, info, errBanner, body, grid, emptyState].forEach(el => el && el.remove());
    return canvas;
  })();

  if (!d || !d.phases || d.phases.length === 0) {
    const grid = document.createElement('div');
    grid.className = 'wf-canvas-grid';
    canvasBody.appendChild(grid);
    const emptyEl = document.createElement('div');
    emptyEl.className = 'wf-empty';
    emptyEl.innerHTML = '<div class="wf-empty-icon">📭</div><div class="wf-empty-text">No workflow data</div>';
    canvasBody.appendChild(emptyEl);
    return;
  }

  // Header
  const hdr = document.createElement('div');
  hdr.className = 'wf-header';
  hdr.innerHTML = '<div class="wf-header-title">🔗 #'+d.task_id+' '+escapeHtml(d.task_name)+'</div>'
    +'<div class="wf-actions">'
    +'<button class="btn btn-accent btn-sm" onclick="triggerPhase(\'plan\')">📋 Re-plan</button>'
    +'<button class="btn btn-primary btn-sm" onclick="triggerCurrent()">▶ Resume</button>'
    +'<button class="btn btn-blue btn-sm" onclick="triggerPhase(\'execute\')">⚡ Execute</button>'
    +'<button class="btn btn-success btn-sm" onclick="triggerPhase(\'approve\')">✅ Approve</button>'
    +'<button class="btn btn-ghost btn-sm" onclick="loadWorkflowForTask('+d.task_id+')">↻</button>'
    +'</div>';
  canvasBody.appendChild(hdr);

  // Info bar
  const info = document.createElement('div');
  info.className = 'wf-info';
  info.innerHTML = '<div class="wf-info-item">Workflow: <strong>'+d.workflow+'</strong></div>'
    +'<div class="wf-info-item">Step: <strong>'+d.current_step+'</strong></div>'
    +'<div class="wf-info-item">Iteration: <strong>'+d.iteration+'</strong></div>'
    +'<div class="wf-info-item">Turns: <strong>'+d.total_turns+'</strong></div>';
  canvasBody.appendChild(info);

  // Error banner nếu có
  if (d.error) {
    const errBanner = document.createElement('div');
    errBanner.className = 'wf-error-banner';
    errBanner.innerHTML = '<strong>⚠️ Lỗi:</strong> ' + escapeHtml(d.error);
    canvasBody.appendChild(errBanner);
  }

  // Grid background
  const grid = document.createElement('div');
  grid.className = 'wf-canvas-grid';
  canvasBody.appendChild(grid);

  // Body with nodes
  const body = document.createElement('div');
  body.className = 'wf-body';

  // Build all steps flat
  const allSteps = [];
  (d.phases || []).forEach(phase => {
    phase.steps.forEach(step => {
      allSteps.push({...step, phaseName: phase.name, phaseLabel: phase.label});
    });
  });

  // Render nodes row by row
  const container = document.createElement('div');
  container.className = 'nodes-container';

  (d.phases || []).forEach((phase, pi) => {
    const phaseDiv = document.createElement('div');
    phaseDiv.style.position = 'relative';
    phaseDiv.style.paddingTop = '20px';

    const label = document.createElement('div');
    label.className = 'node-phase-label';
    label.textContent = phase.label;
    phaseDiv.appendChild(label);

    const row = document.createElement('div');
    row.className = 'node-row';

    phase.steps.forEach((step, si) => {
      if (si > 0) {
        // Connection
        const conn = document.createElement('div');
        conn.className = 'node-connector';
        const prevStep = phase.steps[si-1];
        const prevCompleted = prevStep.state === 'completed';
        const isActive = step.state === 'active';
        if (prevCompleted) conn.classList.add('completed');
        else if (isActive) conn.classList.add('active');
        conn.innerHTML = '<svg viewBox="0 0 80 40"><path d="M0,20 C20,20 20,20 40,20 S60,20 80,20"/></svg>';
        row.appendChild(conn);
      }

      // Node
      const node = document.createElement('div');
      const stateClass = step.state || 'upcoming';
      node.className = 'node ' + stateClass;
      node.dataset.stepId = step.id;
      node.dataset.phaseName = phase.name;

      const statusLabel = step.state === 'completed' ? '✓ Done' : step.state === 'active' ? '● Running' : step.state === 'pending' ? '○ Pending' : '◯ Queued';
      node.innerHTML = '<div class="node-icon">'+step.icon+'</div>'
        +'<div class="node-name">'+(step.desc||step.id).split(':').pop().trim().substring(0,20)+'</div>'
        +'<div class="node-status">'+statusLabel+'</div>';

      node.addEventListener('click', (e) => {
        e.stopPropagation();
        showNodePopover(e, step, phase, d);
      });
      row.appendChild(node);
    });

    phaseDiv.appendChild(row);
    container.appendChild(phaseDiv);
  });

  body.appendChild(container);
  canvasBody.appendChild(body);
  console.log('[WF] renderWorkflowCanvas done');
  } catch(e) {
    console.error('[WF] renderWorkflowCanvas CRASH:', e, e.stack);
    canvas.innerHTML = '<div class="wf-canvas-grid"></div><div class="wf-empty"><div class="wf-empty-icon">💥</div><div class="wf-empty-text">Render error: '+e.message+'</div><div class="wf-empty-sub" style="white-space:pre-wrap;font-size:11px;color:#f87171">'+escapeHtml(e.stack||'')+'</div></div>';
  }
}

function showNodePopover(event, step, phase, data) {
  const pop = document.getElementById('node-popover');
  const content = document.getElementById('np-content');
  const isActive = step.state === 'active' || step.state === 'pending';
  const hasLogs = step.logs && step.logs.length > 0;

  let html = '<div class="np-header"><span style="font-size:24px">'+step.icon+'</span><div><div class="np-title">'+escapeHtml(step.desc)+'</div><div class="np-desc">'+step.id+' · '+step.state+'</div></div></div>';

  html += '<div class="np-actions">';
  if (isActive) {
    html += '<button class="btn btn-primary btn-sm" onclick="triggerStep(\''+phase.name+'\',\''+step.id+'\'); hideNodePopover()">▶ Run from here</button>';
  }
  html += '</div>';

  if (hasLogs) {
    html += '<div class="np-logs">';
    step.logs.forEach(log => {
      html += '<div class="np-log-item">';
      html += '<div class="np-log-role">'+(log.author||log.role||log.agent||'system')+'</div>';
      html += '<div class="np-log-content">'+escapeHtml(log.content)+'</div>';
      if (log.timestamp) html += '<div class="np-log-time">'+log.timestamp+'</div>';
      html += '</div>';
    });
    html += '</div>';
  } else {
    html += '<div style="font-size:12px;color:var(--text3)">No logs yet</div>';
  }

  content.innerHTML = html;

  // Position
  const rect = event.target.closest('.node').getBoundingClientRect();
  let left = rect.right + 10;
  let top = rect.top;
  if (left + 340 > window.innerWidth) left = rect.left - 330;
  if (top + 300 > window.innerHeight) top = window.innerHeight - 310;
  if (top < 10) top = 10;
  pop.style.left = left + 'px';
  pop.style.top = top + 'px';
  pop.classList.add('show');
}

function hideNodePopover() {
  document.getElementById('node-popover').classList.remove('show');
}

// ── Bug 2 fix: Logs panel functions ──
function updateLogsPanel(d) {
  if (!d || !d.step_logs) return;
  const logsContent = document.getElementById('logs-content');
  const logsCount = document.getElementById('logs-count');

  // Collect all logs from all steps
  const allLogs = [];
  Object.values(d.step_logs || {}).forEach(stepLogs => {
    allLogs.push(...stepLogs);
  });

  logsCount.textContent = allLogs.length + ' turns';

  if (allLogs.length === 0) {
    logsContent.innerHTML = '<div style="font-size:12px;color:var(--text3);text-align:center;padding:20px;">No logs yet</div>';
    return;
  }

  // Show recent logs (last 10)
  let html = '';
  const recentLogs = allLogs.slice(-10);
  recentLogs.forEach(log => {
    const role = log.author || log.role || log.agent || 'system';
    const time = log.timestamp ? new Date(log.timestamp).toLocaleTimeString('en-US', {hour:'2-digit',minute:'2-digit',second:'2-digit'}) : '';
    html += '<div class="log-turn">'
      + '<div class="log-turn-meta">'
      + '<span class="log-turn-role">' + escapeHtml(role) + '</span>'
      + (time ? '<span class="log-turn-time">' + time + '</span>' : '')
      + '</div>'
      + '<div class="log-turn-content">' + escapeHtml(log.content || '') + '</div>'
      + '</div>';
  });
  logsContent.innerHTML = html;
}

function toggleLogsPanel() {
  const content = document.getElementById('logs-content');
  const icon = document.getElementById('logs-toggle-icon');
  if (content.style.display === 'none') {
    content.style.display = 'block';
    icon.textContent = '▼';
  } else {
    content.style.display = 'none';
    icon.textContent = '▶';
  }
}

// ── Bug 2 & 3 fix: Global auto-polling for active sessions ──
let _autoPollInterval = null;

function startGlobalAutoPoll() {
  if (_autoPollInterval) return;

  _autoPollInterval = setInterval(async () => {
    // Check all sessions for non-done status
    try {
      const res = await apiFetch('/api/monitor');
      const data = await res.json();

      if (!data.ok) return;

      const activeSessions = data.sessions.filter(s =>
        s.status !== 'done' && s.status !== 'completed'
      );

      // If there are active sessions, refresh the selected task's workflow
      if (activeSessions.length > 0 && window.selectedTaskId) {
        const selectedSession = activeSessions.find(s => s.task_id === window.selectedTaskId);
        if (selectedSession) {
          await loadWorkflowForTask(window.selectedTaskId, true); // silent refresh
        }
      }
    } catch(e) {
      // Silently fail, poll will retry
    }
  }, 5000); // Poll every 5 seconds
}

function stopGlobalAutoPoll() {
  if (_autoPollInterval) {
    clearInterval(_autoPollInterval);
    _autoPollInterval = null;
  }
}

// ── Trigger ──
function triggerCurrent() {
  if (!window._tlData) return;
  triggerStep(window._tlData.current_phase, window._tlData.current_step);
}

function triggerPhase(phase) {
  triggerStep(phase, '');
}

async function triggerStep(phase, step) {
  const d = window._tlData;
  if (!d) return;
  const task_id = d.task_id;
  const wf = d.workflow || 'general';
  if (phase === 'approve' || step === 'done') {
    if (!confirm('Approve task #'+task_id+' and move to Done?')) return;
  }
  const label = step || phase + ' phase';
  try {
    const res = await apiFetch('/api/sessions/'+task_id+'/trigger', {
      method: 'POST',
      body: JSON.stringify({ phase, step, workflow: wf })
    });
    const data = await res.json();
    if (data.ok) {
      showToast('✅ Triggered: '+label+' (PID: '+data.pid+')');
      // Bug 2 & 3 fix: Start global auto-polling
      startGlobalAutoPoll();
      // Also poll mỗi 5s cho đến khi status thay đổi khỏi processing
      const pollInterval = setInterval(async () => {
        try {
          const tr = await apiFetch('/api/sessions/'+task_id+'/timeline');
          const td = await tr.json();
          if (td.ok && td.status !== 'processing') {
            clearInterval(pollInterval);
          }
          loadWorkflowForTask(task_id, true); // silent refresh
        } catch(e) { clearInterval(pollInterval); }
      }, 5000);
      setTimeout(() => loadWorkflowForTask(task_id, true), 2000); // silent refresh
    } else {
      showToast('❌ Error: ' + JSON.stringify(data.error));
    }
  } catch(e) { showToast('❌ ' + e.message); }
}

// ── Toast ──
function showToast(msg) {
  let t = document.getElementById('toast');
  if (!t) {
    t = document.createElement('div');
    t.id = 'toast';
    t.style.cssText = 'position:fixed;bottom:20px;right:20px;z-index:999;background:var(--card);border:1px solid var(--border);border-radius:10px;padding:12px 18px;font-size:13px;color:var(--text);box-shadow:0 8px 30px rgba(0,0,0,.4);transition:opacity .3s;max-width:400px;';
    document.body.appendChild(t);
  }
  t.textContent = msg;
  t.style.opacity = '1';
  clearTimeout(t._timer);
  t._timer = setTimeout(() => { t.style.opacity = '0'; }, 4000);
}

// ── Task Detail Modal (keep for deep link) ──
async function showTask(id) {
  selectTask(id);
}

async function showTaskModal(id) {
  try {
    const res = await apiFetch('/api/tasks/' + id);
    const data = await res.json();
    const t = data.task;
    document.getElementById('task-modal-title').textContent = '#' + t.id + ' ' + t.name;
    const body = document.getElementById('task-modal-body');
    const isDone = t.stage.toLowerCase().includes('done') || t.stage.toLowerCase().includes('closed');
    body.innerHTML = '<div style="margin-bottom:14px"><span class="badge badge-todo" style="font-size:13px;padding:5px 12px;">'+t.stage+'</span> <span class="badge badge-'+(t.priority==='1'?'high':'normal')+'">'+(t.priority==='1'?'High':'Normal')+'</span></div>'
      +'<div style="margin-bottom:10px;font-size:12px;color:var(--text2)">Project: <strong style="color:var(--text)">'+t.project+'</strong></div>'
      +(t.deadline ? '<div style="margin-bottom:10px;font-size:12px;color:var(--text2)">Deadline: '+t.deadline.slice(0,10)+'</div>' : '')
      +'<div style="background:var(--bg);border-radius:8px;padding:14px;font-size:13px;line-height:1.7;white-space:pre-wrap;max-height:300px;overflow-y:auto;">'+escapeHtml(t.description||'(no description)')+'</div>'
      +'<div style="margin-top:10px"><a class="task-link" href="'+t.url+'" target="_blank">🔗 Open in Zrise</a></div>';
    const footer = document.getElementById('task-modal-footer');
    footer.innerHTML = '<button class="btn btn-ghost" onclick="hideTaskModal()">Close</button>'
      +(isDone ? '' : '<button class="btn btn-success" onclick="approveTask('+t.id+')">✅ Approve → Done</button>');
    document.getElementById('task-modal').classList.add('show');
  } catch(e) { alert('Error: ' + e.message); }
}

async function approveTask(id, approveType = null) {
  // Hiển thị modal để user chọn approve type nếu không được chỉ định
  if (!approveType) {
    // Tự động phát hiện dựa trên trạng thái task
    const task = allTasks.find(t => t.id === id);
    if (!task) { showToast('❌ Task not found'); return; }
    
    // Kiểm tra xem task đã có kết quả AI chưa (đơn giản hóa: nếu stage là In Process và đã chạy workflow → assume có result)
    const hasResult = task.stage === 'In Process' && activeSessions[id];
    
    if (hasResult) {
      approveType = 'result';
    } else {
      approveType = 'plan';
    }
  }
  
  const typeLabel = approveType === 'plan' ? 'Plan' : 'Kết quả';
  if (!confirm(`Approve ${typeLabel} cho task #${id}?`)) return;
  
  try {
    const res = await apiFetch('/api/tasks/'+id+'/approve', {
      method: 'POST',
      body: JSON.stringify({ approve_type: approveType })
    });
    const data = await res.json();
    if (data.ok) {
      showToast('✅ ' + (data.message || `${typeLabel} đã được approve`));
      loadTasks();
      if (selectedTaskId === id) loadWorkflowForTask(id);
    } else {
      showToast('❌ ' + (data.error || JSON.stringify(data)));
    }
  } catch(e) {
    showToast('❌ ' + e.message);
  }
}
function hideTaskModal() { document.getElementById('task-modal').classList.remove('show'); }

// ── Workflows ──
async function loadWorkflows() {
  try {
    const res = await apiFetch('/api/workflows');
    const data = await res.json();
    allWorkflows = data.workflows || [];
    document.getElementById('workflows-count').textContent = allWorkflows.length;
    renderWorkflows();
  } catch(e) { document.getElementById('workflow-list').innerHTML = '<div class="empty"><div class="empty-icon">⚡</div><div class="empty-text">Failed</div></div>'; }
}

function filterWorkflows() {
  const q = document.getElementById('wf-search').value.toLowerCase();
  const f = document.getElementById('wf-filter').value;
  const filtered = allWorkflows.filter(w => {
    if (f === 'builtin' && w.source !== 'builtin') return false;
    if (f === 'custom' && w.source === 'builtin') return false;
    if (q && !w.name.toLowerCase().includes(q) && !(w.description||'').toLowerCase().includes(q)) return false;
    return true;
  });
  renderWorkflowList(filtered);
}

function renderWorkflows() { renderWorkflowList(allWorkflows); }

function renderWorkflowList(list) {
  const c = document.getElementById('workflow-list');
  if (!list.length) { c.innerHTML = '<div class="empty"><div class="empty-icon">⚡</div><div class="empty-text">No workflows found</div></div>'; return; }
  c.innerHTML = list.map(w => {
    const isBuiltin = w.source === 'builtin';
    const desc = w.description || '';
    const tags = (w.tags || []).map(t => '<span class="badge badge-custom" style="font-size:10px">'+t+'</span>').join(' ');
    return '<div class="card">'
      +'<div class="card-header">'
      +'<div>'
      +'<div class="card-title">'+w.name+' <span class="badge '+(isBuiltin?'badge-builtin':'badge-custom')+'">'+(isBuiltin?'built-in':'custom')+'</span></div>'
      +'<div class="card-subtitle">'+(w.category||'custom')+' · '+(w.owner||'system')+'</div>'
      +'</div>'
      +'<div class="card-actions">'
      +(isBuiltin ? '<span style="font-size:11px;color:var(--text3)">read-only</span>' : '<button class="btn btn-ghost btn-sm" onclick="event.stopPropagation();editWorkflow(\''+w.workflow_id+'\')">✏️</button><button class="btn btn-danger btn-sm" onclick="event.stopPropagation();deleteWorkflow(\''+w.workflow_id+'\')">🗑️</button>')
      +'</div></div>'
      +(desc ? '<div class="card-desc">'+desc+'</div>' : '')
      +(tags ? '<div class="card-meta">'+tags+'</div>' : '')
      +'</div>';
  }).join('');
}

function showCreateWorkflow() {
  editingId = null;
  document.getElementById('editor-title').textContent = 'New Workflow';
  document.getElementById('wf-name').value = '';
  document.getElementById('wf-desc').value = '';
  document.getElementById('wf-category').value = 'custom';
  document.getElementById('wf-visibility').value = 'private';
  document.getElementById('wf-yaml').value = 'name: my-workflow\nsteps:\n  - id: step1\n    command: echo "Hello"';
  document.getElementById('editor-modal').classList.add('show');
}

async function editWorkflow(id) {
  const wf = allWorkflows.find(w => w.workflow_id === id);
  if (!wf || wf.source === 'builtin') return;
  editingId = id;
  document.getElementById('editor-title').textContent = 'Edit Workflow';
  document.getElementById('wf-name').value = wf.name;
  document.getElementById('wf-desc').value = wf.description || '';
  document.getElementById('wf-category').value = wf.category || 'custom';
  document.getElementById('wf-visibility').value = wf.visibility || 'private';
  try {
    const res = await apiFetch('/api/workflows/'+id+'/yaml');
    const data = await res.json();
    document.getElementById('wf-yaml').value = data.yaml || '';
  } catch(e) {}
  document.getElementById('editor-modal').classList.add('show');
}

function hideEditor() { document.getElementById('editor-modal').classList.remove('show'); }

async function saveWorkflow() {
  const name = document.getElementById('wf-name').value.trim();
  const yaml = document.getElementById('wf-yaml').value.trim();
  if (!name || !yaml) { showToast('Name and YAML required'); return; }
  const body = { name, yaml, description: document.getElementById('wf-desc').value, category: document.getElementById('wf-category').value, visibility: document.getElementById('wf-visibility').value };
  let url = '/api/workflows', method = 'POST';
  if (editingId) { url = '/api/workflows/' + editingId; method = 'PUT'; }
  try {
    const res = await apiFetch(url, {method, body: JSON.stringify(body)});
    const data = await res.json();
    if (data.ok) { hideEditor(); loadWorkflows(); }
    else { showToast('❌ ' + JSON.stringify(data.errors || data.error)); }
  } catch(e) { showToast('❌ ' + e.message); }
}

async function deleteWorkflow(id) {
  if (!confirm('Delete "'+id+'"?')) return;
  try {
    const res = await apiFetch('/api/workflows/'+id, {method:'DELETE'});
    const data = await res.json();
    if (data.ok) loadWorkflows(); else showToast('❌ ' + data.error);
  } catch(e) { showToast('❌ ' + e.message); }
}

// ── Monitor ──
let monitorInterval = null;

async function loadMonitor() {
  try {
    const res = await apiFetch('/api/monitor');
    const d = await res.json();
    document.getElementById('stat-sessions').textContent = d.sessions.length;
    document.getElementById('stat-processes').textContent = d.processes.length;
    document.getElementById('stat-poll').textContent = d.poll_state ? timeAgo(new Date(d.poll_state.last_poll)) : 'N/A';

    const sc = document.getElementById('session-list');
    if (!d.sessions.length) {
      sc.innerHTML = '<div class="empty"><div class="empty-icon">📋</div><div class="empty-text">No active sessions</div></div>';
    } else {
      sc.innerHTML = d.sessions.map(s => {
        const stepLabel = s.current_step || s.status;
        const wfLabel = s.workflow ? '⚡ ' + s.workflow : '';
        const iterLabel = s.iteration > 1 ? ' (iter '+s.iteration+')' : '';
        return '<div class="card" style="cursor:pointer" onclick="switchTab(\'tasks\');selectTask('+s.task_id+')">'
          +'<div class="card-header">'
          +'<div>'
          +'<div class="card-title" style="color:var(--primary2)">#'+s.task_id+' '+escapeHtml(s.task_name)+'</div>'
          +'<div class="card-subtitle">'+s.project+' '+wfLabel+iterLabel+'</div>'
          +'</div>'
          +'<div class="card-actions">'
          +'<span class="badge badge-running" style="animation:none">🟢 '+stepLabel+'</span>'
          +'</div></div>'
          +'<div class="card-meta">'
          +'<span>🕐 '+s.age+'</span>'
          +(s.turns_count ? '<span>💬 '+s.turns_count+'</span>' : '')
          +'</div></div>';
      }).join('');
    }

    const pc = document.getElementById('process-list');
    if (!d.processes.length) {
      pc.innerHTML = '<div class="empty"><div class="empty-icon">🔄</div><div class="empty-text">No running processes</div></div>';
    } else {
      pc.innerHTML = d.processes.map(p => '<div class="card" style="padding:10px 14px">'
        +'<div style="display:flex;align-items:center;gap:10px">'
        +'<span style="font-family:monospace;font-size:11px;color:var(--text3)">PID '+p.pid+'</span>'
        +'<span style="font-size:12px;flex:1;word-break:break-all;color:var(--text2)">'+escapeHtml(p.command)+'</span>'
        +'<span class="badge badge-'+(p.is_lobster?'in-process':'custom')+'">'+(p.is_lobster?'lobster':'system')+'</span>'
        +'</div></div>').join('');
    }
  } catch(e) { console.error('Monitor:', e); }
}

function timeAgo(date) {
  const s = Math.floor((Date.now()-date.getTime())/1000);
  if (s<60) return s+'s ago'; if (s<3600) return Math.floor(s/60)+'m ago';
  if (s<86400) return Math.floor(s/3600)+'h ago'; return Math.floor(s/86400)+'d ago';
}

function escapeHtml(str) { return String(str).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

function toggleAutoRefresh() {
  const btn = document.getElementById('auto-refresh-btn');
  if (monitorInterval) { clearInterval(monitorInterval); monitorInterval=null; btn.textContent='▶ Auto (10s)'; btn.style.background=''; btn.style.color=''; }
  else { monitorInterval = setInterval(loadMonitor, 10000); btn.textContent='⏸ Stop'; btn.style.background='var(--primary)'; btn.style.color='#fff'; loadMonitor(); }
}

// ── Init ──
async function init() {
  try {
    const res = await apiFetch('/api/workflows');
    const data = await res.json();
    document.getElementById('current-user').textContent = data.workflows ? (data.workflows[0]?.owner || '') : '';
  } catch(e) {}
  loadTasks();
  loadWorkflows();
  // Bug 2 & 3 fix: Start global auto-polling on init
  startGlobalAutoPoll();
}

// Close popover on outside click
document.addEventListener('click', (e) => {
  if (!e.target.closest('.node-popover') && !e.target.closest('.node')) hideNodePopover();
});

init();
</script>

</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description='Zrise Workflow + Task Manager UI')
    parser.add_argument('--port', type=int, default=0)
    parser.add_argument('--host', default='0.0.0.0')
    args = parser.parse_args()

    port = args.port or int(os.environ.get('WORKFLOW_UI_PORT', '0'))
    if not port:
        try:
            cfg = json.loads(open(os.path.expanduser('~/.openclaw/openclaw.json')).read())
            port = cfg.get('skills', {}).get('entries', {}).get('zrise-connect', {}).get('ui', {}).get('port', 8080)
        except Exception:
            port = 8080

    server = HTTPServer((args.host, port), WorkflowAPIHandler)
    tk = get_auth_token()
    print(f"🌐 Zrise Workflow Manager UI running at http://localhost:{port}")
    if tk:
        print(f"   Token: {tk[:8]}...")
    else:
        print(f"   Open access (no token)")
    print(f"   Press Ctrl+C to stop")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
        server.shutdown()


if __name__ == '__main__':
    main()
