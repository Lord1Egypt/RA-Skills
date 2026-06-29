#!/usr/bin/env python3
"""
simple_embedder.py - 轻量标题向量匹配器

替代 `_llm_match_proposal_headings()` 中的 LLM 调用。
使用 BAAI/bge-small-zh（33MB 本地模型，纯 CPU），余弦相似度做标题匹配。
零依赖外部服务，只依赖 sentence-transformers。

用法：
  from simple_embedder import TitleMatcher

  matches = TitleMatcher.match_headings(
      ["1.1 研究背景", "2.3 竞争对手分析"],
      [{"id":"1.1","title":"研究背景"}, {"id":"2.3","title":"竞争格局"}],
      threshold=0.75
  )
  # [("1.1", "1.1 研究背景", 0.92), ("2.3", "2.3 竞争对手分析", 0.88)]
"""

import logging
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# 尝试导入 sentence-transformers（可选依赖）
try:
    import numpy as np
    from numpy.linalg import norm

    _SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    _SENTENCE_TRANSFORMERS_AVAILABLE = False


class TitleMatcher:
    """
    标题向量匹配器。

    类变量：
      _model: 单例模式，全局只加载一次模型
      _dim:   向量维度（bge-small-zh = 512）
    """
    _model = None
    _dim = 512

    # ── 标题归一化规则 ──────────────────────────────────
    # 匹配前对标题做标准化：去掉编号、去掉常见前缀
    _NORM_RULES = [
        (r'^\d+\.\d+\.\d+\s*', ''),    # 1.1.1
        (r'^\d+\.\d+\s+', ''),          # 1.1
        (r'^第[一二三四五六七八九十\d]+章\s*', ''),  # 第1章 / 第一章
        (r'^第[一二三四五六七八九十\d]+节\s*', ''),  # 第1节 / 第一节
        (r'^附录[ABCDEF\d]?\s*', '附录'),
        (r'^参考文献\s*', '参考文献'),
        (r'^致谢\s*', '致谢'),
    ]

    @classmethod
    def _normalize_title(cls, title: str) -> str:
        """去掉编号前缀，保留核心标题内容"""
        import re
        t = title.strip()
        for regex, replace in cls._NORM_RULES:
            t = re.sub(regex, replace, t)
        return t.strip()

    @classmethod
    def _load_model(cls):
        """加载 BGE-small-zh 模型（单例，全局只加载一次）"""
        if cls._model is not None:
            return

        # HuggingFace 国内访问策略：
        #   1. 有缓存 → 设 HF_HUB_OFFLINE=1 直接加载（避免连接验证的超时）
        #   2. 无缓存 → 设 HF_ENDPOINT 走镜像下载
        import os
        import glob

        cache_dir = os.path.expanduser("~/.cache/huggingface/hub/models--BAAI--bge-small-zh")
        has_cache = os.path.isdir(cache_dir) and len(glob.glob(f"{cache_dir}/snapshots/*")) > 0

        if has_cache:
            os.environ.setdefault("HF_HUB_OFFLINE", "1")
        else:
            os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")

        try:
            from sentence_transformers import SentenceTransformer
            cls._model = SentenceTransformer('BAAI/bge-small-zh')
            cls._dim = 512
            logger.info("BGE-small-zh loaded (dim=%d, cache=%s)", cls._dim, "yes" if has_cache else "no")
        except Exception as e:
            logger.warning("Failed to load BGE-small-zh: %s", e)
            raise

    @classmethod
    def is_available(cls) -> bool:
        """检查是否可用（依赖 + 模型加载）"""
        if not _SENTENCE_TRANSFORMERS_AVAILABLE:
            return False
        try:
            cls._load_model()
            return cls._model is not None
        except Exception:
            return False

    @classmethod
    def encode(cls, texts: List[str]):
        """
        编码文本为归一化向量。

        参数：
          texts: 文本列表
        返回：
          numpy array, shape (n, 512)，L2 归一化
        """
        cls._load_model()
        import numpy as np
        embeddings = cls._model.encode(texts, normalize_embeddings=True)
        return np.array(embeddings, dtype=np.float32)

    @classmethod
    def match_headings(
        cls,
        proposal_headings: List[str],
        outline_nodes: List[Dict],
        threshold: float = 0.75,
        normalize_titles: bool = True,
    ) -> List[Tuple[str, str, float]]:
        """
        对每个开题报告标题，在 outline 节点中找到最相似节点。

        参数：
          proposal_headings: 开题报告标题列表，如 ["1.1 研究背景", "第一章 绪论"]
          outline_nodes    : outline 节点列表，如 [{"id":"1.1","title":"研究背景"}]
          threshold        : 余弦相似度阈值，>= 此值视为匹配成功
          normalize_titles : 是否去掉编号前缀后再编码（默认 True，提高匹配准确率）

        返回：
          [(node_id, heading_text, score), ...]
          按 score 降序排列（最匹配的在前）
        """
        if not proposal_headings or not outline_nodes:
            return []

        cls._load_model()

        import numpy as np

        # 准备标题文本
        if normalize_titles:
            headings_for_encode = [cls._normalize_title(h) for h in proposal_headings]
            node_titles_for_encode = [cls._normalize_title(n.get("title", "")) for n in outline_nodes]
        else:
            headings_for_encode = proposal_headings
            node_titles_for_encode = [n.get("title", "") for n in outline_nodes]

        # 编码
        heading_vecs = cls.encode(headings_for_encode)   # (M, 512), L2归一化
        node_vecs = cls.encode(node_titles_for_encode)   # (N, 512), L2归一化

        # 余弦相似度矩阵（归一化向量点积 = 余弦相似度）
        sim_matrix = heading_vecs @ node_vecs.T          # (M, N)

        results: List[Tuple[str, str, float]] = []
        for i, heading_text in enumerate(proposal_headings):
            best_idx = int(np.argmax(sim_matrix[i]))
            best_score = float(sim_matrix[i][best_idx])

            if threshold <= best_score <= 1.0:
                results.append((
                    outline_nodes[best_idx]["id"],
                    heading_text,
                    best_score,
                ))

        # 按 score 降序
        results.sort(key=lambda x: x[2], reverse=True)
        return results


# ── 快速测试 ──────────────────────────────────

if __name__ == "__main__":
    import json
    import sys

    if not _SENTENCE_TRANSFORMERS_AVAILABLE:
        print("❌ sentence-transformers 未安装。请执行: pip install sentence-transformers")
        sys.exit(1)

    available = TitleMatcher.is_available()
    print(f"TitleMatcher available: {available}")

    if not available:
        sys.exit(1)

    # 测试用例
    headings = [
        "第一章 绪论",
        "1.2 研究目的与意义",
        "2.3 竞争对手分析",
        "3.4 SWOT分析",
    ]
    nodes = [
        {"id": "1", "title": "绪论"},
        {"id": "1.1", "title": "研究背景"},
        {"id": "1.2", "title": "研究目的与意义"},
        {"id": "2.3", "title": "竞争格局"},
        {"id": "3.4", "title": "SWOT分析"},
    ]

    matches = TitleMatcher.match_headings(headings, nodes, threshold=0.6)
    print(f"\n测试：匹配结果 ({len(matches)} 条)")
    for node_id, heading, score in matches:
        print(f"  {heading} → [{node_id}] (score={score:.3f})")
