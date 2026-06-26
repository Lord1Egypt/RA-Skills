"""
metacognition.py - 元认知引擎（v7.1 增强版）

检索后的反思与修正闭环：
检索 → 评估 → 反思 → 修正查询 → 重新检索

Phase 3 核心模块。

核心能力：
1. MetaEvaluation — 多维度评估检索结果质量
2. 反思生成 — "为什么不确定？缺什么？"
3. 查询修正 — LLM 驱动的智能改写（降级为规则）
4. meta_recall — 带反思的多轮检索（最多 2 轮）
5. 反思记忆化 — 反思结果写入记忆系统
6. 可观测性 — 每步 trace 记录，输出 RRF 分数和修正原因

v7.1 改进：
- LLM 介入查询修正：不再是简单的词替换，而是语义级改写
- 评估公式权重可调：支持根据历史效果动态调整
- 修正效果追踪：记录每次修正是否改善了结果
"""

from __future__ import annotations

import time
import re
import json
import logging
from dataclasses import dataclass, field
from typing import Optional, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from protocols import MetacognitionMemoryProvider

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════
# MetaEvaluation — 检索结果质量评估
# ═══════════════════════════════════════════════════════

@dataclass
class MetaEvaluation:
    """多维度检索结果质量评估"""

    relevance_coverage: float = 0.0    # 结果覆盖了多少查询意图 [0, 1]
    internal_consistency: float = 0.0  # 结果之间是否一致 [0, 1]
    source_diversity: float = 0.0      # 来源是否多样（避免信息茧房）[0, 1]
    temporal_freshness: float = 0.0    # 信息是否过时 [0, 1]
    gap_analysis: list[str] = field(default_factory=list)  # 缺失的关键方面
    overall_confidence: float = 0.0    # 综合置信度 [0, 1]
    needs_reflection: bool = False     # 是否需要反思

    # 各维度权重
    WEIGHTS = {
        "relevance": 0.35,
        "consistency": 0.20,
        "diversity": 0.15,
        "freshness": 0.15,
        "gap_penalty": 0.15,
    }

    def compute_overall(self) -> float:
        """计算综合置信度"""
        gap_penalty = max(0, 1.0 - len(self.gap_analysis) * 0.2)
        score = (
            self.relevance_coverage * self.WEIGHTS["relevance"]
            + self.internal_consistency * self.WEIGHTS["consistency"]
            + self.source_diversity * self.WEIGHTS["diversity"]
            + self.temporal_freshness * self.WEIGHTS["freshness"]
            + gap_penalty * self.WEIGHTS["gap_penalty"]
        )
        self.overall_confidence = round(min(1.0, max(0.0, score)), 3)
        # 置信度低于阈值 → 需要反思
        self.needs_reflection = self.overall_confidence < 0.45
        return self.overall_confidence

    def to_dict(self) -> dict:
        return {
            "relevance_coverage": round(self.relevance_coverage, 3),
            "internal_consistency": round(self.internal_consistency, 3),
            "source_diversity": round(self.source_diversity, 3),
            "temporal_freshness": round(self.temporal_freshness, 3),
            "gap_analysis": self.gap_analysis,
            "overall_confidence": self.overall_confidence,
            "needs_reflection": self.needs_reflection,
        }


# ═══════════════════════════════════════════════════════
# MetacognitiveEngine — 元认知引擎
# ═══════════════════════════════════════════════════════

