#!/usr/bin/env python3
"""
PyWenCai 股票数据获取示例
"""

import sys
sys.path.insert(0, '/tmp/mootdx')  # 如果库安装在这里

import pywencai


def get_limit_up():
    """获取今日涨停股票"""
    df = pywencai.get(query='A股涨停', sort_key='涨跌幅', sort_order='desc')
    return df


def get_limit_down():
    """获取今日跌停股票"""
    df = pywencai.get(query='A股跌停')
    return df


def get_top_gainers(num=10):
    """获取涨幅前N股票"""
    df = pywencai.get(query=f'沪深A股涨幅前{num}', sort_key='涨跌幅', sort_order='desc')
    return df


def get_stock_financial(code):
    """获取个股财务数据"""
    df = pywencai.get(query=f'{code} 财务指标')
    return df


def get_money_flow():
    """获取资金流向"""
    df = pywencai.get(query='主力净流入最多的股票', sort_key='主力净流入', sort_order='desc')
    return df


def get_concept_stocks(concept):
    """获取概念板块股票"""
    df = pywencai.get(query=f'{concept}概念股')
    return df


def search(query):
    """通用查询"""
    df = pywencai.get(query=query, perpage=50)
    return df


if __name__ == '__main__':
    # 示例1: 获取涨停股
    print("=" * 50)
    print("示例1: 获取今日涨停股票")
    print("=" * 50)
    df = get_limit_up()
    print(df.head())
    
    # 示例2: 获取涨幅前10
    print("\n" + "=" * 50)
    print("示例2: 涨幅前10")
    print("=" * 50)
    df = get_top_gainers(10)
    print(df)
    
    # 示例3: 查询个股财务
    print("\n" + "=" * 50)
    print("示例3: 茅台财务指标")
    print("=" * 50)
    df = get_stock_financial('600519')
    print(df)
    
    # 示例4: 资金流向
    print("\n" + "=" * 50)
    print("示例4: 主力净流入")
    print("=" * 50)
    df = get_money_flow()
    print(df.head())
    
    # 示例5: 概念板块
    print("\n" + "=" * 50)
    print("示例5: AI概念股")
    print("=" * 50)
    df = get_concept_stocks('人工智能')
    print(df.head())
