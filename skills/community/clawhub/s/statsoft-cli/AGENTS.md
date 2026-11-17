# AGENTS.md — statsoft-cli

## Overview

`statsoft-cli`: cross-platform CLI integration for statistical software (34+ packages: R, Stata, SAS, SPSS, Python, Bayesian, ML). It auto-detects, configures, and executes historical code assets locked in statistical software (syntax, scripts, projects), wiring them into AI workflows. `SKILL.md` is the entry point; `README.md` (English) and `README_zh-CN.md` (Chinese) are language-specific guides.

---

## ct-base Alignment

This skill is **NOT** a `ct-` skill, but its frontmatter and documentation have been aligned to the `ct-base` unified conventions (BASE.md v1.1.11) wherever applicable:

- **Frontmatter §3**: carries the mandatory `required_commands: [python, bash, powershell]` and a top-level `permissions` block (`scope` / `network` / `filesystem` / `data`). `summary` / `cn_name` stay Chinese-only; `displayName` / `description` / `triggers` are bilingual with the ` / ` separator.
- **README §10.7**: restructured to the user-view layout — logo, one-line intro, chat examples (including a Complex pop-up menu and a Vague / grill-me branch), a scenario index with a "Try saying" column, a first-time FAQ, and a user-language safety note; all developer/technical content moved to `ADVANCED.md` / `ADVANCED_zh-CN.md`.
- **§13.3 i18n**: satisfied by the **script-embedded locale mechanism** (`Write-Lang` + `$script:isZH` in PowerShell, `LANG_ZH()` + `SCRIPT_LANG` in Bash). This is the equivalent implementation; no `scripts/i18n.py` is introduced.
- **§13 gate-0 friendly menu policy**: `SKILL.md` now opens with a Clarification Gate that triages the user's first message into Simple / Complex / Vague and **defaults to the friendliest path** — interactive menus (scan-confirmation, config-mode selection) are never forced onto a simple request. This mirrors ct-advisor's gate 0.
- **NOT applicable (ct- specific, intentionally not copied)**: §0.1 NMPA/CDE localization, §9 four-tier A/B/C/D grading, §10.5 CT-series confidentiality notice, §13.4 R-as-`.py` templating. Normal-language output switching still follows the same locale rule as ct- skills.

---

## Core Rules

### 1. Language

- `SKILL.md` body, `references/*.md`, `ADDITIONAL_SOFTWARE.md`, and this file (`AGENTS.md`) are **English-only and agent-facing**.
- Bilingual human-readable content lives ONLY in the two READMEs; the `## Language` segment in `SKILL.md` links both. Never put Chinese into documentation headings or body.
- Runtime command prompts (from PowerShell / Bash setup scripts) switch to Chinese on a `zh-*` locale and English otherwise, via `$script:isZH` (PowerShell) / `SCRIPT_LANG` (Bash). This is runtime behavior, not doc content.
- `summary` is a **special field**: it MAY be Chinese-only even for a published skill (marketplace discovery relies on the bilingual `displayName` / `description` / `triggers`; `summary` alone does not need to be bilingual).

### 2. Config Write Safety (fail-closed)

- Detection scripts are **detect-only by default**. Writing to `config.json` is fail-closed: it requires explicit opt-in — set `STATSOFT_AUTO_WRITE` to `1` (non-interactive / agent) or `STATSOFT_CONFIRM` to `1` plus a TTY "y" answer. Never block an agent.
- All `config.json` writes go through `scripts/common/write_config.py`: timestamped backup (`config.json.bak.yyyyMMdd_HHMMSS`) + atomic `os.replace`. Canonical targets: skill-root `config.json` and `scripts/windows-only/config.json`.
- GUI-only software (AMOS, GraphPad Prism, JASP, jamovi, Minitab) are detected and given a manual launch guide only; never driven via CLI / headless. Note: `mtb.exe /run` launches the Minitab GUI window (observed title `Minitab - [Untitled]`), so it is not headless-safe.

### 3. Software / R Package Install

- Installing statistical software or R packages requires explicit user confirmation before any network download.

### 4. Activation Boundary

- Only respond to an explicit user request to configure / run a specific tool. Do not auto-trigger on vague mentions.

### 6. Friendly Menu Policy (gate 0, per ct-base §13)

- Before opening any interactive menu (scan-confirmation, config-mode selection), **triage the user's first message** into Simple / Complex / Vague and **default to the friendliest path**.
- **Simple** (named tool + action, e.g. "Connect SPSS 26"): detect / act in one pass; **do NOT pop the scan or config menu**.
- **Complex** (full setup, "not sure what's installed"): present the routing menu and confirm step by step.
- **Vague** (undecided): enter grill-me clarify mode — ask 1–3 high-value questions per round, branch-by-branch, until the tool is locked. Never dump the full 34-tool list or pick for the user.
- When in doubt between simple and complex, give a short direct answer + an optional deeper-menu offer rather than forcing a menu.

### 5. Reuse / Conventions

- Locale-switch helpers: PowerShell `Write-Lang` + `$script:isZH`; Bash `LANG_ZH()` + `SCRIPT_LANG`.
- Validation: `.sh` → `bash -n`; `.py` → `py_compile`; `.ps1` → `[System.Management.Automation.Language.Parser]::ParseInput` (NOT `System.Management.Automation.PSParser`, which lacks `ParseInput` in Windows PowerShell 5.1).
- Cross-platform `*.sh` MUST be LF (Git Bash rejects CRLF). `.ps1` containing Chinese MUST be UTF-8 BOM on WinPS 5.1 (else GBK misread).

---

## Dependencies

- Python: Anaconda `C:\Tools\anaconda3\python.exe` (per environment convention).
- R: `C:\Tools\R-4.5.1\bin\x64` (statistical computation).
- PowerShell 5.1 / Bash (Git Bash) for setup and scan scripts.

---

## Security Red Line

- Never transmit user data off-local. Network use is limited to reading public docs / installing local dependencies, disclosed per action.
