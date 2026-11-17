"""
携程数据抓取模块

- 酒店: Playwright + API 双轨抓取评论，差评分类统计，多维度评价分析
- 航班: Playwright 拦截 batchSearch API，航班票价/余票/降价预测监控
- 扫码登录 + Cookie持久化
"""
from .client import CtripClient, DEFAULT_COOKIE_PATH, DEFAULT_USER_DATA_DIR
from .login import check_login, login, logout
from .reviews import fetch_and_analyze, analyze_reviews, ReviewsFetcher, search_hotel_id
from .flight import (
    FlightTicket, FlightResult, PricePrediction, fetch_flights,
    MULTI_AIRPORT_CITIES, TIME_PERIODS,
    match_airport, classify_time_period,
    is_budget_airline, BUDGET_AIRLINES,
    merge_codeshares,
)

__all__ = [
    "CtripClient",
    "DEFAULT_COOKIE_PATH",
    "DEFAULT_USER_DATA_DIR",
    "check_login",
    "login",
    "logout",
    "fetch_and_analyze",
    "analyze_reviews",
    "search_hotel_id",
    "FlightTicket",
    "FlightResult",
    "PricePrediction",
    "fetch_flights",
    "MULTI_AIRPORT_CITIES",
    "TIME_PERIODS",
    "match_airport",
    "classify_time_period",
    "is_budget_airline",
    "BUDGET_AIRLINES",
    "merge_codeshares",
]
