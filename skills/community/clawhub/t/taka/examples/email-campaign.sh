#!/bin/bash
# Build a complete email campaign

# 1. Create the email project
RESULT=$(taka create-creative --name "Welcome Email" --type email)
CREATIVE_ID=$(echo "$RESULT" | jq -r '.creative.id')
echo "Created creative: $CREATIVE_ID"

# 2. Build the email structure
taka build-email \
  --creative-id "$CREATIVE_ID" \
  --template-id welcome \
  --subject "Welcome to Our Community!" \
  --preheader "We are excited to have you on board" \
  --global-style '{"backgroundColor":"#f4f4f5","contentWidth":600,"fontFamily":"Arial","fontColor":"#333333"}' \
  --sections '[
    {"type":"hero","content":{"title":"Welcome!","subtitle":"We are so glad you joined us"}},
    {"type":"text","content":{"body":"Thanks for signing up. Here is what you can expect from us: great content, exclusive offers, and helpful tips."}},
    {"type":"button","content":{"text":"Get Started","url":"https://example.com"}}
  ]' \
  --footer '{"businessName":"My Business","showUnsubscribe":true,"showViewInBrowser":true}'

# 3. Generate a hero image
taka generate-email-image \
  --section-id hero-0 \
  --prompt "welcoming and warm email banner with confetti and celebration" \
  --aspect-ratio 16:9 \
  --creative-id "$CREATIVE_ID"

echo "Email campaign ready! Creative ID: $CREATIVE_ID"
