---
name: text-to-sql-query
description: |
  直接通过 Text-to-SQL 方式查询零售数据库。根据用户自然语言描述，生成 SQL 查询语句并执行。
  本 Skill 不依赖语义层或指标平台，而是直接基于数据库 schema 生成 SQL。
  触发场景：用户需要查询零售数据、生成 SQL 查询、分析销售/客户/商品数据时使用。
---

# Text-to-SQL 数据查询 Skill

根据用户自然语言描述，直接生成 SQL 查询语句，通过 Gateway JDBC SQL 直查接口在零售数据库上执行并返回结果。

## 执行模式

- **强模型**（Claude Opus/Sonnet, GPT-4o/5）：遵循"原则"段落，自行决定实现细节
- **标准模型**（Qwen, DeepSeek, Llama）：严格按"模板"段落执行，使用提供的代码块，不要自行改写

> 如果你不确定自己属于哪个类别，请按"标准模型"模式执行。

---

## 0. 查询接口信息

通过 Gateway JDBC SQL 直查接口执行 SQL 查询。API Key 通过环境变量 `$CAN_API_KEY` 注入，禁止在 Skill 文件中硬编码。

### 0.1 接口地址

```
POST https://gateway.can.aloudata.com/api/jdbc/query
Content-Type: application/json
X-API-Key: $CAN_API_KEY
```

请求体：
```json
{"sql": "SELECT ... FROM table_name WHERE ... LIMIT N"}
```

### 0.2 执行方式

**方式一：curl（推荐，适合 Bash 环境）**
```bash
curl --noproxy '*' -s \
  -H "X-API-Key: $CAN_API_KEY" \
  -H "Content-Type: application/json" \
  -X POST "https://gateway.can.aloudata.com/api/jdbc/query" \
  -d '{"sql": "YOUR SQL HERE"}'
```

**方式二：Python requests**
```python
import os, requests

response = requests.post(
    "https://gateway.can.aloudata.com/api/jdbc/query",
    headers={
        "X-API-Key": os.environ["CAN_API_KEY"],
        "Content-Type": "application/json"
    },
    json={"sql": "YOUR SQL HERE"}
)
print(response.text)  # 返回 Markdown 表格（纯文本）
```

**多行 SQL 示例（curl heredoc）**：
```bash
curl --noproxy '*' -s \
  -H "X-API-Key: $CAN_API_KEY" \
  -H "Content-Type: application/json" \
  -X POST "https://gateway.can.aloudata.com/api/jdbc/query" \
  -d @- <<'EOF'
{"sql": "SELECT o.dt, o.order_number, p.style_name, s.shop_name, o.retail_amount FROM fact_orders o JOIN dim_product p ON o.sku = p.sku JOIN dim_shop s ON o.shop_code = s.tr_shop_code WHERE o.dt >= '2024-01-01' ORDER BY o.dt DESC LIMIT 20"}
EOF
```

### 0.3 返回格式

**成功时**返回 **Markdown 表格**（纯文本，非 JSON）：
```
| sku | style_name | color_name | tag_price |
| --- | --- | --- | --- |
| SKU1000211 | 泡泡袖衬衫春秋款 | 白色 | 118.8600 |
| SKU1000222 | 背带裤明星同款 | 灰色 | 439.1300 |
2 row(s) returned.
```

**错误时**返回纯文本错误信息：
- `SQL validation error: Table not allowed: xxx` — 查询了白名单以外的表
- `SQL validation error: Only SELECT statements are allowed` — 非 SELECT 语句
- `Query error: Query timed out after 30 seconds` — 查询超时

### 0.4 安全限制

- **只允许 SELECT**：INSERT/UPDATE/DELETE/DROP 等写操作会被拒绝
- **表白名单**：只允许查询 §1.1 中的 6 张表（dim_product, dim_vip, dim_shop, fact_orders, fact_inventory, fact_product_launch），查询其他表会返回 `Table not allowed` 错误
- **禁止多语句**：不能用分号拼接多条 SQL
- **自动加 LIMIT**：未指定 LIMIT 时服务端自动追加 LIMIT 1000
- **查询超时**：默认 30 秒超时
- **UNION 默认禁止**

---

## 1. 数据库 Schema

### 1.1 表结构总览

本数据库采用**星型模型**，包含 3 张事实表 + 3 张维度表。

