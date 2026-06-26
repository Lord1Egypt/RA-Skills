from __future__ import annotations

import dataclasses
import logging
import time
from typing import Optional

from src.analyzer.market import MarketAnalyzer
from src.analyzer.stock import StockAnalyzer
from src.config import SkillConfig, setup_logging
from src.data.akshare_provider import AkShareProvider
from src.data.efinance_provider import EfinanceProvider
from src.data.manager import DataProviderManager
from src.data.miaoxiang_provider import MiaoxiangProvider
from src.llm.client import LLMClient
from src.models import MarketAnalysisResult, StockAnalysisResult
from src.report import save_report
from src.search.base import NewsSearchEngine
from src.search.bocha import BochaSearch
from src.search.brave import BraveSearch
from src.search.miaoxiang import MiaoxiangSearch
from src.search.serpapi import SerpAPISearch
from src.search.tavily import TavilySearch

logger = logging.getLogger(__name__)


def _dataclass_to_dict(obj) -> dict | list | str | int | float | bool | None:
    """递归将 dataclass 转为 JSON 可序列化字典"""
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return {k: _dataclass_to_dict(v) for k, v in dataclasses.asdict(obj).items()}
    if isinstance(obj, list):
        return [_dataclass_to_dict(item) for item in obj]
    if isinstance(obj, dict):
        return {k: _dataclass_to_dict(v) for k, v in obj.items()}
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    return str(obj)


def _build_data_provider(config: SkillConfig) -> DataProviderManager:
    providers = []
    if config.mx_apikey:
        providers.append(MiaoxiangProvider(config.mx_apikey))
    providers.extend([EfinanceProvider(), AkShareProvider()])
    return DataProviderManager(providers)


def _build_search_engines(config: SkillConfig) -> list[NewsSearchEngine]:
    engines: list[NewsSearchEngine] = []
    if config.mx_apikey:
        engines.append(MiaoxiangSearch(config.mx_apikey))
    if config.serpapi_key:
        engines.append(SerpAPISearch(config.serpapi_key))
    if config.tavily_key:
        engines.append(TavilySearch(config.tavily_key))
    if config.brave_key:
        engines.append(BraveSearch(config.brave_key))
    if config.bocha_key:
        engines.append(BochaSearch(config.bocha_key))
    return engines


def _build_llm_client(config: SkillConfig) -> LLMClient:
    return LLMClient(
        base_url=config.llm_base_url,
        api_key=config.llm_api_key,
        model=config.llm_model,
    )


async def analyze_stock(code: str, config: Optional[SkillConfig] = None,
                        save: bool = False, output_dir: Optional[str] = None) -> StockAnalysisResult:
    """个股分析 - 供智能体调用的主入口

    Args:
        code: A股股票代码
        config: 配置对象，为 None 时从环境变量加载
        save: 是否保存 Markdown 报告到 reports/ 目录
        output_dir: 自定义报告输出目录
    """
    if config is None:
        config = SkillConfig()

    setup_logging()

    errors = config.validate()
    if errors:
        logger.error("配置校验失败: %s", "; ".join(errors))
        return StockAnalysisResult(
            stock_code=code,
            core_conclusion=f"配置错误: {'; '.join(errors)}",
        )

    logger.info("========== 个股分析开始 [%s] ==========", code)
    logger.info("配置: model=%s, base_url=%s, 搜索引擎=%d个, 筹码=%s",
                config.llm_model, config.llm_base_url,
                sum(1 for k in ["serpapi_key", "tavily_key", "brave_key", "bocha_key"]
                    if getattr(config, k, "")),
                "启用" if config.enable_chip else "禁用")

    start = time.monotonic()
    data_provider = _build_data_provider(config)
    llm_client = _build_llm_client(config)
    search_engines = _build_search_engines(config)

    analyzer = StockAnalyzer(
        data_provider=data_provider,
        llm_client=llm_client,
        search_engines=search_engines,
        config=config,
    )

    result = await analyzer.analyze(code)
    elapsed = time.monotonic() - start
    logger.info("========== 个股分析完成 [%s] 耗时%.2fs: %s ==========",
                code, elapsed, result.core_conclusion[:50] if result.core_conclusion else "无结论")
    if save:
        save_report(result, output_dir)
    return result


async def analyze_market(config: Optional[SkillConfig] = None,
                         save: bool = False, output_dir: Optional[str] = None) -> MarketAnalysisResult:
    """市场分析 - 供智能体调用的主入口

    Args:
        config: 配置对象，为 None 时从环境变量加载
        save: 是否保存 Markdown 报告到 reports/ 目录
        output_dir: 自定义报告输出目录
    """
    if config is None:
        config = SkillConfig()

    setup_logging()

    errors = config.validate()
    if errors:
        logger.error("配置校验失败: %s", "; ".join(errors))
        return MarketAnalysisResult(
            core_conclusion=f"配置错误: {'; '.join(errors)}",
        )

    logger.info("========== 市场分析开始 ==========")
    logger.info("配置: model=%s, base_url=%s", config.llm_model, config.llm_base_url)

    start = time.monotonic()
    data_provider = _build_data_provider(config)
    llm_client = _build_llm_client(config)

    analyzer = MarketAnalyzer(
        data_provider=data_provider,
        llm_client=llm_client,
        config=config,
    )

    result = await analyzer.analyze()
    elapsed = time.monotonic() - start
    logger.info("========== 市场分析完成 耗时%.2fs: %s ==========",
                elapsed, result.core_conclusion[:50] if result.core_conclusion else "无结论")
    if save:
        save_report(result, output_dir)
    return result


async def handler(input: dict, context: Optional[dict] = None) -> dict:
    """OpenClaw Skill 标准入口

    Args:
        input: {"mode": "stock"|"market", "code": "600519", ...config overrides}
        context: OpenClaw 运行时上下文

    Returns:
        JSON 可序列化的分析结果字典
    """
    try:
        context = context or {}
        mode = input.get("mode", "stock")
        save = input.get("save", False)
        output_dir = input.get("output_dir")

        config_overrides = {k: v for k, v in input.items() if k not in ("mode", "code", "save", "output_dir")}
        config = SkillConfig(**config_overrides) if config_overrides else None

        if mode == "market":
            result = await analyze_market(config, save=save, output_dir=output_dir)
        else:
            code = input.get("code", "")
            if not code:
                return {"error": "缺少股票代码，请在 input.code 中提供"}
            result = await analyze_stock(code, config, save=save, output_dir=output_dir)

        return _dataclass_to_dict(result)
    except Exception as e:
        logger.error("Skill 执行失败: %s", e, exc_info=True)
        return {"error": f"Skill execution failed: {e}"}
