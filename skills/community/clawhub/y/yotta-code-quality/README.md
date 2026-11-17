<p align="center"><b>Language</b>: English · <a href="./README.zh-CN.md">中文</a></p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-code-quality banner" width="100%" />
</p>

<h1 align="center">yotta-code-quality · 元质 (Yuanzhi)</h1>

<p align="center">A pair-style code review skill for <b>Cursor / Codex / Claude Code / generic agents</b>. It turns "code quality review" into a reusable, configurable, methodology-backed skill: before delivery, the agent reads the code like a senior engineer, locates decay, and proposes evidence-based fixes.</p>

<p align="center">One-line positioning: <b>diagnose first, fix second — report only, never touch the code.</b></p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-code-quality"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-code-quality" /></a>
  <a href="https://github.com/YottaMeta/yotta-code-quality"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-code-quality" /></a>
  <a href="https://github.com/YottaMeta/yotta-code-quality/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/yotta-code-quality" /></a>
  <a href="https://github.com/YottaMeta/yotta-code-quality"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen" /></a>
</p>

## Core value

- **Evidence-based, not gut feeling.** The methodology is distilled from 12 classic software-engineering books (Fowler's *Refactoring*, McConnell's *Code Complete*, Ousterhout's *A Philosophy of Software Design*, Evans's *Domain-Driven Design*, and more); every finding anchors to a concrete book principle or code smell.
- **Iron Law against noise.** Every finding must follow `Symptom → Source → Consequence → Remedy`; findings missing "Consequence" or "Remedy" are treated as noise and not reported.
- **Read-only by default, diagnose before fix.** Reports only, no code changes; unless you explicitly ask for `--fix` (apply Remedy).
- **Trackable Health Score.** Each review produces a 0–100 point-deduction index (deliberately defined as a *per-review deduction index*, not an absolute rating) supporting cross-review trend comparison.
- **On-demand loading, not bloated.** By mode (Quick / PR / architecture / tests / release) only the needed reference files are read, keeping the full methodology out of context.
- **Cross-agent + zero dependency.** A pure file-based skill, usable in Cursor / Codex / Claude Code / generic agents; no runtime dependencies.

## Why use it

| Dimension | yotta-code-quality | Note |
|---|---|---|
| Methodology | 12 classic SE books + smells | Every finding traceable, not empirical talk |
| Finding structure | Iron Law four-part | Forces "consequence + remedy", avoids useless griping |
| Scoring | Per-review deduction index (0–100) | Explicitly "not an absolute rating", resists misreading, supports trends |
| Coverage | R1–R6 + T1–T6 + R7 + UX1 | Production, tests, release/supply-chain, first-paint UX |
| Config | `.code-quality.yaml` | Enable/disable/degrade/ignore/focus per risk, adapts to the project |
| Trigger | Conversational | "结对评审" / "发版前扫一眼" also hit |
| Extras | AGENTS-template / hooks.json | Optional; not required for the review core |

## Workflow (protocol in brief)

### Iron Law (non-negotiable)

```
NEVER suggest fixes before completing risk diagnosis.
EVERY finding must follow: Symptom → Source → Consequence → Remedy.
Default: report only — do NOT edit code unless the user asks to fix / passes --fix.
```

### Session contract

1. **Read-only by default** — report only, no opportunistic refactors.
2. **Scope discipline** — stay within the files / diff / "knife" the user names.
3. **Health Score is not a rating** — it is a *per-review deduction index*, not an objective score of the codebase.
4. **Language** — the report uses the user's language; Iron Law field names, book titles, smell names and fixed table headers (`Findings` / `Summary` / `Critical` / `Warning` / `Suggestion`) stay in English.

### On-demand loading (mode routing)

| Mode | When | Read first | Read if needed |
|---|---|---|---|
| **Quick** | pasted function / < 50-line diff / quick look | `SKILL.md` + cheat sheet | `decay-risks.md` |
| **PR review** | PR / branch diff / ready to merge | `common.md` + `pr-review-guide.md` | `decay-risks.md` / `test-decay-risks.md` / `examples.md` |
| **Architecture / tech debt** | whole module / audit / `--full` | `common.md` + `decay-risks.md` + `source-coverage.md` | `editorial-extensions.md` |
| **Test quality** | tests / coverage / flaky | `common.md` + `test-decay-risks.md` | `examples.md` |
| **Release / publishing** | pre-release / updater / CSP / secrets | `common.md` + `editorial-extensions.md` | R1–R6 tables |

