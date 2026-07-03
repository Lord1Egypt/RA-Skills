from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def get_stock_sse_summary(
) -> Dict[str, Any]:
    """
    获取上海证券交易所股票数据总貌

Returns:
    str: 上交所股票数据总貌的JSON格式字符串，包含流通股本、总市值、平均市盈率、上市公司数、流通市值等统计信息
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419072866307", "get_stock_sse_summary", arguments)

def get_stock_szse_summary(
    date: Optional[str] = ""
) -> Dict[str, Any]:
    """
    获取深圳证券交易所市场总貌-证券类别统计

Args:
    date (str): 查询日期，格式："20200619"，为空则查询最新数据

Returns:
    str: 深交所证券类别统计数据的JSON格式字符串，包含股票、基金、债券等各类证券的数量、成交金额、总市值、流通市值等
    
    Args:
        date: null
    
    Returns:
        null
    """
    arguments = {
        "date": date
    }
    
    return call_api("1777419072866307", "get_stock_szse_summary", arguments)

def get_stock_individual_info_em(
    symbol: str,
    timeout: Optional[float] = None
) -> Dict[str, Any]:
    """
    获取东方财富-个股-股票信息

Args:
    symbol (str): 股票代码，例如："000001" 或 "603777"
    timeout (float): 超时参数，默认不设置

Returns:
    str: 个股信息的JSON格式字符串，包含最新价、股票代码、股票简称、总股本、流通股、总市值、流通市值、行业、上市时间等基本信息
    
    Args:
        symbol: null
        timeout: null
    
    Returns:
        null
    """
    arguments = {
        "symbol": symbol,
        "timeout": timeout
    }
    
    return call_api("1777419072866307", "get_stock_individual_info_em", arguments)

def get_stock_individual_basic_info_xq(
    symbol: str,
    token: Optional[str] = None,
    timeout: Optional[float] = None
) -> Dict[str, Any]:
    """
    获取雪球财经-个股-公司概况-公司简介

Args:
    symbol (str): 带市场标识的股票代码，例如："SH601127"
    token (str): 认证令牌，默认为空
    timeout (float): 超时参数，默认不设置

Returns:
    str: 个股基本信息的JSON格式字符串，包含公司ID、中英文名称、主营业务、经营范围、公司简介、法定代表人、总经理、董秘、成立日期、注册资本、员工人数、联系方式、注册地址、办公地址、货币、上市日期、省份、实际控制人、企业性质、曾用名、董事长、高管人数、实际发行量、发行价、募集资金、发行市盈率、网上中签率、所属行业等详细信息
    
    Args:
        symbol: null
        token: null
        timeout: null
    
    Returns:
        null
    """
    arguments = {
        "symbol": symbol,
        "token": token,
        "timeout": timeout
    }
    
    return call_api("1777419072866307", "get_stock_individual_basic_info_xq", arguments)

def get_stock_board_industry_name_em(
) -> Dict[str, Any]:
    """
    获取东方财富-沪深京板块-行业板块数据

Returns:
    str: 行业板块数据的JSON格式字符串，包含排名、板块名称、板块代码、最新价、涨跌额、涨跌幅、总市值、换手率、上涨家数、下跌家数、领涨股票、领涨股票-涨跌幅等所有行业板块的实时行情数据
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419072866307", "get_stock_board_industry_name_em", arguments)

def get_stock_board_industry_spot_em(
    symbol: str
) -> Dict[str, Any]:
    """
    获取东方财富网-沪深板块-行业板块-实时行情数据

Args:
    symbol (str): 板块名称，例如："小金属"

Returns:
    str: 指定行业板块实时行情数据的JSON格式字符串，包含最新、最高、最低、开盘、成交量、成交额、换手率、涨跌额、涨跌幅、振幅等关键指标
    
    Args:
        symbol: null
    
    Returns:
        null
    """
    arguments = {
        "symbol": symbol
    }
    
    return call_api("1777419072866307", "get_stock_board_industry_spot_em", arguments)

