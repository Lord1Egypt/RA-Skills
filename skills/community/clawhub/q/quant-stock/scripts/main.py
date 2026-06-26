import pandas as pd
import requests
import datetime
import time
import sys
import concurrent.futures
import os
import re
import json

import io

# --- Config ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(BASE_DIR, "daily_report.txt")
POOL_FILE = os.path.join(BASE_DIR, "stock_pool.csv")
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

# Feishu Config
FEISHU_CONFIG_FILE = os.path.join(os.path.dirname(BASE_DIR), "..", "feishu_config.json")
FEISHU_CHAT_ID = "oc_0142a8d63ace2e4db368ae7b607e702f"  # Updated to standalone bot chat ID

def fetch_tencent_history(code):
    # ... (Keep existing fetch logic)
    code = str(code).zfill(6)
    prefix = "sh" if code.startswith(('6', '9')) else "sz"
    symbol = f"{prefix}{code}"
    url = f"http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayqfq&param={symbol},day,,,100,qfq"
    try:
        r = requests.get(url, headers=HEADERS, timeout=5)
        if r.status_code != 200: return pd.DataFrame()
        content = r.text
        json_str = content.split('=', 1)[1]
        data = pd.read_json(io.StringIO(json_str))
        stock_data = data['data'].get(symbol, {})
        k_data = stock_data.get('qfqday', stock_data.get('day', []))
        if not k_data: return pd.DataFrame()
        df = pd.DataFrame(k_data)
        if df.shape[1] < 6: return pd.DataFrame()
        df = df.iloc[:, :6]
        df.columns = ['date', 'open', 'close', 'high', 'low', 'vol']
        for col in ['open', 'close', 'high', 'low', 'vol']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        return df
    except:
        return pd.DataFrame()

def analyze_stock_basic(row):
    """
    Round 1: Individual Technical & Trend Analysis
    Returns: {code, name, industry, score, tags, price, change_pct, vol, close_series}
    """
    code = str(row['code']).zfill(6)
    name = row['name']
    industry = row.get('industry', '其他')
    
    df = fetch_tencent_history(code)
    if df.empty or len(df) < 30: return None
    
    score = 0
    tags = []
    
    close = df['close']
    ma5 = close.rolling(5).mean()
    
    # 1. Technical
    # MACD
    exp12 = close.ewm(span=12, adjust=False).mean()
    exp26 = close.ewm(span=26, adjust=False).mean()
    macd = exp12 - exp26
    signal = macd.ewm(span=9, adjust=False).mean()
    
    if macd.iloc[-1] > signal.iloc[-1] and macd.iloc[-2] <= signal.iloc[-2]:
        score += 3
        tags.append("MACD金叉")
        
    # Magic 9
    c_ref4 = close.shift(4)
    if (close < c_ref4).iloc[-9:].all():
        score += 5
        tags.append("神奇九转")
        
    # MA Regression
    recent_ma5 = ma5.iloc[-20:]
    if len(recent_ma5) == 20 and ma5.iloc[-1] <= recent_ma5.min() * 1.01:
        score += 5
        tags.append("均线回归")

    # 3. Trend (Individual)
    p_now = close.iloc[-1]
    p_3ago = close.iloc[-4] if len(close) > 4 else close.iloc[0]
    pct_3d = (p_now - p_3ago) / p_3ago
    
    # Calculate daily change for Market Sentiment
    p_prev = close.iloc[-2]
    daily_change = (p_now - p_prev) / p_prev
    vol_now = df['vol'].iloc[-1]
    vol_prev = df['vol'].iloc[-2]
    vol_ratio = vol_now / vol_prev if vol_prev > 0 else 1

    # Calculate 2-day amplitude for Module 2.3
    high1, low1 = df['high'].iloc[-1], df['low'].iloc[-1]
    high2, low2 = df['high'].iloc[-2], df['low'].iloc[-2]
    pre_close1 = p_prev
    pre_close2 = df['close'].iloc[-3] if len(df) > 2 else pre_close1
    
    amp1 = (high1 - low1) / pre_close1 if pre_close1 > 0 else 0
    amp2 = (high2 - low2) / pre_close2 if pre_close2 > 0 else 0
    high_vol_2days = (amp1 > 0.03 and amp2 > 0.03)

    return {
        'code': code,
        'name': name,
        'industry': industry,
        'base_score': score, # Round 1 Score
        'tags': tags,
        'price': p_now,
        'daily_change': daily_change,
        'vol_ratio': vol_ratio,
        'pct_3d': pct_3d,
        'high_vol_2days': high_vol_2days
    }

