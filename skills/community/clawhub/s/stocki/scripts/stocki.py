#!/usr/bin/env python3
"""Stocki CLI — AI Financial Analyst"""

import argparse
import hashlib
import os
import re
import subprocess
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gateway import (
    format_for_wechat,
    gateway_request,
    gateway_request_raw,
)


# --- instant ---

def cmd_instant(args):
    result = gateway_request(
        "POST", "/v1/instant",
        {"question": args.question, "timezone": args.timezone},
        timeout=180,
    )
    answer = result.get("answer", "")
    if not answer:
        print("No answer returned.", file=sys.stderr)
        sys.exit(1)
    print(format_for_wechat(answer))


# --- quant ---

def cmd_quant(args):
    body = {"question": args.question, "timezone": args.timezone}
    if args.task_id:
        body["task_id"] = args.task_id
    result = gateway_request("POST", "/v1/quant", body, timeout=30)
    print(f"task_id: {result.get('task_id', '')}")
    print(f"task_name: {result.get('task_name', '')}")


# --- tasks ---

def cmd_tasks(_args):
    result = gateway_request("GET", "/v1/tasks", timeout=30)
    tasks = result.get("tasks", [])
    if not tasks:
        print("No tasks found.")
        return
    print(f"{'Name':<40} {'Task ID':<16} {'Updated':<24} {'Msgs':>4}")
    print("-" * 88)
    for t in tasks:
        name = t.get("name", "")[:38]
        tid = t.get("task_id", "")
        updated = t.get("updated_at", "")[:19]
        msgs = t.get("message_count", 0)
        print(f"{name:<40} {tid:<16} {updated:<24} {msgs:>4}")


# --- status ---

def cmd_status(args):
    result = gateway_request("GET", f"/v1/tasks/{args.task_id}", timeout=120)
    name = result.get("name", "")
    print(f"Task: {name} ({args.task_id})")

    current = result.get("current_run")
    if current:
        print(f"\nCurrent run: {current.get('run_id', '')} [{current.get('status', '')}]")
        print(f"  Query: {current.get('query', '')}")

    runs = result.get("runs", [])
    if runs:
        print(f"\nRuns ({len(runs)}):")
        for r in runs:
            status = r.get("status", "")
            rid = r.get("run_id", "")
            query = r.get("query", "")[:60]
            summary = r.get("summary") or ""
            err = r.get("error_message") or ""
            print(f"  [{status}] {rid}: {query}")
            if summary:
                print(f"    Summary: {summary[:120]}")
            if err:
                print(f"    Error: {err}")
            files = r.get("files", [])
            if files:
                print(f"    Files: {', '.join(files)}")


# --- files ---

def cmd_files(args):
    result = gateway_request("GET", f"/v1/tasks/{args.task_id}", timeout=120)
    runs = result.get("runs", [])
    if not runs:
        print("No runs found.")
        return
    for r in runs:
        rid = r.get("run_id", "")
        status = r.get("status", "")
        files = r.get("files", [])
        if files:
            print(f"[{status}] {rid}:")
            for f in files:
                print(f"  {f}")
        else:
            print(f"[{status}] {rid}: (no files)")


# --- download ---

def cmd_download(args):
    raw, content_type = gateway_request_raw(
        "GET",
        f"/v1/tasks/{args.task_id}/files/{args.file_path}",
        timeout=300,
    )
    output = args.output or os.path.basename(args.file_path)
    # Sanitize output path to prevent writing outside current directory
    if os.path.isabs(output) or ".." in output:
        output = os.path.basename(output)
    mode = "wb" if "image" in content_type else "w"
    with open(output, mode) as f:
        if mode == "wb":
            f.write(raw)
        else:
            f.write(raw.decode("utf-8"))
    print(f"Saved: {output} ({len(raw)} bytes)")


# --- diagnose ---

def cmd_diagnose(_args):
    print("Stocki Self-Diagnostic")
    print("=" * 40)

    passed = 0
    total = 1

    if _check_instant():
        passed += 1

    print("=" * 40)
    print(f"Result: {passed}/{total} passed")
    sys.exit(0 if passed == total else 1)


