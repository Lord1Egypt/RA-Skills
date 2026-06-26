#!/usr/bin/env python3
"""SkillRouter v2 - Python embedding 粗筛 top5,返回丰富上下文给 LLM 精排"""
import json
import sys
import re
from pathlib import Path
import numpy as np

V2_DIR = Path(__file__).parent
WORKSPACE = V2_DIR.parent

# 尝试加载 embedding 模型
_EMBEDDING_MODEL = None


def _load_embedding_model():
    global _EMBEDDING_MODEL
    if _EMBEDDING_MODEL is not None:
        return _EMBEDDING_MODEL
    try:
        import os
        os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
        from sentence_transformers import SentenceTransformer
        _EMBEDDING_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
        return _EMBEDDING_MODEL
    except Exception as e:
        print(f"[router_top5] embedding 模型加载失败: {e}", file=sys.stderr)
        return None


class Top5Router:
    """embedding 检索 → top5 候选(含丰富画像)"""

    def __init__(self, index_path: Path = None):
        if index_path is None:
            index_path = V2_DIR / "skill_index_v2.json"

        # 加载索引
        self.data = json.loads(index_path.read_text(encoding="utf-8"))
        self.skills: list[dict] = self.data["skills"]
        self.total = self.data["total"]

        # 加载 embeddings(如果存在)
        emb_path = index_path.with_suffix(".embeddings.npy")
        self.embeddings: np.ndarray | None = None
        if emb_path.exists():
            self.embeddings = np.load(emb_path)

        self._model = None

        # 加载外部配置(翻译映射、拒选词表)
        self._ref_dir = V2_DIR / "references"
        self._load_configs()

    def _load_configs(self):
        """从 references/ 目录加载配置(翻译映射、拒选词表)"""
        ref = self._ref_dir

        # 中英翻译映射
        zh2en_path = ref / "zh2en-map.json"
        if zh2en_path.exists():
            data = json.loads(zh2en_path.read_text(encoding="utf-8"))
            self.zh2en_map = [(item["zh"], item["en"]) for item in data["zh2en"]]
        else:
            self.zh2en_map = []

        # 拒选配置
        noise_path = ref / "noise-words.json"
        if noise_path.exists():
            noise = json.loads(noise_path.read_text(encoding="utf-8"))
            self.info_seek_words = set(noise.get("info_seek_words", []))
            self.strong_skill_words = set(noise.get("strong_skill_words", []))
            self.action_phrases = set(noise.get("action_phrases", []))
            self.task_words_list = noise.get("task_words", [])
            self.task_words_set = set(self.task_words_list)
            self.min_absolute_rrf = noise.get("thresholds", {}).get("min_absolute_rrf", 0.008)
            self.min_gap_ratio = noise.get("thresholds", {}).get("min_gap_ratio", 0.06)
            self.task_min_len = noise.get("thresholds", {}).get("task_min_len", 2)
        else:
            self.info_seek_words = set()
            self.strong_skill_words = set()
            self.action_phrases = set()
            self.task_words_list = []
            self.task_words_set = set()
            self.min_absolute_rrf = 0.008
            self.min_gap_ratio = 0.06
            self.task_min_len = 2

    @property
    def model(self):
        if self._model is None:
            self._model = _load_embedding_model()
        return self._model

    def build_embeddings(self, force: bool = False):
        """为所有 skill 生成 embeddings(首次运行需要)"""
        emb_path = V2_DIR / "skill_index_v2.embeddings.npy"
        if emb_path.exists() and not force:
            self.embeddings = np.load(emb_path)
            return

        model = self.model
        if model is None:
            print("[router_top5] embedding 模型不可用,无法生成 embeddings", file=sys.stderr)
            return

        # 构建 embedding 文本(仅用 compact 字段避免 OOM;body 留给 LLM 精排阶段)
        texts = []
        for s in self.skills:
            parts = [
                f"名称: {s['name']}",
                f"描述: {s.get('description', '')}",
            ]
            caps = s.get('capabilities', [])
            if caps:
                parts.append(f"能力: {', '.join(caps)}")
            t = '\n'.join(parts)
            texts.append(t)

        print(f"[router_top5] 正在为 {len(texts)} 个 skill 生成 embeddings...", file=sys.stderr)

        # 小批次编码避免 OOM(每次 50 个,编码完立即释放)
        import gc
        batch_size = 50
        all_embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_emb = model.encode(batch, show_progress_bar=False)
            all_embeddings.append(batch_emb)
            gc.collect()
            if (i // batch_size) % 5 == 0:
                print(f"  ... {i}/{len(texts)}", file=sys.stderr)

        self.embeddings = np.concatenate(all_embeddings, axis=0)
        np.save(emb_path, self.embeddings)
        print(f"[router_top5] embeddings 已保存到 {emb_path} (shape: {self.embeddings.shape})", file=sys.stderr)

    def _bm25_search(self, query: str, top_k: int = 20) -> list[int]:
        """BM25 关键词检索(name + description + capabilities 作为文档)"""
        import math
        from collections import defaultdict

        # 分词(简单按空格+中文单字切分)
        import re
        def tokenize(text):
            tokens = re.findall(r'[\u4e00-\u9fff]|[a-zA-Z0-9]+', text.lower())
            return tokens

        query_tokens = tokenize(query)
        if not query_tokens:
            return []

        # 预计算文档
        docs = []
        for s in self.skills:
            doc = f"{s['name']} {s.get('description','')} {' '.join(s.get('capabilities',[]))}"
            docs.append(tokenize(doc))

        # IDF
        N = len(docs)
        df = defaultdict(int)
        for doc in docs:
            for t in set(doc):
                df[t] += 1

        k1, b = 1.5, 0.75
        avgdl = sum(len(d) for d in docs) / max(N, 1)

        scores = []
        for i, doc in enumerate(docs):
            dl = len(doc)
            score = 0.0
            tf = defaultdict(int)
            for t in doc:
                tf[t] += 1
            for t in query_tokens:
                if t in tf:
                    idf = math.log((N - df[t] + 0.5) / (df[t] + 0.5) + 1)
                    term_score = idf * (tf[t] * (k1 + 1)) / (tf[t] + k1 * (1 - b + b * dl / avgdl))
                    score += term_score
            scores.append((i, score))

        scores.sort(key=lambda x: -x[1])
        return [idx for idx, s in scores[:top_k] if s > 0]

    # ─── Capability Taxonomy ─────────────────────────────────────────
    # 用户 query → capability 抽象层 → skill 解析
    # 不直接绑 skill 名,先映射到用户要的
    # 中英翻译映射表从 references/zh2en-map.json 加载
    # 在 __init__ 中通过 _load_configs() 初始化 self.zh2en_map

    def _translate_query(self, query: str) -> str:
        """
        翻译桥 v2:纯英文输出,不再拼接中文原文
        让 all-MiniLM-L6-v2 在纯英文空间中匹配 skill 库
        """
        sorted_map = sorted(
            self.zh2en_map,
            key=lambda x: -len(x[0])
        )
        en_parts = []
        for zh, en in sorted_map:
            if zh in query:
                en_parts.append(en)
        # 去重 + 整理成句子
        seen = set()
        unique = []
        for w in en_parts:
            for tok in w.split():
                if tok not in seen:
                    seen.add(tok)
                    unique.append(tok)
        if not unique:
            return query  # fallback 到原文
        # 纯英文输出:翻译词重复两次([翻译词] + [翻译词])增强语义信号
        return ' '.join(unique) + ' . ' + ' '.join(unique)

    def route(self, query: str, top_k: int = 5) -> list[dict]:
        """
        混合检索(BM25 + embedding)→ 返回 top_k 个最匹配的 skill 完整画像

        返回格式:
[{name, description, dir, path, capabilities, brief_guide, body_start, relevance, query_profile}, ...]
        """
        # 1. Capability Taxonomy 检测
        #    在嵌入计算之前做,快速判断方向
        from capability_taxonomy import CapabilityTaxonomy
        if not hasattr(self, '_cap_taxonomy'):
            self._cap_taxonomy = CapabilityTaxonomy()
        matched_caps = self._cap_taxonomy.detect(query)

        # 1a. 通用信息查询 → 直接拒选(走 L0 工具)
        if 'general_info' in matched_caps:
            print(f"[CapTax] 通用信息查询 → 直拒 (caps={matched_caps})", file=sys.stderr)
            return []

        # 1b. 如果检测到明确的能力,尝试 resolve 到 skill
        cap_boost_indices = set()
        if matched_caps:
            cap_skill_indices = self._cap_taxonomy.resolve(matched_caps, self.skills, top_k=top_k)
            cap_boost_indices = set(cap_skill_indices)
            if cap_skill_indices:
                cap_names = [c for c in matched_caps[:3]]
                print(f"[CapTax] 检测到能力: {cap_names} → resolve到{len(cap_skill_indices)}个skill", file=sys.stderr)

        if self.embeddings is None:
            self.build_embeddings()

        model = self.model
        if model is None or self.embeddings is None:
            return self.skills[:top_k]

        # 2. BM25 关键词检索(取 top 20)-- 仍然用中文原文
        bm25_indices = self._bm25_search(query, top_k=20)

        # 3. Embedding 语义检索(双通道加权融合)
        q_emb_zh = model.encode([query], show_progress_bar=False)[0]
        en_query = self._translate_query(query)
        q_emb_en = model.encode([en_query], show_progress_bar=False)[0]
        q_norm_zh = q_emb_zh / (np.linalg.norm(q_emb_zh) + 1e-10)
        q_norm_en = q_emb_en / (np.linalg.norm(q_emb_en) + 1e-10)
        emb_norm = self.embeddings / (
            np.linalg.norm(self.embeddings, axis=1, keepdims=True) + 1e-10
        )
        emb_scores = (
            0.3 * np.dot(emb_norm, q_norm_zh) +
            0.7 * np.dot(emb_norm, q_norm_en)
        )

        # 4. 加权RRF (Weighted Reciprocal Rank Fusion)
        embed_rank = np.argsort(emb_scores)[::-1]
        bm25_rank_map = {idx: r+1 for r, idx in enumerate(bm25_indices)}

        # 复杂度分类器（在此初始化，确保不走 early return 浪费计算）
        from complexity_classifier import QueryProfile
        _query_profile = QueryProfile(query)
        
        k = 60  # RRF 平滑常数（openclaw-tactician 默认值）
        # 复杂度自适应权重（参考 openclaw-tactician）
        # 复杂任务 → 增强语义/降低BM25权重（避免噪声候选混入）
        # 简单任务 → 降低语义/增强BM25权重（允许更多候选）
        complexity = _query_profile.complexity
        if complexity == "complex":
            EMBED_WEIGHT = 2.5
            BM25_WEIGHT = 0.3
        elif complexity == "moderate":
            EMBED_WEIGHT = 2.0
            BM25_WEIGHT = 0.5
        else:  # simple
            EMBED_WEIGHT = 1.5
            BM25_WEIGHT = 0.7

        rrf_scores = np.zeros(len(emb_scores))
        for rank, idx in enumerate(embed_rank):
            rrf_scores[idx] += EMBED_WEIGHT / (k + rank + 1)
        for idx, bm_rank in bm25_rank_map.items():
            rrf_scores[idx] += BM25_WEIGHT / (k + bm_rank)

        # 4a. Capability Boost: resolve到的skill加小额外分
        # 让 taxonomy 优先推荐的 skill 在排序中靠前
        BOOST = 0.005  # 约为典型RRF分数的12-15%
        for idx in cap_boost_indices:
            rrf_scores[idx] += BOOST

        # 5. 取 top_k 候选
        top_indices = np.argsort(rrf_scores)[::-1][:top_k]
        top_candidates = [self.skills[int(idx)] for idx in top_indices]

        if self._is_noise(query, top_candidates, rrf_scores, top_indices):
            return []

        results = []
        for idx in top_indices:
            skill = dict(self.skills[int(idx)])
            skill["relevance"] = round(float(rrf_scores[int(idx)]), 4)
            skill["relevance_embed"] = round(float(emb_scores[int(idx)]), 4)
            skill["query_profile"] = _query_profile.to_dict()
            results.append(skill)

        return results

    def _is_noise(self, query: str, candidates: list[dict],
                  rrf_scores: np.ndarray, top_indices: np.ndarray) -> bool:
        """
        噪声检测:三道防线

        0 - 信息查询意图检测:query只是查/找/搜信息,不要求skill做事
            → 强制拒选,直接进L0工具保底
        A - 任务关键词重叠:query中的任务词与top3候选描述子串匹配
        B - 分数阈值:加权RRF top1太低 或 gap太小

        防线0单独触发即拒绝。防线A+B双重触发才拒绝。
        """
        import sys

        q_lower = query.lower()

        # ================================================================
        # 防线0: 信息查询意图检测 + 垃圾输入检测
        # ================================================================
        INFO_SEEK_WORDS = self.info_seek_words
        STRONG_SKILL_WORDS = self.strong_skill_words

        # 垃圾输入检测
        if len(q_lower.strip()) < 2:
            print(f"[router_top5] 输入过短 → 拒选 (len={len(q_lower.strip())})", file=sys.stderr)
            return True
        # 纯符号/数字
        alpha_chars = sum(1 for c in q_lower if c.isalpha())
        if alpha_chars < 2:
            print(f"[router_top5] 无有效文字 → 拒选 (alpha={alpha_chars})", file=sys.stderr)
            return True

        has_info_seek = any(w in q_lower for w in INFO_SEEK_WORDS)
        has_strong_skill = any(w in q_lower for w in STRONG_SKILL_WORDS)

        # 信息查询意图拒选 + 强技能意图豁免
        # 规则: 有 info_seek 且没有 strong_skill → 拒选
        # 例外: query中包含明确的动作指令(列出来、帮我、发给、发邮件等)
        has_action = any(ap in q_lower for ap in self.action_phrases)

        if has_info_seek and not has_strong_skill and not has_action:
            # 移除年份数字(2024/2025/2026)导致的误拦
            year_pattern = re.search(r'20\d{2}', q_lower)
            # 如果仅因为年份触发 + 有任务词 → 放行
            if year_pattern:
                year_only_info_seek = all(w not in q_lower or w in ('最新','最近') or len(w) < 2
                                          for w in INFO_SEEK_WORDS)
                if year_only_info_seek:
                    pass  # 放行
                else:
                    print(f"[router_top5] 信息查询意图 → 拒选L1,直接L0工具保底 "
                          f"(info_seek={has_info_seek} strong_skill={has_strong_skill})", file=sys.stderr)
                    return True
            else:
                print(f"[router_top5] 信息查询意图 → 拒选L1,直接L0工具保底 "
                      f"(info_seek={has_info_seek} strong_skill={has_strong_skill})", file=sys.stderr)
                return True

        # ================================================================
        # 防线A+B: 任务词重叠 + 分数阈值
        # ================================================================

        top1_score = rrf_scores[top_indices[0]]
        top_k = len(top_indices)
        top_k_score = rrf_scores[top_indices[-1]] if top_k >= 3 else 0
        gap_ratio = (top1_score - top_k_score) / (top1_score + 1e-10)

        # 翻译后 RRF 分数偏低(0.01-0.06),阈值相应调低
        # 防线B: 分数阈值(从 references/noise-words.json 加载)
        score_noise = (top1_score < self.min_absolute_rrf
                       or gap_ratio < self.min_gap_ratio)

        # 防线A: 任务关键词重叠(中英文双轨匹配)
        # 词表从 references/noise-words.json 加载
        q_lower = query.lower()
        hit_tasks = {tw for tw in self.task_words_list
                     if tw in q_lower and len(tw) >= self.task_min_len}

        # 防线A: query中有可识别的任务词 → 直接确认有任务意图
        # skill库已全英文化,中文任务词在英文capabilities中找不到子串匹配
        # 因此 hit_tasks 非空本身就说明用户有明确的任务意图
        # Phase 3 修正:hit_tasks非空→视为有任务重叠,不再检查skill_text
        has_overlap = True if hit_tasks else False

        # 必须双重触发:零任务重叠 AND 分数也低
        if (not has_overlap) and score_noise:
            print(f"[router_top5] 噪声拒绝: 任务词无重叠(hit={hit_tasks}) "
                  f"+ top1_rrf={top1_score:.4f} gap={gap_ratio:.3f}", file=sys.stderr)
            return True

        return False

    def route_formatted(self, query: str, top_k: int = 5) -> str:
        """返回格式化的文本块,直接给 LLM"""

        # 0. CapTax + ChainEngine 检测
        from capability_taxonomy import CapabilityTaxonomy
        if not hasattr(self, '_cap_taxonomy'):
            self._cap_taxonomy = CapabilityTaxonomy()
        matched_caps = self._cap_taxonomy.detect(query)

        from chain_engine import ChainEngine
        if not hasattr(self, '_chain_engine'):
            self._chain_engine = ChainEngine()
        chain = self._chain_engine.match_chain(matched_caps, query) if matched_caps else None

        # 如果匹配到 chain → 优先输出 chain plan
        if chain:
            plan = self._chain_engine.format_plan(chain)
            # 用 route() 获取各步骤的 skill 确认信息
            steps_info = []
            for step in chain.steps:
                step_results = self.route(f"{step.description} {step.skill}", top_k=1)
                if step_results:
                    skill_name = step_results[0]["name"]
                else:
                    skill_name = step.skill
                steps_info.append(f"    {step.order}. [{step.capability}] {skill_name} - {step.description}")

            parallel_info = ""
            if chain.parallel_groups:
                groups = []
                for g in chain.parallel_groups:
                    names = [f"步骤{i+1}" for i in g if i < len(chain.steps)]
                    groups.append("+".join(names))
                parallel_info = f"\n  ⚡ 可并行: {' | '.join(groups)}"

            return (
                f"--- 检测到复杂意图 → 建议多技能链 ---\n"
                f"链: {chain.name}\n"
                f"描述: {chain.description}"
                f"{parallel_info}\n\n"
                + "\n".join(steps_info)
                + f"\n\n  输出: {chain.output}"
                + f"\n\n--- LLM请按步骤顺序选择对应skill执行。如不合适,回复 '拒选'。---"
            )

        # 无 chain 匹配 → 标准单技能路由
        results = self.route(query, top_k=top_k)

        if not results:
            return "--- 无可选技能(噪声拒绝:所有候选与查询无关)---\n\n请回复 '拒选'。"

        from schemas import SkillProfile

        blocks = []
        for i, r in enumerate(results):
            profile = SkillProfile(
                name=r["name"],
                description=r.get("description", ""),
                dir=r.get("dir", ""),
                path=r.get("path", ""),
                capabilities=r.get("capabilities", []),
                brief_guide=r.get("brief_guide", ""),
                body_start=r.get("body_start", ""),
                relevance=r.get("relevance", 0.0),
            )
            blocks.append(profile.to_prompt_block(i + 1))

        header = f"--- 可选技能(语义匹配度 top{top_k})---\n"
        footer = "\n--- 请从以上技能中选择最匹配的一个或多个。如果不匹配任何技能,请回复 '拒选'。---"
        return header + "\n\n".join(blocks) + footer


# ============================================================================
# 独立调用入口
# ============================================================================
if __name__ == "__main__":
    import sys

    router = Top5Router()
    if not router.embeddings:
        print("首次运行:构建 embeddings...")
        router.build_embeddings()

    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = "做一篇脓毒症脑病的文献计量分析"

    print(f"Query: {query}\n")
    print(router.route_formatted(query, top_k=5))