def get_feishu_token():
    """Get Feishu tenant access token"""
    try:
        with open(FEISHU_CONFIG_FILE, 'r') as f:
            config = json.load(f)
        
        url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
        response = requests.post(url, json={
            'app_id': config['app_id'],
            'app_secret': config['app_secret']
        }, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 0:
                return data.get('tenant_access_token')
    except Exception as e:
        print(f"Feishu auth error: {e}")
    return None

def send_feishu_message(token, chat_id, text):
    """Send message to Feishu user"""
    try:
        url = 'https://open.feishu.cn/open-apis/im/v1/messages'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        # Use open_id to send message
        params = {'receive_id_type': 'chat_id'}
        data = {
            'receive_id': chat_id,
            'msg_type': 'text',
            'content': json.dumps({'text': text})
        }
        
        response = requests.post(url, headers=headers, params=params, json=data, timeout=10)
        result = response.json()
        
        if result.get('code') == 0:
            print("Message sent to Feishu successfully!")
            return True
        else:
            print(f"Feishu send error: {result}")
            return False
    except Exception as e:
        print(f"Feishu send exception: {e}")
        return False

def main():
    if not os.path.exists(POOL_FILE):
        print("Stock pool file not found.")
        return

    pool = pd.read_csv(POOL_FILE)
    
    # FIX: Remove duplicates based on code
    pool['code'] = pool['code'].astype(str).str.zfill(6)
    pool = pool.drop_duplicates(subset=['code'])
    
    tasks = [row for _, row in pool.iterrows()]
    results = []
    
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Round 1: Analyzing {len(tasks)} unique stocks...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        futures = [executor.submit(analyze_stock_basic, t) for t in tasks]
        completed = 0
        for f in concurrent.futures.as_completed(futures):
            res = f.result()
            if res: results.append(res)
            completed += 1
            if completed % 100 == 0:
                print(f"Progress: {completed}/{len(tasks)}")
                
    if not results:
        print("No results.")
        return

    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Round 2: Market & Industry Analysis...")
    
    # Module 3: Market Trend (Environment)
    url_index = "http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayqfq&param=sh000001,day,,,100,qfq"
    market_pct_3d = 0
    try:
        r_idx = requests.get(url_index, headers=HEADERS, timeout=5)
        if r_idx.status_code == 200:
            content = r_idx.text
            json_str = content.split('=', 1)[1]
            data = pd.read_json(json_str)
            sh_data = data['data'].get('sh000001', {}).get('day', [])
            if len(sh_data) >= 4:
                p_now_idx = float(sh_data[-1][2])
                p_3ago_idx = float(sh_data[-4][2])
                market_pct_3d = (p_now_idx - p_3ago_idx) / p_3ago_idx
    except Exception as e:
        print(f"Index fetch error: {e}")

    
    up_count = sum(1 for r in results if r['daily_change'] > 0)
    total_count = len(results)
    up_ratio = up_count / total_count if total_count > 0 else 0
    avg_vol_ratio = sum(r['vol_ratio'] for r in results) / total_count if total_count > 0 else 1
    
    market_sentiment_score = 0
    market_tags = []
    
    # --- Round 2: Market & Industry Analysis ---
    # 2.3 High Volatility Check
    high_vol_count = sum(1 for r in results if r.get('high_vol_2days', False))
    if total_count > 0 and (high_vol_count / total_count) > 0.3:
        market_sentiment_score -= 5
        market_tags.append("高位震荡")

    if up_ratio > 0.65 and avg_vol_ratio > 1.15:
        market_sentiment_score += 3
        market_tags.append("市场积极")
    down_ratio = 1 - up_ratio
    # 2.2 Long-term Watch
    if down_ratio > 0.40 and avg_vol_ratio < 0.8:
        market_sentiment_score -= 5
        market_tags.append("市场观望")
        
    # Module 3: Market Trend (Environment)
    if market_pct_3d < -0.01:
        market_sentiment_score += 3
        market_tags.append("逆势超跌")
    elif market_pct_3d > 0.01:
        market_sentiment_score -= 3
        market_tags.append("顺势过热")
        
    for r in results:
        r['score'] = r['base_score'] + market_sentiment_score
        if market_sentiment_score != 0:
            r['tags'].extend(market_tags)
            
    df_res = pd.DataFrame(results)
    industry_stats = df_res.groupby('industry')['daily_change'].mean()
    top_industries = industry_stats.nlargest(int(len(industry_stats) * 0.1)).index.tolist()
    bottom_industries = industry_stats.nsmallest(int(len(industry_stats) * 0.1)).index.tolist()
    
    # Industry scoring update (4.1 & 4.2)
    # Replaced simple top/bottom 10% with +3/-3 rule based on logic
    # Here we map "top 10%" to "Industry Up" (+3) and "bottom 10%" to "Industry Down" (-3)
    # to simulate the "predicted inflow/outflow" logic with available data.
    
    for r in results:
        if r['industry'] in top_industries:
            r['score'] += 3
            r['tags'].append("景气向上")
        elif r['industry'] in bottom_industries:
            r['score'] -= 3
            r['tags'].append("景气向下")
            
    # News scoring update (5.2)
    try:
        from news_module import fetch_news_multi_source, analyze_sentiment, IMPACT_RULES
        news_items = fetch_news_multi_source(limit=50)
        pool_df = pd.DataFrame(results)
        stock_scores, news_tags = analyze_sentiment(news_items, pool_df)
        
        for r in results:
            code = r['code']
            n_score = stock_scores.get(code, 0)
            if n_score != 0:
                # 5.2 Major Negative: [-10]
                if n_score <= -10: 
                    r['score'] -= 10 
                    r['tags'].append("重大利空")
                
                # 5.3 Sudden Positive (War/Disaster/Policy): [+6]
                # In news_module, we set war/quake to 6.
                elif n_score == 6:
                    r['score'] += 6
                    r['tags'].append("突发利好")
                
                # 5.4 Sudden Negative (War/Disaster/Policy): [-6]
                # In news_module, we set pandemic/disaster to -6.
                elif n_score == -6:
                    r['score'] -= 6
                    r['tags'].append("突发利空")

                # 5.1 Major Positive (Standard): [+5] or others
                elif n_score >= 5:
                     r['score'] += n_score 
                     r['tags'].append("重大利好")
                else:
                     r['score'] += n_score

                specific_tags = news_tags.get(code, [])
                unique_tags = list(set(specific_tags))[:2]
                r['tags'].extend(unique_tags)
    except Exception as e:
        print(f"News module error: {e}")
    
    # --- 6.1 Industry Selection (Module 6) ---
    # Top 200 stocks by current score
    top_200 = sorted(results, key=lambda x: x['score'], reverse=True)[:200]
    
    best_industry = "无"
    if top_200:
        # Count total industry frequency in the whole pool
        total_counts = {}
        for r in results:
            i = r.get('industry', '其他')
            total_counts[i] = total_counts.get(i, 0) + 1
            
        # Count industry frequency in Top 200
        top_counts = {}
        for r in top_200:
            i = r.get('industry', '其他')
            top_counts[i] = top_counts.get(i, 0) + 1
            
        # Calculate ratio (top_count / total_count), require at least 5 stocks in pool to avoid small sample bias
        industry_ratios = {}
        for ind, count in top_counts.items():
            if total_counts.get(ind, 0) >= 5:
                industry_ratios[ind] = count / total_counts[ind]
        
        # Find the max ratio industry
        if industry_ratios:
            best_industry = max(industry_ratios, key=industry_ratios.get)
            
            # Apply +6 score to ALL stocks in this industry
            for r in results:
                if r.get('industry') == best_industry:
                    r['score'] += 6
                    r['tags'].append("行业优选")
                    
    # --- Final Sort & Output ---
    results.sort(key=lambda x: x['score'], reverse=True)
    
    # Dedup in Results
    seen_codes = set()
    unique_results = []
    for r in results:
        if r['code'] not in seen_codes:
            unique_results.append(r)
            seen_codes.add(r['code'])
    results = unique_results

    top3 = results[:3]
    rank4_10 = results[3:10]
    
    positive_keywords = ['金叉', '九转', '回归', '超跌', '向上', '优选', '积极', '利好']
    def filter_tags(tags):
        return [t for t in tags if any(k in t for k in positive_keywords)]

    now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    
    lines = []
    lines.append(f"【 🔔AI投资研究院-每日量化选股 {now_str}】")
    lines.append(f"核心选股池 (精选{total_count})")
    lines.append("　") # Full-width space (IDEO_SPACE)

    lines.append("🏆 总分TOP3：")
    for i, s in enumerate(top3):
        pos_tags = filter_tags(s['tags'])
        pos_tags.sort(key=lambda x: 0 if '重大' in x else 1)
        final_tags = pos_tags
        t_str = f"[{' '.join(final_tags)}]" if final_tags else ""
        lines.append(f"{i+1}. {s['name']} [{s['code']}] 评分：{s['score']} {t_str}")
        
    lines.append("　") # Full-width space
    lines.append("🎉 4-10名：")
    for i, s in enumerate(rank4_10):
        pos_tags = filter_tags(s['tags'])
        pos_tags.sort(key=lambda x: 0 if '重大' in x else 1)
        final_tags = pos_tags
        t_str = f"[{' '.join(final_tags)}]" if final_tags else ""
        lines.append(f"{i+1}. {s['name']} [{s['code']}] 评分：{s['score']} {t_str}")
        
    lines.append("　") # Full-width space
    lines.append(f"📈 今日最有潜力上涨行业板块：{best_industry}")
    
    report = "\n".join(lines)
    
    with open(OUTPUT_FILE, "w") as f:
        f.write(report)
    
    # Send to Feishu
    print("Sending report to Feishu...")
    feishu_token = get_feishu_token()
    if feishu_token:
        send_feishu_message(feishu_token, FEISHU_CHAT_ID, report)
    else:
        print("Failed to get Feishu token, skipping message send.")

if __name__ == "__main__":
    main()
