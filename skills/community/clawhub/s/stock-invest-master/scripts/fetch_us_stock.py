#!/usr/bin/env python3
"""美股数据获取与结构化整合脚本。

数据来源（真实可用）:
  - yfinance (Yahoo Finance): 日线行情(Open/High/Low/Close/Volume)、
    财务报表(利润表/资产负债表/现金流)、关键指标(PE/PB/ROE/ROA/毛利率等)
    ── 封装自 query1.finance.yahoo.com / query2.finance.yahoo.com
  - 东方财富 push2 API: 实时行情快照（股价/PE/PB/市值/涨跌幅）
    ── push2.eastmoney.com/api/qt/stock/get
  - Alpha Vantage (可选): 免费API，需申请 apikey
    ── www.alphavantage.co/query

依赖: pip install yfinance requests

用法:
    # 获取完整美股数据（日线 + 财务指标）
    python3 fetch_us_stock.py AAPL

    # 仅获取行情
    python3 fetch_us_stock.py AAPL --only daily

    # 仅获取财务指标
    python3 fetch_us_stock.py AAPL --only fina

    # 指定日期范围
    python3 fetch_us_stock.py AAPL --start 20250101 --end 20250425

    # 使用东方财富数据源（适合国内网络环境）
    python3 fetch_us_stock.py AAPL --source eastmoney

    # 指定输出文件
    python3 fetch_us_stock.py AAPL -o /tmp/aapl_data.json
"""

import json
import sys
import argparse
import time
import logging
from datetime import datetime, timedelta
from typing import Optional

import requests

