#!/bin/bash
# Create a promotional flyer with AI-generated hero image

# 1. Create the flyer project
RESULT=$(taka create-creative --name "Holiday Sale" --type flyer)
CREATIVE_ID=$(echo "$RESULT" | jq -r '.creative.id')
echo "Created creative: $CREATIVE_ID"

# 2. Build the flyer structure
taka build-flyer \
  --creative-id "$CREATIVE_ID" \
  --template-id seasonal \
  --headline "Holiday Sale" \
  --subtitle "Up to 50% off everything" \
  --tagline "Shop Now" \
  --hero-image-prompt "festive holiday shopping scene with warm lights"

# 3. Generate the hero image
taka generate-flyer-image \
  --prompt "festive holiday shopping scene with gift boxes and warm golden lights" \
  --creative-id "$CREATIVE_ID"

echo "Flyer ready! Creative ID: $CREATIVE_ID"
