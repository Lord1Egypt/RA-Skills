# Hosted Relay Self-Host Guide

This guide explains how to inspect and run the hosted relay source that backs WIP-hosted services such as Codex Remote Control.

The public source lives here:

```text
src/hosted-mcp
```

WIP's production relay runs at `wip.computer`. Self-hosting means running the same relay source on your own domain, with your own database, TLS certificate, process manager, and secrets.

## What The Hosted Relay Does

The hosted relay is a Node server with several surfaces:

- hosted MCP over HTTP at `/mcp`;
- OAuth and passkey login routes;
- demo routes under `/demo`;
- Codex Remote Control pairing and relay routes under `/api/codex-relay/*`;
- health reporting at `/health`.

For Codex Remote Control, the relay lets a local `codex-daemon` dial out to a public server. Browser and phone clients connect to that same public server. After E2EE setup, prompt text, assistant output, command output, and errors are carried as encrypted frames. The relay routes and authorizes frames, but it is not the place where Codex runs.

## Current Self-Host Status

The relay source is inspectable and runnable, but the non-WIP self-host story is not yet a one-command installer.

Important current constraints:

- `server.mjs` currently defaults `ISSUER_URL`, `MCP_RESOURCE_URL`, `RP_ID`, and `RP_ORIGIN` to `wip.computer`;
- the nginx examples are written for the WIP production domain and filesystem layout;
- the Codex Remote Control browser surface at `/codex-remote-control/<threadId>` is served by the WIP web app, not by the hosted-mcp Node process itself;
- `codex-daemon` can point at a custom relay with environment variables, but a complete non-WIP phone/web UI deployment must also point at that same relay.

That means a production self-host should treat this guide as the infrastructure map. Before broad use, parameterize or patch the WIP domain constants for your domain.

## Prerequisites

You need:

- Node.js 20 or newer;
- npm;
- Postgres;
- nginx or another reverse proxy that supports WebSocket upgrades;
- TLS for your domain;
- PM2 or another process manager;
- a public domain such as `relay.example.com`.

Optional demo surfaces may also need:

- `OPENAI_API_KEY`;
- `XAI_API_KEY`.

Codex Remote Control relay operation does not require those demo keys.

## Environment

Start from:

```bash
cd src/hosted-mcp
cp .env.example .env
```

Required:

```bash
DATABASE_URL=postgresql://kaleidoscope:YOUR_PASSWORD@localhost:5432/kaleidoscope
```

Common optional variables:

```bash
MCP_PORT=18800
LDM_HOSTED_MCP_WS_ORIGIN_ALLOWLIST=https://relay.example.com
LDM_HOSTED_MCP_RL_MINT=30
LDM_HOSTED_MCP_RL_VALIDATE=60
LDM_HOSTED_MCP_RL_STATUS=120
```

Development-only variables:

```bash
LDM_HOSTED_MCP_DEV_MODE=1
LDM_HOSTED_MCP_ALLOW_WS_URL_TOKEN=1
```

Do not enable those development flags in production. Production should use Postgres and bearer or ticket authentication, not JSON fallback files or URL token fallback.

## Database Setup

Create a Postgres database and user for the relay. Then run Prisma from `src/hosted-mcp`:

```bash
npm install
npx prisma generate
npx prisma migrate deploy
```

The Prisma schema stores:

- users;
- WebAuthn credentials;
- device tokens;
- wallets;
- API keys.

Production should use Postgres. If Prisma cannot connect and `LDM_HOSTED_MCP_DEV_MODE` is not set, the server fails closed.

## Local Smoke Test

From `src/hosted-mcp`:

```bash
npm install
node server.mjs
```

In another shell:

```bash
curl -fsS http://127.0.0.1:18800/health
```

Expected result: JSON health output from the Node process.

## Process Management

WIP production uses PM2 with:

```text
src/hosted-mcp/ecosystem.config.cjs
```

For a self-host:

```bash
cd src/hosted-mcp
pm2 start ecosystem.config.cjs --update-env
pm2 save
pm2 status mcp-server
```

If you use another process manager, preserve the same contract:

- run `server.mjs` from `src/hosted-mcp`;
- provide `DATABASE_URL`;
- keep the process alive across restarts;
- preserve environment variables on reload;
- verify `/health` after restart.

## Deploy Helper

