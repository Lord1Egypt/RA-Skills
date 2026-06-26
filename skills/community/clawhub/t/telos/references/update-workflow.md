# TELOS Update Workflow

## Update Command

Use the TypeScript update script for all changes:

```bash
bun <skill-dir>/scripts/update-telos.ts <file> "<content>" "<change-description>"
```

The script automatically:
1. Validates the filename against the allowed list
2. Creates a timestamped backup in `~/clawd/telos/backups/`
3. Appends content to the file (never overwrites)
4. Logs the change in `~/clawd/telos/updates.md`

## Per-File Format Rules

| File | Format |
|---|---|
| BOOKS.md | `- *Title* by Author — [one-line insight]` |
| LEARNED.md | `## Lesson\n\n[Description]\n\n*Date: YYYY-MM-DD · Source: [book/experience/conversation]*` |
| BELIEFS.md | `## B#: [Statement]\n\n**Evidence:** ...\n**Implications:** ...\n**Confidence:** High/Medium/Low` |
| GOALS.md | `## G#: [Title]\n\n**Supports:** M#\n**Target:** YYYY-MM-DD\n**Milestones:**\n- [ ] ...` |
| WISDOM.md | `> [Quote or principle]\n\n[Source / context]` |
| WRONG.md | `## [Period] — [What I Believed]\n\n**What happened:** ...\n**Lesson:** ...` |

## Examples

```bash
# Add a book
bun <skill-dir>/scripts/update-telos.ts BOOKS.md \
  "- *Thinking, Fast and Slow* by Daniel Kahneman — dual process theory" \
  "Added book: Thinking, Fast and Slow"

# Record a lesson
bun <skill-dir>/scripts/update-telos.ts LEARNED.md \
  "## Consistency Beats Intensity\n\nSmall daily actions compound. Sporadic bursts don't.\n\n*Date: 2026-03-20 · Source: experience*" \
  "Added lesson about consistency"

# Update beliefs
bun <skill-dir>/scripts/update-telos.ts BELIEFS.md \
  "## B5: Complex problems are coordination problems\n\n**Evidence:** Most failures I've seen stem from misalignment, not lack of skill\n**Implications:** Focus on communication and shared context\n**Confidence:** High" \
  "Added belief about coordination"
```

## Batch Interview Extraction

When the user says "extract from this conversation/interview into telos":
1. Identify all telos-relevant content (beliefs, lessons, books, goals, challenges)
2. Group by file type
3. Run update script once per file
4. Report summary: "Added 2 beliefs, 1 book, 3 lessons"
