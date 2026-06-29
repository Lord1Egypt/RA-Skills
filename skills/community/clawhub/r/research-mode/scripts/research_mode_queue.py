from __future__ import annotations

import fcntl
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from research_mode_utils import (
    NO_ACTIVE_LEASE,
    atomic_json_write,
    effective_lock_stale_timeout_min,
    ensure_dir,
    is_relative_to,
    minutes_since,
    read_json,
    utc_now,
)


QUEUE_DIR = ".research-mode/queue"
GLOBAL_LOCK_FILE = "global-worker-lock.json"
WAITERS_FILE = "waiters.json"
FLOCK_FILE = "queue.lock"
TERMINAL_TASK_STATUSES = {"awaiting_review", "complete", "failed", "cancelled"}


def queue_paths(root: Path) -> dict[str, Path]:
    queue_dir = root.expanduser().resolve() / QUEUE_DIR
    return {
        "dir": queue_dir,
        "global_lock": queue_dir / GLOBAL_LOCK_FILE,
        "waiters": queue_dir / WAITERS_FILE,
        "flock": queue_dir / FLOCK_FILE,
    }


def _read_json_object(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = read_json(path)
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _write_json_object(path: Path, payload: dict[str, Any]) -> None:
    atomic_json_write(path, payload)


@contextmanager
def _queue_lock(root: Path):
    paths = queue_paths(root)
    ensure_dir(paths["dir"])
    with paths["flock"].open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield paths
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def _read_waiters(path: Path) -> list[dict[str, Any]]:
    payload = _read_json_object(path)
    waiters = payload.get("waiters")
    return [item for item in waiters if isinstance(item, dict)] if isinstance(waiters, list) else []


def _write_waiters(path: Path, waiters: list[dict[str, Any]]) -> None:
    _write_json_object(path, {"waiters": waiters})


def _task_path_under_root(root: Path, raw_path: str | None) -> Path | None:
    if not raw_path:
        return None
    try:
        task_path = Path(raw_path).expanduser().resolve()
    except OSError:
        return None
    root_resolved = root.expanduser().resolve()
    return task_path if is_relative_to(task_path, root_resolved) else None


def _holder_matching_task_lock_state(root: Path, holder: dict[str, Any]) -> str:
    return _holder_task_lock_diagnostic(root, holder)["state"]


def _holder_task_lock_diagnostic(root: Path, holder: dict[str, Any]) -> dict[str, Any]:
    task_path = _task_path_under_root(root, holder.get("task_path"))
    if task_path is None:
        return {
            "state": "missing",
            "finding": _queue_finding(
                "queue_holder_task_missing",
                "Global queue holder points outside this research root or has no task path.",
                holder,
            ),
        }
    state_path = task_path / "state.json"
    if not state_path.exists():
        return {
            "state": "missing",
            "finding": _queue_finding(
                "queue_holder_task_missing",
                "Global queue holder points to a missing task.",
                holder,
            ),
        }
    try:
        state = read_json(state_path)
    except Exception:
        return {
            "state": "missing",
            "finding": _queue_finding(
                "queue_holder_state_unreadable",
                "Global queue holder task state cannot be read.",
                holder,
            ),
        }
    lock = state.get("lock") or {}
    matches = (
        lock.get("status") == "held"
        and lock.get("run_id") == holder.get("run_id")
        and lock.get("lease_token") == holder.get("lease_token")
        and state.get("id") == holder.get("task_id")
    )
    if not matches:
        return {
            "state": "missing",
            "finding": _queue_finding(
                "queue_holder_task_lock_mismatch",
                "Global queue holder does not match the task lock.",
                holder,
                {
                    "task_status": state.get("status"),
                    "task_lock_status": lock.get("status"),
                    "task_lock_run_id": lock.get("run_id"),
                    "task_lock_lease_token": lock.get("lease_token"),
                },
            ),
        }
    age = minutes_since(lock.get("started_at"))
    timeout = effective_lock_stale_timeout_min(state)
    if age is not None and age <= timeout:
        return {"state": "active", "finding": None}
    return {"state": "stale", "finding": None}


def _queue_finding(
    code: str,
    message: str,
    item: dict[str, Any],
    extra_details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    details = {
        "task_id": item.get("task_id"),
        "task_path": item.get("task_path"),
        "run_id": item.get("run_id") or item.get("last_blocked_by_run_id"),
    }
    if extra_details:
        details.update(extra_details)
    return {
        "code": code,
        "severity": "warning",
        "status": "manual_review_needed",
        "message": message,
        "details": details,
    }


def _waiter_findings(
    root: Path,
    waiters: list[dict[str, Any]],
    *,
    stale_waiter_timeout_min: int = 120,
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for waiter in waiters:
        task_path = _task_path_under_root(root, waiter.get("task_path"))
        if task_path is None or not (task_path / "state.json").exists():
            findings.append(
                _queue_finding(
                    "queue_waiter_task_missing",
                    "Queue waiter points to a missing task.",
                    waiter,
                    {"last_seen_at": waiter.get("last_seen_at")},
                )
            )
            continue
        try:
            state = read_json(task_path / "state.json")
        except Exception:
            findings.append(
                _queue_finding(
                    "queue_waiter_state_unreadable",
                    "Queue waiter task state cannot be read.",
                    waiter,
                    {"last_seen_at": waiter.get("last_seen_at")},
                )
            )
            continue
        if state.get("status") in TERMINAL_TASK_STATUSES:
            findings.append(
                _queue_finding(
                    "queue_terminal_task_waiter",
                    "Terminal task is still present in the global queue waiters.",
                    waiter,
                    {
                        "task_status": state.get("status"),
                        "last_seen_at": waiter.get("last_seen_at"),
                    },
                )
            )
        age = minutes_since(waiter.get("last_seen_at"))
        if age is not None and age > stale_waiter_timeout_min:
            findings.append(
                _queue_finding(
                    "queue_stale_waiter",
                    "Queue waiter has not been seen within the stale waiter timeout.",
                    waiter,
                    {
                        "last_seen_at": waiter.get("last_seen_at"),
                        "stale_waiter_timeout_min": stale_waiter_timeout_min,
                    },
                )
            )
    return findings


def _holder_is_protected(root: Path, holder: dict[str, Any]) -> bool:
    if not holder or holder.get("status") != "held":
        return False
    task_lock_state = _holder_matching_task_lock_state(root, holder)
    if task_lock_state == "active":
        return True
    if task_lock_state == "stale":
        return False
    age = minutes_since(holder.get("started_at"))
    timeout = int(holder.get("stale_timeout_min") or 30)
    return age is not None and age <= timeout


def _update_waiter(
    waiters: list[dict[str, Any]],
    *,
    task_id: str,
    task_path: Path,
    blocked_by_task_id: str | None,
    blocked_by_run_id: str | None,
    now: str,
) -> list[dict[str, Any]]:
    updated = False
    next_waiters: list[dict[str, Any]] = []
    for waiter in waiters:
        if waiter.get("task_id") == task_id:
            first_waiting_at = waiter.get("first_waiting_at") or now
            next_waiters.append(
                {
                    "task_id": task_id,
                    "task_path": str(task_path),
                    "first_waiting_at": first_waiting_at,
                    "last_seen_at": now,
                    "attempt_count": int(waiter.get("attempt_count") or 0) + 1,
                    "last_blocked_by_task_id": blocked_by_task_id,
                    "last_blocked_by_run_id": blocked_by_run_id,
                }
            )
            updated = True
        else:
            next_waiters.append(waiter)
    if not updated:
        next_waiters.append(
            {
                "task_id": task_id,
                "task_path": str(task_path),
                "first_waiting_at": now,
                "last_seen_at": now,
                "attempt_count": 1,
                "last_blocked_by_task_id": blocked_by_task_id,
                "last_blocked_by_run_id": blocked_by_run_id,
            }
        )
    return next_waiters


def _prune_waiters(
    root: Path, waiters: list[dict[str, Any]], *, stale_waiter_timeout_min: int = 120
) -> list[dict[str, Any]]:
    pruned: list[dict[str, Any]] = []
    for waiter in waiters:
        task_path = _task_path_under_root(root, waiter.get("task_path"))
        if task_path is None or not (task_path / "state.json").exists():
            continue
        age = minutes_since(waiter.get("last_seen_at"))
        if age is not None and age > stale_waiter_timeout_min:
            continue
        try:
            state = read_json(task_path / "state.json")
        except Exception:
            state = {}
        if state.get("status") in TERMINAL_TASK_STATUSES:
            continue
        pruned.append(waiter)
    return pruned


def _remove_waiter(waiters: list[dict[str, Any]], task_id: str) -> list[dict[str, Any]]:
    return [waiter for waiter in waiters if waiter.get("task_id") != task_id]


def acquire_global_queue(
    root: Path,
    *,
    task_id: str,
    task_path: Path,
    run_id: str,
    lease_token: str,
    stale_timeout_min: int,
    policy: str = "global_iteration_lock",
) -> dict[str, Any]:
    if policy == "disabled":
        return {"status": "disabled", "acquired": True, "policy": policy}
    now = utc_now()
    with _queue_lock(root) as paths:
        holder = _read_json_object(paths["global_lock"])
        waiters = _prune_waiters(root, _read_waiters(paths["waiters"]))

        if holder and holder.get("status") == "held" and _holder_is_protected(root, holder):
            waiters = _update_waiter(
                waiters,
                task_id=task_id,
                task_path=task_path,
                blocked_by_task_id=holder.get("task_id"),
                blocked_by_run_id=holder.get("run_id"),
                now=now,
            )
            _write_waiters(paths["waiters"], waiters)
            return {
                "status": "busy",
                "acquired": False,
                "reason": "global-research-lock-active",
                "normalized_reason": "deferred:global-research-lock",
                "active_task_id": holder.get("task_id"),
                "active_run_id": holder.get("run_id"),
                "position": next(
                    idx + 1
                    for idx, waiter in enumerate(waiters)
                    if waiter.get("task_id") == task_id
                ),
            }

        if holder and holder.get("status") == "held":
            holder["status"] = "stale_recovered"
            holder["released_at"] = now
            holder["last_released_by"] = task_id

        waiters = _update_waiter(
            waiters,
            task_id=task_id,
            task_path=task_path,
            blocked_by_task_id=None,
            blocked_by_run_id=None,
            now=now,
        )
        waiters = _prune_waiters(root, waiters)
        older_waiters = [waiter for waiter in waiters if waiter.get("task_id") != task_id]
        if older_waiters and waiters[0].get("task_id") != task_id:
            _write_waiters(paths["waiters"], waiters)
            next_waiter = waiters[0]
            return {
                "status": "busy",
                "acquired": False,
                "reason": "global-research-lock-active",
                "normalized_reason": "deferred:global-research-lock",
                "active_task_id": next_waiter.get("task_id"),
                "active_run_id": next_waiter.get("last_blocked_by_run_id"),
                "position": next(
                    idx + 1
                    for idx, waiter in enumerate(waiters)
                    if waiter.get("task_id") == task_id
                ),
            }

        waiters = _remove_waiter(waiters, task_id)
        lease = {
            "status": "held",
            "task_id": task_id,
            "task_path": str(task_path),
            "run_id": run_id,
            "lease_token": lease_token,
            "started_at": now,
            "stale_timeout_min": stale_timeout_min,
            "policy": policy,
            "released_at": None,
            "last_released_by": None,
        }
        _write_json_object(paths["global_lock"], lease)
        _write_waiters(paths["waiters"], waiters)
        return {
            "status": "acquired",
            "acquired": True,
            "lease": lease,
            "stale_recovered": bool(holder and holder.get("status") == "stale_recovered"),
        }


def release_global_queue(
    root: Path,
    *,
    task_id: str,
    run_id: str | None,
    lease_token: str | None,
    released_by: str,
) -> dict[str, Any]:
    if not run_id or lease_token is NO_ACTIVE_LEASE:
        return {"status": "no_active_global_lease"}
    now = utc_now()
    with _queue_lock(root) as paths:
        holder = _read_json_object(paths["global_lock"])
        if holder.get("status") != "held":
            return {"status": "no_active_global_lease"}
        if (
            holder.get("task_id") != task_id
            or holder.get("run_id") != run_id
            or holder.get("lease_token") != lease_token
        ):
            return {
                "status": "holder_mismatch",
                "active_task_id": holder.get("task_id"),
                "active_run_id": holder.get("run_id"),
            }
        holder["status"] = "released"
        holder["released_at"] = now
        holder["last_released_by"] = released_by
        _write_json_object(paths["global_lock"], holder)
        waiters = _remove_waiter(_read_waiters(paths["waiters"]), task_id)
        _write_waiters(paths["waiters"], waiters)
        return {"status": "released", "released_at": now}


def read_queue_status(root: Path) -> dict[str, Any]:
    paths = queue_paths(root)
    holder = _read_json_object(paths["global_lock"])
    raw_waiters = _read_waiters(paths["waiters"])
    waiters = _prune_waiters(root, raw_waiters)
    active_holder = holder if holder.get("status") == "held" else {}
    holder_diagnostic = (
        _holder_task_lock_diagnostic(root, active_holder) if active_holder else {}
    )
    active_holder_state = holder_diagnostic.get("state") if active_holder else None
    findings = []
    if holder_diagnostic.get("finding"):
        findings.append(holder_diagnostic["finding"])
    findings.extend(_waiter_findings(root, raw_waiters))
    if active_holder and active_holder_state == "missing":
        age = minutes_since(active_holder.get("started_at"))
        timeout = int(active_holder.get("stale_timeout_min") or 30)
        active_holder_state = (
            "active" if age is not None and age <= timeout else "stale"
        )
    status = "free"
    if active_holder:
        status = "stale" if active_holder_state == "stale" else "running"
    return {
        "status": status,
        "active_holder": active_holder or None,
        "active_holder_state": active_holder_state,
        "active_task_id": active_holder.get("task_id"),
        "active_run_id": active_holder.get("run_id"),
        "waiters": waiters,
        "waiter_count": len(waiters),
        "findings": findings,
        "has_findings": bool(findings),
    }
