import os
import requests
from typing import List, Dict, Optional

# 尝试导入dotenv，如果没有安装则忽略
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class TDXStockQuery:
    def __init__(self):
        self.api_url = os.getenv('TDX_API_URL')
        if not self.api_url:
            raise ValueError("环境变量 TDX_API_URL 未设置，请先配置API地址")
        
        self.api_url = self.api_url.rstrip('/')
        
        # 初始化akshare API地址
        self.akshare_api_url = os.getenv('AKSHARE_API_URL')
        if self.akshare_api_url:
            self.akshare_api_url = self.akshare_api_url.rstrip('/')
    
    def _make_request(self, method: str, endpoint: str, params: Optional[Dict] = None, 
                     data: Optional[Dict] = None) -> Dict:
        try:
            url = f"{self.api_url}{endpoint}"
            
            if method == 'GET':
                response = requests.get(url, params=params, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, params=params, timeout=30)
            else:
                return {"code": -1, "message": f"不支持的HTTP方法: {method}"}
            
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"code": -1, "message": f"请求失败: {str(e)}"}
        except Exception as e:
            return {"code": -1, "message": f"发生错误: {str(e)}"}
    
    def get_quote(self, codes: List[str]) -> Dict:
        """获取五档行情
        
        Args:
            codes: 股票代码列表，如 ['000001', '600519']
            
        Returns:
            dict: 五档行情数据
        """
        if not codes:
            return {"code": -1, "message": "股票代码列表不能为空"}
        
        codes_str = ','.join(codes)
        return self._make_request('GET', '/api/quote', params={'code': codes_str})
    
    def get_kline(self, code: str, ktype: str = 'day') -> Dict:
        """获取K线数据
        
        Args:
            code: 股票代码，如 '000001'
            ktype: K线类型，默认day
            
        Returns:
            dict: K线数据
        """
        if not code:
            return {"code": -1, "message": "股票代码不能为空"}
        
        return self._make_request('GET', '/api/kline', params={'code': code, 'type': ktype})
    
    def get_minute(self, code: str, date: Optional[str] = None) -> Dict:
        """获取分时数据
        
        Args:
            code: 股票代码，如 '000001'
            date: 日期（YYYYMMDD格式），默认当天
            
        Returns:
            dict: 分时数据
        """
        if not code:
            return {"code": -1, "message": "股票代码不能为空"}
        
        params = {'code': code}
        if date:
            params['date'] = date
        
        return self._make_request('GET', '/api/minute', params=params)
    
    def get_trade(self, code: str, date: Optional[str] = None) -> Dict:
        """获取分时成交
        
        Args:
            code: 股票代码，如 '000001'
            date: 日期（YYYYMMDD格式），默认当天
            
        Returns:
            dict: 分时成交数据
        """
        if not code:
            return {"code": -1, "message": "股票代码不能为空"}
        
        params = {'code': code}
        if date:
            params['date'] = date
        
        return self._make_request('GET', '/api/trade', params=params)
    
    def search_stock(self, keyword: str) -> Dict:
        """搜索股票代码
        
        Args:
            keyword: 搜索关键词（代码或名称）
            
        Returns:
            dict: 搜索结果
        """
        if not keyword:
            return {"code": -1, "message": "搜索关键词不能为空"}
        
        return self._make_request('GET', '/api/search', params={'keyword': keyword})
    
    def get_stock_info(self, code: str) -> Dict:
        """获取股票综合信息
        
        Args:
            code: 股票代码，如 '000001'
            
        Returns:
            dict: 综合信息（五档行情+日K线+分时）
        """
        if not code:
            return {"code": -1, "message": "股票代码不能为空"}
        
        return self._make_request('GET', '/api/stock-info', params={'code': code})
    
    def get_codes(self, exchange: str = 'all') -> Dict:
        """获取股票代码列表
        
        Args:
            exchange: 交易所代码，默认all
            
        Returns:
            dict: 股票代码列表
        """
        params = {}
        if exchange and exchange != 'all':
            params['exchange'] = exchange
        
        return self._make_request('GET', '/api/codes', params=params)
    
    def batch_quote(self, codes: List[str]) -> Dict:
        """批量获取行情
        
        Args:
            codes: 股票代码列表，最多50只
            
        Returns:
            dict: 批量行情数据
        """
        if not codes:
            return {"code": -1, "message": "股票代码列表不能为空"}
        
        if len(codes) > 50:
            return {"code": -1, "message": "一次最多查询50只股票"}
        
        return self._make_request('POST', '/api/batch-quote', data={'codes': codes})
    
    def get_kline_history(self, code: str, ktype: str = 'day', 
                         start_date: Optional[str] = None, 
                         end_date: Optional[str] = None, 
                         limit: int = 100) -> Dict:
        """获取历史K线
        
        Args:
            code: 股票代码
            ktype: K线类型
            start_date: 开始日期（YYYYMMDD）
            end_date: 结束日期（YYYYMMDD）
            limit: 返回条数，默认100，最大800
            
        Returns:
            dict: 历史K线数据
        """
        if not code:
            return {"code": -1, "message": "股票代码不能为空"}
        
        params = {'code': code, 'type': ktype, 'limit': limit}
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
        
        return self._make_request('GET', '/api/kline-history', params=params)
    
    def get_index(self, code: str, ktype: str = 'day') -> Dict:
        """获取指数数据
        
        Args:
            code: 指数代码，如 'sh000001'
            ktype: K线类型，默认day
            
        Returns:
            dict: 指数数据
        """
        if not code:
            return {"code": -1, "message": "指数代码不能为空"}
        
        return self._make_request('GET', '/api/index', params={'code': code, 'type': ktype})
    
    def get_server_status(self) -> Dict:
        """获取服务状态
        
        Returns:
            dict: 服务状态信息
        """
        return self._make_request('GET', '/api/server-status')
    
    def health_check(self) -> Dict:
        """健康检查
        
        Returns:
            dict: 健康状态
        """
        try:
            url = f"{self.api_url}/api/health"
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            return {"code": 0, "message": "success", "data": data}
        except requests.RequestException as e:
            return {"code": -1, "message": f"请求失败: {str(e)}"}
        except Exception as e:
            return {"code": -1, "message": f"发生错误: {str(e)}"}
    
    def create_pull_kline_task(self, codes: Optional[List[str]] = None, 
                               tables: Optional[List[str]] = None, 
                               dir: Optional[str] = None, 
                               limit: int = 1, 
                               start_date: Optional[str] = None) -> Dict:
        """创建批量K线入库任务
        
        Args:
            codes: 股票代码数组，默认全部A股
            tables: K线类型列表，默认['day']
            dir: 存储目录，默认'data/database/kline'
            limit: 并发协程数量，默认1
            start_date: 起始日期阈值
            
        Returns:
            dict: 任务信息（包含task_id）
        """
        data = {'limit': limit}
        if codes:
            data['codes'] = codes
        if tables:
            data['tables'] = tables
        if dir:
            data['dir'] = dir
        if start_date:
            data['start_date'] = start_date
        
        return self._make_request('POST', '/api/tasks/pull-kline', data=data)
    
    def create_pull_trade_task(self, code: str, 
                              dir: Optional[str] = None, 
                              start_year: int = 2000, 
                              end_year: Optional[int] = None) -> Dict:
        """创建分时成交入库任务
        
        Args:
            code: 股票代码
            dir: 输出目录，默认'data/database/trade'
            start_year: 起始年份，默认2000
            end_year: 结束年份，默认当年
            
        Returns:
            dict: 任务信息（包含task_id）
        """
        if not code:
            return {"code": -1, "message": "股票代码不能为空"}
        
        data = {'code': code, 'start_year': start_year}
        if dir:
            data['dir'] = dir
        if end_year:
            data['end_year'] = end_year
        
        return self._make_request('POST', '/api/tasks/pull-trade', data=data)
    
    def get_tasks(self) -> Dict:
        """查询任务列表
        
        Returns:
            dict: 任务列表
        """
        return self._make_request('GET', '/api/tasks')
    
    def get_task_detail(self, task_id: str) -> Dict:
        """查询任务详情
        
        Args:
            task_id: 任务ID
            
        Returns:
            dict: 任务详情
        """
        if not task_id:
            return {"code": -1, "message": "任务ID不能为空"}
        
        return self._make_request('GET', f'/api/tasks/{task_id}')
    
    def cancel_task(self, task_id: str) -> Dict:
        """取消任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            dict: 取消结果
        """
        if not task_id:
            return {"code": -1, "message": "任务ID不能为空"}
        
        return self._make_request('POST', f'/api/tasks/{task_id}/cancel')
    
    def get_etf(self, exchange: str = 'all', limit: Optional[int] = None) -> Dict:
        """获取ETF列表
        
        Args:
            exchange: 交易所，默认all
            limit: 返回条数限制
            
        Returns:
            dict: ETF列表
        """
        params = {}
        if exchange and exchange != 'all':
            params['exchange'] = exchange
        if limit:
            params['limit'] = limit
        
        return self._make_request('GET', '/api/etf', params=params)
    
    def get_trade_history(self, code: str, date: str, 
                         start: int = 0, count: int = 2000) -> Dict:
        """获取历史分时成交（分页）
        
        Args:
            code: 股票代码
            date: 交易日期（YYYYMMDD）
            start: 起始游标，默认0
            count: 返回条数，默认2000，最大2000
            
        Returns:
            dict: 历史分时成交数据
        """
        if not code:
            return {"code": -1, "message": "股票代码不能为空"}
        if not date:
            return {"code": -1, "message": "交易日期不能为空"}
        
        params = {'code': code, 'date': date, 'start': start, 'count': min(count, 2000)}
        return self._make_request('GET', '/api/trade-history', params=params)
    
    def get_minute_trade_all(self, code: str, date: Optional[str] = None) -> Dict:
        """获取全天分时成交
        
        Args:
            code: 股票代码
            date: 交易日期（YYYYMMDD），默认当天
            
        Returns:
            dict: 全天分时成交数据
        """
        if not code:
            return {"code": -1, "message": "股票代码不能为空"}
        
        params = {'code': code}
        if date:
            params['date'] = date
        
        return self._make_request('GET', '/api/minute-trade-all', params=params)
    
    def get_workday(self, date: Optional[str] = None, count: int = 1) -> Dict:
        """查询交易日信息
        
        Args:
            date: 查询日期（YYYYMMDD），默认当天
            count: 返回的前后交易日数量，范围1-30，默认1
            
        Returns:
            dict: 交易日信息
        """
        params = {'count': min(count, 30)}
        if date:
            params['date'] = date
        
        return self._make_request('GET', '/api/workday', params=params)
    
    def get_market_count(self) -> Dict:
        """获取市场证券数量
        
        Returns:
            dict: 市场证券数量统计
        """
        return self._make_request('GET', '/api/market-count')
    
    def get_stock_codes(self, limit: Optional[int] = None, prefix: bool = True) -> Dict:
        """获取股票代码列表
        
        Args:
            limit: 返回条数限制
            prefix: 是否包含交易所前缀，默认true
            
        Returns:
            dict: 股票代码列表
        """
        params = {'prefix': prefix}
        if limit:
            params['limit'] = limit
        
        return self._make_request('GET', '/api/stock-codes', params=params)
    
    def get_etf_codes(self, limit: Optional[int] = None, prefix: bool = True) -> Dict:
        """获取ETF代码列表
        
        Args:
            limit: 返回条数限制
            prefix: 是否包含交易所前缀，默认true
            
        Returns:
            dict: ETF代码列表
        """
        params = {'prefix': prefix}
        if limit:
            params['limit'] = limit
        
        return self._make_request('GET', '/api/etf-codes', params=params)
    
    def get_kline_all(self, code: str, ktype: str = 'day', limit: Optional[int] = None) -> Dict:
        """获取股票全部历史K线
        
        Args:
            code: 股票代码
            ktype: K线类型，默认day
            limit: 返回条数限制
            
        Returns:
            dict: 全部历史K线数据
        """
        if not code:
            return {"code": -1, "message": "股票代码不能为空"}
        
        params = {'code': code, 'type': ktype}
        if limit:
            params['limit'] = limit
        
        return self._make_request('GET', '/api/kline-all', params=params)
    
    def get_index_all(self, code: str, ktype: str = 'day', limit: Optional[int] = None) -> Dict:
        """获取指数全部历史K线
        
        Args:
            code: 指数代码
            ktype: K线类型，默认day
            limit: 返回条数限制
            
        Returns:
            dict: 指数全部历史K线数据
        """
        if not code:
            return {"code": -1, "message": "指数代码不能为空"}
        
        params = {'code': code, 'type': ktype}
        if limit:
            params['limit'] = limit
        
        return self._make_request('GET', '/api/index/all', params=params)
    
    def get_trade_history_full(self, code: str, before: Optional[str] = None, 
                               limit: Optional[int] = None) -> Dict:
        """获取上市以来分时成交
        
        Args:
            code: 股票代码
            before: 截止日期（YYYYMMDD），默认今天
            limit: 返回条数限制
            
        Returns:
            dict: 上市以来分时成交数据
        """
        if not code:
            return {"code": -1, "message": "股票代码不能为空"}
        
        params = {'code': code}
        if before:
            params['before'] = before
        if limit:
            params['limit'] = limit
        
        return self._make_request('GET', '/api/trade-history/full', params=params)
    
    def get_workday_range(self, start: str, end: str) -> Dict:
        """获取交易日范围
        
        Args:
            start: 起始日期（YYYYMMDD）
            end: 结束日期（YYYYMMDD）
            
        Returns:
            dict: 交易日范围列表
        """
        if not start:
            return {"code": -1, "message": "起始日期不能为空"}
        if not end:
            return {"code": -1, "message": "结束日期不能为空"}
        
        return self._make_request('GET', '/api/workday/range', params={'start': start, 'end': end})
    
    def get_income(self, code: str, start_date: str) -> Dict:
        """计算收益区间指标
        
        Args:
            code: 股票代码，如 '000001'
            start_date: 基准日期，如 '2023-01-01'
            
        Returns:
            dict: 收益区间分析结果
        """
        if not code:
            return {"code": -1, "message": "股票代码不能为空"}
        if not start_date:
            return {"code": -1, "message": "基准日期不能为空"}
        
        return self._make_request('GET', '/api/income', params={'code': code, 'start_date': start_date})
    
    def get_stock_news(self, symbol: str) -> Dict:
        """获取股票新闻
        
        Args:
            symbol: 股票代码或关键词，如 '603777' 或 '宁德时代'
            
        Returns:
            dict: 新闻数据
        """
        if not symbol:
            return {"code": -1, "message": "股票代码或关键词不能为空"}
        
        if not self.akshare_api_url:
            return {"code": -1, "message": "环境变量 AKSHARE_API_URL 未设置，请先配置akshare API地址"}
        
        try:
            url = f"{self.akshare_api_url}/api/public/stock_news_em"
            response = requests.get(url, params={'symbol': symbol}, timeout=30)
            response.raise_for_status()
            data = response.json()
            return {"code": 0, "message": "success", "data": data}
        except requests.RequestException as e:
            return {"code": -1, "message": f"请求失败: {str(e)}"}
        except Exception as e:
            return {"code": -1, "message": f"发生错误: {str(e)}"}
    
    def get_stock_disclosure(self, symbol: str, start_date: str, end_date: str, 
                          market: str = '沪深京', category: Optional[str] = None, 
                          keyword: Optional[str] = None) -> Dict:
        """获取股票公告
        
        Args:
            symbol: 股票代码，如 '300058'
            start_date: 起始日期，格式YYYYMMDD，如 '20260101'
            end_date: 结束日期，格式YYYYMMDD，如 '20260314'
            market: 市场，默认'沪深京'
            category: 公告分类，如 '年报'、'董事会'、'权益分派' 等
            keyword: 关键词搜索，在公告标题中进行搜索
            
        Returns:
            dict: 公告数据
        """
        if not symbol:
            return {"code": -1, "message": "股票代码不能为空"}
        if not start_date:
            return {"code": -1, "message": "起始日期不能为空"}
        if not end_date:
            return {"code": -1, "message": "结束日期不能为空"}
        
        if not self.akshare_api_url:
            return {"code": -1, "message": "环境变量 AKSHARE_API_URL 未设置，请先配置akshare API地址"}
        
        try:
            url = f"{self.akshare_api_url}/api/public/stock_zh_a_disclosure_report_cninfo"
            params = {
                'symbol': symbol,
                'start_date': start_date,
                'end_date': end_date
            }
            
            if market:
                params['market'] = market
            if category:
                params['category'] = category
            if keyword:
                params['keyword'] = keyword
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            return {"code": 0, "message": "success", "data": data}
        except requests.RequestException as e:
            return {"code": -1, "message": f"请求失败: {str(e)}"}
        except Exception as e:
            return {"code": -1, "message": f"发生错误: {str(e)}"}


