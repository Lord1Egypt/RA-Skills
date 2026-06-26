#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票基本面数据获取脚本

使用聚宽 JQData API 获取基本面数据（PE、PB、市值等）

使用方法:
    # 先配置聚宽账号（环境变量）
    export JQDATA_PHONE="你的手机号"
    export JQDATA_PASSWORD="你的密码"
    
    python scripts/stock_fundamentals.py --codes 300413.SZ,300251.SZ
    python scripts/stock_fundamentals.py --codes 600519.SH --date 2025-01-20
"""

import argparse
import os
import sys

def check_jqdata():
    """检查聚宽是否可用"""
    phone = os.environ.get('JQDATA_PHONE')
    password = os.environ.get('JQDATA_PASSWORD')
    
    if not phone or not password:
        print("❌ 未配置聚宽账号")
        print("请先设置环境变量:")
        print('  export JQDATA_PHONE="你的手机号"')
        print('  export JQDATA_PASSWORD="你的密码"')
        print()
        print("或使用交互式配置:")
        print("  python scripts/jq_login.py")
        sys.exit(1)
    
    try:
        import jqdatasdk as jq
        jq.auth(phone, password)
        return jq
    except ImportError:
        print("❌ jqdatasdk 未安装，请运行: pip install jqdatasdk")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 聚宽登录失败: {e}")
        sys.exit(1)

def normalize_code(code):
    """标准化股票代码为聚宽格式"""
    if '.' in code:
        return code  # 已经是聚宽格式
    # 纯数字格式，尝试判断交易所
    if code.startswith('6'):
        return f'{code}.XSHG'
    else:
        return f'{code}.XSHE'

def get_fundamentals(jq, codes, date=None):
    """获取基本面数据"""
    results = []
    
    for code in codes:
        jq_code = normalize_code(code)
        print(f"正在查询 {code} ({jq_code}) 的基本面数据...")
        
        try:
            # 获取估值数据（PE、PB、市值）
            val = jq.get_valuation(jq_code, start_date=date, end_date=date)
            
            if val is not None and len(val) > 0:
                row = val.iloc[0]
                result = {
                    'code': code,
                    'market_cap': row.get('market_cap', None),  # 总市值（亿元）
                    'pe_ratio': row.get('pe_ratio', None),
                    'pb_ratio': row.get('pb_ratio', None),
                    'roe': row.get('roe', None),
                    'revenue': row.get('revenue', None),
                    'net_profit': row.get('net_profit', None),
                }
                results.append(result)
                
                # 打印结果
                print(f"  ✅ 总市值: {result['market_cap']:.2f}亿" if result['market_cap'] else "  ✅ 总市值: N/A")
                print(f"     PE: {result['pe_ratio']:.2f}" if result['pe_ratio'] else "     PE: N/A")
                print(f"     PB: {result['pb_ratio']:.2f}" if result['pb_ratio'] else "     PB: N/A")
            else:
                print(f"  ⚠️  无数据（可能日期超出权限范围）")
                # 尝试不用日期过滤
                val_all = jq.get_valuation(jq_code)
                if val_all is not None and len(val_all) > 0:
                    row = val_all.iloc[-1]
                    print(f"  最近日期 {val_all.index[-1].date() if hasattr(val_all.index[-1], 'date') else val_all.index[-1]}:")
                    print(f"    总市值: {row.get('market_cap', 'N/A')}")
                    print(f"    PE: {row.get('pe_ratio', 'N/A')}")
                    print(f"    PB: {row.get('pb_ratio', 'N/A')}")
                    
        except Exception as e:
            print(f"  ❌ 查询失败: {e}")
    
    return results

def get_financial_statements(jq, code, report_date='2024-12-31'):
    """获取财务报表（利润表、资产负债表、现金流量表）"""
    jq_code = normalize_code(code)
    
    print(f"\n财务报表 ({report_date}):")
    
    try:
        from jqdatasdk import finance
        
        # 利润表
        q_income = jq.query(finance.STK_INCOME_STATEMENT).filter(
            finance.STK_INCOME_STATEMENT.code == jq_code
        )
        df_income = finance.run_query(q_income)
        
        if df_income is not None and len(df_income) > 0:
            # 找到最近的报告期
            latest = df_income[df_income['report_date'] == report_date]
            if len(latest) > 0:
                r = latest.iloc[0]
                print(f"  营业收入: {r.get('operating_revenue', 'N/A'):.2f}" if r.get('operating_revenue') else "  营业收入: N/A")
                print(f"  净利润: {r.get('net_profit', 'N/A'):.2f}" if r.get('net_profit') else "  净利润: N/A")
            else:
                print(f"  ⚠️  无 {report_date} 报告期数据")
        else:
            print("  ⚠️  无利润表数据")
            
    except Exception as e:
        print(f"  ⚠️  财务数据查询失败: {e}")

def main():
    parser = argparse.ArgumentParser(description='获取股票基本面数据')
    parser.add_argument('--codes', type=str, required=True, help='股票代码，逗号分隔，如 300413.SZ,300251.SZ')
    parser.add_argument('--date', type=str, help='查询日期，如 2025-01-20')
    parser.add_argument('--financials', action='store_true', help='同时获取财务报表')
    args = parser.parse_args()
    
    codes = [c.strip() for c in args.codes.split(',')]
    
    print(f"\n📊 正在查询 {len(codes)} 只股票的基本面数据...")
    print(f"查询日期: {args.date or '最新可用日期'}")
    print()
    
    jq = check_jqdata()
    
    # 显示积分信息
    try:
        count = jq.get_query_count()
        print(f"积分余额: {count.get('spare', 'N/A')} / {count.get('total', 'N/A')}")
        print()
    except:
        pass
    
    results = get_fundamentals(jq, codes, args.date)
    
    if args.financials:
        for code in codes:
            get_financial_statements(jq, code)
    
    print(f"\n✅ 完成，共获取 {len(results)}/{len(codes)} 只股票数据")

if __name__ == '__main__':
    main()
