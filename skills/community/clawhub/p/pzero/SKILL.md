---
name: pzero
description: >-
  Point OpenClaw at PZERO prepaid inference. OpenAI-compatible chat completions,
  Bearer pzero_ key, custom provider (not a bundled OpenClaw plugin). Use when
  the user wants cheaper privacy-first models on a prepaid USDC balance.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - PZERO_API_KEY
      bins:
        - curl
    primaryEnv: PZERO_API_KEY
    envVars:
      - name: PZERO_API_KEY
        required: true
        description: Studio or agent key. Prefix pzero_. Confirmed USDC required before inference.
    homepage: https://pzero.studio/agents
---

# PZERO (OpenClaw custom provider)

PZERO is prepaid inference: chat, image, and video on one USDC balance. Venice-only upstream. This skill covers OpenClaw chat via the generic custom-provider seam. OpenClaw does not need a PZERO plugin.

Sign-in is free. Usage is paid. Minimum top-up is 1 USDC on Base. There are no starter credits. Every AI Credit is at least 20% off $1 list.

Get a key: https://pzero.studio/agents

OpenClaw generic custom-provider docs: https://docs.openclaw.ai/gateway/config-tools#custom-providers-and-base-urls

## Apply this config

Merge into `openclaw.json` (or the agent `models.json`). Replace `YOUR_MODEL_ID` with a live text id from `GET https://api.pzero.studio/v1/models`. Default on the Agents landing is `deepseek-v4-flash`.

```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "pzero": {
        "baseUrl": "https://api.pzero.studio/v1",
        "apiKey": "${PZERO_API_KEY}",
        "api": "openai-completions",
        "models": [
          {
            "id": "YOUR_MODEL_ID",
            "name": "YOUR_MODEL_ID",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 128000,
            "maxTokens": 8192
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "pzero/YOUR_MODEL_ID"
      },
      "models": {
        "pzero/YOUR_MODEL_ID": {}
      }
    }
  }
}
```

If `GET /v1/models` lists `supports_vision: true` for that id, set `"input": ["text", "image"]`.

Do not set `api` to `openai-responses` unless you have verified that OpenClaw path against PZERO `POST /v1/responses`. The supported OpenClaw adapter for this recipe is `openai-completions` (`POST /v1/chat/completions`).

`PZERO_API_KEY` must be a `pzero_` key with confirmed USDC. Pending top-ups are not spendable.

## Smoke test

Origin (public, no key):

```bash
curl -sS "https://api.pzero.studio/v1/models"
```

First paid call (needs confirmed balance):

```bash
curl -sS -X POST "https://api.pzero.studio/v1/chat/completions" \
  -H "Authorization: Bearer $PZERO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek-v4-flash","messages":[{"role":"user","content":"Hello from PZERO"}],"stream":false}'
```

A `200` means the key and balance work. Then restart or reload OpenClaw so it picks up `models.providers.pzero`.

## MCP (optional)

Same credits, hosted connector: `https://mcp.pzero.studio/mcp` with `Authorization: Bearer $PZERO_API_KEY`. Human docs: https://docs.pzero.studio/agents/mcp

## Not this skill

Do not add a bundled OpenClaw provider id, `openclaw onboard --auth-choice`, or a `docs/providers/pzero.md` core patch. ClawSweeper closed that as ClawHub-scoped. This recipe is the maintainable path.
