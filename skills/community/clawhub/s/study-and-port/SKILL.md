---
name: study-and-port
description: "Research new AI frameworks or technologies, extract their best features, evaluate feasibility, and implement as OpenClaw skills. Triggered when: (1) user mentions a new framework, (2) discovers features other frameworks have that OpenClaw lacks, (3) wants to learn from other AI assistants."
metadata:
  requires:
    bins: [node]
  permissions:
    - write: ~/.openclaw/workspace/skills/
    - write: ~/self-improving/
---

## Safety & Boundaries

- **Always ask user before creating new skills or scripts**
- **Never auto-execute created scripts without confirmation**
- **Research only — do NOT implement features that require core OpenClaw changes**
- **Report findings to user, let them decide what to keep**

# Study and Port — Research &移植框架优点

> _"Don't just use other AI frameworks — learn from them."_

When you discover an AI framework or tool with features worth learning, execute this skill.

---

## Trigger Conditions

- User mentions a new AI framework or tool
- Discover features in other frameworks that OpenClaw doesn't have
- Want to learn from other AI assistants' strengths

---

## Workflow

### Step 1 — Quick Overview (10 min)

**Search endpoint:** Use MiniMax web search (configured in TOOLS.md)

Use search to understand:

**Template A (General Framework):**
```
"[framework name] features capabilities 2026"
"[framework name] vs OpenAI agent differences"
"[framework name] Hermes Agent comparison"
```

**Template B (AI Coding Assistants):**
```
"[framework name] features capabilities 2026"
"[framework name] self-improving memory workflow"
```

**Template C (Chinese Frameworks):**
```
"[framework name] 特点 功能 优势"
"[framework name] 和 OpenClaw 对比"
```

Collect:
- Framework name and version
- Core features (3-5)
- Design philosophy
- How it differs from OpenClaw

### Step 2 — Deep Dive (as needed)

For each core feature:
```
"[framework name]" "[specific feature]" "how it works"
"[framework name]" "implementation" "architecture"
```

Extract the 3-5 most valuable learnings.

### Step 3 — Feasibility Evaluation

For each feature, answer:

| Question | ✅ Yes | ❌ No |
|----------|--------|-------|
| Can this be implemented as SKILL.md? | Mark "portable" | Mark "requires core change" |
| Does it need OpenClaw source changes? | Mark "requires core" | Mark "portable" |
| Does it need external APIs? | Check API availability | Mark "API dependent" |
| Would users benefit from this? | Keep | Mark "low value" |

**Portability Rating:**
- 🌟 **Portable (skill)** — implementable as SKILL.md ± scripts
- 🔧 **Partially Portable** — core part doable, limitations exist
- 🏗️ **Requires Core Change** — needs OpenClaw source modification
- ⏳ **Wait & Watch** — tech not mature enough

### Step 4 — Create Skill (if portable)

**User confirmation required:** Before creating any new skill or script, ALWAYS ask user:
- "这个框架的 [功能] 值得移植，我要创建新 skill，可以吗？"

For each "portable" feature:

1. **Write SKILL.md:**
   - Clear trigger conditions
   - Detailed execution steps
   - Usage boundaries
   - Script location if needed

2. **Write Scripts (if needed):**
   - Scripts must be independently runnable
   - Must handle errors (network failure, file not found, etc.)
   - Node.js runtime must be available (declare in metadata)

3. **Validate:**
   ```bash
   ls ~/.openclaw/workspace/skills/[skill-name]/
   node ~/.openclaw/workspace/skills/[skill-name]/scripts/[script].js --help
   ```

**Permissions required:**
- Write access to `~/.openclaw/workspace/skills/` (for new skill files)
- Write access to `~/self-improving/` (for log files)
- Node.js runtime (pre-installed with OpenClaw)

### Step 5 — Log to Procedural Memory

Append to `~/self-improving/procedural-memory-log.md`:

```markdown
## YYYY-MM-DD

### [Framework] Research
- **Research subject**: [framework name]
- **Features extracted**: [list portable features]
- **Deemed non-portable**: [list with reasons]
- **Skill created**: [skill-name]
- **Portability rating**: 🌟 Fully portable / 🔧 Partially / 🏗️ Core required
```

### Step 6 — Report to User

Tell user:
- What interesting features were found
- Which are portable, which aren't
- What skill was created

---

## Multi-Session Research Tracking

If research spans multiple sessions:

Create `~/self-improving/study-progress.md`:

```markdown
# [Framework] Research Progress

## Started: YYYY-MM-DD
## Status: 🔄 In Progress / ✅ Complete

## Completed
- [ ] Quick overview
- [ ] Core feature analysis

## Pending
- [ ] Feasibility evaluation
- [ ] Skill creation

## Key Findings (update anytime)
-
```

Read this file when resuming research.

---

## Decision Tree: Should I Port?

```
Discover new framework
    │
    ▼
Does OpenClaw already have this feature?
    │
    ├─ Yes → Skip, not worth researching
    │
    └─ No or Not Sure → Continue
              │
              ▼
        Would users benefit from this?
              │
              ├─ Not sure → Ask user: "Should I research [framework]?"
              │
              └─ Yes → Continue
                        │
                        ▼
                  Can it be implemented as a skill?
                        │
                        ├─ Yes → Create skill
                        │
                        ├─ Partial → Create core part, note limitations
                        │
                        └─ No (requires core change) → Log to future features
```

---

## References

- Procedural Memory System: `../procedural-memory/SKILL.md`
- Skill Creator Guide: `../skill-creator/SKILL.md`
- Self-Improving Memory: `~/self-improving/memory.md`
