"""
AKShare数据采集工具
提供新闻舆情数据的获取功能
"""

import os
from datetime import datetime, timedelta
from typing import Dict, List
import json

try:
    import akshare as ak
    AKSHARE_AVAILABLE = True
except ImportError:
    AKSHARE_AVAILABLE = False
    print("警告: akshare未安装，将使用模拟数据")


class AKShareTools:
    """AKShare数据采集工具类"""
    
    def __init__(self):
        """初始化AKShare工具"""
        if AKSHARE_AVAILABLE:
            print("✅ AKShare初始化成功")
        else:
            print("⚠️ AKShare未安装，将使用模拟数据")
    
    def get_stock_news(self, stock_code: str, stock_name: str = "", days: int = 7) -> Dict:
        """
        获取个股相关新闻
        
        Args:
            stock_code: 股票代码（如 600519）
            stock_name: 股票名称（用于搜索）
            days: 获取天数
            
        Returns:
            新闻数据字典
        """
        # 提取纯股票代码
        pure_code = stock_code.split('.')[0] if '.' in stock_code else stock_code
        
        news_list = []
        
        if AKSHARE_AVAILABLE:
            try:
                # 尝试获取个股新闻
                df = ak.stock_news_em(symbol=pure_code)
                if df is not None and not df.empty:
                    # 取最近的新闻
                    for _, row in df.head(20).iterrows():
                        news_item = {
                            "title": row.get('新闻标题', ''),
                            "content": row.get('新闻内容', '')[:200] if row.get('新闻内容') else '',
                            "source": row.get('文章来源', ''),
                            "publish_time": str(row.get('发布时间', '')),
                            "url": row.get('新闻链接', '')
                        }
                        news_list.append(news_item)
            except Exception as e:
                print(f"获取个股新闻失败: {e}")
        
        # 如果没有获取到新闻，使用模拟数据
        if not news_list:
            news_list = self._mock_stock_news(pure_code, stock_name)
        
        # 分析新闻情绪
        sentiment_result = self._analyze_sentiment(news_list)
        
        return {
            "stock_code": stock_code,
            "stock_name": stock_name,
            "news_count": len(news_list),
            "news_list": news_list[:10],  # 最多返回10条
            "sentiment": sentiment_result
        }
    
    def get_market_news(self, limit: int = 10) -> List[Dict]:
        """
        获取市场热点新闻
        
        Args:
            limit: 获取条数
            
        Returns:
            新闻列表
        """
        news_list = []
        
        if AKSHARE_AVAILABLE:
            try:
                # 获取财经新闻
                df = ak.stock_info_global_em()
                if df is not None and not df.empty:
                    for _, row in df.head(limit).iterrows():
                        news_item = {
                            "title": row.get('标题', ''),
                            "content": row.get('内容', '')[:200] if row.get('内容') else '',
                            "publish_time": str(row.get('发布时间', ''))
                        }
                        news_list.append(news_item)
            except Exception as e:
                print(f"获取市场新闻失败: {e}")
        
        if not news_list:
            news_list = self._mock_market_news(limit)
        
        return news_list
    
    def get_industry_news(self, industry: str, limit: int = 5) -> List[Dict]:
        """
        获取行业新闻
        
        Args:
            industry: 行业名称
            limit: 获取条数
            
        Returns:
            新闻列表
        """
        # 行业新闻通常需要特定接口，这里简化处理
        return self._mock_industry_news(industry, limit)
    
    def get_market_sentiment(self) -> Dict:
        """
        获取市场情绪指标
        
        Returns:
            市场情绪数据
        """
        if AKSHARE_AVAILABLE:
            try:
                # 获取涨跌统计
                df = ak.stock_changes_em()
                if df is not None and not df.empty:
                    up_count = len(df[df.get('涨跌幅', 0) > 0]) if '涨跌幅' in df.columns else 0
                    down_count = len(df[df.get('涨跌幅', 0) < 0]) if '涨跌幅' in df.columns else 0
                    flat_count = len(df[df.get('涨跌幅', 0) == 0]) if '涨跌幅' in df.columns else 0
                    
                    total = up_count + down_count + flat_count
                    if total > 0:
                        up_ratio = up_count / total * 100
                        if up_ratio > 60:
                            mood = "乐观"
                        elif up_ratio < 40:
                            mood = "悲观"
                        else:
                            mood = "中性"
                        
                        return {
                            "up_count": up_count,
                            "down_count": down_count,
                            "flat_count": flat_count,
                            "up_ratio": round(up_ratio, 2),
                            "market_mood": mood,
                            "update_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
            except Exception as e:
                print(f"获取市场情绪失败: {e}")
        
        # 返回模拟数据
        import random
        up_ratio = random.uniform(30, 70)
        if up_ratio > 55:
            mood = "乐观"
        elif up_ratio < 45:
            mood = "悲观"
        else:
            mood = "中性"
        
        return {
            "up_count": int(up_ratio * 50),
            "down_count": int((100 - up_ratio) * 50),
            "flat_count": 100,
            "up_ratio": round(up_ratio, 2),
            "market_mood": mood,
            "update_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def _analyze_sentiment(self, news_list: List[Dict]) -> Dict:
        """
        分析新闻情绪
        
        Args:
            news_list: 新闻列表
            
        Returns:
            情绪分析结果
        """
        # 简化的情绪分析（基于关键词）
        positive_keywords = ['上涨', '增长', '利好', '突破', '创新高', '盈利', '超预期', '看好', '买入', '增持', '推荐']
        negative_keywords = ['下跌', '下滑', '利空', '亏损', '减持', '风险', '警告', '暴跌', '卖出', '减仓', '回调']
        
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        
        analyzed_news = []
        
        for news in news_list:
            title = news.get('title', '')
            content = news.get('content', '')
            text = title + content
            
            pos_score = sum(1 for kw in positive_keywords if kw in text)
            neg_score = sum(1 for kw in negative_keywords if kw in text)
            
            if pos_score > neg_score:
                sentiment = "利好"
                positive_count += 1
            elif neg_score > pos_score:
                sentiment = "利空"
                negative_count += 1
            else:
                sentiment = "中性"
                neutral_count += 1
            
            analyzed_news.append({
                **news,
                "sentiment": sentiment
            })
        
        total = positive_count + negative_count + neutral_count
        if total == 0:
            total = 1
        
        # 计算情绪评分（0-100）
        sentiment_score = 50 + (positive_count - negative_count) / total * 50
        sentiment_score = max(0, min(100, sentiment_score))
        
        # 判断整体情绪
        if sentiment_score > 60:
            overall = "乐观"
        elif sentiment_score < 40:
            overall = "悲观"
        else:
            overall = "中性"
        
        return {
            "positive_count": positive_count,
            "negative_count": negative_count,
            "neutral_count": neutral_count,
            "positive_pct": round(positive_count / total * 100, 1),
            "negative_pct": round(negative_count / total * 100, 1),
            "neutral_pct": round(neutral_count / total * 100, 1),
            "sentiment_score": round(sentiment_score),
            "overall_sentiment": overall,
            "analyzed_news": analyzed_news[:5]  # 返回前5条分析结果
        }
    
    def _mock_stock_news(self, stock_code: str, stock_name: str) -> List[Dict]:
        """生成模拟的个股新闻"""
        import random
        
        templates = [
            {"title": f"{stock_name}发布业绩预告，净利润同比增长{random.randint(10, 50)}%", "sentiment": "利好"},
            {"title": f"{stock_name}获得机构调研，多家券商给予买入评级", "sentiment": "利好"},
            {"title": f"{stock_name}签署重大合同，金额达{random.randint(1, 10)}亿元", "sentiment": "利好"},
            {"title": f"{stock_name}股东减持计划公告", "sentiment": "利空"},
            {"title": f"{stock_name}发布新产品，市场反应平淡", "sentiment": "中性"},
            {"title": f"行业分析：{stock_name}所在行业面临调整", "sentiment": "中性"},
            {"title": f"{stock_name}高管增持公司股份", "sentiment": "利好"},
            {"title": f"{stock_name}收到监管问询函", "sentiment": "利空"},
        ]
        
        selected = random.sample(templates, min(6, len(templates)))
        
        news_list = []
        for i, item in enumerate(selected):
            news_list.append({
                "title": item["title"],
                "content": f"这是关于{stock_name}的详细新闻内容...",
                "source": random.choice(["东方财富", "同花顺", "新浪财经", "证券时报"]),
                "publish_time": (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d %H:%M'),
                "url": f"https://example.com/news/{i}",
                "sentiment": item["sentiment"]
            })
        
        return news_list
    
    def _mock_market_news(self, limit: int) -> List[Dict]:
        """生成模拟的市场新闻"""
        import random
        
        templates = [
            "央行宣布货币政策维持稳健中性",
            "北向资金今日净流入超50亿元",
            "科技板块持续走强，半导体概念领涨",
            "新能源汽车销量创新高",
            "房地产调控政策进一步优化",
            "A股市场成交额突破万亿",
            "外资机构看好中国经济增长前景",
            "多家上市公司披露回购计划"
        ]
        
        news_list = []
        for i, title in enumerate(random.sample(templates, min(limit, len(templates)))):
            news_list.append({
                "title": title,
                "content": f"{title}的详细内容...",
                "publish_time": (datetime.now() - timedelta(hours=i*2)).strftime('%Y-%m-%d %H:%M')
            })
        
        return news_list
    
    def _mock_industry_news(self, industry: str, limit: int) -> List[Dict]:
        """生成模拟的行业新闻"""
        import random
        
        templates = [
            f"{industry}行业景气度持续上升",
            f"{industry}板块获资金关注",
            f"政策利好{industry}行业发展",
            f"{industry}龙头企业业绩超预期",
            f"{industry}行业竞争格局分析"
        ]
        
        news_list = []
        for i, title in enumerate(templates[:limit]):
            news_list.append({
                "title": title,
                "content": f"{title}的详细内容...",
                "publish_time": (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d %H:%M')
            })
        
        return news_list
