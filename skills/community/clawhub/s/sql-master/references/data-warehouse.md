# 数仓建模 & 分层架构

## 数仓分层架构（标准）

```
原始数据
    ↓
ODS（Operational Data Store）操作数据层
    ↓
DWD（Data Warehouse Detail）明细数据层
    ↓
DWS（Data Warehouse Summary）汇总数据层
    ↓
ADS（Application Data Store）应用数据层
    ↓
报表 / BI / 应用
```

### 各层职责

| 层 | 职责 | 特点 |
|----|------|------|
| ODS | 原始数据落地，不做业务加工 | 保留原始字段，全量或增量同步 |
| DWD | 数据清洗、标准化、维度关联 | 1:1 对应业务事实，最细粒度 |
| DWS | 按主题聚合，轻度汇总 | 按天/周/月聚合，宽表 |
| ADS | 面向具体应用的指标 | 直接支撑报表，高度聚合 |

---

## 维度建模

### 星型模型 vs 雪花模型

```
星型模型：
  事实表 ← 直接关联 → 维度表（维度表不再关联其他维度表）
  优点：查询简单，JOIN 少，性能好
  缺点：维度表可能有冗余

雪花模型：
  事实表 ← 维度表 ← 子维度表（维度表继续规范化）
  优点：存储空间小，无冗余
  缺点：JOIN 多，查询复杂，性能差

实践建议：OLAP 场景优先用星型模型
```

### 事实表设计
```sql
-- 事实表：记录业务事件，包含度量值和外键
CREATE TABLE dwd_order_detail (
    order_id        BIGINT          COMMENT '订单ID',
    user_id         BIGINT          COMMENT '用户ID（关联用户维度）',
    product_id      BIGINT          COMMENT '商品ID（关联商品维度）',
    date_id         INT             COMMENT '日期ID（关联日期维度，格式 20240101）',
    -- 度量值
    quantity        INT             COMMENT '购买数量',
    unit_price      DECIMAL(10,2)   COMMENT '单价',
    discount_amount DECIMAL(10,2)   COMMENT '优惠金额',
    actual_amount   DECIMAL(10,2)   COMMENT '实付金额',
    -- 分区字段
    dt              STRING          COMMENT '数据日期分区 yyyy-MM-dd'
)
COMMENT '订单明细事实表'
PARTITIONED BY (dt STRING)
STORED AS ORC;
```

### 维度表设计
```sql
-- 维度表：描述业务实体的属性
CREATE TABLE dim_user (
    user_id         BIGINT          COMMENT '用户ID',
    username        STRING          COMMENT '用户名',
    register_date   STRING          COMMENT '注册日期',
    city            STRING          COMMENT '城市',
    age_group       STRING          COMMENT '年龄段（18-24/25-34/...）',
    user_level      STRING          COMMENT '用户等级（普通/银牌/金牌/钻石）',
    -- SCD（缓慢变化维度）字段
    start_date      STRING          COMMENT '该版本生效日期',
    end_date        STRING          COMMENT '该版本失效日期（9999-12-31 表示当前有效）',
    is_current      TINYINT         COMMENT '是否当前版本（1=是）'
)
COMMENT '用户维度表'
STORED AS ORC;
```

---

## 缓慢变化维度（SCD）

### SCD Type 1：直接覆盖
```sql
-- 适用：不需要历史，只关心当前值
UPDATE dim_user SET city = '上海' WHERE user_id = 1001;
-- 缺点：历史数据丢失
```

### SCD Type 2：新增版本（最常用）
```sql
-- 适用：需要保留历史，分析不同时期的属性
-- 用户从北京迁到上海时，新增一行，旧行标记失效

-- 失效旧版本
UPDATE dim_user
SET end_date = '2024-01-14', is_current = 0
WHERE user_id = 1001 AND is_current = 1;

-- 插入新版本
INSERT INTO dim_user VALUES
(1001, '张三', '2020-01-01', '上海', '25-34', '金牌', '2024-01-15', '9999-12-31', 1);

-- 查询某时间点的用户属性（点查）
SELECT * FROM dim_user
WHERE user_id = 1001
  AND start_date <= '2024-01-10'
  AND end_date > '2024-01-10';
```

---

## 数仓常用 SQL 模式

### 增量数据处理（每日 ETL）
```sql
-- 场景：每天增量同步订单数据到 DWD
-- 策略：按分区覆盖写（INSERT OVERWRITE）

INSERT OVERWRITE TABLE dwd_order_detail PARTITION (dt = '2024-01-15')
SELECT
    o.order_id,
    o.user_id,
    o.product_id,
    DATE_FORMAT(o.create_time, '%Y%m%d')    AS date_id,
    o.quantity,
    o.unit_price,
    COALESCE(o.discount_amount, 0)          AS discount_amount,
    o.actual_amount,
    '2024-01-15'                            AS dt
FROM ods_orders o
WHERE DATE(o.create_time) = '2024-01-15'
  AND o.status != 'cancelled';
```

