<p align="center"><b>Language</b>: English · <a href="./README.zh-CN.md">中文</a></p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-skill-creator banner" width="100%" />
</p>

<h1 align="center">yotta-skill-creator · 元造 (YuanZao)</h1>

<p align="center">YottaMeta's <b>end-to-end skill scaffold generator</b>: give it <code>yotta-&lt;name&gt;</code> + a Chinese name + a description, and it renders a release-compliant skill directory from an embedded template, then runs a structure self-check before reporting success. <b>Zero dependencies (Python 3.8+ standard library)</b>; Windows + Linux + macOS.</p>
<p align="center">Triggers when the user wants to create a new yotta- skill, scaffold a skill from scratch, or turn the release-standard pitfalls into a reusable template; or says 元造 / 造技能 / 脚手架 / scaffold / 新建技能.</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-skill-creator"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-skill-creator" /></a>
  <a href="https://github.com/YottaMeta/yotta-skill-creator"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-skill-creator" /></a>
  <a href="https://github.com/YottaMeta/yotta-skill-creator/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/yotta-skill-creator" /></a>
  <a href="https://github.com/YottaMeta/yotta-skill-creator"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen" /></a>
</p>

## What it is

Creating a new skill for an agent often means re-discovering the same release pitfalls each time: naming rules, the four-way install README, version alignment, npm packaging, installers. YuanZao turns the whole "scaffold + structure check" step into one deterministic command — the scaffold it generates is already compliant with the YottaMeta release standard, so the skill body is the only thing left to write.

## How it works

```bash
# Full release scaffold (default)
python3 scripts/yotta_skill_creator.py create yotta-my-tool \
    --zh 元工 --desc "what it does + when it triggers + boundaries" --summary "one-liner"

# Self-use mode: skill body only, no release artifacts
python3 scripts/yotta_skill_creator.py create yotta-private \
    --zh 元私 --desc "private skill description" --self-use

# Also generate a CLI skeleton + tests; skip banner / installer
python3 scripts/yotta_skill_creator.py create yotta-tool2 \
    --zh 元工 --desc "..." --with-cli --no-banner --skip-installer
```

Pipeline: naming validation → embedded template → placeholder replacement → structure self-check. Exit code 0 is returned only when the scaffold passes.

## What you get

**Full mode (default):** SKILL.md (four-field frontmatter) / README.md + README.zh-CN.md (four-way install) / package.json / CHANGELOG.md / LICENSE (MIT) / NOTICE / install.sh + bin/install.js / .gitignore / .npmignore / .github/workflows/publish.yml / references/ / assets/.

**Self-use mode (--self-use):** only the skill body — SKILL.md / references/ (plus scripts/ with --with-cli). No release artifacts.

## Options

| Option | Purpose |
|---|---|
| `--zh 元X` | Chinese name (required, 元X convention) |
| `--desc "..."` | SKILL.md description: what + when to trigger + boundaries (required) |
| `--summary "..."` | One-line summary for the README (defaults to desc) |
| `--out <dir>` | Output parent directory (default: current dir, creates `<out>/<name>/`) |
| `--with-cli` | Also generate a CLI skeleton + tests (scripts/) |
| `--no-banner` | Skip the assets/ folder |
| `--skip-installer` | Skip install.sh / bin/install.js (and drop bin from package.json) |
| `--self-use` | Self-use mode: skill body only, no release artifacts |

## Naming validation (rejects if any rule fails)

| Rule | Requirement | Counter-example |
|---|---|---|
| Prefix | Must start with `yotta-` | `my-tool` |
| Characters | Lowercase letters / digits / hyphens, not ending with a hyphen | `yotta-Bad` / `yotta-` |
| Length | ≤ 64 characters | over-long name |
| Chinese name | `元X`: starts with 元, 2–8 characters | `工具` (missing 元) |
| Target | Output directory must not exist (no overwrite) | an existing directory |

## Structure self-check (runs automatically after creation)

Any failure returns exit code 2: required files present per mode / frontmatter name matches the directory / versions aligned across package.json · SKILL.md · CHANGELOG / README contains the four install methods / no leftover placeholders / balanced Markdown fences.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Success, scaffold compliant |
| 2 | Argument / naming / self-check failed |
| 4 | Fatal exception |
| 130 | Ctrl+C interrupt |

## Behavioral anchors

1. **Generate only, never overwrite**: an existing target directory is rejected.
2. **Embedded template**: the template ships inside the published package (`template/`), with no dependency on the repo's `tools/`.
3. **Self-check before success**: `create` runs the structure check before reporting completion.
4. **Self-use mode never touches release artifacts**: `--self-use` makes it explicit that creating is not publishing.

## Division of labor with the workshop toolchain

| Skill | Role |
|---|---|
| 元造 yotta-skill-creator (this skill) | **Create**: compliant scaffold + structure self-check |
| 元守 yotta-publish-guard | **Guard**: pre-publish check / pack / versions / names / publish |

Recommended flow: **元造 create (scaffold) → develop the skill body / scripts / tests → 元守 check → pack → versions → names → publish**.

References: `references/tutorial.md` (Chinese tutorial), `references/cli-reference.md` (full CLI reference), `references/scaffold-structure.md` (generated layout).

## Installation

Pick any of the four methods below; the order is the recommended priority. Skill files always come from **npm** (GitHub can be slow without a proxy; npm supports mirrors).

### Method 1: npm one-liner (recommended)

```text
# Optional China mirror: npm config set registry https://registry.npmmirror.com
npx -y @yottameta/yotta-skill-creator@0.1.7 --agent <agent-name>      # install to the agent's default user-level skills dir
npx -y @yottameta/yotta-skill-creator@0.1.7 --dir <your-skills-dir>   # point to the skills dir itself (e.g. ~/.codex/skills)
```

- `--agent <name>` installs to that agent's default user-level directory; `--list` shows each agent's default directory.
- `--dir <path>` installs to the given directory; for agents not in the preset list, point `--dir` at their skills directory.
- If the mirror has not synced the new package (404): add `--registry=https://registry.npmjs.org/` (a proxy may be needed in China), or wait for the mirror cache.

### Method 2: git clone (developers / git available)

```text
git clone https://github.com/YottaMeta/yotta-skill-creator.git <your-skills-dir>/yotta-skill-creator
```

### Method 3: GitHub Download ZIP (manual / no git)

On the GitHub repository `YottaMeta/yotta-skill-creator`, click **Code → Download ZIP**, unzip it and put the `yotta-skill-creator` folder into the agent's skills directory.

### Method 4: install.sh (multi-agent one-liner script)

```text
bash install.sh --agent <name>   # install to the agent's default user-level directory
bash install.sh --dir <path>     # install to the given directory
bash install.sh --list           # list agents -> default directories
```

> Method 1 uses the npm registry (npmmirror / npmjs) and does not depend on GitHub; Methods 2/3 use GitHub and may fail without a proxy in China.

## Development & validation

The package ships its own test suite (included in the published package):

```bash
# Run the full suite (20 cases) from the skill directory
python scripts/test_yotta_skill_creator.py
```

## License

MIT © YottaMeta — see [LICENSE](./LICENSE).
