"""
TOC Trading System - AKShare 数据源
免费公开数据，无需 API Key
"""
import akshare as ak
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta

class AKShareClient:
    """AKShare 数据封装 - 东方财富公开数据源"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        print("✅ AKShare 数据源已加载（东方财富）")
    
    def is_available(self) -> bool:
        """检查是否可用"""
        return True  # AKShare 无需认证，始终可用
    
    def get_stock_spot(self) -> List[Dict]:
        """获取实时行情（全部A股）"""
        try:
            df = ak.stock_zh_a_spot_em()
            if df is not None and len(df) > 0:
                result = []
                for _, row in df.iterrows():
                    result.append({
                        'code': row.get('代码', ''),
                        'name': row.get('名称', ''),
                        'price': row.get('最新价', 0),
                        'change': row.get('涨跌幅', 0),
                        'volume': row.get('成交量', 0),
                        'amount': row.get('成交额', 0),
                        'high': row.get('最高', 0),
                        'low': row.get('最低', 0),
                        'open': row.get('今开', 0),
                        'prev_close': row.get('昨收', 0),
                        'pe': row.get('市盈率-动态', 0),
                        'pb': row.get('市净率', 0),
                        'mkt_cap': row.get('总市值', 0),
                        'float_cap': row.get('流通市值', 0)
                    })
                return result
        except Exception as e:
            print(f"获取实时行情失败: {e}")
        return []
    
    def get_industry_boards(self) -> List[Dict]:
        """获取行业板块数据"""
        try:
            df = ak.stock_board_industry_name_em()
            if df is not None and len(df) > 0:
                result = []
                for _, row in df.iterrows():
                    result.append({
                        'name': row.get('板块名称', ''),
                        'code': row.get('板块代码', ''),
                        'change': row.get('涨跌幅', 0),
                        'leader': row.get('领涨股票', ''),
                        'leader_chg': row.get('领涨股票-涨跌幅', 0),
                        'rise_count': row.get('上涨家数', 0),
                        'fall_count': row.get('下跌家数', 0)
                    })
                return result
        except Exception as e:
            print(f"获取行业板块失败: {e}")
        return []
    
    def get_concept_boards(self) -> List[Dict]:
        """获取概念板块数据"""
        try:
            df = ak.stock_board_concept_name_em()
            if df is not None and len(df) > 0:
                result = []
                for _, row in df.iterrows():
                    result.append({
                        'name': row.get('板块名称', ''),
                        'code': row.get('板块代码', ''),
                        'change': row.get('涨跌幅', 0),
                        'leader': row.get('领涨股票', ''),
                        'leader_chg': row.get('领涨股票-涨跌幅', 0)
                    })
                return result
        except Exception as e:
            print(f"获取概念板块失败: {e}")
        return []
    
    def get_hot_concepts(self, limit: int = 10) -> List[Dict]:
        """获取热门概念板块"""
        concepts = self.get_concept_boards()
        concepts.sort(key=lambda x: x.get('change', 0), reverse=True)
        return concepts[:limit]
    
    def get_hot_industries(self, limit: int = 10) -> List[Dict]:
        """获取热门行业板块"""
        industries = self.get_industry_boards()
        industries.sort(key=lambda x: x.get('change', 0), reverse=True)
        return industries[:limit]
    
    def filter_by_industry(self, category: str, limit: int = 10) -> List[Dict]:
        """按行业筛选板块"""
        keywords = {
            'AI/人工智能': ['半导体', '电子', '通信', '软件', '计算机', 'AI', '人工智能', '算力', '芯片', '光通信'],
            '消费品': ['食品', '饮料', '白酒', '家电', '纺织', '商贸', '旅游', '酒店', '乳业'],
            '汽车': ['汽车', '新能源', '锂电', '锂电池', '整车', '零部件'],
            '医疗': ['医疗', '医药', '生物', '中药', '疫苗', '医疗器械', '化学制药']
        }
        
        kws = keywords.get(category, [])
        result = []
        
        # 检查行业板块
        industries = self.get_industry_boards()
        for ind in industries:
            if any(kw in ind.get('name', '') for kw in kws):
                result.append(ind)
        
        # 检查概念板块
        concepts = self.get_concept_boards()
        for con in concepts:
            if any(kw in con.get('name', '') for kw in kws):
                result.append(con)
        
        # 去重排序
        seen = set()
        unique = []
        for r in result:
            if r['name'] not in seen:
                seen.add(r['name'])
                unique.append(r)
        
        unique.sort(key=lambda x: x['change'], reverse=True)
        return unique[:limit]
    
    def get_stock_daily(self, stock_code: str, start_date: str = None, end_date: str = None) -> List[Dict]:
        """获取股票日线数据"""
        try:
            if start_date is None:
                start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
            if end_date is None:
                end_date = datetime.now().strftime('%Y%m%d')
            
            df = ak.stock_zh_a_daily(symbol=f"sh{stock_code}" if stock_code.startswith('6') else f"sz{stock_code}")
            if df is not None and len(df) > 0:
                result = []
                for _, row in df.iterrows():
                    result.append({
                        'date': row.get('日期', ''),
                        'open': row.get('开盘', 0),
                        'high': row.get('最高', 0),
                        'low': row.get('最低', 0),
                        'close': row.get('收盘', 0),
                        'volume': row.get('成交量', 0)
                    })
                return result
        except Exception as e:
            print(f"获取日线数据失败: {e}")
        return []
    
    def format_industry_analysis(self, category: str) -> str:
        """格式化行业分析结果"""
        data = self.filter_by_industry(category)
        
        if not data:
            return f"【{category}】\n暂无匹配数据"
        
        lines = [f"【{category}】"]
        
        for i, d in enumerate(data, 1):
            name = d.get('name', '')
            change = d.get('change', 0)
            leader = d.get('leader', '')
            emoji = "🟢" if change > 0 else "🔴"
            
            lines.append(f"{i}. {emoji} {name} {change:+.2f}%")
            if leader:
                lines.append(f"   领涨: {leader}")
        
        return '\n'.join(lines)
    
    def get_market_summary(self) -> str:
        """获取市场简报"""
        hot_concepts = self.get_hot_concepts(5)
        hot_industries = self.get_hot_industries(5)
        
        lines = ["📊 市场简报"]
        lines.append(f"更新时间: {datetime.now().strftime('%H:%M')}")
        
        if hot_concepts:
            lines.append("\n🔥 热门概念:")
            for c in hot_concepts:
                emoji = "🟢" if c['change'] > 0 else "🔴"
                lines.append(f"  {emoji} {c['name']} {c['change']:+.2f}%")
        
        if hot_industries:
            lines.append("\n📈 热门行业:")
            for ind in hot_industries:
                emoji = "🟢" if ind['change'] > 0 else "🔴"
                lines.append(f"  {emoji} {ind['name']} {ind['change']:+.2f}%")
        
        return '\n'.join(lines)