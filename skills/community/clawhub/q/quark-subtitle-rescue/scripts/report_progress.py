#!/usr/bin/env python3
import json
from pathlib import Path

# Optional env override: QUARK_WORK_DIR=/path/to/quark_subtitle_tool/quark_work
ROOT = Path(__import__('os').environ.get('QUARK_WORK_DIR', 'quark_subtitle_tool/quark_work')).expanduser().resolve()


def load(p):
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}


def main():
    prog = load(ROOT / 'batch_progress.json')
    strict10 = load(ROOT / 'strict_top10_report.json')
    remain = load(ROOT / 'strict_remaining_report.json')
    final2 = load(ROOT / 'final_two_report.json')

    folders = prog.get('folders', {})
    total_videos = 0
    base_ok = 0
    base_fail = 0
    for _, fd in folders.items():
        vids = fd.get('videos', {})
        total_videos += len(vids)
        base_ok += sum(1 for v in vids.values() if v.get('status') == 'ok')
        base_fail += sum(1 for v in vids.values() if v.get('status') == 'fail')

    extra_ok = 0
    extra_ok += strict10.get('ok', 0) if isinstance(strict10.get('ok', 0), int) else 0
    extra_ok += remain.get('ok', 0) if isinstance(remain.get('ok', 0), int) else 0
    extra_ok += final2.get('ok', 0) if isinstance(final2.get('ok', 0), int) else 0

    print('=== Quark Subtitle Rescue Summary ===')
    print(f'Base: ok={base_ok}, fail={base_fail}, total={total_videos}')
    print(f'Extra recovered (strict/final): {extra_ok}')
    print(f'Approx final ok: {base_ok + extra_ok}')


if __name__ == '__main__':
    main()
