# Chanquant Templates

## 1) Latest recommendations by signal type

```sql
SELECT
  code,
  name,
  signal_type,
  signal_label,
  created_at
FROM stock_recommendations
WHERE created_at >= CURRENT_DATE - INTERVAL 14 DAY
ORDER BY created_at DESC
LIMIT 200;
```

## 2) "Potential first-buy candidates" from older third-sell

```sql
SELECT
  code,
  name,
  MAX(created_at) AS last_signal_at,
  DATEDIFF(CURRENT_DATE, MAX(created_at)) AS days_since_signal
FROM stock_recommendations
WHERE signal_label = '三卖'
GROUP BY code, name
HAVING days_since_signal >= 20
ORDER BY days_since_signal DESC
LIMIT 100;
```

## 3) Daily signal distribution trend

```sql
SELECT
  DATE(created_at) AS d,
  SUM(CASE WHEN signal_label LIKE '%买%' THEN 1 ELSE 0 END) AS buy_count,
  SUM(CASE WHEN signal_label LIKE '%卖%' THEN 1 ELSE 0 END) AS sell_count
FROM stock_recommendations
WHERE created_at >= CURRENT_DATE - INTERVAL 60 DAY
GROUP BY DATE(created_at)
ORDER BY d;
```

## 4) Codes with repeated recommendations in short window

```sql
SELECT
  code,
  COUNT(*) AS rec_count,
  MIN(created_at) AS first_seen,
  MAX(created_at) AS last_seen
FROM stock_recommendations
WHERE created_at >= CURRENT_DATE - INTERVAL 7 DAY
GROUP BY code
HAVING COUNT(*) >= 3
ORDER BY rec_count DESC, last_seen DESC;
```

## 5) Data quality check for daily kline

```sql
SELECT
  code,
  COUNT(*) AS bars,
  SUM(CASE WHEN close <= 0 THEN 1 ELSE 0 END) AS invalid_close,
  MIN(trade_date) AS first_date,
  MAX(trade_date) AS last_date
FROM daily_kline
GROUP BY code
HAVING invalid_close > 0
ORDER BY invalid_close DESC, code
LIMIT 100;
```
