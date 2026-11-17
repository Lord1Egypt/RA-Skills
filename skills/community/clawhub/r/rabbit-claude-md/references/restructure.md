# Restructure: moving content out of a CLAUDE.md

The playbook for the four moving dispositions: `move-to-docs`, `move-to-module`, `move-to-skill`, `move-to-todo`. Everything here happens after the audit report and after the user approves the plan, never before.

## Choose the target

- **Depth with a topic name** goes to `.claude/docs/<topic>.md`. Name by topic, never by date or session. The repository's own `docs/` is the project's documentation, written for its users, and agent context filed there litters it: `.claude/docs/` keeps the two audiences apart. Use the repo's `docs/` only when the content genuinely is project documentation, or when the user says that is where they keep this kind of context.
- **A fact scoped to one directory** goes to a CLAUDE.md inside that directory. Create the file if the module has none, and give it only what belongs to it (see `templates.md`).
- **A multi-step workflow relevant only sometimes** goes to `.claude/commands/<name>.md`, `.claude/agents/<name>.md`, or a plugin skill, whichever convention the harness-inventory note shows already in use. Ask before starting a second convention the repository does not already have.
- **Open work, a goal, or a roadmap item** goes to `TODO.md`, the project's existing issue tracker, or `CLAUDE.local.md` when it is personal and machine-specific. Ask which the user wants. Do not default to creating `TODO.md` in a repo that already tracks issues elsewhere.
- When several root gotchas share a topic, they move together into one docs file rather than one file each. A docs folder of six-line fragments is the bloat problem relocated.
- **Check `.gitignore` before the first move to `.claude/docs/`.** The checker's `claudemd-docs-ignored` finding covers the common spellings, and the playbook check is `git check-ignore .claude/docs` from the repo root. When `.claude` is ignored, tell the user plainly: anyone cloning the repository never receives the moved files, so on a shared repo the links are dead for everyone else. Offer the fix (track `.claude/docs/`, a negation line works) before moving anything, and if the docs stay untracked on purpose, say the restructure only serves this one machine. Moved files also have to be added to git: an unignored `.claude/docs/` that nobody commits is the same dead link one push later.

## Move mechanics

1. **Move whole, then tighten in place.** Copy the content to the target first, verify nothing was dropped, then tighten the copy at the target. Tightening during the move is how facts silently disappear.
2. **Delete the source copy in the same change.** One home per fact. A move that leaves the original behind is a duplication, and the two copies start drifting immediately.
3. **Leave a one-line pointer** in the file the content left: what moved and a plain markdown link to where. The root file stays a map, and a map shows where the depth lives.
4. **Link, do not import, by default.** An `@path` import loads the target into every session, which re-spends the context the move just saved. Import only content that genuinely must always be loaded, and say why in the report when you do.
5. **Never move a safety-critical rule out of an always-loaded file.** A rule that prevents a destructive action protects nothing from inside a file nobody opened. If it matters every session, it stays in the root, tightened rather than moved.
6. **Preserve attribution and truth.** Moving is not rewriting: a claim stays a claim, a number stays its number. Rewording happens under the tighten disposition, where the diff shows it.
7. **A move-to-skill target keeps its own frontmatter and structure**, whatever the destination convention expects (a slash command's argument-hint, a subagent's tool list, a skill's SKILL.md shape). Do not paste memory-file prose into a command file unedited. It was written to be loaded silently, not read by a slash-command invocation.
8. **A move-to-todo target is a checklist, not a memory file.** Strip the memory-file framing (no "the model should always...") and state the item as a task with an owner or a date if the source had one.

## Merging a dual-harness pair

`claudemd-dual-harness` is not a content move: it means a `CLAUDE.md` and an `AGENTS.md` in one directory should be one file, not two. Pick whichever name carries the more complete or more recently maintained content as the real file (ask if it is unclear), fold in anything the other file has that the chosen one lacks, delete the other, and symlink it back: `ln -s CLAUDE.md AGENTS.md`, or the reverse. Re-run the checker afterward. It should report the pair as one file with the symlink note, and `claudemd-dual-harness` should not fire again.

## Verify after moving

- Re-run `scripts/claude_check.py` on every CLAUDE.md touched. The moved content should no longer fire where it was, and the target module file should come back clean.
- Run every file that received moved content through the engine at register `docs`, the same scan the checker applies. Moved prose meets the same bar it was held to before the move.
- Confirm every fenced command still resolves from its new file's directory. A command that worked from the root can name a path that no longer resolves relative to a module file.
- Report the move map: each source line range, its target, and before-and-after non-blank line counts for every touched CLAUDE.md.
