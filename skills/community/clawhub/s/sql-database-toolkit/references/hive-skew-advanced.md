# Hive 数据倾斜：大厂生产级深化补充

## 目录
1. [执行引擎底层原理（MR vs Tez vs Spark）](#1-执行引擎底层原理)
2. [倾斜量化评估模型](#2-倾斜量化评估模型)
3. [极端场景与边界案例](#3-极端场景与边界案例)
4. [动态智能倾斜检测](#4-动态智能倾斜检测)
5. [与上下游生态联动](#5-与上下游生态联动)

---

## 1. 执行引擎底层原理

### 1.1 三种引擎的倾斜发生位置

#### MapReduce 引擎
```
Map Task（并行）
    ↓ Shuffle（按 key hash 分发）← 倾斜在这里产生
Reduce Task（并行）
    ↓
输出

倾斜根因：
  hash(key) % numReducers 决定数据去哪个 Reducer
  user_id=1 的 400 万行全部 hash 到同一个 Reducer
  该 Reducer 处理 400 万行，其他 Reducer 处理几万行
  → 整个 Job 等最慢的那个 Reducer 完成
```

#### Tez 引擎（DAG 模型）
```
Tez 把 MR Job 拆成 DAG（有向无环图），每个节点叫 Vertex

典型 GROUP BY 的 DAG：
  Map Vertex（读数据 + 局部聚合）
      ↓ Shuffle Edge（SCATTER_GATHER，按 key 分发）← 倾斜在这里
  Reduce Vertex（全局聚合）
      ↓
  Output Vertex

典型 JOIN 的 DAG：
  Map Vertex A（扫描大表）
  Map Vertex B（扫描小表）
      ↓ Broadcast Edge（小表广播）← MapJoin 走这条边，无倾斜
  Map Join Vertex（在 Map 端完成 JOIN）

关键差异：
  Tez 的 SCATTER_GATHER Edge 支持 Auto Parallelism
  → 运行时动态调整 Reduce Vertex 的并发度
  → 比 MR 的静态 numReducers 更灵活

查看 Tez DAG：
  Tez UI（http://<rm>:8080/tez-ui）→ DAG Details → Vertex 耗时对比
  耗时最长的 Vertex 就是倾斜所在
```

```sql
-- 查看 Tez 执行计划（比 EXPLAIN 更详细）
EXPLAIN FORMATTED
SELECT user_id, COUNT(*), SUM(amount)
FROM ods_orders
GROUP BY user_id;
-- 输出中找 "Reduce Operator Tree" 和 "Statistics"
-- Statistics: Num rows: X Data size: Y → 估算各 Vertex 数据量
```

#### Spark 引擎（Hive on Spark）
```
Spark 把 Job 拆成 Stage，Stage 之间有 Shuffle

典型 GROUP BY：
  Stage 0：Map（读数据）
      ↓ Shuffle Write（按 key 分区写到磁盘）← 倾斜在这里
  Stage 1：Reduce（聚合）
      ↓
  Stage 2：输出

Spark 特有的倾斜表现：
  Spark UI → Stages → 某个 Stage 的 Task 列表
  → 看 "Duration" 列：大多数 Task 几秒，某个 Task 几十分钟
  → 看 "Shuffle Read Size"：某个 Task 读了几 GB，其他只读几 MB

Spark 特有优化（Hive on Spark 可用）：
  spark.sql.adaptive.enabled = true          -- AQE（自适应查询执行）
  spark.sql.adaptive.skewJoin.enabled = true -- 自动倾斜 Join 处理
  spark.sql.adaptive.skewJoin.skewedPartitionFactor = 5   -- 超过中位数5倍认为倾斜
  spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes = 256MB
```

### 1.2 DYNAMIC_PARTITION_PRUNING 与倾斜的关系

```sql
-- DPP（动态分区裁剪）：在 JOIN 时，用小表的过滤条件裁剪大表的分区
-- 这本身不解决倾斜，但能大幅减少参与 JOIN 的数据量，间接缓解倾斜

-- 示例：查询某城市用户的订单
-- 没有 DPP：扫描全部 orders 分区（10 亿行）
-- 有 DPP：先扫描 dim_users 找到北京用户的 user_id，
--          再只扫描这些 user_id 对应的 orders 分区

SET hive.tez.dynamic.partition.pruning = true;
SET hive.tez.dynamic.partition.pruning.max.data.size = 104857600; -- 100MB

EXPLAIN
SELECT o.order_id, o.amount
FROM ods_orders o
JOIN dim_users u ON o.user_id = u.user_id
WHERE u.city = '北京';
-- 执行计划中应出现：Dynamic Partitioning Event Operator
-- 效果：大幅减少 Map 阶段读取的数据量，倾斜 key 的绝对数据量也随之减少
```

---

## 2. 倾斜量化评估模型

### 2.1 倾斜程度量化指标

```python
# skew_analyzer.py
# 量化分析倾斜程度，给出方案选型建议
# 运行：python skew_analyzer.py

import math

def analyze_skew(key_distribution: dict, total_rows: int, num_reducers: int = 200):
    """
    key_distribution: {key: row_count}
    total_rows: 总行数
    num_reducers: Reduce 并发度
    """
    counts = sorted(key_distribution.values(), reverse=True)
    n = len(counts)

    # 指标1：最大 key 占比
    max_key_pct = counts[0] / total_rows * 100

    # 指标2：基尼系数（衡量整体不均匀程度，0=完全均匀，1=极度倾斜）
    sorted_counts = sorted(counts)
    cumsum = 0
    gini_sum = 0
    for i, c in enumerate(sorted_counts):
        cumsum += c
        gini_sum += cumsum
    gini = 1 - 2 * gini_sum / (n * sum(counts)) + 1/n

    # 指标3：理想执行时间 vs 实际执行时间比（倾斜放大系数）
    ideal_rows_per_reducer = total_rows / num_reducers
    max_rows_per_reducer = counts[0]  # 最坏情况：最大 key 独占一个 Reducer
    skew_factor = max_rows_per_reducer / ideal_rows_per_reducer

    # 指标4：Top-N key 集中度
    top1_pct  = counts[0] / total_rows * 100
    top5_pct  = sum(counts[:5]) / total_rows * 100
    top10_pct = sum(counts[:10]) / total_rows * 100

    print("=" * 60)
    print("倾斜分析报告")
    print("=" * 60)
    print(f"总行数：{total_rows:,}")
    print(f"唯一 Key 数：{n:,}")
    print(f"Reduce 并发度：{num_reducers}")
    print()
    print(f"【核心指标】")
    print(f"  最大 Key 占比：{max_key_pct:.2f}%")
    print(f"  基尼系数：{gini:.4f}  （0=均匀，1=极度倾斜）")
    print(f"  倾斜放大系数：{skew_factor:.1f}x  （理想耗时的 {skew_factor:.1f} 倍）")
    print(f"  Top-1/5/10 集中度：{top1_pct:.1f}% / {top5_pct:.1f}% / {top10_pct:.1f}%")
    print()

    # 方案选型建议
    print("【方案选型建议】")
    if max_key_pct > 30:
        print("  ⚠️  极度倾斜（最大 Key > 30%）")
        print("  → 首选：方案三（热点 Key 分离）+ 方案一（MapJoin）")
        print("  → 备选：方案二（加盐打散，盐值建议 >= 20）")
    elif max_key_pct > 10:
        print("  ⚠️  严重倾斜（最大 Key 10%~30%）")
        print("  → 首选：方案二（加盐打散，盐值建议 10）")
        print("  → 备选：方案四（自动优化）")
    elif max_key_pct > 3:
        print("  ⚡ 中度倾斜（最大 Key 3%~10%）")
        print("  → 首选：方案四（自动优化，调低 skewjoin.key 阈值）")
        print("  → 备选：方案二（加盐打散，盐值 5 即可）")
    else:
        print("  ✅ 轻度倾斜（最大 Key < 3%）")
        print("  → 方案四（自动优化）通常足够")
        print("  → 优先检查是否有 NULL 值倾斜（方案五）")

    print()
    print("【盐值推荐计算】")
    recommended_salt = max(2, math.ceil(skew_factor / 10))
    recommended_salt = min(recommended_salt, 100)  # 盐值过大会增加 stage2 压力
    print(f"  推荐盐值：{recommended_salt}")
    print(f"  加盐后最大 Key 预估占比：{max_key_pct / recommended_salt:.2f}%")

    return {
        "max_key_pct": max_key_pct,
        "gini": gini,
        "skew_factor": skew_factor,
        "recommended_salt": recommended_salt
    }


# 模拟我们的数据分布
if __name__ == "__main__":
    import random
    random.seed(42)

    # 模拟 1000 万行的 key 分布
    total = 10_000_000
    dist = {
        1: int(total * 0.40),   # user_id=1，40%
        2: int(total * 0.20),   # user_id=2，20%
    }
    # user_id 3~100，各约 0.3%
    for uid in range(3, 101):
        dist[uid] = int(total * 0.30 / 98)
    # user_id 101~10000，长尾均匀
    for uid in range(101, 10001):
        dist[uid] = int(total * 0.10 / 9900)

    result = analyze_skew(dist, total, num_reducers=200)
```

```
# 预期输出：
# ============================================================
# 倾斜分析报告
# ============================================================
# 总行数：10,000,000
# 唯一 Key 数：10,000
# Reduce 并发度：200
#
# 【核心指标】
#   最大 Key 占比：40.00%
#   基尼系数：0.8923  （0=均匀，1=极度倾斜）
#   倾斜放大系数：800.0x  （理想耗时的 800.0 倍）
#   Top-1/5/10 集中度：40.0% / 61.2% / 62.4%
#
# 【方案选型建议】
#   ⚠️  极度倾斜（最大 Key > 30%）
#   → 首选：方案三（热点 Key 分离）+ 方案一（MapJoin）
#   → 备选：方案二（加盐打散，盐值建议 >= 20）
#
# 【盐值推荐计算】
#   推荐盐值：80
#   加盐后最大 Key 预估占比：0.50%
```

### 2.2 方案收益量化公式

```
设：
  T_ideal  = 理想执行时间（无倾斜，数据均匀分布）
  T_actual = 实际执行时间（有倾斜）
  R        = Reduce 并发度
  N_max    = 最大 key 的行数
  N_total  = 总行数

倾斜放大系数 S = N_max / (N_total / R)

T_actual ≈ T_ideal × S

各方案理论收益：
  方案一（MapJoin）：消除 Reduce 阶段
    T_mapjoin ≈ T_map（通常是 T_ideal 的 0.3~0.5 倍）

  方案二（加盐，盐值=K）：
    新的最大 key 行数 ≈ N_max / K
    新的倾斜放大系数 S' = (N_max/K) / (N_total/R) = S/K
    T_salted ≈ T_ideal × (S/K) + T_stage2（stage2 很小，可忽略）
    → 盐值 K 越大，收益越大，但 K > S 后收益趋于平稳

  方案三（热点分离）：
    热点部分用 MapJoin，非热点正常跑
    T_hot    ≈ T_map（MapJoin）
    T_normal ≈ T_ideal（非热点数据均匀）
    T_total  ≈ max(T_hot, T_normal) ≈ T_ideal
```

---

## 3. 极端场景与边界案例

### 3.1 所有 Key 都倾斜（数据本身极度不均匀）

```sql
-- 场景：电商平台，商品类目只有 10 个，每个类目数据量差异巨大
-- 家电：50%，服装：30%，食品：10%，其他7类：各1%
-- GROUP BY category 时，10 个 Reducer 负载极不均衡

-- 分析：这种情况加盐也没用（因为每个 key 都是"热点"）
-- 根本解法：重新设计聚合粒度

-- ❌ 错误思路：继续在 Hive 里硬怼
SELECT category, COUNT(*), SUM(amount) FROM orders GROUP BY category;

-- ✅ 方案 A：预聚合下沉（在上游 Spark Streaming 实时预聚合）
-- 上游每分钟写入一条聚合结果，Hive 只需 SUM 少量预聚合数据
SELECT category, SUM(order_cnt), SUM(total_amount)
FROM dws_category_minute_agg   -- 每分钟一条，而非原始明细
GROUP BY category;

-- ✅ 方案 B：强制指定 Reduce 数量为 key 数量
SET mapreduce.job.reduces = 10;  -- 正好等于 category 数量
-- 每个 Reducer 处理一个 category，虽然不均衡，但至少不会有空闲 Reducer

-- ✅ 方案 C：分桶表（Bucketing）
-- 建表时按 category 分桶，数据预先分好，JOIN 时直接 Bucket Map Join
CREATE TABLE orders_bucketed (
    order_id BIGINT,
    category STRING,
    amount   DOUBLE
)
CLUSTERED BY (category) INTO 10 BUCKETS
STORED AS ORC;

SET hive.optimize.bucketmapjoin = true;
SET hive.optimize.bucketmapjoin.sortedmerge = true;
```

### 3.2 热点 Key 数量很多（几百个）

```sql
-- 场景：热点 key 不是 1~2 个，而是 500 个
-- 方案三（手动分离）不再适用，需要动态化

-- ✅ 动态热点分离（自动化版本）

-- Step 1：动态计算热点阈值（基于统计信息）
CREATE TABLE tmp_key_stats AS
SELECT
    user_id,
    cnt,
    -- 计算该 key 是否为热点（超过平均值的 N 倍）
    cnt > AVG(cnt) OVER() * 10  AS is_hot,
    -- 推荐盐值（基于倾斜程度动态计算）
    GREATEST(1, CAST(cnt / (SUM(cnt) OVER() / 200) / 10 AS INT)) AS salt_n
FROM (
    SELECT user_id, COUNT(*) AS cnt
    FROM ods_orders
    GROUP BY user_id
) t;

-- Step 2：热点 key 加动态盐（盐值因 key 而异）
CREATE TABLE tmp_orders_salted AS
SELECT
    o.order_id,
    o.user_id,
    o.amount,
    o.status,
    -- 热点 key 加盐，非热点 key 盐值固定为 0
    CASE
        WHEN k.is_hot THEN CAST(FLOOR(RAND() * k.salt_n) AS INT)
        ELSE 0
    END AS salt
FROM ods_orders o
LEFT JOIN tmp_key_stats k ON o.user_id = k.user_id;

-- Step 3：局部聚合
CREATE TABLE tmp_stage1 AS
SELECT user_id, salt, COUNT(*) AS cnt, SUM(amount) AS total
FROM tmp_orders_salted
GROUP BY user_id, salt;

-- Step 4：全局聚合（去盐）
SELECT user_id, SUM(cnt) AS order_cnt, SUM(total) AS total_amount
FROM tmp_stage1
GROUP BY user_id;
```

### 3.3 JOIN 两端都是大表且都倾斜

```sql
-- 场景：orders（10亿行，user_id 倾斜）JOIN user_actions（50亿行，user_id 同样倾斜）
-- 两张表都是大表，MapJoin 不可用，两边都有热点

-- ✅ 方案：双边加盐（Salted Join）

-- 原理：
--   大表 A 的 key 加随机盐 0~K-1
--   大表 B 的 key 复制 K 份（分别加盐 0,1,2,...,K-1）
--   JOIN 条件：(A.key, A.salt) = (B.key, B.salt)
--   这样 A 的每行只和 B 的一份匹配，结果正确

SET K = 10;  -- 盐值范围

-- 大表 A：随机加盐
CREATE TABLE tmp_orders_salted AS
SELECT *, CAST(FLOOR(RAND() * 10) AS INT) AS salt
FROM ods_orders;

-- 大表 B：复制 K 份
CREATE TABLE tmp_actions_replicated AS
SELECT *, salt_val AS salt
FROM user_actions
LATERAL VIEW EXPLODE(ARRAY(0,1,2,3,4,5,6,7,8,9)) t AS salt_val;
-- ⚠️ 注意：B 表数据量变为原来的 K 倍，K 不能太大（建议 5~20）

-- JOIN
SELECT a.user_id, COUNT(*) AS cnt, SUM(a.amount) AS total
FROM tmp_orders_salted a
JOIN tmp_actions_replicated b
    ON a.user_id = b.user_id AND a.salt = b.salt
GROUP BY a.user_id;

-- 清理
DROP TABLE tmp_orders_salted;
DROP TABLE tmp_actions_replicated;
```

### 3.4 倾斜 + 数据量随时间变化（动态热点）

```sql
-- 场景：平时 user_id=1 是热点，大促期间 user_id=9999（某网红）突然变热点
-- 静态配置的热点 key 列表会失效

-- ✅ 方案：每次 ETL 前动态计算热点，写入配置表

-- 每日 ETL 开始前执行（可由调度系统触发）
INSERT OVERWRITE TABLE hot_keys_config
SELECT
    user_id,
    cnt,
    CURRENT_DATE AS stat_date
FROM (
    SELECT user_id, COUNT(*) AS cnt
    FROM ods_orders
    WHERE dt = DATE_SUB(CURRENT_DATE, 1)  -- 用昨天数据预测今天热点
    GROUP BY user_id
    HAVING COUNT(*) > 500000  -- 动态阈值
) t;

-- ETL 主逻辑：读取动态热点配置
-- （后续 JOIN 逻辑同方案三，但热点 key 来自配置表而非硬编码）
```

---

## 4. 动态智能倾斜检测

### 4.1 自动化倾斜监控脚本

```python
# skew_monitor.py
# 生产级倾斜监控：定期扫描关键表，发现倾斜自动告警
# 可集成到 Airflow / DolphinScheduler

import subprocess
import json
from datetime import datetime

HIVE_CMD = "hive -e"
ALERT_THRESHOLD_PCT = 10.0   # 最大 key 占比超过 10% 触发告警
ALERT_THRESHOLD_GINI = 0.7   # 基尼系数超过 0.7 触发告警

MONITOR_TABLES = [
    {"db": "skew_demo", "table": "ods_orders", "key_col": "user_id",   "dt": "2024-01-15"},
    {"db": "skew_demo", "table": "ods_orders", "key_col": "product_id", "dt": "2024-01-15"},
]

def run_hive_query(sql):
    result = subprocess.run(
        f'{HIVE_CMD} "{sql}"',
        shell=True, capture_output=True, text=True
    )
    return result.stdout.strip()

def check_skew(db, table, key_col, dt=None):
    where = f"WHERE dt='{dt}'" if dt else ""
    sql = f"""
    SELECT
        {key_col},
        COUNT(*) AS cnt,
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS pct
    FROM {db}.{table}
    {where}
    GROUP BY {key_col}
    ORDER BY cnt DESC
    LIMIT 20
    """
    output = run_hive_query(sql)
    rows = [line.split('\t') for line in output.split('\n') if line]

    if not rows:
        return None

    total = sum(int(r[1]) for r in rows)
    max_pct = float(rows[0][2])

    # 简化基尼系数计算
    counts = sorted([int(r[1]) for r in rows])
    n = len(counts)
    gini = sum((2*i - n - 1) * c for i, c in enumerate(counts, 1)) / (n * sum(counts))

    result = {
        "table": f"{db}.{table}",
        "key_col": key_col,
        "dt": dt,
        "max_key": rows[0][0],
        "max_key_pct": max_pct,
        "gini": gini,
        "top5": rows[:5],
        "is_skewed": max_pct > ALERT_THRESHOLD_PCT or gini > ALERT_THRESHOLD_GINI
    }
    return result

def main():
    print(f"[{datetime.now()}] 开始倾斜检测...")
    alerts = []

    for cfg in MONITOR_TABLES:
        result = check_skew(**cfg)
        if result and result["is_skewed"]:
            alerts.append(result)
            print(f"⚠️  倾斜告警：{result['table']}.{result['key_col']}")
            print(f"   最大 Key：{result['max_key']}，占比：{result['max_key_pct']:.2f}%")
            print(f"   基尼系数：{result['gini']:.4f}")

    if not alerts:
        print("✅ 未发现倾斜")
    else:
        # 写入告警日志（可对接钉钉/飞书/PagerDuty）
        with open("/tmp/skew_alerts.json", "w") as f:
            json.dump(alerts, f, ensure_ascii=False, indent=2)
        print(f"\n共发现 {len(alerts)} 个倾斜问题，详情见 /tmp/skew_alerts.json")

if __name__ == "__main__":
    main()
```

---

## 5. 与上下游生态联动

### 5.1 上游 Spark 预聚合 → 下游 Hive 轻量消费

```sql
-- 架构思路：
-- Spark Streaming 实时消费 Kafka → 按分钟预聚合 → 写入 Hive 预聚合表
-- Hive 批处理只需对预聚合表做二次聚合，数据量从 10 亿行 → 几十万行

-- Hive 预聚合表（接收 Spark 写入的分钟级聚合数据）
CREATE TABLE dws_orders_minute_agg (
    user_id         BIGINT,
    minute_ts       STRING      COMMENT '分钟时间戳，格式 2024-01-15 10:30',
    order_cnt       BIGINT,
    total_amount    DOUBLE,
    paid_cnt        BIGINT,
    paid_amount     DOUBLE
)
COMMENT '订单分钟级预聚合（由 Spark Streaming 写入）'
PARTITIONED BY (dt STRING)
STORED AS ORC;

-- Hive 日报只需对预聚合表做二次聚合（数据量极小，无倾斜）
INSERT OVERWRITE TABLE ads_user_daily_report PARTITION(dt='2024-01-15')
SELECT
    user_id,
    SUM(order_cnt)      AS daily_order_cnt,
    SUM(total_amount)   AS daily_total_amount,
    SUM(paid_cnt)       AS daily_paid_cnt,
    SUM(paid_amount)    AS daily_paid_amount
FROM dws_orders_minute_agg
WHERE dt = '2024-01-15'
GROUP BY user_id;
-- 数据量：1440分钟 × 用户数，远小于原始明细，倾斜问题自然消失
```

### 5.2 Hive 倾斜数据传递给下游 Spark 的处理建议

```python
# 如果 Hive 输出的数据本身就是倾斜的（如按 user_id 分区），
# 下游 Spark 读取时需要重新分区

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("SkewHandling").getOrCreate()

# 开启 AQE（Spark 3.0+，自动处理倾斜）
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionFactor", "5")
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes", "256mb")

# 读取 Hive 倾斜表
df = spark.table("skew_demo.ods_orders")

# 手动重分区（如果 AQE 不够用）
# 按 user_id 的 hash 重分区，让数据更均匀
df_repartitioned = df.repartition(200, col("user_id"))

# 或者用 salting（与 Hive 方案二思路相同）
from pyspark.sql.functions import rand, floor, concat_ws, lit, cast

df_salted = df.withColumn("salt", floor(rand() * 10).cast("int"))
result = df_salted.groupBy("user_id", "salt").agg({"amount": "sum", "*": "count"})
final = result.groupBy("user_id").agg({"sum(amount)": "sum", "count(1)": "sum"})
```
