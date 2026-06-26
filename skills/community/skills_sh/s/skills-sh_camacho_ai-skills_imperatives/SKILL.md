---
name: imperatives
description: "Use when extracting imperatives from agent instruction files, analyzing rule coverage, or preparing input for /policy-algebra and /distill."
---

# /imperatives

Extract atomic imperatives (MUST/SHOULD/MAY) from markdown instruction files into JSONL.

## Usage

```
/imperatives                                # default: ai-workspace/rules/*.md + AGENTS.md
/imperatives .claude/rules/*.md             # specific globs
/imperatives --output imperatives.jsonl     # write to file
```

## Steps

1. **Resolve files.** Default: `ai-workspace/rules/*.md` and `AGENTS.md`. Expand globs to absolute paths. Zero matches → error, stop.

2. **Pass 1 — Script extraction (fast, deterministic).**
   ```bash
   node --import tsx "${SKILL_DIR}/scripts/extract-imperatives.ts" <files...> --output /tmp/imperatives-pass1.jsonl
   ```
   `${SKILL_DIR}` = this skill's base directory (shown in the "Base directory for this skill:" header above). Keyword-based: catches RFC 2119 terms + imperative verbs. ~80% coverage, <1s.

3. **Pass 2 — Subagent reasoning (catches implicit imperatives).**
   For each file, dispatch a subagent to identify imperatives the regex missed — contextual rules, implicit constraints, prose-embedded obligations.

   Subagent prompt:
   > Read `<file>`. Here are the imperatives already extracted by the script for this file:
   > ```
   > <pass 1 JSONL lines where source.file matches>
   > ```
   > Identify additional imperative statements the regex missed. Look for:
   > - Implicit obligations hidden in prose (e.g., "The workflow is a menu, not a pipeline" implies MUST NOT enforce order)
   > - Contextual constraints (e.g., section context that makes a statement imperative)
   > - Conditional rules not triggered by keyword patterns
   >
   > For each new imperative found, output one JSON line (same schema — id, level, polarity, subject, predicate, when, source, tool_scope, tags, raw).
   > Do NOT duplicate entries already in pass 1. If none found, output nothing.

   Use `subagent_type: "explorer"` (Haiku) for most files. If a file had zero pass-1 imperatives OR contains dense prose (>50 lines without a keyword match), escalate that file to Sonnet for deeper reasoning.

4. **Merge passes.** Concatenate pass 1 + pass 2 outputs. Deduplicate by `raw` text. Write final output to `--output <path>` or present inline.

5. **Present summary.** Report in a table:
   - Total count (pass 1 baseline + pass 2 additions)
   - Breakdown by `level` and `tool_scope`
   - Files with zero imperatives after both passes
   - Pass 2 additions highlighted separately

6. **Downstream callers.** If invoked by `/policy-algebra` or `/distill`, return the JSONL path directly — skip the summary.

## Failure modes

| Condition | Behavior |
|---|---|
| No files matched | Error message. Stop. |
| File not found | Script warns on stderr, continues with remaining files. |
| Zero imperatives | Report zero. Not an error. |
| Script exits non-zero | Surface stderr to user. |

## Cross-tool notes

- **Codex / Cursor**: run the script directly — it's tool-agnostic.
