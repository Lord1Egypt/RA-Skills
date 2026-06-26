---
name: skillguard-check
description: "Audit every locally-installed AI Skill against skill-guard's public security database (skillguard.vip). Use when (1) the user asks 'are my skills safe?' or 'check my skills', (2) the user just installed a new skill from ClawHub / OpenClaw / a marketplace, (3) before invoking an unfamiliar skill, (4) on a periodic security check. Surfaces blocked skills (hard-trigger rules fired) and high-risk skills (score < 50)."
allowed-tools:
  - Bash
  - Read
metadata:
  homepage: https://skillguard.vip
  audit: https://skillguard.vip/skills/clawhub/skillguard-check
  source: https://github.com/yangyixxxx/skillguard
---

# skillguard-check

Audit AI Skills installed on this machine against the public skill-guard
security database at https://skillguard.vip. Returns a JSON report listing
**blocked** and **high-risk** skills along with links to their public audit
pages so the user can decide what to uninstall.

## When to invoke

Trigger this skill any time the user expresses concern about installed-skill
safety, or after the user installs a new skill. Concrete cues:

- "are my skills safe?", "check my installed skills", "audit my skills"
- "I just installed XYZ from ClawHub, is it ok?"
- "any malicious skills on my machine?"
- The user mentions a skill name and asks if it's trusted.
- Periodic: when no audit has been run this session and the user is doing
  security-sensitive work (handling secrets, on a new machine, etc.).

## How to invoke

Run the bundled script. It needs Python 3 (pre-installed on macOS / most
Linux). No network access beyond `https://skillguard.vip`.

```bash
python3 scripts/check.py
```

The script outputs a single JSON object to stdout. Sample shape:

```json
{
  "total": 12,
  "audited": 9,
  "unauditedCount": 3,
  "blocked": [
    {
      "slug": "openclaw-omni-expert",
      "path": "/Users/x/.claude/skills/openclaw-omni-expert",
      "score": 3,
      "riskLevel": "Critical",
      "findingsCount": 155,
      "auditUrl": "https://skillguard.vip/skills/clawhub/openclaw-omni-expert"
    }
  ],
  "highRisk": [
    {
      "slug": "some-skill",
      "score": 42,
      "riskLevel": "High",
      "auditUrl": "..."
    }
  ],
  "medium": [...],
  "safe": 5,
  "unaudited": [
    {"slug": "my-private-skill", "path": "...", "reason": "not in skill-guard database"}
  ],
  "errors": []
}
```

## How to report back to the user

After parsing the JSON:

1. **If `blocked` is non-empty** — open with `⚠️ <N> blocked skill(s) found
   on this machine.` Then for each entry, give:
   - the slug + install path,
   - a one-line risk summary (use riskLevel + findingsCount),
   - the `auditUrl` so they can see findings,
   - a recommendation to uninstall.

2. **If `highRisk` is non-empty (and no blocked)** — open with `Found <N>
   high-risk skill(s).` Same format but softer language: "review the audit
   page and consider whether you trust the publisher".

3. **If only `medium`/`safe`/`unaudited`** — `No blocked or high-risk
   skills detected.` Mention the unaudited count so the user knows some
   skills couldn't be checked (private/local skills that haven't been
   uploaded to skill-guard's database).

4. **Always end with** the `auditUrl` for each surfaced skill. Don't
   paraphrase the audit verdict — link to the canonical page so the user
   reads the real findings, not a summary.

## What gets scanned

The script checks these install paths (in order):

| Path | Used by |
|---|---|
| `~/.claude/skills/` | Claude Code |
| `~/.openclaw/skills/` | OpenClaw |
| `~/.local/share/claude-skills/` | Linux convention |
| `~/.skills/` | Generic |
| `~/Library/Application Support/Claude/skills/` | Claude Desktop on macOS |

Each immediate subdirectory is treated as one skill, named by the directory.
The script then queries `https://skillguard.vip/skills/clawhub/<slug>.json`
for the public audit verdict.

Skills that aren't in the public database (private skills, custom builds,
unpublished bundles) are reported under `unaudited` — not flagged, but
called out so the user knows they're un-audited.

## Limitations

- **Only checks skills that match a slug in skill-guard's ClawHub-sourced
  database.** Privately-developed skills won't have an audit. Users can run
  a fresh scan via `https://skillguard.vip/` (paste the GitHub URL) or
  `POST /v1/scan/upload` with a zip.

- **Uses the most recent verdict in skill-guard's DB.** If a skill was
  re-published on ClawHub after the last skill-guard scan, the verdict may
  be stale. The audit page shows `lastScannedAt` for transparency.

- **Slug-matching only.** Two different skills with the same directory
  name (e.g. `github`) collide. The audit URL is the source of truth — if
  the displayed name doesn't match what the user installed, treat as
  unaudited.
