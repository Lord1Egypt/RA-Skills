#!/bin/bash
# Wrapper for Sage Planning Trainer Cron Job

OUTPUT_FILE="/tmp/sage_trainer_$(date +%s).txt"

# Run Sage Planning in Train Mode
# Using a random topic or a specific one if provided
TOPIC="Project Management for AI Agents"
if [ ! -z "$1" ]; then
  TOPIC="$1"
fi

echo "Generating training scenario for topic: $TOPIC"
node skills/sage-planning/index.js --mode train --task "$TOPIC" > "$OUTPUT_FILE"

# Check if generation succeeded
if [ -s "$OUTPUT_FILE" ]; then
  # Send to Master via Feishu Post
  # target: ou_cdc63fe05e88c580aedead04d851fc04 (Master)
  node skills/feishu-post/send.js \
    --target "ou_cdc63fe05e88c580aedead04d851fc04" \
    --title "🧙‍♂️ 大贤者：今日思维特训" \
    --text-file "$OUTPUT_FILE"
    
  echo "Training scenario sent to Feishu."
  rm "$OUTPUT_FILE"
else
  echo "Error: Sage Planning failed to generate output."
  exit 1
fi
