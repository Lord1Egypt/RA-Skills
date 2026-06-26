---
name: dbt-model
description: |
  dbt模型生成器 - 生成符合dbt最佳实践的SQL模型、schema配置、测试用例。
  当用户需要开发dbt模型、编写dbt SQL、配置dbt测试时触发。
  触发词：生成dbt模型、dbt SQL、dbt测试、staging模型、mart模型。
argument: { description: "模型类型和模型需求描述", required: true }
agent: general-purpose
allowed-tools: [Read, Grep, Glob, Edit, Write, Bash]
---

# dbt模型生成器

生成符合dbt最佳实践的SQL模型，包括Staging、Intermediate、Mart各层模型。

## 工作流程

1. **模型分析** - 确定模型类型（staging/intermediate/mart）
2. **依赖识别** - 识别上游依赖（sources/refs）
3. **SQL生成** - 编写dbt SQL模型
4. **Schema配置** - 生成YAML配置（文档、测试）
5. **测试建议** - 推荐合适的测试用例

## dbt模型分层

```
┌─────────────────────────────────────────────────────────────┐
│                      dbt 模型分层架构                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Sources (raw data)                                         │
│     ├── raw.orders                                          │
│     └── raw.users                                           │
│           │                                                 │
│           ▼                                                 │
│  Staging (clean & standardized)                             │
│     ├── stg_orders.sql                                      │
│     └── stg_users.sql                                       │
│           │                                                 │
│           ▼                                                 │
│  Intermediate (business logic)                              │
│     ├── int_order_items.sql                                 │
│     └── int_user_sessions.sql                               │
│           │                                                 │
│           ▼                                                 │
│  Marts (aggregated & ready for analysis)                    │
│     ├── dimensions/                                         │
│     │   ├── dim_users.sql                                   │
│     │   └── dim_products.sql                                │
│     └── facts/                                              │
│         ├── fct_orders.sql                                  │
│         └── fct_page_views.sql                              │
│           │                                                 │
│           ▼                                                 │
│  Reports (final outputs)                                    │
│     └── rpt_daily_sales.sql                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 输出规范

### 1. Staging 模型

**文件名**：`stg_{source_table}.sql`

**模板**：
```sql
/*
 * Staging: {{ model.name }}
 * Source: {{ source_table }}
 * Description: {{ description }}
 */

WITH source AS (
    SELECT * FROM {{ source('{{ source_schema }}', '{{ source_table }}') }}
),

renamed AS (
    SELECT
        -- 主键
        {{ primary_key }},

        -- 外键
        {{ foreign_keys }},

        -- 属性
        {{ attributes }},

        -- 数值
        {{ measures }},

        -- 时间戳
        {{ timestamps }},

        -- 元数据
        {{ metadata }}

    FROM source
    {{ where_clause }}
)

SELECT * FROM renamed
```

**示例**：
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
        payment_method,

        -- 数值
        order_amount,
        discount_amount,
        shipping_amount,

        -- 时间戳
        created_at,
        updated_at,
        paid_at

    FROM source
    WHERE deleted_at IS NULL
)

SELECT * FROM renamed
```

**对应Schema**：
```yaml
-- _stg_orders.yml
version: 2

models:
  - name: stg_orders
    description: "清洗后的订单数据"
    columns:
      - name: order_id
        description: "订单唯一标识"
        tests:
          - unique
          - not_null

      - name: user_id
        description: "用户ID"
        tests:
          - not_null
          - relationships:
              to: ref('stg_users')
              field: user_id

      - name: order_status
        description: "订单状态"
        tests:
          - not_null
          - accepted_values:
              values: ['pending', 'paid', 'shipped', 'delivered', 'cancelled']
```

### 2. Mart - Dimension 模型

**文件名**：`dim_{entity}.sql`

**模板**：
```sql
/*
 * Dimension: {{ model.name }}
 * Grain: One row per {{ entity }}
 * SCD Type: {{ scd_type }}
 */

WITH source AS (
    SELECT * FROM {{ ref('stg_{{ entity }}') }}
),

{% if scd_type == 2 %}
-- SCD Type 2: 保留历史版本
changes AS (
    SELECT
        *,
        LAG({{ scd_columns }}) OVER (PARTITION BY {{ natural_key }} ORDER BY updated_at) AS prev_values,
        CASE
            WHEN {{ scd_columns }} != LAG({{ scd_columns }}) OVER (PARTITION BY {{ natural_key }} ORDER BY updated_at)
            THEN TRUE
            ELSE FALSE
        END AS has_changed
    FROM source
),

scd AS (
    SELECT
        {{ surrogate_key }},
        {{ natural_key }},
        {{ attributes }},
        valid_from,
        valid_to,
        is_current
    FROM changes
    {{ scd_logic }}
)
{% else %}
-- SCD Type 1: 只保留当前版本
current_version AS (
    SELECT
        {{ surrogate_key }},
        {{ natural_key }},
        {{ attributes }}
    FROM source
)
{% endif %}

SELECT * FROM {% if scd_type == 2 %}scd{% else %}current_version{% endif %}
```

