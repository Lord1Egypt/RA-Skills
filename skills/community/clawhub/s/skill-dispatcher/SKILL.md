---
name: skill-dispatcher
description: >-
  Proactive skill router that prevents forgetting available skills.
  Triggers on any non-trivial task. Routes user intent to available skills
  via a decision tree, enhancer layer, and anti-forget gates.
  Use when you have multiple skills installed and want to ensure none are forgotten.
  First run: scan available_skills list, fill the routing table template, and activate.
---

# Skill Dispatcher — Universal Skill Router

## §0 Configuration (READ FIRST)

Before this skill works, you MUST fill the routing table with YOUR skills:

1. Scan `<available_skills>` in your system prompt
2. Run `scripts/coverage_check.py <skill1> <skill2> ...` — lists uncovered skills
3. Fill each uncovered skill into the routing table below at `<!-- TODO -->` markers
4. Add 2-5 trigger keywords per skill
5. Set frequency (⭐/⭐⭐/⭐⭐⭐) based on how often the skill is used
6. Re-run coverage check — should show "All skills covered"

**Trigger keyword rules:**
- Use phrases the user would naturally say
- Avoid single common words (e.g. "write", "search")
- Test: "If the user said ONLY this phrase, would it match?"

---

## ⚡ Direct Hits (FIRST — 2 seconds)

If user message contains an **exact keyword match**, skip Q1/Q2 and route directly:

| Exact phrase | Direct route |
|---|---|
| <!-- TODO: add 3-6 most common unambiguous triggers --> |

If NOT a direct hit → proceed to decision tree.

---

## 🔴 Quick Decision Tree

```
Q1: Your primary domain?
    ├─ <!-- TODO: add your most common task categories -->
    ├─ category_A / trigger_A → skill_A
    ├─ category_B / trigger_B → skill_B
    ├─ category_C / trigger_C → skill_C (chain if needed)
    └─ ...

    ⚠️ CHAIN RULE: "→" = read 1st skill, execute, THEN read 2nd.
    ⚠️ NO chain for non-multi-step tasks.

Q2: Anything else?
    → Scan Full Routing Table below.
    → No match? Proceed normally.

Q3: Enhancer layer?  ← auto-apply, not user-requested
    After routing to primary skill/tool, check if output needs enhancement:
    ├─ 生成图/图表/UI/配色 → aesthetic, Color Palette Generator, data-viz-palette
    ├─ 生成大段文字/解释   → humanizer
    ├─ 上下文/文件膨胀      → token-optimizer
    ├─ 复杂多步任务         → agent-planner (先规划再执行)
    ├─ 被用户纠正/发现错误  → Self-Improving + Proactive Agent
    ├─ 设计skill/prompt    → context-engineering, prompt-engineer
    └─ 无增强需求           → skip

    ⚠️ 🔴 COMPLIANCE TAG REQUIRED on every user-visible output:
       After routing, append ONE LINE: [enh: skill §specific-parameter]
       Read the enhancer → extract concrete principle → encode it.
       Example: [enh: aesthetic §card间距48px|DP步32px|蓝绿红三色语义]
       Example: [enh: —] means no enhancer applied (internal ops only).
       
       ⚠️ If output involves drawio/mermaid/image_generate/code:
          AND no [enh:] tag present → auto-flagged as violation.
       ⚠️ Generic words without numbers = same as not reading.
       ⚠️ Copying the same [enh:] tag across different tasks = flagged for review.

Q4: Background health?  ← session-state triggers (every ~10 exchanges)
    ├─ Context usage >50% or >10 exchanges → token-optimizer
    ├─ Recent tool failures/timeouts       → healthcheck
    ├─ Bulk file create/delete/reorg       → lobster-workspace-guardian
    └─ All clear                           → skip

    💡 Check with: session_status (📊 session_status tool)
    💡 Not every message — every ~10 exchanges or when things feel off.
```

---

## 🚨 Anti-Forget Gates (backup — when dispatcher NOT loaded)

These are your belt-and-suspenders. If the dispatcher's description didn't match
and you're about to take one of these actions raw, this section catches it.
If the dispatcher IS loaded, the decision tree already handled routing — skip this.

| You are about to... | STOP and check... |
|---|---|
| Write code / explain algorithm | Any code/algorithm skill you have |
| Call `web_search` | Search/scraping skills (they have better extraction) |
| Call `web_fetch` | Web content fetching skills |
| Read/write/clean memory | Memory management skills |
| Delete or reorganize files | Workspace janitor skills |
| Create or modify a skill | Skill creation skills |
| Do anything on GitHub | GitHub skills |
| Generating diagram/image/visual | 🔴 Aesthetic/design skills — read SKILL.md, do NOT skip |
| Writing long explanation/text | 🔴 Humanizer/text quality skills — read SKILL.md, do NOT skip |
| User corrected you / found mistake | 🔴 Self-improvement skills — read SKILL.md, do NOT skip |

---

## 🔼 Enhancer Skills (Q3 layer — auto-triggered by output type)

