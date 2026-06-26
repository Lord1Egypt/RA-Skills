---
name: model-design
description: |
  数据模型设计助手 - 维度建模设计、星型/雪花模型建议、SCD策略选择。
  当用户需要设计数据仓库模型、维度建模、事实表设计时触发。
  触发词：设计数据模型、维度建模、事实表设计、SCD策略、星型模型。
argument: { description: "业务场景描述和模型需求", required: true }
agent: general-purpose
allowed-tools: [Read, Grep, Glob, Edit, Write, Bash]
---

# 数据模型设计助手

基于业务需求设计专业的维度数据模型，包括事实表、维度表、SCD策略等。

## 工作流程

1. **业务分析** - 理解业务流程和分析需求
2. **粒度确定** - 确定事实表的粒度（最细级别）
3. **维度识别** - 识别相关的业务维度
4. **度量确定** - 确定可累加的度量值
5. **模型生成** - 输出完整的数据模型设计

## 输出规范

### 模型设计文档模板

```markdown
# 数据模型设计方案

## 1. 业务背景

**业务流程**：订单销售流程
**分析需求**：销售趋势分析、用户购买行为分析、商品销售分析
**数据来源**：业务系统订单表、用户表、商品表

## 2. 模型概览

**模型类型**：星型模型
**事实表粒度**：单笔订单商品项级别

```
                    ┌─────────────┐
                    │   dim_date  │
                    └──────┬──────┘
                           │
    ┌─────────────┐       │       ┌─────────────┐
    │  dim_user   │       │       │ dim_product │
    └──────┬──────┘       │       └──────┬──────┘
           │              │              │
           └──────────────┼──────────────┘
                          │
                    ┌─────┴─────┐
                    │fact_orders│
                    └───────────┘
```

## 3. 事实表设计

### fact_order_items（订单项事实表）

| 字段名 | 数据类型 | 说明 | 来源 |
|--------|----------|------|------|
| order_item_sk | BIGINT | 代理键（主键） | 生成 |
| date_key | INT | 日期外键 | dim_date |
| user_sk | BIGINT | 用户外键 | dim_user |
| product_sk | BIGINT | 商品外键 | dim_product |
| order_id | VARCHAR | 订单号（退化维度） | ods_orders |
| quantity | INT | 数量 | ods_order_items |
| unit_price | DECIMAL | 单价 | ods_order_items |
| discount_amount | DECIMAL | 优惠金额 | 计算 |
| total_amount | DECIMAL | 总金额 | 计算 |

**粒度说明**：每一行代表一个订单中的一个商品项

**度量类型**：
- 可累加：quantity, total_amount
- 半累加：unit_price（需配合数量计算）

## 4. 维度表设计

### dim_user（用户维度表 - SCD Type 2）

| 字段名 | 数据类型 | 说明 | SCD类型 |
|--------|----------|------|---------|
| user_sk | BIGINT | 代理键 | - |
| user_id | BIGINT | 用户ID（自然键） | 0 |
| username | VARCHAR | 用户名 | 2 |
| email | VARCHAR | 邮箱 | 2 |
| user_level | VARCHAR | 用户等级 | 2 |
| register_date | DATE | 注册日期 | 0 |
| city | VARCHAR | 城市 | 2 |
| valid_from | DATE | 生效日期 | - |
| valid_to | DATE | 失效日期 | - |
| is_current | BOOLEAN | 是否当前版本 | - |

**SCD策略说明**：
- Type 0：register_date（永不改变）
- Type 2：username, email, user_level, city（保留历史）

## 5. ETL映射关系

### 数据流

| 目标表 | 源表 | 转换逻辑 |
|--------|------|----------|
| fact_order_items | ods_orders + ods_order_items | JOIN关联，金额计算 |
| dim_user | ods_users | SCD Type 2处理 |
| dim_product | ods_products | SCD Type 2处理 |

### 加载策略

| 表 | 加载频率 | 加载方式 | 历史数据处理 |
|----|----------|----------|--------------|
| fact_order_items | 每小时 | 增量 | 追加 |
| dim_user | 每日 | 全量+增量 | SCD Type 2 |
| dim_product | 每日 | 全量 | SCD Type 2 |

## 6. 物理设计建议

### 分区策略
- fact_order_items：按date_key按月分区

### 索引策略
- 事实表：date_key, user_sk, product_sk
- 维度表：user_id（自然键）, is_current

## 7. 使用示例

### 查询示例1：按日期统计销售额
```sql
SELECT
    d.date,
    SUM(f.total_amount) AS sales_amount
