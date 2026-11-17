#!/usr/bin/env python3
"""
TianAPI Vehicle Limit Fetcher
-----------------------------
查询全国各城市的车辆限行信息，包括尾号限行规则、限行区域、时间及处罚标准。
零外部依赖，仅使用 Python 标准库。

Usage:
    # 根据城市名称查询
    python3 fetch_vehiclelimit.py --key YOUR_KEY --city 北京

    # 根据城市代码查询
    python3 fetch_vehiclelimit.py --key YOUR_KEY --code 110100

Env Config:
    export TIANAPI_VEHICLELIMIT_KEY=your_api_key
    # 或在脚本同级目录创建 .env 文件: TIANAPI_VEHICLELIMIT_KEY=your_api_key
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
API_ENDPOINT = "https://apis.tianapi.com/vehiclelimit/index"
ENV_KEY_NAME = "TIANAPI_VEHICLELIMIT_KEY"
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
        print(f"💡 提示: 申请 Key -> https://www.tianapi.com/apiview/246", file=sys.stderr)
        sys.exit(1)


class TianAPIClient:
    """天行数据 API 客户端"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_vehiclelimit(self, city: Optional[str] = None, code: Optional[str] = None) -> Dict[str, Any]:
        """
        执行 API 请求
        返回标准化结构: {"success": bool, "data": dict, "error": str|None}
        """
        params = {"key": self.api_key}
        
        # 动态添加查询参数 (city 和 code 二选一)
        if city: params["city"] = city.strip()
        if code: params["code"] = code.strip()

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

        # 业务层校验：检查返回的 JSON 中 code 是否为 200
        if raw_data.get("code") != 200:
            return {
                "success": False, 
                "data": {}, 
                "error": raw_data.get("msg", "未知业务错误"),
                "code": raw_data.get("code")
            }

        # 成功则提取 result
        return {
            "success": True,
            "data": raw_data.get("result", {})
        }


def main():
    parser = argparse.ArgumentParser(description="TianAPI Vehicle Limit Fetcher")
    parser.add_argument("--key", help="API Key (可选，优先使用环境变量)")
    parser.add_argument("--city", help="城市名称 (如: 北京)")
    parser.add_argument("--code", help="城市代码 (如: 110100)")
    args = parser.parse_args()

    # 参数校验：city 和 code 至少提供一个
    if not args.city and not args.code:
        parser.error("请至少提供 --city 或 --code 参数中的一个。")

    # 1. 初始化
    config = Config(args.key)
    client = TianAPIClient(config.api_key)

    # 2. 请求
    result = client.fetch_vehiclelimit(city=args.city, code=args.code)

    # 3. 默认输出 JSON
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()