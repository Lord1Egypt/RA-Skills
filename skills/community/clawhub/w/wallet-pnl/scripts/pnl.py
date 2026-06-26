#!/usr/bin/env python3
"""
Solana Wallet PnL Analyzer
Analyzes a wallet's trading history: win rate, realized PnL, top trades, recent activity.
Powered by Helius API for transaction data.
"""

import os
import sys
import json
import requests
from dataclasses import dataclass, field
from typing import Optional

HELIUS_KEY = os.environ.get("HELIUS_API_KEY", "")
HEADERS = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}


@dataclass
class TradeRecord:
    signature: str
    token_symbol: str
    token_mint: str
    side: str          # "BUY" or "SELL"
    sol_amount: float
    timestamp: int


@dataclass
class PnLResult:
    wallet: str
    total_trades: int = 0
    win_trades: int = 0
    loss_trades: int = 0
    win_rate_pct: float = 0.0
    realized_pnl_sol: float = 0.0
    total_buy_sol: float = 0.0
    total_sell_sol: float = 0.0
    avg_trade_size_sol: float = 0.0
    most_traded_tokens: list = field(default_factory=list)
    recent_trades: list = field(default_factory=list)
    trader_type: str = "UNKNOWN"   # DEGEN / TRADER / HOLDER / INACTIVE
    risk_rating: str = "UNKNOWN"   # FOLLOW / NEUTRAL / AVOID


def fetch_helius_transactions(wallet: str, limit: int = 100) -> list:
    """Fetch parsed transaction history from Helius"""
    if not HELIUS_KEY:
        return []
    try:
        url = (f"https://api.helius.xyz/v0/addresses/{wallet}/transactions"
               f"?api-key={HELIUS_KEY}&limit={limit}&type=SWAP")
        r = requests.get(url, headers=HEADERS, timeout=12)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return []


def fetch_sol_balance(wallet: str) -> float:
    """Get current SOL balance via public RPC"""
    rpc_url = (f"https://mainnet.helius-rpc.com/?api-key={HELIUS_KEY}"
               if HELIUS_KEY else "https://api.mainnet-beta.solana.com")
    try:
        r = requests.post(rpc_url, json={
            "jsonrpc": "2.0", "id": 1, "method": "getBalance", "params": [wallet]
        }, headers=HEADERS, timeout=8)
        if r.status_code == 200:
            res = r.json().get("result", {})
            if isinstance(res, dict) and "value" in res:
                return res["value"] / 1e9
    except Exception:
        pass
    return -1


def fetch_token_accounts(wallet: str) -> list:
    """Get current token holdings"""
    rpc_url = (f"https://mainnet.helius-rpc.com/?api-key={HELIUS_KEY}"
               if HELIUS_KEY else "https://api.mainnet-beta.solana.com")
    try:
        r = requests.post(rpc_url, json={
            "jsonrpc": "2.0", "id": 1,
            "method": "getTokenAccountsByOwner",
            "params": [wallet,
                       {"programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"},
                       {"encoding": "jsonParsed"}]
        }, headers=HEADERS, timeout=8)
        if r.status_code == 200:
            result = r.json().get("result", {})
            return result.get("value", [])
    except Exception:
        pass
    return []


def parse_swap_trades(txns: list) -> list[TradeRecord]:
    """Parse Helius swap transactions into simplified trade records"""
    trades = []
    for tx in txns:
        if not tx or tx.get("transactionError"):
            continue
        events = tx.get("events", {})
        swap = events.get("swap")
        if not swap:
            continue

        sig = tx.get("signature", "")
        ts = tx.get("timestamp", 0)

        native_in = swap.get("nativeInput")
        native_out = swap.get("nativeOutput")
        token_in = swap.get("tokenInputs", [{}])[0] if swap.get("tokenInputs") else {}
        token_out = swap.get("tokenOutputs", [{}])[0] if swap.get("tokenOutputs") else {}

        # SOL → Token (BUY)
        if native_in and token_out:
            sol_amt = native_in.get("amount", 0) / 1e9
            mint = token_out.get("mint", "")
            symbol = token_out.get("tokenAmount", {}).get("uiAmountString", mint[:6])
            trades.append(TradeRecord(sig, symbol, mint, "BUY", sol_amt, ts))

        # Token → SOL (SELL)
        elif token_in and native_out:
            sol_amt = native_out.get("amount", 0) / 1e9
            mint = token_in.get("mint", "")
            symbol = token_in.get("tokenAmount", {}).get("uiAmountString", mint[:6])
            trades.append(TradeRecord(sig, symbol, mint, "SELL", sol_amt, ts))

    return trades


