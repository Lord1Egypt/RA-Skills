#!/usr/bin/env python3
"""
Stock Data - Simplywall.st Data Fetcher for OpenClaw
Fetches comprehensive stock data from Simplywall.st

Direct HTTP fetch (no API key required)
v2.0.0 - Enhanced extraction: price targets, returns, insider activity,
         revenue/earnings growth, margins, health metrics, forecasts
"""

import json
import re
import asyncio
from datetime import datetime, timezone
from typing import Optional, Dict, Any

try:
    import aiohttp
except ImportError:
    raise ImportError('aiohttp required: pip install aiohttp')


def get_stock_url(ticker: str, exchange: Optional[str] = None) -> str:
    """Construct URL for stock page based on exchange"""
    ticker_lower = ticker.lower()
    exchange = (exchange or 'idx').lower()

    patterns = {
        'idx': f'https://simplywall.st/stock/idx/{ticker_lower}',
        'nasdaq': f'https://simplywall.st/stocks/us/any/nasdaq-{ticker_lower}/{ticker_lower}',
        'nyse': f'https://simplywall.st/stocks/us/any/nyse-{ticker_lower}/{ticker_lower}',
        'asx': f'https://simplywall.st/stock/asx/{ticker_lower}',
        'lse': f'https://simplywall.st/stock/lse/{ticker_lower}',
        'tsx': f'https://simplywall.st/stock/tsx/{ticker_lower}',
        'sgx': f'https://simplywall.st/stock/sgx/{ticker_lower}',
        'tse': f'https://simplywall.st/stock/tse/{ticker_lower}',
        'hkse': f'https://simplywall.st/stock/hkse/{ticker_lower}',
        'krx': f'https://simplywall.st/stock/krx/{ticker_lower}',
    }
    return patterns.get(exchange, patterns['idx'])


def parse_react_state(html: str) -> Dict:
    """Extract and parse __REACT_QUERY_STATE__ from HTML"""
    match = re.search(r'window\.__REACT_QUERY_STATE__\s*=\s*(\{[\s\S]+?\});?\s*</script>', html)
    if not match:
        return {}

    json_str = match.group(1)
    json_str = re.sub(r':undefined([,\]}])', r':null\1', json_str)
    json_str = re.sub(r'([,\[{])undefined([,\]}])', r'\1null\2', json_str)

    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return {}


def safe_get(d, *keys, default=None):
    """Safely traverse nested dicts"""
    for k in keys:
        if isinstance(d, dict):
            d = d.get(k)
        else:
            return default
    return d if d is not None else default


