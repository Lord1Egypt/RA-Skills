#!/usr/bin/env python3
"""Check open positions"""
import hmac, hashlib, time, requests, os

API_KEY = os.environ.get('BINANCE_API_KEY', '')
SECRET = os.environ.get('BINANCE_SECRET', '')

if not API_KEY or not SECRET:
    print("Set BINANCE_API_KEY and BINANCE_SECRET")
    exit(1)

ts = int(time.time() * 1000)
params = f"timestamp={ts}"
sig = hmac.new(SECRET.encode(), params.encode(), hashlib.sha256).hexdigest()

r = requests.get(f"https://fapi.binance.com/fapi/v2/positionRisk?{params}&signature={sig}",
                headers={"X-MBX-APIKEY": API_KEY}, timeout=15)

if r.status_code == 200:
    positions = r.json()
    open_pos = [p for p in positions if float(p.get('positionAmt', 0)) != 0]
    
    print(f"📊 Open Positions: {len(open_pos)}/8\n")
    
    total_pnl = 0
    for p in open_pos:
        symbol = p.get('symbol')
        amt = float(p.get('positionAmt', 0))
        entry = float(p.get('entryPrice', 0))
        pnl = float(p.get('unrealizedProfit', 0))
        side = "🟢 LONG" if amt > 0 else "🔴 SHORT"
        
        print(f"{side} {symbol}")
        print(f"  Size: {abs(amt)} @ ${entry:.6f}")
        print(f"  PnL: ${pnl:.2f}")
        print()
        
        total_pnl += pnl
    
    print(f"💰 Total Unrealized PnL: ${total_pnl:.2f}")
else:
    print(f"Error: {r.text}")
