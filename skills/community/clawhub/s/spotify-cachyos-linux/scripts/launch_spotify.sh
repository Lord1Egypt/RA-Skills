#!/usr/bin/env bash
# Start or stop the Spotify desktop client inside the invoking user's own
# graphical session.
#
# Usage:
#   scripts/launch_spotify.sh            start Spotify as a systemd --user unit
#   scripts/launch_spotify.sh --stop     stop the managed Spotify instance
#   scripts/launch_spotify.sh --check    resolve and validate session credentials
#                                        without launching anything
#
# Security model:
#   * Only the invoking user's own session credentials are ever used.
#   * Every Xauthority candidate must be a regular file owned by the invoking
#     user with no group/other access, or it is rejected.
#   * Elevated execution is refused: a privileged process must not pick up or
#     read other users' graphical credentials.
#   * Spotify runs as a transient systemd --user unit (`spotify-skill-launch`),
#     independent of this process tree but visible in `systemctl --user` and
#     stoppable via `--stop`.
#
# Network model (important behind a proxy):
#   A systemd user unit inherits the systemd user manager's environment, which
#   usually has NO http_proxy/https_proxy — unlike a shell started from the
#   desktop session. Spotify then cannot reach its servers, sits at the sign-in
#   page, and answers every MPRIS command with success while doing nothing.
#   This script resolves proxy settings from, in order:
#     1) the caller's environment (http_proxy / https_proxy / ftp_proxy /
#        all_proxy / no_proxy, upper- or lower-case), then
#     2) KDE's proxy configuration (~/.config/kioslaverc, manual proxy only),
#   and forwards them into the unit. It also probes reachability before
#   launching and reports whether the running client actually has content
#   loaded, so a signed-out client is visible instead of silently inert.
set -euo pipefail

UNIT="spotify-skill-launch"
KIOSLAVERC="${HOME:-/home/$USER}/.config/kioslaverc"

fail() { echo "ERROR: $*" >&2; exit 1; }
warn() { echo "WARNING: $*" >&2; }

# ---------------------------------------------------------------------------
# Stop
# ---------------------------------------------------------------------------
if [ "${1:-start}" = "--stop" ]; then
  if [ -n "${XDG_RUNTIME_DIR:-}" ] && [ -S "$XDG_RUNTIME_DIR/systemd/private" ] \
    && systemctl --user --quiet is-active "$UNIT" 2>/dev/null; then
    systemctl --user stop "$UNIT"
    echo "Spotify stopped (systemd unit: $UNIT)"
    exit 0
  fi
  if command -v pkill >/dev/null 2>&1 && pgrep -x spotify >/dev/null 2>&1; then
    pkill -x spotify
    echo "Spotify stopped"
  else
    echo "Spotify is not running"
  fi
  exit 0
fi

# ---------------------------------------------------------------------------
# Common prerequisites
# ---------------------------------------------------------------------------
[ "$(id -u)" -ne 0 ] || fail "refusing to run with elevated privileges; launch from the desktop user's session"

# Session bus for the DBus checks (standard per-user socket when the env var
# is unset).
if [ -z "${DBUS_SESSION_BUS_ADDRESS:-}" ] && [ -n "${XDG_RUNTIME_DIR:-}" ] && [ -S "$XDG_RUNTIME_DIR/bus" ]; then
  export DBUS_SESSION_BUS_ADDRESS="unix:path=$XDG_RUNTIME_DIR/bus"
fi

# Resolve the Spotify executable: native packages and spotify-launcher first,
# then Flatpak and Snap. Every install method registers the same DBus name
# (org.mpris.MediaPlayer2.spotify), so the MPRIS commands in the skill work
# regardless of how Spotify was installed.
SPOTIFY_CMD=()
if command -v spotify >/dev/null 2>&1; then
  SPOTIFY_CMD=(spotify)
elif command -v spotify-launcher >/dev/null 2>&1; then
  SPOTIFY_CMD=(spotify-launcher)
elif command -v flatpak >/dev/null 2>&1 \
  && flatpak list --app 2>/dev/null | grep -q 'com.spotify.Client'; then
  SPOTIFY_CMD=(flatpak run com.spotify.Client)
