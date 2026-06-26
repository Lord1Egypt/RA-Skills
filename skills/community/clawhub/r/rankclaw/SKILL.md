---
name: rankclaw
description: "RankClaw — AI Agent Trust Layer. Check any ClawHub, OpenClaw, nanobot, nanoclaw, picoclaw, or MCP server skill against 14,700+ indexed tools before installing. Get security scores, malicious flags, and AI-generated safety verdicts."
version: "2.1.0"
author: rankclaw
homepage: https://rankclaw.com
category: security
tags:
  - security
  - clawhub
  - openclaw
  - nanobot
  - nanoclaw
  - picoclaw
  - mcp
  - skills
  - trust
  - ranking
  - agent-security
  - supply-chain
metadata:
  openclaw:
    requires:
      env: []
      bins: []
    install: []
---

# RankClaw — AI Agent Trust Layer

RankClaw is the trust and safety layer for the OpenClaw ecosystem and all AI agent tools.

Before you install any skill — OpenClaw, nanoclaw, picoclaw, or MCP server — RankClaw tells you:

- **Is it malicious?** (1,046 confirmed malicious skills and counting)
- **What does the AI security audit say?** (deep scan of SKILL.md, prerequisites, install behavior)
- **What's the trust score?** (0–100 across Security, Maintenance, Documentation, Community)
- **Is the author legitimate?** (detect brand-jacking, impersonation, phantom prereqs)

14,700+ ClawHub skills indexed. Free for agents. No API key required.

---

## Quick Safety Check (use this first)

Before installing any skill, call `rankclaw_check`:

```
rankclaw_check skill="wallet-connector"
rankclaw_check skill="git-auto-commit"
rankclaw_check skill="tkuehnl/cacheforge-stats"
```

Returns: verdict (SAFE / MALICIOUS / MODERATE / RISKY), score, key findings.

If `is_malicious: true` — **do not install, no exceptions.**

---

## MCP Integration (recommended for agents)

RankClaw exposes an MCP server. Add it to your agent configuration:

```
MCP Server URL: https://api.rankclaw.com/api/mcp/
Protocol: JSON-RPC 2.0 (MCP 2024-11-05)
Auth: none required
```

### nanobot (HTTP MCP — recommended, zero config)

nanobot supports HTTP MCP natively. No bridge script required. Add to `~/.nanobot/config.json`:

```json
{
  "tools": {
    "mcp_servers": {
      "rankclaw": {
        "url": "https://api.rankclaw.com/api/mcp/"
      }
    }
  }
}
```

All five tools register automatically on startup.

---

### nanoclaw MCP config

nanoclaw uses stdio-based MCP transport. Download the bridge script and add it to `.mcp.json`:

```bash
curl -O https://raw.githubusercontent.com/RankClaw/rankclaw/main/mcp_bridge.py
```

Add to your nanoclaw `.mcp.json`:
```json
{
  "mcpServers": {
    "rankclaw": {
      "command": "python3",
      "args": ["rankclaw_mcp_bridge.py"],
      "description": "RankClaw — AI Agent Trust Layer"
    }
  }
}
```

### picoclaw

