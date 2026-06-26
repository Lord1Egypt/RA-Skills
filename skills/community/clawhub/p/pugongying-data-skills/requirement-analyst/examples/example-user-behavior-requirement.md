# 示例：用户行为分析需求分析

本示例展示复杂实时场景下的需求分析流程，涉及埋点数据、实时计算、用户画像等。

---

## 场景背景

某内容平台需要建设用户行为分析系统，支持实时推荐优化和用户增长分析。

---

## 原始需求

```
我们是内容平台，想建设用户行为分析系统。

目前埋点数据发到Kafka，格式是JSON，每天大概10亿条事件。
事件类型包括：曝光、点击、播放、点赞、评论、分享、关注等。

我们需要：
1. 实时看板：当前在线用户数、每秒事件量
2. 用户画像：每个用户的兴趣标签、活跃度分级
3. 漏斗分析：曝光→点击→播放→互动的转化
4. 留存分析：次日/7日/30日留存

实时性要求：实时看板延迟<5秒，其他分析T+1即可。

数据要保留1年，用户画像需要每日更新。
```

---

## 阶段1：需求解析

### 解析输出

```yaml
version: "1.0"
parse_result:
  business_domain: "内容平台用户行为分析"
  business_goal: "支持实时推荐优化和用户增长分析"

  entities:
    - name: "用户"
      attributes: ["用户ID", "注册时间", "设备类型", "渠道来源"]
      estimated_volume: "日活5000万，总量2亿"

    - name: "内容"
      attributes: ["内容ID", "内容类型", "作者ID", "标签", "发布时间"]
      estimated_volume: "总量1亿"

    - name: "事件"
      attributes: ["事件ID", "用户ID", "内容ID", "事件类型", "事件时间", "事件属性"]
      estimated_volume: "日增10亿"

  business_processes:
    - name: "内容消费"
      steps: ["曝光", "点击", "播放", "互动"]

  metrics:
    - name: "DAU"
      formula: "COUNT(DISTINCT 用户ID)"
      real_time: true

    - name: "曝光量"
      formula: "COUNT(事件ID WHERE 事件类型='impression')"
      real_time: true

    - name: "点击率"
      formula: "点击量 / 曝光量"

    - name: "播放完成率"
      formula: "完成播放次数 / 播放次数"

    - name: "次日留存率"
      formula: "次日活跃用户数 / 首日新增用户数"

  data_sources:
    - type: "Kafka"
      topic: "user_events"
      format: "JSON"
      volume: "10亿/日"

    - type: "MySQL"
      system: "用户中心"
      tables: ["users", "user_profiles"]

  requirements:
    real_time:
      dashboard_latency: "< 5秒"
    batch:
      user_profile_update: "T+1"
      retention_analysis: "T+1"
    retention: "1年"
```

---

## 阶段2：需求澄清

### 关键澄清点

```markdown
## 🔴 关键澄清

### 1. 实时 vs 批量边界
**问题**: 哪些指标需要实时？哪些可以T+1？

**确认结果**:
| 指标 | 实时性 | 技术方案 |
|------|--------|---------|
| 在线用户数 | 实时(<5s) | Flink + Redis |
| 每秒事件量 | 实时(<5s) | Flink + Redis |
| 用户画像标签 | T+1 | Spark批处理 |
| 留存分析 | T+1 | Spark批处理 |
| 漏斗分析 | 准实时(1min) | Flink窗口 |

### 2. 用户识别方式
**问题**: 如何识别同一个用户？

**确认结果**:
- 登录用户：使用user_id
- 未登录用户：使用device_id
- 关联策略：device_id首次登录后关联到user_id

### 3. 事件属性复杂度
**问题**: 事件属性有哪些？是否标准化？

**确认结果**:
- 公共属性：用户ID、设备ID、时间戳、平台、版本
- 事件特有属性：内容ID、播放时长、互动类型等
- 属性变化：可能新增属性，需要Schema演进支持

### 4. 用户画像标签体系
**问题**: 需要哪些标签？如何计算？

**确认结果**:
- 兴趣标签：基于内容消费行为（观看时长、互动）
- 活跃度：基于近7天活跃天数分级
- 生命周期：新用户/活跃用户/流失预警/沉默用户
- 价值分层：基于消费频次和内容贡献
```