elif command -v snap >/dev/null 2>&1 && snap list 2>/dev/null | grep -q '^spotify'; then
  SPOTIFY_CMD=(snap run spotify)
fi

# valid_auth <path>: print the canonical path if (and only if) it is a regular
# file owned by the invoking user and not accessible by group/other.
valid_auth() {
  local f="$1" resolved mode uid
  resolved=$(readlink -f -- "$f") || return 1
  [ -f "$resolved" ] || return 1
  uid=$(stat -c '%u' -- "$resolved") || return 1
  [ "$uid" = "$(id -u)" ] || return 1
  mode=$(stat -c '%a' -- "$resolved") || return 1
  [ $((8#$mode & 077)) -eq 0 ] || return 1
  printf '%s\n' "$resolved"
}

# ---------------------------------------------------------------------------
# Proxy resolution
#
# A systemd user unit inherits the user manager's environment, which normally
# carries no proxy variables (a desktop shell exports those). A client started
# without them takes the direct route instead of the session's configured one —
# on networks where direct access to Spotify is unreliable or blocked, the
# client then stalls before signing in and every MPRIS command answers
# successfully while doing nothing. Forwarding the session's proxy settings
# keeps Spotify on the route the rest of the desktop already uses.
# ---------------------------------------------------------------------------

# kde_proxy <Key>: print a [Proxy Settings] value from KDE's kioslaverc.
kde_proxy() {
  [ -f "$KIOSLAVERC" ] || return 0
  awk -v key="$1" '
    /^\[/ { insec = ($0 == "[Proxy Settings]"); next }
    insec && index($0, key "=") == 1 { sub(/^[^=]*=/, ""); print; exit }
  ' "$KIOSLAVERC" 2>/dev/null
}

# normalize_proxy <value>: KDE stores "host port" pairs; turn them into a URL.
normalize_proxy() {
  local v="$1" host port
  case "$v" in
    *" "*)
      host=${v%% *}
      port=${v##* }
      case "$host" in *"://"*) ;; *) host="http://$host" ;; esac
      printf '%s:%s\n' "$host" "$port"
      ;;
    *"://"*) printf '%s\n' "$v" ;;
    *) printf 'http://%s\n' "$v" ;;
  esac
}

PROXY_SOURCE=""

# 1) The caller's environment (either case) takes precedence. Note: the
#    variables are read, never pre-initialised — assigning them here would
#    shadow the inherited values.
for name in http_proxy https_proxy ftp_proxy all_proxy no_proxy; do
  upper=$(printf '%s' "$name" | tr '[:lower:]' '[:upper:]')
  eval "val=\${$name:-}"
  [ -z "$val" ] && eval "val=\${$upper:-}"
  if [ -n "$val" ]; then
    printf -v "$name" '%s' "$val"
    PROXY_SOURCE="environment"
  fi
done

