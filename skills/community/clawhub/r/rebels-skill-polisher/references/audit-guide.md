# Audit Guide

Compare the original SKILL.md against the polished version. Flag anything that could hurt LLM effectiveness.

---

## Audit Checklist

Run through these checks after every polish. Flag anything that fails.

### Description (frontmatter)

- [ ] Trigger phrases preserved or improved
- [ ] No trigger phrases removed
- [ ] Still under 1024 characters
- [ ] Credentials still mentioned (if required)
- [ ] Uses imperative phrasing

### Security

- [ ] Security notes preserved (moved to references/ is OK, deleted is NOT)
- [ ] Credential instructions still accessible
- [ ] Token storage location still mentioned
- [ ] No permissions broadened or narrowed without noting it

### Protected Content

Check that none of the following were moved to references/. They must stay inline.

- [ ] Anti-hallucination / data integrity rules still present
- [ ] Safety constraints ("does NOT do", "what NOT to do") still present
- [ ] Confirmation requirements still present
- [ ] Interactive behavior rules still present
- [ ] Display format contracts still present
- [ ] Cross-skill data contracts still present (bundle mode)
- [ ] Post-flow output still present (end-of-turn sections, email draft offers, optional next-step prompts)
- [ ] Root routing logic still present (bundle mode — routing table, dispatch rules, infrastructure overview)

**Why this matters:** The LLM may skip reference files to save tokens. If these rules are in references/, the agent will hallucinate data, skip confirmations, or produce broken output. See rules.md for the full protected content table.

### LLM Execution

- [ ] Exact commands still provided (file paths, flags, arguments)
- [ ] Config file locations still mentioned
- [ ] Dependencies still listed
- [ ] Setup steps still complete (not shortened to the point of being unusable)
- [ ] Error handling guidance preserved (or moved to references/)

### Agent Behavior & Output

Scan for instructions that govern *how* the agent behaves or what the user experiences — not just *what* the agent does. These are non-functional instructions and they are easy to lose during polish because they don't look like commands, configs, or security notes.

Check for these categories:

- [ ] **Output control** — instructions about when to stay silent vs when to produce output, what to include or omit from the user-facing response
- [ ] **Output formatting** — specific formatting rules (symbols, structure, length limits, template requirements)
- [ ] **Agent judgment** — guidance on when the agent should make a decision independently, when to escalate to the user, and how to handle uncertainty
- [ ] **Behavioral contract** — instructions about the agent's posture or role during execution (e.g. "checkpoint not controller", "never replace testing")
- [ ] **User experience** — anything describing what the user sees, hears, or experiences (e.g. "the user never sees this step", "present findings in plain text")
- [ ] **Error behavior** — how errors should be presented, handled, or recovered from in user-facing terms
- [ ] **Interactive behavior** — when to ask for permission, when to proceed automatically, when to confirm before acting

**How to check:** Compare the original against the polished version. For each category above, identify whether the original contained instructions in that category. If it did, verify the polished version preserves the substance of those instructions — either in the SKILL.md or moved to a references/ file.

**Skip this section entirely if the original SKILL.md contains no behavioral or output instructions.** Not every skill has them. This check only applies when the original has content that falls into these categories.

### Content Accounting

- [ ] Nothing deleted without a reference/ home
- [ ] Every reference/ file created is non-empty and useful
- [ ] Every reference/ file is linked from SKILL.md
- [ ] No broken references (file mentioned but doesn't exist)
- [ ] No duplicate content (same info in SKILL.md AND references/)

### Formatting

- [ ] No dense paragraphs (max 2 lines)
- [ ] Lists use code blocks where appropriate
- [ ] Tables have 3 columns max, short cells
- [ ] Sections have clear headings
- [ ] Output example included (if skill produces user-facing text)

---

## Bundle-Specific Audit

Run these additional checks in bundle mode. See [bundle-rules.md](bundle-rules.md) for the full bundle workflow.

### Regression Check (after each sub-skill)

After polishing each sub-skill, verify the data contracts still hold:

- [ ] Every field name mentioned in the polished skill still exists in the dependency map
- [ ] Every path reference (file paths, directory paths) still resolves correctly
- [ ] Every cross-skill reference (field names, report sections, shared variables) has been updated if the source was moved
- [ ] No reference to moved content without a valid inline pointer or updated path
- [ ] Any cross-skill reference update in already-polished skills has been applied correctly

### Cross-Validation (after all sub-skills)

After polishing all sub-skills, do a final verification:

- [ ] Rebuild the dependency map from all polished files — compare against the original map
- [ ] Every original dependency still resolves (field names, paths, sections)
- [ ] No circular or broken references between skills
- [ ] All "pending fixes" have been applied to their respective skills
- [ ] Bundle boilerplate is consistent across all sub-skills (identical content is word-for-word the same)

### Stale Reference Cleanup

- [ ] All §X.Y references to non-existent files have been removed
- [ ] All references to internal design docs (architecture.md, storage.md, <skill>.md) have been removed
- [ ] No orphaned section references remain

---

## Audit Report Format

Present the audit as:

```
📊 Audit Report

✅ Safe changes:
• Commands table → code block (formatting only)
• Credential section compressed (content preserved)

📦 Content moved to references/:
• Platform formatting → references/formatting.md
• Setup tutorial → references/setup.md

🔒 Protected content (kept inline):
• Anti-hallucination rules — reformatted, not moved
• "What NOT to do" section — reformatted, not moved

🔗 Cross-skill updates (bundle mode):
• Updated report template reference in proposal-builder (was moved to lead-qualifier/references/)
• Queued fix for project-onboarder: update qualification_report_path reference

⚠ Flagged:
• Security note about plaintext storage was removed → MOVED TO REFERENCES/NOTES.MD
```

Be specific. Name exactly what was moved and where. Don't say "some notes were moved" — say "the API rate limit note was moved to references/notes.md."

For bundles, include the cross-skill updates and pending fixes sections.

---

## What to Flag vs What's Safe

**Safe to change:**
- Dense paragraphs → short paragraphs
- Bullet lists → code blocks
- Markdown tables → code blocks
- Long setup steps → compressed code block
- Repeated info → consolidated
- Protected content → reformatted (but not moved)

**Flag as potentially risky:**
- Any security note removal
- Any setup instruction removal (auth, tokens, API config)
- Any command path change
- Any dependency removal
- Any trigger phrase removal
- Any protected content moved to references/
- Any cross-skill data contract broken
- Content removed without a reference/ destination
