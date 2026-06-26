#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tushare-CLI 工具 - 完整版
作者：滚滚家族 🌪️
版本：1.0.0
"""

import argparse
import sys
import os
from datetime import datetime

# 尝试导入 tushare
try:
    import tushare as ts
except ImportError:
    print("❌ 未安装 tushare，请运行：pip install tushare")
    sys.exit(1)

# 颜色输出
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    """打印标题"""
    print(f"\n{Colors.OKCYAN}{Colors.BOLD}{'━' * 60}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}{Colors.BOLD}{text}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}{Colors.BOLD}{'━' * 60}{Colors.ENDC}\n")

def print_success(text):
    """打印成功信息"""
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")

def print_error(text):
    """打印错误信息"""
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")

def print_warning(text):
    """打印警告信息"""
    print(f"{Colors.WARNING}⚠️ {text}{Colors.ENDC}")

def get_pro():
    """获取 tushare pro 实例"""
    token = os.getenv('TUSHARE_TOKEN')
    if not token:
        print_warning("未设置 TUSHARE_TOKEN 环境变量")
        print_warning("请运行：export TUSHARE_TOKEN=your_token")
        print_warning("或使用免 Token 基础接口（数据有限）")
        sys.exit(1)
    return ts.pro_api(token)

def query_basic(stock_code):
    """查询股票基本信息"""
    print_header(f"📈 股票基本信息 - {stock_code}")
    
    try:
        pro = get_pro()
        basic = pro.stock_basic(ts_code=stock_code)
        
        if basic.empty:
            print_error("未找到股票信息")
            return
        
        stock = basic.iloc[0]
        
        print(f"{Colors.BOLD}【基本资料】{Colors.ENDC}")
        print(f"股票代码：{stock.get('ts_code', 'N/A')}")
        print(f"股票简称：{stock.get('name', 'N/A')}")
        print(f"所属行业：{stock.get('industry', 'N/A')}")
        print(f"上市日期：{stock.get('list_date', 'N/A')}")
        
        print(f"\n{Colors.BOLD}【股本信息】{Colors.ENDC}")
        print(f"总股本：{stock.get('total_share', 0):.2f}亿股")
        print(f"流通股本：{stock.get('csrc_share', 0):.2f}亿股")
        
        print(f"\n{Colors.BOLD}【公司信息】{Colors.ENDC}")
        print(f"法人代表：{stock.get('legal_rep', 'N/A')}")
        print(f"注册地址：{stock.get('area', 'N/A')}")
        
        print_success("查询完成！")
        
    except Exception as e:
        print_error(f"查询失败：{e}")

def query_indicators(stock_code):
    """查询财务指标"""
    print_header(f"📊 财务指标 - {stock_code}")
    
    try:
        pro = get_pro()
        indicators = pro.fina_indicator(ts_code=stock_code)
        
        if indicators.empty:
            print_error("未找到财务数据")
            return
        
        latest = indicators.iloc[0]
        
        print(f"{Colors.BOLD}【报告期】{latest.get('end_date', 'N/A')}{Colors.ENDC}")
        
        print(f"\n{Colors.BOLD}【盈利能力】{Colors.ENDC}")
        print(f"毛利率：{latest.get('grossprofit_margin', 0):.2f}%")
        print(f"净利率：{latest.get('net_profit_margin', 0):.2f}%")
        print(f"ROE：{latest.get('roe', 0):.2f}%")
        print(f"ROA：{latest.get('roa', 0):.2f}%")
        
        print(f"\n{Colors.BOLD}【成长能力】{Colors.ENDC}")
        print(f"收入增长率：{latest.get('op_yoy', 0):.2f}%")
        print(f"利润增长率：{latest.get('netprofit_yoy', 0):.2f}%")
        
        print(f"\n{Colors.BOLD}【偿债能力】{Colors.ENDC}")
        print(f"流动比率：{latest.get('current_ratio', 0):.2f}")
        print(f"速动比率：{latest.get('quick_ratio', 0):.2f}")
        print(f"资产负债率：{latest.get('debt_to_assets', 0):.2f}%")
        
        print_success("查询完成！")
        
    except Exception as e:
        print_error(f"查询失败：{e}")

def query_daily(stock_code):
    """查询日线行情"""
    print_header(f"💹 日线行情 - {stock_code}")
    
    try:
        pro = get_pro()
        daily = pro.daily(ts_code=stock_code)
        
        if daily.empty:
            print_error("未找到行情数据")
            return
        
        latest = daily.iloc[0]
        
        print(f"{Colors.BOLD}【最新行情】{latest.get('trade_date', 'N/A')}{Colors.ENDC}")
        print(f"收盘价：¥{latest.get('close', 0):.2f}")
        print(f"开盘价：¥{latest.get('open', 0):.2f}")
        print(f"最高价：¥{latest.get('high', 0):.2f}")
        print(f"最低价：¥{latest.get('low', 0):.2f}")
        print(f"成交量：{latest.get('vol', 0):,}手")
        print(f"成交额：¥{latest.get('amount', 0):,.0f}")
        
        print(f"\n{Colors.BOLD}【涨跌幅】{Colors.ENDC}")
        pct_chg = latest.get('pct_chg', 0)
        if pct_chg > 0:
            print(f"{Colors.OKGREEN}涨跌幅：+{pct_chg:.2f}%{Colors.ENDC}")
        elif pct_chg < 0:
            print(f"{Colors.FAIL}涨跌幅：{pct_chg:.2f}%{Colors.ENDC}")
        else:
            print(f"涨跌幅：{pct_chg:.2f}%")
        
        print_success("查询完成！")
        
    except Exception as e:
        print_error(f"查询失败：{e}")

def query_news():
    """查询新闻资讯"""
    print_header(f"📰 财经新闻")
    
    try:
        pro = get_pro()
        news = pro.news(src='cctv')
        
        if news.empty:
            print_warning("未找到新闻")
            return
        
        print(f"{Colors.BOLD}【最新新闻】{Colors.ENDC}\n")
        
        for i, row in news.head(10).iterrows():
            print(f"{i+1}. {row.get('title', 'N/A')}")
            print(f"   时间：{row.get('pub_date', 'N/A')}")
            print(f"   来源：{row.get('src', 'N/A')}\n")
        
        print_success("查询完成！")
        
    except Exception as e:
        print_error(f"查询失败：{e}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='📈 Tushare-CLI 工具 - 滚滚家族 🌪️',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  %(prog)s basic --stock 000001.SZ           查询平安银行基本信息
  %(prog)s indicators --stock 600519.SH      查询贵州茅台财务指标
  %(prog)s daily --stock 000001.SZ           查询平安银行日线行情
  %(prog)s news                              查询财经新闻
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # basic 命令
    basic_parser = subparsers.add_parser('basic', help='股票基本信息')
    basic_parser.add_argument('--stock', type=str, required=True, help='股票代码')
    
    # indicators 命令
    ind_parser = subparsers.add_parser('indicators', help='财务指标')
    ind_parser.add_argument('--stock', type=str, required=True, help='股票代码')
    
    # daily 命令
    daily_parser = subparsers.add_parser('daily', help='日线行情')
    daily_parser.add_argument('--stock', type=str, required=True, help='股票代码')
    
    # news 命令
    news_parser = subparsers.add_parser('news', help='财经新闻')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 执行命令
    if args.command == 'basic':
        query_basic(args.stock)
    
    elif args.command == 'indicators':
        query_indicators(args.stock)
    
    elif args.command == 'daily':
        query_daily(args.stock)
    
    elif args.command == 'news':
        query_news()

if __name__ == '__main__':
    main()
