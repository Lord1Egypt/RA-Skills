import pandas as pd
import baostock as bs
import os

POOL_FILE = "workspace/quant_engine/stock_pool.csv"

def update_sectors_with_baostock():
    if not os.path.exists(POOL_FILE):
        print("Pool file not found.")
        return

    df = pd.read_csv(POOL_FILE)
    
    # Login
    print("Logging into Baostock...")
    lg = bs.login()
    if lg.error_code != '0':
        print(f"Login failed: {lg.error_msg}")
        return
        
    # Query Industry Info
    # query_stock_industry() returns code, code_name, industry, industry_classification
    print("Fetching industry data...")
    rs = bs.query_stock_industry()
    
    industries = []
    while (rs.error_code == '0') and rs.next():
        industries.append(rs.get_row_data())
        
    result = pd.DataFrame(industries, columns=rs.fields)
    
    # Clean code: sh.600000 -> 600000
    # Or pool uses 600000, Baostock uses sh.600000
    # Let's standardize
    
    result['code'] = result['code'].apply(lambda x: x.split('.')[1] if '.' in x else x)
    
    # Map industry
    industry_map = dict(zip(result['code'], result['industry']))
    
    # Apply
    df['code'] = df['code'].astype(str).str.zfill(6)
    df['industry'] = df['code'].map(industry_map)
    df['industry'] = df['industry'].fillna("其他")
    
    # Save
    df.to_csv(POOL_FILE, index=False)
    print(f"Updated {POOL_FILE} with industry info (Baostock source).")
    
    bs.logout()

if __name__ == "__main__":
    update_sectors_with_baostock()
