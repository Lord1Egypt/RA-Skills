#!/usr/bin/env python3
"""
AI 投研团队 — 金融数据 MCP Server
基于 FastMCP + akshare(A股) + yfinance(美股) 提供结构化金融数据。
支持 OpenClaw / WorkBuddy 通过 MCP 协议调用。
"""

import json
import datetime
from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# 初始化 MCP Server
# ---------------------------------------------------------------------------
mcp = FastMCP(
    "stock-analyzer",
    version="1.0.0",
    description="AI 投研团队金融数据服务：提供股票行情、财务指标、K线数据和市场新闻",
)


# ---------------------------------------------------------------------------
# 工具函数：辅助
# ---------------------------------------------------------------------------
def _safe_float(val):
    """安全转换浮点数"""
    try:
        if val is None:
            return None
        return round(float(val), 4)
    except (ValueError, TypeError):
        return None


def _detect_market(symbol: str) -> str:
    """自动判断 A 股 / 美股"""
    if symbol.isdigit() or symbol.startswith(("sh", "sz", "bj", "SH", "SZ", "BJ")):
        return "cn"
    return "us"


# ---------------------------------------------------------------------------
# MCP Tool: 获取实时行情
# ---------------------------------------------------------------------------
@mcp.tool()
def get_stock_quote(symbol: str) -> str:
    """
    获取股票实时行情摘要。
    - A 股示例：600519（贵州茅台）、000001（平安银行）
    - 美股示例：AAPL、TSLA、NVDA
    返回：当前价格、涨跌幅、成交量、市值等核心指标。
    """
    market = _detect_market(symbol)

    if market == "cn":
        return _get_cn_quote(symbol)
    else:
        return _get_us_quote(symbol)


def _get_cn_quote(symbol: str) -> str:
    """A 股实时行情"""
    try:
        import akshare as ak

        df = ak.stock_zh_a_spot_em()
        code = symbol.lstrip("shszbjSHSZBJ")
        row = df[df["代码"] == code]
        if row.empty:
            return json.dumps({"error": f"未找到 A 股代码 {symbol}"}, ensure_ascii=False)

        r = row.iloc[0]
        result = {
            "market": "A股",
            "code": str(r.get("代码", "")),
            "name": str(r.get("名称", "")),
            "price": _safe_float(r.get("最新价")),
            "change_pct": _safe_float(r.get("涨跌幅")),
            "change_amount": _safe_float(r.get("涨跌额")),
            "volume": _safe_float(r.get("成交量")),
            "turnover": _safe_float(r.get("成交额")),
            "amplitude": _safe_float(r.get("振幅")),
            "high": _safe_float(r.get("最高")),
            "low": _safe_float(r.get("最低")),
            "open": _safe_float(r.get("今开")),
            "prev_close": _safe_float(r.get("昨收")),
            "turnover_rate": _safe_float(r.get("换手率")),
            "pe_ratio": _safe_float(r.get("市盈率-动态")),
            "pb_ratio": _safe_float(r.get("市净率")),
            "total_market_cap": _safe_float(r.get("总市值")),
            "circulating_market_cap": _safe_float(r.get("流通市值")),
            "timestamp": datetime.datetime.now().isoformat(),
        }
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": f"获取 A 股行情失败: {str(e)}"}, ensure_ascii=False)


