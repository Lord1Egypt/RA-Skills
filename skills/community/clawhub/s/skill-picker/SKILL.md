---
name: skill-picker
description: Discovers and recommends the best agent skills based on user intent — not just keywords. Activates when users ask "how do I do X", "find a skill for X", "is there a skill that...", or whenever a task would benefit from a specialized skill. Also activates proactively when the agent detects repeated manual tasks, workflow gaps, or missing capabilities mid-conversation. Supports English and Chinese. Recommends skill combinations, not just single skills. This skill only suggests install commands — it never executes installs autonomously. All installs require explicit user confirmation.
tools:
  - npx
binaries:
  - npx
---

# Skill Picker

Discover and recommend the right skills at the right moment.

> **What this skill does with `npx`**: It runs `npx skills find [query]` to search the skills registry and display results. It does NOT run `npx skills add` on its own — install commands are always shown to the user for manual execution or explicit confirmation.

---

## Core Philosophy

**Don't match keywords. Understand intent.**

The difference:
- Keyword match: User says "GitHub" → search "github"
- Intent match: User says "我的PR没人review" → understand they need async code review automation → recommend `gh-issues` + `coding-agent` as a combination

Always ask: *What outcome does the user actually want?* Then find the shortest path to that outcome using available skills.

> **Security principle**: `npx skills find` is used for searching only. `npx skills add` is only ever shown as a command for the user to run themselves — never executed autonomously.

---

## When to Activate

### Explicit triggers (user asks directly)
- "find a skill for X"
- "is there a skill that can..."
- "how do I automate X"
- "can you do X" (where X is specialized)
- "我想自动化X" / "有没有能做X的skill"
- "帮我找一个可以..."

### Implicit triggers (proactive — suggest only, never auto-install)
Suggest when you detect:

- **Repetition**: User manually does the same thing 2+ times in a session → suggest a skill that could help
- **Friction**: User copy-pastes between tools → suggest an integration skill
- **Capability gap**: User asks for something you can't do well alone → find a skill that fills the gap
- **Workflow opportunity**: User completes step 1 of a multi-step process → suggest skills for steps 2-3

Example proactive suggestion:
> User manually summarizes a PDF, then pastes it somewhere else.
> → "I notice you're doing this manually. The `summarize` skill could automate this flow. Want me to show you how to install it?"

**Important**: Proactive suggestions are informational only. Never run `npx skills add` unless the user explicitly confirms they want to install.

---

## Intent Analysis Framework

Before searching, extract three things:

```
1. OUTCOME    — What does the user want to have/feel/achieve?
2. OBSTACLE   — What's standing between them and that outcome?
3. CONTEXT    — Who are they? What tools do they already use?
```

### Intent Translation Examples

| User says | Outcome | Obstacle | Best skill search |
|-----------|---------|----------|-------------------|
| "help me review this PR" | Merged, high-quality code | Manual review takes time | `pr review` + `gh-issues` |
| "I need to send updates to my team" | Team is informed | Manually composing messages | `gog` (Gmail) or `feishu-doc` |
| "summarize this YouTube video" | Get key points fast | Can't watch 2-hour video | `summarize` |
| "我想监控竞品动态" | Know when competitors ship | No alert system | `blogwatcher` + `summarize` |
| "帮我管理邮件" | Zero inbox | Too many emails | `himalaya` + `gog` |
| "我的日历太乱了" | Clear, organized schedule | Manual scheduling | `gog` calendar + proactive-agent |

---

## Search Process

### Step 1: Clarify if ambiguous (max 1 question)

If the intent is unclear, ask ONE focused question:
> "Are you looking to automate this completely, or just get help doing it faster?"

Never ask more than one clarifying question. Make a reasonable assumption and proceed.

### Step 2: Search with intent-based queries

```bash
# This is the ONLY npx command this skill executes autonomously
npx skills find [intent-based query]
```

Use **outcome words**, not task words:
- ❌ `npx skills find email` (too broad)
- ✅ `npx skills find email automation inbox zero` (outcome-focused)
- ❌ `npx skills find github`
- ✅ `npx skills find pull request review automation notify` (outcome-focused)

Try 2-3 different query angles before concluding nothing exists.

### Step 3: Evaluate results with quality signals

When presenting skills, always include:
- **Download count** (from skills.sh) — proxy for reliability
- **Combination potential** — does it work better with another skill?
- **Fit score** — how well does this match the user's specific outcome?

### Step 4: Recommend combinations, not just single skills

Most outcomes need more than one skill. Think in workflows:

```
User outcome: "Keep my team updated automatically"

Single skill answer (weak):
→ gog (Gmail)

Combination answer (strong):
→ gog (send updates) + summarize (condense content) + proactive-agent (trigger automatically)
→ "These three together handle the full workflow: detect → summarize → send"
```

---

## Response Format

