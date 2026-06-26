# TDengine 表结构

## 超级表 (STABLES)
- **bar88_day**: 主力合约日线（仅日线）
- **bar_min/bar_min5/.../bar_day**: 具体合约K线模板
- **tick**: Tick数据模板

## 具体表命名规则
- **主力日线**: `bar88_day` (固定表名)
- **具体合约**: `{symbol}_{period}`  
  - 示例: `rb05_min`, `m09_tick`
- **查询方式**:  
  ```sql
  -- 通过超级表查询
  SELECT * FROM bar_min WHERE symbol='rb05' AND exchange='SHFE'
  
  -- 直接查子表
  SELECT * FROM rb05_min
  ```

## 字段说明
- **K线表**: ts, open, high, low, close, volume, open_interest, trading_day
- **Tick表**: ts, last_price, bid/ask 五档, volume, open_interest
- **TAG字段**: symbol, exchange (用于高效过滤)