#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PyWenCai 技能核心函数
"""

import pandas as pd
from bs4 import BeautifulSoup

def _html_to_markdown(html_str):
    """将HTML表格转换为Markdown格式"""
    if not html_str or '<table' not in html_str:
        return str(html_str) if html_str else ''
    
    try:
        soup = BeautifulSoup(html_str, 'html.parser')
        tables = soup.find_all('table')
        if not tables:
            return str(html_str)
        
        # 取第一个表格
        table = tables[0]
        rows = table.find_all('tr')
        md_lines = []
        
        for i, row in enumerate(rows):
            cells = row.find_all(['th', 'td'])
            texts = [c.get_text(strip=True) for c in cells]
            md_lines.append('| ' + ' | '.join(texts) + ' |')
            if i == 0:
                md_lines.append('| ' + ' | '.join(['---'] * len(texts)) + ' |')
        
        return '\n'.join(md_lines)
    except Exception:
        return str(html_str)

def search(query, page=1, perpage=50, sort_key=None, sort_order='desc', loop=False):
    """
    搜索同花顺问财数据
    
    Args:
        query (str): 查询关键词，如 'A股涨停'
        page (int): 页码，从1开始
        perpage (int): 每页返回条数（默认50，最大100）
        sort_key (str): 排序字段，如 '涨跌幅'、'成交量'
        sort_order (str): 'asc' 升序 或 'desc' 降序
        loop (bool): 是否自动翻页合并所有结果
    
    Returns:
        pandas.DataFrame: 查询结果
    """
    try:
        import pywencai
    except ImportError:
        raise ImportError("请先安装 pywencai: pip install pywencai")
    
    params = {
        'query': query,
        'page': page,
        'perpage': perpage,
        'loop': loop
    }
    
    if sort_key:
        params['sort_key'] = sort_key
    if sort_order:
        params['sort_order'] = sort_order
    
    try:
        result = pywencai.get(**params)
        if result is None:
            raise ValueError("问财返回空数据")
        
        # 处理不同类型返回值
        if isinstance(result, pd.DataFrame):
            df = result
        elif isinstance(result, dict):
            # dict 可能是 {col: value} 单行，或 {col: [list]} 多行
            # 检查是否所有 values 都是标量（非list/dict）
            if all(not isinstance(v, (list, dict)) for v in result.values()):
                # 单行 → 包装成一行 DataFrame
                df = pd.DataFrame([result])
            else:
                # dict of lists → 标准 DataFrame
                df = pd.DataFrame(result)
        elif isinstance(result, list):
            df = pd.DataFrame(result)
        else:
            # 尝试直接转换
            df = pd.DataFrame(result)
        
        return df
    except Exception as e:
        raise RuntimeError(f"pywencai查询失败 (query='{query}'): {e}") from e


def hot_sectors(limit=5):
    """获取热门概念/板块"""
    keywords = [
        '芯片概念股',
        '人工智能概念股',
        '新能源汽车概念股',
        '医药生物概念股',
        '电子元件概念股',
        '国防军工概念股',
        '计算机概念股'
    ]
    results = {}
    for kw in keywords[:limit]:
        try:
            df = search(query=kw, perpage=10)
            results[kw] = df
        except Exception as e:
            results[kw] = None
    return results


def top_gainers(n=10):
    """涨幅榜前N名"""
    df = search(
        query=f'沪深A股涨幅前{n}',
        sort_key='涨跌幅',
        sort_order='desc'
    )
    return df.head(n) if len(df) > n else df


def top_losers(n=10):
    """跌幅榜前N名"""
    df = search(
        query=f'沪深A股跌幅前{n}',
        sort_key='涨跌幅',
        sort_order='asc'
    )
    return df.head(n) if len(df) > n else df


def dragon_tiger_list():
    """今日龙虎榜"""
    return search(query='今日龙虎榜')


def search_stock_by_code(code, info_type='行情'):
    """
    查询特定股票信息
    
    说明：个股查询返回的 dict 中包含嵌套的 title_content (DataFrame)。
    本函数自动提取 title_content 并返回内部的 DataFrame（包含行情/财务等字段）。
    
    Args:
        code (str): 股票代码，如 '600519' 或 '300750'
        info_type (str): 查询类型，'行情'、'财务指标'、'研报评级' 等
    
    Returns:
        pandas.DataFrame: 提取后的表格数据（列如：股票代码、股票名称、最新价等）
    """
    query = f'{code} {info_type}'
    df = search(query=query)
    
    # 检查是否有嵌套 DataFrame
    if 'title_content' in df.columns:
        # 如果该列的值是 DataFrame（多行数据），直接返回它
        if len(df) > 0:
            sample = df['title_content'].iloc[0]
            if isinstance(sample, pd.DataFrame):
                return sample
    
    return df


if __name__ == '__main__':
    # 简单测试
    print("=== PyWenCai 技能测试 ===\n")
    try:
        print("1. 查询'A股涨停'...")
        df = search('A股涨停', perpage=5)
        print(f"   成功！返回 {len(df)} 条记录")
        if len(df) > 0:
            print(df.head(2).to_string(index=False))
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")
        print("   请确保已安装 pywencai: pip install pywencai")
