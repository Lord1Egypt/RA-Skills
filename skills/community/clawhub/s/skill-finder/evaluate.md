# Skill Evaluation Criteria — Skill Finder

Reference for assessing skill quality before recommending.

## Quick Assessment (From Search Results)

Check these signals immediately:

| Signal | Good | Concerning |
|--------|------|------------|
| Downloads | >500 | <50 |
| Last update | <3 months | >1 year |
| Description | Clear what + when | Vague or generic |
| Author | Multiple skills | Single anonymous |
| Source package | Clear install string | Ambiguous or incomplete install path |

## Detailed Evaluation

### ClawHub Candidates

After `npx clawhub inspect`:

### Structure Quality

✅ **Good signs:**
- SKILL.md under 100 lines
- Auxiliary files for details
- Clear sections (When to Use, Core Rules)
- Progressive disclosure pattern

❌ **Red flags:**
- Wall of text in single file
- No organization
- Explains obvious concepts
- README/CHANGELOG noise

### Instruction Quality

✅ **Good signs:**
- Imperative voice ("Do X", "Check Y")
- Actionable instructions
- Clear triggers (when to activate)
- Examples where helpful

❌ **Red flags:**
- Passive voice ("Users should consider...")
- Theory without actionable guidance
- Vague instructions ("be careful with...")
- Over-explanation of basics

### Skills.sh Candidates

After `npx skills find` returns a candidate:

✅ **Good signs:**
- Clear install string like `owner/repo@skill`
- Recognizable or maintained source repository
- skills.sh page or repo makes the purpose obvious
- The skill feels installable without extra guesswork

❌ **Red flags:**
- Unclear install target
- Repo with weak description or no obvious maintenance
- Name sounds relevant but source package is confusing
- Requires guessing project vs global scope or target agent without user input

### Fit Assessment

Ask yourself:
- Does it solve the **actual** need?
- Is it too broad (generic) or too narrow (edge case)?
- Does it conflict with skills already installed?
- Is it worth the context cost?

## Scoring (Mental Model)

Rate 1-5 on each:

| Dimension | Question |
|-----------|----------|
| **Relevance** | How well does it match the specific need? |
| **Quality** | How well is the skill built? |
| **Maintenance** | Is it actively maintained? |
| **Value** | Is it worth the context tokens? |

**Recommend if:** All scores ≥3

## Reporting to User

### When Recommending
> "Found `skill-name` — [what it does in one line]. [Quality note]. Want me to install it?"

Example:
> "Found `stripe` — handles payment integration with webhooks and subscriptions. 4k downloads, updated last week. Want me to install it?"

For `Skills.sh`:
> "Found `owner/repo@skill-name` on Skills.sh — [what it does]. Install command is `npx skills add owner/repo@skill-name`. Want me to install it?"

### When Hesitant
> "Found `skill-name` but [concern]. [Alternative or ask if want anyway]."

Example:
> "Found `old-pdf-tool` but it hasn't been updated in 8 months. There's a newer `pdf-toolkit` with similar features — want that instead?"

### When No Good Options
> "Searched for [query] but nothing fits well. [Explain gap]. I can help directly, or you could create a custom skill."

## Comparison Table (Multiple Options)

When presenting several options:

| Skill | Source | Fits Need | Quality | Signal | Updated |
|-------|--------|-----------|---------|--------|---------|
| `option-1` | ClawHub | ⭐⭐⭐ | ⭐⭐⭐ | 5.2k downloads | 2 weeks |
| `option-2` | Skills.sh | ⭐⭐ | ⭐⭐⭐ | trusted repo | 1 month |
| `option-3` | ClawHub | ⭐⭐⭐ | ⭐⭐ | 800 downloads | 3 months |

Then recommend based on user's stated preferences.
