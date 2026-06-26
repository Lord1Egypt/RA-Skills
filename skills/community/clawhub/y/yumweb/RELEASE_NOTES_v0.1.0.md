# yumweb v0.1.0

Initial public positioning release for yumweb as a **logged-in browser bridge for AI agents**.

## Highlights
- New homepage slogan:
  - **Use your already-logged-in browser as the agent’s hands.**
- Repositioned README around:
  - logged-in browser workflows
  - multi-agent support (OpenClaw, Copilot CLI, Claude Code, Hermes)
  - cross-browser support (Edge, Chrome, Chromium-based browsers)
  - local-first / persistent-session usage
- Added explicit explanation for why sandbox browsers are often not enough for real assistant workflows.
- Synced `SKILL.md` metadata and messaging with the new product direction.
- Updated GitHub repository description to match the new positioning.

## Recent functional improvements
- Active tab persistence to make follow-up `read` / `click` / `type` commands target the intended page more reliably.
- Added local `.venv` wrapper scripts for easier setup and execution:
  - `scripts/bootstrap.sh`
  - `scripts/run.sh`

## Positioning
Built for agent workflows where the user logs in once, and the agent can later continue operating inside that real logged-in browser world.
