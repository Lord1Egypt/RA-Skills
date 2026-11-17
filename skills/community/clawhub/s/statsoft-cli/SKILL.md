---
name: statsoft-cli
slug: statsoft-cli
displayName: Statsoft-CLI / 统计软件接入助手
cn_name: 统计软件接入助手
version: "2.8.4"
summary: "跨平台统计软件 CLI 集成，面向 AI Agent；覆盖 34+ 款软件（R/Stata/SAS/SPSS/Python/贝叶斯/ML等），双语。核心价值：激活历史代码资产，用于 AI 工作流自动化。"
license: MIT
description: "Cross-platform statistical software CLI integration for AI Agent; 34+ packages (R/Stata/SAS/SPSS/Python/Bayesian/ML, etc.), bilingual. Core value: activating historical code assets for AI workflow automation. / 跨平台统计软件 CLI 集成，面向 AI Agent；覆盖 34+ 款软件（R/Stata/SAS/SPSS/Python/贝叶斯/ML等），双语。核心价值：激活历史代码资产，用于 AI 工作流自动化。"
triggers:
  - "SPSS"
  - "SPSS Statistics"
  - "R命令行"
  - "Stata"
  - "SAS"
  - "统计软件"
  - "连接统计软件"
  - "statsoft-cli"
  - "connect statistical software"
required_commands: [python, bash, powershell]
metadata:
  {
    "openclaw": { "emoji": "🛠️", "icon": "assets/icon.svg" },
    "authors": ["medstatstar", "phoe-zip"],
    "contributors": ["medstatstar", "phoe-zip"],
    "version": "2.8.4",
    "license": "MIT",
    "tags": ["Statistical Software", "CLI", "R", "SPSS", "Stata", "SAS", "Bayesian", "Machine Learning", "Econometrics", "SEM", "Data Mining"],
    "homepage": "https://github.com/medstatstar/statsoft-cli",
    "repository": "https://github.com/medstatstar/statsoft-cli"
  }
permissions:
  scope: "user-space-only"
  network: "off"
  network_note: "Offline by default; only CRAN / Anaconda repo access for local dependency install, requires explicit confirmation."
  filesystem: "read-only to its own files; writes only config.json under skill root with explicit opt-in"
  data: "no external data transmission"
---

## Language

Pick the README that matches your language for human-readable, language-specific guides:

