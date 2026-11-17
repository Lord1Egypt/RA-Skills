<p align="center"><b>Language</b>: English · <a href="./README.zh-CN.md">中文</a></p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-vetter banner" width="100%" />
</p>

<h1 align="center">yotta-vetter · 元审 (Yuanshen)</h1>

<p align="center">The "security review protocol" before installing any skill: <b>a four-phase checklist (source → code → permissions → risk) + a lightweight checker</b>, with deep-scan handoff to Yuan'an (yotta-security-audit). Use it whenever you fetch a skill from a marketplace, GitHub or any source and want to review it before installation.</p>
<p align="center">Activates before installing / evaluating any skill, when fetching a skill from a marketplace or GitHub, when reviewing a skill shared by someone else, or in any "about to install unknown code" scenario; also on 审查 / 审查技能 / vetting / 技能安全审查 / 检查技能 — <b>judged by whether unknown code is about to be installed, not keyword luck</b>.</p>
<p align="center">Python 3.8+ standard library, zero dependency; Windows + Linux; review and report only — the final decision requires human confirmation.</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-vetter"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-vetter" /></a>
  <a href="https://github.com/YottaMeta/yotta-vetter"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-vetter" /></a>
  <a href="https://github.com/YottaMeta/yotta-vetter/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/yotta-vetter" /></a>
  <a href="https://github.com/YottaMeta/yotta-vetter"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen" /></a>
</p>

## What it is

"Should I install this skill?" deserves a structured, traceable decision basis rather than a gut feeling. Yuanshen turns pre-install review into a four-phase checklist (source → code → permissions → risk) and uses a lightweight checker to scan for dangerous patterns and output a SKILL VETTING REPORT. It is not tied to any single platform: an agent-agnostic review protocol that works in any agent supporting Agent Skills — initial review and report only, never a substitute for the final decision.

## Core value

- **check** — four-phase initial review (source / code / permissions / risk) outputting a SKILL VETTING REPORT (verdict / decision record / timestamp / reviewer).
- **source** — semi-automated GitHub repo source check (stars / last updated / license) with a local cache; gracefully degrades offline.
- **Shared rules** — dangerous-pattern rules are shared with Yuan'an (scripts/vetter_rules.py is a synced copy of audit_rules.py).
- **Yuan'an handoff** — when the initial review finds high-and-above findings, it prints a one-line command guiding a Yuan'an deep scan.
- **Graded verdicts** — critical=DO NOT INSTALL; high=INSTALL WITH CAUTION; medium=REVIEW REQUIRED; low/info=SAFE TO INSTALL.

## Why use it

| Advantage | Description |
|---|---|
| **Four-phase structured** | source → code → permissions → risk, checked ring by ring, none skippable |
| **Traceable verdicts** | The report carries verdict / decision record / timestamp / reviewer — auditable |
| **Rules shared with Yuan'an** | vetter_rules.py is a synced copy of audit_rules.py; consistent criteria |
| **Semi-automated source** | source checks stars / last-updated / license with a local cache; degrades gracefully offline |
| **Deep-scan handoff** | high-and-above automatically guides you into yotta-security-audit |
| **Zero dependency** | Python 3.8+ standard library; no daemon / database; Windows + Linux |
| **Ecosystem distribution** | GitHub + npm synced; four install methods (npx / git clone / Download ZIP / install.sh) |

## Commands / four-phase review protocol

| Phase | Checkpoint | Command / reference |
|---|---|---|
| 1. Source | Source platform, author reputation, stars / last-updated, license | source github:owner/repo; references/checklist.md |
| 2. Code | SKILL.md integrity, script inventory, dangerous-pattern rule scan | check <path> |
| 3. Permissions | Executable bits, world-writable, symlinks, read/write/network scope | check <path> |
| 4. Risk | Risk-level verdict + conclusion + decision record | Verdict / decision-record sections of the report |

## Verdict matrix

| Risk level | Verdict | Action |
|---|---|---|
| critical | DO NOT INSTALL | Refuse installation and review manually |
| high | INSTALL WITH CAUTION | Decide after manual review |
| medium | REVIEW REQUIRED | Install after review |
| low/info | SAFE TO INSTALL | Still recommended to run the full protocol |

## Usage examples

```bash
# Initial review of a skill directory
python3 scripts/yotta_vetter.py check ./some-skill

# JSON output + generate a report file
python3 scripts/yotta_vetter.py check ./some-skill --json --report report.md

# Report only high and above
python3 scripts/yotta_vetter.py check ./some-skill --severity high

# Semi-automated source check (local cache; degrades gracefully offline)
python3 scripts/yotta_vetter.py source github:YottaMeta/yotta-memory
```

