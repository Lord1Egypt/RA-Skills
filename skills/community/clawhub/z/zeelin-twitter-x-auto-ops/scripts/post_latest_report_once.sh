#!/bin/bash

# Post latest report from THU ZeeLin Reports only once
# Stores last posted report title locally to avoid duplicates

REPORT_SITE="https://thu-nmrc.github.io/THU-ZeeLin-Reports/"
STATE_FILE="$HOME/.openclaw/memory/zeelin_last_report.txt"
TWEET_SCRIPT="/Users/youke/.openclaw/workspace/skills/zeelin-twitter-web-autopost/scripts/tweet.sh"

mkdir -p "$HOME/.openclaw/memory"

# Extract latest report title from page
LATEST_TITLE=$(curl -s "$REPORT_SITE" | grep -m1 -oE '<heading "[^"]+' | sed 's/<heading "//')

if [ -z "$LATEST_TITLE" ]; then
  echo "Could not detect report title"
  exit 1
fi

LAST_POSTED=""
if [ -f "$STATE_FILE" ]; then
  LAST_POSTED=$(cat "$STATE_FILE")
fi

if [ "$LATEST_TITLE" = "$LAST_POSTED" ]; then
  echo "No new report. Skipping post."
  exit 0
fi

# Fixed tweet format required for this skill (English only)
# Structure:
# [One‑line intro]
#
# [Report title]
#
# Report:
# <URL>
#
# #AI #TechTwitter

# Try to extract a short summary sentence from the site
SUMMARY=$(curl -s "$REPORT_SITE" | grep -m1 -oE '<p[^>]*>[^<]+' | sed 's/<p[^>]*>//')

# Fallback summary if extraction fails
if [ -z "$SUMMARY" ]; then
  SUMMARY="A new report analyzing recent developments in AI systems and governance."
fi

TWEET="New AI research report released.

${LATEST_TITLE}

${SUMMARY}

Report:
${REPORT_SITE}

#AI #TechTwitter"

bash "$TWEET_SCRIPT" "$TWEET" "https://x.com"

# Save latest title
 echo "$LATEST_TITLE" > "$STATE_FILE"

echo "Report posted: $LATEST_TITLE"