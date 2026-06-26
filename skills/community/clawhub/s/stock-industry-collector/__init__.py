"""
螃蟹投研-股票行业数据收集器 v2.8
包含：财务数据 + 控股股东 + 每日交易数据（开盘价/收盘价/市值）
使用curl调用API，解决代理阻塞问题
"""

import pandas as pd
import subprocess
import json
import time
from datetime import datetime

class IndustryCollector:
    """股票行业数据收集器"""
    
    def _curl_api(self, url):
        """使用curl调用API"""
        try:
            result = subprocess.run(
                ['curl', '-s', '--max-time', '10', url],
                capture_output=True, text=True, timeout=15
            )
            if result.returncode == 0:
                return json.loads(result.stdout)
        except Exception as e:
            print(f"CURL失败: {e}")
        return None
    
    def get_sw_stocks(self, industry_code):
        """获取申万三级行业成分股"""
        import akshare as ak
        return ak.sw_index_third_cons(industry_code)
    
    def get_daily_price(self, stock_code):
        """
        获取股票每日交易数据（使用东方财富API）
        返回：日期、开盘价、收盘价、最高价、最低价、总市值
        """
        code = stock_code.upper().replace('.SH', '').replace('.SZ', '')
        if code.startswith('6'):
            secid = f"1.{code}"  # 沪市
        else:
            secid = f"0.{code}"  # 深市
        
        # 东方财富实时行情API - f43=最新价, f46=开盘价, f44=最高价, f45=最低价, f47=成交量, f48=成交额, f116=总市值, f117=流通市值, f162=市盈率TTM, f167=市净率
        url = f'https://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f43,f44,f45,f46,f47,f48,f57,f58,f116,f117,f162,f167'
        
        data = self._curl_api(url)
        
        if data and data.get('data'):
            d = data['data']
            return {
                '日期': datetime.now().strftime('%Y-%m-%d'),
                '开盘价': d.get('f46', 0) / 100,
                '收盘价': d.get('f43', 0) / 100,
                '最高价': d.get('f44', 0) / 100,
                '最低价': d.get('f45', 0) / 100,
                '成交量': d.get('f47', 0),
                '成交额': d.get('f48', 0) / 100,
                '总市值': round(d.get('f116', 0) / 100000000, 2) if d.get('f116') else 0,
                '流通市值': round(d.get('f117', 0) / 100000000, 2) if d.get('f117') else 0,
                '市盈率PE': d.get('f162', 0) / 100 if d.get('f162') else 0,
                '市净率PB': d.get('f167', 0) / 100 if d.get('f167') else 0,
            }
        
        return {
            '日期': '', '开盘价': 0, '收盘价': 0, '最高价': 0, '最低价': 0,
            '成交量': 0, '成交额': 0, '总市值': 0, '流通市值': 0, '市盈率PE': 0, '市净率PB': 0
        }
    
    def get_shareholder(self, stock_code):
        """获取控股股东信息（使用akshare）"""
        import akshare as ak
        
        code = stock_code.upper().replace('.SH', '').replace('.SZ', '')
        if code.startswith('6'):
            symbol = 'SH' + code
        else:
            symbol = 'SZ' + code
        
        try:
            df = ak.stock_gdfx_free_top_10_em(symbol=symbol)
            if df is not None and len(df) > 0:
                first = df.iloc[0]
                return {
                    '控股股东': first.get('股东名称', ''),
                    '控股比例': first.get('占总流通股本持股比例', ''),
                    '股东性质': first.get('股东性质', '')
                }
        except Exception as e:
            print(f"获取股东信息失败: {e}")
        
        return {'控股股东': '', '控股比例': '', '股东性质': ''}
    
    def collect(self, industry_name=None, industry_code=None, include_price=True):
        """
        收集行业全部股票数据
        
        参数:
            industry_name: 行业名称（如"煤炭"、"动力煤"、"焦煤"）
            industry_code: 申万行业代码
            include_price: 是否包含每日交易数据
        
        返回:
            dict: 包含stocks列表和count总数
        """
        name_to_code = {
            "煤化工": "850325.SI",
            "动力煤": "859511.SI",
            "焦煤": "859512.SI",
            "煤炭": "859511.SI",
        }
        if industry_name in name_to_code:
            industry_code = name_to_code[industry_name]
        
        print(f"正在获取 {industry_name or industry_code} 行业股票列表...")
        df = self.get_sw_stocks(industry_code)
        print(f"找到 {len(df)} 只股票")
        
        results = []
        for idx, row in df.iterrows():
            stock_code = row['股票代码'].replace('.SH', '').replace('.SZ', '')
            stock_name = row.get('股票简称', '')
            
            print(f"  处理 {stock_code} {stock_name}...", end='', flush=True)
            
            # 获取每日交易数据
            price_data = {}
            if include_price:
                price_data = self.get_daily_price(stock_code)
            
            # 获取控股股东
            sh = self.get_shareholder(stock_code)
            
            r = row.to_dict()
            r.update(price_data)
            r.update(sh)
            results.append(r)
            
            if include_price and price_data.get('总市值'):
                print(f" ✓ 市值{price_data['总市值']}亿")
            else:
                print(f" ✓")
            
            time.sleep(0.1)
        
        return {"stocks": results, "count": len(results)}

if __name__ == "__main__":
    c = IndustryCollector()
    
    # 测试
    print("=" * 60)
    print("测试：煤炭行业数据收集 v2.8")
    print("=" * 60)
    
    r = c.collect(industry_name="煤炭")
    print(f"\n煤炭行业: {r['count']}只\n")
    
    for s in r['stocks'][:5]:
        print(f"{s.get('股票简称', 'N/A')} ({s.get('股票代码', 'N/A')})")
        print(f"  日期: {s.get('日期', 'N/A')}")
        print(f"  开盘价: {s.get('开盘价', 'N/A')}元")
        print(f"  收盘价: {s.get('收盘价', 'N/A')}元")
        print(f"  最高价: {s.get('最高价', 'N/A')}元")
        print(f"  最低价: {s.get('最低价', 'N/A')}元")
        print(f"  总市值: {s.get('总市值', 'N/A')}亿元")
        print(f"  流通市值: {s.get('流通市值', 'N/A')}亿元")
        print(f"  市盈率PE: {s.get('市盈率PE', 'N/A')}")
        print(f"  市净率PB: {s.get('市净率PB', 'N/A')}")
        print(f"  控股股东: {s.get('控股股东', 'N/A')}")
        print()