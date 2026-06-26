#!/usr/bin/env python3
"""从 NeoData / finance-data-retrieval 返回结果中结构化提取单只股票的关键指标。

支持三市场：
  - A股 (market=A)：代码格式 XXXXXX.SZ / XXXXXX.SH
  - 美股 (market=US)：代码格式 AAPL, GOOGL 等
  - 港股 (market=HK)：代码格式 XXXXX.HK

用法:
    # A股（默认）
    python3 scripts/query.py --query "思源电气002028 最新股价 PE PB ROE" > /tmp/result.json
    python3 extract_stock_data.py /tmp/result.json 002028.SZ

    # 美股
    python3 scripts/query.py --query "Apple AAPL stock price PE PB ROE" > /tmp/us_result.json
    python3 extract_stock_data.py /tmp/us_result.json AAPL --market US

    # 港股
    python3 scripts/query.py --query "腾讯00700.HK 最新股价 市盈率 市净率 ROE" > /tmp/hk_result.json
    python3 extract_stock_data.py /tmp/hk_result.json 00700.HK --market HK

    # 也可以直接从 stdin 读取
    python3 scripts/query.py --query "思源电气002028" | python3 extract_stock_data.py - 002028.SZ

输出: JSON 格式的结构化指标，含交叉校验警告
"""

import json
import re
import sys
import argparse
from typing import Optional


# ─── 市场识别 ─────────────────────────────────────────────

def detect_market(stock_code: str) -> str:
    """根据股票代码格式自动检测市场类型。"""
    code = stock_code.upper()
    if code.endswith('.SZ') or code.endswith('.SH'):
        return 'A'
    elif code.endswith('.HK'):
        return 'HK'
    elif re.match(r'^[A-Z]+$', code):
        return 'US'
    else:
        # 尝试数字代码
        if re.match(r'^\d{6}$', code):
            return 'A'  # 可能是A股，需补后缀
        return 'UNKNOWN'


def normalize_a_stock_code(code: str) -> str:
    """将纯数字A股代码补全为标准格式。"""
    if '.' in code:
        return code.upper()
    if re.match(r'^\d{6}$', code):
        if code.startswith(('6',)):
            return f"{code}.SH"
        else:
            return f"{code}.SZ"
    return code.upper()


# ─── A股数据提取 ─────────────────────────────────────────

def extract_a_stock_section(text: str, stock_code: str) -> Optional[str]:
    """从 NeoData 返回文本中提取目标 A 股代码对应的段落。"""
    # 匹配目标股票代码的 A 股段落
    pattern = rf'{stock_code}\)在A股股票的行情：(.*?)(?=(?:\([^)]+\)在(?:美股|港股)股票的行情：)|$)'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1)

    # 备选：匹配 "XXXXXX.XX)在A股股票" 段落
    pattern2 = rf'{stock_code}\)在A股[^：]*：(.*?)(?=(?:\([^)]+\)在(?:美股|港股)股票的行情：)|$)'
    match2 = re.search(pattern2, text, re.DOTALL)
    if match2:
        return match2.group(1)

    return None


def parse_a_realtime_metrics(section: str) -> dict:
    """从 A 股行情段落中解析关键指标。"""
    metrics = {}

    m = re.search(r'数据更新时间[:\s]*(\S+)', section)
    if m: metrics['data_time'] = m.group(1)

    m = re.search(r'最新价格[:\s]*([\d.]+)元', section)
    if m: metrics['price'] = float(m.group(1))

    m = re.search(r'昨日收盘价格[:\s]*([\d.]+)元', section)
    if m: metrics['prev_close'] = float(m.group(1))

    m = re.search(r'当日涨跌幅[:\s]*([-\d.]+)%', section)
    if m: metrics['change_pct'] = float(m.group(1))

    m = re.search(r'市盈率\(TTM\)[:\s]*([\d.]+)', section)
    if m: metrics['pe_ttm'] = float(m.group(1))

    m = re.search(r'市净率[:\s]*([\d.]+)', section)
    if m: metrics['pb'] = float(m.group(1))

    m = re.search(r'股息率[:\s]*([\d.]+)', section)
    if m: metrics['dividend_yield'] = float(m.group(1))

    m = re.search(r'总市值\(亿元\)[:\s]*([\d,.]+)', section)
    if m: metrics['market_cap_yi'] = float(m.group(1).replace(',', ''))

    m = re.search(r'流通市值\(亿元\)[:\s]*([\d,.]+)', section)
    if m: metrics['float_cap_yi'] = float(m.group(1).replace(',', ''))

    m = re.search(r'年初至今涨跌幅[:\s]*([-\d.]+)%', section)
    if m: metrics['ytd_change'] = float(m.group(1))

    m = re.search(r'5日涨跌幅[:\s]*([-\d.]+)%', section)
    if m: metrics['5d_change'] = float(m.group(1))

    m = re.search(r'换手率[:\s]*([\d.]+)%', section)
    if m: metrics['turnover_rate'] = float(m.group(1))

    return metrics


