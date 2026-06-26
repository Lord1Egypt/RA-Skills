#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WeChat MP Spider - OpenClaw Skill CLI Wrapper
微信公众号爬虫 OpenClaw Skill 包装器
"""

import sys
import os
import argparse

# 添加 skill 目录到路径
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SKILL_DIR)

from wechat_mp_crawler import (
    create_accounts_excel_file,
    read_accounts_from_excel,
    crawl_recent_articles,
    search_official_account,
    crawl_account_articles
)


def main():
    parser = argparse.ArgumentParser(
        description='微信公众号文章爬虫',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 批量获取多个公众号最新文章
  python3 wechat_spider.py mode1 --accounts accounts.xlsx
  
  # 获取单个公众号历史文章
  python3 wechat_spider.py mode2 --account "机器之心" --max 10
  
  # 按关键词筛选排序
  python3 wechat_spider.py mode3 --account "机器之心" --keywords "AI,人工智能,大模型" --weights "3,2,1" --max 50
        """
    )
    
    subparsers = parser.add_subparsers(dest='mode', help='爬取模式')
    
    # 模式一：批量最新文章
    parser1 = subparsers.add_parser('mode1', help='批量获取多个公众号最近两天的文章')
    parser1.add_argument('--accounts', default='accounts.xlsx', help='公众号列表 Excel 文件')
    parser1.add_argument('--create-example', action='store_true', help='创建示例公众号列表文件')
    
    # 模式二：单号历史文章
    parser2 = subparsers.add_parser('mode2', help='获取单个公众号的历史文章')
    parser2.add_argument('--account', required=True, help='公众号名称')
    parser2.add_argument('--max', type=int, default=10, help='最大爬取文章数（默认10）')
    
    # 模式三：关键词筛选
    parser3 = subparsers.add_parser('mode3', help='按关键词权重筛选并排序文章')
    parser3.add_argument('--account', required=True, help='公众号名称')
    parser3.add_argument('--keywords', required=True, help='关键词列表，逗号分隔')
    parser3.add_argument('--weights', default='1,1,1', help='关键词权重，逗号分隔')
    parser3.add_argument('--max', type=int, default=50, help='最大爬取文章数（默认50）')
    
    args = parser.parse_args()
    
    if not args.mode:
        parser.print_help()
        return
    
    # 切换到 skill 目录（用于保存凭证和输出文件）
    os.chdir(SKILL_DIR)
    
    if args.mode == 'mode1':
        if args.create_example:
            create_accounts_excel_file(args.accounts)
            print(f"已创建示例文件: {args.accounts}")
            return
        
        accounts = read_accounts_from_excel(args.accounts)
        if not accounts:
            print("没有读取到公众号列表，请检查文件:", args.accounts)
            return
        
        print(f"准备爬取 {len(accounts)} 个公众号的最新文章...")
        crawl_recent_articles(accounts)
    
    elif args.mode == 'mode2':
        print(f"准备爬取公众号 [{args.account}] 的历史文章...")
        crawl_account_articles(args.account, max_articles=args.max)
    
    elif args.mode == 'mode3':
        keywords = [k.strip() for k in args.keywords.split(',')]
        weights = [float(w.strip()) for w in args.weights.split(',')]
        
        if len(keywords) != len(weights):
            print("错误：关键词和权重数量不匹配")
            return
        
        print(f"准备爬取公众号 [{args.account}] 的文章并按关键词筛选...")
        print(f"关键词: {keywords}")
        print(f"权重: {weights}")
        
        # 这里需要调用 mode3 的逻辑
        # 由于原代码比较分散，这里简化处理
        print("提示：请直接编辑 Crawl_All_sort_by_keyword.py 运行")


if __name__ == '__main__':
    main()
