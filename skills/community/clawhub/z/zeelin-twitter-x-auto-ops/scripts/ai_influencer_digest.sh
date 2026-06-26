#!/bin/bash

# Opens key AI influencer timelines to quickly scan latest posts
# Useful for generating a summary tweet based on their recent activity

ACCOUNTS=(
"https://x.com/sama"
"https://x.com/OpenAI"
"https://x.com/AnthropicAI"
"https://x.com/karpathy"
"https://x.com/ylecun"
"https://x.com/rowancheung"
)

for url in "${ACCOUNTS[@]}"; do
  open "$url"
done

echo "Opened AI influencer timelines. Review latest tweets and generate a summary tweet like:"
echo "AI update:"
echo ""
echo "Key things happening today in AI:"
echo "• model updates"
echo "• new research"
echo "• startup activity"
echo ""
echo "Interesting momentum in the AI ecosystem."