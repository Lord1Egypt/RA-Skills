#!/usr/bin/env python3
"""
MiniMax 查询可用音色工具
用法: python voice_list.py --type all
     python voice_list.py --type system
     python voice_list.py --search "中文"
"""

import argparse
import os
import requests
import sys


def get_voice_list(voice_type: str = "all", api_key: str = None):
    """查询可用音色列表"""
    api_key = api_key or os.getenv("MINIMAX_API_KEY")
    if not api_key:
        raise ValueError("未设置 MINIMAX_API_KEY 环境变量")

    url = "https://api.minimaxi.com/v1/get_voice"

    payload = {"voice_type": voice_type}

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    print(f"正在查询音色列表 ({voice_type})...")
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    result = response.json()

    if result.get("base_resp", {}).get("status_code") != 0:
        raise Exception(f"API 错误: {result.get('base_resp', {}).get('status_msg', '未知错误')}")

    return result


def delete_voice(voice_id: str, api_key: str = None):
    """删除音色"""
    api_key = api_key or os.getenv("MINIMAX_API_KEY")
    if not api_key:
        raise ValueError("未设置 MINIMAX_API_KEY 环境变量")

    url = "https://api.minimaxi.com/v1/del_voice"

    payload = {"voice_id": voice_id}

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    response = requests.post(url, json=payload, headers=headers, timeout=30)
    return response.json()


def main():
    parser = argparse.ArgumentParser(description="MiniMax 音色管理工具")
    parser.add_argument("--type", dest="voice_type", default="all",
                        choices=["system", "voice_cloning", "voice_generation", "all"],
                        help="音色类型")
    parser.add_argument("--delete", dest="voice_id", help="删除指定音色 ID")
    parser.add_argument("--search", dest="search", help="搜索音色（按名称或描述）")
    parser.add_argument("--api-key", dest="api_key")

    args = parser.parse_args()

    try:
        if args.delete:
            result = delete_voice(args.delete, args.api_key)
            if result.get("base_resp", {}).get("status_code") == 0:
                print(f"✅ 音色已删除: {args.delete}")
            else:
                print(f"❌ 删除失败: {result.get('base_resp', {}).get('status_msg')}")
            return

        result = get_voice_list(args.voice_type, args.api_key)

        print("\n" + "=" * 60)
        print(f"音色列表 ({args.voice_type})")
        print("=" * 60)

        system_voices = result.get("system_voice", [])
        if system_voices:
            print(f"\n【系统音色】({len(system_voices)} 个)")
            for v in system_voices:
                name = v.get("voice_name", "")
                vid = v.get("voice_id", "")
                desc = v.get("description", [])
                desc_text = desc[0] if desc else ""

                # 搜索过滤
                if args.search:
                    search_lower = args.search.lower()
                    if search_lower not in vid.lower() and search_lower not in name.lower() and search_lower not in desc_text.lower():
                        continue

                print(f"  {vid}")
                if name:
                    print(f"    名称: {name}")
                if desc_text:
                    print(f"    描述: {desc_text[:60]}...")

        cloning_voices = result.get("voice_cloning", [])
        if cloning_voices:
            print(f"\n【复刻音色】({len(cloning_voices)} 个)")
            for v in cloning_voices:
                vid = v.get("voice_id", "")
                created = v.get("created_time", "")
                print(f"  {vid} (创建于 {created})")

        generation_voices = result.get("voice_generation", [])
        if generation_voices:
            print(f"\n【文生音色】({len(generation_voices)} 个)")
            for v in generation_voices:
                vid = v.get("voice_id", "")
                created = v.get("created_time", "")
                print(f"  {vid} (创建于 {created})")

        print("\n" + "=" * 60)

    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
