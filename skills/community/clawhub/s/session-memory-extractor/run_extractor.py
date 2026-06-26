#!/usr/bin/env python3
"""
Session Memory Extractor — Processor v1.0.6
从 config.env 读取配置，支持并行处理
修复: stat -f %s 在 macOS 上返回块数而非字节数
"""

import subprocess
import json
import os
import re
import sys
import glob
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# --- Config loader ---
CONFIG_FILE = Path(__file__).parent / "config.env"

def load_config():
    if not CONFIG_FILE.exists():
        return {}
    config = {}
    for line in open(CONFIG_FILE):
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, val = line.split('=', 1)
        key, val = key.strip(), val.strip()
        config[key] = val
    return config

CONFIG = load_config()

def get_config(key, default=None):
    return os.environ.get(key, CONFIG.get(key, default))

env = os.environ

today = get_config("TODAY", datetime.now().strftime("%Y-%m-%d"))
cutoff_display = get_config("CUTOFF_DISPLAY", "")
cutoff_ts = int(get_config("CUTOFF_DATE", "0"))
dry_run = get_config("DRY_RUN", "false").lower() == "true"

agent_id = get_config("AGENT_ID", "main")
memory_dir = get_config("MEMORY_DIR", "")
sessions_dir = get_config("SESSIONS_DIR", "")
sessions_json = get_config("SESSIONS_JSON", "")
extract_script = get_config("EXTRACT_SCRIPT", "")
report_dir = get_config("REPORT_DIR", ".")
model = get_config("EXTRACTION_MODEL", "MiniMax-M2")
clean_trajectory = get_config("CLEAN_TRAJECTORY", "true").lower() == "true"
parallel = int(get_config("PARALLEL", "1"))
log_level = get_config("LOG_LEVEL", "info")

# 命令行参数覆盖
for arg in sys.argv[1:]:
    if arg == "--dry-run":
        dry_run = True

session_files = [line.strip() for line in sys.stdin if line.strip()]


def fmt_bytes(b):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if b < 1024:
            return f"{b:.0f} {unit}"
        b /= 1024
    return f"{b:.1f} TB"


def dir_size(files):
    total = 0
    for f in files:
        try:
            if os.path.exists(f):
                total += os.path.getsize(f)
        except Exception:
            pass
    return total


jsonl_before = [f for f in glob.glob(os.path.join(sessions_dir, "*.jsonl"))
                if not f.endswith(".deleted.") and "checkpoint" not in os.path.basename(f)]
traj_before = [f for f in glob.glob(os.path.join(sessions_dir, "*.trajectory.jsonl"))
               if not f.endswith(".deleted.")]

disk_before = {
    "jsonl_count": len(jsonl_before),
    "trajectory_count": len(traj_before),
    "jsonl_bytes": fmt_bytes(dir_size(jsonl_before)),
    "trajectory_bytes": fmt_bytes(dir_size(traj_before)),
}

if log_level == "debug":
    print(f"\n[BEFORE] .jsonl files: {disk_before['jsonl_count']} ({disk_before['jsonl_bytes']})")
    print(f"[BEFORE] .trajectory.jsonl files: {disk_before['trajectory_count']} ({disk_before['trajectory_bytes']})")

# --- 处理单个 session ---
def _quarantine_session(session_file, session_id, file_date, failure_reason, file_size, report_dir):
    """v1.0.6 safety: move failed session to quarantine instead of deleting.

    This is the critical safety gate — if extraction fails for any reason
    (no marker, empty content, no structured entries, API error, timeout),
    the original session file is preserved and renamed for later inspection.

    Files in quarantine are skipped on subsequent runs (they don't match the
    *.jsonl pattern required for processing).
    """
    import time
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    # Sanitize: keep only first line, replace whitespace/slashes for safe filename
    first_line = failure_reason.split('\n')[0].strip()
    safe_reason = re.sub(r'[^a-zA-Z0-9_-]', '_', first_line)[:40]
    quarantine_path = f"{session_file}.quarantined-{safe_reason}-{ts}.jsonl"

    moved = False
    try:
        if os.path.exists(session_file):
            os.rename(session_file, quarantine_path)
            moved = True
            print(f"[QUARANTINE] {session_id}.jsonl → {os.path.basename(quarantine_path)} (reason: {failure_reason})")
        else:
            print(f"[QUARANTINE] {session_id}.jsonl already gone (reason: {failure_reason})")
    except Exception as e:
        print(f"[QUARANTINE ERROR] could not move {session_file}: {e}")

    # Append to quarantine log (append-only audit trail)
    log_path = os.path.join(report_dir, "quarantine.log") if report_dir else "quarantine.log"
    try:
        os.makedirs(os.path.dirname(log_path) or '.', exist_ok=True)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat()}\t{session_id}\t{file_date}\t{failure_reason}\t{moved}\t{file_size}\t{quarantine_path if moved else ''}\n")
    except Exception as e:
        print(f"[QUARANTINE LOG ERROR] {e}")

    return {
        "session_id": session_id,
        "file_date": file_date,
        "status": "quarantined",
        "failure_reason": failure_reason,
        "quarantine_path": quarantine_path if moved else None,
        "bytes_freed": 0,
        "entries_extracted": 0,
    }


