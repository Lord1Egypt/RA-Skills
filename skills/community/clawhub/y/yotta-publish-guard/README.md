<p align="center"><b>Language</b>: English · <a href="./README.zh-CN.md">中文</a></p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-publish-guard banner" width="100%" />
</p>

<h1 align="center">yotta-publish-guard · 元守 (YuanShou)</h1>

<p align="center">A <b>generic pre-publish release guard</b> (defaults to the YottaMeta family, customizable to any publishing organization): it folds the release standard and every pitfall already hit into one deterministic CLI — <code>check</code> (aggregated validation, full / github / self modes) · <code>pack</code> (npm pack dry-run) · <code>versions</code> (five-way version alignment) · <code>names</code> (three-channel name availability) · <code>publish</code> (command wrapper with a push gate). <b>Zero dependencies (Python 3.8+ standard library)</b>; Windows + Linux + macOS.</p>
<p align="center">Triggers when publishing a skill, after editing before pushing to GitHub / npm / ClawHub, or when checking versions or name availability in batch; or says 元守 / 发布守门 / 发布前检查 / publish-guard / 推前检查 / 查重 / 版本对齐. Defaults to YottaMeta ownership and can be customized for any organization; the skill never holds or reads platform credentials — authentication is done by each platform CLI using the user's local config.</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-publish-guard"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-publish-guard" /></a>
  <a href="https://github.com/YottaMeta/yotta-publish-guard"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-publish-guard" /></a>
  <a href="https://github.com/YottaMeta/yotta-publish-guard/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/yotta-publish-guard" /></a>
  <a href="https://github.com/YottaMeta/yotta-publish-guard"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen" /></a>
</p>

## What it is

Publishing a skill across GitHub / npm / ClawHub touches a dozen checkpoints: release-standard validation, version alignment across four files, npm pack without pyc, name availability on three channels, git proxy flags, ClawHub quoting, gh --description. YuanShou makes the whole "is it ready to publish?" question one command, and wraps the actual publish steps behind a push gate that blocks by default. It validates against your own publishing ownership (npm scope / GitHub org / ClawHub owner / topic), defaulting to YottaMeta for out-of-the-box use.</p>

## Custom ownership

Validation, name checks, and generated publish commands all follow the configured ownership (npm scope / GitHub org / ClawHub owner / GitHub topic). YottaMeta values are the defaults; other organizations point it at their own ownership via CLI flags or environment variables — the AI using this skill guides the setup. No platform credentials are held or read by this skill; npm / gh / clawhub authenticate with the user's local configuration.

## Commands

```bash
# 1) Pre-publish readiness check (full mode; optional audit / vetter / verify verdicts)
python3 scripts/yotta_publish_guard.py check ./yotta-my-tool
python3 scripts/yotta_publish_guard.py check ./yotta-my-tool --with-audit --with-vetter --with-verify
python3 scripts/yotta_publish_guard.py check ./yotta-private --self-use

# 2) Package check / version alignment / three-channel name availability
python3 scripts/yotta_publish_guard.py pack ./yotta-my-tool
python3 scripts/yotta_publish_guard.py versions ./yotta-my-tool
python3 scripts/yotta_publish_guard.py names ./yotta-my-tool

# 3) Publish command wrapper (dry-run by default; --exec to run; --force bypasses the gate)
python3 scripts/yotta_publish_guard.py publish ./yotta-my-tool
python3 scripts/yotta_publish_guard.py publish ./yotta-my-tool --github-only
python3 scripts/yotta_publish_guard.py publish ./yotta-my-tool --channels github,npm --exec
```

## Three check modes

- **Host hook declaration** — `skill-manifest.json` declares `before_publish` / `publish_gate`; with the wrapper registered a failed gate blocks, without it the result is visibly marked `explicit-unverified`.

| Mode | How | Requires |
|---|---|---|
| full | `check` default / `publish` all channels | SKILL.md + LICENSE + bilingual four-way-install README + package.json + CHANGELOG (recommended) + five-way version alignment + no placeholders + balanced fences |
| github | `publish --github-only` | SKILL.md + LICENSE + README.md (English); npm artifacts not required |
| self | `check --self-use` | skill body only: SKILL.md + frontmatter + no placeholders + balanced fences |

## Sub-commands at a glance

