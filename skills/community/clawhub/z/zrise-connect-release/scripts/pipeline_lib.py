#!/usr/bin/env python3
import hashlib
import json
import pathlib
import re
import tempfile
from datetime import datetime, timezone

from zrise_utils import get_root
ROOT = get_root()
STATE_ROOT = ROOT / 'state' / 'zrise'
PIPELINE_ROOT = STATE_ROOT / 'pipeline'
OUTBOX_ROOT = PIPELINE_ROOT / 'outbox'
INBOX_ROOT = PIPELINE_ROOT / 'inbox'
COMMAND_ROOT = PIPELINE_ROOT / 'commands'
ACTIVE_ROOT = PIPELINE_ROOT / 'active'
EVENT_RECEIPTS_ROOT = PIPELINE_ROOT / 'event-receipts'
SERVICE_ROOT = PIPELINE_ROOT / 'service'
WORK_ITEM_ROOT = STATE_ROOT / 'work-items'

WORK_ITEM_ID_RE = re.compile(r'(zrise-(?:task|activity)-\d+)', re.IGNORECASE)


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def ensure_runtime_dirs():
    for path in [STATE_ROOT, PIPELINE_ROOT, OUTBOX_ROOT, INBOX_ROOT, COMMAND_ROOT, ACTIVE_ROOT, EVENT_RECEIPTS_ROOT, SERVICE_ROOT, WORK_ITEM_ROOT]:
        path.mkdir(parents=True, exist_ok=True)


def load_json(path: pathlib.Path, default=None):
    if not path.exists():
        return {} if default is None else default
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def atomic_write_json(path: pathlib.Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile('w', delete=False, dir=str(path.parent), encoding='utf-8') as tmp:
        json.dump(data, tmp, ensure_ascii=False, indent=2)
        tmp.flush()
        pathlib.Path(tmp.name).replace(path)


def delivery_key(delivery: dict):
    channel = delivery.get('channel') or 'unknown'
    account_id = delivery.get('account_id') or 'default'
    chat_id = delivery.get('chat_id') if delivery.get('chat_id') is not None else 'na'
    topic_id = delivery.get('topic_id') if delivery.get('topic_id') is not None else 'na'
    return f'{channel}__{account_id}__{chat_id}__{topic_id}'


def message_fingerprint(payload: dict):
    return hashlib.sha1(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode('utf-8')).hexdigest()


def event_fingerprint(event: dict):
    payload = {
        'employee_key': event.get('employee_key'),
        'event_type': event.get('event_type'),
        'task_id': event.get('task_id'),
        'activity_id': event.get('activity_id'),
        'task_name': event.get('task_name'),
        'activity_summary': event.get('activity_summary'),
        'project_name': event.get('project_name'),
        'stage': event.get('stage'),
        'deadline': event.get('deadline'),
        'source_hash': event.get('source_hash'),
    }
    return message_fingerprint(payload)


def receipt_path(event_id: str):
    return EVENT_RECEIPTS_ROOT / f'{event_id}.json'


def has_receipt(event_id: str):
    return receipt_path(event_id).exists()


def write_receipt(event_id: str, payload: dict):
    atomic_write_json(receipt_path(event_id), payload)


def outbox_path(outbox_id: str):
    return OUTBOX_ROOT / f'{outbox_id}.json'


def enqueue_outbox(message: dict):
    ensure_runtime_dirs()
    outbox_id = message['outbox_id']
    path = outbox_path(outbox_id)
    if path.exists():
        return load_json(path), False
    atomic_write_json(path, message)
    return message, True


def list_outbox(filter_fn=None):
    ensure_runtime_dirs()
    rows = []
    for path in sorted(OUTBOX_ROOT.glob('*.json')):
        obj = load_json(path, default={})
        obj['_path'] = str(path)
        if filter_fn and not filter_fn(obj):
            continue
        rows.append(obj)
    rows.sort(key=lambda x: x.get('created_at', ''))
    return rows


def mark_outbox_sent(outbox_id: str, extra=None):
    extra = extra or {}
    path = outbox_path(outbox_id)
    obj = load_json(path, default={})
    if not obj:
        return {}
    obj['status'] = 'sent'
    obj['sent_at'] = now_iso()
    obj.update(extra)
    atomic_write_json(path, obj)
    return obj


def inbox_path(inbox_id: str):
    return INBOX_ROOT / f'{inbox_id}.json'


def enqueue_inbox(message: dict):
    ensure_runtime_dirs()
    inbox_id = message['inbox_id']
    path = inbox_path(inbox_id)
    if path.exists():
        return load_json(path), False
    atomic_write_json(path, message)
    return message, True


def list_inbox(filter_fn=None):
    ensure_runtime_dirs()
    rows = []
    for path in sorted(INBOX_ROOT.glob('*.json')):
        obj = load_json(path, default={})
        obj['_path'] = str(path)
        if filter_fn and not filter_fn(obj):
            continue
        rows.append(obj)
    rows.sort(key=lambda x: x.get('received_at') or x.get('created_at', ''))
    return rows


def mark_inbox(inbox_id: str, updates=None):
    updates = updates or {}
    path = inbox_path(inbox_id)
    obj = load_json(path, default={})
    if not obj:
        return {}
    history_append = updates.pop('history_append', None)
    obj.update(updates)
    if history_append:
        obj.setdefault('history', []).append(history_append)
    atomic_write_json(path, obj)
    return obj


def active_path(key: str):
    safe = re.sub(r'[^a-zA-Z0-9_.-]+', '_', key)
    return ACTIVE_ROOT / f'{safe}.json'


def set_active_work_item(work_item_id: str, delivery: dict | None = None):
    ensure_runtime_dirs()
    payload = {
        'work_item_id': work_item_id,
        'updated_at': now_iso(),
    }
    atomic_write_json(active_path('global'), payload)
    if delivery:
        payload = {
            **payload,
            'delivery': delivery,
            'delivery_key': delivery_key(delivery),
        }
        atomic_write_json(active_path(delivery_key(delivery)), payload)


def get_active_work_item(delivery: dict | None = None):
    ensure_runtime_dirs()
    paths = []
    if delivery:
        paths.append(active_path(delivery_key(delivery)))
    paths.append(active_path('global'))
    for path in paths:
        obj = load_json(path, default={})
        if obj.get('work_item_id'):
            return obj['work_item_id']
    return None


def extract_work_item_id(text: str):
    if not text:
        return None
    match = WORK_ITEM_ID_RE.search(text)
    return match.group(1).lower() if match else None


def append_command_log(payload: dict):
    ensure_runtime_dirs()
    ts = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    cmd_id = f'cmd-{ts}'
    obj = {
        'command_id': cmd_id,
        'created_at': now_iso(),
        'status': 'received',
        **payload,
    }
    atomic_write_json(COMMAND_ROOT / f'{cmd_id}.json', obj)
    return obj


def complete_command_log(command_id: str, result: dict):
    path = COMMAND_ROOT / f'{command_id}.json'
    obj = load_json(path, default={})
    if not obj:
        return {}
    obj['status'] = 'processed'
    obj['processed_at'] = now_iso()
    obj['result'] = result
    atomic_write_json(path, obj)
    return obj