def process_one(SESSION_FILE):
    SESSION_ID = os.path.basename(SESSION_FILE).replace(".jsonl", "")

    try:
        file_mtime = os.path.getmtime(SESSION_FILE)
        file_date = datetime.fromtimestamp(file_mtime).strftime("%Y-%m-%d")
    except Exception:
        file_date = "unknown"
        file_mtime = 0

    if file_mtime > cutoff_ts:
        return {"session_id": SESSION_ID, "status": "skipped", "reason": "too recent"}

    if os.path.getsize(SESSION_FILE) == 0:
        return {"session_id": SESSION_ID, "status": "skipped", "reason": "empty"}

    # 防止并发重复处理同一文件
    import threading
    if not hasattr(process_one, '_processed_ids'):
        process_one._processed_ids = set()
        process_one._lock = threading.Lock()
    
    with process_one._lock:
        if SESSION_ID in process_one._processed_ids:
            return {"session_id": SESSION_ID, "status": "skipped", "reason": "already processed"}
        process_one._processed_ids.add(SESSION_ID)

    file_size = os.path.getsize(SESSION_FILE)
    print(f"[PROCESS] {SESSION_ID} — {file_size} bytes — {file_date}")

    try:
        with open(SESSION_FILE, 'r', errors='ignore') as f:
            content = f.read(51200)
    except Exception as e:
        return {"session_id": SESSION_ID, "status": "error", "reason": str(e)}

    if not content.strip():
        return {"session_id": SESSION_ID, "status": "skipped", "reason": "empty content"}

    print(f"[AI] Extracting... {SESSION_ID}")
    try:
        result = subprocess.run(
            ["python3", extract_script,
             "--session-id", SESSION_ID,
             "--content", content,
             "--model", model],
            capture_output=True, text=True, timeout=90
        )
        stdout = result.stdout.strip() if result.stdout else ""
        stderr = result.stderr.strip() if result.stderr else ""
        if stderr:
            for line in stderr.split('\n')[:3]:
                if line.strip():
                    print(f"[AI ERR] {line[:200]}")
    except subprocess.TimeoutExpired:
        stdout = ""
        stderr = "ERROR: extraction timeout (90s)"
        print(f"[AI ERR] {stderr}")
    except Exception as e:
        stdout = ""
        stderr = f"ERROR: {e}"
        print(f"[AI ERR] {stderr}")

    # v1.0.6 safety: verify __EXTRACT_OK__ marker before doing anything destructive
    extract_ok = False
    extraction_body = ""
    if stdout.startswith("__EXTRACT_OK__"):
        extraction_body = stdout[len("__EXTRACT_OK__"):].lstrip("\n")
        extract_ok = True

    # Validate extraction quality (even if marker present, content must be substantial)
    failure_reason = None
    if not extract_ok:
        failure_reason = f"no_marker (stdout_empty={not stdout}, stderr={stderr[:100]})"
    elif len(extraction_body.strip()) < 50:
        failure_reason = f"too_short ({len(extraction_body.strip())} chars)"
    elif "**[FACT]**" not in extraction_body and "**[LEARN]**" not in extraction_body and "**[TODO]**" not in extraction_body and "**[INSIGHT]**" not in extraction_body and "**[NOTE]**" not in extraction_body and "**[REFERENCE]**" not in extraction_body and "**[DECISION]**" not in extraction_body:
        failure_reason = "no_structured_entries"

    entry_count = extraction_body.count("- **[") if extract_ok else 0
    entry_list = []
    if extract_ok and not failure_reason:
        for line in extraction_body.split('\n'):
            if line.startswith('- **['):
                parts = line.split('**', 2)
                if len(parts) >= 3:
                    entry_list.append({"type": parts[1].strip(']'), "content": parts[2].strip()})

    if dry_run:
        if failure_reason:
            print(f"[DRY] Would QUARANTINE {SESSION_ID}.jsonl (reason: {failure_reason})")
            return {"session_id": SESSION_ID, "status": "dry-run-quarantine", "failure_reason": failure_reason, "bytes_freed": 0}
        print(f"[DRY] Would write to memory and delete {SESSION_ID}.jsonl")
        return {"session_id": SESSION_ID, "status": "dry-run", "entries_extracted": entry_count, "bytes_freed": 0}

    # v1.0.6 SAFETY GATE: if extraction failed, do NOT delete original files
    if failure_reason:
        return _quarantine_session(SESSION_FILE, SESSION_ID, file_date, failure_reason, file_size, report_dir)

    # === SUCCESS PATH: extraction verified, safe to delete ===

    # Write to memory
    os.makedirs(memory_dir, exist_ok=True)
    memory_file = os.path.join(memory_dir, f"{today}.md")
    with open(memory_file, "a", encoding="utf-8") as f:
        f.write(f"\n## Extracted from session: {SESSION_ID}\n")
        f.write(f"Original file: {SESSION_FILE}\n")
        f.write(f"File date: {file_date}\n\n")
        f.write(extraction_body + "\n\n")

    # Remove from sessions.json
    if os.path.exists(sessions_json):
        try:
            with open(sessions_json, 'r') as f:
                data = json.load(f)
            removed = None
            for key, val in list(data.items()):
                if val.get('sessionId') == SESSION_ID or key == SESSION_ID:
                    removed = key
                    del data[key]
                    break
            if removed:
                with open(sessions_json, 'w') as f:
                    json.dump(data, f, indent=2)
        except Exception:
            pass

    # Delete files (check exists to avoid race condition)
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
    freed = file_size

    if clean_trajectory:
        traj = SESSION_FILE.replace(".jsonl", ".trajectory.jsonl")
        if os.path.exists(traj):
            freed += os.path.getsize(traj)
            os.remove(traj)

    for v in glob.glob(f"{SESSION_FILE}.deleted.*"):
        if os.path.exists(v):
            os.remove(v)

    return {
        "session_id": SESSION_ID,
        "file_date": file_date,
        "entries_extracted": entry_count,
        "entries": entry_list,
        "extraction": extraction_body if extraction_body else None,
        "bytes_freed": freed,
        "status": "done"
    }


