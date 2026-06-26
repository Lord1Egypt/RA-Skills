#!/usr/bin/env bash
set -euo pipefail

# Multi-Model Weather Forecast - Get ensemble forecast for a city
# Usage: forecast.sh <city> [date]

HOST="${WEATHER_ENSEMBLE_HOST:-https://polymarket-scanner.fly.dev}"
API_KEY="${WEATHER_ENSEMBLE_API_KEY:-}"

CITY="${1:?Usage: forecast.sh <city> [YYYY-MM-DD]}"
CITY=$(echo "$CITY" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9 -]//g' | sed 's/ /%20/g')
DATE=$(echo "${2:-}" | sed 's/[^0-9-]//g')

CURL_ARGS=(-s -w "\n%{http_code}")
if [ -n "$API_KEY" ]; then
    CURL_ARGS+=(-H "X-API-Key: $API_KEY")
fi

URL="${HOST}/forecast/${CITY}"
if [ -n "$DATE" ]; then
    URL="${URL}?target_date=${DATE}"
fi

RESPONSE=$(curl "${CURL_ARGS[@]}" "$URL")
HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" != "200" ]; then
    echo "Error ($HTTP_CODE): $(echo "$BODY" | jq -r '.detail // .message // "Unknown error"' 2>/dev/null || echo "$BODY" | head -c 200)"
    exit 1
fi

echo "$BODY" | jq '{
    city: .city_name,
    date: .target_date,
    high_temp: "\(.high_temp) \(.unit)",
    std_dev: .ensemble_std,
    models_used: .n_models,
    horizon_days: .horizon_days,
    model_predictions: .model_temps
}'
