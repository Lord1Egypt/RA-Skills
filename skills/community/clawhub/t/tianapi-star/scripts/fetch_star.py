#!/usr/bin/env python3
"""
TianAPI Star Sign Fortune Fetcher
--------------------------------
查询十二星座每日运势，包含爱情、工作、幸运色等指数。
零外部依赖，仅使用 Python 标准库。

Usage:
    python3 fetch_star.py --key YOUR_KEY --astro 狮子座
    python3 fetch_star.py --key YOUR_KEY --astro taurus --date 2024-01-01

Env Config:
    export TIANAPI_STAR_KEY=your_api_key
    # 或在脚本同级目录创建 .env 文件: TIANAPI_STAR_KEY=your_api_key
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
API_ENDPOINT = "https://apis.tianapi.com/star/index"
ENV_KEY_NAME = "TIANAPI_STAR_KEY"
DEFAULT_TIMEOUT = 10


class Config:
    """配置加载器：支持 命令行 > 环境变量 > .env 文件 三级优先级"""

    def __init__(self, cli_key: Optional[str] = None):
        self.api_key = self._resolve_key(cli_key)
        if not self.api_key:
            self._exit_with_help("未找到 API Key，请通过 --key 参数、环境变量或 .env 文件配置。")

    def _resolve_key(self, cli_key: Optional[str]) -> str:
        if cli_key:
            return cli_key.strip()

        # 1. 环境变量
        env_val = os.environ.get(ENV_KEY_NAME, "").strip()
        if env_val:
            return env_val

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
        print(f"💡 提示: 申请 Key -> https://www.tianapi.com/apiview/78", file=sys.stderr)
        sys.exit(1)


class TianAPIClient:
    """天行数据 API 客户端"""

    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_fortune(self, astro: str, date: Optional[str] = None) -> Dict[str, Any]:
        """
        执行 API 请求
        返回标准化结构: {"success": bool, "data": list|str, "error": str|None}
        """
        params = {
            "key": self.api_key,
            "astro": astro
        }
        if date:
            params["date"] = date

        query_string = urllib.parse.urlencode(params)
        url = f"{API_ENDPOINT}?{query_string}"

        try:
            req = urllib.request.Request(url, headers={"User-Agent": "OpenClaw-Skill/1.0"})
            with urllib.request.urlopen(req, timeout=DEFAULT_TIMEOUT) as resp:
                raw_data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            return {"success": False, "data": "", "error": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            return {"success": False, "data": "", "error": f"网络异常: {str(e)}"}

        # 业务层校验
        if raw_data.get("code") != 200:
            return {
                "success": False,
                "data": "",
                "error": raw_data.get("msg", "未知业务错误"),
                "code": raw_data.get("code")
            }

        # 成功则提取运势列表
        return {
            "success": True,
            "data": raw_data.get("result", {}).get("list", [])
        }


def main():
    parser = argparse.ArgumentParser(description="TianAPI Star Sign Fortune Fetcher")
    parser.add_argument("--key", help="API Key (可选，优先使用环境变量)")
    parser.add_argument("--astro", required=True, help="星座中文名或英文名 (如: 狮子座, leo)")
    parser.add_argument("--date", help="查询日期 (格式: YYYY-MM-DD, 默认为当天)")
    args = parser.parse_args()

    # 1. 初始化
    config = Config(args.key)
    client = TianAPIClient(config.api_key)

    # 2. 请求
    result = client.fetch_fortune(args.astro, args.date)

    # 3. 默认输出 JSON
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()