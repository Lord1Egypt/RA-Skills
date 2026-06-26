#!/usr/bin/env python3
import sys
import json
import time
import akshare as ak
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

sys.path.insert(0, __file__.rsplit('\\', 1)[0] if '\\' in __file__ else __file__.rsplit('/', 1)[0])
from fetch_status import read_status, write_status, calculate_date_range, update_fetch_time
from data_storage import save_market_data, save_north_flow_data, save_lhb_data, save_sentiment_data, save_financial_data

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

# 获取所有A股股票代码
def fetch_all_stock_codes():
    try:
        data = ak.stock_info_a_code_name()
        
        items = []
        for _, row in data.iterrows():
            items.append({
                'code': row['code'],
                'name': row['name']
            })
        
        return {
            'items': items,
            'total': len(items)
        }
    except Exception as e:
        raise Exception(f'获取股票代码失败: {str(e)}')


def batch_fetch_financial_data(
    status_file: str = 'config/fetch_status.json',
    data_path: str = 'data/financial',
    default_years: int = 3,
    max_retries: int = 3,
    progress_interval: int = 100
) -> Dict[str, Any]:
    start_time = time.time()
    stats = {
        'total_stocks': 0,
        'success_count': 0,
        'failed_count': 0,
        'skipped_count': 0,
        'total_records': 0,
        'failed_stocks': [],
        'is_incremental': False
    }
    
    status = read_status(status_file)
    date_range = calculate_date_range(status, 'financial', default_years)
    stats['is_incremental'] = date_range.get('is_incremental', False)
    
    try:
        stock_codes_data = fetch_all_stock_codes()
        stock_codes = [item['code'] for item in stock_codes_data['items']]
        stats['total_stocks'] = len(stock_codes)
    except Exception as e:
        raise Exception(f'获取股票代码列表失败: {str(e)}')
    
    for idx, symbol in enumerate(stock_codes, 1):
        retry_count = 0
        success = False
        
        while retry_count < max_retries and not success:
            try:
                data = ak.stock_financial_abstract_ths(symbol=symbol, indicator='按报告期')
                
                if data is not None and not data.empty:
                    items = []
                    for _, row in data.iterrows():
                        report_date = row.get('报告期')
                        if report_date is None:
                            continue
                        
                        def parse_value(val):
                            if val is None or str(val) in ['nan', 'None', '', '--']:
                                return 0.0
                            try:
                                val_str = str(val).replace('%', '').replace(',', '')
                                return float(val_str)
                            except (ValueError, TypeError):
                                return 0.0
                        
                        item = {
                            'report_date': str(report_date),
                            'net_profit': parse_value(row.get('净利润')),
                            'revenue': parse_value(row.get('营业总收入')),
                            'eps': parse_value(row.get('基本每股收益')),
                            'roe': parse_value(row.get('净资产收益率')),
                            'asset_liability_ratio': parse_value(row.get('资产负债率')),
                            'operating_profit': parse_value(row.get('营业利润')),
                            'operating_cash_flow': parse_value(row.get('经营活动净现金流量'))
                        }
                        items.append(item)
                    
                    if items:
                        financial_data = {
                            'symbol': symbol,
                            'items': items
                        }
                        
                        save_financial_data(financial_data, data_path)
                        stats['success_count'] += 1
                        stats['total_records'] += len(items)
                    else:
                        stats['skipped_count'] += 1
                    success = True
                else:
                    stats['skipped_count'] += 1
                    success = True
            except Exception as e:
                retry_count += 1
                if retry_count >= max_retries:
                    stats['failed_count'] += 1
                    stats['failed_stocks'].append({
                        'symbol': symbol,
                        'error': str(e)
                    })
                    success = True
                else:
                    time.sleep(2)
        
        if idx % progress_interval == 0:
            elapsed = time.time() - start_time
            progress_pct = (idx / stats['total_stocks']) * 100
            print(json.dumps({
                'progress': {
                    'current': idx,
                    'total': stats['total_stocks'],
                    'percentage': round(progress_pct, 2),
                    'success': stats['success_count'],
                    'failed': stats['failed_count'],
                    'elapsed_seconds': round(elapsed, 2)
                }
            }), file=sys.stderr)
        
        time.sleep(0.5)
    
    fetch_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status = update_fetch_time(status, 'financial', fetch_time, stats['success_count'])
    write_status(status_file, status)
    
    elapsed_time = time.time() - start_time
    stats['elapsed_seconds'] = round(elapsed_time, 2)
    
    return stats


