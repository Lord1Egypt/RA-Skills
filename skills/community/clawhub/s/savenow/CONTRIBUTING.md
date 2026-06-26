# Contributing to savenow

Thanks for thinking about contributing. This is a small focused skill, so I want to keep the bar simple: be helpful, be kind, keep it dependency-free.

## Quick start

```bash
git clone https://github.com/Chelebii/savenow
cd savenow
node tests/run.mjs        # all 12 tests should pass
```

That's it. No `npm install`, no build step, no toolchain — the project is intentionally zero-dependency. If you can run Node, you can hack on it.

## What kinds of contributions are welcome

**Yes, please:**
- Bug fixes with a regression test in `tests/run.mjs`
- New test cases for edge cases I missed
- Documentation improvements (README, SKILL.md, CHANGELOG)
- Translations of error messages / README
- Performance improvements with measurements
- Better semantic-dedupe heuristics (still without adding deps)
- Examples of usage patterns

**Maybe, let's talk first (open an issue):**
- New CLI flags or commands
- Changes to the entries JSON schema
- Changes to the memory file format
- Anything that changes default behavior

**Probably no:**
- Adding runtime dependencies — the scripts use only Node's standard library and that's a feature, not a limitation
- Porting to non-OpenClaw/non-Telegram surfaces — see [README.md#limitations](./README.md#limitations); this is by design, not an oversight
- Heavyweight tooling (linters, formatters, build steps) for such a small codebase
- TypeScript conversion — it's ~600 lines of plain ES modules and that's the right size

## How to propose a change

1. **Open an issue first** if your change touches public surface (commands, JSON schema, memory format) or is more than ~50 lines. Quick fixes can go straight to a PR.
2. **Fork, branch, code.** Branch off `main`. Name your branch like `fix/merge-marker-double` or `feat/explain-fallback`.
3. **Add a test.** Even one. The pattern in `tests/run.mjs` is small and copyable.
4. **Run the tests.** `node tests/run.mjs` should print `12 passed, 0 failed, 12 total` (plus your new test).
5. **Update CHANGELOG.md** under an `## Unreleased` section if your change is user-visible.
6. **Open a PR.** See the template — there's a small checklist.

## Code style

- Plain ES modules, `import` / `export`. No TypeScript, no Babel, no JSX.
- 2-space indent, semicolons, double-quoted strings — match what's already in `scripts/`.
- Prefer small, named functions over inline closures.
- No comments that just restate what the code does. Comments that explain *why* (a tricky invariant, a workaround) are welcome.
- No `console.log` in committed code (the scripts use `process.stdout.write` / `process.stderr.write` deliberately).

## Repository layout

```text
savenow/
├── SKILL.md                    skill spec for OpenClaw agents
├── README.md                   user-facing intro + install
├── CHANGELOG.md                semver-ish notes per release
├── package.json                metadata only — no deps
├── scripts/
│   ├── merge-daily-memory.mjs  apply path: writes to memory file
│   ├── preview-diff.mjs        preview path: renders diff + pending state
│   └── lib/memory.mjs          shared parsing / dedup helpers
├── examples/                   sample inputs and outputs
├── tests/run.mjs               zero-dep test runner
└── .github/                    issue / PR templates and CI
```

## Releasing (for maintainers)

1. Bump `version` in `package.json` and add a release section to `CHANGELOG.md`.
2. Tag: `git tag -a v0.x.y -m "savenow v0.x.y"` and push the tag.
3. Create a GitHub Release pointing to the changelog entry.

## Questions

Open a [Discussion](https://github.com/Chelebii/savenow/discussions) or an issue. I read everything, even when I'm slow to reply.
