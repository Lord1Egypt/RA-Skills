#!/usr/bin/env python3
"""
Tushare Pro 金融数据助手 - 增强版
支持错误处理、重试、Token验证
"""

import os
import time
from functools import wraps


def retry(max_retries=3, delay=2, backoff=2):
    """重试装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            current_delay = delay
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries == max_retries:
                        raise Exception(f"{func.__name__} 失败 (重试{max_retries}次): {e}")
                    print(f"[重试] {func.__name__} 失败，{current_delay}秒后重试 ({retries}/{max_retries})...")
                    time.sleep(current_delay)
                    current_delay *= backoff
            return None
        return wrapper
    return decorator


def get_tushare_api():
    """获取 Tushare API 实例"""
    try:
        import tushare as ts
    except ImportError:
        raise Exception("请安装 tushare: pip install tushare pandas")
    
    token = os.environ.get('TUSHARE_TOKEN')
    if not token:
        raise Exception("请设置 TUSHARE_TOKEN 环境变量")
    
    return ts.pro_api(token)


@retry(max_retries=3, delay=2)
def get_stock_basic(ts_code=None, industry=None, list_status='L'):
    """获取股票列表"""
    pro = get_tushare_api()
    params = {'list_status': list_status}
    if ts_code:
        params['ts_code'] = ts_code
    if industry:
        params['industry'] = industry
    return pro.stock_basic(**params)


@retry(max_retries=3, delay=2)
def get_daily(ts_code, start_date=None, end_date=None):
    """获取日线行情"""
    pro = get_tushare_api()
    params = {'ts_code': ts_code}
    if start_date:
        params['start_date'] = start_date
    if end_date:
        params['end_date'] = end_date
    return pro.daily(**params)


@retry(max_retries=3, delay=2)
def get_weekly(ts_code, start_date=None, end_date=None):
    """获取周线行情"""
    pro = get_tushare_api()
    params = {'ts_code': ts_code}
    if start_date:
        params['start_date'] = start_date
    if end_date:
        params['end_date'] = end_date
    return pro.weekly(**params)


@retry(max_retries=3, delay=2)
def get_monthly(ts_code, start_date=None, end_date=None):
    """获取月线行情"""
    pro = get_tushare_api()
    params = {'ts_code': ts_code}
    if start_date:
        params['start_date'] = start_date
    if end_date:
        params['end_date'] = end_date
    return pro.monthly(**params)


@retry(max_retries=3, delay=2)
def get_financial_indicator(ts_code, period=None):
    """获取财务指标"""
    pro = get_tushare_api()
    params = {'ts_code': ts_code}
    if period:
        params['period'] = period
    return pro.fina_indicator(**params)


@retry(max_retries=3, delay=2)
def get_income(ts_code, period=None):
    """获取利润表"""
    pro = get_tushare_api()
    params = {'ts_code': ts_code}
    if period:
        params['period'] = period
    return pro.income(**params)


@retry(max_retries=3, delay=2)
def get_balancesheet(ts_code, period=None):
    """获取资产负债表"""
    pro = get_tushare_api()
    params = {'ts_code': ts_code}
    if period:
        params['period'] = period
    return pro.balancesheet(**params)


@retry(max_retries=3, delay=2)
def get_cashflow(ts_code, period=None):
    """获取现金流量表"""
    pro = get_tushare_api()
    params = {'ts_code': ts_code}
    if period:
        params['period'] = period
    return pro.cashflow(**params)


@retry(max_retries=3, delay=2)
def get_index_daily(ts_code, start_date=None, end_date=None):
    """获取指数日线"""
    pro = get_tushare_api()
    params = {'ts_code': ts_code}
    if start_date:
        params['start_date'] = start_date
    if end_date:
        params['end_date'] = end_date
    return pro.index_daily(**params)


@retry(max_retries=3, delay=2)
def get_gdp():
    """获取GDP数据"""
    pro = get_tushare_api()
    return pro.gdp()


@retry(max_retries=3, delay=2)
def get_cpi():
    """获取CPI数据"""
    pro = get_tushare_api()
    return pro.cpi()


@retry(max_retries=3, delay=2)
def get_pmi():
    """获取PMI数据"""
    pro = get_tushare_api()
    return pro.pmi()


@retry(max_retries=3, delay=2)
def get_m2():
    """获取货币供应量"""
    pro = get_tushare_api()
    return pro.m2()


def generate_financial_report(ts_code):
    """生成完整财务报表"""
    report = {}
    
    # 基本信息
    try:
        info = get_stock_basic(ts_code=ts_code)
        report['info'] = info.iloc[0].to_dict() if not info.empty else {}
    except Exception as e:
        report['info'] = {'error': str(e)}
    
    # 财务指标
    try:
        indicator = get_financial_indicator(ts_code, period='20231231')
        report['indicator'] = indicator.iloc[0].to_dict() if not indicator.empty else {}
    except Exception as e:
        report['indicator'] = {'error': str(e)}
    
    # 利润表
    try:
        income = get_income(ts_code, period='20231231')
        report['income'] = income.iloc[0].to_dict() if not income.empty else {}
    except Exception as e:
        report['income'] = {'error': str(e)}
    
    # 资产负债表
    try:
        balance = get_balancesheet(ts_code, period='20231231')
        report['balance'] = balance.iloc[0].to_dict() if not balance.empty else {}
    except Exception as e:
        report['balance'] = {'error': str(e)}
    
    return report


def dcf_valuation(ts_code, growth_rate=0.15, wacc=0.1, terminal_growth=0.03):
    """DCF 估值模型"""
    income = get_income(ts_code)
    
    if income.empty:
        return None
    
    latest = income.iloc[0]
    base_revenue = latest.get('revenue', 0)
    net_profit = latest.get('net_profit', 0)
    net_margin = net_profit / base_revenue if base_revenue > 0 else 0
    
    # 预测未来5年现金流
    cash_flows = []
    for year in range(1, 6):
        revenue = base_revenue * (1 + growth_rate) ** year
        profit = revenue * net_margin
        cash_flows.append(profit)
    
    # 终值
    terminal_value = cash_flows[-1] * (1 + terminal_growth) / (wacc - terminal_growth)
    
    # 折现
    pv_sum = sum(cf / (1 + wacc) ** i for i, cf in enumerate(cash_flows, 1))
    pv_terminal = terminal_value / (1 + wacc) ** 5
    
    total_value = pv_sum + pv_terminal
    
    return {
        '公司价值': total_value,
        '现金流预测': cash_flows,
        '终值': terminal_value,
        '假设条件': {
            '增长率': growth_rate,
            'WACC': wacc,
            '永续增长率': terminal_growth,
            '净利率': net_margin
        }
    }


if __name__ == "__main__":
    # 测试
    print("=== Tushare Pro 测试 ===")
    
    # 验证 Token
    token = os.environ.get('TUSHARE_TOKEN')
    if token:
        print(f"Token: {token[:10]}...")
    else:
        print("未设置 TUSHARE_TOKEN")
    
    # 测试获取股票列表
    try:
        df = get_stock_basic(list_status='L')
        print(f"获取到 {len(df)} 只股票")
        print(df[['ts_code', 'name', 'industry']].head(3))
    except Exception as e:
        print(f"获取股票列表失败: {e}")
