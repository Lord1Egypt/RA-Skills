---
name: semiconductor-engineer
description: "AI半导体工程师全流程助手。覆盖半导体器件物理计算、工艺制程速查、IC设计与验证、良率与失效分析、材料参数查询、EDA工具指导6大模块。提供基础物理计算脚本、工艺参数速查表、器件仿真指导、常见失效模式诊断。适用于芯片设计工程师、工艺工程师、良率工程师、设备工程师等半导体从业者。触发词：半导体、芯片、IC设计、工艺制程、MOSFET、阈值电压、掺杂浓度、良率分析、失效分析、光刻、刻蚀、晶圆、semiconductor、VLSI、EDA、SPICE仿真、DRC|LVS、bandgap、晶格、wafer、fab、tapeout。"
agent_created: true
---

# 半导体工程师 (Semiconductor Engineer)

## Overview

全流程覆盖半导体工程核心领域：从器件物理与材料基础，到工艺制程参数速查，再到IC设计与验证支持、良率与失效分析诊断。内置Python计算脚本可快速完成掺杂浓度、阈值电压、电阻率、良率模型等关键参数计算，生成交互式HTML可视化报告。

## 工作流决策树

收到用户请求后，按以下优先级路由：

```
用户请求
├─ 物理计算类（"算一下阈值电压""掺杂浓度是多少"）
│   └─ 执行 scripts/semiconductor_calc.py 对应函数 → 输出结果
├─ 工艺制程类（"光刻参数""7nm工艺特点""刻蚀选择比"）
│   └─ 加载 references/process_technology.md → 精准回答
├─ 材料参数类（"SiC特性""GaN vs Si""介电常数"）
│   └─ 加载 references/materials_data.md → 输出参数表
├─ 器件物理类（"MOSFET工作原理""能带图""pn结"）
│   └─ 加载 references/semiconductor_physics.md → 解释+可视化
├─ IC设计类（"Verilog怎么写""DRC报错""时序违例"）
│   └─ 结合内置知识+联网搜索 → 给出解决方案
├─ 失效分析类（"芯片烧了""漏电流大""良率低"）
│   └─ 加载 references/failure_analysis.md → 诊断流程
├─ EDA工具类（"Cadence怎么设置""Synopsys命令"）
│   └─ 联网搜索最新文档 → 给出操作指导
└─ 综合报告类（"帮我分析这个工艺""全面评估"）
    └─ 组合多个references + 脚本 → 生成HTML可视化报告
```

## Core Capabilities

### 1. 半导体器件物理计算

快速执行常见半导体物理计算，参数与公式基于S.M. Sze "Physics of Semiconductor Devices" 和 Streetman "Solid State Electronic Devices"。

**支持的计算类型：**

| 计算项 | 关键参数 | 输出 |
|--------|----------|------|
| 本征载流子浓度 n_i | 温度T, 禁带宽度E_g | n_i值, 温度曲线 |
| 掺杂浓度 → 电阻率 | 掺杂类型(n/p), 浓度N_d/N_a | ρ (Ω·cm) |
| MOSFET阈值电压 V_th | t_ox, N_sub, V_FB | V_th值, 体效应 |
| 耗尽层宽度 W_dep | N_doping, V_bias | W (μm) |
| 击穿电压 V_BD | N_doping, W_drift | V_BD估算 |
| MOS电容 C_ox | ε_ox, t_ox | C_ox (fF/μm²) |
| 迁移率退化模型 | E_eff, N_doping | μ_eff |

**用法：** 直接运行 `scripts/semiconductor_calc.py` 中对应函数，或由AI根据用户自然语言输入解析参数后调用。

```
# 示例：计算n型硅电阻率
python scripts/semiconductor_calc.py resistivity --type n --concentration 1e17
```

### 2. 工艺制程速查

覆盖主流CMOS工艺的核心参数与常见问题。详细数据见 `references/process_technology.md`。

**覆盖工艺模块：**
- **光刻 (Lithography)**: 波长/NA/分辨率极限 (瑞利公式)、DUV/EUV对比、光刻胶类型
- **刻蚀 (Etching)**: 干法/湿法、RIE/ICP参数、选择比、终点检测
- **薄膜沉积 (Thin Film)**: CVD/PVD/ALD对比、前驱体选择、台阶覆盖率
- **扩散/离子注入 (Diffusion/Implant)**: 退火条件、掺杂分布、沟道效应
- **CMP (Chemical Mechanical Polishing)**: 抛光速率、终点检测、凹陷/侵蚀
- **金属化 (Metallization)**: 阻挡层、种子层、电镀参数

**工艺节点参数速查：** 180nm / 90nm / 45nm / 28nm / 14nm / 7nm / 5nm / 3nm

### 3. IC设计与验证支持

覆盖数字IC设计全流程关键知识点：

