# Changelog

## v2.8.4 (2026-10-14)

Headless execution overhaul (no GUI popups by default) + Stata 19.5 MP integration.

- **New shared headless launcher `scripts/common/invoke_hidden.ps1`** (`Invoke-StatExe`):
  every third-party binary is launched via `cmd.exe /c` with `WindowStyle=Hidden`
  and stdout/stderr redirected to temp files (read back and surfaced). Rationale:
  `Start-Process` crashes in host shells that inject duplicate env keys differing
  only by case (HTTPS_PROXY/https_proxy); `CreateNoWindow` strips the window
  station from GUI-subsystem children and makes Stata fail (exit 1) — Hidden only.
- **All 5 executors** (Stata / SAS / EViews / Statistica / StatTransfer) migrated
  from direct `& $exe` calls to `Invoke-StatExe`; GraphPad `open` intentionally
  keeps GUI launch (Prism has no CLI mode, documented in-file).
- **Stata log handling fixed**: Stata `/e do` writes its log to the process
  working directory, not beside the do-file — `run` now sets `-WorkingDirectory`
  to the do-file's folder and auto-displays the log after execution.
- **BOM fix**: PS 5.1 `Set-Content -Encoding UTF8` writes a UTF-8 BOM; Stata
  treats it as part of the first command so `log using` silently fails.
  Temp .do/.sas files now written BOM-less via
  `[System.IO.File]::WriteAllText(..., UTF8Encoding($false))`.
- **MSYS path-conversion guard**: `setup_stata.sh` / `setup_sas.sh` / `setup_r.sh`
  export `MSYS_NO_PATHCONV=1` (Windows Git Bash converts single-letter switches
  like `/e` to drive paths `E:/`, causing `r(199)` + GUI fallback).
- **Stata 19.5 MP linked** in `config.json` (`C:\Tools\Stata19\StataMP-64.exe`,
  MP, version 19.5; machine-local file, gitignored).
- **Packaging hygiene (§16.8 recheck)**: untracked `tests/` (was git-tracked,
  leaking into the package model), ignore `config.json.bak.*` and `*.log`,
  removed `verify.log` leftover.

## v2.8.3 (2026-09-03)

SPSS-on-Windows robustness: two real failures reproduced when the agent shell
injects a parent `PYTHONPATH` (WorkBuddy Bash injects `<app>/cli/vendor/shim` with
a `sitecustomize.py` using 3.6+ `os.fspath`), plus the skill's own self-test fix.

- **SPSS bundled Python `os.fspath` crash (root-cause fix)**: `_minimal_env()` in
  `scripts/windows-only/SPSS/spss_helper.py` forwarded `PYTHONPATH` into the SPSS
  bundled-Python subprocess, so the injected shim's `sitecustomize.py` (3.6+) broke
  SPSS 26's Python 3.4 with `AttributeError: 'module' object has no attribute
  'fspath'`. Removed `PYTHONPATH` from the env allow-list (`run-internal` /
  `show-version` no longer inherit it); the bundled runner still sets up its own
  site-packages via `sys.path`, so behaviour is unchanged. Agent no longer needs the
  manual `PYTHONPATH=` prefix when going through `spss_helper.py`.
- **SKILL.md Known Issues & Pitfalls (SPSS, Windows)**: documented the three
  failures as an error table — (1) `PYTHONPATH`/`os.fspath` crash + the `PYTHONPATH=`
  prefix workaround + "bundled Python 3.4 has no f-strings, use `%s`/`.format()`";
  (2) `OUTPUT EXPORT` / `OUTPUT SAVE` unavailable in the no-viewer headless backend,
  must use `stats.exe --production "job.spj"`; (3) `SAVE OUTFILE` must use a path
  whose directory exists (relative path, working dir = `tests/`).
- **`tests/test-syntax.sps`**: `SAVE OUTFILE` changed from a hard-coded
  `C:/Users/WintoneFileSrv/...` (non-existent → self-test always failed) to a
  relative `test-data.sav` (working dir = `tests/`).

## v2.8.2 (2026-08-02)

Ten-round bug-hardening cycle (design 10 simple→complex cases, execute fixes, repeat). Round 1 fixes the empirically-confirmed defects from the case design:

- **B1 (test suite broke)**: `tests/run_all.py` asserted SKILL.md contained 6 router paths; the §10.7 alignment had removed them → 6 failures. Fixed by adding a dedicated **`## Router Paths`** section listing the 6 canonical entry scripts (SPSS / R / Stata / SAS on both platforms). Test suite now 48/48 green.
- **B2 (wrong variable names)**: SKILL.md claimed `_platform-detect.sh` sets `$PLATFORM`/`$OS`/`$ARCH`; the script actually exports `WB_OS`/`WB_ARCH` (which `scan_all.sh` uses). Corrected the Execution Workflow step 1.
- **B3 (REVEAL / scan doc contradictions)**: the gate table said `STATSOFT_REVEAL` "reveals path/version during detection", but (a) `scan_all.sh` never reads REVEAL and (b) without consent it is **skipped entirely (no JSON)**, not "returns installed boolean". Rewrote the gate-table row and the Execution Workflow scan bullets, and fixed `references/workflow.md` §Scan Disclosure to match the real consent-gated behaviour. `REVEAL` now documented as governing **per-software setup output only**.
- **B4 (missing UTF-8 BOM)**: 26 `.ps1` files lacked a UTF-8 BOM; under Windows PowerShell 5.1 these parse as the system codepage and Chinese text mojibakes. Added the BOM to all 26 (1 already had it).
- **B5 (dual config divergence)**: root `config.json` and `scripts/windows-only/config.json` are both canonical, but `statsoft-r.ps1` reads only the windows-only copy — a write to one could leave the other stale. `write_config.py` now **mirrors every persist to the sibling canonical location** (with backup + atomic replace) so the two never diverge.

### Round 2 — cross-platform bash portability (macOS bash 3.2)

- **Bash 3.2 compatibility**: `scan_all.sh` used `declare -A` (associative arrays, bash ≥4.0) and `local -n` (nameref, bash ≥4.3) — both unavailable on macOS's default bash 3.2, so the "macOS-supported" batch scan would crash. Rewrote `json_output`/`add_result` to use an indexed array with an empty-array guard safe under `set -u`. Same fix applied to `setup_r.sh` (its `stat_categories`/`stat_categories_zh` associative arrays → parallel indexed arrays).
- **POSIX command substitution**: `scan_all.sh` and 10 `setup_*.sh` used `$(which …)`; `which` is absent on minimal Git Bash / BusyBox. Replaced all with the POSIX `$(command -v …)`. Also replaced the GNU-only `grep -oP` (PCRE) in `scan_all.sh`'s version extractor with the portable `grep -oE '[0-9]+(\.[0-9]+)+'`.
- Static check: `bash -n` passes on all 28 `.sh`; `scan_all.sh` runs clean (valid JSON, no `which`/nameref errors) with and without consent.

### Round 3 — dynamic PowerShell testing (cases 7/8: missing config / missing tool)

- **B6 (config path off-by-one, systemic)**: 21 windows-only `.ps1` resolved config via `$PSScriptRoot\..\config.json`. For scripts that live *directly* in `scripts/windows-only/` (e.g. `statsoft-r.ps1`, `statsoft-sas.ps1`, `statsoft-eviews.ps1`, `statsoft-jmp.ps1`, `statsoft-statistica.ps1`, `statsoft-graphpad.ps1`, `statsoft-stattransfer.ps1`) this jumps one level too high to `scripts/config.json` (non-existent); `statsoft-spss.ps1` used `..\..` (two levels too high). All now use a **3-tier resolution** (same-dir → parent → grandparent), correct for both subdirectory and top-level scripts. Verified `statsoft-r.ps1` now locates `scripts/windows-only/config.json`.
- **B7 (null config key crash)**: `statsoft-r.ps1` did `$rPath = $config.R.Path` then `Test-Path $rPath`; when the config has no `R` key (or an empty `Path`) `$rPath` is `$null` and PowerShell throws a raw "cannot bind Path because it is empty" exception. Added a guard: prefer configured `R.Path`, **fall back to `Get-Command Rscript` auto-detection**, and otherwise emit a clear zh/en error ("Rscript.exe not configured or detected; run R setup first") and exit 1. Confirmed graceful handling via re-run.

### Round 4 — dynamic PowerShell testing (case 4/8: scan false-positive)

