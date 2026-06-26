#!/usr/bin/env python3
"""
Industrial-grade browser file upload script using agent-browser CLI.
"""

import subprocess
import sys
import os
from pathlib import Path


# ================================
# Config
# ================================
DEFAULT_WAIT = 2000
RETRY_COUNT = 2


# ================================
# Utility: Command Runner
# ================================
def run_cmd(cmd, retry=RETRY_COUNT, wait_ms=0):
    """
    Execute command with retry mechanism.
    """
    for i in range(retry):
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=15
            )

            if result.returncode == 0:
                return True, result.stdout

            print(f"[Retry {i+1}] Failed: {' '.join(cmd)}")
            print(result.stderr)

            if wait_ms > 0:
                subprocess.run(["agent-browser", "wait", str(wait_ms)])

        except Exception as e:
            print(f"[Exception] {e}")

    return False, ""


# ================================
# Path Resolver
# ================================
def resolve_path(file_path: str) -> str:
    expanded = os.path.expandvars(file_path)
    expanded = os.path.expanduser(expanded)

    if expanded.startswith("workspace/"):
        workspace = os.environ.get(
            "OPENCLAW_WORKSPACE",
            os.path.expanduser("~/.openclaw/workspace")
        )
        expanded = os.path.join(workspace, expanded[len("workspace/"):])

    return os.path.abspath(expanded)


# ================================
# Page Wait
# ================================
def wait_page(wait_ms):
    run_cmd(["agent-browser", "wait", str(wait_ms)])
    run_cmd(["agent-browser", "wait", "--load", "networkidle"])


# ================================
# Trigger File Input
# ================================
def trigger_file_input():
    print("Triggering file input...")

    strategies = [
        ["agent-browser", "find", "text", "选择文件", "click"],
        ["agent-browser", "find", "text", "上传", "click"],
        ["agent-browser", "find", "text", "Upload", "click"],
        ["agent-browser", "click", "[type=file]"],
    ]

    for cmd in strategies:
        ok, _ = run_cmd(cmd)
        if ok:
            print(f"Triggered by: {' '.join(cmd)}")
            return True

    print("Failed to trigger file input")
    run_cmd(["agent-browser", "snapshot"])
    return False


# ================================
# Upload with Fallback
# ================================
def upload_with_fallback(path, selector=None):
    print("Uploading file...")

    selectors = [
        selector,
        "#filePicker",
        "input[type=file]",
        "[type=file]",
    ]

    for sel in selectors:
        if not sel:
            continue

        print(f"Trying selector: {sel}")

        ok, _ = run_cmd(
            ["agent-browser", "upload", sel, path],
            retry=2,
            wait_ms=1000
        )

        if ok:
            print(f"Upload success with selector: {sel}")
            return True

    return False


# ================================
# Verify Upload
# ================================
def verify_upload():
    print("Verifying upload...")

    ok, output = run_cmd(["agent-browser", "snapshot"])

    if not ok:
        return False

    # 简单检测（可扩展）
    error_keywords = ["error", "failed", "上传失败"]

    for word in error_keywords:
        if word in output.lower():
            print("Detected error in page")
            return False

    return True


# ================================
# Main Upload Logic
# ================================
def upload_file(url, file_path, selector=None, wait_ms=DEFAULT_WAIT):
    path = resolve_path(file_path)

    if not os.path.exists(path):
        print(f"❌ File not found: {path}")
        return False

    print(f"Resolved path: {file_path} -> {path}")

    # Step 1: Open page
    print(f"Opening: {url}")
    ok, _ = run_cmd(["agent-browser", "open", url])
    if not ok:
        print("❌ Failed to open page")
        return False

    # Step 2: Wait
    wait_page(wait_ms)

    # Step 3: Trigger input
    if not selector:
        trigger_file_input()

    # Step 4: Upload
    if not upload_with_fallback(path, selector):
        print("❌ Upload failed after fallback")
        return False

    # Step 5: Verify
    if not verify_upload():
        print("⚠️ Verification failed, retrying once...")
        if not upload_with_fallback(path, selector):
            return False

    print("✅ Upload completed successfully")
    return True


# ================================
# Entry Point
# ================================
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python upload_file.py <url> <file_path> [selector] [wait_ms]")
        sys.exit(1)

    url = sys.argv[1]
    file_path = sys.argv[2]
    selector = sys.argv[3] if len(sys.argv) > 3 else None
    wait_ms = int(sys.argv[4]) if len(sys.argv) > 4 else DEFAULT_WAIT

    success = upload_file(url, file_path, selector, wait_ms)
    sys.exit(0 if success else 1)