### Health Score

Base 100, deducted by `strictness`, floor 0. **Every finding is still reported**; the score is only a trend reference.

| Preset | Critical | Warning | Suggestion |
|---|---|---|---|
| `strict` | −20 | −8 | −2 |
| `balanced` (default) | −15 | −5 | −1 |
| `legacy-friendly` | −8 | −3 | −1 |

### Config (`.code-quality.yaml`)

Read from the repo root before review (single source of truth lives in references/common.md):

```yaml
strictness: balanced
disable: []
severity: {}
ignore:
  - "**/*.generated.*"
  - "**/node_modules/**"
suppress: []
history: false
```

### Optional flags

- `--fix` / "apply Remedy" → fix mode (minimal changes per Remedy, then re-review those findings)
- `--triage` / "handle one by one" → interactive ignore / defer (written to `suppress`)
- `.code-quality.yaml` with `history: true` → generates `.code-quality-history.json` trend records

> The optional extras `AGENTS-template.md` and `hooks.json` do not affect review when not installed.

## Risk matrix (canonical)

| Code | Name | Diagnosis focus |
|---|---|---|
| R1 | Cognitive Overload | How much brainpower does this code take to read |
| R2 | Change Propagation | How many unrelated places break when one thing changes |
| R3 | Knowledge Duplication | Is the same decision scattered across places |
| R4 | Accidental Complexity | Is it more complex than the problem itself |
| R5 | Dependency Disorder | Is the dependency direction consistent |
| R6 | Domain Model Distortion | Does it stay faithful to the domain language |
| T1 | Test Obscurity | Is it clear what is being verified |
| T2 | Test Brittleness | Broken by behavior-equivalent refactors |
| T3 | Test Duplication | Same scenario repeated without added value |
| T4 | Mock Abuse | Is the test more complex than the behavior |
| T5 | Coverage Illusion | Does the suite really protect the points that break |
| T6 | Architecture Mismatch | Does the suite shape match the risk profile |
| R7 | Release / supply-chain security | Plaintext secrets, updaters skipping verification, shipping with DevTools |
| UX1 | First-paint / state clarity | Blank windows, non-centered splash, state copy mismatching the gate |

> Detailed symptoms, book sources, severities and the "no-false-positive list" live in references/decay-risks.md, references/test-decay-risks.md and references/editorial-extensions.md. `anti-over-flag` suppresses noise warnings before reporting R1 etc., to avoid "crying wolf" fatigue.

## Directory structure

```
yotta-code-quality/
├── SKILL.md                  # entry + per-mode on-demand loading router
├── references/
│   ├── common.md             # config / templates / scoring (single source of truth)
│   ├── decay-risks.md        # R1–R6 production risks
│   ├── test-decay-risks.md   # T1–T6 test risks
│   ├── editorial-extensions.md # R7 / UX1 / anti-over-flagging
│   ├── source-coverage.md    # book matrix (deep mode)
│   ├── pr-review-guide.md    # 7-step PR review
│   ├── examples.md           # tone / scoring calibration
│   ├── AGENTS-template.md    # optional: drop into a repo as AGENTS.md
│   └── hooks.json            # optional: PreToolUse hooks for rm -rf / git push --force
├── bin/install.js            # npx cross-platform installer
├── install.sh                # one-shot install to 17 agent families
├── assets/banner.png         # brand banner
└── LICENSE                   # MIT
```

## Install

Pick any of the four methods below; the order is the recommended priority. Skill files always come from **npm** (GitHub can be slow without a proxy; npm supports mirrors).

### Method 1: npm one-liner (recommended)

```text
# Optional China mirror: npm config set registry https://registry.npmmirror.com
npx -y @yottameta/yotta-code-quality --agent <agent-name>      # install to the agent's default user-level skills dir
npx -y @yottameta/yotta-code-quality --dir <your-skills-dir>   # point to the skills dir itself (e.g. ~/.codex/skills)
```