def format_price(price_in_li: int) -> float:
    """将价格从厘转换为元
    
    Args:
        price_in_li: 价格（厘）
        
    Returns:
        float: 价格（元）
    """
    return price_in_li / 1000.0


def format_volume(volume_in_hands: int) -> int:
    """将成交量从手转换为股
    
    Args:
        volume_in_hands: 成交量（手）
        
    Returns:
        int: 成交量（股）
    """
    return volume_in_hands * 100


if __name__ == "__main__":
    import os
    
    if not os.getenv('TDX_API_URL'):
        print("错误：请先设置环境变量 TDX_API_URL")
        print("示例: export TDX_API_URL=http://your-api-domain.com")
        exit(1)
    
    stock_query = TDXStockQuery()
    
    print("=== TDX股票查询技能测试 ===")
    print(f"API地址: {stock_query.api_url}")
    print()
    
    # 测试健康检查
    print("1. 测试健康检查...")
    result = stock_query.health_check()
    print(f"结果: {result}")
    print()
    
    # 测试服务状态
    print("2. 测试服务状态...")
    result = stock_query.get_server_status()
    print(f"结果: {result}")
    print()
    
    # 测试搜索股票
    print("3. 测试搜索股票（平安）...")
    result = stock_query.search_stock('平安')
    print(f"结果: {result}")
    print()
    
    # 测试获取五档行情
    print("4. 测试获取五档行情（000001）...")
    result = stock_query.get_quote(['000001'])
    print(f"结果: {result}")
    print()
    
    # 测试获取K线数据
    print("5. 测试获取K线数据（000001, day）...")
    result = stock_query.get_kline('000001', 'day')
    print(f"结果: {result}")
    print()
    
    # 测试获取分时数据
    print("6. 测试获取分时数据（000001）...")
    result = stock_query.get_minute('000001')
    print(f"结果: {result}")
    print()
    
    # 测试获取股票代码列表
    print("7. 测试获取股票代码列表...")
    result = stock_query.get_codes('sh')
    print(f"结果: {result}")
    print()
    
    # 测试获取指数数据
    print("8. 测试获取指数数据（sh000001）...")
    result = stock_query.get_index('sh000001', 'day')
    print(f"结果: {result}")
    print()
    
    # 测试获取ETF列表
    print("9. 测试获取ETF列表...")
    result = stock_query.get_etf('sh', limit=5)
    print(f"结果: {result}")
    print()
    
    # 测试查询交易日信息
    print("10. 测试查询交易日信息...")
    result = stock_query.get_workday()
    print(f"结果: {result}")
    print()
    
    # 测试获取市场证券数量
    print("11. 测试获取市场证券数量...")
    result = stock_query.get_market_count()
    print(f"结果: {result}")
    print()
    
    print("=== 测试完成 ===")