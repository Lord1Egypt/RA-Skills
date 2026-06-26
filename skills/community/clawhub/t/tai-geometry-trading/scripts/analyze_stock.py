#!/usr/bin/env python3
"""
太几何交易 - 完整版分析脚本
包含核心因子 + 大模型辅助因子分析
"""

import pandas as pd
import numpy as np
import requests
import json
import os
import sys

sys.path.append('/root/.openclaw/workspace/skills/tai-geometry-trading/scripts')

import config
from kline_geometry import analyze_geometry_structure
from macd_wind_tunnel import analyze_multi_period_macd
from volume_shrinkage import analyze_multi_period_shrinkage


def call_llm(prompt, max_tokens=500):
    """调用大模型API"""
    llm_config = config.get_llm_config()
    if not llm_config:
        return None
    
    provider = llm_config['provider']
    api_key = llm_config['api_key']
    base_url = llm_config['base_url']
    model = llm_config['model']
    
    headers = {"Content-Type": "application/json"}
    
    if provider == "openai":
        headers["Authorization"] = f"Bearer {api_key}"
        url = f"{base_url}/chat/completions"
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
    elif provider == "anthropic":
        headers["x-api-key"] = api_key
        headers["anthropic-version"] = "2023-06-01"
        url = f"{base_url}/v1/messages"
        data = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}]
        }
    elif provider == "minimax":
        headers["Authorization"] = f"Bearer {api_key}"
        url = f"{base_url}/chat/completions"
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
    elif provider == "deepseek":
        headers["Authorization"] = f"Bearer {api_key}"
        url = f"{base_url}/chat/completions"
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
    elif provider == "qwen":
        headers["Authorization"] = f"Bearer {api_key}"
        url = f"{base_url}/chat/completions"
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
    elif provider == "custom":
        headers["Authorization"] = f"Bearer {api_key}"
        url = f"{base_url}/chat/completions"
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
    else:
        return None
    
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=60)
        if resp.status_code == 200:
            result = resp.json()
            
            # 解析不同provider的响应格式
            if provider == "anthropic":
                return result['content'][0]['text']
            else:
                return result['choices'][0]['message']['content']
        else:
            print(f"API错误: {resp.status_code} - {resp.text[:200]}")
            return None
    except Exception as e:
        print(f"调用失败: {e}")
        return None


def get_auxiliary_scores(stock_code, stock_name, price_data, macd_data):
    """使用大模型获取辅助因子打分"""
    
    if not config.get_llm_enabled():
        return None
    
    recent = price_data.tail(10)
    price_info = []
    for _, row in recent.iterrows():
        change = (row['close'] - row['open']) / row['open'] * 100
        price_info.append(f"{row['date']}: 开{row['open']:.2f} 收{row['close']:.2f} 涨跌{change:+.1f}%")
    
    price_str = "\n".join(price_info)
    macd_str = f"MACD方向: {macd_data.get('resonance_type', '未知')}"
    
    prompt = f"""你是股票分析师。请根据以下股票信息进行分析，直接给出辅助因子打分，只输出一句话分析。

格式：
基本面分析 得分:X 一句话（含营收增长、PEG、经营现金流、行业地位等）
情绪面分析 得分:X 一句话（含股价波动、概念题材、市场热点等）
AI预测分析 得分:X 一句话（发散性预测，可结合政策、资金面、技术形态等）

股票:{stock_name} 代码:{stock_code}
近期走势:{price_str}
技术面:{macd_str}"""

    result = call_llm(prompt, max_tokens=800)
    return result


def parse_auxiliary_scores(result_text):
    """解析辅助因子打分结果"""
    scores = {'fund': 6, 'sentiment': 6, 'ai': 6}
    
    if not result_text:
        return scores
    
    try:
        lines = result_text.split('\n')
        for line in lines:
            line = line.strip()
            if '基本面' in line and '得分' in line:
                try:
                    score = int([x for x in line if x.isdigit()][0])
                    scores['fund'] = min(10, max(0, score))
                except:
                    pass
            elif '情绪面' in line and '得分' in line:
                try:
                    score = int([x for x in line if x.isdigit()][0])
                    scores['sentiment'] = min(10, max(0, score))
                except:
                    pass
            elif 'AI预测' in line and '得分' in line:
                try:
                    score = int([x for x in line if x.isdigit()][0])
                    scores['ai'] = min(10, max(0, score))
                except:
                    pass
    except Exception as e:
        print(f"解析错误: {e}")
    
    return scores


