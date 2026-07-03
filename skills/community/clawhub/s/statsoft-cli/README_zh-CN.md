# statsoft-cli

[🇨🇳 中文 (Chinese)](./README_zh-CN.md) | [🇬🇧 English](./README.md)

---

跨平台统计软件 CLI 集成技能，用于 AI Agent（如 WorkBuddy / OpenClaw ）。

支持 34 款统计软件：SPSS Statistics、R、Stata、SAS、AMOS、CmdStan、EViews、GenStat、GraphPad Prism、Gretl、H2O.ai、JAGS、JASP、JMP、Julia、KNIME、LIMDEP、Mathematica、Matlab、Microfit、Minitab、Mplus、NCSS、NLOGIT、OpenBUGS、Orange、OriginLab Origin、OxMetrics、PSPP、Q (MRKS)、Rattle、SHAZAM、Stat/Transfer、Statistica、TSP、Tanagra、Weka、jamovi。

同一个软件支持多个版本共存，如 R4.5 和 R4.0 共存，只需要指定默认使用哪个版本即可，需要时用提示词可实现无缝切换。

注意：如果只是希望**完整读入各种统计数据文件，或在各统计数据格式之间无损转换**，强烈建议安装使用技能 **statdata-transfer**。该技能可在无相应统计软件支持的环境下，完美实现数据格式转换目的。

### 技能目的

很多统计软件都有 CLI（命令行）执行方式，但并不是每个人都会使用。本技能的目的是将这些统计软件整合到 AI 智能体环境下统一使用，从而方便统计师充分利用这些统计软件的能力。**本技能的核心价值在于盘活历史代码资产，解决 AI 工作流自动化中的可复用性难题**。在长期的项目积累中，团队已经沉淀了大量可复用的分析代码——R 的统计建模脚本、SPSS 的语法文件、SAS 的宏程序、Stata 的 do-file 等。然而，当试图将这些历史资产直接接入 AI 自动化工作流时，就需要分别提供每种统计软件合适的调用接口。本技能正是要解决这个问题——通过 AI 智能体将这些历史代码纳入统一的执行框架，使得这些代码可以作为 AI 工作流中的一个标准节点，被反复调用、组合和编排。

## 快速开始

### 一键配置

在 AI Agent 对话中触发：
```
帮我关联 SPSS 26
帮我配置 R
```

Agent 会自动检测软件路径并写入 `config.json`。

### 验证安装

```
运行 SPSS 语法：SHOW VERSION.
将 data.sav 转换为 data.dta
```

---

## 典型场景

### 1. 多软件混合工作流
同一会话中无缝调用 R 建模 + SPSS 描述统计 + Stata 数据整理。

### 2. 历史代码资产复用
将 R 脚本、SPSS 语法、SAS 宏、Stata do-file 统一纳入 AI 工作流，作为标准化节点被反复调用、组合和编排。

### 3. 数据格式转换
通过 StatTransfer 在不同统计软件间迁移数据（SAS ↔ SPSS ↔ Stata ↔ Excel）。

### 4. SPSS Statistics 无闪屏批处理
通过内置 Python 引擎（spss.StartSPSS）运行 `.sps` 语法，跳过闪屏。

### 5. SAS 批处理自动化
通过 SAS CLI 调度宏程序，生成定期报告。

### 6. SPSS Modeler 批处理
通过 `clemb.exe` 本机模式执行 `.str` 流文件。

> 📚 **所有 34 款软件的完整详情** → 参见 [`ADDITIONAL_SOFTWARE.md`](./ADDITIONAL_SOFTWARE.md)

---

## 重要说明

闪屏说明：34 款统计软件的 **CLI 模式支持程度不一**：部分软件完全由命令行驱动，另一些在使用中仍可能出现图形界面（闪屏）或必须保持 GUI 运行。具体表现因软件而异：

- ✅ **纯 CLI，无闪屏**（如 R、Stata、SAS、CmdStan、Julia、Gretl、Mathematica）
- ⚠️ **CLI 模式有短暂闪屏**（如 JMP、Minitab、EViews、Statistica）
- 🔴 **需要 GUI，无法避免**（如 AMOS、GraphPad Prism、jamovi、JASP）

配置完成后，AI 智能体会对所关联软件的行为给予具体提示。

---

## 未包含的软件

以下软件经过评估未纳入，原因如下。如需不依赖统计软件的无损数据格式转换，请使用 statdata-transfer 技能。

| 软件 | 原因 |
|------|------|
| Systat | 市场被 SPSS/R/Python 严重挤压，用户群体持续萎缩 |
| MaxStat | 定位小众，用户极少，功能有限 |
| SmartPLS | 纯 GUI 操作，无 CLI 或批处理模式 |
| WinBUGS | 功能已被 OpenBUGS 完全覆盖（均为贝叶斯 MCMC 采样） |

---

## 平台支持

### 核心软件

