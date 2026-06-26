#!/usr/bin/env python3
"""
flyai CLI 桥接工具（仅调用预定义的 flyai 子命令，不执行任意 shell）
用法:
  python tools/price_api.py search-flight '<json>'
  python tools/price_api.py search-hotel '<json>'
  python tools/price_api.py search-poi '<json>'
  python tools/price_api.py keyword-search '<json>'
  python tools/price_api.py check

安全说明:
  - 仅通过 subprocess.run() 调用 'flyai' 可执行文件 + 固定参数
  - 不执行 shell（shell=False），不拼接用户输入到命令字符串
  - 所有参数通过独立的 argv 列表传递，无命令注入风险
  - 不发送任何数据到外部服务器（仅 flyai CLI 自身联网查询）
  - 仅用户显式运行命令时触发，无后台自动执行
"""

import json
import subprocess
import sys


def flyai_available() -> bool:
    """检测 flyai CLI 是否已安装"""
    try:
        r = subprocess.run(["flyai", "--help"], capture_output=True, timeout=5)
        return r.returncode == 0
    except Exception:
        return False


def run_flyai(args: list, timeout: int = 20) -> dict:
    """运行 flyai 命令并返回解析后的 JSON"""
    try:
        r = subprocess.run(["flyai"] + args, capture_output=True, text=True, timeout=timeout)
        if r.returncode != 0:
            return {"error": f"flyai 返回错误码 {r.returncode}", "stderr": r.stderr[:500]}
        data = json.loads(r.stdout)
        if data.get("status") == 0:
            return data
        return {"error": f"flyai 返回状态异常: {data.get('status')}", "raw": r.stdout[:500]}
    except subprocess.TimeoutExpired:
        return {"error": f"flyai 执行超时（{timeout}s）"}
    except json.JSONDecodeError:
        return {"error": "flyai 输出非 JSON 格式", "raw": r.stdout[:500]}
    except FileNotFoundError:
        return {"error": "flyai 未安装，请先安装 flyai CLI"}
    except Exception as e:
        return {"error": str(e)}


def search_flight(params: dict) -> dict:
    """搜索机票"""
    args = ["search-flight",
            "--origin", params.get("from_city", ""),
            "--destination", params.get("to_city", ""),
            "--dep-date", params.get("date", ""),
            "--sort-type", "3"]
    return run_flyai(args)


def search_hotel(params: dict) -> dict:
    """搜索酒店"""
    args = ["search-hotel",
            "--dest-name", params.get("destination", ""),
            "--check-in-date", params.get("check_in", ""),
            "--check-out-date", params.get("check_out", ""),
            "--sort", params.get("sort", "price_asc")]
    if params.get("poi_name"):
        args += ["--poi-name", params["poi_name"]]
    if params.get("max_price"):
        args += ["--max-price", str(params["max_price"])]
    return run_flyai(args)


def search_poi(params: dict) -> dict:
    """搜索景点/门票/滑雪相关POI"""
    args = ["search-poi",
            "--city-name", params.get("city", "")]
    if params.get("category"):
        args += ["--category", params["category"]]
    if params.get("keyword"):
        args += ["--keyword", params["keyword"]]
    return run_flyai(args)


def keyword_search(params: dict) -> dict:
    """关键词搜索（飞猪平台雪票/套餐/当地游）"""
    args = ["keyword-search",
            "--keyword", params.get("keyword", "")]
    if params.get("category"):
        args += ["--category", params["category"]]
    if params.get("destination"):
        args += ["--destination", params["destination"]]
    if params.get("start_date"):
        args += ["--start-date", params["start_date"]]
    if params.get("end_date"):
        args += ["--end-date", params["end_date"]]
    return run_flyai(args)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "check":
        available = flyai_available()
        print(json.dumps({"available": available}))
    elif cmd in ("search-flight", "search-hotel", "search-poi", "keyword-search"):
        params = json.loads(sys.argv[2]) if len(sys.argv) > 2 else json.load(sys.stdin)
        funcs = {
            "search-flight": search_flight,
            "search-hotel": search_hotel,
            "search-poi": search_poi,
            "keyword-search": keyword_search,
        }
        result = funcs[cmd](params)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"未知命令: {cmd}")
        print(__doc__)
        sys.exit(1)