def get_stock_board_industry_cons_em(
    symbol: str
) -> Dict[str, Any]:
    """
    获取东方财富-沪深板块-行业板块-板块成份股数据

Args:
    symbol (str): 板块名称或板块代码，例如："小金属" 或 "BK1027"

Returns:
    str: 指定行业板块成份股数据的JSON格式字符串，包含序号、代码、名称、最新价、涨跌幅、涨跌额、成交量、成交额、振幅、最高、最低、今开、昨收、换手率、市盈率-动态、市净率等该板块所有成份股的详细信息
    
    Args:
        symbol: null
    
    Returns:
        null
    """
    arguments = {
        "symbol": symbol
    }
    
    return call_api("1777419072866307", "get_stock_board_industry_cons_em", arguments)

def get_stock_hot_rank_em(
) -> Dict[str, Any]:
    """
    获取东方财富网站-股票热度-人气榜数据

Returns:
    str: A股人气排行榜数据的JSON格式字符串，包含当前排名、代码、股票名称、最新价、涨跌额、涨跌幅等当前交易日前100个股票的人气排名数据
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419072866307", "get_stock_hot_rank_em", arguments)

def get_stock_hot_deal_xq(
    symbol: Optional[str] = "最热门"
) -> Dict[str, Any]:
    """
    获取雪球-沪深股市-热度排行榜-交易排行榜数据

Args:
    symbol (str): 排行榜类型，可选："本周新增", "最热门"，默认："最热门"

Returns:
    str: 交易排行榜数据的JSON格式字符串，包含股票代码、股票简称、关注数、最新价等排行数据
    
    Args:
        symbol: null
    
    Returns:
        null
    """
    arguments = {
        "symbol": symbol
    }
    
    return call_api("1777419072866307", "get_stock_hot_deal_xq", arguments)

def get_stock_zh_a_spot_em(
) -> Dict[str, Any]:
    """
    获取沪深京A股实时行情数据

Returns:
    str: 沪深京A股实时行情数据的JSON格式字符串，包含所有上市公司的最新价、涨跌幅、成交量、市值等信息
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419072866307", "get_stock_zh_a_spot_em", arguments)

def get_stock_info_xueqiu(
    symbol: str
) -> Dict[str, Any]:
    """
    获取雪球个股实时市场数据信息

Args:
    symbol (str): 带市场标识的股票代码，例如："SH601318"(中国平安)

Returns:
    str: 个股信息的JSON格式字符串，包含实时价格、涨跌幅、成交量等数据
    
    Args:
        symbol: null
    
    Returns:
        null
    """
    arguments = {
        "symbol": symbol
    }
    
    return call_api("1777419072866307", "get_stock_info_xueqiu", arguments)

def get_stock_zt_pool_em(
    date: Optional[str] = ""
) -> Dict[str, Any]:
    """
    获取东方财富网-涨停股池数据

Args:
    date (str): 查询日期，格式："20241008"，为空则查询最新数据

Returns:
    str: 涨停股池数据的JSON格式字符串，包含涨停股票的序号、代码、名称、涨跌幅、最新价、成交额、流通市值、总市值、换手率、封板资金、首次封板时间、最后封板时间、炸板次数、涨停统计、连板数、所属行业等信息
    
    Args:
        date: null
    
    Returns:
        null
    """
    arguments = {
        "date": date
    }
    
    return call_api("1777419072866307", "get_stock_zt_pool_em", arguments)

def get_stock_a_hist(
    symbol: str,
    period: Optional[str] = "daily",
    start_date: Optional[str] = "",
    end_date: Optional[str] = "",
    adjust: Optional[str] = ""
) -> Dict[str, Any]:
    """
    获取A股历史K线数据

Args:
    symbol (str): 股票代码，例如："000001"(平安银行)
    period (str): 周期，可选 "daily"(日线), "weekly"(周线), "monthly"(月线)
    start_date (str): 开始日期，格式："20220101"
    end_date (str): 结束日期，格式："20221231"
    adjust (str): 复权方式，""不复权，"qfq"前复权，"hfq"后复权

Returns:
    str: A股历史数据的JSON格式字符串，包含日期、开盘价、收盘价、最高价、最低价、成交量等信息
    
    Args:
        symbol: null
        period: null
        start_date: null
        end_date: null
        adjust: null
    
    Returns:
        null
    """
    arguments = {
        "symbol": symbol,
        "period": period,
        "start_date": start_date,
        "end_date": end_date,
        "adjust": adjust
    }
    
    return call_api("1777419072866307", "get_stock_a_hist", arguments)

