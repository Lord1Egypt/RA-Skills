# skill-release-audit

> Pre-publish quality & safety auditor for AI agent **skills**
> (the `SKILL.md` + `scripts/` + `references/` format used by Claude Code,
> OpenAI Codex, GitHub Copilot, Cursor, OpenClaw, ClawHub, and compatible
> SkillHub registries).

A **pure auditor**: reads your skill, prints structured `✅/⚠️/❌` findings,
suggests fixes. Never edits your files, never publishes. Publishing is left
to each ecosystem's own tooling.

- **Zero hard dependencies.** Python 3.8+ standard library only. PyYAML is an
  optional enhancement (auto-detected; falls back to a built-in parser that
  handles inline JSON values).
- **No network by default.** The only network action is an opt-in
  `--auto-install` for missing Python deps.
- **Portable.** Works outside OpenClaw — no hardcoded framework paths.

## Install / Run

```bash
git clone https://github.com/Songhonglei/build-better-skills.git
python build-better-skills/skills/skill-release-audit/scripts/healthcheck.py <path/to/skill-dir>
```

Or install via `clawhub`:

```bash
clawhub install skill-release-audit
python ~/.skills/skill-release-audit/scripts/healthcheck.py <path/to/skill-dir>
```

## What it checks (6 modules)

| # | Module | Checks |
|---|--------|--------|
| 1 | Syntax & logic | Python AST parse, Bash `-n`, internal reference paths, leftover TODO/FIXME |
| 2 | Feature coverage | scripts/references mentioned in SKILL.md, stub-file detection |
| 3 | Edge cases | try/except coverage, HTTP timeout, response-status handling, Bash `set -e` |
| 4 | Data safety | data/config/cache written *inside* the skill dir (lost on update) |
| 5 | Dependencies | Python/Node/Bash deps, optional auto-install, **declaration-vs-code env check** |
| 6 | Documentation | frontmatter quality, slug rules, required files, target-specific specs |

Exit codes: `0` = no errors (warnings allowed), `1` = errors found, `2` = invalid input.

## Targets (`--target`)

Different registries have different rules. `--target` tunes which checks fire
and at what severity — it does **not** publish.

```bash
python scripts/healthcheck.py <dir> --target clawhub    # clawhub.com rules
python scripts/healthcheck.py <dir> --target github     # expects README + LICENSE
python scripts/healthcheck.py <dir> --target anthropic  # Anthropic-compat base spec
python scripts/healthcheck.py <dir> --target skillhub   # private SkillHub (version required)
python scripts/healthcheck.py <dir>                     # default: generic (loosest)
```

Profiles live in [`profiles/`](profiles/) as JSON; add your own by dropping a new
`<name>.json` there. See [`references/hub-specs.md`](references/hub-specs.md)
for per-registry specifications.

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--target <name>` | `generic` | Registry profile to validate against |
| `--lang <zh\|en>` | auto-detect | Report language (from `$LC_ALL` / `$LANG`) |
| `--auto-install` | off | pip-install missing Python deps (modifies env) |
| `--install-timeout <s>` | 60 | Per-package install timeout (with `--auto-install`) |
| `--modules <list>` | all | Run only specific modules, e.g. `--modules 5,6` |

## Declaration-vs-code env check

Mirrors registry-side security analysis: if your code reads an environment
variable (`os.environ["X"]`, `os.getenv(...)`, `process.env.X`) that isn't
declared in frontmatter under `metadata.openclaw.requires.env` / `primaryEnv` /
`envVars`, the auditor flags a metadata mismatch (severity is profile-driven).

## Part of build-better-skills

This skill is part of the [build-better-skills](https://github.com/Songhonglei/build-better-skills)
suite — a complete toolchain for the full lifecycle of agent skill development.

| Stage | Skill | Status |
|---|---|---|
| Creation | `skill-creator` | 🚧 Not yet released |
| Audit | **`glic-check`** | ✅ v1.0.1 |
| Audit | **`skill-deep-audit`** | ✅ v1.0.0 |
| **Audit** | **`skill-release-audit`** | ✅ **v1.0.0** |
| Release | `skill-release` | 🚧 Not yet released |
| Testing | `skill-regression` | 🚧 Not yet released |
| Sediment | `skill-sediment` | 🚧 Not yet released |

Three Audit-stage tools are **complementary**:
- `glic-check` = lightweight cognitive UGLIC review (LLM-based, tight edit loops)
- `skill-deep-audit` = heavyweight cognitive scorecard (115-point, mid-cycle)
- `skill-release-audit` = mechanical static gate (no LLM, last automated gate before publishing)

## Known Issues (v1.0.0)

Found by running the auditor on itself. All are non-blocking (0 ERR across
all 5 targets). Will be addressed in v1.0.1+:

- **Module 1 leftover-marker false positive**: scans table cells that start
  with `1.` (e.g. `| 1. Syntax & logic |`) and flags them as TODO/FIXME-style
  leftover markers. Workaround: ignore for Markdown table content.
- **Module 5 PyYAML undeclared**: by best-practice convention, frontmatter
  is restricted to `name` + `description` only — `python_optional` lives in
  README. Module 5 only reads frontmatter so it reports PyYAML as undeclared
  (false positive given the modern convention).
- **Module 5 `SKILL_AUDIT_LANG` undeclared**: same root cause — frontmatter
  `metadata.openclaw.requires.env` would silence it, but is intentionally
  omitted per the new frontmatter discipline.
- **`load_profile` silent degrade on corrupt named profile JSON** (C1
  from internal pre-release audit): currently prints to stderr but uses the
  generic profile. Add a louder warning in v1.0.1.
- **`i18n.py:17` docstring example references wrong key**: `deps.pkg_missing`
  should be `deps.py_missing`. Cosmetic, no functional impact.

## Changelog

### v1.0.1 (2026-06-21)

Documentation-only patch — reclassified within the build-better-skills suite.

- **Stage reclassification**: moved from Release/Audit → **Audit** stage,
  joining `glic-check` and `skill-deep-audit` as the three complementary
  Audit-stage tools (cognitive lightweight / cognitive heavyweight /
  mechanical gate). The Release stage is now reserved for `skill-release`
  (packaging + publishing tool, coming soon)
- **Stages table**: added `skill-deep-audit` row (was missing in v1.0.0)
- **Complementary workflow**: now documents the 3-tool workflow
  (`glic-check` → `skill-deep-audit` → `skill-release-audit`)
- No code changes — all 6 modules, 5 profiles, and bilingual reporting
  remain identical to v1.0.0

### v1.0.0 (2026-06-21)

Initial open-source release. Forked from internal v1.2.0 (stable, in production
use). Highlights:

- 6 modular checks (`scripts/check_*.py`) — all run in parallel
- 5 registry profiles (`profiles/*.json`) — clawhub / anthropic / github / skillhub / generic
- Bilingual reporting (`scripts/i18n.py`) — zh / en, auto-detects locale
- Frontmatter fallback parser handles inline JSON without PyYAML dep
- Zero-network default; `--auto-install` opt-in for Python deps
- `--target` tunes checks per registry, never publishes
- Comprehensive `references/` docs (hub-specs / dep-patterns / safe-paths)

## License

MIT — see [LICENSE](./LICENSE).

## Author

Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
