#!/usr/bin/env python3
"""
SalesClaw - rolling_refresh.py
品种滚动派生表（fct_product_rolling）刷新脚本

功能：
- 根据 fct_prescription_flow + sales_targets 计算派生字段
- 支持全量刷新（full_refresh）和增量刷新（append）
- 写入 OpenClaw 每日记忆

用法：
  python rolling_refresh.py           # 全量刷新
  python rolling_refresh.py dry_run   # 查看 SQL（不执行）
  python rolling_refresh.py incremental  # 增量刷新（仅刷新最近3个月）
"""

import sys
import json
from datetime import datetime
from pathlib import Path
from db import query_all, query_one, execute

SKILL_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_DIR / "tools"))

# ─────────────────────────────────────────
# 建表 SQL
# ─────────────────────────────────────────

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS fct_product_rolling (
    product_id              VARCHAR(50) NOT NULL,
    stat_month              DATE NOT NULL,
    monthly_volume          DECIMAL(16,2) DEFAULT 0,
    monthly_amount          DECIMAL(16,2) DEFAULT 0,
    cumulative_ytd          DECIMAL(16,2) DEFAULT 0,
    cumulative_qtd          DECIMAL(16,2) DEFAULT 0,
    vs_target_pct           DECIMAL(6,2) DEFAULT NULL,
    vs_last_year_pct        DECIMAL(6,2) DEFAULT NULL,
    vs_last_month_pct       DECIMAL(6,2) DEFAULT NULL,
    rolling_3m_avg          DECIMAL(16,2) DEFAULT NULL,
    new_patient_count       INT DEFAULT 0,
    new_patient_3m_sum       INT DEFAULT 0,
    computed_at             DATETIME DEFAULT CURRENT_TIMESTAMP,
    source_tables           JSON,
    PRIMARY KEY (product_id, stat_month)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
"""

# ─────────────────────────────────────────
# 刷新 SQL（基于源表派生）
# ─────────────────────────────────────────

REFRESH_SQL = """
-- Step 1: 月度基础指标
WITH monthly_base AS (
    SELECT
        product_id,
        STR_TO_DATE(CONCAT(prescription_month, '-01'), '%Y-%m-%d') AS stat_month,
        SUM(prescription_volume) AS monthly_volume,
        SUM(prescription_amount) AS monthly_amount,
        SUM(new_patient_count) AS new_patient_count
    FROM fct_prescription_flow
    WHERE prescription_month IS NOT NULL
      AND prescription_month >= :start_month
    GROUP BY product_id, prescription_month
),

-- Step 2: 年初至今累计
cumulative_ytd AS (
    SELECT
        m.product_id,
        m.stat_month,
        SUM(b.monthly_volume) AS cumulative_ytd,
        SUM(b.monthly_amount) AS cumulative_ytd_amt
    FROM monthly_base m
    JOIN monthly_base b
      ON b.product_id = m.product_id
     AND YEAR(b.stat_month) = YEAR(m.stat_month)
     AND b.stat_month <= m.stat_month
    GROUP BY m.product_id, m.stat_month
),

-- Step 3: 季度累计
cumulative_qtd AS (
    SELECT
        m.product_id,
        m.stat_month,
        SUM(b.monthly_volume) AS cumulative_qtd,
        SUM(b.monthly_amount) AS cumulative_qtd_amt
    FROM monthly_base m
    JOIN monthly_base b
      ON b.product_id = m.product_id
     AND QUARTER(b.stat_month) = QUARTER(m.stat_month)
     AND YEAR(b.stat_month) = YEAR(m.stat_month)
     AND b.stat_month <= m.stat_month
    GROUP BY m.product_id, m.stat_month
),

-- Step 4: 环比（上月）
mom AS (
    SELECT
        m.product_id,
        m.stat_month,
        m.monthly_volume,
        LAG(b.monthly_volume) OVER w AS prev_vol,
        (m.monthly_volume - LAG(b.monthly_volume) OVER w)
         / NULLIF(LAG(b.monthly_volume) OVER w, 0) * 100 AS vs_last_month_pct
    FROM monthly_base m
    WINDOW w AS (PARTITION BY m.product_id ORDER BY m.stat_month)
),

-- Step 5: 同比（去年同月）
yoy AS (
    SELECT
        m.product_id,
        m.stat_month,
        LAG(y.monthly_volume) OVER (PARTITION BY m.product_id
                                      ORDER BY m.stat_month) AS last_year_vol
    FROM monthly_base m
),

-- Step 6: 目标达成率（需 join sales_targets）
targets AS (
    SELECT
        t.rep_id,
        t.product_id,
        t.period_value,
        SUM(t.target_value) AS total_target
    FROM sales_targets t
    WHERE t.product_id IS NOT NULL
    GROUP BY t.rep_id, t.product_id, t.period_value
),

-- Step 7: 滚动3月均值
rolling3m AS (
    SELECT
        product_id,
        stat_month,
        AVG(monthly_volume) OVER w AS rolling_3m_avg
    FROM monthly_base
    WINDOW w AS (PARTITION BY product_id ORDER BY stat_month
                ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)
)

-- 最终输出
SELECT
    m.product_id,
    m.stat_month,
    m.monthly_volume,
    m.monthly_amount,
    COALESCE(ytd.cumulative_ytd, m.monthly_volume) AS cumulative_ytd,
    COALESCE(qtd.cumulative_qtd, m.monthly_volume) AS cumulative_qtd,
    ROUND((m.monthly_volume - LAG(y.last_year_vol) OVER w) / NULLIF(LAG(y.last_year_vol) OVER w, 0) * 100, 2)
        AS vs_last_year_pct,
    ROUND(mom.vs_last_month_pct, 2) AS vs_last_month_pct,
    r3m.rolling_3m_avg,
    m.new_patient_count,
    COALESCE(SUM(m.new_patient_count) OVER w_3m, 0) AS new_patient_3m_sum,
    CASE WHEN tgt.total_target > 0
         THEN ROUND(m.monthly_amount / tgt.total_target * 100, 2)
         ELSE NULL
    END AS vs_target_pct,
    NOW() AS computed_at,
    '["fct_prescription_flow","sales_targets"]' AS source_tables
FROM monthly_base m
LEFT JOIN cumulative_ytd ytd ON ytd.product_id = m.product_id AND ytd.stat_month = m.stat_month
LEFT JOIN cumulative_qtd qtd ON qtd.product_id = m.product_id AND qtd.stat_month = m.stat_month
LEFT JOIN mom ON mom.product_id = m.product_id AND mom.stat_month = m.stat_month
LEFT JOIN yoy y ON y.product_id = m.product_id AND y.stat_month = m.stat_month
LEFT JOIN rolling3m r3m ON r3m.product_id = m.product_id AND r3m.stat_month = m.stat_month
LEFT JOIN targets tgt ON tgt.product_id = m.product_id
WINDOW w AS (PARTITION BY m.product_id ORDER BY m.stat_month),
       w_3m AS (PARTITION BY m.product_id ORDER BY m.stat_month
               ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)
ORDER BY m.product_id, m.stat_month
"""


def create_table():
    """建表（如果不存在）"""
    result = execute(CREATE_TABLE_SQL)
    if isinstance(result, dict) and "error" in result:
        print(f"建表失败: {result['error']}")
        return False
    print("✅ fct_product_rolling 表已就绪")
    return True


def get_data(start_month: str = "2020-01") -> list:
    """从源表查询派生数据"""
    params = {"start_month": start_month}
    rows = query_all(REFRESH_SQL, params)
    if isinstance(rows, dict) and "error" in rows:
        print(f"查询失败: {rows['error']}")
        return []
    return rows


def upsert_rows(rows: list) -> dict:
    """UPSERT 批量写入 fct_product_rolling"""
    if not rows:
        return {"ok": True, "inserted": 0}

    inserted = 0
    errors = 0
    for row in rows:
        sql = """
            INSERT INTO fct_product_rolling (
                product_id, stat_month, monthly_volume, monthly_amount,
                cumulative_ytd, cumulative_qtd,
                vs_last_year_pct, vs_last_month_pct,
                rolling_3m_avg, new_patient_count, new_patient_3m_sum,
                vs_target_pct, computed_at, source_tables
            ) VALUES (
                %(product_id)s, %(stat_month)s, %(monthly_volume)s, %(monthly_amount)s,
                %(cumulative_ytd)s, %(cumulative_qtd)s,
                %(vs_last_year_pct)s, %(vs_last_month_pct)s,
                %(rolling_3m_avg)s, %(new_patient_count)s, %(new_patient_3m_sum)s,
                %(vs_target_pct)s, %(computed_at)s, %(source_tables)s
            )
            ON DUPLICATE KEY UPDATE
                monthly_volume   = VALUES(monthly_volume),
                monthly_amount   = VALUES(monthly_amount),
                cumulative_ytd   = VALUES(cumulative_ytd),
                cumulative_qtd   = VALUES(cumulative_qtd),
                vs_last_year_pct = VALUES(vs_last_year_pct),
                vs_last_month_pct = VALUES(vs_last_month_pct),
                rolling_3m_avg  = VALUES(rolling_3m_avg),
                new_patient_count = VALUES(new_patient_count),
                new_patient_3m_sum = VALUES(new_patient_3m_sum),
                vs_target_pct    = VALUES(vs_target_pct),
                computed_at      = VALUES(computed_at),
                source_tables    = VALUES(source_tables)
        """
        result = execute(sql, row)
        if isinstance(result, dict) and "error" in result:
            errors += 1
        else:
            inserted += 1

    return {"ok": errors == 0, "inserted": inserted, "errors": errors}


def full_refresh():
    """全量刷新"""
    print("开始全量刷新 fct_product_rolling...")
    rows = get_data("2020-01")
    if not rows:
        print("无数据或查询失败")
        return
    result = upsert_rows(rows)
    print(f"全量刷新完成：插入/更新 {result['inserted']} 条，错误 {result['errors']} 条")
    return result


def incremental_refresh():
    """增量刷新（最近6个月）"""
    print("开始增量刷新 fct_product_rolling（最近6个月）...")
    from datetime import date
    from dateutil.relativedelta import relativedelta
    cutoff = (date.today() - relativedelta(months=6)).strftime("%Y-%m")
    rows = get_data(cutoff)
    if not rows:
        print("无数据或查询失败")
        return
    result = upsert_rows(rows)
    print(f"增量刷新完成：处理 {result['inserted']} 条，错误 {result['errors']} 条")
    return result


def log_to_memory(count: int, mode: str):
    """写入 OpenClaw 每日记忆"""
    today = datetime.now().strftime("%Y-%m-%d")
    entry = f"""## fct_product_rolling 刷新 [{today}]

- 模式：{mode}
- 刷新记录数：{count}
- 时间：{datetime.now().isoformat()}
"""
    try:
        memory_file = Path(f"~/.openclaw/workspace/memory/{today}.md")
        memory_file.parent.mkdir(parents=True, exist_ok=True)
        with open(memory_file, "a") as f:
            f.write(f"\n{entry}")
        print(f"已写入记忆：{memory_file}")
    except Exception as e:
        print(f"记忆写入失败（不阻断）：{e}")


def dry_run():
    """查看刷新 SQL（不执行）"""
    print("=" * 60)
    print("Dry Run：fct_product_rolling 刷新 SQL")
    print("=" * 60)
    print(REFRESH_SQL[:2000])
    print("\n... (truncated)")
    print(f"\n建表 SQL：{CREATE_TABLE_SQL.strip()[:200]}")


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "full"

    if action == "dry_run":
        dry_run()
    elif action == "create":
        create_table()
    elif action == "incremental":
        create_table()
        result = incremental_refresh()
        if result and result.get("inserted", 0) > 0:
            log_to_memory(result["inserted"], "incremental")
    elif action == "full":
        create_table()
        result = full_refresh()
        if result and result.get("inserted", 0) > 0:
            log_to_memory(result["inserted"], "full")
    else:
        print(f"用法：python rolling_refresh.py [full|dry_run|incremental|create]")
        print("  full         - 全量刷新（从2020-01开始）")
        print("  incremental  - 增量刷新（最近6个月，推荐日常使用）")
        print("  dry_run      - 查看SQL不执行")
        print("  create       - 仅建表")