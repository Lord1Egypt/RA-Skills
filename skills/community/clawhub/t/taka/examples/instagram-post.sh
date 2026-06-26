#!/bin/bash
# Create an Instagram post with AI-generated image

# Create the creative with auto-generated image
RESULT=$(taka create-creative \
  --name "Summer Vibes" \
  --type instagram \
  --prompt "tropical beach sunset with palm trees, vibrant colors")

echo "$RESULT"

# Extract creative ID
CREATIVE_ID=$(echo "$RESULT" | jq -r '.creative.id')

# Update the caption and hashtags
taka update-content \
  --creative-id "$CREATIVE_ID" \
  --fields '{"caption": "Summer is here! Who else is ready for beach days?", "hashtags": ["summer", "beach", "vibes", "sunset"]}'