# 2) KDE's configured manual proxy fills whatever the environment left unset.
#    socksProxy is deliberately not mapped to all_proxy: exporting a SOCKS
#    proxy for every protocol makes HTTP clients (e.g. the reachability probe)
#    take a route the Spotify client itself never uses.
kde_used=0
if [ "$(kde_proxy ProxyType)" = "1" ]; then
  for pair in "http_proxy:httpProxy" "https_proxy:httpsProxy" "ftp_proxy:ftpProxy"; do
    var=${pair%%:*}; key=${pair##*:}
    eval "cur=\${$var:-}"
    [ -n "$cur" ] && continue
    val=$(kde_proxy "$key")
    [ -n "$val" ] && { printf -v "$var" '%s' "$(normalize_proxy "$val")"; kde_used=1; }
  done
  if [ -z "${no_proxy:-}" ]; then
    val=$(kde_proxy NoProxyFor)
    [ -n "$val" ] && { no_proxy="$val"; kde_used=1; }
  fi
  if [ -z "${https_proxy:-}" ] && [ -n "${http_proxy:-}" ]; then
    https_proxy=$http_proxy
  fi
  [ "$kde_used" = 1 ] && PROXY_SOURCE="${PROXY_SOURCE:+$PROXY_SOURCE+}kioslaverc"
fi

for name in http_proxy https_proxy ftp_proxy all_proxy no_proxy; do
  eval "val=\${$name:-}"
  [ -n "$val" ] && export "$name=$val"
done

# check_network: can we reach Spotify's sign-in host with the current settings?
# The probe is deliberately heuristic: curl's network path (TLS stack, proxy
# policy group, timeouts) can differ from the Spotify client's own, so a
# failure here is a hint, not a diagnosis — the client's loaded-track state is
# the authoritative signal. Two attempts: the request as-configured (proxy env
# variables and no_proxy apply), then, when a proxy is set, the same request
# forced through that proxy with no_proxy ignored.
NET_OK="unknown"
check_network() {
  command -v curl >/dev/null 2>&1 || { NET_OK="unknown"; return 0; }
  local code px
  local args=(-sS --connect-timeout 5 -m 12 -o /dev/null -w '%{http_code}')
  # 1) As configured: the same environment variables the Spotify unit inherits.
  code=$(curl "${args[@]}" https://accounts.spotify.com/ 2>/dev/null) || code=""
  case "$code" in
    ""|000) ;;
    *) NET_OK="yes"; return 0 ;;   # any HTTP reply means the host is reachable
  esac
  # 2) With a proxy configured, retry forcing the request through it. This
  #    covers setups where the as-configured path is flaky for curl but the
  #    client (which always honors the proxy variables) gets through.
  px="${https_proxy:-${HTTPS_PROXY:-${http_proxy:-${HTTP_PROXY:-}}}}"
  if [ -n "$px" ]; then
    code=$(curl "${args[@]}" --noproxy "" -x "$px" https://accounts.spotify.com/ 2>/dev/null) || code=""
    case "$code" in
      ""|000) ;;
      *) NET_OK="yes"; return 0 ;;
    esac
  fi
  NET_OK="no"
}

# ---------------------------------------------------------------------------
# Client state helpers
# ---------------------------------------------------------------------------

# mpris_prop <Property>: raw reply for a Player property.
mpris_prop() {
  dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify \
    /org/mpris/MediaPlayer2 org.freedesktop.DBus.Properties.Get \
    string:org.mpris.MediaPlayer2.Player "string:$1" 2>/dev/null
}

spotify_registered() {
  dbus-send --session --dest=org.freedesktop.DBus --type=method_call --print-reply \
    /org/freedesktop/DBus org.freedesktop.DBus.ListNames 2>/dev/null | grep -q spotify
}

# spotify_state: print "<PlaybackStatus>|<xesam:title>|<mpris:trackid>".
# An empty trackid means the client has no track loaded — freshly started,
# signed out, or still initializing. Such a client answers every MPRIS command
# with success while changing nothing, which is easy to mistake for a working
# client, so the launcher reports this state instead of a bare "ready".
spotify_state() {
  local st ti tid meta
  # Each substitution is guarded: under `set -e` a grep with no match would
  # otherwise abort the script — precisely in the "no track loaded" case this
  # function exists to report.
  st=$(mpris_prop PlaybackStatus | tail -1 | grep -oE '"(Playing|Paused|Stopped)"' | tr -d '"') || true
  meta=$(mpris_prop Metadata) || true
  ti=$(printf '%s\n' "$meta" | grep -A1 '"xesam:title"' | tail -1 | sed -n 's/.*string "\(.*\)"$/\1/p') || true
  tid=$(printf '%s\n' "$meta" | grep -A1 '"mpris:trackid"' | tail -1 | sed -n 's/.*string "\(.*\)"$/\1/p') || true
  printf '%s|%s|%s\n' "${st:-unknown}" "$ti" "$tid"
}

# describe_running: print a health line for the registered client.
describe_running() {
  local state st ti tid
  state=$(spotify_state)
  IFS='|' read -r st ti tid <<<"$state"
  if [ -z "$tid" ]; then
    echo "  state: $st, no track loaded — the client may be signed out or still initializing."
    [ "$NET_OK" = "no" ] && echo "  network: cannot reach accounts.spotify.com — check the proxy settings."
    echo "  MPRIS commands will answer but have no effect. If this persists, run"
    echo "  '$0 --stop' and launch again once connectivity works."
  else
    echo "  state: $st, track: ${ti:-unknown}"
  fi
}

