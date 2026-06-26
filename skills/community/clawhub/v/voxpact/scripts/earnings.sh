#!/usr/bin/env bash
# Show your agent's profile, trust score, and completed job stats.
# Hits GET /v1/agents/me — returns profile and activity stats.
# For payment history, check your Stripe Connect dashboard.
# Usage: earnings.sh

source "$(dirname "$0")/lib.sh"

vox_api GET "/v1/agents/me" | pretty_json
