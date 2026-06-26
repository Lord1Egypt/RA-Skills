#!/usr/bin/env python3
"""
scan_sessions.py - Scan recent OpenClaw sessions to auto-detect skill invocations

Detection patterns:
  - Skill directory paths in exec commands: /skills/<name>/
  - Known skill script names: meeting.sh, ai_news_cron_wrapper.sh, etc.
  - Skill name references in message content

Path resolution: uses path_utils (dynamic — works regardless of install location)
"""

import json
import subprocess
import re
import sys
import os
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from path_utils import get_usage_file, get_registry_file, get_data_dir
import i18n

GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
CYAN = '\033[0;36m'
NC = '\033[0m'

SKIP_SKILLS = {'skill-insight'}

def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_gateway_port():
    """Get gateway HTTP port from openclaw config."""
    config_path = Path.home() / ".openclaw" / "openclaw.json"
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        gw = config.get('gateway', {})
        return gw.get('port') or gw.get('httpPort') or 18789
    except:
        return 18789

def gateway_request(path: str, method="GET", data=None, timeout=10):
    """Make a direct request to the local gateway API."""
    port = get_gateway_port()
    url = f"http://localhost:{port}{path}"
    try:
        req = urllib.request.Request(url, method=method)
        req.add_header('Content-Type', 'application/json')
        if data:
            req.data = json.dumps(data).encode()
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode()), resp.status
    except Exception as e:
        return {"error": str(e)}, -1

def get_recent_sessions(limit=20):
    """Fetch recent sessions via gateway API or CLI."""
    body, status = gateway_request("/sessions/list", timeout=8)
    if status == 200 and isinstance(body, list):
        sessions = [(s.get('sessionKey', ''), s.get('updatedAt', ''))
                     for s in body[:limit] if s.get('sessionKey')]
        if sessions:
            return sessions

    try:
        result = subprocess.run(
            ["timeout", "5", "openclaw", "sessions", "--json", "--active", "1440"],
            capture_output=True, text=True, timeout=8
        )
        if result.returncode == 0 and result.stdout.strip():
            sessions = json.loads(result.stdout)
            if isinstance(sessions, list):
                return [(s.get('sessionKey', ''), s.get('updatedAt', ''))
                        for s in sessions[:limit] if s.get('sessionKey')]
    except Exception:
        pass
    return []

