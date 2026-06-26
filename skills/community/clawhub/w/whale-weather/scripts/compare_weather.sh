#!/usr/bin/env bash
set -euo pipefail

# This script compares weather for multiple cities.
# Usage: bash compare_weather.sh "City A" "City B" [lang]

if [ "$#" -lt 1 ]; then
  echo "Usage: bash compare_weather.sh \"City A\" [\"City B\" ...] [lang]" >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GET_WEATHER="${SCRIPT_DIR}/get_weather.sh"

# Heuristic: if the last argument is exactly 2 characters (like 'en' or 'zh'), treat it as language
ARGS=("$@")
LAST_IDX=$(($# - 1))
LANG="zh"
CITIES=("${ARGS[@]}")

if [[ ${#ARGS[$LAST_IDX]} -eq 2 ]]; then
  LANG="${ARGS[$LAST_IDX]}"
  unset 'CITIES[$LAST_IDX]'
fi

for city in "${CITIES[@]}"; do
  bash "$GET_WEATHER" "$city" "$LANG"
  echo
done
