#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全平台搜索示例 - 演示所有 8 个平台的搜索功能
"""

import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from search import PlatformSearch


def main():
    """主函数"""
    print("=" * 70)
    print("TechRecruiter Pro - 全平台搜索示例")
    print("=" * 70)
    
    searcher = PlatformSearch()
    
    # 1. AMiner 搜索
    print("\n" + "=" * 70)
    print("📌 1. AMiner 搜索 - 学者档案")
    print("=" * 70)
    aminer_results = searcher.search_aminer(
        keywords=["RLHF", "LLM"],
        affiliation="Moonshot"
    )
    for result in aminer_results:
        print(f"   找到：{result.get('name', 'Unknown')}")
    
    # 2. Google Scholar 搜索
    print("\n" + "=" * 70)
    print("📌 2. Google Scholar 搜索 - 学术论文")
    print("=" * 70)
    scholar_results = searcher.search_google_scholar(
        author_name="Yifan Bai",
        keywords=["LLM"]
    )
    for result in scholar_results:
        print(f"   找到：{result.get('name', 'Unknown')}")
    
    # 3. GitHub 搜索
    print("\n" + "=" * 70)
    print("📌 3. GitHub 搜索 - 代码仓库")
    print("=" * 70)
    github_results = searcher.search_github(
        keywords=["RLHF", "PPO"],
        language="Python",
        min_stars=100
    )
    for result in github_results:
        print(f"   找到：{result.get('username', 'Unknown')}")
    
    # 4. arXiv 搜索
    print("\n" + "=" * 70)
    print("📌 4. arXiv 搜索 - 最新论文")
    print("=" * 70)
    arxiv_results = searcher.search_arxiv(
        keywords=["Kimi", "K2", "Agentic"],
        date_range="20250101-20251231"
    )
    for result in arxiv_results:
        print(f"   找到：{result.get('title', 'Unknown')}")
    
    # 5. LinkedIn 搜索 (新增)
    print("\n" + "=" * 70)
    print("📌 5. LinkedIn 搜索 - 职业档案 [新增]")
    print("=" * 70)
    linkedin_results = searcher.search_linkedin(
        keywords=["RLHF", "LLM"],
        current_company="Moonshot AI",
        title="Research Scientist"
    )
    for result in linkedin_results:
        print(f"   找到：{result.get('name', 'Unknown')} - {result.get('headline', '')}")
    
    # 6. Reddit 搜索 (新增)
    print("\n" + "=" * 70)
    print("📌 6. Reddit 搜索 - 技术社区 [新增]")
    print("=" * 70)
    reddit_results = searcher.search_reddit(
        keywords=["RLHF", "LLM"],
        subreddits=["MachineLearning", "reinforcementlearning", "LocalLLaMA"],
        min_karma=1000
    )
    for result in reddit_results:
        print(f"   找到：{result.get('username', 'Unknown')} - Karma: {result.get('karma', {})}")
    
    # 7. Discord 搜索 (新增)
    print("\n" + "=" * 70)
    print("📌 7. Discord 搜索 - 技术社区 [新增]")
    print("=" * 70)
    discord_results = searcher.search_discord(
        keywords=["AI", "ML"],
        servers=["AI Research Hub", "Machine Learning"]
    )
    for result in discord_results:
        if "name" in result:
            print(f"   服务器：{result.get('name')} - {result.get('members', 0)} 成员")
        else:
            print(f"   用户：{result.get('username', 'Unknown')} - {result.get('roles', [])}")
    
    # 8. Hugging Face 搜索 (新增)
    print("\n" + "=" * 70)
    print("📌 8. Hugging Face 搜索 - 模型/数据集 [新增]")
    print("=" * 70)
    hf_results = searcher.search_huggingface(
        keywords=["RLHF", "LLM"],
        model_type="transformer",
        min_likes=100
    )
    for result in hf_results:
        if "username" in result:
            print(f"   用户：{result.get('username')} - {result.get('models_count', 0)} 模型")
        else:
            print(f"   模型：{result.get('name')} - {result.get('downloads', 0)} 下载")
    
    # 9. X (Twitter) 搜索 (新增)
    print("\n" + "=" * 70)
    print("📌 9. X (Twitter) 搜索 - 社交媒体影响力 [新增]")
    print("=" * 70)
    twitter_results = searcher.search_twitter(
        keywords=["RLHF", "LLM", "AI"],
        min_followers=10000,
        verified=True
    )
    for result in twitter_results:
        print(f"   找到：{result.get('display_name')} (@{result.get('username')}) - {result.get('followers', 0)} 粉丝")
    
    # 总结
    print("\n" + "=" * 70)
    print("✅ 全平台搜索完成！")
    print("=" * 70)
    print(f"""
搜索平台汇总:
  1. AMiner:         {len(aminer_results)} 个结果
  2. Google Scholar: {len(scholar_results)} 个结果
  3. GitHub:         {len(github_results)} 个结果
  4. arXiv:          {len(arxiv_results)} 个结果
  5. LinkedIn:       {len(linkedin_results)} 个结果 ⭐ 新增
  6. Reddit:         {len(reddit_results)} 个结果 ⭐ 新增
  7. Discord:        {len(discord_results)} 个结果 ⭐ 新增
  8. Hugging Face:   {len(hf_results)} 个结果 ⭐ 新增
  9. X (Twitter):    {len(twitter_results)} 个结果 ⭐ 新增
  
总计：{sum([len(aminer_results), len(scholar_results), len(github_results), 
           len(arxiv_results), len(linkedin_results), len(reddit_results),
           len(discord_results), len(hf_results), len(twitter_results)])} 个结果
""")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