|软件|Windows 脚本|跨平台脚本|验证|
|-|-|-|-|
|SPSS Statistics|scripts/windows-only/SPSS/setup_spss.ps1|—|`stats.com -production silent -nologo "exit.spj"`|
|R|scripts/windows-only/statsoft-r.ps1|scripts/cross-platform/R/setup_r.sh|Rscript --version|
|Stata|—|scripts/cross-platform/Stata/setup_stata.sh|stata-mp -b do "exit"|
|SAS|scripts/windows-only/statsoft-sas.ps1|scripts/cross-platform/SAS/setup_sas.sh|sas -version|

（完整路由表含所有 26 款扩展软件包 — 详见 ADDITIONAL_SOFTWARE.md）

## 目录结构

```
statsoft-cli/
├── SKILL.md                          # 技能主文件
├── README_zh-CN.md                   # 中文 README
├── ADDITIONAL_SOFTWARE.md            # 扩展软件详细配置
├── LICENSE                           # MIT 许可证
├── config.json.example               # 配置模板
├── scripts/
│   ├── cross-platform/               # 跨平台脚本
│   │   ├── _platform-detect.sh       # 平台检测
│   │   └── scan/                      # 系统扫描脚本
│   │       └── scan_all.sh            # 批量检测 (Linux/Mac/Win)
│   └── windows-only/
│       ├── scan/
│       │   └── scan_all.ps1           # 批量检测 (Windows, 注册表)
│   │   ├── Stata/setup_stata.sh     # Stata 配置
│   │   ├── SAS/setup_sas.sh         # SAS 配置
│   │   ├── CmdStan/setup_cmdstan.sh # CmdStan
│   │   ├── Weka/setup_weka.sh       # Weka
│   │   ├── KNIME/setup_knime.sh     # KNIME
│   │   ├── jamovi/setup_jamovi.sh   # jamovi
│   │   ├── JASP/setup_jasp.sh       # JASP
│   │   ├── PSPP/setup_pspp.sh       # PSPP
│   │   ├── JAGS/setup_jags.sh       # JAGS
│   │   ├── SHAZAM/setup_shazam.sh   # SHAZAM
│   │   ├── OxMetrics/setup_oxmetrics.sh # OxMetrics
│   │   ├── TSP/setup_tsp.sh         # TSP
│   │   ├── Tanagra/setup_tanagra.sh # Tanagra
│   │   ├── Orange/setup_orange.sh   # Orange
│   │   ├── H2O/setup_h2o.sh         # H2O.ai
│   │   ├── GenStat/setup_genstat.sh # GenStat
│   │   ├── Mathematica/setup_mathematica.sh # Mathematica
│   │   ├── Rattle/setup_rattle.sh   # Rattle
│   │   ├── OpenBUGS/setup_openbugs.sh # OpenBUGS
│   │   └── Mplus/setup_mplus.sh     # Mplus (跨平台部分)
│   └── windows-only/                 # Windows 专用脚本
│       ├── SPSS/                     # SPSS 全套 (setup + helper + internal)
│       ├── JMP/                      # JMP JSL 批处理
│       ├── GraphPad/                 # GraphPad Prism
│       ├── EViews/                   # EViews 计量经济
│       ├── Statistica/               # Statistica 数据挖掘
│       ├── StatTransfer/             # Stat/Transfer 数据格式转换
│       ├── SHAZAM/setup_shazam.ps1   # SHAZAM (Windows)
│       ├── Mplus/setup_mplus.ps1     # Mplus (Windows)
│       ├── AMOS/setup_amos.ps1       # AMOS
│       ├── Q_MRKS/setup_q.ps1        # Q (MRKS)
│       ├── Limdep/setup_limdep.ps1   # LIMDEP
│       ├── NLOGIT/setup_nlogit.ps1   # NLOGIT
│       ├── Microfit/setup_microfit.ps1 # Microfit
│       ├── statsoft-r.ps1            # R Windows 包装器
│       └── statsoft-sas.ps1          # SAS Windows 包装器
├── references/                       # 参考文件
│   ├── command-examples.md           # CLI 调用示例
│   ├── version-specifics.md          # 版本差异
│   ├── completion-prompts.md         # 配置完成提示
│   └── config-templates.md           # 配置模板
└── tests/                            # 测试文件
    ├── test-syntax.sps               # SPSS 测试语法
    ├── test-job.spj                  # SPSS 生产作业
    └── run_all.py                    # 自动化测试脚本
```

## 使用方式

在 AI Agent 对话中使用自然语言触发：

```
帮我关联 SPSS 26
帮我配置 R
将 data.sav 转换为 data.dta
运行 Stata do-file
```

## 安全说明

本技能执行**高风险操作**（执行本地可执行文件、修改配置、调用网络），使用前请了解风险。SKILL.md 中有完整 Trust \& Safety 说明。

## 许可证

[MIT](LICENSE)

