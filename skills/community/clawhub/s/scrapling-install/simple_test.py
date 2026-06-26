#!/usr/bin/env python3

try:
    from scrapling import Fetcher
    print("✓ Scrapling imported successfully")
    
    # Test basic fetch
    fetcher = Fetcher()
    print("✓ Fetcher created successfully")
    
    # Try to fetch a simple page
    try:
        page = fetcher.get('https://httpbin.org/html')
        print("✓ Basic fetch successful")
        print(f"Page title: {page.find_by_text('Herman Melville - Moby-Dick') is not None}")
    except Exception as e:
        print(f"✗ Basic fetch failed: {e}")
        
except Exception as e:
    print(f"✗ Import error: {e}")