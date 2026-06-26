# Quality Criteria

Score CLAUDE.md files on a 100-point scale across 6 criteria. Use this when running a full audit (Mode 2) or restructure (Mode 3).

## Scoring Rubric

### Commands/Workflows (20 points)

Build, test, deploy, and dev commands documented with context.

| Score | Meaning |
|-------|---------|
| 20 | All essential commands with context (when to use, flags) |
| 15 | Most commands documented, some missing context |
| 10 | Basic commands only (e.g. `npm run dev`) |
| 5 | Few commands, no context |
| 0 | None documented |

### Architecture Clarity (20 points)

Directory structure, module relationships, entry points, data flow.

| Score | Meaning |
|-------|---------|
| 20 | Clear codebase map with relationships and entry points |
| 15 | Good overview, minor gaps |
| 10 | Basic directory listing only |
| 5 | Vague or incomplete |
| 0 | None |

### Non-Obvious Patterns (15 points)

Gotchas, quirks, edge cases, workarounds, "why" for unusual decisions.

| Score | Meaning |
|-------|---------|
| 15 | Gotchas and quirks captured with explanations |
| 10 | Some patterns documented |
| 5 | Minimal |
| 0 | None |

### Conciseness (15 points)

Dense, valuable content. No filler, no redundancy, each line earns its place.

| Score | Meaning |
|-------|---------|
| 15 | Every line adds value, no filler |
| 10 | Mostly concise, minor bloat |
| 5 | Verbose in places |
| 0 | Mostly filler or generic advice |

### Currency (15 points)

Reflects the actual current codebase. Commands work, files exist, stack is correct.

| Score | Meaning |
|-------|---------|
| 15 | All references valid, commands work, stack current |
| 10 | Mostly current, minor staleness |
| 5 | Several outdated references |
| 0 | Severely outdated |

### Actionability (15 points)

Instructions are executable. Copy-paste ready commands, real paths, concrete steps.

| Score | Meaning |
|-------|---------|
| 15 | Copy-paste ready, concrete, real paths |
| 10 | Mostly actionable |
| 5 | Some vague instructions |
| 0 | Theoretical or generic |

## Grading Scale

| Grade | Score | Meaning |
|-------|-------|---------|
| A | 90-100 | Comprehensive, current, actionable |
| B | 70-89 | Good coverage, minor gaps |
| C | 50-69 | Basic info, missing key sections |
| D | 30-49 | Sparse or outdated |
| F | 0-29 | Missing or severely outdated |

## Red Flags

Flag these during audit — each indicates a quality problem:

- Commands that fail when run
- References to files/directories that don't exist
- Outdated technology versions or deprecated APIs
- Generic advice not specific to the project (e.g. "write clean code")
- Copy-paste templates that weren't customised
- "TODO" items that were never completed
- Duplicated content across multiple CLAUDE.md files
- Verbose explanations of things Claude already knows
- Changelogs or version history (belongs in git, not CLAUDE.md)
