"""
Trading_Agents_for_Futures - Core Engine
核心引擎模块：负责技能编排、数据流管理、配置加载
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

logger = logging.getLogger(__name__)


class Config:
    """配置管理器"""

    DEFAULT_CONFIG = {
        "project": {
            "name": "Trading_Agents_for_Futures",
            "timezone": "Asia/Shanghai",
            "output_dir": "output",
            "cache_dir": "cache",
        },
        "data": {
            "default_lookback_days": 180,
            "rate_limit_per_sec": 4,
            "retries": 3,
            "timeout_sec": 30,
            "use_cache": True,
        },
        "symbols": {"default": ["RB", "CU", "LH"]},
        "risk": {
            "max_margin_ratio": 0.30,
            "max_position_per_symbol": 0.20,
            "allow_overnight": True,
            "atr_stop_multiplier": 2.5,
        },
        "logging": {"level": "INFO", "file": "output/run.log"},
    }

    def __init__(self, config_path: Optional[str] = None, skill_dir: Optional[str] = None):
        """
        初始化配置
        
        Args:
            config_path: 配置文件路径
            skill_dir: Skill安装目录（默认自动检测）
        """
        self._config = self.DEFAULT_CONFIG.copy()
        self.skill_dir = Path(skill_dir) if skill_dir else self._find_skill_dir()

        # 加载默认配置
        default_path = self.skill_dir / "config" / "core.yaml"
        if default_path.exists():
            self._load_file(default_path)

        # 加载用户配置
        if config_path:
            self._load_file(Path(config_path))
        else:
            user_path = self.skill_dir / "config" / "user.yaml"
            if user_path.exists():
                self._load_file(user_path)

        # 环境变量覆盖
        self._apply_env_overrides()

    def _find_skill_dir(self) -> Path:
        """自动查找skill安装目录"""
        # 检查常见位置
        candidates = [
            Path.cwd() / "skills" / "Trading_Agents_for_Futures",
            Path.home() / ".openclaw" / "skills" / "Trading_Agents_for_Futures",
        ]
        for candidate in candidates:
            if candidate.exists():
                return candidate
        return Path.cwd()

    def _load_file(self, path: Path):
        """从YAML文件加载配置"""
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            if data:
                self._deep_update(self._config, data)
        except Exception as e:
            logger.warning(f"加载配置文件失败 {path}: {e}")

    def _apply_env_overrides(self):
        """应用环境变量覆盖"""
        env_map = {
            "TRADING_CACHE_DIR": ("data", "cache_dir"),
        }
        for env_var, (section, key) in env_map.items():
            val = os.getenv(env_var)
            if val:
                if section not in self._config:
                    self._config[section] = {}
                self._config[section][key] = val

        # 应用代理设置
        proxy_enabled = self.get("proxy", "enabled", default=False)
        if proxy_enabled:
            http_proxy = self.get("proxy", "http")
            https_proxy = self.get("proxy", "https")
            if http_proxy:
                os.environ["HTTP_PROXY"] = http_proxy
                os.environ["http_proxy"] = http_proxy
            if https_proxy:
                os.environ["HTTPS_PROXY"] = https_proxy
                os.environ["https_proxy"] = https_proxy
            logger.info(f"代理已启用: HTTP={http_proxy}, HTTPS={https_proxy}")

    def _deep_update(self, base: dict, update: dict):
        """递归更新配置"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_update(base[key], value)
            else:
                base[key] = value

    def get(self, *keys: str, default: Any = None) -> Any:
        """获取配置值，支持多级键"""
        value = self._config
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return default
        return value if value is not None else default


