#!/usr/bin/env python3
import sys
import json
import akshare as ak

# 检查 Python 版本
if sys.version_info < (3, 11):
    print(json.dumps({'error': f'需要 Python 3.11 或更高版本，当前版本: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}'}))
    sys.exit(1)

# 获取行情数据
def fetch_market_data(symbol, period='1d', start_date=None, end_date=None):
    try:
        data = ak.stock_zh_a_hist(
            symbol=symbol,
            period='daily' if period == '1d' else 'weekly' if period == '1w' else 'monthly' if period == '1M' else 'daily',
            start_date=start_date,
            end_date=end_date
        )
        
        items = []
        for _, row in data.iterrows():
            items.append({
                'date': row['日期'],
                'open': float(row['开盘']),
                'high': float(row['最高']),
                'low': float(row['最低']),
                'close': float(row['收盘']),
                'volume': float(row['成交量']),
                'amount': float(row['成交额']),
                'change': float(row['涨跌额']),
                'change_percent': float(row['涨跌幅']),
                'turnover': float(row['换手率'])
            })
        
        return {
            'symbol': symbol,
            'period': period,
            'items': items
        }
    except Exception as e:
        raise Exception(f'获取行情数据失败: {str(e)}')

# 获取财务数据
def fetch_finance_data(symbol, report_type='quarter'):
    try:
        data = ak.stock_financial_analysis_indicator(symbol=symbol)
        
        items = []
        for _, row in data.iterrows():
            items.append({
                'report_date': row['日期'],
                'revenue': float(row.get('营业收入(元)', 0) or 0),
                'gross_profit': float(row.get('营业利润(元)', 0) or 0),
                'net_profit': float(row.get('净利润(元)', 0) or 0),
                'eps': float(row.get('每股收益(元)', 0) or 0),
                'roe': float(row.get('净资产收益率(%)', 0) or 0),
                'asset_liability_ratio': float(row.get('资产负债率(%)', 0) or 0),
                'operating_cash_flow': float(row.get('经营活动产生的现金流量净额(元)', 0) or 0)
            })
        
        return {
            'symbol': symbol,
            'report_type': report_type,
            'items': items
        }
    except Exception as e:
        raise Exception(f'获取财务数据失败: {str(e)}')

# 获取资金流向数据
def fetch_fund_flow_data(symbol):
    try:
        # 判断市场类型
        market = 'sh' if symbol.startswith('6') else 'sz'
        data = ak.stock_individual_fund_flow(stock=symbol, market=market)
        
        items = []
        for _, row in data.iterrows():
            # 处理日期格式
            date_value = row['日期']
            if hasattr(date_value, 'strftime'):
                date_str = date_value.strftime('%Y-%m-%d')
            else:
                date_str = str(date_value)
            
            items.append({
                'date': date_str,
                'main_inflow': float(row.get('主力净流入-净额(万元)', 0) or 0),
                'main_inflow_rate': float(row.get('主力净流入-净占比(%)', 0) or 0),
                '超大_inflow': float(row.get('超大单净流入-净额(万元)', 0) or 0),
                '超大_inflow_rate': float(row.get('超大单净流入-净占比(%)', 0) or 0),
                'large_inflow': float(row.get('大单净流入-净额(万元)', 0) or 0),
                'large_inflow_rate': float(row.get('大单净流入-净占比(%)', 0) or 0),
                'medium_inflow': float(row.get('中单净流入-净额(万元)', 0) or 0),
                'medium_inflow_rate': float(row.get('中单净流入-净占比(%)', 0) or 0),
                'small_inflow': float(row.get('小单净流入-净额(万元)', 0) or 0),
                'small_inflow_rate': float(row.get('小单净流入-净占比(%)', 0) or 0)
            })
        
        return {
            'symbol': symbol,
            'items': items
        }
    except Exception as e:
        raise Exception(f'获取资金流向数据失败: {str(e)}')

# 获取舆情数据
def fetch_public_opinion_data(symbol):
    try:
        # 这里使用模拟数据，实际项目中可能需要调用相关API
        mock_data = [
            {
                'date': '2024-01-01',
                'source': '东方财富网',
                'title': f'{symbol}公司发布2024年第一季度财报，净利润同比增长20%',
                'sentiment': 'positive',
                'url': f'https://www.eastmoney.com/{symbol}'
            },
            {
                'date': '2024-01-02',
                'source': '同花顺',
                'title': f'{symbol}股价今日上涨5%，创近期新高',
                'sentiment': 'positive',
                'url': f'https://www.10jqka.com.cn/{symbol}'
            },
            {
                'date': '2024-01-03',
                'source': '新浪财经',
                'title': f'{symbol}公司拟投资10亿元扩大生产规模',
                'sentiment': 'positive',
                'url': f'https://finance.sina.com.cn/{symbol}'
            }
        ]
        
        return {
            'symbol': symbol,
            'items': mock_data
        }
    except Exception as e:
        raise Exception(f'获取舆情数据失败: {str(e)}')

if __name__ == '__main__':
    try:
        if len(sys.argv) < 2:
            print(json.dumps({'error': '缺少参数'}))
            sys.exit(1)
        
        action = sys.argv[1]
        
        # 从 stdin 读取参数
        input_data = sys.stdin.read()
        params = json.loads(input_data) if input_data else {}
        
        if action == 'market':
            result = fetch_market_data(
                params.get('symbol'),
                params.get('period', '1d'),
                params.get('start_date'),
                params.get('end_date')
            )
        elif action == 'finance':
            result = fetch_finance_data(
                params.get('symbol'),
                params.get('report_type', 'quarter')
            )
        elif action == 'fund_flow':
            result = fetch_fund_flow_data(params.get('symbol'))
        elif action == 'public_opinion':
            result = fetch_public_opinion_data(params.get('symbol'))
        else:
            print(json.dumps({'error': '未知的操作类型'}))
            sys.exit(1)
        
        print(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({'error': str(e)}))
        sys.exit(1)
