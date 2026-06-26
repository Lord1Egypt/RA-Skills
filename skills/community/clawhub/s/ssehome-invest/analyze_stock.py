#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Investment Report Skill - 股票投资分析报告生成器

功能:
- 使用 baostock 获取近 3 年日K线数据并保存为 CSV
- 分析近三年走势与大盘相关性
- 分析近三个月月度表现和月线三连阳
- 分析近六个月横盘和突破状态
- 分析近一周技术指标 (MACD/RSI/DMI/BOLL)
- 分析均线系统 (5/14/21/89/250 日)
- 使用 Tavily 搜索最新市场热点资讯
- 生成 Markdown 和 PDF 格式投资报告

使用方法:
    python analyze_stock.py
    或
    from analyze_stock import analyze_stock
    analyze_stock("002328", "新朋股份")

作者:OpenClaw Assistant
版本:1.0.3
日期:2026-04-02
"""

try:
    import baostock as bs
    BAOSTOCK_AVAILABLE = True
except ImportError:
    BAOSTOCK_AVAILABLE = False

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import time
import random
import sys

# 设置控制台编码
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')


def get_tavily_api_key():
    """从环境变量或 .env 文件获取 API Key"""
    try:
        import os
        from dotenv import load_dotenv
        env_path = os.path.expanduser("~/.openclaw/.env")
        if os.path.exists(env_path):
            load_dotenv(env_path)
        api_key = os.getenv("TAVILY_API_KEY", "")
        if not api_key:
            return None
        return api_key
    except:
        return None


def search_tavily_news(query, max_results=3, search_depth="advance", time_range="week"):
    """
    使用 Tavily API 搜索新闻
    
    Args:
        query: 搜索关键词
        max_results: 最大结果数
        search_depth: 搜索深度 basic/advanced
        time_range: 时间范围 day/week/month
    
    Returns:
        搜索结果列表
    """
    api_key = get_tavily_api_key()
    if not api_key:
        print("⚠️ Tavily API Key 未配置，跳过新闻搜索")
        return []
    
    try:
        from tavily import TavilyClient
        client = TavilyClient(api_key=api_key)
        result = client.search(query, search_depth=search_depth, max_results=max_results)
        if "results" in result:
            return result["results"]
        return []
    except Exception as e:
        print(f"⚠️ Tavily 搜索失败: {e}")
        return []


def safe_baostock_call(func, max_retries=3, *args, **kwargs):
    """安全调用 baostock 函数,带重试机制"""
    for i in range(max_retries):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            if i < max_retries - 1:
                delay = random.uniform(2, 5)
                time.sleep(delay)
            else:
                return None
    return None


def get_kline_data_baostock(stock_symbol, start_date, end_date, adjust="qfq"):
    """使用 baostock 获取 K 线数据"""
    try:
        login_rs = bs.login()
        if login_rs.error_code != '0':
            print(f"❌ 登录失败:{login_rs.error_msg}")
            return None

        if stock_symbol.startswith("0") or stock_symbol.startswith("3"):
            market = "sz"
        else:
            market = "sh"
        full_symbol = f"{market}.{stock_symbol}"

        adjust_flag = "3" if adjust == "qfq" else "2" if adjust == "hfq" else "1"
        fields = "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg"
        
        rs = bs.query_history_k_data_plus(
            code=full_symbol, fields=fields,
            start_date=start_date, end_date=end_date,
            frequency="d", adjustflag=adjust_flag
        )

        if rs.error_code != '0':
            print(f"❌ 查询失败:{rs.error_msg}")
            bs.logout()
            return None

        data_list = []
        while rs.error_code == '0' and rs.next():
            data_list.append(rs.get_row_data())
        df = pd.DataFrame(data_list, columns=rs.fields)
        df = df[df['volume'].astype(str).str.strip() != '']

        bs.logout()

        if len(df) == 0:
            return None

        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)

        numeric_cols = ['open', 'high', 'low', 'close', 'preclose', 'volume', 'amount', 'turn', 'pctChg']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        col_mapping = {
            'open': '开盘', 'high': '最高', 'low': '最低', 'close': '收盘',
            'volume': '成交量', 'preclose': '昨收', 'pctChg': '涨跌幅', 'turn': '换手率'
        }
        df.rename(columns=col_mapping, inplace=True)
        df.sort_index(inplace=True)
        df = df.dropna()

        print(f"✅ 成功通过 baostock 获取 {len(df)} 条数据")
        return df
    except Exception as e:
        print(f"❌ baostock 获取异常:{str(e)[:100]}")
        try:
            bs.logout()
        except:
            pass
    return None


def get_index_data_baostock(index_code, start_date, end_date):
    """使用 baostock 获取指数数据"""
    try:
        bs.login()
        fields = "date,code,open,high,low,close,preclose,volume,amount,pctChg"
        rs = bs.query_history_k_data_plus(
            code=index_code, fields=fields,
            start_date=start_date, end_date=end_date, frequency="d"
        )

        if rs.error_code != '0':
            print(f"❌ 指数查询失败:{rs.error_msg}")
            bs.logout()
            return None

        data_list = []
        while rs.error_code == '0' and rs.next():
            data_list.append(rs.get_row_data())
        df = pd.DataFrame(data_list, columns=rs.fields)
        df = df[df['volume'].astype(str).str.strip() != '']

        type_mapping = {
            'code': 'str', 'pctChg': 'float64', 'high': 'float64',
            'low': 'float64', 'close': 'float64', 'preclose': 'float64',
            'amount': 'float64', 'volume': 'int64'
        }
        df = df.astype(type_mapping)
        bs.logout()

        if len(df) == 0:
            return None

        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        df.rename(columns={'open': '开盘', 'high': '最高', 'low': '最低', 'close': '收盘', 'volume': '成交量', 'pctChg': '涨跌幅'}, inplace=True)
        df.sort_index(inplace=True)
        return df
    except Exception as e:
        print(f"❌ 指数获取异常:{str(e)[:100]}")
        try:
            bs.logout()
        except:
            pass
    return None


def get_industry(p_full_symbol:str):
    try:
        bs.login()
        industry = ""
        rs_industry = bs.query_stock_industry(code=p_full_symbol)
        industry_data = []
        while rs_industry.error_code == '0' and rs_industry.next():
            industry_data.append(rs_industry.get_row_data())
        industry_df = pd.DataFrame(industry_data, columns=rs_industry.fields)
        if not industry_df.empty:
            if 'industry' in industry_df.columns:
                industry = industry_df['industry'].iloc[0]
            elif 'industryClassification' in industry_df.columns:
                industry = industry_df['industryClassification'].iloc[0]
            else:
                industry = industry_df.iloc[0].to_string()
        bs.logout()
        print(f"从 Baostock 获取股票行业名称: {industry}")
        return industry
    except Exception as e:
        print(f"获取股票行业分类失败: {e}")


def calculate_technical_indicators(df):
    """计算各种技术指标"""
    df = df.copy()
    df = df.sort_index()

    df['MA5'] = df['收盘'].rolling(window=5).mean()
    df['MA14'] = df['收盘'].rolling(window=14).mean()
    df['MA21'] = df['收盘'].rolling(window=21).mean()
    df['MA89'] = df['收盘'].rolling(window=89).mean()
    df['MA250'] = df['收盘'].rolling(window=250).mean()

    exp12 = df['收盘'].ewm(span=12).mean()
    exp26 = df['收盘'].ewm(span=26).mean()
    df['MACD'] = exp12 - exp26
    df['MACD_Signal'] = df['MACD'].ewm(span=9).mean()
    df['MACD_Hist'] = df['MACD'] - df['MACD_Signal']

    delta = df['收盘'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss.replace(0, np.nan)
    df['RSI'] = 100 - (100 / (1 + rs))

    df['BB_Middle'] = df['收盘'].rolling(window=20).mean()
    bb_std = df['收盘'].rolling(window=20).std()
    df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
    df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)

    n = 14
    high = df['最高']
    low = df['最低']
    close = df['收盘']
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    up_move = high - high.shift(1)
    down_move = low.shift(1) - low
    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0)

    atr = tr.ewm(alpha=1/n, adjust=False).mean()
    plus_dm_smooth = pd.Series(plus_dm, index=df.index).ewm(alpha=1/n, adjust=False).mean()
    minus_dm_smooth = pd.Series(minus_dm, index=df.index).ewm(alpha=1/n, adjust=False).mean()

    df['PlusDI'] = 100 * (plus_dm_smooth / atr)
    df['MinusDI'] = 100 * (minus_dm_smooth / atr)
    dx = 100 * abs(df['PlusDI'] - df['MinusDI']) / (df['PlusDI'] + df['MinusDI'])
    df['ADX'] = dx.ewm(alpha=1/n, adjust=False).mean()

    return df


def analyze_three_year_trend(stock_data, index_data, stock_symbol):
    """分析近三年走势强弱和与大盘的相关性"""
    if len(stock_data) < 100:
        return {"error": "数据不足"}

    stock_data = stock_data.copy()

    # 使用涨跌幅累乘计算总收益率
    stock_data['增长因子'] = 1+stock_data['涨跌幅']/100
    stock_data['累积净值'] = stock_data['增长因子'].cumprod()
    stock_data['累积净值'] = (stock_data['累积净值'] -1)*100
    stock_total_return =stock_data['累积净值'].iloc[-1]

    # 计算与大盘的相关性
    if index_data is not None and len(index_data) > 50:
        stock_returns = stock_data['涨跌幅'].dropna()
        index_returns = index_data['涨跌幅'].dropna()
        common_dates = stock_returns.index.intersection(index_returns.index)
        if len(common_dates) > 50:
            correlation = stock_returns.loc[common_dates].corr(index_returns.loc[common_dates])
            index_data['增长因子'] = 1+index_data['涨跌幅']/100
            index_data['累积净值'] = index_data['增长因子'].cumprod()
            index_data['累积净值'] = (index_data['累积净值'] -1)*100
            index_total_return = index_data['累积净值'].iloc[-1]
        else:
            correlation = 0
            index_total_return = 0
    else:
        correlation = 0
        index_total_return = 0

    volatility = stock_data['涨跌幅'].std() * np.sqrt(252)

    return {
        'stock_return': stock_total_return,
        'index_return': index_total_return,
        'correlation': correlation,
        'volatility': volatility,
        'stronger_than_market': stock_total_return > index_total_return
    }


def analyze_three_month_performance(stock_data):
    """分析近三个月每月涨跌幅和成交量变化"""
    if len(stock_data) < 60:
        return {"error": "数据不足"}

    recent_3m = stock_data.tail(90).copy()
    recent_3m['Month'] = recent_3m.index.to_period('M')
    recent_3m['增长因子'] = 1 + recent_3m['涨跌幅'] / 100

    # 按月份累乘增长因子计算月涨跌幅
    monthly_data = recent_3m.groupby('Month').agg({
        '收盘': ['first', 'last'],
        '成交量': 'sum',
        '增长因子': 'prod'
    })
    monthly_data['涨跌幅'] = (monthly_data[('增长因子', 'prod')] - 1) * 100
    monthly_data.columns = ['开盘', '收盘', '成交量', '增长因子', '涨跌幅']

    last_3 = monthly_data.tail(3)
    three_red_candles = all(last_3['涨跌幅'] > 0)

    return {
        'monthly_data': last_3,
        'three_red_candles': three_red_candles
    }


def analyze_six_month_consolidation(stock_data):
    """分析近六个月是否横盘及近期突破情况"""
    look_back_period = 120

    if len(stock_data) < look_back_period + 1:
        return {"error": "数据不足,无法计算"}

    current_price = stock_data['收盘'].iloc[-1]
    consolidation_data = stock_data.iloc[-(look_back_period + 1) : -1]

    recent_high = consolidation_data['收盘'].max()
    recent_low = consolidation_data['收盘'].min()
    price_range = recent_high - recent_low
    avg_price = consolidation_data['收盘'].mean()

    if avg_price == 0:
        return {"error": "平均价格为0,数据异常"}

    volatility_ratio = price_range / avg_price
    is_consolidation = volatility_ratio < 0.15

    if current_price > recent_high * 1.0316:
        breakout_status = "向上突破"
    elif current_price < recent_low * 0.98:
        breakout_status = "向下突破"
    else:
        breakout_status = "区间震荡"

    return {
        'volatility_ratio': round(volatility_ratio, 4),
        'is_consolidation': is_consolidation,
        'high': recent_high,
        'low': recent_low,
        'current_price': current_price,
        'breakout_status': breakout_status
    }


def analyze_weekly_technicals(stock_data):
    """分析近一周技术指标"""
    if len(stock_data) < 10:
        return {"error": "数据不足"}

    stock_data = calculate_technical_indicators(stock_data)
    recent_week = stock_data.tail(7)
    latest = recent_week.iloc[-1]

    macd_trend = "多头" if latest['MACD'] > latest['MACD_Signal'] else "空头"

    if latest['RSI'] > 70:
        rsi_status = "超买"
    elif latest['RSI'] < 30:
        rsi_status = "超卖"
    else:
        rsi_status = "中性"

    if latest['收盘'] > latest['BB_Upper']:
        boll_pos = "上轨上方"
    elif latest['收盘'] < latest['BB_Lower']:
        boll_pos = "下轨下方"
    else:
        boll_pos = "通道内"

    dmi_trend = "多头" if latest['PlusDI'] > latest['MinusDI'] else "空头"

    avg_vol = recent_week['成交量'].mean()
    vol_trend = "放量" if latest['成交量'] > avg_vol*1.5 else "缩量" if latest['成交量'] < avg_vol*0.7 else "常规"

    bullish_signals = sum([
        latest['MACD'] > latest['MACD_Signal'],
        30 < latest['RSI'] < 70,
        latest['PlusDI'] > latest['MinusDI'],
        latest['成交量'] > avg_vol
    ])

    if bullish_signals >= 3:
        overall = "看多"
    elif bullish_signals <= 1:
        overall = "看空"
    else:
        overall = "震荡"

    return {
        'macd': macd_trend,
        'rsi': latest['RSI'],
        'rsi_status': rsi_status,
        'boll': boll_pos,
        'dmi': dmi_trend,
        'volume': vol_trend,
        'overall': overall,
        'latest': latest
    }


def analyze_moving_averages(stock_data):
    """分析均线系统"""
    if len(stock_data) < 250:
        return {"error": "数据不足"}

    stock_data = calculate_technical_indicators(stock_data)
    latest = stock_data.iloc[-1]

    conditions = [
        ('14>21', latest['MA14'] > latest['MA21']),
        ('21>89', latest['MA21'] > latest['MA89']),
        ('89>250', latest['MA89'] > latest['MA250']),
        ('price>MA5', latest['收盘'] > latest['MA5']),
        ('MA5>14', latest['MA5'] > latest['MA14'])
    ]

    score = sum(1 for _, cond in conditions if cond)

    if score == 5:
        trend = "强势多头"
    elif score >= 3:
        trend = "部分多头"
    else:
        trend = "弱势或空头"

    return {
        'score': score,
        'conditions': conditions,
        'trend': trend,
        'latest': latest
    }


def search_and_analyze_news(stock_name, stock_symbol,industry):
    """使用 Tavily 搜索新闻并分析"""
    print(f"\n📰 正在搜索 {stock_name} 相关新闻...")
    
    news_sections = {}
    
    # 搜索 1: 公司动态
    print("  🔍 搜索公司动态...")
    results1 = search_tavily_news(f"{stock_name} {stock_symbol} 股价 最新 投资", max_results=5, search_depth="advanced")
    news_sections['公司动态'] = results1
    print(f"    找到 {len(results1)} 条")
    
    # 搜索 2: 产品业务
    print("  🔍 搜索产品业务...")
    results2 = search_tavily_news(f"{stock_name} 产品 技术 主营业务", max_results=3)
    news_sections['产品与业务'] = results2
    print(f"    找到 {len(results2)} 条")
    
    # 搜索 3: 行业动态
    print("  🔍 搜索行业动态...")
    results3 = search_tavily_news(f"{industry} 政策 市场 2026", max_results=3)
    news_sections['行业动态'] = results3
    print(f"    找到 {len(results3)} 条")
    
    return news_sections


def generate_markdown_report(stock_symbol, stock_name, industry, analyses, news_data=None):
    """生成 Markdown 格式投资报告"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    three_year = analyses.get('three_year', {})
    three_month = analyses.get('three_month', {})
    six_month = analyses.get('six_month', {})
    weekly = analyses.get('weekly', {})
    ma = analyses.get('moving_avg', {})

    report = f"""# 📊 投资研究报告

| 项目 | 内容 |
|------|------|
| **股票代码** | {stock_symbol} |
| **股票名称** | {stock_name} |
| **所属行业** | {industry} |
| **报告时间** | {current_time} |
| **数据周期** | 近 3 年 |

---

## 📋 执行摘要

均线系统评分 **{ma.get('score', 0)}/5**,短期信号 **{analyses.get('short_term', '观望')}**,趋势判断:**{ma.get('trend', '未知')}**

---

## 📈 详细分析

### 一、近三年走势分析

| 指标 | 数值 |
|------|------|
| 总收益率 | {three_year.get('stock_return', 0):.2f}% |
| 大盘收益率 | {three_year.get('index_return', 0):.2f}% |
| 相对强弱 | **{'强于大盘' if three_year.get('stronger_than_market') else '弱于大盘'}** |
| 与大盘相关性 | {three_year.get('correlation', 0):.3f} |
| 年化波动率 | {three_year.get('volatility', 0):.2f}% |

**走势评价**: {'✅ 股票表现优于大盘,建议关注' if three_year.get('stronger_than_market') else '⚠️ 股票表现弱于大盘,需谨慎'}

---

### 二、近三个月月度表现

"""
    monthly_data = three_month.get('monthly_data')
    if monthly_data is not None:
        report += "| 月份 | 开盘 | 收盘 | 涨跌幅 | 成交量 |\n"
        report += "|------|------|------|--------|--------|\n"
        for idx, row in monthly_data.iterrows():
            color = '🟢' if row['涨跌幅'] > 0 else '🔴'
            report += f"| {idx} | {row['开盘']:.2f} | {row['收盘']:.2f} | {color} {row['涨跌幅']:.2f}% | {row['成交量']:,.0f} |\n"

    report += f"""
**月线三连阳**: {'✅ 是' if three_month.get('three_red_candles') else '❌ 否'}

---

### 三、近六个月横盘分析

| 指标 | 数值 |
|------|------|
| 近 6 个月最高价 | {six_month.get('high', 0):.2f} |
| 近 6 个月最低价 | {six_month.get('low', 0):.2f} |
| 价格波动幅度 | {six_month.get('volatility_ratio', 0):.2%} |
| 横盘判断 | {'✅ 是 (波动<15%)' if six_month.get('is_consolidation') else '❌ 否 (波动较大)'} |
| 突破状态 | **{six_month.get('breakout_status', '未知')}** |

---

### 四、近一周技术指标分析

| 指标 | 状态 | 说明 |
|------|------|------|
| MACD | {'🟢' if weekly.get('macd') == '多头' else '🔴'} {weekly.get('macd', '未知')} | 趋势方向 |
| RSI(14) | {weekly.get('rsi', 0):.2f} | {weekly.get('rsi_status', '未知')} |
| DMI | {'🟢' if weekly.get('dmi') == '多头' else '🔴'} {weekly.get('dmi', '未知')} | 动向指标 |
| BOLL | {weekly.get('boll', '未知')} | 布林带位置 |
| 成交量 | {weekly.get('volume', '未知')} | 与均量对比 |

**综合判断**: {'🟢 看多' if weekly.get('overall') == '看多' else '🔴 看空' if weekly.get('overall') == '看空' else '⚪ 震荡'}

---

### 五、均线系统分析

| 均线条件 | 状态 | 说明 |
|----------|------|------|
| 14 日均线 > 21 日均线 | {'✅' if ma.get('conditions', [])[0][1] else '❌'} | 短期多头排列 |
| 21 日均线 > 89 日均线 | {'✅' if ma.get('conditions', [])[1][1] else '❌'} | 中期多头排列 |
| 89 日均线 > 250 日均线 | {'✅' if ma.get('conditions', [])[2][1] else '❌'} | 长期多头排列 |
| 股价 > 5 日均线 | {'✅' if ma.get('conditions', [])[3][1] else '❌'} | 短期强势 |
| 5 日均线 > 14 日均线 | {'✅' if ma.get('conditions', [])[4][1] else '❌'} | 超短期强势 |

**均线系统评分**: **{ma.get('score', 0)}/5**
**趋势判断**: **{ma.get('trend', '未知')}**

"""
    # 添加新闻分析部分
    if news_data:
        report += "\n---\n\n### 六、市场热点资讯分析\n\n"
        
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        
        for section_name, results in news_data.items():
            if results:
                report += f"**{section_name}** ({len(results)} 条):\n"
                for i, item in enumerate(results, 1):
                    title = item.get('title', '无标题')
                    report += f"{i}. {title}\n"
                    
                    # 简单情感判断
                    title_lower = title.lower()
                    if any(w in title_lower for w in ['利好', '增长', '突破', '上涨', '获', '赢', '创新高']):
                        positive_count += 1
                    elif any(w in title_lower for w in ['利空', '下跌', '亏损', '风险', '警示', '退市']):
                        negative_count += 1
                    else:
                        neutral_count += 1
                
                report += "\n"
        
        # 整体情绪判断
        if positive_count > negative_count + neutral_count:
            sentiment = "🟢 偏正面"
        elif negative_count > positive_count + neutral_count:
            sentiment = "🔴 偏负面"
        else:
            sentiment = "🟡 中性"
        
        report += f"**整体情绪**: {sentiment}\n\n"
        
        # 股价影响评估
        report += "**股价影响评估**:\n"
        if positive_count > negative_count:
            report += "- 短期：可能存在利好支撑，股价有上行压力\n"
            report += "- 中长期：需关注利好因素是否持续\n"
        elif negative_count > positive_count:
            report += "- 短期：可能存在利空压力，股价有下行风险\n"
            report += "- 中长期：需关注风险因素是否消除\n"
        else:
            report += "- 短期：市场情绪平稳，股价以震荡为主\n"
            report += "- 中长期：需关注基本面变化\n"

    report += f"""
---

## 💡 投资建议

| 周期 | 策略 | 说明 |
|------|------|------|
| **短期** | {analyses.get('short_term', '观望')} | 基于技术指标分析 |
| **中期** | {analyses.get('medium_term', '观察')} | 基于趋势分析 |
| **长期** | {analyses.get('long_term', '研究')} | 需结合基本面分析 |

---

## ⚠️ 风险提示

1. **市场风险**: 股市波动可能导致本金损失
2. **政策风险**: 行业政策变化可能影响公司经营
3. **技术风险**: 技术指标存在滞后性和失效可能
4. **数据风险**: 本报告基于公开数据,可能存在延迟

---

*免责声明:本报告由 AI 助手基于 baostock 数据生成,仅供参考,不构成投资建议。投资有风险,入市需谨慎。*

**数据来源**: baostock (https://baostock.com/baostock/index.php/%E9%A6%96%E9%A1%B5) | Tavily Search
**生成工具**: OpenClaw Investment Report Skill(ssehome-invest)
**版本**: 1.0.3
"""

    return report


