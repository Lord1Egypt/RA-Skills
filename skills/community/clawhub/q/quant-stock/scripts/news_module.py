import requests
import re
import datetime
from bs4 import BeautifulSoup
import time

# --- Config ---
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

# --- Knowledge Base: Keyword -> Impact ---
# Adjusted scores per user request (+/- 5 for Major Events)

IMPACT_RULES = {
    # Macro Policy (Positive)
    '降准': {'score': 5, 'industries': ['银行', '房地产', '证券', '保险']},
    '降息': {'score': 5, 'industries': ['房地产', '有色金属', '证券']},
    '逆回购': {'score': 2, 'industries': ['证券', '银行']}, 
    '减税': {'score': 5, 'industries': ['制造业', '消费']},
    '基建': {'score': 5, 'industries': ['建筑', '建材', '工程机械']},
    '新能源': {'score': 5, 'industries': ['光伏', '风电', '锂电池', '新能源车']},
    '人工智能': {'score': 8, 'industries': ['计算机', '软件', '通信', '半导体']}, # Adjusted
    '数字经济': {'score': 5, 'industries': ['计算机', '通信', '软件']},

    # Macro Policy (Negative)
    '加息': {'score': -5, 'industries': ['房地产', '有色金属']}, 
    '监管': {'score': -5, 'industries': ['互联网', '金融']}, 

    # Sudden Events (Global/China) - Adjusted to +/- 6 per user request (5.3 / 5.4)
    '战争': {'score': 6, 'industries': ['军工', '黄金', '石油', '有色金属']}, 
    '冲突': {'score': 6, 'industries': ['军工', '黄金', '石油']},
    '疫情': {'score': -6, 'industries': ['旅游', '酒店', '航空', '餐饮', '消费']}, 
    '自然灾害': {'score': -6, 'industries': ['农业', '保险', '电力']}, 
    '地震': {'score': 6, 'industries': ['建材', '医药']}, # Reconstruction/Medical
    '突发': {'score': 6, 'industries': []}, # General sudden event keyword 

    # General Positive
    '增长': {'score': 3, 'industries': []},
    '突破': {'score': 5, 'industries': []},
    '中标': {'score': 5, 'industries': []},
    '回购': {'score': 5, 'industries': []},
    
    # General Negative
    '亏损': {'score': -5, 'industries': []},
    '减持': {'score': -5, 'industries': []}, # Changed to -5
    '立案': {'score': -5, 'industries': []}, # Changed to -5
    '违规': {'score': -5, 'industries': []}  # Changed to -5
}

def fetch_eastmoney_news(limit=50):
    print("Fetching news from EastMoney...")
    try:
        url = "https://newsapi.eastmoney.com/kuaixun/v1/getlist_102_ajaxResult_50_1_.html"
        r = requests.get(url, headers=HEADERS, timeout=5)
        text = r.text
        # Clean up var ajaxResult = {...} wrapper if present
        if "var ajaxResult=" in text:
            text = text.split("var ajaxResult=")[1].strip()
        
        # Sometimes it might not be valid JSON directly if it has trailing char, but usually requests.json() handles it if clean
        # Let's try simple regex extract to be safe
        import json
        match = re.search(r'({.*})', text)
        if match:
            data = json.loads(match.group(1))
            news_list = []
            if 'LivesList' in data:
                for item in data['LivesList']:
                    title = item.get('title', '')
                    digest = item.get('digest', '')
                    full = f"{title} {digest}"
                    if full.strip():
                        news_list.append(full.strip())
            return news_list
        return []
    except Exception as e:
        print(f"EastMoney news error: {e}")
        return []

def fetch_cls_news(limit=50):
    print("Fetching news from CLS (Cailian Press)...")
    try:
        url = "https://www.cls.cn/nodeapi/telegraphList?rn=20"
        r = requests.get(url, headers=HEADERS, timeout=5)
        data = r.json()
        news_list = []
        if 'data' in data and 'roll_data' in data['data']:
            for item in data['data']['roll_data']:
                title = item.get('title', '')
                content = item.get('content', '')
                full = f"{title} {content}"
                if full.strip():
                    news_list.append(full.strip())
        return news_list
    except Exception as e:
        print(f"CLS news error: {e}")
        return []

def fetch_sina_news(limit=50):
    print("Fetching news from Sina Finance...")
    try:
        url = f"http://zhibo.sina.com.cn/api/zhibo/feed?page=1&page_size={limit}&zhibo_id=152"
        r = requests.get(url, headers=HEADERS, timeout=10)
        data = r.json()
        
        news_list = []
        if 'result' in data and 'data' in data['result']:
            for item in data['result']['data']['feed']['list']:
                html = item.get('rich_text', '')
                soup = BeautifulSoup(html, 'lxml')
                text = soup.get_text().strip()
                if text:
                    news_list.append(text)
        return news_list
    except Exception as e:
        print(f"Sina news error: {e}")
        return []

def fetch_news_multi_source(limit=50):
    # Strategy: Try EastMoney -> CLS -> Sina
    # Combine results? Or just take first success? 
    # Taking first success is faster and usually sufficient for recent news.
    # Combining might duplicate logic but cover more ground. Let's combine unique.
    
    all_news = []
    
    # 1. EastMoney
    em_news = fetch_eastmoney_news(limit)
    if em_news:
        print(f"Got {len(em_news)} items from EastMoney.")
        all_news.extend(em_news)
    
    # 2. CLS (if EastMoney failed or provided few)
    if len(all_news) < 10:
        cls_news = fetch_cls_news(limit)
        if cls_news:
             print(f"Got {len(cls_news)} items from CLS.")
             all_news.extend(cls_news)
             
    # 3. Sina (Fallback)
    if len(all_news) < 5:
        sina_news = fetch_sina_news(limit)
        if sina_news:
            print(f"Got {len(sina_news)} items from Sina.")
            all_news.extend(sina_news)
            
    return list(set(all_news)) # Dedup

def analyze_sentiment(news_items, pool_df):
    stock_scores = {} 
    matched_tags = {} 
    
    name_map = dict(zip(pool_df['name'], pool_df['code']))
    
    industry_map = {}
    for _, row in pool_df.iterrows():
        ind = str(row.get('industry', '其他'))
        if ind not in industry_map: industry_map[ind] = []
        industry_map[ind].append(str(row['code']).zfill(6))
        
    print(f"Analyzing {len(news_items)} news items against {len(pool_df)} stocks...")
    
    for news in news_items:
        for kw, rule in IMPACT_RULES.items():
            if kw in news:
                score = rule['score']
                target_industries = rule['industries']
                
                if target_industries:
                    matched_pool_inds = [i for i in industry_map.keys() if any(ti in i for ti in target_industries)]
                    for pool_ind in matched_pool_inds:
                        codes = industry_map[pool_ind]
                        for c in codes:
                            stock_scores[c] = stock_scores.get(c, 0) + score
                            if c not in matched_tags: matched_tags[c] = []
                            matched_tags[c].append(f"{kw}利{'好' if score>0 else '空'}")
                else:
                    for name, code in name_map.items():
                        if name in news:
                            # Direct mention score logic:
                            # Rule score is usually small (3-5), maybe boost for direct mention?
                            # User says: "符合重大利好... [+5分]"
                            # Let's use the rule score directly as base, or ensure it hits +/- 5
                            # If rule score is small (3), we boost it to 5 for direct mention if significant keyword?
                            # Actually, let's trust the rule score.
                            stock_scores[code] = stock_scores.get(code, 0) + score
                            if code not in matched_tags: matched_tags[code] = []
                            matched_tags[code].append(kw)
                            
    return stock_scores, matched_tags
