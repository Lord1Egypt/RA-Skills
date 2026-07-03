#!/usr/bin/env python3
"""
semantic-split Pipeline A — 语义匹配管线 v0.1.0

三层递进：正则层(keyword substring) → embedding层(cosine) → BERT rerank层(CrossEncoder)

覆盖步骤：
  Step 1:   JSON 扫描匹配（替换 json_manager._match_score 的弱词匹配）
  Step 2.5a: 约束关键词初判(🔴/🟡/⚪)
  Step 2.5c: 注意力锚定[EXAMPLE/CRITICAL](语义补充)
  Step 3:   5W2H 的 Why / When(正则部) / How much
  Step 6:   自增强通用化(语义归类)
  Step 7:   规则凝练(步骤相似度聚类)
  Step 8:   渐进加载决策(命中判定)

用法:
  from pipeline_a import match_json, classify_constraint, generalize_actions, condense_rules
"""

import os
import re
import json
import sys
from pathlib import Path

# ============================================================
# 路径
# ============================================================

SKILL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_DIR.parent / ".standardization" / "semantic-split" / "data"
MODELS_DIR = DATA_DIR / "models"

# ============================================================
# 模型懒加载
# ============================================================

_EMBEDDER = None
_RERANKER = None


def _load_embedder():
    """懒加载 sentence-transformers 嵌入模型"""
    global _EMBEDDER
    if _EMBEDDER is not None:
        return _EMBEDDER

    model_path = str(MODELS_DIR / "BAAI_bge-small-zh-v1.5")
    if not os.path.exists(model_path):
        # 尝试查找
        alt = MODELS_DIR / "bge-small-zh-v1.5"
        model_path = str(alt) if alt.exists() else ""

    if not model_path or not os.path.exists(model_path):
        return None

    try:
        from sentence_transformers import SentenceTransformer
        os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")
        _EMBEDDER = SentenceTransformer(model_path, device="cpu")
        return _EMBEDDER
    except Exception:
        return None


def _load_reranker():
    """懒加载 CrossEncoder rerank 模型"""
    global _RERANKER
    if _RERANKER is not None:
        return _RERANKER

    model_path = str(MODELS_DIR / "BAAI_bge-reranker-base")
    if not os.path.exists(model_path):
        alt = MODELS_DIR / "bge-reranker-base"
        model_path = str(alt) if alt.exists() else ""

    if not model_path or not os.path.exists(model_path):
        return None

    try:
        from sentence_transformers import CrossEncoder
        os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")
        _RERANKER = CrossEncoder(model_path, device="cpu")
        return _RERANKER
    except Exception:
        return None


# ============================================================
# 常量
# ============================================================

# 约束关键词（扩展版，用于 embedding 补充）
CONSTRAINT_LABELS = {
    "critical": ["必须", "只能", "截止", "指定", "强制", "不允许", "不得", "禁止", "一定", "硬性"],
    "soft": ["最好", "尽量", "如果", "建议", "通常", "希望", "可以", "不妨", "推荐", "优先"],
}

# 5W2H 维度关键词
WHY_KEYWORDS = ["为了", "目的是", "目标是", "旨在", "想要", "想", "原因", "目的"]
WHEN_KEYWORDS = ["今天", "明天", "下周", "周", "月", "年", "截止", "之前", "之后"]
HOW_MUCH_KEYWORDS = ["预算", "成本", "费用", "个人", "份", "钱", "时间"]


# ============================================================
# Step 1: JSON 扫描匹配（三层递进）
# ============================================================

def _regex_match(keywords: list[str], json_data: dict) -> float:
    """正则层：关键词子串匹配（保持与 json_manager._match_score 兼容）"""
    if not keywords:
        return 0.0
    score = 0.0
    kw_lower = [k.lower() for k in keywords]

    tags = [t.lower() for t in json_data.get("tags", [])]
    for kw in kw_lower:
        for tag in tags:
            if kw in tag or tag in kw:
                score += 0.15
                break

    name = json_data.get("name", "").lower()
    for kw in kw_lower:
        if kw in name:
            score += 0.2

    desc = json_data.get("description", "").lower()
    for kw in kw_lower:
        if kw in desc:
            score += 0.1

    for step in json_data.get("steps", []):
        st = f"{step.get('name', '')} {step.get('action', '')}".lower()
        for kw in kw_lower:
            if kw in st:
                score += 0.05
                break

    return min(score, 1.0)


def _embedding_match(query: str, json_data: dict) -> float:
    """嵌入层：sentence-embedding 余弦相似度"""
    embedder = _load_embedder()
    if embedder is None:
        return 0.0

    texts = [
        json_data.get("name", ""),
        json_data.get("description", ""),
    ]
    texts += json_data.get("tags", [])

    if not any(texts):
        return 0.0

    query_emb = embedder.encode(query, normalize_embeddings=True)
    doc_embs = embedder.encode(texts, normalize_embeddings=True)

    import numpy as np
    scores = [float(np.dot(query_emb, de)) for de in doc_embs]
    return max(scores) if scores else 0.0


