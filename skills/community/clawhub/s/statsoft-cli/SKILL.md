---
name: statsoft-cli
description: "Cross-platform statistical software CLI integration for AI Agent. Supports 34 packages: R, Stata, SAS, SPSS, Python, Bayesian, ML, and more. Bilingual (中文/English)."
triggers:
  - "SPSS"
  - "SPSS Statistics"
  - "R"
  - "R命令行"
  - "Stata"
  - "SAS"
  - "统计软件"
  - "连接统计软件"
  - "statsoft-cli"
  - "connect statistical software"
metadata:
  {
    "openclaw": { "emoji": "🛠️", "icon": "assets/icon.svg" },
    "authors": ["medstatstar", "phoe-zip"],
    "contributors": ["medstatstar", "phoe-zip"],
    "version": "2.0.0",
    "license": "MIT",
    "tags": ["统计软件", "Statistical Software", "CLI", "R", "SPSS", "Stata", "SAS", "Bayesian", "Machine Learning", "Econometrics", "SEM", "Data Mining"],
    "homepage": "https://github.com/medstatstar/statsoft-cli",
    "repository": "https://github.com/medstatstar/statsoft-cli"
  }
---

# 🛡️ 信任与安全 / Trust & Safety

> 本技能执行**高风险操作**，详见 `references/trust-and-safety.md` / This skill performs **high-risk operations**. See `references/trust-and-safety.md` for details.

**核心权限 / Core Permissions**: 本地文件读写 (config.json, temporary scripts)、进程执行 (statistical software binaries)、环境变量修改 (user-scoped)、网络访问 (CRAN/Anaconda repositories)。 / Local file read-write (config.json, temporary scripts), process execution (statistical software binaries), environment variable modification (user-scoped), network access (CRAN/Anaconda repositories).

---

## 技能目的 / Purpose

很多统计软件都有 CLI（命令行）执行方式，但并不是每个人都会使用。本技能的目的是将这些统计软件整合到 AI 智能体环境下统一使用，从而方便统计师充分利用这些统计软件的能力。**本技能的核心价值在于盘活历史代码资产，解决 AI 工作流自动化中的可复用性难题**。在长期的项目积累中，团队已经沉淀了大量可复用的分析代码——R 的统计建模脚本、SPSS 的语法文件、SAS 的宏程序、Stata 的 do-file 等。然而，当试图将这些历史资产直接接入 AI 自动化工作流时，就需要分别提供每种统计软件合适的调用接口。本技能正是要解决这个问题——通过 AI 智能体将这些历史代码纳入统一的执行框架，使得这些代码可以作为 AI 工作流中的一个标准节点，被反复调用、组合和编排。

Many statistical software packages have CLI (Command Line Interface) execution modes, but not everyone knows how to use them. This skill integrates these statistical software packages into the AI Agent environment for unified access, enabling statisticians to fully leverage these tools' capabilities. From a deeper perspective, **the core value of this skill is integrating and leveraging all statistical software resources and historical assets within AI workflows**. Over years of project accumulation, teams have gathered a wealth of reusable analysis code—R statistical modeling scripts, SPSS syntax files, SAS macro programs, Stata do-files, and more. However, when attempting to plug these historical assets directly into AI automation workflows, the challenge emerges: each statistical software requires its own appropriate invocation interface. This skill addresses exactly this issue—through the AI Agent, it brings historical code into a unified execution framework, enabling these codes to serve as standard nodes in AI workflows, repeatedly callable, composable, and schedulable.

---

## 平台支持 / Platform Support

| 类别 / Category | 软件 / Software |
|-----------------|-----------------|
| ✅ 全部平台 (Win + Mac + Linux) | R, Stata, SAS, CmdStan, GenStat, Gretl, H2O.ai, JAGS, JASP, Julia, KNIME, Mathematica, Matlab, OpenBUGS, Orange, OxMetrics, PSPP, Rattle, SHAZAM, Stat/Transfer, Tanagra, TSP, Weka, jamovi |
| ✅ Win + Mac + 有限 Linux | Mplus |
| ⚠️ Win + 有限 Mac/Linux | Minitab |
| 🔴 Windows only | SPSS Statistics, AMOS, EViews, GraphPad Prism, JMP, LIMDEP, Microfit, NCSS, NLOGIT, Origin, Q (MRKS), SPSS Modeler, Statistica |

*(详细平台支持见 `references/version-specifics.md` / Detailed platform support: `references/version-specifics.md`)*

---

## 执行工作流 / Execution Workflow

