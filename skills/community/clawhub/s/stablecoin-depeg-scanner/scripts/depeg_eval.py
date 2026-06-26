"""
Stablecoin Depeg Evaluator
Automated 3-minute assessment for stablecoin depeg opportunities.

Usage:
    python depeg_eval.py <coin_id_or_symbol> [--peg 1.0]

Example:
    python depeg_eval.py resolv-usr
    python depeg_eval.py USR
    python depeg_eval.py dai --peg 1.0
"""

import sys
import json
import time
import argparse
import urllib.request
import urllib.error
import urllib.parse

# ============================================================
# Config
# ============================================================
COINGECKO_BASE = "https://api.coingecko.com/api/v3"
DEFILLAMA_BASE = "https://api.llama.fi"

# Common stablecoin mappings (symbol -> coingecko id)
SYMBOL_MAP = {
    "USR": "resolv-usr",
    "USDT": "tether",
    "USDC": "usd-coin",
    "DAI": "dai",
    "FRAX": "frax",
    "USDE": "ethena-usde",
    "FDUSD": "first-digital-usd",
    "PYUSD": "paypal-usd",
    "USDD": "usdd",
    "TUSD": "true-usd",
    "LUSD": "liquity-usd",
    "GUSD": "gemini-dollar",
    "SUSD": "susd",
    "CUSD": "celo-dollar",
    "MIM": "magic-internet-money",
    "DOLA": "dola-usd",
    "USDP": "pax-dollar",
    "GHO": "gho",
    "CRVUSD": "crvusd",
    "MKUSD": "prisma-mkusd",
    "USDS": "usds",
}

HEADERS = {"User-Agent": "DepegScanner/1.0", "Accept": "application/json"}

# ============================================================
# HTTP helpers
# ============================================================
def _get(url: str, timeout: int = 20) -> dict | list | None:
    """Simple GET returning parsed JSON or None on error."""
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"[WARN] GET {url} failed: {e}", file=sys.stderr)
        return None


# ============================================================
# Step 1: Get current price & basic info from CoinGecko
# ============================================================
def get_coin_info(coin_id: str) -> dict | None:
    """Fetch coin price, market cap, 24h change, etc."""
    url = (
        f"{COINGECKO_BASE}/coins/{coin_id}"
        "?localization=false&tickers=false&community_data=false"
        "&developer_data=false&sparkline=false"
    )
    data = _get(url)
    if not data:
        return None

    market = data.get("market_data", {})
    return {
        "id": data.get("id"),
        "symbol": data.get("symbol", "").upper(),
        "name": data.get("name"),
        "current_price": market.get("current_price", {}).get("usd", 0),
        "market_cap": market.get("market_cap", {}).get("usd", 0),
        "total_volume_24h": market.get("total_volume", {}).get("usd", 0),
        "price_change_24h_pct": market.get("price_change_percentage_24h", 0),
        "ath": market.get("ath", {}).get("usd", 0),
        "atl": market.get("atl", {}).get("usd", 0),
        "total_supply": market.get("total_supply", 0),
        "circulating_supply": market.get("circulating_supply", 0),
        "description": (data.get("description", {}).get("en", "") or "")[:300],
        "homepage": (data.get("links", {}).get("homepage", [""]) or [""])[0],
        "contract": (
            data.get("platforms", {}).get("ethereum", "")
            or data.get("platforms", {}).get("", "")
        ),
    }


