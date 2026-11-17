#!/usr/bin/env python3
"""
TianAPI Category News Fetcher
-----------------------------
获取指定频道的分类新闻（支持国内、国际、科技、电竞、AI等）。
零外部依赖，仅使用 Python 标准库。

Usage:
    # 获取科技新闻 (ID: 13)
    python tianapi_category_news.py --key YOUR_KEY --col 13 --num 5

    # 获取电竞资讯 (ID: 45)
    python tianapi_category_news.py --key YOUR_KEY --col 45

    # JSON模式 (适合 Agent 调用)
    python tianapi_category_news.py --key YOUR_KEY --col 7 --json

Env Config:
    export TIANAPI_KEY=your_api_key
    # 或在脚本同级目录创建 .env 文件: TIANAPI_KEY=your_api_key
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from typing import Optional, Dict, Any, List

# --- 配置常量 ---
API_ENDPOINT = "https://apis.tianapi.com/allnews/index"
ENV_KEY_NAME = "TIANAPI_KEY"
DEFAULT_TIMEOUT = 10
MAX_NEWS_LIMIT = 50

# --- 频道ID映射表 (基于最新文档) ---
CHANNEL_MAP = {
    "1": "头条", "5": "社会", "7": "国内", "8": "国际", "10": "娱乐",
    "12": "体育", "13": "科技", "17": "健康", "18": "旅游", "20": "NBA",
    "21": "VR科技", "22": "IT资讯", "26": "足球", "27": "军事", "29": "人工智能",
    "30": "CBA", "31": "游戏", "32": "财经", "33": "动漫", "34": "互联网",
    "35": "汽车", "36": "科学探索", "40": "影视", "41": "环保", "42": "垃圾分类",
    "43": "女性", "45": "电竞", "46": "宠物"
}

class Config:
    """配置加载器：支持 命令行 > 环境变量 > .env 文件"""
    
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
        print(f"💡 提示: 申请 Key -> https://www.tianapi.com/apiview/51", file=sys.stderr)
        sys.exit(1)


class TianAPIClient:
    """天行数据 API 客户端"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_news(self, col: str, num: int = 10, page: int = 1) -> Dict[str, Any]:
        """
        执行 API 请求
        返回标准化结构: {"success": bool, "data": list, "error": str|None}
        """
        params = {
            "key": self.api_key,
            "col": col,
            "num": min(max(1, num), MAX_NEWS_LIMIT),
            "page": max(1, page),
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
    """终端渲染器"""
    
    @staticmethod
    def render(result: Dict[str, Any], col_id: str):
        channel_name = CHANNEL_MAP.get(col_id, f"频道{col_id}")
        
        if not result["success"]:
            print(f"❌ 请求失败: {result['error']}")
            return

        items = result["data"]
        if not items:
            print(f"📭 {channel_name} 暂无新闻数据。")
            return

        header = f"📰 {channel_name} 资讯速报 | 共 {len(items)} 条"
        
        print(f"\n{header}\n{'-'*50}")
        for idx, item in enumerate(items, 1):
            title = item.get("title", "无标题")
            source = item.get("source", "未知来源")
            ctime = item.get("ctime", "")[:16]
            url = item.get("url", "#")
            
            print(f"{idx}. {title}")
            print(f"   📅 {ctime} | 🏢 {source}")
            print(f"   🔗 {url}\n")


def main():
    parser = argparse.ArgumentParser(description="TianAPI Category News Fetcher")
    parser.add_argument("--key", help="API Key")
    parser.add_argument("--col", required=True, help="频道ID (如: 13=科技, 45=电竞)")
    parser.add_argument("--num", type=int, default=10, help="返回条数")
    parser.add_argument("--page", type=int, default=1, help="页码")
    args = parser.parse_args()

    # 1. 初始化
    config = Config(args.key)
    client = TianAPIClient(config.api_key)

    # 2. 请求
    result = client.fetch_news(col=args.col, num=args.num, page=args.page)

    # 3. 输出
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        ConsoleRenderer.render(result, col_id=args.col)
        # 调试用原始数据
        # print(f"\n📦 Raw Data:\n{json.dumps(result, ensure_ascii=False, indent=2)}")


if __name__ == "__main__":
    main()