# statsoft-cli — Advanced Reference (Developer)

This file holds the technical details that ordinary users don't need. For daily use, see [README.md](README.md).

## Platform Support

### Core software

| Software | Windows script | Cross-platform script | Verify |
|---|---|---|---|
| SPSS Statistics | `scripts/windows-only/SPSS/setup_spss.ps1` | — | `stats.com -production silent -nologo "exit.spj"` |
| R | `scripts/windows-only/statsoft-r.ps1` | `scripts/cross-platform/R/setup_r.sh` | `Rscript --version` |
| Stata | — | `scripts/cross-platform/Stata/setup_stata.sh` | `stata-mp -b do "exit"` |
| SAS | `scripts/windows-only/statsoft-sas.ps1` | `scripts/cross-platform/SAS/setup_sas.sh` | `sas -version` |

(Full routing table for all additional packages — see `ADDITIONAL_SOFTWARE.md`.)

## Project Structure

```
statsoft-cli/
├── SKILL.md
├── README.md / README_zh-CN.md
├── ADVANCED.md / ADVANCED_zh-CN.md
├── ADDITIONAL_SOFTWARE.md
├── LICENSE
├── config.json.example
├── scripts/
│   ├── cross-platform/   (_platform-detect.sh, scan/scan_all.sh, per-tool setup_*.sh)
│   └── windows-only/     (scan/scan_all.ps1, per-tool setup_*.ps1, statsoft-r.ps1, statsoft-sas.ps1)
├── references/           (command-examples.md, version-specifics.md, completion-prompts.md, config-templates.md, workflow.md, platform-support.md, trust-and-safety.md)
├── tests/
└── assets/icon.svg
```

## Activation Boundary & Usage

The skill activates only on an **explicit, narrowly scoped request** naming the target tool and action (e.g. `configure R`, `run Stata <file>`, `convert data.sav to data.dta`). Free-form phrases like "configure statistical software" are intentionally not auto-activated for high-risk execution.

Trigger examples (require naming the tool/action):
- Connect SPSS 26
- Configure R statistical software
- Convert data.sav to data.dta
- Run a Stata .do file in batch mode

Non-trigger examples (treated as ordinary conversation):
- I read a paper about R
- Can you explain what Stata is?

## Authorization & Persistence Model

- The opt-in flags (`STATSOFT_AUTO_WRITE` / `STATSOFT_CONFIRM`) are set **by the user**; the skill only **reads** them and never writes them or any other environment variable.
- The **only** file the skill may persist is its own `config.json`, and **only after** explicit opt-in (timestamped `config.json.bak.*` backup; delete `config.json` to roll back).
- The skill does **not** write `~/.workbuddy/MEMORY.md` or anything outside its own directory.

## Trust & Safety (detail)

This skill performs high-risk operations; understand the risk levels before use:

| Risk | Level |
|---|---|
| Execute local executables | 🔴 High |
| Download & install software | 🔴 High |
| Execute user scripts (e.g. `.sps` via SPSS Python) | 🔴 High |
| Modify config.json | 🟡 Medium |
| Network access | 🟡 Medium |

**Pre-flight**: ✅ review all scripts; ✅ confirm config.json changes (auto-backup); ✅ confirm any downloads; ✅ inspect generated commands for sensitive projects.

Per-software CLI command examples: see `references/command-examples.md`.
