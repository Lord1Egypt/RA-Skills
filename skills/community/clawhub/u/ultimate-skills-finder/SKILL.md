---
name: ultimate-skills-finder
description: "The ultimate multi-source OpenClaw/agent skills finder. Searches across ClawHub, skills.sh, Rush registry, LobeHub, SkillsMP, llmbase.ai, skillsllm.com, and GitHub curated collections — then cross-references, deduplicates, ranks by popularity, and optionally security-scans via Gen Digital. Use when: (1) user says 'find a skill for X', 'is there a skill that can...', 'how do I do X with OpenClaw', (2) user wants to discover new agent capabilities, (3) user asks what skills exist for a specific domain or task, (4) user wants to install a skill but isn't sure which one, (5) user wants to compare skills across multiple registries."
---

# Ultimate Skills Finder 🔍

Searches **5 sources** (ClawHub, SkillsMP, awesome-list, master-skills, skills.sh) for OpenClaw/agent skills, cross-references results, and returns ranked deduplicated findings with install instructions and optional security scanning.

## Quick Start

```bash
python3 scripts/find_skill.py "web scraping" --scan
python3 scripts/find_skill.py "pdf editor"
python3 scripts/find_skill.py "seo tools" --popular
python3 scripts/find_skill.py "github" --scan --install
```

## Sources Searched

| # | Source | Type | Skills | CLI/Tool |
|---|--------|------|--------|----------|
| 1 | **ClawHub** (clawhub.ai) | Primary registry | ~20,000 | `clawhub search` |
| 2 | **skills.sh** (Vercel) | Directory | ~87,000 | `npx skills add` |
| 3 | **SkillsMP** (skillsmp.com) | Aggregator | 1,000,000+ | REST API |
| 4 | **GitHub: awesome-openclaw-skills** | Curated | 5,200+ | README |
| 5 | **GitHub: openclaw-master-skills** | Curated | 560+ | README |

## Workflow

### Step 1: Understand the Need

When the user says "find me a skill for X", identify:
- The specific task/domain (e.g., "web scraping", "PDF editing", "SEO")
- The platform (OpenClaw, Claude Code, Cursor, etc.)
- Whether they want security scanning

### Step 2: Run the Finder Script

```bash
python3 scripts/find_skill.py "<query>" [options]
```

**Options:**
- `--scan` — Security-scan results via Gen Digital
- `--popular` — Sort by popularity/install count
- `--limit N` — Max results per source (default: 5)
- `--json` — Output as JSON for programmatic use
- `--install` — Show install commands prominently
- `--source <name>` — Only search specific source(s)

### Step 3: Interpret Results

The script outputs a ranked, deduplicated table:

```
🔍 Results for "web scraping" (6 found across 9 sources)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🥇 agent-browser-cli          ★★★★☆  12.4k ⬇  [ClawHub, SkillsMP, llmbase]
   Headless browser automation with accessible tree
   → clawhub install agent-browser-cli
   → npx skills add user/agent-browser-cli

🥇 firecrawl                   ★★★★☆  8.2k ⬇   [ClawHub, GitHub awesome]
   Web scraping with Firecrawl API
   → clawhub install firecrawl

🥈 playwright-mcp             ★★★☆☆  3.1k ⬇   [ClawHub, SkillsMP]
   Browser automation via Playwright MCP
   → clawhub install playwright-mcp

🔒 Security: 2/3 skills scanned SAFE. 1 pending review.
```

### Step 4: Security Scan (Optional)

Run with `--scan` to check skills via Gen Digital's API:

```bash
python3 scripts/find_skill.py "email" --scan
```

The scanner checks each unique skill URL and returns:
- `SAFE` — OK to install
- `analysis_pending` — Not yet reviewed, caution advised
- `WARNING` / `DANGEROUS` / `MALICIOUS` — Do not install

### Step 5: Present & Install

Present the top 3-5 most relevant results:
1. Skill name + description
2. Sources where it was found (confirms it's well-known)
3. Install commands (primary method)
4. Security verdict if scanned

Then ask which one(s) to install and do it:

```bash
# ClawHub
clawhub install <slug>

# skills.sh
npx skills add <owner/repo>

# Manual (from GitHub)
git clone <repo> ~/.openclaw/workspace/skills/<name>
```

## Cross-Reference Logic

Results are deduplicated by fuzzy name matching across all sources. A skill found in **3+ sources** gets a confidence boost. The ranking formula:

```
score = (source_count * 0.3) + (install_count_normalized * 0.4) + (source_authority * 0.3)
```

Where:
- `source_count`: How many registries list this skill (0-10)
- `install_count_normalized`: Popularity within its source (0-1)
- `source_authority`: Official ClawHub > curated lists > aggregators > individual repos

## When No Results Found

If the finder returns nothing:
1. Try a broader or synonym query (e.g., "email" → "smtp" → "messaging")
2. Check if the skill might exist under a different ecosystem
3. Offer to create a custom skill using `skill-creator`