def get_stock_data_tengxun(code, days=320):
    """使用腾讯API获取股票K线数据"""
    if code.startswith('6'):
        market = 'sh' + code
    else:
        market = 'sz' + code
    
    url = 'https://web.ifzq.gtimg.cn/appstock/app/fqkline/get'
    params = {'_var': 'kline_dayqfq', 'param': f'{market},day,,,{days},qfq'}
    
    try:
        r = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        data = json.loads(r.text.split('=')[1])
        klines = data['data'][market]['qfqday']
        clean_klines = [k for k in klines if len(k) == 6]
        
        df = pd.DataFrame(clean_klines, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        for c in ['open', 'high', 'low', 'close', 'volume']:
            df[c] = pd.to_numeric(df[c], errors='coerce')
        df = df.sort_values('date').reset_index(drop=True)
        return df
    except Exception as e:
        print(f"腾讯API获取失败: {e}")
        return None


def get_stock_data_akshare(stock_code):
    """使用AkShare获取股票数据 (备用)"""
    import akshare as ak
    
    if stock_code.startswith('6'):
        symbol = f"sh{stock_code}"
    else:
        symbol = f"sz{stock_code}"
    
    try:
        df = ak.stock_zh_a_hist(symbol=symbol, start_date='20240101', adjust='qfq')
        if df is not None and not df.empty:
            df = df.rename(columns={
                '日期': 'date', '开盘': 'open', '收盘': 'close',
                '最高': 'high', '最低': 'low', '成交量': 'volume'
            })
            df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
        else:
            return None
    except Exception as e:
        return None
    
    return df


def get_stock_data_tushare(stock_code):
    """使用Tushare获取股票数据"""
    import tushare as ts
    
    ts.set_token(config.TUSHARE_TOKEN)
    pro = ts.pro_api()
    
    ts_code = f"{stock_code}.SH" if stock_code.startswith('6') else f"{stock_code}.SZ"
    
    try:
        df = pro.daily(ts_code=ts_code, start_date='20240101', end_date='20261231')
        df = df.sort_values('trade_date')
        df = df.rename(columns={'trade_date': 'date', 'vol': 'volume'})
        df['date'] = pd.to_datetime(df['date']).astype(str)
        return df
    except Exception as e:
        print(f"Tushare获取失败: {e}")
        return None


def get_stock_data(stock_code):
    """根据配置获取股票数据"""
    source = config.get_data_source()
    print(f"数据源: {source}")
    
    df_daily = None
    
    if source == "tushare":
        df_daily = get_stock_data_tushare(stock_code)
    elif source == "akshare":
        df_daily = get_stock_data_tengxun(stock_code)
        if df_daily is None:
            df_daily = get_stock_data_akshare(stock_code)
    
    if df_daily is None or df_daily.empty:
        print("❌ 数据获取失败")
        return None
    
    # 生成各周期数据
    df_daily['date'] = pd.to_datetime(df_daily['date'])
    
    df_weekly = df_daily.set_index('date').resample('W-FRI').agg({
        'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'
    }).dropna().reset_index()
    
    df_monthly = df_daily.set_index('date').resample('ME').agg({
        'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'
    }).dropna().reset_index()
    
    df_2daily = df_daily.set_index('date').resample('2D').agg({
        'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'
    }).dropna().reset_index()
    
    df_8daily = df_daily.set_index('date').resample('8D').agg({
        'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'
    }).dropna().reset_index()
    
    for df_obj in [df_daily, df_weekly, df_monthly, df_2daily, df_8daily]:
        df_obj['date'] = df_obj['date'].astype(str)
    
    return {
        'daily': df_daily,
        'weekly': df_weekly,
        'monthly': df_monthly,
        '2daily': df_2daily,
        '8daily': df_8daily
    }


def analyze_stock(stock_code):
    """完整版分析"""
    print("=" * 60)
    print("  太几何交易 - 完整版")
    print("  (核心因子 + 大模型AI辅助分析)")
    print("=" * 60)
    
    # 检查数据源配置
    if config.get_data_source() == "tushare" and not config.TUSHARE_TOKEN:
        print("❌ 请先在 config.py 中配置 TUSHARE_TOKEN")
        return
    
    # 检查大模型配置
    llm_config = config.get_llm_config()
    if not llm_config:
        print("⚠️ 未配置大模型API Key，将使用默认辅助分数")
        print(f"  当前支持: openai, anthropic, minimax, deepseek, qwen, 自定义")
        print("  完整版需要配置任意一个LLM的API Key")
        print("  或直接运行核心版: python analyze_stock_core.py <股票代码>")
        print()
    else:
        print(f"✅ 大模型({llm_config['provider']}): 已配置")
    
    data_dict = get_stock_data(stock_code)
    
    if not data_dict:
        print("❌ 数据获取失败")
        return
    
    daily = data_dict['daily']
    latest = daily.iloc[-1]
    
    # 获取股票名称
    try:
        import akshare as ak
        info = ak.stock_individual_info_em(symbol=stock_code)
        stock_name = info[info['item'] == '股票简称']['value'].values[0]
    except:
        stock_name = "未知"
    
    print(f"\n{'='*55}")
    print(f"  {stock_name} ({stock_code}) 股票分析")
    print(f"{'='*55}")
    print(f"最新价格: {latest['close']}元")
    
    # 核心因子
    geometry = analyze_geometry_structure(data_dict['daily'])
    geo_score = geometry['total_score']
    geo_desc = geometry.get('description', ['无描述'])
    
    macd = analyze_multi_period_macd(data_dict)
    macd_score = macd['resonance_score']
    macd_dir = macd.get('resonance_type', 'neutral')
    macd_desc = macd.get('description', ['无描述'])
    
    shrink = analyze_multi_period_shrinkage(data_dict)
    shrink_score = shrink['total_score']
    shrink_desc = shrink.get('description', ['无描述'])
    
    print(f"\n【技术分析】")
    print(f"  几何结构: {geo_score}/25 - {geo_desc[0] if geo_desc else '无'}")
    print(f"  MACD风洞: {macd_score}/30 ({'看涨' if macd_dir=='bullish' else ('看跌' if macd_dir=='bearish' else '中性')})")
    print(f"  缩量短线: {shrink_score}/15 - {shrink_desc[0] if isinstance(shrink_desc, list) and shrink_desc else '无'}")
    
    print(f"\n【MACD详情】")
    for p in ['monthly', 'weekly', 'daily']:
        if p in macd:
            r = macd[p]
            direction = r.get('direction', '-')
            desc = r.get('description', [])
            desc_str = desc[0] if desc else '无'
            print(f"  {p}: {direction} - {desc_str}")
    
    # 辅助因子 (大模型)
    fund_score = sent_score = ai_score = 6
    
    if llm_config:
        print(f"\n正在获取辅助因子分析(AI)...")
        aux_result = get_auxiliary_scores(stock_code, stock_name, daily, macd)
        
        if aux_result:
            scores = parse_auxiliary_scores(aux_result)
            fund_score = scores['fund']
            sent_score = scores['sentiment']
            ai_score = scores['ai']
            
            fund_desc = sent_desc = ai_desc = ""
            for line in aux_result.split('\n'):
                line = line.strip()
                if '基本面' in line and '得分' in line:
                    idx = line.find('得分:')
                    if idx != -1:
                        fund_desc = line[idx+3:].lstrip('0123456789').strip()[:50]
                elif '情绪面' in line and '得分' in line:
                    idx = line.find('得分:')
                    if idx != -1:
                        sent_desc = line[idx+3:].lstrip('0123456789').strip()[:50]
                elif 'AI预测' in line and '得分' in line:
                    idx = line.find('得分:')
                    if idx != -1:
                        ai_desc = line[idx+3:].lstrip('0123456789').strip()[:50]
            
            print(f"\n【辅助因子】")
            print(f"  基本面: {fund_score}/10 - {fund_desc}")
            print(f"  情绪面: {sent_score}/10 - {sent_desc}")
            print(f"  AI预测: {ai_score}/10 - {ai_desc}")
        else:
            print("  获取失败，使用默认分数")
    else:
        print(f"\n【辅助因子】(默认分数)")
        print(f"  基本面: {fund_score}/10 - (未配置API)")
        print(f"  情绪面: {sent_score}/10 - (未配置API)")
        print(f"  AI预测: {ai_score}/10 - (未配置API)")
    
    # 总分
    if macd_dir == 'bearish':
        adjusted_macd = -abs(macd_score)
        tech_score = (geo_score + adjusted_macd + shrink_score) * 0.6
        total = max(0, tech_score) + fund_score + sent_score + ai_score
    elif macd_dir == 'bullish':
        total = geo_score + macd_score + shrink_score + fund_score + sent_score + ai_score
    else:
        total = geo_score + macd_score + shrink_score + fund_score + sent_score + ai_score
    
    # 判断建议 (完整版100分制，与核心版70分对应)
    # 100分制: 75以上=强烈看涨, 50以上=看涨, 25以上=看跌
    if total >= 75:
        recommendation = "强烈看涨"
    elif total >= 50:
        recommendation = "看涨"
    elif total >= 25:
        recommendation = "看跌"
    else:
        recommendation = "强烈看跌"
    
    print(f"\n{'='*55}")
    print(f"【综合评分】{int(total)}/100分")
    print(f"【操作建议】 {recommendation}")
    print(f"{'='*55}")


if __name__ == '__main__':
    import sys
    code = sys.argv[1] if len(sys.argv) > 1 else '002378'
    analyze_stock(code)