#!/usr/bin/env bash
# Launch Spotify detached from the current process tree.
# Usage: ./launch_spotify.sh
set -euo pipefail

# Discover Xauthority from running Xwayland or Xorg
XAUTHORITY=$(ps aux | grep -E 'Xwayland|Xorg' | grep -v grep | grep -oP '\-auth \S+' | head -1 | cut -d' ' -f2)

if [ -z "$XAUTHORITY" ]; then
  echo "ERROR: Could not find X11/Wayland auth file" >&2
  exit 1
fi

export DISPLAY=:0
export XAUTHORITY

# Already running?
if dbus-send --session --dest=org.freedesktop.DBus --type=method_call --print-reply \
  /org/freedesktop/DBus org.freedesktop.DBus.ListNames 2>/dev/null | grep -q spotify; then
  echo "Spotify is already running (DBus registered)"
  exit 0
fi

echo "Launching Spotify..."
setsid -f spotify >/dev/null 2>&1

# Wait for DBus registration
for i in $(seq 1 15); do
  sleep 1
  if dbus-send --session --dest=org.freedesktop.DBus --type=method_call --print-reply \
    /org/freedesktop/DBus org.freedesktop.DBus.ListNames 2>/dev/null | grep -q spotify; then
    echo "Spotify ready (took ${i}s)"
    exit 0
  fi
done

echo "WARNING: Spotify process running but DBus not registered after 15s" >&2
exit 1