- **check** — built-in validation (three modes) + optional aggregated verdicts from yotta-security-audit / yotta-vetter / yotta-verify (auto-degrades when not installed).
- **pack** — `npm pack --dry-run`: no pyc / __pycache__ in the tarball, key files (SKILL / LICENSE / bilingual README) present; local fallback when npm is unavailable.
- **versions** — align package.json / SKILL.md / CHANGELOG top / CLI `VERSION` constant.
- **names** — npm view / gh repo view / clawhub search three-channel availability; degrades to manual-check hints when the network fails.
- **publish** — generates the command plan (git init/add/commit → gh repo create --description + topic yottaskills → npm publish → clawhub publish), dry-run by default, `--exec` executes in order, `--force` explicitly bypasses the push gate. The clawhub command defaults to `--owner yottameta` (the org handle) — override with `--clawhub-owner` so a publish can never land on a personal account.

## Channels (optional)

`publish --channels github,npm,clawhub` (default: all) or `--github-only` — npm and ClawHub are not mandatory; the gate switches to the github mode for GitHub-only pushes.

## Push gate

`publish` runs built-in validation first: ERROR blocks by default (exit code 2); `--force` is only available after explicit authorization.

## Exit codes

| Command | 0 | 1 | 2 | Other |
|---|---|---|---|---|
| check | READY | READY (with WARN suggestions) | BLOCKED | 4 fatal |
| pack | PASS | — | pyc or missing key file in tarball | 4 fatal |
| versions | PASS | — | missing / mismatched | 4 fatal |
| names | all three free | a channel could not be confirmed (manual check) | taken | 4 fatal |
| publish | dry-run or executed OK | — | gate blocked / bad channel args | failing command's exit code; 4 fatal |

## Behavioral anchors

1. **Push gate blocks by default**: nothing publishes without passing validation; `--force` only after explicit authorization.
2. **Network commands degrade gracefully**: when npm / gh / clawhub are unavailable it prints manual-check hints instead of fabricating results.
3. **Read-only**: it never modifies the skill directory under test (except npm pack temporary artifacts); git init / commit only run under `--exec`.
4. **Platform-aware**: Windows runs .cmd/.bat subprocesses via cmd.exe; npm commands use a writable --cache directory.

## Division of labor with the workshop toolchain

| Skill | Role |
|---|---|
| 元守 yotta-publish-guard (this skill) | **Guard**: pre-publish validation + publish command wrapper |
| 元造 yotta-skill-creator | **Create**: compliant scaffold (元守's check is READY directly on 元造 scaffolds) |

Recommended flow: **元造 create → develop → 元守 check → pack → versions → names → publish**.

References: `references/tutorial.md` (Chinese tutorial), `references/check-items.md` (validation item details), `references/publish-flow.md` (three-source release flow + pitfall list).

## Installation

Pick any of the four methods below; the order is the recommended priority. Skill files always come from **npm** (GitHub can be slow without a proxy; npm supports mirrors).

### Method 1: npm one-liner (recommended)

```text
# Optional China mirror: npm config set registry https://registry.npmmirror.com
npx -y @yottameta/yotta-publish-guard --agent <agent-name>      # install to the agent's default user-level skills dir
npx -y @yottameta/yotta-publish-guard --dir <your-skills-dir>   # point to the skills dir itself (e.g. ~/.codex/skills)
```

- `--agent <name>` installs to that agent's default user-level directory; `--list` shows each agent's default directory.
- `--dir <path>` installs to the given directory; for agents not in the preset list, point `--dir` at their skills directory.
- If the mirror has not synced the new package (404): add `--registry=https://registry.npmjs.org/` (a proxy may be needed in China), or wait for the mirror cache.

### Method 2: git clone (developers / git available)

```text
git clone https://github.com/YottaMeta/yotta-publish-guard.git <your-skills-dir>/yotta-publish-guard
```

### Method 3: GitHub Download ZIP (manual / no git)

On the GitHub repository `YottaMeta/yotta-publish-guard`, click **Code → Download ZIP**, unzip it and put the `yotta-publish-guard` folder into the agent's skills directory.

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
# Run the full suite (36 cases) from the skill directory
python scripts/test_yotta_publish_guard.py
```

## License

MIT © YottaMeta — see [LICENSE](./LICENSE).