# ============================================================
# Step 2: Get TVL from DefiLlama
# ============================================================
def search_defillama_protocol(coin_name: str, coin_symbol: str) -> dict | None:
    """Search DefiLlama for the protocol and return TVL data."""
    protocols = _get(f"{DEFILLAMA_BASE}/protocols")
    if not protocols:
        return None

    name_lower = coin_name.lower() if coin_name else ""
    sym_lower = coin_symbol.lower() if coin_symbol else ""

    # Score each protocol for relevance
    candidates = []
    for p in protocols:
        pname = (p.get("name") or "").lower()
        psym = (p.get("symbol") or "").lower()
        score = 0

        # Exact symbol match is strong
        if sym_lower and psym == sym_lower:
            score += 100
        # Exact name match
        if name_lower and pname == name_lower:
            score += 100
        # Name contains our search (but penalize very short protocol names to avoid false matches)
        if name_lower and name_lower in pname and len(pname) >= 4:
            score += 50
        if name_lower and pname in name_lower and len(pname) >= 4:
            score += 40
        # Symbol in name
        if sym_lower and sym_lower in pname and len(sym_lower) >= 3:
            score += 30

        if score > 0:
            candidates.append((score, p))

    if not candidates:
        return None

    # Sort by score descending, pick best
    candidates.sort(key=lambda x: x[0], reverse=True)
    best = candidates[0][1]

    tvl = best.get("tvl", 0)
    tvl_prev = best.get("tvlPrevDay", 0)
    tvl_prev_week = best.get("tvlPrevWeek", 0)

    # If no prev day data, try to estimate from protocol detail API
    slug = best.get("slug", "")
    if slug and not tvl_prev:
        detail = _get(f"{DEFILLAMA_BASE}/protocol/{slug}")
        if detail and detail.get("tvl"):
            tvl_history = detail.get("tvl", [])
            if isinstance(tvl_history, list) and len(tvl_history) >= 2:
                tvl_prev = tvl_history[-2].get("totalLiquidityUSD", 0)

    return {
        "protocol_name": best.get("name"),
        "tvl": tvl,
        "tvl_prev_day": tvl_prev,
        "tvl_prev_week": tvl_prev_week,
        "chain": best.get("chain", ""),
        "category": best.get("category", ""),
        "slug": slug,
    }


# ============================================================
# Step 3: Search for security incident info
# ============================================================
def search_exploit_info(coin_name: str, coin_symbol: str) -> dict:
    """
    Try to find exploit-related info.
    Returns a dict with fields we can fill.
    Note: Without a dedicated security API, we return a template
    for the agent to fill via web search.
    """
    return {
        "note": "Auto-search limited. Agent should search Twitter/PeckShield/SlowMist for:",
        "search_queries": [
            f"{coin_name} exploit hack 2026",
            f"{coin_symbol} depeg PeckShield SlowMist",
            f"{coin_name} attack mint vulnerability",
        ],
        "key_questions": [
            "Was collateral stolen or was it a mint/logic exploit?",
            "Has the team paused the protocol?",
            "Is there an official statement or recovery plan?",
            "Has a security firm (PeckShield/SlowMist/CertiK) confirmed the issue?",
        ],
    }


# ============================================================
# Step 4: Calculate depeg metrics & risk assessment
# ============================================================
def assess_depeg(price: float, peg: float, tvl_data: dict | None) -> dict:
    """Core assessment logic."""
    if price <= 0:
        return {"error": "Price is zero or negative, cannot assess"}

    deviation_pct = abs(price - peg) / peg * 100
    odds_ratio = peg / price if price > 0 else 0

    # TVL analysis
    tvl_status = "UNKNOWN"
    tvl_drop_pct = 0
    if tvl_data and tvl_data.get("tvl") and tvl_data.get("tvl_prev_day"):
        tvl = tvl_data["tvl"]
        tvl_prev = tvl_data["tvl_prev_day"]
        if tvl_prev > 0:
            tvl_drop_pct = (tvl_prev - tvl) / tvl_prev * 100
        if tvl > 0 and tvl_drop_pct < 50:
            tvl_status = "INTACT"  # Collateral largely intact
        elif tvl > 0 and tvl_drop_pct < 90:
            tvl_status = "PARTIAL"  # Some collateral lost
        else:
            tvl_status = "DRAINED"  # Collateral gone

    # Scoring
    score = 0
    reasons = []

    # Factor 1: Odds ratio (higher = better opportunity)
    if odds_ratio >= 8:
        score += 40
        reasons.append(f"Extreme discount: {odds_ratio:.1f}x odds (+40)")
    elif odds_ratio >= 5:
        score += 35
        reasons.append(f"Very high discount: {odds_ratio:.1f}x odds (+35)")
    elif odds_ratio >= 3:
        score += 25
        reasons.append(f"High discount: {odds_ratio:.1f}x odds (+25)")
    elif odds_ratio >= 2:
        score += 15
        reasons.append(f"Moderate discount: {odds_ratio:.1f}x odds (+15)")
    elif odds_ratio >= 1.5:
        score += 10
        reasons.append(f"Small discount: {odds_ratio:.1f}x odds (+10)")
    else:
        score += 0
        reasons.append(f"Minimal discount: {odds_ratio:.1f}x odds (+0)")

    # Factor 2: TVL status
    if tvl_status == "INTACT":
        score += 40
        reasons.append(f"TVL intact (drop {tvl_drop_pct:.1f}%) (+40)")
    elif tvl_status == "PARTIAL":
        score += 20
        reasons.append(f"TVL partially lost (drop {tvl_drop_pct:.1f}%) (+20)")
    elif tvl_status == "DRAINED":
        score -= 50
        reasons.append(f"TVL drained (drop {tvl_drop_pct:.1f}%) (-50)")
    else:
        score += 10
        reasons.append("TVL unknown, needs manual check (+10)")

    # Factor 3: Market cap (larger = more likely to recover)
    # Will be filled by caller

    # Determine action
    if score >= 60:
        action = "BUY"
        confidence = "HIGH"
    elif score >= 40:
        action = "BUY"
        confidence = "MEDIUM"
    elif score >= 20:
        action = "WATCH"
        confidence = "LOW"
    else:
        action = "AVOID"
        confidence = "N/A"

    # Position sizing based on odds
    if action == "BUY":
        if odds_ratio >= 8:
            position_pct = 6  # 6% of total capital
        elif odds_ratio >= 5:
            position_pct = 4
        elif odds_ratio >= 3:
            position_pct = 3
        else:
            position_pct = 2
    else:
        position_pct = 0

    return {
        "deviation_pct": round(deviation_pct, 2),
        "odds_ratio": round(odds_ratio, 2),
        "tvl_status": tvl_status,
        "tvl_drop_pct": round(tvl_drop_pct, 2),
        "score": score,
        "score_reasons": reasons,
        "action": action,
        "confidence": confidence,
        "position_pct": position_pct,
    }


