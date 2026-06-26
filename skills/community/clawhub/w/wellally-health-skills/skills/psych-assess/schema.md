# 心理健康评估 Schema

心理健康评估记录的完整数据结构定义。

## 评估类型

| 类型 | 说明 |
|-----|------|
| full | 全面评估（约10-15分钟） |
| quick | 快速筛查（约2分钟） |
| followup | 随访评估 |

## 核心字段

### 基本信息

| 字段 | 类型 | 说明 |
|-----|------|------|
| `id` | string | 唯一标识符，格式：psych_YYYYMMDDHHMMSS_XXX |
| `assessment_type` | enum | 评估类型：full/quick/followup |
| `created_at` | datetime | 创建时间（ISO 8601） |
| `assessment_date` | date | 评估日期（YYYY-MM-DD） |
| `assessment_time` | time | 评估时间（HH:MM） |

### 基线信息 (baseline)

| 字段 | 类型 | 说明 |
|-----|------|------|
| `reason_for_assessment` | string | 评估原因 |
| `recent_life_changes` | array | 近期生活变化 |
| `social_support.has_support` | boolean | 是否有社会支持 |
| `social_support.support_quality` | enum | 支持质量：high/moderate/low |
| `social_support.support_types` | array | 支持类型：family/friends等 |
| `user_goals` | array | 用户目标 |

## 量表评分 (scales)

### PHQ-9 抑郁症状评估

| 字段 | 类型 | 说明 |
|-----|------|------|
| `administered` | boolean | 是否施测 |
| `total_score` | integer | 总分（0-27） |
| `max_score` | integer | 满分（27） |
| `severity` | enum | 严重程度：none/mild/moderate/moderately_severe/severe |
| `severity_code` | enum | 严重程度代码：none/mild/moderate/moderate_severe/severe |
| `item_responses[]` | array | 题目回答 |
| `item_responses[].item` | integer | 题号（1-9） |
| `item_responses[].score` | integer | 得分（0-3） |
| `item_responses[].question` | string | 题目内容 |

**PHQ-9 评分标准**：
- 0-4分：无抑郁 (none)
- 5-9分：轻度抑郁 (mild)
- 10-14分：中度抑郁 (moderate)
- 15-19分：中重度抑郁 (moderate_severe)
- 20-27分：重度抑郁 (severe)

### PHQ-2 抑郁快速筛查

| 字段 | 类型 | 说明 |
|-----|------|------|
| `total_score` | integer | 总分（0-6） |
| `severity` | enum | 结果：negative/positive |

**判断标准**：得分 >= 3 为阳性 (positive)

### GAD-7 焦虑症状评估

| 字段 | 类型 | 说明 |
|-----|------|------|
| `total_score` | integer | 总分（0-21） |
| `max_score` | integer | 满分（21） |
| `severity` | enum | 严重程度：minimal/mild/moderate/severe |
| `severity_code` | enum | 严重程度代码：minimal/mild/moderate/severe |
| `item_responses[]` | array | 题目回答（7题） |

**GAD-7 评分标准**：
- 0-4分：轻微焦虑 (minimal)
- 5-9分：轻度焦虑 (mild)
- 10-14分：中度焦虑 (moderate)
- 15-21分：重度焦虑 (severe)

### GAD-2 焦虑快速筛查

| 字段 | 类型 | 说明 |
|-----|------|------|
| `total_score` | integer | 总分（0-6） |
| `severity` | enum | 结果：negative/positive |

**判断标准**：得分 >= 3 为阳性 (positive)

### PSS-4 知觉压力量表

| 字段 | 类型 | 说明 |
|-----|------|------|
| `total_score` | integer | 总分（0-16） |
| `max_score` | integer | 满分（16） |
| `severity` | enum | 压力水平：low/moderate/high |

**PSS-4 评分标准**：
- 0-6分：低压力 (low)
- 7-10分：中等压力 (moderate)
- 11-16分：高压力 (high)

**注意**：Q3和Q4为反向计分题

### WHO-5 幸福感指数

| 字段 | 类型 | 说明 |
|-----|------|------|
| `total_score` | integer | 总分（0-25） |
| `max_score` | integer | 满分（25） |
| `wellbeing` | enum | 幸福感：poor/moderate/good |

**WHO-5 评分标准**：
- 0-12分：幸福感低 (poor)
- 13-18分：幸福感中等 (moderate)
- 19-25分：幸福感良好 (good)

### 睡眠质量评估

| 字段 | 类型 | 说明 |
|-----|------|------|
| `duration_hours` | number | 睡眠时长（小时） |
| `latency_minutes` | integer | 入睡时间（分钟） |
| `night_awakenings` | integer | 夜醒次数 |
| `quality_rating` | integer | 主观质量（1=很好，5=很差） |
| `composite_score` | integer | 综合得分（0-12） |
| `max_score` | integer | 满分（12） |
| `severity` | enum | 睡眠质量：good/moderate/poor |

