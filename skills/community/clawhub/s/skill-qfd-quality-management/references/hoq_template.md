# 质量屋(HoQ)模板与规范

## 目录
- VOC数据格式规范
- 关系强度评估标准
- 相关性矩阵规范
- 质量屋矩阵格式定义
- 历史数据格式要求

## 概览

质量屋(House of Quality)是QFD的核心工具，用于将客户需求(WHAT)映射到技术需求(HOW)。本模板定义了完整的数据格式和操作规范。

## VOC数据格式规范

### 客户需求(VOC)输入格式

```json
{
  "customer_requirements": [
    {
      "id": "CR1",
      "name": "操作简便",
      "weight": 5,
      "category": "体验",
      "source": "客户访谈",
      "description": "用户无需培训即可上手使用"
    },
    {
      "id": "CR2",
      "name": "响应速度快",
      "weight": 4,
      "category": "性能",
      "source": "市场调研",
      "description": "操作响应时间不超过2秒"
    }
  ]
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 是 | 唯一标识符，格式:CR+N |
| name | string | 是 | 需求名称，简洁明了 |
| weight | integer | 是 | 重要性权重，1-5分 |
| category | string | 否 | 需求类别:功能/性能/体验/服务 |
| source | string | 否 | 需求来源 |
| description | string | 否 | 详细描述 |

### 技术需求(Technical Requirements)格式

```json
{
  "technical_requirements": [
    {
      "id": "TR1",
      "name": "页面加载时间",
      "unit": "ms",
      "direction": "lower_better",
      "target": "≤2000"
    },
    {
      "id": "TR2",
      "name": "系统可用性",
      "unit": "%",
      "direction": "higher_better",
      "target": "≥99.9"
    }
  ]
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 是 | 唯一标识符，格式:TR+N |
| name | string | 是 | 技术指标名称 |
| unit | string | 否 | 单位 |
| direction | string | 否 | 优化方向:higher_better/lower_better |
| target | string | 否 | 目标值 |

## 关系强度评估标准

### 关系矩阵值定义

| 值 | 关系强度 | 说明 | 符号表示 |
|----|----------|------|----------|
| 9 | 强关系 | 该技术指标直接满足该客户需求 | ● |
| 3 | 中关系 | 该技术指标对该客户需求有间接影响 | ○ |
| 1 | 弱关系 | 该技术指标对该客户需求有微弱影响 | · |
| 0 | 无关系 | 无关联 | (空白) |

### 评估原则

1. **直接性原则**: 是否存在直接因果关系
2. **可测量原则**: 技术指标是否可客观量化
3. **独立性原则**: 避免重复计算相同影响
4. **一致性原则**: 评估标准在整个矩阵中保持一致

### 评估示例

| 客户需求 | TR1响应时间 | TR2易用性 | TR3可靠性 |
|----------|-------------|-----------|-----------|
| 操作简便 | 1 | 9 | 0 |
| 响应快速 | 9 | 0 | 3 |
| 使用可靠 | 0 | 3 | 9 |

## 相关性矩阵规范(屋顶)

### 相关性值定义

| 值 | 关系类型 | 说明 |
|----|----------|------|
| +9 | 强正相关 | 一个提升必然带动另一个提升 |
| +3 | 中正相关 | 存在正向关联 |
| +1 | 弱正相关 | 有轻微正向影响 |
| 0 | 无相关 | 无关联 |
| -1 | 弱负相关 | 有轻微反向影响 |
| -3 | 中负相关 | 存在反向关联 |
| -9 | 强负相关 | 一个提升必然导致另一个下降 |

### 常见相关性场景

- 性能↑ ↔ 成本↑ (负相关)
- 可靠性↑ ↔ 复杂度↑ (负相关)
- 体积↓ ↔ 重量↓ (正相关)
- 兼容性↑ ↔ 开发周期↑ (负相关)

## 质量屋矩阵JSON格式

```json
{
  "version": "1.0",
  "customer_requirements": [...],
  "technical_requirements": [...],
  "relationship_matrix": [
    [0, 9, 3],
    [9, 0, 1],
    [3, 1, 0]
  ],
  "correlation_matrix": [
    [0, "?", "+3"],
    ["?", 0, "-1"],
    ["+3", "-1", 0]
  ],
  "technical_targets": {
    "TR1": "≤500ms",
    "TR2": "≥99.9%",
    "TR3": "MTBF>10000h"
  }
}
```

### 矩阵维度说明

- relationship_matrix: N×M矩阵，N=客户需求数，M=技术指标数
- correlation_matrix: M×M矩阵，对称矩阵，表示技术指标间的相关性

## 历史数据格式要求

### 优先级分析历史数据CSV

```csv
project_id,category,initial_weight,final_satisfaction,success_level
P001,功能,4,4.2,success
P001,性能,5,3.8,partial
P002,体验,3,3.5,success
P002,服务,4,4.0,success
```

### 技术可行性分析CSV

```csv
project_id,technical_requirement_id,difficulty_rating,implementation_status,actual_value,notes
P001,TR1,2,success,1800ms,优于目标
P001,TR2,4,success,99.5%,接近目标
P002,TR1,3,partial,2500ms,略超目标
P002,TR3,5,failure,未能实现,技术瓶颈
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| project_id | string | 项目唯一标识 |
| category | string | 需求类别 |
| initial_weight | float | 初始评估权重 |
| final_satisfaction | float | 最终满意度(1-5) |
| success_level | string | 成功度:success/partial/failure |
| technical_requirement_id | string | 技术指标ID |
| difficulty_rating | float | 实现难度(1-5) |
| implementation_status | string | 实现状态 |
| actual_value | string | 实际达成值 |
| notes | string | 备注说明 |

## 迭代优化变更格式

当需要更新质量屋时，使用以下变更格式:

```json
{
  "updated_weights": [
    {"id": "CR1", "weight": 4},
    {"id": "CR3", "weight": 5}
  ],
  "updated_relationships": [
    {"cr_idx": 0, "tr_idx": 1, "strength": 9}
  ],
  "updated_targets": {
    "TR1": "≤1000ms"
  }
}
```

## 示例

### 完整VOC分析示例

输入: 客户访谈记录
```
客户A: "希望产品用起来顺手，不需要看说明书"
客户B: "希望能快速打开使用，不要等太久"
客户C: "希望产品稳定，不要经常出问题"
```

结构化输出:
```json
{
  "customer_requirements": [
    {"id": "CR1", "name": "易上手", "weight": 5, "category": "体验"},
    {"id": "CR2", "name": "响应快", "weight": 4, "category": "性能"},
    {"id": "CR3", "name": "高可靠", "weight": 4, "category": "功能"}
  ]
}
```

### 质量屋构建示例

1. 生成模板: `python scripts/qfd_matrix.py template --cr 3 --tr 4 --output template.json`
2. 填写关系强度
3. 计算权重: `python scripts/qfd_matrix.py weight --matrix template.json --output weights.json`
4. 转换为Markdown查看: `python scripts/qfd_matrix.py weight --matrix template.json --format markdown`

## 验证规则

1. customer_requirements权重总和建议在15-25之间
2. 技术指标数量建议控制在8-12个
3. 关系矩阵中每个需求至少有一个强关系(9)
4. 相关性矩阵主对角线必须为0
5. 所有ID必须唯一且格式正确