| 表名 | 类型 | 说明 |
|------|------|------|
| fact_orders | 事实表 | 订单明细，每行一笔订单行项目 |
| fact_inventory | 事实表 | 库存快照，每行一个 SKU 在某门店/仓库的库存状态 |
| fact_product_launch | 事实表 | 商品上市记录，每行一个 SKU 在某门店的上市信息 |
| dim_product | 维度表 | 商品维度，SKU 级商品属性 |
| dim_shop | 维度表 | 店铺维度，门店属性及地理信息 |
| dim_vip | 维度表 | 会员维度，会员属性信息 |

### 1.2 事实表字段

#### fact_orders（订单事实表）
| 字段名 | 类型 | 说明 |
|--------|------|------|
| pay_time | varchar | 支付时间 |
| delivery_date | varchar | 发货日期 |
| dt | date | 数据日期（分区键，用于时间筛选） |
| sku | varchar | SKU 编码（关联 dim_product） |
| shop_code | varchar | 接单门店编码（关联 dim_shop.tr_shop_code） |
| delivery_shop_code | varchar | 发货门店编码 |
| vip_id | bigint | 会员 ID（关联 dim_vip） |
| vip_code | varchar | 会员编码 |
| seller_id | varchar | 导购 ID |
| seller_code | varchar | 导购编码 |
| seller_name | varchar | 导购姓名 |
| warehouse_code | varchar | 仓库编码 |
| order_number | varchar | 订单号 |
| source_system_code | varchar | 来源系统编码 |
| order_platform_code | varchar | 订单平台编码 |
| retail_amount | decimal(38,9) | 零售金额（吊牌价口径） |
| retail_quantity | bigint | 零售数量 |
| retail_market_value | decimal(38,9) | 零售市值（吊牌额） |
| return_amount | decimal(38,9) | 退货金额 |
| return_quantity | bigint | 退货数量 |
| return_market_value | decimal(38,9) | 退货市值 |
| net_market_value | decimal(38,9) | 净市值 |
| net_quantity | bigint | 净数量（零售数量 - 退货数量） |
| net_amount | decimal(38,9) | 净金额（零售金额 - 退货金额） |
| unshipped_refund_quantity | bigint | 未发货退款数量 |
| unshipped_refund_amount | decimal(38,9) | 未发货退款金额 |
| shipped_refund_amount | decimal(38,9) | 已发货退款金额 |
| return_refund_quantity | bigint | 退货退款数量 |
| return_refund_amount | decimal(38,9) | 退货退款金额 |

#### fact_inventory（库存事实表）
| 字段名 | 类型 | 说明 |
|--------|------|------|
| unit_code | varchar | 单位编码 |
| unit_name | varchar | 单位名称 |
| warehouse_code | varchar | 仓库编码 |
| warehouse_name | varchar | 仓库名称 |
| shop_code | varchar | 门店编码（关联 dim_shop.tr_shop_code） |
| sku | varchar | SKU 编码（关联 dim_product） |
| skc | varchar | SKC 编码（款色） |
| color_code | varchar | 颜色编码 |
| color_name | varchar | 颜色名称 |
| spec_code | varchar | 规格编码 |
| spec_name | varchar | 规格名称 |
| style_code | varchar | 款式编码 |
| style_name | varchar | 款式名称 |
| stock_quantity | int | 库存数量 |
| stock_cost | decimal(20,4) | 库存成本 |
| stock_market_value | decimal(20,4) | 库存市值（吊牌价口径） |
| stock_quantity_onroad | int | 在途库存数量 |
| stock_cost_onroad | decimal(20,4) | 在途库存成本 |
| stock_market_value_onroad | decimal(38,4) | 在途库存市值 |
| stock_quantity_onord | int | 在单库存数量 |
| stock_cost_onord | decimal(20,4) | 在单库存成本 |
| stock_market_value_onord | decimal(29,4) | 在单库存市值 |
| stock_date | date | 库存日期 |
| snapshot_date | date | 快照日期（用于时间筛选） |
| discount_rate | decimal(38,9) | 折扣率 |

#### fact_product_launch（商品上市事实表）
| 字段名 | 类型 | 说明 |
|--------|------|------|
| store_code | varchar | 门店编码（关联 dim_shop.tr_shop_code） |
| sku | varchar | SKU 编码（关联 dim_product） |
| skc | varchar | SKC 编码（款色） |
| zprod_code | varchar | 商品编码 |
| brand_code | varchar | 品牌编码 |
| brand_name | varchar | 品牌名称 |
| launch_date | date | 上市日期 |
| prod_year | varchar | 商品年份 |
| prod_season | varchar | 商品季节 |
| dt | varchar | 数据日期 |

### 1.3 维度表字段

