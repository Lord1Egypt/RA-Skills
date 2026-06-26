# 示例：电商销售分析需求分析

本示例展示如何使用 requirement-analyst Skill 完成从原始需求到技术规格的完整分析流程。

---

## 场景背景

某电商平台需要建设销售分析数据仓库，支持运营团队进行日常销售监控和分析决策。

---

## 阶段1：需求解析

### 原始需求输入

```
我们是电商平台，需要分析销售业绩。目前每天运营同事都要从多个系统导数据做Excel，
效率很低还容易出错。我们希望有一个自动化的销售分析平台。

数据方面，我们有订单系统（MySQL）、用户系统（MySQL）、商品系统（MySQL）。
订单表每天大概新增100万条记录，已经跑了3年。

我们想看的指标包括销售额、订单量、客单价这些基本的，还要能按地区、
用户等级、商品类目来下钻分析。

另外，用户等级会变化，我们希望看当时的等级而不是现在的等级。
更新频率T+1就行，每天早上8点前出数据。
```

### Skill 调用

```bash
/requirement-parser 解析以下电商销售分析需求：
"我们是电商平台，需要分析销售业绩...
[粘贴上述需求]
"
```

### 解析输出

```yaml
# requirements/parsed/ecommerce_sales_parsed.yaml
version: "1.0"
parse_result:
  business_domain: "电商销售分析"
  business_goal: "建设自动化销售分析平台，支持运营决策"

  entities:
    - name: "订单"
      type: "业务实体"
      attributes: ["订单ID", "用户ID", "订单金额", "下单时间", "订单状态", "收货地区"]
      estimated_volume: "日增100万，历史3年约10亿"

    - name: "订单项"
      type: "业务实体"
      attributes: ["订单项ID", "订单ID", "商品ID", "数量", "单价"]

    - name: "用户"
      type: "业务实体"
      attributes: ["用户ID", "注册时间", "用户等级", "所在城市"]
      estimated_volume: "总量约5000万"

    - name: "商品"
      type: "业务实体"
      attributes: ["商品ID", "商品名称", "类目ID", "品牌", "价格"]

    - name: "类目"
      type: "业务实体"
      attributes: ["类目ID", "类目名称", "父类目ID", "层级"]

  business_processes:
    - name: "下单"
      entities_involved: ["订单", "订单项", "用户", "商品"]
    - name: "支付"
      entities_involved: ["订单"]

  metrics:
    - name: "GMV"
      alias: "成交总额"
      formula: "SUM(订单金额)"
      dimensions: ["日期", "地区", "用户等级", "类目"]
      frequency: "每日"

    - name: "订单量"
      formula: "COUNT(DISTINCT 订单ID)"
      dimensions: ["日期", "地区", "用户等级", "类目"]

    - name: "客单价"
      formula: "GMV / 订单量"
      dimensions: ["日期", "地区", "用户等级"]

    - name: "支付订单量"
      formula: "COUNT(DISTINCT CASE WHEN 订单状态='已支付' THEN 订单ID END)"
      dimensions: ["日期", "地区"]

  data_sources:
    - type: "MySQL"
      system: "订单系统"
      tables: ["orders", "order_items"]
      estimated_size: "日增100万订单，历史约10亿"

    - type: "MySQL"
      system: "用户系统"
      tables: ["users", "user_levels"]
      estimated_size: "用户5000万"

    - type: "MySQL"
      system: "商品系统"
      tables: ["products", "categories"]
      estimated_size: "商品100万，类目1000"

  requirements:
    freshness: "T+1"
    data_availability: "早上8点前"
    retention: "3年（历史已存在）"
    scd_requirement: "用户等级使用SCD Type 2保留历史"
    users: ["运营团队", "数据分析师"]

  inferred:
    architecture: "建议星型模型"
    fact_table: "订单项级别事实表"
    dimensions: ["日期", "用户(SCD2)", "商品", "类目"]
    tech_stack: "推荐 Snowflake + dbt + Airflow"
```

---

## 阶段2：需求澄清

### Skill 调用

```bash
/requirement-clarify 基于 ecommerce_sales_parsed.yaml 识别需求缺口
```

### 澄清输出