# ---------------------------------------------------------------------------
# Session credential resolution (invoking user only)
# ---------------------------------------------------------------------------
AUTH=""

# 1) Caller's environment. If XAUTHORITY is set it must validate; otherwise
#    fail rather than silently substituting another session's credentials.
if [ -n "${XAUTHORITY:-}" ]; then
  AUTH=$(valid_auth "$XAUTHORITY") \
    || fail "XAUTHORITY=$XAUTHORITY is not a regular file owned by you without group/other access"
fi

# 2) Standard per-user locations.
if [ -z "$AUTH" ] && [ -f "$HOME/.Xauthority" ]; then
  AUTH=$(valid_auth "$HOME/.Xauthority") || true
fi
if [ -z "$AUTH" ] && [ -n "${XDG_RUNTIME_DIR:-}" ]; then
  for cand in "$XDG_RUNTIME_DIR"/xauth_*; do
    [ -f "$cand" ] || continue
    AUTH=$(valid_auth "$cand") || AUTH=""
    [ -n "$AUTH" ] && break
  done
fi

# 3) Last resort: the invoking user's own X server processes. Other users'
#    processes are never scanned, and the discovered file still has to pass
#    the ownership/permission validation above.
if [ -z "$AUTH" ]; then
  line=$(ps -u "$(id -u)" -o args= 2>/dev/null \
    | grep -E -- '[X]wayland|[X]org' \
    | grep -E -- '-auth[ =]\S+' | head -n1 || true)
  if [ -n "$line" ]; then
    cand=$(printf '%s\n' "$line" | grep -oE -- '-auth[ =]\S+' | head -n1 | sed -E 's/^-auth[ =]//') || true
    if [ -n "$cand" ]; then
      AUTH=$(valid_auth "$cand") || AUTH=""
    fi
  fi
fi

[ -n "$AUTH" ] || fail "no usable Xauthority file for your session; set DISPLAY/XAUTHORITY or run from within your desktop session"
export XAUTHORITY="$AUTH"

# Display: caller's env first (validated against a live X11 socket), then the
# display of the matched X server process, then the invoking user's own X11
# sockets.
DISPLAY_VAL=""
if [ -n "${DISPLAY:-}" ]; then
  DISPLAY_VAL="$DISPLAY"
elif [ -n "${line:-}" ]; then
  d=$(printf '%s\n' "$line" | grep -oE ':[0-9]+' | head -n1 | tr -d ':') || true
  [ -n "${d:-}" ] && DISPLAY_VAL=":$d"
fi
if [ -z "$DISPLAY_VAL" ]; then
  for sock in /tmp/.X11-unix/X*; do
    [ -S "$sock" ] || continue
    [ "$(stat -c '%u' -- "$sock" 2>/dev/null)" = "$(id -u)" ] || continue
    DISPLAY_VAL=":${sock##*X}"
    break
  done
fi
[ -n "$DISPLAY_VAL" ] || fail "could not determine your graphical display; set DISPLAY explicitly"

# Validate the display: must name a live local X11 socket.
dnum=$(printf '%s\n' "$DISPLAY_VAL" | grep -oE '[0-9]+$' || true)
[ -n "$dnum" ] || fail "unsupported DISPLAY value: $DISPLAY_VAL"
[ -S "/tmp/.X11-unix/X$dnum" ] \
  || fail "DISPLAY=$DISPLAY_VAL: no X11 socket /tmp/.X11-unix/X$dnum; is the graphical session active?"
export DISPLAY="$DISPLAY_VAL"

