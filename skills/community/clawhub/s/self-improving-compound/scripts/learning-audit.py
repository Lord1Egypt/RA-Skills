#!/usr/bin/env python3
"""Audit recent daily memory/session notes for likely missed self-improvement learnings.

This is intentionally conservative: it reports candidates and optionally logs a compact
summary only when --log is passed. It dedupes via existing learning search.
"""
from __future__ import annotations
import argparse, datetime as dt, json, os, re, subprocess, sys
from pathlib import Path

PATTERNS = [
    ("error", re.compile(r"(?i)\b(error|exception|traceback|failed|failure|报错|失败|异常|修复|blocked|回归|regression)\b")),
    ("correction", re.compile(r"(?i)(Rockway.*(纠正|要求|指出)|用户纠正|correct(ed|ion)?|should have|不要再|以后.*不要|以后.*统一)")),
    ("workaround", re.compile(r"(?i)(workaround|fallback|retry|绕过|临时方案|根因|root cause|prevention|防止|避免重复)")),
]

def run(cmd: list[str]) -> str:
    return subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False).stdout

def asia_today() -> dt.date:
    return (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=8)).date()

def collect_files(root: Path, days: int) -> list[Path]:
    files: list[Path] = []
    mem = root / "memory"
    today = asia_today()
    for i in range(days):
        p = mem / f"{today - dt.timedelta(days=i)}.md"
        if p.exists():
            files.append(p)
    ctx = root.parent / "projects/automations/daily-memory-digest/context"
    if ctx.exists():
        files.extend(sorted(ctx.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)[:days])
    return files

def candidate_lines(path: Path) -> list[tuple[int, str, str]]:
    out = []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return out
    for idx, line in enumerate(lines, 1):
        s = line.strip()
        if not s or len(s) < 8:
            continue
        for kind, rx in PATTERNS:
            if rx.search(s):
                out.append((idx, kind, s[:500]))
                break
    return out

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.environ.get("OPENCLAW_WORKSPACE", os.getcwd()))
    ap.add_argument("--days", type=int, default=2)
    ap.add_argument("--log", action="store_true", help="log audit summary when missed candidates are found")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    root = Path(args.root).expanduser().resolve()
    skill_dir = Path(os.environ.get("SELF_IMPROVING_SKILL_DIR", Path(__file__).resolve().parents[1])).expanduser().resolve()
    skill = Path(os.environ.get("SELF_IMPROVING_LEARNINGS_CLI", skill_dir / "scripts/learnings.py")).expanduser().resolve()
    if not skill.exists():
        raise SystemExit(f"learnings.py not found: {skill}")
    candidates = []
    for path in collect_files(root, args.days):
        for line_no, kind, text in candidate_lines(path):
            # Dedup roughly against SQLite by searching the most specific 80 chars.
            query = re.sub(r"[`*_#\[\](){}]", "", text)[:100]
            found = run([sys.executable, str(skill), "--root", str(root), "search", query, "--limit", "3"])
            if "No results" in found:
                candidates.append({"file": str(path), "line": line_no, "kind": kind, "text": text})
    report = {
        "checked_files": [str(p) for p in collect_files(root, args.days)],
        "missed_candidates": candidates,
        "count": len(candidates),
    }
    out_path = root / "learning/learning-audit.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.log and candidates:
        sample = "; ".join(f"{Path(c['file']).name}:{c['line']} {c['text'][:120]}" for c in candidates[:5])
        subprocess.run([
            sys.executable, str(skill), "--root", str(root), "log-error",
            "--summary", f"Learning audit found {len(candidates)} possible missed capture-gate item(s)",
            "--details", f"Audit candidates: {sample}. Review {out_path} and convert real reusable lessons into specific log-correction/log-error/log-learning entries.",
            "--pattern", "learning:audit-missed-capture",
            "--area", "domain:openclaw",
            "--force",
        ], check=False)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"[learning-audit] checked {len(report['checked_files'])} files; missed_candidates={len(candidates)}; report={out_path}")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
