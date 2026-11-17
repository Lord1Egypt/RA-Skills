#!/usr/bin/env bash
# set-download-dir.sh — choose where scraped CSVs are saved (persistent).
#
# Usage:  bash set-download-dir.sh [<dir>]
#   bash set-download-dir.sh                    # use the OS default Downloads dir
#   bash set-download-dir.sh "D:/tiktok-data"   # use a custom directory
#
# Reads:  state.json (none needed — state_get may return a previously saved dir)
# Writes: state.json (download_dir)
# Stdout: {"ok":true,"dir":"/c/Users/admin/Downloads","source":"default"}
# Exit:   0 = saved, 1 = could not create the directory
#
# Call this after asking the user where CSV files should go. The choice
# persists, so it is asked at most once per machine.
set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
. "$SCRIPT_DIR/lib.sh"

SOURCE="default"
if [ $# -ge 1 ] && [ -n "${1:-}" ]; then
  WANT="$1"; SOURCE="custom"
else
  WANT="$(detect_download_dir)"
fi

# expand a leading ~ and make relative paths absolute
case "$WANT" in "~"*) WANT="$HOME${WANT#\~}" ;; esac
case "$WANT" in
  /*|[A-Za-z]:[\\/]*) : ;;                     # absolute (posix or windows drive)
  *) WANT="$(pwd)/$WANT" ;;                    # relative → absolute
esac

if ! mkdir -p "$WANT" 2>/dev/null || [ ! -d "$WANT" ]; then
  printf '{"ok":false,"error":"cannot create directory: %s"}\n' "$WANT"
  exit 1
fi

state_set download_dir "$WANT"
printf '{"ok":true,"dir":"%s","source":"%s"}\n' "$WANT" "$SOURCE"