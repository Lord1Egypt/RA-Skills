#!/usr/bin/env bash
# Download unwatched episodes via Stremio server or standalone torrent client.
# Usage:
#   stremio_download.sh                         # Download all unwatched (interactive)
#   stremio_download.sh --filter "show"         # Only specific show
#   stremio_download.sh --id tt1234567          # By IMDB ID
#   stremio_download.sh --season 2              # Only season 2
#   stremio_download.sh --limit 5               # Max 5 episodes
#   stremio_download.sh --quality 1080p         # Prefer quality (1080p|720p|any)
#   stremio_download.sh --client transmission   # Force torrent client
#   stremio_download.sh --dry-run               # Just show what would be downloaded
#   stremio_download.sh --magnets               # Output magnet links only
# Download priority: Stremio server > auto-detected torrent client > magnet output
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
STREMIO_API="https://api.strem.io/api"
STREMIO_SERVER="http://127.0.0.1:11470"

FILTER_NAME=""
FILTER_ID=""
FILTER_SEASON=""
LIMIT=0
QUALITY="any"
CLIENT=""
DRY_RUN=false
MAGNETS_ONLY=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --filter) FILTER_NAME="$2"; shift 2 ;;
    --id) FILTER_ID="$2"; shift 2 ;;
    --season) FILTER_SEASON="$2"; shift 2 ;;
    --limit) LIMIT="$2"; shift 2 ;;
    --quality) QUALITY="$2"; shift 2 ;;
    --client) CLIENT="$2"; shift 2 ;;
    --dry-run) DRY_RUN=true; shift ;;
    --magnets) MAGNETS_ONLY=true; shift ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

# Detect download method
detect_stremio_server() {
  curl -sf "${STREMIO_SERVER}/settings" &>/dev/null
}

detect_torrent_client() {
  if [[ -n "$CLIENT" ]]; then
    command -v "$CLIENT" &>/dev/null && echo "$CLIENT" && return
    # Try common binary names
    case "$CLIENT" in
      transmission) command -v transmission-remote &>/dev/null && echo "transmission-remote" && return ;;
      aria2) command -v aria2c &>/dev/null && echo "aria2c" && return ;;
      deluge) command -v deluge-console &>/dev/null && echo "deluge-console" && return ;;
      qbittorrent) command -v qbittorrent-nox &>/dev/null && echo "qbittorrent-nox" && return ;;
    esac
    echo "error: torrent client '${CLIENT}' not found" >&2
    return 1
  fi
  # Auto-detect
  for cmd in transmission-remote aria2c deluge-console qbittorrent-nox; do
    if command -v "$cmd" &>/dev/null; then
      echo "$cmd"
      return
    fi
  done
  return 1
}

download_via_stremio() {
  local info_hash="$1" file_idx="${2:-0}"
  curl -sf -X POST "${STREMIO_SERVER}/${info_hash}/create" \
    -H "Content-Type: application/json" \
    -d '{}' &>/dev/null
  echo "  Queued in Stremio (${info_hash:0:12}...)" >&2
}

download_via_client() {
  local client="$1" magnet="$2"
  case "$client" in
    transmission-remote)
      transmission-remote -a "$magnet" 2>/dev/null
      echo "  Added to Transmission" >&2
      ;;
    aria2c)
      aria2c --dir="${DOWNLOAD_DIR:-$HOME/Downloads}" -d "$magnet" &>/dev/null &
      echo "  Started aria2c download" >&2
      ;;
    deluge-console)
      deluge-console "add $magnet" 2>/dev/null
      echo "  Added to Deluge" >&2
      ;;
    qbittorrent-nox)
      # qbittorrent-nox uses web API
      echo "  magnet: ${magnet}" >&2
      echo "  (Add manually to qBittorrent)" >&2
      ;;
    *)
      echo "  magnet: ${magnet}" >&2
      ;;
  esac
}

# Get auth key for addon fetching
AUTH_KEY=$("${SCRIPT_DIR}/stremio_auth.sh" --key) || exit 1

# Get unwatched episodes
unwatched_args=(--json)
[[ -n "$FILTER_NAME" ]] && unwatched_args+=(--filter "$FILTER_NAME")
[[ -n "$FILTER_ID" ]] && unwatched_args+=(--id "$FILTER_ID")
[[ -n "$FILTER_SEASON" ]] && unwatched_args+=(--season "$FILTER_SEASON")

unwatched=$("${SCRIPT_DIR}/stremio_unwatched.sh" "${unwatched_args[@]}")
total=$(echo "$unwatched" | jq 'length')

if [[ "$total" -eq 0 ]]; then
  echo "No unwatched episodes to download" >&2
  exit 0
fi

if [[ "$LIMIT" -gt 0 && "$total" -gt "$LIMIT" ]]; then
  echo "Limiting to ${LIMIT} of ${total} episodes" >&2
  unwatched=$(echo "$unwatched" | jq ".[0:${LIMIT}]")
  total=$LIMIT
fi

# Fetch user's installed addons (for stream resolution)
addons_resp=$(curl -sf -X POST "${STREMIO_API}/addonCollectionGet" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg key "$AUTH_KEY" '{authKey: $key}')" 2>/dev/null)