### When skills are found

```
I found [N] skill(s) that match what you're trying to do.

**Best match: [Skill Name]** (★ [stars] · [downloads] installs)
[One sentence: what outcome this enables, not what it does technically]

To install, run this command yourself:
  npx skills add [owner/repo@skill]

Learn more: https://skills.sh/[path]

---
[If combination recommended:]
**Works even better with: [Skill Name 2]**
Together, these handle [full workflow description].

To install both, run:
  npx skills add [skill1]
  npx skills add [skill2]

---
Let me know if you'd like more details before installing.
```

> ⚠️ Always present `npx skills add` commands for the user to run manually — never execute them on behalf of the user without explicit confirmation.

### When no skills are found

Don't just give up. Three-part response:

```
1. CONFIRM: "I searched for [X] and [Y] but didn't find an exact match."

2. CLOSEST: "The closest available skill is [name] — it covers [overlap],
   though it doesn't handle [gap]."

3. OPTIONS:
   a) "I can handle this directly with my built-in capabilities — want me to proceed?"
   b) "This seems like a common enough need that a skill should exist.
       You could create one: npx skills init [suggested-name]"
   c) "Check skills.sh directly — the ecosystem updates frequently."
```

---

## Common Skill Categories & Best Searches

### Productivity & Communication
| Need | Search query | Top skills |
|------|-------------|------------|
| Email management | `email inbox automation` | `himalaya`, `gog` |
| Calendar scheduling | `calendar scheduling meeting` | `gog` |
| Team updates | `team notification summary` | `gog`, `feishu-doc` |
| Document creation | `document write generate` | `feishu-doc`, `prose` |

### Development & Code
| Need | Search query | Top skills |
|------|-------------|------------|
| PR review | `pull request review code` | `gh-issues`, `coding-agent` |
| Issue management | `github issues automate` | `github`, `gh-issues` |
| Code changes | `diff review changes` | `diffs` |
| Multi-agent coding | `agent code build` | `coding-agent`, `prose` |

### Knowledge & Research
| Need | Search query | Top skills |
|------|-------------|------------|
| Summarize content | `summarize url pdf video` | `summarize` |
| Monitor updates | `monitor rss blog watch` | `blogwatcher` |
| Search places | `places search location` | `gsplaces` |
| Agent memory | `memory knowledge graph` | `ontology` |

### System & Automation
| Need | Search query | Top skills |
|------|-------------|------------|
| Self-improvement | `agent learn improve` | `self-improving-agent` |
| Find more skills | `discover install skills` | `skill-picker` |
| Security check | `security audit skill vetting` | `skill-vetter` |
| Smart routing | `route model ai select` | `acp-router` |

### Hardware & Home
| Need | Search query | Top skills |
|------|-------------|------------|
| Music control | `sonos speaker audio` | `sonoscli` |
| Sleep tracking | `sleep pod temperature` | `eightctl` |
| Camera capture | `camera rtsp snapshot` | `camsnap` |

---

## Proactive Skill Suggestions (Mid-conversation)

If during any task you notice a skill would significantly improve the outcome, mention it naturally:

> "There's a skill called `[name]` that would help here. Want me to show you the install command?"

Then wait for the user to confirm before providing the command. **Do not run any install command proactively.**

Threshold for suggesting: skill would save >2 manual steps OR significantly improve output quality.

Don't suggest more than one new skill per conversation unless the user is explicitly building a workflow.

---

## Commands Reference

```bash
# EXECUTED BY THIS SKILL (search only):
npx skills find [query]

# SHOWN TO USER FOR MANUAL EXECUTION (never auto-run by this skill):
npx skills add <owner/repo@skill>   # install a skill
npx skills check                    # check for updates
npx skills update                   # update all skills
npx skills init <skill-name>        # create a new skill

# Browse all skills
open https://skills.sh/
```

> ℹ️ `npx skills add` is intentionally shown without `-g` or `-y` flags. Users should decide install scope themselves and confirm each install interactively.

---

## Quality Signals to Always Check

Before recommending, verify at skills.sh:

```
✓ Download count > 10k = proven, reliable
✓ Stars > 100 = community validated
✓ Recently updated = actively maintained
✓ From known publisher (steipete, pskoett, openclaw) = higher trust
✗ Stars << Downloads = installed but not loved, use with caution
✗ No updates in 6+ months = may have API compatibility issues
```

---

## Language Support

This skill operates in the user's language.

- If user writes in Chinese → respond in Chinese, search in English, present results in Chinese
- If user writes in English → respond in English throughout

Chinese intent → English search translation examples:
- "帮我自动回复邮件" → `email auto-reply automation`
- "监控竞品网站更新" → `website monitor change detection`
- "整理我的GitHub Issues" → `github issues organize triage`
- "把会议内容发给团队" → `meeting summary team notification`
