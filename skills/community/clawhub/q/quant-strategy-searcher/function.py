from __future__ import annotations
import os
import re
import json
import yaml
import time
import logging
from typing import Any
from collections import Counter
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

import pymysql
import pymysql.cursors

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("racing_quant_ai")


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

def load_db_config(path: str = "config/database.yaml") -> dict:
    path = os.path.join(os.path.dirname(__file__), path) if not os.path.isabs(path) else path
    with open(path, "r") as f:
        cfg = yaml.safe_load(f)
    cfg["password"] = os.getenv("DB_PASSWORD", cfg.get("password", ""))
    return cfg


# ---------------------------------------------------------------------------
# Database connection (context manager)
# ---------------------------------------------------------------------------

class DBConnection:
    def __init__(self, config: dict):
        self.config = config

    def __enter__(self):
        self.conn = pymysql.connect(
            host=self.config["host"],
            port=self.config["port"],
            user=self.config["user"],
            password=self.config["password"],
            database=self.config["database"],
            charset=self.config.get("charset", "utf8mb4"),
            cursorclass=pymysql.cursors.DictCursor,
        )
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()


# ---------------------------------------------------------------------------
# Module 1: Strategy Matcher
# ---------------------------------------------------------------------------

class StrategyMatcher:
    def __init__(self, db_config: dict):
        self.db_config = db_config

    def fetch_all(self) -> list[dict]:
        with DBConnection(self.db_config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT strategy_id, strategy_name_cn, strategy_summ, "
                    "strategy_cat, if_recommended FROM strategy_information"
                )
                return cur.fetchall()

    def search_by_keyword(self, keyword: str) -> list[dict]:
        with DBConnection(self.db_config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM strategy_information "
                    "WHERE strategy_name_cn LIKE %s OR strategy_summ LIKE %s OR strategy_desc LIKE %s",
                    (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"),
                )
                return cur.fetchall()

    def filter_by_category(self, category: str) -> list[dict]:
        with DBConnection(self.db_config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM strategy_information WHERE strategy_cat = %s",
                    (category,),
                )
                return cur.fetchall()

    def filter_recommended(self) -> list[dict]:
        with DBConnection(self.db_config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM strategy_information WHERE if_recommended = 1")
                return cur.fetchall()

    def get_by_id(self, strategy_id: str) -> dict | None:
        with DBConnection(self.db_config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM strategy_information WHERE strategy_id = %s",
                    (strategy_id,),
                )
                return cur.fetchone()

    def semantic_match(self, user_intent: str, top_k: int = 3) -> list[dict]:
        all_strategies = self.fetch_all()
        scored: list[tuple[float, dict]] = []
        for s in all_strategies:
            text = f"{s.get('strategy_name_cn', '')} {s.get('strategy_summ', '')} {s.get('strategy_desc', '')}"
            score = self._text_relevance(user_intent, text)
            scored.append((score, s))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [s for _, s in scored[:top_k]]

    @staticmethod
    def _text_relevance(query: str, target: str) -> float:
        query_lower = query.lower()
        target_lower = target.lower()
        if not query_lower:
            return 0.0
        if query_lower in target_lower:
            return 1.0
        q_chars = set(query_lower.replace(" ", ""))
        t_chars = set(target_lower.replace(" ", ""))
        if not q_chars:
            return 0.0
        intersection = q_chars & t_chars
        return len(intersection) / len(q_chars)


# ---------------------------------------------------------------------------
# Module 2: Position Fetcher
# ---------------------------------------------------------------------------

class PositionFetcher:
    def __init__(self, db_config: dict):
        self.db_config = db_config

    def get_positions(self, strategy_id: str, trade_date: str | None = None) -> dict:
        with DBConnection(self.db_config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT strategy_table FROM strategy_information WHERE strategy_id = %s",
                    (strategy_id,),
                )
                row = cur.fetchone()
                if not row:
                    raise ValueError(f"Strategy {strategy_id} not found")
                table_name = row["strategy_table"]

                if trade_date:
                    cur.execute(
                        f"SELECT trading_info FROM {table_name} WHERE strategy_id = %s AND trade_date = %s "
                        "ORDER BY update_time DESC LIMIT 1",
                        (strategy_id, trade_date),
                    )
                else:
                    cur.execute(
                        f"SELECT trading_info FROM {table_name} WHERE strategy_id = %s "
                        "ORDER BY trade_date DESC, update_time DESC LIMIT 1",
                        (strategy_id,),
                    )
                result = cur.fetchone()
                if not result:
                    return {}

                trading_info = result["trading_info"]
                if isinstance(trading_info, str):
                    return json.loads(trading_info)
                return trading_info

    @staticmethod
    def parse_trading_info(trading_info: dict) -> list[dict]:
        return [
            {"stock_code": code, "weight": float(weight)}
            for code, weight in trading_info.items()
        ]


# ---------------------------------------------------------------------------
# Module 3: Data Sources
# ---------------------------------------------------------------------------

class DataSource(ABC):
    @abstractmethod
    def get_market_data(self, stock_code: str) -> dict:
        ...

    @abstractmethod
    def get_financial_data(self, stock_code: str) -> dict:
        ...

    @abstractmethod
    def get_capital_flow(self, stock_code: str) -> dict:
        ...


class AKShareSource(DataSource):
    _PROXY_DETECTED = False

    @classmethod
    def _check_proxy(cls):
        """检测代理设置，避免代理阻塞导致的超时"""
        if cls._PROXY_DETECTED:
            return True
        for var in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"):
            if os.environ.get(var):
                cls._PROXY_DETECTED = True
                logger.warning("Proxy detected (%s=%s), AKShare may have connection issues", var, os.environ.get(var))
                return True
        return False

    def get_market_data(self, stock_code: str) -> dict:
        try:
            import akshare as ak
            if self._check_proxy():
                return {"code": stock_code, "_proxy_blocked": True}
            df = ak.stock_zh_a_hist(symbol=stock_code, adjust="qfq")
            if df.empty:
                return {}
            latest = df.iloc[-1].to_dict()
            return {
                "code": stock_code,
                "date": str(latest.get("日期", "")),
                "open": float(latest.get("开盘", 0)),
                "close": float(latest.get("收盘", 0)),
                "high": float(latest.get("最高", 0)),
                "low": float(latest.get("最低", 0)),
                "volume": int(latest.get("成交量", 0)),
                "amount": float(latest.get("成交额", 0)),
                "amplitude": float(latest.get("振幅", 0)),
                "pct_change": float(latest.get("涨跌幅", 0)),
                "turnover": float(latest.get("换手率", 0)),
            }
        except Exception as e:
            logger.warning("AKShare market data failed for %s: %s", stock_code, e)
            return {}

    def get_financial_data(self, stock_code: str) -> dict:
        try:
            import akshare as ak
            if self._check_proxy():
                return {}
            df = ak.stock_financial_abstract(symbol=stock_code)
            if df.empty:
                return {}
            latest = df.iloc[-1].to_dict()
            return {str(k): v for k, v in latest.items()}
        except Exception as e:
            logger.warning("AKShare financial data failed for %s: %s", stock_code, e)
            return {}

    def get_capital_flow(self, stock_code: str) -> dict:
        try:
            import akshare as ak
            if self._check_proxy():
                return {}
            df = ak.stock_individual_fund_flow(stock=stock_code, market="sh")
            if df.empty:
                df = ak.stock_individual_fund_flow(stock=stock_code, market="sz")
            if df.empty:
                return {}
            latest = df.iloc[-1].to_dict()
            return {str(k): v for k, v in latest.items()}
        except Exception as e:
            logger.warning("AKShare capital flow failed for %s: %s", stock_code, e)
            return {}


class BaoStockSource(DataSource):
    def __init__(self):
        self._login()

    @staticmethod
    def _login():
        try:
            import baostock as bs
            bs.login()
        except Exception as e:
            logger.warning("BaoStock login failed: %s", e)

    def get_market_data(self, stock_code: str) -> dict:
        try:
            import baostock as bs
        except ImportError:
            logger.warning("baostock not installed, skipping market data for %s", stock_code)
            return {}
        try:
            rs = bs.query_history_k_data_plus(
                stock_code,
                "date,open,close,high,low,volume,amount,pctChange,turn",
                frequency="d", count=1,
            )
            data = []
            while rs.next():
                data.append(rs.get_row_data())
            if not data:
                return {}
            row = data[0]
            return {
                "code": stock_code,
                "date": row[0],
                "open": float(row[1]),
                "close": float(row[2]),
                "high": float(row[3]),
                "low": float(row[4]),
                "volume": int(row[5]),
                "amount": float(row[6]),
                "pct_change": float(row[7]),
                "turnover": float(row[8]),
            }
        except Exception as e:
            logger.warning("BaoStock market data failed for %s: %s", stock_code, e)
            return {}

    def get_financial_data(self, stock_code: str) -> dict:
        try:
            import baostock as bs
        except ImportError:
            logger.warning("baostock not installed, skipping financial data for %s", stock_code)
            return {}
        try:
            rs = bs.query_stock_industry()
            data = {}
            while rs.next():
                row = rs.get_row_data()
                if row[0] == stock_code:
                    data = {"industry": row[1], "industry_code": row[2]}
                    break
            return data
        except Exception as e:
            logger.warning("BaoStock financial data failed for %s: %s", stock_code, e)
            return {}

    def get_capital_flow(self, stock_code: str) -> dict:
        return {}


class WebSearchSource:
    def search_stock(self, stock_code: str, stock_name: str = "") -> list[dict]:
        results = []
        # 1. cn-web-search (优先使用)
        try:
            from cn_web_search import search
            query = f"{stock_code} {stock_name} 股票 分析" if stock_name else f"{stock_code} 股票"
            results = search(query, source="wechat", top_k=5)
            if results:
                return results
        except ImportError:
            pass
        except Exception as e:
            logger.warning("cn-web-search failed for %s: %s", stock_code, e)

        # 2. 备用: 使用 akshare 的新闻接口（含原文链接）
        try:
            import akshare as ak
            code = stock_code.replace(".SH", "").replace(".SZ", "").replace(".BJ", "")
            news_df = ak.stock_news_em(symbol=code)
            if not news_df.empty and len(results) < 5:
                for _, row in news_df.iterrows():
                    results.append({
                        "title": row.get("新闻标题", row.get("title", "")),
                        "source": row.get("文章来源", row.get("source", "")),
                        "date": str(row.get("发布时间", row.get("date", ""))),
                        "content": str(row.get("新闻内容", row.get("content", ""))),
                        "url": str(row.get("新闻链接", row.get("url", ""))),
                        "_source_type": "akshare_news_fallback",
                    })
        except Exception as e:
            logger.warning("Web search AKShare news fallback failed for %s: %s", stock_code, e)

        return results


# ---------------------------------------------------------------------------
# Module 4: Financial Deep Analyzer (财报深度分析引擎)
# 数据源: akshare.stock_financial_abstract_ths (同花顺)
# 广度: 盈利能力/成长性/偿债能力/现金流质量/运营效率 五大维度
# 深度: 多期趋势对比、逐指标评分
# 可信度: 数据源标注、指标完整率、置信等级
# ---------------------------------------------------------------------------

def _parse_ths_val(raw) -> float | None:
    """解析同花顺财务数据值为浮点数"""
    if raw is False or raw is None:
        return None
    if isinstance(raw, (int, float)):
        return float(raw)
    if isinstance(raw, str):
        s = raw.strip()
        if not s or s in ("-", "--", ""):
            return None
        for suffix in ("亿", "万", "元", "％"):
            s = s.replace(suffix, "")
        # 去除百分号 (但保留数值)
        s = s.replace("%", "")
        try:
            return float(s)
        except (ValueError, TypeError):
            return None
    return None


class FinancialDeepAnalyzer:
    """
    深度财报分析引擎（基于同花顺数据）
    """

    # 同花顺 abstract 字段 -> 内部键名映射
    THS_FIELD_MAP: dict[str, str] = {
        "roe": "净资产收益率",
        "net_margin": "销售净利率",
        "revenue_growth": "营业总收入同比增长率",
        "profit_growth": "净利润同比增长率",
        "debt_ratio": "资产负债率",
        "current_ratio": "流动比率",
        "quick_ratio": "速动比率",
        "eps": "基本每股收益",
        "bvps": "每股净资产",
        "operating_cf_per_share": "每股经营现金流",
        "revenue": "营业总收入",
        "net_profit": "净利润",
    }

    DIMENSION_CONFIG = {
        "profitability": {
            "name": "盈利能力",
            "weight": 0.25,
            "indicators": {
                "roe": {"label": "ROE(%)", "ranges": [(20, 10), (15, 8), (10, 6), (5, 4), (-999, 2)]},
                "net_margin": {"label": "净利率(%)", "ranges": [(25, 10), (15, 8), (8, 6), (3, 4), (-999, 2)]},
            },
        },
        "growth": {
            "name": "成长性",
            "weight": 0.25,
            "indicators": {
                "revenue_growth": {"label": "营收增长(%)", "ranges": [(30, 10), (15, 8), (5, 6), (-5, 4), (-999, 2)]},
                "profit_growth": {"label": "净利增长(%)", "ranges": [(30, 10), (15, 8), (5, 6), (-5, 4), (-999, 2)]},
            },
        },
        "solvency": {
            "name": "偿债能力",
            "weight": 0.20,
            "indicators": {
                "debt_ratio": {"label": "资产负债率(%)", "ranges": [(85, 2), (70, 4), (55, 6), (35, 8), (0, 9), (-1, 6)]},
                "current_ratio": {"label": "流动比率", "ranges": [(3.0, 7), (2.0, 9), (1.5, 7), (1.0, 5), (0, 3)]},
                "quick_ratio": {"label": "速动比率", "ranges": [(2.0, 7), (1.2, 8), (0.8, 6), (0.5, 4), (0, 2)]},
            },
        },
        "cash_flow": {
            "name": "现金流质量",
            "weight": 0.15,
            "indicators": {
                "operating_cf_per_share": {"label": "每股经营现金流", "ranges": [(5, 10), (2, 8), (0.5, 6), (0, 4), (-999, 2)]},
            },
        },
        "efficiency": {
            "name": "运营效率",
            "weight": 0.15,
            "indicators": {
                "eps": {"label": "每股收益", "ranges": [(5, 10), (2, 8), (0.5, 6), (0, 4), (-999, 2)]},
            },
        },
    }

    def __init__(self, source: AKShareSource):
        self.source = source

    def get_financial_indicators(self, stock_code: str) -> dict:
        """从同花顺接口获取多期财务指标"""
        try:
            import akshare as ak
            code = stock_code.replace(".SH", "").replace(".SZ", "").replace(".BJ", "")
            df = ak.stock_financial_abstract_ths(symbol=code)
            if df.empty:
                return {}
            records = df.to_dict(orient="records")
            return {
                "records": records,
                "periods_available": len(records),
                "columns": list(df.columns),
                "source": "akshare.stock_financial_abstract_ths",
            }
        except Exception as e:
            logger.warning("THS financial abstract failed for %s: %s", stock_code, e)
            return {}

    def _parse_record(self, rec: dict) -> dict:
        """将同花顺原始记录映射为内部键名并解析数值"""
        result: dict[str, float] = {}
        for key, ths_col in self.THS_FIELD_MAP.items():
            raw_val = rec.get(ths_col)
            parsed = _parse_ths_val(raw_val)
            if parsed is not None:
                result[key] = parsed
        return result

    def _score_single_indicator(self, value: float, ranges: list) -> int:
        for threshold, score in ranges:
            if value >= threshold:
                return score
        return 2

    def _compute_trend(self, latest: float, prev: float | None) -> str:
        if prev is None:
            return ""
        if prev == 0:
            return "↑ 改善" if latest > 0 else ("↓ 恶化" if latest < 0 else "→ 持平")
        change = (latest - prev) / abs(prev)
        if change > 0.05:
            return "↑ 改善"
        elif change < -0.05:
            return "↓ 恶化"
        return "→ 持平"

    @staticmethod
    def _build_data_source_url(stock_code: str) -> dict:
        """生成可追溯的数据源链接"""
        code = stock_code.replace(".SH", "").replace(".SZ", "").replace(".BJ", "")
        return {
            "同花顺财务页面": f"https://basic.10jqka.com.cn/{code}/finance.html",
            "同花顺公司概况": f"https://basic.10jqka.com.cn/{code}/",
            "东方财富财务分析": f"https://emweb.securities.eastmoney.com/PC_HSF10/FinanceSummary/Index?type=web&code={code}",
        }

    def analyze_all(self, stock_code: str) -> dict:
        raw = self.get_financial_indicators(stock_code)
        code = stock_code.replace(".SH", "").replace(".SZ", "").replace(".BJ", "")
        source_urls = self._build_data_source_url(stock_code)
        if not raw or not raw.get("records"):
            return {
                "score": None,
                "confidence": "none",
                "error": "无法获取财务数据",
                "breadth": {"dimensions_analyzed": 0, "total_dimensions": len(self.DIMENSION_CONFIG)},
                "credibility": {"confidence_level": "none", "data_completeness": 0, "data_source_urls": source_urls},
            }

        records = raw["records"]
        # records 按日期升序（最老在前），取最后2期
        latest_record = records[-1]
        latest_raw = self._parse_record(latest_record)
        prev_record = records[-2] if len(records) > 1 else {}
        prev_raw = self._parse_record(prev_record) if prev_record else {}
        latest_period = str(latest_record.get("报告期", ""))
        prev_period = str(prev_record.get("报告期", "")) if prev_record else ""

        dimensions = {}
        total_weighted_score = 0.0
        total_weight = 0.0
        total_indicators_found = 0
        total_indicators = 0

        for dim_key, dim_config in self.DIMENSION_CONFIG.items():
            ind_scores = []
            for ind_key, ind_cfg in dim_config["indicators"].items():
                val = latest_raw.get(ind_key)
                prev_val = prev_raw.get(ind_key)

                if val is not None:
                    score = self._score_single_indicator(val, ind_cfg["ranges"])
                    trend = self._compute_trend(val, prev_val)
                    # 原始字段值（用于追溯验证）
                    ths_col = self.THS_FIELD_MAP.get(ind_key, "")
                    raw_val_latest = str(latest_record.get(ths_col, ""))
                    raw_val_prev = str(prev_record.get(ths_col, "")) if prev_record else ""
                    ind_scores.append({
                        "indicator": ind_cfg["label"],
                        "value": round(val, 2),
                        "score": score,
                        "trend": trend,
                        "previous_value": round(prev_val, 2) if prev_val is not None else None,
                        # 可追溯字段
                        "source_period": latest_period,
                        "source_previous_period": prev_period if prev_record else None,
                        "raw_value_source": raw_val_latest if raw_val_latest != "None" else "",
                        "raw_value_previous": raw_val_prev if raw_val_prev and raw_val_prev != "None" else "",
                        "source_field": ths_col,
                        "data_source_name": "同花顺(iFinD)",
                    })
                    total_indicators_found += 1
                total_indicators += 1

            dim_score = round(
                sum(i["score"] for i in ind_scores) / max(len(ind_scores), 1), 1
            ) if ind_scores else None

            dimensions[dim_key] = {
                "score": dim_score,
                "name": dim_config["name"],
                "indicators": ind_scores,
                "indicators_found": len(ind_scores),
                "indicators_total": len(dim_config["indicators"]),
            }
            if dim_score is not None:
                total_weighted_score += dim_score * dim_config["weight"]
                total_weight += dim_config["weight"]

        composite = round(total_weighted_score / max(total_weight, 0.01), 1) if total_weight > 0 else None
        completeness = total_indicators_found / max(total_indicators, 1)
        periods = raw["periods_available"]

        if completeness >= 0.75 and periods >= 4:
            confidence = "high"
        elif completeness >= 0.5 and periods >= 2:
            confidence = "medium"
        elif completeness > 0:
            confidence = "low"
        else:
            confidence = "none"

        risk_factors = []
        for dim_key, dim_result in dimensions.items():
            if dim_result["score"] is not None and dim_result["score"] < 5:
                for ind in dim_result.get("indicators", []):
                    if ind["score"] < 5:
                        risk_factors.append(
                            f"{dim_result['name']}: {ind['indicator']}={ind['value']}，评分较低"
                        )

        return {
            "score": composite,
            "confidence": confidence,
            "breadth": {
                "dimensions_analyzed": sum(1 for d in dimensions.values() if d["score"] is not None),
                "total_dimensions": len(self.DIMENSION_CONFIG),
                "indicators_analyzed": total_indicators_found,
                "total_indicators": total_indicators,
                "periods_analyzed": periods,
                "data_source": raw.get("source", "unknown"),
            },
            "depth": {
                "dimensions": dimensions,
                "risk_factors": risk_factors[:8],
                "latest_period": str(records[-1].get("报告期", "")),
            },
            "credibility": {
                "confidence_level": confidence,
                "data_completeness": round(completeness, 2),
                "data_source": raw.get("source", "unknown"),
                "data_source_urls": source_urls,
                "analysis_method": "同花顺多期财务指标 + 阈值评分 + 趋势对比 + 维度加权聚合",
            },
        }


# ---------------------------------------------------------------------------
# Module 5: News Deep Analyzer (新闻舆论深度分析引擎)
# ---------------------------------------------------------------------------

class NewsDeepAnalyzer:
    """
    深度新闻舆论分析引擎

    广度: 多渠道新闻搜集（AKShare财经新闻 + 全网搜索），多维度分析
    深度: 逐条情感分类 + 来源可信度评分 + 影响力评估 + 趋势判断
    可信度: 来源权威性评级、分析置信度、覆盖时效范围
    """

    # 来源可信度评级（基于中国财经媒体权威性）
    SOURCE_CREDIBILITY_MAP: dict[str, float] = {
        # 官方/权威媒体
        "人民日报": 0.95, "新华社": 0.95, "央视": 0.92, "经济日报": 0.90,
        "中国证券报": 0.90, "上海证券报": 0.90, "证券时报": 0.90, "证券日报": 0.88,
        # 专业财经媒体
        "第一财经": 0.85, "财联社": 0.82, "21世纪经济报道": 0.85,
        "每日经济新闻": 0.80, "经济观察报": 0.82, "中国经营报": 0.80,
        "中国基金报": 0.80, "国际金融报": 0.78,
        # 主流财经平台
        "东方财富": 0.65, "同花顺": 0.60, "新浪财经": 0.60,
        "网易财经": 0.60, "腾讯财经": 0.60, "搜狐财经": 0.55,
        "金融界": 0.60, "和讯网": 0.60,
        # 投资社区/自媒体
        "雪球": 0.50, "华尔街见闻": 0.65,
        # 官方披露渠道
        "巨潮资讯": 0.92, "上交所": 0.95, "深交所": 0.95,
        "全国中小企业股份转让系统": 0.92,
        # 默认
        "default": 0.40,
    }

    # 正面情感关键词
    POSITIVE_KEYWORDS: list[str] = [
        "增长", "突破", "创新高", "涨停", "利好", "盈利", "分红", "回购",
        "中标", "签约", "合作", "扩张", "升级", "扭亏", "超预期",
        "显著提升", "大幅改善", "强劲增长", "优化", "领先", "龙头",
        "受益", "获批", "放量", "主力增持", "北向资金流入", "资买入",
        "增持", "业绩预增", "高送转", "资产注入", "重组", "借壳",
        "摘帽", "产能释放", "订单", "放量上涨",
    ]

    # 负面情感关键词（按严重程度分级）
    NEGATIVE_KEYWORDS_HIGH: list[str] = [
        "立案", "调查", "处罚", "退市", "ST", "*ST", "破产", "清算",
        "冻结", "失信", "违法", "违规", "逮捕", "刑事", "判刑",
    ]

    NEGATIVE_KEYWORDS_MEDIUM: list[str] = [
        "亏损", "暴跌", "跌停", "减持", "利空", "风险警示", "预警",
        "业绩下滑", "不及预期", "下调", "负面", "萎缩", "恶化",
        "违约", "债务危机", "诉讼", "仲裁",
    ]

    NEGATIVE_KEYWORDS_LOW: list[str] = [
        "主力流出", "资金出逃", "质押", "商誉减值", "高估",
        "质疑", "争议", "疲软", "承压", "放缓",
    ]

    def __init__(self, web_search: WebSearchSource):
        self.web_search = web_search

    # ------------------------------------------------------------------
    # 新闻搜集
    # ------------------------------------------------------------------

    def collect_news(self, stock_code: str, stock_name: str = "") -> list[dict]:
        """多渠道新闻搜集"""
        news_items: list[dict] = []
        seen_titles: set[str] = set()

        # 1. AKShare 东方财富新闻
        try:
            import akshare as ak
            df = ak.stock_news_em(symbol=stock_code)
            if not df.empty:
                for _, row in df.iterrows():
                    item = {str(k): v for k, v in row.to_dict().items()}
                    item["_source_type"] = "akshare_em"
                    item["_channel"] = "财经新闻"
                    title = str(item.get("title", item.get("新闻标题", "")))
                    if title and title not in seen_titles:
                        seen_titles.add(title)
                        news_items.append(item)
        except Exception as e:
            logger.warning("AKShare news (EM) failed for %s: %s", stock_code, e)

        # 2. 全网搜索（多角度查询）
        search_queries = [
            f"{stock_code} {stock_name}",
            f"{stock_code} {stock_name} 最新公告",
        ]
        if stock_name:
            search_queries.append(f"{stock_name} 行业 政策")

        for query in search_queries:
            try:
                results = self.web_search.search_stock(stock_code, query)
                for r in results:
                    title = str(r.get("title", ""))
                    if title and title not in seen_titles:
                        seen_titles.add(title)
                        r["_source_type"] = "web_search"
                        r["_channel"] = "全网搜索"
                        news_items.append(r)
            except Exception:
                pass

        return news_items

    # ------------------------------------------------------------------
    # 情感分析
    # ------------------------------------------------------------------

    def _classify_sentiment(self, text: str) -> tuple[str, float]:
        """
        基于关键词的情感分类
        Returns: (classification, score)
          classification: "positive" | "negative" | "neutral"
          score: -1.0 ~ 1.0 (完全负面 ~ 完全正面)
        """
        if not text:
            return "neutral", 0.0

        text_lower = text.lower()

        # 检查高严重性负面关键词
        for kw in self.NEGATIVE_KEYWORDS_HIGH:
            if kw in text_lower:
                return "negative", -0.9

        # 检查中等严重性负面关键词
        for kw in self.NEGATIVE_KEYWORDS_MEDIUM:
            if kw in text_lower:
                return "negative", -0.6

        # 检查低严重性负面关键词
        for kw in self.NEGATIVE_KEYWORDS_LOW:
            if kw in text_lower:
                return "negative", -0.3

        # 检查正面关键词（计数）
        positive_count = sum(1 for kw in self.POSITIVE_KEYWORDS if kw in text_lower)
        if positive_count >= 3:
            return "positive", min(1.0, 0.3 + positive_count * 0.15)
        elif positive_count >= 1:
            return "positive", 0.3

        return "neutral", 0.0

    def _score_source_credibility(self, source: str) -> float:
        """来源可信度评分"""
        if not source:
            return self.SOURCE_CREDIBILITY_MAP["default"]

        source_clean = source.strip()
        # 精确匹配
        if source_clean in self.SOURCE_CREDIBILITY_MAP:
            return self.SOURCE_CREDIBILITY_MAP[source_clean]

        # 模糊匹配（包含关系）
        for key, score in self.SOURCE_CREDIBILITY_MAP.items():
            if key in source_clean or source_clean in key:
                return score

        # 检测微信公众号
        if "微信" in source_clean or "公众号" in source_clean:
            return 0.45

        return self.SOURCE_CREDIBILITY_MAP["default"]

    def _assess_impact_score(self, sentiment_score: float, credibility: float) -> float:
        """综合评估单条新闻影响力得分"""
        impact = abs(sentiment_score) * 0.6 + credibility * 0.4
        return round(impact, 2)

    # ------------------------------------------------------------------
    # 主分析入口
    # ------------------------------------------------------------------

    def analyze_news(self, stock_code: str, stock_name: str = "") -> dict:
        """深度新闻舆论全量分析"""
        news_items = self.collect_news(stock_code, stock_name)

        if not news_items:
            return {
                "score": 5.0,
                "confidence": "none",
                "message": "未获取到相关新闻/舆情信息",
                "breadth": {"total_articles": 0, "unique_sources": 0},
                "depth": {},
                "credibility": {"confidence_level": "none", "data_completeness": 0},
            }

        # 逐条分析
        analyzed: list[dict] = []
        for item in news_items:
            title = str(item.get("title", item.get("content", item.get("新闻标题", ""))))
            source = str(item.get("source", item.get("来源", item.get("media_name", ""))))
            date_str = str(item.get("date", item.get("发布时间", item.get("create_time", ""))))

            sentiment_class, sentiment_val = self._classify_sentiment(title)
            credibility = self._score_source_credibility(source)
            impact = self._assess_impact_score(sentiment_val, credibility)

            # 提取原文链接和内容摘要用于可追溯
            url = str(item.get("新闻链接", item.get("url", item.get("link", ""))))[:300]
            raw_content = str(item.get("新闻内容", item.get("content", item.get("summary", ""))))
            content_excerpt = raw_content[:200] if raw_content and raw_content != "None" else ""

            analyzed.append({
                "title": title[:120],
                "source": source,
                "source_credibility": credibility,
                "sentiment": sentiment_class,
                "sentiment_score": sentiment_val,
                "impact": impact,
                "date": date_str[:20],
                "channel": item.get("_channel", ""),
                "url": url,
                "content_excerpt": content_excerpt,
            })

        # ------------------------------------------------------------------
        # 聚合分析
        # ------------------------------------------------------------------

        # 情感分布
        sentiment_dist = Counter(a["sentiment"] for a in analyzed)
        # 来源分布
        source_credibility_scores = [a["source_credibility"] for a in analyzed]
        avg_credibility = sum(source_credibility_scores) / max(len(source_credibility_scores), 1)
        # 高影响力文章
        high_impact = [a for a in analyzed if a["impact"] >= 0.5]

        # 综合评分计算
        base_score = 5.0
        sentiment_impact = (
            (sentiment_dist["positive"] - sentiment_dist["negative"])
            / max(len(analyzed), 1)
            * 3
        )
        credibility_bonus = (avg_credibility - 0.5) * 2
        composite_score = base_score + sentiment_impact + credibility_bonus
        composite_score = max(1, min(10, composite_score))

        # 趋势方向
        pos_count = sentiment_dist.get("positive", 0)
        neg_count = sentiment_dist.get("negative", 0)
        if pos_count > neg_count * 1.5:
            trend = "positive"
            trend_cn = "偏正面"
        elif neg_count > pos_count * 1.5:
            trend = "negative"
            trend_cn = "偏负面"
        else:
            trend = "neutral"
            trend_cn = "中性"

        # 置信度
        if len(analyzed) >= 10 and avg_credibility >= 0.7:
            confidence = "high"
        elif len(analyzed) >= 5 and avg_credibility >= 0.5:
            confidence = "medium"
        elif len(analyzed) >= 1:
            confidence = "low"
        else:
            confidence = "none"

        # 热门主题提取（基于高频词）
        all_title_text = " ".join(a["title"] for a in analyzed)
        hot_topics = self._extract_hot_topics(all_title_text, top_n=5)

        # 按时间排序构建完整时间线
        timeline = sorted(analyzed, key=lambda x: x.get("date", ""), reverse=True)

        # 综合情感分析结论
        positive_ratio = sentiment_dist.get("positive", 0) / max(len(analyzed), 1)
        negative_ratio = sentiment_dist.get("negative", 0) / max(len(analyzed), 1)

        if positive_ratio >= 0.5:
            overall_sentiment = "整体偏正面"
            detail = f"正面新闻占比 {positive_ratio:.0%}，市场情绪积极"
        elif negative_ratio >= 0.3:
            overall_sentiment = "整体偏负面"
            detail = f"负面新闻占比 {negative_ratio:.0%}，需关注风险事件"
        elif positive_ratio > negative_ratio:
            overall_sentiment = "中性偏正面"
            detail = f"正面({sentiment_dist.get('positive',0)})多于负面({sentiment_dist.get('negative',0)})，情绪温和积极"
        elif negative_ratio > positive_ratio:
            overall_sentiment = "中性偏负面"
            detail = f"负面({sentiment_dist.get('negative',0)})多于正面({sentiment_dist.get('positive',0)})，存在隐忧"
        else:
            overall_sentiment = "中性"
            detail = "正面与负面新闻数量相当，以中性信息为主"

        sentiment_summary = (
            f"舆情综合判断: {overall_sentiment}。{detail}。"
            f"来源可信度均值 {avg_credibility:.2f}（满分1.0），"
            f"高可信来源 {sum(1 for s in source_credibility_scores if s >= 0.8)} 个。"
            f"热点主题: {'、'.join(hot_topics[:4])}。"
            f"高影响力事件 {len(high_impact)} 条。"
        )

        # 按情感分类聚合
        positive_articles = [a for a in analyzed if a["sentiment"] == "positive"]
        negative_articles = [a for a in analyzed if a["sentiment"] == "negative"]
        neutral_articles = [a for a in analyzed if a["sentiment"] == "neutral"]

        return {
            "score": round(composite_score, 1),
            "confidence": confidence,
            "breadth": {
                "total_articles": len(analyzed),
                "unique_sources": len(set(a["source"] for a in analyzed if a["source"])),
                "channels": list(set(a["channel"] for a in analyzed if a["channel"])),
                "high_impact_articles": len(high_impact),
            },
            "depth": {
                "sentiment_distribution": {
                    "positive": sentiment_dist.get("positive", 0),
                    "neutral": sentiment_dist.get("neutral", 0),
                    "negative": sentiment_dist.get("negative", 0),
                },
                "trend_direction": trend_cn,
                "trend": trend,
                "average_credibility": round(avg_credibility, 2),
                "hot_topics": hot_topics,
            },
            "sentiment_summary": sentiment_summary,
            "credibility": {
                "confidence_level": confidence,
                "average_source_credibility": round(avg_credibility, 2),
                "high_credibility_sources": sum(1 for s in source_credibility_scores if s >= 0.8),
                "analysis_method": "多渠道聚合 + 关键词情感分类 + 来源权威性评级 + 影响力加权",
            },
            "timeline": timeline,
            "categorized_articles": {
                "positive": positive_articles,
                "negative": negative_articles,
                "neutral": neutral_articles,
            },
            "key_articles": analyzed[:8],
        }

    def _extract_hot_topics(self, text: str, top_n: int = 5) -> list[str]:
        """从文本中提取热门主题词"""
        # 简单分词：按常见分隔符拆分，过滤停用词
        tokens = re.split(r"[，。、；：！？\s,.;:!?()（）【】\[\]\"''_-]", text)
        # 过滤短词和无意义词
        meaningful = [
            t for t in tokens
            if len(t) >= 2 and t not in {
                "股票", "公司", "股份", "有限", "证券", "市场", "行业",
                "投资", "交易", "报告", "公告", "信息", "业务", "本次",
                "相关", "进行", "发布", "显示", "表示", "预计", "目前",
                "发展", "实现", "亿元", "万元", "同比", "环比", "占比",
            }
        ]
        counter = Counter(meaningful)
        return [word for word, _ in counter.most_common(top_n)]


# ---------------------------------------------------------------------------
# Module 6: Prospectus Analyzer (招股说明书分析引擎)
# ---------------------------------------------------------------------------

class ProspectusAnalyzer:
    """
    招股说明书分析引擎

    基于公司上市前后的财务数据变化，结合多渠道公开信息，
    对公司的业务模式、行业地位、募集资金使用、风险因素等
    进行结构化分析。

    广度: 业务分析/行业分析/财务对比/风险评估四大维度
    深度: 上市前后多期财务对比、业务与财务交叉验证
    可信度: 标注信息来源、区分披露事实与推测判断
    """

    def __init__(self, web_search: WebSearchSource):
        self.web_search = web_search

    def _get_listing_info(self, stock_code: str) -> dict:
        """获取上市基本信息（使用轻量接口）"""
        code = stock_code.replace(".SH", "").replace(".SZ", "").replace(".BJ", "")
        name = ""
        try:
            import akshare as ak
            df = ak.stock_individual_info_em(symbol=code)
            if not df.empty:
                for _, row in df.iterrows():
                    if "股票名称" in str(row.iloc[0]):
                        name = str(row.iloc[1])
                        break
        except Exception as e:
            logger.warning("Listing info via individual_info failed for %s: %s", stock_code, e)
        return {"stock_name": name, "code": code}

    def _get_listing_date(self, stock_code: str) -> str | None:
        """获取上市日期（从个股信息接口提取）"""
        try:
            import akshare as ak
            code = stock_code.replace(".SH", "").replace(".SZ", "").replace(".BJ", "")
            df = ak.stock_individual_info_em(symbol=code)
            if not df.empty:
                for _, row in df.iterrows():
                    if "上市时间" in str(row.iloc[0]) or "上市日期" in str(row.iloc[0]):
                        return str(row.iloc[1])
        except Exception:
            pass
        return None

    def analyze(self, stock_code: str, financial_deep_result: dict | None = None) -> dict:
        """
        招股说明书/上市分析主入口
        结合财务深度分析数据，对比上市前后的业绩变化
        """
        info = self._get_listing_info(stock_code)
        listing_date = self._get_listing_date(stock_code)
        stock_name = info.get("stock_name", "")

        # 尝试搜索招股书相关公开信息
        prospectus_news = []
        try:
            query = f"{stock_code} {stock_name} 招股说明书 上市"
            results = self.web_search.search_stock(stock_code, query)
            prospectus_news = results[:5] if results else []
        except Exception:
            pass

        # 从财务深度分析中提取上市前后对比
        pre_post_analysis = {}
        if financial_deep_result and financial_deep_result.get("depth"):
            dims = financial_deep_result["depth"].get("dimensions", {})
            for dim_key, dim_data in dims.items():
                indicators = dim_data.get("indicators", [])
                ind_list = []
                for ind in indicators:
                    ind_list.append({
                        "indicator": ind.get("indicator", ""),
                        "value": ind.get("value"),
                        "trend": ind.get("trend", ""),
                        "score": ind.get("score"),
                    })
                if ind_list:
                    pre_post_analysis[dim_key] = {
                        "name": dim_data.get("name", ""),
                        "score": dim_data.get("score"),
                        "indicators": ind_list,
                    }

        has_data = bool(prospectus_news) or bool(pre_post_analysis)

        return {
            "has_prospectus_data": has_data,
            "stock_name": stock_name,
            "listing_date": listing_date,
            "confidence": "medium" if has_data else "low",
            "breadth": {
                "dimensions_analyzed": len(pre_post_analysis),
                "available_news": len(prospectus_news),
                "has_financial_data": bool(pre_post_analysis),
            },
            "depth": {
                "financial_analysis": pre_post_analysis,
                "related_news_titles": [
                    str(n.get("title", ""))[:100] for n in prospectus_news
                ],
            },
            "credibility": {
                "confidence_level": "medium" if has_data else "low",
                "data_sources": ["akshare.stock_info_a_code_name"],
                "analysis_method": "上市信息查询 + 财务数据对比 + 公开信息搜索",
                "note": "招股说明书详细分析需结合全文PDF，当前基于公开数据和财务指标提供参考",
            },
        }


# ---------------------------------------------------------------------------
# Module 7: Analysis Query Engine (交互式分析查询)
# ---------------------------------------------------------------------------

class AnalysisQueryEngine:
    """
    交互式分析查询引擎

    支持用户针对财报/舆情数据进行深入的自然语言提问。
    预置了常见的深度追问场景，并为 AI Agent 提供结构化数据查询接口。
    """

    # 预置查询场景（供前端/Agent 参考）
    SCENARIOS = {
        "financial": {
            "profit_decline_reason": "某指标（如ROE、净利率）下滑的原因分析",
            "growth_sustainability": "当前增长率的可持续性判断",
            "debt_risk_assessment": "债务结构是否安全、短期偿债压力",
            "cash_flow_bottleneck": "现金流恶化的根源是什么",
            "segment_performance": "各业务板块的营收和利润贡献",
            "inventory_turnover": "存货和应收款周转效率",
            "margin_trend": "毛利率/净利率趋势及驱动因素",
        },
        "news": {
            "event_impact": "某个具体事件对股价的潜在影响",
            "negative_risk_detail": "所有负面事件的详细梳理",
            "industry_comparison": "行业舆情对比分析",
            "institutional_view": "机构观点汇总",
            "policy_impact": "政策变化对公司的影响",
        },
    }

    def __init__(self, analyzer: StockAnalyzer):
        self.analyzer = analyzer

    def query_financial(self, stock_code: str, question: str,
                        financial_deep_data: dict | None = None) -> dict:
        """
        财报深度追问 —— 返回指定股票的结构化财务数据，供 AI Agent 回答用户问题。
        question: 用户的原生问题文本（如"为什么ROE下降了"）
        """
        fd = financial_deep_data or self.analyzer.financial_deep.analyze_all(stock_code)
        if not fd or fd.get("confidence") == "none":
            return {"answerable": False, "message": "深度财务数据不可用", "data": {}}

        dims = fd.get("depth", {}).get("dimensions", {})
        # 提取所有维度的原始指标用于追问
        all_indicators = []
        for dk, dv in dims.items():
            for ind in dv.get("indicators", []):
                all_indicators.append({
                    "dimension": dv.get("name", dk),
                    "dimension_score": dv.get("score"),
                    "indicator": ind.get("indicator"),
                    "value": ind.get("value"),
                    "score": ind.get("score"),
                    "trend": ind.get("trend"),
                    "source_period": ind.get("source_period"),
                    "raw_value": ind.get("raw_value_source"),
                    "previous_value": ind.get("previous_value"),
                    "previous_raw_value": ind.get("raw_value_previous"),
                    "data_source": ind.get("data_source_name"),
                })

        return {
            "answerable": True,
            "question": question,
            "query_type": "financial",
            "data": {
                "composite_score": fd.get("score"),
                "confidence": fd.get("confidence"),
                "periods_analyzed": fd.get("breadth", {}).get("periods_analyzed", 0),
                "latest_period": fd.get("depth", {}).get("latest_period", ""),
                "all_indicators": all_indicators,
                "risk_factors": fd.get("depth", {}).get("risk_factors", []),
                "data_source_urls": fd.get("credibility", {}).get("data_source_urls", {}),
            },
        }

    def query_news(self, stock_code: str, question: str,
                   news_deep_data: dict | None = None) -> dict:
        """
        新闻舆情深度追问 —— 返回完整的事件时间线和分类数据。
        question: 用户的原生问题文本（如"最近有哪些负面新闻"）
        """
        nd = news_deep_data or self.analyzer.news_deep.analyze_news(stock_code)
        if not nd or nd.get("confidence") == "none":
            return {"answerable": False, "message": "新闻舆情数据不可用", "data": {}}

        return {
            "answerable": True,
            "question": question,
            "query_type": "news",
            "data": {
                "score": nd.get("score"),
                "confidence": nd.get("confidence"),
                "sentiment_distribution": nd.get("depth", {}).get("sentiment_distribution", {}),
                "sentiment_summary": nd.get("sentiment_summary", ""),
                "trend_direction": nd.get("depth", {}).get("trend_direction", ""),
                "total_articles": nd.get("breadth", {}).get("total_articles", 0),
                "timeline": nd.get("timeline", []),
                "categorized_articles": nd.get("categorized_articles", {}),
                "hot_topics": nd.get("depth", {}).get("hot_topics", []),
                "high_impact_articles": nd.get("breadth", {}).get("high_impact_articles", 0),
            },
        }

    def query_financial_timeline(self, stock_code: str, periods: int = 8) -> list[dict]:
        """
        获取多期财务数据时间线，用于分析趋势变化
        返回: 按时间倒序排列的财务数据列表
        """
        try:
            import akshare as ak
            code = stock_code.replace(".SH", "").replace(".SZ", "").replace(".BJ", "")
            df = ak.stock_financial_abstract_ths(symbol=code)
            if df.empty:
                return []
            records = df.to_dict(orient="records")
            # 取最近 N 期，倒序
            selected = records[-periods:] if len(records) >= periods else records
            timeline = []
            for rec in reversed(selected):
                row = {str(k): v for k, v in rec.items()}
                parsed = {}
                for key, ths_col in FinancialDeepAnalyzer.THS_FIELD_MAP.items():
                    raw_val = row.get(ths_col)
                    pv = _parse_ths_val(raw_val)
                    if pv is not None:
                        parsed[key] = {"value": round(pv, 2), "raw": str(raw_val) if raw_val not in (None, False) else ""}
                timeline.append({
                    "period": str(row.get("报告期", "")),
                    "indicators": parsed,
                })
            return timeline
        except Exception as e:
            logger.warning("Financial timeline query failed for %s: %s", stock_code, e)
            return []

    def get_supported_scenarios(self, query_type: str | None = None) -> dict:
        """获取支持的查询场景列表"""
        if query_type:
            return self.SCENARIOS.get(query_type, {})
        return self.SCENARIOS


# ---------------------------------------------------------------------------
# Module 8: Stock Analyzer (enhanced)
# ---------------------------------------------------------------------------

class StockAnalyzer:
    def __init__(self):
        self.primary = AKShareSource()
        self.fallback = BaoStockSource()
        self.web_search = WebSearchSource()
        self.financial_deep = FinancialDeepAnalyzer(self.primary)
        self.news_deep = NewsDeepAnalyzer(self.web_search)
        self.prospectus = ProspectusAnalyzer(self.web_search)
        self.query_engine = AnalysisQueryEngine(self)

    def analyze(self, stock_code: str, stock_name: str = "") -> dict:
        market_data = self.primary.get_market_data(stock_code)
        financial_data = self.primary.get_financial_data(stock_code)
        capital_flow = self.primary.get_capital_flow(stock_code)

        if not market_data:
            logger.info("Primary source failed for %s, switching to BaoStock", stock_code)
            market_data = self.fallback.get_market_data(stock_code)

        news = self.web_search.search_stock(stock_code, stock_name)
        financial_deep = self.financial_deep.analyze_all(stock_code)
        news_deep = self.news_deep.analyze_news(stock_code, stock_name)
        prospectus_data = self.prospectus.analyze(stock_code, financial_deep)

        return {
            "stock_code": stock_code,
            "stock_name": stock_name,
            "market_data": market_data,
            "financial_data": financial_data,
            "capital_flow": capital_flow,
            "news": news,
            "financial_deep": financial_deep,
            "news_deep": news_deep,
            "prospectus_analysis": prospectus_data,
        }

    def analyze_fundamental(self, data: dict) -> dict:
        financial = data.get("financial_data", {})
        score = 5
        details = []
        if financial.get("roe"):
            roe = float(financial["roe"])
            if roe > 15:
                score += 2
                details.append(f"ROE {roe}% 优秀")
            elif roe > 10:
                score += 1
                details.append(f"ROE {roe}% 良好")

        pe = financial.get("pe_ttm")
        if pe:
            pe = float(pe)
            if 10 < pe < 30:
                details.append(f"PE {pe} 估值合理")
            elif pe <= 10:
                score += 1
                details.append(f"PE {pe} 估值偏低")
            else:
                score -= 1
                details.append(f"PE {pe} 估值偏高")

        return {"score": min(max(score, 1), 10), "details": details}

    def analyze_technical(self, data: dict) -> dict:
        market = data.get("market_data", {})
        score = 5
        details = []
        pct = market.get("pct_change")
        if pct is not None:
            pct = float(pct)
            if pct > 3:
                score += 1
                details.append("当日涨幅较大，趋势偏强")
            elif pct < -3:
                score -= 1
                details.append("当日跌幅较大，趋势偏弱")
            else:
                details.append("当日走势平稳")
        return {"score": min(max(score, 1), 10), "details": details}

    def analyze_capital_flow(self, data: dict) -> dict:
        flow = data.get("capital_flow", {})
        score = 5
        details = []
        net_inflow = flow.get("net_inflow")
        if net_inflow:
            net_inflow = float(net_inflow)
            if net_inflow > 0:
                score += 1
                details.append("主力资金净流入")
            else:
                score -= 1
                details.append("主力资金净流出")
        return {"score": min(max(score, 1), 10), "details": details}

    def analyze_sentiment(self, data: dict) -> dict:
        news = data.get("news", [])
        score = 5
        details = [f"相关新闻/文章 {len(news)} 篇"]
        return {"score": min(max(score, 1), 10), "details": details}

    def analyze_financial_deep(self, data: dict) -> dict:
        """
        深度财报分析 —— 返回结构化多维度评分结果
        广度: 5大维度、最多14个细分指标
        深度: 多期趋势对比、逐指标评分
        可信度: 数据完整率、置信等级
        """
        result = data.get("financial_deep", {})
        if not result or result.get("confidence") == "none":
            return {
                "score": 5,
                "confidence": "none",
                "details": ["深度财务数据不可用，使用基础财务评分替代"],
                "breadth": {"dimensions_analyzed": 0, "total_dimensions": 5},
                "credibility": {"confidence_level": "none"},
            }

        score = result.get("score")
        base_score = score if score is not None else 5

        details = []
        dims = result.get("depth", {}).get("dimensions", {})
        for dim_key, dim_data in dims.items():
            if dim_data.get("score") is not None:
                detail_parts = [f"{dim_data['name']}: {dim_data['score']}分"]
                for ind in dim_data.get("indicators", [])[:3]:
                    trend_str = f" {ind.get('trend', '')}" if ind.get("trend") else ""
                    detail_parts.append(f"  - {ind['indicator']}={ind['value']}{trend_str}")
                details.append("\n".join(detail_parts))

        risk_factors = result.get("depth", {}).get("risk_factors", [])
        if risk_factors:
            details.append(f"风险因素 ({len(risk_factors)}项): {risk_factors[0]}")

        return {
            "score": min(max(round(base_score), 1), 10),
            "raw_score": round(base_score, 1) if score is not None else None,
            "confidence": result.get("confidence", "none"),
            "details": details,
            "breadth": result.get("breadth"),
            "depth": {
                "dimensions": dims,
                "risk_factors": result.get("depth", {}).get("risk_factors", []),
                "latest_period": result.get("depth", {}).get("latest_period", ""),
            },
            "credibility": result.get("credibility"),
        }

    def analyze_news_deep(self, data: dict) -> dict:
        """
        深度新闻舆论分析 —— 多源聚合情感分析
        广度: 多渠道搜集、情感分布、来源覆盖
        深度: 逐条情感分类、影响力评估、热门主题
        可信度: 来源权威性评级、分析置信度
        """
        result = data.get("news_deep", {})
        if not result or result.get("confidence") == "none":
            return {
                "score": 5,
                "confidence": "none",
                "details": ["新闻舆情数据不可用"],
                "breadth": {"total_articles": 0},
                "credibility": {"confidence_level": "none"},
            }

        score = result.get("score", 5)
        depth = result.get("depth", {})

        sent_dist = depth.get("sentiment_distribution", {})
        details = [
            f"新闻总量: {result.get('breadth', {}).get('total_articles', 0)}篇 | "
            f"来源: {result.get('breadth', {}).get('unique_sources', 0)}个",
            f"情感分布: 正面{sent_dist.get('positive', 0)} / "
            f"中性{sent_dist.get('neutral', 0)} / "
            f"负面{sent_dist.get('negative', 0)}",
            f"舆情趋势: {depth.get('trend_direction', '中性')} | "
            f"来源可信度: {depth.get('average_credibility', 0)}",
        ]

        hot_topics = depth.get("hot_topics", [])
        if hot_topics:
            details.append(f"热门主题: {' / '.join(hot_topics[:5])}")

        high_impact = result.get("breadth", {}).get("high_impact_articles", 0)
        if high_impact > 0:
            details.append(f"高影响力文章: {high_impact}篇")

        return {
            "score": min(max(round(score), 1), 10),
            "raw_score": round(score, 1),
            "confidence": result.get("confidence", "none"),
            "details": details,
            "sentiment_summary": result.get("sentiment_summary", ""),
            "breadth": result.get("breadth"),
            "depth": {
                "sentiment_distribution": sent_dist,
                "trend_direction": depth.get("trend_direction", "中性"),
                "hot_topics": hot_topics,
            },
            "credibility": result.get("credibility"),
            "key_articles": result.get("key_articles", [])[:5],
            "timeline": result.get("timeline", []),
            "categorized_articles": result.get("categorized_articles", {}),
        }

    def analyze_prospectus_deep(self, data: dict) -> dict:
        """
        招股说明书分析 —— 结合公开信息和财务数据
        """
        result = data.get("prospectus_analysis", {})
        if not result:
            return {
                "score": 5,
                "confidence": "none",
                "details": ["招股说明书数据不可用"],
                "breadth": {},
                "credibility": {"confidence_level": "none"},
            }

        has_data = result.get("has_prospectus_data", False)
        confidence = result.get("confidence", "none")

        details = []
        stock_name = result.get("stock_name", "")
        listing_date = result.get("listing_date", "")
        if stock_name:
            details.append(f"公司名称: {stock_name}")
        if listing_date:
            details.append(f"上市日期: {listing_date}")

        fin_analysis = result.get("depth", {}).get("financial_analysis", {})
        for dim_key, dim_data in fin_analysis.items():
            name = dim_data.get("name", "")
            score = dim_data.get("score")
            if score is not None:
                details.append(f"{name}: {score}分")

        news_titles = result.get("depth", {}).get("related_news_titles", [])
        if news_titles:
            details.append(f"相关公开信息: {len(news_titles)}条")

        score = 6 if has_data else 5
        return {
            "score": score,
            "confidence": confidence,
            "details": details,
            "breadth": result.get("breadth", {}),
            "credibility": result.get("credibility", {}),
        }


# ---------------------------------------------------------------------------
# Module 8: Preference Matcher (Multi-round Dialog)
# ---------------------------------------------------------------------------

class PreferenceMatcher:
    QUESTIONS = [
        {"key": "investment_horizon", "text": "您的投资周期偏好是？（短期/中期/长期）"},
        {"key": "risk_tolerance", "text": "您的风险承受能力如何？（保守/稳健/激进）"},
        {"key": "market_cap_preference", "text": "您更关注哪些投资标的类型？（大盘股/中小盘/科创板等）"},
        {"key": "dividend_preference", "text": "您是否偏好高分红股票？（是/否）"},
        {"key": "sector_preference", "text": "您有偏好的行业板块吗？（如新能源/消费/医药/TMT等，多个用逗号分隔）"},
    ]

    def __init__(self, strategy_matcher: StrategyMatcher):
        self.matcher = strategy_matcher
        self.responses: dict[str, str] = {}

    @property
    def next_question(self) -> str | None:
        for q in self.QUESTIONS:
            if q["key"] not in self.responses:
                return q["text"]
        return None

    def answer(self, key: str, value: str):
        if key not in {q["key"] for q in self.QUESTIONS}:
            raise ValueError(f"Unknown key: {key}")
        self.responses[key] = value

    def match(self) -> list[dict]:
        profile = " ".join(f"{k}:{v}" for k, v in self.responses.items())
        return self.matcher.semantic_match(profile, top_k=3)


# ---------------------------------------------------------------------------
# Module 6: Recommendation Engine
# ---------------------------------------------------------------------------

class RecommendationEngine:
    def __init__(self, analyzer: StockAnalyzer):
        self.analyzer = analyzer

    def generate_report(
        self,
        strategy_info: dict,
        positions: list[dict],
        analysis_results: list[dict],
    ) -> dict:
        stock_analyses = []
        for pos, result in zip(positions, analysis_results):
            fundamental = self.analyzer.analyze_fundamental(result)
            technical = self.analyzer.analyze_technical(result)
            capital = self.analyzer.analyze_capital_flow(result)
            sentiment = self.analyzer.analyze_sentiment(result)

            avg_score = (
                fundamental["score"] * 0.35
                + technical["score"] * 0.25
                + capital["score"] * 0.25
                + sentiment["score"] * 0.15
            )
            recommendation = self._rating(avg_score)

            financial_deep = self.analyzer.analyze_financial_deep(result)
            news_deep = self.analyzer.analyze_news_deep(result)
            prospectus_deep = self.analyzer.analyze_prospectus_deep(result)

            stock_analyses.append({
                "stock_code": pos["stock_code"],
                "weight": pos["weight"],
                "scores": {
                    "fundamental": fundamental,
                    "technical": technical,
                    "capital_flow": capital,
                    "sentiment": sentiment,
                },
                "deep_analysis": {
                    "financial_report": financial_deep,
                    "news_sentiment": news_deep,
                    "prospectus": prospectus_deep,
                },
                "composite_score": round(avg_score, 1),
                "recommendation": recommendation,
                "data": result,
            })

        return {
            "strategy": {
                "id": strategy_info.get("strategy_id"),
                "name": strategy_info.get("strategy_name_cn"),
                "category": strategy_info.get("strategy_cat"),
                "summary": strategy_info.get("strategy_summ"),
                "benchmark": strategy_info.get("benchmark"),
            },
            "positions": positions,
            "stock_analyses": stock_analyses,
            "overall_assessment": self._overall_assessment(stock_analyses),
        }

    @staticmethod
    def explain_strategy_match(strategy: dict) -> str:
        return f"策略「{strategy.get('strategy_name_cn', '')}」匹配您的投资需求。" \
               f"该策略属于{strategy.get('strategy_cat', '')}类别，{strategy.get('strategy_summ', '')}"

    @staticmethod
    def _rating(score: float) -> str:
        if score >= 8:
            return "买入"
        elif score >= 5:
            return "持有"
        elif score >= 3:
            return "观察"
        return "规避"

    @staticmethod
    def _overall_assessment(analyses: list[dict]) -> dict:
        if not analyses:
            return {"conclusion": "无持仓数据", "risk_warning": ""}
        avg = sum(a["composite_score"] for a in analyses) / len(analyses)
        weighted = sum(a["composite_score"] * a["weight"] for a in analyses) / sum(a["weight"] for a in analyses)

        confidence_levels = {"high": 3, "medium": 2, "low": 1, "none": 0}

        def _avg_conf(analyses: list[dict], key: str) -> float:
            confs = [
                a.get("deep_analysis", {}).get(key, {}).get("confidence", "none")
                for a in analyses
            ]
            return sum(confidence_levels.get(c, 0) for c in confs) / max(len(confs), 1)

        def _conf_label(avg: float) -> str:
            if avg >= 2.5:
                return "high"
            elif avg >= 1.5:
                return "medium"
            elif avg > 0:
                return "low"
            return "none"

        return {
            "average_score": round(avg, 1),
            "weighted_score": round(weighted, 1),
            "total_stocks": len(analyses),
            "buy_count": sum(1 for a in analyses if a["recommendation"] == "买入"),
            "hold_count": sum(1 for a in analyses if a["recommendation"] == "持有"),
            "watch_count": sum(1 for a in analyses if a["recommendation"] == "观察"),
            "avoid_count": sum(1 for a in analyses if a["recommendation"] == "规避"),
            "analysis_credibility": {
                "financial_report_confidence": _conf_label(_avg_conf(analyses, "financial_report")),
                "news_sentiment_confidence": _conf_label(_avg_conf(analyses, "news_sentiment")),
                "prospectus_confidence": _conf_label(_avg_conf(analyses, "prospectus")),
            },
        }


# ---------------------------------------------------------------------------
# Main entry point (called by OpenClaw runtime)
# ---------------------------------------------------------------------------

class RacingQuantAI:
    def __init__(self, db_config: dict | None = None):
        self.db_config = db_config or load_db_config()
        self.matcher = StrategyMatcher(self.db_config)
        self.fetcher = PositionFetcher(self.db_config)
        self.analyzer = StockAnalyzer()
        self.engine = RecommendationEngine(self.analyzer)

    def run_pipeline(self, user_input: str) -> dict:
        logger.info("Starting pipeline with input: %s", user_input)
        strategies = self.matcher.semantic_match(user_input)
        if not strategies:
            return {"error": "未匹配到合适策略", "input": user_input}

        best = strategies[0]
        positions_raw = self.fetcher.get_positions(best["strategy_id"])
        positions = PositionFetcher.parse_trading_info(positions_raw)

        analysis_results = [
            self.analyzer.analyze(p["stock_code"]) for p in positions
        ]
        report = self.engine.generate_report(best, positions, analysis_results)
        report["strategy_matching_note"] = self.engine.explain_strategy_match(best)
        return report

    def start_preference_dialog(self) -> PreferenceMatcher:
        return PreferenceMatcher(self.matcher)


if __name__ == "__main__":
    skill = RacingQuantAI()
    result = skill.run_pipeline("帮我推荐一些低估值高股息的策略")
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
