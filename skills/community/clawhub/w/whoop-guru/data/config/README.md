# Credentials Directory

This directory stores user credentials at runtime:
- `llm_config.json`: LLM API keys (user-configured via chat)
- `whoop-tokens.json`: NOT stored here - WHOOP tokens stored at `~/.clawdbot/whoop-tokens.json`

**Note**: WHOOP OAuth tokens are automatically stored by `scripts/whoop_auth.py` at `~/.clawdbot/whoop-tokens.json`. The WHOOP fetcher script (`lib/whoop-fetcher.sh`) also uses `~/.clawdbot/whoop-credentials.env`.