FROM fact_order_items f
JOIN dim_date d ON f.date_key = d.date_key
WHERE d.year = 2024
GROUP BY d.date;
```

### 查询示例2：用户购买行为分析
```sql
SELECT
    u.user_level,
    COUNT(DISTINCT f.user_sk) AS user_cnt,
    SUM(f.total_amount) AS total_sales
FROM fact_order_items f
JOIN dim_user u ON f.user_sk = u.user_sk
WHERE u.is_current = TRUE
GROUP BY u.user_level;
```
```

## 设计输入要素

用户提供以下信息以获得最佳设计：

| 要素 | 说明 | 示例 |
|------|------|------|
| 业务场景 | 描述业务流程 | "电商订单销售" |
| 分析需求 | 需要分析什么 | "销售趋势、用户行为、商品分析" |
| 数据源 | 有哪些源表 | "订单表、用户表、商品表" |
| 数据量 | 大致的数据规模 | "日增100万订单" |
| 历史需求 | 是否需要历史追踪 | "需要追踪用户等级变化" |

## 模型设计模式库

### 模式1：标准星型模型

适用：大多数分析场景
特点：维度表直接关联事实表，无层级规范化

### 模式2：雪花模型

适用：维度属性极多，需要严格规范化
特点：维度表进一步拆分为子维度表

### 模式3：一致性维度

适用：多个事实表共享维度
特点：确保跨业务流程分析的一致性

### 模式4：累积快照事实表

适用：跟踪业务流程的多个阶段
示例：订单从创建到完成的全过程

```
fact_order_lifecycle:
- order_id (退化维度)
- date_ordered_key
- date_paid_key
- date_shipped_key
- date_delivered_key
- days_to_payment
- days_to_shipment
- days_to_delivery
```

### 模式5：无事实事实表

适用：记录事件的发生，无数值度量
示例：用户访问日志、点击流

```
fact_page_views:
- date_key
- user_sk
- page_sk
- session_id (退化维度)
- view_count (恒为1)
```

## SCD策略选择指南

| 策略 | 适用场景 | 实现复杂度 | 存储增长 |
|------|----------|------------|----------|
| Type 0 | 永不改变的属性 | 低 | 无 |
| Type 1 | 不需要历史，只看当前 | 低 | 无 |
| Type 2 | 需要完整历史 | 中 | 中等 |
| Type 3 | 只需要有限历史（新旧） | 低 | 低 |
| Type 4 | 历史表单独查询 | 中 | 高 |
| Type 6 | 复杂场景组合 | 高 | 高 |

**推荐**：默认使用Type 2，除非明确不需要历史或存储受限。

## 粒度确定原则

1. **最细原则**：事实表粒度应该是最细的业务级别
2. **不可再分**：选择的粒度不能进一步拆分有意义的业务事件
3. **一致性**：同一事实表的所有度量必须在相同粒度下
4. **预期分析**：考虑未来可能的分析需求，粒度要足够细

**常见粒度示例**：
- 订单：订单商品项级别
- 库存：商品-仓库-日期级别
- 页面浏览：单次页面访问级别
- 点击：单次点击事件级别

## 当前设计需求

$ARGUMENTS

---

**设计时**：
1. 首先确认业务场景和分析需求理解正确
2. 确定最合适的事实表粒度
3. 识别所有相关维度及SCD策略
4. 确定度量及其累加性
5. 输出完整的模型设计文档
6. 提供ETL映射和物理设计建议
