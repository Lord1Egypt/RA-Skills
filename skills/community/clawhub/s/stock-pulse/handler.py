#!/usr/bin/env python3
"""
stock-pulse: A股智能决策仪表盘
- 实时分析：买/卖/观望 + 精确点位
- 单日走势：指定日期的 K 线图（ASCII）
- 月/年预测：基于历史波动率 + AI 的价格区间预测
- 综合建议：该不该买
"""

import sys
import os
import json
import argparse
import io
import contextlib
from datetime import datetime, timedelta
from pathlib import Path

# ─── LLM ──────────────────────────────────────────────────────────────────────
# 读取调用方（OpenClaw）注入的中性环境变量，不绑定任何具体模型或平台

def build_llm_client():
    api_key = os.getenv("LLM_API_KEY")
    base_url = os.getenv("LLM_BASE_URL", "").rstrip("/")
    model    = os.getenv("LLM_MODEL")

    if not api_key:
        raise RuntimeError("请设置 LLM_API_KEY（OpenClaw 运行时自动注入）")
    if not base_url:
        raise RuntimeError("请设置 LLM_BASE_URL（OpenClaw 运行时自动注入）")
    if not model:
        raise RuntimeError("请设置 LLM_MODEL（OpenClaw 运行时自动注入）")

    return {"api_key": api_key, "base_url": base_url, "model": model}, model


def llm_chat(client, model: str, prompt: str, max_tokens: int = 800) -> str:
    import requests as _req
    url = client["base_url"].rstrip("/") + "/chat/completions"
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": max_tokens,
    }
    headers = {
        "Authorization": f"Bearer {client['api_key']}",
        "Content-Type": "application/json",
    }
    resp = _req.post(url, json=payload, headers=headers, timeout=60)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()


# ─── 数据获取 ─────────────────────────────────────────────────────────────────

def _bs_code(code: str) -> str:
    prefix = "sh" if code.startswith("6") else "sz"
    return f"{prefix}.{code}"


def fetch_history(code: str, days: int = 250) -> "pd.DataFrame":
    """获取日K历史数据（最多 days 天）"""
    import baostock as bs
    import pandas as pd

    start = (datetime.now() - timedelta(days=days + 50)).strftime("%Y-%m-%d")
    with contextlib.redirect_stdout(io.StringIO()):
        bs.login()
    rs = bs.query_history_k_data_plus(
        _bs_code(code),
        "date,open,high,low,close,volume,pctChg",
        start_date=start,
        frequency="d",
        adjustflag="3",
    )
    rows = []
    while rs.error_code == "0" and rs.next():
        rows.append(rs.get_row_data())
    with contextlib.redirect_stdout(io.StringIO()):
        bs.logout()

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows, columns=["date", "open", "high", "low", "close", "volume", "pctChg"])
    for col in ["open", "high", "low", "close", "volume", "pctChg"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["date"] = pd.to_datetime(df["date"])
    return df.dropna(subset=["close"]).tail(days)


def fetch_intraday(code: str, date: str) -> "pd.DataFrame":
    """获取指定日期的分钟K数据"""
    import baostock as bs
    import pandas as pd

    with contextlib.redirect_stdout(io.StringIO()):
        bs.login()
    rs = bs.query_history_k_data_plus(
        _bs_code(code),
        "time,open,high,low,close,volume",
        start_date=date,
        end_date=date,
        frequency="5",
        adjustflag="3",
    )
    rows = []
    while rs.error_code == "0" and rs.next():
        rows.append(rs.get_row_data())
    with contextlib.redirect_stdout(io.StringIO()):
        bs.logout()

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows, columns=["time", "open", "high", "low", "close", "volume"])
    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.dropna(subset=["close"])


def get_stock_name(code: str) -> str:
    import baostock as bs
    with contextlib.redirect_stdout(io.StringIO()):
        bs.login()
    rs = bs.query_stock_basic(code=_bs_code(code))
    name = code
    if rs.error_code == "0" and rs.next():
        name = rs.get_row_data()[1]
    with contextlib.redirect_stdout(io.StringIO()):
        bs.logout()
    return name


# ─── ASCII 图表 ───────────────────────────────────────────────────────────────