def extract_data(state: Dict, ticker: str) -> Dict:
    """Extract structured stock data from React Query state"""
    result = {
        'ticker': ticker.upper(),
        'exchange': None,
        'company': {},
        'price': {},
        'returns': {},
        'valuation': {},
        'financials': {},
        'margins': {},
        'growth': {},
        'dividend': {},
        'forecast': {},
        'priceTarget': {},
        'health': {},
        'insiders': {},
        'snowflake': {},
        'recentEvents': [],
        'fetchedAt': datetime.now(timezone.utc).isoformat()
    }

    # Find extended analysis data
    ext = {}
    basic_analysis = {}

    for query in state.get('queries', []):
        qd = query.get('state', {}).get('data', {})

        # Company info
        if isinstance(qd, dict) and 'Company' in qd:
            info = safe_get(qd, 'Company', 'data', 'info', default={})
            result['exchange'] = info.get('exchange_symbol')
            result['company'] = {
                'name': info.get('name'),
                'description': info.get('short_description'),
                'country': info.get('country'),
                'founded': info.get('year_founded'),
                'website': info.get('url')
            }

        # Analysis data (basic + extended)
        if isinstance(qd, dict) and 'data' in qd and isinstance(qd.get('data'), dict):
            a = safe_get(qd, 'data', 'analysis', 'data', default={})
            if a and 'pe' in a:
                basic_analysis = a
                ext = safe_get(a, 'extended', 'data', 'analysis', default={})

        # Snowflake, price & events
        if isinstance(qd, dict) and isinstance(qd.get('snowflake'), dict):
            axes = safe_get(qd, 'snowflake', 'data', 'axes', default=[])
            result['snowflake'] = {
                'value': axes[0] if len(axes) > 0 else None,
                'future': axes[1] if len(axes) > 1 else None,
                'past': axes[2] if len(axes) > 2 else None,
                'health': axes[3] if len(axes) > 3 else None,
                'dividend': axes[4] if len(axes) > 4 else None
            }
            result['price']['last'] = qd.get('last_share_price')
            result['price']['currency'] = qd.get('currency_iso')

            events = safe_get(qd, 'events', 'data', default=[])
            result['recentEvents'] = [
                {'title': e.get('title'), 'description': (e.get('description') or '')[:200]}
                for e in events[:5]
            ]

    # === Extract from basic analysis ===
    a = basic_analysis

    result['valuation'] = {
        'marketCap': a.get('market_cap'),
        'peRatio': a.get('pe'),
        'pbRatio': a.get('pb'),
        'pegRatio': a.get('peg'),
        'intrinsicDiscount': a.get('intrinsic_discount'),
        'status': 'overvalued' if (a.get('intrinsic_discount') or 0) < 0 else 'undervalued',
        'preferredMultiple': a.get('preferred_multiple'),
    }

    result['financials'] = {
        'eps': a.get('eps'),
        'roe': a.get('roe'),
        'roa': a.get('roa'),
        'debtEquity': a.get('debt_equity'),
        'sharePrice': a.get('share_price'),
        'analystCount': a.get('analyst_count'),
        'insiderBuying': a.get('insider_buying'),
    }

    result['dividend'] = {
        'yield': safe_get(a, 'dividend', 'current'),
        'futureYield': safe_get(a, 'dividend', 'future'),
    }

    result['forecast'] = {
        'earningsGrowth1Y': safe_get(a, 'future', 'growth_1y'),
        'earningsGrowth3Y': safe_get(a, 'future', 'growth_3y'),
        'roe1Y': safe_get(a, 'future', 'roe_1y'),
        'roe3Y': safe_get(a, 'future', 'roe_3y'),
        'analystCount': a.get('analyst_count'),
    }

    # === Extract from EXTENDED analysis (the rich data) ===
    if ext:
        # Value & Returns
        val = ext.get('value', {})
        result['price'].update({
            'last': val.get('last_share_price') or result['price'].get('last'),
            'beta5Y': val.get('beta_5y'),
        })
        result['returns'] = {
            '1d': val.get('return_1d'),
            '7d': val.get('return_7d'),
            '30d': val.get('return_30d'),
            '90d': val.get('return_90d'),
            'ytd': val.get('return_ytd'),
            '1yr': val.get('return_1yr_abs'),
            '3yr': val.get('return_3yr_abs'),
            '5yr': val.get('return_5yr_abs'),
            'sinceIPO': val.get('return_since_ipo_abs'),
        }
        result['valuation'].update({
            'priceToSales': val.get('price_to_sales'),
            'evToSales': val.get('ev_to_sales'),
            'evToEbitda': val.get('ev_to_ebitda'),
            'npvPerShare': val.get('npv_per_share'),
            'marketCapLocal': val.get('market_cap'),
            'marketCapUSD': val.get('market_cap_usd'),
        })
        result['priceTarget'] = {
            'consensus': val.get('price_target'),
            'low': val.get('price_target_low'),
            'high': val.get('price_target_high'),
            'analystCount': val.get('price_target_analyst_count'),
        }

        # Past Performance & Margins
        past = ext.get('past', {})
        result['growth'] = {
            'revenueGrowth1Y': past.get('revenue_growth_1y'),
            'revenueGrowth3Y': past.get('revenue_growth_3y'),
            'revenueGrowth5Y': past.get('revenue_growth_5y'),
            'netIncomeGrowth1Y': past.get('net_income_growth_1y'),
            'netIncomeGrowth3Y': past.get('net_income_growth_3y'),
            'netIncomeGrowth5Y': past.get('net_income_growth_5y'),
            'epsGrowth1Y': past.get('earnings_per_share_growth_1y'),
            'epsGrowth3Y': past.get('earnings_per_share_growth_3y'),
            'epsGrowth5Y': past.get('earnings_per_share_growth_5y'),
        }
        result['margins'] = {
            'grossProfit': past.get('gross_profit_margin'),
            'netIncome': past.get('net_income_margin'),
            'ebit': past.get('ebit_margin'),
            'ebitda': past.get('ebitda_margin'),
        }
        result['financials'].update({
            'revenue': past.get('revenue'),
            'revenueUSD': past.get('revenue_usd'),
            'netIncome': past.get('net_income'),
            'netIncomeUSD': past.get('net_income_usd'),
            'roce': past.get('return_on_capital_employed'),
            'yearsProfitable': past.get('years_profitable'),
            'tradingSinceYears': past.get('trading_since_years'),
            'latestFiscalYear': past.get('latest_fiscal_year'),
            'latestFiscalQuarter': past.get('latest_fiscal_quarter'),
        })

        # Future Forecasts (extended)
        fut = ext.get('future', {})
        result['forecast'].update({
            'roe1Y': fut.get('return_on_equity_1y') or result['forecast'].get('roe1Y'),
            'roe3Y': fut.get('return_on_equity_3y'),
            'epsGrowth1Y': fut.get('earnings_per_share_growth_1y'),
            'epsGrowth3Y': fut.get('earnings_per_share_growth_3y'),
            'revenueGrowth1Y': fut.get('revenue_growth_1y'),
            'revenueGrowth2Y': fut.get('revenue_growth_2y'),
            'revenueGrowth3Y': fut.get('revenue_growth_3y'),
            'netIncomeGrowth1Y': fut.get('net_income_growth_1y'),
            'netIncomeGrowth2Y': fut.get('net_income_growth_2y'),
            'netIncomeGrowth3Y': fut.get('net_income_growth_3y'),
            'forwardPE1Y': fut.get('forward_pe_1y'),
            'nextEarningsRelease': fut.get('next_earnings_release'),
        })

        # Dividend (extended)
        div = ext.get('dividend', {})
        result['dividend'].update({
            'yieldHistory': div.get('historical_dividend_yield'),
            'volatility': div.get('dividend_volatility'),
            'payingYears': div.get('dividend_paying_years'),
            'payoutRatio': div.get('payout_ratio'),
            'payoutRatio3Y': div.get('payout_ratio_3y'),
            'buybackYield': div.get('buyback_yield'),
            'totalShareholderYield': div.get('total_shareholder_yield'),
        })

        # Health (balance sheet)
        health = ext.get('health', {})
        result['health'] = {
            'totalDebt': health.get('total_debt'),
            'totalEquity': health.get('total_equity'),
            'totalAssets': health.get('total_assets'),
            'debtToEquity': health.get('debt_to_equity_ratio'),
            'netDebtToEquity': health.get('net_debt_to_equity'),
            'currentRatio': health.get('current_solvency_ratio'),
            'interestCover': health.get('net_interest_cover'),
            'leveredFCF': health.get('levered_free_cash_flow'),
            'leveredFCF1Y': health.get('levered_free_cash_flow_1y'),
            'fcfGrowthAnnual': health.get('levered_free_cash_flow_growth_annual'),
            'netDebt': health.get('net_debt'),
            'netDebtToEbitda': health.get('net_debt_to_ebitda'),
            'bookValuePerShare': health.get('book_value_per_share'),
            'lastBalanceSheetUpdate': health.get('last_balance_sheet_update'),
        }

        # Insiders & Management
        mgmt = ext.get('management', {})
        result['insiders'] = {
            'buyingRatio': mgmt.get('insider_buying_ratio'),
            'totalSharesBought': mgmt.get('total_shares_bought'),
            'totalSharesSold': mgmt.get('total_shares_sold'),
            'totalEmployees': mgmt.get('total_employees'),
            'ceoCompensation': mgmt.get('ceo_compensation_total'),
            'ceoCompensationUSD': mgmt.get('ceo_compensation_total_usd'),
            'boardMembers': mgmt.get('total_board_members_count'),
            'independentBoardRatio': mgmt.get('independent_board_members_ratio'),
            'managementTenure': mgmt.get('management_tenure'),
            'boardTenure': mgmt.get('board_tenure'),
        }

        # Misc (volatility)
        misc = ext.get('misc', {})
        result['price'].update({
            'min52W': misc.get('min_price_52w'),
            'max52W': misc.get('max_price_52w'),
            'isVolatile': misc.get('is_volatile'),
            'dailyStdDev90d': misc.get('daily_return_standard_deviation_90d'),
            'dailyStdDev1Y': misc.get('daily_return_standard_deviation_1y'),
        })

    return result