**睡眠质量评分标准**：
- 0-3分：睡眠良好 (good)
- 4-6分：睡眠一般 (moderate)
- 7-12分：睡眠差 (poor)

## 危机评估 (crisis_assessment)

### 基本字段

| 字段 | 类型 | 说明 |
|-----|------|------|
| `triggered` | boolean | 是否触发危机评估 |
| `crisis_risk_level` | enum | 风险等级：minimal/low/moderate/high/critical |
| `immediate_danger` | boolean | 是否有立即危险 |

### 增强危机评估 (enhanced_assessment)

| 字段 | 类型 | 范围 | 说明 |
|-----|------|------|------|
| `frequency_score` | integer | 0-2 | 念头频率 |
| `intensity_score` | integer | 0-2 | 念头强度 |
| `plan_specificity` | integer | 0-2 | 计划具体性 |
| `means_availability` | integer | 0-2 | 手段可获得性 |
| `intent_strength` | integer | 0-3 | 实施意图强度 |
| `prior_attempts` | integer | 0-2 | 既往尝试次数 |
| `protective_factors[]` | array | - | 保护性因素 |

### 危机风险等级分层

| 风险等级 | 说明 | 响应 |
|---------|------|------|
| critical | 危急 | 立即拨打热线、前往急诊、不要独处 |
| high | 高危 | 立即寻求专业帮助、制定安全计划 |
| moderate | 中危 | 48小时内预约心理医生 |
| low | 低危 | 心理咨询、自助资源 |
| minimal | 无风险 | 定期监测、健康生活方式 |

## 风险分层 (risk_stratification)

| 字段 | 类型 | 说明 |
|-----|------|------|
| `overall_risk` | enum | 整体风险等级 |
| `primary_concerns[]` | array | 主要关注点 |
| `primary_concerns[].domain` | string | 领域（如depression） |
| `primary_concerns[].severity` | string | 严重程度 |
| `strengths[]` | array | 优势因素 |
| `recommended_action` | string | 建议行动 |
| `urgency` | string | 紧急程度描述 |
| `urgency_code` | string | 紧急程度代码 |

## 建议 (recommendations)

### 立即行动 (immediate)

| 字段 | 类型 | 说明 |
|-----|------|------|
| `priority` | string | 优先级：high/medium/low |
| `action` | string | 行动类型代码 |
| `timeframe` | string | 时间框架 |
| `description` | string | 行动描述 |

### 自助建议 (self_help)

| 字段 | 类型 | 说明 |
|-----|------|------|
| `category` | string | 类别（如sleep_hygiene） |
| `recommendations[]` | array | 建议列表 |

### 随访评估 (follow_up_assessment)

| 字段 | 类型 | 说明 |
|-----|------|------|
| `recommended_interval` | string | 建议间隔（如2_weeks） |
| `next_assessment_date` | date | 下次评估日期 |
| `what_to_monitor[]` | array | 监测项目 |

## 数据关联 (correlations)

| 字段 | 类型 | 说明 |
|-----|------|------|
| `linked_mood_ids[]` | array | 关联的情绪记录ID |
| `linked_symptom_ids[]` | array | 关联的症状记录ID |
| `linked_medication_ids[]` | array | 关联的用药记录ID |

## 元数据 (metadata)

| 字段 | 类型 | 说明 |
|-----|------|------|
| `created_at` | datetime | 创建时间 |
| `last_updated` | datetime | 最后更新时间 |
| `assessment_duration_minutes` | number | 评估耗时（分钟） |
| `completed` | boolean | 是否完成 |
| `data_quality` | enum | 数据质量：low/moderate/high |
| `user_engagement` | enum | 用户参与度：low/moderate/high |

## 数据存储

- 评估记录：`data/psych-assessments/YYYY-MM/YYYY-MM-DD_HHMM_type.json`
- 对话记录：`data/psych-assessments/YYYY-MM/dialogue_YYYY-MM-DD_HHMM.json`

## 对话记录结构

### 字段说明

| 字段 | 类型 | 说明 |
|-----|------|------|
| `id` | string | 对话ID，格式：dialogue_YYYYMMDDHHMMSS_XXX |
| `linked_assessment_id` | string | 关联的评估ID |
| `session_type` | string | 会话类型（如post_assessment_support） |
| `session_context.days_since_assessment` | integer | 距离评估的天数 |
| `session_context.current_risk_level` | string | 当前风险等级 |
| `session_context.session_goal` | string | 会话目标 |
| `conversation[]` | array | 对话记录 |
| `conversation[].turn` | integer | 轮次 |
| `conversation[].speaker` | enum | 发言者：ai/user |
| `conversation[].content` | string | 内容 |
| `conversation[].mode` | string | AI模式（如warm_supportive） |
| `session_outcome.user_mood_start` | string | 开始时情绪 |
| `session_outcome.user_mood_end` | string | 结束时情绪 |
| `session_outcome.insights_gained[]` | array | 获得的洞察 |
| `session_outcome.action_items_set[]` | array | 设定的行动项 |
