"""
AgentScope 工具注册模块
使用 Toolkit 注册 Tushare/AKShare 数据采集工具
"""

from agentscope.tool import Toolkit, ToolResponse
from agentscope.message import TextBlock

from .tushare_tools import TushareTools
from .akshare_tools import AKShareTools
from ..config import config


# 全局工具实例
_tushare_tools = None
_akshare_tools = None


def get_tushare_tools() -> TushareTools:
    """获取 Tushare 工具单例"""
    global _tushare_tools
    if _tushare_tools is None:
        _tushare_tools = TushareTools(config.tushare_token)
    return _tushare_tools


def get_akshare_tools() -> AKShareTools:
    """获取 AKShare 工具单例"""
    global _akshare_tools
    if _akshare_tools is None:
        _akshare_tools = AKShareTools()
    return _akshare_tools


# ============ AgentScope 工具函数定义 ============

async def get_stock_daily(ts_code: str, days: int = 60) -> ToolResponse:
    """
    获取股票日线行情数据
    
    Args:
        ts_code: 股票代码，如 600519.SH
        days: 获取天数，默认60天
        
    Returns:
        包含日线数据的 ToolResponse
    """
    try:
        tools = get_tushare_tools()
        data = tools.get_stock_daily(ts_code, days)
        
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=f"股票 {ts_code} 近 {days} 日行情数据:\n"
                         f"- 最新收盘价: {data.get('latest_close', 'N/A')}\n"
                         f"- 最新涨跌幅: {data.get('latest_pct_chg', 'N/A')}%\n"
                         f"- 最新成交量: {data.get('latest_volume', 'N/A')}\n"
                         f"- 最新成交额: {data.get('latest_amount', 'N/A')}万元\n"
                         f"- 数据条数: {data.get('data_count', 0)}"
                )
            ]
        )
    except Exception as e:
        return ToolResponse(
            content=[TextBlock(type="text", text=f"获取行情数据失败: {str(e)}")]
        )


async def get_technical_indicators(ts_code: str, days: int = 60) -> ToolResponse:
    """
    获取股票技术指标数据（MA、MACD、RSI等）
    
    Args:
        ts_code: 股票代码，如 600519.SH
        days: 数据天数，默认60天
        
    Returns:
        包含技术指标的 ToolResponse
    """
    try:
        tools = get_tushare_tools()
        data = tools.get_technical_indicators(ts_code, days)
        
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=f"股票 {ts_code} 技术指标:\n"
                         f"- 当前价: {data.get('current_price', 'N/A')}\n"
                         f"- MA5: {data.get('ma5', 'N/A')}\n"
                         f"- MA20: {data.get('ma20', 'N/A')}\n"
                         f"- MA60: {data.get('ma60', 'N/A')}\n"
                         f"- MA信号: {data.get('ma_signal', 'N/A')}\n"
                         f"- MACD: {data.get('macd', 'N/A')}\n"
                         f"- RSI: {data.get('rsi', 'N/A')}\n"
                         f"- 趋势: {data.get('trend', 'N/A')}\n"
                         f"- 支撑位: {data.get('support', 'N/A')}\n"
                         f"- 阻力位: {data.get('resistance', 'N/A')}\n"
                         f"- 技术评分: {data.get('technical_score', 50)}/100"
                )
            ]
        )
    except Exception as e:
        return ToolResponse(
            content=[TextBlock(type="text", text=f"获取技术指标失败: {str(e)}")]
        )


async def get_stock_basic(ts_code: str) -> ToolResponse:
    """
    获取股票基本信息
    
    Args:
        ts_code: 股票代码，如 600519.SH
        
    Returns:
        包含基本信息的 ToolResponse
    """
    try:
        tools = get_tushare_tools()
        data = tools.get_stock_basic(ts_code)
        
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=f"股票基本信息:\n"
                         f"- 代码: {ts_code}\n"
                         f"- 名称: {data.get('name', 'N/A')}\n"
                         f"- 行业: {data.get('industry', 'N/A')}\n"
                         f"- 板块: {data.get('market', 'N/A')}\n"
                         f"- 上市日期: {data.get('list_date', 'N/A')}"
                )
            ]
        )
    except Exception as e:
        return ToolResponse(
            content=[TextBlock(type="text", text=f"获取基本信息失败: {str(e)}")]
        )


async def get_valuation(ts_code: str) -> ToolResponse:
    """
    获取股票估值数据（PE、PB、PS等）
    
    Args:
        ts_code: 股票代码，如 600519.SH
        
    Returns:
        包含估值数据的 ToolResponse
    """
    try:
        tools = get_tushare_tools()
        data = tools.get_valuation(ts_code)
        
        total_mv = data.get('total_mv', 0)
        total_mv_yi = round(total_mv / 10000, 2) if total_mv else 'N/A'
        
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=f"股票 {ts_code} 估值数据:\n"
                         f"- PE(TTM): {data.get('pe_ttm', 'N/A')}\n"
                         f"- PB: {data.get('pb', 'N/A')}\n"
                         f"- PS(TTM): {data.get('ps_ttm', 'N/A')}\n"
                         f"- 股息率: {data.get('dv_ratio', 'N/A')}%\n"
                         f"- 总市值: {total_mv_yi}亿元"
                )
            ]
        )
    except Exception as e:
        return ToolResponse(
            content=[TextBlock(type="text", text=f"获取估值数据失败: {str(e)}")]
        )


