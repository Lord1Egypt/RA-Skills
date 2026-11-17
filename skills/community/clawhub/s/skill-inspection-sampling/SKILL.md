---
name: 检验抽样技能
slug: inspection-sampling
displayName: 检验抽样技能
description: 提供检验抽样全流程支持；当你需要设计抽样方案、处理待检数据、生成抽样计划、追踪抽样记录或分析抽样结果时使用；覆盖GB/T2828等标准抽样方法
version: 1.1.0
category: quality
author: org-jaxjwo0r
---
# 检验抽样辅助

## 任务目标
- 本 Skill 用于:检验抽样场景下的方案设计、数据处理、计划生成、过程追踪与结果分析
- 能力包含:抽样方案预设管理、多格式数据解析、多种抽样算法、抽样记录追踪、统计分析报告生成
- 触发条件:用户提及抽样方案、检验抽样、样本选取、数据抽样、质量抽检等场景

## 前置准备
- 依赖说明:pandas>=1.5.0（数据处理）、numpy>=1.21.0（数值计算）
- 抽样方案存储路径:`./sampling_schemes/`（相对于用户工作目录）
- 抽样记录存储路径:`./sampling_records/`（相对于用户工作目录）

## 操作步骤

### 一、抽样方案管理

#### 1.1 创建新方案
- 使用 `scheme_manager.py` 创建抽样方案
- 调用示例:`python scripts/scheme_manager.py create --name <方案名> --type <simple|stratified|systematic|cluster> --params <JSON参数>`
- 参数说明:
  - `sample_size`: 样本量（整数）
  - `sample_rate`: 采样比例（浮点数，0-1之间，与sample_size二选一）
  - `strata_field`: 分层字段（分层抽样必需）
  - `interval`: 抽样间隔（系统抽样必需）
  - `cluster_field`: 整群字段（整群抽样必需）

#### 1.2 查看/列出方案
- 调用示例:`python scripts/scheme_manager.py list`
- 调用示例:`python scripts/scheme_manager.py get --name <方案名>`

#### 1.3 更新方案
- 调用示例:`python scripts/scheme_manager.py update --name <方案名> --params <JSON参数>`

#### 1.4 删除方案
- 调用示例:`python scripts/scheme_manager.py delete --name <方案名>`

### 二、数据输入处理

#### 2.1 解析待检数据
- 使用 `data_parser.py` 解析原始数据
- 调用示例:`python scripts/data_parser.py --input <数据文件路径> --format <csv|excel|json> --output <解析结果JSON路径>`
- 支持格式:
  - CSV: 自动识别分隔符，支持中文编码
  - Excel: 支持 .xlsx/.xls，自动读取第一个sheet
  - JSON: 支持数组格式和对象数组格式

### 三、抽样计划生成

#### 3.1 生成抽样计划
- 使用 `sampler.py` 执行抽样
- 调用示例:`python scripts/sampler.py generate --data <解析后数据JSON路径> --scheme <方案名> --output <抽样结果JSON路径> --record`
- 执行步骤:
  1. 读取方案参数
  2. 解析数据文件
  3. 根据抽样类型执行对应算法
  4. 生成抽样计划（包含样本索引、选取规则说明）
  5. 保存抽样记录（启用--record时）

#### 3.2 抽样算法说明
| 类型 | 适用场景 | 算法特点 |
|------|----------|----------|
| 简单随机抽样 | 数据均匀、无特殊结构 | 完全随机、等概率 |
| 分层抽样 | 需要按类别均匀覆盖 | 先分层、层内随机 |
| 系统抽样 | 大批量、规律性数据 | 等间隔选取 |
| 整群抽样 | 群体为单位抽样 | 整群抽中、群内全检 |

### 四、抽样记录追踪

- 记录自动生成于 `./sampling_records/` 目录
- 记录内容:方案参数、抽样时间、数据摘要、样本索引、操作日志
- 调用示例:`python scripts/scheme_manager.py record --id <记录ID>` 查看历史记录

### 五、抽样结果分析

#### 5.1 生成分析报告
- 使用 `analyzer.py` 进行统计分析
- 调用示例:`python scripts/analyzer.py --samples <抽样结果JSON路径> --original <原始数据路径> --output <报告JSON路径>`
- 分析维度:
  - 样本覆盖率统计
  - 样本分布特征
  - 与总体对比分析
  - 抽样质量评估

#### 5.2 报告内容
- 样本量统计（实际抽量、计划抽量、达成率）
- 字段缺失率分析
- 数值字段分布（均值、标准差、极值）
- 分类字段频次分布
- 质量结论与建议

## 使用示例

### 示例1:质量检验抽样
- 场景/输入:一批产品检验，需要从10000件中抽取500件进行质量检验
- 预期产出:抽样计划文件、样本索引列表、抽样记录
- 关键要点:
  1. 先创建简单随机抽样方案（sample_size=500）
  2. 解析产品数据文件（CSV格式）
  3. 执行抽样生成计划
  4. 如需分层覆盖，按产品类别分层

### 示例2:分层抽样检验
- 场景/输入:按产品类别A/B/C分别抽取样本，要求每类样本量不少于50
- 预期产出:各层样本清单、整体抽样计划
- 关键要点:
  1. 创建分层抽样方案（strata_field=产品类别）
  2. 每层独立计算样本量
  3. 记录各层抽取结果

### 示例3:抽样结果分析
- 场景/输入:完成抽样后，需要评估抽样代表性
- 预期产出:统计分析报告，包含覆盖率、分布对比、质量评估
- 关键要点:
  1. 准备原始数据和抽样结果
  2. 执行分析脚本
  3. 根据报告判断抽样是否满足检验要求

## 资源索引
- 脚本:见 [scripts/scheme_manager.py](scripts/scheme_manager.py)（用途:抽样方案CRUD管理，参数:--cmd create|list|get|update|delete）
- 脚本:见 [scripts/data_parser.py](scripts/data_parser.py)（用途:多格式数据解析，参数:--input --format --output）
- 脚本:见 [scripts/sampler.py](scripts/sampler.py)（用途:抽样执行与计划生成，参数:--data --scheme --output --record）
- 脚本:见 [scripts/analyzer.py](scripts/analyzer.py)（用途:抽样结果统计分析，参数:--samples --original --output）
- 参考:见 [references/format_spec.md](references/format_spec.md)（何时读取:需要定义数据格式或方案参数时）

## 注意事项
- 抽样方案名建议使用英文+数字，避免特殊字符
- 数据文件路径支持相对路径（相对于用户工作目录）
- 抽样记录永久保存，支持追溯审计
- 大数据量时注意内存使用，必要时分批处理

## TRACE 测评

| 维度 | 评分 | 说明 |
|------|------|------|
| T — 可信任度 | 9/10 | 纯文档/脚本技能，无外部依赖风险，支持中文交互 |
| R — 可靠性 | 9/10 | 有异常处理说明; 输出格式明确 |
| A — 适用性 | 9/10 | 有适用范围声明; 触发条件明确 |
| C — 规范性 | 10/10 | frontmatter 完整; 文档结构清晰; 内容充分 |
| E — 有效性 | 10/10 | 输出明确; 含使用示例; 文档详尽 |
| **总分** | **47/50** | 通过 |
