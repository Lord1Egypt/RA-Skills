# 附加统计软件支持 / Additional Statistical Software Support

本文件包含 `statsoft-cli` 技能扩展的统计软件配置信息（核心软件 SPSS Statistics, R, Stata, SAS 见 SKILL.md）。

This file contains configuration information for additional statistical software in the `statsoft-cli` skill (core software SPSS Statistics, R, Stata, SAS see SKILL.md).

---

## 目录 / Table of Contents

0. [Script Routing Tables / 完整脚本路由表](#script-routing-tables--完整脚本路由表)
1. [AMOS](#amos)
2. [CmdStan](#cmdstan)
3. [EViews](#eviews)
4. [GenStat](#genstat)
5. [GraphPad Prism](#graphpad-prism)
6. [Gretl](#gretl)
7. [H2O.ai](#h2oai)
8. [JAGS](#jags)
9. [JASP](#jasp)
10. [JMP](#jmp)
11. [Julia](#julia)
12. [KNIME](#knime)
13. [LIMDEP](#limdep)
14. [Matlab](#matlab)
15. [Mathematica](#mathematica)
16. [Microfit](#microfit)
17. [Minitab](#minitab)
18. [Mplus](#mplus)
19. [NCSS](#ncss)
20. [NLOGIT](#nlogit)
21. [OpenBUGS](#openbugs)
22. [Orange](#orange)
23. [OriginLab Origin](#originlab-origin)
24. [OxMetrics](#oxmetrics)
25. [PSPP](#pspp)
26. [Q (MRKS)](#q-mrks)
27. [Rattle](#rattle)
28. [SHAZAM](#shazam)
29. [SPSS Modeler](#spss-modeler)
30. [Stat/Transfer](#stattranfer)
31. [Statistica](#statistica)
32. [Tanagra](#tanagra)
33. [TSP](#tsp)
34. [Weka](#weka)
35. [jamovi](#jamovi)

---

## 完整脚本路由表 / Script Routing Tables

### 仅 Windows / Windows Only

| 软件 / Software | 配置脚本 | CLI 包装器 | 验证 / Verify |
|-----------------|----------|-----------|--------------|
| AMOS | `scripts/windows-only/AMOS/setup_amos.ps1` | — | Check install |
| EViews | `scripts/windows-only/EViews/setup_eviews.ps1` | `scripts/windows-only/EViews/statsoft-eviews.ps1` | `EViews.exe /?` |
| GraphPad | `scripts/windows-only/GraphPad/setup_graphpad.ps1` | `scripts/windows-only/GraphPad/statsoft-graphpad.ps1` | `prism.exe -help` |
| JMP | `scripts/windows-only/JMP/setup_jmp.ps1` | `scripts/windows-only/JMP/statsoft-jmp.ps1` | `JMP.exe /R "Exit();"` |
| LIMDEP | `scripts/windows-only/Limdep/setup_limdep.ps1` | — | `limdep commands.txt` |
| Mathematica | `scripts/windows-only/Mathematica/setup_mathematica.ps1` | `scripts/cross-platform/Mathematica/setup_mathematica.sh` | `wolframscript -code "Print[1]"` |
| Microfit | `scripts/windows-only/Microfit/setup_microfit.ps1` | — | `microfit commands.txt` |
| Mplus | `scripts/windows-only/Mplus/setup_mplus.ps1` | — | `mplus model.inp` |
| NCSS | `scripts/windows-only/NCSS/setup_ncss.ps1` | — | Check install |
| NLOGIT | `scripts/windows-only/NLOGIT/setup_nlogit.ps1` | — | `nlogit commands.txt` |
| Q (MRKS) | `scripts/windows-only/Q_MRKS/setup_q.ps1` | — | Check install |
| SHAZAM | `scripts/windows-only/SHAZAM/setup_shazam.ps1` | — | `shazam commands.txt` |
| SPSS Modeler | `scripts/windows-only/SPSS/setup_modeler.ps1` | — | `clemb -local -stream test.str -execute` |
| Statistica | `scripts/windows-only/Statistica/setup_statistica.ps1` | `scripts/windows-only/Statistica/statsoft-statistica.ps1` | `Statistica.exe /?` |
| Origin | `scripts/windows-only/Origin/setup_origin.ps1` | — | `origin97 -h test.ogs` |

### 跨平台 / Cross-Platform

| 软件 / Software | 配置脚本 | CLI 包装器 | 验证 / Verify |
|-----------------|----------|-----------|--------------|
| CmdStan | — | `scripts/cross-platform/CmdStan/setup_cmdstan.sh` | Check install |
| GenStat | — | `scripts/cross-platform/GenStat/setup_genstat.sh` | `genstat --help` |
| Gretl | — | `scripts/cross-platform/Gretl/setup_gretl.sh` | `gretlcli -v` |
| H2O.ai | — | `scripts/cross-platform/H2O/setup_h2o.sh` | `h2o --help` |
| JAGS | — | `scripts/cross-platform/JAGS/setup_jags.sh` | `jags scriptfile` |
| JASP | — | `scripts/cross-platform/JASP/setup_jasp.sh` | Check install |
| Julia | — | `scripts/cross-platform/Julia/setup_julia.sh` | `julia -v` |
| KNIME | — | `scripts/cross-platform/KNIME/setup_knime.sh` | Check install |
| Mathematica | — | `scripts/cross-platform/Mathematica/setup_mathematica.sh` | `wolframscript -code "Print[1]"` |
| Matlab | — | `scripts/cross-platform/Matlab/setup_matlab.sh` | `matlab -batch "exit"` |
| Minitab | — | `scripts/cross-platform/Minitab/setup_minitab.sh` | `Minitab -?` |
| Mplus | — | `scripts/cross-platform/Mplus/setup_mplus.sh` | `mplus model.inp` |
| OpenBUGS | — | `scripts/cross-platform/OpenBUGS/setup_openbugs.sh` | `openbugs --help` |
| Orange | — | `scripts/cross-platform/Orange/setup_orange.sh` | `orange-canvas --help` |
| OxMetrics | — | `scripts/cross-platform/OxMetrics/setup_oxmetrics.sh` | `oxmetrics --help` |
| PSPP | — | `scripts/cross-platform/PSPP/setup_pspp.sh` | Check install |
| Rattle | — | `scripts/cross-platform/Rattle/setup_rattle.sh` | `rattle --cli` |
| SHAZAM | — | `scripts/cross-platform/SHAZAM/setup_shazam.sh` | `shazam commands.txt` |
| Stat/Transfer | `scripts/cross-platform/StatTransfer/setup_stattransfer.sh` | `scripts/windows-only/StatTransfer/statsoft-stattransfer.ps1` + `st` (built-in) | `st -v` |
| TSP | — | `scripts/cross-platform/TSP/setup_tsp.sh` | `tsp commands.txt` |
| Tanagra | — | `scripts/cross-platform/Tanagra/setup_tanagra.sh` | `tanagra --help` |
| Weka | — | `scripts/cross-platform/Weka/setup_weka.sh` | Check install |
| jamovi | — | `scripts/cross-platform/jamovi/setup_jamovi.sh` | Check install |

---

## AMOS

### 简介 / Introduction

AMOS 是结构方程模型（SEM）软件，属于 SPSS 家族产品，Windows-only。安装后在开始菜单中可找到，运行时会显示 GUI 图形界面。

AMOS is a Structural Equation Modeling (SEM) software from the SPSS family, Windows-only. After installation, it can be found in the Start Menu, and displays a GUI when running.

### 平台支持 / Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ❌（无 CLI） | ⚠️⚠️⚠️ 全程 GUI |
| macOS | ❌ | ❌ | — |
| Linux | ❌ | ❌ | — |

### 配置完成提示 / Configuration Completion Notes

- ⚠️⚠️⚠️ AMOS 没有 CLI 模式，调用时会弹出 GUI 界面（无法避免）/ No CLI mode — GUI launches when called (unavoidable)
- 💡 适合结构方程模型（SEM）、路径分析和验证性因子分析/ Suitable for SEM, path analysis, confirmatory factor analysis

---

## CmdStan

### 简介 / Introduction

CmdStan 是 Stan 统计平台的命令行接口，纯 CLI 支持，完全无闪屏，用于贝叶斯 MCMC 采样。

CmdStan is the command-line interface for the Stan statistical platform, pure CLI support, completely splash-free, for Bayesian MCMC sampling.

### 平台支持 / Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ✅ | ✅ | ❌ |
| Linux | ✅ | ✅ | ❌ |

### 配置完成提示 / Configuration Completion Notes

- ✅ CmdStan 是纯 CLI 工具，完全无 GUI，无闪屏/ Pure CLI tool, completely GUI-free, no splash screen
- ✅ 适合贝叶斯统计建模和 MCMC 采样/ Suitable for Bayesian statistical modeling and MCMC sampling
- 💡 通过 R 包 `rstan` 或 Python 包 `cmdstanpy` 也可以调用 Stan/ Can also use R `rstan` or Python `cmdstanpy` to call Stan

---

## EViews

### 简介 / Introduction

EViews 是计量经济学时间序列分析软件（Windows-only），有 CLI 支持（批处理模式），可能有闪屏。

EViews is an econometrics time series analysis software (Windows-only), has CLI support (batch mode), may have splash screen.

### 平台支持 / Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ✅（批处理模式 / batch mode） | ⚠️ 可能有闪屏 / May have splash screen |
| macOS | ❌ | ❌ | — |
| Linux | ❌ | ❌ | — |

### 批处理命令 / Batch Command

```powershell
# 运行 EViews 程序文件
"EViews.exe" "program.prg" /r
```

### 配置完成提示 / Configuration Completion Notes

- ⚠️ EViews 批处理模式可能有闪屏/ EViews batch mode may have splash screen
- ⚠️ Windows-only，不支持 macOS 和 Linux/ Windows-only, no macOS/Linux support
- 💡 适合时间序列分析、回归和预测/ Suitable for time series analysis, regression, forecasting

---

## GenStat

### 简介 / Introduction

GenStat 是农业统计与数据分析软件，纯 CLI 支持，完全无闪屏。

GenStat is an agricultural statistics and data analysis software, pure CLI support, completely splash-free.

### 平台支持 / Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ✅ | ✅ | ❌ |
| Linux | ✅ | ✅ | ❌ |

### 配置完成提示 / Configuration Completion Notes

- ✅ GenStat 是纯 CLI 工具，完全无 GUI，无闪屏/ Pure CLI tool, completely GUI-free, no splash screen
- 💡 适合农业统计、试验设计和数据分析/ Suitable for agricultural statistics, experimental design, data analysis

---

## GraphPad Prism

### 简介 / Introduction

GraphPad Prism 是科学绘图与统计分析软件，**没有 CLI 模式**，调用时会弹出 GUI 界面（无法避免）。

GraphPad Prism is scientific graphing and statistical analysis software, **does not have a CLI mode** — calling it will launch the GUI (unavoidable).

### 平台支持 / Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ❌（无 CLI） | ⚠️⚠️⚠️ 全程 GUI |
| macOS | ✅ | ❌（无 CLI） | ⚠️⚠️⚠️ 全程 GUI |
| Linux | ❌ | ❌ | — |

### 安装路径 / Installation Paths

**Windows**:
- `C:\Program Files\GraphPad\Prism 8\prism.exe`
- `C:\Program Files\GraphPad\Prism 9\prism.exe`
- `C:\Program Files\GraphPad\Prism 10\prism.exe`

**macOS**:
- `/Applications/GraphPad Prism.app/Contents/MacOS/GraphPad Prism`

### 调用命令 / Invocation Command

```powershell
# Windows — 会弹出 GUI
"prism.exe" "file.pzfx"
```

### ⚠️ 重要限制 / Important Limitation

GraphPad Prism **没有 CLI 模式**，调用时会弹出 GUI 界面。这与 SPSS（Production Facility）、R（Rscript）、Stata（batch mode）不同。

### 替代方案 / Alternatives

- Python prismWriter — 后台操作 .pzfx 文件，无需 GUI

### 配置完成提示 / Configuration Completion Notes

- ⚠️⚠️⚠️ GraphPad Prism **没有 CLI 模式**，调用时会弹出 GUI 界面（无法避免）/ No CLI mode — GUI launches when called (unavoidable)
- 💡 替代方案：使用 Python `prismWriter` 库后台操作 .pzfx 文件（无需 GUI）/ Alternative: Use Python prismWriter to manipulate .pzfx files in background

---

## Gretl

### 简介 / Introduction

Gretl 是免费跨平台计量经济学软件，纯 CLI 支持，完全无闪屏。

Gretl is a free, cross-platform econometrics software with pure CLI support, completely splash-free.

### 平台支持 / Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ✅ | ✅ | ❌ |
| Linux | ✅ | ✅ | ❌ |

### 批处理命令 / Batch Command

```bash
# 运行脚本
gretlcli -b script.inp
```

### 配置完成提示 / Configuration Completion Notes

- ✅ Gretl 是纯 CLI 工具，完全无 GUI，无闪屏/ Pure CLI tool, completely GUI-free, no splash screen
- ✅ 免费软件，适合计量经济学分析/ Free software, suitable for econometrics analysis

---

## H2O.ai

### 简介 / Introduction

H2O.ai 是自动机器学习平台，纯 CLI 支持，完全无闪屏。

H2O.ai is an automated machine learning platform, pure CLI support, completely splash-free.

### 平台支持 / Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ✅ | ✅ | ❌ |
| Linux | ✅ | ✅ | ❌ |

### 配置完成提示 / Configuration Completion Notes

- ✅ H2O.ai 是纯 CLI 工具，完全无 GUI，无闪屏/ Pure CLI tool, completely GUI-free, no splash screen
- 💡 适合自动机器学习、深度学习和预测分析/ Suitable for AutoML, deep learning, predictive analytics

---

## JAGS

### 简介 / Introduction

JAGS（Just Another Gibbs Sampler）是贝叶斯 MCMC 采样软件，纯 CLI 支持，完全无闪屏。

JAGS (Just Another Gibbs Sampler) is a Bayesian MCMC sampling software, pure CLI support, completely splash-free.

### 平台支持 / Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ✅ | ✅ | ❌ |
| Linux | ✅ | ✅ | ❌ |

### 批处理命令 / Batch Command

```bash
jags scriptfile
```

### 配置完成提示 / Configuration Completion Notes

- ✅ JAGS 是纯 CLI 工具，完全无 GUI，无闪屏/ Pure CLI tool, completely GUI-free, no splash screen
- 💡 适合贝叶斯统计建模，语法与 WinBUGS/OpenBUGS 兼容/ Suitable for Bayesian modeling, syntax compatible with WinBUGS/OpenBUGS

---

## JASP

### 简介 / Introduction

JASP 是开源统计分析软件，提供经典和贝叶斯统计方法。运行时需要 GUI 界面。

JASP is an open-source statistical analysis software offering both classical and Bayesian statistical methods. Requires GUI to run.

### 平台支持 / Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ❌（无纯 CLI） | ⚠️⚠️⚠️ 需 GUI |
| macOS | ✅ | ❌（无纯 CLI） | ⚠️⚠️⚠️ 需 GUI |
| Linux | ✅ | ❌（无纯 CLI） | ⚠️⚠️⚠️ 需 GUI |

### 配置完成提示 / Configuration Completion Notes

- ⚠️⚠️⚠️ JASP 运行时需要 GUI 界面，无法完全避免闪屏/ JASP requires GUI, cannot fully avoid splash screen
- 💡 适合学术研究和教学，界面友好/ Suitable for academic research and teaching, user-friendly interface

---

## JMP

### 简介 / Introduction

JMP 是 SAS 旗下的交互式可视化统计软件，支持 JSL 脚本批处理（`/R` 参数），运行时会有短暂闪屏（1-2秒）。

JMP is an interactive visualization statistical software by SAS, supports JSL script batch processing (`/R` parameter), may have brief splash screen (1-2 seconds) when running.

### 平台支持 / Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ✅（`/R` 参数 / `/R` parameter） | ⚠️ 短暂（1-2秒 / Brief, 1-2 sec） |
| macOS | ✅ | ✅（`/R` 参数 / `/R` parameter） | ⚠️ 短暂（1-2秒 / Brief, 1-2 sec） |
| Linux | ❌ | ❌ | — |

### 安装路径 / Installation Paths

**Windows**:
- `C:\Program Files\SAS\JMP\JMP.exe`
- `C:\Program Files\JMP\JMP\JMP.exe`

**macOS**:
- `/Applications/JMP.app/Contents/MacOS/JMP`

### 批处理命令 / Batch Command

```powershell
# Windows
"JMP.exe" /R "script.jsl"

# macOS
JMP -R "script.jsl"
```

### JSL 脚本模板 / JSL Script Template

```jsl
// script.jsl — JMP 脚本
Clear Log();

// 读取数据
dt = Open("data.csv");

// 分析
[分析平台](
    Y(:column1),
    X(:column2)
);

// 保存结果
Save(dt, "results.jmp");
Close(dt, NoSave);

// 退出（批处理模式）
Exit();
```

### ⚠️ 弹窗问题 / Splash Screen Issue

JMP 是 GUI 应用程序，即使使用 `/R` 批处理模式，运行时仍**可能显示启动闪屏**（splash screen）。闪屏持续时间很短（1-2秒），脚本执行完毕后 JMP 会自动关闭（如果脚本末尾有 `Exit();`）。

### 注意事项 / Notes

- ⚠️ **脚本末尾必须加 `Exit();`**，否则 JMP GUI 会保持打开
- **与 GraphPad 对比**：GraphPad 完全无 CLI，JMP 有 CLI（`/R` 参数），可以批处理

### 配置完成提示 / Configuration Completion Notes

- ⚠️ JMP 运行时会有短暂闪屏（1-2秒），无法完全避免
- ⚠️ 脚本末尾必须加 `Exit();`

---

## Julia

### 简介 / Introduction

Julia 是高性能科学计算语言，纯 CLI 支持，完全无闪屏，适合贝叶斯统计和高性能计算。

Julia is a high-performance scientific computing language, pure CLI support, completely splash-free, suitable for Bayesian statistics and high-performance computing.

### 平台支持 / Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ✅ | ✅ | ❌ |
| Linux | ✅ | ✅ | ❌ |

### 批处理命令 / Batch Command

```bash
julia script.jl
```

### 配置完成提示 / Configuration Completion Notes

- ✅ Julia 是纯 CLI 工具，完全无 GUI，无闪屏/ Pure CLI tool, completely GUI-free, no splash screen
- ✅ 高性能，适合大数据和复杂统计计算/ High performance, suitable for big data and complex statistical computing
- 💡 常用包：`Statistics`、`HypothesisTests`、`GLM`、`Turing`（贝叶斯）/ Common packages: Statistics, HypothesisTests, GLM, Turing (Bayesian)

---

## KNIME

### 简介 / Introduction

KNIME 是开源数据分析工作流平台，纯 CLI 支持（通过命令行执行工作流），完全无闪屏。

KNIME is an open-source data analytics workflow platform, pure CLI support (execute workflows via command line), completely splash-free.

### 平台支持 / Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ✅ | ✅ | ❌ |
| Linux | ✅ | ✅ | ❌ |

### 配置完成提示 / Configuration Completion Notes

- ✅ KNIME 支持命令行批处理，完全无 GUI，无闪屏/ CLI batch processing supported, completely GUI-free, no splash screen
- 💡 适合可视化工作流编排和自动化数据处理管道/ Suitable for visual workflow orchestration and automated data pipelines

---

## LIMDEP

### 简介 / Introduction

LIMDEP 是计量经济学与离散选择分析软件（Windows-only），有 CLI 支持，适合微观计量经济学研究。

LIMDEP is an econometrics and discrete choice analysis software (Windows-only), has CLI support, suitable for microeconometrics research.

### 平台支持 / Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ❌ | ❌ | — |
| Linux | ❌ | ❌ | — |

### 批处理命令 / Batch Command

```powershell
limdep commands.txt
```

### 配置完成提示 / Configuration Completion Notes

- ✅ LIMDEP 有 CLI 支持，适合计量经济学分析/ CLI support available, suitable for econometrics analysis
- ⚠️ Windows-only，不支持 macOS 和 Linux/ Windows-only, no macOS/Linux support
- 💡 适合离散选择模型、限变量模型等微观计量分析/ Suitable for discrete choice and limited dependent variable models

---

## Mathematica

### 简介 / Introduction

Mathematica 是 Wolfram Research 开发的数学计算与统计分析平台，纯 CLI 支持（`wolframscript`），完全无闪屏。可通过命令行执行 Wolfram Language 脚本，支持符号计算、数值分析、统计建模、可视化等。

Mathematica is a mathematical computing and statistical analysis platform developed by Wolfram Research, pure CLI support (`wolframscript`), completely splash-free. Executes Wolfram Language scripts via command line, supporting symbolic computation, numerical analysis, statistical modeling, and visualization.

### 平台支持 / Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ✅（`wolframscript.exe`） | ❌ |
| macOS | ✅ | ✅（`wolframscript`） | ❌ |
| Linux | ✅ | ✅（`wolframscript`） | ❌ |

### 批处理命令 / Batch Command

```bash
# 运行 Wolfram Language 脚本
wolframscript -file script.wl

# 直接执行代码
wolframscript -code "Table[i^2, {i, 10}]"

# 交互式 REPL 模式
wolframscript

# Windows 显式调用（替代 MathKernel）
"C:\Program Files\Wolfram Research\Mathematica\14.0\MathKernel.exe" -noprompt < script.m
```

### 配置完成提示 / Configuration Completion Notes

- ✅ Mathematica 是纯 CLI 工具（`wolframscript`），完全无 GUI，无闪屏/ Pure CLI tool (`wolframscript`), completely GUI-free, no splash screen
- ✅ 跨平台支持（Win/Mac/Linux）/ Cross-platform support (Win/Mac/Linux)
- 💡 适合符号数学、数值分析、统计建模和可视化/ Suitable for symbolic mathematics, numerical analysis, statistical modeling, and visualization
- ⚠️ WolframScript 是商业软件许可证，需要定期激活/ WolframScript requires a commercial license with periodic activation

---

## Matlab

### 简介 / Introduction

Matlab 是工程计算与统计软件，有 CLI 支持（`-batch` 模式），完全无闪屏（使用 `-batch` 参数时）。

Matlab is an engineering computation and statistics software, has CLI support (`-batch` mode), completely splash-free (when using `-batch` parameter).

### 平台支持 / Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ✅（`-batch`） | ❌（使用 -batch 时） |
| macOS | ✅ | ✅（`-batch`） | ❌（使用 -batch 时） |
| Linux | ✅ | ✅（`-batch`） | ❌（使用 -batch 时） |

### 批处理命令 / Batch Command

```bash
# 运行脚本（无 GUI）
matlab -batch "run('script.m')"
```

### 配置完成提示 / Configuration Completion Notes

- ✅ 使用 `-batch` 参数时完全无 GUI，无闪屏/ Completely GUI-free when using `-batch` parameter
- ⚠️ 需要 Statistics and Machine Learning Toolbox 进行统计分析/ Requires Statistics and Machine Learning Toolbox
- 💡 适合工程统计、信号处理和机器学习/ Suitable for engineering statistics, signal processing, ML

---

## Microfit

### 简介 / Introduction

Microfit 是计量经济学时间序列分析软件（Windows-only），有 CLI 支持。

Microfit is an econometrics time series analysis software (Windows-only), has CLI support.

### 平台支持 / Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ❌ | ❌ | — |
| Linux | ❌ | ❌ | — |

### 批处理命令 / Batch Command

```powershell
microfit commands.txt
```

### 配置完成提示 / Configuration Completion Notes

- ✅ Microfit 有 CLI 支持，适合计量经济学时间序列分析/ CLI support available, suitable for econometric time series
- ⚠️ Windows-only，不支持 macOS 和 Linux/ Windows-only, no macOS/Linux support

---

## Minitab

### 简介 / Introduction

Minitab 是工业统计与六西格玛软件，有 CLI 支持（批处理模式），可能有短暂闪屏。

Minitab is an industrial statistics and Six Sigma software, has CLI support (batch mode), may have brief splash screen.

### 平台支持 / Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ✅（批处理模式 / batch mode） | ⚠️ 短暂 / Brief |
| macOS | ⚠️ 有限 / Limited | ⚠️ 有限 / Limited | ⚠️ 短暂 / Brief |
| Linux | ⚠️ 有限 / Limited | ⚠️ 有限 / Limited | ⚠️ 短暂 / Brief |

### 配置完成提示 / Configuration Completion Notes

- ⚠️ Minitab 批处理模式可能有短暂闪屏/ Minitab batch mode may have brief splash screen
- 💡 适合质量控制和六西格玛项目/ Suitable for quality control and Six Sigma projects

---

## Mplus

### 简介 / Introduction

Mplus 是结构方程模型（SEM）和潜变量分析软件，有 CLI 支持，适合复杂统计建模。

Mplus is a Structural Equation Modeling (SEM) and latent variable analysis software, has CLI support, suitable for complex statistical modeling.

### 平台支持 / Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ✅ | ✅ | ❌ |
| Linux | ❌ | ❌ | — |

### 批处理命令 / Batch Command

```bash
mplus model.inp
```

### 配置完成提示 / Configuration Completion Notes

- ✅ Mplus 有 CLI 支持，适合结构方程模型和潜变量分析/ CLI support available, suitable for SEM and latent variable analysis
- 💡 适合多层次模型、增长模型、混合模型等高级统计建模/ Suitable for multilevel, growth, mixture models

---

## NCSS

### 简介 / Introduction

NCSS 是统计分析软件（Windows-only），有 CLI 支持（批处理模式），适合医疗统计、样本量计算等领域。

NCSS is a statistical analysis software (Windows-only), has CLI support (batch mode), suitable for medical statistics, sample size calculation, etc.

### 平台支持 / Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ✅（批处理模式 / batch mode） | ❌ |
| macOS | ❌ | ❌ | — |
| Linux | ❌ | ❌ | — |

### 配置完成提示 / Configuration Completion Notes

- ✅ NCSS 有 CLI 支持，适合统计分析/ CLI support available, suitable for statistical analysis
- ⚠️ Windows-only，不支持 macOS 和 Linux/ Windows-only, no macOS/Linux support
- 💡 适合医疗统计、样本量计算和数据分析/ Suitable for medical statistics, sample size calculation, data analysis

---

## NLOGIT

### 简介 / Introduction

NLOGIT 是离散选择计量经济学软件（Windows-only），有 CLI 支持，是 LIMDEP 的扩展版本。

NLOGIT is a discrete choice econometrics software (Windows-only), has CLI support, an extended version of LIMDEP.

### 平台支持 / Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ❌ | ❌ | — |
| Linux | ❌ | ❌ | — |

### 批处理命令 / Batch Command

```powershell
nlogit commands.txt
```

### 配置完成提示 / Configuration Completion Notes

- ✅ NLOGIT 有 CLI 支持，适合离散选择模型分析/ CLI support available, suitable for discrete choice analysis
- ⚠️ Windows-only，不支持 macOS 和 Linux/ Windows-only, no macOS/Linux support
- 💡 适合 Logit、Probit、Mixed Logit 等离散选择模型/ Suitable for Logit, Probit, Mixed Logit models

---

## OpenBUGS

### 简介 / Introduction

OpenBUGS 是开源贝叶斯 MCMC 采样软件，纯 CLI 支持，完全无闪屏。

OpenBUGS is an open-source Bayesian MCMC sampling software, pure CLI support, completely splash-free.

### 平台支持 / Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ✅ | ✅ | ❌ |
| Linux | ✅ | ✅ | ❌ |

### 配置完成提示 / Configuration Completion Notes

- ✅ OpenBUGS 是纯 CLI 工具，完全无 GUI，无闪屏/ Pure CLI tool, completely GUI-free, no splash screen
- 💡 适合贝叶斯统计建模，是 WinBUGS 的开源替代品/ Suitable for Bayesian modeling, open-source WinBUGS alternative

---

## Orange

### 简介 / Introduction

Orange 是开源可视化数据挖掘与机器学习软件，有 CLI 支持（基于 Python），运行时可能有图形界面。

Orange is an open-source visual data mining and ML software, has CLI support (Python-based), may display graphical interface when running.

### 平台支持 / Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ✅ | ⚠️ 可能有 / May have |
| macOS | ✅ | ✅ | ⚠️ 可能有 / May have |
| Linux | ✅ | ✅ | ⚠️ 可能有 / May have |

### 配置完成提示 / Configuration Completion Notes

- ⚠️ Orange 有 CLI 支持，但部分操作可能涉及图形界面/ CLI support available, but some operations may involve GUI
- 💡 适合可视化数据挖掘、机器学习和数据探索/ Suitable for visual data mining, ML, data exploration

---

## OriginLab Origin

### 简介 / Introduction

Origin 是专业级科学绘图与数据分析软件，全球用户超百万，在中国科研院所渗透率极高。支持 LabTalk 脚本批处理，可通过命令行执行数据分析任务。

Origin is a professional scientific graphing and data analysis software with over 1 million users worldwide, deeply embedded in Chinese research institutions. Supports LabTalk script batch processing, can execute data analysis tasks via command line.

### 平台支持 / Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ✅（LabTalk 脚本） | ❌ |
| macOS | ✅ | ⚠️ 有限 / Limited | ⚠️ 可能有 / May have |
| Linux | ❌ | ❌ | — |

### 安装路径 / Installation Paths

**Windows**:
- `C:\Program Files\OriginLab\Origin2025\Origin95.exe`
- `C:\Program Files\OriginLab\Origin2024\Origin95.exe`

### 批处理命令 / Batch Command

```powershell
# Windows — 运行 LabTalk 脚本
"origin97" -h "script.ogs"

# 或通过 Origin C 编译执行
```

### 配置完成提示 / Configuration Completion Notes

- ✅ Origin 有 LabTalk CLI 支持，完全无 GUI（-h 模式）/ LabTalk CLI support, completely GUI-free (-h mode)
- ✅ 全球百万用户，在中国科研院所使用广泛/ Over 1M users worldwide, widely used in Chinese research institutions
- 💡 适合科学绘图、数据分析和批量图形生成/ Suitable for scientific graphing, data analysis, batch figure generation

---

## OxMetrics

### 简介 / Introduction

OxMetrics 是计量经济学软件套件，纯 CLI 支持，完全无闪屏。

OxMetrics is an econometrics software suite, pure CLI support, completely splash-free.

### 平台支持 / Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ✅ | ✅ | ❌ |
| Linux | ✅ | ✅ | ❌ |

### 配置完成提示 / Configuration Completion Notes

- ✅ OxMetrics 是纯 CLI 工具，完全无 GUI，无闪屏/ Pure CLI tool, completely GUI-free, no splash screen
- 💡 适合计量经济学、金融时间序列和预测建模/ Suitable for econometrics, financial time series, predictive modeling

---

## PSPP

### 简介 / Introduction

PSPP 是 SPSS 的开源替代品，纯 CLI 支持，完全无闪屏。

PSPP is an open-source alternative to SPSS, pure CLI support, completely splash-free.

### 平台支持 / Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ✅ | ✅ | ❌ |
| Linux | ✅ | ✅ | ❌ |

### 配置完成提示 / Configuration Completion Notes

- ✅ PSPP 是纯 CLI 工具，完全无 GUI，无闪屏/ Pure CLI tool, completely GUI-free, no splash screen
- 💡 开源免费，兼容 SPSS 语法/ Open-source, SPSS syntax compatible

---

## Q (MRKS)

### 简介 / Introduction

Q (MRKS) 是市场研究分析软件（Windows-only），支持 CLI 模式执行市场研究分析。

Q (MRKS) is a market research analysis software (Windows-only), supports CLI mode for market research analytics.

### 平台支持 / Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ❌ | ❌ | — |
| Linux | ❌ | ❌ | — |

### 配置完成提示 / Configuration Completion Notes

- ✅ Q (MRKS) 有 CLI 支持，适合市场研究数据分析/ CLI support available, suitable for market research analysis
- ⚠️ Windows-only，不支持 macOS 和 Linux/ Windows-only, no macOS/Linux support
- 💡 适合调查数据分析、统计检验和报告生成/ Suitable for survey analysis, statistical testing, report generation

---

## Rattle

### 简介 / Introduction

Rattle 是 R 语言的可视化数据挖掘界面，有 CLI 支持（`--cli` 模式），适合数据挖掘任务。

Rattle is a visual data mining interface for R, has CLI support (`--cli` mode), suitable for data mining tasks.

### 平台支持 / Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ✅ | ✅ | ❌ |
| Linux | ✅ | ✅ | ❌ |

### 配置完成提示 / Configuration Completion Notes

- ✅ Rattle 有 CLI 支持（`--cli` 模式），完全无 GUI/ CLI support available (`--cli` mode), completely GUI-free
- 💡 适合数据探索、统计分析和机器学习建模/ Suitable for data exploration, statistical analysis, ML modeling

---

## SHAZAM

### 简介 / Introduction

SHAZAM 是计量经济学软件，有 CLI 支持，适合经济统计和计量分析。

SHAZAM is an econometrics software, has CLI support, suitable for economic statistics and econometric analysis.

### 平台支持 / Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ✅ | ✅ | ❌ |
| Linux | ✅ | ✅ | ❌ |

### 批处理命令 / Batch Command

```bash
shazam commands.txt
```

### 配置完成提示 / Configuration Completion Notes

- ✅ SHAZAM 有 CLI 支持，完全无 GUI，无闪屏/ CLI support available, completely GUI-free, no splash screen
- 💡 适合计量经济学、统计分析和数据处理/ Suitable for econometrics, statistical analysis, data processing

---

## SPSS Modeler

### 简介 / Introduction

SPSS Modeler 是 IBM 的数据挖掘与预测分析软件（Windows-only），通过 `clemb.exe` 命令行工具执行 .str 流文件。

SPSS Modeler is IBM's data mining and predictive analytics software (Windows-only), executes .str stream files via the `clemb.exe` command-line tool.

### 平台支持 / Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ✅（`clemb.exe`） | ❌ |
| macOS | ❌ | ❌ | — |
| Linux | ❌ | ❌ | — |

### 安装路径 / Installation Paths

**Windows**:
- `C:\Program Files\IBM\SPSS\Modeler\18.0\clemb.exe`

### 批处理命令 / Batch Command

```powershell
# 本地模式执行流文件
clemb -local -stream "model.str" -execute

# Python 脚本模式
clemb -local -pyscript "script.py" -execute
```

### 配置完成提示 / Configuration Completion Notes

- ✅ SPSS Modeler 通过 `clemb.exe` 支持纯 CLI 执行，完全无 GUI，无闪屏/ Pure CLI execution via `clemb.exe`, completely GUI-free, no splash screen
- ⚠️ Windows-only，不支持 macOS 和 Linux/ Windows-only, no macOS/Linux support
- 💡 适合数据挖掘、预测建模和机器学习流水线/ Suitable for data mining, predictive modeling, ML pipelines

---

## Stat/Transfer

### 简介 / Introduction

Stat/Transfer 是纯 CLI 数据格式转换工具，完全无 GUI，适合自动化。支持 Stata、SPSS、SAS、R、Excel 等格式互转。

Stat/Transfer is a pure CLI data format conversion tool, completely GUI-free, suitable for automation. Supports format conversion between Stata, SPSS, SAS, R, Excel, etc.

### 平台支持 / Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ✅ | ✅ | ❌ |
| Linux | ✅ | ✅ | ❌ |

### 命令行格式 / Command Line Format

```bash
# 单文件转换
"[ST_EXE_PATH]" in.sas7bdat out.dta

# 批量转换
"[ST_EXE_PATH]" in\*.sav out\*.dta

# 命令文件批处理
"[ST_EXE_PATH]" myfile.stcmd
```

### 支持格式 / Supported Formats

| 格式 | 扩展名 |
|------|--------|
| Stata | `.dta` |
| SPSS | `.sav`, `.por` |
| SAS | `.sas7bdat`, `.xpt` |
| R | `.rda`, `.rds` |
| Excel | `.xlsx`, `.xls` |
| CSV | `.csv`, `.tsv` |

### 在 AI 工作流中的角色 / Role in AI Workflow

```
历史数据（.sas7bdat）
      ↓  Stat/Transfer CLI
中间格式（.dta / .sav / .csv）
      ↓  R / Stata / SPSS CLI
分析结果
      ↓  Stat/Transfer CLI
交付格式（.xlsx / .sas7bdat）
```

### 配置完成提示 / Configuration Completion Notes

- ✅ Stat/Transfer 是纯 CLI 工具，完全无 GUI，适合自动化/ Pure CLI tool, completely GUI-free, suitable for automation
- 💡 在 AI 工作流中的角色：数据格式转换桥梁/ Role in AI workflow: data format conversion bridge

---

## Statistica

### 简介 / Introduction

Statistica 是数据挖掘与机器学习软件（Windows-only），有 CLI 支持（SVB 脚本批处理），可能有闪屏。

Statistica is a data mining and machine learning software (Windows-only), has CLI support (SVB script batch processing), may have splash screen.

### 平台支持 / Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ✅（SVB 脚本） | ⚠️ 可能有闪屏 |
| macOS | ❌ | ❌ | — |
| Linux | ❌ | ❌ | — |

### 配置完成提示 / Configuration Completion Notes

- ⚠️ Statistica 批处理模式可能有闪屏/ Statistica batch mode may have splash screen
- ⚠️ Windows-only，不支持 macOS 和 Linux/ Windows-only, no macOS/Linux support
- 💡 适合数据挖掘、机器学习和统计分析/ Suitable for data mining, ML, statistical analysis

---

## Tanagra

### 简介 / Introduction

Tanagra 是开源数据挖掘与机器学习软件，纯 CLI 支持，完全无闪屏。

Tanagra is an open-source data mining and ML software, pure CLI support, completely splash-free.

### 平台支持 / Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ✅ | ✅ | ❌ |
| Linux | ✅ | ✅ | ❌ |

### 配置完成提示 / Configuration Completion Notes

- ✅ Tanagra 是纯 CLI 工具，完全无 GUI，无闪屏/ Pure CLI tool, completely GUI-free, no splash screen
- 💡 开源免费，适合数据挖掘和机器学习教学与研究/ Open-source, suitable for data mining and ML teaching/research

---

## TSP

### 简介 / Introduction

TSP 是时间序列与计量经济学软件，有 CLI 支持，适合时间序列分析和计量建模。

TSP is a time series and econometrics software, has CLI support, suitable for time series analysis and econometric modeling.

### 平台支持 / Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ✅ | ✅ | ❌ |
| Linux | ✅ | ✅ | ❌ |

### 批处理命令 / Batch Command

```bash
tsp commands.txt
```

### 配置完成提示 / Configuration Completion Notes

- ✅ TSP 有 CLI 支持，完全无 GUI，无闪屏/ CLI support available, completely GUI-free, no splash screen
- 💡 适合时间序列分析、计量经济学和金融建模/ Suitable for time series analysis, econometrics, financial modeling

---

## Weka

### 简介 / Introduction

Weka 是开源机器学习与数据挖掘软件，纯 CLI 支持，完全无闪屏。

Weka is an open-source machine learning and data mining software, pure CLI support, completely splash-free.

### 平台支持 / Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ✅ | ✅ | ❌ |
| Linux | ✅ | ✅ | ❌ |

### 配置完成提示 / Configuration Completion Notes

- ✅ Weka 是纯 CLI 工具，完全无 GUI，无闪屏/ Pure CLI tool, completely GUI-free, no splash screen
- 💡 开源免费，适合机器学习、数据挖掘和预测分析/ Open-source, suitable for ML, data mining, predictive analytics

---

## jamovi

### 简介 / Introduction

jamovi 是开源统计分析软件，提供电子表格式数据分析界面。运行时需要 GUI 界面。

jamovi is an open-source statistical analysis software with a spreadsheet-style data analysis interface. Requires GUI to run.

### 平台支持 / Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ❌（无纯 CLI） | ⚠️⚠️⚠️ 需 GUI |
| macOS | ✅ | ❌（无纯 CLI） | ⚠️⚠️⚠️ 需 GUI |
| Linux | ✅ | ❌（无纯 CLI） | ⚠️⚠️⚠️ 需 GUI |

### 配置完成提示 / Configuration Completion Notes

- ⚠️⚠️⚠️ jamovi 运行时需要 GUI 界面，无法完全避免闪屏/ jamovi requires GUI, cannot fully avoid splash screen
- 💡 开源免费，界面友好，适合学术研究和教学/ Open-source, user-friendly, suitable for academic research and teaching

---
