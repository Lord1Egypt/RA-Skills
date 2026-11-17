#!/usr/bin/env bash
# xps-plex — project a web page onto the xps host over SSH.
#
# The same job the MCP server does, with no server: three subcommands, each one
# bash block run on the remote host through ssh.
#
#   xps-plex.sh status                  proxy, browser counts, window titles
#   xps-plex.sh start-proxy             start v2rayN if the port is down
#   xps-plex.sh open [--browser B] [--windowed]
#
# Everything machine-specific is an environment variable with a default:
#   XPS_SSH_HOST, XPS_URL, XPS_PROXY_URL, XPS_PROXY_ADDR,
#   XPS_V2RAY_DIR, XPS_PROXY_WORKSPACE
set -uo pipefail

HOST="${XPS_SSH_HOST:-xps}"
PAGE="${XPS_URL:-https://watch.plex.tv/live-tv}"
PROXY_URL="${XPS_PROXY_URL:-http://127.0.0.1:10808}"
PROXY_ADDR="${XPS_PROXY_ADDR:-127.0.0.1:10808}"
V2RAY_DIR="${XPS_V2RAY_DIR:-\$HOME/pool/Downloads/rog_drive/v2rayN-linux-64}"
WORKSPACE="${XPS_PROXY_WORKSPACE:-2}"

usage() {
  sed -n '5,8p' "$0" | sed 's/^# \{0,1\}//'
  exit 2
}

# Shared remote prelude: discover the session, then define the helpers every
# subcommand uses. Written for `ssh <host> bash -s`, so anything that must
# resolve remotely is left unexpanded here.
prelude() {
  cat <<'REMOTE'
RUNDIR="/run/user/$(id -u)"
WD=$(ls "$RUNDIR" 2>/dev/null | grep -m1 '^wayland-[0-9]*$')
HIS=$(ls "$RUNDIR/hypr" 2>/dev/null | head -1)
export XDG_RUNTIME_DIR="$RUNDIR"
export WAYLAND_DISPLAY="${WD:-wayland-1}"
export DBUS_SESSION_BUS_ADDRESS="unix:path=$RUNDIR/bus"
export HYPRLAND_INSTANCE_SIGNATURE="$HIS"
export MOZ_ENABLE_WAYLAND=1
export XDG_SESSION_TYPE=wayland
XDISP=$(pgrep -a Xwayland 2>/dev/null | awk '{for(i=1;i<=NF;i++) if ($i ~ /^:[0-9]+$/) {print $i; exit}}')
export DISPLAY="${XDISP:-:0}"

# SIGTERM, wait, SIGKILL. Clears what a failed launch left behind.
kill_stale() {
  pids=$(pgrep -x "$1" 2>/dev/null)
  [ -z "$pids" ] && return 0
  kill $pids 2>/dev/null
  for _ in $(seq 1 $(( $2 * 2 ))); do
    pgrep -x "$1" >/dev/null 2>&1 || return 0
    sleep 0.5
  done
  kill -9 $(pgrep -x "$1" 2>/dev/null) 2>/dev/null
  return 0
}

proxy_state=up
ensure_proxy() {
  proxy_state=up
  if ss -ltn 2>/dev/null | grep -q '@PROXY_ADDR@'; then
    # The listener can outlive its GUI: v2rayN hands the port to an xray core,
    # and a killed GUI leaves that core orphaned still holding it.
    pgrep -x v2rayN >/dev/null 2>&1 && return 0
    kill_stale xray 4
  fi
  proxy_state=down
  V2RAY_DIR="@V2RAY_DIR@"
  if [ ! -x "$V2RAY_DIR/v2rayN" ]; then
    proxy_state=missing
    return 0
  fi
  kill_stale v2rayN 5
  kill_stale xray 4
  setsid sh -c "cd '$V2RAY_DIR' && exec ./v2rayN" >/tmp/v2rayN.log 2>&1 < /dev/null &
  for _ in $(seq 1 25); do
    sleep 1
    ss -ltn 2>/dev/null | grep -q '@PROXY_ADDR@' && { proxy_state=started; return 0; }
  done
  proxy_state=failed
  return 0
}

note_proxy() {
  case "$proxy_state" in
    up) echo "already listening" ;;
    started) echo "was down, v2rayN started" ;;
    missing) echo "v2rayN not found, launched without it" ;;
    failed) echo "v2rayN started but the port never opened" ;;
    *) echo "$proxy_state" ;;
  esac
}

