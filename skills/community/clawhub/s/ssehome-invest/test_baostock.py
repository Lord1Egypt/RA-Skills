#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Baostock data retrieval
"""
import pandas as pd
try:
    import baostock as bs
    print("✅ baostock imported successfully")
except ImportError as e:
    print(f"❌ baostock import failed: {e}")
    exit(1)

# Test login
print("🔍 Testing login...")
login_rs = bs.login()
if login_rs.error_code == '0':
    print("✅ Login successful!")
    print(f"Login message: {login_rs.error_msg}")
    
    # Get market list (to verify connection)
    rs = bs.query_all_stock()
    

    if rs.error_code == '0':
        #### 打印结果集 ####
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)

        print(f"✅ Market data retrieved: {len(result)} stocks")
        print("First 5 stocks:", result.head(5))

    else:
        print(f"❌ Market data error: {rs.error_msg}")
    
    # Logout
    bs.logout()
else:
    print(f"❌ Login failed: {login_rs.error_msg}")
    exit(1)

print("✅ Test completed successfully!")