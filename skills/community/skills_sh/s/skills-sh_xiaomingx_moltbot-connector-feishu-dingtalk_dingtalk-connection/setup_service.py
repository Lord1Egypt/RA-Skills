#!/usr/bin/env python3
"""Generate a macOS launchd plist to keep the DingTalk bridge running."""
from __future__ import annotations

import os
import shutil
from pathlib import Path

HOME = Path.home()
SKILL_DIR = Path(__file__).resolve().parent
BRIDGE_PATH = SKILL_DIR / "bridge.py"
LABEL = "com.clawdbot.dingtalk-bridge"

UV_PATH = shutil.which("uv") or "uv"

env_vars = {
    "HOME": str(HOME),
    "PATH": "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin",
    "DINGTALK_PORT": os.getenv("DINGTALK_PORT", "3210"),
    "DINGTALK_PATH": os.getenv("DINGTALK_PATH", "/dingtalk"),
}

optional_vars = [
    "DINGTALK_SIGNING_SECRET",
    "DINGTALK_BOT_ID",
    "DINGTALK_BOT_NAME",
    "DINGTALK_THINKING_THRESHOLD_MS",
    "CLAWDBOT_CONFIG_PATH",
    "CLAWDBOT_AGENT_ID",
]

for key in optional_vars:
    if os.getenv(key):
        env_vars[key] = os.getenv(key, "")

env_block = "\n".join([f"      <key>{k}</key>\n      <string>{v}</string>" for k, v in env_vars.items()])

plist = f"""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<!DOCTYPE plist PUBLIC \"-//Apple//DTD PLIST 1.0//EN\" \"http://www.apple.com/DTDs/PropertyList-1.0.dtd\">
<plist version=\"1.0\">
  <dict>
    <key>Label</key>
    <string>{LABEL}</string>

    <key>ProgramArguments</key>
    <array>
      <string>{UV_PATH}</string>
      <string>run</string>
      <string>python</string>
      <string>{BRIDGE_PATH}</string>
    </array>

    <key>WorkingDirectory</key>
    <string>{SKILL_DIR}</string>

    <key>RunAtLoad</key>
    <true/>

    <key>KeepAlive</key>
    <true/>

    <key>EnvironmentVariables</key>
    <dict>
{env_block}
    </dict>

    <key>StandardOutPath</key>
    <string>{HOME}/.clawdbot/logs/dingtalk-bridge.out.log</string>
    <key>StandardErrorPath</key>
    <string>{HOME}/.clawdbot/logs/dingtalk-bridge.err.log</string>
  </dict>
</plist>
"""

(HOME / ".clawdbot/logs").mkdir(parents=True, exist_ok=True)

out_path = HOME / "Library/LaunchAgents" / f"{LABEL}.plist"
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(plist, encoding="utf-8")

print(f"Wrote: {out_path}")
print("\nTo start the service:")
print(f"  launchctl load {out_path}")
print("\nTo stop:")
print(f"  launchctl unload {out_path}")
