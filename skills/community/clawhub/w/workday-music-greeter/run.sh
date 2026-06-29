#!/usr/bin/env bash
#
# workday-music-greeter — switch a home-music scene for the current weekday
# slot, fetch a matching GIF, and send a greeting email that embeds + attaches
# that GIF.
#
# Usage:
#   run.sh <scene>            # do it for real
#   run.sh <scene> --dry-run  # print every action, touch nothing external
#   run.sh auto               # pick scene from current time using scenes.conf
#   run.sh auto --dry-run
#
# Scenes are defined in scenes.conf (scene|hour-start|gif-query|subject).
#
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONF="$SKILL_DIR/scenes.conf"
GIF_OUT_DIR="${WMG_GIF_DIR:-/tmp/workday-music-greeter}"
DRY_RUN=0

log()  { printf '\033[36m[wmg]\033[0m %s\n' "$*"; }
warn() { printf '\033[33m[wmg]\033[0m %s\n' "$*" >&2; }
die()  { printf '\033[31m[wmg]\033[0m %s\n' "$*" >&2; exit 1; }

scene_greeting() {
  case "$1" in
    morning) echo "Good morning! Coffee's brewing and the playlist is easing us in. Have a steady, focused start." ;;
    chill)   echo "Midday check-in — time to breathe. Chill tunes are on; grab water and reset for the afternoon." ;;
    focus)   echo "Afternoon focus block is live. Calm background music, notifications down, let's get the deep work done." ;;
    off)     echo "That's a wrap on the workday. Music's off — log out, stretch, and enjoy the evening. Well done today." ;;
    party)   echo "Celebration mode! Cranking it up across the house. Enjoy the moment." ;;
    *)       echo "Here's your scene update for today." ;;
  esac
}

run() {
  if [[ "$DRY_RUN" == "1" ]]; then
    printf '\033[90m[dry-run]\033[0m %s\n' "$*"
  else
    eval "$@"
  fi
}

# ----- arg parsing -------------------------------------------------------------
SCENE="${1:-}"; [[ -n "$SCENE" ]] || die "usage: run.sh <scene|auto> [--dry-run]"
shift || true
for a in "$@"; do
  case "$a" in
    --dry-run) DRY_RUN=1 ;;
    *) warn "ignoring unknown arg: $a" ;;
  esac
done

[[ -f "$CONF" ]] || die "missing config: $CONF"

# ----- resolve scene from time when asked --------------------------------------
pick_scene_by_time() {
  local now_h cur best_scene="" best_hour=-1 scene hour _q _s
  now_h=$(date +%H); now_h=$((10#$now_h))
  while IFS='|' read -r scene hour _q _s; do
    [[ "$scene" =~ ^#.*$ || -z "$scene" ]] && continue
    hour=$((10#$hour))
    if (( now_h >= hour && hour > best_hour )); then
      best_hour=$hour; best_scene=$scene
    fi
  done < "$CONF"
  [[ -n "$best_scene" ]] || best_scene="off"
  echo "$best_scene"
}

if [[ "$SCENE" == "auto" ]]; then
  SCENE=$(pick_scene_by_time)
  log "auto-selected scene for $(date +%H:%M): $SCENE"
fi

# ----- weekday gate ------------------------------------------------------------
DOW=$(date +%u)   # 1=Mon .. 7=Sun
if (( DOW >= 6 )); then
  log "today is a weekend (dow=$DOW); weekday automation skipped."
  exit 0
fi

# ----- look up scene row -------------------------------------------------------
ROW=$(grep -E "^${SCENE}\|" "$CONF" || true)
[[ -n "$ROW" ]] || die "scene '$SCENE' not found in $CONF"
IFS='|' read -r _scene _hour GIF_QUERY SUBJECT <<< "$ROW"

log "scene=$SCENE  gif-query=\"$GIF_QUERY\"  subject=\"$SUBJECT\""

# ----- 1) switch the music scene ----------------------------------------------
HOME_MUSIC_BIN="$(command -v home-music || echo "$HOME/clawd/skills/home-music/home-music.sh")"
if [[ "$DRY_RUN" != "1" && ! -x "$HOME_MUSIC_BIN" ]]; then
  warn "home-music not executable at '$HOME_MUSIC_BIN' (macOS-only); skipping live scene switch."
else
  log "switching music scene -> $SCENE"
  run "\"$HOME_MUSIC_BIN\" \"$SCENE\""
fi

# ----- 2) fetch a matching GIF -------------------------------------------------
mkdir -p "$GIF_OUT_DIR"
GIF_URL=""
GIF_FILE=""
if command -v gifgrep >/dev/null 2>&1; then
  if [[ "$DRY_RUN" == "1" ]]; then
    log "would run: gifgrep \"$GIF_QUERY\" --download --max 1 --format url"
    GIF_URL="https://media.tenor.com/example-${SCENE}.gif"
  else
    GIF_URL="$(gifgrep "$GIF_QUERY" --format url 2>/dev/null | head -n1 || true)"
    gifgrep "$GIF_QUERY" --download --max 1 --format url >/dev/null 2>&1 || true
    GIF_FILE="$(ls -t /workspace/gifs/*.gif "$GIF_OUT_DIR"/*.gif 2>/dev/null | head -n1 || true)"
  fi
else
  warn "gifgrep not installed; email will go out without a GIF."
fi
[[ -n "$GIF_URL" ]] && log "gif url: $GIF_URL"
[[ -n "$GIF_FILE" ]] && log "gif file: $GIF_FILE"

# ----- 3) build + send greeting email -----------------------------------------
: "${WMG_MAIL_TO:?set WMG_MAIL_TO (recipient) — see .env.example}"
SMTP_SCRIPT="${WMG_SMTP_SCRIPT:-$SKILL_DIR/../imap-smtp-email/scripts/smtp.js}"

HTML_FILE="$(mktemp "${GIF_OUT_DIR}/greeting.XXXXXX.html")"
GREETING="$(scene_greeting "$SCENE")"
cat > "$HTML_FILE" <<HTML
<div style="font-family:-apple-system,Segoe UI,Roboto,sans-serif;max-width:520px">
  <h2 style="margin:0 0 8px">$SUBJECT</h2>
  <p style="font-size:15px;color:#333">$GREETING</p>
  ${GIF_URL:+<p><img src="$GIF_URL" alt="$SCENE gif" style="max-width:100%;border-radius:12px"/></p>}
  <p style="font-size:12px;color:#999">Sent automatically by workday-music-greeter · scene <b>$SCENE</b></p>
</div>
HTML

ATTACH_ARG=""
[[ -n "$GIF_FILE" ]] && ATTACH_ARG="--attach \"$GIF_FILE\""

if [[ "$DRY_RUN" != "1" && ! -f "$SMTP_SCRIPT" ]]; then
  warn "smtp script not found at $SMTP_SCRIPT; cannot send email."
else
  log "sending greeting email -> $WMG_MAIL_TO"
  run "node \"$SMTP_SCRIPT\" send --to \"$WMG_MAIL_TO\" --subject \"$SUBJECT\" --html-file \"$HTML_FILE\" $ATTACH_ARG"
fi

log "done (scene=$SCENE dry_run=$DRY_RUN)"
