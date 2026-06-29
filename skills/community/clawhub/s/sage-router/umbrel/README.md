# Sage Router for Umbrel

Sage Router is a self-hosted, multi-provider AI router for Umbrel. It
discovers available LLM providers (OpenAI, Anthropic, Google, OpenRouter,
Ollama, NVIDIA NIM, Darkbloom, GitHub Copilot) and routes requests
intelligently based on intent, model capabilities, cost, and provider health.

The Umbrel app uses the upstream `ghcr.io/earlvanze/sage-router` image and
mounts the host OpenClaw config so OpenClaw Codex OAuth works out of the
box.

## OpenClaw Codex OAuth

Sage Router reads the OpenAI OAuth token from
`~/.openclaw/agents/main/agent/auth-profiles.json` (the same token OpenClaw
uses for Codex) and uses it to call `chatgpt.com/backend-api/codex/responses`
directly. There is no gateway subprocess hop, no token refresh helper, and no
separate Codex auth code path. If you sign into Codex via OpenClaw, Sage
Router picks up the same credentials.

When the OAuth token is not present, Sage Router falls back to the OpenClaw
gateway bridge so existing setups continue to work.

## First-time setup

1. Install the Sage Router app from the Umbrel Community App Store.
2. On your Umbrel host, copy your OpenClaw auth profile directory into the
   app's data volume so the OAuth token is reachable from inside the
   container:

   ```sh
   sudo mkdir -p /umbrel/apps/sage-router/data/openclaw
   sudo cp -r ~/.openclaw/agents /umbrel/apps/sage-router/data/openclaw/
   ```

3. Open the Sage Router dashboard from the Umbrel app page. Provider
   discovery runs automatically and lists every model from your auth
   profiles.
4. (Optional) Open the `/admin` panel on the dashboard to enable Ollama
   local model pulls, Dario Claude proxying, and OpenRouter free-only mode.

## Built-in dashboard

The dashboard at port 8790 (Umbrel forwards it automatically) shows:

- Live provider list with model counts and capability flags
- Per-provider health and recent request history
- Latency histogram and intent-based routing breakdown
- API key management (free/lite/pro/max/metered plans)
- Stripe billing integration (configure via `STRIPE_SECRET_KEY` and
  `STRIPE_WEBHOOK_SECRET` in the Umbrel app environment)

## Configuration

Optional environment variables (set in the Umbrel app's environment
settings):

| Variable | Default | Description |
|----------|---------|-------------|
| `SAGE_ROUTER_BUNDLED_OLLAMA_AUTOSTART` | 0 | Auto-start bundled Ollama in-container |
| `SAGE_ROUTER_OLLAMA_AUTO_PULL_PATTERNS` | `:cloud` | Auto-pull Ollama model patterns |
| `SAGE_ROUTER_DARIO_AUTOSTART` | 0 | Auto-start Dario Claude proxy |
| `SAGE_ROUTER_OPENROUTER_FREE_ONLY` | 1 | Prefer free OpenRouter models |
| `STRIPE_SECRET_KEY` | (unset) | Stripe API key for billing |
| `STRIPE_WEBHOOK_SECRET` | (unset) | Stripe webhook signing secret |

## Local development

The upstream repo ships a `docker-compose.yml` for non-Umbrel deployments.
Run `docker compose up -d` from the repo root after copying your
`~/.openclaw` directory into `./data/openclaw`.

## Links

- Source: https://github.com/earlvanze/sage-router
- Issues: https://github.com/earlvanze/sage-router/issues
- OpenClaw: https://github.com/openclaw/openclaw
- Umbrel: https://umbrel.com