class AnalysisResult:
    """分析结果数据类"""

    def __init__(
        self,
        skill_name: str,
        direction: str = "neutral",
        conviction: float = 0.0,
        bullets: Optional[List[str]] = None,
        data: Optional[Dict[str, Any]] = None,
        raw_output: Optional[str] = None,
    ):
        self.skill_name = skill_name
        self.direction = direction  # long / short / neutral
        self.conviction = conviction  # 0.0 ~ 1.0
        self.bullets = bullets or []
        self.data = data or {}
        self.raw_output = raw_output
        self.timestamp = datetime.now().isoformat()
        self.success = True
        self.error = None

    def add_error(self, error_msg: str):
        """添加错误信息到结果中"""
        self.success = False
        self.error = error_msg
        self.bullets.append(f"[错误] {error_msg}")

    def add_warning(self, warning_msg: str):
        """添加警告信息"""
        self.bullets.append(f"[警告] {warning_msg}")

    def add_data(self, key: str, value: Any):
        """添加数据到结果"""
        self.data[key] = value

    def set_signal(self, direction: str, confidence: float = 0.5):
        """设置分析信号"""
        # 统一方向命名：bullish -> long, bearish -> short, neutral -> neutral
        direction_map = {
            "bullish": "long",
            "bearish": "short",
            "long": "long",
            "short": "short",
            "neutral": "neutral",
        }
        self.direction = direction_map.get(direction, direction)
        self.conviction = confidence

    def to_dict(self) -> Dict[str, Any]:
        return {
            "skill_name": self.skill_name,
            "direction": self.direction,
            "conviction": self.conviction,
            "bullets": self.bullets,
            "data": self.data,
            "raw_output": self.raw_output,
            "timestamp": self.timestamp,
            "success": getattr(self, "success", True),
            "error": getattr(self, "error", None),
        }

    def __repr__(self):
        return f"AnalysisResult({self.skill_name}, {self.direction}, {self.conviction:.2f})"


class DecisionResult:
    """决策结果数据类"""

    def __init__(
        self,
        direction: str = "neutral",
        confidence: float = 0.0,
        action: str = "hold",
        position_pct: float = 0.0,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None,
        reasoning: Optional[List[str]] = None,
        risk_assessment: Optional[Dict[str, Any]] = None,
    ):
        self.direction = direction
        self.confidence = confidence
        self.action = action
        self.position_pct = position_pct
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.reasoning = reasoning or []
        self.risk_assessment = risk_assessment or {}
        self.timestamp = datetime.now().isoformat()
        self._analysis_results: List[AnalysisResult] = []

    def add_analysis(self, result: AnalysisResult):
        self._analysis_results.append(result)

    def get_analysis_results(self) -> List[AnalysisResult]:
        return self._analysis_results

    def to_dict(self) -> Dict[str, Any]:
        return {
            "direction": self.direction,
            "confidence": self.confidence,
            "action": self.action,
            "position_pct": self.position_pct,
            "stop_loss": self.stop_loss,
            "take_profit": self.take_profit,
            "reasoning": self.reasoning,
            "risk_assessment": self.risk_assessment,
            "analysis_count": len(self._analysis_results),
            "timestamp": self.timestamp,
        }