def analyze_stock(stock_symbol="002328", stock_name="新朋股份"):
    """主函数:分析指定股票并生成投资报告"""
    print("=" * 60)
    print(f"开始分析股票:{stock_name} ({stock_symbol})")
    print("=" * 60)

    workspace_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_dir = os.path.join(workspace_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    # 仅仅对深圳和上海的证券进行分析
    if stock_symbol.startswith("0") or stock_symbol.startswith("3"):
        market = "sz"
    else:
        market = "sh"
    full_symbol = f"{market}.{stock_symbol}"

    # 获取股票基本信息
    industry = "Unknown"
    try:
        bs.login()
        rs_basic = bs.query_stock_basic(code=full_symbol)
        data_list = []
        while rs_basic.error_code == '0' and rs_basic.next():
            data_list.append(rs_basic.get_row_data())
        basic_df = pd.DataFrame(data_list, columns=rs_basic.fields)

        rs_industry = bs.query_stock_industry(code=full_symbol)
        industry_data = []
        while rs_industry.error_code == '0' and rs_industry.next():
            industry_data.append(rs_industry.get_row_data())
        industry_df = pd.DataFrame(industry_data, columns=rs_industry.fields)
        if not industry_df.empty:
            if 'industry' in industry_df.columns:
                industry = industry_df['industry'].iloc[0]
            elif 'industryClassification' in industry_df.columns:
                industry = industry_df['industryClassification'].iloc[0]
            else:
                industry = industry_df.iloc[0].to_string()
        bs.logout()

        if not basic_df.empty:
            stock_name = basic_df['code_name'][0]
            print(f"从 Baostock 获取股票名称: {stock_name}")
    except Exception as e:
        print(f"获取股票信息失败: {e}")

    end_date_bs = datetime.now().strftime("%Y-%m-%d")
    start_date_bs = (datetime.now() - timedelta(days=1095)).strftime("%Y-%m-%d")

    print(f"\n📡 正在获取 {start_date_bs} 至 {end_date_bs} 的 K 线数据...")

    if BAOSTOCK_AVAILABLE:
        print("🔸 使用 baostock 数据源...")
        stock_data = get_kline_data_baostock(stock_symbol, start_date_bs, end_date_bs)
    else:
        print("❌ baostock 未安装,请运行: pip install baostock")
        raise RuntimeError("baostock 未安装")

    if stock_data is None:
        raise RuntimeError("无法获取股票数据,请检查网络连接")

    print(f"\n🔍 执行各项分析...")
    analyses = {}

    print("  - 三年趋势分析...")
    index_data = get_index_data_baostock("sh.000300", start_date_bs, end_date_bs)
    analyses['three_year'] = analyze_three_year_trend(stock_data, index_data, stock_symbol)
    print(f"    三年收益率:{analyses['three_year'].get('stock_return', 0):.2f}%")

    print("  - 三个月表现分析...")
    analyses['three_month'] = analyze_three_month_performance(stock_data)
    print(f"    月线三连阳:{'是' if analyses['three_month'].get('three_red_candles') else '否'}")

    print("  - 六个月横盘分析...")
    analyses['six_month'] = analyze_six_month_consolidation(stock_data)
    print(f"    横盘判断:{'是' if analyses['six_month'].get('is_consolidation') else '否'}")

    print("  - 一周技术分析...")
    analyses['weekly'] = analyze_weekly_technicals(stock_data)
    print(f"    MACD: {analyses['weekly'].get('macd', '未知')}, "
          f"RSI: {analyses['weekly'].get('rsi', 0):.2f} ({analyses['weekly'].get('rsi_status', '未知')})")

    print("  - 均线系统分析...")
    analyses['moving_avg'] = analyze_moving_averages(stock_data)
    print(f"    均线评分:{analyses['moving_avg'].get('score', 0)}/5,"
          f"趋势:{analyses['moving_avg'].get('trend', '未知')}")

    # 生成投资建议
    ma_score = analyses['moving_avg'].get('score', 0)
    weekly_overall = analyses['weekly'].get('overall', '震荡')

    if ma_score >= 4 and weekly_overall == '看多':
        analyses['short_term'] = '买入/增持'
        analyses['medium_term'] = '持有'
    elif ma_score <= 2 and weekly_overall == '看空':
        analyses['short_term'] = '卖出/减仓'
        analyses['medium_term'] = '观望'
    else:
        analyses['short_term'] = '观望'
        analyses['medium_term'] = '观察'

    analyses['long_term'] = '深入研究'

    # Tavily 新闻搜索
    news_data = search_and_analyze_news(stock_name, stock_symbol, industry)

    # 生成 Markdown 报告
    print("\n📝 生成 Markdown 报告...")
    markdown_report = generate_markdown_report(stock_symbol, stock_name, industry, analyses, news_data)

    md_path = os.path.join(data_dir, f"{stock_symbol}_investment_report.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(markdown_report)
    print(f"✅ Markdown 报告已保存:{md_path}")

    print("\n" + "=" * 60)
    print("📊 分析完成!")
    print("=" * 60)

    return markdown_report


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        analyze_stock(sys.argv[1], sys.argv[2])
    else:
        analyze_stock("002328", "新朋股份")
