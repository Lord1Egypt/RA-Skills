#!/bin/bash
# Clone or update the Midscene boilerplate from the external repo.
# First run: clones the repo. Subsequent runs: pulls once per day.
# Usage: bash scripts/clone-boilerplate.sh

BOILERPLATE_DIR="$HOME/.midscene/boilerplate"
MARKER="$BOILERPLATE_DIR/.last_updated"

# Fresh clone if directory doesn't exist
if [ ! -d "$BOILERPLATE_DIR" ]; then
  git clone --depth 1 --branch main --filter=blob:none --sparse \
    https://github.com/web-infra-dev/midscene-example.git "$BOILERPLATE_DIR"
  cd "$BOILERPLATE_DIR" || exit 1
  git sparse-checkout set vitest-all-platforms-demo
  date +%s > "$MARKER"
  echo "Boilerplate cloned to $BOILERPLATE_DIR/vitest-all-platforms-demo/"
  exit 0
fi

# Update if last pull was more than 1 day ago
NOW=$(date +%s)
LAST_UPDATED=$(cat "$MARKER" 2>/dev/null || echo 0)
ELAPSED=$(( NOW - LAST_UPDATED ))
ONE_DAY=86400

if [ "$ELAPSED" -ge "$ONE_DAY" ]; then
  echo "Boilerplate outdated (last update >1 day ago), pulling latest..."
  cd "$BOILERPLATE_DIR" && git fetch --depth 1 origin main 2>/dev/null && git pull --ff-only origin main 2>/dev/null || echo "Update failed, using existing boilerplate."
  date +%s > "$MARKER"
else
  echo "Boilerplate is up to date."
fi
