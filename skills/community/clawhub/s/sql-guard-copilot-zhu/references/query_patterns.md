# Query Patterns

Engine note:
- MySQL/PostgreSQL support `INTERVAL` syntax (with minor dialect differences).
- SQLite usually needs `date('now', '-30 day')` style expressions.

## 1) Time Window Aggregation

```sql
SELECT
  DATE(trade_date) AS d,
  COUNT(*) AS rows_cnt,
  SUM(amount) AS amount_sum
FROM daily_kline
WHERE trade_date >= CURRENT_DATE - INTERVAL 30 DAY
GROUP BY DATE(trade_date)
ORDER BY d;
```

## 2) Top-N by Metric

```sql
SELECT
  code,
  MAX(close) AS max_close
FROM daily_kline
WHERE trade_date >= '2026-01-01'
GROUP BY code
ORDER BY max_close DESC
LIMIT 20;
```

## 3) Deduplicate Latest Record (Window Function)

```sql
WITH ranked AS (
  SELECT
    code,
    trade_date,
    close,
    ROW_NUMBER() OVER (PARTITION BY code ORDER BY trade_date DESC) AS rn
  FROM daily_kline
)
SELECT code, trade_date, close
FROM ranked
WHERE rn = 1;
```

## 4) Conditional Funnel Counts

```sql
SELECT
  COUNT(*) AS total,
  SUM(CASE WHEN signal = 'BUY' THEN 1 ELSE 0 END) AS buy_cnt,
  SUM(CASE WHEN signal = 'SELL' THEN 1 ELSE 0 END) AS sell_cnt
FROM stock_recommendations
WHERE created_at >= '2026-03-01';
```

## 5) Data Quality Check

```sql
SELECT
  COUNT(*) AS total_rows,
  SUM(CASE WHEN code IS NULL OR code = '' THEN 1 ELSE 0 END) AS missing_code,
  SUM(CASE WHEN trade_date IS NULL THEN 1 ELSE 0 END) AS missing_trade_date
FROM daily_kline;
```

## 6) Duplicate Key Detection

```sql
SELECT
  code,
  trade_date,
  COUNT(*) AS dup_cnt
FROM daily_kline
GROUP BY code, trade_date
HAVING COUNT(*) > 1
ORDER BY dup_cnt DESC, trade_date DESC;
```
