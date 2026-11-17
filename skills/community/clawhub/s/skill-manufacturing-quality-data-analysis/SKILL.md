---
name: 现场不良数据分析助手
slug: manufacturing-quality-data-analysis
displayName: 现场不良数据分析助手
description: 制造业质量现场数据分析；当用户需要分析车间巡检、制程不良、成品检验台账数据或处理现场不合格记录时使用；覆盖数据清洗、统计分析、图表可视化
version: 1.1.0
category: quality
author: org-jaxjwo0r
---
# 制造业质量现场数据分析

## 任务目标
- 本 Skill 用于：分析车间巡检、现场勘查、制程不良、成品检验台账的轻量化数据
- 能力包含：自动解析 Excel/CSV/Word/PDF、数据清洗、不良类型分类统计、TOP3 高频不良分析、生成 HTML 可视化图表
- 触发条件：用户上传质量数据表格文件或粘贴表格数据，要求分析现场不合格、制程不良、巡检勘查记录

## 场景边界
- **支持场景**：车间巡检、现场勘查、制程不良、成品检验台账
- **禁止场景**：供应商质量、客诉分析、SPC 控制图、CPK 计算、成本核算、月报汇总、8D 报告

## 前置准备
- 无需特殊准备，确保提供的数据文件为 Excel（.xlsx/.xls）、CSV、Word 或 PDF 格式

## 操作步骤

### 1. 数据输入与宏观分析
- 用户上传文件或粘贴数据后，使用脚本解析文件结构
- 脚本调用示例：
  - Excel 文件：`python scripts/parse_data.py --file_path /path/to/file.xlsx`
  - CSV 文件：`python scripts/parse_data.py --file_path /path/to/file.csv`
  - Word/PDF 文件：`python scripts/parse_data.py --file_path /path/to/file.docx`
- 宏观分析 Excel 结构：识别 Sheet 数量、表头位置、关键字段

### 2. 字段确认与数据关联
- 自动识别关键字段：产品、工序、班次、不良类型、不良数量、日期
- 多 Sheet 数据自动关联：根据字段含义跨 Sheet 关联数据
- **关键交互**：当字段含义不清楚、数据缺失或数据量不足时，必须先向用户反馈确认
  - 示例确认问题："检测到只有'合格/不合格'标记，无'不良数量'字段，是否按 1 条记录 = 1 个不良数计算？"

### 3. 数据清洗
- 使用脚本自动处理：
  - 合并单元格展开
  - 空行/空值处理
  - 重复数据去重
  - 格式标准化
- 脚本调用示例：`python scripts/clean_data.py --input_file /path/to/parsed_data.json`

### 4. 数据分析
- 脚本执行固定分析维度：
  - 不良类型分类统计（数量、占比）
  - 按工序/班次/产品型号拆分不良分布
  - 自动筛选 TOP3 高频不良问题（遵循二八原则）
- 脚本调用示例：`python scripts/analyze_data.py --input_file /path/to/clean_data.json`

### 5. 报告大纲确认
- 生成分析大纲和摘要，先提交给用户确认
- 等待用户确认是否有补充或调整

### 6. 生成分析报告
- 确认后生成完整报告，包含：
  - 数据概览（总检验量、不良总数、整体不良率）
  - Markdown 格式分类统计表格
  - HTML 完整分析报告（包含数据概览、统计表格、可视化图表、质量分析结论、整改优先级建议）
  - 质量分析结论与整改优先级建议
- 报告按时间命名，方便区分不同时期分析
- HTML 报告生成脚本：`python scripts/generate_charts.py --input_file /path/to/analysis_data.json --output_file /path/to/report.html`

## 使用示例

### 示例 1：Excel 多 Sheet 制程不良分析
- 场景/输入：用户上传包含 3 个 Sheet 的 Excel 文件（Sheet1：巡检记录、Sheet2：制程不良、Sheet3：成品检验）
- 预期产出：自动跨 Sheet 关联数据，输出包含 Markdown 表格和完整 HTML 报告的分析结果
- 关键要点：
  - 脚本先宏观分析 Sheet 结构，识别关键字段
  - 跨 Sheet 关联"不良类型"和"不良数量"
  - 如发现字段缺失，主动询问用户确认计算规则
  - HTML 报告包含数据概览、统计表格、图表、分析结论、整改建议

### 示例 2：CSV 单表巡检记录分析
- 场景/输入：用户上传单表 CSV 文件，包含日期、工序、检验结果、不良描述
- 预期产出：清洗数据后输出 TOP3 不良类型、按工序分布的统计结果和完整 HTML 报告
- 关键要点：
  - 自动解析 CSV，识别表头
  - 将"检验结果"字段转化为"不良类型"和"不良数量"
  - 如数据量过少（少于 3 条），提示用户补充数据
  - HTML 报告包含完整分析内容，可直接查看或分享

### 示例 3：Word 文档检验台账分析
- 场景/输入：用户上传 Word 文档，包含表格形式的检验记录
- 预期产出：解析表格内容，清洗后输出分析报告
- 关键要点：
  - 使用 python-docx 解析 Word 中的表格
  - 处理表格合并单元格和格式混乱
  - 确认报告大纲后再生成最终报告

## 资源索引

- 脚本：
  - [scripts/parse_data.py](scripts/parse_data.py)（用途：解析 Excel/CSV/Word/PDF 文件，输出结构化 JSON 数据）
  - [scripts/clean_data.py](scripts/clean_data.py)（用途：数据清洗，处理合并单元格、空值、重复数据）
  - [scripts/analyze_data.py](scripts/analyze_data.py)（用途：执行不良类型统计、TOP3 分析、维度拆分）
  - [scripts/generate_charts.py](scripts/generate_charts.py)（用途：生成完整 HTML 分析报告，包含数据概览、统计表格、图表、分析结论、整改建议，参数：input_file、output_file）

- 参考：
  - [references/field_mapping.md](references/field_mapping.md)（何时读取：字段识别与映射时，包含关键字段定义和同义词规则）
  - [references/cleaning_rules.md](references/cleaning_rules.md)（何时读取：数据清洗规则参考，包含合并单元格处理、空值处理策略）

- 资产：
  - [assets/chart_template.html](assets/chart_template.html)（直接用于生成 HTML 图表：图表模板和样式）

## 注意事项

- **单一垂直场景**：仅处理现场不合格、制程不良、巡检勘查记录，拒绝跨场景分析
- **禁止复杂算法**：不使用 SPC 控制图、CPK 计算、复杂统计算法
- **交互优先**：数据不明确时必须主动询问用户，禁止自作主张计算
- **输出简洁**：不生成长篇大报告，内容可直接复制到飞书、WPS 文档使用
- **用语规范**：贴合生产现场品质管理，客观、量化、不主观夸大
- **命名规范**：报告按时间命名，方便区分不同时期分析

## TRACE 测评

| 维度 | 评分 | 说明 |
|------|------|------|
| T — 可信任度 | 9/10 | 纯文档/脚本技能，无外部依赖风险，支持中文交互 |
| R — 可靠性 | 9/10 | 有异常处理说明; 输出格式明确 |
| A — 适用性 | 9/10 | 有适用范围声明; 触发条件明确 |
| C — 规范性 | 10/10 | frontmatter 完整; 文档结构清晰; 内容充分 |
| E — 有效性 | 10/10 | 输出明确; 含使用示例; 文档详尽 |
| **总分** | **47/50** | 通过 |
