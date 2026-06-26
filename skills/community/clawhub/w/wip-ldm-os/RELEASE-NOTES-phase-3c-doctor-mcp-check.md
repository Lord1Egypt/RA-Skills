# Installer: `ldm doctor` MCP path check (Phase 3c)

## What changed

`ldm doctor` now walks `~/.claude.json#mcpServers` and verifies that every entry whose command is `node` and whose first arg resolves under `~/.ldm/extensions/` or `~/.openclaw/extensions/` points at a file that exists and parses.

- For each qualifying entry: `existsSync` + `node --check` (5s timeout).
- Broken entries report as `! MCP <name>: missing at <path>` or `! MCP <name>: unparseable at <path> (<first line of stderr>)`.
- Healthy state logs a single green line: `+ MCP entries under LDM/OC extensions: all paths exist and parse`.
- `ldm doctor --fix` removes dangling entries and writes `~/.claude.json` back.
- Without `--fix`: broken count is added to the doctor `issues` total so the exit code reflects the problem.

## Why

Phase 3c of the 1password MCP bug plan. The existing `--fix` path in doctor already caught tmp-path MCP entries, but not the case where an extension rename left `~/.claude.json` pointing at a rotated-out `mcp-server.mjs`. Doctor would pass while `claude mcp list` showed red ✗. Shift the failure mode from "find out when you run claude mcp list" to "doctor tells you on the next run."

## Scope

Strictly limited to `node <path>` MCPs whose path resolves under the LDM/OpenClaw extension roots. Third-party MCPs (`npx ...`, HTTP endpoints, user-added tools outside extension dirs) are not touched or reported on.

## Verification

- `node --check bin/ldm.js` passes.
- `node bin/ldm.js doctor` run locally prints the new green line (all entries currently valid on this machine).
- Paired with Phase 3a and 3b, the system is now loud-stop at install time and loud-report at doctor time.

## Tracking

Closes Phase 3c of:
`ai/product/bugs/1password/2026-04-21--cc-mini--mcp-server-missing-from-install.md`

Remaining follow-up (separate PR):
- `buildSourceInfo` captures the parent repo's remote when extraction lands inside `~/.ldm/tmp`. Registry `source.repo` values are therefore unreliable. Phase 3b used path-based matching to avoid the issue. The underlying fix for `buildSourceInfo` is a distinct cleanup and will ship separately.
