#!/usr/bin/env python3
"""
TianAPI AI News Fetcher
-----------------------
获取人工智能、大模型、算法领域的前沿资讯。
零外部依赖，仅使用 Python 标准库。

Usage:
    # 基础查询
    python fetch_ai_news.py --key YOUR_KEY --num 5

    # 关键词搜索 + JSON输出 (适合 Agent)
    python fetch_ai_news.py --key YOUR_KEY --word "Sora" --json

    # 翻页
    python fetch_ai_news.py --key YOUR_KEY --page 2

Env Config:
    export TIANAPI_AI_KEY=your_api_key
    # 或在脚本同级目录创建 .env 文件: TIANAPI_AI_KEY=your_api_key
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional, Dict, Any, List

# --- 配置常量 ---
API_ENDPOINT = "https://apis.tianapi.com/ai/index"
ENV_KEY_NAME = "TIANAPI_AI_KEY"
DEFAULT_TIMEOUT = 10
MAX_NEWS_LIMIT = 50


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
        print(f"💡 提示: 申请 Key -> https://www.tianapi.com/apiview/22", file=sys.stderr)
        sys.exit(1)


class TianAPIClient:
    """天行数据 API 客户端"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_news(self, num: int = 10, page: int = 1, word: Optional[str] = None) -> Dict[str, Any]:
        """
        执行 API 请求
        返回标准化结构: {"success": bool, "data": list, "error": str|None}
        """
        params = {
            "key": self.api_key,
            "num": min(max(1, num), MAX_NEWS_LIMIT),
            "page": max(1, page),
        }
        if word:
            params["word"] = word.strip()

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

        # 业务层校验
        if raw_data.get("code") != 200:
            return {
                "success": False, 
                "data": [], 
                "error": raw_data.get("msg", "未知业务错误"),
                "code": raw_data.get("code")
            }

        return {
            "success": True,
            "data": raw_data.get("result", {}).get("list", []),
            "total": raw_data.get("result", {}).get("allnum", 0)
        }


class ConsoleRenderer:
    """终端渲染器：负责把数据变成人话"""
    
    @staticmethod
    def render(result: Dict[str, Any], keyword: Optional[str] = None):
        if not result["success"]:
            print(f"❌ 请求失败: {result['error']}")
            return

        items = result["data"]
        if not items:
            print("📭 暂无匹配的 AI 资讯。")
            return

        header = f"🤖 AI 资讯速报"
        if keyword: header += f" (关键词: {keyword})"
        header += f" | 共 {len(items)} 条"
        
        print(f"\n{header}\n{'-'*40}")
        for idx, item in enumerate(items, 1):
            title = item.get("title", "无标题")
            source = item.get("source", "未知来源")
            ctime = item.get("ctime", "")[:16]  # 截取到分钟
            url = item.get("url", "#")
            
            print(f"{idx}. {title}")
            print(f"   📅 {ctime} | 🏢 {source}")
            print(f"   🔗 {url}\n")


def main():
    parser = argparse.ArgumentParser(description="TianAPI AI News Fetcher")
    parser.add_argument("--key", help="API Key (可选，优先使用环境变量)")
    parser.add_argument("--num", type=int, default=10, help="返回条数 (1-50)")
    parser.add_argument("--page", type=int, default=1, help="页码")
    parser.add_argument("--word", help="搜索关键词")
    args = parser.parse_args()

    # 1. 初始化
    config = Config(args.key)
    client = TianAPIClient(config.api_key)

    # 2. 请求
    result = client.fetch_news(num=args.num, page=args.page, word=args.word)

    # 3. 输出
    if args.json:
        # Agent 模式：只输出 JSON，不带任何装饰
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 人类模式：带排版
        ConsoleRenderer.render(result, keyword=args.word)
        # 附带原始数据供调试
        print(f"\n📦 Raw Data:\n{json.dumps(result, ensure_ascii=False, indent=2)}")


if __name__ == "__main__":
    main()