```markdown
# 需求澄清报告

## 🔴 高风险缺口（必须澄清）

### 1. GMV计算口径
**问题**: GMV的计算口径是什么？
- 是下单金额还是支付金额？
- 是否包含已取消/退款订单？
- 是否包含运费？
- 是否扣除优惠券？

**建议确认问题**:
"GMV是按下单时间统计的下单金额，还是按支付时间统计的实付金额？
退款订单如何处理？"

### 2. 用户等级SCD策略
**问题**: 解析中提到"看当时的等级"，需要明确：
- 用户等级变化频率如何？
- 需要保留每次变化的完整历史吗？
- 分析时如何关联？

**建议确认问题**:
"用户等级变化时，需要保留历史记录吗？比如用户1月1日是普通会员，
1月15日升级为VIP，看1月1日的订单时，显示当时的普通会员还是现在的VIP？"

### 3. 订单状态流转
**问题**: 订单有哪些状态？如何流转？
- 是否包含未支付订单？
- 取消订单是否计入订单量？

**建议确认问题**:
"订单状态有哪些？（如：待支付、已支付、已发货、已完成、已取消）
各指标的计算口径是什么？"

## 🟡 中等风险缺口（建议澄清）

### 4. 数据范围
**问题**:
- 历史数据从什么时候开始？
- 是否需要回溯全部3年历史？
- 测试/内部订单是否排除？

### 5. 地区维度
**问题**:
- 地区是指收货地址还是下单IP？
- 地区粒度到哪里？（省/市/区）
- 海外订单如何处理？

### 6. 商品类目
**问题**:
- 类目有几级？
- 分析时按当前类目还是下单时类目？
- 类目调整时历史数据如何处理？

## 🟢 低风险缺口（可选澄清）

### 7. 技术约束
- 目标数仓平台有偏好吗？
- 源系统允许什么时间段抽取？
- 数据延迟容忍度？（如8:10出数据可以吗？）

### 8. 权限要求
- 不同运营角色能看到的数据范围？
- 是否需要行级权限控制？

## 确认后决策记录

| 决策项 | 决策内容 | 决策依据 | 决策人 | 日期 |
|--------|---------|---------|--------|------|
| GMV口径 | 按下单时间统计的支付成功金额，扣除退款 | 与财务口径一致 | 运营负责人 | 2024-01-10 |
| 用户等级 | 使用SCD Type 2，关联当时的等级 | 运营分析需求 | 运营负责人 | 2024-01-10 |
| 订单状态 | 仅包含支付成功订单 | 避免未支付订单干扰 | 运营负责人 | 2024-01-10 |
| 地区 | 使用收货地址，粒度到市 | 与物流口径一致 | 运营负责人 | 2024-01-10 |
| 类目 | 使用下单时类目，SCD Type 1 | 类目不常变化 | 运营负责人 | 2024-01-10 |

## 风险预警

⚠️ **数据质量风险**: 历史数据可能存在质量问题，建议增加数据清洗环节
⚠️ **性能风险**: 10亿级订单数据，需要考虑分区策略
⚠️ **一致性风险**: 跨系统数据关联可能存在时间差
```

---

## 阶段3：需求转化

### Skill 调用

```bash
/requirement-transform 基于确认后的电商销售分析需求生成技术规格
```

### 转化输出

#### 1. 数据模型规格

