#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
社保公积金查询助手 - 统一入口
支持社保查询、公积金查询、五险一金计算、退休金估算
"""

import argparse
import subprocess
import sys
import os

# 切换到脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def run_script(script: str, args: list) -> None:
    """运行子脚本"""
    cmd = [sys.executable, os.path.join(SCRIPT_DIR, script)] + args
    subprocess.run(cmd, cwd=SCRIPT_DIR)

def main():
    parser = argparse.ArgumentParser(
        description="社保公积金查询助手",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 五险一金计算
  python check_deals.py calculate --salary 10000 --city 北京

  # 社保查询
  python check_deals.py social-security --city 上海 --guide

  # 公积金查询
  python check_deals.py fund --city 深圳 --guide

  # 退休金估算
  python check_deals.py pension --years 25 --avg-salary 8000
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # 五险一金计算
    calc_parser = subparsers.add_parser("calculate", help="五险一金计算")
    calc_parser.add_argument("--salary", type=float, required=True, help="月薪")
    calc_parser.add_argument("--city", type=str, default="北京", help="城市")
    calc_parser.add_argument("--fund-ratio", type=float, default=None, help="公积金比例")
    calc_parser.add_argument("--json", action="store_true", help="JSON 输出")
    
    # 社保查询
    ss_parser = subparsers.add_parser("social-security", help="社保查询")
    ss_parser.add_argument("--city", type=str, default="北京", help="城市")
    ss_parser.add_argument("--idcard", type=str, help="身份证号")
    ss_parser.add_argument("--guide", action="store_true", help="查询指引")
    ss_parser.add_argument("--json", action="store_true", help="JSON 输出")
    
    # 公积金查询
    fund_parser = subparsers.add_parser("fund", help="公积金查询")
    fund_parser.add_argument("--city", type=str, default="北京", help="城市")
    fund_parser.add_argument("--account", type=str, help="公积金账号")
    fund_parser.add_argument("--guide", action="store_true", help="查询指引")
    fund_parser.add_argument("--json", action="store_true", help="JSON 输出")
    
    # 退休金估算
    pension_parser = subparsers.add_parser("pension", help="退休金估算")
    pension_parser.add_argument("--years", type=int, required=True, help="缴费年限")
    pension_parser.add_argument("--avg-salary", type=float, required=True, help="平均缴费工资")
    pension_parser.add_argument("--local-avg", type=float, default=10000, help="当地社平工资")
    pension_parser.add_argument("--balance", type=float, default=None, help="个人账户余额")
    pension_parser.add_argument("--retirement-age", type=int, default=60, help="退休年龄")
    pension_parser.add_argument("--json", action="store_true", help="JSON 输出")
    
    args = parser.parse_args()
    
    if args.command == "calculate":
        cmd_args = ["--salary", str(args.salary), "--city", args.city]
        if args.fund_ratio:
            cmd_args.extend(["--fund-ratio", str(args.fund_ratio)])
        if args.json:
            cmd_args.append("--json")
        run_script("calculate.py", cmd_args)
        
    elif args.command == "social-security":
        cmd_args = ["--city", args.city]
        if args.idcard:
            cmd_args.extend(["--idcard", args.idcard])
        if args.guide:
            cmd_args.append("--guide")
        if args.json:
            cmd_args.append("--json")
        run_script("query_social_security.py", cmd_args)
        
    elif args.command == "fund":
        cmd_args = ["--city", args.city]
        if args.account:
            cmd_args.extend(["--account", args.account])
        if args.guide:
            cmd_args.append("--guide")
        if args.json:
            cmd_args.append("--json")
        run_script("query_fund.py", cmd_args)
        
    elif args.command == "pension":
        cmd_args = [
            "--years", str(args.years),
            "--avg-salary", str(args.avg_salary),
            "--local-avg", str(args.local_avg),
        ]
        if args.balance:
            cmd_args.extend(["--balance", str(args.balance)])
        if args.retirement_age:
            cmd_args.extend(["--retirement-age", str(args.retirement_age)])
        if args.json:
            cmd_args.append("--json")
        run_script("pension_estimate.py", cmd_args)
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
