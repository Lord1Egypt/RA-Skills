<p align="center"><b>Language</b>: English · <a href="./README.zh-CN.md">中文</a></p>

<h1 align="center">{{skill_name}} · {{zh_name}}</h1>

<p align="center">{{summary}}</p>
<p align="center">{{description}}</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/{{skill_name}}"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/{{skill_name}}" /></a>
  <a href="https://github.com/YottaMeta/{{skill_name}}"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/{{skill_name}}" /></a>
  <a href="https://github.com/YottaMeta/{{skill_name}}/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/{{skill_name}}" /></a>
</p>

## What it is

Fill in: describe what this skill does, when it triggers, and what it outputs.

## When to use

- Fill in: trigger scenarios.
- Fill in: more trigger scenarios.

**Do NOT trigger** when: Fill in boundaries.

## Quick usage

```bash
# Fill in: replace with real commands this skill ships
python3 scripts/{{skill_name}}.py --help
```

## Installation

Pick any of the four methods below; the order is the recommended priority. Skill files always come from **npm** (GitHub can be slow without a proxy; npm supports mirrors).

### Method 1: npm one-liner (recommended)

```text
# Optional China mirror: npm config set registry https://registry.npmmirror.com
npx -y @yottameta/{{skill_name}} --agent <agent-name>      # install to the agent's default user-level skills dir
npx -y @yottameta/{{skill_name}} --dir <your-skills-dir>   # point to the skills dir itself (e.g. ~/.codex/skills)
```

- `--agent <name>` installs to that agent's default user-level directory; `--list` shows each agent's default directory.
- `--dir <path>` installs to the given directory; for agents not in the preset list, point `--dir` at their skills directory.
- If the mirror has not synced the new package (404): add `--registry=https://registry.npmjs.org/` (a proxy may be needed in China), or wait for the mirror cache.

### Method 2: git clone (developers / git available)

```text
git clone https://github.com/YottaMeta/{{skill_name}}.git <your-skills-dir>/{{skill_name}}
```

### Method 3: GitHub Download ZIP (manual / no git)

On the GitHub repository `YottaMeta/{{skill_name}}`, click **Code → Download ZIP**, unzip it and put the `{{skill_name}}` folder into the agent's skills directory.

### Method 4: install.sh (multi-agent one-liner script)

```text
bash install.sh --agent <name>   # install to the agent's default user-level directory
bash install.sh --dir <path>     # install to the given directory
bash install.sh --list           # list agents -> default directories
```

> Method 1 uses the npm registry (npmmirror / npmjs) and does not depend on GitHub; Methods 2/3 use GitHub and may fail without a proxy in China.

## Development & validation

```bash
# Fill in: run the skill's own test suite
python scripts/test_{{skill_name}}.py
```

## License

MIT © YottaMeta — see [LICENSE](./LICENSE).