async def fetch_stock(ticker: str, exchange: Optional[str] = None) -> Dict:
    """Main function to fetch stock data"""
    url = get_stock_url(ticker, exchange)

    print(f'[stock_data] Fetching: {url}')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as resp:
            if resp.status != 200:
                return {'success': False, 'error': f'HTTP error {resp.status}'}

            html = await resp.text()
            print(f'[stock_data] HTML length: {len(html)}')

            state = parse_react_state(html)
            if not state:
                return {'success': False, 'error': 'Could not parse React state from page'}

            data = extract_data(state, ticker)
            data['url'] = url
            data['data_source'] = 'simplywall.st'

            return {'success': True, 'data': data}


# OpenClaw skill interface
async def execute(params: Dict) -> Dict:
    """OpenClaw skill executor"""
    ticker = params.get('ticker')
    if not ticker:
        return {'success': False, 'error': 'ticker parameter is required'}

    try:
        return await fetch_stock(ticker, params.get('exchange'))
    except Exception as e:
        return {'success': False, 'error': str(e)}


METADATA = {
    'name': 'stock_data',
    'description': 'Fetch comprehensive stock data from Simplywall.st',
    'category': 'finance',
    'tags': ['stock', 'valuation', 'analysis', 'simplywall', 'investment'],
    'triggers': ['saham', 'stock', 'cek saham', 'valuation', 'dividend', 'analisa'],
    'requiredEnvVars': [],
    'version': '2.0.0',
    'changelog': 'v2.0.0 - Enhanced extraction: price targets, all returns, insider activity, margins, health, growth, forecasts',
    'author': 'OpenClaw Community'
}


if __name__ == '__main__':
    import sys
    ticker = sys.argv[1] if len(sys.argv) > 1 else 'ADRO'
    exchange = sys.argv[2] if len(sys.argv) > 2 else 'IDX'

    print(f'Stock Data Skill Test: {ticker} ({exchange})\n')
    result = asyncio.run(execute({'ticker': ticker, 'exchange': exchange}))
    print(json.dumps(result, indent=2, default=str))