def ascii_line_chart(values: list, width: int = 50, height: int = 10, label: str = "") -> str:
    """把价格序列渲染成 ASCII 折线图"""
    if not values:
        return ""
    vmin, vmax = min(values), max(values)
    if vmax == vmin:
        vmax = vmin + 0.01

    grid = [[" "] * width for _ in range(height)]
    n = len(values)

    for xi in range(width):
        idx = int(xi / (width - 1) * (n - 1))
        yi_float = (values[idx] - vmin) / (vmax - vmin) * (height - 1)
        yi = height - 1 - int(round(yi_float))
        yi = max(0, min(height - 1, yi))
        grid[yi][xi] = "●"

    # 连接相邻点
    for xi in range(width - 1):
        idx0 = int(xi / (width - 1) * (n - 1))
        idx1 = int((xi + 1) / (width - 1) * (n - 1))
        y0 = height - 1 - int(round((values[idx0] - vmin) / (vmax - vmin) * (height - 1)))
        y1 = height - 1 - int(round((values[idx1] - vmin) / (vmax - vmin) * (height - 1)))
        lo, hi = min(y0, y1), max(y0, y1)
        for y in range(lo, hi + 1):
            if grid[y][xi] == " ":
                grid[y][xi] = "│" if lo < hi else "─"

    lines = []
    for i, row in enumerate(grid):
        price = vmax - i / (height - 1) * (vmax - vmin)
        lines.append(f"  {price:>8.2f} │{''.join(row)}")

    # X 轴
    lines.append(f"  {'':>8} └{'─' * width}")
    if label:
        lines.append(f"           {label}")
    return "\n".join(lines)


def ascii_candle_chart(df: "pd.DataFrame", width: int = 40) -> str:
    """简易 ASCII K 线图（日K）"""
    import pandas as pd
    n = min(len(df), width)
    df = df.tail(n)

    all_prices = list(df["high"]) + list(df["low"])
    vmin, vmax = min(all_prices), max(all_prices)
    height = 12

    if vmax == vmin:
        return "（价格区间过小，无法绘制）"

    grid = [[" "] * n for _ in range(height)]

    for xi, (_, row) in enumerate(df.iterrows()):
        hi_y = height - 1 - int((row["high"] - vmin) / (vmax - vmin) * (height - 1))
        lo_y = height - 1 - int((row["low"] - vmin) / (vmax - vmin) * (height - 1))
        op_y = height - 1 - int((row["open"] - vmin) / (vmax - vmin) * (height - 1))
        cl_y = height - 1 - int((row["close"] - vmin) / (vmax - vmin) * (height - 1))

        hi_y = max(0, min(height - 1, hi_y))
        lo_y = max(0, min(height - 1, lo_y))
        op_y = max(0, min(height - 1, op_y))
        cl_y = max(0, min(height - 1, cl_y))

        # 上下影线
        for y in range(hi_y, lo_y + 1):
            grid[y][xi] = "│"
        # 实体（涨=▲ 跌=▼）
        body_top = min(op_y, cl_y)
        body_bot = max(op_y, cl_y)
        char = "▲" if row["close"] >= row["open"] else "▼"
        for y in range(body_top, body_bot + 1):
            grid[y][xi] = char

    lines = []
    for i, row in enumerate(grid):
        price = vmax - i / (height - 1) * (vmax - vmin)
        lines.append(f"  {price:>8.2f} │{''.join(row)}")

    # X 轴日期
    dates = [str(d)[:10] for d in df["date"]]
    start_d, end_d = dates[0] if dates else "", dates[-1] if dates else ""
    lines.append(f"  {'':>8} └{'─' * n}")
    lines.append(f"           {start_d} {'─' * max(0, n - 22)} {end_d}")
    lines.append(f"\n  ▲=涨  ▼=跌  │=影线")
    return "\n".join(lines)


# ─── 功能模块 ─────────────────────────────────────────────────────────────────