#### dim_product（商品维度表）
| 字段名 | 类型 | 说明 |
|--------|------|------|
| sku | varchar | SKU 编码（主键） |
| skc | varchar | SKC 编码（款色） |
| product_sc_type | varchar | 商品小类 |
| product_sc_type_code | varchar | 商品小类编码 |
| mid_category | varchar | 中类 |
| mid_category_code | varchar | 中类编码 |
| little_category | varchar | 小类 |
| little_category_code | varchar | 小类编码 |
| style_code | varchar | 款式编码 |
| style_name | varchar | 款式名称 |
| age_group | varchar | 年龄段 |
| age_group_code | varchar | 年龄段编码 |
| brand_id | int | 品牌 ID |
| color_code | varchar | 颜色编码 |
| color_name | varchar | 颜色名称 |
| come_up_batch | varchar | 上市批次 |
| gender | varchar | 性别 |
| gender_code | varchar | 性别编码 |
| price_level | varchar | 价格带 |
| product_brand_code | varchar | 商品品牌编码 |
| product_brand_name | varchar(255) | 商品品牌名称 |
| product_hierarchy | varchar | 商品层级 |
| product_position_code | varchar | 商品定位编码 |
| real_market_date | varchar | 实际上市日期 |
| product_year | smallint | 商品年份 |
| product_season | varchar | 商品季节 |
| season | varchar | 季节 |
| season_code | varchar | 季节编码 |
| coefficient | varchar | 系数 |
| sub_brand_id | varchar(255) | 子品牌 ID |
| tag_price | decimal(20,4) | 吊牌价 |
| new_arrival_price | decimal(38,9) | 新品价 |
| dt | date | 数据日期 |

#### dim_shop（店铺维度表）
| 字段名 | 类型 | 说明 |
|--------|------|------|
| tr_shop_code | varchar | 门店编码-数仓 Key（主键，用于与事实表 JOIN） |
| shop_code | varchar | 门店编码（业务编码） |
| shop_id | bigint | 门店 ID |
| shop_brand_id | bigint | 门店品牌 ID |
| shop_leader | varchar | 店长姓名 |
| shop_leader_code | varchar | 店长编码 |
| shop_status | varchar | 门店状态 |
| shop_status_code | varchar | 门店状态编码 |
| province | varchar | 省份 |
| province_id | bigint | 省份 ID |
| city | varchar | 城市 |
| city_id | bigint | 城市 ID |
| city_grade | varchar | 城市等级 |
| city_grade_id | bigint | 城市等级 ID |
| district | varchar | 区县 |
| address | varchar | 地址 |
| shop_name | varchar | 门店名称 |
| business_area | int | 营业面积 |
| business_district_level | varchar | 商圈等级 |
| business_district_level_code | varchar | 商圈等级编码 |
| first_channel | varchar | 一级渠道 |
| first_channel_id | bigint | 一级渠道 ID |
| first_channel_code | varchar | 一级渠道编码 |
| second_channel | varchar | 二级渠道 |
| second_channel_id | bigint | 二级渠道 ID |
| second_channel_code | varchar | 二级渠道编码 |
| channel_type_id | bigint | 渠道类型 ID |
| opening_date | varchar | 开店日期 |
| closing_date | varchar | 闭店日期 |
| dt | date | 数据日期 |

#### dim_vip（会员维度表）
| 字段名 | 类型 | 说明 |
|--------|------|------|
| dt | date | 数据日期 |
| vip_id | bigint | 会员 ID（主键） |
| vip_code | varchar | 会员编码 |
| vip_name | varchar | 会员姓名 |
| vip_level | varchar | 会员等级 |
| vip_level_code | varchar | 会员等级编码 |
| vip_status | varchar | 会员状态 |
| vip_status_code | varchar | 会员状态编码 |
| vip_reg_date | varchar | 注册日期 |
| vip_last_login_date | varchar | 最后登录日期 |

### 1.4 表间关系（JOIN 规范）

```
-- 订单表关联维度表
fact_orders.sku = dim_product.sku
fact_orders.shop_code = dim_shop.tr_shop_code
fact_orders.vip_id = dim_vip.vip_id

-- 库存表关联维度表
fact_inventory.sku = dim_product.sku
fact_inventory.shop_code = dim_shop.tr_shop_code

-- 商品上市表关联维度表
fact_product_launch.sku = dim_product.sku
fact_product_launch.store_code = dim_shop.tr_shop_code
```

