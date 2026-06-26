#!/usr/bin/env python3
"""测试服务器启动脚本"""
import os
import sys
sys.path.insert(0, '.')

# 加载测试配置
with open('.env.test') as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            key, value = line.strip().split('=', 1)
            os.environ[key] = value

from app.main import app
import uvicorn

if __name__ == "__main__":
    print("Starting x402 Proxy Gateway on Base Sepolia...")
    print(f"Developer Wallet: {os.getenv('DEVELOPER_WALLET')}")
    print(f"Chain: {os.getenv('X402_CHAIN')}")
    print(f"Price: {os.getenv('PRICE_PER_REQUEST')} USDC")
    uvicorn.run(app, host="0.0.0.0", port=8080)
