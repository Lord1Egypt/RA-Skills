#!/bin/bash
# TikTok Live Stream URL Extraktion via yt-dlp v1.1
# Usage: ./extract-tiktok-yt-dlp.sh <username> [format] [--json]
# Gibt nackte URL aus oder JSON bei --json Flag
# Korrekturen: Besseres JSON-Handling und Fehlerquellen-Logging

USERNAME="$1"
FORMAT="${2:-best}" # Default best quality for yt-dlp
JSON_FLAG="$3"

# Temporäres Verzeichnis für Logs und Output
TMP_DIR="/tmp/tiktok_$(date +%s)"
mkdir -p "$TMP_DIR"

if [ -z "$USERNAME" ]; then
    echo '{"success":false,"method":"yt-dlp","error":"Usage: extract-tiktok-yt-dlp.sh <username> [format] [--json]","timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"}' >&2
    exit 1
fi

LIVE_URL="https://www.tiktok.com/@${USERNAME}/live"

# yt-dlp Kommando mit mehr Optionen für Robustheit
# --print-json gibt strukturierte Daten aus
# --output_args '%(url,http_headers.cookie)s' könnte nützlich sein, wird aber hier ignoriert
# --no-warnings sollte nur für saubere Ausgabe verwendet werden, aber wir loggen stderr
COMMAND="yt-dlp --no-warnings --print-json --skip-download --write-info-json --prefer-free-formats --format \"${FORMAT}\" \"${LIVE_URL}\""

echo "Running command: ${COMMAND}" >&2 # Log command for debugging

# Führe yt-dlp aus und fange stdout/stderr auf
eval "$COMMAND" 2> "${TMP_DIR}/yt-dlp.stderr.log" > "${TMP_DIR}/yt-dlp.stdout.log"
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    STDERR_OUTPUT=$(cat "${TMP_DIR}/yt-dlp.stderr.log")
    echo "yt-dlp exited with code $EXIT_CODE. Stderr: ${STDERR_OUTPUT}" >&2
    if [ "$JSON_FLAG" = "--json" ]; then
        echo "{\"success\":false,\"method\":\"yt-dlp\",\"username\":\"${USERNAME}\",\"error\":\"yt-dlp failed with code ${EXIT_CODE}. Stderr: ${STDERR_OUTPUT//\"/\\\"}\",\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}"
    else
        echo "ERROR: yt-dlp failed for @${USERNAME}." >&2
    fi
    exit $EXIT_CODE
fi

# Parse die stdout
STDOUT_OUTPUT=$(cat "${TMP_DIR}/yt-dlp.stdout.log")

# Versuche, die URL direkt zu finden
# yt-dlp gibt manchmal direkt die URL zurück, wenn --print-json nicht gut funktioniert
EXTRACTED_URL=$(echo "$STDOUT_OUTPUT" | grep -o 'http.*\.flv' | head -n 1)

if [ -n "$EXTRACTED_URL" ]; then
    if [ "$JSON_FLAG" = "--json" ]; then
        echo "{\"success\":true,\"method\":\"yt-dlp\",\"username\":\"${USERNAME}\",\"url\":\"${EXTRACTED_URL}\",\"format\":\"${FORMAT}\",\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}"
    else
        echo "$EXTRACTED_URL"
    fi
    exit 0
fi

# Wenn directe URL nicht gefunden, parse JSON output
JSON_DATA=$(echo "$STDOUT_OUTPUT" | jq -r '. | select(length > 0)')
if [ -z "$JSON_DATA" ] || [ "$JSON_DATA" == "null" ]; then
    # Wenn kein JSON gefunden wurde, prüfen wir die STDERR für Hinweise
    STDERR_OUTPUT=$(cat "${TMP_DIR}/yt-dlp.stderr.log")
    if [[ "$STDERR_OUTPUT" == *"No live cdn found"* ]] || [[ "$STDERR_OUTPUT" == *"is not available"* ]] || [[ "$STDERR_OUTPUT" == *"private video"* ]]; then
         if [ "$JSON_FLAG" = "--json" ]; then
            echo "{\"success\":false,\"method\":\"yt-dlp\",\"username\":\"${USERNAME}\",\"error\":\"Stream not found or private. ${STDERR_OUTPUT//\"/\\\"}\",\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}"
        else
            echo "ERROR: Stream not found or private for @${USERNAME}. ${STDERR_OUTPUT}" >&2
        fi
        exit 1
    fi
    # Wenn es kein klarer Fehler ist, aber kein JSON/URL, dann schlagen wir fehl
    if [ "$JSON_FLAG" = "--json" ]; then
        echo "{\"success\":false,\"method\":\"yt-dlp\",\"username\":\"${USERNAME}\",\"error\":\"Could not find JSON or URL in yt-dlp output. Check logs.\",\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}"
    else
        echo "ERROR: Could not find JSON or URL in yt-dlp output for @${USERNAME}." >&2
    fi
    exit 1
fi

# Extrahiere die beste URL aus dem JSON, mit Priorität auf FLV
BEST_URL=$(echo "$JSON_DATA" | jq -r '
  .url // (if .formats then
    (
      .formats
      | map(select(.protocol | test("http")) | select(.ext == "flv" or .vcodec == "avc1") | .url)
      | if length > 0 then .[0]
        else
          (map(.url) | .[0]) // ""
        end
    )
  else "" end)
')

if [ -n "$BEST_URL" ]; then
    if [ "$JSON_FLAG" = "--json" ]; then
        echo "{\"success\":true,\"method\":\"yt-dlp\",\"username\":\"${USERNAME}\",\"url\":\"${BEST_URL}\",\"format\":\"${FORMAT}\",\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}"
    else
        echo "$BEST_URL"
    fi
    exit 0
else
    if [ "$JSON_FLAG" = "--json" ]; then
        echo "{\"success\":false,\"method\":\"yt-dlp\",\"username\":\"${USERNAME}\",\"error\":\"Could not extract stream URL from JSON data.\",\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}"
    else
        echo "ERROR: Could not extract stream URL from JSON data for @${USERNAME}." >&2
    fi
    exit 1
fi
