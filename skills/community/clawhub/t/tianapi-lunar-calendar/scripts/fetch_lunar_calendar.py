#!/usr/bin/env python3
"""
TianAPI Lunar Calendar Fetcher
------------------------------
查询中国老黄历，获取指定日期的宜忌、冲煞、吉时、胎神等传统民俗信息。
零外部依赖，仅使用 Python 标准库。

Usage:
    # 查询当天黄历
    python3 fetch_lunar_calendar.py --key YOUR_KEY

    # 查询指定公历日期
    python3 fetch_lunar_calendar.py --key YOUR_KEY --date 2024-07-13

    # 查询指定农历日期 (需加 --lunar 参数)
    python3 fetch_lunar_calendar.py --key YOUR_KEY --date 2024-6-8 --lunar

    # JSON模式 (适合 Agent 调用)
    python3 fetch_lunar_calendar.py --key YOUR_KEY --json

Env Config:
    export TIANAPI_LUNAR_CALENDAR_KEY=your_api_key
    # 或在脚本同级目录创建 .env 文件: TIANAPI_LUNAR_CALENDAR_KEY=your_api_key
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
API_ENDPOINT = "https://apis.tianapi.com/lunar/index"
ENV_KEY_NAME = "TIANAPI_LUNAR_CALENDAR_KEY"
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
        print(f"💡 提示: 申请 Key -> https://www.tianapi.com/apiview/45", file=sys.stderr)
        sys.exit(1)


class TianAPIClient:
    """天行数据 API 客户端"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_lunar(self, date: Optional[str] = None, is_lunar: bool = False) -> Dict[str, Any]:
        """
        执行 API 请求
        返回标准化结构: {"success": bool, "data": dict, "error": str|None}
        """
        params = {"key": self.api_key}
        
        if date:
            params["date"] = date.strip()
        if is_lunar:
            params["type"] = "1"

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
            print("📭 未查询到相关黄历数据。")
            return

        gregorian = data.get("gregoriandate", "未知日期")
        lunar = data.get("lunardate", "")
        shengxiao = data.get("shengxiao", "")
        chongsha = data.get("chongsha", "")
        
        print(f"\n📅 {gregorian} 老黄历")
        print(f"农历：{lunar} | 生肖：{shengxiao}")
        print(f"冲煞：{chongsha}\n")
        
        print(f"✅ 宜：{data.get('fitness', '无')}")
        print(f"❌ 忌：{data.get('taboo', '无')}\n")
        
        shenwei = data.get('shenwei', '')
        if shenwei:
            print(f"🧭 吉神方位：{shenwei}")
            
        taishen = data.get('taishen', '')
        if taishen:
            print(f"👶 胎神方位：{taishen}")
        print("-" * 40)


def main():
    parser = argparse.ArgumentParser(description="TianAPI Lunar Calendar Fetcher")
    parser.add_argument("--key", help="API Key (可选，优先使用环境变量)")
    parser.add_argument("--date", help="查询日期 (如: 2024-07-13 或 2024-6-8)")
    parser.add_argument("--type", action="store_true", help="按农历查询该值为1且日期不能有前导零")
    args = parser.parse_args()

    # 1. 初始化
    config = Config(args.key)
    client = TianAPIClient(config.api_key)

    # 2. 请求
    result = client.fetch_lunar(date=args.date, is_lunar=args.lunar)

    # 3. 输出
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        ConsoleRenderer.render(result)


if __name__ == "__main__":
    main()