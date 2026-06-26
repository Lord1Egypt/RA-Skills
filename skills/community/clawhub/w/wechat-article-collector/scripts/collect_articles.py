#!/usr/bin/env python3
"""
通用网页文章采集器 - 支持多种网站配置
"""
import json
import os
import sys
import time
import re
import subprocess
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from utils import (
    get_config,
    ensure_browser_harness,
    extract_articles_generic,
    find_new_articles,
    download_article_content_generic
)


def main():
    parser = argparse.ArgumentParser(description="通用网页文章采集器")
    parser.add_argument(
        "--profile",
        default=None,
        help="配置文件名（wechat_mp, zhihu_column, juejin, custom）"
    )
    parser.add_argument(
        "--url",
        help="文章列表页 URL（覆盖配置文件中的 URL）"
    )
    parser.add_argument(
        "--save-dir",
        help="保存目录（覆盖配置文件）"
    )
    parser.add_argument(
        "--custom-selectors",
        help="自定义选择器 JSON 文件路径"
    )
    
    args = parser.parse_args()
    
    print("=== 通用网页文章采集器 ===\n")
    
    # 1. 加载配置
    config = get_config()
    profile_name = args.profile or config["default_profile"]
    
    if profile_name not in config["profiles"]:
        print(f"❌ 未找到配置: {profile_name}")
        print(f"可用配置: {', '.join(config['profiles'].keys())}")
        return 1
    
    profile = config["profiles"][profile_name]
    print(f"使用配置: {profile['name']}")
    
    # 覆盖 URL
    if args.url:
        profile["list_url"] = args.url
        print(f"目标 URL: {args.url}")
    
    # 加载自定义选择器
    if args.custom_selectors:
        with open(args.custom_selectors, "r") as f:
            custom = json.load(f)
            profile["selectors"].update(custom.get("selectors", {}))
            profile["content_selectors"] = custom.get("content_selectors", profile["content_selectors"])
    
    # 2. 检查 Browser Harness
    print("\n[1/5] 检查 Browser Harness...")
    if not ensure_browser_harness():
        print("❌ Browser Harness 未就绪")
        return 1
    print("✅ Browser Harness 就绪")
    
    # 3. 导航到列表页
    if profile["list_url"]:
        print(f"\n[2/5] 导航到列表页...")
        navigate_code = f'''
goto("{profile["list_url"]}")
wait_for_load()
import time
time.sleep({profile["wait_after_load"]})
print("OK")
'''
        result = subprocess.run(
            f"printf '{navigate_code}' | browser-harness",
            shell=True,
            capture_output=True,
            text=True,
            timeout=15
        )
        if "OK" not in result.stdout:
            print("❌ 导航失败")
            return 1
        print("✅ 页面已加载")
    else:
        print("\n[2/5] 跳过导航（使用当前页面）")
    
    # 4. 提取文章列表
    print("\n[3/5] 提取文章列表...")
    articles = extract_articles_generic(profile)
    if not articles:
        print("❌ 未提取到文章")
        print("提示：检查选择器配置是否正确")
        return 1
    print(f"✅ 提取到 {len(articles)} 篇文章")
    
    # 保存列表
    with open("/tmp/all_articles.json", "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    
    # 5. 去重
    print("\n[4/5] 对比本地知识库去重...")
    save_dir = Path(args.save_dir or config["save_dir"]).expanduser()
    site_name = profile_name.replace("_", "-")
    save_dir = save_dir / site_name
    save_dir.mkdir(parents=True, exist_ok=True)
    
    new_articles = find_new_articles(articles, save_dir)
    print(f"✅ 需要下载 {len(new_articles)} 篇新文章")
    
    if not new_articles:
        print("\n🎉 所有文章已收录")
        return 0
    
    # 6. 下载新文章
    print("\n[5/5] 下载新文章全文...")
    success_count = 0
    for i, article in enumerate(new_articles, 1):
        print(f"[{i}/{len(new_articles)}] {article['title']}")
        if download_article_content_generic(article, save_dir, profile, config):
            success_count += 1
            print(f"  ✅ 已保存")
        else:
            print(f"  ❌ 下载失败")
        time.sleep(config["sleep_between_downloads"])
    
    print(f"\n=== 完成 ===")
    print(f"成功下载: {success_count}/{len(new_articles)} 篇")
    print(f"保存位置: {save_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
