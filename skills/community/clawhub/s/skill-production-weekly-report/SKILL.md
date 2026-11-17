---
name: 工作周报技能
slug: production-weekly-report
displayName: 工作周报技能
description: 生产管理周报生成工具；将口头描述、Word/Excel数据解析为结构化HTML周报，支持4周历史追踪，数据不足时自动拒绝
version: 1.1.0
category: quality
author: org-jaxjwo0r
---
# 生产管理周报

## 任务目标
- 本 Skill 用于:生产管理岗位周报自动生成
- 能力包含:多源数据解析(口头/Word/Excel)、历史数据追踪、HTML网页输出、自动归档
- 触发条件:用户提交生产数据、要求生成周报、查看历史追踪

## 前置准备
- 依赖说明:python-docx==1.1.0(Word解析), openpyxl==3.1.2(Excel解析)
- 非标准文件/文件夹准备:历史周报目录 `./weekly_reports/history/` 由脚本自动创建

## 操作步骤

### 阶段一：数据收集与校验

**1. 收集用户输入**
- 方式A(口头):询问用户描述本周生产情况
- 方式B(Word):用户提供 .docx 文件路径
- 方式C(Excel):用户提供 .xlsx 文件路径

**2. 数据完整性校验**
执行脚本解析后，校验最低数据门槛：
- 本周完成事项:至少1条
- 下周计划:至少1条
- 核心指标:至少1项(产量/良率/OEE/交付率等)

**数据不足时**:输出以下内容并停止，禁止生成报告：
```
[数据不足，无法生成周报]
缺少以下必要信息：
- [ ] 待补充项1
- [ ] 待补充项2
请补充后重新提交。
```

**3. 数据解析**
- Word解析:`python scripts/parse_docx.py --file <path>`
- Excel解析:`python scripts/parse_xlsx.py --file <path>`
- 解析结果为JSON结构化数据

### 阶段二：历史数据读取

**4. 读取最近4周历史**
```bash
python scripts/history_manager.py --action read --weeks 4
```
- 提取项:未解决问题、进行中项目、上周遗留任务
- 追踪标记:问题持续时间、状态变更

### 阶段三：周报生成

**5. 整合数据生成HTML**
- 口头输入由智能体理解后映射到结构化字段
- 合并解析数据 + 历史追踪项
- 按6章节结构生成HTML网页

**6. 生成HTML文件**
```bash
python scripts/generate_html.py --data @file:./temp_data.json --output ./weekly_reports/YYYY-WXX.html
```
- 样式内嵌，打开即可查看
- 支持打印为PDF

**7. 周报归档**
```bash
python scripts/history_manager.py --action archive --file <output_path>
```
- 自动归档到 `./weekly_reports/history/YYYY-WXX.html`

## 使用示例

### 示例1：口头输入
- 场景/输入:用户描述"这周产量8000台，良率98.2%，完成了A线改造，有台设备故障影响了半天"
- 预期产出:生成HTML周报，包含产量数据、设备异常、完成事项
- 关键要点:需追问确认下周计划和需协调事项

### 示例2：Word文件
- 场景/输入:`./data/week_report.docx`
- 预期产出:解析表格/段落数据，生成HTML周报
- 关键要点:文件需包含本周数据，可含历史对比列

### 示例3：Excel文件
- 场景/输入:`./data/production_data.xlsx`
- 预期产出:读取数据Sheet，提取指标与明细，生成HTML周报
- 关键要点:数据应按标准模板组织

## 资源索引
- 脚本:见 [scripts/parse_docx.py](scripts/parse_docx.py)(用途:解析Word文档，参数:`--file <path>`)
- 脚本:见 [scripts/parse_xlsx.py](scripts/parse_xlsx.py)(用途:解析Excel表格，参数:`--file <path>`)
- 脚本:见 [scripts/history_manager.py](scripts/history_manager.py)(用途:历史数据读写，参数:`--action read|archive --weeks N --file <path>`)
- 脚本:见 [scripts/generate_html.py](scripts/generate_html.py)(用途:生成HTML网页版周报，参数:`--data <json> --output <path>`)
- 参考:见 [references/report_format.md](references/report_format.md)(何时读取:生成周报前确认格式规范)

## 注意事项
- 数据不足时必须拒绝生成，禁止编造任何数据
- 口头输入需完整确认6章节信息
- 历史追踪仅读取最近4周文件
- 输出路径默认 `./weekly_reports/YYYY-WXX.html`
- HTML文件样式内嵌，无需额外资源

## TRACE 测评

| 维度 | 评分 | 说明 |
|------|------|------|
| T — 可信任度 | 9/10 | 纯文档/脚本技能，无外部依赖风险，支持中文交互 |
| R — 可靠性 | 9/10 | 有异常处理说明; 输出格式明确 |
| A — 适用性 | 9/10 | 有适用范围声明; 触发条件明确 |
| C — 规范性 | 10/10 | frontmatter 完整; 文档结构清晰; 内容充分 |
| E — 有效性 | 10/10 | 输出明确; 含使用示例; 文档详尽 |
| **总分** | **47/50** | 通过 |
