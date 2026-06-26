"""
reranker.py - 检索结果重排序器
用交叉编码器对初始检索结果精排，提升精度 15-20%

支持：
1. FlagEmbedding (bge-reranker-v2-m3) — 最佳精度
2. sentence-transformers CrossEncoder — 兼容方案
3. 启发式降级 — 无依赖时保证可用
"""

from __future__ import annotations

import logging
import time

logger = logging.getLogger(__name__)


class Reranker:
    """
    检索结果重排序。

    用法：
        reranker = Reranker()
        reranked = reranker.rerank("RAG 怎么实现", results, top_k=10)

    加载策略（自动降级）：
    1. FlagEmbedding (bge-reranker-v2-m3) → 最佳
    2. sentence-transformers CrossEncoder (cross-encoder/ms-marco-MiniLM-L-6-v2)
    3. 启发式关键词匹配 → 保底可用
    """

    def __init__(
        self,
        model_name: str = None,
        use_reranker: bool = True,
        batch_size: int = 32,
    ):
        """
        参数:
            model_name: 模型名，None 则自动选择
            use_reranker: 是否启用（False 则直接返回原文）
            batch_size: 批量编码大小
        """
        self._use_reranker = use_reranker
        self._batch_size = batch_size
        self._model = None
        self._model_type = None  # "flag" / "cross" / "heuristic"

        if not use_reranker:
            self._model_type = "disabled"
            return

        # 尝试加载模型
        self._load_model(model_name)

    def _load_model(self, model_name: str = None):
        """按优先级加载模型"""

        # 1. 尝试 FlagEmbedding (bge-reranker)
        if model_name is None or "bge" in (model_name or "").lower():
            try:
                from FlagEmbedding import FlagReranker
                name = model_name or "BAAI/bge-reranker-v2-m3"
                self._model = FlagReranker(name, use_fp16=True)
                self._model_type = "flag"
                logger.info(f"✅ Reranker 加载成功: {name} (FlagEmbedding)")
                return
            except ImportError:
                pass
            except Exception as e:
                logger.debug(f"FlagReranker 加载失败: {e}")

        # 2. 尝试 sentence-transformers CrossEncoder
        try:
            from sentence_transformers import CrossEncoder
            name = model_name or "cross-encoder/ms-marco-MiniLM-L-6-v2"
            self._model = CrossEncoder(name, device="cpu")
            self._model_type = "cross"
            logger.info(f"✅ Reranker 加载成功: {name} (CrossEncoder)")
            return
        except ImportError as e:
            logger.debug("reranker: CrossEncoder not available: %s", e)
        except Exception as e:
            logger.debug(f"CrossEncoder 加载失败: {e}")

        # 3. 降级为启发式
        self._model_type = "heuristic"
        logger.info("⚠️ Reranker 不可用，降级为启发式重排")

    def rerank(
        self,
        query: str,
        results: list[dict],
        top_k: int = None,
        score_field: str = "_rank_score",
    ) -> list[dict]:
        """
        对检索结果重排序。

        参数:
            query: 用户查询
            results: 检索结果列表（每条有 content 字段）
            top_k: 返回 top_k 条（None 则全部）
            score_field: 写入的分数字段名

        返回: 重排序后的结果列表
        """
        if not results:
            return results

        if self._model_type == "disabled":
            return results[:top_k] if top_k else results

        # 取内容
        pairs = []
        valid_results = []
        for r in results:
            content = r.get("content", "")
            if content:
                pairs.append([query, content])
                valid_results.append(r)

        if not pairs:
            return results

        # 计算 rerank 分数
        try:
            if self._model_type == "flag":
                scores = self._model.compute_score(pairs, batch_size=self._batch_size)
                # FlagReranker 返回的是相似度分数（越高越好）
            elif self._model_type == "cross":
                scores = self._model.predict(pairs, batch_size=self._batch_size)
                # CrossEncoder 返回的是相关性分数
            else:
                scores = self._heuristic_score(query, valid_results)
        except Exception as e:
            logger.warning("reranker: %s", e)
            scores = self._heuristic_score(query, valid_results)

        # 写入分数
        for i, (result, score) in enumerate(zip(valid_results, scores)):
            result["_rerank_score"] = float(score)
            # 融合：70% rerank + 30% 原始分数
            original = result.get(score_field, 0)
            result[score_field] = 0.7 * float(score) + 0.3 * original

        # 重排序
        valid_results.sort(key=lambda r: r.get(score_field, 0), reverse=True)

        return valid_results[:top_k] if top_k else valid_results

    def _heuristic_score(self, query: str, results: list[dict]) -> list[float]:
        """
        启发式重排（无模型时降级）。

        基于：
        1. 查询词在内容中的命中次数
        2. 命中位置（越早越好）
        3. 内容长度惩罚（太短信息量少）
        """
        import re
        query_lower = query.lower()
        # 提取查询关键词（去停用词）
        stop_words = {"的", "了", "是", "在", "和", "有", "我", "你", "他", "她", "它", "们", "这", "那", "什么", "怎么", "如何"}
        query_words = set(re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', query_lower))
        query_words = query_words - stop_words

        scores = []
        for r in results:
            content = r.get("content", "").lower()
            if not query_words:
                scores.append(0.5)
                continue

            # 命中次数
            hits = sum(content.count(w) for w in query_words)
            # 早期命中加权
            early_bonus = 0
            for w in query_words:
                pos = content.find(w)
                if 0 <= pos < 100:
                    early_bonus += 0.3
            # 内容长度
            length_score = min(1.0, len(content) / 200)

            score = min(1.0, (hits * 0.2 + early_bonus + length_score * 0.1))
            scores.append(score)

        return scores

    @property
    def is_available(self) -> bool:
        return self._model_type not in ("disabled", "heuristic")

    @property
    def model_type(self) -> str:
        return self._model_type

    def get_stats(self) -> dict:
        return {
            "model_type": self._model_type,
            "available": self.is_available,
            "batch_size": self._batch_size,
        }