- `--agent <name>` installs to that agent's default user-level directory; `--list` shows each agent's default directory.
- `--dir <path>` installs to the given directory; for agents not in the preset list, point `--dir` at their skills directory.
- If the mirror has not synced the new package (404): add `--registry=https://registry.npmjs.org/` (a proxy may be needed in China), or wait for the mirror cache.

### Method 2: git clone (developers / git available)

```text
git clone https://github.com/YottaMeta/yotta-code-quality.git <your-skills-dir>/yotta-code-quality
```

### Method 3: GitHub Download ZIP (manual / no git)

On the GitHub repository `YottaMeta/yotta-code-quality`, click **Code → Download ZIP**, unzip it and put the `yotta-code-quality` folder into the agent's skills directory.

### Method 4: install.sh (multi-agent one-liner script)

```text
bash install.sh --agent <name>   # install to the agent's default user-level directory
bash install.sh --dir <path>     # install to the given directory
bash install.sh --list           # list agents -> default directories
```

> Method 1 uses the npm registry (npmmirror / npmjs) and does not depend on GitHub; Methods 2/3 use GitHub and may fail without a proxy in China.
## Usage

Say "review this PR", "结对评审" or "发版前扫一眼" in conversation, or call `/yotta-code-quality` directly. Optional flags are listed above.

### Example: Quick review (pasted function)

```
User: 帮我看看这段函数有没有问题 / 结对评审
Agent: Quick mode → read SKILL + cheat sheet → output Findings + Health Score
```

### Example: PR review (7-step flow)

```
User: review this PR / ready to merge?
Agent: PR mode → .code-quality.yaml config → auto scope → 7 steps in pr-review-guide.md
       → output Findings (Critical/Warning/Suggestion sorted) + fix-order suggestion
```

### Example: wire into a project and configure

```bash
# 1. Put a .code-quality.yaml at the repo root (optional)
# 2. Trigger a review in conversation, or use --dir to install the skill into the target agent
```

## Upgrade / uninstall

- **Upgrade**: reinstall the latest version to overwrite — rerun the install command you used (e.g. `npx -y @yottameta/yotta-code-quality --agent <name>` or `bash install.sh --agent <name>`). Old files in the skill directory are replaced; other project files are untouched.
- **Uninstall**: delete the `yotta-code-quality/` folder under the target agent's skills directory.
- **No side effects**: the skill writes nothing outside the project; the optional trend file (`.code-quality-history.json`) is only generated when you enable `history: true`, at the repo root.

## FAQ

- **How is this different from generic code review or a linter?** Generic tools are mostly rule/style based; this skill provides "methodology grounding + Iron Law four-part + per-review deduction index", focusing on systemic decay (complexity, propagation, duplication, dependencies, domain modeling, test and release safety) rather than style nitpicking.
- **Does the Health Score judge code quality with a "grade"?** No. It is a *per-review deduction index*, explicitly not an absolute rating, used for cross-review trend comparison.
- **Will it change my code directly?** Report only by default; only with `--fix` / "apply Remedy" does it edit, and then in the smallest behavior-equivalent way.
- **Want to review only some risk classes?** Use `disable` / `focus` / `severity` in `.code-quality.yaml`.
- **Is `.agents/skills` universal?** No. Claude Code and Codex do not read it by default; use --dir when unsure.
- **Does it need network or dependencies?** No. It is a zero-dependency pure file skill; running only relies on the host agent's file-reading ability.

## Source & license

- **Methodology** distilled from 12 classic software-engineering books and open-source community quality-review practice (MIT). The original methodology copyright belongs to hyhmrright; this skill rewrites it into a single self-contained, cross-agent version, adding R7 / UX1 / the on-demand-loading session contract.
- **License:** MIT — see `LICENSE` (copyright: hyhmrright (original methodology) + YottaMeta (this packaging)).

## Changelog

See [CHANGELOG.md](./CHANGELOG.md).

## 参考文档

- 常见问题：`references/faq.md`
- 复杂场景走查：`references/walkthroughs.md`

## License

[MIT](./LICENSE) © hyhmrright (original methodology) + YottaMeta (this packaging). "Yuanzhi" / "yotta-code-quality" and the YottaMeta family names (yotta-* prefix) are YottaMeta brand identifiers; derived works must not reuse them, see [NOTICE](./NOTICE).