async def get_financial_indicator(ts_code: str) -> ToolResponse:
    """
    获取股票财务指标数据
    
    Args:
        ts_code: 股票代码，如 600519.SH
        
    Returns:
        包含财务指标的 ToolResponse
    """
    try:
        tools = get_tushare_tools()
        data = tools.get_financial_indicator(ts_code)
        
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=f"股票 {ts_code} 财务指标:\n"
                         f"- ROE: {data.get('roe', 'N/A')}%\n"
                         f"- ROA: {data.get('roa', 'N/A')}%\n"
                         f"- 毛利率: {data.get('gross_margin', 'N/A')}%\n"
                         f"- 净利率: {data.get('net_margin', 'N/A')}%\n"
                         f"- 负债率: {data.get('debt_ratio', 'N/A')}%"
                )
            ]
        )
    except Exception as e:
        return ToolResponse(
            content=[TextBlock(type="text", text=f"获取财务指标失败: {str(e)}")]
        )


async def get_stock_news(ts_code: str, stock_name: str = "", days: int = 7) -> ToolResponse:
    """
    获取股票相关新闻
    
    Args:
        ts_code: 股票代码，如 600519.SH
        stock_name: 股票名称（可选）
        days: 新闻天数，默认7天
        
    Returns:
        包含新闻数据的 ToolResponse
    """
    try:
        tools = get_akshare_tools()
        data = tools.get_stock_news(ts_code, stock_name, days)
        
        sentiment = data.get('sentiment', {})
        analyzed_news = sentiment.get('analyzed_news', [])
        
        news_list = ""
        for i, news in enumerate(analyzed_news[:5], 1):
            news_list += f"{i}. {news.get('title', 'N/A')} - {news.get('sentiment', '中性')}\n"
        
        if not news_list:
            news_list = "暂无相关新闻"
        
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=f"股票 {ts_code} 近 {days} 天新闻舆情:\n"
                         f"- 新闻总数: {data.get('news_count', 0)}条\n"
                         f"- 利好新闻: {sentiment.get('positive_count', 0)}条 ({sentiment.get('positive_pct', 0)}%)\n"
                         f"- 利空新闻: {sentiment.get('negative_count', 0)}条 ({sentiment.get('negative_pct', 0)}%)\n"
                         f"- 中性新闻: {sentiment.get('neutral_count', 0)}条\n"
                         f"- 整体情绪: {sentiment.get('overall_sentiment', '中性')}\n"
                         f"- 舆情评分: {sentiment.get('sentiment_score', 50)}/100\n\n"
                         f"关键新闻:\n{news_list}"
                )
            ]
        )
    except Exception as e:
        return ToolResponse(
            content=[TextBlock(type="text", text=f"获取新闻数据失败: {str(e)}")]
        )


async def get_market_sentiment() -> ToolResponse:
    """
    获取市场整体情绪
    
    Returns:
        包含市场情绪数据的 ToolResponse
    """
    try:
        tools = get_akshare_tools()
        data = tools.get_market_sentiment()
        
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=f"市场整体情绪:\n"
                         f"- 上涨股票数: {data.get('up_count', 'N/A')}\n"
                         f"- 下跌股票数: {data.get('down_count', 'N/A')}\n"
                         f"- 上涨比例: {data.get('up_ratio', 'N/A')}%\n"
                         f"- 市场情绪: {data.get('market_mood', '中性')}"
                )
            ]
        )
    except Exception as e:
        return ToolResponse(
            content=[TextBlock(type="text", text=f"获取市场情绪失败: {str(e)}")]
        )


# ============ 创建 Toolkit ============

def create_stock_toolkit() -> Toolkit:
    """
    创建股票分析工具包
    
    Returns:
        Toolkit: 包含所有股票分析工具的工具包
    """
    toolkit = Toolkit()
    
    # 注册 Tushare 工具
    toolkit.register_tool_function(get_stock_daily)
    toolkit.register_tool_function(get_technical_indicators)
    toolkit.register_tool_function(get_stock_basic)
    toolkit.register_tool_function(get_valuation)
    toolkit.register_tool_function(get_financial_indicator)
    
    # 注册 AKShare 工具
    toolkit.register_tool_function(get_stock_news)
    toolkit.register_tool_function(get_market_sentiment)
    
    return toolkit


# ============ 为 ReActAgent 创建预配置的 Toolkit ============

def create_market_analyst_toolkit() -> Toolkit:
    """创建技术面分析师工具包"""
    toolkit = Toolkit()
    toolkit.register_tool_function(get_stock_daily)
    toolkit.register_tool_function(get_technical_indicators)
    toolkit.register_tool_function(get_stock_basic)
    return toolkit


def create_fundamentals_analyst_toolkit() -> Toolkit:
    """创建基本面分析师工具包"""
    toolkit = Toolkit()
    toolkit.register_tool_function(get_stock_basic)
    toolkit.register_tool_function(get_valuation)
    toolkit.register_tool_function(get_financial_indicator)
    return toolkit


def create_news_analyst_toolkit() -> Toolkit:
    """创建舆情分析师工具包"""
    toolkit = Toolkit()
    toolkit.register_tool_function(get_stock_basic)
    toolkit.register_tool_function(get_stock_news)
    toolkit.register_tool_function(get_market_sentiment)
    return toolkit