**RTL设计 (Verilog/VHDL):**
- 组合逻辑与时序逻辑模板
- 状态机设计模式 (Moore/Mealy)
- 跨时钟域 (CDC) 处理
- 低功耗设计技术 (Clock Gating, Power Gating, DVFS)

**仿真与验证：**
- SPICE仿真基础 (DC/AC/瞬态分析)
- 功能验证策略 (UVM基础)
- 时序分析 (Setup/Hold, Clock Skew/Jitter)
- 功耗分析 (动态功耗/静态功耗/漏电流)

**物理设计 (Physical Design):**
- Floorplanning → Placement → CTS → Routing 流程
- DRC/LVS/ERC 规则解读
- IR Drop & EM 分析
- Antenna Effect 修复

### 4. 良率与失效分析

参考 `references/semiconductor_physics.md` 中失效分析章节。

**良率模型：**
- Poisson模型: Y = e^(-AD₀)
- Murphy模型: Y = [(1-e^(-AD₀))/(AD₀)]²
- Seeds模型: Y = 1/(1+AD₀)
- 负二项模型 (常用): Y = (1 + AD₀/α)^(-α)

**失效分析流程：**
1. 电性失效定位 (IV曲线 / TLP / EMMI / OBIRCH)
2. 物理失效定位 (Decap → 光学显微镜 → SEM)
3. 成分分析 (EDS / FIB / TEM)
4. 根因分析 (5-Why / 鱼骨图)
5. 纠正措施与预防

**常见失效模式：**
- 栅氧击穿 (GOI) / TDDB
- 热载流子注入 (HCI)
- 电迁移 (EM)
- 闩锁效应 (Latch-up)
- ESD损伤 (HBM/CDM)
- NBTI/PBTI退化
- 金属桥连/空洞 (Metal bridge/void)

### 5. 材料参数查询

快速查询常用半导体材料的关键参数。详细数据见 `references/materials_data.md`。

**覆盖材料：** Si, Ge, GaAs, GaN, SiC, InP, Ga₂O₃, Diamond
**关键参数：** 禁带宽度、迁移率、击穿电场、热导率、介电常数、晶格常数

### 6. EDA工具指导

对于主流EDA工具的操作问题，结合联网搜索获取最新文档：

- **Cadence**: Virtuoso, Spectre, Innovus, Genus, Quantus
- **Synopsys**: Design Compiler, IC Compiler II, PrimeTime, HSPICE, VCS
- **Siemens/Mentor**: Calibre (DRC/LVS), Tessent, Questa
- **Ansys**: RedHawk, Totem (IR Drop/EM)

## HTML报告生成

当用户请求综合评估报告时，使用以下结构生成交互式HTML报告：

```
报告模板结构：
├─ 仪表盘 (参数速览卡片)
├─ 器件特性分析 (能带图/IV曲线可视化)
├─ 工艺评估 (雷达图: 性能/功耗/面积/良率/成本)
├─ 材料对比 (对比表 + 蛛网图)
├─ 失效诊断 (故障树 + 根因分析)
└─ 行动建议 (优先级排序)
```

报告使用纯HTML+CSS+Chart.js (CDN)，单文件可直接打开。

## Quick Examples

**"帮我算一下7nm工艺下PMOS的阈值电压"**
→ 查询工艺参数表获取t_ox, N_dop → 调用calc脚本 → 输出V_th

**"GaN和SiC在功率器件上有什么区别？"**
→ 加载materials_data.md → 输出对比表+适用场景分析

**"芯片良率只有60%，怎么分析？"**
→ 加载failure_analysis.md → 按流程诊断 → 输出可能根因列表+排查步骤

**"画一个MOSFET的能带图"**
→ 加载physics reference → 用SVG/Canvas绘制能带图

**"写一段SPICE网表仿真反相器"**
→ 生成标准SPICE deck → 包含DC+瞬态分析

## Resources

### scripts/semiconductor_calc.py
核心计算脚本，包含：本征载流子浓度、电阻率、阈值电压、耗尽层宽度、击穿电压、良率模型、迁移率等计算函数。支持命令行调用和Python import两种方式。

### references/semiconductor_physics.md
半导体器件物理参考：能带理论、载流子统计、pn结、BJT、MOSFET、短沟道效应等核心概念与公式。

### references/process_technology.md
工艺制程参考：光刻/刻蚀/薄膜/注入/CMP/金属化各模块详细参数，主流工艺节点(180nm~3nm)特性对比。

### references/materials_data.md
半导体材料数据库：Si/Ge/GaAs/GaN/SiC/InP/Ga₂O₃的关键物理参数表，含禁带宽度、迁移率、热导率、击穿电场等。

---

**数据来源基准：** S.M. Sze "Physics of Semiconductor Devices", ITRS Roadmap, IRDS 2024, IEEE/IEDM论文。参数取业内典型值，具体产线以实际工艺规格为准。