def _check_instant():
    print("[1/1] Instant mode...", end=" ", flush=True)
    try:
        result = gateway_request(
            "POST", "/v1/instant",
            {"question": "What is the ticker symbol of Apple Inc on NASDAQ?", "timezone": "Asia/Shanghai"},
            timeout=180,
        )
        answer = result.get("answer", "")
        if not answer:
            print("FAIL (empty answer)")
            return False
        if "AAPL" in answer.upper():
            print(f"OK (verified AAPL, {len(answer)} chars)")
            return True
        else:
            print("FAIL (answer does not contain 'AAPL')")
            print(f"  Answer: {answer[:200]}...")
            return False
    except SystemExit:
        print("FAIL")
        return False


# --- doctor ---

GITHUB_SKILL_URL = "https://raw.githubusercontent.com/stocki-ai/open-stocki/main/SKILL.md"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)


def _get_local_version():
    """Read version from local SKILL.md frontmatter."""
    skill_md = os.path.join(SKILL_DIR, "SKILL.md")
    if not os.path.isfile(skill_md):
        return None
    with open(skill_md, "r") as f:
        for line in f:
            if line.startswith("version:"):
                return line.split(":", 1)[1].strip().strip('"').strip("'")
    return None


def _get_remote_version():
    """Fetch latest version from GitHub."""
    try:
        req = Request(GITHUB_SKILL_URL, method="GET")
        with urlopen(req, timeout=15) as resp:
            for line in resp.read().decode().splitlines():
                if line.startswith("version:"):
                    return line.split(":", 1)[1].strip().strip('"').strip("'")
    except Exception:
        return None
    return None


