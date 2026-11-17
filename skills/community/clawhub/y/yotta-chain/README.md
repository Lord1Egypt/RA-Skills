<p align="center"><b>Language</b>: English · <a href="./README.zh-CN.md">中文</a></p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-chain banner" width="100%" />
</p>

<h1 align="center">yotta-chain · 元链 (Yuanlian)</h1>

<p align="center">YottaMeta's zero-dependency <b>supply-chain dependency validator</b>: detects <b>dependency confusion, lockfile inconsistencies, missing lockfiles, unpinned versions and typosquatting</b> across npm / Python / Maven by parsing manifests and lockfiles locally, and generates <b>SBOM-lite (CycloneDX 1.5 subset)</b>.</p>
<p align="center">Activates when the user needs to check a project's dependencies for supply-chain risks before build / release / CI, verify a lockfile matches its manifest, assess dependency-confusion exposure, or generate an SBOM — <b>fully local and offline: no online CVE lookups, no package-registry queries, no data leaves the machine</b>.</p>
<p align="center">No external tools required (Python 3.8+ standard library); Windows + Linux + macOS; every finding ships a severity, a plain-language explanation and a fix hint.</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-chain"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-chain" /></a>
  <a href="https://github.com/YottaMeta/yotta-chain"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-chain" /></a>
  <a href="https://github.com/YottaMeta/yotta-chain/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/yotta-chain" /></a>
  <a href="https://github.com/YottaMeta/yotta-chain"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen" /></a>
</p>

## What it is

Supply-chain attacks target the parts developers trust: dependency confusion (a private package name is squatted on a public registry), typosquatting, stale or hand-edited lockfiles, missing integrity hashes. Yuanlian packages "supply-chain triage" into a zero-dependency engine that reads your manifests and lockfiles **locally** — no Trivy / Snyk / npm audit needed.

It is agent-agnostic and works in any agent supporting Agent Skills. **Fully local and offline** — no online CVE databases, no registry queries, no data leaves the machine.

## Core value

- **Zero-dependency engine** — npm semver + PEP 440 range checks, TOML / JSON / requirements parsers, all built with Python 3.8+ standard library.
- **Dependency confusion** — scope registry configured in `.npmrc` but resolved from a public registry; the same package resolved from multiple registries; suspicious registry URLs (http / IP literal / localhost); pip extra-index and poetry secondary-source public fallback.
- **Lockfile consistency** — manifest entry missing from lockfile, locked version out of the declared range, root name / version mismatch, dangling references, missing integrity, same version with conflicting sources.
- **Hygiene** — missing lockfile, unpinned versions (`*` / `latest` / no constraint), Maven SNAPSHOT dependencies.
- **Typosquatting** — dependency names within edit distance 2 of well-known npm / PyPI packages are flagged for manual review.
- **SBOM-lite** — CycloneDX 1.5 subset JSON (components + dependencies + purl, with scope / direct / resolved / integrity as properties).
- **Three output modes** — text / JSON / CSV, plus a `--gate` exit-code gate for CI.

## Why use it

| Advantage | Description |
|---|---|
| **Zero dependency** | Python 3.8+ standard library; no daemon / database / external scanner; Windows + Linux + macOS |
| **Fully local offline** | Parses existing manifests / lockfiles only; no online CVE lookups, no registry queries, no data leaves the machine |
| **Deterministic signals** | Registry config vs actual resolution, range math (npm semver / PEP 440), integrity presence — not a random URL list |
| **CI-friendly** | `scan --gate high` exits 1 only when findings reach a chosen severity |
| **Teaching layer** | Every rule ships a Chinese plain-language explanation and a fix hint |

## Commands

| Command | Purpose |
|---|---|
| `scan` | Validate a project directory (auto-detect npm / python / maven) |
| `sbom` | Generate SBOM-lite (CycloneDX 1.5 subset JSON or text) |
| `version` | Print version |

`scan` exit codes: **0** = no findings at or above `--gate`; **1** = findings; **4** = usage / path / unsupported-manifest error. Default `--gate=info` (any finding exits 1); use `--gate high` for a stricter CI gate.

## Quick start

Windows: use `python`; Linux/macOS: use `python3`.

```bash
# scan the current project (auto-detects npm / python / maven)
python3 scripts/yotta_chain.py scan --path ./

# only medium and above, JSON output
python3 scripts/yotta_chain.py scan --path ./src --level medium --format json

# CI gate: exit 1 only when high-severity findings exist
python3 scripts/yotta_chain.py scan --path . --gate high; echo $?

# generate SBOM-lite (CycloneDX 1.5 subset JSON)
python3 scripts/yotta_chain.py sbom --path . --output sbom.json

# view the SBOM as text
python3 scripts/yotta_chain.py sbom --path . --format text

# version
python3 scripts/yotta_chain.py version
```

## Installation

Pick any of the four methods below; the order is the recommended priority. Skill files always come from **npm** (GitHub can be slow without a proxy; npm supports mirrors).