def get_session_messages(session_key: str, limit=30):
    """Fetch messages for a session."""
    body, status = gateway_request(
        f"/sessions/{session_key}/messages?limit={limit}", timeout=8
    )
    if status == 200 and isinstance(body, list):
        return body

    try:
        result = subprocess.run(
            ["timeout", "8", "openclaw", "sessions", "history", session_key,
             "--limit", str(limit), "--json"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout)
    except Exception:
        pass
    return []

def extract_skills_from_content(content: str, valid_skills: set) -> list:
    """Extract skill invocations from message/exec content.

    Detection patterns (generic — no hardcoded skill names):
      1. Skill directory paths: /skills/<name>/
      2. Skill name word-boundary mentions (from registry)
    """
    found = []
    content_lower = content.lower()

    # 1. Skill directory paths: /skills/<name>/
    for match in re.finditer(r'/skills/([a-z0-9_-]+)/', content, re.IGNORECASE):
        skill = match.group(1).lower()
        if skill not in SKIP_SKILLS and skill in valid_skills:
            found.append(skill)

    for skill in valid_skills:
        if skill in SKIP_SKILLS:
            continue
        pattern = rf'\b{re.escape(skill)}\b'
        if re.search(pattern, content_lower):
            found.append(skill)

    seen = set()
    result = []
    for s in found:
        if s not in seen:
            seen.add(s)
            result.append(s)
    return result

def scan_all_sessions(session_limit=15, messages_limit=30, valid_skills=None) -> dict:
    """Scan recent sessions for skill invocations."""
    if valid_skills is None:
        valid_skills = set()
    detections = {}
    sessions = get_recent_sessions(limit=session_limit)
    if not sessions:
        print(f"{YELLOW}[scan] No recent sessions found (gateway may be inaccessible){NC}")
        return detections

    print(f"{CYAN}[scan] Scanning {len(sessions)} sessions...{NC}")

    for session_key, updated_at in sessions:
        if not session_key or 'subagent' in session_key.lower():
            continue

        messages = get_session_messages(session_key, limit=messages_limit)
        full_text = ""

        if isinstance(messages, list):
            for msg in messages:
                if isinstance(msg, dict):
                    full_text += msg.get('content', '') + ' '
                    full_text += msg.get('text', '') + ' '
                    if 'toolCalls' in msg:
                        for tc in msg['toolCalls']:
                            full_text += json.dumps(tc) + ' '

        if not full_text.strip():
            continue

        found = extract_skills_from_content(full_text, valid_skills)
        for skill in found:
            if skill not in detections:
                detections[skill] = []
            ts = updated_at or datetime.now(timezone(timedelta(hours=8))).isoformat()
            detections[skill].append((ts, f"auto-scan:{session_key[:40]}", session_key))

    return detections

def update_usage(detections: dict):
    """Merge detections into usage.json, avoiding duplicates."""
    usage_file = get_usage_file()
    usage_data = load_json(usage_file) or {"schema": "skill_usage_log:v1", "last_updated": "", "records": []}

    added = 0
    now = datetime.now(timezone(timedelta(hours=8)))
    now_str = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")

    for skill, occurrences in detections.items():
        for ts, scene, session_key in occurrences:
            is_new = True
            for r in usage_data["records"]:
                if (r["skill"] == skill and "auto-scan" in r.get("scene", "")
                        and session_key[:30] in r.get("notes", "")):
                    is_new = False
                    break
            if is_new:
                entry = {
                    "id": f"auto-{int(now.timestamp())}-{skill[:8]}",
                    "skill": skill,
                    "timestamp": now_str,
                    "scene": f"[auto] {scene}",
                    "outcome": "auto-detected",
                    "notes": f"session={session_key[:50]}"
                }
                usage_data["records"].append(entry)
                added += 1

    if added > 0:
        usage_data["last_updated"] = now_str
        save_json(usage_file, usage_data)
        print(f"{GREEN}[scan] Added {added} auto-detected invocations{NC}")
    else:
        print(f"{YELLOW}[scan] No new invocations (already recorded){NC}")

    return added

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--lang', default=None, choices=['en', 'zh'])
    args = parser.parse_args()
    lang = args.lang or i18n.detect_lang()

    title = {"en": "Skill Session Scanner", "zh": "技能会话扫描器"}.get(lang, "Skill Session Scanner")
    data_label = {"en": "Data:", "zh": "数据:"}.get(lang, "Data:")
    error_label = {"en": "Error:", "zh": "错误:"}.get(lang, "Error:")
    not_found_hint = {"en": "Run add_skill.py first to initialize.", "zh": "请先运行 add_skill.py 初始化注册表。"}.get(lang, "")

    print(f"\n{'='*60}")
    print(f"  🔍 {title}")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  {data_label} {get_usage_file()}")
    print(f"{'='*60}")

    registry_file = get_registry_file()
    registry_data = load_json(registry_file)
    if not registry_data:
        print(f"{RED}[scan] Error: registry not found at {registry_file}{NC}")
        print(f"{RED}Run add_skill.py first to initialize.{NC}")
        sys.exit(1)

    valid_skills = {s["name"] for s in registry_data["skills"] if s.get("installed", True)}
    print(f"{CYAN}[scan] {len(valid_skills)} installed skills in registry{NC}")

    detections = scan_all_sessions(session_limit=15, messages_limit=30, valid_skills=valid_skills)

    if not detections:
        print(f"{YELLOW}[scan] No skill invocations detected in recent sessions{NC}")
        body, status = gateway_request("/health", timeout=5)
        if status != 200:
            print(f"{RED}[scan] Gateway health check failed (status={status}){NC}")
        print(f"\n{'='*60}")
        return

    valid_detections = {s: o for s, o in detections.items() if s in valid_skills}

    if valid_detections:
        update_usage(valid_detections)
        print(f"\n{CYAN}[scan] Summary:{NC}")
        for skill, occs in valid_detections.items():
            print(f"  • {skill}: {len(occs)} occurrence(s)")
    else:
        print(f"{YELLOW}[scan] Detected skills not found in registry (normal for cross-references){NC}")

    print(f"\n{'='*60}")

if __name__ == "__main__":
    main()
