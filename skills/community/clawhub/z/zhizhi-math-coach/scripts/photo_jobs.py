#!/usr/bin/env python3
"""Durable photo queue consumed by an OpenClaw multimodal session, not by OCR here."""

from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import fcntl
import hashlib
import io
import json
import sys
import time
import uuid
from pathlib import Path

from workspace_transaction import atomic_write, inside


def save(path: Path, value: dict) -> None:
    atomic_write(path, (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode())


def enqueue(workspace: Path, images: list[str], date: str, note: str = "") -> dict:
    if dt.date.fromisoformat(date).isoformat() != date:
        raise ValueError("date must be YYYY-MM-DD")
    source_data = []
    digest = hashlib.sha256(date.encode())
    for source in images:
        path = Path(source)
        if not path.is_absolute():
            path = workspace / path
        suffix = path.suffix.lower()
        if suffix not in {".png", ".jpg", ".jpeg", ".webp", ".heic"}:
            raise ValueError(f"unsupported image type: {suffix}")
        data = path.read_bytes()
        if not data:
            raise ValueError("source image is empty")
        digest.update(hashlib.sha256(data).digest())
        source_data.append((suffix, data))
    if not source_data:
        raise ValueError("at least one image is required")
    job_id = digest.hexdigest()[:24]
    path = inside(workspace, f".zhizhi-math-coach/photo-jobs/{job_id}.json")
    if path.exists():
        return {**json.loads(path.read_text(encoding="utf-8")), "duplicate": True}
    image_paths = []
    for index, (suffix, data) in enumerate(source_data, 1):
        relative = f"uploads/photo-jobs/{job_id}/page-{index}{suffix}"
        atomic_write(inside(workspace, relative), data)
        image_paths.append(relative)
    job = {"id": job_id, "status": "queued", "date": date, "created_at": time.time(),
           "images": image_paths, "note": note, "attempts": 0}
    save(path, job)
    return job


def run_action(args: argparse.Namespace, workspace: Path, directory: Path) -> dict:
    if args.action == "enqueue":
        return enqueue(workspace, args.image, args.date, args.note)
    jobs = [(path, json.loads(path.read_text(encoding="utf-8"))) for path in directory.glob("*.json")]
    if args.action == "list":
        return {"jobs": [{k: job.get(k) for k in ("id", "status", "date", "attempts", "last_error", "result")} for _, job in jobs]}
    if args.action == "claim":
        now = time.time()
        for path, job in sorted(jobs, key=lambda pair: pair[1]["created_at"]):
            if job["status"] == "running" and job.get("lease_until", 0) <= now:
                job["status"] = "queued" if job["attempts"] < 3 else "failed"
                job["last_error"] = "worker lease expired"
                save(path, job)
            if job["status"] != "queued":
                continue
            job.update(status="running", lease_token=uuid.uuid4().hex,
                       lease_until=now + args.lease_seconds, attempts=job["attempts"] + 1)
            save(path, job)
            return {"job": job}
        return {"job": None}
    match = next(((path, job) for path, job in jobs if job["id"] == args.job_id), None)
    if match is None:
        raise ValueError("unknown job id")
    path, job = match
    if args.action == "retry":
        if job["status"] != "failed":
            raise ValueError("only failed jobs can be retried; new evidence should be submitted as a new batch")
        job.update(status="queued", attempts=0)
        job.pop("lease_token", None)
        save(path, job)
        return job
    if job["status"] != "running" or job.get("lease_token") != args.lease_token or job.get("lease_until", 0) <= time.time():
        raise ValueError("job lease is missing, expired or belongs to another worker")
    if args.action == "heartbeat":
        job["lease_until"] = time.time() + args.lease_seconds
    elif args.action == "fail":
        job.update(status="queued" if job["attempts"] < 3 else "failed", last_error=args.error)
    elif args.action == "finish":
        from record_grading_diagnosis import main as record_main
        payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
        if not isinstance(payload, dict) or not payload.get("items"):
            raise ValueError("photo jobs require full items, including correct/unanswered/uncertain questions")
        payload.update(record_id=f"photo-{job['id']}", date=job["date"], source_images=job["images"])
        # A failed recorder can be safely retried with this exact persisted payload.
        payload_path = inside(workspace, f".zhizhi-math-coach/photo-inputs/{job['id']}.json")
        save(payload_path, payload)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = record_main(["--workspace", str(workspace), "--input", str(payload_path), "--mode", "auto"])
        result = json.loads(output.getvalue())
        if code:
            raise ValueError("invalid photo diagnosis: " + json.dumps(result.get("errors", []), ensure_ascii=False))
        uncertain = payload.get("coverage") == "partial" or any(item.get("result") == "need-confirmation" for item in payload["items"])
        job.update(status="needs-confirmation" if uncertain else "completed", result=result, completed_at=time.time())
    save(path, job)
    return job


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=Path("."))
    commands = parser.add_subparsers(dest="action", required=True)
    add = commands.add_parser("enqueue")
    add.add_argument("--image", action="append", required=True)
    add.add_argument("--date", default=dt.date.today().isoformat())
    add.add_argument("--note", default="")
    commands.add_parser("list")
    claim = commands.add_parser("claim")
    claim.add_argument("--lease-seconds", type=int, default=900)
    for action in ("finish", "fail", "heartbeat", "retry"):
        command = commands.add_parser(action)
        command.add_argument("--job-id", required=True)
        if action != "retry":
            command.add_argument("--lease-token", required=True)
        if action == "finish":
            command.add_argument("--input", required=True)
        elif action == "fail":
            command.add_argument("--error", required=True)
        elif action == "heartbeat":
            command.add_argument("--lease-seconds", type=int, default=900)
    args = parser.parse_args(argv)
    if hasattr(args, "lease_seconds") and not 30 <= args.lease_seconds <= 3600:
        parser.error("--lease-seconds must be between 30 and 3600")
    workspace = args.workspace.resolve()
    directory = inside(workspace, ".zhizhi-math-coach/photo-jobs")
    directory.mkdir(parents=True, exist_ok=True)
    with inside(workspace, ".zhizhi-math-coach/photo-jobs.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        result = run_action(args, workspace, directory)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(1)
