# Incremental Merge Prompt

## Task

You will receive:
1. Existing `work.md` content
2. Existing `persona.md` content
3. New source material (files or messages)

Your task is to determine which parts the new content should update and output incremental changes.

**Principle: Only append incremental content — never overwrite existing conclusions. If there's a conflict, output a conflict alert for the user to decide.**

---

## Step 1: Classify

Categorize each piece of new information:

| Information Type | Destination |
|-----------------|-------------|
| Technical standards, code style, API design, workflow | → work.md |
| Domain knowledge, system responsibilities, technical conclusions | → work.md |
| Communication style, catchphrases, expression habits | → persona.md |
| Decision behavior, interpersonal patterns, emotional patterns | → persona.md |
| Both applicable | → Split into both |

---

## Step 2: Check for Conflicts

Compare new content against existing content:

- If new content **supplements** existing info (adds new details) → append directly
- If new content **confirms** existing info → skip (don't duplicate)
- If new content **contradicts** existing info → output conflict alert:

```
⚠️ Conflict detected:
- Existing: {existing description}
- New finding: {new content description}
- Source: {filename / timestamp}

Recommendation: [keep existing / update to new / keep both with timestamps]
User decision required.
```

---

## Step 3: Generate Update Patch

For `work.md` updates:
```
=== work.md updates ===

[Append to "Technical Standards / Naming Conventions" section]
- {new content}

[Append to "Experience & Knowledge Base" section]
- {new knowledge conclusion}

[No updates] or [Sections above updated]
```

For `persona.md` updates:
```
=== persona.md updates ===

[Append to "Layer 2 / Catchphrases & Vocabulary" section]
- New catchphrase: "{xxx}"

[Append to "Layer 4 / With Peers" section]
- {new behavior description}

[No updates] or [Sections above updated]
```

---

## Step 4: Generate Update Summary

Display to user:
```
📦 Update applied (v{N} → v{N+1}):
  work.md:    +{N} items (naming conventions, new API patterns)
  persona.md: +{N} items (3 catchphrases, Slack emoji usage)
  ⚠️ {N} conflicts need your input (see above)
```

Auto-apply if there are zero conflicts. Only ask for confirmation when conflicts exist.