def batch_fetch_market_data(
    status_file: str = 'config/fetch_status.json',
    data_path: str = 'data/market',
    default_years: int = 5,
    max_retries: int = 3,
    progress_interval: int = 100
) -> Dict[str, Any]:
    start_time = time.time()
    stats = {
        'total_stocks': 0,
        'success_count': 0,
        'failed_count': 0,
        'skipped_count': 0,
        'total_records': 0,
        'failed_stocks': [],
        'is_incremental': False,
        'date_range': {}
    }
    
    try:
        status = read_status(status_file)
        date_range = calculate_date_range(status, 'market', default_years)
        stats['date_range'] = date_range
        stats['is_incremental'] = date_range.get('is_incremental', False)
        
        start_date = date_range['start_date']
        end_date = date_range['end_date']
        
        stocks_data = fetch_all_stock_codes()
        stock_list = stocks_data['items']
        stats['total_stocks'] = len(stock_list)
        
        if stats['total_stocks'] == 0:
            raise Exception('未获取到任何股票代码')
        
        print(json.dumps({
            'type': 'progress',
            'message': f'开始批量拉取，共 {stats["total_stocks"]} 只股票',
            'date_range': date_range
        }, ensure_ascii=False), flush=True)
        
        for idx, stock in enumerate(stock_list, 1):
            symbol = stock['code']
            retry_count = 0
            success = False
            
            while retry_count < max_retries and not success:
                try:
                    market_data = fetch_market_data(
                        symbol=symbol,
                        period='1d',
                        start_date=start_date,
                        end_date=end_date
                    )
                    
                    if market_data and market_data.get('items'):
                        items = market_data['items']
                        for item in items:
                            item['symbol'] = symbol
                        
                        save_market_data(items, data_path)
                        stats['total_records'] += len(items)
                    
                    stats['success_count'] += 1
                    success = True
                    
                except Exception as e:
                    retry_count += 1
                    if retry_count >= max_retries:
                        stats['failed_count'] += 1
                        stats['failed_stocks'].append({
                            'code': symbol,
                            'name': stock.get('name', ''),
                            'error': str(e)
                        })
                    else:
                        time.sleep(0.5)
            
            if idx % progress_interval == 0:
                elapsed = time.time() - start_time
                progress_pct = (idx / stats['total_stocks']) * 100
                print(json.dumps({
                    'type': 'progress',
                    'message': f'进度: {idx}/{stats["total_stocks"]} ({progress_pct:.1f}%)',
                    'success': stats['success_count'],
                    'failed': stats['failed_count'],
                    'elapsed_seconds': round(elapsed, 1)
                }, ensure_ascii=False), flush=True)
            
            time.sleep(0.1)
        
        fetch_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = update_fetch_time(status, 'market', fetch_time, stats['success_count'])
        write_status(status_file, status)
        
        elapsed_time = time.time() - start_time
        stats['elapsed_seconds'] = round(elapsed_time, 2)
        
        return {
            'success': True,
            'stats': stats,
            'message': f'批量拉取完成，成功 {stats["success_count"]} 只，失败 {stats["failed_count"]} 只'
        }
        
    except Exception as e:
        return {
            'success': False,
            'stats': stats,
            'error': str(e),
            'message': f'批量拉取失败: {str(e)}'
        }


def batch_fetch_lhb_data(status_file: str = 'config/fetch_status.json', data_path: str = 'data/lhb'):
    try:
        status = read_status(status_file)
        date_range = calculate_date_range(status, 'lhb', default_years=3)
        
        start_date = date_range['start_date']
        end_date = date_range['end_date']
        is_incremental = date_range['is_incremental']
        
        start_dt = datetime.strptime(start_date, '%Y%m%d')
        end_dt = datetime.strptime(end_date, '%Y%m%d')
        
        all_items = []
        current_dt = start_dt
        success_days = 0
        failed_days = 0
        
        while current_dt <= end_dt:
            date_str = current_dt.strftime('%Y%m%d')
            try:
                data = ak.stock_lhb_detail_em(start_date=date_str, end_date=date_str)
                
                if data is not None and not data.empty:
                    items = []
                    for _, row in data.iterrows():
                        items.append({
                            'date': current_dt.strftime('%Y-%m-%d'),
                            'symbol': str(row.get('代码', '')),
                            'name': str(row.get('名称', '')),
                            'close_price': float(row.get('收盘价', 0) or 0),
                            'change_percent': float(row.get('涨跌幅', 0) or 0),
                            'turnover_rate': float(row.get('换手率', 0) or 0),
                            'net_buy': float(row.get('龙虎榜净买额', 0) or 0),
                            'total_buy': float(row.get('龙虎榜买入额', 0) or 0),
                            'total_sell': float(row.get('龙虎榜卖出额', 0) or 0),
                            'total_amount': float(row.get('龙虎榜成交额', 0) or 0),
                            'market_amount': float(row.get('市场总成交额', 0) or 0),
                            'reason': str(row.get('上榜原因', ''))
                        })
                    
                    if items:
                        all_items.extend(items)
                        success_days += 1
            except Exception as e:
                failed_days += 1
            
            current_dt += timedelta(days=1)
        
        saved_files = []
        if all_items:
            saved_files = save_lhb_data(all_items, data_path)
        
        fetch_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = update_fetch_time(status, 'lhb', fetch_time, len(all_items))
        write_status(status_file, status)
        
        return {
            'success': True,
            'total_records': len(all_items),
            'success_days': success_days,
            'failed_days': failed_days,
            'is_incremental': is_incremental,
            'date_range': {
                'start_date': start_date,
                'end_date': end_date
            },
            'saved_files': saved_files
        }
    except Exception as e:
        raise Exception(f'批量获取龙虎榜数据失败: {str(e)}')


