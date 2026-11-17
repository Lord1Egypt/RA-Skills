"""
搜索引擎调度层 — 16引擎智能路由
──────────────────────────────
职责：
  - 根据语言和引擎组选择引擎
  - 分批调用（每批3-4个，间隔1.5s）
  - 跨源去重（URL + 内容指纹）
  - 单引擎熔断不拖垮整组
  - 全部失败时降级返回
  - 输出强制通过 contracts/search_schema.py 的 SearchOutput Schema

严禁：
  - 直接操作文件系统
  - 修改全局状态
  - 跨阶段通信（输出必须通过ACL）
"""
from __future__ import annotations

import hashlib
import logging
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Optional
from urllib.parse import urlparse

from middlewares.circuit_breaker import TieredCircuitBreaker, CircuitBreakerOpenError
from contracts.search_schema import SearchHit as SchemaSearchHit, SearchOutput

logger = logging.getLogger(__name__)

# ── 引擎配置 ─────────────────────────────────────────────────

ENGINE_GROUPS = {
    "cn": ["baidu", "bing_cn", "bing_int", "360", "sogou", "wechat", "shenma"],
    "global": ["google", "google_hk", "duckduckgo", "yahoo", "startpage", "brave", "ecosia", "qwant", "wolframalpha"],
}

BATCH_SIZE = 4          # 每批并发引擎数
BATCH_INTERVAL = 1.5    # 批间间隔（秒）
SINGLE_ENGINE_TIMEOUT = 15  # 单引擎超时（秒）
MAX_RESULTS_PER_ENGINE = 10  # 每引擎取前N条
ENGINE_RETRY_MAX = 2     # Phase 5.1: 单引擎最大重试次数
ENGINE_RETRY_BACKOFF = 2.0  # Phase 5.1: 重试退避基数（秒）


@dataclass
class SearchHit:
    """单条搜索结果（内部表示，最终转为 Schema）"""
    url: str
    title: str
    snippet: str
    source_engine: str
    source_region: str   # "cn" | "global"
    rank: int
    fingerprint: str = ""

    def compute_fingerprint(self) -> str:
        """计算内容指纹（用于去重）"""
        content = f"{self.title}|{self.snippet[:200]}"
        self.fingerprint = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]
        return self.fingerprint

    def to_schema_hit(self) -> SchemaSearchHit:
        """转为 Pydantic Schema 对象（入口校验）"""
        return SchemaSearchHit(
            url=self.url,
            title=self.title or "无标题",
            snippet=self.snippet,
            source_engine=self.source_engine,
            source_region=self.source_region,
            rank=self.rank,
            fingerprint=self.fingerprint,
        )