def get_stock_zh_a_hist_tx(
    symbol: str,
    start_date: Optional[str] = "19000101",
    end_date: Optional[str] = "20500101",
    adjust: Optional[str] = "",
    timeout: Optional[float] = None
) -> Dict[str, Any]:
    """
    获取腾讯证券-日频-股票历史数据

Args:
    symbol (str): 带市场标识的股票代码，例如："sz000001"
    start_date (str): 开始查询的日期，格式："20200101"，默认："19000101"
    end_date (str): 结束查询的日期，格式："20231027"，默认："20500101"
    adjust (str): 复权方式，默认返回不复权数据；"qfq": 前复权；"hfq": 后复权
    timeout (float): 超时参数，默认不设置

Returns:
    str: 腾讯证券历史行情数据的JSON格式字符串，包含交易日、开盘价、收盘价、最高价、最低价、成交量(手)等信息
    
    Args:
        symbol: null
        start_date: null
        end_date: null
        adjust: null
        timeout: null
    
    Returns:
        null
    """
    arguments = {
        "symbol": symbol,
        "start_date": start_date,
        "end_date": end_date,
        "adjust": adjust,
        "timeout": timeout
    }
    
    return call_api("1777419072866307", "get_stock_zh_a_hist_tx", arguments)

def get_stock_zh_a_hist_min_em(
    symbol: str,
    start_date: Optional[str] = "",
    end_date: Optional[str] = "",
    period: Optional[str] = "5",
    adjust: Optional[str] = ""
) -> Dict[str, Any]:
    """
    获取东方财富网-沪深京A股-每日分时行情数据

Args:
    symbol (str): 股票代码，例如："000001"
    start_date (str): 开始日期时间，格式："2024-03-20 09:30:00"，为空则返回所有数据
    end_date (str): 结束日期时间，格式："2024-03-20 15:00:00"，为空则返回所有数据
    period (str): 时间周期，可选："1", "5", "15", "30", "60"，其中1分钟数据只返回近5个交易日数据且不复权
    adjust (str): 复权方式，可选：""(不复权), "qfq"(前复权), "hfq"(后复权)，其中1分钟数据只返回近5个交易日数据且不复权

Returns:
    str: 分时行情数据的JSON格式字符串，1分钟数据包含时间、开盘、收盘、最高、最低、成交量、成交额、均价；其他周期数据还包含涨跌幅、涨跌额、振幅、换手率等信息
    
    Args:
        symbol: null
        start_date: null
        end_date: null
        period: null
        adjust: null
    
    Returns:
        null
    """
    arguments = {
        "symbol": symbol,
        "start_date": start_date,
        "end_date": end_date,
        "period": period,
        "adjust": adjust
    }
    
    return call_api("1777419072866307", "get_stock_zh_a_hist_min_em", arguments)

def get_stock_financial_analysis_indicator(
    symbol: str,
    start_year: Optional[str] = "2020"
) -> Dict[str, Any]:
    """
    获取新浪财经-财务分析-财务指标数据

Args:
    symbol (str): 股票代码，例如："600004"
    start_year (str): 开始查询的时间，例如："2020"

Returns:
    str: 财务指标数据的JSON格式字符串，包含日期、摊薄每股收益、加权每股收益、每股净资产、总资产利润率、主营业务利润率、净资产收益率、应收账款周转率、流动比率、资产负债率等86项财务指标
    
    Args:
        symbol: null
        start_year: null
    
    Returns:
        null
    """
    arguments = {
        "symbol": symbol,
        "start_year": start_year
    }
    
    return call_api("1777419072866307", "get_stock_financial_analysis_indicator", arguments)

def get_stock_profit_forecast_em(
    symbol: Optional[str] = ""
) -> Dict[str, Any]:
    """
    获取东方财富网-数据中心-研究报告-盈利预测数据

Args:
    symbol (str): 股票代码或行业板块，默认为获取全部数据；例如："船舶制造"，行业板块可以通过 ak.stock_board_industry_name_em() 接口获取

Returns:
    str: 盈利预测数据的JSON格式字符串，包含序号、代码、名称、研报数、机构投资评级（买入、增持、中性、减持、卖出）、各年度预测每股收益等信息
    
    Args:
        symbol: null
    
    Returns:
        null
    """
    arguments = {
        "symbol": symbol
    }
    
    return call_api("1777419072866307", "get_stock_profit_forecast_em", arguments)

