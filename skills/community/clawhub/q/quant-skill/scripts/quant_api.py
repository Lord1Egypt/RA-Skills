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

            # 🆕 万能兼容解析逻辑
            if isinstance(result, dict):
                # 情况 1：标准的 {success, message, data} 结构
                if "success" in result:
                    if result["success"]:
                        print(json.dumps(result.get("data"), ensure_ascii=False, indent=2))
                    else:
                        print(f"API 业务错误: {result.get('message')}")
                # 情况 2：没有 success 字段，直接返回了业务数据字典（如回测、实时行情）
                else:
                    print(json.dumps(result, ensure_ascii=False, indent=2))

            # 情况 3：直接返回了数组（如选股列表）
            elif isinstance(result, list):
                print(json.dumps(result, ensure_ascii=False, indent=2))

            # 其他类型
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
        # 🆕 自动补全后端要求的默认参数，防止 400 报错
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
        # GET 请求如果要带参数，需要拼在 URL 后面
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