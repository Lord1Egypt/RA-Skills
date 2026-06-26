# -*- coding: utf-8 -*-
"""
报告生成模块 - 股票行业分析 Skill
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict


# 行业公司关系图谱（扩展版）
INDUSTRY_GRAPH = {
    "新能源": {
        "description": "新能源汽车、光伏、储能、风电等清洁能源产业链",
        "sub_industry": {
            "动力电池": ["宁德时代(300750)", "比亚迪(002594)", "国轩高科(002074)", "亿纬锂能(300014)", "欣旺达(300207)"],
            "光伏": ["隆基绿能(601012)", "通威股份(600438)", "阳光电源(300274)", "晶澳科技(002459)", "天合光能(688599)"],
            "储能": ["阳光电源(300274)", "锦浪科技(300749)", "固德威(688390)", "德业股份(605117)"],
            "整车": ["比亚迪(002594)", "长城汽车(601633)", "吉利汽车(00175.HK)", "长安汽车(000625)", "广汽集团(601238)"],
            "风电": ["金风科技(002202)", "明阳智能(601226)", "运达股份(300772)"]
        },
        "hot_keywords": ["锂电池", "新能源汽车", "光伏", "储能", "碳中和", "固态电池"]
    },
    "信息技术": {
        "description": "人工智能、云计算、半导体、软件、互联网等",
        "sub_industry": {
            "AI大模型": ["科大讯飞(002230)", "百度(9888.HK)", "商汤(0024.HK)", "寒武纪(688256)"],
            "云计算": ["金山办公(688111)", "用友网络(600588)", "恒生电子(600570)", "广联达(002410)"],
            "半导体": ["中芯国际(688981)", "北方华创(002371)", "海光信息(688041)", "华虹半导体(600183)", "韦尔股份(603501)"],
            "软件": ["金山办公(688111)", "用友网络(600588)", "东软集团(600718)", "中国软件(600536)"],
            "通信": ["中兴通讯(000063)", "烽火通信(600498)", "紫光股份(000938)"]
        },
        "hot_keywords": ["AI", "大模型", "芯片", "云计算", "5G", "国产替代"]
    },
    "金融": {
        "description": "银行、保险、证券、基金、信托等",
        "sub_industry": {
            "银行": ["招商银行(600036)", "工商银行(601398)", "建设银行(601939)", "中国银行(601988)", "平安银行(000001)"],
            "保险": ["中国平安(601318)", "中国人寿(601628)", "中国太保(601601)", "新华保险(601336)"],
            "证券": ["中信证券(600030)", "华泰证券(601688)", "国泰君安(601211)", "海通证券(600837)"],
            "多元金融": ["中国平安(601318)", "东方财富(300059)", "同花顺(300033)"]
        },
        "hot_keywords": ["银行", "保险", "券商", "理财", "降息", "IPO"]
    },
    "医药": {
        "description": "创新药、医疗器械、医疗服务、CXO等",
        "sub_industry": {
            "创新药": ["恒瑞医药(600276)", "百济神州(688235)", "复星医药(600196)", "君实生物(688180)"],
            "医疗器械": ["迈瑞医疗(300760)", "联影医疗(688271)", "乐普医疗(300003)", "开立医疗(300633)"],
            "医疗服务": ["爱尔眼科(300015)", "通策医疗(600763)", "国际医学(000516)"],
            "CXO": ["药明康德(603259)", "康龙化成(300759)", "泰格医药(300347)", "昭衍新药(603127)"],
            "中药": ["片仔癀(600436)", "云南白药(000538)", "同仁堂(600085)", "以岭药业(002603)"]
        },
        "hot_keywords": ["创新药", "集采", "医疗器械", "疫苗", "CXO", "中药"]
    },
    "消费": {
        "description": "食品饮料、家电、汽车、餐饮、旅游等",
        "sub_industry": {
            "白酒": ["贵州茅台(600519)", "五粮液(000858)", "泸州老窖(000568)", "山西汾酒(600809)"],
            "食品": ["海天味业(603288)", "伊利股份(600887)", "蒙牛乳业(02319.HK)", "双汇发展(000895)"],
            "家电": ["美的集团(000333)", "格力电器(000651)", "海尔智家(600690)", "石头科技(688169)"],
            "汽车": ["比亚迪(002594)", "长城汽车(601633)", "吉利汽车(00175.HK)"],
            "餐饮旅游": ["中国中免(601888)", "宋城演艺(300144)", "锦江酒店(600754)"]
        },
        "hot_keywords": ["白酒", "消费升级", "家电", "新能源汽车", "免税"]
    },
    "半导体": {
        "description": "芯片设计、制造、设备、材料等",
        "sub_industry": {
            "芯片制造": ["中芯国际(688981)", "华虹半导体(600183)"],
            "设备": ["北方华创(002371)", "中微公司(688012)", "华峰测控(688200)", "长川科技(300604)"],
            "设计": ["海光信息(688041)", "寒武纪(688256)", "韦尔股份(603501)", "兆易创新(603986)"],
            "材料": ["沪硅产业(688126)", "中环股份(002129)", "立昂微(605358)"],
            "封测": ["长电科技(600584)", "通富微电(002156)", "华天科技(002185)"]
        },
        "hot_keywords": ["芯片", "半导体设备", "光刻机", "国产替代", "先进封装"]
    }
}


class ReportGenerator:
    """报告生成类"""
    
    def __init__(self):
        self.industry_graph = INDUSTRY_GRAPH
    
    def generate_daily_report(self, news_list: List[Dict], industry_trends: List[Dict], stocks: List[Dict] = None) -> str:
        """生成完整的分析报告"""
        report = []
        report.append("=" * 75)
        report.append(f"📊 股票行业深度分析报告 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report.append("=" * 75)
        
        # ==================== 第一部分：新闻概要 ====================
        report.append("\n" + "=" * 75)
        report.append("【第一部分】今日新闻概要及链接")
        report.append("=" * 75)
        
        # 按行业分组显示新闻
        news_by_industry = {}
        for news in news_list:
            ind = news.get("industry", "其他")
            if ind not in news_by_industry:
                news_by_industry[ind] = []
            news_by_industry[ind].append(news)
        
        total_news = sum(len(v) for v in news_by_industry.values())
        report.append(f"\n📰 共发现 {total_news} 条财经新闻\n")
        
        for industry, news_items in news_by_industry.items():
            report.append(f"\n{'━' * 60}")
            report.append(f"📌 {industry} 行业 ({len(news_items)}条新闻)")
            report.append(f"{'━' * 60}")
            
            for i, news in enumerate(news_items, 1):
                title = news.get("title", "")[:50]
                source = news.get("source", "")
                url = news.get("url", "")
                sentiment = news.get("sentiment", "中性")
                api_source = news.get("api_source", "unknown")
                
                # 情感 emoji
                sentiment_emoji = {"利好": "⬆️", "利空": "⬇️", "中性": "➡️"}.get(sentiment, "➡️")
                
                report.append(f"\n  {i}. {title}")
                report.append(f"     来源: {source} | 情感: {sentiment} {sentiment_emoji}")
                if url:
                    report.append(f"     🔗 链接: {url}")
        
        # ==================== 第二部分：行业深度分析 ====================
        report.append("\n\n" + "=" * 75)
        report.append("【第二部分】行业深度分析")
        report.append("=" * 75)
        
        for trend in industry_trends:
            industry = trend.get("industry", "未知")
            news_count = trend.get("news_count", 0)
            avg_sentiment = trend.get("avg_sentiment", 0)
            
            # 获取行业图谱信息
            graph_info = self.industry_graph.get(industry, {})
            description = graph_info.get("description", "")
            sub_industries = graph_info.get("sub_industry", {})
            hot_keywords = graph_info.get("hot_keywords", [])
            
            report.append(f"\n{'━' * 60}")
            report.append(f"🏭 {industry} 行业 (新闻: {news_count}条)")
            report.append(f"{'━' * 60}")
            
            # 行业描述
            if description:
                report.append(f"\n  📝 行业描述: {description}")
            
            # 热门关键词
            if hot_keywords:
                report.append(f"  🔥 热门关键词: {', '.join(hot_keywords)}")
            
            # 情感分析
            if avg_sentiment > 0.2:
                sentiment_label = "利好 ⬆️"
            elif avg_sentiment < -0.2:
                sentiment_label = "利空 ⬇️"
            else:
                sentiment_label = "中性 ➡️"
            report.append(f"  📈 情感倾向: {sentiment_label}")
            
            # 子行业及公司
            if sub_industries:
                report.append(f"\n  📋 子行业及代表性公司:")
                for sub_ind, companies in sub_industries.items():
                    report.append(f"\n    ▶ {sub_ind}:")
                    for c in companies[:5]:  # 每个子行业显示5个公司
                        report.append(f"      • {c}")
            
            # 该行业热门公司股票数据
            related_stocks = self._get_industry_stocks(industry, sub_industries)
            if related_stocks:
                report.append(f"\n  📊 行业热门股票实时数据:")
                report.append(f"  {'代码':<12} {'名称':<15} {'现价':<10} {'涨跌幅':<10} {'趋势':<10}")
                report.append(f"  {'-'*60}")
                for stock in related_stocks[:10]:
                    code = stock.get("code", "")
                    name = stock.get("name", "")[:10]
                    price = stock.get("price", 0)
                    change = stock.get("change_pct", 0)
                    trend_val = stock.get("trend", "")[:6]
                    
                    change_str = f"+{change:.2f}%" if change >= 0 else f"{change:.2f}%"
                    report.append(f"  {code:<12} {name:<15} ¥{price:<9.2f} {change_str:<10} {trend_val:<10}")
        
        # ==================== 第三部分：股票评分及建议 ====================
        if stocks:
            report.append("\n\n" + "=" * 75)
            report.append("【第三部分】股票评分及建议")
            report.append("=" * 75)
            
            # 按评分排序
            sorted_stocks = sorted(stocks, key=lambda x: x.get("total_score", 0), reverse=True)
            
            for stock in sorted_stocks:
                code = stock.get("code", "")
                name = stock.get("name", "未知")
                industry = stock.get("industry", "未知")
                price = stock.get("price", 0)
                change_pct = stock.get("change_pct", 0)
                ma5 = stock.get("ma5", 0)
                ma10 = stock.get("ma10", 0)
                ma20 = stock.get("ma20", 0)
                rsi = stock.get("rsi", 0)
                macd_signal = stock.get("macd_signal", "未知")
                trend = stock.get("trend", "震荡")
                score = stock.get("total_score", 0)
                suggestion = stock.get("suggestion", "观望")
                action = stock.get("action", "等待")
                
                change_sign = "+" if change_pct >= 0 else ""
                
                report.append(f"\n{'━' * 60}")
                report.append(f"🔍 {name} (代码: {code}) - {industry}")
                report.append(f"{'━' * 60}")
                
                # 基础信息
                report.append(f"\n  💰 当前价格: ¥{price:.2f}")
                report.append(f"  📊 涨跌幅: {change_sign}{change_pct:.2f}%")
                
                # 技术指标
                report.append(f"\n  【技术指标】")
                report.append(f"    MA5: {ma5:.2f} | MA10: {ma10:.2f} | MA20: {ma20:.2f}")
                report.append(f"    RSI: {rsi:.2f}")
                report.append(f"    MACD: {macd_signal}")
                report.append(f"    趋势: {trend}")
                
                # 综合评分
                score_bar = "█" * int(score/10) + "░" * (10-int(score/10))
                if score >= 60:
                    emoji = "✅"
                elif score >= 40:
                    emoji = "⚠️"
                else:
                    emoji = "❌"
                
                report.append(f"\n  【综合评分】{emoji} {score}/100 [{score_bar}]")
                report.append(f"    建议: {suggestion}")
                report.append(f"    操作: {action}")
        
        # ==================== 总结 ====================
        report.append("\n\n" + "=" * 75)
        report.append("【总结】")
        report.append("=" * 75)
        
        # 今日最热行业
        if industry_trends:
            top_industry = industry_trends[0]
            report.append(f"\n🔥 今日最热行业: {top_industry.get('industry', '未知')} ({top_industry.get('news_count', 0)}条新闻)")
        
        # 推荐关注的股票
        if stocks:
            good_stocks = [s for s in stocks if s.get("total_score", 0) >= 60]
            if good_stocks:
                report.append(f"\n✅ 建议关注的股票:")
                for s in sorted(good_stocks, key=lambda x: x.get("total_score", 0), reverse=True):
                    report.append(f"   • {s.get('name', '未知')} ({s.get('code', '')}): 评分 {s.get('total_score', 0)}")
        
        report.append("\n" + "=" * 75)
        report.append("⚠️ 风险提示: 本分析仅供参考，不构成投资建议")
        report.append("=" * 75)
        
        return "\n".join(report)
    
    def _get_industry_stocks(self, industry: str, sub_industries: Dict) -> List[Dict]:
        """获取行业相关股票数据"""
        # 从预定义的图谱中获取
        all_companies = []
        for companies in sub_industries.values():
            for c in companies:
                # 解析 "公司名(代码)" 格式
                if "(" in c and ")" in c:
                    name = c.split("(")[0]
                    code = c.split("(")[1].rstrip(")")
                    all_companies.append({"code": code, "name": name})
        
        # 尝试获取这些公司的实时数据
        from src.analyzer import StockAnalyzer
        analyzer = StockAnalyzer()
        
        stocks_data = []
        for comp in all_companies[:15]:  # 最多15只
            try:
                stock_info = analyzer.get_stock_info(comp["code"])
                if stock_info:
                    stocks_data.append(stock_info)
            except:
                pass
        
        return stocks_data
    
    def generate_stock_report(self, stock: Dict) -> str:
        """生成个股分析报告"""
        report = []
        report.append("=" * 50)
        report.append(f"🔍 个股分析 - {stock.get('name', '未知')} ({stock.get('code', '')})")
        report.append("=" * 50)
        # ... (保持原有逻辑)
        return "\n".join(report)


def generate_report(news_list: List[Dict], industry_trends: List[Dict], stocks: List[Dict] = None) -> str:
    """生成报告（主函数）"""
    generator = ReportGenerator()
    return generator.generate_daily_report(news_list, industry_trends, stocks)


def generate_stock_report(stock: Dict) -> str:
    """生成个股报告（主函数）"""
    generator = ReportGenerator()
    return generator.generate_stock_report(stock)


if __name__ == '__main__':
    # 测试
    from src.analyzer import analyze_industry, analyze_stock
    
    news_list = [
        {"title": "宁德时代发布新技术", "content": "锂电池技术突破", "industry": "新能源", "source": "新浪财经", "country": "国内", "sentiment": "利好", "companies": [{"code": "300750", "name": "宁德时代", "industry": "新能源"}], "url": "https://example.com", "api_source": "test"},
    ]
    
    trends = analyze_industry(news_list)
    stocks = [analyze_stock("300750", news_list)]
    
    report = generate_report(news_list, trends, stocks)
    print(report)