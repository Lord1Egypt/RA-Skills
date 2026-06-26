from __future__ import annotations

import asyncio
import logging
import re
from typing import Optional

import pandas as pd

from src.analyzer.prompts import STOCK_ANALYSIS_SYSTEM_PROMPT, STOCK_ANALYSIS_USER_PROMPT
from src.config import SkillConfig
from src.data.provider import MarketDataProvider
from src.llm.client import LLMClient
from src.models import (
    CapitalFlow,
    CheckItem,
    ChipDistribution,
    FinancialData,
    NewsItem,
    RealtimeQuote,
    StockAnalysisResult,
    StockInfo,
    TechnicalIndicators,
    Valuation,
)
from src.search.base import NewsSearchEngine

logger = logging.getLogger(__name__)


def calculate_technical_indicators(df: pd.DataFrame, bias_threshold: float = 5.0) -> TechnicalIndicators:
    """从日K线数据计算技术指标"""
    if df is None or df.empty or len(df) < 5:
        return TechnicalIndicators()

    close = df["close"]

    ma5 = round(float(close.rolling(5).mean().iloc[-1]), 2) if len(close) >= 5 else 0.0
    ma10 = round(float(close.rolling(10).mean().iloc[-1]), 2) if len(close) >= 10 else 0.0
    ma20 = round(float(close.rolling(20).mean().iloc[-1]), 2) if len(close) >= 20 else 0.0
    ma60 = round(float(close.rolling(60).mean().iloc[-1]), 2) if len(close) >= 60 else 0.0

    is_bullish = ma5 > ma10 > ma20 if ma5 and ma10 and ma20 else False

    current_price = float(close.iloc[-1])
    bias = 0.0
    if ma20 > 0:
        bias = round((current_price - ma20) / ma20 * 100, 2)

    volume_ratio = 0.0
    if "volume" in df.columns and len(df) >= 5:
        vol = df["volume"]
        avg_vol_5 = vol.rolling(5).mean().iloc[-1] if len(vol) >= 5 else 0
        if avg_vol_5 and avg_vol_5 > 0:
            volume_ratio = round(float(vol.iloc[-1]) / float(avg_vol_5), 2)

    recent_trend = "震荡"
    if is_bullish:
        recent_trend = "多头排列"
    elif ma5 < ma10 < ma20 if ma5 and ma10 and ma20 else False:
        recent_trend = "空头排列"

    return TechnicalIndicators(
        ma5=ma5,
        ma10=ma10,
        ma20=ma20,
        ma60=ma60,
        is_bullish_alignment=is_bullish,
        bias=bias,
        volume_ratio=volume_ratio,
        recent_trend=recent_trend,
    )