⚠️ **JOIN 关键注意事项**：
- dim_shop 的主键是 `tr_shop_code`（数仓 Key），不是 `shop_code`（业务编码）。事实表中的 `shop_code` / `store_code` 对应的是 `dim_shop.tr_shop_code`
- dim_vip 的主键是 `vip_id`（bigint），与 fact_orders 的 `vip_id` 关联
- dim_product 的主键是 `sku`，三张事实表都通过 `sku` 字段关联
- **本数据库没有独立的日期维度表**，时间筛选直接使用事实表的 `dt`（date 类型）或 `snapshot_date` 字段

---

## 常用 SQL 查询模板（标准模型：直接复制修改）

### 模板 1：上月某指标的汇总值

```sql
SELECT
    SUM(retail_amount) AS total_sales
FROM fact_orders
WHERE dt >= DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 MONTH), '%Y-%m-01')
  AND dt < DATE_FORMAT(CURDATE(), '%Y-%m-01');
```

### 模板 2：上月各渠道的销售额及环比

```sql
WITH current_month AS (
    SELECT
        ds.first_channel,
        SUM(fo.retail_amount) AS sales
    FROM fact_orders fo
    JOIN dim_shop ds ON fo.shop_code = ds.tr_shop_code
    WHERE fo.dt >= DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 MONTH), '%Y-%m-01')
      AND fo.dt < DATE_FORMAT(CURDATE(), '%Y-%m-01')
    GROUP BY ds.first_channel
),
previous_month AS (
    SELECT
        ds.first_channel,
        SUM(fo.retail_amount) AS sales
    FROM fact_orders fo
    JOIN dim_shop ds ON fo.shop_code = ds.tr_shop_code
    WHERE fo.dt >= DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 2 MONTH), '%Y-%m-01')
      AND fo.dt < DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 MONTH), '%Y-%m-01')
    GROUP BY ds.first_channel
)
SELECT
    c.first_channel,
    c.sales AS current_sales,
    p.sales AS previous_sales,
    (c.sales - p.sales) / NULLIF(p.sales, 0) AS mom_growth
FROM current_month c
LEFT JOIN previous_month p ON c.first_channel = p.first_channel
ORDER BY c.sales DESC;
```

### 模板 3：Top-N 品牌排名

```sql
SELECT
    dp.product_brand_name,
    SUM(fo.retail_amount) AS total_sales,
    COUNT(DISTINCT fo.order_number) AS order_count,
    SUM(fo.retail_amount) / NULLIF(COUNT(DISTINCT fo.vip_id), 0) AS aov
FROM fact_orders fo
JOIN dim_product dp ON fo.sku = dp.sku
WHERE fo.dt >= DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 MONTH), '%Y-%m-01')
  AND fo.dt < DATE_FORMAT(CURDATE(), '%Y-%m-01')
GROUP BY dp.product_brand_name
ORDER BY total_sales DESC
LIMIT 10;
```

### 模板 4：某维度在全局的占比

```sql
SELECT
    ds.first_channel,
    SUM(fo.retail_amount) AS channel_sales,
    SUM(fo.retail_amount) / SUM(SUM(fo.retail_amount)) OVER () AS sales_proportion
FROM fact_orders fo
JOIN dim_shop ds ON fo.shop_code = ds.tr_shop_code
WHERE fo.dt >= DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 MONTH), '%Y-%m-01')
  AND fo.dt < DATE_FORMAT(CURDATE(), '%Y-%m-01')
GROUP BY ds.first_channel
ORDER BY channel_sales DESC;
```

### 模板 5：日趋势查询

```sql
SELECT
    fo.dt,
    SUM(fo.retail_amount) AS daily_sales
FROM fact_orders fo
WHERE fo.dt >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
  AND fo.dt < CURDATE()
GROUP BY fo.dt
ORDER BY fo.dt;
```

> ⚠️ **StarRocks 兼容性提示**：StarRocks 兼容 MySQL 语法，但注意：
> - 使用 `DATE_FORMAT`、`DATE_SUB`、`CURDATE()` 等标准函数
> - 窗口函数（`OVER()`）完全支持
> - `NULLIF` 用于避免除零错误

---

## 2. 语义理解（SQL 生成前必做）

在写任何 SQL 之前，先把用户的问题拆解为四个维度：

| 维度 | 问自己 | 示例 |
|------|--------|------|
| 看什么（指标） | 用户要看的业务量是什么？ | "销售额""客单价""库存量" |
| 怎么看（分析方式） | 直接看值？还是要对比/占比/排名/趋势？ | "同比增长率""占比""排名前5""月趋势" |
| 看谁的（维度 & 筛选） | 按什么维度拆分？筛选哪些范围？ | "各品牌""某渠道""某地区" |
| 看哪段时间（时间） | 时间范围是什么？ | "上月""近7天""某月 vs 另一月" |

