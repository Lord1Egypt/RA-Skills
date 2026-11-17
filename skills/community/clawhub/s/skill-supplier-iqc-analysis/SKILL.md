---
name: 供应商来料质量专项分析
slug: supplier-iqc-analysis
displayName: 供应商来料质量专项分析
description: 企业SQE供应商来料质量分析工具；当用户需要分析IQC来料检验数据、供应商质量对标、生成质量报告时使用
version: 1.1.0
category: quality
author: org-jaxjwo0r
---
# 供应商IQC质量分析Skill

## 任务目标
- 本 Skill 用于：企业SQE专家对供应商来料质量数据进行自动化分析和报告生成
- 能力包含：多Sheet数据结构分析、数据清洗、质量指标计算、不良分布统计、供应商横向对标、趋势分析、风险评级、双格式报告输出
- 触发条件：用户上传IQC检验表、供应商台账、来料不良记录等Excel文件并请求分析

## 前置准备
- 依赖说明：pandas（数据处理）、openpyxl（Excel读取）、numpy（数值计算）
- 文件准备：用户需提供Excel格式的来料质量数据文件

## 操作步骤
- 标准流程：
  1. **宏观分析数据结构** — 脚本调用处理说明
     - 脚本调用示例：`python scripts/analyze.py --file <file_path> --action analyze_structure`
     - 输出：数据结构概览（Sheet列表、字段分布、关联关系建议）
  2. **确认分析需求**
     - 向用户询问：分析目标（单供应商/多供应商/物料维度）、报告关注点、输出要求
     - 若无法识别供应商字段，要求用户提供字段映射
  3. **执行质量分析** — 脚本调用处理说明
     - 脚本调用示例：`python scripts/analyze.py --file <file_path> --action analyze --mapping <json_mapping>`
     - 输出：结构化分析数据（JSON格式）
  4. **生成质量报告** — 脚本调用处理说明
     - 脚本调用示例：`python scripts/generate_report.py --data <json_data> --output_dir <output_dir>`
     - 输出：Markdown和HTML双格式报告
- 可选分支：
  - 当需要细化分析：增加检验项目TOP分析、多供应商横向对标
  - 当数据包含时间维度：自动生成趋势分析（月度/季度）
  - 当需要风险评估：自动计算供应商风险等级（A/B/C类）

## 使用示例
- 示例1: 单供应商IQC数据分析
  - 场景/输入: 用户上传单个供应商的IQC检验表Excel
  - 预期产出: 生成包含批次合格率、不良PPM、不良类型TOP5、检验项目TOP5的分析报告
  - 关键要点: 确认不良类型字段和检验项目字段，生成双格式报告
- 示例2: 多供应商质量对标分析
  - 场景/输入: 用户上传包含多个供应商的台账数据
  - 预期产出: 生成供应商横向对比表、排名、风险评级报告
  - 关键要点: 需确认供应商字段映射，输出包含供应商对比的HTML可视化报告
- 示例3: 多Sheet复杂数据关联分析
  - 场景/输入: 用户上传Excel包含"IQC检验表"和"不良记录表"两个Sheet
  - 预期产出: 识别Sheet间通过"批次号"关联，合并分析后输出完整报告
  - 关键要点: 先输出数据结构概览，确认关联逻辑后再执行分析

## 资源索引
- 脚本: 见 [scripts/analyze.py](scripts/analyze.py)(用途与参数: 数据结构分析与质量指标计算，支持--file、--action、--mapping参数)
- 脚本: 见 [scripts/generate_report.py](scripts/generate_report.py)(用途与参数: 生成双格式报告，支持--data、--output_dir参数)
- 参考: 见 [references/data-schema.md](references/data-schema.md)(何时读取: 数据字段映射规范和示例)
- 资产: 见 [assets/report-template.html](assets/report-template.html)(直接用于生成/修饰输出: HTML报告模板，包含纯CSS图表样式)

## 注意事项
- 严格遵循交互流程：先分析结构→确认需求→执行分析→生成报告
- 若数据中无供应商字段，必须要求用户提供字段映射，否则不开始分析
- 所有分析报告需包含：数据汇总→关键质量指标→不良分布统计→专项分析结论
- 结论必须量化、可举证，适合直接发给供应商作为改善依据
- 拒绝回答其他质量模块问题（现场不良、车间制程、客户投诉、SPC、质量成本、月报、8D等）

## TRACE 测评

| 维度 | 评分 | 说明 |
|------|------|------|
| T — 可信任度 | 9/10 | 纯文档/脚本技能，无外部依赖风险，支持中文交互 |
| R — 可靠性 | 9/10 | 有异常处理说明; 输出格式明确 |
| A — 适用性 | 9/10 | 有适用范围声明; 触发条件明确 |
| C — 规范性 | 10/10 | frontmatter 完整; 文档结构清晰; 内容充分 |
| E — 有效性 | 10/10 | 输出明确; 含使用示例; 文档详尽 |
| **总分** | **47/50** | 通过 |
