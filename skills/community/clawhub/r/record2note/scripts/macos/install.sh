#!/bin/bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
CONFIG="$SKILL_DIR/config.json"
PROCESS_SH="$SKILL_DIR/scripts/macos/process.sh"

echo "=== record2note Install ==="

# Check config exists
if [ ! -f "$CONFIG" ]; then
    echo "Error: config not found at $CONFIG"
    echo "Run the record2note skill setup first."
    exit 1
fi

# Read config
WHISPER_BIN=$(python3 -c "import json; print(json.load(open('$CONFIG')).get('whisper_binary', 'whisper-cli'))")
DIARIZATION=$(python3 -c "import json; print(json.load(open('$CONFIG')).get('diarization', True))")

# Add record2note bin to PATH so deps check finds whisper-cli etc.
RECORD2NOTE_BIN="$HOME/.config/record2note/bin"
if [ -d "$RECORD2NOTE_BIN" ]; then
    export PATH="$RECORD2NOTE_BIN:/opt/local/bin:$PATH"
fi

# Check prerequisites
command -v "$WHISPER_BIN" >/dev/null 2>&1 || { echo "Error: $WHISPER_BIN not found."; echo "Install whisper.cpp or ensure '$WHISPER_BIN' is on PATH"; exit 1; }
command -v fswatch >/dev/null 2>&1 || { echo "Error: fswatch not found. Install: brew install fswatch"; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "Error: python3 not found"; exit 1; }
command -v ffmpeg >/dev/null 2>&1 || { echo "Error: ffmpeg not found. Install: brew install ffmpeg"; exit 1; }
command -v ffprobe >/dev/null 2>&1 || { echo "Error: ffprobe not found. Install: brew install ffmpeg"; exit 1; }

# Check pyannote only if diarization is enabled
if [ "$DIARIZATION" = "True" ] || [ "$DIARIZATION" = "true" ]; then
    python3 -c "import pyannote.audio" 2>/dev/null || {
        echo "Error: pyannote-audio not installed."
        echo "Run: pip install pyannote-audio torch"
        echo "And: huggingface-cli login"
        exit 1
    }
fi

# Set execute permissions
chmod +x "$PROCESS_SH"

# Generate and install launchd plist
echo "Installing launchd agent..."
mkdir -p "$HOME/Library/LaunchAgents"

PLIST_TARGET="$HOME/Library/LaunchAgents/com.user.record2note.plist"

RECORD2NOTE_BIN="$HOME/.config/record2note/bin"

# Detect node/opencode/claude bin directory (nvm, fnm, etc.)
AGENT_PATH=""
for cli in opencode claude; do
    cli_path=$(command -v "$cli" 2>/dev/null) || continue
    AGENT_PATH=$(dirname "$cli_path")
    break
done
if [ -z "$AGENT_PATH" ]; then
    node_path=$(command -v node 2>/dev/null) && AGENT_PATH=$(dirname "$node_path")
fi
AGENT_PATH="${AGENT_PATH:-/usr/local/bin}"

cat > "$PLIST_TARGET" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.record2note</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$PROCESS_SH</string>
        <string>--watch</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/tmp</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>$RECORD2NOTE_BIN:$AGENT_PATH:/usr/local/bin:/opt/homebrew/bin:/opt/local/bin:/usr/bin:/bin</string>
    </dict>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/record2note.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/record2note.err</string>
</dict>
</plist>
EOF

# Unload existing if present
launchctl unload "$PLIST_TARGET" 2>/dev/null || true

# Load launchd agent
if launchctl load "$PLIST_TARGET"; then
    echo "launchd agent loaded."
else
    echo "Warning: launchd agent could not be loaded."
    echo "Try: launchctl load -w $PLIST_TARGET"
fi

echo ""
echo "=== Install complete ==="
echo "Pipeline is now running in the background."
echo "Logs: /tmp/record2note.log"
echo "To test: drop an audio file into your watch directory."
