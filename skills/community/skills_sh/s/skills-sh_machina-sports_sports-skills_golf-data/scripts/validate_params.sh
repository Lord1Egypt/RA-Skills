#!/bin/bash
SPORT="${1:-golf}"  # golf
MONTH=$(date +%m)

case "$SPORT" in
  golf)
    DOW=$(date +%u)
    if [[ $DOW -le 3 ]]; then
      echo "INFO: Golf tournaments run Thu-Sun. Leaderboard may show last week's results."
    fi
    ;;
esac
echo "OK"
