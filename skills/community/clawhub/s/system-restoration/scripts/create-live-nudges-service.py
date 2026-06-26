#!/usr/bin/env python3
"""
Generate LaunchD service for Live Nudges
Creates com.ranger.live-nudges.plist
"""

import os
from pathlib import Path

PLIST_CONTENT = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ranger.live-nudges</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Library/Frameworks/Python.framework/Versions/3.12/bin/python3</string>
        <string>/Users/stephendobbins/.config/ranger/scripts/pulse_os_full.py</string>
        <string>nudges</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/stephendobbins/.config/ranger/scripts</string>
    <key>StartInterval</key>
    <integer>900</integer>
    <key>StandardOutPath</key>
    <string>/tmp/live_nudges.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/live_nudges.err</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
    </dict>
</dict>
</plist>'''

def create_service():
    """Create LaunchD service plist for live nudges"""
    launch_agents_dir = Path.home() / "Library" / "LaunchAgents"
    launch_agents_dir.mkdir(exist_ok=True)
    
    plist_file = launch_agents_dir / "com.ranger.live-nudges.plist"
    
    with open(plist_file, 'w') as f:
        f.write(PLIST_CONTENT)
    
    print(f"✅ Created {plist_file}")
    print("\nTo activate:")
    print(f"launchctl load {plist_file}")
    print("launchctl start com.ranger.live-nudges")

if __name__ == "__main__":
    create_service()