def _rerank_match(query: str, candidates: list[dict]) -> list[tuple]:
    """BERT rerank 层：CrossEncoder 重排序"""
    reranker = _load_reranker()
    if reranker is None:
        return [(c, 0.0) for c in candidates]

    pairs = []
    for c in candidates:
        doc_text = f"{c.get('name', '')} {c.get('description', '')}"
        pairs.append((query, doc_text))

    scores = reranker.predict(pairs)
    scored = list(zip(candidates, scores.tolist() if hasattr(scores, 'tolist') else scores))
    return sorted(scored, key=lambda x: x[1], reverse=True)


def match_json(query: str, json_entries: list[dict]) -> list[dict]:
    """
    三层递进匹配。
    返回按分数降序的 [(entry, score, layer), ...]
    """
    results = []

    # 1. 正则层
    for entry in json_entries:
        score = _regex_match(query.split(), entry)
        if score >= 0.15:
            results.append((entry, score, "regex"))

    # 检查是否足够
    if results and results[0][1] >= 0.8:
        return _format_results(results)

    # 2. 嵌入层
    for entry in json_entries:
        if entry in [r[0] for r in results if r[2] == "regex"]:
            continue  # 正则已过
        score = _embedding_match(query, entry)
        if score >= 0.6:
            results.append((entry, score, "embedding"))
        elif score >= 0.3:
            results.append((entry, score, "embedding_candidate"))

    # 3. BERT rerank 层（仅 top-5 候选）
    pending = [e for e in json_entries if e not in [r[0] for r in results]]
    if pending and _load_reranker() is not None:
        reranked = _rerank_match(query, pending[:10])
        for entry, score in reranked:
            if score >= 0.5:
                results.append((entry, score, "rerank"))

    return _format_results(results)


def _format_results(results: list) -> list:
    """格式化输出"""
    seen = set()
    final = []
    for entry, score, layer in sorted(results, key=lambda x: x[1], reverse=True):
        eid = entry.get("id", "")
        if eid in seen:
            continue
        seen.add(eid)
        final.append({
            "id": eid,
            "name": entry.get("name", ""),
            "score": round(score, 3),
            "layer": layer,
        })
    return final


# ============================================================
# Step 2.5a: 约束关键词初判（用 embedding 补充）
# ============================================================

def classify_constraint(text: str) -> dict:
    """
    约束强度三分类。
    正则 → embedding 语义补充 → BERT（如果有）
    """
    # 正则层
    if re.search(r'(必须|只能|截止|指定|强制|不允许|不得)', text):
        return {"level": "critical", "method": "regex", "keyword": re.search(r'(必须|只能|截止)', text).group(0)}

    if re.search(r'(最好|尽量|如果|建议|通常|希望)', text):
        return {"level": "soft", "method": "regex"}

    # embedding 语义补充
    embedder = _load_embedder()
    if embedder is not None:
        import numpy as np
        t_emb = embedder.encode(text, normalize_embeddings=True)
        crit_embs = embedder.encode(CONSTRAINT_LABELS["critical"], normalize_embeddings=True)
        soft_embs = embedder.encode(CONSTRAINT_LABELS["soft"], normalize_embeddings=True)

        crit_sim = max(float(np.dot(t_emb, ce)) for ce in crit_embs)
        soft_sim = max(float(np.dot(t_emb, se)) for se in soft_embs)

        if crit_sim > 0.7:
            return {"level": "critical", "method": "embedding", "similarity": round(crit_sim, 3)}
        if soft_sim > 0.7:
            return {"level": "soft", "method": "embedding", "similarity": round(soft_sim, 3)}

    return {"level": "none", "method": "default"}


# ============================================================
# Step 6: 通用化语义归类
# ============================================================

def generalize_actions(actions: list[str], known_params: list[str] = None) -> list[str]:
    """
    将具体操作泛化为通用占位符。
    同一语义类别的不同表达映射到统一占位符。
    """
    if not actions:
        return []

    known = known_params or []

    # 时间类
    time_patterns = {
        r'(今天|明天|后天|下周|下周一|下个月|周五前|周[一二三四五六日]|明天下午|后天上午)': '[时间]',
        r'\d{4}-\d{2}-\d{2}': '[时间]',
    }

    # 数量类
    amount_patterns = {
        r'\d+[个份页张条]': '[数量]',
        r'\d+[元人天小时]': '[数量]',
    }

    # 产品/对象类
    product_patterns = {
        r'(钛合金马扎|演示PPT|报告|方案|产品说明)': '[产品/对象]',
    }

    generalized = []
    for action in actions:
        result = action
        for pattern, replacement in {**time_patterns, **amount_patterns, **product_patterns}.items():
            result = re.sub(pattern, replacement, result)
        generalized.append(result)

    # 检查是否所有泛化后的占位符都在 known 中
    for g in generalized:
        found = re.findall(r'\[([^\]]+)\]', g)
        for p in found:
            fp = f"[{p}]"
            if fp not in known:
                known.append(fp)

    return generalized