### 2.1 从 Schema 推断指标

本数据库没有统一的指标定义层。你需要根据 §1 中的表结构和字段说明，自行推断用户业务术语对应的 SQL 写法。

⚠️ **这是 Text-to-SQL 最容易出错的环节**。以下是常见的歧义陷阱，务必留意：

**陷阱 A — 金额口径歧义**：fact_orders 中有多个金额字段（retail_amount、net_amount、retail_market_value 等），用户说"销售额"时到底指哪个？不同口径的差异可能很大。当无法确定时，应在查询解读中说明你采用的口径。

**陷阱 B — 复合指标的计算方式**：像"客单价""连带率""件单价""折扣率""退货率"这类复合指标，需要你根据业务含义自行组合字段计算。同一个术语可能有多种合理的计算方式（例如"客单价"的分母是人数还是单数？），不同算法的结果可能相差数十倍。

**陷阱 C — 跨表指标**：有些指标可能涉及多张表的数据（如库存相关指标在 fact_inventory，销售相关在 fact_orders）。注意判断指标来自哪张表，不要在错误的表上查询。

**陷阱 D — 数据库能力边界**：本数据库是零售订单、库存和商品数据，不包含所有业务数据。如果用户询问的指标在现有表中找不到对应字段，应如实告知，不要强行拼凑。

### 2.2 关键语义消歧规则

**规则 A — "总和" vs "分别"**

| 用户说 | 含义 | GROUP BY |
|-------|------|----------|
| "A 和 B 的某指标分别是多少" | 按 A、B 分组展示 | 保留分组 |
| "A 和 B 的某指标总和" | A+B 合并为一个数字 | 不分组 |
| "A 和 B 的某指标"（无修饰） | 默认"分别" | 保留分组 |

**规则 B — "占比" 的两种含义**

| 用户说 | 含义 | SQL 实现 |
|-------|------|---------|
| "某指标占比"（如"销售额占比"） | 值占比 | `SUM(x) / SUM(SUM(x)) OVER()` |
| "某实体占比"（如"款色占比"） | 数量占比 | `COUNT(DISTINCT entity) / (SELECT COUNT(DISTINCT entity) FROM ...)` |

**规则 C — "同比" vs "环比"**

| 用户说 | 含义 | SQL 实现 |
|-------|------|---------|
| "同比"（无限定）| 年同比 (YoY) | 与去年同期对比 |
| "月同比" | 与上月同期对比 | 上个月的同日/同周 |
| "环比" | 与上一个周期对比 | 根据粒度：日→前一天，月→前一月 |

**规则 D — 简单优先**

如果用户问题可以用简单 SQL 回答，就不要写复杂的 CTE 和窗口函数。

---

## 3. SQL 生成规范

### 3.1 JOIN 规则

- 只 JOIN 需要的表，不要多余 JOIN
- 使用 LEFT JOIN 保证事实表数据不丢失
- 维度表字段用于 SELECT/WHERE/GROUP BY 时才 JOIN 对应维度表
- **dim_shop 关联用 `tr_shop_code`**，不要用 `shop_code`

```sql
-- 示例：按一级渠道查销售额
SELECT ds.first_channel, SUM(fo.retail_amount) AS retail_amt
FROM fact_orders fo
LEFT JOIN dim_shop ds ON fo.shop_code = ds.tr_shop_code
WHERE fo.dt >= '2026-02-01' AND fo.dt < '2026-03-01'
GROUP BY ds.first_channel
ORDER BY retail_amt DESC;
```

```sql
-- 示例：按品牌查销售额
SELECT dp.product_brand_name, SUM(fo.retail_amount) AS retail_amt
FROM fact_orders fo
LEFT JOIN dim_product dp ON fo.sku = dp.sku
WHERE fo.dt >= '2026-02-01' AND fo.dt < '2026-03-01'
GROUP BY dp.product_brand_name
ORDER BY retail_amt DESC;
```

```sql
-- 示例：按会员等级查购买人数
SELECT dv.vip_level, COUNT(DISTINCT fo.vip_id) AS vip_count
FROM fact_orders fo
LEFT JOIN dim_vip dv ON fo.vip_id = dv.vip_id
WHERE fo.dt >= '2026-02-01' AND fo.dt < '2026-03-01'
GROUP BY dv.vip_level
ORDER BY vip_count DESC;
```

### 3.2 时间处理

**时间字段说明**：
- fact_orders 用 `dt`（date 类型）做时间筛选
- fact_inventory 用 `snapshot_date`（date 类型）做时间筛选
- fact_product_launch 用 `launch_date`（date 类型）做时间筛选

