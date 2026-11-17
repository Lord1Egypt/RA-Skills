---
name: quant-data
description: A股量化数据与策略回测工具。支持实时行情、多条件选股、以及运行回测策略。当用户需要查询A股数据、筛选股票、或者运行量化回测时使用。
metadata:
  openclaw:
    emoji: "📈"
    requires:
      bins: ["python3"]
---

# 量化复盘技能 (Quant Data)

这是一个直连 A 股量化数据后端的免费工具集，支持实时行情查询、多条件选股、以及策略回测。

## ⚠️ 数据解析提示

调用 `run_backtest` 时，接口会返回极长的数组（每日净值、每日持仓、买卖点）。**为了提高效率，请直接从返回的 JSON 中提取以下核心字段展示给用户，忽略大数组**：

- `results[0].strategyReturn`（策略收益）
- `results[0].maxDrawdown`（最大回撤）
- `results[0].winRate`（胜率）
- `summary`（整体汇总）
- `results[0].trades`（具体交易记录）

## 可用指令

### 1. 运行策略回测 (run_backtest)

对指定股票运行回测策略。支持的策略类型：`MA_CROSS`、`MACD`、`RSI`、`BOLLINGER`、`KDJ`、`VOLUME_BREAKOUT`。

```bash
python3 scripts/quant_api.py run_backtest '{"codes":["600519"],"startDate":"2024-01-01","endDate":"2024-12-31","strategyTypes":["MA_CROSS"]}'
```

### 2. 查询个股实时行情 (get_stock_realtime)

获取股票的最新价、涨跌幅、换手率、市值等。

```bash
python3 scripts/quant_api.py get_stock_realtime '{"code":"600519"}'
```

### 3. 多条件选股 (filter_stocks)

根据换手率、量比、成交额等指标筛选股票。参数示例：`minTurnover`、`minVolumeRatio`、`minAmount`。

```bash
python3 scripts/quant_api.py filter_stocks '{"minTurnover":5,"minAmount":100000000}'
```

### 4. 获取个股 K 线 (get_stock_kline)

获取股票的历史日线数据。

```bash
python3 scripts/quant_api.py get_stock_kline '{"code":"600519","startDate":"2024-01-01","endDate":"2024-12-31"}'
```

## 完整脚本

`scripts/quant_api.py`：

```python
import sys
import json
import urllib.request
import urllib.error

# 你的后端 API 基础地址
BASE_URL = "https://zizhenghua.com/api"


def send_request(url, method="POST", payload=None):
    headers = {
        "Content-Type": "application/json",
        "X-Free-Skill": "true",  # 关键：放行令牌
        "User-Agent": "OpenClaw-FreeSkill/1.0"
    }

    data = json.dumps(payload).encode('utf-8') if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as response:
            raw_text = response.read().decode('utf-8')
            result = json.loads(raw_text)

            # 万能兼容解析逻辑（兼容后端各种返回格式）
            if isinstance(result, dict):
                if "success" in result:
                    if result["success"]:
                        print(json.dumps(result.get("data"), ensure_ascii=False, indent=2))
                    else:
                        print(f"API 业务错误: {result.get('message')}")
                else:
                    print(json.dumps(result, ensure_ascii=False, indent=2))
            elif isinstance(result, list):
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(result)

    except urllib.error.HTTPError as e:
        print(f"HTTP 错误: {e.code} - {e.reason}")
        try:
            err_body = e.read().decode('utf-8')
            try:
                err_json = json.loads(err_body)
                print(f"详细信息: {err_json.get('message', err_body)}")
            except json.JSONDecodeError:
                print(f"详细信息: {err_body[:500]}")
        except:
            pass
    except Exception as e:
        print(f"网络请求失败: {str(e)}")


def main():
    if len(sys.argv) < 3:
        print("用法: python quant_api.py <tool_name> '<json_args>'")
        sys.exit(1)

    tool_name = sys.argv[1]
    try:
        args = json.loads(sys.argv[2])
    except json.JSONDecodeError:
        print("错误: 参数必须是合法的 JSON 字符串")
        sys.exit(1)

    # 路由到不同的后端接口
    if tool_name == "run_backtest":
        # 自动补全后端要求的默认参数
        args.setdefault("combinationMode", "OR")
        args.setdefault("stopLoss", -5)
        args.setdefault("takeProfit", 10)
        args.setdefault("positionRatio", 1.0)
        args.setdefault("initialCapital", 1000000)
        send_request(f"{BASE_URL}/multi-backtest/run", "POST", args)

    elif tool_name == "filter_stocks":
        send_request(f"{BASE_URL}/stock/filter", "POST", args)

    elif tool_name == "get_stock_realtime":
        code = args.get("code")
        if not code:
            print("错误: 缺少 code 参数")
            sys.exit(1)
        send_request(f"{BASE_URL}/stock/realtime/{code}", "GET")

    elif tool_name == "get_stock_kline":
        code = args.get("code")
        if not code:
            print("错误: 缺少 code 参数")
            sys.exit(1)
        # 拼接 GET 参数
        params = ""
        if args.get("startDate"):
            params += f"startDate={args['startDate']}&"
        if args.get("endDate"):
            params += f"endDate={args['endDate']}&"

        url = f"{BASE_URL}/stock/detail/{code}"
        if params:
            url += f"?{params.rstrip('&')}"
        send_request(url, "GET")

    else:
        print(f"未知工具: {tool_name}")


if __name__ == "__main__":
    main()
```
