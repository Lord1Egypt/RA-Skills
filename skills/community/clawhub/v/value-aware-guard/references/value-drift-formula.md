# 价值漂移监测 - 详细计算公式与算法

## 核心概念

价值漂移指用户行为与其声明的核心价值之间的不一致程度。系统通过量化分析检测这种不一致，为适度干预提供依据。

### 价值定义结构

每个核心价值在系统中定义为：

```json
{
  "value_id": "health_priority",
  "name": "健康优先",
  "description": "将身体健康置于优先位置",
  "importance": 9, // 1-10，用户重要性评分
  "confirmed_at": "2026-03-15T10:30:00",
  "confirmation_method": "explicit_statement", // explicit_statement/behavior_pattern/inferred
  "evidence": [
    {"type": "statement", "content": "健康第一", "timestamp": "2026-03-15"},
    {"type": "behavior", "content": "定期运动记录", "timestamp": "2026-03-20"}
  ],
  "related_behaviors": {
    "supporting": ["早睡", "规律运动", "健康饮食"],
    "contradicting": ["熬夜", "久坐", "不健康饮食"]
  },
  "monitoring_frequency": "daily" // daily/weekly/monthly
}
```

## 漂移检测指标体系

### 1. 行为一致性指标

检测用户行为与价值声明的一致性。

#### 支持行为检测
当用户行为符合价值时记录：

```json
{
  "value": "健康优先",
  "behavior": "早睡",
  "timestamp": "2026-04-01T22:30:00",
  "confidence": 0.9,
  "source": "sleep_tracker" // conversation/sensor/external_api
}
```

#### 矛盾行为检测
当用户行为与价值冲突时记录：

```json
{
  "value": "健康优先", 
  "behavior": "熬夜",
  "timestamp": "2026-04-01T01:30:00",
  "severity": 0.7, // 矛盾严重程度 0-1
  "context": "工作项目截止期",
  "mitigating_factors": ["紧急任务", "团队依赖"]
}
```

### 2. 时间模式分析

分析价值一致性的时间分布模式。

#### 一致性频率
```
consistency_frequency = supporting_behaviors_count / (supporting_behaviors_count + contradicting_behaviors_count)
```

#### 趋势分析
计算最近7天 vs 前7天的变化：
```
trend_score = (recent_consistency - previous_consistency) / previous_consistency
```
- trend_score > 0: 一致性提升
- trend_score < 0: 一致性下降

### 3. 情境因素考量

考虑外部因素对行为的影响。

#### 压力水平调整
检测到高压情境时，降低矛盾行为权重：
```
adjusted_severity = raw_severity × (1 - stress_factor)
```
其中 stress_factor ∈ [0, 0.5]，基于压力检测结果。

#### 特殊时期调整
- 项目截止期：矛盾行为权重 × 0.8
- 家庭事务：矛盾行为权重 × 0.9  
- 节假日：支持行为权重 × 1.2

## 核心漂移计算公式

### 基础漂移分数

```
DriftScore = (contradiction_weight - support_weight) × importance_factor × time_decay

其中：
- contradiction_weight = Σ(矛盾行为权重 × 情境调整因子)
- support_weight = Σ(支持行为权重 × 情境增强因子)
- importance_factor = 价值重要性 / 10
- time_decay = e^(-days_since_last_assessment/7) // 最近数据权重更高
```

### 各分量详细计算

#### 矛盾行为权重计算

```
contradiction_weight = Σ(behavior_severity × frequency_factor × recency_factor)

behavior_severity: 行为矛盾严重程度（0-1）
frequency_factor: 频率调整（1 + log10(occurrence_count)）
recency_factor: 时间衰减，最近行为权重更高
```

#### 支持行为权重计算

```
support_weight = Σ(behavior_strength × consistency_factor × recency_factor)

behavior_strength: 行为支持强度（0-1）
consistency_factor: 一致性调整，连续支持行为权重递增
recency_factor: 时间衰减
```

### 漂移分数解释

| DriftScore 范围 | 解释 | 建议行动 |
|----------------|------|---------|
| (-∞, -0.3) | 高度一致 | 正向强化，无需干预 |
| [-0.3, 0.0) | 轻度一致 | 保持观察 |
| [0.0, 0.3) | 轻度偏离 | L1观察记录 |
| [0.3, 0.6) | 中度偏离 | L2温和提醒 |
| [0.6, 0.8) | 严重偏离 | L3严肃对话 |
| [0.8, ∞) | 极度偏离 | L4强制干预（如涉及风险） |

