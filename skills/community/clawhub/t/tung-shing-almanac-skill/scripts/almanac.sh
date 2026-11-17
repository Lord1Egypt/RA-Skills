#!/usr/bin/env bash
# Tung Shing Almanac API client (12Zodiacs.com)
# Usage: almanac.sh {day|hours|term|auspicious|horoscope} [args] [api_key]
set -euo pipefail
API="https://12zodiacs.com/wp-json/12z/v1/almanac"
CMD="${1:-day}"
ARG="${2:-}"
KEY="${3:-}"
KEY_Q=""
[ -n "$KEY" ] && KEY_Q="&key=$KEY"

case "$CMD" in
  day)
    DATE_Q=""
    [ -n "$ARG" ] && DATE_Q="date=$ARG"
    curl -s -A 'tung-shing-almanac-skill/2.0' "${API}/day?${DATE_Q}${KEY_Q}" | jq .
    ;;
  hours)
    : "${ARG:?usage: almanac.sh hours YYYY-MM-DD}"
    curl -s -A 'tung-shing-almanac-skill/2.0' "${API}/hours?date=${ARG}${KEY_Q}" | jq .
    ;;
  term)
    : "${ARG:?usage: almanac.sh term YYYY}"
    curl -s -A 'tung-shing-almanac-skill/2.0' "${API}/term?year=${ARG}${KEY_Q}" | jq .
    ;;
  auspicious)
    # Pick auspicious dates for an activity. Synonyms welcome:
    # wedding|marriage|moving|buy-a-car|开业|装修|travel|... (see README table)
    # Usage: auspicious <activity> [days=30] [weekend_only=0] [api_key]
    DAYS="${3:-30}"
    WEEKEND="${4:-0}"
    KEY_A="${5:-}"
    WK_Q=""
    KEY_AQ=""
    [ "$WEEKEND" = "1" ] && WK_Q="&weekend_only=1"
    [ -n "$KEY_A" ] && KEY_AQ="&key=$KEY_A"
    curl -s -A 'tung-shing-almanac-skill/2.0' "${API}/auspicious?activity=${ARG}&days=${DAYS}${WK_Q}${KEY_AQ}" | jq .
    ;;
  lucky-hour)
    # Personal best hours for your zodiac on a date: e.g. lucky-hour horse 2026-08-22
    : "${ARG:?usage: almanac.sh lucky-hour <zodiac> [date] [key]}"
    DATE_L="${3:-}"
    DATE_Q=""
    KEY_LQ=""
    if [[ "$DATE_L" =~ ^[0-9]{4}- ]]; then
      DATE_Q="&date=$DATE_L"
      [ -n "${4:-}" ] && KEY_LQ="&key=$4"
    fi
    curl -s -A 'tung-shing-almanac-skill/2.0' "${API}/personal-hours?zodiac=${ARG}${DATE_Q}${KEY_LQ}" | jq .
    ;;
  horoscope)
    # Daily zodiac horoscope: rat|ox|tiger|rabbit|dragon|snake|horse|goat|monkey|rooster|dog|pig
    : "${ARG:?usage: almanac.sh horoscope <sign> [date] [key]}"
    DATE_H="${3:-}"
    DATE_Q=""
    if [[ "$DATE_H" =~ ^[0-9]{4}- ]]; then DATE_Q="&date=$DATE_H"; KEY=""; KEY_Q=""; fi
    curl -s -A 'tung-shing-almanac-skill/2.0' "${API}/horoscope?sign=${ARG}${DATE_Q}${KEY_Q}" | jq .
    ;;
  *)
    echo "usage: almanac.sh {day|hours|term|auspicious|horoscope} [args] [api_key]" >&2
    exit 1
    ;;
esac