def parse_a_fundamental_metrics(text: str) -> dict:
    """从基本面/估值段落中提取A股指标。"""
    metrics = {}

    m = re.search(r'净资产收益率TTM为([-\d.]+)%', text)
    if m: metrics['roe_ttm'] = float(m.group(1))

    m = re.search(r'销售净利率TTM为([-\d.]+)%', text)
    if m: metrics['net_margin_ttm'] = float(m.group(1))

    m = re.search(r'销售毛利率TTM为([-\d.]+)%', text)
    if m: metrics['gross_margin_ttm'] = float(m.group(1))

    m = re.search(r'营业收入同比增长率TTM为([-\d.]+)%', text)
    if m: metrics['revenue_yoy_ttm'] = float(m.group(1))

    m = re.search(r'净利润增长率TTM为([-\d.]+)%', text)
    if m: metrics['profit_yoy_ttm'] = float(m.group(1))

    m = re.search(r'资产负债率[为]?([-\d.]+)%', text)
    if m: metrics['debt_ratio'] = float(m.group(1))

    return metrics


# ─── 美股数据提取 ─────────────────────────────────────────

def extract_us_stock_section(text: str, stock_code: str) -> Optional[str]:
    """从 NeoData 返回文本中提取美股代码对应的段落。"""
    # 匹配 "(代码:AAPL)在美股股票的行情：" 段落
    pattern = rf'{stock_code}\)在美股股票的行情：(.*?)(?=(?:\([^)]+\)在(?:A股|港股)股票的行情：)|$)'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1)
    return None


def parse_us_realtime_metrics(section: str) -> dict:
    """从美股行情段落中解析关键指标。"""
    metrics = {}

    m = re.search(r'数据更新时间[:\s]*(\S+)', section)
    if m: metrics['data_time'] = m.group(1)

    m = re.search(r'最新价格[:\s]*\$?([\d.]+)', section)
    if m: metrics['price'] = float(m.group(1))

    m = re.search(r'昨日收盘价格[:\s]*\$?([\d.]+)', section)
    if m: metrics['prev_close'] = float(m.group(1))

    m = re.search(r'当日涨跌幅[:\s]*([-\d.]+)%', section)
    if m: metrics['change_pct'] = float(m.group(1))

    m = re.search(r'市盈率\(TTM\)[:\s]*([\d.]+)', section)
    if m: metrics['pe_ttm'] = float(m.group(1))

    m = re.search(r'市净率[:\s]*([\d.]+)', section)
    if m: metrics['pb'] = float(m.group(1))

    # 美股市值可能是美元或百万美元
    m = re.search(r'总市值\(百万美元\)[:\s]*([\d,.]+)', section)
    if m: metrics['market_cap_m_usd'] = float(m.group(1).replace(',', ''))

    m = re.search(r'总市值\(亿美元\)[:\s]*([\d,.]+)', section)
    if m: metrics['market_cap_yi_usd'] = float(m.group(1).replace(',', ''))

    m = re.search(r'总市值[:\s]*\$?([\d,.]+)', section)
    if m and 'market_cap_m_usd' not in metrics and 'market_cap_yi_usd' not in metrics:
        metrics['market_cap_raw'] = float(m.group(1).replace(',', ''))

    return metrics