**示例**：
```sql
-- dim_users.sql (SCD Type 2)
WITH source AS (
    SELECT * FROM {{ ref('stg_users') }}
),

changes AS (
    SELECT
        user_id,
        username,
        email,
        user_level,
        city,
        updated_at,
        LAG(user_level) OVER (PARTITION BY user_id ORDER BY updated_at) AS prev_level,
        LAG(city) OVER (PARTITION BY user_id ORDER BY updated_at) AS prev_city,
        CASE
            WHEN user_level != LAG(user_level) OVER (PARTITION BY user_id ORDER BY updated_at)
              OR city != LAG(city) OVER (PARTITION BY user_id ORDER BY updated_at)
            THEN TRUE
            ELSE FALSE
        END AS has_changed
    FROM source
),

scd AS (
    SELECT
        {{ dbt_utils.generate_surrogate_key(['user_id', 'updated_at']) }} AS user_sk,
        user_id,
        username,
        email,
        user_level,
        city,
        updated_at AS valid_from,
        COALESCE(
            LEAD(updated_at) OVER (PARTITION BY user_id ORDER BY updated_at),
            '9999-12-31'::timestamp
        ) AS valid_to,
        CASE
            WHEN LEAD(updated_at) OVER (PARTITION BY user_id ORDER BY updated_at) IS NULL
            THEN TRUE
            ELSE FALSE
        END AS is_current
    FROM changes
)

SELECT * FROM scd
```

### 3. Mart - Fact 模型

**文件名**：`fct_{event}.sql`

**模板**：
```sql
/*
 * Fact: {{ model.name }}
 * Grain: {{ grain_description }}
 */

WITH {{ ctes }} AS (
    SELECT * FROM {{ ref('stg_{{ source }}') }}
),

{{ intermediate_ctes }}

final AS (
    SELECT
        -- 代理键
        {{ surrogate_key }},

        -- 维度外键
        {{ dimension_fks }},

        -- 退化维度
        {{ degenerate_dims }},

        -- 度量
        {{ measures }},

        -- 审计字段
        CURRENT_TIMESTAMP AS loaded_at

    FROM {{ base_table }}
    {{ joins }}
)

SELECT * FROM final
```

**示例**：
```sql
-- fct_orders.sql
WITH stg_orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

stg_order_items AS (
    SELECT * FROM {{ ref('stg_order_items') }}
),

order_items AS (
    SELECT
        oi.order_item_id,
        o.order_id,
        o.user_id,
        oi.product_id,
        o.order_status,
        DATE(o.created_at) AS order_date,
        oi.quantity,
        oi.unit_price,
        oi.discount_amount,
        (oi.quantity * oi.unit_price - oi.discount_amount) AS item_total
    FROM stg_orders o
    JOIN stg_order_items oi ON o.order_id = oi.order_id
),

final AS (
    SELECT
        -- 代理键
        {{ dbt_utils.generate_surrogate_key(['order_item_id']) }} AS order_item_sk,

        -- 维度外键
        {{ dbt_utils.generate_surrogate_key(['user_id', 'order_date']) }} AS user_sk,
        {{ dbt_utils.generate_surrogate_key(['product_id', 'order_date']) }} AS product_sk,
        {{ dbt_utils.generate_surrogate_key(['order_date']) }} AS date_sk,

        -- 退化维度
        order_id,
        order_item_id,
        order_status,

        -- 度量
        quantity,
        unit_price,
        discount_amount,
        item_total,

        -- 审计
        CURRENT_TIMESTAMP AS loaded_at

    FROM order_items
)

SELECT * FROM final
```

## 输入格式

### 格式1：从源表生成Staging模型
```
/dbt-model 生成staging模型
源表: raw.orders
字段:
- order_id (VARCHAR): 订单ID，主键
- user_id (BIGINT): 用户ID，外键
- order_status (VARCHAR): 订单状态
- order_amount (DECIMAL): 订单金额
- created_at (TIMESTAMP): 创建时间
```

### 格式2：生成Dimension模型
```
/dbt-model 生成dimension模型
实体: user
源模型: stg_users
SCD类型: Type 2
变化属性: user_level, city
```

### 格式3：生成Fact模型
```
/dbt-model 生成fact模型
事实: orders
粒度: 订单商品项级别
依赖模型: stg_orders, stg_order_items
维度: dim_users, dim_products, dim_date
```

## 输出内容

1. **SQL模型文件** - 符合dbt规范的SQL代码
2. **YAML配置文件** - 包含文档和测试配置
3. **依赖说明** - 上游sources/refs列表
4. **测试建议** - 推荐的测试用例

## dbt最佳实践检查清单

### SQL规范
- [ ] 使用CTE而非子查询
- [ ] CTE有描述性命名
- [ ] 字段有明确注释
- [ ] 使用dbt宏（如dbt_utils.generate_surrogate_key）
- [ ] 避免SELECT *

### 模型配置
- [ ] 配置materialized策略
- [ ] 配置分区（大表）
- [ ] 配置标签和所有者

### 测试覆盖
- [ ] 主键：unique + not_null
- [ ] 外键：relationships
- [ ] 枚举值：accepted_values
- [ ] 数值范围：自定义测试

## 当前生成任务

$ARGUMENTS

---

**生成模型时**：
1. 首先确认模型类型和需求
2. 识别所有上游依赖
3. 编写符合规范的dbt SQL
4. 生成对应的YAML配置
5. 提供测试建议和部署指南
