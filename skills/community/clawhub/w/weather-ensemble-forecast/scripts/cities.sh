#!/usr/bin/env bash
set -euo pipefail

# Multi-Model Weather Forecast - List available cities

HOST="${WEATHER_ENSEMBLE_HOST:-https://polymarket-scanner.fly.dev}"
API_KEY="${WEATHER_ENSEMBLE_API_KEY:-}"

CURL_ARGS=(-s -w "\n%{http_code}")
if [ -n "$API_KEY" ]; then
    CURL_ARGS+=(-H "X-API-Key: $API_KEY")
fi

RESPONSE=$(curl "${CURL_ARGS[@]}" "${HOST}/cities")
HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" != "200" ]; then
    echo "Error ($HTTP_CODE): $(echo "$BODY" | jq -r '.detail // "Unknown error"' 2>/dev/null || echo "$BODY" | head -c 200)"
    exit 1
fi

echo "$BODY" | jq '{
    cities: [.cities[] | {
        key: .key,
        name: .name,
        unit: .unit
    }]
}'