def _sha256(filepath):
    """Compute SHA256 of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _reinstall_skill():
    """Try to reinstall skill via clawhub, then GitHub."""
    print("      Reinstalling skill...")
    try:
        r = subprocess.run(["clawhub", "install", "stocki", "--force"],
                           capture_output=True, text=True, timeout=30)
        if r.returncode == 0:
            print("      -> Reinstalled via clawhub")
            return True
    except Exception:
        pass
    # Validate SKILL_DIR before rm -rf
    if "stocki" not in os.path.basename(SKILL_DIR):
        print("      -> Reinstall aborted: unexpected skill directory path")
        return False
    try:
        subprocess.run(["rm", "-rf", SKILL_DIR], check=True)
        r = subprocess.run(
            ["git", "-c", "http.postBuffer=524288000", "-c", "http.lowSpeedLimit=0",
             "-c", "http.lowSpeedTime=300", "clone",
             "https://github.com/stocki-ai/open-stocki.git", SKILL_DIR],
            capture_output=True, text=True, timeout=120)
        if r.returncode == 0:
            print("      -> Reinstalled from GitHub")
            return True
    except Exception:
        pass
    print("      -> Reinstall failed. See INSTALL.md for manual instructions.")
    return False


def cmd_doctor(_args):
    print("Stocki Doctor")
    print("=" * 48)

    ok = 0
    fixed = 0
    failed = 0
    total = 6

    # 1. API Key
    api_key = os.environ.get("STOCKI_API_KEY", "")
    if not api_key:
        print("[1/6] API Key.............. FAIL")
        print("      No API key set. Register at:")
        print("      https://api.stocki.com.cn/wechat")
        print('      Then: export STOCKI_API_KEY="sk_your_key_here"')
        failed += 1
    elif not api_key.startswith("sk_"):
        print(f"[1/6] API Key.............. WARN (invalid format: {api_key[:10]}...)")
        print("      API key should start with 'sk_'")
        failed += 1
    else:
        masked = api_key[:3] + "..." + api_key[-2:]
        print(f"[1/6] API Key.............. OK ({masked})")
        ok += 1

    # 2. Gateway URL
    gw_url = os.environ.get("STOCKI_GATEWAY_URL", "")
    if not gw_url:
        print("[2/6] Gateway URL.......... FAIL")
        print('      export STOCKI_GATEWAY_URL="https://api.stocki.com.cn"')
        failed += 1
    else:
        print(f"[2/6] Gateway URL.......... OK ({gw_url})")
        ok += 1

    # 3. API Connectivity
    if api_key and gw_url:
        try:
            result = gateway_request(
                "POST", "/v1/instant",
                {"question": "ping", "timezone": "Asia/Shanghai"},
                timeout=30,
            )
            if result.get("answer"):
                print("[3/6] API Connectivity..... OK")
                ok += 1
            else:
                print("[3/6] API Connectivity..... WARN (empty response)")
                ok += 1
        except SystemExit:
            print("[3/6] API Connectivity..... FAIL (see error above)")
            failed += 1
    else:
        print("[3/6] API Connectivity..... SKIP (no credentials)")
        failed += 1

    # 4. Skill Version
    local_ver = _get_local_version()
    remote_ver = _get_remote_version()
    if not local_ver:
        print("[4/6] Skill Version........ FAIL (cannot read local version)")
        failed += 1
    elif not remote_ver:
        print(f"[4/6] Skill Version........ WARN (v{local_ver}, cannot check remote)")
        ok += 1
    elif local_ver == remote_ver:
        print(f"[4/6] Skill Version........ OK (v{local_ver}, up to date)")
        ok += 1
    else:
        print(f"[4/6] Skill Version........ WARN (v{local_ver} -> v{remote_ver} available)")
        if _reinstall_skill():
            fixed += 1
        else:
            failed += 1

    # 5. File Integrity
    checksum_file = os.path.join(SCRIPT_DIR, "checksums.sha256")
    if not os.path.isfile(checksum_file):
        print("[5/6] File Integrity....... WARN (no checksums file)")
        ok += 1
    else:
        integrity_ok = True
        with open(checksum_file) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) != 2:
                    continue
                expected_hash, filename = parts
                filepath = os.path.join(SCRIPT_DIR, filename)
                if not os.path.isfile(filepath):
                    print(f"[5/6] File Integrity....... FAIL ({filename} missing)")
                    integrity_ok = False
                    break
                actual_hash = _sha256(filepath)
                if actual_hash != expected_hash:
                    print(f"[5/6] File Integrity....... FAIL ({filename} modified)")
                    integrity_ok = False
                    break
        if integrity_ok:
            print("[5/6] File Integrity....... OK")
            ok += 1
        else:
            print("      Files have been modified or corrupted.")
            if _reinstall_skill():
                fixed += 1
            else:
                failed += 1

    # 6. Workspace
    home = os.path.expanduser("~")
    workspace = os.path.join(home, "stocki")
    quant_dir = os.path.join(workspace, "quant")
    profile = os.path.join(workspace, "profile.md")
    dirs_ok = os.path.isdir(workspace) and os.path.isdir(quant_dir)
    if dirs_ok:
        print("[6/6] Workspace............ OK")
        ok += 1
    else:
        print("[6/6] Workspace............ WARN (missing directories)")
        os.makedirs(quant_dir, exist_ok=True)
        if not os.path.isfile(profile):
            open(profile, "a").close()
        print("      -> Created ~/stocki/quant/ and ~/stocki/profile.md")
        fixed += 1

    # Summary
    print("=" * 48)
    print(f"Result: {ok} OK, {fixed} fixed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)


# --- main ---

def main():
    parser = argparse.ArgumentParser(prog="stocki", description="Stocki — AI Financial Analyst CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("instant", help="Quick financial Q&A")
    p.add_argument("question", help="The question to ask")
    p.add_argument("--timezone", default="Asia/Shanghai", help="IANA timezone (default: Asia/Shanghai)")

    p = sub.add_parser("quant", help="Submit quantitative analysis")
    p.add_argument("question", help="Analysis question")
    p.add_argument("--task-id", default=None, help="Existing task ID for iteration")
    p.add_argument("--timezone", default="Asia/Shanghai", help="IANA timezone (default: Asia/Shanghai)")

    sub.add_parser("list", help="List all quant analyses")

    p = sub.add_parser("status", help="Show task details and run statuses")
    p.add_argument("task_id", help="Task ID")

    p = sub.add_parser("files", help="List result files for a task")
    p.add_argument("task_id", help="Task ID")

    p = sub.add_parser("download", help="Download a result file")
    p.add_argument("task_id", help="Task ID")
    p.add_argument("file_path", help="File path (e.g. runs/run_001/report.md)")
    p.add_argument("--output", help="Local output path (default: basename)")

    sub.add_parser("diagnose", help="Self-diagnostic: verify instant mode")

    sub.add_parser("doctor", help="Check and fix setup issues")

    args = parser.parse_args()
    {
        "instant": cmd_instant,
        "quant": cmd_quant,
        "list": cmd_tasks,
        "status": cmd_status,
        "files": cmd_files,
        "download": cmd_download,
        "diagnose": cmd_diagnose,
        "doctor": cmd_doctor,
    }[args.command](args)


if __name__ == "__main__":
    main()