def parse_us_fina_indicator_data(data: dict) -> dict:
    """从 finance-data-retrieval us_fina_indicator API返回中解析美股财务指标。"""
    metrics = {}
    fields = data.get('data', {}).get('fields', [])
    items = data.get('data', {}).get('items', [])

    if not items:
        return metrics

    # 取最新一期数据
    item = items[0]
    field_map = {f: i for i, f in enumerate(fields)}

    def get_val(field_name):
        if field_name in field_map:
            try:
                val = item[field_map[field_name]]
                return float(val) if val is not None else None
            except (ValueError, TypeError, IndexError):
                return None
        return None

    metrics['operate_income'] = get_val('operate_income')
    metrics['operate_income_yoy'] = get_val('operate_income_yoy')
    metrics['parent_holder_netprofit'] = get_val('parent_holder_netprofit')
    metrics['parent_holder_netprofit_yoy'] = get_val('parent_holder_netprofit_yoy')
    metrics['basic_eps'] = get_val('basic_eps')
    metrics['diluted_eps'] = get_val('diluted_eps')
    metrics['gross_profit_ratio'] = get_val('gross_profit_ratio')
    metrics['net_profit_ratio'] = get_val('net_profit_ratio')
    metrics['roe_avg'] = get_val('roe_avg')
    metrics['roa'] = get_val('roa')
    metrics['current_ratio'] = get_val('current_ratio')
    metrics['debt_asset_ratio'] = get_val('debt_asset_ratio')
    metrics['equity_ratio'] = get_val('equity_ratio')

    # 提取日期和名称
    if 'end_date' in field_map:
        try:
            metrics['end_date'] = str(item[field_map['end_date']])
        except (IndexError, TypeError):
            pass
    if 'ind_type' in field_map:
        try:
            metrics['ind_type'] = str(item[field_map['ind_type']])
        except (IndexError, TypeError):
            pass
    if 'security_name_abbr' in field_map:
        try:
            metrics['security_name_abbr'] = str(item[field_map['security_name_abbr']])
        except (IndexError, TypeError):
            pass
    if 'currency_abbr' in field_map:
        try:
            metrics['currency'] = str(item[field_map['currency_abbr']])
        except (IndexError, TypeError):
            pass

    return metrics


def parse_us_daily_data(data: dict) -> dict:
    """从 finance-data-retrieval us_daily API返回中解析美股日线数据。"""
    metrics = {}
    fields = data.get('data', {}).get('fields', [])
    items = data.get('data', {}).get('items', [])

    if not items:
        return metrics

    # 取最新一条
    item = items[0]
    field_map = {f: i for i, f in enumerate(fields)}

    def get_val(field_name):
        if field_name in field_map:
            try:
                val = item[field_map[field_name]]
                return float(val) if val is not None else None
            except (ValueError, TypeError, IndexError):
                return None
        return None

    metrics['trade_date'] = get_val('trade_date')
    metrics['close'] = get_val('close')
    metrics['open'] = get_val('open')
    metrics['high'] = get_val('high')
    metrics['low'] = get_val('low')
    metrics['pre_close'] = get_val('pre_close')
    metrics['pct_change'] = get_val('pct_change')
    metrics['vol'] = get_val('vol')
    metrics['amount'] = get_val('amount')
    metrics['pe'] = get_val('pe')
    metrics['pb'] = get_val('pb')
    metrics['total_mv'] = get_val('total_mv')
    metrics['turnover_ratio'] = get_val('turnover_ratio')

    # 转换整型字段
    for key in ['trade_date']:
        if key in metrics and metrics[key] is not None:
            metrics[key] = str(int(metrics[key]))

    return metrics


# ─── 港股数据提取 ─────────────────────────────────────────

def extract_hk_stock_section(text: str, stock_code: str) -> Optional[str]:
    """从 NeoData 返回文本中提取港股代码对应的段落。"""
    pattern = rf'{stock_code}\)在港股股票的行情：(.*?)(?=(?:\([^)]+\)在(?:A股|美股)股票的行情：)|$)'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1)
    return None


