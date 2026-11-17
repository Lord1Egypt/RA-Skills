#!/bin/bash
# Download media without loading local yt-dlp configuration or browser sessions.
set -euo pipefail

usage() {
    cat <<'HELP'
Usage: download.sh [options] URL
  -p, --path PATH      Output directory (default: ~/Downloads/yt-dlp)
  -a, --audio          Extract MP3 audio
  -s, --subs           Download subtitles
  -q, --quality NUM    Maximum video height (positive integer)
  -f, --format ID      yt-dlp format selector
  -l, --list           List formats without creating an output directory
      --playlist      Allow downloading a playlist (default: single video)
  -h, --help           Show help
Only HTTP(S) URLs are accepted. Browser authentication is not supported by this helper.
HELP
}
fail() { printf 'Error: %s\n' "$1" >&2; exit 1; }
require_value() {
    [[ $# -ge 2 && -n "$2" && "$2" != -* ]] || fail "Missing value for $1"
}

DOWNLOAD_PATH="${HOME}/Downloads/yt-dlp"
AUDIO_ONLY=false
DOWNLOAD_SUBS=false
QUALITY=""
FORMAT_ID=""
LIST_FORMATS=false
PLAYLIST=false
URL=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        -p|--path) require_value "$@"; DOWNLOAD_PATH="$2"; shift 2 ;;
        -a|--audio) AUDIO_ONLY=true; shift ;;
        -s|--subs) DOWNLOAD_SUBS=true; shift ;;
        -q|--quality) require_value "$@"; QUALITY="$2"; shift 2 ;;
        -f|--format) require_value "$@"; FORMAT_ID="$2"; shift 2 ;;
        -l|--list) LIST_FORMATS=true; shift ;;
        --playlist) PLAYLIST=true; shift ;;
        -h|--help) usage; exit 0 ;;
        --) shift; [[ $# -eq 1 && -z "$URL" ]] || fail 'Expected one URL'; URL="$1"; shift ;;
        -*) fail "Unknown option: $1" ;;
        *) [[ -z "$URL" ]] || fail 'Expected one URL'; URL="$1"; shift ;;
    esac
done

[[ -n "$URL" ]] || fail 'No URL provided'
[[ "$URL" =~ ^https?://[^/?#[:space:]]+ && ! "$URL" =~ [[:space:][:cntrl:]] ]] || fail 'URL must use HTTP(S) with a nonempty host and no whitespace'
[[ -z "$QUALITY" || "$QUALITY" =~ ^[1-9][0-9]*$ ]] || fail 'Quality must be a positive integer'
[[ -z "$QUALITY" || -z "$FORMAT_ID" ]] || fail 'Choose quality or format, not both'
[[ ! "$DOWNLOAD_PATH" =~ [[:cntrl:]] ]] || fail 'Output path contains control characters'
# Expand only the current-user home prefix; never evaluate path text as shell code.
case "$DOWNLOAD_PATH" in
    '~') DOWNLOAD_PATH="$HOME" ;;
    '~/'*) DOWNLOAD_PATH="$HOME/${DOWNLOAD_PATH:2}" ;;
esac
command -v yt-dlp >/dev/null 2>&1 || fail 'yt-dlp is not installed; install it before running this helper'

CMD=(yt-dlp --ignore-config)
if [[ "$PLAYLIST" == true ]]; then CMD+=(--yes-playlist); else CMD+=(--no-playlist --playlist-end 1); fi
if [[ "$LIST_FORMATS" == true ]]; then
    printf 'Requesting available formats from the supplied URL.\n'
    "${CMD[@]}" -F -- "$URL"
    exit 0
fi

CMD+=(-P "$DOWNLOAD_PATH")
if [[ -n "$FORMAT_ID" ]]; then
    CMD+=(-f "$FORMAT_ID")
elif [[ -n "$QUALITY" ]]; then
    CMD+=(-f "bestvideo[height<=$QUALITY]+bestaudio/best[height<=$QUALITY]")
fi
if [[ "$AUDIO_ONLY" == true ]]; then
    command -v ffmpeg >/dev/null 2>&1 || fail 'ffmpeg is required for MP3 extraction; install it first'
    CMD+=(-x --audio-format mp3)
fi
if [[ "$DOWNLOAD_SUBS" == true ]]; then CMD+=(--write-subs --sub-langs all); fi
CMD+=(-- "$URL")
printf 'Downloading media over the network to: %s\n' "$DOWNLOAD_PATH"
mkdir -p -- "$DOWNLOAD_PATH"
"${CMD[@]}"
printf 'Download complete! Files saved to: %s\n' "$DOWNLOAD_PATH"
