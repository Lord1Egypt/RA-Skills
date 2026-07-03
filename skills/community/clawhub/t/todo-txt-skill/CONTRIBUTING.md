# Contributing to the todo.txt Skill

Thanks for your interest in improving this skill! It's a small project, so the process is lightweight.

## Ways to contribute

- **Report bugs** — if the agent picks the wrong command, misreads the todo.txt format, or the install steps fail, open an issue.
- **Improve the instructions** — the entire skill lives in [`SKILL.md`](./SKILL.md). Clearer guidance, better examples, or coverage of more `todo.sh` features are all welcome.
- **Improve the docs** — fixes to the README or this guide.

## Project layout

```
.
├── SKILL.md                          # The skill itself: frontmatter + instructions for the agent
├── scripts/
│   └── install_todo_cli.sh           # Bundled installer the agent falls back to when todo.sh is missing
├── README.md                         # User-facing documentation
├── CONTRIBUTING.md
├── CHANGELOG.md
└── LICENSE
```

There is no build step. `scripts/install_todo_cli.sh` is the only piece of executable code, and `SKILL.md` is what the agent reads to know when to call it. If you change one, check whether the other (and the manual fallback steps in `SKILL.md`) need to stay in sync.

## Editing the skill

`SKILL.md` has two parts:

1. **YAML frontmatter** — `name`, `description`, and `argument-hint`. The `description` is what the agent uses to decide when to trigger the skill, so keep it accurate and specific.
2. **The body** — instructions, a command reference, format rules, and behavior guidelines.

When adding a new `todo.sh` capability, please:

- Verify the command and flags against the [official todo.txt CLI](https://github.com/todotxt/todo.txt-cli) (`todo.sh help`).
- Add it to the relevant section of the command reference with a short comment.
- Keep examples consistent with the existing style.

## Testing your changes

1. Install the todo.txt CLI (`todo.sh -V` should work).
2. Point Claude at your edited skill (clone or symlink the repo into `~/.claude/skills/todo.txt-skill`).
3. Start a fresh Claude Code session and try prompts that exercise your change, e.g.:
   - "add buy milk +groceries"
   - "list everything in +work"
   - "mark task 2 as done"
4. Confirm the agent runs the expected command and re-lists tasks afterward.

> Tip: test against a throwaway `todo.txt` (set `TODO_DIR` or use a temporary `~/.todo.cfg`) so you don't disturb your real list.

## Submitting changes

1. Fork the repo and create a branch: `git checkout -b my-improvement`.
2. Make your change and update [`CHANGELOG.md`](./CHANGELOG.md) under the "Unreleased" section.
3. Open a pull request describing what changed and why, including an example prompt that now works better.

## Code of conduct

Be respectful and constructive. We follow the spirit of the [Contributor Covenant](https://www.contributor-covenant.org/).