move_proxy_window() {
  [ "$proxy_state" = "missing" ] && return 0
  addr=""
  for _ in $(seq 1 15); do
    addr=$(hyprctl clients -j 2>/dev/null \
      | jq -r '[.[] | select(.class|test("v2rayN"))] | sort_by(.focusHistoryID) | .[0].address // empty')
    [ -n "$addr" ] && break
    sleep 0.5
  done
  [ -z "$addr" ] && return 0
  ws=$(hyprctl clients -j 2>/dev/null | jq -r --arg a "$addr" '.[] | select(.address==$a) | .workspace.name')
  [ "$ws" = "@PROXY_WS@" ] || \
    hyprctl dispatch "hl.dsp.window.move({ window = \"address:$addr\", workspace = \"@PROXY_WS@\" })" >/dev/null 2>&1
  printf 'proxy window\tworkspace %s\n' "$(hyprctl clients -j 2>/dev/null | jq -r --arg a "$addr" '.[] | select(.address==$a) | .workspace.name')"
}

# Ready when one window carries a real title: blank tabs, New Tab, Untitled,
# the crash-restore dialog and the pre-load title all mean "keep waiting".
wait_title() {
  cls=$1; title=""; ready=""
  for _ in $(seq 1 45); do
    title=$(hyprctl clients -j 2>/dev/null | jq -r --arg c "$cls" '[.[] | select(.class|test($c)) | .title] | join(" ; ")')
    ready=$(printf '%s' "$title" | tr ';' '\n' | sed 's/^ *//;s/ *$//' \
      | grep -vE '^(|Mozilla Firefox|Untitled.*|New Tab.*|New Window.*|Restore Session.*)$' | head -1)
    [ -n "$ready" ] && break
    sleep 2
  done
  [ -z "$ready" ] && printf 'warning\tno page window\n'
  printf 'window\t%s\n' "$title"
}

# Fullscreen is dispatched, not passed. Focus by address first, so a sign-in
# popup cannot take the fullscreen from the page that was asked for.
zoom_window() {
  cls=$1; ttl=$2
  fs=$(hyprctl clients -j 2>/dev/null | jq -r --arg c "$cls" '[.[] | select(.class|test($c)) | .fullscreen] | max // 0')
  [ "${fs:-0}" = "2" ] && { printf 'fullscreen\tmode 2\n'; return; }
  addr=$(hyprctl clients -j 2>/dev/null | jq -r --arg c "$cls" --arg t "$ttl" \
    '([.[] | select(.class|test($c)) | select(.title|test($t))] | sort_by(.focusHistoryID) | .[0].address)
     // ([.[] | select(.class|test($c))] | sort_by(.focusHistoryID) | .[0].address)')
  if [ -n "${addr:-}" ] && [ "$addr" != "null" ]; then
    hyprctl dispatch "hl.dsp.focus({ window = \"address:$addr\" })" >/dev/null 2>&1
    hyprctl dispatch 'hl.dsp.window.fullscreen()' >/dev/null 2>&1
  fi
  printf 'fullscreen\tmode %s\n' "$(hyprctl clients -j 2>/dev/null | jq -r --arg c "$cls" '[.[] | select(.class|test($c)) | .fullscreen] | max // 0')"
}
REMOTE
}

# Substitute the placeholders once, so the subcommands stay readable.
fill() {
  sed -e "s|@PROXY_ADDR@|$PROXY_ADDR|g" \
      -e "s|@V2RAY_DIR@|$V2RAY_DIR|g" \
      -e "s|@PROXY_WS@|$WORKSPACE|g" \
      -e "s|@URL@|$PAGE|g" \
      -e "s|@PROXY@|$PROXY_URL|g"
}

# Run a body on the remote host with the prelude prepended, and print the
# key/value lines as "key: value" for a human or a model to read.
run_remote() {
  local out status
  out=$({ prelude; cat; } | fill | ssh -o BatchMode=yes -o ConnectTimeout=8 "$HOST" bash -s)
  status=$?
  if [ $status -ne 0 ] && [ -z "$out" ]; then
    echo "ssh to $HOST failed (exit $status)" >&2
    return 1
  fi
  printf '%s\n' "$out" | sed 's/\t/: /'
}

cmd_status() {
  run_remote <<'REMOTE'
printf 'host\t%s\n' "$(cat /proc/sys/kernel/hostname 2>/dev/null || uname -n)"
printf 'proxy\t%s\n' "$(ss -ltn 2>/dev/null | grep -q '@PROXY_ADDR@' && echo listening || echo down)"
printf 'v2rayN\t%s\n' "$(pgrep -x v2rayN | wc -l)"
printf 'firefox\t%s\n' "$(pgrep -x firefox | wc -l)"
printf 'brave\t%s\n' "$(pgrep -x brave | wc -l)"
printf 'windows\t%s\n' "$(hyprctl clients -j 2>/dev/null | jq -r '[.[] | select(.class|test("firefox|brave")) | .title] | join(" ; ")')"
REMOTE
}

