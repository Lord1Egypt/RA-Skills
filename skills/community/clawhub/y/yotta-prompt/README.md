<p align="center"><b>Language</b>: English · <a href="./README.zh-CN.md">中文</a></p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-prompt banner" width="100%" />
</p>

<h1 align="center">yotta-prompt · 元引 (YuanYin)</h1>

<p align="center">YottaMeta's <b>intent-clarification &amp; ecosystem-entry</b> skill: when a user types a vague phrase or a single word, it identifies the intent, offers <b>2-4 candidate directions</b>, deep-dives into goal / scope / output, then routes to the matching YottaMeta skill and outputs a <b>ready-to-run prompt</b>.</p>
<p align="center">Activates when the user does not know how to prompt AI, does not know what they want, or says something vague — <b>always-load at session start</b>, so it catches users who would never trigger a skill on their own.</p>
<p align="center">No external tools required (Python 3.8+ standard library); Windows + Linux + macOS; fully local and offline — no network calls, no external services.</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-prompt"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-prompt" /></a>
  <a href="https://github.com/YottaMeta/yotta-prompt"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-prompt" /></a>
  <a href="https://github.com/YottaMeta/yotta-prompt/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/yotta-prompt" /></a>
  <a href="https://github.com/YottaMeta/yotta-prompt"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen" /></a>
</p>

## What it is

Many users do not know how to talk to an AI: they type a vague phrase or a single word and expect help, but they cannot say what they want. YuanYin is the **front door** of the YottaMeta skill family: it turns "I have no idea how to ask" into "here is a task that can actually run".

It follows a five-step flow: **1) identify intent → 2) offer 2-4 candidate directions → 3) confirm → 4) deep-dive (goal / scope / output / constraints) → 5) route to the matching YottaMeta skill and output a ready-to-run prompt.**

It is not a prompt beautifier. Prompt polishing is a red ocean; YuanYin only clarifies intent and connects users to the right skill.

## Core value

- **Intent clarification, not prompt polishing** — turns vague words into executable tasks; never jumps to conclusions on step 1.
- **Ten intent domains** — development / data / planning / memory / security / logs / learning / writing / quality / general, with Chinese + English keyword scoring (fully local). Industry-agnostic: works for weekly reports, spreadsheets, plans, speeches, translation, meeting notes, contracts, brainstorming, interview prep and more.
- **Skill-name locking** — mentions of `yotta-*` or a Chinese family name (元忆 / 元安 / …) pin that direction immediately.
- **Ecosystem entry** — maps every direction to the matching YottaMeta skill with its Chinese name, one-liner and install command.
- **Ready-to-run prompts** — each domain ships a prompt template you can fill in and run.
- **Scenario library** — 18 built-in walkthroughs across any industry (vague input → candidates → deep-dive → routing), see `references/scenarios.md`.

## Why use it

| Advantage | Description |
|---|---|
| **Always-load** | `always-load: true` at session start; catches users who would never manually load a skill |
| **Zero dependency** | Python 3.8+ standard library; no daemon / database / network; Windows + Linux + macOS |
| **Fully local offline** | Intent classification and mapping run locally; no external calls |
| **Works with zero skills installed** | Prompts are self-contained behavior descriptions; YottaMeta skills are optional accelerators, never a hard dependency |
| **Honest boundaries** | Clarification only — no preset stance, no safety review; prompts have no artificial limits (never violating laws / jailbreaking) |
| **Ecosystem distribution** | GitHub + npm + ClawHub synced; four install methods (npx / git clone / Download ZIP / install.sh) |

## Commands

| Command | Description |
|---|---|
| clarify | One vague phrase / word → 2-4 candidate directions with Chinese explanations |
| clarify --json | Structured candidates for programmatic use |
| clarify --top N | Limit candidate count (2-4, default 4) |
| map | Direction or skill name → YottaMeta skills + install commands + ready-to-run prompt |
| map --json | Structured mapping result |
| scenarios | List built-in scenario cases |
| --version | Print version |

## Usage

Windows uses `python`, Linux/macOS uses `python3`.

```bash
# Clarify a vague phrase into 2-4 candidate directions
python3 scripts/yotta_prompt.py clarify "help me write an email"

# JSON output for programmatic consumption
python3 scripts/yotta_prompt.py clarify "remember this" --json

# Limit the number of candidates
python3 scripts/yotta_prompt.py clarify "how do I learn python" --top 3

# Map a direction / skill name to YottaMeta skills, install commands and a runnable prompt
python3 scripts/yotta_prompt.py map writing
python3 scripts/yotta_prompt.py map yotta-humanize --json

# Built-in scenario cases
python3 scripts/yotta_prompt.py scenarios
```

Exit codes: **0** = success; **1** = not recognized (guidance printed); **4** = usage or read error.

Sample text output:

```
元引 yotta-prompt —— 意图澄清
输入：「帮我写一封邮件」

我猜你想做这几件事（回复数字选择，或直接说出你的选择）：

1. 写作与语言（writing）
   · 命中关键词：邮件
   · 可串联：元真 yotta-humanize
2. 通用与入门（general）
   · 还没想清楚，先从通用引导开始
```

## Installation

Pick any of the four methods below; the order is the recommended priority. Skill files always come from **npm** (GitHub can be slow without a proxy; npm supports mirrors).

### Method 1: npm one-liner (recommended)

```text
# Optional China mirror: npm config set registry https://registry.npmmirror.com
npx -y @yottameta/yotta-prompt --agent <agent-name>      # install to the agent's default user-level skills dir
npx -y @yottameta/yotta-prompt --dir <your-skills-dir>   # point to the skills dir itself (e.g. ~/.codex/skills)
```

- `--agent <name>` installs to that agent's default user-level directory; `--list` shows each agent's default directory.
- `--dir <path>` installs to the given directory; for agents not in the preset list, point `--dir` at their skills directory.
- If the mirror has not synced the new package (404): add `--registry=https://registry.npmjs.org/` (a proxy may be needed in China), or wait for the mirror cache.

### Method 2: git clone (developers / git available)

```text
git clone https://github.com/YottaMeta/yotta-prompt.git <your-skills-dir>/yotta-prompt
```

### Method 3: GitHub Download ZIP (manual / no git)

On the GitHub repository `YottaMeta/yotta-prompt`, click **Code → Download ZIP**, unzip it and put the `yotta-prompt` folder into the agent's skills directory.

### Method 4: install.sh (multi-agent one-liner script)

```text
bash install.sh --agent <name>   # install to the agent's default user-level directory
bash install.sh --dir <path>     # install to the given directory
bash install.sh --list           # list agents -> default directories
```

> Method 1 uses the npm registry (npmmirror / npmjs) and does not depend on GitHub; Methods 2/3 use GitHub and may fail without a proxy in China.
## Development & validation

The package ships its own test script (included in the published package):

```bash
# Run the full suite (41 cases) from the skill directory
python scripts/test_yotta_prompt.py
```

The scenario walkthroughs live in `references/scenarios.md`.

## References

- references/faq.md

## License

MIT © YottaMeta — see [LICENSE](./LICENSE).