def analyze_wallet(wallet: str, tx_limit: int = 100) -> PnLResult:
    result = PnLResult(wallet=wallet)

    # Fetch data
    txns = fetch_helius_transactions(wallet, tx_limit)
    sol_balance = fetch_sol_balance(wallet)
    token_accounts = fetch_token_accounts(wallet)

    if not txns:
        result.trader_type = "INACTIVE"
        result.risk_rating = "NEUTRAL"
        return result

    trades = parse_swap_trades(txns)
    if not trades:
        result.trader_type = "INACTIVE"
        result.risk_rating = "NEUTRAL"
        return result

    # Aggregate by token mint: track buys and sells
    token_pnl: dict[str, dict] = {}
    for t in trades:
        if t.token_mint not in token_pnl:
            token_pnl[t.token_mint] = {
                "symbol": t.token_symbol, "mint": t.token_mint,
                "buy_sol": 0.0, "sell_sol": 0.0, "trades": 0
            }
        entry = token_pnl[t.token_mint]
        entry["trades"] += 1
        if t.side == "BUY":
            entry["buy_sol"] += t.sol_amount
            result.total_buy_sol += t.sol_amount
        else:
            entry["sell_sol"] += t.sol_amount
            result.total_sell_sol += t.sol_amount

    # Calculate per-token PnL (only for tokens where we have both buy and sell)
    win_count = 0
    loss_count = 0
    closed_positions = []

    for mint, d in token_pnl.items():
        if d["buy_sol"] > 0 and d["sell_sol"] > 0:
            pnl = d["sell_sol"] - d["buy_sol"]
            d["pnl_sol"] = round(pnl, 4)
            d["pnl_pct"] = round((pnl / d["buy_sol"]) * 100, 1)
            result.realized_pnl_sol += pnl
            if pnl > 0:
                win_count += 1
            else:
                loss_count += 1
            closed_positions.append(d)

    # Summary stats
    result.total_trades = len(trades)
    result.win_trades = win_count
    result.loss_trades = loss_count
    result.win_rate_pct = round(
        win_count / (win_count + loss_count) * 100, 1
    ) if (win_count + loss_count) > 0 else 0.0
    result.realized_pnl_sol = round(result.realized_pnl_sol, 4)
    result.total_buy_sol = round(result.total_buy_sol, 4)
    result.total_sell_sol = round(result.total_sell_sol, 4)
    result.avg_trade_size_sol = round(
        (result.total_buy_sol + result.total_sell_sol) / result.total_trades, 4
    ) if result.total_trades > 0 else 0

    # Most traded tokens (by trade count)
    sorted_tokens = sorted(token_pnl.values(), key=lambda x: x["trades"], reverse=True)
    result.most_traded_tokens = [
        {"symbol": t["symbol"][:20], "mint": t["mint"],
         "trades": t["trades"], "pnl_sol": t.get("pnl_sol")}
        for t in sorted_tokens[:10]
    ]

    # Recent trades (last 10)
    recent = sorted(trades, key=lambda x: x.timestamp, reverse=True)[:10]
    result.recent_trades = [
        {"side": t.side, "token": t.token_symbol[:20],
         "sol_amount": round(t.sol_amount, 4), "timestamp": t.timestamp}
        for t in recent
    ]

    # Trader type classification
    buys = sum(1 for t in trades if t.side == "BUY")
    sells = sum(1 for t in trades if t.side == "SELL")
    if result.total_trades < 5:
        result.trader_type = "INACTIVE"
    elif result.avg_trade_size_sol > 10:
        result.trader_type = "WHALE"
    elif result.total_trades > 50:
        result.trader_type = "DEGEN"
    elif sells / max(buys, 1) > 0.7:
        result.trader_type = "TRADER"
    else:
        result.trader_type = "HOLDER"

    # Risk rating (should I copy this wallet?)
    if result.win_rate_pct >= 60 and result.realized_pnl_sol > 0:
        result.risk_rating = "FOLLOW"
    elif result.win_rate_pct < 35 or result.realized_pnl_sol < -5:
        result.risk_rating = "AVOID"
    else:
        result.risk_rating = "NEUTRAL"

    return result


if __name__ == "__main__":
    wallet = sys.argv[1] if len(sys.argv) > 1 else input("Wallet address: ").strip()
    r = analyze_wallet(wallet)
    print(f"\n{'='*55}")
    print(f"  Wallet: {wallet[:8]}...{wallet[-6:]}")
    print(f"  Type: {r.trader_type}  |  Copy Rating: {r.risk_rating}")
    print(f"{'='*55}")
    print(f"  Trades analyzed : {r.total_trades}")
    print(f"  Win Rate        : {r.win_rate_pct}%  ({r.win_trades}W / {r.loss_trades}L)")
    print(f"  Realized PnL    : {r.realized_pnl_sol:+.3f} SOL")
    print(f"  Avg Trade Size  : {r.avg_trade_size_sol:.3f} SOL")
    print(f"\n  Top Traded Tokens:")
    for t in r.most_traded_tokens[:5]:
        pnl_str = f"  PnL: {t['pnl_sol']:+.3f} SOL" if t["pnl_sol"] is not None else ""
        print(f"    {t['symbol'][:15]:<16} {t['trades']} trades{pnl_str}")
