---
name: CP控制计划技能
slug: cp-control-plan
displayName: CP控制计划技能
description: 提供CP控制计划模板生成、数据分析、风险预警、可视化及版本管理指导；当质量工程师需要编制/优化控制计划、执行过程能力分析或识别质量风险时使用
version: 1.1.0
category: quality
author: org-jaxjwo0r
---
# CP控制计划专业技能

## 任务目标
- 本技能用于：支持质量工程师完成CP（Control Plan）控制计划的编制、分析与优化
- 能力包含：结构化模板生成、数据导入分析、风险预警、可视化展示、版本管理指导
- 触发条件：用户需要创建/审查控制计划、执行过程能力分析、识别潜在质量风险或生成质量报告

## 前置准备
- 依赖说明：pandas、openpyxl、numpy、matplotlib
- 数据文件准备：支持CSV或Excel格式的质量数据文件，包含测量值、规格限、过程参数等字段

## 操作步骤

### 1. 模板生成（智能体执行）

#### 1.1 确定控制计划范围
- 识别关键过程步骤（从过程流程图中提取）
- 确定特殊特性（SC）和关键特性（CC）
- 确认测量系统分析（MSA）需求

#### 1.2 填充控制计划要素
每个过程步骤需包含：
- 过程编号与名称
- 过程描述（输入、输出、设备、工装）
- 关键产品特性（KPC）与关键过程参数（KPP）
- 特性编号、规格限、测量方法
- 控制方法（防错、检验、统计过程控制）
- 反应计划与纠正措施
- 职责分配

#### 1.3 生成结构化文档
调用智能体生成完整的控制计划文档，确保符合IATF 16949或行业标准格式。

### 2. 数据导入与分析（脚本处理）

#### 2.1 数据导入
```bash
python scripts/cp_data_analyzer.py --input <数据文件路径> --format <csv|xlsx> --output ./cp_analysis_result.json
```

#### 2.2 数据验证与清洗
脚本自动执行：
- 缺失值检测与处理
- 异常值识别（3σ原则或IQR方法）
- 数据类型校验
- 规格限验证

#### 2.3 关键参数提取
脚本输出包含：
- 质量特性列表及其统计参数（均值、标准差、CPK）
- 规格限与控制限
- 过程能力指数（CP、CPK、PP、PPK）
- 风险评估值（RPN）

### 3. 风险预警分析（脚本处理）

#### 3.1 风险评估计算
```bash
python scripts/cp_risk_analyzer.py --input ./cp_analysis_result.json --method <fmea|spc> --threshold <RPN阈值> --output ./cp_risk_result.json
```

#### 3.2 风险等级判定
- 严重度（S）：1-10分，基于缺陷后果
- 频度（O）：1-10分，基于失效概率
-探测度（D）：1-10分，基于检测难度
- RPN = S × O × D

#### 3.3 智能预警生成
脚本根据以下规则自动识别潜在变异点：
- CPK < 1.0：过程能力不足，需立即改善
- CPK 1.0-1.33：过程能力勉强，需要监控
- 连续5点中有2点超出2σ：存在趋势异常
- 连续8点在中心线同一侧：存在漂移

### 4. 版本管理与协作（智能体指导）

#### 4.1 版本控制原则
- 主版本号：重大结构变更时递增
- 次版本号：内容更新时递增
- 修订号：小幅修改时递增
- 命名格式：CP-{零件号}-V{主}.{次}.{修订}

#### 4.2 协作流程
1. **创建**：发起人创建初始控制计划
2. **审核**：质量工程师进行技术审核
3. **批准**：质量经理批准发布
4. **分发**：按受控文件流程分发
5. **变更**：通过正式变更申请（ECN）流程

#### 4.3 协作工具建议
- 飞书文档：实时协作编辑
- Git：版本追踪与变更管理
- PDF+电子签：正式批准流程

### 5. 可视化展示（脚本处理）

#### 5.1 生成可视化图表
```bash
python scripts/cp_visualizer.py --input ./cp_analysis_result.json --output ./cp_charts/ --chart <all|cpk|spc|distribution>
```

#### 5.2 图表类型
- **CPK仪表盘**：各质量特性的过程能力指数对比
- **控制图**：X-bar、R、S等控制图展示过程稳定性
- **分布图**：直方图展示数据分布与规格限关系
- **风险热力图**：RPN值分布可视化

#### 5.3 图表输出
- PNG格式图片文件
- 分辨率：300 DPI
- 支持批量生成与单图生成

## 使用示例

### 示例1：新建控制计划
- 场景/输入：用户需要为新零件创建控制计划，提供过程流程图和特殊特性清单
- 预期产出：完整的CP控制计划文档，包含所有过程步骤和控制要素
- 关键要点：确认关键特性与控制方法，建立合理的抽样方案

### 示例2：过程能力分析
- 场景/输入：用户提供过去30天的测量数据（CSV格式）
- 预期产出：数据分析报告，包含CPK指数、风险预警、控制建议
- 关键要点：数据需包含测量值、规格上下限、时间戳
```bash
python scripts/cp_data_analyzer.py --input ./quality_data.csv --format csv --output ./result.json
python scripts/cp_risk_analyzer.py --input ./result.json --method fmea --threshold 100 --output ./risk.json
```

### 示例3：控制计划可视化
- 场景/输入：已完成数据分析，需要生成可视化报告
- 预期产出：一组PNG图表，展示CPK、控制图、分布图
- 关键要点：先生成分析结果，再进行可视化
```bash
mkdir -p ./cp_charts
python scripts/cp_visualizer.py --input ./result.json --output ./cp_charts/ --chart all
```

## 资源索引

- 数据分析脚本：见 [scripts/cp_data_analyzer.py](scripts/cp_data_analyzer.py)（用途：导入CSV/Excel数据，提取质量特性，计算统计参数；参数：--input, --format, --output）
- 风险预警脚本：见 [scripts/cp_risk_analyzer.py](scripts/cp_risk_analyzer.py)（用途：FMEA风险分析，识别潜在变异点，生成预警；参数：--input, --method, --threshold, --output）
- 可视化脚本：见 [scripts/cp_visualizer.py](scripts/cp_visualizer.py)（用途：生成CPK仪表盘、控制图、分布图等；参数：--input, --output, --chart）
- CP模板指南：见 [references/cp_template_guide.md](references/cp_template_guide.md)（何时读取：需要详细了解CP控制计划结构要素或参考行业标准模板时）

## 注意事项

- 数据分析前需确认数据格式与字段命名符合规范
- 风险预警阈值可根据行业标准或企业内部标准调整
- 可视化图表建议用于报告展示，详细分析仍需查看JSON结果
- 版本管理与协作功能需结合企业实际流程使用
- 脚本运行需要Python 3.8+环境

## TRACE 测评

| 维度 | 评分 | 说明 |
|------|------|------|
| T — 可信任度 | 9/10 | 纯文档/脚本技能，无外部依赖风险，支持中文交互 |
| R — 可靠性 | 9/10 | 有异常处理说明; 输出格式明确 |
| A — 适用性 | 9/10 | 有适用范围声明; 触发条件明确 |
| C — 规范性 | 10/10 | frontmatter 完整; 文档结构清晰; 内容充分 |
| E — 有效性 | 10/10 | 输出明确; 含使用示例; 文档详尽 |
| **总分** | **47/50** | 通过 |