These are NOT standalone skills. They **overlay** on top of a primary skill/tool.
User doesn't need to ask for them — check automatically when output matches:

| Enhancer | Triggers when... | Priority |
|---|---|---|
| <!-- TODO: aesthetic skill --> | Generating image/diagram/visual → improve visual quality | ⭐⭐ |
| <!-- TODO: color palette skill --> | New diagram/chart/UI → pick color scheme | ⭐⭐ |
| <!-- TODO: humanizer skill --> | Writing long text/explanation → make it more natural | ⭐⭐ |
| <!-- TODO: token optimizer skill --> | Context growing / files bloated → trim | ⭐⭐ |
| <!-- TODO: planner skill --> | Complex multi-step task → plan before execute | ⭐⭐ |
| <!-- TODO: self-improvement skill --> | User corrects you / you find a mistake | ⭐⭐⭐ |

---

## 📋 Full Routing Table

### <!-- TODO: Category 1 — your primary domain -->
| Trigger | Skill | Freq |
|---|---|---|
| <!-- trigger keywords --> | <!-- skill-name --> | ⭐ |

### <!-- TODO: Category 2 — memory/knowledge -->
| Trigger | Skill | Freq |
|---|---|---|
| <!-- trigger keywords --> | <!-- skill-name --> | ⭐ |

### <!-- TODO: Category 3 — browser/desktop -->
| Trigger | Skill | Freq |
|---|---|---|
| <!-- trigger keywords --> | <!-- skill-name --> | ⭐ |

### <!-- TODO: Category 4 — content/search -->
| Trigger | Skill | Freq |
|---|---|---|
| <!-- trigger keywords --> | <!-- skill-name --> | ⭐ |

### <!-- TODO: Category 5 — dev/tools -->
| Trigger | Skill | Freq |
|---|---|---|
| <!-- trigger keywords --> | <!-- skill-name --> | ⭐ |

### <!-- TODO: Category 6 — workflow -->
| Trigger | Skill | Freq |
|---|---|---|
| <!-- trigger keywords --> | <!-- skill-name --> | ⭐ |

### <!-- TODO: Category 7 — design/creative -->
| Trigger | Skill | Freq |
|---|---|---|
| <!-- trigger keywords --> | <!-- skill-name --> | ⭐ |

### <!-- TODO: Category 8 — system/meta -->
| Trigger | Skill | Freq |
|---|---|---|
| <!-- trigger keywords --> | <!-- skill-name --> | ⭐ |

---

## 🔄 Fallback Protocol + Coverage Gap Detection

If NO routing table match but you SUSPECT a skill exists:
1. Scan the `<available_skills>` list in current context
2. **Coverage check**: Compare every skill in `<available_skills>` against names in the routing table + Direct Hits.
   - If a skill exists in `<available_skills>` but NOT in this dispatcher → 🚨 **uncovered skill detected** → trigger [New Skill Onboarding](#-new-skill-onboarding-protocol)
3. If still unsure → read `references/skill-capabilities.md` for full capability details
4. If the skill doesn't exist locally → search Clawhub or other registries
5. If still nothing → proceed with built-in tools

---

## 🆕 New Skill Onboarding Protocol

When a new skill is detected, follow the full 6-step protocol:
→ **[references/onboarding.md](references/onboarding.md)** — Detection → Classify → Draft → 3-Round Review → Commit → Log

---

## 🔗 System Integration

- Your agent workspace files (SOUL.md, AGENTS.md, TOOLS.md) should reference this dispatcher
- Add a line to your core rules: "每次回复前先问哪个 skill 能处理这个任务？路由细节见 skill-dispatcher"
- The system prompt already instructs "scan available_skills, read matching SKILL.md". The dispatcher makes this scan systematic.

---

## 📊 Self-Correction Protocol + Output Compliance

### [enh:] Output Tagging
Every user-visible output that involves drawio/mermaid/code/image generation
MUST carry an [enh:] tag. Format: [enh: skill §concrete-principle-applied].
No tag → violation. Generic words without specifics → same as not reading.

### When you realize you forgot a skill
1. Check if repeat — search memory for prior forgets
2. If 2nd+ time → write correction: date, skill, task, root cause
3. Always fix the immediate task.

### External audit (if you have automated checks)
Set up periodic scanning for missing [enh:] tags on visual/code outputs.
Repeat violations → upgrade enhancer priority or add to Direct Hits.

### Why 2-strike threshold?
Writing memory on every single forget creates noise. Repeated patterns persist.

---

## 📖 References

- **[skill-capabilities.md](references/skill-capabilities.md)** — Full capability descriptions for reference (fill with YOUR skills)
- **[onboarding.md](references/onboarding.md)** — 6-step protocol for integrating new skills

---

## 📋 Covered Skills Registry

<!-- Keep this list in sync with routing table + Direct Hits. Used for coverage gap detection. -->
<!-- Last sync: [DATE] -->
<!-- Fill with your skill names: `skill1` `skill2` `skill3` ... -->
