# working-memory

A long session with Claude runs out of context and gets **compacted** — the transcript is squeezed into a summary. The details go with it: what you decided, the edge-cases, the three approaches you already ruled out. Claude keeps working on the thinned-out version, quality slips, and the next session opens blind — *didn't we already do this?*

**working-memory** fixes that by giving each project a `WORKING.md` in the repo — a small, living file that holds the current stage's state (decision log, dead ends, next steps). It survives compaction and new sessions, and at the end of a stage its settled conclusions get distilled up into long-term memory. Your context stops being the only copy.

*A [Claude Code skill](https://code.claude.com/docs/en/skills). Everything is local: one Markdown file in your repo, plus (optionally) a pointer in your `CLAUDE.md`.*

## The idea: three levels of memory, like a brain

| Level | Medium | Lifespan |
|---|---|---|
| **Short-term** | session context | hours — dies on compaction |
| **Mid-term** | `WORKING.md` in the repo | days–weeks — while a stage runs |
| **Long-term** | the assistant's memory | months — survives everything |

The flow runs one way: **context → WORKING.md → (distill at stage end) → long-term memory.** WORKING.md is a *staging area*, not a parallel store — operational state lives there and dies with the stage; only settled conclusions rise to long-term memory.

The rule that keeps the two apart is one question — the **belonging test**: *"When this stage ends and WORKING.md is reset, should this line survive?"* Yes → it's a durable conclusion, promote it. No → it's progress, leave it to expire.

## What this skill does

- **Setup** — drops a `WORKING.md` at your repo root and (optionally) a pointer into your `CLAUDE.md` so it's read every session.
- **Resume** — Claude reads WORKING.md at the start of a session and picks up exactly where the last one left off, even across a compaction.
- **Checkpoint** — after a meaningful step, or right before you `/compact`, Claude appends the decision, the reason, and what's next. This is the core habit; it's written *during* the work, not saved up for the end.
- **Consolidate** — when a stage closes, Claude distills the keepers into long-term memory and resets WORKING.md for the next stage.

## Install

Via plugin marketplace (recommended):

```
/plugin marketplace add ikotelkin/claude-skills
/plugin install working-memory@ikotelkin-skills
```

Or manually:

```bash
git clone https://github.com/ikotelkin/claude-skills.git
cp -r claude-skills/skills/working-memory ~/.claude/skills/
```

Then, in a Claude Code session: *"Set up working memory for this project."* From then on, *"checkpoint"* saves state, and *"consolidate — this stage is done"* promotes the keepers and clears the slate.

## Pairs well with dialog-tree

[dialog-tree](../dialog-tree/) maps the branches of one live conversation; **working-memory** carries a project's state across many sessions. One is the map of *this discussion*, the other is the memory of *the work*.

## Files

```
working-memory/
  SKILL.md                    ← instructions Claude follows
  README.md                   ← this file
  assets/
    WORKING.template.md        ← the file Claude copies into your repo
    CLAUDE-snippet.md          ← pointer to paste into your CLAUDE.md
```