def batch_fetch_sentiment_data(
    status_file: str = 'config/fetch_status.json',
    data_path: str = 'data/sentiment',
    default_years: int = 2,
    max_retries: int = 3,
    progress_interval: int = 50
) -> Dict[str, Any]:
    start_time = time.time()
    stats = {
        'total_stocks': 0,
        'success_count': 0,
        'failed_count': 0,
        'skipped_count': 0,
        'total_records': 0,
        'failed_stocks': [],
        'is_incremental': False,
        'date_range': {}
    }
    
    try:
        status = read_status(status_file)
        date_range = calculate_date_range(status, 'sentiment', default_years)
        stats['date_range'] = date_range
        stats['is_incremental'] = date_range.get('is_incremental', False)
        
        stocks_data = fetch_all_stock_codes()
        stock_list = stocks_data['items']
        stats['total_stocks'] = len(stock_list)
        
        if stats['total_stocks'] == 0:
            raise Exception('未获取到任何股票代码')
        
        print(json.dumps({
            'type': 'progress',
            'message': f'开始批量拉取舆情数据，共 {stats["total_stocks"]} 只股票',
            'date_range': date_range
        }, ensure_ascii=False), flush=True)
        
        for idx, stock in enumerate(stock_list, 1):
            symbol = stock['code']
            retry_count = 0
            success = False
            
            while retry_count < max_retries and not success:
                try:
                    # 尝试获取舆情数据
                    news_data = ak.stock_news_em(symbol=symbol)
                    
                    if news_data is not None and not news_data.empty:
                        items = []
                        for _, row in news_data.iterrows():
                            date_val = row.get('发布时间', '')
                            if hasattr(date_val, 'strftime'):
                                date_str = date_val.strftime('%Y-%m-%d')
                            else:
                                date_str = str(date_val).split(' ')[0] if ' ' in str(date_val) else str(date_val)
                            
                            items.append({
                                'date': date_str,
                                'symbol': symbol,
                                'title': str(row.get('新闻标题', '')),
                                'content': str(row.get('新闻内容', '')),
                                'source': str(row.get('文章来源', '')),
                                'url': str(row.get('新闻链接', ''))
                            })
                        
                        if items:
                            save_sentiment_data(items, data_path)
                            stats['total_records'] += len(items)
                    
                    stats['success_count'] += 1
                    success = True
                    
                except Exception as e:
                    retry_count += 1
                    if retry_count >= max_retries:
                        stats['failed_count'] += 1
                        stats['failed_stocks'].append({
                            'code': symbol,
                            'name': stock.get('name', ''),
                            'error': str(e)
                        })
                    else:
                        time.sleep(0.5)
            
            if idx % progress_interval == 0:
                elapsed = time.time() - start_time
                progress_pct = (idx / stats['total_stocks']) * 100
                print(json.dumps({
                    'type': 'progress',
                    'message': f'进度: {idx}/{stats["total_stocks"]} ({progress_pct:.1f}%)',
                    'success': stats['success_count'],
                    'failed': stats['failed_count'],
                    'elapsed_seconds': round(elapsed, 1)
                }, ensure_ascii=False), flush=True)
            
            time.sleep(0.15)
        
        fetch_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = update_fetch_time(status, 'sentiment', fetch_time, stats['success_count'])
        write_status(status_file, status)
        
        elapsed_time = time.time() - start_time
        stats['elapsed_seconds'] = round(elapsed_time, 2)
        
        return {
            'success': True,
            'stats': stats,
            'message': f'批量拉取舆情数据完成，成功 {stats["success_count"]} 只，失败 {stats["failed_count"]} 只'
        }
        
    except Exception as e:
        return {
            'success': False,
            'stats': stats,
            'error': str(e),
            'message': f'批量拉取舆情数据失败: {str(e)}'
        }


