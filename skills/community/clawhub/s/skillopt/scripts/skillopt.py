#!/usr/bin/env python3
"""Small local harness for SkillOpt-style skill optimization."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import shlex
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCORER_TYPES = {"exact", "contains", "regex", "command", "manual"}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def fail(message: str, code: int = 1) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(code)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for lineno, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                fail(f"{path}:{lineno}: invalid JSON: {exc}")
            if not isinstance(value, dict):
                fail(f"{path}:{lineno}: task must be a JSON object")
            value["_line"] = lineno
            tasks.append(value)
    return tasks


def validate_task(task: dict[str, Any], seen: set[str], source: Path) -> None:
    lineno = task.get("_line", "?")
    task_id = task.get("id")
    if not isinstance(task_id, str) or not task_id.strip():
        fail(f"{source}:{lineno}: missing string id")
    if task_id in seen:
        fail(f"{source}:{lineno}: duplicate id {task_id!r}")
    seen.add(task_id)
    if not isinstance(task.get("prompt"), str) or not task["prompt"].strip():
        fail(f"{source}:{lineno}: missing string prompt")
    scorer = task.get("scorer")
    if not isinstance(scorer, dict):
        fail(f"{source}:{lineno}: missing scorer object")
    scorer_type = scorer.get("type")
    if scorer_type not in SCORER_TYPES:
        fail(f"{source}:{lineno}: scorer.type must be one of {sorted(SCORER_TYPES)}")
    if scorer_type == "exact" and "expected" not in scorer:
        fail(f"{source}:{lineno}: exact scorer requires expected")
    if scorer_type == "contains" and "expected" not in scorer:
        fail(f"{source}:{lineno}: contains scorer requires expected")
    if scorer_type == "regex" and "pattern" not in scorer:
        fail(f"{source}:{lineno}: regex scorer requires pattern")
    if scorer_type == "command" and "command" not in scorer:
        fail(f"{source}:{lineno}: command scorer requires command")


def cmd_validate_tasks(args: argparse.Namespace) -> None:
    path = Path(args.tasks)
    tasks = read_jsonl(path)
    seen: set[str] = set()
    for task in tasks:
        validate_task(task, seen, path)
    print(json.dumps({"path": str(path), "tasks": len(tasks), "ok": True}, indent=2))


def normalize_text(value: str) -> str:
    return " ".join(value.strip().split())


def safe_filename(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("_") or "task"


def quote(value: Any) -> str:
    return shlex.quote(str(value))


def format_template(template: str, values: dict[str, Any]) -> str:
    rendered = template
    for key, value in values.items():
        rendered = rendered.replace("{" + key + "}", quote(value))
    return rendered


def score_output(
    task: dict[str, Any],
    output: str,
    output_path: Path,
    skill_path: Path,
) -> tuple[float | None, dict[str, Any]]:
    scorer = task["scorer"]
    scorer_type = scorer["type"]
    if scorer_type == "manual":
        return None, {"type": "manual", "rubric": scorer.get("rubric")}

    if scorer_type == "exact":
        expected = str(scorer["expected"])
        passed = normalize_text(output) == normalize_text(expected)
        return (1.0 if passed else 0.0), {"type": "exact", "passed": passed}

    if scorer_type == "contains":
        expected = scorer["expected"]
        values = expected if isinstance(expected, list) else [expected]
        missing = [str(item) for item in values if str(item) not in output]
        passed = not missing
        return (1.0 if passed else 0.0), {
            "type": "contains",
            "passed": passed,
            "missing": missing,
        }

    if scorer_type == "regex":
        pattern = str(scorer["pattern"])
        passed = re.search(pattern, output, flags=re.MULTILINE) is not None
        return (1.0 if passed else 0.0), {"type": "regex", "passed": passed}

    if scorer_type == "command":
        expected = scorer.get("expected", "")
        command = format_template(
            str(scorer["command"]),
            {
                "output_path": output_path,
                "expected": expected,
                "task_id": task["id"],
                "skill_path": skill_path,
            },
        )
        proc = subprocess.run(
            command,
            shell=True,
            cwd=scorer.get("cwd"),
            text=True,
            capture_output=True,
        )
        passed = proc.returncode == 0
        return (1.0 if passed else 0.0), {
            "type": "command",
            "command": command,
            "passed": passed,
            "exit_code": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }

    fail(f"unknown scorer type {scorer_type!r}")


def write_summary(out_dir: Path) -> dict[str, Any]:
    records = []
    for path in sorted(out_dir.glob("*.json")):
        if path.name == "summary.json":
            continue
        with path.open("r", encoding="utf-8") as handle:
            records.append(json.load(handle))
    summary = summarize_records(records)
    summary["path"] = str(out_dir)
    with (out_dir / "summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, ensure_ascii=False)
    return summary


def summarize_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    scored = [record for record in records if isinstance(record.get("score"), (int, float))]
    scores = [float(record["score"]) for record in scored]
    pass_count = sum(1 for score in scores if score >= 1.0)
    return {
        "created_at": now_iso(),
        "tasks": len(records),
        "scored_tasks": len(scored),
        "unscored_tasks": len(records) - len(scored),
        "avg_score": (sum(scores) / len(scores)) if scores else None,
        "pass_rate": (pass_count / len(scores)) if scores else None,
    }


def cmd_run(args: argparse.Namespace) -> None:
    tasks_path = Path(args.tasks)
    skill_path = Path(args.skill)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    tasks = read_jsonl(tasks_path)
    seen: set[str] = set()
    for task in tasks:
        validate_task(task, seen, tasks_path)

    for task in tasks:
        task_id = task["id"]
        base = safe_filename(task_id)
        text_path = out_dir / f"{base}.txt"
        json_path = out_dir / f"{base}.json"
        command = format_template(
            args.agent_command,
            {
                "skill_path": skill_path,
                "prompt": task["prompt"],
                "task_id": task_id,
                "output_path": text_path,
            },
        )
        proc = subprocess.run(
            command,
            shell=True,
            cwd=args.cwd,
            text=True,
            capture_output=True,
            timeout=args.timeout,
        )
        output = proc.stdout
        if text_path.exists() and text_path.stat().st_size > 0:
            output = text_path.read_text(encoding="utf-8", errors="replace")
        else:
            text_path.write_text(output, encoding="utf-8")
        score, scorer_result = score_output(task, output, text_path, skill_path)
        record = {
            "task": {k: v for k, v in task.items() if k != "_line"},
            "task_id": task_id,
            "created_at": now_iso(),
            "skill_path": str(skill_path),
            "command": command,
            "exit_code": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "output_path": str(text_path),
            "score": score,
            "passed": (score is not None and score >= 1.0),
            "scorer_result": scorer_result,
        }
        with json_path.open("w", encoding="utf-8") as handle:
            json.dump(record, handle, indent=2, ensure_ascii=False)
        print(f"{task_id}: score={score} exit={proc.returncode}")

    summary = write_summary(out_dir)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def cmd_init(args: argparse.Namespace) -> None:
    skill = Path(args.skill)
    out = Path(args.out)
    if not skill.exists():
        fail(f"skill not found: {skill}")
    (out / "candidates").mkdir(parents=True, exist_ok=True)
    (out / "tasks").mkdir(parents=True, exist_ok=True)
    (out / "rollouts" / "train").mkdir(parents=True, exist_ok=True)
    (out / "rollouts" / "val").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(skill, out / "source_skill.md")
    shutil.copyfile(skill, out / "candidates" / "candidate_000.md")
    for split in ("train", "val"):
        task_path = out / "tasks" / f"{split}.jsonl"
        if not task_path.exists():
            task_path.write_text("", encoding="utf-8")
    rejected = out / "rejected_edits.md"
    if not rejected.exists():
        rejected.write_text("# Rejected Edits\n\n", encoding="utf-8")
    print(json.dumps({"run_dir": str(out), "source_skill": str(out / "source_skill.md")}, indent=2))


def load_rollout_dir(path: Path) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for item in sorted(path.glob("*.json")):
        if item.name == "summary.json":
            continue
        with item.open("r", encoding="utf-8") as handle:
            record = json.load(handle)
        records[record["task_id"]] = record
    return records


def avg_score(records: dict[str, dict[str, Any]]) -> float | None:
    scores = [float(r["score"]) for r in records.values() if isinstance(r.get("score"), (int, float))]
    return (sum(scores) / len(scores)) if scores else None


def cmd_gate(args: argparse.Namespace) -> None:
    baseline = load_rollout_dir(Path(args.baseline))
    candidate = load_rollout_dir(Path(args.candidate))
    baseline_avg = avg_score(baseline)
    candidate_avg = avg_score(candidate)
    if baseline_avg is None or candidate_avg is None:
        fail("baseline and candidate must both have scored tasks")
    regressions = []
    for task_id, base_record in baseline.items():
        cand_record = candidate.get(task_id)
        if not cand_record:
            regressions.append({"task_id": task_id, "reason": "missing candidate rollout"})
            continue
        base_score = base_record.get("score")
        cand_score = cand_record.get("score")
        if isinstance(base_score, (int, float)) and isinstance(cand_score, (int, float)):
            if base_score >= 1.0 and cand_score < 1.0:
                regressions.append(
                    {"task_id": task_id, "baseline": base_score, "candidate": cand_score}
                )
    delta = candidate_avg - baseline_avg
    accepted = delta >= args.min_delta and (not regressions or args.allow_regression)
    result = {
        "accepted": accepted,
        "baseline_avg": baseline_avg,
        "candidate_avg": candidate_avg,
        "delta": delta,
        "min_delta": args.min_delta,
        "regressions": regressions,
    }
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if accepted else 2)


def cmd_record_score(args: argparse.Namespace) -> None:
    path = Path(args.rollout)
    with path.open("r", encoding="utf-8") as handle:
        record = json.load(handle)
    record["score"] = args.score
    record["passed"] = args.score >= 1.0
    record["manual_note"] = args.note
    record["manual_scored_at"] = now_iso()
    with path.open("w", encoding="utf-8") as handle:
        json.dump(record, handle, indent=2, ensure_ascii=False)
    write_summary(path.parent)
    print(json.dumps({"updated": str(path), "score": args.score}, indent=2))


def cmd_report(args: argparse.Namespace) -> None:
    baseline = load_rollout_dir(Path(args.baseline))
    candidate = load_rollout_dir(Path(args.candidate))
    baseline_summary = summarize_records(list(baseline.values()))
    candidate_summary = summarize_records(list(candidate.values()))
    lines = [
        f"# {args.title}",
        "",
        "## Summary",
        "",
        "| Split | Tasks | Scored | Avg score | Pass rate |",
        "| --- | ---: | ---: | ---: | ---: |",
        format_summary_row("Baseline", baseline_summary),
        format_summary_row("Candidate", candidate_summary),
        "",
        "## Regressions",
        "",
    ]
    regressions = []
    for task_id, base_record in baseline.items():
        cand_record = candidate.get(task_id)
        if not cand_record:
            regressions.append(f"- `{task_id}` missing in candidate")
            continue
        base_score = base_record.get("score")
        cand_score = cand_record.get("score")
        if isinstance(base_score, (int, float)) and isinstance(cand_score, (int, float)):
            if base_score >= 1.0 and cand_score < 1.0:
                regressions.append(f"- `{task_id}` regressed from {base_score} to {cand_score}")
    lines.extend(regressions or ["None recorded."])
    lines.extend(["", "## Notes", "", args.notes or "Add accepted/rejected edit rationale here."])
    Path(args.out).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"report": args.out}, indent=2))


def format_summary_row(label: str, summary: dict[str, Any]) -> str:
    avg = summary["avg_score"]
    pass_rate = summary["pass_rate"]
    avg_text = "" if avg is None else f"{avg:.3f}"
    pass_text = "" if pass_rate is None else f"{pass_rate:.3f}"
    return (
        f"| {label} | {summary['tasks']} | {summary['scored_tasks']} | "
        f"{avg_text} | {pass_text} |"
    )


def cmd_export(args: argparse.Namespace) -> None:
    source = Path(args.candidate)
    dest = Path(args.out)
    if not source.exists():
        fail(f"candidate not found: {source}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, dest)
    print(json.dumps({"exported": str(dest), "source": str(source)}, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create a SkillOpt run directory")
    init.add_argument("--skill", required=True, help="Path to source SKILL.md")
    init.add_argument("--out", required=True, help="Run directory to create")
    init.set_defaults(func=cmd_init)

    validate = sub.add_parser("validate-tasks", help="Validate a task JSONL file")
    validate.add_argument("tasks")
    validate.set_defaults(func=cmd_validate_tasks)

    run = sub.add_parser("run", help="Run tasks through an arbitrary agent command")
    run.add_argument("--tasks", required=True)
    run.add_argument("--skill", required=True)
    run.add_argument("--out", required=True)
    run.add_argument("--agent-command", required=True)
    run.add_argument("--cwd", default=None)
    run.add_argument("--timeout", type=int, default=300)
    run.set_defaults(func=cmd_run)

    gate = sub.add_parser("gate", help="Compare baseline and candidate rollout dirs")
    gate.add_argument("--baseline", required=True)
    gate.add_argument("--candidate", required=True)
    gate.add_argument("--min-delta", type=float, default=0.02)
    gate.add_argument(
        "--allow-regression",
        action="store_true",
        help="Accept even if previously passing validation tasks regress",
    )
    gate.set_defaults(func=cmd_gate)

    record = sub.add_parser("record-score", help="Record a manual score in a rollout JSON")
    record.add_argument("rollout")
    record.add_argument("--score", required=True, type=float)
    record.add_argument("--note", default="")
    record.set_defaults(func=cmd_record_score)

    report = sub.add_parser("report", help="Write a compact Markdown optimization report")
    report.add_argument("--baseline", required=True)
    report.add_argument("--candidate", required=True)
    report.add_argument("--out", required=True)
    report.add_argument("--title", default="SkillOpt Report")
    report.add_argument("--notes", default="")
    report.set_defaults(func=cmd_report)

    export = sub.add_parser("export", help="Copy an accepted candidate to best_skill.md")
    export.add_argument("--candidate", required=True)
    export.add_argument("--out", required=True)
    export.set_defaults(func=cmd_export)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