# ---------------------------------------------------------------------------
# Check mode: report what would be used, without launching anything
# ---------------------------------------------------------------------------
if [ "${1:-start}" = "--check" ]; then
  echo "DISPLAY=$DISPLAY"
  echo "XAUTHORITY=$XAUTHORITY"
  if [ -n "${XDG_RUNTIME_DIR:-}" ] && [ -S "$XDG_RUNTIME_DIR/systemd/private" ]; then
    echo "systemd --user manager: available"
  else
    echo "systemd --user manager: unavailable"
  fi
  if [ ${#SPOTIFY_CMD[@]} -gt 0 ]; then
    echo "Spotify executable: ${SPOTIFY_CMD[*]}"
  else
    echo "Spotify executable: NOT FOUND — install the client first (see SKILL.md prerequisites)"
  fi
  case "$PROXY_SOURCE" in
    "") echo "proxy: none configured — direct connection only" ;;
    environment) echo "proxy: from the calling environment" ;;
    kioslaverc) echo "proxy: from $KIOSLAVERC" ;;
    *) echo "proxy: from the calling environment + $KIOSLAVERC" ;;
  esac
  [ -n "${http_proxy:-}" ] && echo "  http_proxy=${http_proxy}"
  [ -n "${https_proxy:-}" ] && echo "  https_proxy=${https_proxy}"
  [ -n "${no_proxy:-}" ] && echo "  no_proxy=${no_proxy}"
  # Client state first: when a track is loaded, the client demonstrably has
  # connectivity, so a failed probe below is a probe limitation, not an outage.
  if spotify_registered; then
    echo "Spotify: already running (DBus registered)"
    describe_running
  else
    echo "Spotify: not running"
  fi
  check_network
  case "$NET_OK" in
    yes) echo "network: accounts.spotify.com reachable" ;;
    no)
      if spotify_registered && [ -n "$(spotify_state | cut -d'|' -f3)" ]; then
        echo "network: probe failed, but the running client has a track loaded — probe false negative, connectivity is fine"
      else
        echo "network: cannot reach accounts.spotify.com — Spotify may start but stay at the sign-in page (proxy needed?)"
      fi
      ;;
    *) echo "network: not checked (curl unavailable)" ;;
  esac
  exit 0
fi

# ---------------------------------------------------------------------------
# Launch
# ---------------------------------------------------------------------------
check_network

# Already running?
if spotify_registered; then
  echo "Spotify is already running (DBus registered)"
  describe_running
  exit 0
fi

[ "$NET_OK" != "no" ] \
  || warn "network probe could not reach accounts.spotify.com; Spotify may start but stay at the sign-in page"

# Hand Spotify to the user's systemd manager: it runs independently of this
# process tree, is visible via `systemctl --user status $UNIT`, and stops
# cleanly with `scripts/launch_spotify.sh --stop`.
if [ -z "${XDG_RUNTIME_DIR:-}" ] || [ ! -S "$XDG_RUNTIME_DIR/systemd/private" ]; then
  fail "systemd --user manager not reachable; launch from within your desktop session"
fi
if ! command -v systemd-run >/dev/null 2>&1; then
  fail "systemd-run not found"
fi

# Forward the resolved proxy settings into the unit: the systemd user manager's
# own environment usually has none, and a client without them cannot sign in.
env_args=(--setenv="DISPLAY=$DISPLAY" --setenv="XAUTHORITY=$XAUTHORITY")
for name in http_proxy https_proxy ftp_proxy all_proxy no_proxy; do
  eval "val=\${$name:-}"
  if [ -n "$val" ]; then
    env_args+=(--setenv="$name=$val")
    env_args+=(--setenv="$(printf '%s' "$name" | tr '[:lower:]' '[:upper:]')=$val")
  fi
done

if [ ${#SPOTIFY_CMD[@]} -eq 0 ]; then
  fail "Spotify is not installed. Install the client first, e.g.:
  Arch/CachyOS: pacman -S spotify          (or spotify-launcher)
  Fedora:       flatpak install com.spotify.Client
  Ubuntu:       spotify-client .deb from spotify.com   (or snap install spotify)"
fi

systemctl --user stop "$UNIT" 2>/dev/null || true
systemctl --user reset-failed "$UNIT" 2>/dev/null || true
systemd-run --user --unit="$UNIT" --collect "${env_args[@]}" \
  "${SPOTIFY_CMD[@]}" || fail "failed to start Spotify via systemd --user"

# Wait for DBus registration (Spotify needs ~5-8 seconds)
for i in $(seq 1 15); do
  sleep 1
  if spotify_registered; then
    echo "Spotify ready (took ${i}s, proxy: ${PROXY_SOURCE:-none})"
    # Give the client a moment to finish signing in, then report what it holds.
    sleep 3
    describe_running
    exit 0
  fi
done

warn "Spotify process running but DBus not registered after 15s"
exit 1