**相对时间转换**：

| 用户说 | WHERE 条件 |
|-------|-----------|
| 上月 | `dt >= DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 MONTH), '%Y-%m-01') AND dt < DATE_FORMAT(CURDATE(), '%Y-%m-01')` |
| 本月 | `dt >= DATE_FORMAT(CURDATE(), '%Y-%m-01') AND dt < DATE_ADD(DATE_FORMAT(CURDATE(), '%Y-%m-01'), INTERVAL 1 MONTH)` |
| 昨天 | `dt = DATE_SUB(CURDATE(), INTERVAL 1 DAY)` |
| 近7天 | `dt >= DATE_SUB(CURDATE(), INTERVAL 7 DAY) AND dt < CURDATE()` |
| 近30天 | `dt >= DATE_SUB(CURDATE(), INTERVAL 30 DAY) AND dt < CURDATE()` |
| 本年 | `dt >= DATE_FORMAT(CURDATE(), '%Y-01-01')` |
| 去年 | `dt >= DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 YEAR), '%Y-01-01') AND dt < DATE_FORMAT(CURDATE(), '%Y-01-01')` |

### 3.3 同环比计算

同环比需要用 CTE 或子查询分别获取两个时期的数据再对比：

```sql
-- 月环比示例：上月 vs 上上月整体销售额
WITH current_month AS (
    SELECT SUM(retail_amount) AS current_val
    FROM fact_orders
    WHERE dt >= DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 MONTH), '%Y-%m-01')
      AND dt < DATE_FORMAT(CURDATE(), '%Y-%m-01')
),
previous_month AS (
    SELECT SUM(retail_amount) AS previous_val
    FROM fact_orders
    WHERE dt >= DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 2 MONTH), '%Y-%m-01')
      AND dt < DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 MONTH), '%Y-%m-01')
)
SELECT
    cm.current_val,
    pm.previous_val,
    cm.current_val - pm.previous_val AS change_value,
    (cm.current_val - pm.previous_val) / NULLIF(pm.previous_val, 0) AS growth_rate
FROM current_month cm, previous_month pm;
```

**按维度拆分的同环比更加复杂**，需要用 FULL JOIN：

```sql
-- 各渠道月环比
WITH current_month AS (
    SELECT ds.first_channel, SUM(fo.retail_amount) AS current_val
    FROM fact_orders fo
    LEFT JOIN dim_shop ds ON fo.shop_code = ds.tr_shop_code
    WHERE fo.dt >= DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 MONTH), '%Y-%m-01')
      AND fo.dt < DATE_FORMAT(CURDATE(), '%Y-%m-01')
    GROUP BY ds.first_channel
),
previous_month AS (
    SELECT ds.first_channel, SUM(fo.retail_amount) AS previous_val
    FROM fact_orders fo
    LEFT JOIN dim_shop ds ON fo.shop_code = ds.tr_shop_code
    WHERE fo.dt >= DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 2 MONTH), '%Y-%m-01')
      AND fo.dt < DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 MONTH), '%Y-%m-01')
    GROUP BY ds.first_channel
)
SELECT
    COALESCE(cm.first_channel, pm.first_channel) AS `一级渠道`,
    cm.current_val AS `本月销售金额`,
    pm.previous_val AS `上月销售金额`,
    (cm.current_val - pm.previous_val) / NULLIF(pm.previous_val, 0) AS `月环比增长率`
FROM current_month cm
FULL JOIN previous_month pm ON cm.first_channel = pm.first_channel
ORDER BY `月环比增长率` DESC;
```

### 3.4 占比计算

```sql
-- 各渠道销售额占比
SELECT
    ds.first_channel,
    SUM(fo.retail_amount) AS retail_amt,
    SUM(fo.retail_amount) / SUM(SUM(fo.retail_amount)) OVER() AS proportion
FROM fact_orders fo
LEFT JOIN dim_shop ds ON fo.shop_code = ds.tr_shop_code
WHERE fo.dt >= DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 MONTH), '%Y-%m-01')
  AND fo.dt < DATE_FORMAT(CURDATE(), '%Y-%m-01')
GROUP BY ds.first_channel
ORDER BY retail_amt DESC;
```

### 3.5 排名计算

```sql
-- 品牌销售额 TOP 5
SELECT
    dp.product_brand_name,
    SUM(fo.retail_amount) AS retail_amt,
    RANK() OVER(ORDER BY SUM(fo.retail_amount) DESC) AS rk
FROM fact_orders fo
LEFT JOIN dim_product dp ON fo.sku = dp.sku
WHERE fo.dt >= DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 MONTH), '%Y-%m-01')
  AND fo.dt < DATE_FORMAT(CURDATE(), '%Y-%m-01')
GROUP BY dp.product_brand_name
ORDER BY retail_amt DESC
LIMIT 5;
```

