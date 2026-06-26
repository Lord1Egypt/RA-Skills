#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QoderWork 专用：场景库向量检索脚本
仅负责检索，不做对话生成（对话由 QoderWork LLM 完成）

用法：
    python3 search_scenarios.py "用户的问题" [top_k]

输出：JSON 格式的匹配场景列表
"""

import sys
import json
import warnings
import os
import numpy as np
from pathlib import Path

# 静默 sklearn/numpy 数值警告
warnings.filterwarnings("ignore", category=RuntimeWarning)

# 环境设置：禁止模型下载尝试
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_HUB_OFFLINE"] = "1"

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# 路径配置
SKILL_DIR = Path(__file__).parent
DATA_DIR = SKILL_DIR / "data"
SRC_DIR = SKILL_DIR / "src"

# 添加 src 到路径
sys.path.insert(0, str(SRC_DIR))
from encrypt import EncryptManager

MODEL_NAME = "shibing624/text2vec-base-chinese"


def load_scenarios():
    """加载并解密场景库"""
    enc_file = DATA_DIR / "scenario_library.json.enc"
    manager = EncryptManager()
    with open(enc_file, "r", encoding="utf-8") as f:
        return json.loads(manager.decrypt_data(f.read()))


def search(query: str, top_k: int = 20):
    """
    执行向量检索，返回最相关的场景

    Args:
        query: 用户问题
        top_k: 返回条数

    Returns:
        list[dict]: 匹配的场景（含相似度分数）
    """
    # 加载数据
    scenarios = load_scenarios()
    embeddings = np.load(DATA_DIR / "scenario_embeddings.npy")

    # 加载模型并编码查询
    model = SentenceTransformer(MODEL_NAME)
    query_emb = model.encode([query], show_progress_bar=False)

    # 计算余弦相似度
    sims = cosine_similarity(query_emb, embeddings)[0]

    # 取候选（多取一些用于去重）
    candidate_idx = np.argsort(sims)[::-1][: top_k * 3]

    # 去重：按「用户具体场景 + 任务 + 痛点 + 底层需求」内容去重
    seen = set()
    results = []
    for idx in candidate_idx:
        s = scenarios[idx]
        dedup_key = (
            s.get("用户具体场景", ""),
            s.get("任务", ""),
            s.get("痛点", ""),
            s.get("底层需求", ""),
        )
        if dedup_key in seen:
            continue
        seen.add(dedup_key)

        item = s.copy()
        item["similarity_score"] = round(float(sims[idx]), 4)
        results.append(item)

        if len(results) >= top_k:
            break

    return results


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "用法: python3 search_scenarios.py \"查询问题\" [top_k]"}, ensure_ascii=False))
        sys.exit(1)

    query = sys.argv[1]
    top_k = int(sys.argv[2]) if len(sys.argv) > 2 else 20

    # 加载场景库一次（避免重复解密 125MB 文件）
    scenarios = load_scenarios()
    total = len(scenarios)
    embeddings = np.load(DATA_DIR / "scenario_embeddings.npy")

    # 加载模型并编码查询
    model = SentenceTransformer(MODEL_NAME)
    query_emb = model.encode([query], show_progress_bar=False)

    # 计算余弦相似度
    sims = cosine_similarity(query_emb, embeddings)[0]

    # 取候选（多取一些用于去重）
    candidate_idx = np.argsort(sims)[::-1][: top_k * 3]

    # 去重
    seen = set()
    results = []
    for idx in candidate_idx:
        s = scenarios[idx]
        dedup_key = (
            s.get("用户具体场景", ""),
            s.get("任务", ""),
            s.get("痛点", ""),
            s.get("底层需求", ""),
        )
        if dedup_key in seen:
            continue
        seen.add(dedup_key)
        item = s.copy()
        item["similarity_score"] = round(float(sims[idx]), 4)
        results.append(item)
        if len(results) >= top_k:
            break

    # 输出摘要到 stderr
    print(f"[INFO] 场景库 {total:,} 条 | 查询: {query} | 返回 {len(results)} 条", file=sys.stderr)

    # JSON 输出到 stdout
    output = {
        "query": query,
        "total_scenarios": total,
        "returned": len(results),
        "scenarios": results,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
