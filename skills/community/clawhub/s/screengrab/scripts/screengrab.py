#!/usr/bin/env python3
"""
screengrab - Quick macOS display snapshot for AI agents
Captures the current screen without a browser. Saves to file or /tmp.

Commands:
  snap              Capture all displays to /tmp/screengrab-TIMESTAMP.png
  snap --display N  Capture specific display (0=main, 1=second, etc.)
  snap --out PATH   Save to custom path
  snap --open       Open in Preview after capture
  list              List connected displays
  watch --interval  Periodic screenshots (saves timestamped files)
"""

import sys
import os
import subprocess
import argparse
import time
from datetime import datetime
from pathlib import Path


def run(cmd, timeout=10):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, shell=isinstance(cmd, str))
        return r.stdout.strip(), r.returncode
    except Exception as e:
        return str(e), 1


def list_displays():
    """List connected displays using system_profiler."""
    out, _ = run(['system_profiler', 'SPDisplaysDataType'])
    displays = []
    current = {}
    for line in out.splitlines():
        line = line.strip()
        if line.endswith(':') and not line.startswith(' '):
            if current:
                displays.append(current)
            current = {'name': line.rstrip(':')}
        elif 'Resolution:' in line:
            current['resolution'] = line.split('Resolution:')[-1].strip()
        elif 'Main Display:' in line:
            current['main'] = 'Yes' in line
    if current:
        displays.append(current)

    # Filter to actual display entries
    displays = [d for d in displays if 'resolution' in d]

    print(f"📺 Connected displays: {len(displays)}")
    for i, d in enumerate(displays):
        main = ' (main)' if d.get('main') else ''
        res = d.get('resolution', 'unknown')
        name = d.get('name', f'Display {i}')
        print(f"  [{i}] {name}{main} — {res}")

    return displays


def snap(display=None, out_path=None, open_after=False, quiet=False):
    """Take a screenshot."""
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')

    if out_path:
        path = Path(out_path)
    else:
        path = Path(f'/tmp/screengrab-{ts}.png')

    # Build screencapture command
    cmd = ['/usr/sbin/screencapture', '-x']  # -x = no sound

    if display is not None:
        cmd += ['-D', str(display + 1)]  # screencapture uses 1-indexed displays

    if open_after:
        cmd.append('-P')  # open in Preview

    cmd.append(str(path))

    out, code = run(cmd, timeout=15)

    if code != 0:
        print(f"❌ Failed: {out}")
        sys.exit(1)

    if not path.exists():
        print(f"❌ Screenshot file not created at {path}")
        sys.exit(1)

    size_kb = path.stat().st_size // 1024

    if not quiet:
        display_str = f" (display {display})" if display is not None else ""
        print(f"📸 Saved{display_str}: {path}  ({size_kb} KB)")

    return str(path)


def watch(interval=30, display=None, out_dir='/tmp', count=None):
    """Periodic screenshot capture."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"👁  Watch mode — every {interval}s → {out_dir}  (Ctrl+C to stop)")
    i = 0
    try:
        while count is None or i < count:
            ts = datetime.now().strftime('%Y%m%d-%H%M%S')
            path = out_dir / f'screengrab-{ts}.png'
            snap(display=display, out_path=str(path), quiet=True)
            print(f"  [{datetime.now().strftime('%H:%M:%S')}] → {path.name}")
            i += 1
            if count is None or i < count:
                time.sleep(interval)
    except KeyboardInterrupt:
        print(f"\nStopped. {i} screenshots saved to {out_dir}")


def main():
    parser = argparse.ArgumentParser(description='screengrab — quick macOS display snapshot')
    subparsers = parser.add_subparsers(dest='command')

    snap_p = subparsers.add_parser('snap', help='Take a screenshot')
    snap_p.add_argument('--display', '-d', type=int, default=None, help='Display index (0=main)')
    snap_p.add_argument('--out', '-o', default=None, help='Output path')
    snap_p.add_argument('--open', action='store_true', help='Open in Preview')
    snap_p.add_argument('--quiet', '-q', action='store_true')

    subparsers.add_parser('list', help='List connected displays')

    watch_p = subparsers.add_parser('watch', help='Periodic screenshots')
    watch_p.add_argument('--interval', type=int, default=30)
    watch_p.add_argument('--display', '-d', type=int, default=None)
    watch_p.add_argument('--out-dir', default='/tmp')
    watch_p.add_argument('--count', type=int, default=None)

    args = parser.parse_args()

    if args.command == 'snap' or args.command is None:
        display = getattr(args, 'display', None)
        out = getattr(args, 'out', None)
        open_after = getattr(args, 'open', False)
        quiet = getattr(args, 'quiet', False)
        path = snap(display=display, out_path=out, open_after=open_after, quiet=quiet)
        if quiet:
            print(path)
    elif args.command == 'list':
        list_displays()
    elif args.command == 'watch':
        watch(interval=args.interval, display=args.display, out_dir=args.out_dir, count=args.count)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
