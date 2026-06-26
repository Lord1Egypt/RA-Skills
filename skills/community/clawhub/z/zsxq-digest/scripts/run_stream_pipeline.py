#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parent
COLLECT_SESSION = ROOT / "collect_from_session.py"
COLLECT_BROWSER = ROOT / "collect_from_browser.py"
DEDUPE = ROOT / "dedupe_and_state.py"
ENRICH = ROOT / "enrich_stream_items.py"
RENDER = ROOT / "render_stream_digest.py"


class PipelineError(Exception):
    pass


def run_json(cmd: List[str]) -> dict:
    proc = subprocess.run(cmd, text=True, capture_output=True)
    if proc.returncode != 0:
        try:
            payload = json.loads(proc.stdout)
            raise PipelineError(json.dumps(payload, ensure_ascii=False))
        except Exception:
            raise PipelineError(proc.stderr.strip() or proc.stdout.strip() or f"command failed: {' '.join(cmd)}")
    try:
        return json.loads(proc.stdout)
    except Exception as e:
        raise PipelineError(f"failed to parse JSON output from {' '.join(cmd)}: {e}")


def run_text(cmd: List[str]) -> str:
    proc = subprocess.run(cmd, text=True, capture_output=True)
    if proc.returncode != 0:
        raise PipelineError(proc.stderr.strip() or proc.stdout.strip() or f"command failed: {' '.join(cmd)}")
    return proc.stdout


def path_or_temp(value: str, td: str, name: str) -> str:
    return value or os.path.join(td, name)


def main():
    parser = argparse.ArgumentParser(description="Run collect -> dedupe -> enrich -> render for zsxq stream digest")
    parser.add_argument("--source", choices=["token", "browser-file"], required=True)
    parser.add_argument("--token-file")
    parser.add_argument("--group-id", action="append", default=[])
    parser.add_argument("--exclude-group-id", action="append", default=[])
    parser.add_argument("--groups-file")
    parser.add_argument("--browser-input")
    parser.add_argument("--default-circle", default="未分类星球")
    parser.add_argument("--cursor", required=True)
    parser.add_argument("--scope", default="all")
    parser.add_argument("--count", type=int, default=20)
    parser.add_argument("--api-base", default="https://api.zsxq.com")
    parser.add_argument("--ttl-days", type=int, default=7)
    parser.add_argument("--max-entries", type=int, default=500)
    parser.add_argument("--full-per-circle", type=int, default=3)
    parser.add_argument("--full-max-chars", type=int, default=800)
    parser.add_argument("--compact-max-items", type=int, default=0)
    parser.add_argument("--min-full-score", type=int, default=0)
    parser.add_argument("--weight-overrides-file")
    parser.add_argument("--scope-label", default="最近可见更新（非严格今日）")
    parser.add_argument("--private-news-list-mode", action="store_true")
    parser.add_argument("--collected-output")
    parser.add_argument("--new-items-output")
    parser.add_argument("--enriched-output")
    parser.add_argument("--digest-output")
    parser.add_argument("--print-digest", action="store_true")
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as td:
        collected_output = path_or_temp(args.collected_output, td, "collected.json")
        new_items_output = path_or_temp(args.new_items_output, td, "new_items.json")
        enriched_output = path_or_temp(args.enriched_output, td, "stream_enriched.json")
        digest_output = args.digest_output

        if args.source == "token":
            if not args.token_file:
                raise SystemExit("--token-file is required when --source=token")
            collect_cmd = [
                sys.executable,
                str(COLLECT_SESSION),
                "--token-file", args.token_file,
                "--output", collected_output,
                "--count", str(args.count),
                "--scope", args.scope,
                "--api-base", args.api_base,
            ]
            if args.group_id or args.groups_file:
                collect_cmd += ["--mode", "multi-group-topics"]
                for group_id in args.group_id:
                    collect_cmd += ["--group-id", group_id]
                for group_id in args.exclude_group_id:
                    collect_cmd += ["--exclude-group-id", group_id]
                if args.groups_file:
                    collect_cmd += ["--groups-file", args.groups_file]
            else:
                collect_cmd += ["--mode", "groups"]
        else:
            if not args.browser_input:
                raise SystemExit("--browser-input is required when --source=browser-file")
            collect_cmd = [
                sys.executable,
                str(COLLECT_BROWSER),
                args.browser_input,
                "--default-circle", args.default_circle,
                "--output", collected_output,
            ]

        collected = run_json(collect_cmd)
        dedupe = run_json([
            sys.executable,
            str(DEDUPE),
            collected_output,
            "--cursor", args.cursor,
            "--ttl-days", str(args.ttl_days),
            "--max-entries", str(args.max_entries),
            "--access-mode", collected.get("access_mode", args.source),
            "--write-new-items", new_items_output,
        ])
        enrich_cmd = [
            sys.executable,
            str(ENRICH),
            new_items_output,
            "--output", enriched_output,
            "--full-per-circle", str(args.full_per_circle),
            "--full-max-chars", str(args.full_max_chars),
            "--min-full-score", str(args.min_full_score),
        ]
        if args.weight_overrides_file:
            enrich_cmd += ["--weight-overrides-file", args.weight_overrides_file]
        enriched = run_json(enrich_cmd)

        render_cmd = [
            sys.executable,
            str(RENDER),
            enriched_output,
            "--scope-label", args.scope_label,
            "--full-max-chars", str(args.full_max_chars),
        ]
        if args.compact_max_items:
            render_cmd += ["--compact-max-items", str(args.compact_max_items)]
        if args.private_news_list_mode:
            render_cmd += ["--private-news-list-mode"]
        digest_text = run_text(render_cmd)

        if digest_output:
            Path(digest_output).parent.mkdir(parents=True, exist_ok=True)
            Path(digest_output).write_text(digest_text, encoding="utf-8")

        summary = {
            "status": "ok",
            "source": args.source,
            "collected_status": collected.get("status"),
            "collected_count": collected.get("count"),
            "skipped_groups_count": collected.get("skipped_count", 0),
            "new_count": dedupe.get("new_count"),
            "enriched_count": enriched.get("count"),
            "full_blocks_count": ((enriched.get("stats") or {}).get("full_blocks_count")),
            "compact_items_count": ((enriched.get("stats") or {}).get("compact_items_count")),
            "pipeline_message": ((enriched.get("stats") or {}).get("pipeline_message")),
            "collected_output": collected_output,
            "new_items_output": new_items_output,
            "enriched_output": enriched_output,
            "digest_output": digest_output,
        }
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        if args.print_digest:
            print("\n=== STREAM DIGEST ===\n")
            print(digest_text)


if __name__ == "__main__":
    main()
