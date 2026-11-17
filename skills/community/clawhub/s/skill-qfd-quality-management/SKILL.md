---
name: 质量功能展开技能
slug: qfd-quality-management
displayName: 质量功能展开技能
description: 将客户需求转化为产品设计规范和质量目标的质量管理工具；当用户需要构建质量屋(VOC分析)、评估需求优先级或计算技术权重时使用
version: 1.1.0
category: quality
author: org-jaxjwo0r
---
# QFD质量管理技能

## 任务目标
- 本Skill用于：系统性地将客户需求转化为产品设计规范和质量目标
- 能力包含：VOC分析、QFD流程指导、质量屋构建、权重计算、迭代优化
- 触发条件：用户提出产品质量规划、需求优先级排序、技术指标确定等需求

## 前置准备
- 依赖说明：numpy==1.24.0（数值计算）
- 输入文件准备：
  - VOC数据：JSON格式，包含客户需求列表及原始描述
  - 历史项目数据：CSV格式（可选），包含历史需求权重和技术实现结果

## 操作步骤

### 阶段一：VOC分析（智能体执行）

1. **需求收集**
   - 引导用户列出所有客户声音（原始表述）
   - 识别需求类别：功能需求、性能需求、体验需求、服务需求
   - 避免需求重叠和矛盾

2. **需求结构化**
   - 将模糊需求转化为可量化指标
   - 格式要求：见 references/hoq_template.md 的 VOC表格规范

3. **需求优先级排序**
   - 评估维度：重要性、紧迫性、市场竞争力影响
   - 建议使用1-5分制评分

### 阶段二：质量屋构建（脚本执行）

1. **输入准备**
   - 生成或用户提供需求列表和技术指标列表
   - 按以下JSON格式准备输入：

```json
{
  "customer_requirements": [
    {"id": "CR1", "name": "易用性", "weight": 5, "category": "体验"},
    {"id": "CR2", "name": "可靠性", "weight": 4, "category": "功能"}
  ],
  "technical_requirements": [
    {"id": "TR1", "name": "响应时间", "unit": "ms"},
    {"id": "TR2", "name": "MTBF", "unit": "小时"}
  ]
}
```

2. **构建质量屋矩阵**
   - 调用脚本：`python scripts/qfd_matrix.py build --input voc_data.json --output hoq_matrix.json`
   - 脚本输出：完整质量屋矩阵（含屋顶相关性矩阵）

3. **评估关系强度**
   - 在生成矩阵中填写关系：强(9)、中(3)、弱(1)、无(0)
   - 或使用脚本自动生成模板：`python scripts/qfd_matrix.py template --cr 5 --tr 8 --output template.json`

4. **计算技术权重**
   - 调用脚本：`python scripts/qfd_matrix.py weight --matrix hoq_matrix.json --output weights.json`
   - 输出：各技术指标的目标值和优先级排序

### 阶段三：数据分析与优化（脚本执行）

1. **历史数据参考分析**
   - 准备CSV格式历史数据：`python scripts/data_analysis.py analyze --history data.csv --current current_requirements.json`
   - 输出：优先级调整建议、技术可行性评估

2. **迭代优化**
   - 根据分析结果调整需求权重
   - 重新计算质量屋
   - 脚本支持增量更新：`python scripts/qfd_matrix.py update --base hoq_matrix.json --changes changes.json`

## 使用示例

### 示例1：新建QFD分析
- 场景/输入：用户需要为新产品的触摸屏功能进行质量规划
- 预期产出：完整质量屋矩阵、技术权重排序表
- 关键要点：先收集5-8条核心客户需求，再识别8-12个技术指标

### 示例2：优先级优化
- 场景/输入：用户已有初步质量屋，需根据历史项目数据优化
- 预期产出：调整后的需求权重、技术指标优先级
- 关键要点：历史数据需包含至少3个相关项目的完成数据

### 示例3：VOC分析指导
- 场景/输入：用户有大量客户反馈文本需转化为技术需求
- 预期产出：结构化的需求列表和技术指标映射
- 关键要点：智能体协助提取关键词并量化表达

## 资源索引

- 脚本：见 [scripts/qfd_matrix.py](scripts/qfd_matrix.py)（用途：质量屋矩阵构建、权重计算；参数：build/template/weight/update子命令）
- 脚本：见 [scripts/data_analysis.py](scripts/data_analysis.py)（用途：历史数据分析、优先级建议；参数：--history, --current, --output）
- 参考：见 [references/hoq_template.md](references/hoq_template.md)（何时读取：准备VOC数据或构建质量屋时）

## 注意事项

- 质量屋构建建议不超过12个技术指标，避免矩阵过于复杂
- 关系强度评估需结合业务专家判断，脚本仅做数值计算
- 迭代优化建议不超过3轮，避免过度优化导致失真
- 历史数据分析需确保数据质量和相关性

## TRACE 测评

| 维度 | 评分 | 说明 |
|------|------|------|
| T — 可信任度 | 9/10 | 纯文档/脚本技能，无外部依赖风险，支持中文交互 |
| R — 可靠性 | 9/10 | 有异常处理说明; 输出格式明确 |
| A — 适用性 | 9/10 | 有适用范围声明; 触发条件明确 |
| C — 规范性 | 10/10 | frontmatter 完整; 文档结构清晰; 内容充分 |
| E — 有效性 | 10/10 | 输出明确; 含使用示例; 文档详尽 |
| **总分** | **47/50** | 通过 |
