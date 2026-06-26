# Solar Delegation Setup Guide

## Prerequisites

- OpenClaw installed and onboarded
- Node.js 18+
- Primary model API key (for planning/tool calls)
- OpenRouter API key (for Solar Pro3 text generation)

## Step 1: Get API Keys

### Primary Model Key
Use your primary provider key (for example, Anthropic).

### OpenRouter API Key
1. Go to https://openrouter.ai
2. Sign up / log in
3. Create API key
4. Copy the `sk-or-...` key
5. Solar Pro3 model reference: https://openrouter.ai/upstage/solar-pro-3

## Step 2: Configure OpenClaw

### Register primary-provider auth
Use the auth command for your primary provider.

Example:
```bash
openclaw auth add anthropic
```

### Add OpenRouter provider to config

Add under `models.providers`:

```json
"openrouter": {
  "baseUrl": "https://openrouter.ai/api/v1",
  "apiKey": "sk-or-YOUR-KEY-HERE",
  "api": "openai-completions",
  "models": [{
    "id": "upstage/solar-pro-3",
    "name": "Solar Pro3",
    "input": ["text"],
    "contextWindow": 128000,
    "maxTokens": 16384,
    "reasoning": false,
    "cost": {
      "input": "CHECK_OPENROUTER",
      "output": "CHECK_OPENROUTER",
      "cacheRead": "CHECK_OPENROUTER",
      "cacheWrite": "CHECK_OPENROUTER"
    }
  }]
}
```

### Add model alias/allowlist

Add under `agents.defaults.models`:

```json
"openrouter/upstage/solar-pro-3": {
  "alias": "solar-pro3"
}
```

### Set primary model

Keep your primary model set to the model used for planning/tool orchestration.

## Step 3: Configure Delegation Policy

Store delegation policy in persistent memory/config used by your environment.

Recommended baseline:

```markdown
## Solar Delegation Policy
- default threshold: 200
- optional per-session overrides
- if no override exists, use default
```

Threshold guidance:
- `0`: delegate all responses
- `200`: delegate medium/long responses (recommended baseline)
- higher values (e.g., `500`, `1000`): delegate less often

## Step 4: Restart / Reload

```bash
openclaw gateway restart
```

## Runtime Pattern

```text
User Request
  → Primary model (analyze/plan)
    ├─ estimated output < threshold  → direct response
    └─ estimated output >= threshold → sessions_spawn(Solar Pro3)
```

## Troubleshooting

- **Output too short/truncated**: increase `maxTokens` for Solar model
- **Responses are slower**: delegation adds spawn + generation latency
- **Quality mismatch**: raise threshold so only longer drafts are delegated
- **Delegate less often**: increase threshold (for example 500+)
