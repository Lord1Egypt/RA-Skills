import pandas as pd
import requests
import os
import time

POOL_FILE = "workspace/quant_engine/stock_pool.csv"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def fetch_top_turnover_stocks(limit=300):
    """
    Fetch top stocks by turnover from Tencent Web Interface.
    URL: http://qt.gtimg.cn/q=rank:col%3Damount%26sort%3Ddes%26num%3D{limit}
    Note: Tencent rank interface is tricky. Better to use EastMoney or Sina rank if possible, 
    BUT since we want stability, let's try a proven Tencent rank URL if known, 
    OR use EastMoney Rank (which is usually separate from the blocked quote interface).
    
    Actually, EastMoney Rank Interface (http://push2.eastmoney.com/api/qt/clist/get) is what akshare uses.
    If that is blocked, we can try Sina.
    
    Let's try Sina Rank (http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=100&sort=amount&asc=0&node=hs_a&symbol=&_s_r_a=page)
    """
    all_stocks = []
    page = 1
    while len(all_stocks) < limit:
        url = f"http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page={page}&num=100&sort=amount&asc=0&node=hs_a&symbol=&_s_r_a=page"
        try:
            r = requests.get(url, headers=HEADERS, timeout=5)
            if r.status_code != 200: break
            
            data = r.json()
            if not data: break
            
            for item in data:
                # Sina format: {symbol:"sh600000", code:"600000", name:"...", amount:"..."}
                all_stocks.append({
                    'code': item['code'],
                    'name': item['name'],
                    'turnover': float(item['amount'])
                })
                
            page += 1
            time.sleep(1) # Be nice
            
        except Exception as e:
            print(f"Error fetching rank page {page}: {e}")
            break
            
    return pd.DataFrame(all_stocks)

def update_hot_pool():
    print("Fetching top turnover stocks (Hot 200)...")
    
    # 1. Fetch Top 500 by Turnover (to ensure we have enough after filtering)
    top_df = fetch_top_turnover_stocks(limit=500)
    if top_df.empty:
        print("Failed to fetch hot stocks.")
        return

    # 2. Load existing pool
    if os.path.exists(POOL_FILE):
        pool = pd.read_csv(POOL_FILE)
        # Keep BlueChips (source != '热点')
        # Actually, let's keep '指数' or 'CSI300/500' sources
        # Identify existing blue chips
        blue_chips = pool[pool['source'].isin(['CSI300', 'CSI500', '蓝筹'])]
    else:
        print("No existing pool found. Please run init_pool.py first.")
        return

    print(f"Existing Blue Chips: {len(blue_chips)}")
    
    # 3. Filter: Remove stocks already in BlueChips
    # Ensure code is string
    top_df['code'] = top_df['code'].astype(str)
    blue_chips['code'] = blue_chips['code'].astype(str)
    
    existing_codes = set(blue_chips['code'])
    
    # Candidates: Not in existing
    candidates = top_df[~top_df['code'].isin(existing_codes)].copy()
    
    # 4. Take Top 200
    hot_200 = candidates.head(200).copy()
    hot_200['source'] = '热点'
    hot_200 = hot_200[['code', 'name', 'source']]
    
    print(f"Found {len(hot_200)} new hot stocks.")
    
    # 5. Merge and Save
    final_pool = pd.concat([blue_chips, hot_200])
    final_pool.to_csv(POOL_FILE, index=False)
    
    print(f"Updated pool saved to {POOL_FILE}. Total: {len(final_pool)} stocks.")

if __name__ == "__main__":
    update_hot_pool()
