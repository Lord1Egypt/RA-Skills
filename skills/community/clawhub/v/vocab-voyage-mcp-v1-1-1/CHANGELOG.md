# Changelog

All notable changes to the public Vocab Voyage MCP server scaffold will be
documented here. Versions follow [SemVer](https://semver.org).

## [1.1.1] — 2026-04-22

- `mcp-server-repo/` is now the single source of truth — `server.json`,
  `smithery.yaml`, `clawhub.json`, and `SUBMISSION_LINKS.md` are committed
  here and regenerated on every `pnpm release:check` from the canonical
  20-tool catalog and `apps.json` (17 widgets).
- Adopted flat repo layout (no nested `manifest/`) to mirror the live
  GitHub repo so each file maps 1:1 onto upload-zone overwrites.
- Added `SKILL.md` and `docs/openclaw-quickstart.md` to the mirror.
- New build-time validators assert version + tool/widget count parity
  across server-card, server.json, smithery.yaml, clawhub.json.

## [1.1.0] — 2026-04-22

- Public GitHub mirror first cut (`mcp-server-repo/`).
- `server-card.json` now exposes `repository.url`, `source_url`, and a
  `screenshots[]` array for directory previews.
- Added cache-busted widget poster URLs powered by the snapshot manifest's
  per-file sha256.
- New `pnpm release:check` orchestrator that runs the entire pre-publish
  pipeline in canonical order.
- New `/mcp/tools` browser polish: per-field validation hints, copyable
  syntax-highlighted headers block, fetch ↔ axios sub-toggle.

## [1.0.0] — 2025-11

- Initial public launch: 20 MCP tools and 17 interactive widgets.
- Anonymous-friendly transport (`streamable-http`) with optional
  `Bearer vv_mcp_…` token for personalization.
- Live listings on MCP Registry, Glama, Smithery, ClawHub, and MCP Market.