1. **检测平台 / Detect Platform** — `source scripts/cross-platform/_platform-detect.sh`
2. **扫描前确认 / Pre-scan Confirmation** — 在执行任何扫描操作前，必须向用户做出以下提示并等待用户选择 / Before any scan, MUST prompt the user and wait for their choice：
   - 提示内容 / Prompt message:
     - **中文**: "⚠️ 自动扫描系统可能耗时较长（Windows 约 30-60 秒）。如果您已知已安装的统计软件数量有限（≤3），建议直接指定软件及对应安装路径，跳过扫描。您希望如何选择？" 选项：A) 自动扫描 B) 手工指定软件路径
     - **English**: "⚠️ Auto-scan may take a while (~30s on Windows). If you have few statistical packages (≤3), you can skip scanning and specify paths directly. Your choice?" Options: A) Auto-scan B) Specify paths manually
   - 用户选择 A → 继续第 3 步系统扫描 / User selects A → proceed to step 3
   - 用户选择 B → 询问用户"希望配置哪些软件？各软件的安装路径是什么？"，跳过第 3 步，直接进入第 4 步配置 / User selects B → ask "Which software to configure? What are the installation paths?", skip step 3, go directly to step 4
3. **系统扫描 / System Scan** — 批量检测系统已安装统计软件 / Batch detect installed statistical software（仅在步骤 2 选择 A 时执行 / Execute only when step 2 = A）：
   - **Windows**: 调用 `scripts/windows-only/scan/scan_all.ps1`（注册表检测 + 路径扫描 + 命令行查找）
   - **Mac/Linux**: 调用 `scripts/cross-platform/scan/scan_all.sh`（命令查找 + 路径扫描）
   - 输出 JSON 格式：`{"R":{"installed":true,"path":"...","version":"..."},...}`
   - AI 解析输出后，向用户列出可配置的软件清单
3. **选择配置模式 / Select Config Mode**:
   - **批量配置 / Batch**: 自动配置所有检测到的软件 / Auto-configure all detected
   - **指定配置 / Specific**: 用户选择要配置的特定软件 / User selects specific software
   - **单软件配置 / Single**: 调用单个 `setup_*.ps1` / `setup_*.sh` 脚本 / Call individual setup script
4. **检测与配置 / Detect & Setup** — 按平台路由到对应脚本，非 Windows 自动隐藏不兼容软件 / Route to platform-specific script, auto-hide incompatible software on non-Windows
5. **保存配置 / Save Config** — 写入 `config.json` / Write to `config.json`
6. **写入记忆 / Write Memory** (需用户同意 / With user consent) — 询问后追加到 `~/.workbuddy/MEMORY.md` / Append to `~/.workbuddy/MEMORY.md` after confirmation
7. **输出完成摘要 / Output Completion Summary** — 按 `references/completion-prompts.md` 模板输出 / Output using `references/completion-prompts.md` template

---

## 脚本路由表 / Script Routing Table

### 核心软件 / Core Software

| 软件 / Software | Windows 脚本 | 跨平台脚本 | 验证 / Verify |
|-----------------|-------------|------------|--------------|
| SPSS Statistics | `scripts/windows-only/SPSS/setup_spss.ps1` | — | `stats.com -production silent -nologo "exit.spj"` |
| R | `scripts/windows-only/statsoft-r.ps1` | `scripts/cross-platform/R/setup_r.sh` | `Rscript --version` |
| Stata | — | `scripts/cross-platform/Stata/setup_stata.sh` | `stata-mp -b do "exit"` |
| SAS | `scripts/windows-only/statsoft-sas.ps1` | `scripts/cross-platform/SAS/setup_sas.sh` | `sas -version` |

**扩展软件 / Extended Software** (AMOS, CmdStan, EViews, GenStat, GraphPad Prism, Gretl, H2O.ai, JAGS, JASP, JMP, Julia, KNIME, LIMDEP, Matlab, Microfit, Minitab, Mplus, NCSS, NLOGIT, OpenBUGS, Orange, Origin, OxMetrics, PSPP, Q/MRKS, Rattle, SHAZAM, SPSS Modeler, Stat/Transfer, Statistica, Tanagra, TSP, Weka, jamovi, etc.) **见 `ADDITIONAL_SOFTWARE.md` / See `ADDITIONAL_SOFTWARE.md` for details**。

---

## 详细配置 / Detailed Configuration

- `ADDITIONAL_SOFTWARE.md` — 扩展软件配置（31 款）/ Extended software configuration (31 packages)
- `references/command-examples.md` — 所有支持软件的 CLI 命令示例 / CLI command examples for all supported software
- `references/version-specifics.md` — 版本差异（SPSS 26/30, R 4.5/4.1, Python 3.4/3.13）/ Version differences
- `references/completion-prompts.md` — 配置完成提示模板 / Configuration completion prompt templates
- `tests/` — `run_all.py`（自动化测试脚本）, `test-syntax.sps`, `test-job.spj` / automated test scripts

---

## 何时阅读参考文件 / When to Read Reference Files

- 版本差异问题？ → `references/version-specifics.md` / Version differences? → `references/version-specifics.md`
- 需要命令示例？ → `references/command-examples.md` / Need command examples? → `references/command-examples.md`
- 编写完成提示？ → `references/completion-prompts.md` / Writing completion prompts? → `references/completion-prompts.md`

---

## 触发短语 / Trigger Phrases

**中文**: SPSS, R, Stata, SAS, 统计软件, 连接统计软件, statsoft-cli

**English**: SPSS, R command line, Stata CLI, SAS batch, connect statistical software, statsoft-cli