# ============================================================
# Step 5: Generate report
# ============================================================
def format_report(
    coin_info: dict,
    tvl_data: dict | None,
    exploit_info: dict,
    assessment: dict,
    peg: float,
    capital: float,
) -> str:
    """Format the final assessment report."""
    price = coin_info.get("current_price", 0)
    symbol = coin_info.get("symbol", "???")
    name = coin_info.get("name", "Unknown")

    action_emoji = {"BUY": "🟢", "WATCH": "🟡", "AVOID": "🔴"}.get(
        assessment["action"], "⚪"
    )

    position_usd = capital * assessment["position_pct"] / 100
    potential_profit = position_usd * (assessment["odds_ratio"] - 1)

    lines = []
    lines.append("=" * 50)
    lines.append(f"  STABLECOIN DEPEG ASSESSMENT: {symbol} ({name})")
    lines.append("=" * 50)
    lines.append("")

    # Price section
    lines.append("--- PRICE ---")
    lines.append(f"  Current Price:  ${price:.4f}")
    lines.append(f"  Peg Target:     ${peg:.2f}")
    lines.append(f"  Deviation:      {assessment['deviation_pct']:.1f}%")
    lines.append(f"  Odds (peg/now): {assessment['odds_ratio']:.1f}x")
    lines.append(f"  24h Change:     {coin_info.get('price_change_24h_pct', 0):.1f}%")
    lines.append("")

    # TVL section
    lines.append("--- TVL (COLLATERAL) ---")
    if tvl_data:
        tvl = tvl_data.get("tvl", 0)
        tvl_prev = tvl_data.get("tvl_prev_day", 0)
        lines.append(f"  Protocol:       {tvl_data.get('protocol_name', 'N/A')}")
        lines.append(f"  Current TVL:    ${tvl/1e6:.1f}M" if tvl else "  Current TVL:    N/A")
        lines.append(
            f"  Previous TVL:   ${tvl_prev/1e6:.1f}M" if tvl_prev else "  Previous TVL:   N/A"
        )
        lines.append(f"  TVL Drop:       {assessment['tvl_drop_pct']:.1f}%")
        lines.append(f"  Status:         {assessment['tvl_status']}")
    else:
        lines.append("  [!] TVL data not found on DefiLlama")
        lines.append("  [!] MANUAL CHECK REQUIRED: search DefiLlama or Etherscan")
    lines.append("")

    # Market info
    lines.append("--- MARKET INFO ---")
    mc = coin_info.get("market_cap", 0)
    vol = coin_info.get("total_volume_24h", 0)
    supply = coin_info.get("circulating_supply", 0)
    lines.append(f"  Market Cap:     ${mc/1e6:.1f}M" if mc else "  Market Cap:     N/A")
    lines.append(f"  24h Volume:     ${vol/1e6:.1f}M" if vol else "  24h Volume:     N/A")
    lines.append(
        f"  Circulating:    {supply/1e6:.1f}M tokens" if supply else "  Circulating:    N/A"
    )
    contract = coin_info.get("contract", "")
    if contract:
        lines.append(f"  Contract:       {contract}")
    lines.append("")

    # Exploit info
    lines.append("--- EXPLOIT ANALYSIS (AGENT MUST VERIFY) ---")
    for q in exploit_info.get("key_questions", []):
        lines.append(f"  [ ] {q}")
    lines.append("")
    lines.append("  Suggested searches:")
    for sq in exploit_info.get("search_queries", []):
        lines.append(f"    - {sq}")
    lines.append("")

    # Score
    lines.append("--- ASSESSMENT ---")
    lines.append(f"  Score:          {assessment['score']}/80")
    for r in assessment.get("score_reasons", []):
        lines.append(f"    • {r}")
    lines.append("")

    # Action
    lines.append("--- RECOMMENDATION ---")
    lines.append(f"  {action_emoji} Action:   {assessment['action']}")
    lines.append(f"  Confidence:     {assessment['confidence']}")
    if assessment["action"] == "BUY":
        lines.append(f"  Position Size:  {assessment['position_pct']}% of capital = ${position_usd:.0f}")
        lines.append(f"  If re-pegs:     +${potential_profit:.0f} ({assessment['odds_ratio']:.1f}x)")
        lines.append(f"  Max Loss:       -${position_usd:.0f}")
        lines.append("")
        lines.append("  EXECUTION:")
        lines.append("    1. Buy on DEX (Uniswap/Curve) - CEX may not list")
        lines.append("    2. Split into 2-3 orders (don't go all at once)")
        lines.append("    3. Set mental stop: team announces unrecoverable -> sell immediately")
        lines.append(f"    4. Target exit: ${peg * 0.9:.2f} - ${peg:.2f}")
    elif assessment["action"] == "WATCH":
        lines.append("  Wait for: team statement / security audit / more TVL data")
        lines.append("  Re-evaluate in 1-2 hours")
    else:
        lines.append("  Reason: Risk too high or insufficient data")
    lines.append("")
    lines.append("=" * 50)
    lines.append("  ⚠️  AGENT MUST complete exploit analysis above")
    lines.append("  ⚠️  before forwarding recommendation to user")
    lines.append("=" * 50)

    return "\n".join(lines)


