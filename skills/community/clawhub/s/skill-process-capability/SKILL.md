---
name: 过程能力分析技能
slug: process-capability
displayName: 过程能力分析技能
description: 过程能力分析技能；计算CP/CPK/PP/PPK等指标，支持正态/二项分布建模，控制图/直方图/能力图可视化；用于质量工程师进行过程能力评估、数据建模或生成质量分析报告
version: 1.1.0
category: quality
author: org-jaxjwo0r
---
# 过程能力分析技能

## 任务目标
- 本技能用于:生产线过程能力评估、质量数据建模、可视化分析报告生成
- 核心能力:过程能力指标计算、分布拟合、可视化图表、数据导入导出
- 触发条件:用户提供质量数据要求分析；需要计算CP/CPK等指标；生成质量控制图或分析报告

## 前置准备
- Python环境需安装: numpy, scipy, pandas, matplotlib, openpyxl
- 数据格式要求: CSV或Excel文件，单列或多列数值型数据
- 规格限(USL/LSL)由用户提供，无规格限时仅计算统计量

## 操作步骤

### 步骤1:数据导入
- 若数据为文件路径，调用 `data_io.py` 导入数据
- 若用户提供原始数据，直接解析为列表

### 步骤2:计算过程能力指标
调用 `process_capability.py` 计算指标:
```bash
python scripts/process_capability.py --data-path ./data.csv --column quality --usl 100 --lsl 80 --sigma-level 3
```
输出包含: CP, CPK, CPu, CPl, PPM, 过程均值, 标准差等

### 步骤3:分布拟合(可选)
调用 `process_capability.py` 进行分布拟合:
```bash
python scripts/process_capability.py --data-path ./data.csv --column quality --fit-distribution normal
```

### 步骤4:生成可视化图表
调用 `quality_charts.py` 生成图表:
```bash
# 控制图
python scripts/quality_charts.py --chart-type control --data-path ./data.csv --column quality --output ./charts/control.png

# 直方图+正态拟合
python scripts/quality_charts.py --chart-type histogram --data-path ./data.csv --column quality --usl 100 --lsl 80 --output ./charts/histogram.png

# 过程能力图
python scripts/quality_charts.py --chart-type capability --data-path ./data.csv --column quality --usl 100 --lsl 80 --output ./charts/capability.png
```

### 步骤5:数据导出
调用 `data_io.py` 导出结果:
```bash
python scripts/data_io.py --action export --data '{"cp":1.33,"cpk":1.25}' --format xlsx --output ./results/report.xlsx
```

## 使用示例

### 示例1:计算标准过程能力指标
- 场景/输入: 生产线测量数据在`quality_data.csv`的`measurement`列，USL=105, LSL=95
- 预期产出: 返回CP、CPK、PP、PPK等完整指标
- 关键要点: 确保数据无缺失值；sigma-level默认3表示3σ原则

### 示例2:生成控制图分析
- 场景/输入: 连续25个测量值，需要分析过程稳定性
- 预期产出: X-bar控制图，显示上下控制限和中心线
- 关键要点: 数据点按时间顺序排列；异常点会用红色标记

### 示例3:多指标对比分析
- 场景/输入: 同时分析3个质量特性，每个有独立规格限
- 预期产出: 对比表格+能力雷达图
- 关键要点: 批量处理时使用--columns参数指定多列

## 资源索引
- 脚本:见 [scripts/process_capability.py](scripts/process_capability.py)(用途:计算CP/CPK/PP/PPK指标，支持分布拟合；参数: --data-path, --column, --usl, --lsl, --sigma-level, --fit-distribution)
- 脚本:见 [scripts/quality_charts.py](scripts/quality_charts.py)(用途:生成控制图/直方图/能力图；参数: --chart-type, --data-path, --column, --usl, --lsl, --output)
- 脚本:见 [scripts/data_io.py](scripts/data_io.py)(用途:导入CSV/Excel或导出分析结果；参数: --action, --data-path, --data, --format, --output)
- 参考:见 [references/metrics_guide.md](references/metrics_guide.md)(何时读取:需要理解各指标含义或计算公式时)

## 注意事项
- 规格限(USL/LSL)必须由用户明确提供，未提供时仅输出统计描述
- 数据量建议≥30个样本点，少于20个样本时计算结果仅供参考
- 分布拟合前建议先做正态性检验(K-S检验)
- 控制图假设数据按时间顺序排列，请确保数据顺序正确

## TRACE 测评

| 维度 | 评分 | 说明 |
|------|------|------|
| T — 可信任度 | 9/10 | 纯文档/脚本技能，无外部依赖风险，支持中文交互 |
| R — 可靠性 | 9/10 | 有异常处理说明; 输出格式明确 |
| A — 适用性 | 9/10 | 有适用范围声明; 触发条件明确 |
| C — 规范性 | 10/10 | frontmatter 完整; 文档结构清晰; 内容充分 |
| E — 有效性 | 10/10 | 输出明确; 含使用示例; 文档详尽 |
| **总分** | **47/50** | 通过 |