WIP's production deploy helper is:

```text
src/hosted-mcp/deploy.sh
```

It copies `server.mjs`, supporting modules, static app/demo files, nginx snippets, and package metadata to WIP's VPS, then reloads nginx, reloads PM2, and writes a deploy manifest.

For self-hosting, read it as an example of the file inventory and verification sequence. Do not run it unmodified unless your SSH host, remote directories, nginx layout, PM2 process name, and deploy-manifest path intentionally match the WIP production layout.

## nginx, TLS, And Domain

The production nginx examples live in:

```text
src/hosted-mcp/nginx
```

Key files:

- `codex-relay.conf` contains the `/api/codex-relay/*`, `/pair`, and WebSocket proxy routes;
- `mcp-oauth.conf` and `mcp-server.conf` contain hosted MCP and OAuth routes;
- `wip.computer.conf` shows how WIP includes those snippets inside the public site config;
- `conf.d/redact-logs.conf` defines the redacted access-log format.

For self-hosting:

1. Put TLS in front of your relay domain.
2. Proxy HTTP routes to `http://127.0.0.1:18800`.
3. Preserve WebSocket upgrade headers for `/api/codex-relay/web/` and `/api/codex-relay/daemon`.
4. Use redacted logs so bearer tokens, relay tickets, and API keys do not land in access logs.
5. Replace WIP paths and domains with your own.

Minimum verification:

```bash
sudo nginx -t
sudo systemctl reload nginx
curl -fsS https://relay.example.com/health
```

## Pointing Codex Remote Control At A Custom Relay

`codex-daemon` defaults to WIP's hosted relay. For a custom relay, set the relay endpoints before pairing and starting the daemon:

```bash
export CODEX_DAEMON_RELAY_HTTP=https://relay.example.com
export CODEX_DAEMON_RELAY_WS=wss://relay.example.com/api/codex-relay/daemon
codex-daemon link
codex-daemon start
```

The MCP tool that creates browser links also defaults to WIP's hosted origin. Set this for sessions that should generate links for your relay domain:

```bash
export CODEX_REMOTE_CONTROL_ORIGIN=https://relay.example.com
```

A full non-WIP deployment also needs a browser or phone UI that serves `/codex-remote-control/<threadId>` and talks to the same relay routes. In WIP production, that UI is part of the Kaleidoscope web app.

## Verify The Relay

Use these checks after any deploy:

```bash
curl -fsS https://relay.example.com/health
curl -fsS https://relay.example.com/api/codex-relay/state
```

For WIP production deploys, `scripts/verify-deploy.sh` verifies a deploy manifest against live remote file hashes:

```bash
bash src/hosted-mcp/scripts/verify-deploy.sh latest
```

That script assumes the WIP deploy-manifest layout unless you pass a different manifest and remote.

## What Not To Copy From WIP Production

Do not copy:

- WIP `.env` files;
- WIP Postgres credentials;
- WIP API keys or `ck-` tokens;
- WIP passkey, device, wallet, or user rows;
- WIP PM2 process state;
- WIP nginx certificate paths;
- WIP domain constants without changing them for your domain;
- WIP deploy manifests as proof of your deploy.

Use the source shape, not WIP's production secrets or account data.

## Production Checklist

- Domain and TLS are live.
- `DATABASE_URL` points at your Postgres database.
- Prisma migrations have run.
- `server.mjs` starts without `LDM_HOSTED_MCP_DEV_MODE`.
- nginx proxies `/health`, `/mcp`, `/oauth/*`, `/api/codex-relay/*`, `/pair`, and WebSocket upgrades.
- WebSocket origins are restricted with `LDM_HOSTED_MCP_WS_ORIGIN_ALLOWLIST`.
- URL token fallback is disabled.
- Access logs redact bearer tokens, relay tickets, and `ck-` values.
- `codex-daemon link` completes against your domain.
- `codex-daemon start` reports relay paired.
- Browser links are generated for your domain, not `wip.computer`.

## Open Work

The remaining product work is to turn this infrastructure map into a first-class self-host installer:

- parameterize issuer and WebAuthn relying party settings;
- package the phone/web Remote Control UI for non-WIP domains;
- add a guided `ldm` self-host profile;
- add an end-to-end self-host smoke test that pairs a daemon and browser through a non-WIP domain.