cmd_start_proxy() {
  run_remote <<'REMOTE'
ensure_proxy
move_proxy_window
printf 'proxy\t%s\n' "$(note_proxy)"
REMOTE
}

cmd_open() {
  local browser="firefox" fullscreen=1 body
  while [ $# -gt 0 ]; do
    case "$1" in
      --browser) browser="${2:-}"; shift 2 ;;
      --windowed) fullscreen=0; shift ;;
      *) echo "unknown argument: $1" >&2; usage ;;
    esac
  done
  case "$browser" in firefox|brave) ;; *) echo "unknown browser: $browser (use firefox or brave)" >&2; exit 2 ;; esac

  if [ "$browser" = "firefox" ]; then
    body=$(cat <<'REMOTE'
ensure_proxy
move_proxy_window
PROF="$HOME/.mozilla/firefox/plex-proxy"
mkdir -p "$PROF"
cat > "$PROF/user.js" <<'JS'
user_pref("network.proxy.type", 1);
user_pref("network.proxy.http", "127.0.0.1");
user_pref("network.proxy.http_port", 10808);
user_pref("network.proxy.ssl", "127.0.0.1");
user_pref("network.proxy.ssl_port", 10808);
user_pref("network.proxy.share_proxy_settings", true);
user_pref("network.proxy.no_proxies_on", "localhost, 127.0.0.1");
user_pref("browser.startup.page", 1);
user_pref("browser.startup.homepage", "@URL@");
user_pref("browser.sessionstore.resume_from_crash", false);
user_pref("browser.startup.homepage_override.mstone", "ignore");
user_pref("startup.homepage_welcome_url", "");
user_pref("startup.homepage_welcome_url.additional", "");
user_pref("trailhead.firstrun.didSeeAboutWelcome", true);
user_pref("browser.aboutwelcome.enabled", false);
user_pref("browser.shell.checkDefaultBrowser", false);
user_pref("datareporting.policy.dataSubmissionEnabled", false);
user_pref("toolkit.telemetry.reportingpolicy.firstRun", false);
JS
rm -f "$PROF/sessionstore.jsonlz4" "$PROF"/sessionstore-backups/*
ff_windows() { hyprctl clients -j 2>/dev/null | jq '[.[] | select(.class|test("firefox"))] | length'; }
page_windows() { hyprctl clients -j 2>/dev/null | jq '[.[] | select(.class|test("firefox")) | select(.title|test("Plex"))] | length'; }
pid=$(pgrep -x firefox | head -1)
on_profile=""
if [ -n "${pid:-}" ] && tr '\0' ' ' < "/proc/$pid/cmdline" 2>/dev/null | grep -q 'plex-proxy'; then
  on_profile=1
fi
# Exactly one window showing the page: reuse it. Anything else — no browser,
# another profile, a blank or duplicated window — is cleared and started once.
if [ -n "$on_profile" ] && [ "$(ff_windows)" = "1" ] && [ "$(page_windows)" -ge 1 ]; then
  action=reuse
else
  if [ -z "${pid:-}" ]; then action=start
  elif [ -n "$on_profile" ]; then action=clean
  else action=restart; fi
  kill_stale firefox 8
  setsid firefox --profile "$PROF" --new-instance >/tmp/firefox-plex.log 2>&1 < /dev/null &
fi
printf 'action\t%s\n' "$action"
wait_title firefox
printf 'proxy\t%s\n' "$(note_proxy)"
REMOTE
)
  else
    body=$(cat <<'REMOTE'
ensure_proxy
move_proxy_window
pid=$(pgrep -x brave | head -1)
if [ -n "${pid:-}" ] && tr '\0' ' ' < "/proc/$pid/cmdline" 2>/dev/null | grep -q -- '--proxy-server='; then
  action=reuse
else
  if [ -n "${pid:-}" ]; then action=restart; kill_stale brave 8; else action=start; fi
  setsid brave --ozone-platform=wayland --proxy-server='@PROXY@' \
    --no-first-run --no-default-browser-check --new-window '@URL@' \
    >/tmp/brave-plex.log 2>&1 < /dev/null &
fi
printf 'action\t%s\n' "$action"
wait_title brave
printf 'proxy\t%s\n' "$(note_proxy)"
REMOTE
)
  fi

  if [ "$fullscreen" = "1" ]; then
    body+=$'\n'"zoom_window $browser Plex"
  fi
  printf '%s\n' "$body" | run_remote
}

case "${1:-}" in
  status) cmd_status ;;
  start-proxy) cmd_start_proxy ;;
  open) shift; cmd_open "$@" ;;
  *) usage ;;
esac
