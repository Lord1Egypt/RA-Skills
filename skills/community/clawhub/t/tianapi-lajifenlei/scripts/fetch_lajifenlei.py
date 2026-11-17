#!/usr/bin/env python3
"""
TianAPI Lajifenlei Fetcher
------------------------------------
根据物品名称查询垃圾分类信息，支持模糊搜索、精确搜索及分页。
零外部依赖，仅使用 Python 标准库。

Usage:
    # 基础查询
    python3 fetch_lajifenlei.py --key YOUR_KEY --word 眼镜

    # 精确查询并指定返回数量
    python3 fetch_lajifenlei.py --key YOUR_KEY --word 眼镜 --mode 1 --num 5

    # 翻页查询
    python3 fetch_lajifenlei.py --key YOUR_KEY --word 眼镜 --page 2

    # JSON模式 (适合 Agent 调用)
    python3 fetch_lajifenlei.py --key YOUR_KEY --word 电池 --json

Env Config:
    export TIANAPI_LAJIFENLEI_KEY=your_api_key
    # 或在脚本同级目录创建 .env 文件: TIANAPI_LAJIFENLEI_KEY=your_api_key
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
API_ENDPOINT = "https://apis.tianapi.com/lajifenlei/index"
ENV_KEY_NAME = "TIANAPI_LAJIFENLEI_KEY"
DEFAULT_TIMEOUT = 10

# 垃圾分类类型映射
TYPE_MAP = {
    0: "可回收垃圾",
    1: "有害垃圾",
    2: "厨余垃圾(湿)",
    3: "其他垃圾(干)"
}


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
        print(f"💡 提示: 申请 Key -> https://www.tianapi.com/apiview/97", file=sys.stderr)
        sys.exit(1)


class TianAPIClient:
    """天行数据 API 客户端"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_waste(self, word: str, num: Optional[int] = None, mode: Optional[int] = None, page: Optional[int] = None) -> Dict[str, Any]:
        """
        执行 API 请求
        返回标准化结构: {"success": bool, "data": list, "error": str|None}
        """
        params = {
            "key": self.api_key,
            "word": word.strip()
        }
        
        # 动态添加可选参数
        if num is not None: params["num"] = num
        if mode is not None: params["mode"] = mode
        if page is not None: params["page"] = page

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


class ConsoleRenderer:
    """终端渲染器：负责把数据变成人话"""
    
    @staticmethod
    def render(result: Dict[str, Any], keyword: str):
        if not result["success"]:
            print(f"❌ 请求失败: {result['error']}")
            return

        items = result["data"]
        if not items:
            print(f"📭 未查询到 '{keyword}' 的垃圾分类信息。")
            return

        print(f"\n♻️ '{keyword}' 垃圾分类查询结果 (共 {len(items)} 条)\n{'-'*40}")
        for idx, item in enumerate(items, 1):
            name = item.get("name", "未知物品")
            type_id = item.get("type")
            type_name = TYPE_MAP.get(type_id, f"未知类型({type_id})")
            tip = item.get("tip", "无")
            explain = item.get("explain", "")
            
            print(f"{idx}. {name}")
            print(f"   🏷️ 分类: {type_name}")
            print(f"   💡 提示: {tip}")
            if explain:
                print(f"   📝 解释: {explain}")
            print()


def main():
    parser = argparse.ArgumentParser(description="TianAPI Lajifenlei Fetcher")
    parser.add_argument("--key", help="API Key (可选，优先使用环境变量)")
    parser.add_argument("--word", required=True, help="物品名称 (如: 眼镜, 电池)")
    parser.add_argument("--num", type=int, help="返回数量 (默认10)")
    parser.add_argument("--mode", type=int, choices=[0, 1], help="查询模式: 0-模糊查询(默认), 1-精确查询")
    parser.add_argument("--page", type=int, help="翻页 (默认1)")
    args = parser.parse_args()

    # 1. 初始化
    config = Config(args.key)
    client = TianAPIClient(config.api_key)

    # 2. 请求
    result = client.fetch_waste(word=args.word, num=args.num, mode=args.mode, page=args.page)

    # 3. 输出
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        ConsoleRenderer.render(result, keyword=args.word)


if __name__ == "__main__":
    main()