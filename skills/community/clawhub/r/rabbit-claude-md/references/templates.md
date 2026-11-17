# Shapes: what a healthy CLAUDE.md looks like at each level

Slots, not wording. This file describes what each section holds and what it must not, and never supplies a sentence to paste: a literal phrase shipped here would open every user's memory file the same way, which is the shared-fingerprint failure the engine exists to catch. The user's own voice fills the slots.

There is no required format. These shapes are the ones that keep the file short and the facts findable.

## Root CLAUDE.md

The file every session loads. Small: a map plus rules. When it grows past the size band in `scripts/claude_check.py`, something below has claimed altitude it does not hold.

- **Title and one line of what this is.** Enough for a fresh session to orient. Not a pitch, not a feature list, not the README restated.
- **Commands.** A fenced block of the commands Claude cannot guess: build, test, lint, run, in copy-pasteable form, each with a short comment saying what it proves. Verified against the tree, because a dead command costs trust in the live ones.
- **Architecture pointers.** Where the parts that matter most live, as pointers rather than descriptions. A line naming the directory and its role beats a paragraph describing its contents, which the code states better.
- **Conventions.** Only the ones that differ from defaults: style choices, repository etiquette, branch and PR habits. Standard language conventions cost lines and change nothing.
- **Gotchas.** Non-obvious behavior that has caused a real mistake, one line each. Depth behind any of them goes to `.claude/docs/` with a link. A gotcha section that keeps growing is a changelog forming: prune it against the removal test.

Sections a project does not need are omitted, not stubbed. An empty heading is a line spent announcing nothing.

## Module or crate CLAUDE.md

Lives inside the directory it describes and loads when Claude works there. That placement is the whole point: facts here cost nothing in sessions that never touch the module.

- Only facts scoped to this directory. A rule that applies repo-wide belongs in the root, once.
- Never repeats the root. The reader has both in context when this one loads.
- Commands, if the module has its own (its test runner, its build), in the same verified fenced form as the root.
- The module's gotchas, at the same one-line standard.

## Monorepo root

- The root is the map: what packages exist, one line each, and the rules that cross package lines.
- One nested CLAUDE.md per package that needs one. A package with nothing non-obvious gets no file.
- `.claude/docs/` for anything deep enough to have a topic name.
- Cross-package workflow (build order, shared tooling) stays in the root, because no single package owns it.

## Serving two harnesses: CLAUDE.md and AGENTS.md

A repository worked by both Claude Code and an AGENTS.md-reading harness keeps one real file and symlinks the other name to it (`ln -s AGENTS.md CLAUDE.md`, or the reverse). Two real files with the same content drift the day one gets edited, and the duplicate check will say so. The checker states the symlink at the top of its report so a reader knows both names are one file.

## CLAUDE.local.md and .claude.local.md

Personal and gitignored: machine quirks, private paths, individual preferences. Anything a teammate would need belongs in the checked-in file instead. The audit reads local files when asked, and never proposes moving shared facts into one.

## Where open work lives, and where it does not

A memory file states standing rules, not what is left to do. Goals, roadmaps, and TODOs belong in one of three places, depending on who needs to see them and whether they are shared. `TODO.md` at the repository root holds shared, short-lived work items. The project's existing issue tracker takes over when one is already in use, so open work has one home rather than two. `CLAUDE.local.md` is for personal, machine-specific items only, never for anything a teammate needs to see.

`claude_check.py`'s `claudemd-todo-marker` and `claudemd-session-state` findings are the mechanical tell. Where exactly it goes is a question for the user, not a default the skill picks.

## Where an occasional workflow lives, and where it does not

A multi-step procedure that only comes up sometimes (a release checklist, a migration playbook, a rarely-run diagnostic) does not need to load every session to be useful. It belongs in a `.claude/commands/<name>.md` slash command, a `.claude/agents/<name>.md` subagent, or a plugin skill, whichever the harness already uses, with at most a one-line pointer left in the memory file. `claude_check.py`'s harness-inventory note lists which of these surfaces already exist in the tree, so the workflow lands beside the ones already there rather than starting a second convention.

## Files that receive moved content

Moved depth goes under `.claude/docs/`, named by topic (`.claude/docs/testing.md`, `.claude/docs/release.md`), never by date or by the session that created it. The repository's `docs/` belongs to the project's own documentation and stays out of this by default. Each moved file is linked from the file the content left, one line, so the map still shows where the depth lives. See `restructure.md` for the move mechanics.