def batch_fetch_north_flow_data(
    status_file: str = 'config/fetch_status.json',
    data_path: str = 'data/north_flow',
    default_years: int = 5
) -> Dict[str, Any]:
    start_time = time.time()
    stats = {
        'total_records': 0,
        'is_incremental': False,
        'date_range': {},
        'saved_files': []
    }
    
    try:
        status = read_status(status_file)
        date_range = calculate_date_range(status, 'north_flow', default_years)
        stats['date_range'] = date_range
        stats['is_incremental'] = date_range.get('is_incremental', False)
        
        print(json.dumps({
            'type': 'progress',
            'message': '开始获取北向资金数据',
            'date_range': date_range
        }, ensure_ascii=False), file=sys.stderr, flush=True)
        
        data = ak.stock_hsgt_hist_em(symbol="沪股通")
        
        if data is None or data.empty:
            return {
                'success': True,
                'stats': stats,
                'message': '北向资金数据为空'
            }
        
        items = []
        for _, row in data.iterrows():
            date_value = row['日期']
            if hasattr(date_value, 'strftime'):
                date_str = date_value.strftime('%Y-%m-%d')
            else:
                date_str = str(date_value)
            
            items.append({
                'date': date_str,
                'net_buy': float(row.get('当日成交净买额', 0) or 0),
                'buy_amount': float(row.get('买入成交额', 0) or 0),
                'sell_amount': float(row.get('卖出成交额', 0) or 0),
                'cumulative_net_buy': float(row.get('历史累计净买额', 0) or 0),
                'fund_inflow': float(row.get('当日资金流入', 0) or 0),
                'balance': float(row.get('当日余额', 0) or 0)
            })
        
        stats['total_records'] = len(items)
        
        print(json.dumps({
            'type': 'progress',
            'message': f'获取到 {stats["total_records"]} 条记录，开始保存'
        }, ensure_ascii=False), file=sys.stderr, flush=True)
        
        saved_files = save_north_flow_data(items, data_path)
        stats['saved_files'] = saved_files
        
        fetch_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = update_fetch_time(status, 'north_flow', fetch_time, stats['total_records'])
        write_status(status_file, status)
        
        elapsed_time = time.time() - start_time
        stats['elapsed_seconds'] = round(elapsed_time, 2)
        
        return {
            'success': True,
            'stats': stats,
            'message': f'北向资金数据拉取完成，共 {stats["total_records"]} 条记录'
        }
        
    except Exception as e:
        return {
            'success': False,
            'stats': stats,
            'error': str(e),
            'message': f'北向资金数据拉取失败: {str(e)}'
        }


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
        elif action == 'stock_codes':
            result = fetch_all_stock_codes()
        elif action == 'batch_financial':
            result = batch_fetch_financial_data(
                params.get('status_file', 'config/fetch_status.json'),
                params.get('data_path', 'data/financial'),
                params.get('default_years', 3),
                params.get('max_retries', 3),
                params.get('progress_interval', 100)
            )
        elif action == 'batch_market':
            result = batch_fetch_market_data(
                params.get('status_file', 'config/fetch_status.json'),
                params.get('data_path', 'data/market'),
                params.get('default_years', 5),
                params.get('max_retries', 3),
                params.get('progress_interval', 100)
            )
        elif action == 'batch_lhb':
            result = batch_fetch_lhb_data(
                params.get('status_file', 'config/fetch_status.json'),
                params.get('data_path', 'data/lhb')
            )
        elif action == 'batch_north_flow':
            result = batch_fetch_north_flow_data(
                params.get('status_file', 'config/fetch_status.json'),
                params.get('data_path', 'data/north_flow'),
                params.get('default_years', 5)
            )
        elif action == 'batch_sentiment':
            result = batch_fetch_sentiment_data(
                params.get('status_file', 'config/fetch_status.json'),
                params.get('data_path', 'data/sentiment'),
                params.get('default_years', 2),
                params.get('max_retries', 3),
                params.get('progress_interval', 50)
            )
        else:
            print(json.dumps({'error': '未知的操作类型'}))
            sys.exit(1)
        
        print(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({'error': str(e)}))
        sys.exit(1)
