---
name: tickflow-realtime
description: 使用 TickFlow 数据中心查询实时行情和日K数据。适用于用户想查单个或多个标的的最新价格、涨跌幅、成交量、交易时段，或查询单标的/多标的的日K、最近N根K线、复权K线时。
---

# TickFlow 实时行情与日K

这个 skill 用 TickFlow HTTP API 查询两类数据：

- 实时行情：最新价、涨跌幅、成交量、交易时段
- K 线数据：默认日 K，也可按周期查询最近 N 根 K 线

## 何时使用

在这些场景触发：

- 用户要查某只股票、ETF、美股、港股的最新行情
- 用户要批量比较多个代码的实时价格或涨跌幅
- 用户要查某个标的池 `universes` 的实时行情
- 用户要查某个代码的日 K、周 K、月 K
- 用户要查多只标的最近一根或最近几根 K 线

## 工作流

1. 判断用户是要实时行情还是 K 线。
2. 从环境变量 `TICKFLOW_API_KEY` 读取 API Key。
3. 实时行情优先使用 `GET /v1/quotes`；标的较多时可以切到 `POST /v1/quotes`。
4. K 线单标的使用 `GET /v1/klines`；多标的使用 `GET /v1/klines/batch`。
5. 校验响应结构。
6. 返回简洁摘要；如果用户明确要原始数据，再返回 JSON。

## API Key

- 统一从环境变量 `TICKFLOW_API_KEY` 读取
- 不要把 API Key 写入文件、日志或输出内容。

## 脚本

- 实时行情脚本：`scripts/query_quotes.py`
- K 线脚本：`scripts/query_klines.py`
- 共享工具：`scripts/tickflow_common.py`

## 参考文档

- API 结构与字段说明：`references/api.md`
- 对外输出约定：`references/output-contract.md`

## 使用约定

- 百分比字段需要按 TickFlow 语义换算：`0.01 -> 1%`
- `timestamp` 是毫秒时间戳
- `region` 枚举目前是 `CN | US | HK`
- `session` 枚举见 `references/api.md`
- K 线接口返回紧凑列式结构；做摘要或表格前先解压

## 示例

查询单个标的实时行情：

```bash
python3 scripts/query_quotes.py --symbols 600519.SH --format summary
```

批量查询多个代码实时行情：

```bash
python3 scripts/query_quotes.py --symbols 600519.SH,000001.SZ,AAPL.US --format table
```

查询单个标的日 K：

```bash
python3 scripts/query_klines.py --symbol 600519.SH --period 1d --count 20 --format table
```

查询多个标的最近一根日 K：

```bash
python3 scripts/query_klines.py --symbols 600519.SH,000001.SZ --period 1d --count 1 --format summary
```
