#!/usr/bin/env python3
"""
行情查询模块
使用腾讯财经实时行情 API
"""
import sys
import os
import requests

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def get_quote_tencent(code):
    """获取腾讯财经实时行情"""
    # 添加市场前缀：sh=沪市，sz=深市
    if code.startswith('6'):
        market = 'sh'
    else:
        market = 'sz'
    
    url = f"https://qt.gtimg.cn/q={market}{code}"
    
    try:
        response = requests.get(url, timeout=5)
        text = response.text.strip()
        
        if text and '=' in text:
            parts = text.split('=')[1].strip('"').split('~')
            
            if len(parts) > 10:
                try:
                    current_price = float(parts[3])
                    if current_price > 0:
                        # 安全获取数值
                        def safe_float(s, default=0.0):
                            try:
                                return float(s) if s else default
                            except:
                                return default
                        
                        def safe_int(s, default=0):
                            try:
                                return int(float(s)) if s else default
                            except:
                                return default
                        
                        # 计算涨跌和涨跌幅
                        yesterday_close = safe_float(parts[4])
                        change = current_price - yesterday_close
                        change_pct = (change / yesterday_close * 100) if yesterday_close > 0 else 0
                        
                        return {
                            'code': code,
                            'name': parts[1],  # 股票名称
                            'price': current_price,
                            'change': change,  # 涨跌
                            'change_pct': change_pct,  # 涨跌幅
                            'open': safe_float(parts[9]),  # 开盘价
                            'high': safe_float(parts[33]) if len(parts) > 33 else current_price,  # 最高
                            'low': safe_float(parts[34]) if len(parts) > 34 else current_price,  # 最低
                            'volume': safe_int(parts[6]) * 100,  # 成交量(股)
                            'amount': safe_float(parts[7]),  # 成交额(元)
                            'yesterday_close': yesterday_close,  # 昨收
                        }
                except (ValueError, IndexError) as e:
                    print(f"解析错误: {e}")
                    return None
    
    except Exception as e:
        print(f"获取行情失败: {e}")
    
    return None


def show_quote(code):
    """显示股票行情"""
    quote = get_quote_tencent(code)
    
    if not quote:
        print(f"❌ 无法获取 {code} 的行情")
        return None
    
    print("=" * 60)
    print(f"📈 {quote['name']} ({quote['code']})")
    print("=" * 60)
    print(f"💰 当前价格：¥{quote['price']:.2f}")
    print(f"📊 涨跌：{quote['change']:+.2f} ({quote['change_pct']:+.2f}%)")
    print("-" * 60)
    print(f"📅 昨收：¥{quote['yesterday_close']:.2f}")
    print(f"📅 开盘：¥{quote['open']:.2f}")
    print(f"📈 最高：¥{quote['high']:.2f}")
    print(f"📉 最低：¥{quote['low']:.2f}")
    print(f"📊 成交量：{quote['volume']:,} 股")
    print(f"💵 成交额：¥{quote['amount']:,.0f}")
    print("=" * 60)
    
    return quote


def main():
    if len(sys.argv) < 2:
        print("用法：")
        print("  python3 quote.py <股票代码> [股票代码2] ...")
        print("")
        print("示例：")
        print("  python3 quote.py 600900")
        print("  python3 quote.py 600900 600025 600919")
        sys.exit(1)
    
    codes = sys.argv[1:]
    
    for code in codes:
        show_quote(code)
        print()


if __name__ == "__main__":
    main()