**Exit codes**: **0** = clean / low only; **1** = medium; **2** = high; **3** = critical; **4** = error.

## Division of labor with Yuan'an

- **Yuanshen** = initial review: fast and light — four-phase checklist + rule scan + source check.
- **Yuan'an** = deep scan: 13 detector classes + system security baseline.
- When Yuanshen finds high-and-above → it prints a command guiding a Yuan'an deep scan.

## Install

Pick any of the four methods below; the order is the recommended priority. Skill files always come from **npm** (GitHub can be slow without a proxy; npm supports mirrors).

### Method 1: npm one-liner (recommended)

```text
# Optional China mirror: npm config set registry https://registry.npmmirror.com
npx -y @yottameta/yotta-vetter --agent <agent-name>      # install to the agent's default user-level skills dir
npx -y @yottameta/yotta-vetter --dir <your-skills-dir>   # point to the skills dir itself (e.g. ~/.codex/skills)
```

- `--agent <name>` installs to that agent's default user-level directory; `--list` shows each agent's default directory.
- `--dir <path>` installs to the given directory; for agents not in the preset list, point `--dir` at their skills directory.
- If the mirror has not synced the new package (404): add `--registry=https://registry.npmjs.org/` (a proxy may be needed in China), or wait for the mirror cache.

### Method 2: git clone (developers / git available)

```text
git clone https://github.com/YottaMeta/yotta-vetter.git <your-skills-dir>/yotta-vetter
```

### Method 3: GitHub Download ZIP (manual / no git)

On the GitHub repository `YottaMeta/yotta-vetter`, click **Code → Download ZIP**, unzip it and put the `yotta-vetter` folder into the agent's skills directory.

### Method 4: install.sh (multi-agent one-liner script)

```text
bash install.sh --agent <name>   # install to the agent's default user-level directory
bash install.sh --dir <path>     # install to the given directory
bash install.sh --list           # list agents -> default directories
```

> Method 1 uses the npm registry (npmmirror / npmjs) and does not depend on GitHub; Methods 2/3 use GitHub and may fail without a proxy in China.
## Upgrade / uninstall

- **Upgrade**: reinstall the latest version to overwrite — rerun the install command you used (e.g. `npx -y @yottameta/yotta-vetter --agent <name>` or `bash install.sh --agent <name>`). Old files in the skill directory are replaced; other project files are untouched.
- **Uninstall**: delete the yotta-vetter folder under the target agent's skills directory (see the table above). The skill stops taking effect after removal.

## FAQ

- **Can Yuanshen decide for me?** No. The checker only does the initial review and report; the final verdict must be confirmed by a human.
- **What if high risk is found?** The report prints a guiding command to run Yuan'an (yotta-security-audit) for a deep scan; isolate or stop using the skill first, then review manually.
- **Does it work offline?** Yes. The GitHub API check in source degrades gracefully without network; check runs fully locally.
- **Will scanning itself false-positive?** Yuanshen's own source check uses the standard-library urllib to hit the GitHub API, so self-scan hits a network-call hint (medium) — expected behavior, not a risk.

## Related skills

Part of the YottaMeta skill matrix (security family): [yotta-security-audit](https://github.com/YottaMeta/yotta-security-audit) (Yuan'an, 13 detector classes + system security baseline) does the deep scan while Yuanshen does the pre-install review — high-and-above findings guide you into Yuan'an; [yotta-memory](https://github.com/YottaMeta/yotta-memory) (Yuanyi) handles cross-session long-term memory.

## Boundaries

- **Initial review & report only** — the checker never replaces the final decision; human confirmation is always required.
- **Authorized targets only** — source checks hit public GitHub metadata for explicitly named repos; no unauthorized scanning of others' systems.
- **Offline-capable** — everything except the GitHub source check works fully offline; that check degrades gracefully.

## Development & validation

- Run at the project root: python tools/validate-skill.py yotta-vetter
- Tests: python scripts/test_yotta_vetter.py (Windows: python)
- Details: references/checklist.md, references/vetting-report-template.md

Keep tests green and bump the version before releasing changes.

## Changelog

See [CHANGELOG.md](./CHANGELOG.md).

## License

[MIT](./LICENSE) © YottaMeta. "Yuanshen" / "yotta-vetter" and the YottaMeta family names (yotta-* prefix) are YottaMeta brand identifiers; derived works must not reuse them, see [NOTICE](./NOTICE). YottaMeta original implementation (zero-dependency, self-developed).
