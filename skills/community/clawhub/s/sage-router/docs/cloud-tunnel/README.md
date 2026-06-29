# Sage Cloud Tunnel

Sage Cloud Tunnel is the privacy-preserving hosted convenience layer for Sage Router.

It gives users a hosted OpenAI-compatible endpoint without collecting their provider API keys, OAuth tokens, cookies, or subscription credentials.

## Architecture

```text
Client app
  -> Cloudflare Worker /v1/chat/completions
  -> Durable Object tunnel
  -> user's local connector WebSocket
  -> user's local Sage Router
  -> user's own provider subscriptions
```

Credentials stay on the user's machine. Sage Cloud only relays request/response bytes through an authenticated tunnel.

## Monetization

Charge for the hosted relay/control plane, not inference resale:

- hosted low-latency endpoint
- connector uptime/health checks
- team routing policy sync
- analytics and reliability dashboard
- support/private deployment

## Deploy Worker

```bash
cd edge/cloudflare-ai-tunnel
npx wrangler secret put SAGE_TUNNEL_TOKEN
npx wrangler deploy
```

## Run local connector

```bash
SAGE_TUNNEL_URL=wss://sage-ai-tunnel.<account>.workers.dev/tunnel/connect \
SAGE_TUNNEL_TOKEN='<same secret>' \
SAGE_TUNNEL_LOCAL_BASE_URL=http://127.0.0.1:8790 \
node scripts/sage_tunnel_connector.mjs
```

## Call hosted endpoint

```bash
curl https://sage-ai-tunnel.<account>.workers.dev/v1/chat/completions \
  -H 'Authorization: Bearer <same secret>' \
  -H 'Content-Type: application/json' \
  -d '{"model":"auto","messages":[{"role":"user","content":"hello"}]}'
```

## Security properties

- No provider credentials collected by Sage Cloud.
- No provider OAuth/token/cookie custody.
- User can disconnect by stopping the connector.
- Worker stores no prompts by default.
- Token can be rotated at Cloudflare and locally.

## MVP limitation

This MVP uses one shared tunnel token and one connector per Worker namespace. Production should add per-user tunnels, token hashing, usage metering, wallet/crypto payments, rate limits, and optional org/team policy sync.
