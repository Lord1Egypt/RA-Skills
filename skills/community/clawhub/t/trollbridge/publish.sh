#!/bin/bash
# Retry ClawHub publish for the TrollBridge skill.
# Blocked 2026-10-08 by ClawHub's 14-day GitHub account age gate ("try again in 3 days").
# Earliest retry: ~2026-10-11/12. Just re-run this script; it publishes and verifies.
set -e
cd ~/workspace/revenue-agent/clawhub-skill
clawhub skill publish . \
  --slug trollbridge-x402-intel \
  --name "TrollBridge x402 Intel" \
  --version 1.0.0 \
  --changelog "Initial release: 100-lane x402 pay-per-call crypto intel feed for OpenClaw agents" \
  --tags latest,x402,crypto,defi,api \
  --categories development,finance \
  --topics "x402,pay-per-call,crypto-intel,defi,base"
echo "--- verifying ---"
clawhub search "trollbridge" --limit 3
echo "Expected live URL: https://clawhub.ai/skills/trollbridge-x402-intel"