def _get_us_quote(symbol: str) -> str:
    """美股实时行情"""
    try:
        import yfinance as yf

        ticker = yf.Ticker(symbol)
        info = ticker.info
        if not info or "regularMarketPrice" not in info:
            fast = ticker.fast_info
            result = {
                "market": "美股",
                "symbol": symbol.upper(),
                "price": _safe_float(getattr(fast, "last_price", None)),
                "prev_close": _safe_float(getattr(fast, "previous_close", None)),
                "market_cap": _safe_float(getattr(fast, "market_cap", None)),
                "timestamp": datetime.datetime.now().isoformat(),
            }
        else:
            result = {
                "market": "美股",
                "symbol": symbol.upper(),
                "name": info.get("shortName", ""),
                "price": _safe_float(info.get("regularMarketPrice")),
                "change_pct": _safe_float(info.get("regularMarketChangePercent")),
                "prev_close": _safe_float(info.get("regularMarketPreviousClose")),
                "market_cap": _safe_float(info.get("marketCap")),
                "pe_ratio": _safe_float(info.get("trailingPE")),
                "forward_pe": _safe_float(info.get("forwardPE")),
                "pb_ratio": _safe_float(info.get("priceToBook")),
                "dividend_yield": _safe_float(info.get("dividendYield")),
                "52w_high": _safe_float(info.get("fiftyTwoWeekHigh")),
                "52w_low": _safe_float(info.get("fiftyTwoWeekLow")),
                "avg_volume": _safe_float(info.get("averageVolume")),
                "sector": info.get("sector", ""),
                "industry": info.get("industry", ""),
                "timestamp": datetime.datetime.now().isoformat(),
            }
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": f"获取美股行情失败: {str(e)}"}, ensure_ascii=False)


# ---------------------------------------------------------------------------
# MCP Tool: 获取 K 线数据
# ---------------------------------------------------------------------------
@mcp.tool()
def get_stock_history(symbol: str, period: str = "3mo") -> str:
    """
    获取股票历史 K 线数据。
    - symbol: 股票代码（同 get_stock_quote）
    - period: 时间范围，可选 1mo/3mo/6mo/1y/2y（默认 3mo）
    返回：日期、开盘、收盘、最高、最低、成交量的时序数据（最近 60 条）。
    """
    market = _detect_market(symbol)

    if market == "cn":
        return _get_cn_history(symbol, period)
    else:
        return _get_us_history(symbol, period)


def _get_cn_history(symbol: str, period: str) -> str:
    """A 股历史 K 线"""
    try:
        import akshare as ak

        code = symbol.lstrip("shszbjSHSZBJ")
        period_map = {"1mo": 30, "3mo": 90, "6mo": 180, "1y": 365, "2y": 730}
        days = period_map.get(period, 90)
        end_date = datetime.date.today().strftime("%Y%m%d")
        start_date = (datetime.date.today() - datetime.timedelta(days=days)).strftime(
            "%Y%m%d"
        )

        df = ak.stock_zh_a_hist(
            symbol=code,
            period="daily",
            start_date=start_date,
            end_date=end_date,
            adjust="qfq",
        )
        if df.empty:
            return json.dumps({"error": f"未获取到 {symbol} 的历史数据"}, ensure_ascii=False)

        records = []
        for _, row in df.tail(60).iterrows():
            records.append(
                {
                    "date": str(row.get("日期", "")),
                    "open": _safe_float(row.get("开盘")),
                    "close": _safe_float(row.get("收盘")),
                    "high": _safe_float(row.get("最高")),
                    "low": _safe_float(row.get("最低")),
                    "volume": _safe_float(row.get("成交量")),
                    "turnover": _safe_float(row.get("成交额")),
                    "change_pct": _safe_float(row.get("涨跌幅")),
                }
            )

        return json.dumps(
            {"market": "A股", "symbol": code, "period": period, "data": records},
            ensure_ascii=False,
        )
    except Exception as e:
        return json.dumps(
            {"error": f"获取 A 股历史数据失败: {str(e)}"}, ensure_ascii=False
        )


def _get_us_history(symbol: str, period: str) -> str:
    """美股历史 K 线"""
    try:
        import yfinance as yf

        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period)
        if df.empty:
            return json.dumps({"error": f"未获取到 {symbol} 的历史数据"}, ensure_ascii=False)

        records = []
        for date, row in df.tail(60).iterrows():
            records.append(
                {
                    "date": date.strftime("%Y-%m-%d"),
                    "open": _safe_float(row.get("Open")),
                    "close": _safe_float(row.get("Close")),
                    "high": _safe_float(row.get("High")),
                    "low": _safe_float(row.get("Low")),
                    "volume": _safe_float(row.get("Volume")),
                }
            )

        return json.dumps(
            {"market": "美股", "symbol": symbol.upper(), "period": period, "data": records},
            ensure_ascii=False,
        )
    except Exception as e:
        return json.dumps(
            {"error": f"获取美股历史数据失败: {str(e)}"}, ensure_ascii=False
        )


