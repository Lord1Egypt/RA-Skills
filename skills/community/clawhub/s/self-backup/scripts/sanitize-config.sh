#!/bin/bash

# Sanitize OpenClaw config for backup
# Removes sensitive tokens/keys while preserving structure

CONFIG_FILE="$1"
OUTPUT_FILE="$2"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Config file not found: $CONFIG_FILE"
    exit 1
fi

if ! command -v jq &> /dev/null; then
    echo "Error: jq is required for config sanitization"
    echo "Install with: sudo apt install jq  OR  brew install jq"
    exit 1
fi

# Use jq to sanitize sensitive fields
jq '
# Remove all tokens and sensitive keys
(.channels.telegram.botToken // empty) = "TELEGRAM_BOT_TOKEN_REDACTED" |
(.channels.discord.token // empty) = "DISCORD_BOT_TOKEN_REDACTED" |
(.gateway.auth.token // empty) = "GATEWAY_AUTH_TOKEN_REDACTED" |

# Remove any API keys in auth profiles
.auth.profiles = (.auth.profiles | with_entries(
  .value |= (
    if has("apiKey") then .apiKey = "API_KEY_REDACTED"
    elif has("token") then .token = "TOKEN_REDACTED"
    else . end
  )
)) |

# Remove sensitive model provider keys
.models.providers = (.models.providers | with_entries(
  .value |= (
    if has("apiKey") then .apiKey = "API_KEY_REDACTED"
    else . end
  )
))
' "$CONFIG_FILE" > "$OUTPUT_FILE"

if [ $? -eq 0 ]; then
    echo "Config sanitized: $OUTPUT_FILE"
else
    echo "Error: Failed to sanitize config"
    exit 1
fi