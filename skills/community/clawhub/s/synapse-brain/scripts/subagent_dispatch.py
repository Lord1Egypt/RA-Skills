#!/usr/bin/env python3
"""
Synapse Brain — Subagent Dispatch (v2.0.1)
子代理并行调度管理器，支持自动重试。

Usage:
    python subagent_dispatch.py dispatch <project> <task_id> --mode parallel --agents 3
    python subagent_dispatch.py report <project>
    python subagent_dispatch.py retry <project> <subagent_id>
"""

import json
import os
import sys
import time
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(__file__))
from state_manager import _load, _save

MAX_ATTEMPTS = 3
RETRY_BASE_DELAY = 5  # seconds


def dispatch(project: str, task_id: str, mode: str = "sequential", agents: int = 1):
    """Dispatch subagents for a task."""
    state = _load(project)
    if not state:
        print(f"[brain] No session for '{project}'. Initialize first.")
        return

    # Validate agent count (OpenClaw max: 8)
    max_agents = 8
    agents = min(agents, max_agents)

    # Create subagent records
    subagents = []
    for i in range(agents):
        subagents.append({
            "id": f"sub-{task_id}-{i+1}",
            "task_id": task_id,
            "status": "pending",
            "attempts": 0,
            "max_attempts": MAX_ATTEMPTS,
            "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        })

    if "subagents_list" not in state:
        state["subagents_list"] = []
    state["subagents_list"].extend(subagents)

    # Update state
    state["subagents"]["active"] += agents
    state["log"].append(
        f"[{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}] "
        f"Dispatched {agents} subagents for {task_id} (mode={mode})"
    )

    _save(project, state)

    print(f"[brain] Dispatched {agents} subagent(s) for task '{task_id}'")
    print(f"  Mode: {mode}")
    print(f"  Active: {state['subagents']['active']}")

    return subagents


def complete(project: str, subagent_id: str, success: bool = True, result: str = None):
    """Mark a subagent as completed or trigger retry on failure."""
    state = _load(project)
    if not state:
        return

    # Find the subagent
    subagent = None
    for sa in state.get("subagents_list", []):
        if sa["id"] == subagent_id:
            subagent = sa
            break

    if not subagent:
        print(f"[brain] Subagent '{subagent_id}' not found")
        return

    if success:
        subagent["status"] = "completed"
        subagent["completed_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        subagent["attempts"] = max(subagent.get("attempts", 0) + 1, 1)
        state["subagents"]["completed"] += 1
        state["subagents"]["active"] = max(0, state["subagents"]["active"] - 1)
        state["log"].append(
            f"[{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}] "
            f"Subagent {subagent_id} -> completed"
        )
        _save(project, state)
        print(f"[brain] Subagent {subagent_id} completed")
    else:
        attempts = subagent.get("attempts", 0) + 1  # count this attempt
        max_attempts = subagent.get("max_attempts", MAX_ATTEMPTS)
        subagent["attempts"] = attempts

        if attempts < max_attempts:
            # Retry with exponential backoff
            delay = RETRY_BASE_DELAY * (2 ** (attempts - 1))
            subagent["status"] = "retrying"
            subagent["last_failure"] = result or "Unknown error"
            subagent["last_failure_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            subagent["next_retry_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            state["log"].append(
                f"[{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}] "
                f"Subagent {subagent_id} failed (attempt {attempts}/{max_attempts}), "
                f"retrying in {delay}s: {result or 'Unknown'}"
            )
            _save(project, state)
            print(f"[brain] Subagent {subagent_id} failed, retry {attempts}/{max_attempts} in {delay}s")
            return {"retrying": True, "attempt": attempts, "delay": delay}
        else:
            # Max attempts exceeded
            subagent["status"] = "failed"
            subagent["final_error"] = result or "Unknown error"
            subagent["failed_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            state["subagents"]["failed"] += 1
            state["subagents"]["active"] = max(0, state["subagents"]["active"] - 1)
            state["log"].append(
                f"[{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}] "
                f"Subagent {subagent_id} -> failed (max attempts exceeded): {result or 'Unknown'}"
            )
            _save(project, state)
            print(f"[brain] Subagent {subagent_id} failed after {max_attempts} attempts")
            return {"retrying": False, "attempts": max_attempts}


def retry_subagent(project: str, subagent_id: str):
    """Manually retry a failed subagent."""
    state = _load(project)
    if not state:
        return

    subagent = None
    for sa in state.get("subagents_list", []):
        if sa["id"] == subagent_id:
            subagent = sa
            break

    if not subagent:
        print(f"[brain] Subagent '{subagent_id}' not found")
        return

    if subagent["status"] not in ("failed", "completed"):
        print(f"[brain] Subagent '{subagent_id}' is {subagent['status']}, not retryable")
        return

    subagent["status"] = "pending"
    subagent["attempts"] = 0
    subagent.pop("final_error", None)
    subagent.pop("last_failure", None)
    state["subagents"]["active"] += 1
    state["subagents"]["failed"] = max(0, state["subagents"]["failed"] - 1)
    state["log"].append(
        f"[{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}] "
        f"Subagent {subagent_id} manually retried"
    )
    _save(project, state)
    print(f"[brain] Subagent {subagent_id} reset for retry")


def report(project: str):
    """Generate subagent execution report."""
    state = _load(project)
    if not state:
        return

    sa = state["subagents"]
    subagents_list = state.get("subagents_list", [])
    total = len(subagents_list)

    print(f"\n Subagent Report: {project}")
    print(f"  Active:    {sa['active']}")
    print(f"  Completed: {sa['completed']}")
    print(f"  Failed:    {sa['failed']}")
    print(f"  Total:     {total}")

    # Show retry details for failed subagents
    failed = [s for s in subagents_list if s["status"] == "failed"]
    if failed:
        print(f"\n  Failed subagents (max retries exceeded):")
        for s in failed:
            error = s.get("final_error", s.get("last_failure", "Unknown"))
            print(f"    - {s['id']}: {error}")
    print()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "dispatch":
        if len(sys.argv) < 4:
            print("Usage: subagent_dispatch.py dispatch <project> <task_id> [--mode MODE] [--agents N]")
            sys.exit(1)
        mode = "sequential"
        agents = 1
        i = 4
        while i < len(sys.argv):
            if sys.argv[i] == "--mode" and i + 1 < len(sys.argv):
                mode = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--agents" and i + 1 < len(sys.argv):
                agents = int(sys.argv[i + 1])
                i += 2
            else:
                i += 1
        dispatch(sys.argv[2], sys.argv[3], mode, agents)
    elif cmd == "complete":
        if len(sys.argv) < 4:
            print("Usage: subagent_dispatch.py complete <project> <subagent_id> [--success BOOL] [--result MSG]")
            sys.exit(1)
        success = True
        result = None
        i = 4
        while i < len(sys.argv):
            if sys.argv[i] == "--success" and i + 1 < len(sys.argv):
                success = sys.argv[i + 1].lower() in ("true", "1", "yes")
                i += 2
            elif sys.argv[i] == "--result" and i + 1 < len(sys.argv):
                result = sys.argv[i + 1]
                i += 2
            else:
                i += 1
        complete(sys.argv[2], sys.argv[3], success, result)
    elif cmd == "retry":
        if len(sys.argv) < 4:
            print("Usage: subagent_dispatch.py retry <project> <subagent_id>")
            sys.exit(1)
        retry_subagent(sys.argv[2], sys.argv[3])
    elif cmd == "report":
        if len(sys.argv) < 3:
            print("Usage: subagent_dispatch.py report <project>")
            sys.exit(1)
        report(sys.argv[2])
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
