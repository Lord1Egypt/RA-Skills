---
name: skillme
description: Use when user asks to find, search, add, or install skills, or discover agent capabilities. Also triggers on 'install skills', 'add skills', 'is there a skill for X', 'find me a skill that does X', 'search clawhub', 'search skills.sh', 'can you do X', 'how do I do X with a skill', 'extend your capabilities', or when the user provides a GitHub or skills.sh URL to a SKILL.md. Searches ClawHub and skills.sh simultaneously and can auto-convert skills.sh results into OpenClaw-compatible format.
---

# SkillMe

Search ClawHub and skills.sh simultaneously to discover, compare, and install agent skills. Converts skills.sh skills into OpenClaw-compatible format automatically.

## Step 1: Run Parallel Search

Always search both registries at the same time:

```bash
# Run both in parallel, capture output
clawhub search "<query>" &
CLAWHUB_PID=$!
npx skills find <query> 2>&1 &
SKILLS_PID=$!
wait $CLAWHUB_PID $SKILLS_PID
```

Or use exec with two commands in sequence since both are fast:

```bash
echo "=== ClawHub ===" && clawhub search "<query>"
echo "=== skills.sh ===" && npx skills find <query> 2>&1
```

## Step 2: Present Merged Results

Show results in a clean table or list. For each result include:
- **Name** — the skill slug
- **Source** — ClawHub or skills.sh
- **Description/snippet** — what it does
- **Install count** — if available (skills.sh shows this)
- **Install command** — ready to copy-paste

Example output format:

```
Found 4 results for "react":

[ClawHub]
• react-patterns — React component patterns (score: 3.8)
  Install: clawhub install react-patterns

[skills.sh]
• vercel-labs/agent-skills@react-best-practices — 185K installs
  React and Next.js performance optimization from Vercel Engineering
  Install: npx skills add vercel-labs/agent-skills@react-best-practices -g -y
  More: https://skills.sh/vercel-labs/agent-skills/react-best-practices
```

Deduplicate by name when the same skill appears in both registries.

## Step 3: Quality Check Before Recommending

For skills.sh results:
- Prefer skills with 1K+ installs
- Trust official sources: `vercel-labs`, `anthropics`, `microsoft`
- Be skeptical of anything under 100 installs from unknown authors

For ClawHub results:
- Higher score = better semantic match
- Check the slug for recognizable names

## Step 4: Installing Skills

### 1. Choose Location (User Choice)
Before installing, ALWAYS ask the user if they want the skill installed to:
- **Project Workspace (local):** `/root/.openclaw/workspace/skills/<skill-name>/`
- **Global User Skills (shared):** `/root/.openclaw/skills/<skill-name>/`

### 2. ClawHub skills
```bash
# Workspace (default):
clawhub install <slug> --workdir /root/.openclaw/workspace

# Global:
clawhub install <slug> --workdir /root/.openclaw
```

### 3. skills.sh / GitHub skills (Conversion)
When the user wants to install a skills.sh skill directly:
1. Determine the path based on their location choice.
2. Use the convert script:
```bash
python3 /root/.openclaw/workspace/skills/skill-finder/scripts/convert_skillssh.py \
  "<url-or-slug>" \
  --output /path/to/chosen/location/<skill-name>/SKILL.md
```

## Step 5: Verify Installation

After any install, confirm the file exists:

```bash
# For converted skills:
ls /path/to/chosen/location/<skill-name>/SKILL.md

# For clawhub installs:
clawhub list | grep <slug>
```

Tell the user: "Installed and verified at `/path/to/location`."

## Conversion Rules (skills.sh → OpenClaw)

When converting a skills.sh skill:

1. **Extract "When to Use" section** → use as the `description` frontmatter value (make it self-contained with trigger phrases)
2. **Remove "When to Use This Skill" section from body** (it lives in frontmatter now)
3. **Keep all other sections** intact in the body
4. **Folder name** must be kebab-case matching the skill name
5. **Description must include trigger phrases** so OpenClaw can match it correctly

The convert script handles all of this automatically.

## When No Results Are Found

If neither registry returns relevant results:

1. Tell the user no skills were found for that query
2. Suggest alternative search terms
3. Offer to help directly with the task using general capabilities
4. Mention they can create a custom skill: ask if they want Angie to build one

Example:
```
No skills found for "obscure-thing". I can still help directly.
Want me to build a custom OpenClaw skill for this? I'll use the skill-creator.
```

## Common Search Categories

| Need | Try These Queries |
|------|-------------------|
| Web dev | react, nextjs, tailwind, typescript |
| Testing | testing, jest, playwright, e2e |
| DevOps | deploy, docker, kubernetes, cicd |
| Writing | copywriting, blog, seo, content |
| Data | scraping, csv, sheets, analytics |
| Crypto | solana, defi, onchain, wallet |
| Design | ui, ux, design-system, figma |
| Research | research, summarize, news, arxiv |
