import requests
import io
import sys

def search_stock_code(stock_name):
    """通过股票名称搜索股票代码"""
    try:
        url = f"https://searchapi.eastmoney.com/api/suggest/get?input={stock_name}&type=14&count=5"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        if data.get('QuotationCodeTable') and data['QuotationCodeTable'].get('Data'):
            stocks = data['QuotationCodeTable']['Data']
            for stock in stocks:
                if stock.get('SecurityTypeName') in ['沪A', '深A', '创业板', '科创板','美股','港股']:
                    return {
                        'name': stock['Name'],
                        'code': stock['Code'],
                        'market': stock['SecurityTypeName']
                    }
        return None
    except Exception as e:
        return {'error': str(e)}

def get_stock_price(stock_code,stock_type):
    """使用新浪财经API查询股票价格"""
    try:
        if stock_type=='美股':
            sina_code=f"gb_{stock_code.lower()}"
        elif stock_type=='港股':
            sina_code=f"hk{stock_code}"
        else:
            if stock_code.startswith('6') or stock_code.startswith('5') or stock_code.startswith('9'):
                sina_code = f"sh{stock_code}"
            else:
                sina_code = f"sz{stock_code}"
            
        url = f"https://hq.sinajs.cn/list={sina_code}"
        headers = {
            'Referer': 'https://finance.sina.com.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'gb2312'
        data = response.text
        if stock_type=='港股':
            if 'hq_str_' in data and '"' in data:
                start = data.find('"') + 1
                end = data.rfind('"')
                if start > 0 and end > start:
                    values = data[start:end].split(',')
                    if len(values) > 3:
                        return {
                            'name': values[1],
                            'code': stock_code,
                            'open_price': values[2],
                            'close_price': values[3],
                            'current_price': values[6],
                            'high_price': values[4],
                            'low_price': values[5],
                            'volume': values[12] if len(values) > 8 else 'N/A'
                        }
        elif stock_type=='美股':
            if 'hq_str_' in data and '"' in data:
                start = data.find('"') + 1
                end = data.rfind('"')
                if start > 0 and end > start:
                    values = data[start:end].split(',')
                    if len(values) > 3:
                        return {
                            'name': values[0],
                            'code': stock_code,
                            'open_price': values[5],
                            'close_price': values[26],
                            'current_price': values[1],
                            'high_price': values[6],
                            'low_price': values[7],
                            'volume': values[10] if len(values) > 8 else 'N/A'
                        }
        else:
            if 'hq_str_' in data and '"' in data:
                start = data.find('"') + 1
                end = data.rfind('"')
                if start > 0 and end > start:
                    values = data[start:end].split(',')
                    if len(values) > 3:
                        return {
                            'name': values[0],
                            'code': stock_code,
                            'open_price': values[1],
                            'close_price': values[2],
                            'current_price': values[3],
                            'high_price': values[4],
                            'low_price': values[5],
                            'volume': values[8] if len(values) > 8 else 'N/A'
                        }
        return None
    except Exception as e:
        return {'error': str(e)}

def query_stock_price(stock_name):
    """通过自然语言股票名称查询价格"""
    search_result = search_stock_code(stock_name)
    
    if not search_result:
        return f"未找到股票: {stock_name}"
    
    if 'error' in search_result:
        return f"搜索失败: {search_result['error']}"
    
    stock_code = search_result['code']
    stock_type = search_result['market']
    price_info = get_stock_price(stock_code,stock_type)
    
    if not price_info:
        return f"无法获取 {search_result['name']}({stock_code}) 的价格信息"
    
    if 'error' in price_info:
        return f"查询失败: {price_info['error']}"
    
    result = f"""
📈 {price_info['name']} ({price_info['code']})
━━━━━━━━━━━━━━━━━━━━
💰 当前价格: ¥{price_info['current_price']}
📊 今日开盘: ¥{price_info['open_price']}
📈 昨日收盘: ¥{price_info['close_price']}
⬆️  今日最高: ¥{price_info['high_price']}
⬇️  今日最低: ¥{price_info['low_price']}
📦 成交量: {price_info['volume']}股
    """
    return result

if __name__ == '__main__':
    print("=" * 50)
    print("A股股票价格查询")
    print("=" * 50)
    
    # 设置stdout编码为UTF-8
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    # 支持命令行参数查询
    if len(sys.argv) > 1:
        stock_name = sys.argv[1]
        print(f"\n查询: {stock_name}")
        print(query_stock_price(stock_name))
    else:
        # 默认查询示例
        print("=" * 50)
        print("A股股票价格查询")
        print("=" * 50)
        print("\n用法: python stock_price_query.py <股票名称或代码>")
        print("示例: python stock_price_query.py 贵州茅台")
        print("      python stock_price_query.py 600519")
        print("\n" + "-" * 50)
        
        # 演示查询
        stock_name = '贵州茅台'
        print(f"\n查询: {stock_name}")
        print(query_stock_price(stock_name))
