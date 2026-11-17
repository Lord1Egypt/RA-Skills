#!/usr/bin/env bash
# lib.sh — shared helpers for MonsterGet skill scripts.
# Source this file from other scripts; it only defines functions/variables, runs nothing.
#
# Configuration via environment (all optional):
#   MONSTERGET_BASE_URL   API host           (default https://monsterget.com)
#   MONSTERGET_SITE_URL   page host          (default = BASE_URL)
#   MONSTERGET_STATE_DIR  state directory    (default ~/.monsterget)
#   MONSTERGET_STATE_FILE state file         (default $STATE_DIR/state.json)
#   MONSTERGET_POLLS      login-check polls  (default 12 × 5s)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
STATE_DIR="${MONSTERGET_STATE_DIR:-$HOME/.monsterget}"
STATE_FILE="${MONSTERGET_STATE_FILE:-$STATE_DIR/state.json}"
BASE_URL="${MONSTERGET_BASE_URL:-https://monsterget.com}"
SITE_URL="${MONSTERGET_SITE_URL:-$BASE_URL}"
POLLS="${MONSTERGET_POLLS:-12}"

# ---------------------------------------------------------------------------
# OS detection — windows | macos | linux | unknown
# ---------------------------------------------------------------------------
detect_os() {
  case "$(uname -s 2>/dev/null)" in
    MINGW*|MSYS*|CYGWIN*) echo "windows" ;;
    Darwin*)              echo "macos"   ;;
    Linux*)               echo "linux"   ;;
    *)                    echo "unknown" ;;
  esac
}

# ---------------------------------------------------------------------------
# State persistence — tiny JSON key/value store (string values only)
# ---------------------------------------------------------------------------
state_init() {
  mkdir -p "$STATE_DIR" 2>/dev/null
  [ -f "$STATE_FILE" ] || printf '{}' > "$STATE_FILE"
}

# state_get <key>  → prints the value (or nothing if missing)
state_get() {
  state_init
  grep -o "\"$1\":\"[^\"]*\"" "$STATE_FILE" 2>/dev/null | head -n1 | sed "s/\"$1\":\"//; s/\"$//"
}

# state_set <key> <value>  → upsert a string value, keeps other keys intact.
# The state file is single-line JSON, so grep -v (line-based) would delete the whole
# line when the key exists — use awk for a true in-place key replacement instead.
#
# v1.2.1 fix — awk sub() replacement treats unescaped & as "matched text",
# causing exponential corruption when values contain & (e.g. scrape URLs:
# "...?auto=1&agentTaskId=..."). Using match() + substr() string concatenation
# avoids any replacement-string semantics. Value passed via ENVIRON rather than
# -v to avoid -v expanding backslash escapes.
state_set() {
  local key="$1" value="${2//\"/\\\"}"
  state_init
  MGS_K="$key" MGS_V="$value" awk '
    BEGIN { k=ENVIRON["MGS_K"]; v=ENVIRON["MGS_V"] }
    {
      if (match($0, "\"" k "\":\"[^\"]*\"")) {
        $0 = substr($0, 1, RSTART-1) "\"" k "\":\"" v "\"" substr($0, RSTART+RLENGTH)
      } else if ($0 ~ /^\{[[:space:]]*\}$/) {
        $0 = "{\"" k "\":\"" v "\"}"
      } else if (match($0, /\}[[:space:]]*$/)) {
        $0 = substr($0, 1, RSTART-1) ",\"" k "\":\"" v "\"" substr($0, RSTART)
      }
      print
    }' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
}

# ---------------------------------------------------------------------------
# Browser selection — pure manual flow (no disk detection).
# The user manually confirms which browser has the MonsterGet extension
# installed (SKILL.md). We only read the saved `browser_pref` from state and
# look up that browser's launch paths:
#   BROWSER         the chosen one (edge|chrome|none)
#   BROWSER_EXE     process/exe name for the chosen one
#   BROWSER_FULLPATH absolute path to the chosen one's binary (may be empty)
#   CHOSEN_BY       preference (always, in pure manual flow)
#
# ARCHIVED: `_probe_browser` (disk scan for the extension) is kept below as
# reference only — the AI must never call it, and it always returns 1.
# ---------------------------------------------------------------------------
BROWSER="none"; BROWSER_EXE=""; BROWSER_FULLPATH=""; BROWSERS=""; CHOSEN_BY="none"

