#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Baostock test - check if baostock is installed and can be imported
"""

import sys

print("Python version:", sys.version)
print("Python executable:", sys.executable)

try:
    import baostock as bs
    print("✅ baostock imported successfully")
    
    # Test basic functionality
    print("🔍 Testing login...")
    login_rs = bs.login()
    if login_rs.error_code == '0':
        print("✅ Login successful!")
        print("Login message:", login_rs.error_msg)
        
        # Test logout
        bs.logout()
        print("✅ Logout successful!")
    else:
        print(f"❌ Login failed: {login_rs.error_msg}")
        
except ImportError as e:
    print(f"❌ baostock import failed: {e}")
    print("Please install with: pip install baostock")
    exit(1)

print("✅ Test completed successfully!")