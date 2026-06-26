
#!/usr/bin/env python3
import sys
import requests
import json

def get_stock_price(stock_code):
    """
    查询股票实时价格
    """
    try:
        # 这里使用一个模拟 API，实际应该使用真实的股票 API
        response = requests.get(f"https://api.mock-stock.com/price?code={stock_code}")
        data = response.json()
        return data.get("price", "无法获取价格")
    except Exception as e:
        return f"查询失败: {str(e)}"

def get_stock_info(stock_code):
    """
    查询股票详细信息
    """
    try:
        response = requests.get(f"https://api.mock-stock.com/info?code={stock_code}")
        data = response.json()
        return data
    except Exception as e:
        return {"error": str(e)}

def get_etf_info(etf_name):
    """
    查询 ETF 详细信息
    """
    try:
        response = requests.get(f"https://api.mock-stock.com/etf?name={etf_name}")
        data = response.json()
        return data
    except Exception as e:
        return {"error": str(e)}

def recommend_stocks():
    """
    推荐高潜力股票
    """
    try:
        response = requests.get("https://api.mock-stock.com/recommend")
        data = response.json()
        return data.get("stocks", [])
    except Exception as e:
        return {"error": str(e)}

def main():
    if len(sys.argv) < 2:
        print("使用方法: python3 stock_query.py <command> [args]")
        print("命令列表:")
        print("  price <股票代码> - 查询股票价格")
        print("  info <股票代码> - 查询股票详细信息")
        print("  etf <ETF名称> - 查询ETF信息")
        print("  recommend - 推荐高潜力股票")
        return

    command = sys.argv[1]
    
    if command == "price":
        if len(sys.argv) < 3:
            print("请提供股票代码")
            return
        stock_code = sys.argv[2]
        price = get_stock_price(stock_code)
        print(f"股票价格: {price}")
    elif command == "info":
        if len(sys.argv) < 3:
            print("请提供股票代码")
            return
        stock_code = sys.argv[2]
        info = get_stock_info(stock_code)
        print(json.dumps(info, indent=2, ensure_ascii=False))
    elif command == "etf":
        if len(sys.argv) < 3:
            print("请提供ETF名称")
            return
        etf_name = sys.argv[2]
        info = get_etf_info(etf_name)
        print(json.dumps(info, indent=2, ensure_ascii=False))
    elif command == "recommend":
        stocks = recommend_stocks()
        print(json.dumps(stocks, indent=2, ensure_ascii=False))
    else:
        print("未知命令")

if __name__ == "__main__":
    main()
