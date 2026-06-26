"""
TOC Trading System - 股票推荐服务
集成 AKShare 免费数据源
"""
import uuid
from typing import Dict, List, Optional, Tuple
from datetime import datetime

# 尝试导入 AKShare
try:
    import akshare as ak
    from akshare_client import AKShareClient
    AKSHARE_AVAILABLE = True
except ImportError:
    AKSHARE_AVAILABLE = False

from data.storage import Storage

class RecommendationService:
    """股票推荐服务"""
    
    def __init__(self, storage: Storage = None):
        self.storage = storage or Storage()
        self.akshare = AKShareClient() if AKSHARE_AVAILABLE else None
    
    def get_industry_analysis(self, category: str) -> str:
        """获取行业分析"""
        if not self.akshare:
            return "❌ 数据源不可用"
        return self.akshare.format_industry_analysis(category)
    
    def get_market_summary(self) -> str:
        """获取市场简报"""
        if not self.akshare:
            return "❌ 数据源不可用"
        return self.akshare.get_market_summary()
    
    def get_all_industries_analysis(self) -> str:
        """获取四大行业分析"""
        categories = ['AI/人工智能', '消费品', '汽车', '医疗']
        results = []
        
        for cat in categories:
            analysis = self.get_industry_analysis(cat)
            results.append(analysis)
        
        header = "📊 四大行业板块分析\n"
        header += "=" * 40
        header += "\n"
        
        return header + "\n\n".join(results)
    
    def get_hot_concepts(self, limit: int = 10) -> List[Dict]:
        """获取热门概念"""
        if not self.akshare:
            return []
        return self.akshare.get_hot_concepts(limit)
    
    def get_hot_industries(self, limit: int = 10) -> List[Dict]:
        """获取热门行业"""
        if not self.akshare:
            return []
        return self.akshare.get_hot_industries(limit)
    
    def format_recommendations(self, recommendations: List[Dict], title: str = "📊 今日推荐") -> str:
        """格式化推荐结果"""
        if not recommendations:
            return f"{title}\n暂无推荐"
        
        lines = [title]
        
        for i, r in enumerate(recommendations, 1):
            name = r.get('name', '-')
            code = r.get('code', '-')
            price = r.get('close', r.get('price', '-'))
            change = r.get('pct_chg', r.get('change_pct', 0))
            reason = r.get('reason', '')
            tags = ' '.join(r.get('tags', []))
            
            if isinstance(price, (int, float)):
                price_str = f"{price:.2f}"
            else:
                price_str = str(price)
            
            if isinstance(change, (int, float)):
                change_str = f"{change:+.2f}%"
            else:
                change_str = '-'
            
            lines.append(f"\n**{i}. {name}({code})** {tags}")
            lines.append(f"- 价格：{price_str} ({change_str})")
            if reason:
                lines.append(f"- 原因：{reason}")
        
        return '\n'.join(lines)
    
    def save_recommendation(self, stock: Dict, rec_type: str) -> bool:
        """保存推荐记录"""
        data = self.storage.get_recommendations()
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        daily_found = False
        for daily in data.get('daily_stocks', []):
            if daily.get('date') == today:
                daily['stocks'].append({
                    'id': str(uuid.uuid4())[:8],
                    'stock_code': stock.get('code', ''),
                    'stock_name': stock.get('name', ''),
                    'type': rec_type,
                    'price': stock.get('close', 0),
                    'change_pct': stock.get('pct_chg', 0),
                    'reason': stock.get('reason', ''),
                    'industry': stock.get('industry', ''),
                    'tags': stock.get('tags', []),
                    'created_at': datetime.now().isoformat()
                })
                daily_found = True
                break
        
        if not daily_found:
            data.setdefault('daily_stocks', []).append({
                'date': today,
                'stocks': [{
                    'id': str(uuid.uuid4())[:8],
                    'stock_code': stock.get('code', ''),
                    'stock_name': stock.get('name', ''),
                    'type': rec_type,
                    'price': stock.get('close', 0),
                    'change_pct': stock.get('pct_chg', 0),
                    'reason': stock.get('reason', ''),
                    'industry': stock.get('industry', ''),
                    'tags': stock.get('tags', []),
                    'created_at': datetime.now().isoformat()
                }]
            })
        
        return self.storage.save_recommendations(data)
    
    def get_today_recommendations(self) -> List[Dict]:
        """获取今日推荐"""
        data = self.storage.get_recommendations()
        today = datetime.now().strftime('%Y-%m-%d')
        
        for daily in data.get('daily_stocks', []):
            if daily.get('date') == today:
                return daily.get('stocks', [])
        
        return []
    
    def get_hot_signals(self) -> str:
        """获取今日热门信号汇总"""
        if not self.akshare:
            return "📊 今日市场信号\n数据源不可用"
        
        signals = []
        
        # 热门概念
        hot_concepts = self.akshare.get_hot_concepts(5)
        if hot_concepts:
            signals.append("🔥 **热门概念 TOP5**：")
            for s in hot_concepts:
                emoji = "🟢" if s['change'] > 0 else "🔴"
                signals.append(f"  {emoji} {s['name']} {s['change']:+.2f}%")
        
        # 热门行业
        hot_industries = self.akshare.get_hot_industries(5)
        if hot_industries:
            signals.append(f"\n📈 **热门行业 TOP5**：")
            for s in hot_industries:
                emoji = "🟢" if s['change'] > 0 else "🔴"
                signals.append(f"  {emoji} {s['name']} {s['change']:+.2f}%")
        
        if not signals:
            return "📊 今日市场信号\n暂无热门信号"
        
        return "📊 今日市场信号\n" + "\n".join(signals)