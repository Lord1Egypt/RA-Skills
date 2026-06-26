---
name: skill-factory
description: "Meta-skill for creating new agent skills — generates well-structured SKILL.md files with proper frontmatter, triggers, protocols, and rules. Use when building custom skills."
metadata: { "openclaw": { "emoji": "🏭", "homepage": "https://clawhub.ai/NakedoShadow", "os": ["darwin", "linux", "win32"] } }
---

# Skill Factory — Agent Skill Creator

**Version**: 1.1.0 | **Author**: Shadows Company | **License**: MIT

---

## WHEN TO TRIGGER

- User wants to create a new skill for their agent
- User says "create a skill", "make a skill", "new skill for..."
- Formalizing a recurring workflow into a reusable skill
- Publishing to ClawHub or any skill registry

## WHEN NOT TO TRIGGER

- User wants to use an existing skill
- One-time task that won't be repeated

## PREREQUISITES

No binaries required. This skill generates SKILL.md files — pure text output. No external tools, runtimes, or dependencies needed to run the skill-factory itself.

---

## SKILL ANATOMY

Every skill MUST have this structure:

```markdown
---
name: skill-slug-name
description: "When to use this skill and what it does. Include trigger phrases."
metadata: { "openclaw": { "emoji": "X", "requires": { ... }, "os": [...] } }
---

# Skill Name — Subtitle

**Version**: X.Y.Z | **Author**: [Name] | **License**: [License]

## WHEN TO TRIGGER
[Conditions that activate this skill]

## WHEN NOT TO TRIGGER
[Conditions where this skill should NOT be used]

## PREREQUISITES
[Required and optional binaries, tools, and dependencies]

## PROTOCOL / PROCESS
[Step-by-step instructions the agent follows]

## SECURITY CONSIDERATIONS
[What commands run, what data is read, network access, credentials]

## RULES
[Ordered list of constraints and priorities]

## OUTPUT FORMAT
[Template for the skill's output]
```

---

## CREATION PROCESS

### Step 1 — Interview

Ask the user (exactly these 5 questions):
1. **What does the skill do?** (core purpose in one sentence)
2. **When should it trigger?** (keywords, contexts, conditions)
3. **What's the process?** (steps the agent should follow)
4. **What tools does it need?** (binaries, APIs, environment variables)
5. **What should it NEVER do?** (constraints, safety rules)

### Step 2 — Generate Frontmatter

```yaml
---
name: [kebab-case-name]
description: "[Trigger description — what it does and when to use it]"
metadata: { "openclaw": { "emoji": "[relevant emoji]", "homepage": "[publisher URL]", "requires": { "bins": [...], "env": [...] }, "os": ["darwin", "linux", "win32"] } }
---
```

Rules for frontmatter:
- `name`: lowercase kebab-case, unique, descriptive
- `description`: must include trigger phrases for the agent to match
- `metadata`: single-line JSON (OpenClaw parser requirement)
- `requires.bins`: only include if external tools are strictly needed
- `requires.env`: only include if API keys are needed
- `os`: include all three unless the skill is platform-specific

### Step 3 — Write the Body

Structure the skill body following the anatomy above.

Quality checklist:
- [ ] Clear trigger conditions (WHEN TO TRIGGER)
- [ ] Explicit exclusions (WHEN NOT TO TRIGGER)
- [ ] Prerequisites section listing all required and optional tools
- [ ] Step-by-step process (numbered phases)
- [ ] Concrete examples (code blocks, templates)
- [ ] Security considerations (commands, data access, network, credentials)
- [ ] Prioritized rules (numbered, most important first)
- [ ] Output format template
- [ ] No vague instructions ("do the right thing" = bad, "run pytest on all test files" = good)

### Step 4 — Validate

Check the generated skill:
1. Frontmatter parses as valid YAML
2. Metadata is valid single-line JSON
3. Description is under 200 characters
4. All mandatory sections are present (WHEN TO TRIGGER, WHEN NOT TO TRIGGER, PREREQUISITES, SECURITY CONSIDERATIONS, RULES)
5. Every instruction is concrete and unambiguous

### Step 5 — Save and Test

```bash
# Create skill directory
mkdir -p skills/[skill-name]

# Save SKILL.md to the new directory
# (generated content written here)

# Test: start a new agent session and try triggering the skill
# with the phrases listed in the description field
```

---

## SKILL QUALITY TIERS

| Tier | Requirements |
|------|-------------|
| **Draft** | Frontmatter + basic process |
| **Standard** | + WHEN NOT TO TRIGGER + rules + output format |
| **Professional** | + examples + edge cases + testing instructions |
| **Production** | + version history + changelog + published to registry |
| **HIGH TRUST** | + PREREQUISITES + SECURITY CONSIDERATIONS + homepage + concrete instructions |

---

## COMMON PATTERNS

### Pattern: Gate-based (sequential checks)
```
Gate 1: Check X → PASS/FAIL
Gate 2: Check Y → PASS/FAIL
Gate 3: Check Z → PASS/FAIL
Verdict: ALL PASS = proceed
```

### Pattern: Technique Selection (choose one approach)
```
Triage → Classify problem
If type A → Technique 1
If type B → Technique 2
If type C → Technique 3
```

### Pattern: Multi-Round (iterative refinement)
```
Round 1: Explore broadly
Round 2: Challenge assumptions
Round 3: Synthesize
Round 4: Crystallize decision
```

### Pattern: Interview-then-Execute
```
Phase 1: Ask 3-5 clarifying questions
Phase 2: Generate options
Phase 3: User selects
Phase 4: Execute selection
```

---

## SECURITY CONSIDERATIONS

This skill generates text files (SKILL.md) only. It does not execute commands, read sensitive data, make network calls, or modify existing files. The generated skills should be reviewed by the user before publishing, as they may include shell commands in their instructions section. Zero risk from the skill-factory itself; standard review practices apply to generated output.

---

## OUTPUT FORMAT

The output is a complete SKILL.md file written to `skills/[skill-name]/SKILL.md`, following the anatomy structure defined above.

---

## RULES

1. **Unambiguous instructions** — the agent must know exactly what to do at each step
2. **Trigger phrases in description** — this is how the agent matches skills to user requests
3. **Single-line metadata JSON** — OpenClaw parser requires metadata on one line
4. **WHEN NOT TO TRIGGER is mandatory** — prevents false activations
5. **Test before publishing** — try the skill in a real session before distributing

---

**Published by Shadows Company — "We work in the shadows to serve the Light."**