---

## 4. 输出规范

每次执行查询时，必须按以下**三段式结构**向用户展示信息，缺一不可，顺序不可颠倒：

### 4.1 📊 查询解读（自然语言，放在最前面）

用一段自然语言向用户解释"查了什么、怎么查的"，让非技术用户也能理解查询含义。

写作要求：
- 用一段连贯的话描述，不要用列表
- 涵盖以下要素：查了什么指标、什么时间范围、按什么维度拆分、有什么筛选条件、做了什么计算
- 简单查询简短说（1~2句），复杂查询可以多说几句

### 4.2 📋 SQL 查询语句

展示完整的、格式化的 SQL 语句：

```sql
SELECT ...
FROM ...
WHERE ...
GROUP BY ...
ORDER BY ...;
```

### 4.3 📈 查询结果

以表格形式展示查询返回的数据结果。列名使用中文展示名。

### 4.4 完整输出示例

**示例 A — 简单查询**：用户问"上月的销售额是多少？"

📊 **查询解读**

帮你查询了上月（2026年2月）的零售金额（retail_amount 求和），查的是整体总量，没有按维度拆分。

📋 **SQL 查询语句：**
```sql
SELECT SUM(retail_amount) AS `零售金额`
FROM fact_orders
WHERE dt >= '2026-02-01' AND dt < '2026-03-01';
```

📈 **查询结果**：
上月（2026年2月）的零售金额为 **12,345,678 元**。

**示例 B — 带维度和环比的复杂查询**：用户问"上月各渠道的销售额及月环比增长率，增速前5名是哪些？"

📊 **查询解读**

帮你查询了上月（2026年2月）各一级渠道的零售金额（retail_amount 求和），并用 CTE 分别计算了本月和上月的数据后做对比，得出月环比增长率。结果按环比增长率从高到低排列，取前 5 名。

📋 **SQL 查询语句：**
```sql
WITH current_month AS (
    SELECT ds.first_channel, SUM(fo.retail_amount) AS current_val
    FROM fact_orders fo
    LEFT JOIN dim_shop ds ON fo.shop_code = ds.tr_shop_code
    WHERE fo.dt >= '2026-02-01' AND fo.dt < '2026-03-01'
    GROUP BY ds.first_channel
),
previous_month AS (
    SELECT ds.first_channel, SUM(fo.retail_amount) AS previous_val
    FROM fact_orders fo
    LEFT JOIN dim_shop ds ON fo.shop_code = ds.tr_shop_code
    WHERE fo.dt >= '2026-01-01' AND fo.dt < '2026-02-01'
    GROUP BY ds.first_channel
)
SELECT
    COALESCE(cm.first_channel, pm.first_channel) AS `一级渠道`,
    cm.current_val AS `本月零售金额`,
    pm.previous_val AS `上月零售金额`,
    (cm.current_val - pm.previous_val) / NULLIF(pm.previous_val, 0) AS `月环比增长率`
FROM current_month cm
FULL JOIN previous_month pm ON cm.first_channel = pm.first_channel
ORDER BY `月环比增长率` DESC
LIMIT 5;
```

📈 **查询结果**：
| 一级渠道 | 本月零售金额 | 上月零售金额 | 月环比增长率 |
|---------|------------|------------|------------|
| 电商 | 5,234,567 | 4,426,012 | +18.3% |
| 直营 | 3,456,789 | 3,083,754 | +12.1% |
| ... | ... | ... | ... |

---

## 5. SQL 生成流程

### 步骤 0：语义解析
按 §2 将用户问题拆解为"看什么 / 怎么看 / 看谁的 / 看哪段时间"四维度。检查 §2.2 的消歧规则。

### 步骤 1：确定指标和表
- 根据 §2.1 的映射表，确定需要的 SQL 聚合表达式
- 确定涉及哪些事实表（fact_orders / fact_inventory / fact_product_launch）
- **⚠️ 当指标存在歧义时**（如"销售额"可能是 retail_amount 或 net_amount，"客单价"有多种算法），应在查询解读中说明所采用的口径，或主动询问用户

### 步骤 2：确定维度和 JOIN
- 根据用户需要的分组维度，确定需要 JOIN 哪些维度表
- 按 §1.4 的关系进行 JOIN
- **特别注意**：渠道/地区维度在 dim_shop 中，品类/品牌维度在 dim_product 中，会员维度在 dim_vip 中