def cmd_today(codes: list, client, model: str):
    """今日决策仪表盘"""
    import time
    results = []
    for i, code in enumerate(codes):
        if i > 0:
            time.sleep(1)
        print(f"  分析 {code}...", end="", flush=True)
        df = fetch_history(code, 60)
        if df.empty:
            print(" ❌ 无数据")
            continue
        name = get_stock_name(code)
        data = _build_data(code, name, df)
        analysis = _ai_analyze(data, client, model)
        results.append({"data": data, "analysis": analysis})
        print(f" {_signal_emoji(analysis.get('signal', '?'))}")

    print()
    print(f"📊 {datetime.now().strftime('%Y-%m-%d')} 决策仪表盘\n")
    for r in results:
        _print_stock_card(r["data"], r["analysis"])
    print(f"---\n生成时间: {datetime.now().strftime('%H:%M')} | 数据: baostock | 模型: {model}")


def cmd_day(code: str, date: str, client, model: str):
    """指定日期走势图"""
    print(f"  获取 {code} {date} 走势...", end="", flush=True)
    df_intra = fetch_intraday(code, date)
    name = get_stock_name(code)

    if df_intra.empty:
        # 没有分钟数据则用日K
        df = fetch_history(code, 60)
        if df.empty:
            print(" ❌ 无数据")
            return
        row = df[df["date"].dt.strftime("%Y-%m-%d") == date]
        if row.empty:
            print(f" ❌ {date} 无交易数据（非交易日？）")
            return
        r = row.iloc[0]
        print(" 完成\n")
        print(f"📅 {name}({code})  {date} 日K\n")
        print(f"  开盘: {r['open']:.2f}  收盘: {r['close']:.2f}  "
              f"最高: {r['high']:.2f}  最低: {r['low']:.2f}")
        chg = r['pctChg']
        print(f"  涨跌: {'▲' if chg >= 0 else '▼'} {abs(chg):.2f}%  "
              f"成交量: {r['volume'] / 1e4:.1f}万手\n")
        return

    print(" 完成\n")
    closes = list(df_intra["close"])
    open_price = float(df_intra["open"].iloc[0])
    close_price = float(df_intra["close"].iloc[-1])
    high_price = float(df_intra["high"].max())
    low_price = float(df_intra["low"].min())
    chg_pct = (close_price - open_price) / open_price * 100

    print(f"📅 {name}({code})  {date} 分时走势（5分钟K）\n")
    print(f"  开盘 {open_price:.2f}  收盘 {close_price:.2f}  "
          f"最高 {high_price:.2f}  最低 {low_price:.2f}")
    print(f"  全天涨跌: {'▲' if chg_pct >= 0 else '▼'} {abs(chg_pct):.2f}%\n")

    # ASCII 走势图
    times = [r["time"][-6:-2] if len(r["time"]) >= 6 else "" for _, r in df_intra.iterrows()]
    label = f"{times[0] if times else ''} {'─'*30} {times[-1] if times else ''}"
    print(ascii_line_chart(closes, width=50, height=10, label=label))

    # AI 点评
    print("\n  🤖 AI 走势点评")
    prompt = f"""{name}({code}) {date} 走势数据:
开盘:{open_price} 收盘:{close_price} 最高:{high_price} 最低:{low_price} 涨跌:{chg_pct:.2f}%
分时收盘序列(5min): {closes[:24]}

用2-3句话点评这天的走势特点（资金流向、上下影线含义、尾盘异动等），给出明日开盘预期。不超过100字。"""
    try:
        comment = llm_chat(client, model, prompt, max_tokens=150)
        for line in comment.split("\n"):
            if line.strip():
                print(f"  {line.strip()}")
    except Exception:
        pass


