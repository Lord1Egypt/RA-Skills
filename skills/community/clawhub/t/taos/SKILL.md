# TDengine Database Skill

## Connection

```bash
# CLI
taos -h localhost -u root -p taosdata

# Python
pip install taospy
```

## Schema

- **超级表**: bar88_day (主力日线), bar_min/bar_min5/.../bar_day (K线模板), tick (Tick模板)
- **具体表**: `{symbol}_{period}` (如 `rb05_min`, `m09_tick`)
- **TAG字段**: symbol, exchange

## Common Queries

```sql
-- 主力合约日线
SELECT * FROM bar88_day WHERE symbol='IF' ORDER BY ts DESC LIMIT 100;

-- 具体合约K线
SELECT * FROM bar_min WHERE symbol='rb05' AND exchange='SHFE' ORDER BY ts DESC LIMIT 100;

-- 最新tick
SELECT * FROM tick WHERE symbol='IF' AND exchange='CFFEX' ORDER BY ts DESC LIMIT 1;
```
