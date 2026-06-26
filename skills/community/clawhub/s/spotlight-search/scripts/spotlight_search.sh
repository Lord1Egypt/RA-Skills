#!/bin/bash
#
# Hybrid file search: tries Spotlight (mdfind) first, falls back to find.
# Safe version: avoids eval and passes user input as arguments.
#
# Usage: spotlight_search.sh [options] <query>
#
# Options:
#   -t, --type <kind>      Filter by kind (pdf, image, application, video, audio, text)
#   -d, --dir <directory>  Search only within directory (default: current directory)
#   -l, --limit <N>        Limit results to N (default: 20)
#   -f, --fallback-only    Skip Spotlight, use only fallback search
#   -v, --verbose          Show detailed output
#   -h, --help             Show this help

set -euo pipefail

TYPE=""
DIR="."
LIMIT=20
FALLBACK_ONLY=false
VERBOSE=false
QUERY=""

usage() {
  cat <<EOF
Usage: $0 [options] <query>

Hybrid file search: tries Spotlight (mdfind) first, falls back to find.

Options:
  -t, --type <kind>      Filter by kind (pdf, image, application, video, audio, text)
  -d, --dir <directory>  Search only within directory (default: current directory)
  -l, --limit <N>        Limit results to N (default: 20)
  -f, --fallback-only    Skip Spotlight, use only fallback search
  -v, --verbose          Show detailed output
  -h, --help             Show this help

Examples:
  $0 "invoice"
  $0 -t pdf "report"
  $0 -d ~/Documents "meeting"
EOF
}

log() {
  if $VERBOSE; then
    echo "[INFO] $*" >&2
  fi
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -t|--type)
      [[ $# -ge 2 ]] || { echo "Error: Missing value for $1" >&2; exit 1; }
      TYPE="$2"
      shift 2
      ;;
    -d|--dir)
      [[ $# -ge 2 ]] || { echo "Error: Missing value for $1" >&2; exit 1; }
      DIR="$2"
      shift 2
      ;;
    -l|--limit)
      [[ $# -ge 2 ]] || { echo "Error: Missing value for $1" >&2; exit 1; }
      LIMIT="$2"
      shift 2
      ;;
    -f|--fallback-only)
      FALLBACK_ONLY=true
      shift
      ;;
    -v|--verbose)
      VERBOSE=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      if [[ $# -gt 0 ]]; then
        QUERY="$1"
        shift
      fi
      break
      ;;
    -*)
      echo "Error: Unknown option $1" >&2
      exit 1
      ;;
    *)
      if [[ -z "$QUERY" ]]; then
        QUERY="$1"
      else
        echo "Error: Multiple query arguments not supported" >&2
        exit 1
      fi
      shift
      ;;
  esac
done

if [[ -z "$QUERY" ]]; then
  echo "Error: Query argument required" >&2
  exit 1
fi

if [[ ! "$LIMIT" =~ ^[0-9]+$ ]] || [[ "$LIMIT" -lt 1 ]]; then
  echo "Error: Limit must be a positive integer" >&2
  exit 1
fi

if [[ ! -d "$DIR" ]]; then
  echo "Error: Directory '$DIR' does not exist" >&2
  exit 1
fi

DIR="$(cd "$DIR" && pwd)"

fallback_search() {
  local q="$1"
  local dir="$2"
  local limit="$3"
  local kind="$4"

  log "Starting fallback search with find..."

  local -a cmd=(find "$dir")

  case "$kind" in
    application)
      cmd+=( -type d )
      ;;
    "")
      cmd+=( -type f )
      ;;
    *)
      cmd+=( -type f )
      ;;
  esac

  case "$kind" in
    pdf)
      cmd+=( -iname "*.pdf" )
      ;;
    image)
      cmd+=( \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.gif" -o -iname "*.bmp" -o -iname "*.tiff" -o -iname "*.webp" \) )
      ;;
    application)
      cmd+=( -iname "*.app" )
      ;;
    video)
      cmd+=( \( -iname "*.mp4" -o -iname "*.mov" -o -iname "*.avi" -o -iname "*.mkv" -o -iname "*.webm" \) )
      ;;
    audio)
      cmd+=( \( -iname "*.mp3" -o -iname "*.m4a" -o -iname "*.wav" -o -iname "*.flac" -o -iname "*.aac" \) )
      ;;
    text)
      cmd+=( \( -iname "*.txt" -o -iname "*.md" -o -iname "*.json" -o -iname "*.yml" -o -iname "*.yaml" -o -iname "*.xml" -o -iname "*.csv" \) )
      ;;
    "")
      ;;
    *)
      echo "Error: Unsupported type '$kind'" >&2
      exit 1
      ;;
  esac

  cmd+=( -iname "*${q}*" )

  log "Running fallback search safely with argument array"
  "${cmd[@]}" 2>/dev/null | head -n "$limit"
}

spotlight_search() {
  local q="$1"
  local dir="$2"
  local limit="$3"
  local kind="$4"

  log "Starting Spotlight search..."

  local -a cmd=(mdfind)
  if [[ "$dir" != "$HOME" ]]; then
    cmd+=( -onlyin "$dir" )
  fi

  local full_query="$q"
  if [[ -n "$kind" ]]; then
    if [[ -n "$full_query" ]]; then
      full_query="kind:$kind ${full_query}"
    else
      full_query="kind:$kind"
    fi
  fi

  log "Running Spotlight search safely with argument array"
  "${cmd[@]}" "$full_query" 2>/dev/null | head -n "$limit"
}

RESULTS=""
if ! $FALLBACK_ONLY; then
  log "Attempting Spotlight search..."
  RESULTS="$(spotlight_search "$QUERY" "$DIR" "$LIMIT" "$TYPE")"
  if [[ -n "$RESULTS" ]]; then
    printf '%s\n' "$RESULTS"
    log "Spotlight search successful."
    exit 0
  fi
  log "Spotlight returned no results."
fi

log "Using fallback search..."
RESULTS="$(fallback_search "$QUERY" "$DIR" "$LIMIT" "$TYPE")"
if [[ -n "$RESULTS" ]]; then
  printf '%s\n' "$RESULTS"
  log "Fallback search successful."
else
  log "No results found."
  exit 1
fi
