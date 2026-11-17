#!/usr/bin/env python3
"""
TianAPI Gold Price Fetcher
--------------------------
查询黄金、白银等贵金属的实时行情，包括买入卖出价、最高最低价及涨跌幅等数据。
零外部依赖，仅使用 Python 标准库。

Usage:
    # 查询指定种类的贵金属行情
    python3 fetch_gold-price.py --key YOUR_KEY --kinds au9999

    # 查询多个品种
    python3 fetch_gold-price.py --key YOUR_KEY --kinds au9999,agTplusD

Env Config:
    export TIANAPI_GOLD_KEY=your_api_key
    # 或在脚本同级目录创建 .env 文件: TIANAPI_GOLD_KEY=your_api_key
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
API_ENDPOINT = "https://apis.tianapi.com/gold/index"
ENV_KEY_NAME = "TIANAPI_GOLD_KEY"
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
        print(f"💡 提示: 申请 Key -> https://www.tianapi.com/apiview/146", file=sys.stderr)
        sys.exit(1)


class TianAPIClient:
    """天行数据 API 客户端"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_gold(self, kinds: str) -> Dict[str, Any]:
        """
        执行 API 请求
        返回标准化结构: {"success": bool, "data": list, "error": str|None}
        """
        params = {
            "key": self.api_key,
            "kinds": kinds.strip()
        }
        query_string = urllib.parse.urlencode(params)
        url = f"{API_ENDPOINT}?{query_string}"

        try:
            req = urllib.request.Request(url, headers={"User-Agent": "OpenClaw-Skill/1.0"})
            with urllib.request.urlopen(req, timeout=DEFAULT_TIMEOUT) as resp:
                raw_data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            return {"success": False, "data": [], "error": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            return {"success": False, "data": [], "error": f"网络异常: {str(e)}"}

        # 业务层校验：检查返回的 JSON 中 code 是否为 200
        if raw_data.get("code") != 200:
            return {
                "success": False, 
                "data": [], 
                "error": raw_data.get("msg", "未知业务错误"),
                "code": raw_data.get("code")
            }

        # 成功则提取 result 中的 list
        return {
            "success": True,
            "data": raw_data.get("result", {}).get("list", [])
        }


def main():
    parser = argparse.ArgumentParser(description="TianAPI Gold Price Fetcher")
    parser.add_argument("--key", help="API Key (可选，优先使用环境变量)")
    parser.add_argument("--kinds", required=True, help="贵金属种类代码，多个用逗号分隔 (如: au9999,agTplusD)")
    args = parser.parse_args()

    # 1. 初始化
    config = Config(args.key)
    client = TianAPIClient(config.api_key)

    # 2. 请求
    result = client.fetch_gold(kinds=args.kinds)

    # 3. 默认输出 JSON
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()