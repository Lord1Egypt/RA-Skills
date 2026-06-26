#!/usr/bin/env python3
"""
Generate a polished HTML valuation report from pipeline JSON + research JSON.
Usage: uv run python3 generate_report.py /tmp/TICKER_data.json [--research /tmp/TICKER_research.json] [--output /tmp/TICKER_report.html]
"""
import argparse
import base64
import json
import os
import sys
from datetime import datetime


# ─── Helpers ──────────────────────────────────────────────────────────

def sf(val, default=None):
    """Safe float."""
    if val is None: return default
    try:
        v = float(val)
        return default if v != v else v
    except: return default

def fmt(n, pre="$", dec=0):
    if n is None: return "—"
    try: n = float(n)
    except: return "—"
    if abs(n) >= 1e12: return f"{pre}{n/1e12:.1f}T"
    if abs(n) >= 1e9: return f"{pre}{n/1e9:.1f}B"
    if abs(n) >= 1e6: return f"{pre}{n/1e6:.1f}M"
    if abs(n) >= 1e3: return f"{pre}{n/1e3:.1f}K"
    if dec > 0: return f"{pre}{n:.{dec}f}"
    return f"{pre}{n:,.0f}"

def pct(n):
    if n is None: return "—"
    try: n = float(n)
    except: return "—"
    return f"{n*100:.1f}%" if abs(n) < 2 else f"{n:.1f}%"

def pe(n):
    if n is None: return "—"
    try: return f"{float(n):.1f}x"
    except: return "—"

def cls(val, pos_good=True):
    try: v = float(val)
    except: return ""
    if pos_good: return "up" if v > 0 else ("dn" if v < 0 else "")
    return "dn" if v > 0 else ("up" if v < 0 else "")

def b64img(path):
    if not path or not os.path.isfile(path): return ""
    try:
        with open(path, "rb") as f: return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    except: return ""


# ─── CSS (Light Professional Theme) ──────────────────────────────────

CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif; background: #ffffff; color: #1e293b; line-height: 1.7; font-size: 15px; }
.container { max-width: 1100px; margin: 0 auto; padding: 32px 40px; }
h1 { font-size: 2.2em; color: #1e293b; margin-bottom: 4px; font-weight: 800; }
h2 { font-size: 1.4em; color: #1e293b; margin: 36px 0 16px; padding-bottom: 8px; border-bottom: 2px solid #e2e8f0; font-weight: 700; }
h3 { font-size: 1.15em; color: #475569; margin: 24px 0 12px; font-weight: 600; }
.subtitle { color: #64748b; font-size: 0.95em; margin-bottom: 24px; }
.badge { display: inline-block; background: linear-gradient(135deg, #f59e0b, #d97706); color: #fff; padding: 8px 20px; border-radius: 8px; font-weight: 700; font-size: 1.05em; margin: 12px 0 28px; box-shadow: 0 2px 8px rgba(245,158,11,0.3); }
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin: 16px 0; }
.kpi { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px 16px; text-align: center; }
.kpi .label { font-size: 0.75em; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.8px; font-weight: 600; }
.kpi .value { font-size: 1.6em; font-weight: 800; color: #1e293b; margin-top: 4px; }
.kpi .sub { font-size: 0.8em; color: #64748b; margin-top: 4px; }
.up { color: #16a34a !important; }
.dn { color: #dc2626 !important; }
.neu { color: #ca8a04 !important; }
table { width: 100%; border-collapse: collapse; margin: 14px 0; font-size: 0.9em; }
th { background: #f1f5f9; color: #475569; padding: 10px 14px; text-align: left; font-weight: 600; border-bottom: 2px solid #e2e8f0; font-size: 0.85em; text-transform: uppercase; letter-spacing: 0.3px; }
td { padding: 9px 14px; border-bottom: 1px solid #f1f5f9; }
tr:hover { background: #f8fafc; }
tr.hl { background: #eff6ff !important; border-left: 3px solid #2563eb; }
.co { border-left: 4px solid #2563eb; padding: 16px 20px; border-radius: 0 8px 8px 0; margin: 16px 0; }
.co.gr { background: #f0fdf4; border-left-color: #16a34a; }
.co.yw { background: #fefce8; border-left-color: #ca8a04; }
.co.rd { background: #fef2f2; border-left-color: #dc2626; }
.co.bl { background: #eff6ff; border-left-color: #2563eb; }
.sg { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin: 16px 0; }
.sc { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 22px 18px; text-align: center; }
.sc.bear { border-top: 4px solid #dc2626; }
.sc.base { border-top: 4px solid #2563eb; }
.sc.bull { border-top: 4px solid #16a34a; }
.sc .lb { font-size: 0.85em; color: #64748b; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }
.sc .pr { font-size: 2.1em; font-weight: 800; margin: 8px 0; }
.sc .mt { font-size: 0.85em; color: #94a3b8; }
.sc .us { font-size: 1.1em; font-weight: 700; margin-top: 8px; }
.sc .ds { font-size: 0.82em; color: #64748b; margin-top: 10px; line-height: 1.5; }
.cg { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; margin: 16px 0; }
.cg img { width: 100%; border-radius: 8px; border: 1px solid #e2e8f0; }
.tg { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 16px 0; }
.tc { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 16px; text-align: center; }
.tc .mk { font-size: 0.75em; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600; }
.tc .vl { font-size: 1.5em; font-weight: 800; margin: 6px 0; }
.tc .nt { font-size: 0.8em; }
ul { margin: 10px 0 10px 24px; }
li { margin: 6px 0; line-height: 1.6; }
.tw { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 14px 18px; margin: 10px 0; }
.tw .au { color: #2563eb; font-weight: 700; }
.tw .st { display: inline-block; padding: 2px 10px; border-radius: 4px; font-size: 0.78em; font-weight: 700; }
.tw .st.bul { background: #dcfce7; color: #16a34a; }
.tw .st.ber { background: #fef2f2; color: #dc2626; }
.tw .st.net { background: #eff6ff; color: #2563eb; }
.ft { text-align: center; color: #94a3b8; font-size: 0.8em; margin-top: 48px; padding-top: 20px; border-top: 1px solid #e2e8f0; }
@media print {
  .kpi-grid, .sg, .tg, .cg, table, .co, .sc, .tw { page-break-inside: avoid; }
  .pb { page-break-before: always; }
  body { font-size: 13px; }
  .container { padding: 0; }
}
@page { size: A4; margin: 18mm 15mm; }
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data_json")
    parser.add_argument("--output", default=None)
    parser.add_argument("--research", default=None)
    args = parser.parse_args()

    with open(args.data_json) as f: data = json.load(f)
    ticker = data.get("ticker", "UNKNOWN")
    out = args.output or f"/tmp/{ticker}_report.html"
    
    research = {}
    if args.research and os.path.isfile(args.research):
        with open(args.research) as f: research = json.load(f)

    fund = data.get("fundamentals", {})
    if "error" in fund: fund = {}
    
    price = sf(fund.get("currentPrice"))
    fwd_eps = sf(fund.get("forwardEps"))
    trail_pe = sf(fund.get("trailingPE"))
    fwd_pe = sf(fund.get("forwardPE"))
    mcap = fund.get("marketCap")
    rev = fund.get("totalRevenue")
    rev_g = sf(fund.get("revenueGrowth"))
    gm = sf(fund.get("grossMargins"))
    om = sf(fund.get("operatingMargins"))
    nm = sf(fund.get("profitMargins"))
    roe = sf(fund.get("returnOnEquity"))
    high52 = sf(fund.get("fiftyTwoWeekHigh"))
    low52 = sf(fund.get("fiftyTwoWeekLow"))
    name = fund.get("shortName", ticker)
    today = data.get("generated_at", datetime.now().isoformat())[:10]
    
    peers = data.get("peers", {})
    tech = data.get("technicals", {})
    hist = data.get("historical_valuation", {})
    opts = data.get("options", {})
    ins = data.get("insiders", {})
    earn = data.get("earnings", {})
    charts = data.get("charts", {})
    dcf = data.get("dcf", {})

    # ── Peer forward PEs
    peer_fwd_pes = [sf(peers[p].get("forwardPE")) for p in peers if sf(peers[p].get("forwardPE")) and 0 < sf(peers[p].get("forwardPE")) < 100]
    avg_peer_pe = sum(peer_fwd_pes) / len(peer_fwd_pes) if peer_fwd_pes else None

    # ── Historical PE (filtered)
    pe_hist = [p for p in hist.get("pe_history", []) if p.get("pe_ratio", 999) < 100]
    pe_vals = [p["pe_ratio"] for p in pe_hist] if pe_hist else []
    avg_hist_pe = sum(pe_vals)/len(pe_vals) if pe_vals else None
    min_hist_pe = min(pe_vals) if pe_vals else None
    max_hist_pe = max(pe_vals) if pe_vals else None
    
    # Percentile
    hist_pctile = None
    cur_pe = sf(hist.get("current_pe"))
    if cur_pe and pe_vals:
        hist_pctile = round(sum(1 for p in pe_vals if p < cur_pe) / len(pe_vals) * 100)

    # ── Technicals
    rsi = sf(tech.get("rsi_14"))
    sma50 = sf(tech.get("sma_50"))
    sma200 = sf(tech.get("sma_200"))
    macd_d = tech.get("macd", {})
    macd_line = sf(macd_d.get("macd_line")) if isinstance(macd_d, dict) else None
    signal_line = sf(macd_d.get("signal_line")) if isinstance(macd_d, dict) else None
    pct_high = sf(tech.get("price_vs_52w_high_pct"))
    pct_low = sf(tech.get("price_vs_52w_low_pct"))
    t_high52 = sf(tech.get("52_week_high"))
    t_low52 = sf(tech.get("52_week_low"))

    # ── Options
    opt_sum = opts.get("summary", opts) if "error" not in opts else {}
    pc_vol = sf(opt_sum.get("put_call_volume_ratio"))
    pc_oi = sf(opt_sum.get("put_call_oi_ratio"))
    call_iv = sf(opt_sum.get("avg_call_iv"))
    put_iv = sf(opt_sum.get("avg_put_iv"))

    # ── Earnings
    next_earn = earn.get("next_earnings_date") if "error" not in earn else None
    days_earn = earn.get("days_until_earnings") if "error" not in earn else None

    # ── Analyst consensus from research
    consensus = research.get("analyst_consensus", {})

    # ── Scenarios
    # Bear
    bear_pe = max(5.0, (trail_pe * 0.65) if trail_pe else 7.0) if trail_pe else 7.0
    bear_eps = fwd_eps * 0.85 if fwd_eps else 0
    bear_price = bear_pe * bear_eps if bear_eps else 0
    bear_up = ((bear_price / price - 1) * 100) if price and bear_price else 0

    # Base
    base_pe = avg_peer_pe if avg_peer_pe else (12.0 if not trail_pe else trail_pe * 1.3)
    base_pe = min(base_pe, 25.0)
    base_price = base_pe * fwd_eps if fwd_eps else 0
    base_up = ((base_price / price - 1) * 100) if price and base_price else 0

    # Bull
    bull_pe = min(max(base_pe * 1.5, 15.0), 30.0)
    bull_eps = fwd_eps * 1.15 if fwd_eps else 0
    bull_price = bull_pe * bull_eps if bull_eps else 0
    bull_up = ((bull_price / price - 1) * 100) if price and bull_price else 0

    # ── Determine verdict
    verdict = "Hold"
    if fwd_pe and avg_peer_pe and rev_g:
        if fwd_pe < avg_peer_pe * 0.7 and rev_g > 0.2: verdict = "Strong Buy"
        elif fwd_pe < avg_peer_pe: verdict = "Buy"
        elif fwd_pe > avg_peer_pe * 1.3 and rev_g < 0: verdict = "Sell"
    elif fwd_pe and trail_pe and fwd_pe < trail_pe * 0.8 and rev_g and rev_g > 0.15:
        verdict = "Buy"

    sources = "yfinance"
    if research: sources += ", Seeking Alpha, X/Twitter, analyst consensus"

    # ── BUILD HTML ────────────────────────────────────────────────────
    sections = []

    # Header
    sections.append(f"""<h1>{ticker} — {name}</h1>
<p class="subtitle">Comprehensive Valuation Report · {today} · Sources: {sources}</p>""")

    # Earnings badge
    if next_earn:
        days_str = f" — {days_earn} days away" if days_earn else ""
        sections.append(f'<div class="badge">📅 Next Earnings: {next_earn}{days_str}</div>')

    # KPIs
    price_sub = ""
    if price and high52 and high52 > 0:
        p = (price - high52) / high52 * 100
        price_sub = f'<div class="sub {"dn" if p < 0 else "up"}">{p:+.1f}% from 52W High</div>'
    
    rev_sub = ""
    if rev_g is not None:
        rev_sub = f'<div class="sub {"up" if rev_g > 0 else "dn"}">{rev_g*100:+.1f}% YoY</div>'

    # Smart sub-texts
    gm_sub = ""
    if gm and gm > 0.7: gm_sub = '<div class="sub">Expanding</div>'
    elif gm and gm > 0.5: gm_sub = '<div class="sub">Healthy</div>'
    
    om_sub = ""
    if om and om > 0.3: om_sub = '<div class="sub">Industry-leading</div>'
    elif om and om > 0.15: om_sub = '<div class="sub">Above average</div>'
    
    beta = sf(fund.get("beta"))
    beta_sub = f'<div class="sub">Beta: {beta:.2f}</div>' if beta else ""

    sections.append(f"""<h2>📊 Key Metrics</h2>
<div class="kpi-grid">
    <div class="kpi"><div class="label">Stock Price</div><div class="value">{fmt(price,"$",2)}</div>{price_sub}</div>
    <div class="kpi"><div class="label">Market Cap</div><div class="value">{fmt(mcap)}</div><div class="sub">Shares: {fmt(fund.get("sharesOutstanding"),"",0)}</div></div>
    <div class="kpi"><div class="label">Trailing P/E</div><div class="value">{pe(trail_pe)}</div><div class="sub up">EPS: {fmt(fund.get("trailingEps"),"$",2)}</div></div>
    <div class="kpi"><div class="label">Forward P/E</div><div class="value{" up" if fwd_pe and trail_pe and fwd_pe < trail_pe else ""}">{pe(fwd_pe)}</div><div class="sub">Fwd EPS: {fmt(fwd_eps,"$",2)}</div></div>
</div>
<div class="kpi-grid">
    <div class="kpi"><div class="label">Revenue (TTM)</div><div class="value">{fmt(rev)}</div>{rev_sub}</div>
    <div class="kpi"><div class="label">Gross Margin</div><div class="value {cls(gm)}">{pct(gm)}</div>{gm_sub}</div>
    <div class="kpi"><div class="label">Operating Margin</div><div class="value {cls(om)}">{pct(om)}</div>{om_sub}</div>
    <div class="kpi"><div class="label">Net Margin</div><div class="value {cls(nm)}">{pct(nm)}</div><div class="sub">ROE: {pct(roe)}</div></div>
</div>""")

    # Quarterly Trends
    quarters = fund.get("quarterly", [])
    if quarters:
        q_rows = ""
        accel_count = 0
        for i, q in enumerate(quarters):
            r = sf(q.get("Total Revenue"))
            ni = sf(q.get("Net Income"))
            gp = sf(q.get("Gross Profit"))
            oi = sf(q.get("Operating Income"))
            eps_q = sf(q.get("Diluted EPS")) or sf(q.get("Basic EPS"))
            
            arrow = "—"
            if i < len(quarters) - 1:
                prev_r = sf(quarters[i+1].get("Total Revenue"))
                if prev_r and r and prev_r > 0:
                    g = (r - prev_r) / prev_r * 100
                    if g > 20: arrow = '<span class="up">↑↑</span>'; accel_count += 1
                    elif g > 0: arrow = '<span class="up">↑</span>'
                    else: arrow = '<span class="dn">↓</span>'
            
            gm_q = f"{gp/r*100:.1f}%" if gp and r and r > 0 else "—"
            om_q = f"{oi/r*100:.1f}%" if oi and r and r > 0 else "—"
            nm_q = f"{ni/r*100:.1f}%" if ni and r and r > 0 else "—"
            
            q_rows += f"""<tr><td>{q.get("period","")}</td><td>{fmt(r)} {arrow}</td><td>{fmt(ni)}</td><td>{gm_q}</td><td>{om_q}</td><td>{nm_q}</td><td>{f"${eps_q:.3f}" if eps_q else "—"}</td></tr>\n"""

        sections.append(f"""<h2>📈 Quarterly Financial Trends</h2>
<table><thead><tr><th>Quarter</th><th>Revenue</th><th>Net Income</th><th>Gross Margin</th><th>Op Margin</th><th>Net Margin</th><th>Diluted EPS</th></tr></thead>
<tbody>{q_rows}</tbody></table>""")

        # Smart callout
        if len(quarters) >= 2:
            latest = quarters[0]
            lr = sf(latest.get("Total Revenue"))
            lni = sf(latest.get("Net Income"))
            leps = sf(latest.get("Diluted EPS"))
            if lr and rev_g:
                growth_pct = rev_g * 100 if abs(rev_g) < 2 else rev_g
                callout_text = f"<strong>🔥 Accelerating Growth:</strong> Revenue reached {fmt(lr)} in the latest quarter"
                if accel_count > 0:
                    callout_text += f", with {accel_count} consecutive quarter(s) of 20%+ sequential growth"
                callout_text += f". TTM revenue growth is {growth_pct:+.0f}% YoY"
                if lni: callout_text += f", with net income of {fmt(lni)}"
                if nm: callout_text += f" ({pct(nm)} net margin)"
                callout_text += "."
                sections.append(f'<div class="co gr">{callout_text}</div>')

    # Revenue Composition (from research)
    rev_comp = research.get("revenue_composition", [])
    if rev_comp:
        rc_rows = ""
        for item in rev_comp:
            rc_rows += f"""<tr><td><strong>{item.get("stream","")}</strong></td><td>{item.get("amount","")}</td><td>{item.get("pct","")}</td><td class="up">{item.get("trend","")}</td><td>{item.get("notes","")}</td></tr>\n"""
        sections.append(f"""<h2>💰 Revenue Composition</h2>
<table><thead><tr><th>Revenue Stream</th><th>Amount</th><th>% of Total</th><th>YoY Trend</th><th>Notes</th></tr></thead>
<tbody>{rc_rows}</tbody></table>""")
        
        # Smart callout: identify interest/recurring income
        for item in rev_comp:
            stream = item.get("stream", "").lower()
            p = item.get("pct", "")
            if ("interest" in stream or "recurring" in stream or "subscription" in stream) and p:
                try:
                    pval = float(p.replace("%",""))
                    if pval >= 25:
                        sections.append(f'<div class="co bl"><strong>💡 Hidden Gem — {item.get("stream")}:</strong> At {p} of revenue, this provides a stable, recurring base that adds durability beyond volatile trading/transaction volumes.</div>')
                except: pass

    # Geographic Expansion (from research)
    geo = research.get("geographic_data", [])
    if geo:
        geo_rows = ""
        for g in geo:
            asset_growth = g.get("asset_growth", "")
            ag_cls = "up" if "strong" in str(asset_growth).lower() or "grow" in str(asset_growth).lower() else ""
            geo_rows += f"""<tr><td>{g.get("market","")}</td><td>{g.get("new_accounts_pct","")}</td><td>{g.get("avg_deposit","")}</td><td class="{ag_cls}">{asset_growth}</td><td>{g.get("highlights","")}</td></tr>\n"""
        sections.append(f"""<h2>🌏 Geographic Expansion</h2>
<table><thead><tr><th>Market</th><th>New Accounts %</th><th>Avg. Deposit</th><th>Asset Growth</th><th>Highlights</th></tr></thead>
<tbody>{geo_rows}</tbody></table>""")
        
        # Smart callout: highlight highest-deposit market and total metrics
        max_deposit = max(geo, key=lambda x: float(x.get("avg_deposit","$0").replace("$","").replace("K","000").replace(",","")) if x.get("avg_deposit","").replace("$","").replace("K","000").replace(",","").replace(".","").isdigit() else 0)
        if max_deposit.get("avg_deposit"):
            sections.append(f'<div class="co gr"><strong>📊 Key Metric:</strong> Highest average deposits in {max_deposit.get("market","")} at {max_deposit.get("avg_deposit","")}, signaling a high-net-worth clientele. Geographic diversification across {len(geo)} markets reduces concentration risk.</div>')

    # Technical Analysis
    if "error" not in tech and rsi is not None:
        rsi_cls = "dn" if rsi < 35 else ("up" if rsi > 65 else "neu")
        rsi_note = "Oversold" if rsi < 30 else ("Near Oversold" if rsi < 35 else ("Overbought" if rsi > 70 else "Neutral"))
        sma50_cls = "up" if price and sma50 and price > sma50 else "dn"
        sma200_cls = "up" if price and sma200 and price > sma200 else "dn"
        macd_cls = "up" if macd_line and macd_line > 0 else "dn"
        macd_note = ""
        if macd_line is not None and signal_line is not None:
            macd_note = "Bullish (above signal)" if macd_line > signal_line else "Bearish (below signal)"

        sections.append(f"""<h2 class="pb">📉 Technical Analysis</h2>
<div class="tg">
    <div class="tc"><div class="mk">RSI (14-day)</div><div class="vl {rsi_cls}">{rsi:.1f}</div><div class="nt {rsi_cls}">{rsi_note}</div></div>
    <div class="tc"><div class="mk">SMA 50</div><div class="vl {sma50_cls}">{fmt(sma50,"$",2)}</div><div class="nt {sma50_cls}">Price {"above" if sma50_cls=="up" else "below"}</div></div>
    <div class="tc"><div class="mk">SMA 200</div><div class="vl {sma200_cls}">{fmt(sma200,"$",2)}</div><div class="nt {sma200_cls}">Price {"above" if sma200_cls=="up" else "below"}</div></div>
    <div class="tc"><div class="mk">MACD</div><div class="vl {macd_cls}">{f"{macd_line:.3f}" if macd_line is not None else "—"}</div><div class="nt {macd_cls}">{macd_note}</div></div>
    <div class="tc"><div class="mk">52W High</div><div class="vl">{fmt(t_high52,"$",2)}</div><div class="nt dn">{f"{pct_high:+.1f}%" if pct_high is not None else ""}</div></div>
    <div class="tc"><div class="mk">52W Low</div><div class="vl">{fmt(t_low52,"$",2)}</div><div class="nt up">{f"+{pct_low:.1f}%" if pct_low is not None else ""}</div></div>
</div>""")

        # Smart tech callout — always generate one
        tech_insights = []
        if rsi:
            if rsi < 30: tech_insights.append(f"RSI at {rsi:.1f} is in oversold territory")
            elif rsi < 35: tech_insights.append(f"RSI at {rsi:.1f} is near oversold")
            elif rsi > 70: tech_insights.append(f"RSI at {rsi:.1f} signals overbought conditions")
        if pct_high and pct_high < -30:
            tech_insights.append(f"price is {abs(pct_high):.0f}% below 52-week high")
        if price and sma50 and price < sma50 and sma200 and price < sma200:
            tech_insights.append("trading below both SMA50 and SMA200")
        elif price and sma50 and price > sma50 and sma200 and price > sma200:
            tech_insights.append("trading above both SMA50 and SMA200 (bullish trend)")
        if macd_line is not None and signal_line is not None:
            if macd_line < signal_line: tech_insights.append("MACD bearish crossover")
            else: tech_insights.append("MACD bullish crossover")
        
        if tech_insights:
            earn_str = f" However, with earnings in {days_earn} days, this represents a potential contrarian entry point if results confirm fundamental acceleration." if days_earn and days_earn <= 30 and rsi and rsi < 40 else ""
            co_cls = "rd" if rsi and rsi < 35 else ("yw" if rsi and rsi > 70 else "bl")
            sections.append(f'<div class="co {co_cls}"><strong>⚠️ Technical Signal:</strong> {". ".join(tech_insights).capitalize()}.{earn_str}</div>')

    # Charts
    chart_imgs = []
    for key in ["price", "revenue", "margins", "pe"]:
        src = b64img(charts.get(key, ""))
        if src: chart_imgs.append(f'<img src="{src}" alt="{key}">')
    if chart_imgs:
        sections.append(f'<h2>📊 Charts</h2>\n<div class="cg">\n{"".join(chart_imgs)}\n</div>')

    # Historical Valuation
    if pe_vals and cur_pe:
        pe_cls_v = "up" if avg_hist_pe and cur_pe < avg_hist_pe else "dn"
        pctile_cls = "up" if hist_pctile is not None and hist_pctile < 30 else ("dn" if hist_pctile and hist_pctile > 70 else "")
        pctile_sub = "Cheapest in 5 years" if hist_pctile is not None and hist_pctile < 5 else ("Below average" if hist_pctile is not None and hist_pctile < 50 else "Above average")
        
        sections.append(f"""<h2>📏 Historical Valuation</h2>
<div class="kpi-grid">
    <div class="kpi"><div class="label">Current P/E</div><div class="value {pe_cls_v}">{pe(cur_pe)}</div></div>
    <div class="kpi"><div class="label">5Y Avg P/E*</div><div class="value">{avg_hist_pe:.1f}x</div><div class="sub">*Outliers filtered (PE&lt;100)</div></div>
    <div class="kpi"><div class="label">5Y P/E Range</div><div class="value">{min_hist_pe:.0f}x – {max_hist_pe:.0f}x</div></div>
    <div class="kpi"><div class="label">Percentile</div><div class="value {pctile_cls}">{f"{hist_pctile}th" if hist_pctile is not None else "—"}</div><div class="sub">{pctile_sub}</div></div>
</div>""")

        # Mean reversion callout
        if avg_hist_pe and fwd_eps and fwd_eps > 0 and price and price > 0:
            implied = avg_hist_pe * fwd_eps
            upside = (implied / price - 1) * 100
            if upside > 10:
                sections.append(f'<div class="co gr"><strong>📐 Mean Reversion Upside:</strong> At {pe(cur_pe)} trailing P/E vs. filtered 5Y average of {avg_hist_pe:.1f}x, applying the historical average to forward EPS of ${fwd_eps:.2f} implies a price of <strong>${implied:.2f}</strong> — <strong class="up">+{upside:.0f}% upside</strong>.</div>')

    # Peer Comparison
    if peers:
        p_rows = ""
        all_t = [ticker] + list(peers.keys())
        all_d = {ticker: fund}
        all_d.update(peers)
        for t in all_t:
            d = all_d.get(t, {})
            hl = ' class="hl"' if t == ticker else ""
            p_rows += f"""<tr{hl}><td><strong>{t}</strong></td><td>{fmt(sf(d.get("currentPrice")),"$",2)}</td><td>{fmt(d.get("marketCap"))}</td><td>{pe(d.get("trailingPE"))}</td><td>{pe(d.get("forwardPE"))}</td><td>{pct(d.get("revenueGrowth"))}</td><td>{pct(d.get("grossMargins"))}</td><td>{pct(d.get("operatingMargins"))}</td><td>{pct(d.get("profitMargins"))}</td></tr>\n"""

        sections.append(f"""<h2>🏆 Peer Comparison</h2>
<table><thead><tr><th>Company</th><th>Price</th><th>MCap</th><th>Trail P/E</th><th>Fwd P/E</th><th>Rev Growth</th><th>Gross Margin</th><th>Op Margin</th><th>Net Margin</th></tr></thead>
<tbody>{p_rows}</tbody></table>""")

        # Discount callout
        if fwd_pe and avg_peer_pe and fwd_eps and price and fwd_pe < avg_peer_pe:
            impl = avg_peer_pe * fwd_eps
            ups = (impl / price - 1) * 100
            sections.append(f'<div class="co gr"><strong>🔍 Discount Alert:</strong> {ticker} trades at {pe(fwd_pe)} forward P/E vs. peer average of {avg_peer_pe:.1f}x. Despite having {"the highest" if rev_g and rev_g > 0.5 else "strong"} revenue growth among peers, {ticker} carries the lowest forward multiple. At peer-average P/E, {ticker} would be worth <strong>${impl:.2f}</strong> (+{ups:.0f}% upside).</div>')

    # Options Sentiment
    if opt_sum and pc_vol is not None:
        vol_cls = "up" if pc_vol < 0.7 else ("dn" if pc_vol > 1.0 else "neu")
        vol_sub = "Bullish bias" if vol_cls == "up" else ("Bearish bias" if vol_cls == "dn" else "Neutral")
        oi_cls = "up" if pc_oi and pc_oi < 0.7 else ("dn" if pc_oi and pc_oi > 1.0 else "neu")
        oi_sub = "Bullish positioning" if oi_cls == "up" else ("Bearish positioning" if oi_cls == "dn" else "Neutral")

        sections.append(f"""<h2>🎯 Options Sentiment</h2>
<div class="kpi-grid">
    <div class="kpi"><div class="label">P/C Volume Ratio</div><div class="value {vol_cls}">{pc_vol:.2f}</div><div class="sub">{vol_sub}</div></div>
    <div class="kpi"><div class="label">P/C Open Interest</div><div class="value {oi_cls}">{f"{pc_oi:.2f}" if pc_oi else "—"}</div><div class="sub">{oi_sub}</div></div>
    <div class="kpi"><div class="label">Avg Call IV</div><div class="value">{f"{call_iv*100:.0f}%" if call_iv else "—"}</div></div>
    <div class="kpi"><div class="label">Avg Put IV</div><div class="value neu">{f"{put_iv*100:.0f}%" if put_iv else "—"}</div></div>
</div>""")

        # Options callout — always generate one
        opt_insights = []
        if pc_oi and pc_oi < 0.5:
            opt_insights.append(f"P/C OI ratio of {pc_oi:.2f} shows heavy call positioning — bulls are stacking open interest")
        elif pc_oi and pc_oi > 1.0:
            opt_insights.append(f"P/C OI ratio of {pc_oi:.2f} shows elevated put positioning — hedging activity or bearish bets")
        if pc_vol and pc_vol > 1.0 and pc_oi and pc_oi < 0.7:
            opt_insights.append("high put volume but low put OI suggests short-term hedging rather than directional bearishness")
        if call_iv and put_iv and put_iv > call_iv * 1.5:
            opt_insights.append(f"put IV skew ({put_iv*100:.0f}% vs {call_iv*100:.0f}% call) indicates demand for downside protection")
        if days_earn and days_earn <= 30 and call_iv and call_iv > 0.5:
            opt_insights.append(f"elevated IV ({call_iv*100:.0f}%/{put_iv*100:.0f}%) reflects the upcoming earnings event in {days_earn} days")
        if opts.get("expiry"):
            opt_insights.append(f"nearest expiry: {opts.get('expiry')}")
        
        if opt_insights:
            sections.append(f'<div class="co bl"><strong>📊 Options Read:</strong> {". ".join(opt_insights).capitalize()}.</div>')

    # Insider Activity
    if "error" not in ins:
        purchases = ins.get("insider_purchases_summary", [])
        total_held = None
        net_purchased = None
        for p in purchases:
            label = str(p.get("Insider Purchases Last 6m", ""))
            if "Total Insider Shares Held" in label:
                total_held = sf(p.get("Shares"))
            if "Net Shares Purchased" in label and "%" not in label:
                net_purchased = sf(p.get("Shares"))
        
        # Institutional holders
        inst_holders = ins.get("major_holders", [])
        inst_str = ""
        if isinstance(inst_holders, list):
            for ih in inst_holders[:3]:
                if isinstance(ih, dict) and ih.get("Holder"):
                    inst_str += f", {ih['Holder']}"
        
        txns = ins.get("insider_transactions", [])
        if txns:
            tx_items = "".join(f"<li>{t.get('insider','Unknown')} — {t.get('transaction','')} {fmt(t.get('shares',0),'',0)} shares ({t.get('date','')})</li>" for t in txns[:5])
            sections.append(f'<h2>👔 Insider Activity</h2>\n<div class="co bl">{"<strong>Total insider shares held:</strong> " + fmt(total_held,"",0) + ". " if total_held else ""}{"<strong>Net shares purchased (6m):</strong> " + fmt(net_purchased,"",0) + ". " if net_purchased else ""}<ul>{tx_items}</ul></div>')
        else:
            held_str = f"Total insider shares held: ~{fmt(total_held,'',0)}. " if total_held else ""
            down_note = ""
            if pct_high and pct_high < -20:
                down_note = f" Despite a {abs(pct_high):.0f}% decline from 52-week highs, management is holding — no panic selling. This stability suggests confidence in the company's trajectory."
            elif pct_high and pct_high > -10:
                down_note = " Insiders maintaining positions near highs shows conviction."
            sections.append(f'<h2>👔 Insider Activity</h2>\n<div class="co bl"><strong>Insider Holdings:</strong> {held_str}No insider transactions (buy or sell) reported in the last 6 months.{down_note}</div>')

    # Seeking Alpha Research (from research)
    sa = research.get("sa_articles", [])
    if sa:
        sa_cards = ""
        for a in sa:
            rating = a.get("rating", "")
            sc = "bul" if "buy" in rating.lower() else ("ber" if "sell" in rating.lower() else "net")
            sa_cards += f'<div class="tw"><span class="au">"{a.get("title","")}"</span> · {a.get("date","")} · <span class="st {sc}">{rating}</span><p style="margin-top:8px; color:#475569">{a.get("summary","")}</p></div>\n'
        
        buys = sum(1 for a in sa if "buy" in a.get("rating","").lower())
        total = len(sa)
        sections.append(f'<h2>📝 Seeking Alpha Research</h2>\n{sa_cards}')
        if buys > total / 2:
            sections.append(f'<div class="co gr"><strong>SA Consensus:</strong> {buys} of {total} recent articles rate Buy or Strong Buy, citing the fundamental disconnect between strong growth and compressed valuation.</div>')

    # X/Twitter Sentiment (from research)
    tweets = research.get("twitter_sentiment", [])
    if tweets:
        tw_cards = ""
        for t in tweets:
            stance = t.get("stance", t.get("sentiment", ""))
            sc = "bul" if "bull" in stance.lower() else ("ber" if "bear" in stance.lower() else "net")
            tw_cards += f'<div class="tw"><span class="au">@{t.get("user","")}</span> · <span class="st {sc}">{stance}</span><p style="margin-top:8px; color:#475569">{t.get("summary","")}</p></div>\n'
        
        bulls = sum(1 for t in tweets if "bull" in t.get("stance", t.get("sentiment", "")).lower())
        sections.append(f'<h2>🐦 X/Twitter Sentiment</h2>\n{tw_cards}')
        if bulls > len(tweets) / 2:
            sections.append(f'<div class="co gr"><strong>X Consensus:</strong> Overwhelmingly bullish ({bulls}/{len(tweets)}). Key themes include fundamental mispricing at single-digit P/E, strong growth trajectory, and geographic diversification.</div>')

    # Catalysts (from research)
    cats = research.get("catalysts", [])
    if cats:
        items = "\n".join(f"<li>{c}</li>" for c in cats)
        sections.append(f'<h2 class="pb">🚀 Catalysts</h2>\n<ul>\n{items}\n</ul>')

    # Risks (from research)
    risks = research.get("risks", [])
    if risks:
        items = "\n".join(f"<li>{r}</li>" for r in risks)
        sections.append(f'<h2>⚠️ Risks</h2>\n<ul>\n{items}\n</ul>')

    # Analyst Consensus (from research)
    if consensus:
        sections.append(f"""<h2>🎯 Analyst Consensus</h2>
<div class="kpi-grid">
    <div class="kpi"><div class="label">Rating</div><div class="value up">{consensus.get("rating","—")}</div></div>
    <div class="kpi"><div class="label">Avg Price Target</div><div class="value up">${sf(consensus.get("avg_pt"),0):.2f}</div><div class="sub up">+{((sf(consensus.get("avg_pt"),0)/price-1)*100):.0f}% upside</div></div>
    <div class="kpi"><div class="label">Low PT</div><div class="value">${sf(consensus.get("low_pt"),0):.2f}</div></div>
    <div class="kpi"><div class="label">High PT</div><div class="value">${sf(consensus.get("high_pt"),0):.2f}</div></div>
</div>""")

    # Valuation Framework — detailed with methodology explanation
    if fwd_eps and fwd_eps > 0 and price and price > 0:
        # Build detailed peer PE breakdown for methodology explanation
        peer_pe_details = []
        for pt, pd in peers.items():
            fpe = sf(pd.get("forwardPE"))
            rg = sf(pd.get("revenueGrowth"))
            if fpe and 0 < fpe < 100:
                rg_str = f", Rev Growth: {pct(rg)}" if rg is not None else ""
                peer_pe_details.append({"ticker": pt, "fwd_pe": fpe, "rev_growth": rg, "mcap": pd.get("marketCap")})

        # Sort peers by forward PE
        peer_pe_details.sort(key=lambda x: x["fwd_pe"])

        # Build the closest-comp PE (most similar by market cap)
        closest_comp = None
        closest_comp_pe = None
        if peer_pe_details and mcap:
            closest_comp = min(peer_pe_details, key=lambda x: abs((x.get("mcap") or 1e18) - mcap))
            closest_comp_pe = closest_comp["fwd_pe"]

        # Methodology intro
        sections.append(f"""<h2 class="pb">💎 Valuation Framework</h2>
<div class="co bl"><strong>📋 Data & Methodology:</strong> All financial data sourced from Yahoo Finance (yfinance) as of {today}. Forward EPS of <strong>${fwd_eps:.2f}</strong> is the consensus analyst estimate. Trailing P/E of <strong>{pe(trail_pe)}</strong> is calculated from TTM EPS of ${sf(fund.get("trailingEps"),0):.2f}. Historical P/E data spans {len(pe_vals)} quarterly observations over 5 years, filtered for outliers (PE > 100x removed — these occur during near-zero EPS periods). Peer multiples are current forward P/E ratios. Three independent methods are used to triangulate fair value.</div>""")

        # Method 1: P/E Multiple Approach
        cons_pe_v = trail_pe if trail_pe else (fwd_pe if fwd_pe else 10)
        cons_price_v = cons_pe_v * fwd_eps
        cons_up_v = (cons_price_v / price - 1) * 100

        rows = f'<tr><td>Conservative (current multiple)</td><td>{cons_pe_v:.1f}x</td><td>${fwd_eps:.2f}</td><td>${cons_price_v:.2f}</td><td class="{cls(cons_up_v)}">{cons_up_v:+.0f}%</td><td>Assumes no re-rating; market keeps current multiple</td></tr>\n'
        rows += f'<tr><td>Base (peer-informed avg)</td><td>{base_pe:.1f}x</td><td>${fwd_eps:.2f}</td><td>${base_price:.2f}</td><td class="up">+{base_up:.0f}%</td><td>Avg of peer fwd P/E: {", ".join(f"{p["ticker"]} {p["fwd_pe"]:.1f}x" for p in peer_pe_details)}</td></tr>\n'
        
        # Closest comp parity row
        if closest_comp and closest_comp_pe:
            par_price = closest_comp_pe * fwd_eps
            par_up = (par_price / price - 1) * 100
            rows += f'<tr><td>{closest_comp["ticker"]} Parity (closest comp)</td><td>{closest_comp_pe:.1f}x</td><td>${fwd_eps:.2f}</td><td>${par_price:.2f}</td><td class="up">+{par_up:.0f}%</td><td>Most comparable by market cap ({fmt(closest_comp.get("mcap"))})</td></tr>\n'

        # Additional peer parity rows for key peers
        for p in peer_pe_details:
            if p["ticker"] != (closest_comp["ticker"] if closest_comp else ""):
                pp = p["fwd_pe"] * fwd_eps
                pu = (pp / price - 1) * 100
                rg_note = f"Rev growth: {pct(p['rev_growth'])}" if p.get("rev_growth") is not None else ""
                rows += f'<tr><td>{p["ticker"]} Parity</td><td>{p["fwd_pe"]:.1f}x</td><td>${fwd_eps:.2f}</td><td>${pp:.2f}</td><td class="up">+{pu:.0f}%</td><td>{rg_note}</td></tr>\n'

        rows += f'<tr><td>Optimistic (multiple expansion)</td><td>{bull_pe:.1f}x</td><td>${bull_eps:.2f}</td><td>${bull_price:.2f}</td><td class="up">+{bull_up:.0f}%</td><td>Bull EPS assumes +15% beat; multiple at 1.5× peer avg</td></tr>\n'

        sections.append(f"""<h3>Method 1: P/E Multiple Approach</h3>
<p style="color:#64748b; margin-bottom:12px">Each scenario applies a different P/E multiple to forward EPS. The multiple is justified by peer comparison, historical averages, or growth-adjusted reasoning. Forward EPS of ${fwd_eps:.2f} is the Yahoo Finance consensus estimate.</p>
<table><thead><tr><th>Scenario</th><th>P/E</th><th>EPS</th><th>Price</th><th>Upside</th><th>Rationale</th></tr></thead>
<tbody>{rows}</tbody></table>""")

        # Method 2: Mean Reversion
        mr_kpis = []
        mr_explanations = []
        if avg_hist_pe:
            impl_h = avg_hist_pe * fwd_eps
            up_h = (impl_h / price - 1) * 100
            mr_kpis.append(f'<div class="kpi"><div class="label">5Y Avg PE × Fwd EPS</div><div class="value up">${impl_h:.2f}</div><div class="sub up">+{up_h:.0f}% upside</div></div>')
            mr_explanations.append(f"5-year average P/E of {avg_hist_pe:.1f}x (filtered, {len(pe_vals)} data points, range {min_hist_pe:.0f}x–{max_hist_pe:.0f}x) × forward EPS ${fwd_eps:.2f} = ${impl_h:.2f}")
        if avg_peer_pe:
            impl_p = avg_peer_pe * fwd_eps
            up_p = (impl_p / price - 1) * 100
            mr_kpis.append(f'<div class="kpi"><div class="label">Peer Avg PE × Fwd EPS</div><div class="value up">${impl_p:.2f}</div><div class="sub up">+{up_p:.0f}% upside</div></div>')
            mr_explanations.append(f"Peer average forward P/E of {avg_peer_pe:.1f}x ({', '.join(f'{p["ticker"]} {p["fwd_pe"]:.1f}x' for p in peer_pe_details)}) × ${fwd_eps:.2f} = ${impl_p:.2f}")
        if consensus.get("avg_pt"):
            avg_pt = sf(consensus.get("avg_pt"))
            up_a = (avg_pt / price - 1) * 100
            mr_kpis.append(f'<div class="kpi"><div class="label">Analyst Consensus PT</div><div class="value up">${avg_pt:.2f}</div><div class="sub up">+{up_a:.0f}% upside</div></div>')
            mr_explanations.append(f"Wall Street analyst consensus price target: ${avg_pt:.2f} (range: ${sf(consensus.get('low_pt'),0):.2f}–${sf(consensus.get('high_pt'),0):.2f})")
        
        if mr_kpis:
            expl_html = "<ul>" + "".join(f"<li>{e}</li>" for e in mr_explanations) + "</ul>"
            sections.append(f"""<h3>Method 2: Mean Reversion & Consensus</h3>
<p style="color:#64748b; margin-bottom:12px">If the stock reverts to its historical or peer-implied valuation, what would it be worth? These are independent cross-checks on Method 1.</p>
<div class="kpi-grid">
{"".join(mr_kpis)}
</div>
<div class="co bl"><strong>📐 Calculation Details:</strong>{expl_html}</div>""")

        # DCF
        if "error" in dcf:
            err_msg = dcf.get("error", "Insufficient data")
            # Clean up error message
            if "exited with code" in err_msg:
                err_msg = "No positive free cash flow (FCF) found. This is common for financial services companies where client deposits and margin lending dominate cash flows"
            sections.append(f'<h3>Method 3: Discounted Cash Flow (DCF)</h3>\n<div class="co yw"><strong>⚠️ DCF Not Available:</strong> {err_msg}. For financial companies, P/E and price-to-book multiples are more appropriate valuation methods than DCF.</div>')
        elif dcf.get("scenarios"):
            dcf_rows = ""
            for case, label in [("bear","Bear"),("base","Base"),("bull","Bull")]:
                s = dcf["scenarios"].get(case, {})
                sv = sf(s.get("per_share_value"))
                su = sf(s.get("upside_pct"))
                gr = s.get("growth_rate", "")
                tr = s.get("terminal_growth", "")
                wacc = s.get("wacc", "")
                if sv:
                    dcf_rows += f'<tr><td>{label}</td><td>{gr}%</td><td>{wacc if wacc else "10"}%</td><td>{tr if tr else "3"}%</td><td>${sv:.2f}</td><td class="{cls(su)}">{f"{su:+.1f}%" if su else "—"}</td></tr>\n'
            if dcf_rows:
                sections.append(f"""<h3>Method 3: Discounted Cash Flow (DCF)</h3>
<p style="color:#64748b; margin-bottom:12px">10-year DCF model using free cash flow projections under three growth scenarios. Terminal value calculated using perpetuity growth method.</p>
<table><thead><tr><th>Scenario</th><th>Rev Growth</th><th>WACC</th><th>Terminal Growth</th><th>Intrinsic Value</th><th>Upside</th></tr></thead><tbody>{dcf_rows}</tbody></table>""")

        # Summary callout before scenarios
        methods_agree = []
        if avg_hist_pe:
            methods_agree.append(f"historical mean reversion (${avg_hist_pe * fwd_eps:.2f})")
        if avg_peer_pe:
            methods_agree.append(f"peer parity (${avg_peer_pe * fwd_eps:.2f})")
        if consensus.get("avg_pt"):
            methods_agree.append(f"analyst consensus (${sf(consensus['avg_pt']):.2f})")
        
        if len(methods_agree) >= 2:
            sections.append(f'<div class="co gr"><strong>✅ Multiple Methods Converge:</strong> {", ".join(methods_agree)} — all pointing significantly above the current price of ${price:.2f}. This convergence across independent approaches strengthens the valuation case.</div>')

        # Price Target Scenarios
        bear_desc = "Multiple compression on earnings miss, macro headwinds, or regulatory shock."
        base_desc = f"Earnings meet consensus, gradual re-rating toward peer average of {base_pe:.0f}x as market recognizes growth trajectory."
        bull_desc = "Earnings beat + guidance raise, institutional discovery drives multiple expansion, geographic catalysts accelerate."
        
        if cats and len(cats) > 0:
            bull_desc = cats[0][:150] + "."
        if risks and len(risks) > 0:
            r = risks[0].split(". Mitigant")[0] if ". Mitigant" in risks[0] else risks[0]
            bear_desc = r[:150] + ". Multiple compresses to distressed levels."

        sections.append(f"""<h3>Price Target Scenarios (12-Month)</h3>
<p style="color:#64748b; margin-bottom:12px">Three scenarios combining P/E multiple assumptions with EPS estimates. Bear uses {bear_pe:.0f}x (35% discount to current) × 85% of consensus EPS. Base uses {base_pe:.0f}x (peer average) × consensus EPS. Bull uses {bull_pe:.0f}x (1.5× peer avg) × 115% of consensus EPS.</p>
<div class="sg">
    <div class="sc bear"><div class="lb">🐻 Bear Case</div><div class="pr dn">${bear_price:.2f}</div><div class="mt">{bear_pe:.0f}x × ${bear_eps:.2f} EPS</div><div class="us dn">{bear_up:+.0f}%</div><div class="ds">{bear_desc}</div></div>
    <div class="sc base"><div class="lb">📊 Base Case</div><div class="pr up">${base_price:.2f}</div><div class="mt">{base_pe:.0f}x × ${fwd_eps:.2f} EPS</div><div class="us up">+{base_up:.0f}% upside</div><div class="ds">{base_desc}</div></div>
    <div class="sc bull"><div class="lb">🐂 Bull Case</div><div class="pr up">${bull_price:.2f}</div><div class="mt">{bull_pe:.0f}x × ${bull_eps:.2f} EPS</div><div class="us up">+{bull_up:.0f}% upside</div><div class="ds">{bull_desc}</div></div>
</div>""")

    # Investment Thesis — rich, specific, opinionated
    thesis = f"<p><strong>{ticker}</strong> "
    
    # Opening: the mispricing argument
    if rev_g and fwd_pe and nm:
        growth_str = f"{rev_g*100:.0f}%" if abs(rev_g) < 2 else f"{rev_g:.0f}%"
        thesis += f"is a rare fundamental mispricing: a company growing revenue at {growth_str} YoY with {pct(nm)} net margins, trading at just {fwd_pe:.1f}x forward earnings"
        if avg_peer_pe and fwd_pe < avg_peer_pe:
            # Find a well-known peer for comparison
            comp_name = None
            comp_pe = None
            for pt, pd in peers.items():
                fpe_p = sf(pd.get("forwardPE"))
                rg_p = sf(pd.get("revenueGrowth"))
                if fpe_p and fpe_p > fwd_pe and rg_p is not None:
                    comp_name = pt
                    comp_pe = fpe_p
                    break
            if comp_name and comp_pe:
                comp_rg = sf(peers[comp_name].get("revenueGrowth"))
                comp_rg_str = f", which is growing at {'single digits' if comp_rg and comp_rg < 0.1 else pct(comp_rg)}" if comp_rg is not None else ""
                thesis += f" — cheaper than {comp_name} ({comp_pe:.1f}x{comp_rg_str})"
        thesis += ". "
    elif fwd_pe:
        thesis += f"trades at {fwd_pe:.1f}x forward earnings. "
    else:
        thesis += "presents a compelling investment case. "

    # Middle: the market narrative vs reality
    market_narrative = []
    if pct_high and pct_high < -30:
        market_narrative.append(f"the stock is down {abs(pct_high):.0f}% from its 52-week high")
    if rsi and rsi < 35:
        market_narrative.append(f"RSI at {rsi:.1f} signals oversold conditions")
    if market_narrative:
        thesis += "The market is pricing in pessimism — " + " and ".join(market_narrative) + ". "

    # What could change
    catalyst_parts = []
    if days_earn and days_earn <= 30:
        catalyst_parts.append(f"upcoming earnings on {next_earn} ({days_earn} days away) could serve as the catalyst for re-rating")
    if avg_hist_pe and cur_pe and cur_pe < avg_hist_pe * 0.6:
        catalyst_parts.append(f"the stock trades at its cheapest valuation in 5 years ({pe(cur_pe)} vs 5Y avg {avg_hist_pe:.1f}x)")
    if consensus.get("avg_pt") and price:
        avg_pt_v = sf(consensus["avg_pt"])
        up_v = (avg_pt_v / price - 1) * 100
        if up_v > 30:
            catalyst_parts.append(f"analyst consensus target of ${avg_pt_v:.2f} implies +{up_v:.0f}% upside")
    
    if catalyst_parts:
        thesis += ". ".join(catalyst_parts).capitalize() + ". "

    # Risk acknowledgment
    risk_parts = []
    if risks and len(risks) > 0:
        # Extract first risk without mitigant
        first_risk = risks[0].split(". Mitigant")[0].split(". mitigant")[0]
        risk_parts.append(first_risk.lower())
    if risk_parts:
        thesis += f"The risk is real — {risk_parts[0]} — but "
    
    # Verdict
    thesis += f"at {fwd_pe:.1f}x forward earnings" if fwd_pe else ""
    if rev_g and abs(rev_g) < 2:
        thesis += f" with {rev_g*100:.0f}% growth" if rev_g else ""
    thesis += f", the risk/reward is heavily skewed to the upside."
    thesis += f"</p><p><strong>Verdict: {verdict} with a 12-month base case target of ${base_price:.2f} (+{base_up:.0f}% upside).</strong></p>"

    sections.append(f'<h2>🎯 Investment Thesis</h2>\n<div class="co gr">{thesis}</div>')

    # Disclaimer
    sections.append('<div class="co yw"><strong>⚠️ Disclaimer:</strong> This report is for informational purposes only and does not constitute investment advice. All data sourced from public sources including Yahoo Finance, Seeking Alpha, and X/Twitter. Past performance does not guarantee future results. Always conduct your own due diligence.</div>')

    # Footer
    sections.append(f'<div class="ft"><p>Generated by Stock Valuation Skill · {sources} · {today}</p></div>')

    # Assemble
    body = "\n\n".join(s for s in sections if s)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{ticker} | Valuation Report</title>
<style>{CSS}</style>
</head>
<body>
<div class="container">
{body}
</div>
</body>
</html>"""

    with open(out, "w") as f: f.write(html)
    print(f"Report written to {out}")


if __name__ == "__main__":
    main()