# _browser_conf <name> → "<user_data_dir>|<full_binary_path>|<exe_name>"
# First field is the browser's USER DATA dir (Default profile inside) —
# historically used by the archived `_probe_browser` for extension scanning.
# In pure manual flow we only use the path fields to launch the browser.
_browser_conf() {
  case "$(detect_os):$1" in
    windows:edge)
      printf '%s|%s|%s' \
        "$HOME/AppData/Local/Microsoft/Edge/User Data" \
        "/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" "msedge" ;;
    windows:chrome)
      printf '%s|%s|%s' \
        "$HOME/AppData/Local/Google/Chrome/User Data" \
        "/c/Program Files/Google/Chrome/Application/chrome.exe" "chrome" ;;
    macos:edge)
      printf '%s|%s|%s' \
        "$HOME/Library/Application Support/Microsoft Edge" \
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" "Microsoft Edge" ;;
    macos:chrome)
      printf '%s|%s|%s' \
        "$HOME/Library/Application Support/Google/Chrome" \
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" "Google Chrome" ;;
    linux:edge)
      printf '%s|%s|%s' \
        "$HOME/.config/microsoft-edge" "" "microsoft-edge" ;;
    linux:chrome)
      printf '%s|%s|%s' \
        "$HOME/.config/google-chrome" "" "google-chrome" ;;
    *) return 1 ;;
  esac
}

# _probe_browser <name> → 0 if that browser has the MonsterGet extension
# ══════════════════════════════════════════════════════════════════════
# ARCHIVED — pure manual flow. The AI never scans the disk for the extension;
# the user confirms manually which browser they installed it in (SKILL.md).
# Kept only as reference; always returns 1 (nothing detected).
# --------------------------------------------------------------------------
# OLD DISK SCAN (reference only — do not re-enable):
#   Covers BOTH install types (they land in different places on disk):
#   ① Preferences manifest snapshot — Chrome/Edge embed the extension manifest
#      (incl. "name") inside Default/Preferences (and Edge's Secure Preferences),
#      for store-installed AND load-unpacked alike. Match the escaped form
#      \"name\": \"MonsterGet so a download-path hit cannot false-positive.
#   ② Physical Extensions/<id>/manifest.json — store-installed only; fallback
#      in case the Preferences snapshot is not flushed yet.
_probe_browser() {
  # local udir pref m
  # udir="$(_browser_conf "$1" | cut -d'|' -f1)"
  # [ -n "$udir" ] || return 1
  #
  # # ① manifest name snapshot in Preferences / Secure Preferences (Default profile)
  # for pref in "$udir/Default/Preferences" "$udir/Default/Secure Preferences"; do
  #   [ -f "$pref" ] && grep -aqE '\\"name\\": ?\\"MonsterGet' "$pref" 2>/dev/null && return 0
  # done
  #
  # # ② physical folder (store-installed fallback)
  # for m in "$udir/Default/Extensions/"*/*/manifest.json; do
  #   [ -f "$m" ] && grep -q 'MonsterGet' "$m" 2>/dev/null && return 0
  # done
  #
  # return 1
  return 1
}

# _select_browser <name> → point the globals at that browser
_select_browser() {
  local conf
  conf="$(_browser_conf "$1")" || return 1
  BROWSER="$1"
  BROWSER_FULLPATH="$(printf '%s' "$conf" | cut -d'|' -f2)"
  BROWSER_EXE="$(printf '%s' "$conf" | cut -d'|' -f3)"
}

# detect_browser — select the user's saved browser preference.
# ═══════════════════════════════════════════════════════════════
# Pure manual flow: no disk scan, no extension probe. The user
# has manually confirmed which browser has the extension installed
# (see SKILL.md Step I-II). We just read browser_pref from state
# and look up the hardcoded paths for that browser.
detect_browser() {
  BROWSER="none"; BROWSER_EXE=""; BROWSER_FULLPATH=""; BROWSERS=""; CHOSEN_BY="none"
  local pref
  pref="$(state_get browser_pref)"
  if [ -n "$pref" ] && _select_browser "$pref" 2>/dev/null; then
    CHOSEN_BY="preference"
    BROWSERS="$pref"
    return 0
  fi
  return 1
}

# browser_choices_json — the detected browsers as a JSON array literal
# ARCHIVED — pure manual flow never builds a multi-browser list.
# Kept for backward compatibility; always returns [BROWSERS] (one element).
browser_choices_json() {
  # local n out=""
  # for n in $BROWSERS; do
  #   [ -n "$out" ] && out="$out,"
  #   out="$out\"$n\""
  # done
  # printf '[%s]' "$out"
  printf '["%s"]' "$BROWSERS"
}

# ---------------------------------------------------------------------------
# Browser launch & process verification
# ---------------------------------------------------------------------------
# _focus_browser — raise the extension browser's window to the foreground (Windows).
# A URL opened from a background shell lands in the EXISTING window without raising
# it, so the user — often in another app (an AI client) — never sees the page, and
# the scraper popup it later triggers stays hidden too. Raising the browser here is
# what makes the whole flow visible: page opens → browser in front → popup on top.
#
# A .ps1 sibling does the heavy lifting: AttachThreadInput + SetForegroundWindow
# bypasses Windows' foreground-lock (AppActivate silently fails when this script runs
# as a background child of an AI client — see focus-browser.ps1).
_focus_browser() {
  [ "$(detect_os)" = "windows" ] || return 0
  [ -z "$BROWSER_EXE" ] && return 0
  command -v powershell >/dev/null 2>&1 || return 0
  local script_dir
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  powershell -NoProfile -File "$script_dir/focus-browser.ps1" -ExeName "$BROWSER_EXE" >/dev/null 2>&1
  return 0
}