---

## 阶段3：需求转化

### 1. 数据架构规格

```yaml
# Lambda架构：实时流 + 批量批
architecture:
  type: "Lambda"
  layers:
    speed_layer:
      engine: "Flink"
      use_case: "实时指标、即席查询"
      latency: "< 5秒"

    batch_layer:
      engine: "Spark"
      use_case: "用户画像、留存分析、历史数据"
      schedule: "每日"

    serving_layer:
      type: "OLAP"
      engine: "ClickHouse"
      use_case: "报表查询、多维分析"
```

### 2. 实时流规格

```yaml
stream_spec:
  source:
    type: "Kafka"
    topic: "user_events"
    format: "JSON"
    partitions: 100

  processing:
    engine: "Flink"
    parallelism: 50

    windows:
      - name: "1min_window"
        type: "tumbling"
        size: "1 minute"
        use_for: ["实时PV/UV", "漏斗分析"]

      - name: "5min_window"
        type: "tumbling"
        size: "5 minute"
        use_for: ["趋势分析"]

  sinks:
    - type: "Redis"
      use_for: "实时看板指标"
      ttl: "1小时"

    - type: "ClickHouse"
      use_for: "明细数据存储"
      retention: "1年"
```

### 3. 用户画像规格

```yaml
user_profile_spec:
  update_frequency: "daily"
  storage: "HBase"

  tags:
    - name: "interest_tags"
      type: "multi_value"
      source: "内容消费行为"
      algorithm: "TF-IDF权重计算"
      ttl: "30天"

    - name: "activity_level"
      type: "enum"
      values: ["高活跃", "中活跃", "低活跃", "流失预警", "沉默"]
      source: "近7天活跃天数"
      rules:
        - "高活跃: 活跃天数 >= 5"
        - "中活跃: 活跃天数 >= 3"
        - "低活跃: 活跃天数 >= 1"
        - "流失预警: 近7天未活跃但之前活跃"
        - "沉默: 长期未活跃"

    - name: "lifecycle_stage"
      type: "enum"
      values: ["新用户", "成长用户", "成熟用户", "衰退用户", "流失用户"]
      source: "注册时间 + 活跃行为"
```

### 4. 下游Skill调用指令

```bash
# Step 1: 实时流开发
/etl-template 生成Flink实时处理Pipeline：
- 源: Kafka (user_events topic)
- 处理: JSON解析、窗口聚合、用户关联
- 输出: Redis(实时指标) + ClickHouse(明细)

# Step 2: 用户画像批处理
/etl-template 生成Spark用户画像Pipeline：
- 源: ClickHouse事件明细
- 处理: 兴趣标签计算、活跃度分级、生命周期判断
- 输出: HBase用户画像

# Step 3: 数据质量
/dq-rule-gen 生成行为数据质量规则：
- 事件时间合法性
- 用户ID/DeviceID至少一个存在
- 事件类型枚举值检查
- 实时流延迟监控
```

---

## 需求包摘要

```yaml
requirement_package:
  project: "用户行为分析平台"
  complexity: "高"
  architecture: "Lambda (实时+批量)"

  key_challenges:
    - "日增10亿事件的高吞吐处理"
    - "实时(<5s)和批量(T+1)双重要求"
    - "复杂用户画像标签计算"

  tech_stack:
    streaming: ["Kafka", "Flink"]
    batch: ["Spark", "HDFS"]
    storage: ["ClickHouse", "HBase", "Redis"]

  downstream:
    - skill: etl-assistant
      tasks: ["flink-stream", "spark-batch"]
    - skill: dq-assistant
      tasks: ["streaming-quality", "batch-quality"]
```