class MetacognitiveEngine:
    """
    元认知引擎：检索后的反思与修正（v7.1 增强版）。

    架构：
    - 规则层：快速评估 + 简单修正（扩展/泛化/换角度）
    - LLM 层：语义级查询改写 + 上下文推理

    使用模式：
        meta = MetacognitiveEngine(store, recall_engine, llm_fn=my_llm)

        # 单次评估
        evaluation = meta.evaluate_result(query, results, trace)

        # 带反思的多轮检索
        results, reflections = meta.meta_recall(query)
    """

    # 需要反思的置信度阈值
    REFLECTION_THRESHOLD = 0.45
    # 最大反思轮数（防止无限循环）
    MAX_REFLECTION_ROUNDS = 2
    # 查询修正的关键词扩展数
    MAX_QUERY_EXPANSIONS = 3

    def __init__(self, store=None, recall_engine=None, self_model=None,
                 memory_system: Optional[MetacognitionMemoryProvider] = None,
                 llm_fn: Callable = None):
        """
        参数:
            store: MemoryStore 实例
            recall_engine: RecallEngine 实例
            self_model: SelfModel 实例
            memory_system: MetacognitionMemoryProvider 实例（用于写入反思记忆）
            llm_fn: LLM 函数 fn(prompt: str) -> str（用于语义级查询改写）
        """
        self.store = store
        self.recall = recall_engine
        self.self_model = self.self_model_ref = self_model
        self.memory = memory_system
        self.llm_fn = llm_fn
        self._in_meta_recall = False

    # ── 评估 ─────────────────────────────────────────

    def evaluate_result(
        self,
        query: str,
        results: list[dict],
        trace=None,
    ) -> MetaEvaluation:
        """
        评估检索结果质量。

        维度：
        1. 相关性覆盖 — 结果数量和 top 分数
        2. 内部一致性 — 结果之间主题是否一致
        3. 来源多样性 — 是否跨多个主题/时间窗口
        4. 时间新鲜度 — 最近的结果占比
        5. 缺口分析 — 查询意图的哪些方面没被覆盖
        """
        eval_result = MetaEvaluation()

        if not results:
            eval_result.relevance_coverage = 0.0
            eval_result.gap_analysis.append("没有找到任何结果")
            eval_result.compute_overall()
            return eval_result

        # 1. 相关性覆盖
        top_score = results[0].get("_rank_score", results[0].get("_semantic_score", 0.5))
        count_factor = min(1.0, len(results) / 5)  # 5 条以上算满分
        eval_result.relevance_coverage = min(1.0, top_score * 0.6 + count_factor * 0.4)

        # 2. 内部一致性（主题重叠度）
        eval_result.internal_consistency = self._compute_consistency(results)

        # 3. 来源多样性
        eval_result.source_diversity = self._compute_diversity(results)

        # 4. 时间新鲜度
        eval_result.temporal_freshness = self._compute_freshness(results)

        # 5. 缺口分析
        eval_result.gap_analysis = self._analyze_gaps(query, results, trace)

        # 综合
        eval_result.compute_overall()

        # 如果有 trace，记录不确定因素
        if trace and eval_result.needs_reflection:
            for gap in eval_result.gap_analysis:
                if trace:
                    trace.add_uncertainty(f"gap: {gap}")

        return eval_result

    def _compute_consistency(self, results: list[dict]) -> float:
        """计算结果内部一致性（主题重叠率）"""
        if len(results) <= 1:
            return 1.0

        # 收集所有主题
        all_topics = []
        for m in results:
            topics = set()
            for t in m.get("topics", []):
                if isinstance(t, dict):
                    topics.add(t.get("code", ""))
                else:
                    topics.add(t)
            all_topics.append(topics)

        # 计算平均 Jaccard 相似度
        similarities = []
        for i in range(len(all_topics)):
            for j in range(i + 1, min(i + 3, len(all_topics))):  # 只比较相邻的
                a, b = all_topics[i], all_topics[j]
                if a and b:
                    sim = len(a & b) / len(a | b)
                    similarities.append(sim)
                elif not a and not b:
                    similarities.append(1.0)

        return sum(similarities) / len(similarities) if similarities else 0.5

    def _compute_diversity(self, results: list[dict]) -> float:
        """计算来源多样性（不同主题数 / 结果数）"""
        if len(results) <= 1:
            return 0.5

        unique_topics = set()
        unique_natures = set()
        for m in results:
            for t in m.get("topics", []):
                if isinstance(t, dict):
                    unique_topics.add(t.get("code", ""))
                else:
                    unique_topics.add(t)
            nat = m.get("nature_id", "")
            if nat:
                unique_natures.add(nat)

        topic_diversity = min(1.0, len(unique_topics) / max(1, len(results) * 0.5))
        nature_diversity = min(1.0, len(unique_natures) / max(1, len(results) * 0.3))

        return 0.6 * topic_diversity + 0.4 * nature_diversity

    def _compute_freshness(self, results: list[dict]) -> float:
        """计算时间新鲜度"""
        now = time.time()
        if not results:
            return 0.0

        fresh_count = 0
        for m in results:
            ts = m.get("time_ts", 0)
            if ts and (now - ts) < 86400 * 7:  # 一周内
                fresh_count += 1

        return fresh_count / len(results)

    def _analyze_gaps(
        self,
        query: str,
        results: list[dict],
        trace=None,
    ) -> list[str]:
        """分析查询意图的哪些方面没被覆盖"""
        gaps = []

        if not results:
            gaps.append("empty_results")
            return gaps

        # 结果太少
        if len(results) < 3:
            gaps.append(f"low_result_count: only {len(results)} results")

        # top 分数太低
        top_score = results[0].get("_rank_score", results[0].get("_semantic_score", 0))
        if top_score < 0.2:
            gaps.append(f"low_relevance: top_score={top_score:.3f}")

        # 没有语义命中
        has_semantic = any(m.get("_semantic_score", 0) > 0.3 for m in results[:5])
        if not has_semantic and trace:
            semantic_step = any(s.get("step_type") == "vec_search" for s in (trace.steps if trace else []))
            if semantic_step:
                gaps.append("no_strong_semantic_match")

        # 没有双路命中
        has_dual = any(m.get("_dual_hit") for m in results[:5])
        if not has_dual and len(results) > 1:
            gaps.append("no_dual_hit")

        # 结果全部很旧（超过 30 天）
        now = time.time()
        old_count = sum(1 for m in results[:10] if m.get("time_ts", 0) and (now - m["time_ts"]) > 86400 * 30)
        if old_count > len(results[:10]) * 0.8:
            gaps.append("mostly_outdated_data")

        # trace 不确定因素
        if trace and trace.uncertainty_factors:
            for uf in trace.uncertainty_factors[:3]:
                if "failed" in uf.lower() or "missing" in uf.lower():
                    gaps.append(f"trace_uncertainty: {uf}")

        return gaps

    # ── 反思生成 ─────────────────────────────────────

    def generate_reflection(
        self,
        query: str,
        evaluation: MetaEvaluation,
        results: list[dict],
    ) -> dict:
        """
        基于评估结果生成反思（v7.1 增强版）。

        架构：规则层分析缺口 → LLM 层生成改写（如有）→ 合并

        返回: {
            "reflection_text": str,
            "revised_queries": list[str],
            "action": str,
            "gaps_addressed": list[str],
            "revision_source": str,  # "rules" | "llm" | "hybrid"
            "trace": dict,
        }
        """
        t_start = time.monotonic()
        trace = {"steps": []}

        insights = []
        revised_queries = []
        actions = []

        # 分析缺口
        for gap in evaluation.gap_analysis:
            if "empty_results" in gap:
                insights.append("查询完全没有返回结果，可能关键词不准确")
                revised_queries.extend(self._expand_query(query))
                actions.append("尝试扩展查询关键词")

            elif "low_result_count" in gap:
                insights.append(f"结果数量不足，覆盖面可能不够")
                revised_queries.extend(self._generalize_query(query))
                actions.append("尝试放宽查询范围")

            elif "low_relevance" in gap:
                insights.append("最高相关度分数太低，结果可能不相关")
                revised_queries.extend(self._reframe_query(query))
                actions.append("尝试换一个角度重述查询")

            elif "no_strong_semantic_match" in gap:
                insights.append("语义搜索没有强匹配，可能用词不同但意思相近")
                revised_queries.extend(self._paraphrase_query(query))
                actions.append("尝试同义改写查询")

            elif "no_dual_hit" in gap:
                insights.append("没有结构化和语义双路命中，单一检索路径不够可靠")

            elif "mostly_outdated_data" in gap:
                insights.append("大部分结果超过 30 天，信息可能已过时")
                actions.append("查询最近的更新或变更记录")

            elif "trace_uncertainty" in gap:
                insights.append(f"推理过程存在不确定因素: {gap}")

        # 覆盖率低
        if evaluation.relevance_coverage < 0.3:
            if "查询完全没有返回结果，可能关键词不准确" not in insights:
                insights.append(f"相关性覆盖率低（{evaluation.relevance_coverage:.2f}）")

        # 多样性低
        if evaluation.source_diversity < 0.3:
            insights.append("结果来源过于集中，可能存在信息茧房")
            revised_queries.extend(self._diversify_query(query))
            actions.append("尝试从不同角度查询")

        trace["steps"].append(f"rules_revisions: {len(revised_queries)}")

        # ── LLM 层：语义级查询改写 ──────────────────
        revision_source = "rules"
        if self.llm_fn and (not revised_queries or evaluation.overall_confidence < 0.3):
            try:
                llm_revisions = self._revise_query_with_llm(query, evaluation, results)
                if llm_revisions:
                    trace["steps"].append(f"llm_revisions: {llm_revisions}")
                    if revised_queries:
                        # 混合：LLM 优先
                        revised_queries = llm_revisions + revised_queries[:1]
                        revision_source = "hybrid"
                    else:
                        revised_queries = llm_revisions
                        revision_source = "llm"
                    actions.append("LLM 语义改写查询")
            except Exception as e:
                logger.debug(f"LLM 查询改写失败: {e}")
                trace["steps"].append(f"llm_error: {e}")

        # 去重修正查询
        seen = set()
        unique_revised = []
        for q in revised_queries:
            if q not in seen and q != query:
                seen.add(q)
                unique_revised.append(q)
        revised_queries = unique_revised[:self.MAX_QUERY_EXPANSIONS]

        reflection_text = "；".join(insights) if insights else "检索结果质量尚可，无明显问题"
        action_text = "；".join(set(actions)) if actions else "无需修正"

        elapsed_ms = (time.monotonic() - t_start) * 1000
        trace["elapsed_ms"] = round(elapsed_ms, 2)
        trace["revision_source"] = revision_source
        trace["final_revisions"] = revised_queries

        return {
            "reflection_text": reflection_text,
            "revised_queries": revised_queries,
            "action": action_text,
            "gaps_addressed": evaluation.gap_analysis,
            "confidence": evaluation.overall_confidence,
            "revision_source": revision_source,
            "trace": trace,
        }

    # ── 查询修正策略 ─────────────────────────────────

    def _expand_query(self, query: str) -> list[str]:
        """扩展查询：添加相关词"""
        expansions = []
        # 提取核心名词
        words = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', query)
        if len(words) > 2:
            # 缩短查询
            expansions.append(" ".join(words[:2]) if any(w.isascii() for w in words) else "".join(words[:2]))
            # 添加"相关"前缀
            expansions.append(f"{query} 相关")
        return expansions

    def _generalize_query(self, query: str) -> list[str]:
        """泛化查询：去掉限定词"""
        # 去掉时间限定
        generalized = re.sub(r'(最近|今天|昨天|上周|本月)\s*', '', query)
        if generalized != query:
            return [generalized.strip()]
        # 去掉具体数字
        generalized = re.sub(r'\d+', '', query).strip()
        if generalized and generalized != query:
            return [generalized]
        return []

    def _reframe_query(self, query: str) -> list[str]:
        """换角度重述"""
        reframed = []
        # 把疑问句换成陈述句
        q = query.replace("？", "").replace("?", "").replace("什么", "").replace("怎么", "").strip()
        if q and q != query:
            reframed.append(q)
        return reframed

    def _paraphrase_query(self, query: str) -> list[str]:
        """同义改写"""
        paraphrases = []
        # 简单同义替换
        replacements = {
            "问题": "issue",
            "bug": "错误",
            "优化": "改善",
            "性能": "速度",
            "方案": "做法",
            "配置": "设置",
        }
        for old, new in replacements.items():
            if old in query:
                paraphrases.append(query.replace(old, new))
        return paraphrases[:2]

    def _diversify_query(self, query: str) -> list[str]:
        """多样化查询：从不同角度"""
        diversified = []
        words = re.findall(r'[\u4e00-\u9fff]{2,}', query)
        if len(words) >= 2:
            # 反转词序
            diversified.append("".join(reversed(words)))
            # 只取非核心词
            if len(words) > 2:
                diversified.append("".join(words[1:]))
        return diversified

    def _revise_query_with_llm(
        self,
        query: str,
        evaluation: MetaEvaluation,
        results: list[dict],
    ) -> list[str]:
        """
        用 LLM 进行语义级查询改写。

        比规则层的优势：
        - 理解查询的真实意图，不只是关键词替换
        - 考虑已返回结果的内容，避免重复
        - 生成多个不同角度的改写

        返回: 改写后的查询列表（最多 3 个）
        """
        if not self.llm_fn:
            return []

        # 准备已返回结果的摘要（避免改写后还是搜到同样的）
        result_summaries = []
        for r in results[:5]:
            content = r.get("content", "")[:100]
            topics = r.get("topics", [])
            topic_str = ", ".join(
                t.get("code", t) if isinstance(t, dict) else str(t)
                for t in topics[:3]
            )
            result_summaries.append(f"- [{topic_str}] {content}")

        result_section = "\n".join(result_summaries) if result_summaries else "（无结果）"

        gap_text = "；".join(evaluation.gap_analysis[:3]) if evaluation.gap_analysis else "无"

        prompt = (
            "你是一个搜索优化专家。用户搜索了一个记忆系统，但结果不太理想。\n\n"
            f"原始查询：「{query}」\n"
            f"当前结果：{len(results)} 条，综合置信度 {evaluation.overall_confidence:.2f}\n"
            f"缺口分析：{gap_text}\n\n"
            f"已返回的结果摘要：\n{result_section}\n\n"
            "请生成 1-3 个改写查询，要求：\n"
            "1. 语义上与原查询相关，但角度不同\n"
            "2. 避免搜到上面已有的结果\n"
            "3. 每个改写应覆盖缺口的一个方面\n\n"
            "返回 JSON 数组，如：[\"改写1\", \"改写2\"]\n"
            "不要输出其他内容。"
        )

        try:
            response = self.llm_fn(prompt)
            if not response:
                return []

            json_match = re.search(r'\[[^\]]*\]', response, re.DOTALL)
            if json_match:
                queries = json.loads(json_match.group())
                # 过滤和清理
                clean = [
                    q.strip().strip('"').strip("'")
                    for q in queries
                    if isinstance(q, str) and q.strip() and q.strip() != query
                ]
                logger.debug(f"LLM 查询改写: {query[:30]} → {clean[:3]}")
                return clean[:self.MAX_QUERY_EXPANSIONS]
        except (json.JSONDecodeError, ValueError, TypeError) as e:
            logger.debug(f"LLM 查询改写 JSON 解析失败: {e}")

        return []

    # ── 多轮反思检索 ─────────────────────────────────

    def meta_recall(
        self,
        query: str,
        limit: int = 10,
        max_rounds: int = None,
        remember_reflection: bool = True,
    ) -> dict:
        """
        带反思的检索：不确定 → 反思 → 修正查询 → 重新检索。

        参数:
            query: 原始查询
            limit: 每轮返回条数
            max_rounds: 最大反思轮数（默认 2）
            remember_reflection: 是否将反思写入记忆系统

        返回: {
            "results": [memory dicts],           # 最终结果（可能经过多轮修正）
            "reflections": [reflection dicts],   # 每轮的反思
            "rounds": int,                       # 实际执行了几轮
            "original_results": [memory dicts],  # 第一轮原始结果
            "evaluation": dict,                  # 最终评估
        }
        """
        max_rounds = max_rounds or self.MAX_REFLECTION_ROUNDS
        if self._in_meta_recall:
            return {"results": [], "reflections": [], "rounds": 0, "original_results": [], "evaluation": {}}
        if not self.recall:
            return {"results": [], "reflections": [], "rounds": 0, "original_results": [], "evaluation": {}}

        self._in_meta_recall = True
        all_reflections = []
        current_query = query
        original_results = None
        query_history = [{"round": 0, "query": query}]

        try:
            for round_num in range(max_rounds + 1):
                # 执行检索
                recall_result = self.recall.recall(
                    query=current_query,
                    limit=limit,
                )
                results = recall_result.get("primary", [])
                trace_data = recall_result.get("_trace")
                trace = None

                # 恢复 trace 对象
                if trace_data and self.self_model:
                    from self_model import ReasoningTrace
                    trace = ReasoningTrace.from_dict(trace_data)

                # 保存第一轮原始结果
                if round_num == 0:
                    original_results = results

                # 评估
                evaluation = self.evaluate_result(current_query, results, trace)

                # 如果不需要反思，或者已到最大轮数，结束
                if not evaluation.needs_reflection or round_num >= max_rounds:
                    # 最后一轮反思（如果有）
                    if evaluation.needs_reflection and round_num < max_rounds:
                        pass  # 下面会处理
                    else:
                        break

                # 生成反思
                reflection = self.generate_reflection(current_query, evaluation, results)
                reflection["round"] = round_num + 1
                reflection["original_query"] = query
                all_reflections.append(reflection)

                # 反思修正追踪日志
                try:
                    from trace_logger import get_tracer
                    tracer = get_tracer()
                    confidence_before = evaluation.overall_confidence
                    tracer.log_meta_recall_reflection(
                        round_num=round_num + 1,
                        original_query=query,
                        refined_query=current_query,
                        strategy=reflection.get("revision_source"),
                        before_results=results,
                        confidence_before=confidence_before,
                        trace_id=None,
                    )
                except Exception as e:
                    logger.warning("metacognition: %s", e)

                # 如果没有修正查询可用，停止
                if not reflection.get("revised_queries"):
                    break

                # 使用第一个修正查询
                current_query = reflection["revised_queries"][0]
                query_history.append({
                    "round": round_num + 1,
                    "query": current_query,
                    "source": reflection.get("revision_source", "rules"),
                    "confidence_before": evaluation.overall_confidence,
                })
                logger.debug(
                    f"元认知反思第 {round_num+1} 轮: "
                    f"confidence={evaluation.overall_confidence:.3f}, "
                    f"revised_query={current_query[:50]}"
                )

                # 反思记忆化
                if remember_reflection and self.memory:
                    self._remember_reflection(query, reflection, evaluation)

            return {
                "results": results if 'results' in dir() else [],
                "reflections": all_reflections,
                "rounds": len(all_reflections) + 1,
                "original_results": original_results or [],
                "evaluation": evaluation.to_dict() if 'evaluation' in dir() else {},
                "query_history": query_history,
            }
        finally:
            self._in_meta_recall = False

    def _remember_reflection(self, original_query: str, reflection: dict, evaluation: MetaEvaluation):
        """将反思写入记忆系统"""
        if not self.memory:
            return
        try:
            content = (
                f"检索'{original_query}'时的元认知反思："
                f"{reflection['reflection_text']}。"
                f"置信度: {evaluation.overall_confidence:.2f}。"
                f"建议: {reflection.get('action', '无')}"
            )
            self.memory.remember(
                content=content,
                importance="medium",
                nature="retro",
                force=True,  # 跳过过滤，反思总是值得记录
            )
            logger.debug(f"反思已写入记忆: {content[:60]}")
        except Exception as e:
            logger.warning("metacognition: %s", e)

    # ── 统计 ─────────────────────────────────────────

    def get_stats(self) -> dict:
        """元认知引擎统计"""
        stats = {
            "reflection_threshold": self.REFLECTION_THRESHOLD,
            "max_rounds": self.MAX_REFLECTION_ROUNDS,
        }
        if self.store:
            try:
                rows = self.store.conn.execute(
                    "SELECT COUNT(*) FROM memories WHERE nature_id LIKE '%retro%'"
                ).fetchone()
                stats["reflection_memories"] = rows[0] if rows else 0
            except Exception:
                stats["reflection_memories"] = "unknown"
        return stats

    # ══════════════════════════════════════════════════════
    # v8.3: 知识盲区检测
    # ══════════════════════════════════════════════════════

    def detect_knowledge_gaps(self, topic_registry=None) -> list[dict]:
        """
        检测知识盲区：已注册但无/少记忆的主题领域。

        策略：
        1. 从主题注册表获取所有已注册主题
        2. 查询每个主题的记忆数量和最近活跃时间
        3. 标记空白/稀疏/过时的主题
        4. 分析主题树的结构性缺失（父主题有记忆但子主题没有）

        参数:
            topic_registry: TopicRegistry 实例（可选）

        返回: [{
            "topic": str,
            "gap_type": "empty"|"sparse"|"stale"|"structural",
            "memory_count": int,
            "last_active_ts": int,
            "priority": float,
            "suggestion": str,
        }]
        """
        if not self.store:
            return []

        gaps = []

        try:
            topic_counts = self.store.conn.execute(
                "SELECT topic_code, COUNT(*) as cnt, MAX(m.time_ts) as last_ts "
                "FROM memory_topics mt JOIN memories m ON mt.memory_id = m.memory_id "
                "GROUP BY topic_code"
            ).fetchall()
        except Exception as e:
            logger.warning("metacognition: %s", e)
            return []

        count_map = {r["topic_code"]: {"count": r["cnt"], "last_ts": r["last_ts"]} for r in topic_counts}

        registered_topics = set()
        if topic_registry:
            try:
                for code in topic_registry.list_codes():
                    registered_topics.add(code)
            except Exception as e:
                logger.warning("metacognition: %s", e)

        if not registered_topics:
            registered_topics = set(count_map.keys())

        now = int(time.time())
        for topic_code in registered_topics:
            info = count_map.get(topic_code, {"count": 0, "last_ts": 0})
            cnt = info["count"]
            last_ts = info["last_ts"] or 0

            if cnt == 0:
                gaps.append({
                    "topic": topic_code,
                    "gap_type": "empty",
                    "memory_count": 0,
                    "last_active_ts": 0,
                    "priority": 0.8,
                    "suggestion": f"主题 '{topic_code}' 已注册但无任何记忆，建议主动探索",
                })
            elif cnt < 3:
                gaps.append({
                    "topic": topic_code,
                    "gap_type": "sparse",
                    "memory_count": cnt,
                    "last_active_ts": last_ts,
                    "priority": 0.6,
                    "suggestion": f"主题 '{topic_code}' 仅有 {cnt} 条记忆，知识覆盖不足",
                })
            elif last_ts and (now - last_ts) > 30 * 86400:
                gaps.append({
                    "topic": topic_code,
                    "gap_type": "stale",
                    "memory_count": cnt,
                    "last_active_ts": last_ts,
                    "priority": 0.5,
                    "suggestion": f"主题 '{topic_code}' 超过30天无新记忆，可能需要更新",
                })

        structural_gaps = self._detect_structural_gaps(count_map, registered_topics)
        gaps.extend(structural_gaps)

        gaps.sort(key=lambda x: -x["priority"])

        logger.info(f"🔍 知识盲区检测: {len(gaps)} 个盲区 "
                     f"(empty={sum(1 for g in gaps if g['gap_type']=='empty')}, "
                     f"sparse={sum(1 for g in gaps if g['gap_type']=='sparse')}, "
                     f"stale={sum(1 for g in gaps if g['gap_type']=='stale')}, "
                     f"structural={sum(1 for g in gaps if g['gap_type']=='structural')})")
        return gaps

    def _detect_structural_gaps(
        self, count_map: dict, registered_topics: set
    ) -> list[dict]:
        """检测主题树的结构性缺失：父主题有记忆但子主题没有"""
        gaps = []
        parent_map = {}

        for topic_code in registered_topics:
            parts = topic_code.split(".")
            if len(parts) > 1:
                parent = ".".join(parts[:-1])
                if parent not in parent_map:
                    parent_map[parent] = []
                parent_map[parent].append(topic_code)

        for parent, children in parent_map.items():
            parent_info = count_map.get(parent, {"count": 0})
            if parent_info["count"] >= 3:
                empty_children = [
                    c for c in children
                    if count_map.get(c, {"count": 0})["count"] == 0
                ]
                if empty_children:
                    gaps.append({
                        "topic": parent,
                        "gap_type": "structural",
                        "memory_count": parent_info["count"],
                        "last_active_ts": parent_info.get("last_ts", 0),
                        "priority": 0.7,
                        "suggestion": f"父主题 '{parent}' 有记忆但子主题 {empty_children} 无记忆，知识结构不完整",
                        "empty_children": empty_children,
                    })

        return gaps

    # ══════════════════════════════════════════════════════
    # v8.3: 主动学习建议
    # ══════════════════════════════════════════════════════

    def generate_learning_plan(
        self,
        focus_topics: list[str] = None,
        max_suggestions: int = 5,
        use_llm: bool = True,
    ) -> list[dict]:
        """
        基于知识盲区生成主动学习建议。

        参数:
            focus_topics: 聚焦的主题列表（None=全部）
            max_suggestions: 最大建议数
            use_llm: 是否使用 LLM 生成更精准的建议

        返回: [{
            "topic": str,
            "action": str,
            "reason": str,
            "priority": float,
            "learning_path": [str],
        }]
        """
        gaps = self.detect_knowledge_gaps()

        if focus_topics:
            gaps = [g for g in gaps if g["topic"] in focus_topics or
                    any(ft in g["topic"] for ft in focus_topics)]

        suggestions = []
        for gap in gaps[:max_suggestions * 2]:
            topic = gap["topic"]
            gap_type = gap["gap_type"]
            priority = gap["priority"]

            if gap_type == "empty":
                suggestions.append({
                    "topic": topic,
                    "action": "探索新领域",
                    "reason": gap["suggestion"],
                    "priority": priority,
                    "learning_path": [
                        f"了解 {topic} 的基本概念",
                        f"查找 {topic} 的核心问题和挑战",
                        f"记录对 {topic} 的初步理解",
                    ],
                })
            elif gap_type == "sparse":
                suggestions.append({
                    "topic": topic,
                    "action": "补充知识",
                    "reason": gap["suggestion"],
                    "priority": priority,
                    "learning_path": [
                        f"深入 {topic} 的关键子领域",
                        f"对比 {topic} 的不同方法/观点",
                        f"总结 {topic} 的知识体系",
                    ],
                })
            elif gap_type == "stale":
                suggestions.append({
                    "topic": topic,
                    "action": "更新知识",
                    "reason": gap["suggestion"],
                    "priority": priority,
                    "learning_path": [
                        f"检查 {topic} 的最新进展",
                        f"对比旧认知与新信息",
                        f"更新 {topic} 的理解",
                    ],
                })
            elif gap_type == "structural":
                empty_children = gap.get("empty_children", [])
                suggestions.append({
                    "topic": topic,
                    "action": "完善知识结构",
                    "reason": gap["suggestion"],
                    "priority": priority,
                    "learning_path": [
                        f"逐个探索子主题: {', '.join(empty_children[:3])}",
                        f"建立 {topic} 的完整知识树",
                    ],
                })

        if use_llm and self.llm_fn and suggestions:
            suggestions = self._enhance_learning_plan_with_llm(suggestions[:3])

        suggestions.sort(key=lambda x: -x["priority"])
        return suggestions[:max_suggestions]

    def _enhance_learning_plan_with_llm(self, suggestions: list[dict]) -> list[dict]:
        """用 LLM 增强学习建议的精准度"""
        if not self.llm_fn:
            return suggestions

        for s in suggestions[:3]:
            try:
                prompt = (
                    f"对于主题「{s['topic']}」，当前知识状态：{s['reason']}。\n"
                    f"请给出 2-3 个具体的学习步骤，每步不超过 20 字。\n"
                    f"返回 JSON 数组，如：[\"步骤1\", \"步骤2\"]\n"
                    f"不要输出其他内容。"
                )
                raw = self.llm_fn(prompt)
                match = re.search(r'\[[^\]]*\]', raw, re.DOTALL)
                if match:
                    steps = json.loads(match.group())
                    if isinstance(steps, list) and steps:
                        s["learning_path"] = [str(st).strip() for st in steps if isinstance(st, str)]
            except Exception as e:
                logger.warning("metacognition: %s", e)

        return suggestions

    # ══════════════════════════════════════════════════════
    # v8.3: 认知一致性检查
    # ══════════════════════════════════════════════════════

    def check_cognitive_consistency(
        self,
        topic_code: str = None,
        window_days: int = 90,
    ) -> dict:
        """
        检查记忆系统中的认知一致性。

        检测：
        1. 同一主题下的矛盾观点
        2. 情感极性翻转（对同一事物的态度变化）
        3. 重要性跃迁（同一主题的重要性突然变化）
        4. 认知演进（旧观点被新观点修正）

        参数:
            topic_code: 限定主题（None=全部）
            window_days: 检测窗口（天）

        返回: {
            "consistency_score": float,
            "inconsistencies": [dict],
            "evolutions": [dict],
            "summary": str,
        }
        """
        if not self.store:
            return {"consistency_score": 1.0, "inconsistencies": [], "evolutions": [], "summary": "无数据"}

        cutoff = int(time.time()) - window_days * 86400
        inconsistencies = []
        evolutions = []

        try:
            if topic_code:
                rows = self.store.conn.execute(
                    "SELECT m.memory_id, m.content, m.valence, m.importance, "
                    "m.time_ts, m.significance, m.confidence "
                    "FROM memories m JOIN memory_topics mt ON m.memory_id = mt.memory_id "
                    "WHERE mt.topic_code = ? AND m.time_ts >= ? "
                    "ORDER BY m.time_ts",
                    (topic_code, cutoff),
                ).fetchall()
            else:
                rows = self.store.conn.execute(
                    "SELECT memory_id, content, valence, importance, "
                    "time_ts, significance, confidence FROM memories "
                    "WHERE time_ts >= ? ORDER BY time_ts",
                    (cutoff,),
                ).fetchall()
        except Exception as e:
            logger.warning("metacognition: %s", e)
            return {"consistency_score": 1.0, "inconsistencies": [], "evolutions": [], "summary": "查询失败"}

        if len(rows) < 2:
            return {"consistency_score": 1.0, "inconsistencies": [], "evolutions": [], "summary": "数据不足"}

        importance_order = {"trivial": 0, "notable": 1, "medium": 2, "important": 3,
                            "breakthrough": 4, "crisis": 4, "milestone": 5}

        for i in range(len(rows) - 1):
            curr = rows[i]
            next_row = rows[i + 1]

            curr_valence = curr[2] or 0.0
            next_valence = next_row[2] or 0.0
            valence_diff = abs(curr_valence - next_valence)

            if valence_diff > 0.6 and (curr_valence * next_valence < 0):
                inconsistencies.append({
                    "type": "valence_flip",
                    "memory_a_id": curr[0],
                    "memory_b_id": next_row[0],
                    "valence_a": curr_valence,
                    "valence_b": next_valence,
                    "time_gap_hours": (next_row[4] - curr[4]) / 3600 if curr[4] and next_row[4] else 0,
                })

            curr_imp = importance_order.get(curr[3] or "medium", 2)
            next_imp = importance_order.get(next_row[3] or "medium", 2)
            if next_imp - curr_imp >= 2:
                evolutions.append({
                    "type": "importance_upgrade",
                    "memory_a_id": curr[0],
                    "memory_b_id": next_row[0],
                    "importance_a": curr[3],
                    "importance_b": next_row[3],
                })

            curr_conf = curr[6] or 0.5
            next_conf = next_row[6] or 0.5
            if curr_conf > 0.7 and next_conf < 0.3:
                inconsistencies.append({
                    "type": "confidence_drop",
                    "memory_a_id": curr[0],
                    "memory_b_id": next_row[0],
                    "confidence_a": curr_conf,
                    "confidence_b": next_conf,
                })

        total_pairs = len(rows) - 1
        inconsistency_ratio = len(inconsistencies) / max(1, total_pairs)
        consistency_score = max(0.0, 1.0 - inconsistency_ratio * 2)

        summary_parts = []
        if inconsistencies:
            summary_parts.append(f"{len(inconsistencies)} 处不一致")
        if evolutions:
            summary_parts.append(f"{len(evolutions)} 处认知演进")
        summary = "；".join(summary_parts) if summary_parts else "认知一致"

        return {
            "consistency_score": round(consistency_score, 3),
            "inconsistencies": inconsistencies,
            "evolutions": evolutions,
            "summary": summary,
        }
