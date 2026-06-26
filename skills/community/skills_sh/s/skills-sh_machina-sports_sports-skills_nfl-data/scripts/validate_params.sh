#!/bin/bash
SPORT="${1:-nfl}"  # nfl
MONTH=$(date +%m)

case "$SPORT" in
  nfl)
    if [[ $MONTH -ge 3 && $MONTH -le 8 ]]; then
      echo "WARNING: NFL is in off-season (Sep-Feb). Scoreboard may be empty."
      echo "SUGGESTION: Use get_news or get_standings with a prior season."
    fi
    ;;
esac
echo "OK"
