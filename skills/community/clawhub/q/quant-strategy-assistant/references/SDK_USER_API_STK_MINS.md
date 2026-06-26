# qgdata 用户接口文档（历史分钟行情 专版）

## 1. 安装与初始化

```bash
pip install qgdata
```
```python
import qgdata as qg

qg.set_token("your-token")
pro = qg.pro_api(timeout=30.0)
```

## 2. 通用调用方式（适用于所有接口）

### 2.1 统一入口 `query`

```python
df = pro.query(
    "daily",
    ts_code="000001.SZ",
    trade_date="20260217",
    fields="ts_code,trade_date,open,high,low,close",
    order_by="trade_date",
    sort="desc",
    limit=200,
    offset=0,
)
```

### 2.2 动态方法（推荐）

```python
df = pro.daily(
    ts_code="000001.SZ",
    trade_date="20260217",
    limit=200,
)
```

动态方法与 `pro.query("daily", ...)` 完全等价，方法名即 `api_name`。

### 2.3 查询可用接口

```python
apis = pro.list_apis(enabled_only=True)
print(apis)
```

## 3. 通用参数约定

- `fields`: 字段白名单，支持 `"a,b,c"` 或 `["a", "b", "c"]`
- `order_by`: 排序字段，支持单字段或多字段
- `sort`: 排序方向，`asc` / `desc`（默认 `desc`）
- `limit`: 返回条数（默认 5000，最终受服务端 `max_limit` 限制，且服务端全局最大 6000）
- `offset`: 分页偏移（默认 0）

业务过滤参数通过 `**kwargs` 直接传入，服务端按“字段=值”或“字段 IN 列表”处理：

```python
df = pro.daily(ts_code=["000001.SZ", "000002.SZ"], trade_date="20260217")
```

## 4. `stk_mins` 接口说明

- 中文说明：股票分钟级行情（分频率分表）
- 动态方法：`pro.stk_mins(...)`
- 默认时间字段：`trade_time`
- 典型过滤参数：`ts_code`（必填）、`freq`（必填）、`start_date/end_date`
- 主要字段：`ts_code`, `trade_time`, `open`, `close`

### 4.1 基础示例

```python
df = pro.stk_mins(
    ts_code="000001.SZ",
    freq="1min",
    start_date="20260217",
    fields="ts_code,trade_time,open,close",
    order_by="trade_time",
    sort="asc",
    limit=500,
)
```

### 4.2 区间示例（推荐）

```python
df = pro.stk_mins(
    ts_code="000001.SZ",
    freq="1min",
    start_date="2025-01-02",
    end_date="2025-01-02",
    fields="ts_code,trade_time,open,close",
    order_by="trade_time",
    sort="asc",
    limit=500,
)
```

### 4.3 时间范围规则（服务端）

- 建议始终传 `start_date/end_date` 控制查询范围
- `start_date/end_date` 支持 `YYYYMMDD` 或 `YYYY-MM-DD`
- 当接口时间字段为 `trade_time` 时，服务端自动补齐边界时间：
  - `start_date` -> `09:30:00`
  - `end_date` -> `15:00:00`
- 最终按 `trade_time >= start_date`、`trade_time <= end_date` 做区间过滤

## 5. 异常处理

SDK 请求失败或业务失败会抛出 `PipelineSDKError`：

```python
from qgdata import PipelineSDKError

try:
    df = pro.stk_mins(ts_code="000001.SZ", freq="1min", limit=10)
except PipelineSDKError as exc:
    print("message:", str(exc))
    print("code:", exc.code)
    print("detail:", exc.detail)
```

常见错误：
- `401 unauthorized`: token 缺失或无效
- `unknown api_name`: 接口名未注册
- `order_by field not found`: 排序字段不存在
- `invalid query response format`: 返回数据格式不符合约定

## 6. 调用建议

- 优先使用动态方法 `pro.stk_mins(...)`
- 对分钟行情优先添加 `start_date/end_date`，避免全量扫描
- 大数据量场景使用 `limit + offset` 分页拉取
- 尽量显式指定 `fields`，减少传输与 DataFrame 内存占用