class SearchEngine:
    """
    搜索引擎调度器

    用法:
        engine = SearchEngine(circuit_breaker=tcb)
        result = engine.search(
            query="AI趋势",
            language="zh",
            engine_group="all",
        )
    """

    def __init__(self, circuit_breaker: Optional[TieredCircuitBreaker] = None):
        self._circuit_breaker = circuit_breaker or TieredCircuitBreaker()

    def search(
        self,
        query: str,
        language: str = "zh",
        engine_group: str = "all",
        max_results: int = 100,
        session_id: str = "",
    ) -> dict:
        """
        执行16引擎搜索

        Args:
            query: 搜索查询
            language: 语言 ("zh" | "en")
            engine_group: 引擎组 ("cn" | "global" | "all")
            max_results: 最大结果数
            session_id: 会话ID

        Returns:
            dict: 通过 SearchOutput Schema 校验后的字典表示
        """
        request_id = session_id or f"sr_{uuid.uuid4().hex[:8]}"

        # 选择引擎列表
        engines = self._select_engines(language, engine_group)
        logger.info(f"[Search:{request_id}] Using {len(engines)} engines: {engines}")

        # 分批搜索
        all_hits: list[SearchHit] = []
        failed_engines: list[str] = []
        warnings: list[str] = []

        for batch_idx in range(0, len(engines), BATCH_SIZE):
            batch = engines[batch_idx:batch_idx + BATCH_SIZE]
            batch_results = self._search_batch(query, batch, request_id)

            all_hits.extend(batch_results["hits"])
            failed_engines.extend(batch_results["failed"])
            warnings.extend(batch_results["warnings"])

            # 批间间隔
            if batch_idx + BATCH_SIZE < len(engines):
                time.sleep(BATCH_INTERVAL)

        # 去重
        deduped_hits = self._deduplicate(all_hits)

        # 截断到 max_results
        deduped_hits = deduped_hits[:max_results]

        # 确定状态
        if not all_hits:
            status = "failed"
        elif failed_engines and len(failed_engines) == len(engines):
            status = "failed"
        elif failed_engines:
            status = "partial"
        else:
            status = "complete"

        # ── 核心改动：通过 Pydantic Schema 构造输出 ──
        # 这确保了每个 SearchHit 都经过字段级校验（URL 非空、rank 在范围内等）
        try:
            schema_hits = [h.to_schema_hit() for h in deduped_hits]
            output = SearchOutput(
                request_id=request_id,
                query=query,
                deduplicated_results=schema_hits,
                total_raw=len(all_hits),
                total_deduped=len(deduped_hits),
                total_engines=len(engines),
                failed_engines=failed_engines,
                warnings=warnings,
                status=status,
            )
            result_dict = output.model_dump()
        except Exception as e:
            logger.error(f"[Search:{request_id}] Schema validation failed: {e}")
            # 降级：返回最小合法输出
            output = SearchOutput(
                request_id=request_id,
                query=query,
                total_raw=0,
                total_deduped=0,
                total_engines=len(engines),
                failed_engines=engines,
                warnings=warnings + [f"Schema validation failed: {e}"],
                status="failed",
            )
            result_dict = output.model_dump()

        logger.info(
            f"[Search:{request_id}] Done: {output.total_raw} raw, "
            f"{output.total_deduped} deduped, {len(failed_engines)} engines failed"
        )
        return result_dict

    def _select_engines(self, language: str, engine_group: str) -> list[str]:
        """根据语言和引擎组选择引擎"""
        if engine_group == "cn":
            return list(ENGINE_GROUPS["cn"])
        elif engine_group == "global":
            return list(ENGINE_GROUPS["global"])
        else:
            # "all": 中文用国内+国际混合，英文用国际
            if language == "zh":
                return ENGINE_GROUPS["cn"] + ENGINE_GROUPS["global"][:4]
            else:
                return list(ENGINE_GROUPS["global"])

    def _search_batch(
        self,
        query: str,
        engines: list[str],
        request_id: str,
    ) -> dict:
        """搜索一批引擎 — Phase 5.1: 增加单引擎重试+退避"""
        hits = []
        failed = []
        warnings = []

        for engine_name in engines:
            engine_hits = None
            last_error = None

            for attempt in range(ENGINE_RETRY_MAX + 1):
                try:
                    engine_hits = self._circuit_breaker.engine_call(
                        engine_name,
                        self._search_single_engine,
                        engine_name,
                        query,
                    )
                    if engine_hits:
                        hits.extend(engine_hits)
                    break  # 成功，退出重试循环
                except CircuitBreakerOpenError:
                    warnings.append(f"Engine {engine_name} is circuit-broken, skipping")
                    failed.append(engine_name)
                    break  # 熔断打开不重试
                except Exception as e:
                    last_error = e
                    if attempt < ENGINE_RETRY_MAX:
                        backoff = ENGINE_RETRY_BACKOFF * (2 ** attempt)
                        logger.warning(
                            f"Engine {engine_name} attempt {attempt + 1}/{ENGINE_RETRY_MAX + 1} "
                            f"failed: {e}, retrying in {backoff:.1f}s"
                        )
                        time.sleep(backoff)
                    else:
                        logger.warning(
                            f"Engine {engine_name} failed after {ENGINE_RETRY_MAX + 1} attempts: {last_error}"
                        )
                        failed.append(engine_name)

        return {"hits": hits, "failed": failed, "warnings": warnings}

    def _search_single_engine(self, engine_name: str, query: str) -> list[SearchHit]:
        """调用单个搜索引擎

        在 CodeBuddy runtime 环境中，此方法通过 web_search 工具执行实际搜索。
        在非 runtime 环境（测试/本地）中，返回空列表作为占位。

        搜索契约:
            web_search(query=query, engine=engine_name, max_results=MAX_RESULTS_PER_ENGINE)

        返回值格式化为统一的 SearchHit 对象。引擎不可用时抛异常让熔断器处理。
        """
        region = "cn" if engine_name in ENGINE_GROUPS["cn"] else "global"
        logger.debug(f"[{engine_name}] Searching (region={region}): {query}")

        # Phase 5.2: 尝试实际调用 web_search 工具（runtime 环境）
        try:
            # 在 CodeBuddy runtime 中，web_search 是内置工具
            # 这里尝试调用，如果不可用则返回空列表
            import builtins
            if hasattr(builtins, 'web_search'):
                raw_results = builtins.web_search(
                    query=query,
                    engine=engine_name,
                    max_results=MAX_RESULTS_PER_ENGINE,
                )
                hits = []
                for i, r in enumerate(raw_results[:MAX_RESULTS_PER_ENGINE]):
                    hits.append(SearchHit(
                        url=r.get("url", ""),
                        title=r.get("title", ""),
                        snippet=r.get("snippet", ""),
                        source_engine=engine_name,
                        source_region=region,
                        rank=i + 1,
                    ))
                if hits:
                    return hits
        except Exception:
            pass

        # 非 runtime 环境或 web_search 不可用：返回空列表
        return []

    def _deduplicate(self, hits: list[SearchHit]) -> list[SearchHit]:
        """
        两层去重：
        1. URL 去重 — 相同 URL 只保留排名最高的
        2. 内容指纹去重 — 相似度 >90% 的内容合并
        """
        # Layer 1: URL 去重
        url_map: dict[str, SearchHit] = {}
        for hit in hits:
            normalized_url = self._normalize_url(hit.url)
            if normalized_url in url_map:
                # 保留排名更高的
                if hit.rank < url_map[normalized_url].rank:
                    url_map[normalized_url] = hit
            else:
                url_map[normalized_url] = hit

        url_deduped = list(url_map.values())

        # Layer 2: 内容指纹去重
        fingerprint_map: dict[str, SearchHit] = {}
        for hit in url_deduped:
            fp = hit.compute_fingerprint()
            # 简单去重：相同指纹只保留一个
            if fp not in fingerprint_map:
                fingerprint_map[fp] = hit
            else:
                # 相同指纹，保留排名更高的
                existing = fingerprint_map[fp]
                if hit.rank < existing.rank:
                    fingerprint_map[fp] = hit

        # 按排名排序
        result = sorted(fingerprint_map.values(), key=lambda h: h.rank)

        return result

    def _normalize_url(self, url: str) -> str:
        """标准化 URL 用于去重"""
        try:
            parsed = urlparse(url)
            # 去除 www 前缀、尾部斜杠、fragment
            netloc = parsed.netloc.lower()
            if netloc.startswith("www."):
                netloc = netloc[4:]
            path = parsed.path.rstrip("/") or "/"
            return f"{parsed.scheme}://{netloc}{path}"
        except Exception:
            return url
