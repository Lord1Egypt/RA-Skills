# social-org-research

> Research a B Corp / social enterprise / NGO / youth culture brand with a 10-dimension framework, `depth: quick | deep` switch, and a verified case study.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Skill](https://img.shields.io/badge/type-agent%20skill-blueviolet)](./SKILL.md)
[![Platforms](https://img.shields.io/badge/platforms-Hermes%20%7C%20Claude%20Code%20%7C%20OpenClaw-lightgrey)](#platforms)
[![Version](https://img.shields.io/badge/version-0.1.0-success)](./CHANGELOG.md)

---

## What It Does

`social-org-research` is a structured research prompt and evaluation framework for investigating **social innovation organizations** — B Corps, social enterprises, NGOs, public-interest platforms, youth culture brands, and other "business as a force for good" entities.

Unlike generic market research, this skill targets organizations whose business model mixes revenue with mission: sponsored content, donor relationships, volunteer labor, paid partnerships with global NGOs, government grants, and "co-creator" rather than "sponsor" brand relationships.

It comes with a **10-dimension framework**, a **`depth: quick | deep` switch**, and a **case study from a real BottleDream research session** that demonstrates the skill in action.

---

## Why Use It

| Without `social-org-research` | With `social-org-research` |
|--------------------------------|------------------------------|
| "How does this NGO make money?" → confused silence | Concrete revenue categories: media / content sponsorship / training / consulting / co-branded products / event sponsorship |
| "Are volunteers paid?" → speculation based on Chinese nonprofit stereotypes | Reference to the Volunteer Service Regulations and the 5-non-cash-hook framework |
| "What's the difference between co-creator and sponsor?" → blur | Clear taxonomy: co-creator = brings plan + resources + product to solve the issue; sponsor = pays for naming rights |
| "The registered capital is 1M RMB — is the company small?" | Distinction: registered capital ≠ actual scale; cross-reference LinkedIn / B Lab / office size |

---

## Use Cases

| Scenario | Use this skill? |
|----------|-----------------|
| Researching a B Corp, social enterprise, or co-benefit company | Yes |
| Investigating an NGO, public-interest platform, or foundation | Yes |
| Mapping a youth culture brand's content + event + community operations | Yes |
| Trying to understand how a "social good" organization makes money | Yes |
| Quick competitive scan before a pitch meeting | Yes (`depth: quick`) |
| Researching a commercial product or B2B SaaS company | No — use `market-research` instead |
| Literature review for an academic paper | No — use `academic-research` instead |
| Investigating industry trends across many players | No — use `deep-research` instead |

---

## Trigger Keywords

**English:** `social enterprise`, `B Corp`, `co-benefit`, `co-benefit enterprise`, `social innovation`, `NGO research`, `youth culture brand`, `public-interest platform`, `B Impact Assessment`, `BIA score`, `social good`, `volunteer benefits`, `co-creator vs sponsor`

**Chinese (informational only — package itself is English-only):** 调研 NGO / 共益企业 / 社会企业 / 公益平台 / B 型企业 / 青年文化品牌 / 商业向善 / 创变者 / 志愿者报酬 / 影响力投资

---

## Quick Start

### 1. Install (Hermes / OpenClaw)

```bash
hermes skills install 0xcjl/social-org-research
# or, from local source
ln -s ~/.hermes/skills/social-org-research ~/.openclaw/workspace/skills/social-org-research
```

### 2. Use it

In any agent conversation, invoke the skill and pass a target:

```
Research BottleDream, depth: deep
```

The skill auto-loads, walks through 10 dimensions, and produces a Markdown + clickable-link PDF.

---

## Architecture

```
social-org-research/
├── SKILL.md                      # The skill body (loaded by agents)
├── README.md                     # This file
├── INSTALLATION.md               # Hermes / OpenClaw / Claude Code install guide
├── LICENSE                       # MIT
├── CHANGELOG.md                  # Version history
└── references/
    └── case-bottledream.md       # Real-world case study (simplified)
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `gh auth status` fails | `gh auth login` |
| `clawhub publish` rejects YAML | Validate with `python3 -c "import yaml; yaml.safe_load(open('SKILL.md').read().split('---')[1])"` |
| Topics count differs from expected | Re-run `gh repo edit --add-topic` for each missing tag |
| README doesn't render | Preview with `grip -b README.md` locally |
| Skill loads but description triggers wrong | Edit frontmatter `description` (keep ≤60 chars to avoid index truncation) |

---

## Platforms

| Platform | Compatible? | Notes |
|----------|-------------|-------|
| Hermes | Yes | `~/.hermes/skills/social-org-research/` |
| OpenClaw / Claude Code | Yes | Symlink to `~/.openclaw/workspace/skills/social-org-research/` |
| Other SKILL.md readers | Yes | Standard YAML frontmatter + markdown body |

---

## Credits

- **Author:** 0xcjl
- **License:** MIT
- **Case study source:** A real BottleDream research session conducted by the author with this skill, September 2026
- **Skill publisher workflow:** `agent-skill-publisher` — 9-step end-to-end publish workflow

---

## License

MIT (c) 2026 0xcjl
