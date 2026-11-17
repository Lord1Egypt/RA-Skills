#!/usr/bin/env python3
"""Render the LaunchAgent plist with absolute home and installed script paths."""

from pathlib import Path

script_dir = Path(__file__).resolve().parent
src = script_dir.joinpath('com.openclaw.token-ledger-watcher.plist').read_text()
print(
    src.replace('__HOME__', str(Path.home()))
       .replace('__LEDGER_WATCHER__', str(script_dir / 'ledger_watcher.py'))
)
