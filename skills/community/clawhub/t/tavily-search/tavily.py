#!/usr/bin/env python3
import os
import sys
import json
import argparse
import requests
import io

# 设置输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
API_URL = "https://api.tavily.com/search"

def save_config(api_key):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump({"api_key": api_key}, f, ensure_ascii=False, indent=2)
    print(f"[成功] API密钥已保存到: {CONFIG_PATH}")

def load_config():
    if not os.path.exists(CONFIG_PATH):
        print("[错误] 未配置API密钥，请先执行: python tavily.py config --api-key <your-tavily-api-key>")
        print("[提示] 密钥可以在 https://tavily.com/ 免费申请")
        sys.exit(1)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description="Tavily AI 搜索工具")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 配置命令
    config_parser = subparsers.add_parser("config", help="配置API密钥")
    config_parser.add_argument("--api-key", required=True, help="Tavily API密钥")

    # 搜索命令
    search_parser = subparsers.add_parser("search", help="基础搜索")
    search_parser.add_argument("query", help="搜索关键词")
    search_parser.add_argument("--max-results", type=int, default=5, help="返回结果数量")
    search_parser.add_argument("--search-depth", choices=["basic", "advanced"], default="basic", help="搜索深度")
    search_parser.add_argument("--include-images", action="store_true", help="是否返回图片")
    search_parser.add_argument("--include-raw-content", action="store_true", help="是否返回网页原始内容")
    search_parser.add_argument("--format", choices=["text", "json"], default="text", help="输出格式")

    # 深度研究命令
    research_parser = subparsers.add_parser("research", help="深度研究模式")
    research_parser.add_argument("query", help="研究关键词")
    research_parser.add_argument("--max-results", type=int, default=10, help="返回结果数量")
    research_parser.add_argument("--format", choices=["text", "json"], default="text", help="输出格式")

    # 图片搜索命令
    image_parser = subparsers.add_parser("image", help="图片搜索")
    image_parser.add_argument("query", help="搜索关键词")
    image_parser.add_argument("--count", type=int, default=5, help="返回图片数量")
    image_parser.add_argument("--format", choices=["text", "json"], default="text", help="输出格式")

    args = parser.parse_args()

    if args.command == "config":
        save_config(args.api_key)
        return

    config = load_config()
    api_key = config["api_key"]

    if args.command in ["search", "research", "image"]:
        query = args.query
        print(f"[提示] 正在搜索: {query}...")

        body = {
            "api_key": api_key,
            "query": query,
            "max_results": args.max_results if args.command != "image" else args.count,
            "search_depth": "advanced" if args.command == "research" else "basic",
            "include_answer": True,
            "include_images": args.command == "image" or args.include_images,
            "include_raw_content": args.include_raw_content if args.command == "search" else False
        }

        try:
            response = requests.post(API_URL, json=body, timeout=30)
            response.raise_for_status()
            result = response.json()

            if args.format == "json":
                print(json.dumps(result, ensure_ascii=False, indent=2))
                return

            # 文本输出
            print("\n[搜索结果] ")
            print("----------------------------------------")
            print(f"[答案] {result.get('answer', '无答案')}\n")

            if args.command == "image" and result.get("images"):
                print("[相关图片] ")
                for i, img in enumerate(result["images"][:args.count], 1):
                    print(f"   {i}. {img}")
                print()

            print("[来源详情] ")
            for i, item in enumerate(result["results"], 1):
                print(f"   {i}. {item['title']}")
                print(f"      链接: {item['url']}")
                pub_date = item.get('published_date', '未知')
                print(f"      发布时间: {pub_date}")
                content = item['content'][:150] + "..." if len(item['content'])>150 else item['content']
                print(f"      摘要: {content}\n")

            print(f"[响应时间] {result.get('response_time', '未知')}s")

        except Exception as e:
            print(f"[错误] 搜索失败: {str(e)}")
            sys.exit(1)

if __name__ == "__main__":
    main()
