#!/bin/bash
# Job: crystal-capture
# Continuous capture for Claude Code sessions.
# Reads JSONL files on disk, ingests into Crystal, exports MD sessions, writes daily logs.
# Primary capture path. Runs every minute via cron.
# The Stop hook (cc-hook.ts) is a redundancy check only.
#
# Source of truth: memory-crystal-private/scripts/crystal-capture.sh
# Deployed to: ~/.ldm/bin/crystal-capture.sh (via crystal init)
# Cron entry: * * * * * ~/.ldm/bin/crystal-capture.sh >> /tmp/ldm-dev-tools/crystal-capture.log 2>&1
#
# The Node poller fetches the OpenAI API key internally via opRead() in core.ts.
# opRead uses: op read "op://Agent Secrets/OpenAI API/api key" with the SA token from
# ~/.openclaw/secrets/op-sa-token. Do NOT call op from this shell script... it triggers
# macOS TCC popups when run from cron.

# Cron provides minimal PATH. Ensure Homebrew binaries (node, op) are findable.
export PATH="/opt/homebrew/bin:$PATH"

POLLER="$HOME/.ldm/extensions/memory-crystal/dist/cc-poller.js"
NODE="/opt/homebrew/bin/node"

if [ ! -f "$POLLER" ]; then
  echo "ERROR: cc-poller not found at $POLLER"
  exit 1
fi

# Single run: scan all sessions, ingest new turns, export MD, exit.
$NODE "$POLLER" 2>&1
