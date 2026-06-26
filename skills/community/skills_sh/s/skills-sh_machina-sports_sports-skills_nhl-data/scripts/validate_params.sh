#!/bin/bash
SPORT="${1:-nhl}"  # nhl
MONTH=$(date +%m)

case "$SPORT" in
  nhl)
    if [[ $MONTH -ge 7 && $MONTH -le 9 ]]; then
      echo "WARNING: NHL is in off-season (Oct-Jun). Scoreboard may be empty."
      echo "SUGGESTION: Use get_news or get_standings with a prior season."
    fi
    ;;
esac
echo "OK"