def cmd_predict(code: str, horizon: str, client, model: str):
    """月/年价格预测"""
    import math
    horizon_days = 30 if horizon == "month" else 252
    horizon_label = "1个月" if horizon == "month" else "1年"

    print(f"  获取 {code} 历史数据...", end="", flush=True)
    df = fetch_history(code, 250)
    if df.empty or len(df) < 20:
        print(" ❌ 数据不足")
        return
    name = get_stock_name(code)
    print(" 完成\n")

    close = float(df["close"].iloc[-1])

    # ── 统计预测（对数正态随机游走）──
    returns = df["close"].pct_change().dropna()
    mu_daily = float(returns.mean())
    sigma_daily = float(returns.std())

    # 年化
    mu_annual = mu_daily * 252
    sigma_annual = sigma_daily * math.sqrt(252)

    # 预测期漂移
    mu_period = mu_daily * horizon_days
    sigma_period = sigma_daily * math.sqrt(horizon_days)

    # 蒙特卡洛 2000 次模拟
    import random
    random.seed(42)
    simulated_finals = []
    for _ in range(2000):
        price = close
        for _ in range(horizon_days):
            price *= math.exp(random.gauss(mu_daily - 0.5 * sigma_daily**2, sigma_daily))
        simulated_finals.append(price)
    simulated_finals.sort()

    p10 = simulated_finals[int(0.10 * len(simulated_finals))]
    p25 = simulated_finals[int(0.25 * len(simulated_finals))]
    p50 = simulated_finals[int(0.50 * len(simulated_finals))]
    p75 = simulated_finals[int(0.75 * len(simulated_finals))]
    p90 = simulated_finals[int(0.90 * len(simulated_finals))]

    bull = round(p75, 2)
    base = round(p50, 2)
    bear = round(p25, 2)
    bull_pct = (bull - close) / close * 100
    base_pct = (base - close) / close * 100
    bear_pct = (bear - close) / close * 100

    print(f"🔮 {name}({code})  {horizon_label}价格预测\n")
    print(f"  当前价格: {close:.2f} 元")
    print(f"  历史年化收益: {mu_annual*100:+.1f}%")
    print(f"  历史年化波动: {sigma_annual*100:.1f}%\n")
    print(f"  蒙特卡洛模拟 2000 次（概率分布）:\n")
    print(f"  {'悲观(10%)':>10}  {'保守(25%)':>10}  {'中性(50%)':>10}  {'乐观(75%)':>10}  {'极乐(90%)':>10}")
    print(f"  {p10:>10.2f}  {p25:>10.2f}  {p50:>10.2f}  {p75:>10.2f}  {p90:>10.2f}")
    print(f"  {(p10-close)/close*100:>+9.1f}%  {(p25-close)/close*100:>+9.1f}%  "
          f"{(p50-close)/close*100:>+9.1f}%  {(p75-close)/close*100:>+9.1f}%  "
          f"{(p90-close)/close*100:>+9.1f}%\n")

    # 价格路径图（中位数模拟）
    path = [close]
    random.seed(42)
    for _ in range(horizon_days):
        path.append(path[-1] * math.exp(random.gauss(mu_daily - 0.5 * sigma_daily**2, sigma_daily)))

    steps = min(50, len(path))
    sampled = [path[int(i / (steps - 1) * (len(path) - 1))] for i in range(steps)]
    end_label = (datetime.now() + timedelta(days=horizon_days)).strftime("%Y-%m-%d")
    print(ascii_line_chart(sampled, width=50, height=8,
                           label=f"今日 → {end_label}（中性情景）"))

    # AI 定性分析
    print(f"\n  🤖 AI 综合判断\n")
    data = _build_data(code, name, df)
    prompt = f"""你是一位专业 A 股分析师，请对 {name}({code}) 做{horizon_label}预测分析。

当前数据:
- 最新收盘: {close:.2f} 元
- MA5:{data['ma5']} MA10:{data['ma10']} MA20:{data['ma20']}
- 20日波动率: {data['volatility']:.2f}
- 历史年化收益: {mu_annual*100:+.1f}%  年化波动: {sigma_annual*100:.1f}%

统计模型预测（蒙特卡洛）:
- 悲观情景(25%概率): {bear:.2f} 元 ({bear_pct:+.1f}%)
- 中性情景(50%): {base:.2f} 元 ({base_pct:+.1f}%)
- 乐观情景(75%): {bull:.2f} 元 ({bull_pct:+.1f}%)

请给出:
1. 三种情景的触发条件（各20字内）
2. 关键支撑位和阻力位
3. 该不该在当前价格买入（明确说是/否，并说明理由）
4. 如果买，建议仓位比例（10%-100%）

回答控制在150字内，直接给结论。"""
    try:
        analysis = llm_chat(client, model, prompt, max_tokens=300)
        for line in analysis.split("\n"):
            if line.strip():
                print(f"  {line.strip()}")
    except Exception as e:
        print(f"  ⚠️  AI 分析失败: {e}")


