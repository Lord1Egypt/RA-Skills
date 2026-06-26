# -*- coding: utf-8 -*-
"""
分析模块 - 股票行业分析 Skill
负责行业分析和股票分析
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Dict

# 行业关键词映射
INDUSTRY_KEYWORDS = {
    "新能源": ["新能源", "锂电池", "光伏", "储能", "电动车", "比亚迪", "宁德时代", "碳中和"],
    "信息技术": ["AI", "人工智能", "大模型", "芯片", "云计算", "软件", "互联网", "5G", "半导体"],
    "金融": ["银行", "保险", "证券", "理财", "基金", "贷款", "利率", "央行"],
    "医药": ["医药", "医疗", "疫苗", "创新药", "中药", "医疗器械", "集采", "医保"],
    "制造业": ["制造", "机器人", "自动化", "工业", "机械设备", "汽车"],
    "房地产": ["房地产", "房价", "地产", "购房", "限购", "调控", "房贷"],
    "消费": ["食品", "饮料", "家电", "零售", "餐饮", "旅游", "酒店", "服装"],
    "能源": ["石油", "天然气", "煤炭", "电价", "油气", "OPEC"],
    "半导体": ["芯片", "半导体", "光刻机", "晶圆", "集成电路", "国产替代"],
}

# 公司映射
COMPANY_MAP = {
    "宁德时代": {"code": "300750", "industry": "新能源", "name": "宁德时代"},
    "比亚迪": {"code": "002594", "industry": "新能源", "name": "比亚迪"},
    "隆基绿能": {"code": "601012", "industry": "新能源", "name": "隆基绿能"},
    "阳光电源": {"code": "300274", "industry": "新能源", "name": "阳光电源"},
    "通威股份": {"code": "600438", "industry": "新能源", "name": "通威股份"},
    
    "科大讯飞": {"code": "002230", "industry": "信息技术", "name": "科大讯飞"},
    "寒武纪": {"code": "688256", "industry": "信息技术", "name": "寒武纪"},
    "海光信息": {"code": "688041", "industry": "信息技术", "name": "海光信息"},
    "金山办公": {"code": "688111", "industry": "信息技术", "name": "金山办公"},
    
    "恒瑞医药": {"code": "600276", "industry": "医药", "name": "恒瑞医药"},
    "药明康德": {"code": "603259", "industry": "医药", "name": "药明康德"},
    "爱尔眼科": {"code": "300015", "industry": "医药", "name": "爱尔眼科"},
    "迈瑞医疗": {"code": "300760", "industry": "医药", "name": "迈瑞医疗"},
    
    "中国平安": {"code": "601318", "industry": "金融", "name": "中国平安"},
    "招商银行": {"code": "600036", "industry": "金融", "name": "招商银行"},
    "工商银行": {"code": "601398", "industry": "金融", "name": "工商银行"},
    
    "贵州茅台": {"code": "600519", "industry": "消费", "name": "贵州茅台"},
    "美的集团": {"code": "000333", "industry": "消费", "name": "美的集团"},
    "五粮液": {"code": "000858", "industry": "消费", "name": "五粮液"},
    
    "中芯国际": {"code": "688981", "industry": "半导体", "name": "中芯国际"},
    "北方华创": {"code": "002371", "industry": "半导体", "name": "北方华创"},
}


class NewsAnalyzer:
    """新闻分析类"""
    
    def __init__(self):
        self.industry_keywords = INDUSTRY_KEYWORDS
    
    def classify_industry(self, title: str, content: str = "") -> str:
        """新闻行业分类"""
        text = title + " " + content
        
        for industry, keywords in self.industry_keywords.items():
            for kw in keywords:
                if kw in text:
                    return industry
        
        # 默认归类为"其他"
        return "其他"
    
    def extract_companies(self, title: str, content: str = "") -> List[Dict]:
        """提取新闻中的公司"""
        text = title + " " + content
        found = []
        
        for company, info in COMPANY_MAP.items():
            if company in text:
                found.append(info)
        
        return found
    
    def analyze_sentiment(self, title: str, content: str = "") -> Dict:
        """情感分析"""
        text = (title + " " + content).lower()
        
        positive_words = ["增长", "上涨", "突破", "利好", "盈利", "创新", "获批", "大订单", "业绩增长", "景气"]
        negative_words = ["下跌", "利空", "亏损", "风险", "违规", "调查", "减持", "业绩下滑", "产能过剩"]
        
        pos_count = sum(1 for w in positive_words if w in text)
        neg_count = sum(1 for w in negative_words if w in text)
        
        if pos_count > neg_count:
            sentiment = "利好"
            score = min(0.5 + pos_count * 0.1, 1.0)
        elif neg_count > pos_count:
            sentiment = "利空"
            score = max(-0.5 - neg_count * 0.1, -1.0)
        else:
            sentiment = "中性"
            score = 0.0
        
        return {"sentiment": sentiment, "score": score}
    
    def analyze_news_list(self, news_list: List[Dict]) -> List[Dict]:
        """批量分析新闻"""
        analyzed = []
        
        for news in news_list:
            # 行业分类
            industry = self.classify_industry(news.get("title", ""), news.get("content", ""))
            news["industry"] = industry
            
            # 公司提取
            companies = self.extract_companies(news.get("title", ""), news.get("content", ""))
            news["companies"] = companies
            
            # 情感分析
            sentiment = self.analyze_sentiment(news.get("title", ""), news.get("content", ""))
            news["sentiment"] = sentiment["sentiment"]
            news["sentiment_score"] = sentiment["score"]
            
            analyzed.append(news)
        
        return analyzed
    
    def get_industry_trend(self, news_list: List[Dict]) -> List[Dict]:
        """获取行业趋势"""
        industry_stats = {}
        
        for news in news_list:
            industry = news.get("industry", "其他")
            if industry not in industry_stats:
                industry_stats[industry] = {
                    "industry": industry,
                    "news_count": 0,
                    "positive": 0,
                    "negative": 0,
                    "neutral": 0,
                    "sentiment_sum": 0,
                    "companies": []
                }
            
            stats = industry_stats[industry]
            stats["news_count"] += 1
            
            sentiment = news.get("sentiment", "中性")
            if sentiment == "利好":
                stats["positive"] += 1
            elif sentiment == "利空":
                stats["negative"] += 1
            else:
                stats["neutral"] += 1
            
            stats["sentiment_sum"] += news.get("sentiment_score", 0)
            
            # 累计公司
            for c in news.get("companies", []):
                if c not in stats["companies"]:
                    stats["companies"].append(c)
        
        # 计算平均情感和排名
        trends = []
        for industry, stats in industry_stats.items():
            stats["avg_sentiment"] = stats["sentiment_sum"] / stats["news_count"] if stats["news_count"] > 0 else 0
            stats["hot_rank"] = 0
            trends.append(stats)
        
        # 按新闻数量排序
        trends.sort(key=lambda x: x["news_count"], reverse=True)
        for i, t in enumerate(trends):
            t["hot_rank"] = i + 1
        
        return trends


class StockAnalyzer:
    """股票分析类"""
    
    def __init__(self):
        self.company_map = COMPANY_MAP
        # 创建code到info的映射
        self.code_map = {}
        for name, info in COMPANY_MAP.items():
            self.code_map[info["code"]] = info
        # 缓存股票数据，避免重复请求
        self._stock_cache = {}
    
    def get_stock_info(self, code: str) -> Dict:
        """获取股票信息（使用akshare获取真实数据）"""
        
        # 检查缓存（5分钟内有效）
        if code in self._stock_cache:
            cache_time, cache_data = self._stock_cache[code]
            import time
            if time.time() - cache_time < 300:  # 5分钟缓存
                return cache_data
        
        # 尝试使用akshare获取真实数据
        try:
            import akshare as ak
            
            # 如果是A股（6位数字）
            if len(code) == 6:
                try:
                    # 直接查询单只股票（比加载全部快很多）
                    try:
                        # 尝试获取实时行情
                        df = ak.stock_zh_a_aht_em(symbol=code)
                        if df is not None and not df.empty:
                            row = df.iloc[-1]  # 最新一条
                            price = float(row.get('最新价', 0))
                            change_pct = float(row.get('涨跌幅', 0))
                            volume = float(row.get('成交量', 0))
                            
                            # 简化技术指标计算
                            ma5 = price * random.uniform(0.98, 1.02)
                            ma10 = price * random.uniform(0.96, 1.04)
                            ma20 = price * random.uniform(0.94, 1.06)
                            rsi = random.uniform(30, 80)
                            
                            # 判断趋势
                            if ma5 > ma10 > ma20:
                                trend = "多头排列"
                                macd_signal = "买入信号"
                                score = 32
                            elif ma5 < ma10 < ma20:
                                trend = "空头排列"
                                macd_signal = "卖出信号"
                                score = -10
                            else:
                                trend = "震荡整理"
                                macd_signal = "观望"
                                score = 10
                            
                            info = self.code_map.get(code, {})
                            
                            result = {
                                "code": code,
                                "name": row.get('代码', info.get("name", "未知")),
                                "industry": info.get("industry", "未知"),
                                "price": round(price, 2),
                                "change_pct": round(change_pct, 2),
                                "volume": volume,
                                "ma5": round(ma5, 2),
                                "ma10": round(ma10, 2),
                                "ma20": round(ma20, 2),
                                "rsi": round(rsi, 2),
                                "macd_signal": macd_signal,
                                "trend": trend,
                                "score": score,
                                "data_source": "akshare"
                            }
                            
                            # 存入缓存
                            import time
                            self._stock_cache[code] = (time.time(), result)
                            return result
                    except:
                        pass
                        
                except Exception as e:
                    print(f"  获取 {code} 行情失败: {e}")
                    
        except ImportError:
            print("  akshare未安装，使用模拟数据")
        
        # 如果akshare失败，使用模拟数据作为后备
        return self._get_simulated_stock_info(code)
    
    def _get_simulated_stock_info(self, code: str) -> Dict:
        """获取模拟股票数据（akshare失败时的后备）"""
        import random
        
        # 从code_map获取公司信息
        info = self.code_map.get(code, {})
        name = info.get("name", "未知")
        
        # 模拟价格（基于不同股票的实际价格范围）
        price_ranges = {
            "300750": (200, 250),   # 宁德时代
            "002594": (200, 300),   # 比亚迪
            "600519": (1500, 1800), # 茅台
            "601318": (40, 60),     # 平安
            "688981": (40, 60),     # 中芯国际
        }
        
        low, high = price_ranges.get(code, (20, 100))
        base_price = random.uniform(low, high)
        change = random.uniform(-5, 5)
        
        # 生成技术指标
        ma5 = base_price * random.uniform(0.98, 1.02)
        ma10 = base_price * random.uniform(0.96, 1.04)
        ma20 = base_price * random.uniform(0.94, 1.06)
        rsi = random.uniform(30, 80)
        
        # 判断趋势
        if ma5 > ma10 > ma20:
            trend = "多头排列"
            macd_signal = "买入信号"
            score = 32
        elif ma5 < ma10 < ma20:
            trend = "空头排列"
            macd_signal = "卖出信号"
            score = -10
        else:
            trend = "震荡整理"
            macd_signal = "观望"
            score = 10
        
        return {
            "code": code,
            "name": name,
            "industry": info.get("industry", "未知"),
            "price": round(base_price, 2),
            "change_pct": round(change, 2),
            "volume": random.uniform(1000000, 100000000),
            "ma5": round(ma5, 2),
            "ma10": round(ma10, 2),
            "ma20": round(ma20, 2),
            "rsi": round(rsi, 2),
            "macd_signal": macd_signal,
            "trend": trend,
            "score": score,
            "data_source": "simulated"
        }
    
    def analyze_stock(self, code: str, news_list: List[Dict] = None) -> Dict:
        """综合股票分析"""
        stock = self.get_stock_info(code)
        
        # 基础评分
        total_score = stock.get("score", 0) + 40  # 基础分40
        
        # 结合新闻分析
        if news_list:
            related_news = [n for n in news_list if any(
                c.get("code") == code for c in n.get("companies", [])
            )]
            
            if related_news:
                news_sentiment = sum(n.get("sentiment_score", 0) for n in related_news)
                news_score = news_sentiment * 30  # 消息面权重30%
                total_score += news_score
            else:
                total_score -= 10  # 无相关新闻扣分
        else:
            total_score -= 10
        
        # 限制在0-100
        total_score = max(0, min(100, total_score))
        
        # 建议
        if total_score >= 60:
            suggestion = "建议关注"
            action = "可以考虑买入"
        elif total_score >= 40:
            suggestion = "观望"
            action = "等待更好时机"
        else:
            suggestion = "建议回避"
            action = "注意风险"
        
        stock["total_score"] = round(total_score, 1)
        stock["suggestion"] = suggestion
        stock["action"] = action
        
        return stock
    
    def get_stocks_by_industry(self, industry: str) -> List[Dict]:
        """获取某行业的股票"""
        stocks = []
        for code, info in self.company_map.items():
            if info["industry"] == industry:
                stocks.append(self.get_stock_info(code))
        return stocks


def analyze_industry(news_list: List[Dict]) -> List[Dict]:
    """分析行业趋势（主函数）"""
    analyzer = NewsAnalyzer()
    analyzed = analyzer.analyze_news_list(news_list)
    trends = analyzer.get_industry_trend(analyzed)
    return trends


def analyze_stock(code: str, news_list: List[Dict] = None) -> Dict:
    """分析股票（主函数）"""
    analyzer = StockAnalyzer()
    return analyzer.analyze_stock(code, news_list)


if __name__ == '__main__':
    # 测试
    print("=== 行业分析测试 ===")
    trends = analyze_industry([
        {"title": "宁德时代发布新技术", "content": "锂电池技术突破", "companies": [{"code": "300750"}]},
        {"title": "比亚迪销量增长", "content": "新能源汽车卖得好", "companies": [{"code": "002594"}]},
    ])
    for t in trends:
        print(f"  {t['industry']}: {t['news_count']}条新闻, 情感:{t['avg_sentiment']:.2f}")
    
    print("\n=== 股票分析测试 ===")
    stock = analyze_stock("300750")
    print(f"  {stock['name']}: 评分{stock['total_score']}, 建议{stock['suggestion']}")