"""Small, offline-first command line. No background service and no hidden model."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import shutil
import sys
from collections import Counter
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from datetime import datetime, timedelta, timezone
from pathlib import Path

from . import __version__
from .analysis import build_packets, render_report, validate_findings
from .records import in_window
from .runtime import SECRET_KEYS, Session, SourceError, now, verify_raw

STOP_STATUSES = {"auth-failed", "forbidden", "budget-exhausted", "rate-limited", "timeout",
                 "export-interrupted", "export-resume-needs-review", "permission-gap"}


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_new(path, data):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("x", encoding="utf-8") as out:
        out.write(data if isinstance(data, str) else json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def validate_config(config):
    if not isinstance(config, dict) or not isinstance(config.get("domain"), str) or not config["domain"].strip():
        raise ValueError("config needs a nonempty domain")
    # Configs are shared research scope, not credential containers.
    def no_secrets(value):
        if isinstance(value, dict):
            for key, item in value.items():
                if key.lower() in SECRET_KEYS:
                    raise ValueError("Do not put credentials in config; use named environment variables")
                no_secrets(item)
        elif isinstance(value, list):
            for item in value:
                no_secrets(item)
    no_secrets(config)
    jobs = config.get("sources")
    if not isinstance(jobs, list) or not jobs:
        raise ValueError("config.sources must contain at least one explicit source job")
    ids = set()
    for job in jobs:
        if not isinstance(job, dict) or not isinstance(job.get("id"), str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", job["id"]):
            raise ValueError("Each job needs a unique letters/numbers/hyphens id")
        if job["id"] in ids:
            raise ValueError("Duplicate job id")
        ids.add(job["id"])
        if job.get("platform") not in {"discord", "reddit", "x", "youtube"}:
            raise ValueError("Supported sources: discord, reddit, x, youtube")
        window = {**config.get("window", {}), **{k: job[k] for k in ("start", "end") if k in job}}
        if window.get("start") or window.get("end"):
            in_window(window.get("start") or now(), window.get("start"), window.get("end"))
    retention = config.get("retention_days", 30)
    if isinstance(retention, bool) or not isinstance(retention, int) or retention < 1:
        raise ValueError("retention_days must be a positive integer; this schedules review, never automatic deletion")
    return copy.deepcopy(config)


def get_session(run_dir, config=None, live=False):
    limits = (config or {}).get("limits", {})
    return Session(run_dir, live=live, max_requests=limits.get("max_requests", 100),
                   max_units=limits.get("max_units"))


def saved_run(run_dir):
    if not Path(run_dir, "config.json").is_file():
        raise ValueError("Not a Voice2Need run: missing config.json")
    config = read_json(Path(run_dir, "config.json"))
    ctx = get_session(run_dir, config)
    config["coverage"] = ctx.load_json("coverage.json", [])
    return ctx, config


def verify_records(ctx, records):
    errors, checked = [], 0
    cache = {}
    def contains_text(value, text):
        if isinstance(value, str):
            return value == text
        if isinstance(value, dict):
            return any(contains_text(v, text) for v in value.values())
        if isinstance(value, list):
            return any(contains_text(v, text) for v in value)
        return False
    for record in records:
        refs = record.get("raw", [])
        text_found = not record.get("text")
        if not refs:
            errors.append({"evidence_id": record.get("evidence_id"), "error": "Missing raw reference"})
        for ref in refs:
            try:
                value = verify_raw(ctx.root, ref, cache=cache)
                text_found = text_found or contains_text(value, record["text"])
                checked += 1
            except (ValueError, KeyError, IndexError, TypeError, OSError):
                errors.append({"evidence_id": record.get("evidence_id"), "error": "Invalid raw bytes or locator"})
        if not text_found:
            errors.append({"evidence_id": record.get("evidence_id"), "error": "Normalized text does not match its cited raw object"})
    return {"valid": not errors, "records": len(records), "raw_refs_checked": checked, "errors": errors,
            "observation_gaps": ctx.observation_gaps}


def run_collection(config, run_dir, *, live=False, workers=2):
    config = validate_config(config)
    if not 1 <= workers <= 4:
        raise ValueError("workers must be between 1 and 4")
    root = Path(run_dir).resolve()
    root.mkdir(parents=True, exist_ok=True)
    lock_path = root / ".run.lock"
    try:
        lock = lock_path.open("x")
    except FileExistsError:
        raise ValueError("Run is locked. Check whether its recorded process is alive before removing only .run.lock") from None
    with lock:
        lock.write(json.dumps({"pid": os.getpid(), "at": now()}))
    try:
        ctx = get_session(root, config, live)
        old = ctx.load_json("config.json")
        if old is not None and old != config:
            if {k: v for k, v in old.items() if k != "limits"} != {k: v for k, v in config.items() if k != "limits"}:
                raise ValueError("Scope changed: use a new run directory; keep the old run intact")
            ctx.write_raw({"before": old.get("limits", {}), "after": config.get("limits", {})}, kind="explicit-limit-revision")
            ctx.save_json("config.json", config)
        if old is None:
            ctx.save_json("config.json", config)
            ctx.save_json("retention.json", {"created_at": now(), "review_due":
                (datetime.now(timezone.utc) + timedelta(days=config.get("retention_days", 30))).isoformat(),
                "action": "Review source-specific retention requirements; nothing is deleted automatically"})
        from .adapters import discord, reddit, x, youtube
        adapters = {"discord": discord, "reddit": reddit, "x": x, "youtube": youtube}
        previous = {row["job_id"]: row for row in ctx.load_json("coverage.json", [])}
        jobs = []
        for source in config["sources"]:
            if previous.get(source["id"], {}).get("status") in {"complete", "no-results"}:
                continue
            jobs.append({**config.get("window", {}), **source})
        # Discord itself has a two-channel exporter queue. Do not multiply it by
        # running separate Discord jobs concurrently.
        if any(j["platform"] == "discord" and j.get("mode") == "export" for j in jobs):
            workers = 1
        outcomes, stop = previous.copy(), False

        def execute(job):
            ctx.event({"type": "job-start", "job_id": job["id"]})
            try:
                result = adapters[job["platform"]].collect(ctx, job)
            except SourceError as exc:
                result = {"job_id": job["id"], "platform": job["platform"], "status": exc.status,
                          "gaps": [{"status": exc.status, "detail": str(exc), "raw": exc.raw}],
                          "counts": {}, "checkpoint": ctx.get_checkpoint(job["id"])}
            except (OSError, ValueError, KeyError, TypeError, IndexError):
                result = {"job_id": job["id"], "platform": job["platform"], "status": "invalid-input-or-schema",
                          "counts": {}, "gaps": [{"detail": "Check input shape and saved raw response; existing data was preserved"}]}
            ctx.event({"type": "job-end", **result})
            return result

        iterator = iter(jobs)
        with ThreadPoolExecutor(max_workers=workers) as pool:
            pending = {}
            for _ in range(workers):
                job = next(iterator, None)
                if job:
                    pending[pool.submit(execute, job)] = job
            while pending:
                done, _ = wait(pending, return_when=FIRST_COMPLETED)
                for future in done:
                    job = pending.pop(future)
                    result = future.result()
                    outcomes[job["id"]] = result
                    if result["status"] in STOP_STATUSES:
                        stop = True
                    for gap in result.get("gaps", []):
                        if isinstance(gap, dict) and (gap.get("status") in STOP_STATUSES or gap.get("reason") in STOP_STATUSES):
                            stop = True
                ctx.save_json("coverage.json", list(outcomes.values()))
                while not stop and len(pending) < workers:
                    job = next(iterator, None)
                    if job is None:
                        break
                    pending[pool.submit(execute, job)] = job
            for job in iterator:
                outcomes[job["id"]] = {"job_id": job["id"], "platform": job["platform"],
                    "status": "not-attempted", "counts": {}, "gaps": [{"detail": "A previous job stopped; no automatic paid fallback"}]}
        ordered = [outcomes[j["id"]] for j in config["sources"]]
        ctx.save_json("coverage.json", ordered)
        ctx.save_json("manifest.json", {"version": __version__, "updated_at": now(),
                                       "usage": ctx.state, "coverage": ordered,
                                       "records": len(ctx.records()), "live": live})
        return ordered
    finally:
        lock_path.unlink()  # Only the lock this invocation created, never research data.


def demo(output):
    root = Path(output)
    if root.exists():
        raise ValueError("Choose a new demo output directory; existing files are never overwritten")
    fixture = Path(__file__).resolve().parents[2] / "assets" / "demo" / "podcast-production"
    config, records, findings = [read_json(fixture / f"{n}.json") for n in ("config", "records", "findings")]
    ctx = get_session(root, config)
    ctx.save_json("config.json", config)
    for record in records:
        record["raw"] = [ctx.write_raw(copy.deepcopy(record), synthetic=True)]
    ctx.add_records(records)
    ctx.save_json("coverage.json", config.get("coverage", []))
    write_new(root / "findings.json", findings)
    write_new(root / "packets.json", build_packets(records, config))
    write_new(root / "report.md", render_report(findings, records, config))
    return {"synthetic": True, "network_requests": 0, "records": len(records), "report": str((root / "report.md").resolve())}


def merge_runs(run_dirs, output):
    """Consolidate local runs with matching research scope; never mutate inputs."""
    if len(run_dirs) < 2:
        raise ValueError("merge requires at least two run directories")
    inputs = [Path(p).resolve() for p in run_dirs]
    if len(set(inputs)) != len(inputs):
        raise ValueError("Do not merge the same run twice")
    target = Path(output).resolve()
    if target.exists() or any(p == target or p in target.parents for p in inputs):
        raise ValueError("Choose a new output directory outside all input runs")
    sources = []
    for root in inputs:
        ctx, config = saved_run(root)
        if ctx.path(".run.lock").exists():
            raise ValueError("Finish active collection before merging its run")
        rows = ctx.records()
        if not verify_records(ctx, rows)["valid"]:
            raise ValueError("An input run failed raw verification; fix it before merging")
        if sources and (config.get("domain"), config.get("window")) != (sources[0][1].get("domain"), sources[0][1].get("window")):
            raise ValueError("Merge inputs need matching domain and window; review different scopes separately")
        for name in ("raw", "imports", "exports", "source-runs"):
            source = root / name
            if source.exists() and (source.is_symlink() or any(p.is_symlink() for p in source.rglob("*"))):
                raise ValueError("Refusing symlinked raw input")
        sources.append((ctx, config, rows))
    target.mkdir(parents=True)
    output_ctx = Session(target, max_requests=0)
    config = copy.deepcopy(sources[0][1])
    config["sources"], config["coverage"], config["limits"] = [], [], {"max_requests": 0}
    config["merged"] = True
    source_index = []
    for index, (ctx, source_config, rows) in enumerate(sources):
        prefix = f"source-runs/{index + 1:03d}"
        dest = output_ctx.path(prefix)
        dest.mkdir(parents=True)
        # Keep all raw pages and export fragments, not only useful evidence.
        # Credentials and arbitrary unrelated files are not copied.
        for name in ("raw", "imports", "exports", "source-runs"):
            source = ctx.root / name
            if source.exists():
                shutil.copytree(source, dest / name)
        copied_records = []
        for record in rows:
            copied = copy.deepcopy(record)
            for ref in copied.get("raw", []):
                ref["path"] = f"{prefix}/{ref['path']}"
            copied.setdefault("metadata", {})["source_run"] = prefix
            copied_records.append(copied)
        output_ctx.add_records(copied_records)
        for job in source_config.get("sources", []):
            config["sources"].append({**job, "id": f"run{index + 1}-{job['id']}"})
        for row in source_config.get("coverage", []):
            config["coverage"].append({**row, "job_id": f"run{index + 1}-{row.get('job_id', 'unknown')}", "source_run": prefix})
        source_index.append({"source_run": prefix, "records": len(rows), "config": source_config,
                             "retention": ctx.load_json("retention.json")})
    output_ctx.save_json("config.json", config)
    output_ctx.save_json("coverage.json", config["coverage"])
    output_ctx.save_json("merged-sources.json", source_index)
    report = verify_records(output_ctx, output_ctx.records())
    output_ctx.save_json("merge-verification.json", report)
    return {"output": str(target), "input_runs": len(inputs), **report,
            "note": "Source copies preserve their original retention deadlines; merge does not reset them"}


def parser():
    p = argparse.ArgumentParser(description="Voice2Need: collect discussions, preserve sources, validate needs research")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="command", required=True)
    d = sub.add_parser("demo", help="See a synthetic report: no account, no network, no charge")
    d.add_argument("--output", required=True)
    m = sub.add_parser("merge", help="Combine local runs with the same domain/window; preserve raw copies")
    m.add_argument("--run-dirs", nargs="+", required=True)
    m.add_argument("--output", required=True)
    c = sub.add_parser("collect", help="Run explicit collection jobs; network requires --live")
    c.add_argument("--config", required=True)
    c.add_argument("--run-dir", required=True)
    c.add_argument("--live", action="store_true")
    c.add_argument("--workers", type=int, default=2)
    for name in ("status", "prepare", "verify", "report"):
        item = sub.add_parser(name)
        item.add_argument("--run-dir", required=True)
        if name in {"prepare", "report"}:
            item.add_argument("--output", required=True)
        if name == "report":
            item.add_argument("--findings", required=True)
    return p


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command == "demo":
            result = demo(args.output)
        elif args.command == "merge":
            result = merge_runs(args.run_dirs, args.output)
        elif args.command == "collect":
            result = run_collection(read_json(args.config), args.run_dir, live=args.live, workers=args.workers)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0 if all(r["status"] in {"complete", "no-results"} for r in result) else 2
        else:
            ctx, config = saved_run(args.run_dir)
            records = ctx.records()
            if ctx.observation_gaps:
                config["coverage"].append({"job_id": "local-observation-recovery", "platform": "storage",
                                           "status": "partial", "gaps": ctx.observation_gaps})
            if args.command == "status":
                result = {"records": len(records), "platforms": dict(Counter(r["platform"] for r in records)),
                          "coverage": config["coverage"], "usage": ctx.state,
                          "observation_gaps": ctx.observation_gaps,
                          "retention": ctx.load_json("retention.json", {"status": "not-recorded"})}
            elif args.command == "verify":
                result = verify_records(ctx, records)
                print(json.dumps(result, ensure_ascii=False, indent=2))
                return 0 if result["valid"] else 2
            elif args.command == "prepare":
                result = verify_records(ctx, records)
                if not result["valid"]:
                    raise ValueError("Raw reference checks failed; run verify for details")
                write_new(args.output, build_packets(records, config))
                result = {"packets": str(Path(args.output).resolve()), "records": len(records),
                          "next": "Host AI reads packets and writes findings using the bundled analysis guide"}
            elif args.command == "report":
                if not verify_records(ctx, records)["valid"]:
                    raise ValueError("Raw reference checks failed; run verify for details")
                findings = read_json(args.findings)
                result = validate_findings(findings, records)
                if not result["valid"]:
                    print(json.dumps(result, ensure_ascii=False, indent=2))
                    return 2
                write_new(args.output, render_report(findings, records, config))
                result = {"report": str(Path(args.output).resolve()), "checks": result,
                          "note": "Mechanical checks pass; semantic review still belongs to a person or the host AI"}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (SourceError, ValueError, OSError, KeyError, TypeError) as exc:
        # Never echo arbitrary file/provider contents or authenticated URLs.
        message = str(exc) if isinstance(exc, (SourceError, ValueError)) and not isinstance(exc, json.JSONDecodeError) else type(exc).__name__
        print(json.dumps({"error": message}, ensure_ascii=False), file=sys.stderr)
        return 2