# ─── 日志配置 ─────────────────────────────────────────────
logging.basicConfig(
    level=logging.WARNING,
    format='%(levelname)s: %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════
# 数据源 1: yfinance (Yahoo Finance) — 最全面
# ═══════════════════════════════════════════════════════════

def _get_yf_ticker(symbol: str):
    """获取 yfinance Ticker 对象（带重试）。"""
    try:
        import yfinance as yf
    except ImportError:
        raise ImportError(
            "yfinance 未安装，请执行: pip install yfinance\n"
            "或使用 --source eastmoney 切换到东方财富数据源"
        )

    for attempt in range(3):
        try:
            return yf.Ticker(symbol)
        except Exception as e:
            if attempt < 2:
                wait = 2 ** attempt
                logger.warning(f"yfinance 连接失败 (尝试 {attempt + 1}/3)，{wait}s 后重试: {e}")
                time.sleep(wait)
            else:
                raise


def fetch_daily_via_yfinance(symbol: str, start: str, end: str) -> dict:
    """通过 yfinance 获取美股日线行情（含 PE/PB/市值）。

    数据来源: Yahoo Finance v8 chart API
    URL: https://query1.finance.yahoo.com/v8/finance/chart/{symbol}
    """
    stock = _get_yf_ticker(symbol)

    # 转换日期格式: YYYYMMDD → YYYY-MM-DD
    start_fmt = f"{start[:4]}-{start[4:6]}-{start[6:8]}"
    end_fmt = f"{end[:4]}-{end[4:6]}-{end[6:8]}"

    # 获取历史行情
    hist = stock.history(start=start_fmt, end=end_fmt)

    if hist.empty:
        logger.warning(f"yfinance: {symbol} 在 {start}-{end} 无行情数据")
        return {}

    # 取最后一行
    last = hist.iloc[-1]
    prev = hist.iloc[-2] if len(hist) > 1 else last

    # 获取实时指标
    try:
        info = stock.info
    except Exception:
        info = {}

    trade_date_str = str(last.name.date()).replace('-', '')
    pre_close = float(prev['Close'])
    close = float(last['Close'])
    pct_change = ((close - pre_close) / pre_close * 100) if pre_close else None

    result = {
        'ticker': symbol,
        'trade_date': trade_date_str,
        'open': float(last['Open']),
        'high': float(last['High']),
        'low': float(last['Low']),
        'close': close,
        'pre_close': pre_close,
        'pct_change': round(pct_change, 2) if pct_change else None,
        'vol': int(last['Volume']) if last['Volume'] else None,
        'amount': round(close * int(last['Volume']), 2) if last['Volume'] and close else None,
        'pe': info.get('trailingPE'),
        'pb': info.get('priceToBook'),
        'total_mv': info.get('marketCap'),
        'turnover_ratio': info.get('sharesPercentSharesOut'),  # 近似换手率
    }

    return result


def fetch_financials_via_yfinance(symbol: str, _period: str = None) -> dict:
    """通过 yfinance 获取美股财务指标。

    数据来源: Yahoo Finance quoteSummary API
    URL: https://query2.finance.yahoo.com/v10/finance/quoteSummary/{symbol}
    """
    stock = _get_yf_ticker(symbol)

    try:
        info = stock.info
    except Exception as e:
        logger.error(f"yfinance 获取 info 失败: {e}")
        return {}

    # 尝试从 quarterly_financials 获取最新报告期
    end_date = None
    ind_type = None
    try:
        qf = stock.quarterly_financials
        if not qf.empty:
            latest_col = qf.columns[0]
            end_date = str(latest_col.date()).replace('-', '')
            # 推断报告类型
            month = latest_col.month
            if month in [12, 1]:
                ind_type = 'Q4'  # FY年报
            elif month in [3, 4]:
                ind_type = 'Q1'
            elif month in [6, 7]:
                ind_type = 'Q2'
            elif month in [9, 10]:
                ind_type = 'Q3'
    except Exception:
        pass

    # yfinance info 字段映射
    # 注意: yfinance 返回的百分比值通常是小数形式（0.20 = 20%）
    gross_margin = info.get('grossMargins')
    net_margin = info.get('profitMargins')
    roe = info.get('returnOnEquity')
    roa = info.get('returnOnAssets')

    result = {
        'ticker': symbol,
        'end_date': end_date,
        'ind_type': ind_type,
        'security_name_abbr': info.get('shortName') or info.get('longName') or symbol,
        'operate_income': info.get('totalRevenue'),                  # 营业收入
        'operate_income_yoy': round(info.get('revenueGrowth', 0) * 100, 2)
                              if info.get('revenueGrowth') else None,  # 营收YoY%
        'gross_profit_ratio': round(gross_margin * 100, 2)
                              if gross_margin else None,              # 毛利率%
        'net_profit_ratio': round(net_margin * 100, 2)
                            if net_margin else None,                  # 净利率%
        'parent_holder_netprofit': info.get('netIncomeToCommon'),     # 归母净利润
        'parent_holder_netprofit_yoy': round(info.get('earningsGrowth', 0) * 100, 2)
                                       if info.get('earningsGrowth') else None,
        'basic_eps': info.get('trailingEps'),                         # 基本EPS
        'diluted_eps': info.get('dilutedEps'),                        # 稀释EPS
        'roe_avg': round(roe * 100, 2) if roe else None,             # ROE%
        'roa': round(roa * 100, 2) if roa else None,                 # ROA%
        'current_ratio': info.get('currentRatio'),                    # 流动比率
        'debt_asset_ratio': round(info.get('debtToEquity', 0), 2)
                            if info.get('debtToEquity') else None,    # 负债权益比
        'equity_ratio': None,  # yfinance 不直接提供，可从 balance sheet 计算
        'currency': info.get('currency') or 'USD',
    }

    return result


# ═══════════════════════════════════════════════════════════
# 数据源 2: 东方财富 push2 API — 实时行情快照
# ═══════════════════════════════════════════════════════════

EASTMONEY_US_QUOTE_URL = "https://push2.eastmoney.com/api/qt/stock/get"

# 东方财富 美股行情字段定义
# secid 格式: 105.{TICKER} (105 = 美股市场代码)
EASTMONEY_US_FIELDS = (
    "f43,f44,f45,f46,f47,f48,f50,f51,f52,f55,"
    "f57,f58,f60,f115,f116,f117,f162,f167,f168,f169,f170,f171"
)
# f43: 最新价     f44: 最高价     f45: 最低价     f46: 开盘价
# f47: 成交量     f48: 成交额     f50: 量比       f57: 代码
# f58: 名称       f60: 昨收       f115: 市盈率(动) f116: 总市值
# f117: 流通市值   f162: ？        f167: 市净率    f168: 换手率
# f169: 涨跌幅    f170: 涨跌额    f171: ？


def fetch_daily_via_eastmoney(symbol: str) -> dict:
    """通过东方财富 push2 API 获取美股实时行情。

    数据来源: 东方财富网 push2 接口（公开无需认证）
    URL: https://push2.eastmoney.com/api/qt/stock/get
    """
    params = {
        'secid': f'105.{symbol}',
        'fields': EASTMONEY_US_FIELDS,
    }
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ),
        'Referer': 'https://quote.eastmoney.com/',
    }

    try:
        resp = requests.get(EASTMONEY_US_QUOTE_URL, params=params, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        logger.error(f"东方财富 API 请求失败: {e}")
        return {}
    except json.JSONDecodeError:
        logger.error("东方财富 API 返回非 JSON 数据")
        return {}

    d = data.get('data')
    if not d:
        logger.warning(f"东方财富: 未找到 {symbol} 的数据")
        return {}

    f43 = d.get('f43')     # 最新价 (已除以1000? 需确认)
    f60 = d.get('f60')     # 昨收
    f169 = d.get('f169')   # 涨跌幅 (已为百分比数值)

    # 东方财富价格/市值可能需除以单位换算
    # 美股价格通常 f43/1000 = 实际美元价格
    price = f43 / 1000 if f43 and f43 > 100 else f43
    pre_close = f60 / 1000 if f60 and f60 > 100 else f60

    result = {
        'ticker': symbol,
        'trade_date': datetime.now().strftime('%Y%m%d'),
        'open': (d.get('f46') or 0) / 1000 if d.get('f46', 0) > 100 else d.get('f46'),
        'high': (d.get('f44') or 0) / 1000 if d.get('f44', 0) > 100 else d.get('f44'),
        'low': (d.get('f45') or 0) / 1000 if d.get('f45', 0) > 100 else d.get('f45'),
        'close': price,
        'pre_close': pre_close,
        'pct_change': f169 / 100 if f169 and abs(f169) > 10 else f169,  # 转换为%
        'vol': d.get('f47'),
        'amount': d.get('f48'),
        'pe': d.get('f115'),
        'pb': d.get('f167'),
        'total_mv': d.get('f116'),  # 东方财富市值单位需确认（通常为美元）
        'turnover_ratio': (d.get('f168') or 0) / 100 if d.get('f168', 0) > 10 else d.get('f168'),
    }

    return result


def fetch_financials_via_eastmoney(_symbol: str, _period: str = None) -> dict:
    """通过东方财富获取美股财务指标。

    注意: 东方财富美股财务数据需要更复杂的 datacenter API，
    目前建议使用 yfinance 获取财务数据。
    此函数作为占位符返回空字典。
    """
    logger.warning(
        "东方财富美股财务数据API较复杂，建议使用 yfinance (默认) 获取财务指标。\n"
        "如只需实时行情，可用: --source eastmoney --only daily"
    )
    return {}


# ═══════════════════════════════════════════════════════════
# 统一获取接口
# ═══════════════════════════════════════════════════════════

def fetch_daily(symbol: str, start: str, end: str, source: str = 'auto') -> dict:
    """获取美股日线行情，自动选择数据源。

    优先级: yfinance > 东方财富
    """
    if source in ('auto', 'yfinance'):
        try:
            result = fetch_daily_via_yfinance(symbol, start, end)
            if result:
                logger.info(f"✓ 使用 yfinance 获取 {symbol} 行情成功")
                return result
        except Exception as e:
            logger.warning(f"yfinance 行情获取失败: {e}")

    if source in ('auto', 'eastmoney'):
        try:
            result = fetch_daily_via_eastmoney(symbol)
            if result:
                logger.info(f"✓ 使用东方财富获取 {symbol} 行情成功")
                return result
        except Exception as e:
            logger.warning(f"东方财富行情获取失败: {e}")

    return {}


def fetch_financials(symbol: str, period: str = None, source: str = 'auto') -> dict:
    """获取美股财务指标，自动选择数据源。"""
    if source in ('auto', 'yfinance'):
        try:
            result = fetch_financials_via_yfinance(symbol, period)
            if result:
                logger.info(f"✓ 使用 yfinance 获取 {symbol} 财务指标成功")
                return result
        except Exception as e:
            logger.warning(f"yfinance 财务指标获取失败: {e}")

    if source in ('auto', 'eastmoney'):
        try:
            result = fetch_financials_via_eastmoney(symbol, period)
            if result:
                return result
        except Exception as e:
            logger.warning(f"东方财富财务指标获取失败: {e}")

    return {}


# ═══════════════════════════════════════════════════════════
# 交叉校验
# ═══════════════════════════════════════════════════════════

def cross_validate_us_data(daily_metrics: dict, fina_metrics: dict) -> list:
    """美股数据交叉校验。

    校验项:
    1. PE ≈ PB/ROE (偏差<40%正常，因美股回购会导致ROE失真)
    2. PB 为负 → 提示净资产为负
    3. ROE > 100% → 提示回购影响
    """
    warnings = []

    pe = daily_metrics.get('pe')
    pb = daily_metrics.get('pb')
    roe = fina_metrics.get('roe_avg')

    if pe and pb and roe and roe > 0:
        expected_pe = pb / (roe / 100)
        ratio = pe / expected_pe if expected_pe > 0 else float('inf')
        if abs(ratio - 1) > 0.40:
            warnings.append(
                f"⚠️ PE/PB/ROE 不一致: PE={pe}, PB={pb}, ROE={roe}%, "
                f"预期PE≈{expected_pe:.1f}, 偏差{abs(ratio - 1) * 100:.0f}% "
                f"(注意：美股大量回购可能导致ROE失真)"
            )

    if pb is not None and pb < 0:
        warnings.append(
            f"⚠️ PB为负({pb})：净资产为负，PE/PB估值可能失真，建议改用EV/EBITDA"
        )

    if roe is not None and roe > 100:
        warnings.append(
            f"⚠️ ROE异常高({roe}%)：可能因大量回购导致净资产极低，需结合净利润绝对值分析"
        )

    # 价格一致性校验
    daily_close = daily_metrics.get('close')
    if daily_close is not None and daily_close <= 0:
        warnings.append(f"⚠️ 股价异常: {daily_close}")

    return warnings


# ═══════════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description='美股数据获取与结构化整合 — 支持 yfinance / 东方财富 双数据源',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
数据源:
  yfinance     Yahoo Finance 封装 (默认) — 日线+财报+指标，最全面
  eastmoney    东方财富 push2 API — 实时行情快照，国内网络友好

示例:
  python3 fetch_us_stock.py AAPL
  python3 fetch_us_stock.py NVDA --only fina
  python3 fetch_us_stock.py GOOGL --source eastmoney --only daily
  python3 fetch_us_stock.py AAPL --start 20250401 --end 20250430 -o aapl.json
        """
    )
    parser.add_argument('ticker', help='美股代码 (如 AAPL, GOOGL, NVDA, MSFT)')
    parser.add_argument(
        '--only', choices=['daily', 'fina'], default=None,
        help='仅获取行情(daily)或财务指标(fina)，默认两者都获取'
    )
    parser.add_argument(
        '--source', choices=['auto', 'yfinance', 'eastmoney'], default='auto',
        help='数据来源: auto(自动选择) / yfinance / eastmoney (默认: auto)'
    )
    parser.add_argument('--start', help='行情开始日期 (YYYYMMDD)', default=None)
    parser.add_argument('--end', help='行情结束日期 (YYYYMMDD)', default=None)
    parser.add_argument('--period', help='财务指标报告期 (YYYYMMDD)', default=None)
    parser.add_argument('--output', '-o', help='输出文件路径 (默认stdout)', default=None)
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细日志')

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.INFO)

    ticker = args.ticker.upper()

    # 默认日期范围：最近30天
    if not args.end:
        args.end = datetime.now().strftime('%Y%m%d')
    if not args.start:
        args.start = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')

    result = {
        'stock_code': ticker,
        'market': 'US',
        'currency': 'USD',
        'data_source': [],
        'daily': {},
        'fina_indicator': {},
        'warnings': [],
    }

    # 获取日线行情
    if args.only in (None, 'daily'):
        logger.info(f"📊 获取 {ticker} 日线行情 (数据源: {args.source})...")
        daily = fetch_daily(ticker, args.start, args.end, source=args.source)

        if daily:
            result['daily'] = daily
            data_src = 'yfinance' if daily.get('amount') and daily.get('pe') else 'eastmoney'
            result['data_source'].append(data_src)
            print(
                f"  ✓ 行情获取成功: {daily.get('trade_date')} "
                f"收盘 ${daily.get('close')}  PE={daily.get('pe')}",
                file=sys.stderr
            )
        else:
            print(f"  ✗ 无日线数据返回", file=sys.stderr)

    # 获取财务指标
    if args.only in (None, 'fina'):
        logger.info(f"📊 获取 {ticker} 财务指标 (数据源: {args.source})...")
        fina = fetch_financials(ticker, args.period, source=args.source)

        if fina:
            result['fina_indicator'] = fina
            if 'yfinance' not in result['data_source']:
                result['data_source'].append('yfinance')
            name = fina.get('security_name_abbr', ticker)
            period_str = fina.get('end_date', 'N/A')
            roe_str = f"ROE={fina.get('roe_avg')}%" if fina.get('roe_avg') else ''
            print(
                f"  ✓ 财务指标获取成功: {name} 报告期={period_str} {roe_str}",
                file=sys.stderr
            )
        else:
            print(f"  ✗ 无财务指标数据返回", file=sys.stderr)

    # 交叉校验
    if result['daily'] and result['fina_indicator']:
        result['warnings'] = cross_validate_us_data(result['daily'], result['fina_indicator'])

    # 如果没有数据源标注，说明全部失败
    if not result['data_source']:
        result['warnings'].append(
            "❌ 所有数据源均获取失败。请检查:\n"
            "  1. 网络连接是否正常\n"
            "  2. yfinance 是否安装: pip install yfinance\n"
            "  3. 尝试: --source eastmoney (国内网络)\n"
            "  4. 股票代码是否正确 (美股代码不含后缀)"
        )

    # 输出
    output_json = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output_json)
        print(f"\n✓ 结果已保存至 {args.output}", file=sys.stderr)
    else:
        print(output_json)

    # 警告输出到 stderr
    if result['warnings']:
        print("\n--- 校验警告 ---", file=sys.stderr)
        for w in result['warnings']:
            print(w, file=sys.stderr)


if __name__ == "__main__":
    main()