# Extract addon URLs that provide streams for series
# The API returns {result: {addons: [...]}}
stream_addons=$(echo "$addons_resp" | jq -r '
  [(.result.addons // .result // [])[] |
    select(
      (.manifest.resources // [] | map(if type == "string" then . else .name end) | index("stream")) and
      (.manifest.types // [] | index("series"))
    ) | .transportUrl
  ] | .[]' 2>/dev/null)

if [[ -z "$stream_addons" ]]; then
  echo "warning: no stream addons found, using default sources" >&2
fi

# Determine download method
use_stremio=false
torrent_client=""
if ! $MAGNETS_ONLY; then
  if detect_stremio_server; then
    use_stremio=true
    echo "Download method: Stremio streaming server" >&2
  else
    torrent_client=$(detect_torrent_client 2>/dev/null) || true
    if [[ -n "$torrent_client" ]]; then
      echo "Download method: ${torrent_client}" >&2
    else
      echo "Download method: magnet links (no torrent client found)" >&2
      MAGNETS_ONLY=true
    fi
  fi
fi

# Process each episode
downloaded=0
failed=0

while IFS= read -r ep; do
  show=$(echo "$ep" | jq -r '.show')
  video_id=$(echo "$ep" | jq -r '.video_id')
  season=$(echo "$ep" | jq -r '.season')
  episode_num=$(echo "$ep" | jq -r '.episode')
  title=$(echo "$ep" | jq -r '.title')

  label="${show} S$(printf '%02d' "$season")E$(printf '%02d' "$episode_num")"
  [[ -n "$title" && "$title" != "null" ]] && label="${label}: ${title}"

  echo "---" >&2
  echo "Resolving: ${label}" >&2

  # Query each stream addon
  best_stream=""
  best_hash=""
  best_url=""

  for addon_url in $stream_addons; do
    # Strip manifest.json to get base URL
    addon_base="${addon_url%/manifest.json}"
    addon_base="${addon_base%/}"
    streams=$(curl -sfL "${addon_base}/stream/series/${video_id}.json" 2>/dev/null) || continue
    stream_count=$(echo "$streams" | jq '[.streams // [] | .[]] | length')
    [[ "$stream_count" -eq 0 ]] && continue

    # Score and pick best stream based on quality preference
    selected=$(echo "$streams" | jq --arg q "$QUALITY" '
      [.streams // [] | .[] |
        # Compute quality score from name/description/title
        ((.name // "") + " " + (.description // "") + " " + (.title // "")) as $text |
        (if ($text | test("2160p|4k|4K|UHD"; "i")) then 4
         elif ($text | test("1080p|FHD"; "i")) then 3
         elif ($text | test("720p|HD"; "i")) then 2
         elif ($text | test("480p|SD"; "i")) then 1
         else 0 end) as $score |
        {
          infoHash: (.infoHash // ""),
          fileIdx: (.fileIdx // 0),
          url: (.url // ""),
          externalUrl: (.externalUrl // ""),
          name: (.name // ""),
          description: (.description // ""),
          score: $score
        }
      ]
      | (if $q == "1080p" then sort_by(- (if .score == 3 then 100 else .score end))
         elif $q == "720p" then sort_by(- (if .score == 2 then 100 else .score end))
         else sort_by(-.score) end)
      | first // empty')

    [[ -z "$selected" || "$selected" == "null" ]] && continue

    hash=$(echo "$selected" | jq -r '.infoHash // ""')
    url=$(echo "$selected" | jq -r '.url // ""')
    file_idx=$(echo "$selected" | jq -r '.fileIdx // 0')
    desc=$(echo "$selected" | jq -r '(.name // "") + " " + (.description // "")' | head -c 80)

    if [[ -n "$hash" && "$hash" != "null" ]]; then
      best_hash="$hash"
      best_stream="$desc"
      break
    elif [[ -n "$url" && "$url" != "null" ]]; then
      best_url="$url"
      best_stream="$desc"
      break
    fi
  done

  if [[ -z "$best_hash" && -z "$best_url" ]]; then
    echo "  No streams found" >&2
    ((failed++)) || true
    continue
  fi

  echo "  Stream: ${best_stream}" >&2

  if $DRY_RUN; then
    if [[ -n "$best_hash" ]]; then
      echo "  [dry-run] Would download: magnet:?xt=urn:btih:${best_hash}" >&2
    else
      echo "  [dry-run] Would download: ${best_url}" >&2
    fi
    ((downloaded++)) || true
    continue
  fi

  if $MAGNETS_ONLY; then
    if [[ -n "$best_hash" ]]; then
      echo "magnet:?xt=urn:btih:${best_hash}&dn=$(echo "$label" | sed 's/ /%20/g')"
    else
      echo "$best_url"
    fi
    ((downloaded++)) || true
    continue
  fi

  # Download
  if [[ -n "$best_hash" ]]; then
    if $use_stremio; then
      download_via_stremio "$best_hash" "${file_idx:-0}" && ((downloaded++)) || ((failed++))
    elif [[ -n "$torrent_client" ]]; then
      magnet="magnet:?xt=urn:btih:${best_hash}&dn=$(echo "$label" | sed 's/ /%20/g')"
      download_via_client "$torrent_client" "$magnet" && ((downloaded++)) || ((failed++))
    fi
  elif [[ -n "$best_url" ]]; then
    echo "  Direct URL: ${best_url}" >&2
    echo "  (Direct URL downloads not yet supported, use --magnets)" >&2
    ((failed++)) || true
  fi
done < <(echo "$unwatched" | jq -c '.[]')

echo "===" >&2
echo "Done: ${downloaded} downloaded, ${failed} failed" >&2
