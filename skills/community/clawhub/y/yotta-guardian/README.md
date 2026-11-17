<p align="center"><b>Language</b>: English · <a href="./README.zh-CN.md">中文</a></p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-guardian banner" width="100%" />
</p>

<h1 align="center">yotta-guardian · 元盾 (Yuandun)</h1>

<p align="center">YottaMeta's tool-call interception guardrail: a <b>deterministic rule engine + pluggable intent verifier</b> that evaluates exec / write / edit / read / run / shell tool calls and returns <b>allow / deny + matched rules + audit logs</b>. Use it as a deterministic safety gate before an agent runs a high-risk command, writes a sensitive system path, or changes system configuration.</p>
<p align="center">Activates when an agent is about to perform dangerous operations — recursive delete, disk formatting, privilege escalation, firewall changes, reverse shell, download-and-run, writes to core system files — <b>deterministic verdicts by rules, not prompt-engineering luck</b>.</p>
<p align="center">Pure Python 3.8+ standard library, zero external dependencies; Windows + Linux + macOS; read-only evaluation by default, configurable allowances, full audit trail.</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-guardian"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-guardian" /></a>
  <a href="https://github.com/YottaMeta/yotta-guardian"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-guardian" /></a>
  <a href="https://github.com/YottaMeta/yotta-guardian/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/yotta-guardian" /></a>
  <a href="https://github.com/YottaMeta/yotta-guardian"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen" /></a>
</p>

## What it is

When an AI agent acts autonomously, a single recursive delete, one disk write, or a download-and-run can cause irreversible damage. Yuandun packages these dangerous actions into a deterministic rule engine: every tool call (exec / write / edit / read / run / shell) is evaluated structurally — command text, argv-level verb and target analysis, sensitive paths, and written content — producing an allow / deny verdict with the matched rules and reasons, plus audit-log trails.

It is not tied to any single platform: an agent-agnostic toolkit that works in any agent supporting Agent Skills. Read-only evaluation by default — it neither executes nor auto-approves dangerous actions; intent verification calls no model by default and can be plugged into any external verifier (e.g. an LLM gateway) through a JSON protocol.

## Core value

- **Deterministic rule engine** — text patterns (download-and-run / encoded execution / reverse shell) + argv-level verb/target analysis (rm / dd / mkfs / chmod / chown / privilege escalation / firewall / services / persistence) + sensitive paths + written content: four stacked layers of rules.
- **Sensitive-path guard** — writes to /etc/passwd, /etc/sudoers, SSH authorized keys, /boot, /dev devices, Windows system directories and hosts, and registry startup entries are denied.
- **Pluggable intent verification (no model required)** — zero-dependency by default; optional built-in local heuristics (--heuristic), or any external intent verifier via a stdin/stdout JSON protocol (--verifier / config file).
- **Three policies** — default (deny high+), strict (deny medium+), loose (deny critical only), chosen per scenario.
- **Audit trail** — JSONL audit log + audit query subcommand; every allow / deny is traceable.
- **Machine readable** — --json outputs pure JSON (per-call verdicts, rules, exit codes); --batch pre-checks a list of calls, ideal as a pre-execution gate.

## Why use it

| Advantage | Description |
|---|---|
| **Zero dependency** | Python 3.8+ standard library; no daemon / database / external scanner; Windows + Linux + macOS |
| **Deterministic** | Verdicts are reproducible and explainable, not model probability; intent verification is off by default and opt-in |
| **Structural** | Evaluates commands, paths and content per tool type (exec / write / edit / read), not naive string matching |
| **Configurable** | --allow / --allow-path / custom rule JSON (policy / deny / allow / verifier) |
| **Traceable** | Every verdict lands in a JSONL audit log; audit subcommand filters by denied / tool / time |
| **Ecosystem distribution** | GitHub + npm + ClawHub synced; four install methods (npx / git clone / Download ZIP / install.sh) |

## Commands

| Command | Description |
|---|---|
| check | Evaluate one or a batch of tool calls (--batch); text / JSON / Markdown reports |
| audit | Query audit logs (--tail / --denied / --since / --tool / --json) |
| rules | Print the built-in rule summary / validate a custom rules file |
| version | Print the version |

## Quick start

Windows uses python, Linux/macOS uses python3.