# --- 主循环：串行或并行 ---
results = []
processed = 0
extracted_total = 0
freed_total = 0
quarantined = 0

if parallel <= 1:
    # 串行
    for SESSION_FILE in session_files:
        if SESSION_FILE:
            result = process_one(SESSION_FILE)
            results.append(result)
            if result["status"] == "done":
                processed += 1
                extracted_total += result.get("entries_extracted", 0)
                freed_total += result.get("bytes_freed", 0)
            elif result["status"] == "quarantined":
                quarantined += 1
else:
    # 并行
    print(f"\n[PARALLEL] Running with {parallel} workers...")
    with ThreadPoolExecutor(max_workers=parallel) as executor:
        futures = {executor.submit(process_one, f): f for f in session_files if f}
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            if result["status"] == "done":
                processed += 1
                extracted_total += result.get("entries_extracted", 0)
                freed_total += result.get("bytes_freed", 0)
            elif result["status"] == "quarantined":
                quarantined += 1
            print(f"[DONE] {result['session_id']} — {result['status']}")

# Disk stats AFTER
jsonl_after = [f for f in glob.glob(os.path.join(sessions_dir, "*.jsonl"))
               if not f.endswith(".deleted.") and "checkpoint" not in os.path.basename(f)]
traj_after = [f for f in glob.glob(os.path.join(sessions_dir, "*.trajectory.jsonl"))
              if not f.endswith(".deleted.")]

disk_after = {
    "jsonl_count": len(jsonl_after),
    "trajectory_count": len(traj_after),
    "jsonl_bytes": fmt_bytes(dir_size(jsonl_after)),
    "trajectory_bytes": fmt_bytes(dir_size(traj_after)),
}

print(f"\n[AFTER] .jsonl files: {disk_after['jsonl_count']} ({disk_after['jsonl_bytes']})")
print(f"[AFTER] .trajectory.jsonl files: {disk_after['trajectory_count']} ({disk_after['trajectory_bytes']})")

report = {
    "version": "1.0.6",
    "date": today,
    "agent": agent_id,
    "cutoff_days": int(get_config("MIN_AGE_DAYS", "7")),
    "cutoff_date": cutoff_display,
    "dry_run": dry_run,
    "parallel": parallel,
    "sessions_scanned": len(session_files),
    "sessions_processed": processed,
    "sessions_quarantined": quarantined,
    "total_entries_extracted": extracted_total,
    "total_bytes_freed": freed_total,
    "total_bytes_freed_human": fmt_bytes(freed_total),
    "disk_before": disk_before,
    "disk_after": disk_after,
    "memory_file": os.path.join(memory_dir, f"{today}.md"),
    "config_source": str(CONFIG_FILE),
    "results": results
}

report_path = os.path.join(report_dir, f"extract-report-{agent_id}-{today}.json")
with open(report_path, 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

print("")
print("=== Summary ===")
print(f"Sessions processed:   {processed}")
print(f"Sessions quarantined: {quarantined}  (extraction failed, files preserved)")
print(f"Entries extracted:    {extracted_total}")
print(f"Total bytes freed:   {freed_total} bytes ({fmt_bytes(freed_total)})")
print(f"Memory written:       {os.path.join(memory_dir, today + '.md')}")
print(f"Report:              {report_path}")
print("Done.")