# ---------------------------------------------------------------------------
# MCP Tool: 获取财务指标
# ---------------------------------------------------------------------------
@mcp.tool()
def get_financial_indicators(symbol: str) -> str:
    """
    获取股票核心财务指标。
    - A 股：营收、净利润、ROE、毛利率等（来自最新财报）
    - 美股：营收、净利润、EPS、ROE 等
    返回：结构化财务数据摘要。
    """
    market = _detect_market(symbol)

    if market == "cn":
        return _get_cn_financials(symbol)
    else:
        return _get_us_financials(symbol)


def _get_cn_financials(symbol: str) -> str:
    """A 股财务指标"""
    try:
        import akshare as ak

        code = symbol.lstrip("shszbjSHSZBJ")
        df = ak.stock_financial_abstract_ths(symbol=code, indicator="按报告期")
        if df is None or df.empty:
            return json.dumps(
                {"error": f"未获取到 {symbol} 的财务数据"}, ensure_ascii=False
            )

        latest = df.iloc[0]
        result = {
            "market": "A股",
            "symbol": code,
            "report_date": str(latest.get("报告期", "")),
            "revenue": str(latest.get("营业总收入", "")),
            "net_profit": str(latest.get("净利润", "")),
            "eps": str(latest.get("每股收益", "")),
            "roe": str(latest.get("净资产收益率", "")),
            "gross_margin": str(latest.get("销售毛利率", "")),
            "debt_ratio": str(latest.get("资产负债率", "")),
        }
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        return json.dumps(
            {"error": f"获取 A 股财务数据失败: {str(e)}"}, ensure_ascii=False
        )


def _get_us_financials(symbol: str) -> str:
    """美股财务指标"""
    try:
        import yfinance as yf

        ticker = yf.Ticker(symbol)
        info = ticker.info
        result = {
            "market": "美股",
            "symbol": symbol.upper(),
            "name": info.get("shortName", ""),
            "revenue": _safe_float(info.get("totalRevenue")),
            "net_income": _safe_float(info.get("netIncomeToCommon")),
            "eps_trailing": _safe_float(info.get("trailingEps")),
            "eps_forward": _safe_float(info.get("forwardEps")),
            "roe": _safe_float(info.get("returnOnEquity")),
            "profit_margin": _safe_float(info.get("profitMargins")),
            "operating_margin": _safe_float(info.get("operatingMargins")),
            "debt_to_equity": _safe_float(info.get("debtToEquity")),
            "free_cashflow": _safe_float(info.get("freeCashflow")),
            "revenue_growth": _safe_float(info.get("revenueGrowth")),
            "earnings_growth": _safe_float(info.get("earningsGrowth")),
        }
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        return json.dumps(
            {"error": f"获取美股财务数据失败: {str(e)}"}, ensure_ascii=False
        )


