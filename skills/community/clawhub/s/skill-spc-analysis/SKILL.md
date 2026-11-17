---
name: SPC绘图及分析技能
slug: spc-analysis
displayName: SPC绘图及分析技能
description: SPC统计过程控制分析；当用户需要对制造业生产过程进行质量监控、过程稳定性评估、异常点识别、多周期数据对比分析时使用
version: 1.1.0
category: quality
author: org-jaxjwo0r
---
# SPC统计过程控制分析

## 任务目标
- 本 Skill 用于：制造业生产过程数据的统计过程控制分析，支持6种标准控制图，提供完整的HTML报告
- 能力包含：数据读取与预处理、控制图生成（Xbar-R/Xbar-S/I-MR/P/C/U）、Nelson判异规则检测、过程稳定性评估、过程能力分析、历史报告对比
- 触发条件：用户需要分析生产过程数据、监控过程稳定性、识别异常点、进行多周期数据对比

## 前置准备
- 依赖说明：scripts脚本所需的依赖包及版本
  ```
  pandas>=2.0.0
  numpy>=1.24.0
  openpyxl>=3.1.0
  ```
- 非标准文件/文件夹准备：无

## 操作步骤
- 标准流程：
  1. 数据接收与识别
     - 智能体识别数据来源（Excel文件或直接提供的数据）
     - 确认数据特性（如"产品A的直径"、"温度数据"等）
     - 检测数据结构是否符合所选控制图类型要求
     - 如果数据特性与历史不同，提醒用户开启新对话

  2. 控制图类型确认
     - 根据数据类型选择控制图：
       - 计量型数据（连续值）：Xbar-R图、Xbar-S图、I-MR图
       - 计数型数据（离散值）：P图、C图、U图
     - 参考 [references/control_chart_guide.md](references/control_chart_guide.md) 确认适用场景

  3. 数据分析与报告生成
     - 使用exec_shell调用分析脚本：
       ```bash
       cd /workspace/projects/spc-analysis && python scripts/spc_analysis.py --input <数据文件路径> --chart-type <控制图类型> [--output <报告输出路径>] [--usl <规格上限>] [--lsl <规格下限>]
       ```
       - 输入参数说明：
         - `--input`: Excel文件路径（用户上传或本地文件）
         - `--chart-type`: 控制图类型（xbarr/xbars/imr/p/c/u）
         - `--output`: HTML报告输出路径（可选，默认自动生成带日期的文件名）
         - `--usl`: 可选，规格上限（用于过程能力分析）
         - `--lsl`: 可选，规格下限（用于过程能力分析）
       - 输出：HTML报告文件（包含SVG控制图）
       - 报告命名：如果不指定--output，自动生成 `spc_analysis_report_YYYYMMDD_HHMMSS.html`；如果指定但不包含日期，自动添加日期前缀
     - 智能体分析报告内容，生成结论和建议

  4. 历史对比（如适用）
     - 智能体检索对话历史中的摘要信息
     - 对比关键指标：均值、标准差、异常点数量、稳定性评级
     - 识别趋势变化：均值偏移、波动变化、异常模式

  5. 结果呈现
     - 在对话中呈现报告摘要和关键发现
     - 提供HTML报告文件供用户下载
     - 给出改进建议和后续监控要点

- 可选分支：
  - 当需要过程能力分析时：询问用户提供规格限（USL、LSL），重新计算Cp/Cpk等指标
  - 当数据特性变化时：提醒用户开启新对话以保持分析的连续性和准确性
  - 当对话过长时（超过15-20次分析）：建议开启新对话并复制关键摘要

## 资源索引
- 必要脚本：见 [scripts/spc_analysis.py](scripts/spc_analysis.py)（用途与参数：主分析脚本，支持6种控制图，执行Nelson规则检测，生成HTML报告）
- 领域参考：
  - 见 [references/control_chart_guide.md](references/control_chart_guide.md)（何时读取：选择控制图类型或确认数据格式时）
  - 见 [references/nelson_rules.md](references/nelson_rules.md)（何时读取：解释异常检测结果或学习判异规则时）
  - 见 [references/data_format_spec.md](references/data_format_spec.md)（何时读取：准备数据或理解输入要求时）

## 注意事项
- **脚本调用方式**：必须使用exec_shell工具调用脚本，工作目录为 `/workspace/projects/spc-analysis`
- **命令格式**：`python scripts/spc_analysis.py --input <数据文件> --chart-type <类型> [--output <报告文件>] [--usl <上限>] [--lsl <下限>]`
- **报告自动命名**：--output参数为可选，不提供时自动生成带日期的文件名（格式：spc_analysis_report_YYYYMMDD_HHMMSS.html），方便用户按日期查找和管理
- **文件路径**：用户上传的文件通常在当前工作目录（.），使用相对路径即可
- 保持数据特性一致性：同一对话中应分析同一特性数据，不同特性需开启新对话
- 智能摘要管理：每次分析后只保留关键摘要信息，详细报告已保存为文件
- 增量对比策略：优先对比最近3-5次分析，长期趋势通过统计指标观察
- 上下文管理：建议每15-20次分析开启新对话，将关键摘要复制到新对话
- 规格限处理：过程能力分析需要用户提供USL和LSL，无规格限时仅关注过程稳定性
- 报告输出：HTML报告文件保存在当前工作目录，同时在对话中呈现摘要

## 使用示例
- 示例1：单次Xbar-R图分析
  - 功能说明：分析子组数据，生成Xbar-R控制图
  - 执行方式：调用脚本 + 智能体生成结论
  - 关键参数：控制图类型=xbarr，数据包含多列子组
  - 简单示例：`scripts/spc_analysis.py --input data.xlsx --chart-type xbarr`（自动生成带日期的报告）

- 示例2：连续多周期监控
  - 功能说明：按周提供数据，对比分析过程变化趋势
  - 执行方式：智能体维护历史摘要，执行增量对比
  - 关键参数：同一特性数据，多周期提交
  - 简单示例：用户每周提交新数据，智能体自动对比并识别趋势

- 示例3：过程能力分析
  - 功能说明：评估过程是否满足规格要求
  - 执行方式：提供规格限后重新计算
  - 关键参数：USL、LSL（规格上限和下限）
  - 简单示例：`scripts/spc_analysis.py --input data.xlsx --chart-type xbars --usl 30 --lsl 20 --output report.html`

## TRACE 测评

| 维度 | 评分 | 说明 |
|------|------|------|
| T — 可信任度 | 9/10 | 纯文档/脚本技能，无外部依赖风险，支持中文交互 |
| R — 可靠性 | 9/10 | 有异常处理说明; 输出格式明确 |
| A — 适用性 | 9/10 | 有适用范围声明; 触发条件明确 |
| C — 规范性 | 10/10 | frontmatter 完整; 文档结构清晰; 内容充分 |
| E — 有效性 | 10/10 | 输出明确; 含使用示例; 文档详尽 |
| **总分** | **47/50** | 通过 |
