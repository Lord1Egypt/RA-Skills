# OpenClaw Integration Guide

This guide helps you connect RuRussian MCP to OpenClaw bots for Russian tutoring and self-service paid activation.

## Prerequisites

- Python 3.9+
- OpenClaw installed and running
- A RuRussian API key from the official account dashboard, or a RuRussian account email for checkout

## Step 1: Install the MCP Server

```bash
pip install rurussian-mcp
```

If you run OpenClaw in a virtual environment, install `rurussian-mcp` in that same environment.

## Step 2: Configure OpenClaw

Open your `~/.openclaw/config.json` and add the server entry:

```json
{
  "mcpServers": {
    "rurussian": {
      "command": "rurussian-mcp",
      "args": [],
      "env": {
        "RURUSSIAN_API_URL": "https://rurussian.com/api",
        "RURUSSIAN_API_KEY": "YOUR_BOT_API_KEY"
      }
    }
  }
}
```

Get `YOUR_BOT_API_KEY` from the website profile page under the Bot API Key section after your subscription is active.
You can also copy [openclaw_config.json](../examples/openclaw_config.json) as a starting template.

## Step 3: Key Flow in Bot Runtime

- If you already have a key:
  - The cleanest path is to preload `RURUSSIAN_API_KEY` in the OpenClaw config.
  - Call `authenticate(api_key, user_agent?)`.
- If you do not have a key:
  - Call `list_pricing_plans()` if you need to compare options first.
  - Call `create_key_purchase_session(email, plan, success_url?, cancel_url?)`.
  - Send `checkout_url` to the user or let a payment-capable bot open it directly.
  - After hosted checkout finishes, get `session_id` from the success redirect URL if it was not returned immediately.
  - Call `confirm_key_purchase(session_id)` to unlock the MCP session without exposing the raw key in tool output.

## Step 4: Learning Tools

After authentication, call tools like `get_word_data`, `get_sentences`, `analyze_sentence`, `generate_zakuska`, and `translate_text`.
For `generate_zakuska`, pass `learner_email` because the latest backend binds Zakuska generation to a learner account and saved Rusvibe state.

## Telegram Setup Flow

- Create a Telegram bot with BotFather.
- Connect your bot token in OpenClaw.
- Add startup logic:
  - Check `authentication_status`.
  - If not authenticated, prompt for an existing key or offer `list_pricing_plans` plus the purchase flow when the user asks to buy.
- Route learner prompts to RuRussian tools based on intent:
  - Vocabulary lookup → `get_word_data`
  - Grammar breakdown → `analyze_sentence`
  - Practice content → `generate_zakuska` with `learner_email`

## Discord Setup Flow

- Create a Discord bot application and invite it to your server.
- Connect it to OpenClaw.
- Add first-message hook:
  - Check `authentication_status`.
  - If not authenticated, request an existing key or offer `list_pricing_plans` plus the purchase flow when the user asks to buy.
- Route slash commands or messages:
  - `/word <term>` → `get_word_data`
  - `/translate <text>` → `translate_text`
  - `/analyze <sentence>` → `analyze_sentence`
  - `/zakuska <email>` → `generate_zakuska`

## Advanced Usage

- Set custom user agent:
  - Pass `user_agent` in `authenticate` for analytics segmentation.
- Use a custom API backend:
  - Set `RURUSSIAN_API_URL` when you need an alternate endpoint.
- Override purchase endpoint paths:
  - Set `RURUSSIAN_BUY_SESSION_ENDPOINTS`.
  - Set `RURUSSIAN_CONFIRM_PURCHASE_ENDPOINTS`.

## Common Issues

- Authentication required
  - You called another tool before key setup.
- Purchase endpoint not found
  - Configure `RURUSSIAN_BUY_SESSION_ENDPOINTS` and `RURUSSIAN_CONFIRM_PURCHASE_ENDPOINTS`.
- Invalid API key
  - Re-run `confirm_key_purchase` after payment or use a valid key in `authenticate`.
- Payment confirmed but no key returned
  - This backend can still unlock the MCP session in checkout-backed mode after `confirm_key_purchase`.
- Python runtime mismatch
  - Use Python 3.9 or newer.
- Tool command not available
  - Reinstall in the same environment used by OpenClaw.
