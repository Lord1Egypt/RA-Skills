---
title: "Remote Control E2EE daemon key registration must survive hosted reloads"
status: done
priority: P0
owner: Cody
repo: wip-ldm-os-private / wip-codex-remote-control-private
created: 2026-05-05
---

# Remote Control E2EE Key Persistence

## Problem

After a hosted MCP deploy or PM2 reload, the Remote Control page can fail with:

```text
daemon has no E2EE key registered. Re-run `codex-daemon link` to upgrade.
```

The local daemon is still paired, and the local E2EE identity still exists. The hosted relay forgot the daemon's E2EE public key because the server-side registry is currently process memory.

That is acceptable as a one-time smoke recovery, but it is not acceptable product behavior. Users must not have to run `codex-daemon link` after every deploy, restart, or hosted process reload.

## Current Evidence

Observed during Remote Control dogfood after hosted MCP reload:

- Browser opened an existing Remote Control URL for thread `019dfa1e-0c3d-7f01-86b9-9a22cd452bde`.
- The page showed `daemon has no E2EE key registered`.
- `codex-daemon link` produced a new pair URL and re-registered the key.
- Parker correctly asked whether this means users must relink every time.
- Diagnosis: hosted MCP reload cleared the relay's in-memory daemon E2EE pubkey registry. The daemon pairing was not wiped locally.

Security review evidence:

- Verdict: `PASS PRIVATE ONLY`. `LIVE BLOCKED` for broad dogfood until this and daemon-side thread authority binding are fixed.
- CC security review classed this as `CRITICAL`: fix before broader dogfood.
- Relay key registry is currently in memory as `codexDaemonPubkeys`.
- Source pointers from review:
  - `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/server.mjs:2576`
  - `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/server.mjs:2728`
  - `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/server.mjs:2754`
- PM2 reload or relay restart can drop `e2ee_available` until re-pair or relink.

Additional review evidence:

- The daemon key is persisted locally at `~/.codex-daemon/e2ee-key.json` with mode `600`.
- Source pointers from review:
  - `repos/ldm-os/apps/wip-codex-remote-control-private/src/e2ee.ts:71`
  - `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/server.mjs:2725`
- Current behavior appears fail-closed, not a plaintext downgrade.
- The risk is product and regression reliability: proven co-presence breaks after VPS restart until relink.
- Hosted auth review confirmed daemon reconnect alone does not appear to republish the key.
- Source pointer from review:
  - `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/server.mjs:2758`
- Daemon reconnect path clears sessions and reauths with bearer token, but does not re-register the public key:
  - `repos/ldm-os/apps/wip-codex-remote-control-private/src/relay-client.ts:259-262`

## Expected Behavior

Remote Control E2EE key registration survives hosted reloads.

After a hosted MCP restart:

1. The daemon remains locally paired.
2. The daemon's existing E2EE public key is available to the relay again.
3. Opening `/codex-remote-control/<threadId>` succeeds without re-running `codex-daemon link`.
4. The browser can complete E2EE bootstrap and attach to the live thread.
5. Existing Remote Control URLs remain usable after deploys and process restarts.

## Likely Implementation

Choose one or both durable paths:

- Persist the daemon E2EE public key server-side, likely in Postgres with the paired daemon or agent identity.
- Make the daemon re-register its existing E2EE public key automatically when it reconnects after a relay reload.
- If choosing reconnect re-registration, the daemon must send its public key on authenticated WebSocket connect.
- Preferred fix: do both. Persist for durability, and send a `daemon.identity` or equivalent frame on reconnect for self-healing.

The product contract matters more than the exact mechanism: `codex-daemon link` should be for first pairing, lost credentials, or explicit account changes, not routine hosted restarts.

## Acceptance

- Pair daemon once with `codex-daemon link`.
- Start `codex-daemon`.
- Open Remote Control URL and verify E2EE attach succeeds.
- Restart hosted MCP or PM2 process.
- Verify PM2 reload preserves `--env-file` and `/health` reports `database=postgres`.
- Refresh the same Remote Control URL.
- Browser completes E2EE bootstrap without running `codex-daemon link`.
- Browser attaches to the same thread.
- Browser to TUI and TUI to browser still work.
- If the relay has genuinely never seen a daemon key, the error explains first-time pairing rather than implying routine relink.
- Add a regression proving relay restart preserves or restores daemon key availability.
- Add a PM2-equivalent reload test: relay restart does not require re-pair and bootstrap still reports E2EE available.

## Closure Evidence

Closed on 2026-05-11 after the paired daemon and hosted relay fixes landed and passed live dogfood.

Implementation shipped:

- `wip-codex-remote-control-private` PR #62: daemon sends `daemon.identity` with its E2EE public key on authenticated relay WebSocket reconnect.
- `wip-codex-remote-control@0.0.2-alpha.20`: released and installed locally.
- `wip-ldm-os-private` PR #867: hosted relay persists daemon E2EE public keys in Postgres, reloads them on startup, and accepts authenticated `daemon.identity` reconnect frames.
- `@wipcomputer/wip-ldm-os@0.4.85-alpha.10`: released and deployed to hosted MCP.

Validation passed:

- Daemon: `npm run typecheck`.
- Daemon: `npm test`, including the reconnect identity gate.
- Hosted relay: `npm run test:crc-e2ee-key-persistence`.
- Hosted relay: `npm run test:crc-e2ee-session-route`.
- Hosted relay: `npm run test:crc-pair-status-poll-token`.
- Hosted relay: `npm run test:crc-pair-login-flow`.
- Hosted relay: `node --check src/hosted-mcp/server.mjs`.
- Hosted deploy: `/health` returned healthy with `database=postgres`.
- Hosted deploy manifest: `23 ok, 0 mismatched`.
- Live VPS log showed `loaded 0 persisted E2EE daemon pubkey(s)` followed by `registered E2EE pubkey ... via daemon-reconnect`.

Manual smoke passed without running `codex-daemon link`:

- Existing thread: `019dfa1e-0c3d-7f01-86b9-9a22cd452bde`.
- Existing title: `test`.
- Browser opened the current Remote Control URL after hosted deploy and login.
- Browser completed encrypted Remote Control attach without the `daemon has no E2EE key registered` error.
- Browser to TUI marker passed: `E2EE_RECONNECT_BROWSER_TO_T`.
- TUI to browser direction passed in the same thread.

This closes the routine hosted reload relink regression. First-time pairing and explicit account changes still use `codex-daemon link`.

## Related Product Improvement

Add a natural-language recovery path:

```text
relink remote control
```

This should call a Remote Control MCP relink tool that starts or proxies the `codex-daemon link` flow and returns the pair URL/code.

This recovery command is useful, but it is not the primary fix. The primary fix is key persistence or automatic re-registration.

## Non-Goals

- Do not change the one-browser co-presence path.
- Do not weaken E2EE or bypass browser-to-daemon key agreement.
- Do not make the hosted relay the session authority. It remains transport and login surface only.
- Do not require users to relink after normal hosted deploys.
