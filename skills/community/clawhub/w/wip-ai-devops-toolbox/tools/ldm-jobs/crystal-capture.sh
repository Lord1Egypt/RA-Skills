#!/bin/bash
# Job: crystal-capture
#
# SOURCE OF TRUTH: memory-crystal-private/scripts/crystal-capture.sh
# This copy is for LDM Dev Tools.app manual runs only.
# The cron job runs from ~/.ldm/bin/crystal-capture.sh (installed via crystal init).
# Memory Crystal does not depend on this app.
#
# If updating: update the source in memory-crystal-private first, then copy here.

POLLER="$HOME/.ldm/extensions/memory-crystal/dist/cc-poller.js"
NODE="/opt/homebrew/bin/node"

if [ ! -f "$POLLER" ]; then
  echo "ERROR: cc-poller not found at $POLLER"
  exit 1
fi

$NODE "$POLLER" 2>&1
