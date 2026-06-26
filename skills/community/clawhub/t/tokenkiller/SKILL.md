---
name: tokenkiller
description: Reduces token usage across multi-skill agent workflows (search, coding, debugging, testing, docs) using budgets, gating, progressive disclosure, and deduped evidence. Use when the user mentions saving tokens, cost, context length, long logs, large codebases, or when tasks involve multi-step exploration or debugging.
---

# TokenKiller (Universal Throttling)

## Goal

Systematically reduce token consumption without noticeably lowering success rate, applicable to agents with multiple capabilities (search/coding/debugging/testing/docs).

## Task Complexity Assessment

Before setting budgets, assess task complexity:

| Complexity | Criteria | Tool Budget | Output Budget |
|------------|----------|-------------|---------------|
| Simple | Single file modification, single-point localization, clear requirements | ≤3 calls | ≤50 lines |
| Medium | Across 2-3 files, needs simple exploration, relatively clear requirements | ≤6 calls | ≤120 lines |
| Complex | Cross-module refactoring, multi-step debugging, unclear requirements | ≤10 calls | ≤200 lines |

**Extension Mechanism (Soft Warning)**: When budget is about to run out but task is incomplete:
1. Output warning: `[TokenKiller] Budget running low, current progress X/Y, remaining work: ...`
2. Continue execution, but switch to more conservative strategy
3. User can interrupt or request more detailed output at any time

## Default Working Mode (Balanced)

### Global Hard Rules (Must Follow)

- **Goal First, Evidence Later**: State the goal in one sentence (L0) first, then decide if evidence is needed (L2/L3).
- **Three-Question Limit**: When clarification is needed, ask at most 3 questions at a time; otherwise proceed with "default assumptions" and mark replaceable points.
- **Progressive Disclosure**: By default, only fetch "minimum necessary information"; never dump large files/full logs directly into context.
- **Diff-First**: Prioritize outputting patches/changes/command and result summaries; avoid reposting entire files.
- **Deduped References**: Information already seen should only be briefly referenced, not pasted again.

### Budget Gate (Budget + Gate)

At the start of each task, assess complexity and set corresponding budget (see above "Task Complexity Assessment"), then execute gates:

- **Tool Call Budget**: Set by complexity (Simple ≤3, Medium ≤6, Complex ≤10).
- **Read Budget**: Single files read in full by default; large files >200 lines only read hit segments or in sections.
- **Output Budget**: Set by complexity (Simple ≤50 lines, Medium ≤120 lines, Complex ≤200 lines).

If any gate is exceeded:

- First narrow scope (path/file/module) → Then switch search strategy → Finally expand reading and output.

## Token Consumption Self-Check

### High-Consumption Behaviors (Avoid)

- Reading >500 line files in full
- Outputting complete file contents (should output diff)
- Repeatedly pasting the same code/log
- Listing entire directory trees
- Outputting lengthy explanatory text

### Self-Check Timing

After every 3 tool calls, quickly self-check:

- Am I currently at L0-L2 level?
- Is there duplicate information?
- Is output exceeding necessary length?

## Information Layers (L0-L3)

- **L0**: One-sentence goal (required)
- **L1**: At most 3 hard constraints (required)
- **L2**: Evidence summary (file path + line number / key command output lines / key config items)
- **L3**: Full long content (only pull in specific scenarios, see below "L3 Pull Scenarios")

Default output and context stay at L0-L2.

### L3 Pull Scenarios (Explicit)

Only pull L3 (full content) in these scenarios:

1. **Code Modification**: When exact indentation/format matching is needed, read target function's complete code
2. **Config Debugging**: When config items are interdependent, need to see complete config block
3. **Error Analysis**: When error message is incomplete, need complete stack trace or context
4. **User Explicit Request**: User requests to see full content

**Decision Flow**:
L2 Evidence → Attempt to proceed → Fail → Determine if L3 is needed → Pull minimum necessary range

## Multi-Skill Collaboration

When this Skill is activated alongside other Skills:

### Priority Rules

- **Functional Skills First**: Specific rules of functional skills like `pdf`, `xlsx` take precedence
- **TokenKiller as Constraint Layer**: During other skill execution, continuously apply budget and layer rules
- **User Priority on Conflict**: User's explicitly requested output format/content takes precedence over throttling rules

### Collaboration Mode

```
[User Request] → [Functional Skill Processing] → [TokenKiller Constrains Output]
```

## Workflow (General)

### 1) Task Entry (Any Domain)

1. Produce L0 + L1 (quickly infer if user didn't provide)
2. Choose strategy (search/direct modification/verify first)
3. Execute minimal action
4. Immediately verify (cheapest verification first)
5. Summarize: only key conclusion + 1 next step

### 2) Search/Exploration (Priority Domain)

Priority:

1. **Filename/Path** (Glob)
2. **Exact String** (Grep)
3. **Semantic Search** (SemanticSearch)
4. **Read File** (Read, by sections/line ranges)

Rules:

- Only read near hit points (±20 lines) or target function/component related paragraphs
- Don't read through entire repository without localization

### 3) Coding/Refactoring

Rules:

- Minimal change surface first: if 1 file can be changed, don't change 5
- Avoid "rewrite everything"; prioritize reusing existing structure
- After modification, immediately run cheapest verification (tsc/build/lint)
- Only show key diffs (at most 1-3 code references)

### 4) Debugging/Troubleshooting

Rules:

- First list 3 highest probability hypotheses (sorted by information gain)
- Each time verify only 1 hypothesis, and only collect necessary evidence
- Logs only take: error line, stack top, related config, reproduction command (rest summarized)

### 5) Testing/Verification

Priority (from cheap to expensive):

1. lint / typecheck
2. build
3. unit test
4. e2e / browser automation

When failed, only append "diff information", don't repost full output.

### 6) Docs/Summary

Rules:

- Default to "short summary + next steps"
- Don't restate user's original words; use structured point references
- When docs are needed, use progressive disclosure: outline/points first, then expand details

## Output Template (Default)

Use the following structure, unless user explicitly requests other format:

- **Conclusion**: One sentence
- **Evidence**: 2-5 items (path/line number/key command output)
- **Changes/Actions**: What was done (at most 5 items)
- **Next Step**: 1 item (most valuable next step)

## Trigger Words (Recommended Auto-Enable)

Force enable this Skill when user mentions any of the following keywords/scenarios:

- "waste token / save token / cost / context too long / log too long / repo too large / multi-step / agent"