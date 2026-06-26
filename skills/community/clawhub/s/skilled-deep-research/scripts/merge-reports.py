#!/usr/bin/env python3
"""
merge-reports.py — Merge worker results into a deduplicated, ranked final report.

Usage:
  python3 merge-reports.py <slug> [--output /path/to/final-report.md]

Reads from:
  ~/.openclaw/workspace/skills-data/skilled-deep-research/<slug>/workers/*-results.md

Writes to:
  ~/.openclaw/workspace/skills-data/skilled-deep-research/<slug>/report.md
  (and optionally copies to --output)
"""

import os
import sys
import re
import json
import shutil
import argparse
from datetime import datetime
from pathlib import Path

WORKSPACE = os.environ.get("OPENCLAW_WORKSPACE",
            os.path.expanduser("~/.openclaw/workspace"))

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("slug", help="Research run slug")
    p.add_argument("--output", help="Copy final report to this path", default=None)
    p.add_argument("--title", help="Report title override", default=None)
    return p.parse_args()

def load_meta(data_dir):
    meta_path = data_dir / "meta.json"
    if meta_path.exists():
        return json.loads(meta_path.read_text())
    return {}

def load_known_urls(data_dir):
    p = data_dir / "known-urls.txt"
    if not p.exists():
        return set()
    return set(line.strip() for line in p.read_text().splitlines() if line.strip())

def parse_worker_results(results_file):
    """Parse a worker results.md file into a list of source dicts."""
    sources = []
    text = results_file.read_text().replace('\r\n', '\n').replace('\r', '\n')
    # Split on section headers: ### [score/5] [Title](url)
    blocks = re.split(r'\n(?=### )', text)
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        # Primary: ### [5/5] [Title](url) — with or without brackets around score
        header_match = re.match(r'### \[?(\d)\s*/\s*5\]?\s+\[(.+?)\]\((.+?)\)', block)
        if not header_match:
            # Fallback A: ### [5/5] Title — url (no markdown link)
            header_match = re.match(r'### \[?(\d)\s*/\s*5\]?\s+(.+?)(?:\s*[-—]\s*(https?://\S+))?\s*$', block, re.MULTILINE)
        if not header_match:
            # Fallback B: ### Title\n — no score at all
            header_match2 = re.match(r'### (.+?)$', block, re.MULTILINE)
            if header_match2:
                # Try to extract URL from body
                url_match = re.search(r'https?://\S+', block)
                sources.append({
                    "title": header_match2.group(1).strip(),
                    "url": url_match.group(0).rstrip(')') if url_match else "",
                    "quality_score": 2,
                    "raw": block,
                    "worker": results_file.stem.replace("-results", "")
                })
            continue
        title = header_match.group(2).strip()
        url = header_match.group(3).strip() if header_match.group(3) else ""
        sources.append({
            "title": title,
            "url": url,
            "quality_score": int(header_match.group(1)),
            "raw": block,
            "worker": results_file.stem.replace("-results", "")
        })
    return sources

def load_worker_statuses(data_dir):
    statuses = {}
    for pf in (data_dir / "workers").glob("*-progress.json"):
        try:
            d = json.loads(pf.read_text())
            statuses[d.get("worker", pf.stem)] = d
        except Exception:
            pass
    return statuses

def main():
    args = parse_args()
    data_dir = Path(WORKSPACE) / "skills-data" / "skilled-deep-research" / args.slug

    if not data_dir.exists():
        print(f"Error: data directory not found: {data_dir}", file=sys.stderr)
        sys.exit(1)

    meta = load_meta(data_dir)
    known_urls = load_known_urls(data_dir)
    worker_statuses = load_worker_statuses(data_dir)

    # Load all worker results
    all_sources = []
    seen_urls = set()
    workers_dir = data_dir / "workers"

    worker_files = sorted(workers_dir.glob("*-results.md"))
    if not worker_files:
        print("Warning: no worker results files found.", file=sys.stderr)

    for rf in worker_files:
        sources = parse_worker_results(rf)
        for src in sources:
            url = src["url"].strip()
            # Deduplicate by URL
            if url and url in seen_urls:
                continue
            if url:
                seen_urls.add(url)
            all_sources.append(src)

    # Sort by quality score descending
    all_sources.sort(key=lambda s: s["quality_score"], reverse=True)

    # Load retry queue
    retry_path = workers_dir / "retry-queue.md"
    retry_count = 0
    if retry_path.exists():
        retry_count = retry_path.read_text().count("\n- ")

    # Build report
    topic = meta.get("topic", args.slug)
    started = meta.get("started", "unknown")
    title = args.title or topic

    worker_summary = []
    for name, status in worker_statuses.items():
        phase = status.get("phase", "unknown")
        found = status.get("urls_found", "?")
        fetched = status.get("urls_fetched", "?")
        findings = status.get("findings", "?")
        worker_summary.append(f"- **{name}**: {phase} | found {found} | fetched {fetched} | findings {findings}")

    lines = [
        f"# {title}: Deep Research Report",
        f"*Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')} | Run: {args.slug} | Sources: {len(all_sources)} | Workers: {len(worker_files)}*",
        "",
        "## Executive Summary",
        "_[To be filled in by the synthesizing agent or manually]_",
        "",
        f"## Top Sources (Quality Ranked)",
    ]

    for i, src in enumerate(all_sources[:15], 1):
        url_part = f"[{src['title']}]({src['url']})" if src['url'] else src['title']
        lines.append(f"{i}. [{src['quality_score']}/5] {url_part} *(worker: {src['worker']})*")

    lines += ["", "---", "", "## Full Worker Results", ""]

    for rf in worker_files:
        worker_name = rf.stem.replace("-results", "")
        lines.append(f"### Worker: {worker_name}")
        lines.append("")
        lines.append(rf.read_text())
        lines.append("")

    lines += [
        "---",
        "",
        "## Gaps & Limitations",
        "",
    ]

    if retry_count:
        lines.append(f"- **Retry queue:** {retry_count} URLs failed to fetch — see `workers/retry-queue.md`")

    for name, status in worker_statuses.items():
        if status.get("phase") != "complete":
            lines.append(f"- Worker **{name}** did not reach `complete` phase (last: {status.get('phase', 'unknown')})")

    lines += [
        "",
        "## Methodology",
        "",
        f"**Topic:** {topic}",
        f"**Started:** {started}",
        f"**Workers:**",
        *worker_summary,
        f"**Total sources (deduplicated):** {len(all_sources)}",
        f"**Retry queue:** {retry_count} URLs pending",
        "",
    ]

    report_text = "\n".join(lines)

    # Write to data dir
    report_path = data_dir / "report.md"
    report_path.write_text(report_text)
    print(f"Report written: {report_path}")

    # Copy to user-specified output (arg takes priority, then meta.json output_dir)
    output_dest = args.output or meta.get("output_dir") or None
    if output_dest:
        out = Path(output_dest)
        # If it's a directory, write report.md inside it
        if out.is_dir():
            out = out / "report.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(report_path, out)
        print(f"Copied to: {out}")

    # Update meta.json
    meta["status"] = "complete"
    meta["completed"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    meta["sources_total"] = len(all_sources)
    (data_dir / "meta.json").write_text(json.dumps(meta, indent=2))

    print(f"Done. {len(all_sources)} sources, {retry_count} retries pending.")

if __name__ == "__main__":
    main()
