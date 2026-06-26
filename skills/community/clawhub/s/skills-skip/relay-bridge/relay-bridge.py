#!/usr/bin/env python3
"""
Relay Bridge - Cross-chain bridging skill
Supports 20+ EVM chains
"""

import os
import sys
import json
import time
import requests
from typing import Optional, Dict, Any

# === LOAD ENV ===
script_dir = os.path.dirname(os.path.abspath(__file__))
env_file = os.path.join(script_dir, '.env')

if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and '=' in line:
                k, v = line.split('=', 1)
                os.environ[k] = v

RELAY_API_KEY = os.environ.get('RELAY_API_KEY', '')

# Supported chains
CHAINS = {
    1: 'Ethereum',
    42161: 'Arbitrum',
    10: 'Optimism',
    8453: 'Base',
    43114: 'Avalanche',
    137: 'Polygon',
    56: 'BNB Chain',
    250: 'Fantom',
    14: 'Flare',
    100: 'Gnosis',
    11155111: 'Sepolia',
    4217: 'Songbird',
    11155420: 'Optimism Sepolia',
    421614: 'Arbitrum Sepolia',
    84532: 'Base Sepolia',
    80001: 'Mumbai',
    97: 'BNB Testnet',
}

# Token addresses (use 0x0 for native token)
NATIVE_TOKEN = '0x0000000000000000000000000000000000000000'

def get_quote(from_chain: int, to_chain: int, token: str, amount: str, from_address: str, to_address: str = None) -> Dict[str, Any]:
    """Get bridge quote from Relay API v2"""
    if not RELAY_API_KEY:
        return {'error': 'RELAY_API_KEY not set'}
    
    # Convert token to address (use NATIVE for ETH/native tokens)
    token_address = NATIVE_TOKEN if token.upper() in ['ETH', 'NATIVE', 'SGB', 'FLR'] else token
    
    url = "https://api.relay.link/quote/v2"
    
    data = {
        'user': from_address,
        'recipient': to_address or from_address,
        'originChainId': from_chain,
        'destinationChainId': to_chain,
        'originCurrency': token_address,
        'destinationCurrency': token_address,
        'amount': amount,
        'tradeType': 'EXACT_INPUT',
    }
    
    headers = {
        'Content-Type': 'application/json',
        'x-relay-api-key': RELAY_API_KEY,
    }
    
    try:
        r = requests.post(url, json=data, headers=headers, timeout=30)
        if r.status_code == 200:
            return r.json()
        else:
            return {'error': f'API error: {r.status_code}', 'detail': r.text}
    except Exception as e:
        return {'error': str(e)}

def execute_bridge(quote_request: Dict, from_address: str, to_address: str = None) -> Dict[str, Any]:
    """Execute bridge transaction using quote"""
    if not RELAY_API_KEY:
        return {'error': 'RELAY_API_KEY not set'}
    
    # First get quote
    quote = get_quote(
        from_chain=quote_request.get('originChainId'),
        to_chain=quote_request.get('destinationChainId'),
        token=quote_request.get('originCurrency'),
        amount=quote_request.get('amount'),
        from_address=from_address,
        to_address=to_address
    )
    
    if 'error' in quote:
        return quote
    
    # Get quoteId from response
    quote_id = quote.get('requestId') or quote.get('quoteId')
    if not quote_id:
        return {'error': 'No quote ID in response'}
    
    # Execute with quote
    url = "https://api.relay.link/execute"
    data = {
        'quote': quote,
        'user': from_address,
        'recipient': to_address or from_address,
    }
    headers = {
        'Content-Type': 'application/json',
        'x-relay-api-key': RELAY_API_KEY,
    }
    
    try:
        r = requests.post(url, json=data, headers=headers, timeout=60)
        if r.status_code == 200:
            return r.json()
        else:
            return {'error': f'API error: {r.status_code}', 'detail': r.text}
    except Exception as e:
        return {'error': str(e)}

def get_status(transaction_hash: str, from_chain: int) -> Dict[str, Any]:
    """Get bridge transaction status"""
    url = f"https://api.relay.link/v1/status/{transaction_hash}"
    params = {'chainId': from_chain}
    
    try:
        r = requests.get(url, params=params, timeout=30)
        if r.status_code == 200:
            return r.json()
        else:
            return {'error': f'API error: {r.status_code}'}
    except Exception as e:
        return {'error': str(e)}

def list_chains():
    """List supported chains"""
    print("🌉 Supported Chains:")
    print("-" * 40)
    for chain_id, name in sorted(CHAINS.items()):
        print(f"  {chain_id:>6}: {name}")

def format_quote(quote: Dict) -> str:
    """Format quote for display"""
    if 'error' in quote:
        return f"❌ Error: {quote['error']}"
    
    result = []
    result.append("🌉 Bridge Quote:")
    result.append("-" * 40)
    result.append(f"  From: {CHAINS.get(quote.get('fromChainId'), 'Unknown')}")
    result.append(f"  To:   {CHAINS.get(quote.get('toChainId'), 'Unknown')}")
    result.append(f"  Amount: {quote.get('amountIn', 'N/A')}")
    result.append(f"  Output: {quote.get('amountOut', 'N/A')}")
    
    fees = quote.get('fees', {})
    if fees:
        result.append(f"  Fees: ${fees.get('total', 'N/A')}")
    
    eta = quote.get('estimatedArrivalSeconds', 0)
    if eta:
        result.append(f"  ETA: ~{eta//60} minutes")
    
    result.append(f"  Quote ID: {quote.get('quoteId', 'N/A')}")
    
    return "\n".join(result)

# === CLI ===
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 relay-bridge.py chains          - List supported chains")
        print("  python3 relay-bridge.py quote FROM TO AMOUNT TOKEN FROM_ADDRESS")
        print("  python3 relay-bridge.py execute QUOTE_ID TO_ADDRESS FROM_ADDRESS")
        print()
        print("Example:")
        print("  python3 relay-bridge.py quote 1 42161 0.1 ETH 0x1234...")
        sys.exit(1)
    
    cmd = sys.argv[1].lower()
    
    if cmd == 'chains':
        list_chains()
    
    elif cmd == 'quote':
        if len(sys.argv) < 7:
            print("Usage: quote FROM_CHAIN TO_CHAIN AMOUNT TOKEN FROM_ADDRESS")
            sys.exit(1)
        from_chain = int(sys.argv[2])
        to_chain = int(sys.argv[3])
        amount = sys.argv[4]
        token = sys.argv[5]
        from_address = sys.argv[6]
        
        quote = get_quote(from_chain, to_chain, token, amount, from_address)
        print(format_quote(quote))
    
    elif cmd == 'execute':
        if len(sys.argv) < 5:
            print("Usage: execute QUOTE_ID TO_ADDRESS FROM_ADDRESS")
            sys.exit(1)
        quote_id = sys.argv[2]
        to_address = sys.argv[3]
        from_address = sys.argv[4]
        
        result = execute_bridge(quote_id, to_address, from_address)
        print(json.dumps(result, indent=2))
    
    else:
        print(f"Unknown command: {cmd}")