# open_url <url> — open in the EXTENSION browser, not the system default, and bring
# that browser to the foreground (see _focus_browser).
# Windows: `cmd /c start` would open the DEFAULT browser — never use it first,
# or a URL meant for the extension browser ends up in the wrong one.
open_url() {
  local url="$1" opened=1
  case "$(detect_os)" in
    windows)
      if [ -n "$BROWSER_FULLPATH" ] && [ -f "$BROWSER_FULLPATH" ]; then
        "$BROWSER_FULLPATH" "$url" >/dev/null 2>&1 && opened=0
      fi
      if [ "$opened" != 0 ] && [ -n "$BROWSER_EXE" ] && command -v "$BROWSER_EXE" >/dev/null 2>&1; then
        "$BROWSER_EXE" "$url" >/dev/null 2>&1 && opened=0
      fi
      if [ "$opened" != 0 ] && command -v cmd >/dev/null 2>&1; then
        MSYS_NO_PATHCONV=1 cmd /c start "" "$url" >/dev/null 2>&1 && opened=0
      fi
      [ "$opened" = 0 ] && _focus_browser
      return "$opened"
      ;;
    macos)
      [ -n "$BROWSER_FULLPATH" ] && [ -f "$BROWSER_FULLPATH" ] && "$BROWSER_FULLPATH" "$url" >/dev/null 2>&1 && return 0
      open "$url" >/dev/null 2>&1 && return 0
      return 1
      ;;
    linux)
      [ -n "$BROWSER_EXE" ] && command -v "$BROWSER_EXE" >/dev/null 2>&1 && "$BROWSER_EXE" "$url" >/dev/null 2>&1 && return 0
      command -v xdg-open >/dev/null 2>&1 && xdg-open "$url" >/dev/null 2>&1 && return 0
      return 1
      ;;
    *) return 1 ;;
  esac
}

# browser_running — exit 0 if the extension browser's process is alive
browser_running() {
  local exe="$BROWSER_EXE"
  [ -z "$exe" ] && return 1
  case "$(detect_os)" in
    windows)
      MSYS_NO_PATHCONV=1 tasklist /fi "IMAGENAME eq $exe.exe" 2>/dev/null | grep -qi "$exe"
      ;;
    macos|linux)
      pgrep -x "$exe" >/dev/null 2>&1 || pgrep -f "$exe" >/dev/null 2>&1
      ;;
    *) return 1 ;;
  esac
}

# ---------------------------------------------------------------------------
# Pacing
# ---------------------------------------------------------------------------
# random_delay [min] [max] — sleep a random whole number of seconds in [min,max].
# Used between consecutive scrapes so a batch does not look like a machine
# opening window after window. The chosen value is left in RAND_DELAY.
RAND_DELAY=0
random_delay() {
  local min="${1:-15}" max="${2:-45}" span
  span=$(( max - min + 1 ))
  [ "$span" -lt 1 ] && span=1
  RAND_DELAY=$(( min + RANDOM % span ))
  sleep "$RAND_DELAY"
}

# ---------------------------------------------------------------------------
# Download directory — where scraped CSVs are saved.
# ---------------------------------------------------------------------------
# detect_download_dir — the OS's default downloads folder.
detect_download_dir() {
  local d
  case "$(detect_os)" in
    linux)
      if command -v xdg-user-dir >/dev/null 2>&1; then
        d="$(xdg-user-dir DOWNLOAD 2>/dev/null)"
        [ -n "$d" ] && { printf '%s' "$d"; return 0; }
      fi
      printf '%s' "$HOME/Downloads" ;;
    *) printf '%s' "$HOME/Downloads" ;;
  esac
}

# resolve_download_dir — precedence: env override > saved choice > OS default.
# Prints the directory (never empty).
resolve_download_dir() {
  local d="${MONSTERGET_DOWNLOAD_DIR:-}"
  [ -z "$d" ] && d="$(state_get download_dir)"
  [ -z "$d" ] && d="$(detect_download_dir)"
  case "$d" in "~"*) d="$HOME${d#\~}" ;; esac   # expand a leading ~
  printf '%s' "$d"
}

# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------
generate_task_id() {
  curl -s --max-time 10 "$BASE_URL/api/agent/generate-task-id" 2>/dev/null | sed -n 's/.*"taskId":"\([^"]*\)".*/\1/p'
}

# urlencode <string> — RFC 3986 percent-encoding, byte-safe for UTF-8
urlencode() {
  local LC_ALL=C
  local s="$1" c out="" i hex=""
  for ((i=0; i<${#s}; i++)); do
    c="${s:i:1}"
    case "$c" in
      [a-zA-Z0-9._~-]) out+="$c" ;;
      "'")             out+="%27" ;;
      *)               printf -v hex '%%%02X' "'$c"; out+="$hex" ;;
    esac
  done
  printf '%s' "$out"
}
