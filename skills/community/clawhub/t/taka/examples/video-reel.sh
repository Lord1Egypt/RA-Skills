#!/bin/bash
# Generate a short video for Instagram Reels

# Generate a vertical video (9:16 for Reels/TikTok/Shorts)
taka generate-video \
  --prompt "smooth coffee pour into a ceramic mug, steam rising, cozy atmosphere" \
  --duration 5 \
  --aspect-ratio 9:16

# Or generate and associate with a creative
RESULT=$(taka create-creative --name "Coffee Reel" --type instagram)
CREATIVE_ID=$(echo "$RESULT" | jq -r '.creative.id')

taka generate-video \
  --prompt "smooth coffee pour into a ceramic mug, steam rising" \
  --duration 7 \
  --aspect-ratio 9:16 \
  --creative-id "$CREATIVE_ID"

taka update-content \
  --creative-id "$CREATIVE_ID" \
  --fields '{"caption": "Morning ritual", "hashtags": ["coffee", "morningroutine", "reels"]}'