### 步骤 3：构建时间条件
- 按 §3.2 将用户的时间描述转为 WHERE 条件
- 用户未指定时间时的默认策略：
  - 有同环比 → 默认上月
  - 有趋势 → 默认近12个月
  - 有排名/TOP-N → 默认上月
  - 其他 → 默认近7天

### 步骤 4：构建聚合和计算
- 同环比 → CTE 分两期查询再 JOIN（§3.3）
- 占比 → 窗口函数（§3.4）
- 排名 → 窗口函数（§3.5）

### 步骤 5：SQL 自检
生成 SQL 后，逐项检查：
- ✅ 输出结构为三段式：📊 查询解读 → 📋 SQL → 📈 结果
- ✅ 所有 JOIN 条件正确：fact_orders.shop_code = dim_shop.tr_shop_code（不是 shop_code）
- ✅ WHERE 条件中时间范围正确（左闭右开）
- ✅ GROUP BY 包含所有非聚合列
- ✅ NULLIF 处理除零问题
- ✅ 聚合函数与业务含义一致（SUM vs COUNT DISTINCT vs AVG）
- ✅ 列别名使用中文展示名

### 步骤 6：执行并展示
通过 §0 的 Gateway JDBC API 执行 SQL，按 §4 的三段式格式展示结果。

**执行注意事项**：
- API 返回的是 Markdown 表格纯文本，直接展示给用户即可
- 如遇 `Table not allowed` 错误，说明查询了白名单以外的表，检查 §1.1 的可用表列表
- 如遇查询超时（30 秒），考虑缩小时间范围或加更严格的 WHERE 条件
- SQL 中字符串值用**单引号**包裹（如 `WHERE sku = 'SKU1000211'`）
- 始终显式加 LIMIT，避免依赖服务端自动 LIMIT 1000

---

## 6. 常见错误模式

**❌ 模式 1：金额字段选错**
retail_amount（零售金额）和 net_amount（净销售金额）差异可能很大。必须确认用户意图。

**❌ 模式 2：客单价算法歧义**
- `SUM(retail_amount) / COUNT(DISTINCT vip_id)` = 人均消费金额
- `SUM(retail_amount) / COUNT(DISTINCT order_number)` = 单均金额
- 两者数值可能相差数十倍。

**❌ 模式 3：dim_shop JOIN 键用错**
事实表的 `shop_code` 对应 dim_shop 的 `tr_shop_code`（数仓 Key），**不是** dim_shop 的 `shop_code`（业务编码）。这是最容易犯的错误。

**❌ 模式 4：同环比时间范围写错**
手动计算两个时期的时间范围容易出错，特别是跨年、跨月场景。

**❌ 模式 5：维度值不确定**
不知道维度表中具体有哪些值（如一级渠道到底有哪些），应先查询确认：
```sql
SELECT DISTINCT first_channel FROM dim_shop;
SELECT DISTINCT product_brand_name FROM dim_product;
SELECT DISTINCT vip_level FROM dim_vip;
```

**❌ 模式 6：缺少行业术语理解**
数据库 schema 不包含业务语义。例如"动销率""售罄率""库销比"等行业指标，纯靠 schema 无法推断其计算公式。

**❌ 模式 7：GROUP BY 缺失列**
SELECT 中有非聚合列但 GROUP BY 中遗漏，在严格模式下会报错。

**❌ 模式 8：除零错误**
环比增长率等计算中，分母可能为 0 或 NULL，必须用 NULLIF 处理。

**❌ 模式 9：库存表时间字段用错**
fact_inventory 的时间筛选用 `snapshot_date`，不是 `dt`（该表无 dt 字段）。fact_orders 的时间筛选用 `dt`。

---

## 7. 局限性声明

本 Skill 直接基于数据库 schema 生成 SQL，存在以下固有局限：

1. **指标口径无统一定义**：同一业务概念（如"客单价"）可能有多种 SQL 实现，需要人工确认
2. **无内置快速计算**：同环比、占比、排名等分析计算需要手写复杂 SQL（CTE/窗口函数）
3. **无维度值元数据**：不知道维度表中具体有哪些值，需要先查询确认
4. **无业务语义层**：数据库字段注释不足以表达完整的业务语义（如"销售额"到底用哪个金额字段）
5. **无独立流量表**：本数据库无流量数据（UV/PV），无法计算转化率等跨表指标
6. **无日期维度表**：时间属性（年/季/月/周/是否周末等）需要通过 SQL 日期函数实现