# ---------------------------------------------------------------------------
# MCP Tool: 技术指标计算
# ---------------------------------------------------------------------------
@mcp.tool()
def get_technical_indicators(symbol: str) -> str:
    """
    计算股票的常用技术指标。
    基于最近 120 个交易日的收盘价计算：
    - MA5/MA10/MA20/MA60 均线
    - RSI(14)
    - MACD(12,26,9)
    - 布林带(20,2)
    返回：结构化技术指标数据。
    """
    market = _detect_market(symbol)

    try:
        if market == "cn":
            import akshare as ak

            code = symbol.lstrip("shszbjSHSZBJ")
            end_date = datetime.date.today().strftime("%Y%m%d")
            start_date = (
                datetime.date.today() - datetime.timedelta(days=365)
            ).strftime("%Y%m%d")
            df = ak.stock_zh_a_hist(
                symbol=code,
                period="daily",
                start_date=start_date,
                end_date=end_date,
                adjust="qfq",
            )
            close_col = "收盘"
        else:
            import yfinance as yf

            ticker = yf.Ticker(symbol)
            df = ticker.history(period="1y")
            df = df.reset_index()
            close_col = "Close"

        if df is None or df.empty or len(df) < 26:
            return json.dumps(
                {"error": f"数据不足，无法计算技术指标"}, ensure_ascii=False
            )

        closes = df[close_col].astype(float).tolist()

        # MA
        def ma(data, n):
            if len(data) < n:
                return None
            return round(sum(data[-n:]) / n, 4)

        # RSI
        def rsi(data, n=14):
            if len(data) < n + 1:
                return None
            deltas = [data[i] - data[i - 1] for i in range(1, len(data))]
            recent = deltas[-n:]
            gains = [d for d in recent if d > 0]
            losses = [-d for d in recent if d < 0]
            avg_gain = sum(gains) / n if gains else 0
            avg_loss = sum(losses) / n if losses else 0.0001
            rs = avg_gain / avg_loss
            return round(100 - (100 / (1 + rs)), 2)

        # MACD
        def ema(data, n):
            if len(data) < n:
                return data[-1] if data else 0
            k = 2 / (n + 1)
            val = sum(data[:n]) / n
            for price in data[n:]:
                val = price * k + val * (1 - k)
            return val

        ema12 = ema(closes, 12)
        ema26 = ema(closes, 26)
        dif = round(ema12 - ema26, 4)

        # Bollinger Bands
        ma20 = ma(closes, 20)
        if ma20 and len(closes) >= 20:
            std20 = (
                sum((c - ma20) ** 2 for c in closes[-20:]) / 20
            ) ** 0.5
            bb_upper = round(ma20 + 2 * std20, 4)
            bb_lower = round(ma20 - 2 * std20, 4)
        else:
            bb_upper = bb_lower = None

        current_price = closes[-1]
        result = {
            "symbol": symbol,
            "current_price": round(current_price, 4),
            "ma5": ma(closes, 5),
            "ma10": ma(closes, 10),
            "ma20": ma20,
            "ma60": ma(closes, 60),
            "rsi_14": rsi(closes),
            "macd_dif": dif,
            "bollinger_upper": bb_upper,
            "bollinger_mid": ma20,
            "bollinger_lower": bb_lower,
            "ma_trend": "多头排列"
            if ma(closes, 5)
            and ma(closes, 10)
            and ma(closes, 20)
            and ma(closes, 5) > ma(closes, 10) > ma(closes, 20)
            else "空头排列"
            if ma(closes, 5)
            and ma(closes, 10)
            and ma(closes, 20)
            and ma(closes, 5) < ma(closes, 10) < ma(closes, 20)
            else "震荡整理",
            "rsi_signal": "超买"
            if rsi(closes) and rsi(closes) > 70
            else "超卖"
            if rsi(closes) and rsi(closes) < 30
            else "中性",
            "price_vs_bollinger": "接近上轨"
            if bb_upper and current_price > ma20 + 1.5 * (bb_upper - ma20) / 2
            else "接近下轨"
            if bb_lower and current_price < ma20 - 1.5 * (ma20 - bb_lower) / 2
            else "中轨附近",
        }
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        return json.dumps(
            {"error": f"计算技术指标失败: {str(e)}"}, ensure_ascii=False
        )


# ---------------------------------------------------------------------------
# MCP Tool: 综合速览
# ---------------------------------------------------------------------------
@mcp.tool()
def get_stock_overview(symbol: str) -> str:
    """
    一站式获取股票综合速览：行情 + 财务 + 技术指标。
    适合快速了解一只股票的全貌，是投研分析的起点。
    返回三大维度的合并数据。
    """
    quote = json.loads(get_stock_quote(symbol))
    financials = json.loads(get_financial_indicators(symbol))
    technicals = json.loads(get_technical_indicators(symbol))

    result = {
        "overview": "股票综合速览",
        "quote": quote,
        "financials": financials,
        "technicals": technicals,
        "generated_at": datetime.datetime.now().isoformat(),
    }
    return json.dumps(result, ensure_ascii=False)


# ---------------------------------------------------------------------------
# 启动
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    mcp.run()
