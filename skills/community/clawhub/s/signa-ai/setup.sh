#!/bin/bash
# SignaAI skill setup — run on each machine after cloning and after git pull.
#
# What this does:
#   1. Rewrites SKILL.md with this machine's actual home path
#   2. Configures OpenClaw exec approvals for all skill scripts
#   3. Creates and loads the launchd listener daemon
#   4. Creates ~/.openclaw/signaai-worker.json with this machine's passphrase

set -e

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
APPROVALS_FILE="$HOME/.openclaw/exec-approvals.json"
PLIST_FILE="$HOME/Library/LaunchAgents/io.signaai.listener.plist"
LOG_FILE="$HOME/.openclaw/logs/signaai-listener.log"
WORKER_CFG="$HOME/.openclaw/signaai-worker.json"
PLACEHOLDER="/Users/mkfolkerds"

echo "SignaAI Setup"
echo "  Skill dir: $SKILL_DIR"
echo "  Home:      $HOME"
echo ""

# ── 1. Rewrite SKILL.md paths ─────────────────────────────────────────────────

# Generate SKILL.md from template with this machine's actual paths.
# SKILL.md is gitignored — always regenerated here, never committed.
# To update the template: edit SKILL.md.template and push.
cp "$SKILL_DIR/SKILL.md.template" "$SKILL_DIR/SKILL.md"
sed -i '' "s|$PLACEHOLDER|$HOME|g" "$SKILL_DIR/SKILL.md"
echo "✓ SKILL.md generated for $HOME"

# ── 2. Exec approvals ─────────────────────────────────────────────────────────

PYTHON3=$(which python3 2>/dev/null || echo "")
GIT=$(which git 2>/dev/null || echo "")

if [ ! -f "$APPROVALS_FILE" ]; then
    echo "⚠  $APPROVALS_FILE not found — skipping exec approvals (is OpenClaw installed?)"
elif [ -z "$PYTHON3" ]; then
    echo "⚠  python3 not found — skipping exec approvals"
else
    python3 - <<PYEOF
import json, uuid, os

path = "$APPROVALS_FILE"
with open(path) as f:
    data = json.load(f)

data.setdefault("defaults", {})
data["defaults"].update({
    "security": "allowlist",
    "ask": "on-miss",
    "askFallback": "deny",
    "autoAllowSkills": True,
})

data.setdefault("agents", {})
data["agents"].setdefault("main", {})
data["agents"]["main"].update({
    "security": "allowlist",
    "ask": "on-miss",
    "askFallback": "deny",
    "autoAllowSkills": True,
})
data["agents"]["main"].setdefault("allowlist", [])
allowlist = data["agents"]["main"]["allowlist"]

entries = [
    ("$PYTHON3", "python3 $SKILL_DIR/scripts/wallet.py"),
    ("/bin/ls",  "ls $HOME/.openclaw/workspace/skills/"),
]
if "$GIT":
    entries.append(("$GIT", "git -C $SKILL_DIR pull origin main"))

for pattern, cmd in entries:
    if not pattern:
        continue
    if not any(e.get("pattern") == pattern for e in allowlist):
        allowlist.append({
            "id": str(uuid.uuid4()).upper(),
            "pattern": pattern,
            "lastUsedAt": 0,
            "lastUsedCommand": cmd,
            "lastResolvedPath": pattern,
        })

with open(path, "w") as f:
    json.dump(data, f, indent=2)
PYEOF
    echo "✓ Exec approvals configured"
fi

# ── 3. Worker passphrase ──────────────────────────────────────────────────────

echo ""

EXISTING_PASSPHRASE=""
if [ -f "$WORKER_CFG" ]; then
    EXISTING_PASSPHRASE=$(python3 -c \
        "import json; print(json.load(open('$WORKER_CFG')).get('passphrase',''))" 2>/dev/null || echo "")
fi

if [ -t 0 ]; then
    if [ -n "$EXISTING_PASSPHRASE" ]; then
        echo "Worker passphrase already set. Press Enter to keep it, or type a new one:"
    else
        echo "Enter this machine's wallet passphrase (stored in $WORKER_CFG):"
    fi
    echo -n "> "
    read -r INPUT_PASSPHRASE
    PASSPHRASE="${INPUT_PASSPHRASE:-$EXISTING_PASSPHRASE}"
else
    PASSPHRASE="$EXISTING_PASSPHRASE"
fi

if [ -n "$PASSPHRASE" ]; then
    python3 - <<PYEOF
import json, os
path = "$WORKER_CFG"
data = {}
if os.path.exists(path):
    try:
        with open(path) as f:
            data = json.load(f)
    except Exception:
        pass
data["passphrase"] = """$PASSPHRASE"""
data.pop("default_worker", None)
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, "w") as f:
    json.dump(data, f, indent=2)
os.chmod(path, 0o600)
PYEOF
    echo "✓ Worker config saved: $WORKER_CFG"
else
    echo "⚠  No passphrase set — autonomous mode will be disabled until you create $WORKER_CFG"
fi

# ── 4. Launchd daemon ─────────────────────────────────────────────────────────

echo ""

if [ "$(uname)" = "Darwin" ]; then
    mkdir -p "$(dirname "$LOG_FILE")"
    mkdir -p "$(dirname "$PLIST_FILE")"

    cat > "$PLIST_FILE" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>io.signaai.listener</string>
    <key>ProgramArguments</key>
    <array>
        <string>$PYTHON3</string>
        <string>-u</string>
        <string>$SKILL_DIR/scripts/listener.py</string>
        <string>--network</string>
        <string>mainnet</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>ThrottleInterval</key>
    <integer>10</integer>
    <key>StandardOutPath</key>
    <string>$LOG_FILE</string>
    <key>StandardErrorPath</key>
    <string>$LOG_FILE</string>
    <key>WorkingDirectory</key>
    <string>$SKILL_DIR/scripts</string>
</dict>
</plist>
PLIST

    launchctl unload "$PLIST_FILE" 2>/dev/null || true
    launchctl load "$PLIST_FILE"
    echo "✓ Daemon loaded: io.signaai.listener"
    echo "  Log: $LOG_FILE"
else
    echo "  Non-macOS — skipping launchd setup. Run manually:"
    echo "  bash $SKILL_DIR/run.sh"
fi

echo ""
echo "Setup complete. Restart OpenClaw:"
echo "  openclaw gateway restart"
echo ""
echo "Verify daemon is running:"
echo "  launchctl list | grep signaai"
echo "  tail -f $LOG_FILE"
