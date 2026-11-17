"""Terminal-state polling, heartbeats, task journal, and crash recovery."""

from __future__ import annotations

import json
import os
import sys
import tempfile
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .errors import SkillError
from .http import ApiClient
from .outputs import OutputManager
from .paths import task_dir


WAITING = {"", "queued", "queueing", "pending", "waiting", "submitted", "created", "preparing", "running", "processing", "in_progress", "generating"}
SUCCESS = {"success", "succeeded", "completed", "complete", "done", "finished"}
FAILED = {"failed", "failure", "error", "canceled", "cancelled", "expired", "timeout"}


@dataclass
class TaskRecord:
    task_id: str
    kind: str
    query_url: str
    output_category: str
    stem: str
    status: str = "submitted"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    attempts: int = 0
    progress: str = ""
    result_urls: list[str] = field(default_factory=list)
    files: list[str] = field(default_factory=list)
    error: str = ""


class TaskJournal:
    def __init__(self, directory: Path | None = None) -> None:
        self.directory = directory or task_dir()
        self.directory.mkdir(parents=True, exist_ok=True)

    def path(self, task_id: str) -> Path:
        safe_id = "".join(character for character in task_id if character.isalnum() or character in "-_")
        return self.directory / f"{safe_id}.json"

    def save(self, record: TaskRecord) -> None:
        record.updated_at = datetime.now(timezone.utc).isoformat()
        path = self.path(record.task_id)
        fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(asdict(record), handle, ensure_ascii=False, indent=2)
                handle.write("\n")
            os.replace(temp_name, path)
        finally:
            if os.path.exists(temp_name):
                os.unlink(temp_name)

    def pending(self) -> list[TaskRecord]:
        records: list[TaskRecord] = []
        for path in sorted(self.directory.glob("*.json")):
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
                record = TaskRecord(**payload)
            except (OSError, json.JSONDecodeError, TypeError):
                continue
            if record.status.lower() not in SUCCESS | FAILED and not record.files:
                records.append(record)
        return records


def _nested(payload: dict[str, Any], *path: str) -> Any:
    value: Any = payload
    for key in path:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def normalize_response(kind: str, response: dict[str, Any]) -> tuple[str, str, list[str], str]:
    data = response.get("data")
    status: Any = response.get("status", "")
    progress: Any = response.get("progress", "")
    error = ""
    urls: list[str] = []

    if kind == "music" and isinstance(data, dict):
        status = data.get("status", status)
        progress = data.get("progress", progress)
        error = str(data.get("fail_reason", ""))
        for item in data.get("data", []) if isinstance(data.get("data"), list) else []:
            if isinstance(item, dict) and item.get("audio_url"):
                urls.append(str(item["audio_url"]))
    elif kind == "pic" and isinstance(data, dict):
        state = data.get("state")
        progress = data.get("progress", progress)
        if isinstance(state, int):
            status = "success" if state == 1 else ("failed" if state < 0 else "processing")
            if state < 0:
                error = str(data.get("state_detail", f"Image task failed with state {state}."))
        for key in ("image", "mask"):
            if data.get(key):
                urls.append(str(data[key]))
    else:
        status = response.get("status", _nested(response, "data", "status") or "")
        progress = response.get("progress", _nested(response, "data", "progress") or "")
        candidates = [
            _nested(response, "content", "video_url"),
            _nested(response, "output", "file_url"),
            _nested(response, "data", "url"),
            response.get("url"),
        ]
        urls.extend(str(item) for item in candidates if isinstance(item, str) and item)

    normalized = str(status).strip().lower()
    if urls and normalized not in FAILED:
        normalized = "success"
    elif normalized in SUCCESS:
        normalized = "success"
    elif normalized in FAILED:
        normalized = "failed"
    else:
        normalized = "processing"
    return normalized, str(progress), urls, error


class TaskRunner:
    def __init__(
        self,
        client: ApiClient,
        config: dict[str, Any],
        *,
        journal: TaskJournal | None = None,
        sleep_fn: Callable[[float], None] = time.sleep,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self.client = client
        self.config = config
        self.journal = journal or TaskJournal()
        self.sleep_fn = sleep_fn
        self.clock = clock

    def wait(self, record: TaskRecord, out_dir: str = "", max_wait: float | None = None) -> dict[str, Any]:
        polling = self.config["polling"]
        heartbeat_seconds = int(polling.get("heartbeat_seconds", 30))
        configured_wait = polling.get("max_wait_seconds")
        max_wait = max_wait if max_wait is not None else configured_wait
        started = self.clock()
        last_heartbeat = started - heartbeat_seconds
        interval = 2.0 if record.kind in {"3d", "pic"} else 5.0
        transient_errors = 0
        max_transient_errors = int(polling.get("max_transient_errors", 8))
        self.journal.save(record)

        while True:
            elapsed = self.clock() - started
            if max_wait is not None and elapsed >= float(max_wait):
                record.status = "timeout"
                record.error = "User-configured maximum wait reached."
                self.journal.save(record)
                raise SkillError("TASK_WAIT_TIMEOUT", record.error, details={"task_id": record.task_id})

            self.sleep_fn(interval)
            try:
                response = self.client.request_json("GET", record.query_url, timeout=90)
                transient_errors = 0
            except SkillError as error:
                if not error.retryable:
                    record.status = "failed"
                    record.error = error.message
                    self.journal.save(record)
                    raise
                transient_errors += 1
                record.status = "retrying"
                record.error = error.message
                record.attempts += 1
                self.journal.save(record)
                if transient_errors > max_transient_errors:
                    raise SkillError(
                        "TASK_POLL_ERROR_LIMIT",
                        "Task polling exceeded the configured transient-error limit.",
                        details={"task_id": record.task_id, "last_error": error.message},
                        retryable=True,
                    ) from error
                print(
                    f"Transient polling error for {record.kind} task {record.task_id}; retrying "
                    f"({transient_errors}/{max_transient_errors}).",
                    file=sys.stderr,
                    flush=True,
                )
                interval = min(15.0, interval * 1.35)
                continue
            status, progress, urls, error = normalize_response(record.kind, response)
            record.status = status
            record.progress = progress
            record.result_urls = urls
            record.attempts += 1
            record.error = error
            self.journal.save(record)

            now = self.clock()
            if now - last_heartbeat >= heartbeat_seconds:
                print(
                    f"Waiting for {record.kind} task {record.task_id}: status={status} progress={progress or '-'} elapsed={int(now-started)}s",
                    file=sys.stderr,
                    flush=True,
                )
                last_heartbeat = now

            if status == "failed":
                raise SkillError("TASK_FAILED", error or f"{record.kind} task failed.", details={"task_id": record.task_id})
            if status == "success":
                if not urls:
                    raise SkillError("TASK_RESULT_MISSING", "Task succeeded but no downloadable result was returned.", details={"task_id": record.task_id})
                manager = OutputManager(self.config, record.output_category, out_dir)
                paths = [str(manager.download(self.client, url, record.stem)) for url in urls]
                record.files = paths
                self.journal.save(record)
                return {"task_id": record.task_id, "status": "success", "files": paths, "response": response}

            interval = min(15.0, interval * 1.35)
