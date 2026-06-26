# Installer: registerMCP postcondition check (Phase 3a)

## What changed

`lib/deploy.mjs::registerMCP` now verifies the resolved MCP entrypoint exists and parses before touching `~/.claude.json`. If either check fails, the registration is aborted with a loud error listing every path that was tried.

- `existsSync(mcpPath)` check: was implicit in the fallback chain, now authoritative.
- `node --check <mcpPath>`: catches syntax errors, missing shebangs that matter, ESM/CJS mismatches, etc.
- On failure: `fail()` with the resolved path, the candidate paths that were tried, and the suggestion to verify the tarball's `files` array.

## Why

Phase 3a of the 1password MCP bug plan. The old registration path would happily write a `~/.claude.json` entry for a file that did not exist (or was unparseable), leaving a silent "Failed to connect" state that only surfaced when someone ran `claude mcp list`. The wip-1password 0.2.3-alpha.2 incident is the motivating example: the published tarball excluded `mcp-server.mjs`, the installer installed something, and `claude mcp list` started showing a red ✗ that nobody saw for days.

This change shifts the failure mode from silent-wrong to loud-stop. If the installer cannot verify the MCP entrypoint, it does not pretend to have registered one.

## Verification

- `node --check lib/deploy.mjs` passes.
- A dogfood install of a known-good extension still registers cleanly.
- A deliberately-broken test (delete the `mcp-server.mjs` from an extension after deploy, then re-run `ldm install` and watch the output) shows the new `MCP: ... registration aborted` messages.

## Tracking

Closes Phase 3a of:
`ai/product/bugs/1password/2026-04-21--cc-mini--mcp-server-missing-from-install.md`

Phase 3b (stale-entry cleanup on deploy) and Phase 3c (`ldm doctor` MCP path check) land in separate PRs for independent revertability.
