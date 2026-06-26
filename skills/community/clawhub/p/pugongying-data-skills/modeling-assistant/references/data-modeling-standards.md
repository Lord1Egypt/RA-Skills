# 数据建模标准与规范

## 目录

1. [维度建模核心概念](#维度建模核心概念)
2. [模型设计模式](#模型设计模式)
3. [命名规范](#命名规范)
4. [表结构设计规范](#表结构设计规范)
5. [dbt最佳实践](#dbt最佳实践)
6. [数据血缘规范](#数据血缘规范)

---

## 维度建模核心概念

### 事实表 (Fact Table)

**定义**：存储业务过程的度量数据，是数据分析的核心。

**特征**：
- 包含外键关联到维度表
- 包含数值型度量（可累加、半累加、不可累加）
- 通常有非常大的数据量
- 记录数随时间增长

**类型**：
| 类型 | 说明 | 示例 |
|------|------|------|
| 事务事实表 | 记录单个业务事件 | 订单表、支付表 |
| 周期快照 | 记录某一时间点的状态 | 每日库存余额 |
| 累积快照 | 记录业务过程的多个阶段 | 订单全流程 |
| 无事实事实表 | 记录事件的发生 | 点击流、访问日志 |

**设计要点**：
```
事实表 = 维度外键 + 退化维度 + 度量 + 时间戳

示例：订单事实表
┌─────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│ date_key    │ user_key    │ product_key │ order_id    │ quantity    │
│ (FK)        │ (FK)        │ (FK)        │ (退化)      │ (度量)      │
├─────────────┼─────────────┼─────────────┼─────────────┼─────────────┤
│ 20240101    │ 10001       │ 5001        │ ORD2024001  │ 2           │
│ 20240101    │ 10002       │ 5002        │ ORD2024002  │ 1           │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────────┘
```

### 维度表 (Dimension Table)

**定义**：存储业务实体的描述性属性，为事实表提供上下文。

**特征**：
- 包含主键（通常是代理键）
- 包含丰富的描述属性
- 数据量相对较小
- 相对稳定，变化缓慢

**类型**：
| 类型 | 说明 | 处理策略 |
|------|------|----------|
| 类型0 | 原始值，永不改变 | 直接插入 |
| 类型1 | 覆盖旧值 | UPDATE直接更新 |
| 类型2 | 保留历史，新增版本 | 增加生效/失效日期 |
| 类型3 | 保留有限历史 | 增加旧值字段 |
| 类型4 | 历史表 | 当前表+历史表 |
| 类型6 | 混合类型 | 组合1+2+3 |

**设计要点**：
```
维度表 = 代理键 + 自然键 + 描述属性 + 层级属性 + SCD字段

示例：用户维度表（SCD Type 2）
┌─────────┬─────────┬──────────┬─────────┬─────────────┬─────────────┐
│ user_sk │ user_id │ username │ status  │ valid_from  │ valid_to    │
│ (PK)    │ (NK)    │          │         │             │             │
├─────────┼─────────┼──────────┼─────────┼─────────────┼─────────────┤
│ 1       │ 10001   │ 张三     │ active  │ 2024-01-01  │ 9999-12-31  │
│ 2       │ 10001   │ 张三_改  │ active  │ 2024-03-01  │ 9999-12-31  │ ← 历史版本
└─────────┴─────────┴──────────┴─────────┴─────────────┴─────────────┘
```

### 星型模型 vs 雪花模型

| 特性 | 星型模型 | 雪花模型 |
|------|----------|----------|
| 结构 | 维度表直接连接事实表 | 维度表进一步规范化 |
| 查询复杂度 | 简单，JOIN少 | 复杂，JOIN多 |
| 存储空间 | 略多（有冗余） | 较少（规范化） |
| 查询性能 | 快 | 较慢 |
| 维护难度 | 简单 | 复杂 |
| 推荐场景 | 大多数分析场景 | 维度属性极多的场景 |

**推荐**：默认使用星型模型，除非维度属性非常多且需要严格规范化。

---

## 模型设计模式

### 1. 星型模型设计

```
                    ┌─────────────┐
                    │   dim_date  │
                    │   (日期维度) │
                    └──────┬──────┘
                           │
    ┌─────────────┐       │       ┌─────────────┐
    │  dim_user   │       │       │ dim_product │
    │  (用户维度)  │       │       │  (商品维度)  │
    └──────┬──────┘       │       └──────┬──────┘
           │              │              │
           └──────────────┼──────────────┘
                          │
                    ┌─────┴─────┐
                    │fact_orders│
                    │ (订单事实) │
                    └───────────┘
```

### 2. 一致性维度

多个事实表共享相同的维度表，确保跨业务流程分析的一致性。

```
    dim_date ◄────────┬────────► fact_sales
                      │
    dim_product ◄─────┼────────► fact_inventory
                      │
    dim_store ◄───────┴────────► fact_returns
```

### 3. 桥接表（多对多关系）

处理事实表与维度表的多对多关系。

```
    dim_order ◄─────┐
                    │
               ┌────┴────┐
               │bridge_  │     权重：表示分摊比例
               │order_   │     或：表示角色（主/次）
               │product  │
               └────┬────┘
                    │
    dim_product ◄───┘
```

### 4. 微型维度

将大型维度表中变化频繁的属性分离出来。

```
    ┌─────────────────────────────────────┐
    │           dim_user                  │
    │  (稳定属性：用户ID、注册时间等)      │
    └───────────────┬─────────────────────┘
                    │ FK: user_attr_key
                    ▼
    ┌─────────────────────────────────────┐
    │      dim_user_attributes            │
    │  (变化属性：等级、积分、标签等)      │
    │  Type 2 SCD                         │
    └─────────────────────────────────────┘
```

### 5. 事实表分区策略

| 分区方式 | 适用场景 | 优点 |
|----------|----------|------|
| 时间分区 | 按天/月分区 | 高效删除旧数据，并行查询 |
| 范围分区 | 按日期范围 | 适合时间序列分析 |
| 列表分区 | 按地区/类别 | 适合区域分析 |
| 哈希分区 | 均匀分布 | 适合数据倾斜严重的场景 |

---

## 命名规范

### 表命名

| 类型 | 前缀 | 示例 |
|------|------|------|
| 事实表 | `fact_` | `fact_orders`, `fact_page_views` |
| 维度表 | `dim_` | `dim_user`, `dim_product` |
| 桥接表 | `bridge_` | `bridge_order_product` |
| 汇总表 | `agg_` | `agg_daily_sales` |
| 临时表 | `tmp_` | `tmp_order_processing` |
| 视图 | `vw_` | `vw_order_detail` |
| dbt模型 | 无/语义化 | `stg_orders`, `fct_orders` |

### 字段命名

| 类型 | 后缀/前缀 | 示例 |
|------|----------|------|
| 代理键 | `_sk` | `user_sk`, `order_sk` |
| 自然键 | `_nk` | `user_nk` 或直接 `user_id` |
| 外键 | `_fk` 或原字段名 | `user_fk` 或 `user_id` |
| 度量 | 无 | `quantity`, `amount` |
| 计数 | `_cnt` | `order_cnt` |
| 标记 | `_flg` / `_is_` | `is_active`, `deleted_flg` |
| 时间戳 | `_at` | `created_at`, `updated_at` |
| 日期 | `_date` | `order_date`, `birth_date` |

### dbt模型命名

| 层 | 前缀 | 示例 |
|----|------|------|
| Source | 无 | `raw.orders` |
| Staging | `stg_` | `stg_orders`, `stg_users` |
| Intermediate | `int_` | `int_order_items` |
| Mart - Dimension | `dim_` | `dim_users`, `dim_products` |
| Mart - Fact | `fct_` | `fct_orders`, `fct_events` |
| Mart - Aggregate | `agg_` | `agg_daily_sales` |
| Report | `rpt_` | `rpt_sales_dashboard` |

---

## 表结构设计规范

### 事实表结构模板

```sql
CREATE TABLE fact_orders (
    -- 代理键（可选，取决于是否使用）
    order_sk BIGINT PRIMARY KEY AUTO_INCREMENT,

    -- 维度外键
    date_key INT NOT NULL COMMENT '日期维度外键',
    user_sk BIGINT NOT NULL COMMENT '用户维度代理键',
    product_sk BIGINT NOT NULL COMMENT '商品维度代理键',

    -- 退化维度
    order_id VARCHAR(32) NOT NULL COMMENT '订单编号（退化维度）',

    -- 度量
    quantity INT NOT NULL COMMENT '数量',
    unit_price DECIMAL(10,2) NOT NULL COMMENT '单价',
    discount_amount DECIMAL(10,2) DEFAULT 0 COMMENT '优惠金额',
    total_amount DECIMAL(10,2) NOT NULL COMMENT '订单金额',

    -- 审计字段
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    etl_batch_id VARCHAR(32) COMMENT 'ETL批次号',

    -- 约束
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (user_sk) REFERENCES dim_user(user_sk),
    FOREIGN KEY (product_sk) REFERENCES dim_product(product_sk)
)
PARTITION BY RANGE (YEAR(order_date)) (
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);

-- 索引
CREATE INDEX idx_fact_orders_date ON fact_orders(date_key);
CREATE INDEX idx_fact_orders_user ON fact_orders(user_sk);
CREATE INDEX idx_fact_orders_product ON fact_orders(product_sk);
```

### 维度表结构模板

```sql
-- SCD Type 2 维度表
CREATE TABLE dim_user (
    -- 代理键
    user_sk BIGINT PRIMARY KEY AUTO_INCREMENT,

    -- 自然键
    user_id BIGINT NOT NULL COMMENT '用户自然键',

    -- 描述属性
    username VARCHAR(50) NOT NULL COMMENT '用户名',
    email VARCHAR(100) COMMENT '邮箱',
    phone VARCHAR(20) COMMENT '手机号',
    gender VARCHAR(10) COMMENT '性别',
    birth_date DATE COMMENT '生日',
    register_date DATE NOT NULL COMMENT '注册日期',

    -- 层级属性
    city_code VARCHAR(10) COMMENT '城市代码',
    city_name VARCHAR(50) COMMENT '城市名称',
    province_code VARCHAR(10) COMMENT '省份代码',
    province_name VARCHAR(50) COMMENT '省份名称',

    -- SCD Type 2 字段
    valid_from DATE NOT NULL COMMENT '生效日期',
    valid_to DATE NOT NULL COMMENT '失效日期',
    is_current BOOLEAN DEFAULT TRUE COMMENT '是否当前版本',

    -- 审计字段
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- 唯一约束：自然键 + 版本
    UNIQUE KEY uk_user_version (user_id, valid_from)
);

-- 索引
CREATE INDEX idx_dim_user_natural ON dim_user(user_id);
CREATE INDEX idx_dim_user_current ON dim_user(user_id, is_current);
```

---

## dbt最佳实践

### 项目结构

```
dbt_project/
├── dbt_project.yml
├── packages.yml
├── models/
│   ├── staging/
│   │   ├── _sources.yml
│   │   ├── stg_orders.sql
│   │   └── stg_users.sql
│   ├── intermediate/
│   │   ├── int_order_items.sql
│   │   └── int_user_events.sql
│   ├── marts/
│   │   ├── dimensions/
│   │   │   ├── dim_users.sql
│   │   │   └── dim_products.sql
│   │   └── facts/
│   │       ├── fct_orders.sql
│   │       └── fct_events.sql
│   └── reports/
│       └── rpt_daily_sales.sql
├── seeds/
├── snapshots/
├── tests/
│   ├── generic/
│   └── specific/
└── macros/
```

### 模型开发规范

**1. Staging 模型**
```sql
-- stg_orders.sql
WITH source AS (
    SELECT * FROM {{ source('raw', 'orders') }}
),

renamed AS (
    SELECT
        -- 主键
        order_id,

        -- 外键
        user_id,

        -- 属性
        order_status,

        -- 数值
        order_amount,

        -- 时间戳
        created_at,
        updated_at

    FROM source
)

SELECT * FROM renamed
```

**2. Mart 模型**
```sql
-- fct_orders.sql
WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

order_items AS (
    SELECT * FROM {{ ref('int_order_items') }}
),

final AS (
    SELECT
        -- 维度外键
        {{ dbt_utils.generate_surrogate_key(['o.order_id']) }} AS order_sk,
        u.user_sk,
        p.product_sk,
        d.date_key,

        -- 退化维度
        o.order_id,
        o.order_status,

        -- 度量
        oi.quantity,
        oi.unit_price,
        o.total_amount,

        -- 审计
        CURRENT_TIMESTAMP AS loaded_at

    FROM orders o
    LEFT JOIN {{ ref('dim_users') }} u ON o.user_id = u.user_id AND u.is_current = TRUE
    LEFT JOIN {{ ref('dim_products') }} p ON oi.product_id = p.product_id AND p.is_current = TRUE
    LEFT JOIN {{ ref('dim_date') }} d ON DATE(o.created_at) = d.date
    LEFT JOIN order_items oi ON o.order_id = oi.order_id
)

SELECT * FROM final
```

### dbt测试规范

```yaml
# _schema.yml
version: 2

models:
  - name: fct_orders
    description: "订单事实表"
    columns:
      - name: order_sk
        description: "订单代理键"
        tests:
          - unique
          - not_null

      - name: user_sk
        description: "用户外键"
        tests:
          - not_null
          - relationships:
              to: ref('dim_users')
              field: user_sk

      - name: total_amount
        description: "订单金额"
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
```

---

## 数据血缘规范

### 血缘关系类型

| 类型 | 说明 | 示例 |
|------|------|------|
| 表级血缘 | 表与表之间的依赖 | `stg_orders` → `fct_orders` |
| 字段级血缘 | 字段与字段的映射 | `stg_orders.user_id` → `fct_orders.user_sk` |
| 任务级血缘 | ETL任务间的依赖 | `load_staging` → `load_marts` |

### 血缘标注规范

在SQL中使用注释标注血缘关系：

```sql
/*
 * 上游依赖:
 *   - raw.orders (source)
 *   - raw.order_items (source)
 *
 * 下游消费:
 *   - fct_orders (mart)
 *   - agg_daily_sales (aggregate)
 *
 * 业务 owner: sales-team@company.com
 * 技术 owner: data-team@company.com
 */

WITH orders AS (
    -- source: raw.orders
    SELECT * FROM {{ source('raw', 'orders') }}
),

items AS (
    -- source: raw.order_items
    SELECT * FROM {{ source('raw', 'order_items') }}
)

SELECT
    -- pk: order_id from orders.order_id
    order_id,

    -- fk: user_id from orders.user_id
    user_id,

    -- measure: sum of items.amount
    SUM(i.amount) AS total_amount

FROM orders o
JOIN items i ON o.order_id = i.order_id
GROUP BY 1, 2
```

### 血缘文档格式

```yaml
# lineage.yml
table: fct_orders
lineage:
  upstream:
    tables:
      - name: raw.orders
        type: source
        mapping:
          order_id: order_id
          user_id: user_id
          amount: total_amount

      - name: raw.order_items
        type: source
        mapping:
          order_id: order_id
          product_id: product_id
          quantity: quantity

      - name: dim_users
        type: dimension
        join_key: user_id

  downstream:
    tables:
      - name: agg_daily_sales
        type: aggregate

      - name: rpt_sales_dashboard
        type: report
```

---

## 参考资料

- 《数据仓库工具箱》Ralph Kimball
- dbt Labs 官方文档: https://docs.getdbt.com/
- Data Vault 2.0 标准
- medallion architecture (青铜-白银-黄金架构)