def cmd_should_buy(code: str, client, model: str):
    """该不该买 — 综合月预测 + 年预测 + 当前技术面"""
    import math, random

    print(f"  获取数据...", end="", flush=True)
    df = fetch_history(code, 250)
    if df.empty:
        print(" ❌ 无数据")
        return
    name = get_stock_name(code)
    print(" 完成\n")

    close = float(df["close"].iloc[-1])
    returns = df["close"].pct_change().dropna()
    mu_d = float(returns.mean())
    sigma_d = float(returns.std())
    data = _build_data(code, name, df)

    # 快速计算月/年预期
    def mc_median(days):
        random.seed(42)
        sims = []
        for _ in range(1000):
            p = close
            for _ in range(days):
                p *= math.exp(random.gauss(mu_d - 0.5 * sigma_d**2, sigma_d))
            sims.append(p)
        sims.sort()
        return round(sims[500], 2)

    month_pred = mc_median(30)
    year_pred = mc_median(252)
    month_pct = (month_pred - close) / close * 100
    year_pct = (year_pred - close) / close * 100

    prompt = f"""你是一位专业 A 股基金经理，给出明确的买入建议。

股票: {name}({code})
当前价: {close:.2f}元  今日涨跌: {data['change_pct']:+.2f}%

技术面:
  MA5:{data['ma5']}  MA10:{data['ma10']}  MA20:{data['ma20']}
  偏离MA5: {data['deviation_ma5']:+.2f}%
  20日波动率: {data['volatility']:.2f}

预测:
  1个月中性预期: {month_pred:.2f}元 ({month_pct:+.1f}%)
  1年中性预期:   {year_pred:.2f}元 ({year_pct:+.1f}%)

请给出严格的买入评估，包含:
1. 结论: 【立刻买/等待回调买/观望/不买】（必须明确选一个）
2. 理由（3点，每点15字内）
3. 如果买: 建议买入价区间、仓位比例(10-100%)、止损价
4. 风险提示（1句话）

格式要直接、有用，不废话。"""

    print(f"🎯 {name}({code})  该不该买？\n")
    print(f"  当前价: {close:.2f}  1个月预期: {month_pred:.2f}({month_pct:+.1f}%)  "
          f"1年预期: {year_pred:.2f}({year_pct:+.1f}%)\n")

    try:
        result = llm_chat(client, model, prompt, max_tokens=400)
        for line in result.split("\n"):
            if line.strip():
                print(f"  {line.strip()}")
    except Exception as e:
        print(f"  ❌ AI 分析失败: {e}")


# ─── 辅助函数 ─────────────────────────────────────────────────────────────────

def _build_data(code: str, name: str, df: "pd.DataFrame") -> dict:
    close = float(df["close"].iloc[-1])
    ma5 = float(df["close"].tail(5).mean())
    ma10 = float(df["close"].tail(10).mean())
    ma20 = float(df["close"].tail(20).mean())
    std20 = float(df["close"].tail(20).std())
    dev = (close - ma5) / ma5 * 100
    chg = float(df["pctChg"].iloc[-1]) if "pctChg" in df.columns else 0.0
    return {
        "code": code, "name": name, "close": close,
        "change_pct": chg, "ma5": round(ma5, 2),
        "ma10": round(ma10, 2), "ma20": round(ma20, 2),
        "deviation_ma5": round(dev, 2), "volatility": round(std20, 2),
    }


def _ai_analyze(data: dict, client, model: str) -> dict:
    prompt = f"""你是 A 股交易分析师。给出操作建议。

{data['name']}({data['code']}) 当前:{data['close']} 涨跌:{data['change_pct']:+.2f}%
MA5:{data['ma5']} MA10:{data['ma10']} MA20:{data['ma20']} 偏离MA5:{data['deviation_ma5']:+.2f}%

铁律: 乖离率>5%严禁追高; MA5>MA10>MA20 才是多头排列

只返回 JSON:
{{"signal":"BUY|HOLD|SELL","reason":"一句话理由","entry":{data['close']},"stop_loss":{round(data['ma20']*0.97,2)},"target":{round(data['close']*1.06,2)},"checklist":["✅/⚠️/❌ 条件1","✅/⚠️/❌ 条件2","✅/⚠️/❌ 条件3"]}}"""
    try:
        raw = llm_chat(client, model, prompt, max_tokens=250)
        s = raw.find("{"); e = raw.rfind("}") + 1
        result = json.loads(raw[s:e])
        c = data["close"]
        if not result.get("entry"): result["entry"] = round(c * 0.99, 2)
        if not result.get("stop_loss"): result["stop_loss"] = round(data["ma20"] * 0.97, 2)
        if not result.get("target"): result["target"] = round(c * 1.06, 2)
        return result
    except Exception:
        dev = data["deviation_ma5"]
        signal = "HOLD" if abs(dev) < 1 else ("BUY" if data["ma5"] > data["ma10"] > data["ma20"] else "HOLD")
        return {"signal": signal, "reason": "规则分析", "entry": round(data["close"]*0.99,2),
                "stop_loss": round(data["ma20"]*0.97,2), "target": round(data["close"]*1.06,2),
                "checklist": [f"{'✅' if data['ma5']>data['ma10']>data['ma20'] else '❌'} 多头排列",
                               f"{'✅' if abs(dev)<5 else '⚠️'} 乖离({dev:+.1f}%)",
                               "⚠️ 请人工复核"]}


