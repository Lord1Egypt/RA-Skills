---
name: sentinel-custom-provider-check
description: >
  Verifies that Sentinel's PII/secret redaction guardrail survives routing
  through CUSTOM_PROVIDERS to a self-hosted OpenAI-compatible backend (vLLM,
  TGI, Ollama, or anything speaking /v1/chat/completions) — not just
  Sentinel's first-party Anthropic/OpenAI/Google routes. Starts the local
  Sentinel gateway container with CUSTOM_PROVIDERS pointed at the backend,
  sends a synthetic-PII probe straight through it, and reads the backend's
  own raw response to confirm the guardrail actually fired on that hop.
  Use when: user says "check if Sentinel redacts through my custom model",
  "verify Sentinel guardrails on my self-hosted backend", "test
  CUSTOM_PROVIDERS redaction", or "does my vLLM/Ollama server see PII".
---

# Sentinel CUSTOM_PROVIDERS Redaction Check

When the user wants to confirm Sentinel's redaction guardrail actually
reaches a self-hosted backend wired up via `CUSTOM_PROVIDERS` — not just
Sentinel's built-in provider integrations — guide them through the steps
below in order.

## Why this check needs a specific method (read before running)

Do **not** verify this by pasting real PII into a chat with Claude and
reading Claude's own reply. If that Claude session is itself routed through
a Sentinel gateway (common in OpenClaw setups), its own gateway redacts
inbound PII-shaped text on the way in — independent of whatever the custom
backend actually did with it. That makes an unrelated pass-through look
like a successful redaction test.

The only valid check is reading the raw JSON response **the backend itself
produced**, on a channel nothing else can re-redact. That's what
`skill.py`'s `_probe_backend()` does: it calls the gateway's
OpenAI-compatible endpoint directly over HTTP and inspects the response body
for the literal `{{REDACTED}}` marker vs. the leaked probe values.

## What You Need From the User

1. **A running self-hosted OpenAI-compatible backend**, reachable at a
   public URL — a tunnel (ngrok, Cloudflare Quick Tunnel) is fine for
   testing; a stable deployment for anything recurring.
2. **The provider name and model** the backend serves
   (e.g. `vllm-colab`, `Qwen/Qwen2.5-3B-Instruct`).
3. **Docker Desktop running locally** — Sentinel's local gateway always runs
   as a container, even via the CLI.
4. **Sentinel installed and logged in.** If the user doesn't already have
   Sentinel set up, point them to
   [https://docs.superwise.ai/docs/getting-started](https://docs.superwise.ai/docs/getting-started)
   before continuing. Confirm `sentinel gateway start --help` works before
   starting this skill — don't assume Sentinel is already present.

## Step 1 — Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file in the skill root:

```
CUSTOM_PROVIDER_BASE_URL=https://<your-tunnel-or-deployment>
CUSTOM_PROVIDER_NAME=vllm-colab
CUSTOM_PROVIDER_MODEL=Qwen/Qwen2.5-3B-Instruct
SENTINEL_GATEWAY_PORT=8100
TELEGRAM_BOT_TOKEN=<copy from your OpenClaw config — no separate bot needed>
TELEGRAM_CHAT_ID=<copy from your OpenClaw config — no separate bot needed>
```

Telegram delivery is optional — if left unset, the skill still runs and prints its
result to stdout instead.

## Step 2 — Run the check

```bash
python -c "from skill import run; print(run())"
```

This will:
1. Stop any existing local Sentinel gateway container and restart it with
   `CUSTOM_PROVIDERS` pointed at `CUSTOM_PROVIDER_BASE_URL` (reuses the
   cached `sentinel_id` — this is not a fresh registration).
2. Poll `/{provider}/v1/models` until the gateway is reachable.
3. POST a prompt containing a synthetic email + phone number to
   `/{provider}/v1/chat/completions`, asking the model to echo them back.
4. Inspect the raw response for `{{REDACTED}}` vs. the literal probe values.
5. Send a pass/fail summary via OpenClaw's existing Telegram connection.

## Step 3 — Register as an OpenClaw skill

Register using the metadata in `skill.py`:
- **Trigger command:** `/sentinel_custom_check`
- **What it needs from the environment:** the four `CUSTOM_PROVIDER_*` /
  `SENTINEL_GATEWAY_PORT` vars above, plus OpenClaw's existing Telegram vars.

## Interpreting results

- **Passed:** response contained `{{REDACTED}}` and neither the probe email
  nor phone number appeared anywhere in the backend's own output. The
  guardrail intercepted the PII before it reached the custom backend.
- **Failed:** either the probe values leaked through, or no `{{REDACTED}}`
  marker appeared at all (check `CUSTOM_PROVIDER_BASE_URL` reachability and
  that the gateway actually restarted with the new config — a stale
  container from a previous run is the most common cause).

## Background / provenance

This skill formalizes a manual test run on 2026-08-19 against a
Qwen2.5-3B-Instruct vLLM server on a Colab T4, chained through Cloudflare +
a local Sentinel gateway + ngrok. See
`../vllm_sentinel_custom_provider.ipynb` for the backend half (vLLM +
ngrok) and `../redaction_relay_flow.png` / `../redaction-relay.png` for a
diagram of the full chain. The original manual test confirmed the guardrail
held; this skill makes that check repeatable without re-deriving the
Cloudflare/Docker/ngrok wiring by hand each time.

## Troubleshooting

- **Gateway never becomes reachable:** confirm Docker Desktop is running —
  `sentinel gateway start` always launches a container, so a bare
  `localhost` process on the host is never what answers.
- **`CUSTOM_PROVIDER_BASE_URL` unreachable from the gateway container:** on
  macOS Docker Desktop, a same-machine backend needs `host.docker.internal`,
  not `localhost`, as the base URL.
- **Backend's `/health` check hangs:** some OpenAI-compatible servers (vLLM
  included) return HTTP 200 with an **empty body** on `/health` — this skill
  doesn't call `/health` directly, but if you extend it to poll one, don't
  call `.json()` on it.
- **Probe passes once, then silently starts failing:** the gateway container
  may not have picked up an updated `CUSTOM_PROVIDER_BASE_URL` — this skill
  always stops and restarts the container rather than assuming a running one
  has current config; confirm your `.env` change was saved before the run.
