#!/usr/bin/env python3
"""
TianAPI Nutrient Query Fetcher
------------------------------
查询近两千种常见食物的详细营养成分，支持按食品名称、分类或特定营养素进行检索和排序。
零外部依赖，仅使用 Python 标准库。

Usage:
    # 查询指定食物的营养成分
    python3 fetch_nutrient-query.py --key YOUR_KEY --word 油条

    # 按钙含量(gai)从高到低排名
    python3 fetch_nutrient-query.py --key YOUR_KEY --word gai --mode 2 --num 5

    # JSON模式 (适合 Agent 调用)
    python3 fetch_nutrient-query.py --key YOUR_KEY --word 黄瓜 --json

Env Config:
    export TIANAPI_NUTRIENT_KEY=your_api_key
    # 或在脚本同级目录创建 .env 文件: TIANAPI_NUTRIENT_KEY=your_api_key
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
API_ENDPOINT = "https://apis.tianapi.com/nutrient/index"
ENV_KEY_NAME = "TIANAPI_NUTRIENT_KEY"
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
        print(f"💡 提示: 申请 Key -> https://www.tianapi.com/apiview/121", file=sys.stderr)
        sys.exit(1)


class TianAPIClient:
    """天行数据 API 客户端"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_nutrient(self, word: str, mode: Optional[int] = None, num: Optional[int] = None, page: Optional[int] = None) -> Dict[str, Any]:
        """
        执行 API 请求
        返回标准化结构: {"success": bool, "data": dict|list, "error": str|None}
        """
        params = {
            "key": self.api_key,
            "word": word.strip()
        }
        
        # 动态添加可选参数
        if mode is not None: params["mode"] = mode
        if num is not None: params["num"] = num
        if page is not None: params["page"] = page

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


class ConsoleRenderer:
    """终端渲染器：负责把数据变成人话"""
    
    @staticmethod
    def render(result: Dict[str, Any], keyword: str):
        if not result["success"]:
            print(f"❌ 请求失败: {result['error']}")
            return

        data = result["data"]
        if not data:
            print(f"📭 未查询到 '{keyword}' 的营养成分信息。")
            return

        # 如果返回的是列表（例如查询排名或分类），遍历输出
        if isinstance(data, list):
            print(f"\n🥗 '{keyword}' 营养成分查询结果 (共 {len(data)} 条)\n{'-'*40}")
            for idx, item in enumerate(data, 1):
                name = item.get("name", "未知食物")
                rl = item.get("rl", "N/A")
                print(f"{idx}. {name} | 热量: {rl}大卡/100g")
        else:
            # 如果返回的是字典（单个食物详情）
            print(f"\n🥗 {data.get('name', '未知食物')} 的营养成分 (每100克)\n{'-'*40}")
            print(f"食品种类: {data.get('type', '未知')}")
            print(f"热量(rl): {data.get('rl', 'N/A')} 大卡")
            print(f"蛋白质(dbz): {data.get('dbz', 'N/A')} 克")
            print(f"脂肪(zf): {data.get('zf', 'N/A')} 克")
            print(f"碳水(shhf): {data.get('shhf', 'N/A')} 克")
            print(f"钠(la): {data.get('la', 'N/A')} 毫克")
            print(f"钙(gai): {data.get('gai', 'N/A')} 毫克")
            print("-" * 40)


def main():
    parser = argparse.ArgumentParser(description="TianAPI Nutrient Query Fetcher")
    parser.add_argument("--key", help="API Key (可选，优先使用环境变量)")
    parser.add_argument("--word", required=True, help="查询关键词 (如: 油条, 谷类, gai)")
    parser.add_argument("--mode", type=int, choices=[0, 1, 2, 3], help="查询模式: 0-查食品(默认), 1-查分类, 2-正序排名, 3-倒序排名")
    parser.add_argument("--num", type=int, help="返回数量 (默认10)")
    parser.add_argument("--page", type=int, help="翻页 (默认1)")
    args = parser.parse_args()

    # 1. 初始化
    config = Config(args.key)
    client = TianAPIClient(config.api_key)

    # 2. 请求
    result = client.fetch_nutrient(word=args.word, mode=args.mode, num=args.num, page=args.page)

    # 3. 输出
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        ConsoleRenderer.render(result, keyword=args.word)


if __name__ == "__main__":
    main()