#!/usr/bin/env bash
# xiaopai-ctl.sh — CLI helper for controlling XiaoPai media player
# Usage:
#   xiaopai-ctl.sh discover                          Discover players on LAN
#   xiaopai-ctl.sh <IP> sendkey <KEYCODE>
#   xiaopai-ctl.sh <IP> play-path <video_path_or_url>
#   xiaopai-ctl.sh <IP> play-name <video_name>
#   xiaopai-ctl.sh <IP> status

set -euo pipefail

usage() {
    echo "Usage:"
    echo "  $0 discover                          Discover players on LAN via mDNS"
    echo "  $0 <IP> sendkey <KEYCODE>          Send remote key (e.g. PLA, VUP, HOM)"
    echo "  $0 <IP> play-path <path_or_url>    Play video by file path or URL"
    echo "  $0 <IP> play-name <name>           Play video by name (search library)"
    echo "  $0 <IP> status                     Query current playback status"
    exit 1
}

[ $# -lt 1 ] && usage

# --- discover subcommand (no IP required) ---
if [ "$1" = "discover" ]; then
    echo "Searching for XiaoPai players on LAN (_xiaopai._tcp) ..."
    if command -v dns-sd >/dev/null 2>&1; then
        echo "(Press Ctrl+C to stop)"
        dns-sd -B _xiaopai._tcp .
    elif command -v avahi-browse >/dev/null 2>&1; then
        avahi-browse -r _xiaopai._tcp --terminate
    elif command -v python3 >/dev/null 2>&1; then
        python3 -c "
from zeroconf import ServiceBrowser, Zeroconf, ServiceStateChange
import time, sys

found = []

def on_change(zc, type_, name, state_change):
    if state_change is ServiceStateChange.Added:
        info = zc.get_service_info(type_, name)
        if info:
            from ipaddress import ip_address
            ip = ip_address(info.addresses[0])
            tcp_port = info.properties.get(b'tcp_port', b'').decode()
            mac = info.properties.get(b'mac', b'').decode()
            print(f'  {info.server}  IP={ip}  HTTP={info.port}  TCP={tcp_port}  MAC={mac}')
            found.append(True)

zc = Zeroconf()
ServiceBrowser(zc, '_xiaopai._tcp.local.', handlers=[on_change])
time.sleep(5)
zc.close()
if not found:
    print('  No players found.')
" 2>/dev/null || echo "Error: install zeroconf (pip3 install zeroconf) or use dns-sd / avahi-browse."
    else
        echo "Error: no mDNS tool found. Install one of:"
        echo "  - dns-sd  (macOS built-in, or Bonjour SDK on Windows)"
        echo "  - avahi-browse  (apt install avahi-utils)"
        echo "  - python3 + zeroconf  (pip3 install zeroconf)"
        exit 1
    fi
    exit 0
fi

[ $# -lt 2 ] && usage

IP="$1"
CMD="$2"
BASE="http://${IP}:9050"

url_encode() {
    python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$1" 2>/dev/null \
    || python -c "import urllib,sys; print(urllib.quote(sys.argv[1]))" "$1" 2>/dev/null \
    || printf '%s' "$1"
}

case "$CMD" in
    sendkey)
        [ $# -lt 3 ] && { echo "Error: missing KEYCODE"; usage; }
        KEYCODE=$(echo "$3" | tr '[:lower:]' '[:upper:]')
        curl -s "${BASE}/xiaopai/sendkey?keycode=${KEYCODE}"
        echo
        ;;
    play-path)
        [ $# -lt 3 ] && { echo "Error: missing video path"; usage; }
        ENCODED=$(url_encode "$3")
        curl -s "${BASE}/xiaopai/play?videopath=${ENCODED}"
        echo
        ;;
    play-name)
        [ $# -lt 3 ] && { echo "Error: missing video name"; usage; }
        ENCODED=$(url_encode "$3")
        curl -s "${BASE}/xiaopai/play?videoname=${ENCODED}"
        echo
        ;;
    status)
        echo "" | nc -w 2 "$IP" 9051 2>/dev/null || echo '{"error":"connection failed"}'
        ;;
    *)
        echo "Unknown command: $CMD"
        usage
        ;;
esac
