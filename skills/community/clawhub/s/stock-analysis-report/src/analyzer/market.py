from __future__ import annotations

import logging

from src.analyzer.prompts import MARKET_ANALYSIS_SYSTEM_PROMPT, MARKET_ANALYSIS_USER_PROMPT
from src.config import SkillConfig
from src.data.provider import MarketDataProvider
from src.llm.client import LLMClient
from src.models import MarketAnalysisResult, MarketOverview

logger = logging.getLogger(__name__)


class MarketAnalyzer:
    """市场分析引擎"""

    def __init__(
        self,
        data_provider: MarketDataProvider,
        llm_client: LLMClient,
        config: SkillConfig,
    ):
        self.data_provider = data_provider
        self.llm = llm_client
        self.config = config

    async def analyze(self) -> MarketAnalysisResult:
        """执行市场分析"""
        logger.info("[市场分析] 开始采集市场数据...")

        overview = await self.data_provider.get_market_overview()

        logger.info("[市场分析] 数据采集完成: 指数%d个, 涨%d/跌%d, 领涨%d/领跌%d板块",
                    len(overview.indices),
                    overview.statistics.up_count, overview.statistics.down_count,
                    len(overview.top_sectors), len(overview.bottom_sectors))
        logger.info("[市场分析] 开始调用 LLM 分析...")

        system_prompt = MARKET_ANALYSIS_SYSTEM_PROMPT
        user_prompt = self._build_user_prompt(overview)

        try:
            result_dict = await self.llm.analyze_json(system_prompt, user_prompt)
            result = self._parse_result(overview, result_dict)
            logger.info("[市场分析] LLM 分析完成: 情绪=%s", result.sentiment)
            return result
        except Exception as e:
            logger.error("市场分析 LLM 调用失败: %s", e)
            return MarketAnalysisResult(
                core_conclusion=f"分析失败: {e}",
                raw_report="",
            )

    def _build_user_prompt(self, overview: MarketOverview) -> str:
        """组装市场分析 Prompt"""
        indices_lines = []
        for idx in overview.indices:
            emoji = "🟢" if idx.change_pct > 0 else "🔴" if idx.change_pct < 0 else "⚪"
            indices_lines.append(
                f"- {emoji} {idx.name}: {idx.close:.2f} ({'+' if idx.change_pct > 0 else ''}{idx.change_pct:.2f}%)"
            )
        indices_text = "\n".join(indices_lines) if indices_lines else "暂无数据"

        top_lines = []
        for s in overview.top_sectors:
            top_lines.append(f"- {s.name}: +{s.change_pct:.2f}%")
        top_sectors_text = "\n".join(top_lines) if top_lines else "暂无数据"

        bottom_lines = []
        for s in overview.bottom_sectors:
            bottom_lines.append(f"- {s.name}: {s.change_pct:.2f}%")
        bottom_sectors_text = "\n".join(bottom_lines) if bottom_lines else "暂无数据"

        return MARKET_ANALYSIS_USER_PROMPT.format(
            indices_text=indices_text,
            up_count=overview.statistics.up_count,
            down_count=overview.statistics.down_count,
            flat_count=overview.statistics.flat_count,
            limit_up_count=overview.statistics.limit_up_count,
            limit_down_count=overview.statistics.limit_down_count,
            top_sectors_text=top_sectors_text,
            bottom_sectors_text=bottom_sectors_text,
        )

    def _parse_result(self, overview: MarketOverview, data: dict) -> MarketAnalysisResult:
        """解析 LLM 返回的结果"""
        from datetime import datetime

        return MarketAnalysisResult(
            date=datetime.now().strftime("%Y-%m-%d"),
            core_conclusion=str(data.get("core_conclusion", "")),
            indices=overview.indices,
            statistics=overview.statistics,
            top_sectors=overview.top_sectors,
            bottom_sectors=overview.bottom_sectors,
            sentiment=str(data.get("sentiment", "")),
            strategy=str(data.get("strategy", "")),
            raw_report=str(data.get("report", "")),
        )
