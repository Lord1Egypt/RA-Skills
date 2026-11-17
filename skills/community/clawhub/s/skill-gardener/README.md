# Skill Gardener

Turn proven work into compact, reusable agent skills. Gardener checks the evidence, repairs a matching skill when possible, validates a staged candidate, and links the result back to its source.

It is designed for OpenClaw and file-based Agent Skills workflows. It does not install a scheduler or background hook: automatic selection depends on the host agent. Creating a skill does not itself schedule recurring work.

## Install

Review this repository first. Install it through your runtime's supported Git/local skill installer, or clone into the chosen workspace's skill collection. For the manual route, run from that workspace, with no existing `skills/skill-gardener` directory:

```bash
git clone https://github.com/ShadowNineX/skill-gardener.git skills/skill-gardener
```

The repository root is the skill package. Confirm the runtime discovers its `SKILL.md`; actual skill roots, precedence, gating, and refresh behavior depend on the runtime/version. See the [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills).

## Prepare the audit

Requires Python 3.10+. The audit uses PyYAML when it is already available and otherwise uses its built-in bounded parser, so a fresh Python installation can run it directly:

```bash
python3 scripts/audit_skills.py --skill .
```

The helper never installs packages, accesses the network, executes candidate code, or changes audited files.

Once installed elsewhere, resolve the helper from the loaded skill's directory, not the current working directory. `{baseDir}` in the OpenClaw skill instructions is supplied by OpenClaw; it is not a literal shell environment variable.

## Use

Ask your agent to save a verified workflow as a skill, repair a stale skill, or review a recurring procedure for promotion. You may authorize ongoing local gardening; otherwise Gardener prepares a proposal before changing skills. Existing authorization is reused. Governance edits, removals/merges, hooks, installations, and publishing require their own applicable authorization.

A successful run identifies the source evidence, selects one destination, stages and checks the change, applies it, verifies runtime discovery, and records provenance. Failed checks keep the candidate a draft. Runtime discovery or source-link failures are reported as pending, not complete.

## Optional companions

- [Self-Improving Agent](https://github.com/pskoett/self-improving-agent) supplies `.learnings/` records. Gardener supports its `promoted_to_skill` / `Skill-Path` schema without running its hook or extraction script.
- [Skill Vetter](https://clawhub.ai/spclaudehome/skills/skill-vetter) can assist external package review. Direct static review or the runtime's own verification workflow also works.

Neither is required or installed automatically. See [integration guidance and review limitations](references/integrations.md) for the versions inspected, confirmed companion issues, and precise review scope.

## Audit behavior

```bash
# One skill, without reading siblings
python3 scripts/audit_skills.py --skill /path/to/skill

# One actual collection root, including grouped skill directories
python3 scripts/audit_skills.py /path/to/workspace/skills
```

The JSON report includes scope, discovered skill count, pass/fail, issues, and warnings. Exit codes: `0` passes structural checks, `1` validation/discovery fails, `2` invalid invocation or root.

Checks cover valid YAML, a nonempty body, name syntax and the 64-character limit, nonempty string descriptions and their decoded 1024-character limit, supported optional-field types, and duplicate names within the selected root. Directory/name mismatches are warnings because OpenClaw supports layouts that differ from the portable Agent Skills naming convention; newly authored skills should match.

Collection discovery stops below each directory containing `SKILL.md`, including invalid files. It searches up to six directory levels by default (`--max-depth` accepts 1–64), visits at most 10,000 entries, and skips `.git`, `.hg`, `.svn`, `.venv`, `venv`, `node_modules`, and `__pycache__`. Encountering a symlink, unreadable directory, or discovery limit makes the result fail rather than silently declaring full coverage. Root paths must also have no symlink components; use the actual physical path on systems with aliased temporary directories. File symlinks and special files are rejected; each `SKILL.md` is capped at 1 MiB. Run against a stable tree: this helper is not a sandbox against concurrent adversarial filesystem changes.

The parser accepts quoted values, comments, multiline scalars, simple flow collections, and nested OpenClaw metadata. It rejects duplicate keys, aliases, merge keys, unsafe YAML tags, and nesting beyond 32 levels. These are deliberate audit restrictions, not claims that every runtime rejects those constructs. The built-in fallback intentionally supports this audit subset rather than all YAML syntax.

The audit does **not** establish that instructions are safe, triggers are useful, scripts work, references exist, all runtime metadata is valid, or the host can load a skill. The procedural review, relevant tests, and runtime discovery check remain necessary. It does not merge separate roots or account for runtime precedence; audit roots separately and inspect the effective catalog.

## Development checks

From the repository root:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/audit_skills.py --skill .
```

Tests use temporary fixtures and cover malformed and valid YAML, limits, grouped discovery, links/special files, duplicate skills, read-only behavior, and CLI exit codes. GitHub Actions runs these checks on supported Python versions.
