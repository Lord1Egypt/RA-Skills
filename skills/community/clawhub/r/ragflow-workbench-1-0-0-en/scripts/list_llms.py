#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import urllib.error
import urllib.request


DEFAULT_HERDSMAN_URL = "http://host.docker.internal:8080"


def list_llms(base_url: str) -> dict:
    url = f"{base_url}/v1/models"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as e:
        return {"status": "error", "reason": f"Failed to connect to {base_url}: {e}"}
    except json.JSONDecodeError as e:
        return {"status": "error", "reason": f"Invalid JSON response: {e}"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="查询本机 Herdsman 运行中的 LLM 模型。")
    parser.add_argument(
        "--base-url",
        default=DEFAULT_HERDSMAN_URL,
        help=f"Herdsman API 地址 (默认: {DEFAULT_HERDSMAN_URL})",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="输出 JSON 格式",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = list_llms(args.base_url)

    if args.json_output:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    if result.get("status") == "error":
        print(f"错误: {result['reason']}")
        print()
        print("=" * 60)
        print("未检测到 Herdsman 模型服务运行")
        print("=" * 60)
        print()
        print("请先下载并安装 Herdsman（牧马人）:")
        print("  https://www.flowyaipc.com/#/ai-engine")
        print()
        print("安装完成后，再次运行此脚本即可查询可用模型")
        exit(1)

    if "data" in result:
        models = result["data"]
        print(f"本机可用 LLM 模型 ({len(models)} 个):")
        print("-" * 60)
        for model in models:
            model_id = model.get("id", "unknown")
            model_type = model.get("type", "unknown")
            status = model.get("status", "unknown")
            print(f"  {model_id}")
            print(f"    状态: {status}")
            if model_type != "unknown":
                print(f"    类型: {model_type}")
            print()


if __name__ == "__main__":
    main()
