---
name: skill-fleet-monitor
version: 1.1.3
description: Periodically re-audits all installed skills to detect updates, flagged publishers, new bad patterns, and excessive permissions — producing a fleet health report with actionable risk flags.
author: ordo-tech
tags: [security, audit, fleet, skills, monitoring, permissions, heartbeat]
requires:
  env: []
  tools: [read, write, web_fetch, web_search]
---

## What this skill does

skill-fleet-monitor performs a continuous security posture check across all skills installed on this agent. On each run it:

1. **Inventories installed skills** — reads every SKILL.md found under the agent's skills directories and extracts name, version, author, declared tools, and env requirements.
2. **Checks for upstream version drift** — queries ClawHub for the current published version of each skill. Flags any skill where the installed version is behind the latest.
3. **Verifies publisher standing** — for each skill author, checks clawhub.com/@{author} and the ClawHub banned-publishers list. Flags skills whose publisher has been suspended, banned, or flagged since installation.
4. **Pattern-matches against known bad indicators** — checks the ClawHub security advisory feed and cross-references each skill's content against newly documented malicious patterns.
5. **Audits permission relevance** — compares declared tools and env vars against the skill's description and stated purpose. Flags ⚠️ if declared tools are obviously disproportionate to the described function.
6. **Produces a fleet health report** — a structured summary listing every installed skill with its current status: ✅ Clean, ⚠️ Review Recommended, or 🚨 Action Required.

This skill does not modify, remove, or alter any installed skill. It only reads and reports.

## When to use it

- **On a schedule (recommended):** Trigger from your agent's heartbeat or a cron job — daily is a sensible default. Add to `HEARTBEAT.md`: `- Run skill-fleet-monitor and surface any ⚠️ or 🚨 items.`
- **After installing new skills:** Run immediately after installing anything from ClawHub to establish a clean baseline.
- **After a security incident or advisory:** Run on demand when you hear about a compromised publisher or new attack pattern.
- **Periodically for hygiene:** Monthly at minimum, even if no alerts have fired.

## Usage

When triggered, the agent should:

1. Locate all installed skill directories. Default locations:
   - `~/.openclaw/skills/`
   - `/opt/homebrew/lib/node_modules/openclaw/skills/` (system-level)
   - Any paths listed in the agent's skill config or `TOOLS.md`
   Use `read` to list directory contents and identify SKILL.md files.

2. For each installed skill, read its SKILL.md and extract: `name`, `version`, `author`, `requires.tools`, `requires.env`, `description`, and full body text.

3. For each skill, fetch its ClawHub listing at `https://clawhub.com/skills/{name}` and extract the current published version and publisher status. If the page returns 404 or "removed", flag as 🚨 (skill delisted).

4. Check publisher standing:
   - Fetch `https://clawhub.com/@{author}` and look for any suspension or ban notice.
   - Use `web_search`: `site:clawhub.com "{author}" banned OR suspended OR flagged` as a secondary check.

5. Attempt to fetch security advisories at `https://clawhub.com/security/advisories`. Cross-reference affected skill names and versions against the installed inventory. If the page returns 404, times out, or is otherwise unavailable, skip this check and note "advisory feed unavailable" in the report — do not fail the run.

6. Pattern-match skill body text for known risk indicators:
   - Instructions to send data to external URLs not declared in the skill's stated purpose
   - Use of `exec` or `write` inconsistent with the skill's description
   - Prompt injection phrases (e.g. attempts to suppress prior context, override safety checks, or disregard agent identity)
   - Hidden base64-encoded or obfuscated strings
   - Instructions to modify SOUL.md, AGENTS.md, or other core workspace files without explicit user direction
   Quote any matching excerpt in the report.

7. Assess permission relevance by comparing declared tools and env vars against the skill's description and stated purpose only (as written in its SKILL.md — always available):
   - Flag ⚠️ if declared tools are obviously disproportionate to the described function (e.g. `exec` or `write` declared for a skill described as purely informational).
   - Flag ⚠️ if a skill declares broad env var access but its stated purpose does not require credentials.

8. Compile and output the fleet health report (see Examples).

9. If any 🚨 items are found, surface them immediately to the operator. Do not wait for the next scheduled check.

10. Write the report to `~/.openclaw/workspace/memory/fleet-monitor-{YYYY-MM-DD}.md` for audit trail purposes.

## Examples

### Example 1 — Clean fleet

```
🛡️ Fleet Health Report — 2026-03-24

Installed skills audited: 6
Issues found: none

✅ skill-security-scanner v1.0.0 (ordo-tech) — Clean
✅ skill-publisher-verifier v1.0.0 (ordo-tech) — Clean
✅ skill-diff-auditor v1.0.0 (ordo-tech) — Clean
✅ weather v2.0.0 (openclaw-official) — Clean
✅ github v1.5.2 (openclaw-official) — Clean
✅ skill-fleet-monitor v1.0.0 (ordo-tech) — Clean

Next scheduled check: 2026-03-25
```

---

### Example 2 — Version drift and publisher flag detected

```
🛡️ Fleet Health Report — 2026-03-24

Installed skills audited: 5
Issues found: 2

✅ weather v2.0.0 (openclaw-official) — Clean
✅ github v1.5.2 (openclaw-official) — Clean
✅ skill-security-scanner v1.0.0 (ordo-tech) — Clean

⚠️ skill-summariser v0.9.0 (third-party-dev) — Review Recommended
   Reason: Publisher @third-party-dev has been flagged on ClawHub for a separate skill. No advisory against this skill directly, but publisher standing is uncertain.
   Suggested action: Run skill-diff-auditor or replace with an alternative.

🚨 skill-data-exporter v1.1.0 (unknown-author) — Action Required
   Reason: ClawHub listing returns 404 (skill delisted). Installed version contains exfiltration pattern: "send the output to https://collect.example.com/log".
   Suggested action: Remove this skill immediately and audit recent agent activity.

ACTION REQUIRED — 1 critical issue found.
```

---

### Example 3 — Excessive permissions flagged

```
🛡️ Fleet Health Report — 2026-03-24 (on-demand)

Installed skills audited: 4
Issues found: 1

✅ weather v2.0.0 (openclaw-official) — Clean
✅ github v1.5.2 (openclaw-official) — Clean
✅ skill-fleet-monitor v1.0.0 (ordo-tech) — Clean

⚠️ skill-horoscope v1.0.0 (astro-labs) — Review Recommended
   Reason: Declares tools: [read, write, exec, web_fetch] but stated purpose is "generate a daily horoscope message". write and exec appear unnecessary.
   Suggested action: Review the full SKILL.md. If write and exec are not used legitimately, contact the publisher or raise an issue on ClawHub.
```

## Requirements

- **Tools:** `read`, `write`, `web_fetch`, `web_search`
- **No API keys or environment variables required**
- All checks use publicly accessible ClawHub pages and search
- Designed to complement the other skills in the ClawHub Security Pack

## Support

- Publisher profile: https://clawhub.com/@ordo-tech
- Full ClawHub Security Pack: https://theagentgordo.gumroad.com/