## 多维价值冲突分析

### 价值冲突矩阵

当多个价值间存在冲突时分析：

```json
{
  "conflict_matrix": {
    "health_priority": {
      "vs_family_first": 0.4,
      "vs_career_advancement": 0.7,
      "vs_quality_work": 0.3
    },
    "conflict_resolution": {
      "health_vs_career": {
        "user_preference": "situational", // balanced/priority_a/priority_b/situational
        "recent_trend": "career_increasing",
        "suggested_balance": 0.6 // 健康权重建议
      }
    }
  }
}
```

### 冲突检测算法

```
检测条件：用户行为同时涉及多个价值，且对不同价值有相反影响

例如：熬夜工作 → 损害健康优先，促进职业发展

冲突分数 = |value_A_impact - value_B_impact| × conflict_intensity

其中 conflict_intensity 基于：
- 价值重要性差异
- 行为影响程度差异
- 历史冲突频率
```

### 冲突解决建议

#### 平衡策略
当冲突分数 < 0.5 时：
- 提供平衡建议
- 强调价值间协调
- 建议时间分配优化

#### 优先级策略  
当冲突分数 ≥ 0.5 时：
- 基于用户历史偏好建议优先级
- 提供短期/长期视角
- 建议补偿机制

## 漂移预警生成

### 预警条件

同时满足以下条件时生成预警：
1. DriftScore ≥ 0.3（中度偏离）
2. 连续3天漂移趋势为负（一致性下降）
3. 无近期有效干预记录
4. 用户非明确拒绝状态

### 预警消息生成算法

```
预警消息 = 观察描述 + 影响说明 + 开放式问题

观察描述：基于具体数据，非评价性语言
影响说明：连接价值与行为后果
开放式问题：提供选择而非指令
```

#### 示例生成
```
输入：健康优先 DriftScore=0.45，最近3天熬夜2次

输出：
"注意到最近3天有2次工作到23点后，
这可能影响休息和第二天状态。
需要调整工作安排吗？"
```

### 预警优化学习

基于用户响应优化预警：

| 用户响应 | 优化动作 |
|---------|---------|
| 接受并改变 | 降低类似预警阈值 |
| 接受但未改变 | 保持阈值，优化时机 |
| 忽略 | 分析忽略原因（时机/语气/内容） |
| 拒绝 | 提高阈值，该话题沉默期 |

## 数据记录与分析

### 漂移计算记录

```json
{
  "drift_calculation": {
    "timestamp": "2026-04-01T23:00:00",
    "value": "健康优先",
    "time_period": "2026-03-25 to 2026-04-01",
    "input_data": {
      "supporting_behaviors": [
        {"behavior": "早睡", "count": 3, "avg_strength": 0.8},
        {"behavior": "运动", "count": 2, "avg_strength": 0.7}
      ],
      "contradicting_behaviors": [
        {"behavior": "熬夜", "count": 4, "avg_severity": 0.6}
      ],
      "context_factors": {
        "project_deadline": true,
        "stress_level": 0.6
      }
    },
    "intermediate_calculations": {
      "raw_contradiction": 2.4,
      "adjusted_contradiction": 1.92, // ×0.8压力调整
      "raw_support": 3.8,
      "importance_factor": 0.9,
      "time_decay": 0.95
    },
    "final_results": {
      "drift_score": 0.45,
      "confidence": 0.85,
      "trend": "deteriorating", // improving/stable/deteriorating
      "recommended_action": "L2_gentle_reminder"
    }
  }
}
```

### 长期趋势分析

#### 月度报告
分析每个价值的长期趋势：
- 漂移分数变化趋势
- 干预效果评估
- 价值重要性演化
- 行为模式变化

#### 个性化调整
基于历史数据调整：
- 用户敏感阈值（对提醒的接受度）
- 最佳干预时机
- 有效消息模板
- 价值权重动态调整

## 特殊情况处理

### 价值演化
用户价值可能随时间变化：
- 检测到长期一致性变化模式
- 询问确认价值优先级调整
- 更新价值定义和监控策略

### 外部重大事件
处理影响价值一致性的外部事件：
- 工作变动、家庭变化、健康事件
- 临时调整监控标准
- 提供额外支持而非批评

### 系统置信度管理
当数据不足或矛盾时：
- 明确标注低置信度
- 使用保守估计
- 优先收集更多数据而非立即干预
