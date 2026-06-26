#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WeChat MP Spider CLI with x402 Payment
微信公众号爬虫命令行工具 - 支持 x402 支付
"""

import argparse
import json
import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from spider_api import get_api, X402PaymentRequired
from config import RECEIVING_ADDRESS, PRICING


def print_status(user_id: str):
    """打印用户状态"""
    status = get_api().get_user_status(user_id)
    
    print(f"\n{'='*50}")
    print(f"💳 用户: {user_id[:10]}...{user_id[-6:]}")
    print(f"{'='*50}")
    
    # 免费额度
    free = status.get("free", {})
    print(f"\n🎁 免费额度: {free.get('remaining', 0)}/{free.get('total', 10)} 篇")
    
    # 订阅状态
    sub = status.get("subscription", {})
    if sub.get("active"):
        print(f"📅 包月订阅: ✅ 有效 (到期: {sub.get('expires_at', '未知')})")
    else:
        print(f"📅 包月订阅: ❌ 未开通 (${PRICING['monthly']}/月)")
    
    # 使用统计
    print(f"📊 总使用次数: {status.get('total_usage', 0)}")
    print(f"{'='*50}\n")


def handle_x402_payment(request):
    """处理 x402 支付请求"""
    print(f"\n💳 需要支付: ${request.amount} USDC")
    print(f"   收款地址: {RECEIVING_ADDRESS}")
    print(f"   网络: Base")
    print(f"   资源: {request.resource}:{request.resource_id}")
    print(f"   有效期: 5分钟")
    
    print(f"\n请完成以下步骤:")
    print(f"1. 打开你的钱包 (MetaMask / Coinbase Wallet)")
    print(f"2. 切换到 Base 网络")
    print(f"3. 发送 ${request.amount} USDC 到: {RECEIVING_ADDRESS}")
    print(f"4. 复制交易哈希 (Transaction Hash)")
    
    tx_hash = input(f"\n请输入交易哈希 (0x...): ").strip()
    
    # 构建支付证明 token (简化版)
    payment_token = json.dumps({
        "tx_hash": tx_hash,
        "nonce": request.nonce,
        "amount": request.amount,
        "from": "user_wallet_address",  # 实际应从签名获取
        "timestamp": int(time.time()),
    })
    
    return payment_token


def cmd_status(args):
    """查看状态命令"""
    if not args.user:
        print("❌ 请提供用户ID: --user 0xYourWalletAddress")
        return
    print_status(args.user)


def cmd_crawl(args):
    """爬取命令"""
    if not args.user:
        print("❌ 请提供用户ID: --user 0xYourWalletAddress")
        return
    
    if not args.account:
        print("❌ 请提供公众号名称: --account 机器之心")
        return
    
    # 先显示状态
    print_status(args.user)
    
    # 确定计费模式
    if args.mode == "free":
        # 免费模式
        print(f"\n🚀 使用免费额度爬取 {args.max} 篇文章...")
        result = get_api().crawl_with_free_quota(args.user, args.account, args.max)
        
    elif args.mode == "async" or args.max >= 50:
        # 异步模式（大额）
        print(f"\n🚀 创建异步任务（按号计费 $10）...")
        try:
            result = get_api().crawl_async(args.user, args.account, args.max)
        except X402PaymentRequired as e:
            payment_token = handle_x402_payment(e.payment_request)
            result = get_api().crawl_async(args.user, args.account, args.max, payment_token)
    else:
        # 实时模式（小额）
        print(f"\n🚀 实时爬取 {args.max} 篇文章（按篇计费 $0.1/篇）...")
        try:
            result = get_api().crawl_realtime(args.user, args.account, args.max)
        except X402PaymentRequired as e:
            payment_token = handle_x402_payment(e.payment_request)
            result = get_api().crawl_realtime(args.user, args.account, args.max, payment_token)
    
    # 显示结果
    if result.get("success"):
        print(f"\n✅ 爬取成功!")
        print(f"   文章数量: {result.get('count', 0)}")
        print(f"   费用: ${result.get('cost', 0)} USDC")
        print(f"   支付方式: {result.get('paid_by', 'unknown')}")
        
        if result.get('tx_hash'):
            print(f"   交易哈希: {result.get('tx_hash')}")
        
        if result.get('mode') == 'async':
            print(f"\n   任务ID: {result.get('task_id')}")
            print(f"   使用 'status {result.get('task_id')}' 查看进度")
    else:
        print(f"\n❌ 失败: {result.get('error', '未知错误')}")


def cmd_task_status(args):
    """查看任务状态命令"""
    if not args.task_id:
        print("❌ 请提供任务ID")
        return
    
    result = get_api().get_task_status(args.task_id)
    
    if result.get("success"):
        print(f"\n📋 任务状态: {args.task_id}")
        print(f"   公众号: {result.get('account')}")
        print(f"   状态: {result.get('status')}")
        print(f"   创建时间: {result.get('created_at')}")
        
        if result.get('started_at'):
            print(f"   开始时间: {result.get('started_at')}")
        
        if result.get('completed_at'):
            print(f"   完成时间: {result.get('completed_at')}")
        
        if result.get('result'):
            print(f"   结果: {json.dumps(result.get('result'), indent=2)}")
        
        if result.get('error'):
            print(f"   错误: {result.get('error')}")
    else:
        print(f"❌ {result.get('error')}")


def cmd_subscribe(args):
    """开通包月命令"""
    if not args.user:
        print("❌ 请提供用户ID")
        return
    
    print(f"\n📅 开通包月订阅 (${PRICING['monthly']} USDC/月)")
    print(f"   无限爬取，30天有效")
    
    # 创建支付请求
    from x402_core import X402Processor
    processor = X402Processor()
    request = processor.create_payment_request(
        user_id=args.user,
        resource="subscription",
        resource_id="monthly",
        amount=PRICING['monthly']
    )
    
    payment_token = handle_x402_payment(request)
    result = get_api().subscribe_monthly(args.user, payment_token)
    
    if result.get("success"):
        print(f"\n✅ {result.get('message')}")
        print(f"   到期时间: {result.get('expires_at')}")
    else:
        print(f"\n❌ 失败: {result.get('error')}")


def main():
    parser = argparse.ArgumentParser(
        description="微信公众号爬虫 - x402支付版",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 查看状态
  python3 spider_cli.py status --user 0xYourWallet
  
  # 使用免费额度爬取
  python3 spider_cli.py crawl --user 0xYourWallet --account 机器之心 --max 5 --mode free
  
  # 实时付费爬取（小额）
  python3 spider_cli.py crawl --user 0xYourWallet --account 机器之心 --max 20
  
  # 异步付费爬取（大额/全量）
  python3 spider_cli.py crawl --user 0xYourWallet --account 机器之心 --max 100 --mode async
  
  # 查看异步任务状态
  python3 spider_cli.py status TASK-1234567890
  
  # 开通包月
  python3 spider_cli.py subscribe --user 0xYourWallet
        """
    )
    
    parser.add_argument("--user", help="用户钱包地址 (0x...)")
    
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # status 命令
    parser_status = subparsers.add_parser("status", help="查看用户状态或任务状态")
    parser_status.add_argument("task_id", nargs="?", help="任务ID (查看任务状态时提供)")
    
    # crawl 命令
    parser_crawl = subparsers.add_parser("crawl", help="爬取公众号文章")
    parser_crawl.add_argument("--account", required=True, help="公众号名称")
    parser_crawl.add_argument("--max", type=int, default=10, help="最大文章数")
    parser_crawl.add_argument(
        "--mode", 
        choices=["free", "realtime", "async"], 
        default="realtime",
        help="支付模式 (默认: 自动选择)"
    )
    
    # subscribe 命令
    parser_sub = subparsers.add_parser("subscribe", help="开通包月订阅")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 路由命令
    if args.command == "status":
        if args.task_id:
            cmd_task_status(args)
        else:
            cmd_status(args)
    elif args.command == "crawl":
        cmd_crawl(args)
    elif args.command == "subscribe":
        cmd_subscribe(args)


if __name__ == "__main__":
    import time  # 在main中导入
    main()
