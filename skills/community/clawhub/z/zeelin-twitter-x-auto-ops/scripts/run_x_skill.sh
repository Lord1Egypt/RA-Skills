#!/bin/bash

# run_x_skill.sh
# One-command workflow for ZeeLin Twitter / X Self-Ops Skill

BASE_DIR="/Users/youke/.openclaw/workspace/skills/x-auto-growth/scripts"
POST_SCRIPT="/Users/youke/.openclaw/workspace/skills/zeelin-twitter-web-autopost/scripts/tweet.sh"

echo "=== ZeeLin Twitter/X Self-Ops Skill ==="

echo "Step 1: Discover AI trends"
bash "$BASE_DIR/ai_trend_autotweet.sh"

echo "Step 2: Open AI influencer timelines"
bash "$BASE_DIR/ai_influencer_digest.sh"

echo "Step 3: Open high-engagement AI tweets for quote opportunities"
bash "$BASE_DIR/quote_ai_tweet.sh"

echo "Step 4: Open follow-back growth threads"
bash "$BASE_DIR/comment_follow_growth.sh"

echo ""
read -p "Enter tweet text to publish automatically (or press Enter to skip): " TWEET

if [ -n "$TWEET" ]; then
  echo "Publishing tweet..."
  bash "$POST_SCRIPT" "$TWEET" "https://x.com"
else
  echo "No tweet entered. Skipping publish step."
fi

echo "=== Workflow complete ==="