### 拉链表（全量历史快照）
```sql
-- 场景：记录每天的用户状态快照，支持任意时间点查询
-- 比 SCD Type 2 更简单，适合数仓

-- 每天生成当天快照
INSERT INTO dws_user_snapshot PARTITION (dt = '2024-01-15')
SELECT
    user_id,
    username,
    status,
    vip_level,
    total_orders,
    total_amount,
    '2024-01-15' AS dt
FROM (
    -- 昨天快照 + 今天变更 = 今天快照
    SELECT * FROM dws_user_snapshot WHERE dt = '2024-01-14'
    UNION ALL
    SELECT user_id, username, status, vip_level, ...
    FROM ods_user_changes WHERE dt = '2024-01-15'
) t
-- 如果同一用户有多条，取最新的
QUALIFY ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY dt DESC) = 1;
```

### 漏斗分析
```sql
-- 场景：分析用户从浏览 → 加购 → 下单 → 支付的转化漏斗
WITH funnel AS (
    SELECT
        user_id,
        MAX(CASE WHEN event = 'view'    THEN 1 ELSE 0 END) AS step1_view,
        MAX(CASE WHEN event = 'add_cart' THEN 1 ELSE 0 END) AS step2_cart,
        MAX(CASE WHEN event = 'order'   THEN 1 ELSE 0 END) AS step3_order,
        MAX(CASE WHEN event = 'pay'     THEN 1 ELSE 0 END) AS step4_pay
    FROM user_events
    WHERE dt = '2024-01-15'
    GROUP BY user_id
)
SELECT
    SUM(step1_view)                                     AS view_cnt,
    SUM(step2_cart)                                     AS cart_cnt,
    SUM(step3_order)                                    AS order_cnt,
    SUM(step4_pay)                                      AS pay_cnt,
    ROUND(SUM(step2_cart) / SUM(step1_view) * 100, 2)  AS view_to_cart_rate,
    ROUND(SUM(step3_order) / SUM(step2_cart) * 100, 2) AS cart_to_order_rate,
    ROUND(SUM(step4_pay) / SUM(step3_order) * 100, 2)  AS order_to_pay_rate
FROM funnel;
```

### 留存分析
```sql
-- 场景：计算用户次日留存、7日留存、30日留存
WITH new_users AS (
    -- 每天新注册用户
    SELECT user_id, DATE(register_time) AS register_date
    FROM users
    WHERE register_time >= '2024-01-01'
),
active_users AS (
    -- 每天活跃用户
    SELECT DISTINCT user_id, DATE(login_time) AS active_date
    FROM user_logins
)
SELECT
    n.register_date,
    COUNT(DISTINCT n.user_id)                                           AS new_user_cnt,
    COUNT(DISTINCT CASE WHEN DATEDIFF(a1.active_date, n.register_date) = 1  THEN n.user_id END) AS day1_retain,
    COUNT(DISTINCT CASE WHEN DATEDIFF(a7.active_date, n.register_date) = 7  THEN n.user_id END) AS day7_retain,
    COUNT(DISTINCT CASE WHEN DATEDIFF(a30.active_date, n.register_date) = 30 THEN n.user_id END) AS day30_retain
FROM new_users n
LEFT JOIN active_users a1  ON n.user_id = a1.user_id AND DATEDIFF(a1.active_date, n.register_date) = 1
LEFT JOIN active_users a7  ON n.user_id = a7.user_id AND DATEDIFF(a7.active_date, n.register_date) = 7
LEFT JOIN active_users a30 ON n.user_id = a30.user_id AND DATEDIFF(a30.active_date, n.register_date) = 30
GROUP BY n.register_date
ORDER BY n.register_date;
```

---

## 数据倾斜处理（Hive/Spark）

```sql
-- 症状：某些 Reduce 任务跑很久，其他早就完成了
-- 原因：JOIN 或 GROUP BY 的 key 分布不均

-- 方案 1：广播小表（Map Join）
SELECT /*+ MAPJOIN(dim_user) */ o.*, u.username
FROM dwd_orders o
JOIN dim_user u ON o.user_id = u.user_id;

-- 方案 2：加盐打散（处理 GROUP BY 倾斜）
-- 第一步：加随机盐，局部聚合
SELECT
    CONCAT(user_id, '_', FLOOR(RAND() * 10)) AS salted_key,
    SUM(amount) AS partial_sum
FROM orders
GROUP BY CONCAT(user_id, '_', FLOOR(RAND() * 10));

-- 第二步：去盐，全局聚合
SELECT
    SPLIT(salted_key, '_')[0] AS user_id,
    SUM(partial_sum) AS total_amount
FROM (上面的结果)
GROUP BY SPLIT(salted_key, '_')[0];

-- 方案 3：Hive 配置（自动处理倾斜）
SET hive.optimize.skewjoin = true;
SET hive.skewjoin.key = 100000;  -- 超过此行数认为倾斜
```
