import akshare as ak
import pandas as pd
import os

POOL_FILE = "workspace/quant_engine/stock_pool.csv"

def init_pool():
    print("Initializing stock pool from Indices (CSI300 + CSI500)...")
    try:
        # 1. CSI 300
        df300 = ak.index_stock_cons(symbol="000300")
        df300['source'] = 'CSI300'
        print(f"Got {len(df300)} from CSI300")
        
        # 2. CSI 500
        df500 = ak.index_stock_cons(symbol="000905")
        df500['source'] = 'CSI500'
        print(f"Got {len(df500)} from CSI500")
        
        # Combine
        # Columns usually: 品种代码, 品种名称, 纳入日期
        # Rename to: code, name, source
        df300 = df300.rename(columns={'品种代码': 'code', '品种名称': 'name'})
        df500 = df500.rename(columns={'品种代码': 'code', '品种名称': 'name'})
        
        final = pd.concat([df300[['code', 'name', 'source']], df500[['code', 'name', 'source']]])
        final = final.drop_duplicates(subset=['code'])
        
        print(f"Total: {len(final)} unique stocks.")
        
        # Save
        final.to_csv(POOL_FILE, index=False)
        print(f"Saved to {POOL_FILE}")
        
    except Exception as e:
        print(f"Error initializing pool: {e}")

if __name__ == "__main__":
    init_pool()
