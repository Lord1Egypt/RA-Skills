# Tushare 股票数据源

从 Tushare 获取 A 股股票基础数据，支持按股票代码查询。

## 输入参数
- `ts_code` (string, 可选): 股票代码，如 "000001.SZ"
- `limit` (int, 可选): 返回数据条数，默认 1

## 输出结果
- `status`: 执行状态（success/error）
- `count`: 返回数据条数
- `data`: 股票基础数据列表