def _signal_emoji(signal: str) -> str:
    return {"BUY": "🟢 买入", "HOLD": "🟡 观望", "SELL": "🔴 卖出"}.get(signal, "❓")


def _print_stock_card(data: dict, analysis: dict):
    sig = _signal_emoji(analysis.get("signal", "HOLD"))
    print(f"{sig} | {data['name']} ({data['code']})")
    print(f"  📌 {analysis.get('reason', '-')}")
    print(f"  💰 买入 {analysis.get('entry','-')} | 止损 {analysis.get('stop_loss','-')} | 目标 {analysis.get('target','-')}")
    for item in analysis.get("checklist", []):
        print(f"  {item}")
    print()


def push_feishu(content: str):
    url = os.getenv("FEISHU_WEBHOOK_URL")
    if not url:
        print("⚠️  未设置 FEISHU_WEBHOOK_URL"); return
    import requests
    requests.post(url, json={"msg_type": "text", "content": {"text": content}})
    print("✅ 已推送到飞书")


# ─── CLI 入口 ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="stock-pulse: A股智能决策仪表盘",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例:
  python handler.py --stocks "600519,300750"          # 今日决策仪表盘
  python handler.py --day 600519 --date 2026-04-10    # 指定日期走势图
  python handler.py --predict 600519 --horizon month  # 1个月价格预测
  python handler.py --predict 600519 --horizon year   # 1年价格预测
  python handler.py --should-buy 600519               # 该不该买（综合判断）
        """,
    )

    sub = parser.add_mutually_exclusive_group(required=True)
    sub.add_argument("--stocks", help="今日决策仪表盘，代码逗号分隔")
    sub.add_argument("--day", metavar="CODE", help="指定日期走势图")
    sub.add_argument("--predict", metavar="CODE", help="月/年价格预测")
    sub.add_argument("--should-buy", metavar="CODE", help="该不该买（综合判断）")
    sub.add_argument("--watchlist", action="store_true", help="分析 STOCK_LIST 自选股")

    parser.add_argument("--date", help="日期 YYYY-MM-DD（配合 --day 使用）")
    parser.add_argument("--horizon", choices=["month", "year"], default="month",
                        help="预测周期（配合 --predict）")
    parser.add_argument("--push", choices=["feishu", "wechat"], help="推送渠道")
    parser.add_argument("--format", choices=["md", "json"], default="md")

    args = parser.parse_args()

    try:
        client, model = build_llm_client()
    except RuntimeError as e:
        print(f"❌ {e}"); sys.exit(1)

    if args.day:
        date = args.date or datetime.now().strftime("%Y-%m-%d")
        cmd_day(args.day, date, client, model)

    elif args.predict:
        cmd_predict(args.predict, args.horizon, client, model)

    elif args.should_buy:
        cmd_should_buy(args.should_buy, client, model)

    else:
        # 今日仪表盘
        if args.watchlist:
            sl = os.getenv("STOCK_LIST", "")
            if not sl:
                print("❌ 请设置 STOCK_LIST 环境变量"); sys.exit(1)
            codes = [s.strip() for s in sl.split(",") if s.strip()]
        else:
            codes = [s.strip() for s in args.stocks.split(",") if s.strip()]
        cmd_today(codes, client, model)


if __name__ == "__main__":
    main()