def get_stock_zh_a_disclosure_report_cninfo(
    symbol: str,
    market: Optional[str] = "沪深京",
    keyword: Optional[str] = "",
    category: Optional[str] = "",
    start_date: Optional[str] = "",
    end_date: Optional[str] = ""
) -> Dict[str, Any]:
    """
    获取巨潮资讯网-信息披露公告数据

Args:
    symbol (str): 股票代码，例如："000001"
    market (str): 市场类型，可选："沪深京", "港股", "三板", "基金", "债券", "监管", "预披露"
    keyword (str): 关键词搜索，默认为空字符串
    category (str): 公告类别，可选：'年报', '半年报', '一季报', '三季报', '业绩预告', '权益分派', '董事会', '监事会', '股东大会', '日常经营', '公司治理', '中介报告', '首发', '增发', '股权激励', '配股', '解禁', '公司债', '可转债', '其他融资', '股权变动', '补充更正', '澄清致歉', '风险提示', '特别处理和退市', '退市整理期'
    start_date (str): 开始日期，格式："20230618"
    end_date (str): 结束日期，格式："20231219"

Returns:
    str: 信息披露公告数据的JSON格式字符串，包含代码、简称、公告标题、公告时间、公告链接等信息
    
    Args:
        symbol: null
        market: null
        keyword: null
        category: null
        start_date: null
        end_date: null
    
    Returns:
        null
    """
    arguments = {
        "symbol": symbol,
        "market": market,
        "keyword": keyword,
        "category": category,
        "start_date": start_date,
        "end_date": end_date
    }
    
    return call_api("1777419072866307", "get_stock_zh_a_disclosure_report_cninfo", arguments)

def get_stock_lhb_detail_em(
    start_date: str,
    end_date: str
) -> Dict[str, Any]:
    """
    获取东方财富网-数据中心-龙虎榜单-龙虎榜详情数据

Args:
    start_date (str): 开始日期，格式："20220314"
    end_date (str): 结束日期，格式："20220315"

Returns:
    str: 龙虎榜详情数据的JSON格式字符串，包含序号、代码、名称、上榜日、解读、收盘价、涨跌幅、龙虎榜净买额、龙虎榜买入额、龙虎榜卖出额、龙虎榜成交额、市场总成交额、净买额占总成交比、成交额占总成交比、换手率、流通市值、上榜原因、上榜后各日涨跌幅等信息
    
    Args:
        start_date: null
        end_date: null
    
    Returns:
        null
    """
    arguments = {
        "start_date": start_date,
        "end_date": end_date
    }
    
    return call_api("1777419072866307", "get_stock_lhb_detail_em", arguments)

def get_stock_individual_fund_flow(
    stock: str,
    market: str
) -> Dict[str, Any]:
    """
    获取东方财富网-数据中心-个股资金流向数据

Args:
    stock (str): 股票代码，例如："000425" 或 "600094"
    market (str): 交易所代码，可选："sh"(上海证券交易所), "sz"(深证证券交易所), "bj"(北京证券交易所)

Returns:
    str: 个股资金流向数据的JSON格式字符串，包含日期、收盘价、涨跌幅、主力净流入-净额、主力净流入-净占比、超大单净流入-净额、超大单净流入-净占比、大单净流入-净额、大单净流入-净占比、中单净流入-净额、中单净流入-净占比、小单净流入-净额、小单净流入-净占比等近100个交易日的资金流数据
    
    Args:
        stock: null
        market: null
    
    Returns:
        null
    """
    arguments = {
        "stock": stock,
        "market": market
    }
    
    return call_api("1777419072866307", "get_stock_individual_fund_flow", arguments)

def get_stock_comment_detail_zlkp_jgcyd_em(
    symbol: str
) -> Dict[str, Any]:
    """
    获取东方财富网-数据中心-特色数据-千股千评-主力控盘-机构参与度数据

Args:
    symbol (str): 股票代码，例如："600000"

Returns:
    str: 机构参与度数据的JSON格式字符串，包含交易日和机构参与度(%)的历史数据，用于分析机构资金对该股票的参与程度
    
    Args:
        symbol: null
    
    Returns:
        null
    """
    arguments = {
        "symbol": symbol
    }
    
    return call_api("1777419072866307", "get_stock_comment_detail_zlkp_jgcyd_em", arguments)