# ============================================================
# Main
# ============================================================
def evaluate(coin_input: str, peg: float = 1.0, capital: float = 5000.0) -> str:
    """
    Main entry point.
    
    Args:
        coin_input: CoinGecko ID or symbol (e.g., "resolv-usr" or "USR")
        peg: Target peg price (default 1.0 for USD stablecoins)
        capital: Total available capital in USD
    
    Returns:
        Formatted assessment report string
    """
    # Resolve symbol to coingecko id
    coin_id = coin_input.lower()
    upper = coin_input.upper()
    if upper in SYMBOL_MAP:
        coin_id = SYMBOL_MAP[upper]

    print(f"[1/4] Fetching coin data for '{coin_id}'...", file=sys.stderr)
    coin_info = get_coin_info(coin_id)
    if not coin_info:
        return f"ERROR: Could not find coin '{coin_input}' on CoinGecko. Try using the CoinGecko ID (e.g., 'resolv-usr')."

    price = coin_info["current_price"]
    if price <= 0:
        return f"ERROR: Price for {coin_info['symbol']} is ${price}. Cannot assess."

    deviation = abs(price - peg) / peg * 100
    if deviation < 5:
        return f"INFO: {coin_info['symbol']} is at ${price:.4f}, only {deviation:.1f}% from peg. No significant depeg detected."

    print(f"[2/4] Searching TVL on DefiLlama...", file=sys.stderr)
    tvl_data = search_defillama_protocol(coin_info["name"], coin_info["symbol"])

    print(f"[3/4] Preparing exploit analysis template...", file=sys.stderr)
    exploit_info = search_exploit_info(coin_info["name"], coin_info["symbol"])

    print(f"[4/4] Running assessment...", file=sys.stderr)
    assessment = assess_depeg(price, peg, tvl_data)

    report = format_report(coin_info, tvl_data, exploit_info, assessment, peg, capital)
    return report


def main():
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="Stablecoin Depeg Evaluator")
    parser.add_argument("coin", help="CoinGecko ID or symbol (e.g., resolv-usr, USR, DAI)")
    parser.add_argument("--peg", type=float, default=1.0, help="Target peg price (default: 1.0)")
    parser.add_argument("--capital", type=float, default=5000.0, help="Total capital in USD (default: 5000)")
    args = parser.parse_args()

    report = evaluate(args.coin, args.peg, args.capital)
    print(report)


if __name__ == "__main__":
    main()