def parse_hk_realtime_metrics(section: str) -> dict:
    """从港股行情段落中解析关键指标。"""
    metrics = {}

    m = re.search(r'数据更新时间[:\s]*(\S+)', section)
    if m: metrics['data_time'] = m.group(1)

    m = re.search(r'最新价格[:\s]*([\d.]+)港元', section)
    if m: metrics['price'] = float(m.group(1))

    m = re.search(r'最新价格[:\s]*([\d.]+)', section)
    if m and 'price' not in metrics: metrics['price'] = float(m.group(1))

    m = re.search(r'昨日收盘价格[:\s]*([\d.]+)港元', section)
    if m: metrics['prev_close'] = float(m.group(1))

    m = re.search(r'当日涨跌幅[:\s]*([-\d.]+)%', section)
    if m: metrics['change_pct'] = float(m.group(1))

    m = re.search(r'市盈率\(TTM\)[:\s]*([\d.]+)', section)
    if m: metrics['pe_ttm'] = float(m.group(1))

    m = re.search(r'市净率[:\s]*([\d.]+)', section)
    if m: metrics['pb'] = float(m.group(1))

    m = re.search(r'股息率[:\s]*([\d.]+)', section)
    if m: metrics['dividend_yield'] = float(m.group(1))

    m = re.search(r'总市值\(亿港元\)[:\s]*([\d,.]+)', section)
    if m: metrics['market_cap_yi_hkd'] = float(m.group(1).replace(',', ''))

    m = re.search(r'总市值\(百万港元\)[:\s]*([\d,.]+)', section)
    if m: metrics['market_cap_m_hkd'] = float(m.group(1).replace(',', ''))

    m = re.search(r'换手率[:\s]*([\d.]+)%', section)
    if m: metrics['turnover_rate'] = float(m.group(1))

    return metrics


def parse_hk_fundamental_metrics(text: str) -> dict:
    """从港股基本面/估值段落中提取指标。"""
    metrics = {}

    m = re.search(r'净资产收益率TTM为([-\d.]+)%', text)
    if m: metrics['roe_ttm'] = float(m.group(1))

    m = re.search(r'销售净利率TTM为([-\d.]+)%', text)
    if m: metrics['net_margin_ttm'] = float(m.group(1))

    m = re.search(r'销售毛利率TTM为([-\d.]+)%', text)
    if m: metrics['gross_margin_ttm'] = float(m.group(1))

    m = re.search(r'营业收入同比增长率TTM为([-\d.]+)%', text)
    if m: metrics['revenue_yoy_ttm'] = float(m.group(1))

    m = re.search(r'净利润增长率TTM为([-\d.]+)%', text)
    if m: metrics['profit_yoy_ttm'] = float(m.group(1))

    m = re.search(r'资产负债率[为]?([-\d.]+)%', text)
    if m: metrics['debt_ratio'] = float(m.group(1))

    return metrics


def parse_hk_daily_data(data: dict) -> dict:
    """从 finance-data-retrieval hk_daily API返回中解析港股日线数据。"""
    metrics = {}
    fields = data.get('data', {}).get('fields', [])
    items = data.get('data', {}).get('items', [])

    if not items:
        return metrics

    item = items[0]
    field_map = {f: i for i, f in enumerate(fields)}

    def get_val(field_name):
        if field_name in field_map:
            try:
                val = item[field_map[field_name]]
                return float(val) if val is not None else None
            except (ValueError, TypeError, IndexError):
                return None
        return None

    metrics['trade_date'] = get_val('trade_date')
    metrics['close'] = get_val('close')
    metrics['open'] = get_val('open')
    metrics['high'] = get_val('high')
    metrics['low'] = get_val('low')
    metrics['pre_close'] = get_val('pre_close')
    metrics['pct_chg'] = get_val('pct_chg')
    metrics['vol'] = get_val('vol')
    metrics['amount'] = get_val('amount')

    if metrics.get('trade_date'):
        metrics['trade_date'] = str(int(metrics['trade_date']))

    return metrics


# ─── 交叉校验 ─────────────────────────────────────────────

def cross_validate_a(metrics: dict) -> list:
    """A股交叉校验。"""
    warnings = []

    pe = metrics.get('pe_ttm')
    pb = metrics.get('pb')
    roe = metrics.get('roe_ttm')

    if pe and pb and roe and roe > 0:
        expected_pe = pb / (roe / 100)
        ratio = pe / expected_pe
        if abs(ratio - 1) > 0.25:
            warnings.append(
                f"⚠️ PE/PB/ROE 不一致: PE={pe}, PB={pb}, ROE={roe}%, "
                f"预期PE≈{expected_pe:.1f} (PB/ROE), 实际偏差{abs(ratio-1)*100:.0f}%"
            )

    price = metrics.get('price')
    market_cap = metrics.get('market_cap_yi')
    if price and market_cap:
        implied_shares = market_cap / price
        if implied_shares < 0.1 or implied_shares > 10000:
            warnings.append(
                f"⚠️ 市值/股价 不一致: 市值={market_cap}亿, 股价={price}元, "
                f"隐含总股本={implied_shares:.1f}亿股 (异常)"
            )

    return warnings