class StockAnalyzer:
    """个股分析引擎"""

    def __init__(
        self,
        data_provider: MarketDataProvider,
        llm_client: LLMClient,
        search_engines: list[NewsSearchEngine],
        config: SkillConfig,
    ):
        self.data_provider = data_provider
        self.llm = llm_client
        self.search_engines = search_engines
        self.config = config

    async def analyze(self, code: str) -> StockAnalysisResult:
        """执行个股分析"""
        logger.info("[个股分析] 开始采集数据: %s", code)

        stock_info = await self.data_provider.get_stock_info(code)
        logger.debug("[个股分析] 股票信息: %s(%s) 行业=%s", stock_info.name, stock_info.code, stock_info.industry)

        logger.info("[个股分析] 并行采集数据...")
        gather_start = asyncio.get_event_loop().time()

        daily_data, realtime, chip, capital_flow, valuation, financial, news = await asyncio.gather(
            self.data_provider.get_daily_data(code, 120),
            self.data_provider.get_realtime_quote(code),
            self._get_chip(code),
            self._get_capital_flow(code),
            self._get_valuation(code),
            self._get_financial_data(code),
            self._search_news(stock_info.name, stock_info.code),
            return_exceptions=True,
        )

        gather_elapsed = asyncio.get_event_loop().time() - gather_start
        logger.info("[个股分析] 并行采集完成 耗时%.2fs", gather_elapsed)

        if isinstance(daily_data, Exception):
            logger.warning("[个股分析] 日K线采集异常: %s", daily_data)
            daily_data = pd.DataFrame()
        if isinstance(realtime, Exception):
            logger.warning("[个股分析] 实时行情采集异常: %s", realtime)
            realtime = RealtimeQuote()
        if isinstance(chip, Exception):
            logger.warning("[个股分析] 筹码分布采集异常: %s", chip)
            chip = None
        if isinstance(capital_flow, Exception):
            logger.warning("[个股分析] 主力资金采集异常: %s", capital_flow)
            capital_flow = None
        if isinstance(valuation, Exception):
            logger.warning("[个股分析] 估值数据采集异常: %s", valuation)
            valuation = None
        if isinstance(financial, Exception):
            logger.warning("[个股分析] 财务数据采集异常: %s", financial)
            financial = None
        if isinstance(news, Exception):
            logger.warning("[个股分析] 新闻搜索异常: %s", news)
            news = []

        logger.debug("[个股分析] 日K线: %d条", len(daily_data) if daily_data is not None else 0)
        logger.debug("[个股分析] 实时行情: price=%.2f", realtime.price if isinstance(realtime, RealtimeQuote) else 0)
        logger.debug("[个股分析] 筹码: %s", "有" if chip else "无")
        logger.debug("[个股分析] 主力资金: %s", "有" if capital_flow else "无")
        logger.debug("[个股分析] 估值: %s", "有" if valuation else "无")
        logger.debug("[个股分析] 财务: %s", "有" if financial else "无")
        logger.debug("[个股分析] 新闻: %d条", len(news) if isinstance(news, list) else 0)

        if isinstance(news, list):
            news = news[:5]

        tech = calculate_technical_indicators(daily_data, self.config.bias_threshold)
        logger.debug("[个股分析] 技术指标: MA5=%.2f MA20=%.2f 多头排列=%s 乖离=%.2f%%",
                     tech.ma5, tech.ma20, tech.is_bullish_alignment, tech.bias)

        logger.info("[个股分析] 数据采集完成，开始调用 LLM 分析: %s", code)

        system_prompt = STOCK_ANALYSIS_SYSTEM_PROMPT.format(
            bias_threshold=self.config.bias_threshold,
            news_max_age_days=self.config.news_max_age_days,
        )
        user_prompt = self._build_user_prompt(stock_info, realtime, tech, chip, capital_flow, valuation, financial, news)

        try:
            result_dict = await self.llm.analyze_json(system_prompt, user_prompt)
            result = self._parse_result(stock_info, result_dict, news)

            summaries = result_dict.get("news_summaries", [])
            if isinstance(summaries, list):
                for i, item in enumerate(news):
                    if i < len(summaries) and summaries[i]:
                        item.snippet = str(summaries[i])

            result.stock_info = stock_info
            result.realtime = realtime
            result.tech = tech
            result.chip = chip
            result.capital_flow = capital_flow
            result.valuation = valuation
            result.financial = financial
            result.news = news
            logger.info("[个股分析] LLM 分析完成: %s → %s (评分%d, %s)",
                        code, result.action, result.score, result.trend)
            return result
        except Exception as e:
            logger.error("个股分析 LLM 调用失败 %s: %s", code, e)
            return StockAnalysisResult(
                stock_code=code,
                stock_name=stock_info.name,
                core_conclusion=f"分析失败: {e}",
                raw_report="",
                stock_info=stock_info,
                realtime=realtime,
                tech=tech,
                chip=chip,
                capital_flow=capital_flow,
                valuation=valuation,
                financial=financial,
                news=news,
            )

    async def _get_chip(self, code: str) -> Optional[ChipDistribution]:
        """获取筹码分布"""
        if not self.config.enable_chip:
            return None
        try:
            return await self.data_provider.get_chip_distribution(code)
        except Exception as e:
            logger.warning("获取筹码分布失败 %s: %s", code, e)
            return None

    async def _get_capital_flow(self, code: str) -> Optional[CapitalFlow]:
        try:
            return await self.data_provider.get_capital_flow(code)
        except Exception as e:
            logger.warning("获取主力资金流向失败 %s: %s", code, e)
            return None

    async def _get_valuation(self, code: str) -> Optional[Valuation]:
        try:
            return await self.data_provider.get_valuation(code)
        except Exception as e:
            logger.warning("获取估值数据失败 %s: %s", code, e)
            return None

    async def _get_financial_data(self, code: str) -> Optional[FinancialData]:
        try:
            return await self.data_provider.get_financial_data(code)
        except Exception as e:
            logger.warning("获取财务数据失败 %s: %s", code, e)
            return None

    async def _search_news(self, stock_name: str, stock_code: str) -> list[NewsItem]:
        """搜索新闻舆情"""
        if not self.search_engines:
            logger.debug("[个股分析] 未配置搜索引擎，跳过新闻搜索")
            return []

        for engine in self.search_engines:
            try:
                if engine.name == "MiaoxiangSearch":
                    query = f"{stock_name} 最新新闻 研报"
                else:
                    query = f"{stock_name} {stock_code} 股票 最新消息"
                results = await engine.search(query, self.config.news_max_age_days)
                if results:
                    logger.debug("[个股分析] 搜索引擎 %s 返回 %d 条新闻", engine.name, len(results))
                    return results
            except Exception as e:
                logger.warning("搜索引擎 %s 失败: %s", engine.name, e)
                continue
        logger.debug("[个股分析] 所有搜索引擎均未返回新闻")
        return []

    def _build_user_prompt(
        self,
        stock_info: StockInfo,
        realtime: RealtimeQuote,
        tech: TechnicalIndicators,
        chip: Optional[ChipDistribution],
        capital_flow: Optional[CapitalFlow],
        valuation: Optional[Valuation],
        financial: Optional[FinancialData],
        news: list[NewsItem],
    ) -> str:
        news_text = "暂无资讯数据"
        if news:
            limited = news[:5]
            lines = []
            for i, item in enumerate(limited, 1):
                type_tag = {"report": "[研报]", "announcement": "[公告]"}.get(item.info_type, "[新闻]")
                source_tag = f" [{item.source}]" if item.source else ""
                text = item.content or item.snippet
                if text and len(text) > 2000:
                    text = text[:2000] + "..."
                lines.append(f"{i}. {type_tag} [{item.date}] {item.title}{source_tag}\n{text}")
            news_text = "\n\n".join(lines)

        chip_info = chip or ChipDistribution()

        valuation_text = "暂无估值数据"
        if valuation:
            parts = []
            if valuation.pe_ttm > 0:
                parts.append(f"- 市盈率(TTM)：{valuation.pe_ttm:.1f}")
            if valuation.pb > 0:
                parts.append(f"- 市净率：{valuation.pb:.2f}")
            if valuation.pe_percentile > 0:
                parts.append(f"- PE历史分位：{valuation.pe_percentile:.1f}%")
            if valuation.pb_percentile > 0:
                parts.append(f"- PB历史分位：{valuation.pb_percentile:.1f}%")
            valuation_text = "\n".join(parts) if parts else "暂无估值数据"

        financial_text = "暂无财务数据"
        if financial:
            parts = []
            if financial.net_profit != 0:
                parts.append(f"- 归母净利润：{financial.net_profit:.0f}元")
            if financial.revenue != 0:
                parts.append(f"- 营业收入：{financial.revenue:.0f}元")
            if financial.net_profit_yoy != 0:
                parts.append(f"- 净利润同比增长：{financial.net_profit_yoy:.2f}%")
            if financial.revenue_yoy != 0:
                parts.append(f"- 营收同比增长：{financial.revenue_yoy:.2f}%")
            if financial.roe != 0:
                parts.append(f"- 净资产收益率(ROE)：{financial.roe:.2f}%")
            if financial.gross_margin != 0:
                parts.append(f"- 毛利率：{financial.gross_margin:.2f}%")
            if financial.debt_ratio != 0:
                parts.append(f"- 资产负债率：{financial.debt_ratio:.2f}%")
            if financial.forecast_profit != 0:
                parts.append(f"- 预测净利润中值：{financial.forecast_profit:.0f}元")
            if financial.forecast_growth != 0:
                parts.append(f"- 预测增长率：{financial.forecast_growth:.2f}%")
            if financial.institution_holding_pct != 0:
                parts.append(f"- 机构持股比例：{financial.institution_holding_pct:.2f}%")
            financial_text = "\n".join(parts) if parts else "暂无财务数据"

        capital_flow_text = "暂无主力资金数据"
        if capital_flow:
            parts = []
            if capital_flow.super_large_net != 0:
                parts.append(f"- 超大单净额：{capital_flow.super_large_net:.0f}元")
            if capital_flow.large_net != 0:
                parts.append(f"- 大单净额：{capital_flow.large_net:.0f}元")
            if capital_flow.medium_net != 0:
                parts.append(f"- 中单净额：{capital_flow.medium_net:.0f}元")
            if capital_flow.small_net != 0:
                parts.append(f"- 小单净额：{capital_flow.small_net:.0f}元")
            if capital_flow.ddx != 0:
                parts.append(f"- DDX(大单动向)：{capital_flow.ddx:.2f}")
            if capital_flow.ddy != 0:
                parts.append(f"- DDY(筹码集中度变化)：{capital_flow.ddy:.2f}")
            if capital_flow.ddz != 0:
                parts.append(f"- DDZ(资金强度)：{capital_flow.ddz:.2f}")
            capital_flow_text = "\n".join(parts) if parts else "暂无主力资金数据"

        return STOCK_ANALYSIS_USER_PROMPT.format(
            stock_code=stock_info.code,
            stock_name=stock_info.name,
            industry=stock_info.industry or "未知",
            market_cap=f"{stock_info.market_cap:.0f}" if stock_info.market_cap else "未知",
            price=realtime.price or "未知",
            change_pct=f"{realtime.change_pct:.2f}" if realtime.change_pct else "0.00",
            volume=f"{realtime.volume:.0f}" if realtime.volume else "0",
            turnover=f"{realtime.turnover:.0f}" if realtime.turnover else "0",
            high=realtime.high or "未知",
            low=realtime.low or "未知",
            open_price=realtime.open or "未知",
            amplitude=f"{realtime.amplitude:.2f}" if realtime.amplitude else "0.00",
            turnover_rate=f"{realtime.turnover_rate:.2f}" if realtime.turnover_rate else "0.00",
            valuation_text=valuation_text,
            financial_text=financial_text,
            capital_flow_text=capital_flow_text,
            ma5=tech.ma5 or "未知",
            ma10=tech.ma10 or "未知",
            ma20=tech.ma20 or "未知",
            ma60=tech.ma60 or "未知",
            bullish_alignment="是 ✓" if tech.is_bullish_alignment else "否 ✗",
            bias=f"{tech.bias:.2f}" if tech.bias else "0.00",
            volume_ratio=f"{tech.volume_ratio:.2f}" if tech.volume_ratio else "0.00",
            recent_trend=tech.recent_trend or "未知",
            profit_ratio=f"{chip_info.profit_ratio:.1f}" if chip_info.profit_ratio else "未知",
            avg_cost=f"{chip_info.avg_cost:.2f}" if chip_info.avg_cost else "未知",
            concentration=f"{chip_info.concentration:.2f}" if chip_info.concentration else "未知",
            profit_90_cost=f"{chip_info.profit_90_cost:.2f}" if chip_info.profit_90_cost else "未知",
            profit_10_cost=f"{chip_info.profit_10_cost:.2f}" if chip_info.profit_10_cost else "未知",
            news_text=news_text,
        )

    def _extract_name_from_news(self, news: list[NewsItem], code: str) -> str:
        """从新闻标题中提取股票名称"""
        for item in news:
            m = re.search(r'([^\s（(]+?)（?' + re.escape(code) + r'）?', item.title)
            if m:
                name = m.group(1).strip()
                if name and len(name) >= 2 and not name.isdigit():
                    return name
        return ""

    def _parse_result(self, stock_info: StockInfo, data: dict, news: list[NewsItem] = None) -> StockAnalysisResult:
        """解析 LLM 返回的结果"""
        checklist = []
        for item in data.get("checklist", []):
            if isinstance(item, dict):
                checklist.append(CheckItem(
                    condition=str(item.get("condition", "")),
                    status=str(item.get("status", "")),
                    detail=str(item.get("detail", "")),
                ))

        buy_price = data.get("buy_price")
        stop_loss = data.get("stop_loss_price")
        target = data.get("target_price")

        stock_name = stock_info.name
        if (not stock_name or stock_name == stock_info.code) and news:
            extracted = self._extract_name_from_news(news, stock_info.code)
            if extracted:
                stock_name = extracted

        return StockAnalysisResult(
            stock_code=stock_info.code,
            stock_name=stock_name,
            core_conclusion=str(data.get("core_conclusion", "")),
            score=int(data.get("score", 0) or 0),
            action=str(data.get("action", "")),
            trend=str(data.get("trend", "")),
            buy_price=float(buy_price) if buy_price is not None else None,
            stop_loss_price=float(stop_loss) if stop_loss is not None else None,
            target_price=float(target) if target is not None else None,
            checklist=checklist,
            risk_alerts=[str(a) for a in data.get("risk_alerts", [])],
            positive_catalysts=[str(c) for c in data.get("positive_catalysts", [])],
            strategy=str(data.get("strategy", "")),
            raw_report=str(data.get("report", "")),
        )