### Method 1: npm one-liner (recommended)

```text
# Optional China mirror: npm config set registry https://registry.npmmirror.com
npx -y @yottameta/yotta-chain --agent <agent-name>      # install to the agent's default user-level skills dir
npx -y @yottameta/yotta-chain --dir <your-skills-dir>   # point to the skills dir itself (e.g. ~/.codex/skills)
```

- `--agent <name>` installs to that agent's default user-level directory; `--list` shows each agent's default directory.
- `--dir <path>` installs to the given directory; for agents not in the preset list, point `--dir` at their skills directory.
- If the mirror has not synced the new package (404): add `--registry=https://registry.npmjs.org/` (a proxy may be needed in China), or wait for the mirror cache.

### Method 2: git clone (developers / git available)

```text
git clone https://github.com/YottaMeta/yotta-chain.git <your-skills-dir>/yotta-chain
```

### Method 3: GitHub Download ZIP (manual / no git)

On the GitHub repository `YottaMeta/yotta-chain`, click **Code → Download ZIP**, unzip it and put the `yotta-chain` folder into the agent's skills directory.

### Method 4: install.sh (multi-agent one-liner script)

```text
bash install.sh --agent <name>   # install to the agent's default user-level directory
bash install.sh --dir <path>     # install to the given directory
bash install.sh --list           # list agents -> default directories
```

> Method 1 uses the npm registry (npmmirror / npmjs) and does not depend on GitHub; Methods 2/3 use GitHub and may fail without a proxy in China.
## Usage with an AI agent

Tell the agent the context, e.g.:

```text
Before we release, run yotta-chain scan on the repo (gate high) and summarize the findings with fix suggestions.
```

The agent runs the engine, reports findings by severity, and explains each rule with the Chinese plain-language guidance in `references/rules.md`.

## Detection rules

| Rule | Severity | What it means |
|---|---|---|
| `confusion_scope_registry` | high | Scope has a private registry in `.npmrc`, but the lockfile resolves it from a public registry |
| `confusion_mixed_registry` | high | The same package is resolved from multiple registry hosts |
| `lockfile_missing_entry` | high | A manifest dependency is absent from the lockfile |
| `lockfile_range_unsatisfied` | high | Locked version does not satisfy the declared range (npm semver / PEP 440) |
| `lockfile_dangling_ref` | high | A lockfile package depends on a package not present in the lockfile |
| `lockfile_duplicate_conflict` | high | Same name + version with conflicting resolved / integrity sources |
| `missing_lockfile` | medium | Dependencies declared but no lockfile committed |
| `lockfile_root_mismatch` | medium | Lockfile root name / version differs from the manifest |
| `lockfile_integrity_missing` | medium | Lockfile entry has no integrity / hash |
| `confusion_extra_index` | medium | pip / poetry / pipenv mix a public registry with a private one (public becomes a fallback) |
| `confusion_suspicious_registry` | medium | Registry / index URL is http, an IP literal or a localhost address |
| `confusion_registry_mismatch` | medium | A private default registry is configured but packages resolve from a public registry |
| `unpinned` | low / medium | Dependency has no fixed version (`*` / `latest` / no constraint) |
| `typosquat` | low | Name within edit distance 2 of a well-known package — review manually |
| `snapshot` | low | Maven dependency uses a SNAPSHOT version |

## Supported ecosystems

- **npm** — `package.json` + `package-lock.json` (v1 / v2 / v3) / `npm-shrinkwrap.json` / `yarn.lock` / `pnpm-lock.yaml` / `bun.lock` + `.npmrc` (per-scope registries);
- **Python** — `requirements*.txt` (with `--index-url` / `--extra-index-url` / `-r` recursion), `pyproject.toml` (PEP 621 / poetry), `poetry.lock`, `uv.lock`, `Pipfile` / `Pipfile.lock`;
- **Maven** — `pom.xml` (basic: unpinned / SNAPSHOT / suspicious repository URLs / property + dependencyManagement resolution).
- `bun.lockb` is recognized but not deeply parsed; `go.mod` / `Cargo.lock` are not yet supported.

JSON scan output contains both `scannedFiles` (inputs actually read) and `files` (files with findings). A clean scan can have `files: []` while `scannedFiles` still lists the manifest and lock file.

## Boundaries

- Reads local files only; no networking, no CVE databases, no package-registry queries, no data leaves the machine.
- No online CVE comparison — that is the domain of Trivy / Snyk / npm audit; this engine provides local deterministic parsing and heuristic signals.
- Dependency-confusion detection is a **local approximation**: confirming "a private name is squatted publicly" needs an online check; the engine emits strong signals for manual review.
- Read-only; it never edits lockfiles or upgrades dependencies.

## Development & validation

```bash
python3 -m py_compile scripts/yotta_chain.py
python3 scripts/test_yotta_chain.py   # 52/52
```

## Changelog

Version history lives in [CHANGELOG.md](./CHANGELOG.md).

## License

[MIT](./LICENSE)
