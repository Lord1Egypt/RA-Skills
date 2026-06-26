#!/usr/bin/env python3
"""Check Binance Futures balance"""
import hmac, hashlib, time, requests, os

API_KEY = os.environ.get('BINANCE_API_KEY', '')
SECRET = os.environ.get('BINANCE_SECRET', '')

if not API_KEY or not SECRET:
    print("Set BINANCE_API_KEY and BINANCE_SECRET")
    exit(1)

ts = int(time.time() * 1000)
params = f"timestamp={ts}"
sig = hmac.new(SECRET.encode(), params.encode(), hashlib.sha256).hexdigest()

r = requests.get(f"https://fapi.binance.com/fapi/v3/account?{params}&signature={sig}",
                headers={"X-MBX-APIKEY": API_KEY}, timeout=15)

if r.status_code == 200:
    acc = r.json()
    print(f"💰 Balance: ${acc.get('totalMarginBalance', 'N/A')}")
    print(f"� Available: ${acc.get('availableBalance', 'N/A')}")
    print(f"⚠️ Margin Used: ${acc.get('totalMarginBalance', 0) - acc.get('availableBalance', 0):.2f}")
else:
    print(f"Error: {r.text}")