```yaml
# specs/ecommerce_model_spec.yaml
model_spec:
  version: "1.0"
  project: "电商销售分析数仓"

  architecture:
    type: "星型模型"
    description: "以订单项为粒度的销售分析模型"

  fact_tables:
    - name: fct_order_items
      grain: "订单项级别 - 每个订单中的每个商品一行"
      description: "订单项事实表，记录每个商品的购买详情"

      source_tables:
        primary: "order_items"
        lookup: ["orders", "users", "products"]

      dimensions:
        - dim_date
        - dim_user
        - dim_product
        - dim_category

      measures:
        - name: quantity
          type: "integer"
          description: "购买数量"
          aggregation: "sum"

        - name: unit_price
          type: "decimal(18,2)"
          description: "商品单价"

        - name: item_amount
          type: "decimal(18,2)"
          description: "商品金额 = 数量 * 单价"
          aggregation: "sum"

        - name: discount_amount
          type: "decimal(18,2)"
          description: "优惠金额"
          aggregation: "sum"

        - name: paid_amount
          type: "decimal(18,2)"
          description: "实付金额"
          aggregation: "sum"

      degenerate_dimensions:
        - name: order_id
          description: "订单ID（退化维度）"
        - name: order_no
          description: "订单编号"

      calculated_measures:
        - name: gmv
          formula: "SUM(paid_amount)"
          description: "成交总额"

        - name: order_count
          formula: "COUNT(DISTINCT order_id)"
          description: "订单数"

        - name: avg_order_value
          formula: "gmv / order_count"
          description: "客单价"

  dimensions:
    - name: dim_date
      scd_type: 0
      description: "日期维度"
      source: "自动生成"

    - name: dim_user
      scd_type: 2
      description: "用户维度，SCD Type 2追踪等级变化"
      natural_key: "user_id"

      attributes:
        - name: user_id
          type: "bigint"
          is_key: true

        - name: user_nk
          type: "varchar(50)"
          description: "用户自然键（业务ID）"

        - name: user_level
          type: "varchar(20)"
          track_history: true

        - name: city
          type: "varchar(50)"
          track_history: false

        - name: register_date
          type: "date"
          track_history: false

        - name: effective_date
          type: "date"
          description: "记录生效日期"

        - name: expiry_date
          type: "date"
          description: "记录失效日期"

        - name: is_current
          type: "boolean"
          description: "是否当前有效记录"

    - name: dim_product
      scd_type: 2
      description: "商品维度"
      natural_key: "product_id"

      attributes:
        - name: product_id
          type: "bigint"
          is_key: true

        - name: product_name
          type: "varchar(200)"

        - name: brand
          type: "varchar(100)"
          track_history: true

        - name: current_price
          type: "decimal(18,2)"
          track_history: true

    - name: dim_category
      scd_type: 1
      description: "类目维度"
      natural_key: "category_id"

      attributes:
        - name: category_id
          type: "bigint"
          is_key: true

        - name: category_name
          type: "varchar(100)"

        - name: parent_category_id
          type: "bigint"

        - name: category_level
          type: "int"
          description: "类目层级（1/2/3级）"

  physical_design:
    fct_order_items:
      partitioning:
        type: "range"
        column: "date_key"
        granularity: "month"

      clustering:
        columns: ["user_sk", "product_sk"]

      indexes:
        - columns: ["order_id"]
        - columns: ["date_key", "user_sk"]
```

#### 2. ETL规格

```yaml
# specs/ecommerce_etl_spec.yaml
etl_spec:
  version: "1.0"

  pipelines:
    - name: order_sync
      description: "订单数据同步"
      priority: "high"

      source:
        type: "MySQL"
        connection: "order_db"
        tables:
          - name: "orders"
            columns: ["order_id", "user_id", "order_no", "total_amount", "status", "created_at", "updated_at", "receiver_city"]
          - name: "order_items"
            columns: ["item_id", "order_id", "product_id", "quantity", "unit_price", "item_amount", "discount_amount", "paid_amount"]

      extract:
        strategy: "incremental"
        watermark_column: "updated_at"
        lookback_hours: 24

      transform:
        logic:
          - name: "filter_paid_orders"
            description: "过滤已支付订单"
            condition: "orders.status = 'paid'"

          - name: "join_order_items"
            description: "关联订单和订单项"
            join_type: "inner"

          - name: "lookup_user_sk"
            description: "关联用户维表获取代理键（SCD2）"
            lookup_table: "dim_user"
            condition: "user_id = dim_user.user_nk AND dim_user.is_current = true"

          - name: "lookup_product_sk"
            description: "关联商品维表获取代理键"
            lookup_table: "dim_product"
            condition: "product_id = dim_product.product_nk"

      load:
        target: "fct_order_items"
        mode: "upsert"
        unique_key: ["order_id", "product_sk"]
        partition_column: "date_key"

      schedule:
        frequency: "daily"
        start_time: "02:00"
        timeout: "2h"

      quality_checks:
        - name: "row_count_check"
          type: "anomaly"
          description: "行数异常检测"

        - name: "gmv_check"
          type: "reconciliation"
          source_query: "SELECT SUM(paid_amount) FROM order_items JOIN orders..."

    - name: user_dimension_sync
      description: "用户维度同步（SCD Type 2）"
      priority: "high"

      source:
        type: "MySQL"
        connection: "user_db"
        tables:
          - name: "users"
            columns: ["user_id", "user_name", "user_level", "city", "register_date", "updated_at"]

      extract:
        strategy: "incremental"
        watermark_column: "updated_at"

      transform:
        logic:
          - name: "scd_type2_handler"
            description: "处理SCD Type 2变更"
            track_columns: ["user_level"]
            current_flag_column: "is_current"
            effective_date_column: "effective_date"
            expiry_date_column: "expiry_date"

      load:
        target: "dim_user"
        mode: "upsert"
        unique_key: ["user_nk", "effective_date"]

    - name: product_dimension_sync
      description: "商品维度同步"
      priority: "medium"

      source:
        type: "MySQL"
        connection: "product_db"
        tables:
          - name: "products"
            columns: ["product_id", "product_name", "brand", "price", "category_id", "updated_at"]

      extract:
        strategy: "incremental"
        watermark_column: "updated_at"

      transform:
        logic:
          - name: "scd_type2_handler"
            track_columns: ["brand", "price"]

      load:
        target: "dim_product"
        mode: "upsert"

  dependencies:
    - pipeline: "user_dimension_sync"
      must_complete_before: ["order_sync"]

    - pipeline: "product_dimension_sync"
      must_complete_before: ["order_sync"]
```

