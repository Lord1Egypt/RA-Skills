# Changelog

All notable changes to `cybernetic-thinking` will be documented in this file.
Versioning follows [Semantic Versioning](https://semver.org/) in `X.Y.Z` format.

---

## [0.6.0] — 2026-08-09

### Added
- **WorkBuddy** to the agent registry (slug `workbuddy`, root `~/.workbuddy` / project `.workbuddy`) — skills live at `~/.workbuddy/skills/`
- **Trae** to the agent registry (slug `trae`) with **two candidate roots**: `~/.trae` (international) and `~/.trae-cn` (China / **Trae Work** — Trae IDE and Trae Work share this global skills dir, so one entry covers both)
- **Agent Skills standard / user-level `.agents`** entry (slug `agents`, root `.agents`) — the cross-agent `~/.agents/skills/` location read by Trae, Kilo, Claude and other Agent-Skills-compliant agents; this is the user-level shared folder for custom installs (`-a agents` or `Customize...`)
- Multi-root agent detection: each agent may declare several candidate roots; the first existing root wins for detection, and install targets an existing root when present (robust against version/variant drift)
- **`--copy` flag** (and `-c`) plus an automatic copy fallback: when junction creation fails (locked-down / non-admin Windows, or agents that don't resolve junctions at runtime), the installer copies the skill files instead of failing. `--copy` forces a copy unconditionally. `--count` prints the agent count and exits

### Changed
- **Agent registry refactored** to support multiple roots per agent. `Kilo` now also detects `~/.kilocode` (legacy) alongside `~/.kilo`. `detectAll()` / `installRoots()` rewritten accordingly
- Both `README.md` and `README_CN.md` — skill directory tables extended with WorkBuddy, Trae (incl. Trae Work / `.trae-cn`), and the Agent Skills standard / user-level `.agents` folder; agent count now 12
- `package.json` keywords extended with `workbuddy`, `trae`, `trae-cn`, `agent-skills`, `kilocode` for discoverability

### Fixed
- **GitHub Copilot false-positive detection**. The `copilot` agent used `roots: ['.github']`, which resolves to a global check of `~/.github`. That folder exists on any machine that has installed git, GitHub Desktop, or the `gh` CLI — so Copilot was wrongly "detected" everywhere. It now uses `~/.copilot` (the real Copilot CLI user-level skills dir at `~/.copilot/skills/`), which only the Copilot CLI creates. Project-level `.github/skills/` is still documented as a valid location the CLI reads, but is no longer used for global detection

### Notes
- The `--path <dir>` flag remains the recommended way to install for any agent not on the built-in list
- Windows installs use a `junction` symlink (no admin needed); on link failure the installer automatically copies the files, and `--copy` forces a copy
- `evals/checks.json` now has a MUST item `installer-readme-sync`; `init.ps1` additionally verifies at runtime that the installer agent count matches the README EN/CN directory-table row counts (no drift allowed)

---

## [0.5.0] — 2026-08-05

### Added
- `@clack/prompts` (`^0.9.1`) as a runtime dependency — the installer now uses a proper TUI instead of raw `readline`
- **Gemini CLI** to the agent registry (slug `gemini`, root `~/.gemini`)
- **skills.sh discoverability**: `author` (`ShrimpLeon`) and `tags` (`control-theory`, `cybernetics`, `thinking-mode`, `ai-agent`, `coding-agent`, `debugging`) fields added to `SKILL.md` frontmatter; `skills-sh` keyword added to `package.json`. Closes out the previously-stubbed feat-013 (0.4.1) that was marked done but never actually shipped

### Changed
- **`scripts/install.js` rewritten end-to-end** with `@clack/prompts`, mirroring the `npx impeccable skills install` UX:
  1. `◇ Detected agents` — scans and lists detected agents with resolved paths
  2. `◆ Detected only / Customize` — single-select; `Customize...` opens a `multiselect` (space to toggle)
  3. `◆ Install location` — `Project (cwd)` or `Global (~)`
  4. Link the skill into each selected agent's `skills/` directory (junction on Windows, symlink elsewhere)
  5. `◇ Done!` outro with `installed / skipped / failed` summary
- **Unified agent registry layout**: every agent now detects at `~/.<root>` (global) or `./.<root>` (project) and installs at `~/.<root>/skills/<skillName>` (or project). Replaces the previous per-agent custom paths (e.g. `~/.claude/plugins/custom-skills/`, `~/.config/kilo/skills/`)
- Agent slugs simplified: `claude` (was `claude-code`), `codex` (was `openai-codex`), `copilot` (was `github-copilot`, root `.github`). `kilo`, `aider`, `cursor`, `windsurf`, `zed` unchanged
- Non-TTY / CI / piped-stdin path auto-skips the TUI and installs for all detected agents at global scope
- Both `README.md` and `README_CN.md` — install section rewritten with the new clack TUI example session, updated agent directory table (now 9 agents), and slug examples (`-a claude,codex`)

### Fixed
- **`install` subcommand crash**: the previous arg parser treated the `install` positional as an unknown option and exited with `Unknown option: install`. The new parser accepts `install` (or no subcommand) explicitly; unknown subcommands now get a clear error
- `--agents` / `--path` / `--yes` / `--force` / `--global` / `--local` flags all preserved for scripting and CI

### Notes
- The interactive TUI requires a TTY; in CI it degrades gracefully to non-interactive install
- Windows symlinks use `junction` (no admin rights needed for directory junctions); real symlinks may still require Developer Mode or admin on some setups

---

## [0.4.0] — 2026-07-30

### Changed
- **Renamed** the skill from `systems-thinking` to `cybernetic-thinking` across the entire project. Rationale: `systems-thinking` collided with many existing published skills; `cybernetic-thinking` is distinctive and accurately names the discipline (both source books are cybernetics classics — Engineering Cybernetics + Cybernetics and Scientific Methodology).
- `package.json` `name`: `skill-systems-thinking` → `skill-cybernetic-thinking`
- `package.json` `bin`, `repository.url`, `homepage` updated to the new name
- `SKILL.md` frontmatter `name` and `slug` updated
- `evals/checks.json` `skill` field updated
- Both `README.md` and `README_CN.md` — all `npx` / `npm install` / `git clone` commands updated; added a rename notice for existing users
- `scripts/install.js` header comment updated
- `init.ps1` header comment updated

### Notes
- **npm**: the old package `skill-systems-thinking` cannot be renamed on npm; it will be marked as `deprecated` pointing to the new name. Users must install `skill-cybernetic-thinking` instead.
- **Repo**: GitHub and Gitee repository renamed from `systems-thinking` to `cybernetic-thinking` (old URLs auto-redirect).
- **Existing users**: remove the old skill directory (e.g. `rm -rf ~/.config/kilo/skills/skill-systems-thinking`) and reinstall with the new `npx` command.

---

## [0.3.1] — 2026-07-30

### Added
- Integrated a second source book: 金观涛《控制论与科学方法论》(*Cybernetics and Scientific Methodology*), contributing the epistemological half of the skill (possibility space, black-box recognition, information–control dependence, ultra-stability, bifurcation)
- 4 new reference files:
  - `references/possibility-space.md` — possibility space, conjugate control, feedback amplification
  - `references/black-box-epistemology.md` — black-box recognition, falsifiability, undecidability
  - `references/information-and-control.md` — information–control dependence; build the channel before the actuator
  - `references/system-evolution.md` — stable-state structure, ultra-stability, self-reproduction, bifurcation, catastrophe
- 5 new cognitive laws (total now 13): possibility space naming, missing-channel suspicion, model-as-hypothesis, falsifiability, ultra-stability/bifurcation recognition
- New `MUST`/`SHOULD` checks in `evals/checks.json` (total now 18): `possibility-space-named`, `missing-channel-suspected`, `model-falsifiable`, `ultra-stability-recognized`, `bifurcation-identified`, `threshold-tested`
- New excerpts from Book 2 in `references/original-text.md` (§1.1, §1.6, §1.7–§1.8, §2.4, §3.3, §3.7, §4.2, §5.1, §5.4, §5.6)
- `--path <dir>` flag to install into a custom directory (for agents not on the built-in list)
- Interactive install menu: scan results are listed with `[√]`/`[ ]` markers; user can pick detected / all / select-from-list / abort
- `--yes` / `-y` flag to skip confirmation prompts (implied when not a TTY)

### Changed
- `scripts/install.js` rewritten to mirror `npx impeccable skills install` UX: scan → list → confirm → link. Non-TTY environments fall back to "install for detected agents only" (CI-friendly)
- `SKILL.md` expanded: frontmatter, scope, runtime prompt block (13 laws), workflow, principle map (14 rows) now reference both books
- `references/stability.md` extended with stable-state structure, feedback overshoot, ultra-stability sections
- `references/closed-loop-workflow.md` extended with feedback amplification and convergence-rate dynamics
- `templates/debugging-checklist.md` extended with possibility space, black-box model, falsifiability, ultra-stability checks
- `init.ps1` now checks 4 additional reference files (24 total)
- Both `README.md` and `README_CN.md` rewritten in a more natural, conversational tone; listed both books, 13 laws, 12 references, and the new install UX

### Removed
- AI-sounding marketing phrases from both READMEs (e.g. "这不是给人类做的知识测试", "one-line pitch" blocks)

---

## [0.3.1] — 2026-07-30

### Removed
- `assets/runtime-prompt.txt` — redundant with the runtime prompt block already inlined in `SKILL.md`; the duplicate copy could drift out of sync (this cleanup targets the LLM pain point of "two sources of truth"). Removed the `assets/` directory, the `Source: assets/runtime-prompt.txt` line in `SKILL.md`, the `assets/` entry in `package.json` `files`, and the corresponding check in `init.ps1` (now 23 checks)

---

## [0.2.0] — 2026-07-26

### Added
- `--agents` flag to `scripts/install.js` for selecting specific agents
- `--global`, `--local`, and `--all` scope flags to control install location
- `--help` output to the install CLI

### Changed
- Default install behavior: now scans for actually installed agents (directory exists) instead of installing for all 8 agents
- `--agents` flag creates agent directories when explicitly requested
- No agents detected: prints helpful message listing available agents
- Updated `README.md` and `README_CN.md` Installation sections with new flags and auto-detection description
- Added `npm install` documentation noting it downloads only, plus explains still needing to run `npx skill-systems-thinking install`
- Removed implementation-detail paragraphs from Compatibility sections in both READMEs
- Fixed AI-sounding Chinese phrasing in README_CN.md

---

## [0.1.5] — 2026-07-25

### Changed
- Unified version numbers across documentation files to `0.1.5`
- Split `README.md` into `README.md` (English) and `README_CN.md` (Chinese) for cleaner GitHub reading experience

## [0.1.3] — 2026-07-25

### Added
- XYZ versioning convention documented in `AGENTS.md` (X=major, Y=minor, Z=patch)

### Changed
- Unified version numbers across all project files to `0.1.3`
- README.md and progress.md version tables updated from `0.1.0` to `0.1.3`
- `postinstall` script removed from `package.json` (npx-first approach)

## [0.1.2] — 2026-07-25

### Added
- Gitee download link in README.md (both 中文 and English sections)
- `repository.url` and `homepage` in `package.json` updated to point to Gitee (`gitee.com/leon0903/systems-thinking`)

## [0.1.1] — 2026-07-24

### Changed
- Fixed `repository.url` and `homepage` in `package.json` (replaced `YOUR_USERNAME` placeholder with `ShrimpLeon`)
- Expanded `keywords` from 5 to 14 for better npm search discoverability across AI agents
- Added `homepage` field to `package.json`
- Added `init.ps1` to `files` array in `package.json` so it's included in the npm package
- README.md Installation section restructured: npx one-command install as primary method, GitHub download as alternative
- Added `scripts/install.js` for npx auto-detection of AI agents and automatic symlinking
- Added `bin` field to `package.json` so `npx skill-systems-thinking install` works
- Added agent-specific setup info for 8 agents in README.md
- Added Compatibility section in both 中文 and English
- Removed npm install as a separate method; npx is the recommended approach

## [0.1.0] — 2026-07-24

### Added
- Initial public release of the skill
- SKILL.md with runtime prompt block, 7-step workflow, principle map, and 8 cognitive laws
- README.md with bilingual (中文/English) documentation
- 8 reference files: `state-and-control.md`, `stability.md`, `modeling.md`, `multivariable.md`,
  `disturbance.md`, `bounded-control.md`, `discrete-systems.md`, `closed-loop-workflow.md`
- 2 prompt templates: `debugging-checklist.md`, `change-proposal.md`
- Self-audit checklist: `evals/checks.json` with 11 MUST/SHOULD cognitive-law probes
- Harness files: `AGENTS.md`, `init.ps1`, `feature_list.json`, `progress.md`, `session-handoff.md`
- LICENSE (MIT)

### Notes
- First implementation of the thinking-mode scaffold derived from Qian Xuesen & Song Jian's
  *Engineering Cybernetics* (工程控制论).
- Language- and framework-agnostic; targets any non-trivial code change where correctness
  AND robustness must both be verified.
