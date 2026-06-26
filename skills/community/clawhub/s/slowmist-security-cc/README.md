# SlowMist Security Review 🛡️

[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-blue)](https://claude.com/claude-code)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Security: Security Review](https://img.shields.io/badge/Security-Comprehensive%20Review-red.svg)](#)

> **Core principle: Every external input is untrusted until verified.**
>
> 🛡️ This is the Claude Code adapted version of the [SlowMist Agent Security](https://github.com/slowmist/slowmist-agent-security) framework.

A comprehensive security review framework for Claude Code agents operating in adversarial environments. Covers 6 review types, 11 code red-flag patterns, 8 social engineering patterns, and 7 supply chain attack patterns.

**Available in:** [English](README.md) · [中文](README.zh-CN.md)

---

## Quick Decision Card

```
  External Input Detected → Select Review Type → Execute Steps → Output Report
```

| Scenario | Route To | Remember |
|----------|---------|----------|
| Installing Skill/MCP/npm package | `skill-mcp.md` | List file inventory first |
| GitHub repository | `repository.md` | Check commit history first |
| URL / Document / Gist | `url-document.md` | Scan code blocks line-by-line |
| On-chain address / contract | `onchain.md` | Check AML score first |
| Product / Service / API | `product-service.md` | Check private key management first |
| Tool shared in group chat | `message-share.md` | Always verify source first |

**4-Level Rating**: 🟢 LOW → 🟡 MEDIUM → 🔴 HIGH → ⛔ REJECT
**Trust Principle**: Trust tier only adjusts scrutiny intensity — it never skips review steps.

---

## Activation Triggers

Activate this framework **automatically** when:

- User says "review", "security check", "is this safe", "trust this"
- User says "install", "help me check this", "review"
- Before installing any Skill, MCP Server, npm/pip/cargo package
- Before evaluating a GitHub repo, URL, on-chain address, or product
- When someone recommends a tool in a group chat or social channel

---

## Reviews

### 1. Skill / MCP Installation Review
`references/skill-mcp.md`

File inventory → code audit → architecture assessment → rating.
**MCP-specific coverage**: tool definitions, resource access, prompt injection in prompt templates.

### 2. GitHub Repository Review
`references/repository.md`

Metadata → code audit → GitHub Actions security → dependency review → fork analysis.

### 3. URL / Document Review
`references/url-document.md`

URL safety → **18-category prompt injection scan** → rating.
**Critical**: Scans code blocks line-by-line. Mixed payloads (legitimate + malicious commands combined) are the most dangerous pattern.

### 4. On-Chain Address / Contract Review
`references/onchain.md`

AML risk score → smart contract audit → DApp frontend review → transaction checklist.
**MistTrack + Dune MCP** fallback when API unavailable.

### 5. Product / Service / API Review
`references/product-service.md`

Provider evaluation → architecture security → permission scope analysis → trust chain.

### 6. Social Share Review
`references/message-share.md`

Source assessment → content routing → social engineering detection → response framework.
**DM "support" = almost certainly scam.**

---

## Pattern Libraries

Shared across all review types:

| Pattern | Coverage |
|---------|----------|
| [red-flags.md](references/red-flags.md) | 11 code-level red flag categories |
| [social-engineering.md](references/social-engineering.md) | 8 social engineering & prompt injection patterns |
| [supply-chain.md](references/supply-chain.md) | 7 supply chain attack patterns |

---

## Risk Rating System

| Level | Meaning | Agent Action |
|-------|---------|--------------|
| 🟢 LOW | Information-only, no execution, trusted source | Inform user, proceed if requested |
| 🟡 MEDIUM | Limited capability, clear scope, some risk | Full report, recommend caution |
| 🔴 HIGH | Involves credentials, funds, unknown source | Detailed report, **requires human approval** |
| ⛔ REJECT | Matches red-flag patterns, confirmed malicious | Refuse to proceed, explain why |

---

## Trust Hierarchy

| Tier | Source Type | Base Scrutiny |
|------|-------------|---------------|
| 1 | Official project/exchange org | Moderate — still verify |
| 2 | Known security teams (SlowMist, Trail of Bits) | Moderate |
| 3 | High-download + multi-version Claude Code skill | Moderate-High |
| 4 | High-star + actively maintained GitHub repo | High — must verify code |
| 5 | Unknown source, new account | Maximum scrutiny |

---

## Claude Code Adaptation

| Original (OpenClaw) | Claude Code |
|---------------------|-----------|
| `~/.openclaw/` | `~/.claude/` |
| ClawHub install | Claude Code Skills |
| `openclaw.json` | `CLAUDE.md` |

---

## Installation

**Option 1: Claude Code Skills (recommended)**
```
# Just activate the skill — it auto-registers
/slowmist-security-cc
```

**Option 2: Clone to skills directory**
```bash
git clone https://github.com/0xcjl/slowmist-security-cc.git ~/.claude/skills/slowmist-security-cc
```

---

## File Structure

```
slowmist-security-cc/
├── SKILL.md                           # Main entry point
├── README.md                          # This file (English)
├── README.zh-CN.md                    # Chinese version
├── _meta.json                         # ClawHub metadata
├── LICENSE                            # MIT License
└── references/
    ├── skill-mcp.md                   # Skill/MCP review
    ├── repository.md                  # GitHub repo review
    ├── url-document.md                # URL/document review
    ├── onchain.md                     # On-chain address review
    ├── product-service.md             # Product/service review
    ├── message-share.md               # Social share review
    ├── red-flags.md                   # Code red flag patterns
    ├── social-engineering.md          # Social engineering patterns
    └── supply-chain.md                # Supply chain attack patterns
```

---

## Credits

- **Original framework**: [SlowMist / slowmist-agent-security](https://github.com/slowmist/slowmist-agent-security) — inspired by [skill-vetter](https://clawhub.ai/spclaudehome/skill-vetter) by spclaudehome
- **Attack patterns**: Informed by the [OpenClaw Security Practice Guide](https://github.com/slowmist/openclaw-security-practice-guide)
- **Prompt injection patterns**: Based on real-world PoC research
- **Claude Code adaptation**: 0xcjl

---

*Security is not a feature — it's a prerequisite.* 🛡️

**SlowMist** · https://slowmist.com
