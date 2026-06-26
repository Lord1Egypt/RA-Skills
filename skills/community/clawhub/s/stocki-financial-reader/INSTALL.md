# stocki-financial-reader — Install & Setup

## Install

### SkillHub (recommended)

```bash
curl -fsSL https://skillhub.cn/install/install.sh | bash
skillhub install stocki-financial-reader
```

If the installation fails, see latest instructions at the project repo.

## Configure

Set the required environment variables in `~/.bashrc` (or `~/.zshrc`):

```bash
export STOCKI_GATEWAY_URL="https://skill.stocki.com.cn"
export STOCKI_API_KEY="sk_your_key_here"
```

For local development against a stocki gateway running locally:

```bash
export STOCKI_GATEWAY_URL="http://localhost:9996"
export STOCKI_API_KEY="sk_dev_any_string"   # localhost does not validate
```

## Verify

Run the self-diagnostic and connectivity smoke test:

```bash
python3 ~/.openclaw/workspace/skills/stocki-financial-reader/scripts/doctor.py
python3 ~/.openclaw/workspace/skills/stocki-financial-reader/scripts/diagnose.py
```

Expected: both exit 0. Exit codes:

| Code | Meaning |
|---|---|
| 0 | OK |
| 1 | Auth invalid |
| 2 | Unreachable (TCP/DNS) |
| 3 | Stocki gateway unavailable (5xx / timeout) |
| 4 | Rate limited / quota exceeded |

## Update

```bash
skillhub install stocki-financial-reader
```

## API Key & Privacy

- **Credential handling**: API keys are issued per user and are equivalent to identity credentials. Do NOT embed them in source code, commits, chat logs, or public configuration. If exposed, rotate immediately via your stocki account's key management.
- **Data flow**: This skill does NOT collect PII on its own. But content the agent embeds in queries (user descriptions, conversation context, etc.) is sent over HTTP to the stocki gateway and is subject to stocki's privacy policy. Mask or strip PII before sending in sensitive scenarios.