picoclaw does not currently support MCP servers directly (Issue #77 closed). Use our OpenClaw skill instead — it is natively compatible with picoclaw's skill system.

### Claude Code / cursor / Windsurf (HTTP MCP)

For clients that support HTTP MCP directly:

```json
{
  "mcpServers": {
    "rankclaw": {
      "url": "https://api.rankclaw.com/api/mcp/"
    }
  }
}
```

### Available MCP tools:

| Tool | Description |
|------|-------------|
| `rankclaw_check` | Safety verdict for any skill (fuzzy match) — use this first |
| `rankclaw_score` | Full score + findings for a specific skill ID |
| `rankclaw_leaderboard` | Top-ranked safe skills (filter by category/author) |
| `rankclaw_find` | Search by name, author, or keyword |
| `rankclaw_malicious` | List of all flagged malicious skills |

---

## Agent Decision Protocol

When an agent is about to install a skill, run this decision tree:

```
1. Call rankclaw_check with the skill name
2. If verdict == "MALICIOUS":
   → ABORT. Do not install. Report malicious_reason to user.
   → Suggest safe alternatives via rankclaw_find
3. If verdict == "RISKY" or score < 40:
   → WARN user. Show key_findings. Ask for explicit confirmation.
4. If verdict == "MODERATE" or score 40–79:
   → Install with caution. Show summary to user.
5. If verdict == "SAFE" or score >= 80:
   → Proceed. Optionally mention the score to user.
```

### Example agent prompt

```
I need to install the OpenClaw skill "{skill_name}".
Before I proceed, I will check its security status with RankClaw.

[Call rankclaw_check skill="{skill_name}"]

Based on the verdict:
- If MALICIOUS: I will not install this skill. It is a confirmed security threat.
- If score < 60: I will warn you and ask for confirmation.
- If score >= 80: I will proceed with installation.
```

---

## What RankClaw Detects

RankClaw AI audits every skill for these attack patterns:

### 1. Prompt Injection
SKILL.md contains hidden instructions that override the agent's system prompt. Detected by scanning for anomalous instruction blocks, invisible characters, and instruction-style text embedded in descriptions.

### 2. Phantom Prerequisites
Install steps reference packages or scripts not publicly available (e.g., `openclaw-agent`, private npm packages, obfuscated URLs). High correlation with credential theft.

### 3. Brand Impersonation
Skills named `phantom-wallet-connector`, `anthropic-official`, `cursor-helper` that are not authored by the legitimate organization. 31 coordinated impersonation campaigns detected to date.

### 4. Credential Staging
Skills that write API keys, tokens, or session data to accessible paths (`.env`, `/tmp/`, public URLs). Usually combined with a legitimate-looking feature to avoid suspicion.

### 5. Supply Chain Pivots
Skills that install additional scripts or packages at runtime (not declared in install steps). Common pattern: safe SKILL.md, malicious download in install script.

### 6. Scope Creep
Skills claiming `scope: instruction-only` but containing shell execution steps. OpenClaw has no sandbox enforcement — full host access is the reality.

---

## Score Interpretation

| Score | Tier | Meaning |
|-------|------|---------|
| 90–100 | Elite | Excellent — clean, well-documented, actively maintained |
| 75–89 | Top 25% | Good — safe to use, minor gaps |
| 60–74 | Mid | Acceptable — review findings first |
| 40–59 | Low trust | Proceed with caution — significant concerns |
| 0–39 | Risky | Not recommended — major issues found |
| N/A | MALICIOUS | Do not install — confirmed threat |

Scores are weighted: **Security 40% · Maintenance 20% · Documentation 20% · Community 20%**

---

## Direct API Usage

### Check a skill by ID:
```bash
curl https://api.rankclaw.com/api/skill/tkuehnl/cacheforge-stats/
```

### Leaderboard (top safe skills):
```bash
curl "https://api.rankclaw.com/api/leaderboard/?per_page=10&safe_only=1"
```

### Malicious skills list:
```bash
curl "https://api.rankclaw.com/api/leaderboard/?malicious_only=1"
```

### Badge (embed in your SKILL.md):
```markdown
[![RankClaw](https://api.rankclaw.com/api/badge/your-author/your-skill.svg)](https://rankclaw.com/skill/your-author/your-skill)
```

Badges update hourly. Green = Top 25%, Yellow = Top 60%, Red = Below 60%.

---

## For Skill Authors

If you publish OpenClaw skills, RankClaw monitors your score continuously.

**A dropping score is public.** Users and agents can see it.

To protect your reputation:

1. **Claim your skill** at https://rankclaw.com → get Defender Pro ($29/mo)
2. **Deep AI scan** — full repo audit with detailed findings
3. **Verified badge** — shows agents your skill is author-claimed and monitored
4. **Score alerts** — get notified immediately if your score drops

Subscribers get priority rescans when their SKILL.md changes.

---

## Score Freshness

Scores decay over time without rescans:

- **Fresh (≤14 days):** Verified — safe to trust
- **Aging (15–45 days):** May not reflect recent changes
- **Needs Review (46–90 days):** Rescan recommended
- **Unverified (>90 days):** Badge grays out, treat as unknown

---

## Coverage

RankClaw indexes skills from:
- **OpenClaw** (openclaw.ai) — primary registry, 14,700+ skills
- **Smithery** — MCP server registry (5,800+ servers, indexing in progress)
- **Manus** and other AI agent tool registries

One trust layer. All ecosystems.
