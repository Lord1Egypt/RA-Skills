#!/usr/bin/env python3
"""
Shared utilities for system-controller scripts.
Handles Windows encoding issues and PowerShell execution.
"""

import subprocess
import sys
import os


def run_ps(script, timeout=30):
    """
    Execute PowerShell script with proper encoding handling.
    Returns (stdout: str, stderr: str, returncode: int)
    """
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    
    # Prepend encoding setup to ensure UTF-8 output
    encoding_setup = (
        "[Console]::InputEncoding = [Console]::OutputEncoding = "
        "[System.Text.Encoding]::UTF8; "
        "$OutputEncoding = [System.Text.Encoding]::UTF8; "
    )
    
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command",
             encoding_setup + script],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            env=env
        )
        stdout = (result.stdout or "").strip()
        stderr = (result.stderr or "").strip()
        return stdout, stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "ERROR: Command timed out", -1
    except Exception as e:
        return "", f"ERROR: {e}", -1


def run_cmd(command, timeout=30):
    """
    Execute a shell command with proper encoding.
    Returns (stdout: str, stderr: str, returncode: int)
    """
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            shell=True,
            env=env
        )
        stdout = (result.stdout or "").strip()
        stderr = (result.stderr or "").strip()
        return stdout, stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "ERROR: Command timed out", -1
    except Exception as e:
        return "", f"ERROR: {e}", -1


def json_safe(obj):
    """Ensure output is serializable, replacing None with null."""
    if obj is None:
        return "null"
    return obj
