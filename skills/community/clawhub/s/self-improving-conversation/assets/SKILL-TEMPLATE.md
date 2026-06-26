# Skill Template

Template for creating skills extracted from conversational learnings. Copy and customize.

---

## SKILL.md Template

```markdown
---
name: skill-name-here
description: "Concise description of the conversational pattern this skill addresses. Include trigger conditions."
---

# Skill Name

Brief introduction explaining the dialogue problem this skill solves and its origin.

## Quick Reference

| Conversation Signal | Action |
|---------------------|--------|
| [Trigger phrase or pattern] | [Conversational response strategy] |
| [Trigger phrase or pattern] | [Conversational response strategy] |

## Background

Why this conversational knowledge matters. What dialogue failures it prevents.
Context from the original learning.

## Solution

### Dialogue Strategy

1. Detect the conversation signal (user tone, intent, frustration level)
2. Apply the response adjustment (tone shift, escalation, clarification)
3. Verify the outcome (user sentiment, conversation continuity)

### Example Exchange

\`\`\`
User: [example input showing the trigger]
Agent (before fix): [problematic response]
Agent (after fix): [improved response]
\`\`\`

## Common Variations

- **Channel A (web)**: Description and how to handle
- **Channel B (slack)**: Description and how to handle

## Gotchas

- Warning or common mistake in conversation handling #1
- Warning or common mistake in conversation handling #2

## Related

- Link to related dialogue documentation
- Link to related conversational skill

## Source

Extracted from conversational learning entry.
- **Learning ID**: LRN-YYYYMMDD-XXX
- **Original Category**: tone_mismatch | misunderstanding | escalation_failure | context_loss | sentiment_drift | hallucination
- **Extraction Date**: YYYY-MM-DD
```

---

## Minimal Template

For simple conversational skills:

```markdown
---
name: skill-name-here
description: "What conversational pattern this skill addresses and when to use it."
---

# Skill Name

[Dialogue problem statement in one sentence]

## Solution

[Direct conversational strategy with example exchange]

## Source

- Learning ID: LRN-YYYYMMDD-XXX
```

---

## Template with Scripts

For skills that include dialogue analysis helpers:

```markdown
---
name: skill-name-here
description: "What conversational pattern this skill addresses and when to use it."
---

# Skill Name

[Introduction]

## Quick Reference

| Command | Purpose |
|---------|---------|
| `./scripts/analyze-sentiment.sh` | [What it does] |
| `./scripts/validate-intents.sh` | [What it does] |

## Usage

### Automated (Recommended)

\`\`\`bash
./skills/skill-name/scripts/analyze-sentiment.sh [args]
\`\`\`

### Manual Steps

1. Review conversation transcript
2. Identify pattern match
3. Apply response strategy

## Scripts

| Script | Description |
|--------|-------------|
| `scripts/analyze-sentiment.sh` | Sentiment analysis utility |
| `scripts/validate-intents.sh` | Intent taxonomy validator |

## Source

- Learning ID: LRN-YYYYMMDD-XXX
```

---

## Naming Conventions

- **Skill name**: lowercase, hyphens for spaces
  - Good: `tone-adaptation`, `escalation-protocol`, `context-recovery`
  - Bad: `Tone_Adaptation`, `EscalationProtocol`

- **Description**: Start with action verb, mention conversation trigger
  - Good: "Adapts agent tone to match user formality level. Use when tone mismatch is detected."
  - Bad: "Conversation stuff"

- **Files**:
  - `SKILL.md` - Required, main documentation
  - `scripts/` - Optional, analysis code
  - `references/` - Optional, detailed docs
  - `assets/` - Optional, templates

---

## Extraction Checklist

Before creating a skill from a conversational learning:

- [ ] Dialogue pattern is verified across multiple conversations
- [ ] Solution is broadly applicable (not one user's preference)
- [ ] Content is complete (has needed conversation context)
- [ ] Name follows conventions
- [ ] Description is concise but informative
- [ ] Quick Reference table uses conversation signals
- [ ] Example exchanges are anonymized
- [ ] Source learning ID is recorded

After creating:

- [ ] Update original learning with `promoted_to_skill` status
- [ ] Add `Skill-Path: skills/skill-name` to learning metadata
- [ ] Test skill by reading it in a fresh session
