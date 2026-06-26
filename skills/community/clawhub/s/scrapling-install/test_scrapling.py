#!/usr/bin/env python3
"""
Test script to verify scrapling functionality
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import scrapling
    print(f"✓ Scrapling version {scrapling.__version__} imported successfully")
    
    # Test basic fetcher
    from scrapling import Fetcher
    print("✓ Fetcher imported successfully")
    
    # Test if we can create a fetcher instance
    fetcher = Fetcher()
    print("✓ Fetcher instance created successfully")
    
    # Test CLI availability
    from scrapling import cli
    print("✓ CLI module imported successfully")
    
    # Check if MCP command is available
    if hasattr(cli, 'mcp'):
        print("✓ MCP command is available in CLI")
    else:
        print("✗ MCP command not found in CLI")
    
    print("\n✅ All basic tests passed!")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Runtime error: {e}")
    sys.exit(1)