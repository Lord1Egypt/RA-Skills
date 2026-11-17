---
name: skill-release-audit
version: 1.2.0
python_optional: [yaml]
metadata: {"openclaw": {"requires": {"env": ["SKILL_AUDIT_LANG"]}}}
description: >
  Pre-publish quality and safety auditor for AI agent skills (SKILL.md +
  scripts/ + references/ format used by Claude Code, Cursor, OpenAI Codex,
  GitHub Copilot, OpenClaw, ClawHub, and compatible SkillHub registries).
  Six static-check modules (no LLM, no network by default): (1) syntax and
  logic correctness, (2) feature completeness, (3) edge-case and error
  handling, (4) data safety (detects files written inside the skill dir that
  would be lost on update), (5) dependency declaration vs code, (6) SKILL.md
  documentation standards. Per-registry rule profiles via `--target`. Pure
  reporter — never edits your files, never publishes. Use when publishing
  a skill, modifying an existing skill, or diagnosing why a skill behaves
  unexpectedly — run it as the last machine-checkable gate before release.
  Trigger phrases: "skill release audit", "audit before publishing",
  "pre-release check", "release gate", "skill safety check",
  "发版前检查", "skill 发布检查", "审查这个 skill 能不能发版".
---

# skill-release-audit

- **Version**: 1.2.0
- **License**: MIT
- **Author**: Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
- **Repository**: https://github.com/Songhonglei/build-better-skills
- **Part of**: [`build-better-skills`](https://github.com/Songhonglei/build-better-skills) suite — see [Stages](https://github.com/Songhonglei/build-better-skills#stages) for the lifecycle map.

A six-module static inspector that catches mechanical problems machines can
verify — broken Python syntax, undeclared env vars, files written inside the
skill dir that would be lost on update, missing README/LICENSE for GitHub
targets, mismatched docs and scripts. Pairs with [`glic-check`](https://github.com/Songhonglei/build-better-skills/tree/main/skills/glic-check)
which does cognitive UGLIC review; together they cover both layers
(see [Part of build-better-skills](#part-of-build-better-skills)).

Prints a structured `✅/⚠️/❌` report per module with actionable fixes. **Does
not auto-fix.** All fixes require user confirmation.

---

## Agent Behavior Rules (must-read)

This skill is an **Auditor, not a Fixer.**

After running the check, the agent must follow these rules strictly:

1. **Show the full report first** — every module result, every warning / error
   with its specific description.
2. **Suggest fixes per finding, but only as suggestions, not actions.**
3. **Wait for explicit user confirmation** before touching any file.
4. **Never modify SKILL.md, scripts/, references/, or any other file** without
   confirmation.
5. **Never delete files**, even ones that look like leftovers — always ask first.

**Correct output template:**

```
📋 Check report: <skill-name>
[full output of healthcheck.py]

---
Issues found. Please confirm what to do:

✅ Can be ignored (false positives):
- Module 1: cache.json path warning — SKILL.md mentions it as descriptive text,
  not a file reference.

⚠️ Suggested fixes (awaiting your confirmation):
1. Module 3: auto_update.py _log() missing try/except — suggest wrapping.
2. Module 2: guide.py not listed in SKILL.md's module table — suggest adding.

Tell me which to fix and which to ignore. I'll act after you confirm.
```

---

## Usage

```bash
# Full check — report only, does NOT modify your environment (default)
python scripts/healthcheck.py <path/to/skill-dir>

# Opt in to auto pip-install missing Python deps (off by default)
python scripts/healthcheck.py <path/to/skill-dir> --auto-install

# Tune per-package install timeout (only with --auto-install)
python scripts/healthcheck.py <path/to/skill-dir> --auto-install --install-timeout 120

# Validate against a specific publishing target (tunes checks, does NOT publish)
python scripts/healthcheck.py <path/to/skill-dir> --target clawhub
python scripts/healthcheck.py <path/to/skill-dir> --format json

# Report output language: zh or en (default: auto-detected from $LC_ALL / $LANG)
python scripts/healthcheck.py <path/to/skill-dir> --lang en

# Run specific modules only (e.g. deps + docs)
python scripts/healthcheck.py <path/to/skill-dir> --modules 5,6
```

> Default behavior is **report only, do not install** — an auditor should not
> mutate the user's environment. Missing required deps are reported as ERROR;
> with `--auto-install`, install failures are reported as WARN (usually
> network/registry issues, not skill bugs).

## Publishing target (`--target`)

Different registries have different rules. `--target` tunes which checks fire
and at what severity — it **does not publish**.

| target | Use case | Notes |
|--------|----------|-------|
| `generic` (default) | Cross-registry minimum | Loosest, smallest common set |
| `clawhub` | clawhub.com | name+description required, strict slug, 50MB cap, declaration-vs-code consistency |
| `anthropic` | Anthropic-compatible base spec | name≤64 / description≤1024, body recommended <5k tokens |
| `github` | Open-sourcing to GitHub | Requires README + LICENSE |
| `skillhub` | Private SkillHub (vendor-compatibility layers) | Same as clawhub but version required (WARN) |

Profiles live in [`profiles/`](profiles/) as JSON; add your own by dropping a new
`<name>.json` there.

Env-var check severity is configured **per finding code** via each profile's
`env_severity` key (v1.1 governance): `ENV_REQUIRED_UNDECLARED` /
`ENV_OPTIONAL_OVERRIDE` / `ENV_RUNTIME_INJECTED` / `ENV_AMBIENT` /
`ENV_TEST_ONLY` / `ENV_REVIEW_REQUIRED` — each maps to `WARN` / `INFO` / `OFF`.
Platform env contracts (runtime-injected / ambient lists) live in
[`config/env_contracts.json`](config/env_contracts.json). See [`references/hub-specs.md`](references/hub-specs.md)
for per-registry specifications encoded by these profiles.

**JS env data-flow tracking (v1.2)**: for JS/TS scripts the auditor tracks
environment-object alias propagation — `const environment = process.env`,
`fn(process.env)` parameter binding, Zod `schema.parse(environment)` /
`safeParse({...environment})` results, and config-loader return values
(`const config = loadConfig(process.env)`). Member accesses on those aliases /
parse results count as **indirect uses**: they only affect the reverse check
(a declared var is no longer misjudged `ENV_DECLARED_UNUSED`) and are filed
under the `ENV_DECLARED_INDIRECT` class — silent in the console report by
default, with hit paths preserved in JSON evidence. Indirect uses never
soften the forward classification (required / optional). Vars whose
propagation cannot be confirmed still report `ENV_DECLARED_UNUSED`.

**Module-1 ref classification (v1.2.1)**: paths referenced in SKILL.md are
split into package-internal refs (validated as before) and runtime-external
refs (`~/...`, `$HOME/...`, absolute paths incl. Windows drive letters) —
the latter resolve in the *user's* environment at runtime, so existence is
not a package-completeness problem: resolvable paths are skipped silently,
unresolvable ones emit INFO (never WARN).

## Report language

Default: auto-detected from `$LC_ALL` / `$LC_MESSAGES` / `$LANG`. Falls back to
`zh` (legacy default). Currently supported: `zh` / `en`.

- CLI: `--lang zh` / `--lang en`
- Env: `SKILL_AUDIT_LANG=en` (lower priority than `--lang`)

All user-facing text is centralized in `scripts/i18n.py` as a bilingual
key-table — add a new check by adding one `zh`/`en` entry; do not hardcode
strings in module files.

Exit codes: `0` = no errors (may have warnings), `1` = errors found,
`2` = invalid input.

## The six modules

| Module | Checks | Script |
|--------|--------|--------|
| 1. Syntax & logic | Python AST parse, Bash `-n` syntax check, internal reference paths (**package-internal vs runtime-external classification**: `~/`, `$HOME/`, absolute paths are user-environment paths — existence not enforced, INFO at most) | `scripts/check_logic.py` |
| 2. Feature coverage | scripts / references mentioned in SKILL.md, stub-file detection | `scripts/check_features.py` |
| 3. Edge cases | try/except coverage, HTTP timeout, response-status handling, Bash `set -e` | `scripts/check_edges.py` |
| 4. Data safety | Files written *inside* the skill dir (lost on update) | `scripts/check_data_safety.py` |
| 5. Dependencies | Python / Node / Bash deps, optional `--auto-install`, **env-var classification check** (false-positive governance v1.1 + v1.2 JS data-flow: classifies required / optional-override / runtime-injected / ambient / test-only / review / declared-indirect before demanding metadata — no more "reads == must declare", and alias/parse-flow accesses no longer false-positive as unused) | `scripts/check_deps.py` + `scripts/_env_check.py` |
| 6. Documentation | description quality, frontmatter discipline, slug rules, target-specific required files (README / LICENSE) | `scripts/check_docs.py` |

## Data safety hint

Skill directories are overwritten on update. All persistent data must live
**outside** the skill dir. The auditor probes the runtime environment
(OpenClaw / Claude Code / Codex / plain checkout) and suggests a portable path:

```python
from pathlib import Path
DATA_DIR = Path.home() / ".skill-data" / "<skill-name>"   # example, auto-tuned
```

See `references/safe-paths.md` for the full resolution order.

## Declaration vs code env check

Mirrors registry-side security analysis: if your code reads an env var
(`os.environ["X"]`, `os.getenv(...)`, `process.env.X`) that isn't declared in
frontmatter under `metadata.openclaw.requires.env` / `primaryEnv` / `envVars`,
the auditor flags a metadata mismatch (severity is profile-driven). This catches
the most common cause of post-publish runtime failures.

## Dependency declaration convention

In SKILL.md body, add a dependency section:

```markdown
## Dependencies

Auto-installed on first use: requests, pyyaml

System commands (install manually): jq (`brew install jq`)
```

See `references/dep-patterns.md`.

## Dependencies

Core uses Python 3.8+ standard library only — no external installs needed.

Optional enhancement: `pyyaml` (auto-detected). With PyYAML, frontmatter
parsing handles multi-line / list / nested fields strictly. Without it, a
tolerant built-in parser handles inline JSON values (e.g.
`metadata: {"key": "value"}`) so the same checks still work — no functionality
loss.

## Part of build-better-skills

This skill belongs to the [`build-better-skills`](https://github.com/Songhonglei/build-better-skills) suite.
For the full lifecycle map (Install → Audit → Release → Testing → Sediment),
all sibling skills, and their current status, see the
[**Stages table**](https://github.com/Songhonglei/build-better-skills#stages) on the suite repo home — kept as the single source
of truth (this file does not duplicate it).

