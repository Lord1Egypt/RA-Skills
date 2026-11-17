#!/usr/bin/env python3
"""Poll Tencent Meeting deterministically and emit NDJSON only for new conflicts."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, time as clock_time, timedelta, timezone
from itertools import combinations
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


STATE_VERSION = 1


class WatcherError(RuntimeError):
    """A safe, user-actionable watcher failure."""


def utc_iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def parse_time(value: Any) -> datetime:
    if isinstance(value, (int, float)):
        timestamp = float(value)
    elif isinstance(value, str):
        raw = value.strip()
        if not raw:
            raise ValueError("empty time")
        try:
            timestamp = float(raw)
        except ValueError:
            normalized = raw[:-1] + "+00:00" if raw.endswith("Z") else raw
            parsed = datetime.fromisoformat(normalized)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=datetime.now().astimezone().tzinfo)
            return parsed.astimezone(timezone.utc)
    else:
        raise ValueError("unsupported time type")

    if timestamp > 10_000_000_000:
        timestamp /= 1000
    return datetime.fromtimestamp(timestamp, tz=timezone.utc)


def parse_clock(value: str) -> clock_time:
    try:
        parsed = datetime.strptime(value, "%H:%M").time()
    except ValueError as error:
        raise WatcherError(f"invalid HH:MM time: {value}") from error
    return parsed.replace(second=0, microsecond=0)


def parse_number_set(value: str, minimum: int, maximum: int, label: str) -> Tuple[int, ...]:
    try:
        numbers = {int(part.strip()) for part in value.split(",") if part.strip()}
    except ValueError as error:
        raise WatcherError(f"invalid {label}: {value}") from error
    if not numbers or any(number < minimum or number > maximum for number in numbers):
        raise WatcherError(f"{label} must contain comma-separated values from {minimum} to {maximum}")
    return tuple(sorted(numbers))


def schedule_timezone(name: str) -> Any:
    if name == "local":
        return datetime.now().astimezone().tzinfo
    try:
        return ZoneInfo(name)
    except ZoneInfoNotFoundError as error:
        raise WatcherError(f"unknown IANA timezone: {name}") from error


def schedule_times(
    office_start: clock_time,
    office_end: clock_time,
    minutes: Sequence[int],
    explicit: str,
) -> Tuple[clock_time, ...]:
    if office_end < office_start:
        raise WatcherError("--office-end must not be earlier than --office-start")
    if explicit:
        slots = {parse_clock(part.strip()) for part in explicit.split(",") if part.strip()}
        if not slots:
            raise WatcherError("--schedule-times must contain at least one HH:MM value")
    else:
        slots = {
            clock_time(hour=hour, minute=minute)
            for hour in range(24)
            for minute in minutes
            if office_start <= clock_time(hour=hour, minute=minute) <= office_end
        }
    if not slots:
        raise WatcherError("the configured office window contains no scheduled check time")
    if any(slot < office_start or slot > office_end for slot in slots):
        raise WatcherError("all --schedule-times values must fall within office hours")
    return tuple(sorted(slots))


def scheduled_slots_for_date(
    day: datetime,
    timezone_value: Any,
    weekdays: Sequence[int],
    slots: Sequence[clock_time],
) -> Tuple[datetime, ...]:
    local_day = day.astimezone(timezone_value)
    if local_day.isoweekday() not in weekdays:
        return ()
    return tuple(
        datetime.combine(local_day.date(), slot, tzinfo=timezone_value)
        for slot in slots
    )


def matching_schedule_slot(
    now: datetime,
    timezone_value: Any,
    weekdays: Sequence[int],
    slots: Sequence[clock_time],
    grace_seconds: int,
) -> Optional[datetime]:
    local_now = now.astimezone(timezone_value)
    for slot in scheduled_slots_for_date(local_now, timezone_value, weekdays, slots):
        elapsed = (local_now - slot).total_seconds()
        if 0 <= elapsed < grace_seconds:
            return slot
    return None


def next_schedule_slot(
    after: datetime,
    timezone_value: Any,
    weekdays: Sequence[int],
    slots: Sequence[clock_time],
) -> datetime:
    local_after = after.astimezone(timezone_value)
    for offset in range(15):
        candidate_day = local_after + timedelta(days=offset)
        for slot in scheduled_slots_for_date(candidate_day, timezone_value, weekdays, slots):
            if slot > local_after:
                return slot
    raise WatcherError("cannot find a scheduled check within the next 15 days")


def digest(parts: Iterable[str]) -> str:
    return hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()[:24]


@dataclass(frozen=True)
class Meeting:
    key: str
    signature: str
    subject: str
    meeting_code: str
    start: datetime
    end: datetime
    status: str

    def public(self) -> Dict[str, str]:
        result = {
            "subject": self.subject,
            "meeting_code": self.meeting_code,
            "start_time": utc_iso(self.start),
            "end_time": utc_iso(self.end),
        }
        if self.status:
            result["status"] = self.status
        return result

    def state_record(self) -> Dict[str, str]:
        result = self.public()
        result["signature"] = self.signature
        return result


def first_value(item: Dict[str, Any], names: Sequence[str], default: Any = "") -> Any:
    for name in names:
        if name in item and item[name] not in (None, ""):
            return item[name]
    return default


def normalize_meeting(item: Dict[str, Any]) -> Optional[Meeting]:
    try:
        start_raw = first_value(item, ("start_time", "startTime", "start"))
        end_raw = first_value(item, ("end_time", "endTime", "end"))
        start = parse_time(start_raw)
        end = parse_time(end_raw)
    except (TypeError, ValueError, OverflowError):
        return None
    if end <= start:
        return None

    subject = str(first_value(item, ("subject", "meeting_subject", "topic", "title"), "未命名会议"))
    meeting_code = str(first_value(item, ("meeting_code", "meetingCode", "meeting_number"), ""))
    meeting_id = str(first_value(item, ("meeting_id", "meetingId"), meeting_code))
    sub_meeting_id = str(first_value(item, ("sub_meeting_id", "subMeetingId"), ""))
    status = str(first_value(item, ("status", "meeting_status"), ""))

    # Include the occurrence start so expanded recurring meetings remain distinct.
    key = digest((meeting_id, sub_meeting_id, utc_iso(start)))
    signature = digest((subject, meeting_code, utc_iso(start), utc_iso(end), status))
    return Meeting(key, signature, subject, meeting_code, start, end, status)


def response_page(payload: Any) -> Tuple[List[Dict[str, Any]], str]:
    if not isinstance(payload, (dict, list)):
        raise WatcherError("tmeet returned an unsupported JSON shape")

    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)], ""

    data = payload.get("data", payload)
    containers = [data, payload] if isinstance(data, dict) else [payload]
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)], ""

    items: Optional[List[Any]] = None
    for container in containers:
        if not isinstance(container, dict):
            continue
        for key in ("meeting_info_list", "meetings", "items", "list"):
            candidate = container.get(key)
            if isinstance(candidate, list):
                items = candidate
                break
        if items is not None:
            break

    next_token = ""
    for container in containers:
        if isinstance(container, dict) and container.get("next_page_token") not in (None, ""):
            next_token = str(container["next_page_token"])
            break
    return [item for item in (items or []) if isinstance(item, dict)], next_token


def parse_cli_json(stdout: str) -> Any:
    text = stdout.strip()
    if not text:
        raise WatcherError("tmeet returned empty output")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        for line in reversed(text.splitlines()):
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                continue
    raise WatcherError("tmeet output did not contain valid JSON")


def resolve_executable(value: str) -> str:
    executable = shutil.which(value)
    if executable is None:
        raise WatcherError(f"tmeet executable not found: {value}")
    return executable


def needs_windows_batch_shell(executable: str, platform_name: str = os.name) -> bool:
    return platform_name == "nt" and Path(executable).suffix.lower() in (".bat", ".cmd")


def run_cli(command: Sequence[str], timeout_seconds: int) -> Any:
    executable = resolve_executable(command[0])
    resolved_command = [executable, *command[1:]]
    windows_batch = needs_windows_batch_shell(executable)
    try:
        completed = subprocess.run(
            resolved_command,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="strict",
            # npm exposes package binaries as .cmd shims on Windows. Python's
            # subprocess documentation recommends a shell for intentional
            # batch-file launches so arguments receive Windows escaping.
            shell=windows_batch,
            timeout=timeout_seconds,
        )
    except (FileNotFoundError, UnicodeError) as error:
        raise WatcherError(f"cannot execute tmeet as UTF-8: {executable}") from error
    except subprocess.TimeoutExpired as error:
        raise WatcherError("tmeet meeting list timed out") from error
    except OSError as error:
        raise WatcherError(f"cannot execute tmeet: {executable}") from error

    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).strip().splitlines()
        safe_detail = detail[-1][:240] if detail else "no error detail"
        raise WatcherError(f"tmeet meeting list failed ({completed.returncode}): {safe_detail}")
    return parse_cli_json(completed.stdout)


def query_meetings(
    tmeet_bin: str,
    start: datetime,
    end: datetime,
    max_pages: int,
    timeout_seconds: int,
) -> List[Meeting]:
    meetings: Dict[str, Meeting] = {}
    token = ""
    seen_tokens: Set[str] = set()
    invalid_records = 0

    for page_index in range(max_pages):
        command = [
            tmeet_bin,
            "meeting",
            "list",
            "--start",
            start.astimezone().isoformat(timespec="seconds"),
            "--end",
            end.astimezone().isoformat(timespec="seconds"),
            "--show-all-sub",
            "1",
            "--page-size",
            "20",
            "--compact",
        ]
        if token:
            command.extend(("--page-token", token))
        payload = run_cli(command, timeout_seconds)
        page, next_token = response_page(payload)
        for item in page:
            meeting = normalize_meeting(item)
            if meeting is None:
                invalid_records += 1
                continue
            meetings[meeting.key] = meeting

        if not next_token:
            if invalid_records:
                raise WatcherError(
                    f"{invalid_records} meeting record(s) lacked a valid start/end time; state was not updated"
                )
            return sorted(meetings.values(), key=lambda meeting: (meeting.start, meeting.end, meeting.key))
        if next_token in seen_tokens:
            raise WatcherError("tmeet returned a repeated page token")
        seen_tokens.add(next_token)
        token = next_token

    raise WatcherError(f"meeting list exceeded --max-pages={max_pages}; state was not updated")


def conflict_fingerprint(kind: str, keys: Iterable[str], start: datetime, end: datetime) -> str:
    return digest((kind, *sorted(keys), utc_iso(start), utc_iso(end)))


def pair_conflicts(meetings: Sequence[Meeting], soft_gap_minutes: int) -> List[Dict[str, Any]]:
    conflicts: List[Dict[str, Any]] = []
    for left, right in combinations(meetings, 2):
        overlap_start = max(left.start, right.start)
        overlap_end = min(left.end, right.end)
        keys = (left.key, right.key)
        public_meetings = [left.public(), right.public()]
        if overlap_start < overlap_end:
            conflicts.append(
                {
                    "kind": "hard",
                    "meetings": public_meetings,
                    "overlap_start": utc_iso(overlap_start),
                    "overlap_end": utc_iso(overlap_end),
                    "overlap_minutes": int((overlap_end - overlap_start).total_seconds() // 60),
                    "_keys": keys,
                    "_fingerprint": conflict_fingerprint("hard", keys, overlap_start, overlap_end),
                }
            )
            continue

        earlier, later = (left, right) if left.end <= right.start else (right, left)
        gap_seconds = (later.start - earlier.end).total_seconds()
        if 0 <= gap_seconds < soft_gap_minutes * 60:
            conflicts.append(
                {
                    "kind": "soft",
                    "meetings": [earlier.public(), later.public()],
                    "gap_minutes": int(gap_seconds // 60),
                    "_keys": keys,
                    "_fingerprint": conflict_fingerprint("soft", keys, earlier.end, later.start),
                }
            )
    return conflicts


def multi_conflicts(meetings: Sequence[Meeting]) -> List[Dict[str, Any]]:
    boundaries = sorted({meeting.start for meeting in meetings} | {meeting.end for meeting in meetings})
    segments: List[Tuple[datetime, datetime, Tuple[Meeting, ...]]] = []
    for start, end in zip(boundaries, boundaries[1:]):
        active = tuple(sorted(
            (meeting for meeting in meetings if meeting.start < end and meeting.end > start),
            key=lambda meeting: meeting.key,
        ))
        if len(active) < 3:
            continue
        if segments and segments[-1][1] == start and tuple(m.key for m in segments[-1][2]) == tuple(m.key for m in active):
            previous = segments[-1]
            segments[-1] = (previous[0], end, active)
        else:
            segments.append((start, end, active))

    conflicts: List[Dict[str, Any]] = []
    for start, end, active in segments:
        keys = tuple(meeting.key for meeting in active)
        conflicts.append(
            {
                "kind": "multi",
                "meetings": [meeting.public() for meeting in active],
                "overlap_start": utc_iso(start),
                "overlap_end": utc_iso(end),
                "overlap_minutes": int((end - start).total_seconds() // 60),
                "_keys": keys,
                "_fingerprint": conflict_fingerprint("multi", keys, start, end),
            }
        )
    return conflicts


def detect_conflicts(meetings: Sequence[Meeting], soft_gap_minutes: int) -> List[Dict[str, Any]]:
    return pair_conflicts(meetings, soft_gap_minutes) + multi_conflicts(meetings)


def load_state(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {"version": STATE_VERSION, "initialized": False, "meetings": {}, "active_conflicts": []}
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise WatcherError(f"cannot read state file: {path}") from error
    if not isinstance(state, dict) or state.get("version") != STATE_VERSION:
        raise WatcherError(f"unsupported state file version: {path}")
    return state


def atomic_write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        temporary.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True), encoding="utf-8")
        os.chmod(temporary, 0o600)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def public_conflict(conflict: Dict[str, Any]) -> Dict[str, Any]:
    return {key: value for key, value in conflict.items() if not key.startswith("_")}


def process_snapshot(
    meetings: Sequence[Meeting],
    state_path: Path,
    soft_gap_minutes: int,
    alert_existing: bool,
    query_start: datetime,
    query_end: datetime,
) -> Optional[Dict[str, Any]]:
    state = load_state(state_path)
    previous_meetings = state.get("meetings", {}) if isinstance(state.get("meetings"), dict) else {}
    initialized = bool(state.get("initialized"))
    current = {meeting.key: meeting.state_record() for meeting in meetings}
    changed_keys = {
        key
        for key, record in current.items()
        if key not in previous_meetings or previous_meetings[key].get("signature") != record.get("signature")
    }

    conflicts = detect_conflicts(meetings, soft_gap_minutes)
    active_fingerprints = {str(conflict["_fingerprint"]) for conflict in conflicts}
    previous_fingerprints = {str(value) for value in state.get("active_conflicts", [])}
    eligible_keys = changed_keys if initialized or alert_existing else set()
    alerts = [
        conflict
        for conflict in conflicts
        if set(conflict["_keys"]) & eligible_keys and conflict["_fingerprint"] not in previous_fingerprints
    ]

    new_state = {
        "version": STATE_VERSION,
        "initialized": True,
        "updated_at": utc_iso(datetime.now(timezone.utc)),
        "query_window": {"start": utc_iso(query_start), "end": utc_iso(query_end)},
        "meetings": current,
        "active_conflicts": sorted(active_fingerprints),
    }
    atomic_write_json(state_path, new_state)

    if not alerts:
        return None
    meeting_map = {meeting.key: meeting for meeting in meetings}
    involved_changed_keys = sorted(
        {key for conflict in alerts for key in conflict["_keys"] if key in changed_keys}
    )
    return {
        "event": "meeting.conflict.detected",
        "event_time": utc_iso(datetime.now(timezone.utc)),
        "source": "tmeet-conflict-check",
        "query_window": {"start": utc_iso(query_start), "end": utc_iso(query_end)},
        "changed_meetings": [meeting_map[key].public() for key in involved_changed_keys if key in meeting_map],
        "conflicts": [public_conflict(conflict) for conflict in alerts],
    }


def append_event(path: Path, event: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    try:
        os.write(descriptor, (json.dumps(event, ensure_ascii=False) + "\n").encode("utf-8"))
    finally:
        os.close(descriptor)


class StateLock:
    def __init__(self, state_path: Path):
        self.path = state_path.with_name(state_path.name + ".lock")
        self.acquired = False

    def __enter__(self) -> "StateLock":
        self.path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        try:
            descriptor = os.open(self.path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            try:
                pid = int(self.path.read_text(encoding="utf-8").strip())
                if not process_is_running(pid):
                    raise ProcessLookupError(pid)
            except (ValueError, ProcessLookupError, FileNotFoundError):
                self.path.unlink(missing_ok=True)
                descriptor = os.open(self.path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            except OSError as error:
                raise WatcherError(f"cannot inspect state lock: {self.path}") from error
            else:
                raise WatcherError(f"another watcher is already running: pid {pid}")
        os.write(descriptor, str(os.getpid()).encode("ascii"))
        os.close(descriptor)
        self.acquired = True
        return self

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        if self.acquired:
            self.path.unlink(missing_ok=True)


def _windows_process_is_running(pid: int) -> bool:
    """Check a Windows PID without sending a signal or terminating it."""
    import ctypes
    from ctypes import wintypes

    synchronize = 0x00100000
    wait_object_0 = 0x00000000
    wait_timeout = 0x00000102
    wait_failed = 0xFFFFFFFF
    error_access_denied = 5
    error_invalid_parameter = 87

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    open_process = kernel32.OpenProcess
    open_process.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
    open_process.restype = wintypes.HANDLE
    wait_for_single_object = kernel32.WaitForSingleObject
    wait_for_single_object.argtypes = (wintypes.HANDLE, wintypes.DWORD)
    wait_for_single_object.restype = wintypes.DWORD
    close_handle = kernel32.CloseHandle
    close_handle.argtypes = (wintypes.HANDLE,)
    close_handle.restype = wintypes.BOOL

    handle = open_process(synchronize, False, pid)
    if not handle:
        error_code = ctypes.get_last_error()
        if error_code == error_invalid_parameter:
            return False
        if error_code == error_access_denied:
            return True
        raise OSError(error_code, f"OpenProcess failed for pid {pid}")
    try:
        result = wait_for_single_object(handle, 0)
        if result == wait_timeout:
            return True
        if result == wait_object_0:
            return False
        if result == wait_failed:
            error_code = ctypes.get_last_error()
            raise OSError(error_code, f"WaitForSingleObject failed for pid {pid}")
        raise OSError(f"unexpected Windows wait result for pid {pid}: {result}")
    finally:
        close_handle(handle)


def process_is_running(pid: int) -> bool:
    if pid <= 0:
        raise ValueError("invalid pid")
    if pid == os.getpid():
        return True
    if os.name == "nt":
        return _windows_process_is_running(pid)
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def fixture_meetings(path: Path) -> List[Meeting]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise WatcherError(f"cannot read fixture JSON: {path}") from error
    page, _ = response_page(payload)
    return sorted(
        (meeting for item in page if (meeting := normalize_meeting(item)) is not None),
        key=lambda meeting: (meeting.start, meeting.end, meeting.key),
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--trigger",
        choices=("scheduled", "manual"),
        default="scheduled",
        help="scheduled obeys office-hour slots; manual runs immediately",
    )
    parser.add_argument("--watch", action="store_true", help="wait for and run at configured schedule slots")
    parser.add_argument("--timezone", default="local", help="IANA timezone or 'local'")
    parser.add_argument("--weekdays", default="1,2,3,4,5", help="ISO weekdays, Monday=1")
    parser.add_argument("--office-start", default="09:00", help="inclusive office start HH:MM")
    parser.add_argument("--office-end", default="18:00", help="inclusive office end HH:MM")
    parser.add_argument(
        "--schedule-minutes",
        default="0,30",
        help="minutes within each office hour; default is whole and half hour",
    )
    parser.add_argument(
        "--schedule-times",
        default="",
        help="custom comma-separated HH:MM slots; overrides --schedule-minutes",
    )
    parser.add_argument(
        "--slot-grace-seconds",
        type=int,
        default=120,
        help="maximum scheduler launch delay still accepted for a slot",
    )
    parser.add_argument("--lookahead-days", type=int, default=14, help="future query window in days")
    parser.add_argument("--lookback-hours", type=int, default=1, help="include recently started meetings")
    parser.add_argument("--soft-gap-minutes", type=int, default=15, help="soft-conflict threshold")
    parser.add_argument("--state-file", type=Path, required=True, help="persistent private state JSON")
    parser.add_argument("--event-file", type=Path, help="optional NDJSON event append file")
    parser.add_argument("--alert-existing", action="store_true", help="alert conflicts on first baseline")
    parser.add_argument("--tmeet-bin", default="tmeet", help="tmeet executable path")
    parser.add_argument("--max-pages", type=int, default=10, help="fail instead of saving partial data")
    parser.add_argument("--timeout", type=int, default=30, help="seconds allowed for each CLI call")
    parser.add_argument("--max-consecutive-errors", type=int, default=3)
    parser.add_argument("--fixture", type=Path, help=argparse.SUPPRESS)
    return parser


def validate_args(args: argparse.Namespace) -> None:
    if args.watch and args.trigger != "scheduled":
        raise WatcherError("--watch only supports --trigger scheduled")
    if args.lookahead_days < 1 or args.lookback_hours < 0:
        raise WatcherError("query window must be positive")
    if (
        args.soft_gap_minutes < 0
        or args.max_pages < 1
        or args.timeout < 1
        or args.max_consecutive_errors < 1
        or args.slot_grace_seconds < 1
    ):
        raise WatcherError("threshold, pagination, and timeout values must be valid")


def configured_schedule(
    args: argparse.Namespace,
) -> Tuple[Any, Tuple[int, ...], Tuple[clock_time, ...]]:
    timezone_value = schedule_timezone(args.timezone)
    weekdays = parse_number_set(args.weekdays, 1, 7, "weekdays")
    minutes = (
        ()
        if args.schedule_times
        else parse_number_set(args.schedule_minutes, 0, 59, "schedule minutes")
    )
    slots = schedule_times(
        parse_clock(args.office_start),
        parse_clock(args.office_end),
        minutes,
        args.schedule_times,
    )
    return timezone_value, weekdays, slots


def run_once(args: argparse.Namespace, now: Optional[datetime] = None) -> Optional[Dict[str, Any]]:
    now = now or datetime.now().astimezone()
    query_start = now - timedelta(hours=args.lookback_hours)
    query_end = now + timedelta(days=args.lookahead_days)
    meetings = (
        fixture_meetings(args.fixture)
        if args.fixture
        else query_meetings(args.tmeet_bin, query_start, query_end, args.max_pages, args.timeout)
    )
    event = process_snapshot(
        meetings,
        args.state_file,
        args.soft_gap_minutes,
        args.alert_existing,
        query_start,
        query_end,
    )
    if event is not None:
        # Keep the event stream ASCII-safe for Windows consoles and pipes with
        # legacy code pages. JSON consumers recover the original Unicode text.
        print(json.dumps(event, ensure_ascii=True), flush=True)
        if args.event_file:
            append_event(args.event_file, event)
    return event


def run_watch_loop(
    args: argparse.Namespace,
    timezone_value: Any,
    weekdays: Sequence[int],
    slots: Sequence[clock_time],
) -> int:
    errors = 0
    last_slot: Optional[datetime] = None
    while True:
        # Refresh the OS-local offset so a long-running watcher follows a
        # Windows/macOS/Linux daylight-saving transition without tzdata.
        active_timezone = schedule_timezone("local") if args.timezone == "local" else timezone_value
        now = datetime.now(active_timezone)
        due_slot = matching_schedule_slot(
            now,
            active_timezone,
            weekdays,
            slots,
            args.slot_grace_seconds,
        )
        if due_slot is not None and due_slot != last_slot:
            last_slot = due_slot
            try:
                run_once(args, now=now)
                errors = 0
            except WatcherError as error:
                errors += 1
                print(f"conflict watcher error: {error}", file=sys.stderr, flush=True)
                if errors >= args.max_consecutive_errors:
                    return 2

        next_slot = next_schedule_slot(datetime.now(active_timezone), active_timezone, weekdays, slots)
        delay = max(1.0, (next_slot - datetime.now(active_timezone)).total_seconds())
        if args.timezone == "local":
            delay = min(delay, 300.0)
        time.sleep(delay)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        validate_args(args)
        timezone_value, weekdays, slots = configured_schedule(args)

        # A scheduler may launch this command more frequently than the desired
        # check cadence. Outside a valid slot, exit before touching the lock,
        # state, CLI, stdout, or the Agent.
        if not args.watch and args.trigger == "scheduled":
            now = datetime.now(timezone_value)
            if matching_schedule_slot(
                now,
                timezone_value,
                weekdays,
                slots,
                args.slot_grace_seconds,
            ) is None:
                return 0

        with StateLock(args.state_file):
            if args.watch:
                return run_watch_loop(args, timezone_value, weekdays, slots)
            run_once(args, now=datetime.now(timezone_value))
            return 0
    except WatcherError as error:
        print(f"conflict watcher error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