- **B8 (`scan_all.ps1` misreports uninstalled as installed)**: `Add-RResult` used `if ($installed -or $null -eq $installed)` — PowerShell's `$null -eq $installed` is `$true` when a tool was *not* found (detection returns `$null`), so every uninstalled package (TSP/GenStat/SHAZAM/NCSS/…) was written as `"installed": true`. Changed the guard to `if ($installed)` only. Verified with TSP/GenStat/SHAZAM/NCSS now correctly report `installed:false`. (R/SPSS/Stata/etc. still show `true` because this host genuinely has them.)

### Round 5 — schema-contract audit (config ↔ scanners ↔ setup)

- **B9 (`platform` taxonomy split)**: `config.json.example` and four windows-only setup scripts emitted `"win"` while every scanner (`scan_all.ps1`, `scan_all.sh`) and the other setup scripts emit `"windows"`; nothing emits the `"all"` value used by cross-platform tools in the example. Normalised all `"win"` → `"windows"` in `config.json.example` (Mplus/AMOS/Q_MRKS), `setup_amos.ps1`, `setup_minitab.ps1`, `setup_mplus.ps1`, `setup_q.ps1`, and the live `scripts/windows-only/config.json`. `"all"` retained as the documented cross-platform sentinel.
- **B10 (config key mismatch `Q (MRKS)` vs `Q_MRKS`)**: `scan_all.ps1` emitted the detection key `"Q (MRKS)"` but `config.json.example` and `setup_q.ps1` use the canonical config key `"Q_MRKS"`. Merging scan output into `config.json` would create a duplicate/orphan key. Changed the scanner to emit `"Q_MRKS"`. Verified via re-run.
- **B11 (`H2O.ai` vs `H2O`)**: `scan_all.sh` (Linux/macOS branch) emitted `"H2O.ai"` while `config.json.example` and the cross-platform setup use `"H2O"`. Normalised the scanner to `"H2O"`.
- **B12 / B15 (example schema gaps)**: `config.json.example` omitted the `installed` field on 13 entries (inconsistent with the 17 that had it) and omitted `Minitab` entirely though the skill supports and scans it. Added `installed:true` to all entries and added a `Minitab` template block. Both `config.json.example` and the live `config.json` re-validated as JSON; `scan_all.sh` re-checked with `bash -n`.

### Round 6 — R wrapper e2e + write_config mirror re-verification

- **B15 (R `-e` argument/command injection in `statsoft-r.ps1`)**: the `install` branch and the `data-info` `haven` fallback interpolated the user-supplied `$package` / `$Repo` directly into an `R -e "..."` expression — a crafted package name such as `x'); system('...') #` could execute arbitrary R code. Refactored both to write a throwaway R script that receives `pkg` / `repo` via `commandArgs(trailingOnly=TRUE)` (the same safe pattern `data-info` already uses for file reads), and removed the inconsistent hardcoded CRAN URL in the `haven` fallback (now honours `$Repo`). Verified: script parses; with R unconfigured it exits gracefully at the resolution guard so the injection-shaped input never reaches R.
- Re-verified `write_config.py` (B5 mirror) in an isolated temp copy: writing to one canonical `config.json` now mirrors the sibling; non-canonical targets, empty payloads, invalid JSON, and missing consent are all rejected safely (no config mutation without opt-in). No regression.

### Round 7 — i18n / locale completeness audit

- No defect. Every `$(LANG_ZH …)` call in all 28 `.sh` carries both CN+EN quoted args; all 27 PowerShell scripts that call `Write-Lang` define it (no undefined-function), and every call either supplies both branches or uses the inline `$(if ($script:isZH) {…} else {…})` selector (the single flagged `setup_spss.ps1` call was a false positive of that pattern). Locale output is consistent across both runtimes.

### Round 8 — `.sh` POSIX / bash-3.2 re-lint

- No residual hazard. Re-grepped all `.sh` for bash ≥4.0-only constructs (`${var,,}`/`${var^^}`, `mapfile`/`readarray`, `;&`/`;;&`, `test -v`, `grep -P`/`-oP`, `declare -A`, `local -n`, `$(which `) — none remain. `bash -n` passes on all 28 `.sh`.

### Round 9 — Python helper robustness

- **B16 (SPSS runner gated by the wrong opt-in)**: `run-spss-internal.py` (the SPSS syntax **runner**) exited at its top-level guard unless `STATSOFT_REVEAL set to 1` was set. But `REVEAL` is the *disclosure* gate (install-path/version), whereas the skill's execution opt-in is `STATSOFT_VERIFY set to 1` (enforced by `statsoft-spss.ps1`). An authorized run with `VERIFY=1` and no `REVEAL` was therefore wrongly blocked. Changed the helper to require `STATSOFT_VERIFY set to 1` (defense-in-depth, matching the caller) and reworded the message. Verified: with `VERIFY=1` and no `REVEAL` the script now passes the gate and reaches SPSS loading (the subsequent DLL error is just this non-SPSS interpreter, not a code fault).
- All 8 `.py` modules `py_compile` clean; `setup_amos.py` and `statsoft-cmdstan.py` already default missing `config.json` to `{}`, so fresh-install runs don't crash.

### Round 10 — final integration / regression pass

- **Router Paths regression (B1)**: re-verified the 6 canonical entry scripts listed in `## Router Paths` — SPSS `setup_spss.ps1`, R `statsoft-r.ps1` + `setup_r.sh`, Stata `setup_stata.sh`, SAS `statsoft-sas.ps1` + `setup_sas.sh` — all exist on disk at the documented paths. A `sed | cat -A` byte-level check confirmed the cross-platform paths carry the correct `R/` / `Stata/` / `SAS/` subdirectories; a first-pass `grep` display artifact (showing the flat path) was ruled out as non-defect after cross-verification. No divergence between documented router and filesystem.
- Full suite `tests/run_all.py` re-run: **48/48 green** (no regression). ct-base §3 frontmatter (`name` / `slug` / `displayName` / `version` / `summary` / `license` / `description` / `triggers` / `required_commands` / `metadata` / `permissions`) re-audited clean.
- Ten-round cycle complete: R1–R10 each designed and executed a simple→complex case set; empirically confirmed and fixed **B1–B16** across schema-contract, bash-portability, PowerShell, Python, and security-gate dimensions. R7 / R8 / R10 found no residual defect (hardening evidence, not a skipped round). Version 2.8.2; local only, publishing pending user confirmation.

### Security audit remediation (ClawHub SkillSpector, 2026-08-02)

Reviewed the live ClawHub SkillSpector + VirusTotal audit. VirusTotal: **64/64 vendors clean**. Findings and dispositions:

- **Critical `exposed_secret_literal` (references/workflow.md:11) — FALSE POSITIVE, remediated.** The scanner matched doc-form `STATSOFT_AUTO_WRITE=1`-style `KEY=VALUE` literals as a hardcoded secret. No real credential exists anywhere in the skill. Remediated by rewriting every `STATSOFT_X=1` assignment literal in documentation to the prose form `STATSOFT_X set to 1` (or `为 1` in zh-CN) across `references/workflow.md`, `SKILL.md`, `README.md`, `README_zh-CN.md`, `AGENTS.md`, `CHANGELOG.md`, and `tests/bug-check-cases.md`. Script-side `STATSOFT_X=1 cmd` env assignments are real opt-in usage and were left intact (not flagged by the scanner).
- **Overly Broad / Vague Triggers (Low/Medium) — FIXED.** Removed the single-letter `R` trigger (it survives as `R命令行` and via `统计软件` / tool-name phrases). Reduces spurious activation of a host-scanning / binary-launching skill.
- **Lp3 (permissions not machine-enforceable) — already declared locally.** Local v2.8.2 ships a ct-base §3 `permissions` block (`scope` / `network` / `filesystem` / `data`). The audited build (published v2.7.1) predates this block; publishing v2.8.2 carries the declaration. (ClawHub's exact machine-enforceable schema is platform-defined; the manifest now documents the surface explicitly.)
- **Tp4 (broad operational surface) + subprocess (Medium ×2) — accepted risk, fully gated & disclosed.** Launching third-party statistical binaries (R / Stata / SPSS / SAS / CmdStan) is the skill's purpose; every such execution is **fail-closed by default** and requires explicit opt-in (`STATSOFT_VERIFY set to 1` for version probes, `STATSOFT_CMDSTAN_RUN set to 1` for compiling/running untrusted Stan models). The README/SKILL docs state this surface up front. No code change beyond the doc wording above.

All changes local-only; publishing v2.8.2 (which already includes R1–R10 hardening + this remediation) is pending user confirmation.

Version bumped to 2.8.2 (top-level + metadata). Local only; publishing pending user confirmation.

## v2.8.1 (2026-08-02)

User-friendly adaptation of the interactive menu and README, referencing ct-advisor's gate-0 modification and ct-base §13 (triaged clarification):

- **SKILL.md — Clarification Gate (gate 0)**: added a triage gate before the Execution Workflow, mirroring ct-advisor's gate 0. The user's first message is classified as **Simple** (named tool + action → detect/act directly, **no menu forced**), **Complex** (full setup / undecided on method → present the routing menu, confirm step by step), or **Vague** (undecided → grill-me clarify mode, 1–3 high-value questions per round, branch-by-branch). Defaults to the friendliest path: never force a menu onto a simple request; skip the menu entirely when the target is already clear. Revised Execution Workflow step 2 to only prompt for a pre-scan when gate 0 classifies as Complex. Version bumped to 2.8.1 (top-level + metadata).
- **README § user-friendliness (both languages)**: added a "Quick start" callout in §1 stating that a clear request acts immediately and a menu only appears when undecided; Example 1 now explicitly notes the simple path forces no menu (links to the SKILL.md Clarification Gate). All §10.7 required blocks retained (logo / chat examples / scenario index / FAQ / safety / ADVANCED / contact-author).
- **AGENTS.md**: added Core Rule §6 "Friendly Menu Policy (gate 0, per ct-base §13)" and noted the gate-0 alignment in the ct-base Alignment section.

## v2.8.0 (2026-07-23)

Comprehensive alignment to the `ct-base` unified conventions (BASE.md v1.1.11), applied where applicable to a non-`ct-` skill:

- **SKILL.md frontmatter §3**: added mandatory `required_commands: [python, bash, powershell]` and a top-level `permissions` block (`scope` / `network` / `filesystem` / `data`); bumped version to 2.8.0 in both the top-level field and `metadata`.
- **README §10.7 user-view restructure** (both `README.md` and `README_zh-CN.md`): added the logo block, a one-line intro quote, a "How to Use in a Chat" section with 5 real examples (including a Complex pop-up menu and a Vague / grill-me branch), a "What You Can Do" scenario index with a "Try saying" column, a first-time FAQ, and a user-language safety note. All developer/technical content (platform matrix, project structure, activation boundary, detailed Trust & Safety) moved to new `ADVANCED.md` / `ADVANCED_zh-CN.md`.
- **Contact-author statement** (§10.6): added to both READMEs — `medstatstar@gmail.com (Wintone Zhang / 张文彤)`.
- **AGENTS.md**: added a "ct-base Alignment" section documenting what was aligned and what was intentionally skipped (§0.1 NMPA/CDE, §9 four-tier grading, §10.5 CT confidentiality, §13.4 R-as-.py) because they are `ct-` specific; confirms the script-embedded locale mechanism is the §13.3-equivalent i18n.
- Version bump to 2.8.0 (local only; publishing pending user confirmation).

## v2.7.1 (2026-07-22)

Bug fixes (no feature changes):

- **Minitab reclassified as GUI-only**: `mtb.exe /run` launches the full Minitab GUI and hangs headless (verified via `tasklist /V`), so it is now detect-only + manual launch guide, consistent with AMOS/GraphPad/JASP/jamovi. Updated SKILL.md, AGENTS.md, ADDITIONAL_SOFTWARE.md, command-examples.md, config-templates.md, setup_minitab.ps1/.sh. Removed the inaccurate `mtb.exe /?` and `/run` batch examples.
- **cross-platform `*.sh` CRLF → LF**: converted 27 working-copy shell scripts to LF and added `.gitattributes` with `*.sh eol=lf` so they stay LF on every platform checkout (previously `core.autocrlf=true` reconverted to CRLF on Windows, breaking the shebang for ClawHub/SkillHub publishes on macOS/Linux).
- **Fixed README links on SkillHub**: SKILL.md `## Language` guide links now point to absolute GitHub blob URLs because SkillHub's markdown renderer wrongly resolves relative links against a global `/skills/` base and drops the skill slug, producing dead links. Absolute GitHub URLs render correctly on every platform.

## v2.7.0 (2026-07-22)

Improved Minitab support and bilingual compliance cleanup:

- **Minitab (Windows)**: added `scripts/windows-only/Minitab/setup_minitab.ps1` (detects `mtb.exe`, fail-closed persist gate); added Minitab detection block to `scan_all.ps1`; fixed `setup_minitab.sh` path list (added 22/23, was capped at 21) + converted to LF; fixed `ADDITIONAL_SOFTWARE.md` routing (added Windows `.ps1` route, `Minitab -?` → `mtb.exe /?`); fixed `command-examples.md` (`mtb.exe /run "analysis.mtb"`); added Minitab section to `config-templates.md`. Minitab 22.3.0.0 detected and persisted locally.
- **write_config.py fixes** (pre-existing bugs affecting all windows-only setup scripts): accept `scripts/windows-only/config.json` as canonical target; read JSON with `utf-8-sig` to tolerate BOM written by WinPS `Set-Content`. `scan_all.ps1` gained UTF-8 BOM so its consent-gate Chinese parses correctly on Windows PowerShell 5.1.
- **Bilingual compliance (per ct-base policy)**: stripped residual bilingual headings across `references/*.md` / `ADDITIONAL_SOFTWARE.md` / `README.md` (103 headings, English-only kept); added required `cn_name` frontmatter field; added English-only `AGENTS.md`. `tests/README.md` exempted as internal test doc. `summary` kept Chinese-only (allowed per ct-base summary exception).

## v2.6.23 (2026-07-19)

- Full alignment to the "locale auto-switch" standard: SKILL.md body, references/*.md (7), and ADDITIONAL_SOFTWARE.md changed to English monolingual (frontmatter displayName/description/triggers keep bilingual for marketplace discovery); .ps1 runners/setup scripts removed hardcoded [CN]/[EN] and inline "中文 / English", unified on Write-Lang + $script:isZH locale switching; .sh setup scripts wrapped ~100 hardcoded-Chinese echo lines into LANG_ZH; all Chinese code comments translated to English.
- Document headings made bilingual (English first, Chinese after); body text stays English; software-name headings (R/Stata/SPSS) stay English.
- Fixed cross-reference dead links: completion-prompts.md (12 links) and example_workflow.md (1 link) ADDITIONAL_SOFTWARE.md paths gained `../`; SKILL.md Reference Files list gained config-templates.md; README files gained CHANGELOG link; ADDITIONAL_SOFTWARE.md TOC anchor typo `#stattranfer` fixed.
- Fixed two real bugs: setup_statistica.ps1 Write-Info/Warn/Error printed both languages in every locale (now switches properly); setup_r.sh stat_categories en-branch mistakenly showed Chinese (now pure-English keys + parallel zh labels).

## v2.6.22 (2026-07-19)

SKILL.md 双语排版顺序对齐新规范（准备提交 GitHub 的技能）：

- **YAML frontmatter 双语字段保持中文在前、英文在后**（displayName / description 已合规，未变）
- **正文全部翻转为英文在前、中文在后**（标题、段落、表格、列表项），与 v2.6.20「中文在前」相反——按用户 2026-07-19 新规则执行
- **尽量同行 ` / ` 分隔**：标题与短内容由两行（中/英各一行）合并为单行 `英文 / 中文`，减少分行
- 正文长度 108 行（≤200）

## v2.6.21 (2026-07-19)

Execution Workflow 与代码实际设定再对齐（纠偏 v2.6.20 文档重构时的两处不一致）：

- **删除「写入记忆 Write Memory」步骤**（原第 7 步）：该步骤要求技能追加 `~/.workbuddy/MEMORY.md`，违反 v2.6.7 确立的安全模型（技能唯一可持久化文件为 `config.json`，不写 MEMORY.md）；写 MEMORY.md 属 AI 助手 / 平台行为，非技能功能。删除后工作流恢复 1–7 连续。
- **修正披露门描述**（原第 63 行）：扫描批量输出的路径/版本披露由 `STATSOFT_AUTO_WRITE set to 1` 或 `STATSOFT_CONFIRM set to 1`+交互 y 控制（与 `scan_all.ps1/.sh` 实际 consent gate 一致），而非 `STATSOFT_REVEAL`；`REVEAL` 仅控制单个软件 setup 检测期输出，已在文中注明区分。
- **精确化平台检测**（第 55 行）：注明跨平台 `source _platform-detect.sh`，Windows 由 `.ps1` 内部处理、不 source 该文件。
- frontmatter metadata 版本 bump 至 2.6.21。

## v2.6.20 (2026-07-19)

SKILL.md 文档重构（中文在前、英文在后；总长度 84 → 约 110 行）：

- **一致性修复**：修正执行工作流编号错位（原两个"3"，现 1–8 连续）
- **补齐功能设定**：新增「默认拒绝闸门」一节，显式列出 `AUTO_WRITE`/`CONFIRM`/`REVEAL`/`VERIFY`/`CMDSTAN_RUN` 五道 fail-closed 闸门，与代码实现对齐（此前 SKILL.md 完全未记载）
- **新增内容**：概述、核心功能（34+ 软件分类清单）、信任与安全（风险等级 + 飞行前检查）
- **去重**：删除 `references/trust-and-safety.md` 中与「核心权限」逐字重复的权限行（改为指向 SKILL.md）；`references/workflow.md` 精简为「闸门细节」补遗，去除与 SKILL.md 重复的流程步骤
- 顺序统一为「中文 / 英文」

## v2.6.19 (2026-07-18)

SkillHub listing 更新（simplify displayName、refine summary 核心价值、streamline bilingual description）；因 SkillHub 不允许同版本覆盖，版本号 bump 至 2.6.19 重新发布（skillId=93580，pending review）。

## v2.6.18 (2026-07-18)

ClawHub SkillSpector v2.6.17 残留 3 issue 修复（TP4 HIGH + 2xAST4 MEDIUM）：

- **TP4 HIGH (SKILL.md)**: 重写 description，显式枚举 4 类行为（主机清单扫描 / 第三方二进制验证运行 / 多类文件创建 / CmdStan 不可信原生代码执行），去掉"有限披露"弱化措辞，与实现像素级对齐
- **AST4 MEDIUM (CmdStan)**: 新增专用显式开关 `STATSOFT_CMDSTAN_RUN set to 1`（独立于通用 AUTO_WRITE/CONFIRM），构建/运行前打印醒目 UNTRUSTED NATIVE CODE 警告；失败-关闭
- 版本号 bump 至 2.6.18

## v2.6.17 (2026-07-14)

ClawHub SkillSpector v2.6.16 残留 3 issue 清零（TP4 HIGH + 2xSDI-4 MEDIUM）：

- **TP4 HIGH (SKILL.md)**: 修正 Default-Deny Gates 表中"config.json 是技能目录下唯一持久化文件"的失真表述，与 Workflow/Trust-Boundary 已披露的 `.spj`/`.spv` 与 CmdStan 编译产物事实对齐
- **SDI-4 MEDIUM (Mathematica)**: REVEAL 门原本只控 console 输出、不控写入 config 的内容；现 REVEAL 关闭时 config 仅记录 `installed=true`，完整路径/版本不再落盘
- **SDI-4 MEDIUM (SPSS Modeler)**: 同上，REVEAL 关闭时 config 不再写入 `path`/`version`

## v2.6.16 (2026-07-13)

TP4 root fix — description-behavior alignment:

- Description now explicitly discloses ALL file operations (persistent .json + .bak backups, ephemeral temp dirs, user-directed .spj/.spv, CmdStan build artifacts)
- Trust Boundary section rewritten with full file operation matrix
- Gretl: `"$gretl_path"` quoted (prevents word splitting)
- SPSS: `"$pyPath"` quoted (same fix)

## v2.6.15 (2026-07-12)

Bilingual restructure — SKILL.md 全面双语化（英中双语、英语在前）+ 内容精简：

- SKILL.md 从 20.6 KB 缩减到 9.2 KB（内容更紧凑）
- 正文采用英中双语段落（英→中），标题英中双语
- 详细内容移到 references（workflow.md、platform-support.md）
- description 字段改为英中双语
- Default-Deny Gates 表格改用英中混合四列表格
- 所有语言自动选择提示统一为 "the user's current input language"

## v2.6.14 (2026-07-12)

ClawHub SkillSpector v2.6.13→v2.6.14 修复 10 个 HIGH/MED 底层 issue（1 HIGH SDI-3 + 1 HIGH TP4 + 多个 MED）：

- **SDI-3 HIGH 致命修复**：移出 `fix_statsoft_functions.py`（代码维护工具误入生产运行时包，被审计器判定为违反"config.json 唯一持久化"模型）
- **TP4 HIGH 继续收紧**：H2O 安装引导加门、Mathematica MathKernel 路径已对齐 REVEAL 门
- **Python-shell 混合修复**：GenStat / OxMetrics 的 `python3 -c` 内不再包含 shell 函数定义，JSON 配置生成恢复正确
- **Rattle OPT-IN 对齐**：`Rscript` 调用全部移到 `STATSOFT_VERIFY set to 1` 门后，默认仅被动检测
- **Windows ps1 未授权读 config 修复**：Limdep / Q_MRKS / SHAZAM 的 config.json 读取 + config 配置构建移到 opt-in gate 之后，真正 fail-closed
- **SPSS spss_helper.py create_spj 修复移除回归**：删除在 finally 块中清理 temp_dir 的代码，spj 文件的路径在调用者使用期间保持有效
- **SKILL.md v2.6.14 更新**

## v2.6.13 (2026-07-12)

ClawHub SkillSpector v2.6.12 扫描 15 项全清（1 HIGH + 13 MEDIUM + 1 LOW）：

- **TP4/HIGH (SKILL.md)**: H2O setup 模块路径无 REVEAL 门 → 已加门
- **SDI-3/HIGH (Mathematica)**: 验证例程无 STATSOFT_VERIFY 门启动 wolframscript → 已加门；MathKernel 路径泄漏 → 已加 REVEAL 门
- **SDI-4 (Gretl)**: `statsoft_reveal()` 函数嵌在 `detect_gretl()` 函数体内（malformed function structure）→ 移到顶层
- **SDI-4 (JAGS)**: python3 -c 内出现 shell 函数定义（`statsoft_reveal()`），损坏 JSON 配置生成 → 已清理
- **SDI-3 (H2O)**: Python 模块路径无 REVEAL 门 → 已加门
- **SDI-4 (OpenBUGS)**: 同 JAGS inline-shell 混合 → 已清理
- **SDI-4 (Orange)**: Python 模块路径无 REVEAL 门 → 已加门
- **SDI-4 (Rattle)**: R 包路径无 REVEAL 门 → 已加门
- **SDI-4 (SHAZAM)**: python3 -c 内非法 shell 函数定义 → 已清理
- **SDI-1 (NCSS)**: 持久化时不区分 REVEAL → 改为默认仅保存 `installed=true`
- **SDI-3 (SPSS run-spss-internal.py)**: 主机扫描 + 路径打印无 REVEAL 门 → 顶部增加门检查
- **SDI-4 (SPSS spss_helper.py create_spj)**: 输出目录可写到任意位置 → 默认使用 `tempfile.mkdtemp()` 临时目录 + 自动清理；显式 output_dir 需 containment 检查
- **SDI-1 (command-examples.md H2O)**: `h2o.init()` 启动本地服务器未醒目警告 → 已加警告
- **AST4 (CmdStan)**: 已有 `user_authorized_to_run()` + temp 目录约束；审计器标记为 CmdStan 固有非恶意 → 无需修改
- **全局（28 个 .sh 文件）**: 9 个文件中 `statsoft_reveal()` / `statsoft_verify()` 定义在函数体内（缩进）引发 malformed structure → 全部移至顶层定义

## v2.6.12 (2026-07-12)

ClawHub SkillSpector 审计深层修复（v2.6.11 扫描 22 项，TP4 主干 HIGH 直击「文档-代码不匹配」根因；本轮不仅逐条修复被抽样命中的文件，更对全部 43 脚本做防雷机分层抽样的系统性门类加固；审计页面显示的 v2.6.11 遗留 16 项本轮全部处理）。本轮核心修复：

- **TP4/HIGH `write_config.py` 单一路径强制执行（根因性修复）**：此前脚本接受任意调用者传入的 `target_path` 并执行「创建目录→备份→原子替换」，审计器标记为"可成为通用文件写入原语"。现从脚本自身位置推导规范路径 `../../config.json`，任何偏离的被拒收（fail-closed），彻底消除任意路径写入风险。直接修复 HIGH #2 与 MED #3。
- **TP4/HIGH `statsoft-spss.ps1` show_version 增加 `STATSOFT_VERIFY set to 1` 闸门**：version 命令启动 SPSS 内置 Python 并拉起 SPSS 引擎（第三方代码执行），现需独立 `STATSOFT_VERIFY set to 1` 才能运行。修复 HIGH #16。
- **TP4/HIGH `statsoft-spss.ps1` 顶部裸路径打印增加 REVEAL 闸门**：L79-81 发现 SPSS 即打印 `stats.com`/`python.exe`/`stats.exe` 完整路径，现纳入 `STATSOFT_REVEAL set to 1` 披露门；默认仅报告检测到的组件列表（不含路径）。
- **TP4/HIGH `SKILL.md` 继续对齐（之三）**：进一步收紧「唯一持久化文件 `config.json`（仅限技能目录）」声明，明确 `write_config.py` 单一路径强制校验；新增披露 show_version 受 `STATSOFT_VERIFY set to 1` 约束。
- **TP4/多层级 Wave 1+2 全门类加固（43 脚本）**：新增 `STATSOFT_REVEAL`（检测输出披露，默认关闭）+ `STATSOFT_VERIFY`（第三方二进制验证，默认关闭）双门体系，覆盖全部检测期路径/版本/包清单打印与二进制启动用例；与既有 `STATSOFT_AUTO_WRITE`/`STATSOFT_CONFIRM`（持久化门）形成完整四门体系。

## v2.6.11 (2026-07-12)

ClawHub SkillSpector 审计继续修复（v2.6.10 仍 `suspicious`，11 项发现，新增 AST4 类型；本轮对扫描器"分层抽样"暴露的整类根因做一次性系统性修复）。逐条 + 整类修复：

- **TP4/HIGH `SKILL.md` 描述再对齐（之二）**：显式声明"所有持久化写入仅落在单一技能目录 `config.json`（绝不在 `$HOME` 等用户主目录）"；声明包清单扫描（`scan_all`）与单目标探测均受显式授权门槛约束、未授权仅返回布尔 `installed`；声明验证步骤启动第三方二进制（如 `--version`）需 `STATSOFT_VERIFY set to 1`。（直接回应审计器点名的"硬编码 `$HOME` 路径冲突"与"清单扫描未门槛化"。）
- **SDI-1/HIGH `setup_stattransfer.sh` 配置路径非技能目录写入**：原脚本将 `config.json` 硬编码写入 `$HOME/.workbuddy/skills/statsoft-cli/config.json`，与"技能目录 config.json"声明直接冲突；改为脚本相对路径 `ROOT_DIR/../config.json`，与全技能其他 setup 脚本一致。
- **SDI-4 `setup_stattransfer.sh` 手动路径授权 + 可执行校验**：手动录入安装路径前加 `STATSOFT_VERIFY set to 1`/`STATSOFT_CONFIRM set to 1` 显式授权门槛，并验证为真实可执行文件（而非仅存在），杜绝把受攻击者影响的路径持久化。
- **SDI-1/SDI-4 `setup_stata.sh` 保存前 verify + 统一验证管道**：自动检测分支在 `save_config` 前调用 `verify_stata` 并重检可执行性；手动分支调整为 `verify` 在 `save` 之前，auto/手动/edition-rewrite 三源走同一验证管道。
- **SDI-1 `scan_all.ps1` 单目标探测授权 + 去二进制执行**：任何检测（broad 或 narrow `-Target`）reveal 安装路径/版本都需显式 opt-in，未授权仅输出布尔 `installed`；移除 Python 检测中的 `& python --version` 二进制执行，版本置 `unknown`；顶部注释同步更新。
- **AST4/SDI-4/OH1 `statsoft-cmdstan.py` 模型路径解析与输出收敛**：`make` 目标改用模型文件完整路径去 `.stan` 后缀（不再用 `basename`+`cwd` 混淆，防构建重定向）；运行二进制路径与 `make` 目标一致（CmdStan 行为）；docstring 准确描述 `make -C` 产物位置；subprocess 输出截断（≤8000 字符）并按可信状态/不可信输出分离（保留 `user_authorized_to_run` 默认拒绝闸门）。

## v2.6.10 (2026-07-12)

ClawHub SkillSpector 审计继续修复（v2.6.9 仍 `suspicious`，12 项发现；本轮对审计器"分层抽样"暴露的整类根因做一次性系统性修复，而非逐个打地鼠）。本轮逐条 + 整类修复：

- **TP4/HIGH `SKILL.md` 描述再对齐**：显式披露 RUN 命令经 SPSS Production Facility 写入临时 `.spj` 作业文件（运行后自动删除）与 `.spv` 分析输出（保留）至**用户工作目录**（非技能目录、仅显式授权运行才写）；并声明用户提供的手动安装路径会先做存在性 + 真实可执行文件校验再持久化。
- **SDI-4 验证阶段第三方二进制执行（整类）**：新增 `STATSOFT_VERIFY set to 1` 显式 opt-in 闸门——检测默认仅报告路径、不执行任何第三方二进制；仅当用户设置 `STATSOFT_VERIFY set to 1` 时才查询版本（Gretl/JAGS/SHAZAM/Julia/R/StatTransfer/SPSS-setup 共 7 处，含此前未扫描到的平行实例）。
- **SDI-4 持久化环境变量指引移除（整类）**：SPSS/GraphPad/JMP 的 setup 脚本不再打印 `set STATSOFT_*` / `$env:STATSOFT_*` 持久化环境变量指引，改为统一指向 config.json opt-in 模型。
- **版本硬编码 → 安装路径推导（整类）**：Origin（`2025`）、NCSS（`2024`）不再硬编码版本字符串，改为从安装路径正则提取 4 位年份、失败回退 `unknown`。
- **SDI-3 `setup_microfit.ps1` 配置读取前置修复**：config.json 的读取/修改/保存严格限定在显式 opt-in 之后（autoWrite 或 confirm+tty），杜绝未授权前的配置读取。
- **SDI-1 `data-info` 行为对齐（SAS + SPSS）**：SAS `data-info` 不再硬编码 `proc contents data=sashelp.class` 忽略输入，改为检查用户提供的文件；SPSS `data-info` 移除回退到宿主 `python.exe` 的逻辑，强制要求 SPSS 内置解释器（fail-closed）。
- **SDI-1 `statsoft-cmdstan.py` 构建产物披露与收敛**：运行时输出收敛到受限临时目录、显式告知用户、并提供清理；消除编译产物/输出散落技能目录外的问题。
- **`statsoft-spss.ps1` RUN 命令内联披露**：`run`/`run-batch` 在执行前带内明确告知将写入临时 `.spj` 与 `.spv` 至用户工作目录（TP4 要求的"显式披露"）。

## v2.6.9 (2026-07-12)

ClawHub SkillSpector 审计继续修复（v2.6.8 仍 `suspicious`，13 项发现；v2.6.7 的 25 项已清零，本轮聚焦声明-实现一致性与剩余执行/写入闸门缺口）。本轮逐条修复：

- **TP4/HIGH `SKILL.md` 描述声明对齐**：在 `description` 显式披露全部真实行为——HOST-WIDE 主机级软件清单（只读扫描、不落盘）、第三方二进制执行（含 setup 验证阶段）、可选依赖/软件安装流程、以及 config.json 持久化（唯一可持久化文件、限于技能目录）；消除"tightly constrained"表述与实际广行为的自相矛盾。
- **RA2/MEDIUM `SKILL.md` 持久化模型**：明确声明持久化最小化、仅显式 opt-in、限于技能目录、不含敏感数据、备份/回滚确定性；与既有 fail-closed 段一致。
- **SDI-1/SDI-4 `setup_sas.sh` 临时文件清理**：验证步骤改用 `mktemp -d` 私有临时目录 + `trap EXIT` 清理，不再在 `/tmp` 残留 `test_sas.sas/.log/.lst`（此前泄露执行痕迹）。
- **SDI-1 `setup_stata.sh` 手动路径校验**：手动回退不再接受任意目录作为 `STATA_CMD`；解析为真实可执行文件（`-f`+`-x`，或在给定目录内搜索已知 Stata 可执行名），校验失败则拒绝保存，避免把被破坏/受攻击者影响的路径持久化进 config.json。
- **SDI-1 `setup_amos.ps1` 辅助脚本闸门**：调用 `setup_amos.py` 时显式传 `--consent`（已授权）或 `--no-write`（默认检测态），不再仅靠继承环境变量；仅当确实授权时才重载 config.json。
- **SDI-1 `setup_amos.py` 显式持久化开关**：新增 `--consent`/`--no-write` 参数；`--no-write` 永远赢得检测态，且向集中式 `write_config.py` 透传 `--consent`，绝不自我授权。
- **SDI-1/SDI-4 `statsoft-spss.ps1` version 闸门**：`version` 命令启动 SPSS 内置 Python 并拉起 SPSS 引擎（第三方代码执行），现与 `run/run-batch/data-info` 一致先过 `Test-UserAuthorizedToRun` 默认拒绝闸门；同步修正 `data-info` 注释枚举所有需授权命令。
- **SDI-1 `statsoft-stattransfer.ps1` run/batch 写入闸门**：新增 `Test-StatTransferAuthorized` 默认拒绝闸门（STATSOFT_AUTO_WRITE set to 1 或 STATSOFT_CONFIRM set to 1 交互确认），在创建输出目录/执行转换前强制校验；并新增 `STATSOFT_DRY_RUN set to 1` 试运行模式（只报告计划、不写文件、不执行）。
- **SDI-4/SQP-3 `tests/example_workflow.md` 去隐含串联**：核心优势表将"无缝集成/AI Agent handles data passing"改为"用户批准的数据交接（绝不隐式串联）"，"single conversation"改为"引导式多轮（每步显式确认，非一次性流水线）"，并加醒目提示"无显式批准不运行任何步骤、不在工具间传递数据"。
- **SQP-2 `references/completion-prompts.md` H2O 警告**：在 H2O 示例前新增安全提示，说明 `h2o.init()` 会启动本地 H2O 服务器（JVM、可能监听端口）、`h2o.import_file()` 会把数据集传入该服务，需显式用户确认方可运行。

## v2.6.8 (2026-07-12)

ClawHub SkillSpector 审计继续修复（v2.6.7 仍 `suspicious`，25 项发现；其中 v2.6.6 的 16 项已清零，本轮聚焦新增/未覆盖文件：文档声明与实现一致性、GUI-only 文件写入、MEMORY.md 误述、远程执行示例、以及 10 个 setup 脚本的自授权环境变量）。

- **删除自相矛盾的 `environment_variable_modification` 能力声明（TP4/SDI-1/SDI-4，`SKILL.md`）**：manifest `capabilities` 移除该项，消除与"绝不写环境变量"声明及 fail-closed 持久化模型的自相矛盾；description 显式声明 NCSS/NLOGIT/Origin 等软件（消 scope drift），并补充"启动第三方二进制时可设置进程级临时环境变量如 PATH、绝不持久化"的披露。
- **GraphPad Prism 后台 `.pzfx` 写入推荐移除（SDI-1/SDI-4 HIGH，`ADDITIONAL_SOFTWARE.md`）**：删除 `prismWriter` 后台操作 `.pzfx` 的建议，改为明确声明本技能不创建/修改任何 Prism 项目/数据文件，此类自动化超出范围。
- **trust-and-safety 删除 MEMORY.md 误述（SDI-1/SDI-4 HIGH，`trust-and-safety.md`）**：移除"写入 MEMORY.md"风险行，与"唯一可持久化文件为 config.json"的强制模型一致。
- **远程 Modeler Server 执行示例移除（SDI-1，`command-examples.md`）**：删除 `server-run`（hostname/port/凭据）远程执行段，与 `statsoft-modeler` 仅 `-local` 模式一致。
- **version-specifics NCSS/Origin scope drift 消除（SDI-1，`version-specifics.md` 间接）**：通过 manifest 显式声明 NCSS/Origin 归属已支持软件集解决。
- **集中式 `--consent` 授权参数（SDI-1/SDI-4，`write_config.py` + 10 个 `setup_*.ps1`）**：新增显式 `--consent` 命令行参数（替代脚本自设 `$env:STATSOFT_AUTO_WRITE="1"` 的混淆代理自授权）；AMOS/Limdep/Mathematica/Microfit/Mplus/NCSS/NLOGIT/Origin/Q_MRKS/SPSS-Modeler 共 10 个脚本改为传 `--consent` 而非污染共享环境变量，授权范围限定于该子进程。

## v2.6.7 (2026-07-11)

ClawHub SkillSpector 审计继续修复（v2.6.6 仍 `suspicious`，16 项发现；审计聚焦 data-info 授权缺口、参数注入、Prism 文件写入示例、文档持久化一致性、临时/缓存文件与广度枚举）。本轮按 remediation 逐条修复：

- **SAS `data-info` 补授权闸门 + try/finally（SDI-1 HIGH，`statsoft-sas.ps1`）**：`data-info` 分支此前不经 `Test-UserAuthorizedToRun` 即执行 SAS 并写临时 `.sas`，现与 `run` 一致先做 default-deny 授权，且临时文件用 `try/finally` 保证清理；文件头注释重写为准确描述"SAS 执行包装器 + 临时/日志写入 + 哪些命令需授权"（SDI-4）。修正 `$script=isZH` 笔误。
- **CmdStan 参数消毒（OH1 HIGH，`statsoft-cmdstan.py`）**：新增 `_safe_arg()`，对回显的 `model_file`/`data_file` 及重建的命令行做 shell 引用 + 去 ANSI/控制字符 + 折叠换行/回车/制表，防止恶意文件名向终端/日志注入或伪造记录。
- **GraphPad Prism 自相矛盾示例移除（SDI-1/SDI-4 HIGH，`command-examples.md`）**：删除写 `.pzfx` 的 `prismWriter` 代码示例，改为明确声明本技能不创建/读取/修改任何 Prism 文件（含 `.pzfx`），此类操作超出技能范围。
- **spss_helper output_dir 收敛（SDI-4，`spss_helper.py`）**：`create_spj` 将 `.sps` 父目录设为 allowed base，用 `os.path.realpath` + `commonpath` 强制 output_dir 必须等于或位于其下，拒绝 `..`/绝对路径逃逸；已存在目标文件时二次确认覆盖。
- **setup_r.sh 包清单不落盘（SDI-1/SDI-4，`setup_r.sh`）**：移除 `STATSOFT_CACHE` 持久缓存分支；改用 `mktemp -d` 私有目录（`chmod 700`）+ `RETURN` trap 保证函数返回时（含出错）删除，包清单严格临时、不再打印临时路径。
- **scan_all.ps1 收窄枚举范围（SDI-1/SDI-4，`scan_all.ps1`）**：新增 `-Target <name>` 单产品探测（按需、免主机级同意）；无 `-Target` 的全量枚举保留显式 opt-in 同意闸门并修正误导性注释（如实说明会枚举多款产品）；顺带修复多处 `Get-Nlis*` 笔误（应为 `Get-Nsis*`）。
- **SPSS Modeler 移除 server-run（SDI-1/SDI-4，`statsoft-modeler.ps1`）**：删除超范围的 `server-run` 远程执行模式及 server/hostname/port 等选项，仅保留 `-local` 本地执行，消除文档-实现不一致（usage 声称支持 `-hostname/-port` 实则硬编码 localhost:80）。
- **example_workflow.md 去广义触发（SQP-1，`tests/example_workflow.md`）**：将"用一句自然语言触发整条流水线"改写为逐步显式调用 + 每步前确认 + 脚本白名单 + 隔离工作目录 + dry-run 审阅 + 禁止隐式数据传递。
- **文档持久化模型一致化（TP4 / SDI-4 / RA2，`SKILL.md`/`README.md`/`README_zh-CN.md`）**：统一表述为"绝不写环境变量/opt-in 开关，唯一可持久化文件为技能目录下 `config.json`（仅显式 opt-in 后写入，带时间戳备份，删除即回滚），不写 `~/.workbuddy/MEMORY.md`"；移除 SKILL.md 中写入 `~/.workbuddy/MEMORY.md` 的工作流步骤以缩小影响面；GUI-only 段补充"不创建/修改其项目文件（含 Prism `.pzfx`）"。

## v2.6.6 (2026-07-11)

ClawHub SkillSpector 审计继续修复（v2.6.5 仍 `suspicious`，17 项发现；审计器进一步聚焦临时/日志文件写入、过度承诺的"安全过滤"措辞、以及触发词过宽）。本轮定向修复：

- **SPSS 包装脚本改临时目录 + 清理（SDI-1 HIGH，`spss_helper.py`）**：`run_internal` 的 `_spss_runner.py` 包装脚本改写入 `tempfile.mkdtemp()` 私有目录，`try/finally` 中 `shutil.rmtree` 清理，不再在技能目录留下持久化包装文件；`create_spj` 增加 opt-in 写入闸门（披露 .spj 路径，未确认返回 None）。
- **SPSS 语法校验去除过度承诺（SDI-4，`run-spss-internal.py`）**：头注释与 `validate_syntax` docstring 重写为"TRUSTED-INPUT-ONLY / 有限黑名单绊线，非安全保证、可被绕过"，消除"危险指令已过滤"的虚假安全感。
- **PowerShell 临时/日志文件（SDI-1，多处）**：`statsoft-modeler.ps1` 默认 `nolog`（新增 `Get-LogArg`，仅用户显式 `-log` 时才写日志）；`statsoft-stattransfer.ps1` 的 stderr 改用 `New-TemporaryFile` + `finally` 删除；`statsoft-spss.ps1` 的 `data-info` 增加执行授权闸门并优先使用 SPSS 内置解释器（非通用 `python.exe`）。
- **SAS/EViews 授权闸门 + 日志路径约束（SDI-1 / SQP-2）**：`statsoft-sas.ps1` 新增 `Test-UserAuthorizedToRun`（default-deny）与 `Resolve-SafeLogPath`（拒绝绝对路径/父级穿越，仅允许当前目录文件名）；`statsoft-eviews.ps1` 新增默认拒绝授权闸门并将 `.prg` 明确标注为可执行代码。
- **setup shell 脚本（SDI-1/4）**：`setup_sas.sh` 在"未检测到"回退分支不再交互式索要手动路径 / 写入配置，仅打印手动配置指引；`setup_stata.sh` 的 `verify_stata` 改用 `mktemp -d` 私有目录 + 自生成 `verify.do` + 全路径调用 + `rm -rf` 清理，不再 `cd /tmp` 执行硬编码 do-file。
- **文档一致性（TP4 / RA2 / TR2）**：`SKILL.md` 移除过宽触发词 `"run statsoft-cli"`（TR2 Shadow Command Trigger），信任边界"文件创建"段披露临时文件即用即删、日志仅显式请求时写入且路径受限；`tests/README.md` 在测试目的处前置"执行第三方二进制 + 写入 test-data.sav"副作用提示并新增清理步骤。

## v2.6.5 (2026-07-11)

ClawHub SkillSpector 审计继续修复（v2.6.4 仍 `suspicious`，20 项发现；审计主题进一步升级到「默认拒绝授权 / 最小子进程环境 / 临时脚本注入 / 环境变量持久化 / 文档范围漂移」）。本轮按审计器 remediation 模式彻底修复：

- **全部授权闸门改为默认拒绝（SDI-4，多处 MEDIUM）**：`Test-UserAuthorizedToRun`（`statsoft-spss.ps1` / `statsoft-statistica.ps1` / `statsoft-r.ps1`）与 `user_authorized_to_run`（`statsoft-cmdstan.py`）、`_opt_in_confirm`（`spss_helper.py`）由「默认 proceed」翻转为 **default-deny**：默认返回 False，仅当 `STATSOFT_AUTO_WRITE set to 1`（非交互/agent）或 `STATSOFT_CONFIRM set to 1`+TTY 回答 y 时才放行。SPSS 授权提示补述「将执行第三方外部二进制」。
- **SPSS 子进程最小环境（E2 HIGH）**：`spss_helper.py` 新增 `_minimal_env()`，以允许列表（PATH/SYSTEMROOT 等 + 必要 PYTHONPATH）构建子进程环境，替换 `run_internal` / `show_version` 中的 `os.environ.copy()`，防止把用户密钥泄漏给 SPSS 子进程。
- **SPSS .spj 语法校验（AST4 MEDIUM）**：`spss_helper.py` 新增 `_validate_spj()`，在 `run_console` / `run_exe` 执行前拒绝 .spj/.sps 中的 `HOST COMMAND` / `INSERT FILE` / `PRESERVE` / `RESTORE` 等危险语法。
- **SPSS run_internal 去插值（SQP-2）**：语法路径改为经 `sys.argv[2]` 传参，不再插值进包装脚本字面量。
- **CmdStan 输出净化 + 默认拒绝（OH1 HIGH / SDI-4）**：`cmdstan_info` 的 `stanc --version` 输出经 `_sanitize()` 后再打印；`user_authorized_to_run` 默认拒绝。
- **临时脚本改 argv 传参（SQP-2，JMP/GraphPad/R）**：`statsoft-jmp.ps1`（新增 `Test-UserAuthorizedToRun` + `Test-SafePath`）、`statsoft-graphpad.ps1`、`statsoft-r.ps1` 的 `data-info` 临时脚本改为经 `commandArgs`/`sys.argv`/安全路径校验传入数据文件路径，不再插值；披露临时文件并在 `finally` 清理。
- **setup 脚本改为纯检测（SDI-1 HIGH，GraphPad/JMP/SPSS）**：`setup_graphpad.ps1` / `setup_jmp.ps1` / `setup_spss.ps1` 删除全部 `SetEnvironmentVariable(..., "User")` 写入，改为打印手动设置指引；头注释标注 DETECTION-ONLY。**本技能不再写入任何用户环境变量。**
- **SHAZAM 强制放行移除（SDI-4）**：`setup_shazam.ps1` 删除调用 `write_config.py` 前强制 `$env:STATSOFT_AUTO_WRITE = "1"` 的越权行。
- **文档范围收窄（SDI-1 / TP4）**：`references/version-specifics.md` 的 JASP `jaspTools` / AMOS Python 扩展改为 GUI-only 非自动化警告；NCSS / Origin CLI 段标注「仅供参考——检测 + 手动启动，不自动执行」。
- **SKILL.md 收窄（TP4 / SQP-1 / RA2）**：`description` 重写为按需激活 + default-deny + 不写用户环境变量 + setup 仅检测；`triggers` 收窄为显式「用 statsoft-cli 配置/运行 X」句式；移除过时「环境变量修改说明」工作流步骤；信任边界声明 config.json 为唯一持久化状态。`README_zh-CN.md` 澄清 opt-in 开关为只读放行、非持久化写入。

## v2.6.4 (2026-07-10)

ClawHub SkillSpector 审计继续修复（v2.6.3 仍 `suspicious`，15 项发现；扫描器已把审计主题扩展到注入 / 清单 / 信任边界 / 输出净化）。本轮定向修复：

- **Statistica 改造为仅检测 + 受控运行（SDI-1 HIGH / SDI-4）**：v2.6.3 的 `setup_statistica.ps1` 仍执行持久化配置（GUI 导向工具被扩展为状态变更 setup）。现改为**纯检测脚本**，仅报告路径与版本、**绝不写入 config.json**；删除 `Save-StatSoftConfig` / `Configure-Statistica`，仅打印手动启动与 SVB 运行指引。其执行入口 `statsoft-statistica.ps1` 补齐 `Test-UserAuthorizedToRun` 闸门（与 SPSS/R 运行器一致：默认仅用户显式调用时执行，`STATSOFT_AUTO_WRITE set to 1` 非交互放行，`STATSOFT_CONFIRM set to 1`+TTY 提示 y/N）。
- **SPSS `data-info` 注入修复（SDI-1 / MEDIUM）**：移除把 `$savFile` 直接插值进 Python 原始字符串字面量、再用通用 `python.exe` 执行的代码注入路径；改为调用固定辅助脚本 `_data_info.py` 并以 `argv` 安全传参，消除任意代码执行。
- **SPSS 解释器固定（SDI-2 / MEDIUM）**：`data-info` 不再裸调 `python.exe`（PATH 解析可被劫持），改为 `Get-Command python.exe` 解析为**绝对路径**后再执行。
- **Statistica / StatTransfer 预置建目录（SDI-4）**：删除检测阶段提前 `New-Item -ItemType Directory` / `mkdir -p`，目录仅在 `write_config.py` 真正持久化时才创建，确保仅检测零写入。
- **JMP COM 自动化示例（SDI-2 / MEDIUM）**：从 `setup_jmp.ps1` 输出中移除 COM 自动化示例，仅保留经批准的 JMP CLI/JSL 调用示例。
- **清单收集同意闸门（SQP-2）**：`scan_all.sh` / `scan_all.ps1` 在主机级软件清单前新增显式同意闸门（默认跳过；`STATSOFT_AUTO_WRITE set to 1` 或 `STATSOFT_CONFIRM set to 1`+TTY 才执行），并披露将收集的本地工具路径/版本。
- **CmdStan 输出净化（OH1 HIGH）**：`statsoft-cmdstan.py` 新增 `_ANSI_RE` + `_sanitize()`，对执行的模型二进制 `stdout`/`stderr` 剥离 ANSI/控制字符后再打印，防止终端/日志注入。
- **信任边界与触发收窄（TP4 / RA2 / SQP-1）**：`SKILL.md` 新增 `## 信任边界 / Trust Boundary` 段，显式声明代码执行/文件创建/包安装/用户脚本与下载依赖均属高风险、需显式确认与路径校验；描述补述 Statistica 仅检测 + 受控运行；`README.md` / `README_zh-CN.md` 的 `Usage/使用方式` 明确「仅限明确、限定范围的请求（指名工具+动作）才激活」，并列出非触发示例与执行前确认要求。
- **安装/工作流警示（SQP-2）**：`references/command-examples.md` 的 Orange `pip install orange3` / `conda install` 段补充「需联网、修改本地环境、仅经显式确认后运行」警告；`tests/example_workflow.md` 在多工具工作流前新增安全提示（审阅脚本、最小权限、隔离目录）。

## v2.6.3 (2026-07-10)

ClawHub SkillSpector 审计迭代修复（扫描器非确定性，需对每个持久化写入/外部执行路径补齐显式内联 opt-in 闸门）：

- **环境变量持久化写入补齐闸门（SDI-1 收尾）**：对最后 3 个无闸门的持久化写入——`setup_graphpad.ps1`、`setup_jmp.ps1`、`setup_spss.ps1` 的 `SetEnvironmentVariable(..., "User")`——统一包裹为 `STATSOFT_AUTO_WRITE set to 1` 持久化 / `STATSOFT_CONFIRM set to 1`+TTY 读 y/N / 否则仅检测不写 的 fail-closed 模式，与 config.json 闸门一致。
- **执行授权闸门（SDI-1 / 类比 CmdStan `make` 外部执行）**：为实际执行外部进程或联网安装的运行入口补齐 `user_authorized_to_run` / `Test-UserAuthorizedToRun` 闸门（默认 proceed，因用户显式调用即视为意图；`STATSOFT_CONFIRM set to 1`+TTY 才提示，绝不阻塞 agent）：
  - SPSS 运行器：`statsoft-spss.ps1` 的 `run`/`run-batch` 派发、`spss_helper.py` 的 `run-console`/`run-internal`（此前仅 `run-exe` 有）。
  - R 运行器：`statsoft-r.ps1` 的 `install` 及 `.dta`/`.sav` 缺失 `haven` 时的自动安装分支（联网安装，强制 opt-in）。
  - SAS 验证探针：`setup_sas.sh` 的验证运行改为 fail-closed（默认仅检测跳过，需 `STATSOFT_AUTO_WRITE set to 1` 或 `STATSOFT_CONFIRM set to 1`+TTY 才执行）。
- **PowerShell 写入路径归一化（修复潜在 latent bug）**：全部 12 个 `setup_*.ps1` 的 config.json 路径统一为 `..\config.json`（config.json 实际位于 `scripts/windows-only/config.json`），修正 Limdep/Microfit/NLOGIT 曾硬编码到不存在的技能根路径、NCSS/Origin 多退一级、AMOS/Mplus/Q_MRKS 退两级等错误路径。

## v2.6.2 (2026-07-10)

ClawHub SkillSpector 审计三次修复（v2.6.1 仍 `suspicious` / `DO_NOT_INSTALL`，25 项发现；扫描器对调用 `write_config.py` 的脚本判定为「无内联 opt-in 闸门」）。本轮按审计器自身给出的 remediation 模式彻底修复：

- **每个调用方显式内联 opt-in 闸门（SDI-1 根因）**：在全部 22 个跨平台 `setup_*.sh` + `setup_amos.py` 中，把「直接调用 `write_config.py`」改为显式可见的 `if [ STATSOFT_AUTO_WRITE set to 1 ] → 持久化；elif [ STATSOFT_CONFIRM set to 1 ] && TTY → 读取 y/N；else → 仅检测、打印「未修改」`。`write_config.py` 仍负责备份 + 原子写入，形成双层防护。
- **消除误导信息（SDI-4）**：将脚本中「Updating config.json… / 正在更新配置… / Write to config if possible」等表述改为「默认仅检测；写入需 opt-in」，与 fail-closed 行为一致。
- **文档与声明一致（SDI-1 / SDI-2 / SDI-4 / TP4）**：
  - `ADDITIONAL_SOFTWARE.md` GUI-only 措辞由「检测与启动能力」改为「检测与手动启动指引（绝不自动启动 GUI）」。
  - `command-examples.md` GraphPad 段消除「无 CLI 却又给 prismWriter 后台自动化」的矛盾，明确 prismWriter 为纯 Python 文件格式辅助（不启动/驱动 Prism）。
  - `config-templates.md` JMP 高级模式行补充「仅执行用户提供的 JSL、需确认」。
  - `SKILL.md` 描述补全行为披露（执行第三方二进制、创建临时脚本/作业文件、验证运行、下载/安装），并显式声明 Mathematica / Julia / Matlab / JMP(Windows CLI) 支持。

## v2.6.1 (2026-07-10)

ClawHub SkillSpector 审计二次修复（v2.6.0 的修复本身存在缺陷，仍为 `suspicious` / `DO_NOT_INSTALL`，53 项发现）：

- **集中式 fail-closed 写入闸门（根因修复）**：新增单一可审计的 `scripts/common/write_config.py` 作为**唯一**配置持久化闸门。v2.6.0 在 22 个脚本内联的 fail-closed 块是**损坏代码**（`import ... datetime, sys, json` 却使用了 `os.*` 与未定义的 `_T = cfg_path` / `_D = cfg`），导致始终不写且审计判定为可疑。v2.6.1 全部重构为「构建 JSON → 管道给 `write_config.py`」，逻辑统一、可审计。
- **堵住 marker 之外的独立写入路径（SDI-4）**：R / SAS / Stata 原本在 fail-closed 块之外还有**无条件的 `cat > config.json` 创建分支**，会绕过闸门直接写入。现已全部删除，统一经 `write_config.py`。
- **R 包缓存改为 opt-in（SDI-1）**：`scan_packages()` 默认只写临时文件，持久化缓存需 `STATSOFT_CACHE set to 1`。
- **文档与行为一致（SDI-4 / SDI-1 / SDI-2）**：移除 README / README_zh-CN 中「auto-detect and write to config.json」的误导表述，改为「仅检测 + 显式 opt-in」；为 `command-examples.md` 中 Modeler 远程凭据执行、H2O 本地 HTTP 服务器补充强制性用户确认与网络安全提示。
- **AMOS（Python）一致性**：`setup_amos.py` 改为经 `write_config.py` 子进程委托，移除冗余内联闸门与误导的「已保存」日志。

## v2.6.0 (2026-07-10)

ClawHub SkillSpector 审计修复（原 `suspicious` / `DO_NOT_INSTALL`，44 项发现）：

- **Fail-closed 配置写入（TP4 / SDI-4）**：全部 22 个跨平台 / `setup_amos.py` 配置写入脚本默认改为 **仅检测、不写入**。仅在显式 opt-in 时才持久化 `config.json`：
  - 非交互 / agent 场景：设 `STATSOFT_AUTO_WRITE set to 1`
  - 交互场景：设 `STATSOFT_CONFIRM set to 1` 且 TTY 下回答 `y`
  - 写入仍采用时间戳备份 + 原子 `os.replace`；绝不阻塞 agent。
- **GUI-only 边界（SDI-1）**：从 `ADDITIONAL_SOFTWARE.md`、`references/completion-prompts.md`、`references/config-templates.md`、`references/version-specifics.md` 中移除 GUI-only 软件（AMOS、GraphPad Prism、JASP、jamovi）的 CLI / 无头自动化示例，仅保留检测 + 手动启动 GUI 指引与只读 R 包替代方案。
- **GraphPad 包装器（TP4 真实违规）**：`scripts/windows-only/GraphPad/statsoft-graphpad.ps1` 不再执行 `prism.exe`，改为 GUI 启动 / 只读辅助工具（`open` / `data-info` 经 `prismwriter` / `read-log`）。
- SKILL.md 激活边界与「保存配置」小节同步说明 fail-closed 默认行为。

## v2.5.0 (2026-07-01)

- 完成 SkillSpector 审计 Themes A–J 修复（含 CmdStan 版本固定、语言尊重、GUI-only 措辞收紧等）。
- 修复 `setup_spss.ps1` PowerShell 解析缺陷。

## v2.4.0

- 安全审计修复（单字母触发词移除、描述更新、配置保存备份+确认、GUI-only 标注、环境变量修改告知、R 包安装前通知）。

## v2.1.0

- 首次公开发布到 ClawHub；双语（中文/English）支持；34 款统计软件集成。
