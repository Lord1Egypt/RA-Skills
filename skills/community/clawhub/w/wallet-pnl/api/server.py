"""
Solana Wallet PnL Analyzer - Paid API
Analyzes wallet trading history: win rate, PnL, trader type, copy rating.
Pay-per-request via x402 USDC on Base chain.
"""

import os, sys, json
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from pnl import analyze_wallet, PnLResult

app = FastAPI(title="Solana Wallet PnL Analyzer API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

PRICE = os.environ.get("PRICE_PER_REQUEST", "0.03")
PAY_TO = os.environ.get("PAY_TO_ADDRESS", "")
FACILITATOR = os.environ.get("FACILITATOR_URL", "https://x402.org/facilitator")
USDC_BASE = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"


def payment_requirements():
    return {
        "x402Version": 1,
        "accepts": [{
            "scheme": "exact", "network": "base",
            "maxAmountRequired": str(int(float(PRICE) * 1_000_000)),
            "resource": "/pnl", "description": f"Solana wallet PnL analysis — ${PRICE} per request",
            "mimeType": "application/json", "payTo": PAY_TO,
            "maxTimeoutSeconds": 60, "asset": USDC_BASE,
        }],
        "error": "Payment required"
    }


def verify_payment(request: Request) -> bool:
    if not PAY_TO:
        return True
    ph = request.headers.get("X-PAYMENT")
    if not ph:
        return False
    try:
        r = requests.post(f"{FACILITATOR}/verify",
                          json={"payment": ph, "paymentRequirements": payment_requirements()["accepts"][0]},
                          timeout=10)
        return r.status_code == 200 and r.json().get("isValid", False)
    except Exception:
        return False


def settle_payment(ph: str) -> dict:
    try:
        r = requests.post(f"{FACILITATOR}/settle",
                          json={"payment": ph, "paymentRequirements": payment_requirements()["accepts"][0]},
                          timeout=10)
        return r.json() if r.status_code == 200 else {}
    except Exception:
        return {}


def result_to_dict(r: PnLResult) -> dict:
    return {
        "wallet": r.wallet,
        "summary": {
            "trader_type": r.trader_type,
            "copy_rating": r.risk_rating,
            "total_trades": r.total_trades,
            "win_rate_pct": r.win_rate_pct,
            "win_trades": r.win_trades,
            "loss_trades": r.loss_trades,
            "realized_pnl_sol": r.realized_pnl_sol,
            "total_buy_sol": r.total_buy_sol,
            "total_sell_sol": r.total_sell_sol,
            "avg_trade_size_sol": r.avg_trade_size_sol,
        },
        "most_traded_tokens": r.most_traded_tokens,
        "recent_trades": r.recent_trades,
    }


@app.get("/")
def root():
    idx = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(idx):
        return FileResponse(idx)
    return {"name": "Solana Wallet PnL Analyzer", "price": f"${PRICE} USDC/request",
            "endpoint": "GET /pnl?wallet=<ADDRESS>"}


@app.get("/health")
def health():
    helius = bool(os.environ.get("HELIUS_API_KEY"))
    return {"status": "ok", "payment_configured": bool(PAY_TO), "helius_configured": helius}


@app.get("/demo")
async def demo(wallet: str, limit: int = 50):
    """Free endpoint for web UI"""
    if not wallet or len(wallet) < 32:
        raise HTTPException(400, "Invalid wallet address")
    if not os.environ.get("HELIUS_API_KEY"):
        raise HTTPException(503, "HELIUS_API_KEY required for transaction history")
    try:
        r = analyze_wallet(wallet, min(limit, 50))
        return result_to_dict(r)
    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/pnl")
async def pnl(wallet: str, request: Request, limit: int = 100):
    """
    Analyze a Solana wallet's trading PnL and copy-trade rating.
    Requires x402 payment of ${PRICE} USDC per request.

    Parameters:
        wallet: Solana wallet address
        limit:  Number of transactions to analyze (default 100, max 200)

    Returns:
        trader_type, win_rate, realized_pnl_sol, copy_rating, top tokens, recent trades
    """
    if not wallet or len(wallet) < 32:
        raise HTTPException(400, "Invalid wallet address")

    if PAY_TO:
        ph = request.headers.get("X-PAYMENT")
        if not ph:
            return Response(content=json.dumps(payment_requirements()),
                            status_code=402, headers={"Content-Type": "application/json"})
        if not verify_payment(request):
            raise HTTPException(402, "Invalid or expired payment")

    try:
        r = analyze_wallet(wallet, min(limit, 200))
        result = result_to_dict(r)
        if PAY_TO:
            ph = request.headers.get("X-PAYMENT")
            if ph:
                settlement = settle_payment(ph)
                return Response(content=json.dumps(result), status_code=200,
                                headers={"Content-Type": "application/json",
                                         "X-PAYMENT-RESPONSE": json.dumps(settlement)})
        return result
    except Exception as e:
        raise HTTPException(500, str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
