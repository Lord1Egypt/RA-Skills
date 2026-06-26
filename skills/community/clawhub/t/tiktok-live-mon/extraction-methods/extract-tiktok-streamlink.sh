#!/bin/bash
# TikTok Live Stream URL Extraktion via streamlink v1.2
# Usage: ./extract-tiktok-streamlink.sh <username> [quality] [--json]

USERNAME="$1"
QUALITY="${2:-best}"
JSON_FLAG="$3"
LIVE_URL="https://www.tiktok.com/@${USERNAME}/live"
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

if [ -z "$USERNAME" ]; then
    echo '{"success":false,"method":"streamlink","error":"Usage: extract-tiktok-streamlink.sh <username> [quality] [--json]"}' >&2
    exit 1
fi

if ! command -v streamlink &> /dev/null; then
    echo "{\"success\":false,\"method\":\"streamlink\",\"error\":\"streamlink not installed\",\"timestamp\":\"${TIMESTAMP}\"}"
    exit 1
fi

# Streamlink mit --json gibt strukturierte Stream-Infos aus
OUTPUT=$(streamlink --json "${LIVE_URL}" "${QUALITY}" 2>/dev/null)
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ] || [ -z "$OUTPUT" ]; then
    # Fallback: ohne --json probieren, nur URL extrahieren
    URL=$(streamlink --stream-url "${LIVE_URL}" "${QUALITY}" 2>/dev/null)
    if [ $? -eq 0 ] && [ -n "$URL" ]; then
        if [ "$JSON_FLAG" = "--json" ]; then
            echo "{\"success\":true,\"method\":\"streamlink\",\"username\":\"${USERNAME}\",\"url\":\"${URL}\",\"quality\":\"${QUALITY}\",\"timestamp\":\"${TIMESTAMP}\"}"
        else
            echo "$URL"
        fi
        exit 0
    fi

    if [ "$JSON_FLAG" = "--json" ]; then
        echo "{\"success\":false,\"method\":\"streamlink\",\"username\":\"${USERNAME}\",\"error\":\"streamlink failed or no stream found\",\"timestamp\":\"${TIMESTAMP}\"}"
    else
        echo "ERROR: streamlink failed for @${USERNAME}" >&2
    fi
    exit 1
fi

# Extrahiere URL aus JSON Output
URL=$(echo "$OUTPUT" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    url = data.get('url', '')
    if not url and 'streams' in data:
        for k in ['best', 'worst']:
            if k in data['streams'] and 'url' in data['streams'][k]:
                url = data['streams'][k]['url']
                break
        if not url:
            for k, v in data['streams'].items():
                if 'url' in v:
                    url = v['url']
                    break
    print(url)
except:
    print('')
" 2>/dev/null)

# Wenn URL nicht aus JSON gefunden, versuche direkt aus dem Output zu greifen
if [ -z "$URL" ]; then
    URL=$(echo "$OUTPUT" | grep -oP '"url":\s*"\K[^"]+\.flv[^"]*' | head -1)
fi

if [ -n "$URL" ]; then
    if [ "$JSON_FLAG" = "--json" ]; then
        # Extrahiere Metadaten falls vorhanden
        AUTHOR=$(echo "$OUTPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('metadata',{}).get('author',''))" 2>/dev/null)
        TITLE=$(echo "$OUTPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('metadata',{}).get('title',''))" 2>/dev/null)
        echo "{\"success\":true,\"method\":\"streamlink\",\"username\":\"${USERNAME}\",\"url\":\"${URL}\",\"quality\":\"${QUALITY}\",\"author\":\"${AUTHOR}\",\"title\":\"${TITLE}\",\"timestamp\":\"${TIMESTAMP}\"}"
    else
        echo "$URL"
    fi
    exit 0
else
    if [ "$JSON_FLAG" = "--json" ]; then
        echo "{\"success\":false,\"method\":\"streamlink\",\"username\":\"${USERNAME}\",\"error\":\"Could not extract URL from streamlink output\",\"timestamp\":\"${TIMESTAMP}\"}"
    else
        echo "ERROR: Could not extract URL for @${USERNAME}" >&2
    fi
    exit 1
fi
