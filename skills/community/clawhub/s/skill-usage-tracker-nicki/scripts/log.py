#!/usr/bin/env python3
"""记录技能调用"""
import json, sys, os
from datetime import datetime, timezone

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'usage.json')

def load_records():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE) as f:
        return json.load(f).get('records', [])

def save_records(records):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump({'records': records}, f, ensure_ascii=False, indent=2)

def log_skill(skill_name: str, note: str = ''):
    records = load_records()
    records.append({
        'skill': skill_name,
        'called_at': datetime.now(timezone.utc).isoformat(),
        'note': note
    })
    save_records(records)
    return f"已记录: {skill_name}"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: log.py <技能名> [备注]")
        sys.exit(1)
    skill = sys.argv[1]
    note = sys.argv[2] if len(sys.argv) > 2 else ''
    print(log_skill(skill, note))