- **English guide** → [README.md](https://github.com/medstatstar/statsoft-cli/blob/main/README.md)
- **中文指南** → [README_zh-CN.md](https://github.com/medstatstar/statsoft-cli/blob/main/README_zh-CN.md)

This skill responds in the user's current input language (Chinese or English) and auto-detects / switches accordingly. The runtime scripts embed a locale check (`$script:isZH` in PowerShell, `SCRIPT_LANG` in Bash) so all user-facing prompts switch to Chinese on a `zh-*` UI culture and to English otherwise. Code comments and documentation are English-only.

The SKILL.md body, `references/*.md`, and `ADDITIONAL_SOFTWARE.md` are English-only and agent-facing; runtime command prompts switch to Chinese / English by locale. For end-to-end walkthroughs, examples, and troubleshooting in your language, open the README above.

## Overview

Activates historical code assets locked in statistical software (syntax, scripts, projects) and wires them into AI workflows via automated detection, configuration, and execution.

## Core Functions

Covers 34+ statistical / data-science packages, auto-routed by platform; non-Windows auto-hides incompatible software:

- **Cross-platform (Win / Mac / Linux, CLI)**: R, Stata, SAS, CmdStan, GenStat, Gretl, H2O.ai, JAGS, Julia, KNIME, Mathematica, Matlab, OpenBUGS, Orange, OxMetrics, PSPP, Rattle, SHAZAM, Stat/Transfer, Tanagra, TSP, Weka
- **Windows + limited cross-platform**: Mplus
- **Windows-only CLI**: SPSS Statistics, EViews, JMP, LIMDEP, Microfit, NCSS, NLOGIT, Origin, Q(MRKS), SPSS Modeler, Statistica
- **GUI-only detection + manual launch guide**: AMOS, GraphPad Prism, JASP, jamovi, Minitab (never drive batch via CLI; `mtb.exe /run` opens the Minitab GUI, not headless)

Full platform matrix in `references/platform-support.md`; extended config in `ADDITIONAL_SOFTWARE.md`.

## Router Paths

When gate 0 classifies a request as **Simple** (clear tool + action), route straight to the canonical per-tool entry script. These are the 6 primary entry points; the rest are auto-discovered from the platform matrix:

- `scripts/windows-only/SPSS/setup_spss.ps1` — SPSS Statistics (Windows)
- `scripts/windows-only/statsoft-r.ps1` — R CLI wrapper / data conversion (Windows)
- `scripts/cross-platform/R/setup_r.sh` — R (cross-platform)
- `scripts/cross-platform/Stata/setup_stata.sh` — Stata (cross-platform)
- `scripts/windows-only/statsoft-sas.ps1` — SAS (Windows)
- `scripts/cross-platform/SAS/setup_sas.sh` — SAS (cross-platform)

## Clarification Gate (gate 0) — friendly menu policy

Per ct-base §13 (the same pattern ct-advisor implements as its gate 0), this skill **triages the user's first message before opening any menu** and **defaults to the friendliest path**. The interactive menus (scan-confirmation, config-mode selection) are only shown when step-by-step confirmation genuinely helps — never forced onto a simple request.

Classify the first message into one of three paths:

- **Simple** — specific, single-intent, answerable directly (e.g. "Connect SPSS 26", "Convert data.sav to data.dta", "Run my Stata do-file batch"). → Detect / act in one pass. **Do NOT pop the scan or config menu.** If the tool and target are clear, route straight to detection / configuration (detect-only by default) and report; optionally offer a deeper step ("want me to also scan for the rest?") rather than demanding a choice.
- **Complex** — multi-decision or "set up everything / I'm not sure what's installed" (Example 4 in the README). → Present the **routing menu** (auto-scan vs specify-paths) and confirm step by step. Only open the full menu when step-by-step confirmation genuinely helps.
- **Vague** — need unclear / user undecided (Example 5, "I want to use statistical software but don't know where to start"). → Enter **grill-me clarify mode**: ask 1–3 conclusion-changing questions per round (which tools are installed? what do you want to do — run old scripts / convert data / build new analysis? headless or GUI?), branch-by-branch, until the right tool is locked — never dump the 34-tool list or pick for the user.

**Default to the friendliest path**: when in doubt between simple and complex, give a short direct detection + an optional deeper-menu offer instead of forcing a menu. When the user's first message already names a clear target (a specific tool + action), **skip the menu entirely** and go straight to detection / configuration.

> The clarification strings themselves follow the locale switch (`$script:isZH` / `SCRIPT_LANG`), so menus and probes render in Chinese on a `zh-*` system and English otherwise — consistent with ct-base §13.3 (this skill's script-embedded locale mechanism is the equivalent of `i18n.py`).

## Execution Workflow

1. **Detect Platform** — cross-platform `source scripts/cross-platform/_platform-detect.sh` (sets `WB_OS` / `WB_ARCH`; Windows handled inside `.ps1` scripts, no source)
2. **Pre-scan Confirmation** (only when gate 0 classifies the request as **Complex**) — before a full scan, prompt and wait:
   - Prompt (English by default; auto-switched to Chinese on a `zh-*` locale): "⚠️ Auto-scan may take a while (~30s on Windows). If you have ≤3 packages, specify paths to skip. Your choice?" Options: A) Auto-scan  B) Specify paths
   - A → step 3; B → skip scan, go to step 4
3. **System Scan** (only if A) — batch-detect installed software:
   - Windows: `scripts/windows-only/scan/scan_all.ps1`; Mac/Linux: `scripts/cross-platform/scan/scan_all.sh`
   - Output JSON: `{"R":{"installed":true,"path":"...","version":"..."},...}`
   - **Batch scan** (`scan_all.*`): without explicit consent it is **skipped entirely** (prints a notice, exits 0, no JSON). With consent (set `STATSOFT_AUTO_WRITE` to `1` or `STATSOFT_CONFIRM` to `1` plus an interactive `y`) it returns the full `{path, version}` JSON. `STATSOFT_REVEAL` does **not** affect the batch scan.
   - **Per-software setup** (`setup_*.sh` / `setup_*.ps1`): reports `installed=true` with path / version **hidden by default**; `STATSOFT_REVEAL` set to `1` reveals them in the setup output — this is the only thing `REVEAL` controls.
4. **Select Config Mode** — batch / specified / single-software (calls individual `setup_*.ps1` or `setup_*.sh`)
5. **Detect & Setup** — route to the platform script; non-Windows auto-hides incompatible software
6. **Save Config** — detect-only by default; writes `config.json` only with explicit authorization (set `STATSOFT_AUTO_WRITE` to `1` or `STATSOFT_CONFIRM` to `1` plus an interactive `y`)
7. **Output Summary** — per `references/completion-prompts.md` template

## Default-Deny Gates

All persistence and sensitive operations are **off by default** and require explicit authorization (fail-closed), consistent with the scripts:

| Gate | Effect | Default |
|------|--------|---------|
| `STATSOFT_AUTO_WRITE` set to `1` | Persist `config.json` (non-interactive / agent context) | off |
| `STATSOFT_CONFIRM` set to `1` + TTY y | Persist after interactive confirmation | off |
| `STATSOFT_REVEAL` set to `1` | Reveal path / version in **per-software setup** output only (batch `scan_all` needs consent, not `REVEAL`) | off |
| `STATSOFT_VERIFY` set to `1` | Allow launching third-party binaries for version / verification | off |
| `STATSOFT_CMDSTAN_RUN` set to `1` | Allow compiling & running user Stan models (untrusted native code) | off |

All writes go through `scripts/common/write_config.py`: accepts only the canonical `config.json` under the skill root, and before writing takes a timestamped backup (`config.json.bak.yyyymmdd_hhmmss`) then atomic-replaces.

## Core Permissions

- **Local file read-write** — `config.json`, temp scripts
- **Process execution** — statistical software binaries
- **Network access** — CRAN / Anaconda repos

## Trust & Safety

This skill performs high-risk operations; understand the risk levels before use:

| Risk | Level |
|------|-------|
| Execute local executables | 🔴 High |
| Download & install software | 🔴 High |
| Execute user scripts (e.g. `.sps` via SPSS Python) | 🔴 High |
| Modify config.json | 🟡 Medium |
| Network access | 🟡 Medium |

**Pre-flight**: ✅ review all scripts; ✅ confirm config.json changes (auto-backup); ✅ confirm any downloads; ✅ inspect generated commands for sensitive projects.

## Known Issues & Pitfalls (SPSS, Windows)

Two real failures reproduced when running SPSS on a host where the agent shell
injects its own `PYTHONPATH` (e.g. WorkBuddy Bash injects
`PYTHONPATH=<app>/cli/vendor/shim` with a `sitecustomize.py` using Python 3.6+
`os.fspath`). Recorded here so the agent never repeats them.

Detailed root-cause + exact fix commands for the 3 reproduced SPSS failures (PYTHONPATH/`os.fspath` crash; `OUTPUT EXPORT` unavailable in headless mode; `SAVE OUTFILE` must point at an existing directory) → `references/known_issues.md`.

| # | Error / failure | Cause | Fix |
|---|-----------------|-------|-----|
| 1 | `AttributeError: 'module' object has no attribute 'fspath'` on `spss.StartSPSS()` | Injected `PYTHONPATH` shim uses 3.6+ `os.fspath`; SPSS bundled Python is 3.4 | Use `spss_helper.py` (drops `PYTHONPATH`); manual calls prefix `PYTHONPATH=` |
| 2 | `OUTPUT EXPORT` / `OUTPUT SAVE` to `.spv`/`.pdf` fails in headless mode | No output-viewer document in the no-GUI backend | Use `stats.exe --production "job.spj"` |
| 3 | `SAVE OUTFILE` fails / skill self-test fails | Absolute path to a non-existent directory | Use a relative path (working dir = `tests/`) |

## Reference Files

- `ADDITIONAL_SOFTWARE.md` — extended software config (31 packages)
- `references/command-examples.md` — per-software CLI command examples
- `references/config-templates.md` — `config.json` templates & field reference
- `references/version-specifics.md` — version differences
- `references/completion-prompts.md` — completion prompt templates
- `references/trust-and-safety.md` — risk levels & pre-flight details
- `references/workflow.md` — workflow gating details
- `references/platform-support.md` — full platform support matrix
- `tests/` — automated test scripts