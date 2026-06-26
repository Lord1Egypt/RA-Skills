#!/usr/bin/env python3
"""Render the LaunchAgent plist with correct $HOME absolute path."""

from pathlib import Path
import os

src = Path(__file__).with_name('com.openclaw.token-ledger-watcher.plist').read_text()
print(src.replace('__HOME__', str(Path.home())))
