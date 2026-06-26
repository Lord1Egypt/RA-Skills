#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shlex
import subprocess
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser(description='Retry Slack thread export using a failed-channels file from a previous run')
    ap.add_argument('--target-id', required=True)
    ap.add_argument('--user-id', required=True)
    ap.add_argument('--team-id', required=True)
    ap.add_argument('--failed-channels-file', required=True)
    ap.add_argument('--out-csv', required=True)
    ap.add_argument('--out-jsonl', required=True)
    ap.add_argument('--summary-json')
    ap.add_argument('--after')
    ap.add_argument('--before')
    ap.add_argument('--max-pages', type=int, default=60)
    ap.add_argument('--sleep-seconds', type=float, default=0.5)
    ap.add_argument('--mode', choices=['strict','raw','heuristic'], default='heuristic')
    ap.add_argument('--resume-from-jsonl')
    ap.add_argument('--failed-channels-out')
    ap.add_argument('--keyword', action='append', default=[])
    ap.add_argument('--channel-hint', action='append', default=[])
    ap.add_argument('--dry-run', action='store_true', help='Print the generated retry command without running it')
    args = ap.parse_args()

    failed_path = Path(args.failed_channels_file)
    if not failed_path.exists():
        raise SystemExit(f'Failed channels file not found: {failed_path}')
    channels = [line.strip() for line in failed_path.read_text(encoding='utf-8').splitlines() if line.strip() and not line.strip().startswith('#')]
    if not channels:
        raise SystemExit('Failed channels file is empty; nothing to retry.')

    export_script = Path(__file__).with_name('export_slack_threads.py')
    cmd = [
        sys.executable, str(export_script),
        '--target-id', args.target_id,
        '--user-id', args.user_id,
        '--team-id', args.team_id,
        '--channel-file', str(failed_path),
        '--out-csv', args.out_csv,
        '--out-jsonl', args.out_jsonl,
        '--mode', args.mode,
        '--max-pages', str(args.max_pages),
        '--sleep-seconds', str(args.sleep_seconds),
    ]
    if args.summary_json:
        cmd += ['--summary-json', args.summary_json]
    if args.after:
        cmd += ['--after', args.after]
    if args.before:
        cmd += ['--before', args.before]
    if args.resume_from_jsonl:
        cmd += ['--resume-from-jsonl', args.resume_from_jsonl]
    if args.failed_channels_out:
        cmd += ['--failed-channels-out', args.failed_channels_out]
    for kw in args.keyword:
        cmd += ['--keyword', kw]
    for hint in args.channel_hint:
        cmd += ['--channel-hint', hint]

    rendered = ' '.join(shlex.quote(x) for x in cmd)
    if args.dry_run:
        print(rendered)
        return 0

    print(rendered)
    raise SystemExit(subprocess.run(cmd).returncode)


if __name__ == '__main__':
    raise SystemExit(main())
