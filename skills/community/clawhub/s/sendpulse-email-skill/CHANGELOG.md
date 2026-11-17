# Changelog

All notable changes to the SendPulse Email Service Skill. Format follows
[Keep a Changelog](https://keepachangelog.com/); versioning follows
[SemVer](https://semver.org/).

## [1.1.1] — 2026-07-13

### Changed

- Published to GitHub: all placeholder repository URLs replaced with the real
  monorepo paths (`github.com/sendpulse/sendpulse-skills`, skill folder
  `sendpulse-email-skill/`). The version self-check now points at
  `raw.githubusercontent.com/sendpulse/sendpulse-skills/main/sendpulse-email-skill/VERSION`
  and is live. Install/update instructions rewritten for the monorepo layout
  (clone once → copy or symlink the skill folder).

## [1.1.0] — 2026-07-08

### Added

- **SendPulse MCP server support** (`references/sendpulse-mcp.md`): the hosted MCP
  server at `https://mcp.sendpulse.com/mcp` as the preferred channel for
  interactive, chat-driven campaign work (books, contacts, campaigns via tools —
  no API code); REST API remains the path for standalone apps/integrations.
  Includes connection setup (Single API Key), runtime tool discovery
  (`email_*` tools), the confirm-before-send safety rule, and fallbacks.
  SKILL.md Step 1 renamed to "Pick the channel and authorize".

## [1.0.0] — 2026-07-06

### Added

- Initial release.
- `SKILL.md` core playbook: three-skill routing (template / SMTP / email service),
  Single API Key auth (OAuth alternative), campaign lifecycle mental model,
  critical rules (Base64 body, verified sender, review expectations, 4/hour limit,
  cost check, tracking), troubleshooting order, self-update check.
- References: quickstart (first campaign), address books & subscribers & variables
  & tags & blacklist, segmentation (presets, conditions, recipes), campaigns
  (create/schedule/statuses/review, A/B, resend to unopened, best time, timezone,
  dynamic lists), analytics playbook with reference ranges, full API reference,
  errors & campaign-status decoder, webhooks (incl. task_status_update),
  list building & hygiene.
- Examples: curl, PHP, Python, Node.js — full lifecycle each (book → subscribers →
  campaign → analytics → suppression), webhook receiver sketches.
- Adapters: Claude Code (native), Cursor rule (.mdc), ChatGPT Custom GPT
  instructions, Gemini GEMINI.md, generic install guide.