```bash
# Check one exec call (0 = allowed)
python3 scripts/yotta_guardian.py check exec --cmd "git status"

# Check a dangerous command (denied by default, exit code 3)
python3 scripts/yotta_guardian.py check exec --cmd "rm -rf /"

# Check a write (writing /etc/passwd is denied)
python3 scripts/yotta_guardian.py check write --path /etc/passwd --content "..."

# Batch pre-check (the agent hands the pending call list to the guardrail before running)
python3 scripts/yotta_guardian.py check --batch calls.json --json

# Audit
python3 scripts/yotta_guardian.py check exec --cmd "..." --audit-log .yotta-guardian/audit.jsonl
python3 scripts/yotta_guardian.py audit --file .yotta-guardian/audit.jsonl --tail 20
```

Exit codes (same semantics as the YuanAn / YuanShen family): **0** = allowed; **1** = allowed with warning (manual review recommended); **2** = denied (high); **3** = denied (critical); **4** = usage error / fatal exception.

## Install

Pick any of the four methods below; the order is the recommended priority. Skill files always come from **npm** (GitHub can be slow without a proxy; npm supports mirrors).

### Method 1: npm one-liner (recommended)

```text
# Optional China mirror: npm config set registry https://registry.npmmirror.com
npx -y @yottameta/yotta-guardian --agent <agent-name>      # install to the agent's default user-level skills dir
npx -y @yottameta/yotta-guardian --dir <your-skills-dir>   # point to the skills dir itself (e.g. ~/.codex/skills)
```

- `--agent <name>` installs to that agent's default user-level directory; `--list` shows each agent's default directory.
- `--dir <path>` installs to the given directory; for agents not in the preset list, point `--dir` at their skills directory.
- If the mirror has not synced the new package (404): add `--registry=https://registry.npmjs.org/` (a proxy may be needed in China), or wait for the mirror cache.

### Method 2: git clone (developers / git available)

```text
git clone https://github.com/YottaMeta/yotta-guardian.git <your-skills-dir>/yotta-guardian
```

### Method 3: GitHub Download ZIP (manual / no git)

On the GitHub repository `YottaMeta/yotta-guardian`, click **Code → Download ZIP**, unzip it and put the `yotta-guardian` folder into the agent's skills directory.

### Method 4: install.sh (multi-agent one-liner script)

```text
bash install.sh --agent <name>   # install to the agent's default user-level directory
bash install.sh --dir <path>     # install to the given directory
bash install.sh --list           # list agents -> default directories
```

> Method 1 uses the npm registry (npmmirror / npmjs) and does not depend on GitHub; Methods 2/3 use GitHub and may fail without a proxy in China.
## Usage examples (AI agent)

1. Hook this repo's SKILL.md into any AI agent's skill/rule system (see install above).
2. Before executing any high-risk tool call, run a check first:
   ```bash
   python3 scripts/yotta_guardian.py check exec --cmd "<pending command>" --json
   ```
   With exit code 2 / 3, do not execute — explain the matched rules to the user; only with explicit authorization use --allow / --allow-path / custom rules.
3. For multiple calls, pre-check in batch:
   ```bash
   python3 scripts/yotta_guardian.py check --batch calls.json --json
   ```
4. Before writing sensitive paths / changing system config, check the target path and content with write / edit.
5. High-risk operations land in the audit log; query them later with audit.

## Boundaries (security red lines)

- **Read-only evaluation by default** — does not execute, does not auto-approve, does not modify anything; it is a gate before execution, not a substitute for the user's decision.
- **No hidden audit** — every verdict is recorded and traceable; rules are configurable but critical rules cannot be overridden.
- **Authorization** — for explicitly authorized / own-asset / educational environments only; using it to bypass real-world authorization is the user's own responsibility.

## Development & validation

- Tests: python scripts/test_yotta_guardian.py (60 tests; Windows: python)
- Base validation: python tools/validate-skill.py yotta-guardian (run at the repo root)
- Rule details: references/rules.md; policies & exit codes: references/policies.md; intent-verifier protocol: references/intent-verifier.md

Keep tests green and bump the version before releasing changes.

## Changelog

See [CHANGELOG.md](./CHANGELOG.md).

## License

[MIT](./LICENSE) © YottaMeta. "Yuandun" / "yotta-guardian" and the YottaMeta family names (yotta-* prefix) are YottaMeta brand identifiers; derived works must not reuse them, see [NOTICE](./NOTICE). The guardrail direction references open-source safe-guardian style skills; the implementation is YottaMeta's own new code.