def cross_validate_us(metrics: dict) -> list:
    """美股交叉校验。"""
    warnings = []

    pe = metrics.get('pe_ttm')
    pb = metrics.get('pb')
    roe = metrics.get('roe_avg')

    # 美股ROE可能极高（如回购导致净资产为负时ROE>100%）
    if pe and pb and roe and roe > 0:
        expected_pe = pb / (roe / 100)
        ratio = pe / expected_pe
        # 美股由于回购等因素，PE/PB/ROE关系可能偏差更大
        if abs(ratio - 1) > 0.40:
            warnings.append(
                f"⚠️ PE/PB/ROE 不一致: PE={pe}, PB={pb}, ROE={roe}%, "
                f"预期PE≈{expected_pe:.1f}, 偏差{abs(ratio-1)*100:.0f}% "
                f"(注意：美股大量回购可能导致ROE失真)"
            )

    # 检查净资产为负的情况
    if pb and pb < 0:
        warnings.append(
            f"⚠️ PB为负({pb})：净资产为负，PE/PB估值可能失真，建议改用EV/EBITDA"
        )

    if roe and roe > 100:
        warnings.append(
            f"⚠️ ROE异常高({roe}%)：可能因大量回购导致净资产极低，需结合净利润绝对值分析"
        )

    return warnings


def cross_validate_hk(metrics: dict) -> list:
    """港股交叉校验。"""
    warnings = []

    pe = metrics.get('pe_ttm')
    pb = metrics.get('pb')
    roe = metrics.get('roe_ttm')

    if pe and pb and roe and roe > 0:
        expected_pe = pb / (roe / 100)
        ratio = pe / expected_pe
        if abs(ratio - 1) > 0.30:
            warnings.append(
                f"⚠️ PE/PB/ROE 不一致: PE={pe}, PB={pb}, ROE={roe}%, "
                f"预期PE≈{expected_pe:.1f}, 偏差{abs(ratio-1)*100:.0f}%"
            )

    return warnings


# ─── 主逻辑 ─────────────────────────────────────────────

def process_neodata_a(raw_data: dict, stock_code: str) -> dict:
    """处理A股 NeoData数据。"""
    result = {
        'stock_code': stock_code,
        'market': 'A',
        'currency': 'CNY',
        'realtime': {},
        'fundamentals': {},
        'warnings': [],
    }

    api_data = raw_data.get('data', {}).get('apiData', {})
    recalls = api_data.get('apiRecall', [])

    if not recalls:
        result['warnings'].append('❌ 未找到任何 apiRecall 数据')
        return result

    for recall in recalls:
        content = recall.get('content', '')
        recall_type = recall.get('type', '')

        # 提取 A 股行情段落
        section = extract_a_stock_section(content, stock_code)
        if section:
            if recall_type == '股票实时行情':
                result['realtime'] = parse_a_realtime_metrics(section)

        # 从估值/基本面段落提取
        if stock_code.replace('.', '') in content or any(
            keyword in content for keyword in [f'代码：{stock_code}', f'代码:{stock_code}']
        ):
            if recall_type in ('估值数据与基本面分析', '财务主要复合指标'):
                fund_metrics = parse_a_fundamental_metrics(content)
                result['fundamentals'].update(fund_metrics)

    # 交叉校验
    all_metrics = {**result['realtime'], **result['fundamentals']}
    result['warnings'].extend(cross_validate_a(all_metrics))

    return result


