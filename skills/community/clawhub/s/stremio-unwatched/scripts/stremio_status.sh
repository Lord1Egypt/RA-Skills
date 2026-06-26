#!/usr/bin/env bash
# Check download progress for active Stremio/torrent downloads.
# Usage:
#   stremio_status.sh                     # Show all active downloads
#   stremio_status.sh --hash <infoHash>   # Status of specific torrent
#   stremio_status.sh --json              # JSON output
#   stremio_status.sh --watch             # Refresh every 5s
set -euo pipefail

STREMIO_SERVER="http://127.0.0.1:11470"

INFO_HASH=""
JSON_OUTPUT=false
WATCH=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --hash) INFO_HASH="$2"; shift 2 ;;
    --json) JSON_OUTPUT=true; shift ;;
    --watch) WATCH=true; shift ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

format_bytes() {
  local bytes=$1
  if (( bytes >= 1073741824 )); then
    echo "$(echo "scale=1; $bytes / 1073741824" | bc)G"
  elif (( bytes >= 1048576 )); then
    echo "$(echo "scale=1; $bytes / 1048576" | bc)M"
  elif (( bytes >= 1024 )); then
    echo "$(echo "scale=1; $bytes / 1024" | bc)K"
  else
    echo "${bytes}B"
  fi
}

check_stremio_server() {
  curl -sf "${STREMIO_SERVER}/settings" &>/dev/null
}

get_torrent_status() {
  local hash="$1" file_idx="${2:-0}"
  curl -sf "${STREMIO_SERVER}/${hash}/${file_idx}/stats.json" 2>/dev/null
}

show_status() {
  if ! check_stremio_server; then
    echo "Stremio streaming server not running on ${STREMIO_SERVER}" >&2

    # Try to show torrent client status
    if command -v transmission-remote &>/dev/null; then
      echo "--- Transmission ---" >&2
      transmission-remote -l 2>/dev/null || echo "Could not connect to Transmission" >&2
      return
    fi
    if command -v aria2c &>/dev/null; then
      echo "--- aria2 ---" >&2
      echo "(aria2 status requires aria2c RPC; check manually)" >&2
      return
    fi

    echo "No download status available" >&2
    return 1
  fi

  if [[ -n "$INFO_HASH" ]]; then
    stats=$(get_torrent_status "$INFO_HASH")
    if [[ -z "$stats" ]]; then
      echo "No stats for hash: ${INFO_HASH}" >&2
      return 1
    fi
    if $JSON_OUTPUT; then
      echo "$stats"
    else
      name=$(echo "$stats" | jq -r '.streamName // .name // "unknown"')
      progress=$(echo "$stats" | jq -r '.streamProgress // 0')
      progress_pct=$(echo "scale=1; $progress * 100" | bc)
      dl_speed=$(echo "$stats" | jq -r '.downloadSpeed // 0' | cut -d. -f1)
      ul_speed=$(echo "$stats" | jq -r '.uploadSpeed // 0' | cut -d. -f1)
      peers=$(echo "$stats" | jq -r '.peers // 0')
      downloaded=$(echo "$stats" | jq -r '.downloaded // 0')

      printf "%-50s\n" "$name"
      printf "  Progress: %s%%  Downloaded: %s  Peers: %s\n" \
        "$progress_pct" "$(format_bytes "$downloaded")" "$peers"
      printf "  DL: %s/s  UL: %s/s\n" \
        "$(format_bytes "$dl_speed")" "$(format_bytes "$ul_speed")"
    fi
  else
    echo "Stremio server is running" >&2
    echo "Use --hash <infoHash> to check specific torrent status" >&2
    # Show server info
    settings=$(curl -sf "${STREMIO_SERVER}/settings" 2>/dev/null)
    if [[ -n "$settings" ]]; then
      version=$(echo "$settings" | jq -r '.values.serverVersion // "unknown"')
      cache_size=$(echo "$settings" | jq -r '.values.cacheSize // 0')
      echo "  Server version: ${version}" >&2
      echo "  Cache size: $(format_bytes "$cache_size")" >&2
    fi
  fi
}

if $WATCH; then
  while true; do
    clear
    echo "=== Stremio Download Status ($(date +%H:%M:%S)) ==="
    show_status || true
    sleep 5
  done
else
  show_status
fi