def get_stock_info_global_em(
) -> Dict[str, Any]:
    """
    获取东方财富-全球财经快讯数据

Returns:
    str: 全球财经快讯数据的JSON格式字符串，包含标题、摘要、发布时间、链接等最近200条新闻数据
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419072866307", "get_stock_info_global_em", arguments)

def get_stock_info_global_futu(
) -> Dict[str, Any]:
    """
    获取富途牛牛-快讯数据

Returns:
    str: 富途牛牛快讯数据的JSON格式字符串，包含标题、内容、发布时间、链接等最近50条新闻数据
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419072866307", "get_stock_info_global_futu", arguments)

def get_stock_zh_valuation_comparison_em(
    symbol: str
) -> Dict[str, Any]:
    """
    获取东方财富-行情中心-同行比较-估值比较数据

Args:
    symbol (str): 带市场标识的股票代码，例如："SZ000895"

Returns:
    str: 估值比较数据的JSON格式字符串，包含代码、简称、PEG、市盈率（24A、TTM、25E、26E、27E）、市销率（24A、TTM、25E、26E、27E）、市净率（24A、MRQ）、市现率PCE（24A、TTM）、市现率PCF（24A、TTM）、EV/EBITDA（24A）及PEG排名等同行估值比较数据
    
    Args:
        symbol: null
    
    Returns:
        null
    """
    arguments = {
        "symbol": symbol
    }
    
    return call_api("1777419072866307", "get_stock_zh_valuation_comparison_em", arguments)

def get_stock_zh_growth_comparison_em(
    symbol: str
) -> Dict[str, Any]:
    """
    获取东方财富-行情中心-同行比较-成长性比较数据

Args:
    symbol (str): 带市场标识的股票代码，例如："SZ000895"

Returns:
    str: 成长性比较数据的JSON格式字符串，包含代码、简称、基本每股收益增长率（3年复合、24A、TTM、25E、26E、27E）、营业收入增长率（3年复合、24A、TTM、25E、26E、27E）、净利润增长率（3年复合、24A、TTM、25E、26E、27E）及其排名等同行比较数据
    
    Args:
        symbol: null
    
    Returns:
        null
    """
    arguments = {
        "symbol": symbol
    }
    
    return call_api("1777419072866307", "get_stock_zh_growth_comparison_em", arguments)

def get_stock_inner_trade_xq(
) -> Dict[str, Any]:
    """
    获取雪球-行情中心-沪深股市-内部交易数据

Returns:
    str: 内部交易数据的JSON格式字符串，包含股票代码、股票名称、变动日期、变动人、变动股数、成交均价、变动后持股数、与董监高关系、董监高职务等所有历史内部交易记录
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419072866307", "get_stock_inner_trade_xq", arguments)

def get_stock_research_report_em(
    symbol: str
) -> Dict[str, Any]:
    """
    获取东方财富网-数据中心-研究报告-个股研报数据

Args:
    symbol (str): 股票代码，例如："000001"

Returns:
    str: 个股研报数据的JSON格式字符串，包含序号、股票代码、股票简称、报告名称、东财评级、机构、近一月个股研报数、2024-2026年盈利预测-收益和市盈率、行业、日期、报告PDF链接等详细信息
    
    Args:
        symbol: null
    
    Returns:
        null
    """
    arguments = {
        "symbol": symbol
    }
    
    return call_api("1777419072866307", "get_stock_research_report_em", arguments)

def get_stock_info_a_code_name(
    company_name: Optional[str] = ""
) -> Dict[str, Any]:
    """
    根据公司名称获取沪深京A股股票代码

Args:
    company_name: 公司名称，支持模糊匹配。如果为空，则返回所有股票数据
    
Returns:
    str: 股票代码数据的JSON格式字符串，包含匹配的股票代码(code)和股票简称(name)
    
    Args:
        company_name: null
    
    Returns:
        null
    """
    arguments = {
        "company_name": company_name
    }
    
    return call_api("1777419072866307", "get_stock_info_a_code_name", arguments)

def get_tool_trade_date_hist_sina(
) -> Dict[str, Any]:
    """
    获取新浪财经-股票交易日历数据

Returns:
    str: 股票交易日历数据的JSON格式字符串，包含从1990-12-19到2024-12-31之间的所有股票交易日数据
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419072866307", "get_tool_trade_date_hist_sina", arguments)