#### 3. 数据质量规格

```yaml
# specs/ecommerce_dq_spec.yaml
dq_spec:
  version: "1.0"

  rules:
    # 事实表质量规则
    - table: fct_order_items
      column: order_item_sk
      rules:
        - type: not_null
          severity: error
        - type: unique
          severity: error

    - table: fct_order_items
      column: order_id
      rules:
        - type: not_null
          severity: error

    - table: fct_order_items
      column: quantity
      rules:
        - type: not_null
          severity: error
        - type: positive
          severity: error

    - table: fct_order_items
      column: paid_amount
      rules:
        - type: not_null
          severity: error
        - type: range
          min: 0
          max: 1000000
          severity: warning

    - table: fct_order_items
      column: user_sk
      rules:
        - type: not_null
          severity: error
        - type: relationship
          ref_table: dim_user
          ref_column: user_sk
          severity: error

    # 维度表质量规则
    - table: dim_user
      column: user_sk
      rules:
        - type: not_null
          severity: error
        - type: unique
          severity: error

    - table: dim_user
      column: user_nk
      rules:
        - type: not_null
          severity: error

    - table: dim_user
      column: is_current
      rules:
        - type: accepted_values
          values: [true, false]
          severity: error

  table_level_checks:
    fct_order_items:
      - name: "daily_gmv_range"
        description: "日GMV在合理范围内"
        type: "custom_sql"
        sql: |
          SELECT date_key, SUM(paid_amount) as daily_gmv
          FROM fct_order_items
          WHERE date_key >= CURRENT_DATE - 7
          GROUP BY date_key
          HAVING daily_gmv < 1000000 OR daily_gmv > 1000000000
        severity: warning

      - name: "order_count_anomaly"
        description: "订单数异常检测"
        type: "anomaly"
        column: "order_id"
        aggregation: "count_distinct"
        threshold: 3  # 3个标准差

  pipeline_checks:
    order_sync:
      - name: "source_target_reconciliation"
        description: "源表和目标表数据一致性校验"
        type: "reconciliation"
        source_query: "SELECT COUNT(*) FROM orders WHERE updated_at >= '{{ yesterday }}'"
        target_query: "SELECT COUNT(DISTINCT order_id) FROM fct_order_items WHERE date_key = '{{ yesterday_key }}'"
        tolerance: 0.01  # 1%容差

  alerting:
    channels:
      - type: "email"
        recipients: ["data-team@company.com"]
        for_severity: [error, warning]

      - type: "slack"
        channel: "#data-alerts"
        for_severity: [error]

    thresholds:
      error_rate: 0.001  # 0.1%
      warning_rate: 0.01  # 1%
```

#### 4. 下游Skill调用指令

```markdown
# 下游 Skill 调用指令

根据需求转化结果，建议按以下顺序执行：

## Step 1: 数据建模

```bash
/model-design 为电商销售分析设计维度模型：

业务背景：
- 电商平台销售分析
- 日增100万订单，历史约10亿
- 需要支持GMV、订单量、客单价分析
- 维度包括日期、用户(SCD2)、商品(SCD2)、类目

事实表规格：
- 名称: fct_order_items
- 粒度: 订单项级别
- 度量: quantity, unit_price, item_amount, discount_amount, paid_amount
- 退化维度: order_id, order_no

