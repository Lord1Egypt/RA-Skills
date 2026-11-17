# Changelog

All notable changes to the SendPulse SMTP Skill. Format follows
[Keep a Changelog](https://keepachangelog.com/); versioning follows
[SemVer](https://semver.org/).

## [1.2.1] — 2026-07-13

### Changed

- Published to GitHub: all placeholder repository URLs replaced with the real
  monorepo paths (`github.com/sendpulse/sendpulse-skills`, skill folder
  `sendpulse-smtp-skill/`). The version self-check now points at
  `raw.githubusercontent.com/sendpulse/sendpulse-skills/main/sendpulse-smtp-skill/VERSION`
  and is live. Install/update instructions rewritten for the monorepo layout
  (clone once → copy or symlink the skill folder).

## [1.2.0] — 2026-07-08

### Added

- **SendPulse MCP server reference** (`references/sendpulse-mcp.md`): what the
  hosted MCP server (`https://mcp.sendpulse.com/mcp`) is, how to connect (Single
  API Key), and — importantly — correct expectations: MCP is for interactive
  account work from AI chat (senders, stats, unsubscribe list); it does not
  replace the API/relay integration inside the user's application. Mentioned in
  SKILL.md Step 2.

## [1.1.0] — 2026-07-06

### Changed

- Authorization: the **Single API Key** (*Settings → API → API keys*, long-lived
  Bearer) is now the preferred method; OAuth client credentials remains the
  alternative. Updated SKILL.md, api-reference, quickstart.
- Product routing now points to the dedicated **`sendpulse-email-skill`** for bulk
  campaigns (address books, segments, analytics) and explicitly names
  **`sendpulse-template-skill`** for building email HTML;
  `references/email-service-api.md` stays as the overview fallback.

## [1.0.0] — 2026-07-06

### Added

- Initial release.
- `SKILL.md` core playbook: product routing (SMTP vs Email Service), prerequisite
  checks, OAuth flow, send rules, hygiene rules, troubleshooting order,
  self-update check.
- References: quickstart, account/sender/DNS setup, full SMTP API reference,
  error & troubleshooting tables, deliverability guide, webhooks guide, SMTP
  relay guide (smtp-pulse.com), Email Service API overview.
- Examples: curl, PHP (SDK + plain cURL), Python (requests), Node.js (fetch),
  plus relay snippets for PHPMailer / nodemailer / smtplib.
- Adapters: Claude Code (native), Cursor rule (.mdc), ChatGPT Custom GPT
  instructions, Gemini GEMINI.md, generic install guide.
