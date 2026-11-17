# Hosted MCP And Relay

This directory contains the public source for the hosted WIP relay that serves `wip.computer`.

It includes:

- OAuth, passkey, and hosted MCP routes in `server.mjs`;
- Codex Remote Control relay routes under `/api/codex-relay/*`;
- nginx snippets for the relay, MCP, and site proxy;
- Prisma schema and migrations for Postgres-backed account, API key, passkey, device, and wallet state;
- PM2 and deploy helpers for the WIP-operated VPS.

WIP runs the production hosted relay so user setup is easy and works across networks. The source is public so users can inspect the relay path and build their own infrastructure.

## Codex Remote Control WebSocket Abuse Limits

The browser relay path enforces app-layer limits after a Remote Control ticket attaches:

- max browser frame bytes;
- max messages per rate window;
- max browser bytes per rate window;
- max malformed browser frames;
- max pending bytes on the daemon socket before forwarding;
- max browser sockets per `(tenant id, thread id)`;
- idle connection TTL;
- env-driven operator kill switch for all tenants or selected tenant ids.

Violation logs are metadata-only: reason, tenant id, thread id, and a generated connection id. The relay does not inspect decrypted Remote Control payloads.

Operational notes:

- rate windows are tumbling windows, not sliding windows, so short bursts can straddle a window boundary;
- kill switch environment changes take effect after the hosted relay process reloads;
- idle close runs on a timer, so the close can happen up to one polling interval after the configured TTL;
- daemon-to-browser Codex output is intentionally not throughput-limited in this browser-abuse slice.

For the self-hosting shape, read [docs/self-host.md](docs/self-host.md).
