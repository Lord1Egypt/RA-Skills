#!/usr/bin/env python3
"""
🐋 Whale Watcher - 巨鲸钱包监控
Monitor crypto whale wallets for large transactions
"""

import json
import urllib.request
import urllib.error
from datetime import datetime

# API Keys (free tier)
ETHERSCAN_API = "https://api.etherscan.io/api"
BSCSCAN_API = "https://api.bscscan.com/api"

# Default free API keys (rate limited)
DEFAULT_ETHERSCAN_KEY = "YourApiKeyToken"

def get_eth_transactions(address, api_key=DEFAULT_ETHERSCAN_KEY):
    """Get Ethereum transactions for an address"""
    url = f"{ETHERSCAN_API}?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=desc&apikey={api_key}"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data.get('result', [])
    except Exception as e:
        return {"error": str(e)}

def get_bsc_transactions(address, api_key=DEFAULT_ETHERSCAN_KEY):
    """Get BSC transactions for an address"""
    url = f"{BSCSCAN_API}?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=desc&apikey={api_key}"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data.get('result', [])
    except Exception as e:
        return {"error": str(e)}

def analyze_transaction(tx, chain="ETH"):
    """Analyze a single transaction"""
    value_ether = int(tx.get('value', 0)) / 1e18
    value_usd = value_ether * 3500  # Approximate ETH price
    
    return {
        "hash": tx.get('hash', '')[:10] + '...',
        "from": tx.get('from', '')[:10] + '...',
        "to": tx.get('to', '')[:10] + '...',
        "value": f"{value_ether:.2f} {chain}",
        "value_usd": f"${value_usd:,.2f}",
        "timestamp": datetime.fromtimestamp(int(tx.get('timeStamp', 0))).strftime('%Y-%m-%d %H:%M:%S'),
        "is_large": value_usd > 100000  # $100k+ threshold
    }

def monitor_wallet(address, chain="ETH", threshold_usd=100000):
    """Monitor a whale wallet"""
    print(f"🐋 监控钱包：{address[:10]}... ({chain})")
    print(f"💰 阈值：${threshold_usd:,}")
    print("=" * 60)
    
    if chain.upper() == "ETH":
        txs = get_eth_transactions(address)
        chain_name = "ETH"
    elif chain.upper() == "BSC":
        txs = get_bsc_transactions(address)
        chain_name = "BNB"
    else:
        print(f"❌ 不支持的链：{chain}")
        return
    
    if isinstance(txs, dict) and 'error' in txs:
        print(f"❌ 错误：{txs['error']}")
        return
    
    if not isinstance(txs, list):
        print(f"❌ 数据格式错误：{type(txs)}")
        return
    
    large_txs = []
    for tx in txs[:20]:  # Last 20 transactions
        if not isinstance(tx, dict):
            continue
        analysis = analyze_transaction(tx, chain_name)
        if analysis['is_large'] or float(analysis['value_usd'].replace('$','').replace(',','')) > threshold_usd:
            large_txs.append(analysis)
    
    if large_txs:
        print(f"\n✅ 发现 {len(large_txs)} 笔大额交易:\n")
        for i, tx in enumerate(large_txs[:5], 1):
            print(f"{i}. {tx['timestamp']}")
            print(f"   💰 {tx['value']} ({tx['value_usd']})")
            print(f"   📤 {tx['from']} → {tx['to']}")
            print(f"   🔗 https://{chain.lower()}.etherscan.io/tx/{tx['hash']}")
            print()
    else:
        print("\n💤 暂无大额交易")
    
    print("=" * 60)

if __name__ == "__main__":
    # Example: Monitor Vitalik's wallet
    VITALIK_WALLET = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
    
    print("🐋 Whale Watcher v1.0")
    print("Starting whale monitoring...\n")
    
    monitor_wallet(VITALIK_WALLET, "ETH", 50000)
