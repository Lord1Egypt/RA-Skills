# -*- coding: utf-8 -*-
"""
本地零密钥「语义」向量 —— 不依赖任何模型 / API Key / 联网。

做法（纯标准库实现，适合个人规模数据，且极其省资源）：
  1. 中文：按「字 unigram + 字 bigram」切分。例：「机器学习」-> 机,器,学,习,机器,器学,学习
     —— 即使表述不同（"学机器" vs "机器学习"）也能共享大量 token，获得语义近似召回。
  2. 英文/数字：按非中文字符边界切成词，转小写。
  3. 过滤标点、停用词、纯空白。
  4. 文档向量 = TF（词频）；检索时结合语料 IDF 计算 TF-IDF 余弦相似度。

这是「轻量语义检索」而非大模型嵌入，但与「不拖累电脑 + 不用密钥」的约束完全契合。
如需更强语义，可在 config 中挂接外部嵌入适配器（可插拔，不影响默认路径）。
"""

from __future__ import annotations

import re
import math
from collections import Counter

# 常见中文停用词（精简版，避免噪声）
_STOP = set(
    "的了着过和是与在也我都你他会她它这那有个们把被让给从对在到上中下"
    "并把或但如因为所以而且而则等又就很再更最之后之前当时当虽然但可是"
    "吧呢啊嘛哟哦啦嘞呃这个那个怎么什么哪些为什么如何怎样是否可以能否"
    "we you they he she it the a an and or but if of to in on for is are was"
    "be do does did has have had not no yes this that these those i my your"
)

# 中文（含中日韩统一表意文字）范围
_CJK = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf]")
_NON_CJK_SPLIT = re.compile(r"[^a-z0-9\u4e00-\u9fff\u3400-\u4dbf]+")


def is_cjk(ch: str) -> bool:
    return bool(_CJK.match(ch))


def tokenize(text: str) -> list[str]:
    """把文本切成 token 列表（中文 char/bigram + 英文词）。"""
    if not text:
        return []
    text = text.lower()
    tokens: list[str] = []

    # 1) 中文片段：逐字 + 相邻 bigram
    cjk_runs = re.findall(r"[\u4e00-\u9fff\u3400-\u4dbf]+", text)
    for run in cjk_runs:
        for ch in run:
            if ch not in _STOP:
                tokens.append(ch)
        for i in range(len(run) - 1):
            bg = run[i] + run[i + 1]
            if bg[0] not in _STOP and bg[1] not in _STOP:
                tokens.append(bg)

    # 2) 非中文片段：按空白/标点切词
    for seg in _NON_CJK_SPLIT.split(text):
        seg = seg.strip()
        if not seg:
            continue
        # 只保留含字母或数字的片段
        if re.search(r"[a-z0-9]", seg):
            if len(seg) >= 2 and not seg.isdigit():
                tokens.append(seg)

    return tokens


def tf_vector(tokens: list[str]) -> Counter:
    return Counter(tokens)


def normalize_vec(vec: Counter) -> Counter:
    """L2 归一化（原地返回新 Counter）。"""
    norm = math.sqrt(sum(v * v for v in vec.values()))
    if norm == 0:
        return Counter()
    return Counter({k: v / norm for k, v in vec.items()})


def cosine(a: Counter, b: Counter) -> float:
    if not a or not b:
        return 0.0
    # 用小字典迭代
    if len(a) <= len(b):
        small, big = a, b
    else:
        small, big = b, a
    dot = sum(v * big.get(k, 0.0) for k, v in small.items())
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def norm_hash(tokens: list[str]) -> str:
    """去重指纹：对 token 排序后哈希（忽略顺序，只看内容集合）。"""
    import hashlib
    key = "|".join(sorted(set(tokens)))
    return hashlib.md5(key.encode("utf-8")).hexdigest()


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def build_idf(memory_tokens: list[tuple[int, list[str]]]) -> dict[str, float]:
    """从语料构建 IDF。返回 {token: idf}。"""
    df: Counter = Counter()
    n_docs = 0
    for _mid, toks in memory_tokens:
        if not toks:
            continue
        n_docs += 1
        for t in set(toks):
            df[t] += 1
    idf = {}
    for t, c in df.items():
        idf[t] = math.log((n_docs + 1) / (c + 1)) + 1.0
    return idf


def tfidf_query(tokens: list[str], idf: dict[str, float]) -> Counter:
    """查询文本 -> TF-IDF 向量（对已见 token 加权，未见 token 用默认 IDF=1）。"""
    tf = Counter(tokens)
    vec = Counter()
    for t, f in tf.items():
        w = idf.get(t, 1.0)
        vec[t] = (1.0 + math.log(1.0 + f)) * w
    return vec


if __name__ == "__main__":
    s1 = tokenize("机器学习需要大量数据和算力")
    s2 = tokenize("学机器要用很多数据")
    v1, v2 = normalize_vec(tf_vector(s1)), normalize_vec(tf_vector(s2))
    print("jaccard:", round(jaccard(set(s1), set(s2)), 3))
    print("cosine :", round(cosine(v1, v2), 3))