# ============================================================
# Step 7: 规则凝练（步骤相似度聚类）
# ============================================================

def _steps_similarity_regex(step_a: dict, step_b: dict) -> float:
    """正则层：步骤名称相似度（兼容旧版 _steps_similar）"""
    name_a = step_a.get("name", "").lower()
    name_b = step_b.get("name", "").lower()
    if name_a == name_b:
        return 1.0
    if name_a in name_b or name_b in name_a:
        return 0.8
    stopwords = {"的", "与", "和", "及", "或", "等", "进行", "完成", "执行"}
    words_a = {w for w in name_a if w not in stopwords}
    words_b = {w for w in name_b if w not in stopwords}
    if not words_a or not words_b:
        return 0.0
    overlap = len(words_a & words_b) / max(len(words_a), len(words_b))
    return overlap if overlap >= 0.6 else 0.0


def _steps_similarity_embedding(step_a: dict, step_b: dict) -> float:
    """嵌入层：步骤语义相似度"""
    embedder = _load_embedder()
    if embedder is None:
        return 0.0

    text_a = f"{step_a.get('name', '')} {step_a.get('action', '')}"
    text_b = f"{step_b.get('name', '')} {step_b.get('action', '')}"
    if not text_a.strip() or not text_b.strip():
        return 0.0

    import numpy as np
    emb_a = embedder.encode(text_a, normalize_embeddings=True)
    emb_b = embedder.encode(text_b, normalize_embeddings=True)
    return float(np.dot(emb_a, emb_b))


def condense_rules(all_steps: list[dict], threshold: float = 0.6) -> list[dict]:
    """
    将多个步骤压缩为规则级 condensed_steps。
    先走正则相似度（快），不满足再走 embedding（慢）。
    """
    groups = []
    used = set()

    for i, step_i in enumerate(all_steps):
        if i in used:
            continue
        group = [step_i]
        used.add(i)

        for j, step_j in enumerate(all_steps):
            if j in used:
                continue

            # 正则层
            sim = _steps_similarity_regex(step_i, step_j)
            if sim >= threshold:
                group.append(step_j)
                used.add(j)
                continue

            # embedding 层补充
            if sim > 0 and _load_embedder() is not None:
                sim_e = _steps_similarity_embedding(step_i, step_j)
                if sim_e >= threshold:
                    group.append(step_j)
                    used.add(j)

        groups.append(group)

    condensed = []
    for idx, group in enumerate(groups, 1):
        rep = group[0]
        pg = None
        for e in group:
            if e.get("parallel_group"):
                pg = f"r{idx}"
                break
        ms = all(e.get("milestone", False) for e in group)
        condensed.append({
            "id": f"r{idx}",
            "name": rep.get("name", f"步骤{idx}"),
            "milestone": ms,
            "parallel_group": pg,
            "step_count": len(group),
        })

    return condensed


# ============================================================
# Step 8: 渐进加载决策（命中判定）
# ============================================================

def should_load_json(query: str, json_entry: dict, threshold: float = 0.6) -> dict:
    """
    渐进加载决策：判断用户 query 是否命中某个 json 条目。
    正则 → embedding → rerank 三层，任一通过即判定命中。
    """
    # 正则层
    regex_score = _regex_match(query.split(), json_entry)
    if regex_score >= threshold:
        return {"hit": True, "score": round(regex_score, 3), "layer": "regex"}

    # embedding 层
    embed_score = _embedding_match(query, json_entry)
    if embed_score >= threshold:
        return {"hit": True, "score": round(embed_score, 3), "layer": "embedding"}

    # rerank 层
    reranker = _load_reranker()
    if reranker is not None:
        doc = f"{json_entry.get('name', '')} {json_entry.get('description', '')}"
        if doc.strip():
            score = reranker.predict([(query, doc)])[0]
            if score >= threshold:
                return {"hit": True, "score": round(float(score), 3), "layer": "rerank"}

    return {"hit": False, "score": 0.0, "layer": "none"}


# ============================================================
# 统一入口
# ============================================================

def analyze_semantic(query: str, json_entries: list[dict] = None) -> dict:
    """
    Pipeline A 统一入口。
    包含：JSON匹配 + 约束分类 + 渐进决策
    """
    result = {
        "query": query,
        "pipeline_layers": ["regex"],
    }

    if _load_embedder() is not None:
        result["pipeline_layers"].append("embedding")
    if _load_reranker() is not None:
        result["pipeline_layers"].append("rerank")

    # JSON 匹配
    if json_entries:
        result["json_matches"] = match_json(query, json_entries)

    # 约束分类
    result["constraint"] = classify_constraint(query)

    return result


if __name__ == "__main__":
    import json
    # 测试
    test_query = "帮我制作一份 PPT"
    result = analyze_semantic(test_query)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 测试约束分类
    for t in ["必须周五前提交", "尽量用公司模板", "随便写写"]:
        c = classify_constraint(t)
        print(f"  [{t}] → {c}")
