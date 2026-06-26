# PMA Docs And Tracking

## Canonical Structure

```text
docs/
├── task/
│   ├── index.md
│   └── PREFIX-NNN.md
├── plan/
│   ├── index.md
│   └── PLAN-NNN.md
├── architecture.md
└── changelog.md
```

## Required Files

- `docs/task/index.md`: one-line task entries
- `docs/task/PREFIX-NNN.md`: task detail files
- `docs/plan/index.md`: one-line plan entries
- `docs/plan/PLAN-NNN.md`: plan detail files
- `docs/architecture.md`
- `docs/changelog.md`

Use these format references:

- [task-format.md](../docs/task-format.md)
- [plan-format.md](../docs/plan-format.md)

## Documentation Rules

- Use English for repository docs and headings by default.
- Use Chinese docs only when the user explicitly requests a specific document in Chinese.
- Keep filenames in English even when content is Chinese.
- Write investigation findings into the relevant plan context section.
- Do not create extra report files; temporary files belong in `./tmp/`.

## Changelog Conventions

Entry format:

```markdown
## YYYY-MM-DD HH:MM [tag]

[content]
```

Recommended tags:

- `[progress]`
- `[BUG-P0]`
- `[BUG-P1]`
- `[pitfall]`
- `[decision]`

## Project Initialization

The project's `AGENTS.md` (with `CLAUDE.md` symlinked to it) only carries **project-personalized** facts — which stack skills apply, language/runtime choice, quality-gate command, link to local divergences. Skill rules are not duplicated into the project file; they are loaded from `/pma` and the stack skills on demand.

See [project-injection.md](../docs/project-injection.md) for the canonical template, the anti-patterns to avoid, and the full initialization checklist.

Minimum on first use in a project:

1. Create `AGENTS.md` with the *Project Development* template from [project-injection.md](../docs/project-injection.md), then `ln -s AGENTS.md CLAUDE.md` so the two cannot drift.
2. Initialize `docs/task/index.md` and `docs/plan/index.md` per the canonical formats.
3. Initialize `docs/architecture.md` and `docs/changelog.md` in English unless the user explicitly requests Chinese.
4. Apply *Repository Hygiene* (`/pma references/delivery.md`) — `.gitignore`, `.gitattributes`, `.editorconfig`, `LICENSE`, `README.md`, `.env.example`, plus the stack-pinned toolchain file.