维度表规格：
- dim_user: SCD Type 2，追踪user_level变化
- dim_product: SCD Type 2，追踪brand/price变化
- dim_category: SCD Type 1
- dim_date: 标准日期维

技术要求：
- 目标平台: Snowflake
- 分区: 按月分区
- 聚簇: user_sk, product_sk
```

## Step 2: SQL开发

```bash
/sql-gen 生成订单事实表抽取SQL：

源表：
- orders (order_id, user_id, order_no, total_amount, status, created_at, updated_at, receiver_city)
- order_items (item_id, order_id, product_id, quantity, unit_price, item_amount, discount_amount, paid_amount)

抽取条件：
- 仅status='paid'的订单
- 增量抽取，updated_at > '{{ last_extract_time }}'

转换逻辑：
- JOIN orders和order_items
- LOOKUP dim_user获取user_sk（SCD2关联）
- LOOKUP dim_product获取product_sk
- 生成date_key

目标: fct_order_items
```

## Step 3: ETL开发

```bash
/etl-template 生成订单同步Pipeline：

配置：
- 名称: order_sync
- 源: MySQL (orders, order_items)
- 目标: Snowflake (fct_order_items)
- 策略: 增量UPSERT
- 调度: 每日凌晨2点
- 依赖: user_dimension_sync, product_dimension_sync

特殊要求：
- 需要SCD Type 2 lookup逻辑
- 需要数据质量检查
- 超时2小时告警
```

## Step 4: 数据质量

```bash
/dq-rule-gen 为电商销售数仓生成质量规则：

目标表：
- fct_order_items: 主键、非空、外键、范围检查
- dim_user: SCD2完整性
- dim_product: SCD2完整性

质量维度：
- 完整性: 主键非空、外键有效
- 准确性: 金额范围、数量正数
- 一致性: 源目标对账
- 时效性: 数据新鲜度

告警：
- Error → Slack + Email
- Warning → Email
```

## 执行顺序

```
1. /model-design → 生成模型设计
2. /sql-gen → 生成维度表DDL
3. 执行维度表DDL
4. /etl-template → 生成维度同步Pipeline
5. 运行维度同步（初始化）
6. /sql-gen → 生成事实表抽取SQL
7. /etl-template → 生成事实表同步Pipeline
8. /dq-rule-gen → 生成质量规则
9. 部署Pipeline并测试
```
```

---

## 完整需求包

```yaml
# outputs/requirement_package.yaml
requirement_package:
  version: "1.0"

  metadata:
    project_name: "电商销售分析数仓"
    analyst: "requirement-analyst"
    generated_at: "2024-01-15T10:00:00Z"
    confirmed: true

  business:
    domain: "电商"
    subdomain: "销售分析"
    owner: "销售运营部"
    goal: "建设自动化销售分析平台，支持运营决策"
    success_criteria:
      - "日报自动生成，早上8点前出数"
      - "支持按地区/用户等级/类目下钻分析"
      - "数据准确性与财务口径一致"

  functional:
    entities:
      - 订单
      - 订单项
      - 用户
      - 商品
      - 类目

    metrics:
      - GMV
      - 订单量
      - 客单价

    dimensions:
      - 日期
      - 用户(SCD2)
      - 商品(SCD2)
      - 类目

  non_functional:
    freshness: "T+1"
    retention: "3年"
    availability: "99.9%"
    data_availability: "08:00"

  technical:
    preferred_stack: ["Snowflake", "dbt", "Airflow"]
    estimated_volume:
      daily: "100万订单"
      total: "约10亿历史订单"

  specifications:
    model_spec:
      file: "specs/ecommerce_model_spec.yaml"
    etl_spec:
      file: "specs/ecommerce_etl_spec.yaml"
    dq_spec:
      file: "specs/ecommerce_dq_spec.yaml"

  downstream_tasks:
    - skill: "model-design"
      priority: high
    - skill: "sql-gen"
      priority: high
    - skill: "etl-template"
      priority: high
    - skill: "dq-rule-gen"
      priority: medium
```

---

## 使用总结

通过这个示例，可以看到 requirement-analyst Skill 如何将模糊的业务需求：

1. **解析**为结构化的实体、指标、维度
2. **澄清**识别出关键缺口并得到确认
3. **转化**为可执行的技术规格

最终生成的 `requirement_package.yaml` 可以直接驱动下游 Skill 进行自动化开发。
