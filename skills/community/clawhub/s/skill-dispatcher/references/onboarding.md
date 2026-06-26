# New Skill Onboarding Protocol

> **When**: A new skill is installed, OR coverage gap detected, OR skill-creator/clawhub was just used.
> **Goal**: Integrate the new skill into the dispatcher's routing table before it goes unused.

## Step 1: Detect
Triggered by any of:
- Fallback Protocol finds skill in `<available_skills>` not in routing table
- `skill-creator` finishes creating a skill
- `clawhub` installs a skill
- Session startup: quick diff of available_skills vs routing table

## Step 2: Classify
Read the new skill's SKILL.md. Determine:
- **Category**: Which section does it belong to? (CP, Memory, Browser, Content, Dev, Workflow, Design, System)
- **Is it CP-related?** → Needs Q1 decision tree entry + possibly chain rule
- **Is it high-frequency?** → Candidate for ⚡Direct Hits
- **Overlaps with existing skill?** → Needs disambiguation note

## Step 3: Draft Routing Entry
Write the routing entry in standard format:
```
| <trigger keywords> | <skill-name> | ⭐ (start low, upgrade by usage) |
```
Rules for trigger keywords:
- Use 2-5 short Chinese/English phrases the user would naturally say
- Test: "If the user said ONLY this phrase, would it match?"
- Avoid single common words (e.g., "写" alone, "看" alone)
- If CP-related: also draft Q1 decision tree branch
- If direct-hit-worthy: add to ⚡Direct Hits table

## Step 4: 3-Round User-Perspective Review ⚠️ MANDATORY

**Round 1 — Happy path**: Simulate 3 common user requests that SHOULD trigger this skill.
- Does each request hit the routing entry?
- Is the routing unambiguous?

**Round 2 — False positive guard**: Simulate 3 requests that contain the trigger keywords but SHOULD NOT trigger this skill.
- Would there be a misroute? If yes → narrow the trigger.

**Round 3 — Edge cases**:
- Mixed intent (user mentions two things, one CP one not)
- Vague request (user assumes you know which skill)
- Cross-skill scenario (this skill + another in sequence → does the chain make sense?)

Only proceed to Step 5 after ALL 3 rounds pass.

## Step 5: Commit
1. Edit SKILL.md — insert routing entry into the correct table section
2. If CP: add branch to Q1 decision tree
3. Update `references/skill-capabilities.md` with the new skill's capabilities
4. Also add the skill name to the Covered Skills Registry at the bottom of SKILL.md
5. Re-package: use skill-creator's `package_skill.py` at `C:\Documents\Openclaw\workspace\skills\skill-creator\scripts\package_skill.py`
6. Re-install: extract .skill to `~/.openclaw/skills/skill-dispatcher/`

## Step 6: Log
Record in dispatcher (as comment near the new entry):
```
<!-- Onboarded: [YYYY-MM-DD], reviewed 3 rounds, no false positives -->
```

## Example: Hypothetical new skill "pdf-editor"
```
Step 2 → Category: Dev/Tools (file manipulation)
Step 3 → | PDF/文档编辑/合并/旋转 | `pdf-editor` | ⭐ |
Step 4 → Round 1: "帮我旋转PDF" ✅ / "合并这两个PDF" ✅ / "提取PDF文字" ✅
          Round 2: "PDF是什么意思" → NOT a match (definition query, not editing) ✅
          Round 3: "帮我截图PDF" → Screenshot vs pdf-editor？→ disambiguate: "截图" prefers Screenshot ✅
Step 5 → Add to Dev/Tools table, update references, add to Registry
```
