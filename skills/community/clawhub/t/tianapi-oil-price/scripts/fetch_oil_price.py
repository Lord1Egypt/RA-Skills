#!/usr/bin/env python3
"""
TianAPI Oil Price Fetcher
-------------------------
查询全国各省份最新汽油及柴油价格。
零外部依赖，仅使用 Python 标准库。

Usage:
    # 查询指定省份油价
    python3 fetch_oil_price.py --key YOUR_KEY --prov 湖北

    # JSON模式 (适合 Agent 调用)
    python3 fetch_oil_price.py --key YOUR_KEY --prov 上海 --json

Env Config:
    export TIANAPI_OIL_PRICE_KEY=your_api_key
    # 或在脚本同级目录创建 .env 文件: TIANAPI_OIL_PRICE_KEY=your_api_key
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from typing import Optional, Dict, Any

# --- 配置常量 ---
API_ENDPOINT = "https://apis.tianapi.com/oilprice/index"
ENV_KEY_NAME = "TIANAPI_OIL_PRICE_KEY"
DEFAULT_TIMEOUT = 10


class Config:
    """配置加载器：支持 命令行 > 环境变量 > .env 文件 三级优先级"""
    
    def __init__(self, cli_key: Optional[str] = None):
        self.api_key = self._resolve_key(cli_key)
        if not self.api_key:
            self._exit_with_help("未找到 API Key，请通过 --key 参数、环境变量或 .env 文件配置。")

    def _resolve_key(self, cli_key: Optional[str]) -> str:
        if cli_key: return cli_key.strip()
        
        # 1. 环境变量
        env_val = os.environ.get(ENV_KEY_NAME, "").strip()
        if env_val: return env_val
        
        # 2. .env 文件
        env_file = Path(__file__).parent / ".env"
        if env_file.exists():
            try:
                content = env_file.read_text(encoding="utf-8")
                for line in content.splitlines():
                    line = line.strip()
                    if line.startswith(f"{ENV_KEY_NAME}="):
                        return line.split("=", 1)[1].strip().strip('"\'')
            except Exception:
                pass
        return ""

    def _exit_with_help(self, msg: str):
        print(f"❌ 配置错误: {msg}", file=sys.stderr)
        print(f"💡 提示: 申请 Key -> https://www.tianapi.com/apiview/104", file=sys.stderr)
        sys.exit(1)


class TianAPIClient:
    """天行数据 API 客户端"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_oil_price(self, province: str) -> Dict[str, Any]:
        """
        执行 API 请求
        返回标准化结构: {"success": bool, "data": dict, "error": str|None}
        """
        params = {
            "key": self.api_key,
            "prov": province.strip()
        }
        query_string = urllib.parse.urlencode(params)
        url = f"{API_ENDPOINT}?{query_string}"

        try:
            req = urllib.request.Request(url, headers={"User-Agent": "OpenClaw-Skill/1.0"})
            with urllib.request.urlopen(req, timeout=DEFAULT_TIMEOUT) as resp:
                raw_data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            return {"success": False, "data": {}, "error": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            return {"success": False, "data": {}, "error": f"网络异常: {str(e)}"}

        # 业务层校验
        if raw_data.get("code") != 200:
            return {
                "success": False, 
                "data": {}, 
                "error": raw_data.get("msg", "未知业务错误"),
                "code": raw_data.get("code")
            }

        return {
            "success": True,
            "data": raw_data.get("result", {})
        }


class ConsoleRenderer:
    """终端渲染器：负责把数据变成人话"""
    
    @staticmethod
    def render(result: Dict[str, Any]):
        if not result["success"]:
            print(f"❌ 请求失败: {result['error']}")
            return

        data = result["data"]
        if not data:
            print("📭 未查询到相关油价数据。")
            return

        prov = data.get("prov", "未知省份")
        time = data.get("time", "")
        
        print(f"\n⛽ {prov}最新油价 (更新时间: {time})\n{'-'*40}")
        print(f"89号汽油: {data.get('p89', 'N/A')} 元/升")
        print(f"92号汽油: {data.get('p92', 'N/A')} 元/升")
        print(f"95号汽油: {data.get('p95', 'N/A')} 元/升")
        print(f"98号汽油: {data.get('p98', 'N/A')} 元/升")
        print(f"0号柴油:  {data.get('p0', 'N/A')} 元/升")
        print("-" * 40)


def main():
    parser = argparse.ArgumentParser(description="TianAPI Oil Price Fetcher")
    parser.add_argument("--key", help="API Key (可选，优先使用环境变量)")
    parser.add_argument("--prov", required=True, help="省份名称 (如: 湖北, 上海)")
    args = parser.parse_args()

    # 1. 初始化
    config = Config(args.key)
    client = TianAPIClient(config.api_key)

    # 2. 请求
    result = client.fetch_oil_price(province=args.prov)

    # 3. 输出
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        ConsoleRenderer.render(result)


if __name__ == "__main__":
    main()