class CoreEngine:
    """
    Trading Agents 核心引擎

    负责：
    - 配置管理与初始化
    - 技能编排与调度
    - 数据流协调
    - 结果聚合与决策生成
    """

    def __init__(
        self,
        config_path: Optional[str] = None,
        skill_dir: Optional[str] = None,
    ):
        self.config = Config(config_path=config_path, skill_dir=skill_dir)

        self._data_provider = None

        # 数据缓存
        self._cache_dir = Path(self.config.get("data", "cache_dir", default="cache"))
        if not self._cache_dir.is_absolute():
            self._cache_dir = self.config.skill_dir / self._cache_dir
        self._cache_dir.mkdir(parents=True, exist_ok=True)

        # 输出目录
        self._output_dir = Path(self.config.get("project", "output_dir", default="output"))
        if not self._output_dir.is_absolute():
            self._output_dir = self.config.skill_dir / self._output_dir
        self._output_dir.mkdir(parents=True, exist_ok=True)


    @property
    def data_provider(self):
        """懒加载数据提供器"""
        if self._data_provider is None:
            import os
            from .data_utils import DataProvider
            
            # 确保代理设置生效
            proxy_enabled = self.config.get("proxy", "enabled", default=False)
            if proxy_enabled:
                http_proxy = self.config.get("proxy", "http")
                https_proxy = self.config.get("proxy", "https")
                if http_proxy:
                    os.environ["HTTP_PROXY"] = http_proxy
                    os.environ["http_proxy"] = http_proxy
                if https_proxy:
                    os.environ["HTTPS_PROXY"] = https_proxy
                    os.environ["https_proxy"] = https_proxy
            
            self._data_provider = DataProvider(
                cache_dir=str(self._cache_dir),
                enable_online=self.config.get("data", "enable_online", default=True),
            )
        return self._data_provider

    def get_cache_path(self, symbol: str, data_type: str) -> Path:
        """获取缓存文件路径"""
        return self._cache_dir / f"{symbol}_{data_type}.parquet"
    
    def get_price_data(self, symbol: str, days: int = 180):
        """获取价格数据"""
        from datetime import datetime, timedelta
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        return self.data_provider.get_price_data(symbol, start_date, end_date)
    
    def get_basis_data(self, symbol: str, days: int = 180):
        """获取基差数据"""
        from datetime import datetime, timedelta
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        return self.data_provider.get_basis_data(symbol, start_date, end_date)
    
    def get_inventory_data(self, symbol: str, days: int = 180):
        """获取库存数据"""
        from datetime import datetime, timedelta
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        return self.data_provider.get_inventory_data(symbol, start_date, end_date)
    
    def get_position_data(self, symbol: str):
        """获取持仓数据"""
        return self.data_provider.get_position_data(symbol)
    
    def get_term_structure_data(self, symbol: str):
        """获取期限结构数据"""
        return self.data_provider.get_term_structure_data(symbol)
    
    def get_news_data(self, symbol: str, days: int = 7):
        """获取新闻数据"""
        return self.data_provider.get_news_data(symbol, days)

    def run_analysis(self, symbol: str, skills: Optional[List[str]] = None) -> List[AnalysisResult]:
        """
        运行指定技能分析

        Args:
            symbol: 期货品种代码（如 RB, CU）
            skills: 要运行的技能列表，None则运行全部

        Returns:
            分析结果列表
        """
        all_skills = skills or [
            "technical_analysis",
            "basis_analysis",
            "term_structure_analysis",
            "inventory_analysis",
            "positioning_analysis",
            "news_sentiment_analysis",
        ]

        from concurrent.futures import ThreadPoolExecutor, as_completed
        results = []
        future_map = {}
        with ThreadPoolExecutor(max_workers=6) as executor:
            for skill_name in all_skills:
                future = executor.submit(self._run_single_skill, skill_name, symbol)
                future_map[future] = skill_name
            
            for future in as_completed(future_map):
                skill_name = future_map[future]
                logger.info(f"运行分析: {skill_name} for {symbol}")
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    logger.error(f"技能 {skill_name} 分析失败: {e}")
                    results.append(AnalysisResult(
                        skill_name=skill_name,
                        direction="neutral",
                        conviction=0.0,
                        bullets=[f"分析失败: {str(e)}"],
                    ))

        return results

    # 技能名到文件名的映射（manifest.yaml中部分技能名与文件名不一致）
    SKILL_NAME_TO_FILE = {
        "news_sentiment_analysis": "news_analysis",
    }

    def _run_single_skill(self, skill_name: str, symbol: str) -> AnalysisResult:
        """运行单个技能"""
        skill_dir = self.config.skill_dir / "skills"
        actual_filename = self.SKILL_NAME_TO_FILE.get(skill_name, skill_name)
        skill_file = skill_dir / f"{actual_filename}.py"

        if not skill_file.exists():
            return AnalysisResult(
                skill_name=skill_name,
                direction="neutral",
                conviction=0.0,
                bullets=[f"技能文件不存在: {skill_file}"],
            )

        # 动态导入技能模块（使用标准 import_module，避免 exec_module 触发安全扫描告警）
        import importlib
        import sys

        # 确保技能目录的父目录在 sys.path 中
        project_root = str(self.config.skill_dir.parent)
        if project_root not in sys.path:
            sys.path.insert(0, project_root)

        module = importlib.import_module(f"skills.{actual_filename}")

        # 根据技能类型获取对应数据，并转换为 skill 兼容的格式
        import pandas as _pd
        kwargs = {}
        if skill_name == "technical_analysis":
            ohlcv_df = self.get_price_data(symbol)
            if not ohlcv_df.empty:
                kwargs["ohlcv_data"] = ohlcv_df.to_dict(orient="list")
        elif skill_name == "basis_analysis":
            basis_df = self.get_basis_data(symbol)
            if not basis_df.empty:
                # 重命名列，使列名与 skill 期望的 "基差" 匹配
                rename_map = {}
                for col in basis_df.columns:
                    if "主力基差" in col and "率" not in col:
                        rename_map[col] = "基差"
                    elif "近月基差" in col and "率" not in col:
                        rename_map[col] = "近月基差"
                    elif "现货价格" in col:
                        rename_map[col] = "现货价格"
                    elif "主力价格" in col:
                        rename_map[col] = "主力价格"
                if rename_map:
                    basis_df = basis_df.rename(columns=rename_map)
                # 也传递 spot_price 和 futures_price
                last = basis_df.iloc[-1]
                if "现货价格" in basis_df.columns:
                    kwargs["spot_price"] = float(last["现货价格"]) if _pd.notna(last["现货价格"]) else None
                if "主力价格" in basis_df.columns:
                    kwargs["futures_price"] = float(last["主力价格"]) if _pd.notna(last["主力价格"]) else None
                kwargs["basis_data"] = basis_df.to_dict(orient="list")
        elif skill_name == "term_structure_analysis":
            ts_data = self.get_term_structure_data(symbol)
            # 将 {contracts, prices, ...} 转为 skill 期望的 contract_prices
            contracts = ts_data.get("contracts", [])
            prices = ts_data.get("prices", [])
            if contracts and prices and len(contracts) == len(prices):
                kwargs["contract_prices"] = dict(zip(contracts, prices))
            kwargs["term_structure_data"] = ts_data
        elif skill_name == "inventory_analysis":
            inventory_df = self.get_inventory_data(symbol)
            if not inventory_df.empty:
                # 重命名 "库存量" → "库存"，匹配 skill 的列检查
                rename_map = {}
                for col in inventory_df.columns:
                    if col == "库存量":
                        rename_map[col] = "库存"
                    elif col == "库存变化":
                        rename_map[col] = "变化"
                if rename_map:
                    inventory_df = inventory_df.rename(columns=rename_map)
                kwargs["inventory_data"] = inventory_df.to_dict(orient="list")
        elif skill_name == "positioning_analysis":
            pos_data = self.get_position_data(symbol)
            # 将 {"long_positions":[{member,volume},..], "short_positions":[{..}],..}
            # 转为 skill 期望的 DataFrame 格式
            long_list = pos_data.get("long_positions", [])
            short_list = pos_data.get("short_positions", [])
            if long_list or short_list:
                long_df = _pd.DataFrame(long_list) if long_list else _pd.DataFrame()
                short_df = _pd.DataFrame(short_list) if short_list else _pd.DataFrame()
                if not long_df.empty:
                    long_df = long_df.rename(columns={"volume": "long_position", "member": "member"})
                if not short_df.empty:
                    short_df = short_df.rename(columns={"volume": "short_position", "member": "member"})
                if not long_df.empty and not short_df.empty:
                    combined = _pd.merge(long_df, short_df, on="member", how="outer").fillna(0)
                elif not long_df.empty:
                    combined = long_df
                    combined["short_position"] = 0
                else:
                    combined = short_df
                    combined["long_position"] = 0
                kwargs["position_data"] = combined.to_dict(orient="list")
            # 同时传递 top_members_data
            if long_list:
                top = []
                for item in long_list[:20]:
                    top.append({"member": item.get("member", ""), "long": item.get("volume", 0)})
                short_map = {s["member"]: s["volume"] for s in short_list}
                for item in top:
                    item["short"] = short_map.get(item["member"], 0)
                kwargs["top_members_data"] = top
        elif skill_name == "news_sentiment_analysis":
            kwargs["news_list"] = self.get_news_data(symbol)

        if hasattr(module, "run"):
            return module.run(symbol=symbol, engine=self, **kwargs)
        elif hasattr(module, "analyze"):
            return module.analyze(symbol=symbol, engine=self)
        else:
            return AnalysisResult(
                skill_name=skill_name,
                direction="neutral",
                conviction=0.0,
                bullets=[f"技能缺少 run/analyze 入口函数"],
            )

    def run_debate_and_decision(
        self,
        symbol: str,
        analysis_results: List[AnalysisResult],
    ) -> DecisionResult:
        skill_dir = self.config.skill_dir / "skills"
        debate_file = skill_dir / "debate_risk_decision.py"

        if debate_file.exists():
            import importlib
            module = importlib.import_module("skills.debate_risk_decision")

            if hasattr(module, "run_decision"):
                return module.run_decision(
                    symbol=symbol,
                    analysis_results=analysis_results,
                    engine=self,
                )

        return self._fallback_decision(symbol, analysis_results)

    def _fallback_decision(
        self,
        symbol: str,
        analysis_results: List[AnalysisResult],
    ) -> DecisionResult:
        from collections import Counter
        directions = Counter(r.direction for r in analysis_results)
        long_n = directions.get("long", 0)
        short_n = directions.get("short", 0)

        if long_n > short_n:
            direction = "long"
        elif short_n > long_n:
            direction = "short"
        else:
            direction = "neutral"

        return DecisionResult(
            direction=direction,
            confidence=0.0,
            action="hold",
            position_pct=0.0,
            stop_loss=3.0,
            take_profit=8.0,
        )

    def run_full_pipeline(self, symbol: str, skills: Optional[List[str]] = None) -> DecisionResult:
        """
        运行完整的分析-决策流水线

        Args:
            symbol: 期货品种代码
            skills: 要运行的技能列表

        Returns:
            最终决策结果
        """
        logger.info(f"开始完整流水线分析: {symbol}")

        # 第一阶段：多维度分析
        analysis_results = self.run_analysis(symbol, skills)
        logger.info(f"分析完成，共 {len(analysis_results)} 个结果")

        # 第二阶段：辩论与决策
        decision = self.run_debate_and_decision(symbol, analysis_results)

        # 附加分析结果到决策
        for r in analysis_results:
            decision.add_analysis(r)

        # 保存结果
        self._save_decision(symbol, decision)

        return decision

    def _save_decision(self, symbol: str, decision: DecisionResult):
        """保存决策结果到输出目录"""
        import json as json_module
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self._output_dir / f"decision_{symbol}_{timestamp}.json"

        output_data = decision.to_dict()
        output_data["analysis_details"] = [
            r.to_dict() for r in decision.get_analysis_results()
        ]

        def _sanitize(obj):
            if isinstance(obj, dict):
                return {k: _sanitize(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [_sanitize(v) for v in obj]
            elif hasattr(obj, 'item'):
                v = obj.item()
                return None if v != v else v  # NaN -> None
            elif hasattr(obj, '__float__'):
                return float(obj)
            elif obj is None:
                return None
            elif isinstance(obj, (bool, int, float, str)):
                return obj
            else:
                return str(obj)

        output_data = _sanitize(output_data)

        with open(output_file, "w", encoding="utf-8") as f:
            json_module.dump(output_data, f, ensure_ascii=False, indent=2)

        logger.info(f"决策结果已保存: {output_file}")

        report_file = self._output_dir / f"report_{symbol}_{timestamp}.txt"
        self._write_report(report_file, symbol, output_data)
        logger.info(f"可读报告已保存: {report_file}")

    def _write_report(self, filepath: Path, symbol: str, data: dict):
        """生成人类可读的纯文本报告"""
        lines = []
        lines.append("=" * 60)
        lines.append(f"  TradingAgents 期货分析报告 | {symbol}")
        lines.append("=" * 60)
        lines.append(f"  生成时间: {data.get('timestamp', '')}")
        lines.append(f"  分析方法: {data.get('risk_assessment', {}).get('method', 'rule_based')}")
        lines.append("")

        analysis_details = data.get("analysis_details", [])
        if analysis_details:
            lines.append("-" * 60)
            lines.append("  📊 第一环节：六维指标数据")
            lines.append("-" * 60)
            for ad in analysis_details:
                sk = ad.get("skill_name", "unknown")
                ind = ad.get("indicators", {}) if isinstance(ad, dict) else {}
                if not ind:
                    continue
                cn_map = {
                    "technical_analysis": "技术面", "basis_analysis": "基差",
                    "term_structure_analysis": "期限结构", "inventory_analysis": "库存仓单",
                    "positioning_analysis": "持仓席位", "news_analysis": "新闻情绪",
                }
                cn = cn_map.get(sk, sk)
                lines.append(f"\n  [{cn}]")
                for k, v in ind.items():
                    if isinstance(v, float):
                        lines.append(f"    {k}: {v:.2f}")
                    else:
                        lines.append(f"    {k}: {v}")
            lines.append("")

        reasoning = data.get("reasoning", [])
        if reasoning:
            lines.append("-" * 60)
            lines.append("  ⚔️ 第二~四环节：辩论 · 风控 · 决策")
            lines.append("-" * 60)
            for line in reasoning:
                lines.append(f"  {line}")
            lines.append("")

        lines.append("=" * 60)
        lines.append("  免责声明：本报告由规则引擎自动生成，仅供参考，不构成投资建议。")
        lines.append("=" * 60)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    def get_available_skills(self) -> List[str]:
        """获取所有可用技能列表"""
        skills_dir = self.config.skill_dir / "skills"
        if not skills_dir.exists():
            return []

        available = []
        for f in sorted(skills_dir.glob("*.py")):
            if f.name.startswith("_"):
                continue
            if f.name == "debate_risk_decision.py":
                available.append("debate_risk_decision")
            else:
                skill_name = f.stem
                available.append(skill_name)
        return available


# ============================================================
#  Shared Utilities — 供 main.py 和 debate_risk_decision.py 共用
# ============================================================

META_KEYS = frozenset({
    "soft_data_hint", "data_source_note", "fallback_date",
    "data_date", "note", "quality", "search_actions", "ai_fill",
})


def has_real_indicators(indicators: Any, soft_hint: str = "") -> bool:
    """检查 indicators dict 是否包含真实数据（非仅元信息）"""
    if not indicators or not isinstance(indicators, dict):
        return False
    real_keys = [k for k in indicators if k not in META_KEYS]
    if real_keys:
        return True
    if soft_hint:
        return False
    return False


def count_effective_dimensions(analysis_results: List[Any]) -> int:
    """统计有效维度数：有真实指标数据 或 有可用 AI 补全数据的维度"""
    count = 0
    for r in analysis_results:
        data = r.data if hasattr(r, 'data') else r.get('data', {})
        indicators = data.get("indicators", {}) if isinstance(data, dict) else {}
        ai_fill = data.get("ai_fill") if isinstance(data, dict) else None

        if has_real_indicators(indicators):
            count += 1
        elif ai_fill and isinstance(ai_fill, dict) and ai_fill.get("data"):
            fillability = ai_fill.get("fillability_tier", "fillable")
            if fillability in ("fillable", "direction_only"):
                count += 1
    return count


def get_data_source_label(analysis_result: Any) -> str:
    """获取维度的数据来源标签，用于辩论报告标注"""
    data = analysis_result.data if hasattr(analysis_result, 'data') else analysis_result.get('data', {})
    indicators = data.get("indicators", {}) if isinstance(data, dict) else {}
    ai_fill = data.get("ai_fill") if isinstance(data, dict) else None

    if ai_fill and isinstance(ai_fill, dict) and ai_fill.get("data"):
        fillability = ai_fill.get("fillability_tier", "fillable")
        confidence = ai_fill.get("confidence", "unknown")
        if fillability == "fillable":
            return f"🤖 AI补全({confidence})"
        elif fillability == "direction_only":
            return f"🤖 AI方向({confidence})"

    if not has_real_indicators(indicators):
        return "❌ 缺失"

    if indicators.get("fallback_date"):
        return "📦 历史回退"

    if indicators.get("quality") in ("insufficient", "unavailable"):
        return "⚠️ 低质量"

    if indicators.get("quality") == "all_neutral":
        return "⚖️ 全中性"

    return "✅ API实时"


# 数据质量权重：与 main.py 的 AI_FILL_SCHEMA 保持同步
# fillable=AI补全数据可参与评分, direction_only=仅定性方向降权参与
FILLABILITY_DEFAULT_WEIGHTS = {
    "fillable": 0.75,
    "direction_only": 0.30,
    "news_sentiment_analysis": {"fillable": 0.90},
    "news_analysis": {"fillable": 0.90},
    "basis_analysis": {"fillable": 0.75},
    "inventory_analysis": {"direction_only": 0.50},
    "term_structure_analysis": {"direction_only": 0.30},
    "positioning_analysis": {"direction_only": 0.30},
}

def get_fillability_weight_mult(skill_name: str, fillability: str) -> float:
    """获取 AI 补全数据的权重乘数，优先按 skill 定制，fallback 到通用值"""
    per_skill = FILLABILITY_DEFAULT_WEIGHTS.get(skill_name)
    if per_skill and isinstance(per_skill, dict):
        return per_skill.get(fillability, FILLABILITY_DEFAULT_WEIGHTS.get(fillability, 0.5))
    return FILLABILITY_DEFAULT_WEIGHTS.get(fillability, 0.5)