#!/usr/bin/env bash
# openclaw-smartlead skill setup helper
#
# Usage:
#   ./setup.sh
#
# Optional env vars before running:
#   SMARTLEAD_API_KEY
#   OPENCLAW_HOOKS_TOKEN
#   OPENCLAW_GATEWAY_BASE_URL   (default: http://127.0.0.1:18789)
#   SMARTLEAD_WEBHOOK_PUBLIC_URL (e.g. https://gateway.example.com/smartlead/webhook)

set -euo pipefail

PLUGIN_DIR="/home/worker/code/openclaw-smartlead"
GATEWAY_BASE_URL="${OPENCLAW_GATEWAY_BASE_URL:-http://127.0.0.1:18789}"
SMARTLEAD_WEBHOOK_PUBLIC_URL="${SMARTLEAD_WEBHOOK_PUBLIC_URL:-https://your-openclaw-host.example.com/smartlead/webhook}"

echo "Setting up openclaw-smartlead..."
echo ""

if command -v openclaw >/dev/null 2>&1; then
  echo "Installing plugin in linked mode..."
  openclaw plugins install -l "$PLUGIN_DIR" || true
  openclaw plugins enable smartlead || true
else
  echo "openclaw CLI not found. Skipping plugin install commands."
fi

echo ""
echo "Recommended OpenClaw config (hooks mapping + plugin):"
cat <<EOF
{
  "hooks": {
    "enabled": true,
    "token": "\${OPENCLAW_HOOKS_TOKEN}",
    "path": "/hooks",
    "mappings": [
      {
        "id": "smartlead-reply",
        "match": { "path": "smartlead", "source": "smartlead" },
        "action": "agent",
        "wakeMode": "now",
        "name": "Smartlead Reply",
        "sessionKey": "hook:smartlead:{{campaign_id}}:{{lead_id}}",
        "messageTemplate": "New lead answer\\nCampaign: {{campaign_name}} ({{campaign_id}})\\nLead: {{lead_email}}\\nPreview: {{preview_text}}\\n\\nFetch and summarize prior conversation using smartlead CLI.",
        "deliver": true,
        "channel": "slack"
      }
    ]
  },
  "plugins": {
    "entries": {
      "smartlead": {
        "enabled": true,
        "config": {
          "webhookSecret": "<optional-smartlead-secret>",
          "inboundWebhookPath": "/smartlead/webhook"
        }
      }
    }
  }
}
EOF

echo ""
echo "Smartlead campaign webhook request body example:"
cat <<EOF
{
  "id": null,
  "name": "OpenClaw Reply Alerts",
  "webhook_url": "${SMARTLEAD_WEBHOOK_PUBLIC_URL}",
  "event_types": ["EMAIL_REPLY"],
  "categories": ["Interested"]
}
EOF

echo ""
echo "Optional branching transform:"
echo "  copy ${PLUGIN_DIR}/examples/hooks-transforms/smartlead-reply-branch.example.js \\"
echo "    ~/.openclaw/hooks/transforms/smartlead-reply-branch.js"
echo "  then set hooks.mappings[].transform.module = \"smartlead-reply-branch.js\""
echo ""
echo "Optional: install smartlead-cli for manual debugging (not required by the plugin):"
if command -v uv >/dev/null 2>&1; then
  echo "  uv tool install smartlead-cli"
elif command -v pip3 >/dev/null 2>&1; then
  echo "  pip3 install --user smartlead-cli"
else
  echo "  (uv/pip3 not found)"
fi

echo ""
echo "Next steps:"
echo "1) Set SMARTLEAD_API_KEY and OPENCLAW_HOOKS_TOKEN"
echo "2) Add the config snippet to your OpenClaw config"
echo "3) Create/update the Smartlead campaign webhook to point at /smartlead/webhook"
echo "4) Test with a Smartlead EMAIL_REPLY webhook (plugin -> /hooks/smartlead mapping)"
