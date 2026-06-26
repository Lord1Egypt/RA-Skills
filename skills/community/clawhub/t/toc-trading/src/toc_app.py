"""
TOC Trading System - 主入口
"""
import sys
import os
from typing import Dict

# 添加 src 目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from command_parser import Parser, CommandType
from data.storage import Storage
from tushare_client import TushareClient
from services.stock_pool import StockPoolService
from services.position import PositionService
from services.recommendation import RecommendationService
from services.challenge import ChallengeService

class TOCTTrading:
    """TOC 模拟交易系统"""
    
    def __init__(self):
        self.storage = Storage()
        self.tushare = TushareClient()
        self.parser = Parser()
        self.stock_pool = StockPoolService(self.storage, self.tushare)
        self.position = PositionService(self.storage, self.tushare)
        self.recommendation = RecommendationService(self.storage)
        self.challenge = ChallengeService(self.storage)
    
    def process(self, text: str) -> str:
        """处理用户输入"""
        cmd_type, params = self.parser.parse(text)
        
        if cmd_type == CommandType.ADD_STOCK:
            stock_name = params.get('stock_name', '')
            reason = params.get('reason', '')
            remark = params.get('remark', '')
            return self.handle_add_stock(stock_name, reason, remark)
        
        elif cmd_type == CommandType.REMOVE_STOCK:
            stock_name = params.get('stock_name', '')
            return self.handle_remove_stock(stock_name)
        
        elif cmd_type == CommandType.LIST_STOCKS:
            group_by = '行业' in text
            return self.handle_list_stocks(group_by)
        
        elif cmd_type == CommandType.SEARCH_STOCK:
            keyword = params.get('keyword', '')
            return self.handle_search_stock(keyword)
        
        elif cmd_type == CommandType.BUY:
            return self.handle_buy(params)
        
        elif cmd_type == CommandType.SELL:
            return self.handle_sell(params)
        
        elif cmd_type == CommandType.POSITIONS:
            return self.handle_positions()
        
        elif cmd_type == CommandType.TRADES:
            return self.handle_trades()
        
        elif cmd_type == CommandType.DRILL:
            return self.handle_drill(params)
        
        elif cmd_type == CommandType.RECOMMEND:
            return self.handle_recommend(params)
        
        elif cmd_type == CommandType.HOT_SIGNALS:
            return self.handle_hot_signals()
        
        elif cmd_type == CommandType.FOUR_INDUSTRIES:
            return self.handle_four_industries()
        
        elif cmd_type == CommandType.MARKET_SUMMARY:
            return self.handle_market_summary()
        
        elif cmd_type == CommandType.DAILY_STOCK:
            return self.handle_daily_stock()
        
        elif cmd_type == CommandType.HELP:
            return self.handle_help()
        
        elif cmd_type in [CommandType.START_CHALLENGE, CommandType.END_CHALLENGE]:
            return self.handle_challenge(cmd_type)
        
        elif cmd_type == CommandType.CHALLENGE_STATUS:
            return self.handle_challenge_status()
        
        elif cmd_type == CommandType.CHALLENGE_STATS:
            return self.handle_challenge_stats()
        
        else:
            return self.handle_unknown(text)
    
    def handle_add_stock(self, stock_name: str, reason: str = '', remark: str = '') -> str:
        """处理添加股票"""
        if not stock_name:
            return "❌ 请告诉我股票名称或代码\n格式：加一只 XXX"
        
        results = self.stock_pool.search_stock(stock_name)
        if not results:
            return f"❌ 未找到股票：{stock_name}"
        
        if len(results) == 1:
            stock_code = results[0].get('symbol', results[0].get('ts_code', ''))
        else:
            lines = [f"🔍 找到多只股票，请确认："]
            for i, r in enumerate(results[:5], 1):
                name = r.get('name', r.get('ts_code', ''))
                code = r.get('symbol', r.get('ts_code', ''))
                lines.append(f"{i}. {name}({code})")
            return '\n'.join(lines) + "\n\n请输入序号或完整代码"
        
        success, msg = self.stock_pool.add_stock(stock_code, reason=reason, remark=remark)
        return msg
    
    def handle_remove_stock(self, stock_name: str) -> str:
        """处理移除股票"""
        if not stock_name:
            return "❌ 请告诉我股票名称或代码"
        success, msg = self.stock_pool.remove_stock(stock_name)
        return msg
    
    def handle_list_stocks(self, group_by_industry: bool = False) -> str:
        """处理列出股票"""
        if group_by_industry:
            grouped = self.stock_pool.list_stocks(group_by_industry=True)
            return self.stock_pool.format_grouped_stocks(grouped)
        else:
            stocks = self.stock_pool.list_stocks()
            return self.stock_pool.format_stock_list(stocks)
    
    def handle_search_stock(self, keyword: str) -> str:
        """处理搜索股票"""
        if not keyword:
            return "❌ 请输入搜索关键词"
        results = self.stock_pool.search_stock(keyword)
        if not results:
            return f"❌ 未找到股票：{keyword}"
        lines = ["🔍 搜索结果：", "| 代码 | 名称 | 行业 |", "|------|------|------|"]
        for r in results[:10]:
            code = r.get('symbol', r.get('ts_code', '-'))
            name = r.get('name', '-')
            industry = r.get('industry', '-')
            lines.append(f"| {code} | {name} | {industry} |")
        return '\n'.join(lines)
    
    def handle_buy(self, params: Dict) -> str:
        """处理买入"""
        stock_name = params.get('stock_name', '')
        quantity = params.get('quantity', 100)
        price = params.get('price', 0)
        if not stock_name:
            return "❌ 请告诉我股票名称\n格式：买 100 手 @ 15.6 招商银行"
        if price <= 0:
            return "❌ 请指定买入价格\n格式：买 100 手 @ 15.6 招商银行"
        
        # 检查挑战状态
        can_trade, trade_msg = self.challenge.can_trade()
        if not can_trade:
            return f"❌ {trade_msg}\n\n输入「开启挑战」开始月度挑战"
        
        results = self.stock_pool.search_stock(stock_name)
        if not results:
            return f"❌ 未找到股票：{stock_name}"
        stock_code = results[0].get('symbol', results[0].get('ts_code', stock_name))
        
        # 检查止损线提醒
        stop_loss_check, stop_loss_msg = self.challenge.check_stop_loss(stock_code, price, price)
        
        success, msg = self.position.buy(stock_code, quantity, price, stock_name=results[0].get('name'))
        
        # 记录到挑战
        if success:
            self.challenge.record_trade({
                'id': f"trade_{datetime.now().timestamp()}",
                'type': 'buy',
                'stock_code': stock_code,
                'price': price,
                'quantity': quantity * 100
            })
        
        return msg
    
    def handle_sell(self, params: Dict) -> str:
        """处理卖出"""
        stock_name = params.get('stock_name', '')
        quantity = params.get('quantity')
        
        if not stock_name:
            return "❌ 请告诉我股票名称\n格式：卖 50 手 招商银行"
        
        # 检查挑战状态
        can_trade, trade_msg = self.challenge.can_trade()
        if not can_trade:
            return f"❌ {trade_msg}"
        
        success, msg = self.position.sell(stock_name, quantity)
        
        # 记录到挑战
        if success:
            self.challenge.record_trade({
                'id': f"trade_{datetime.now().timestamp()}",
                'type': 'sell',
                'stock_code': stock_name,
            })
        
        return msg
    
    def handle_positions(self) -> str:
        """处理持仓查询"""
        return self.position.format_positions()
    
    def handle_trades(self) -> str:
        """处理交易记录"""
        return self.position.format_trades()
    
    def handle_drill(self, params: Dict) -> str:
        """处理演练模式"""
        import re
        scenario = params.get('scenario', '')
        
        # 尝试提取股票名称
        patterns = [
            r'买入(.+?)(?:的话|现在|赚|$)',
            r'持有(.+?)(?:的话|现在|赚|$)',
            r'(.+?)涨了多少',
            r'(.+?)赚多少',
            r'持有(.+?)赚',
        ]
        
        stock_name = None
        for pattern in patterns:
            match = re.search(pattern, scenario)
            if match:
                stock_name = match.group(1).strip()
                break
        
        if not stock_name:
            return "❌ 无法解析演练场景，请用自然语言描述\n例如：如果昨天开盘买入招商银行"
        
        # 搜索股票
        results = self.stock_pool.search_stock(stock_name)
        if not results:
            return f"❌ 未找到股票：{stock_name}\n请先添加股票到股票池"
        
        stock_code = results[0].get('symbol', results[0].get('ts_code', ''))
        name = results[0].get('name', stock_name)
        
        # 获取昨日开盘价
        yesterday_open = self.tushare.get_yesterday_open(stock_code)
        # 获取当前价
        quote = self.tushare.get_realtime_quote(stock_code)
        
        if not yesterday_open:
            # 如果没有真实数据，返回提示
            return (
                f"🔍 演练结果\n"
                f"股票：{name}({stock_code})\n\n"
                f"⚠️ 暂无昨日开盘价数据\n"
                f"请确保 TUSHARE_TOKEN 已配置"
            )
        
        current_price = quote.get('price', yesterday_open) if quote else yesterday_open
        profit = (current_price - yesterday_open) * 100
        profit_rate = (profit / (yesterday_open * 100)) * 100
        
        return (
            f"🔍 演练结果\n"
            f"股票：{name}({stock_code})\n"
            f"买入假设：昨日开盘价 {yesterday_open:.2f}\n"
            f"当前价格：{current_price:.2f}\n"
            f"演练收益：{profit:+,.0f} 元 ({profit_rate:+.2f}%)"
        )
    
    def handle_recommend(self, params: Dict) -> str:
        """处理股票推荐"""
        criteria = params.get('criteria', '')
        recommendations = []
        if criteria == 'hsgt':
            recommendations = self.recommendation.get_hsgt_stocks('in', 5)
        else:
            limit_stocks = self.recommendation.get_limit_stocks(3)
            mf_stocks = self.recommendation.get_moneyflow_stocks(3)
            recommendations = limit_stocks + mf_stocks
        return self.recommendation.format_recommendations(recommendations, "📈 股票推荐")
    
    def handle_hot_signals(self) -> str:
        """处理热门信号"""
        return self.recommendation.get_hot_signals()
    
    def handle_four_industries(self) -> str:
        """处理四大行业分析"""
        return self.recommendation.get_all_industries_analysis()
    
    def handle_market_summary(self) -> str:
        """处理市场概况"""
        return self.recommendation.get_market_summary()
    
    def handle_daily_stock(self) -> str:
        """处理每日金股"""
        limit_stocks = self.recommendation.get_limit_stocks(5)
        if limit_stocks:
            return self.recommendation.format_recommendations([limit_stocks[0]], "🌟 今日金股")
        else:
            return "📈 今日金股\n今日暂无明显信号，建议关注市场动态"
    
    def handle_help(self) -> str:
        """处理帮助"""
        return """📖 TOC 模拟交易系统 - 命令帮助

**股票池操作：**
- 加一只 XXX — 添加股票到自选
- 去掉 XXX — 从自选移除
- 股票池 — 查看自选股列表

**交易操作：**
- 买 100 手 @ 15.6 招商银行 — 记录买入
- 卖 50 手 招商银行 — 记录卖出
- 持仓 — 查看当前持仓
- 历史交易 — 查看成交记录

**演练模式：**
- 如果昨天开盘买入 XXX — 假设收益

**股票推荐：**
- 推荐一只股票 — AI 推荐
- 今日金股 — 每日推荐
- 有什么消息 — 市场热点

**挑战模式：**
- 开启挑战 — 开始月度挑战
- 挑战状态 — 查看当前状态
- 挑战统计 — 查看详细统计
- 结束挑战 — 结束当前挑战

**市场分析：**
- 四大行业 — AI/消费品/汽车/医疗分析
- 市场概况 — 大盘整体情况
- 有什么消息 — 热门板块信号

**其他：**
- 帮助 — 显示此帮助
"""
    
    def handle_challenge(self, cmd_type) -> str:
        """处理挑战相关命令"""
        if cmd_type == CommandType.START_CHALLENGE:
            success, msg = self.challenge.start_challenge()
            return msg
        elif cmd_type == CommandType.END_CHALLENGE:
            success, msg = self.challenge.end_challenge()
            return msg
        return "❌ 无法处理的挑战命令"
    
    def handle_challenge_status(self) -> str:
        """处理挑战状态查询"""
        return self.challenge.get_status()
    
    def handle_challenge_stats(self) -> str:
        """处理挑战统计查询"""
        return self.challenge.get_stats()
    
    def handle_unknown(self, text: str) -> str:
        """处理未知命令"""
        return f"❓ 无法理解：{text}\n\n输入「帮助」查看可用命令"


def process(text: str) -> str:
    """处理用户输入的快捷函数"""
    toc = TOCTTrading()
    return toc.process(text)