def process_neodata_us(raw_data: dict, stock_code: str) -> dict:
    """处理美股 NeoData数据。"""
    result = {
        'stock_code': stock_code,
        'market': 'US',
        'currency': 'USD',
        'realtime': {},
        'fundamentals': {},
        'warnings': [],
    }

    api_data = raw_data.get('data', {}).get('apiData', {})
    recalls = api_data.get('apiRecall', [])

    if not recalls:
        result['warnings'].append('❌ 未找到任何 apiRecall 数据')
        return result

    for recall in recalls:
        content = recall.get('content', '')
        recall_type = recall.get('type', '')

        # 提取美股行情段落
        section = extract_us_stock_section(content, stock_code)
        if section:
            if recall_type == '股票实时行情':
                result['realtime'] = parse_us_realtime_metrics(section)

        # 美股基本面段落
        if stock_code in content:
            if recall_type in ('估值数据与基本面分析', '财务主要复合指标', '美股基本面'):
                fund_metrics = {}
                # 美股基本面指标提取
                m = re.search(r'净资产收益率[TTM]*[为]?([-\d.]+)%', content)
                if m: fund_metrics['roe_ttm'] = float(m.group(1))
                m = re.search(r'销售净利率[TTM]*[为]?([-\d.]+)%', content)
                if m: fund_metrics['net_margin_ttm'] = float(m.group(1))
                m = re.search(r'销售毛利率[TTM]*[为]?([-\d.]+)%', content)
                if m: fund_metrics['gross_margin_ttm'] = float(m.group(1))
                m = re.search(r'资产负债率[为]?([-\d.]+)%', content)
                if m: fund_metrics['debt_ratio'] = float(m.group(1))

                result['fundamentals'].update(fund_metrics)

    # 交叉校验
    all_metrics = {**result['realtime'], **result['fundamentals']}
    result['warnings'].extend(cross_validate_us(all_metrics))

    return result


def process_neodata_hk(raw_data: dict, stock_code: str) -> dict:
    """处理港股 NeoData数据。"""
    result = {
        'stock_code': stock_code,
        'market': 'HK',
        'currency': 'HKD',
        'realtime': {},
        'fundamentals': {},
        'warnings': [],
    }

    api_data = raw_data.get('data', {}).get('apiData', {})
    recalls = api_data.get('apiRecall', [])

    if not recalls:
        result['warnings'].append('❌ 未找到任何 apiRecall 数据')
        return result

    for recall in recalls:
        content = recall.get('content', '')
        recall_type = recall.get('type', '')

        # 提取港股行情段落
        section = extract_hk_stock_section(content, stock_code)
        if section:
            if recall_type == '股票实时行情':
                result['realtime'] = parse_hk_realtime_metrics(section)

        # 港股基本面段落
        if stock_code.replace('.', '') in content or any(
            keyword in content for keyword in [f'代码：{stock_code}', f'代码:{stock_code}']
        ):
            if recall_type in ('估值数据与基本面分析', '财务主要复合指标', '港股基本面'):
                fund_metrics = parse_hk_fundamental_metrics(content)
                result['fundamentals'].update(fund_metrics)

    # 交叉校验
    all_metrics = {**result['realtime'], **result['fundamentals']}
    result['warnings'].extend(cross_validate_hk(all_metrics))

    return result


def main():
    parser = argparse.ArgumentParser(description='结构化提取股票数据，支持A股/美股/港股')
    parser.add_argument('input_path', help='输入JSON文件路径，或 "-" 从stdin读取')
    parser.add_argument('stock_code', help='股票代码 (如 002028.SZ / AAPL / 00700.HK)')
    parser.add_argument('--market', choices=['A', 'US', 'HK', 'auto'], default='auto',
                        help='市场类型 (默认自动检测)')

    args = parser.parse_args()

    stock_code = args.stock_code.upper()

    # 市场识别
    if args.market == 'auto':
        market = detect_market(stock_code)
    else:
        market = args.market

    if market == 'UNKNOWN':
        print(f"❌ 无法识别市场类型: {stock_code}，请使用 --market 指定", file=sys.stderr)
        sys.exit(1)

    # A股代码标准化
    if market == 'A':
        stock_code = normalize_a_stock_code(stock_code)

    # 读取输入
    if args.input_path == '-':
        raw = sys.stdin.read()
    else:
        with open(args.input_path, 'r') as f:
            raw = f.read()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        print("❌ 输入不是有效的 JSON", file=sys.stderr)
        sys.exit(1)

    # 按市场分发处理
    if market == 'A':
        result = process_neodata_a(data, stock_code)
    elif market == 'US':
        result = process_neodata_us(data, stock_code)
    elif market == 'HK':
        result = process_neodata_hk(data, stock_code)

    # 检查是否找到了目标股票
    if not result['realtime'] and not result['fundamentals']:
        print(f"❌ 未在返回数据中找到 {stock_code} 的 {market} 市场数据", file=sys.stderr)
        sys.exit(1)

    # 输出
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 有警告时输出到 stderr
    if result['warnings']:
        print("\n--- 校验警告 ---", file=sys.stderr)
        for w in result['warnings']:
            print(w, file=sys.stderr)


if __name__ == "__main__":
    main()
