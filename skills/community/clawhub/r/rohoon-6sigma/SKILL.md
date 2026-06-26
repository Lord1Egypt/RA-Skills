---
name: rohoon-6sigma
description: Rohoon Six Sigma professional support. Based on AIAG-VDA SPC Manual, MSA Manual, and Six Sigma/Lean methodology. Provides: DMAIC/DMADV tools, SPC control charts, process capability indices (Pm/Pmk, Pp/Ppk, Cp/Cpk), MSA analysis (GR&R/Bias/Linearity/Stability), DOE (Full/Partial Factorial/RSM/Taguchi), FMEA, 5S/VSM, and more. For automotive quality management, process optimization, supplier assessment.
---

# Rohoon Six Sigma Professional Support

本技能提供基于 **AIAG-VDA SPC Manual (Yellow Volume) 第 1 版，2026 年 2 月**、**AIAG MSA Manual 第 4 版**、**ISO 13053 六西格玛标准** 和 **精益方法论** 的全面质量管理支持。

## 🎯 Quick Navigation

| Need | Reference | Core Scripts |
|------|-----------|--------------|
| **🇨🇳 GB/T 36077-2025 国标评价** | [本 SKILL.md 下方](#gbt-36077-2025-中国国家标准评价框架) | - |
| **DMAIC/DMADV Tools** | [lean-six-sigma-tools.md](references/lean-six-sigma-tools.md) | - |
| **DOE Design of Experiments** | [doe-guide.md](references/doe-guide.md) | `doe_full_factorial.py`, `doe_factor_effects.py`, `doe_sn_ratio.py` |
| **SPC Control Charts** | [control-charts.md](references/control-charts.md) | `control_chart.py`, `advanced_control_charts.py` |
| **Process Capability** | [capability-indices.md](references/capability-indices.md) | `calculate_capability.py`, `excel_report.py` |
| **MSA Analysis** | [msa-reference.md](references/msa-reference.md) | `msa_grr_analysis.py`, `msa_other_studies.py` |
| **Advanced Analysis** | [lean-six-sigma-tools.md](references/lean-six-sigma-tools.md) | `advanced_control_charts.py`, `pooled_std.py` |

## Quick Start

### 📊 AIAG-VDA Standard Reports (NEW! ✨)

**⚠️ 重要 - 报告格式稳定性**

Figure 12-1/12-2/12-3 PDF 报告遵循特定的标准格式，**除非用户明确指示，否则不要修改布局、字体、表格宽度或格式**。

- 当前标准格式：
  - 英文版：`tmp/YOUR_ORIGINAL_EN.pdf` (210,401 bytes)
  - 中文版：`tmp/YOUR_ORIGINAL_v2.pdf` (258,583 bytes)
- 格式基于 AIAG-VDA SPC Manual 标准
- 如需更改格式，请先询问用户
- 标准格式参考 PDF：
  - 英文：`references/AIAG_VDA_Standard_EN_Format.pdf`
  - 中文：`references/AIAG_VDA_Standard_ZH_Format.pdf`

**统一报告生成器** - 严格遵循黄皮书标准格式

```bash
# Figure 12-1: 正态分布报告 (中文)
python3 scripts/aiagvda_unified_report.py -o report.pdf -f 12-1 -l zh

# Figure 12-1: Normal Distribution Report (English)
python3 scripts/aiagvda_unified_report.py -o report.pdf -f 12-1 -l en

# Figure 12-2: 非正态/混合分布报告
python3 scripts/aiagvda_unified_report.py -o report.pdf -f 12-2 -l zh

# Figure 12-3: 标准统计表格报告
python3 scripts/aiagvda_unified_report.py -o report.pdf -f 12-3 -l zh
```

**报告特点**:
- 20-22 个编号元素 (严格匹配黄皮书格式)
- 中英文双语支持
- 几何法能力指数 (Cp,G / Cpk,G)
- 95% 置信区间
- PPM 计算
- 专业图表 (直方图、原始值图、概率图、控制图)

### 📊 Process Capability Analysis

```bash
# Two-sided specification
python3 scripts/calculate_capability.py \
  --data "10.1,10.2,10.15,10.18,10.12,10.05,10.22,10.08,10.14,10.19" \
  --usl 10.5 --lsl 9.5 --json

# Only upper specification
python3 scripts/calculate_capability.py \
  --data "..." --usl 10.5 --json
```

### 📈 Control Charts

```bash
# Xbar-R chart (n=5)
python3 scripts/control_chart.py \
  --data "[10.1,10.2,10.15,10.18,10.12, 10.05,10.22,10.08,10.14,10.19]" \
  --chart-type Xbar-R --subgroup-size 5 --json

# I-MR chart (individual values)
python3 scripts/control_chart.py \
  --data "10.1,10.2,10.15,10.18,10.12" \
  --chart-type I-MR --json
```

### 📏 MSA GR&R Study

```bash
# 10 parts × 3 operators × 3 trials = 90 measurements
python3 scripts/msa_grr_analysis.py \
  --data "[10.1,10.15,10.12, ...]" \
  --parts 10 --operators 3 --trials 3 \
  --tolerance 0.5 --json
```

### 🧪 DOE Full Factorial

```bash
# 2^2 full factorial design
python3 scripts/doe_full_factorial.py \
  --factors 2 \
  --responses "[40,50,45,55]" \
  --analyze

# 2^3 with center points
python3 scripts/doe_full_factorial.py \
  --factors 3 \
  --responses "[45,52,48,58,46,53,49,59]" \
  --center-points 3 \
  --analyze

# Effect calculation and visualization
python3 scripts/doe_factor_effects.py \
  --design "2^3" \
  --responses "[...]" \
  --plot main-effects interaction
```

### 🧪 Taguchi S/N Ratios

```bash
# S/N ratio calculation
python3 scripts/doe_sn_ratio.py \
  --responses "[45,52,48,...]" \
  --type larger-is-better \
  --json
```

### 📊 Response Surface

```bash
# Response Surface (CCD / Box-Behnken)
python3 scripts/doe_response_surface.py --help
```

### 📊 Excel Report Generation

```bash
# Excel report
python3 scripts/excel_report.py --help
```

## 🇨🇳 GB/T 36077-2025 中国国家标准评价框架

### 七大评价维度 (总分 1000 分)

| 类目 | 条款 | 分值 | 核心要求 |
|------|------|------|----------|
| **4.1 领导力** | 4.1.1 使命/愿景/价值观/战略 | 100 | 高层领导确立愿景价值观，制定 LSS 战略支撑组织战略 |
| | 4.1.2 高层领导推进作用 | | 承诺参与、资源支持 (设施/资金/人力/时间/激励) |
| **4.2 顾客驱动** | 4.2.1 顾客需求分析 | 80 | 建立动态顾客需求收集分析体系，预测未来需求 |
| | 4.2.2 顾客响应 | | 建立响应机制，将 VOC 转化为 CTQ |
| | 4.2.3 顾客满意测评 | | 建立测评体系，识别改进机会 |
| | 4.2.4 顾客导向指标体系 | | 建立可量化指标体系，分解到职能部门 |
| **4.3 推进规划** | 4.3.1 推进规划制定 | 80 | 目标/计划/措施/资源配置，与组织战略契合 |
| | 4.3.2 推进规划部署 | | 自上而下展开，设定绩效指标 |
| **4.4 项目管理** | 4.4.1 项目选择 | 180 | 从战略层面识别改进机会，符合 SMART 原则 |
| | 4.4.2 项目团队 | | 跨职能团队，分工明确，融洽合作 |
| | 4.4.3 技术路线和工具方法 | | DMAIC/DLSS 结构化路线，选用适当工具 |
| | 4.4.4 项目计划与实施 | | 详细工作计划，节点评审 |
| | 4.4.5 项目成果测评 | | 硬收益 (财务) + 软收益 (创新/推广/社会价值) |
| | 4.4.6 项目团队合作评估 | | 团队绩效评估，成员贡献评价 |
| **4.5 评价与激励** | 4.5.1 推进绩效评价 | 100 | 对部门/人员绩效评价，及时改进 |
| | 4.5.2 激励机制 | | 奖励认可制度 + 职业发展规划 (资深黑带/黑带/绿带/黄带) |
| **4.6 基础架构** | 4.6.1 推进机构 | 220 | 推进委员会/倡导者/责任部门 |
| | 4.6.2 管理制度与流程 | | 系统化文件化制度，与现有体系融合 |
| | 4.6.3 培训体系 | | 分层培训体系 (高层/倡导者/黑带/绿带/黄带/员工) |
| | 4.6.4 沟通交流与员工参与 | | 内部沟通 + 外部交流 + 一线员工参与 |
| | 4.6.5 基础数据管理 | | 数据收集系统，测量系统能力，数据治理 |
| | 4.6.6 管理信息系统 | | 项目管理平台 + 知识管理智能化系统 (AI) |
| | 4.6.7 产业链供应链推广 | | 在供应链上开展 LSS 项目，提供培训辅导 |
| **4.7 实施成果** | 4.7.2 顾客满意 | 240 | 满意度/忠诚度/抱怨/推荐 |
| | 4.7.3 财务收益 | | 成本降低/利润率/回报率/资金周转率 |
| | 4.7.4 人力资源 | | 带级人员数量/占比/流失率，员工满意度 |
| | 4.7.5 业务过程 | | 质量/效率/合格率/周期/成本/环境/安全 |
| | 4.7.6 相关方 | | 供货合格率/及时交货率/成本 |
| | 4.7.7 组织文化与管理变革 | | 理念认同度/活动普及率 |

### DMAIC 各阶段输入、主要工作和输出

| 阶段 | 输入 | 主要工作 | 输出 |
|------|------|----------|------|
| **D 界定** | 组织战略、VOC、顾客投诉、KPI、竞争对手比较 | 确定改进机会、团队、问题描述、边界、流程图、CTQ | 改进机会、项目目标、团队任务书、SIPOC 图、项目计划 |
| **M 测量** | VOC、KPI 分解、流程、CTQ、SIPOC | 确定测量对象/方法/指标、数据清洗、MSA、过程业绩测量 | 测量指标方法、数据收集方案、MSA 报告、过程质量水平 |
| **A 分析** | 过程测量数据、MSA 报告、过程能力报告 | 测量数据分析、流程分析、根因分析、变异源分析、价值流分析 | 根因分析报告、变异源报告、价值流报告、数据分析报告 |
| **I 改进** | 原因分析报告、关键影响因素 | 改进策略、流程优化、方案评价与实施验证 | 改进备选方案、评价指标、实施评价报告 |
| **C 控制** | 改进方案、实施评价报告 | 确定控制对象、控制方法、更新文件、OCAP、知识库 | 控制方案、程序文件、OCAP、效果评价、推广计划 |

### DMADV (DLSS) 各阶段输入、主要工作和输出

| 阶段 | 输入 | 主要工作 | 输出 |
|------|------|----------|------|
| **D 界定** | 组织战略、产品/技术规划、新产品需求、VOC | 确定项目机会、跨职能团队、范围、CTQ、失效模式分析、风险评估 | 设计目标、团队任务书、CTQ 计分卡、可行性报告、项目计划 |
| **M 测量** | 团队任务书、CTQ、CTQ 计分卡 | VOC 展开为设计特征、MSA、过程能力分析、流程映射 | MSA 报告、过程能力报告、CTQ 与 CTP 测量数据、工艺流程图 |
| **A 分析** | 问题分析报告、CTQ 与 CTP 数据、工艺流程图 | 原因分析、FTA、概念设计、方案生成与筛选、可靠性分析 | 根因报告、概念设计方案、方案评估表、风险分析报告、CTQ 展开图 |
| **D 设计** | 概念设计方案、方案评估表、风险分析报告 | 系统/子系统设计、DFMEA、参数设计、公差设计、原型机制作 | 详细设计文档、参数/公差报告、实验计划、原型机、实验报告 |
| **V 验证** | 详细设计文档、原型机、实验报告 | 验证计划、试生产、供应链确认、目标验证、过程能力验证 | 完整设计报告、试生产报告、控制计划、标准化文档、项目移交书 |

### 精益六西格玛项目评分表 (满分 110 分)

| 评价维度 | 分值 | 评价标准要点 |
|----------|------|--------------|
| **项目选择** | 20 分 | 项目来源清晰 (10 分)、目标符合 SMART(5 分)、范围与团队合作 (5 分) |
| **项目的逻辑方法** | 30 分 | 逻辑思路 (15 分)、工具方法 (15 分) |
| **项目收益** | 15 分 | 目标达成、收益计算科学合理、高层认可 |
| **项目的标准化和推广应用** | 15 分 | 标准化 (5 分)、示范推广 (10 分) |
| **项目的创新性** | 10 分 | 选题新颖 (5 分)、工具方法创新 (5 分) |
| **申报资料** | 10 分 | 完整性和质量 |
| **发表效果** | 10 分 | 现场表现和发表效果 (仅项目发布时) |

### 常用工具与方法 (GB/T 36077-2025 附录 B)

#### DMAIC 各阶段工具
- **D 界定**: 头脑风暴、亲和图、树图、流程图、SIPOC、平衡计分卡、水平对比、QFD、甘特图
- **M 测量**: 因果图、散点图、MSA、过程能力分析、因果矩阵、FTA、箱线图、直方图、抽样
- **A 分析**: 假设检验、方差分析、统计分布识别、时间序列分析、价值流图、FMEA、回归分析、大数据分析、机器学习
- **I 改进**: 试验设计、数学优化、EVOP、目视管理、5S、ECRS 原则、看板、快速换型、TOC、TRIZ
- **C 控制**: SPC、防错、定置管理、SOP、控制计划、OCAP

#### DMADV 各阶段工具
- **D 界定**: 顾客需求分析、市场调查、KANO 分析、QFD、多属性决策、设计计分卡
- **M 测量**: 关系矩阵、因果图、MSA、FMEA、过程能力分析、IPO 分析、工艺计分卡
- **A 分析**: 头脑风暴、FMEA、方差分析、试验设计、TRIZ、大数据分析、机器学习、FTA
- **D 设计**: TRIZ、DFx、公理化设计、试验设计、稳健性设计、田口方法、DFMEA、数字化仿真
- **V 验证**: 模拟技术、过程能力分析、假设检验、试验验证、可靠性分析、PFMEA、SPC

### 核心术语定义 (GB/T 36077-2025)

| 术语 | 定义 |
|------|------|
| **精益六西格玛 (LSS)** | 精益和六西格玛的融合，系统化结构化业务改进与创新模式，减少波动、消除浪费、提高质量效率 |
| **精益 (Lean)** | 通过持续改进，识别和消除产品/服务/流程中的浪费/非增值作业的理念和方法 |
| **六西格玛 (Six Sigma)** | 采用统计技术及其他科学方法减少波动、降低缺陷、提升顾客满意的战略性业务改进系统方法 |
| **精益六西格玛设计 (DLSS)** | 针对顾客需求/痛点，在产品/服务/流程开发源头进行消除缺陷和减少浪费的创新设计 |
| **DMAIC** | 界定 (Define)、测量 (Measure)、分析 (Analyze)、改进 (Improve)、控制 (Control) |
| **DMADV** | 界定 (Define)、测量 (Measure)、分析 (Analyze)、设计 (Design)、验证 (Verify) |
| **倡导者 (Champion)** | 高层领导担任的推进负责人，负责规划制定、项目选择、资源分配、组织协调 |
| **资深黑带 (MBB)** | 方法和工具应用专家，协助倡导者制定规划、选择和评审项目、培训指导黑带/绿带/黄带 |
| **黑带 (BB)** | 系统掌握 LSS 方法，负责/参与项目，培训指导绿带/黄带，至少完成 2 个黑带项目 |
| **绿带 (GB)** | 掌握基本方法，负责/参与项目，培训指导黄带，至少完成 1 个绿带项目 |
| **黄带 (YB)** | 掌握基本理念和工具，负责小规模项目或参与项目 |

---

## Core Features

### 1. SPC Statistical Process Control ✅
- **7 Control Charts**: Xbar-R, Xbar-S, I-MR, CUSUM, EWMA, p/np, c/u
- **8 AIAG-VDA Out-of-Control Rules**: Automatic detection
- **🆕 Western Electric 7 Rules**: Comprehensive rule set for anomaly detection
- **Process Capability**: Cp, Cpk, Pp, Ppk, Pm, Pmk (Geometric Method)
- **🆕 Sigma Estimation**: Range (R/d₂), Std Dev (s/c₄), Pooled Std Dev (s_p)
- **Normality Tests**: Shapiro-Wilk, Anderson-Darling
- **🆕 Distribution Selection**: Normal, Binomial, Poisson, Weibull guidance
- **🆕 Nonparametric Control Charts**: Distribution-free MEC/MCE charts (Ansari-Bradley)
- **🆕 Change-Point Detection**: Single and multiple change-point monitoring
- **🆕 Multivariate SPC**: MCUSUM, MEWMA, LASSO-based charts
- **🆕 Profile Monitoring**: Linear and nonlinear profile analysis
- **🆕 Short Production Runs**: Standardized Z-MR charts for high-mix low-volume
- **🆕 Montgomery Coefficients**: A₂, D₃, D₄, d₂, c₄ tables (n=2 to 25)

### 2. MSA Measurement System Analysis ✅
- **GR&R Studies**: ANOVA method, Xbar-R method
- **Bias Study**: Accuracy assessment
- **Linearity Study**: Range consistency
- **Stability Study**: Time drift monitoring

### 3. DOE Design of Experiments ✅
- **Full Factorial**: 2^k designs (2-8 factors)
- **Fractional Factorial**: Resolution III, IV, V
- **Response Surface**: CCD, Box-Behnken
- **Taguchi Methods**: L4, L8, L9, L16, L18, L27 orthogonal arrays
- **ANOVA**: One-way, Two-way with interaction
- **🆕 Main & Interaction Effects**: Effect calculation and visualization
- **🆕 S/N Ratios**: Taguchi signal-to-noise ratio (smaller/larger/nominal-is-better)
- **🆕 Mixture Designs**: Scheffé polynomial models
- **🆕 Robust Parameter Design**: Control vs noise factors

### 4. Reports & Export ✅
- **Excel Reports**: Professional format with 3 worksheets
- **PDF Reports**: AIAG-VDA standard format
- **JSON Output**: For system integration

### 5. Advanced Analysis ✅
- **EWMA Control Charts**: Detect small shifts
- **CUSUM Control Charts**: Cumulative sum monitoring
- **Multivariate Control**: Hotelling T² charts
- **Outlier Detection**: Modified Z-score, IQR, ARIMA
- **🆕 Nonparametric MEC/MCE**: Mixed EWMA-CUSUM charts (distribution-free)
- **🆕 Change-Point Detection**: Mean and variance monitoring
- **🆕 Performance Metrics**: RMI, AEQL, PCI, ARARL
- **🆕 Short Run SPC**: Standardized charts for high-mix low-volume production
- **🆕 Capability Confidence Intervals**: 95% CI for Cp/Cpk/Pp/Ppk
- **🆕 Western Electric Rules**: 7 rules for out-of-control detection
- **🆕 Sigma Estimation Methods**: Range, Std Dev, Pooled Std Dev
- **🆕 Distribution Selection Guide**: Normal, Binomial, Poisson, Weibull

### 6. System Integration ✅
- **HTTP API**: Real-time monitoring
- **ERP/MES Integration**: CSV, Excel, JSON import/export
- **Database Support**: SQLite, PostgreSQL
- **🆕 ISA-95 B2MML**: Enterprise-control system integration

## Usage Examples

### Define Phase
```markdown
- Project Charter Template
- SIPOC Diagram
- CTQ Tree
- VOC/VOB Collection
```

### Measure Phase
```bash
# MSA GR&R Study
python3 scripts/msa_grr_analysis.py \
  --data "[...]" --parts 10 --operators 3 --trials 3 \
  --tolerance 0.5 --json

# Baseline Capability
python3 scripts/calculate_capability.py \
  --data "..." --usl 10.5 --lsl 9.5 --json
```

### Analyze Phase
```bash
# Control Chart with out-of-control detection
python3 scripts/control_chart.py \
  --data "[...]" --chart-type Xbar-R --subgroup-size 5

# Advanced Charts (CUSUM, EWMA, I-MR, MAMR, Hotelling T2)
python3 scripts/advanced_control_charts.py
```

### Improve Phase
```bash
# DOE Full Factorial
python3 scripts/doe_full_factorial.py \
  --factors 3 --responses "[45,52,48,58,46,53,49,59]" \
  --analyze

# Factor Effects
python3 scripts/doe_factor_effects.py \
  --responses "[45,52,48,58,46,53,49,59]" --json

# Response Surface
python3 scripts/doe_response_surface.py --help
```

### Control Phase
```bash
# Excel Report
python3 scripts/excel_report.py --help

# Generate test data + batch reports
python3 scripts/generate_test_data.py
python3 scripts/batch_generate_reports_v2.py
```

## Evaluation Criteria

### Process Capability
| Index | Rating | Action |
|-------|--------|--------|
| ≥ 2.0 | 🟢 Six Sigma | Maintain, can relax control |
| 1.67-2.0 | 🟢 Excellent | Maintain current state |
| 1.33-1.67 | 🟡 Good | Maintain, continuous improvement |
| 1.0-1.33 | 🟡 Marginal | Need improvement plan |
| < 1.0 | 🔴 Insufficient | Must improve, 100% inspection |

### MSA GR&R
| %GR&R | Rating | Action |
|-------|--------|--------|
| < 10% | 🟢 Acceptable | Measurement system OK |
| 10-30% | 🟡 Conditionally Acceptable | Evaluate risk |
| ≥ 30% | 🔴 Unacceptable | Must improve system |

### ndc (Number of Distinct Categories)
- ndc ≥ 5: ✅ Adequate resolution
- ndc < 5: ⚠️ Insufficient resolution

## Standards & References

### SPC Standards
- **AIAG-VDA SPC Manual (Yellow Volume)**, 1st edition, February 2026
- **ISO 22514**: Statistical methods in process management
- **ISO 3534**: Statistics - Vocabulary and symbols
- **ISO 7870**: Control charts
- **GB/T 36077-2025**: 精益六西格玛管理评价准则 (Criteria for lean six sigma management assessment)

### MSA Standards
- **AIAG MSA Manual**, 4th edition
- **ISO 22514-7**: Measurement system analysis
- **VDA 5**: Measurement process capability

### Six Sigma Standards
- **ASQ Six Sigma Body of Knowledge**
- **ISO 13053**: Six Sigma methodology (DMAIC/DMADV)
- **GB/T 36077-2025**: 精益六西格玛管理评价准则 (代替 GB/T 36077-2018)

### Quality System Standards
- **IATF 16949**: Automotive quality management
- **ISO 9001**: Quality management systems
- **GB/T 19001**: 质量管理体系 要求
- **GB/T 19580**: 卓越绩效评价准则

## Script Tools

### SPC Core
- `calculate_capability.py` - Process capability indices (Cp, Cpk, Pp, Ppk, Pm, Pmk)
- `control_chart.py` - Control charts (Xbar-R, Xbar-S, I-MR)
- `attribute_control_charts.py` - Attribute control charts (p/np/c/u/Z)
- `advanced_control_charts.py` - CUSUM, EWMA, MAMR, Hotelling T²
- `pooled_std.py` - Sigma estimation (Range, Std Dev, Pooled)
- `western_electric_rules.py` - Western Electric out-of-control rules
- `spc_calculator.py` - SPC calculations
- `spc_report.py` - SPC report generation
- `excel_report.py` - Excel report generation

### MSA
- `msa_calculator.py` - MSA calculations
- `msa_grr_analysis.py` - GR&R study (Xbar-R method)
- `msa_other_studies.py` - Bias, Linearity, Stability
- `msa_report.py` - MSA report generation

### DOE
- `doe_full_factorial.py` - 2^k full factorial designs
- `doe_response_surface.py` - CCD, Box-Behnken
- `doe_factor_effects.py` - Main and interaction effects
- `doe_sn_ratio.py` - Taguchi S/N ratio calculation
- `generate_doe_report.py` - DOE report generation

### Utilities
- `generate_test_data.py` - Generate test datasets
- `batch_generate_reports_v2.py` - Batch PDF report generation
- `data_import.py` - Data import utilities
- `demo_report_generation.py` - Demo report generation

## Version

**Current**: v1.8.0 (2026-04-13)

**Changes in v1.8.0**:
- ✅ **NEW: GB/T 36077-2025 中国国家标准整合** - 完整融入《精益六西格玛管理评价准则》
- ✅ 七大评价维度框架 (领导力/顾客驱动/推进规划/项目管理/评价与激励/基础架构/实施成果)
- ✅ DMAIC/DMADV 各阶段输入 - 主要工作 - 输出完整对照表
- ✅ 精益六西格玛项目评分表 (110 分制)
- ✅ 常用工具与方法 (按 DMAIC/DMADV 各阶段分类)
- ✅ 核心术语定义 (LSS/Lean/Six Sigma/DLSS/DMAIC/DMADV/倡导者/黑带/绿带/黄带)
- ✅ 评价准则条款赋值表 (总分 1000 分)
- ✅ 基于 GB/T 36077-2025 (代替 GB/T 36077-2018),2025-12-31 发布，2026-07-01 实施
- ✅ 支持中国组织精益六西格玛管理自我评价、相关方评价、第三方评价

**Changes in v1.7.0**:
- ✅ NEW: Real-time data stream processing for Quality 4.0
- ✅ Predictive quality analytics framework
- ✅ AI/ML anomaly detection integration
- ✅ Supply chain quality management support
- ✅ Digital twin integration guidelines
- ✅ FMEA 7-step method (AIAG-VDA FMEA Handbook)
- ✅ Quality big data visualization
- ✅ Industry best practices from automotive conferences
- ✅ Based on: Quality 4.0 conferences, automotive industry best practices

**Changes in v1.6.0**:
- ✅ NEW: Western Electric 7 rules for out-of-control detection
- ✅ Sigma estimation methods (Range R/d₂, Std Dev s/c₄, Pooled s_p)
- ✅ Extended coefficient tables (d₂, c₄ for n=2 to 25)
- ✅ Distribution selection guide (Normal, Binomial, Poisson, Weibull)
- ✅ Nonparametric multivariate control charts
- ✅ Goodness-of-fit based nonparametric EWMA
- ✅ MIL-HDBK-1916 guidance
- ✅ Based on: ASQ SPC guidelines, Western Electric rules

**Changes in v1.1.1**:
- ✅ Fixed DOE parameter parsing
- ✅ Added JSON output for EWMA
- ✅ Improved error messages
- ✅ Updated help documentation

## Support

For issues or questions:
1. Check reference documentation in `references/`
2. Run scripts with `--help` for usage
3. Review example reports in `aiagvda_standard_reports/`
4. Check test cases in `tests/` (`python3 -m pytest tests/ -v`)
5. Install dependencies: `pip install -r requirements.txt`

---

*Rohoon Six Sigma - Professional Quality Management Support*  
*Based on AIAG-VDA, ISO, and Lean Six Sigma Standards*

---

## 📊 Figure 12-3 标准格式报告生成

### 功能说明
生成符合 AIAG/VDA SPC 协调标准 Figure 12-3 格式的综合分析报告，支持中英文双语。

### 使用方式

```bash
# 1. 生成测试数据
cd ~/.openclaw/workspace/skills/rohoon-6sigma
python3 scripts/generate_test_data.py

# 2. 批量生成报告（中英文）
python3 scripts/batch_generate_reports_v2.py
```

### 输出文件
- **英文版**：`tmp/SPC_Reports_EN/*.pdf`
- **中文版**：`tmp/SPC_Reports_CN/*.pdf`

### 报告特性
- 6 列等宽表头布局
- 字段名加粗，字段值蓝色
- 单元格自动合并
- 能力指数进度条可视化
- 字体 6 号紧凑排版

### 应用场景
1. **客户审核** - 提供符合 AIAG/VDA 标准的正式报告
2. **内部培训** - 展示标准报告格式要求
3. **数据分析** - 识别过程能力问题
4. **持续改进** - 跟踪改进效果

