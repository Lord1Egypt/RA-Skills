#!/usr/bin/env python3
"""
Memory BM25 搜索脚本（效果最佳版 v7）
四路融合 + 同文件去重 + 长词优先匹配 + Dice Coefficient
用法:
  python3 search.py --build     # 构建索引
  python3 search.py "查询内容"  # 搜索
"""

import os
import sys
import glob
import json
import math
import re
from collections import Counter, defaultdict

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
MEMORY_PATHS = [
    f"{WORKSPACE}/MEMORY.md",
    f"{WORKSPACE}/memory/*.md",
]
INDEX_PATH = os.path.expanduser("~/.openclaw/memory_bm25_index.json")
TOKEN_CACHE_PATH = os.path.expanduser("~/.openclaw/memory_bm25_token_cache.json")

# BM25 参数
BM25_K1 = 1.5
BM25_B = 0.75
TOP_K = 8

# 分块参数
CHUNK_SIZE = 400
CHUNK_OVERLAP = 150

# 重排参数
RERANK_TOP_K = 20
POSITION_DECAY = 0.97

# 融合权重
FUSE_BM25 = 0.38
FUSE_COVERAGE = 0.22
FUSE_PROXIMITY = 0.20
FUSE_PHRASE = 0.12
CONSEC_BONUS_MAX = 0.08

# Soft match 参数
SOFT_EDIT_THRESHOLD = 0.70

# 预编译正则
_RE_EN_TOKEN = re.compile(r'^[a-zA-Z0-9_\-\.]+$')
_RE_WHITESPACE = re.compile(r'^\s+$')
_RE_HEADING = re.compile(
    r'^#{1,6}\s+.+|^\*\*[^*]+\*\*$|^\-\-\-$|^第[一二三四五六七八九十百千万\d]+[章节段]'
)


def is_cjk(char):
    cp = ord(char)
    return (
        0x4e00 <= cp <= 0x9fff or
        0x2e80 <= cp <= 0x2eff or
        0x3000 <= cp <= 0x303f or
        0xff00 <= cp <= 0xffef
    )


def tokenize(text, ngram_range=(2, 6)):
    tokens = []
    first_line = text.split('\n')[0] or ''
    heading_hit = bool(_RE_HEADING.search(first_line))

    en_parts = _RE_WHITESPACE.split(text)
    for part in en_parts:
        if _RE_WHITESPACE.match(part):
            continue
        if _RE_EN_TOKEN.match(part):
            tokens.append(part.lower())
        else:
            cjk_chars = [c for c in part if is_cjk(c)]
            for i in range(len(cjk_chars)):
                for n in range(2, ngram_range[1] + 1):
                    if i + n <= len(cjk_chars):
                        tokens.append(''.join(cjk_chars[i:i + n]))
    return tokens, heading_hit


def query_expand_long_first(tokens):
    """
    A. 长词优先匹配：query bigram 扩展，同时按长度降序排列，
    优先匹配最长词（4-6字），减少单字噪声。
    """
    expanded = list(tokens)
    for i in range(len(tokens) - 1):
        bigram = tokens[i] + tokens[i + 1]
        if len(bigram) >= 3:
            expanded.append(bigram)

    # 按长度降序排列（最长在前）
    expanded.sort(key=lambda t: -len(t))
    return expanded


def consecutive_match_score(query_text, doc_text):
    """
    连续匹配加分（Consecutive Match Bonus）：
    在 doc 中找 query 的有序连续子序列。
    """
    if not query_text or not doc_text:
        return 0.0, 0

    query_lower = query_text.lower()
    doc_lower = doc_text.lower()

    # 提取 query 中的词（英文按空格分，中文取2字以上）
    en_parts = _RE_WHITESPACE.split(query_lower)
    query_words = []
    for part in en_parts:
        if _RE_WHITESPACE.match(part):
            continue
        if _RE_EN_TOKEN.match(part):
            query_words.append(part.lower())
        else:
            cjk_chars = [c for c in part if is_cjk(c)]
            if len(cjk_chars) >= 2:
                query_words.append(''.join(cjk_chars))

    if len(query_words) < 2:
        return 0.0, 0

    # 找 doc 中每个 query word 的所有出现位置
    positions = []
    for qw in query_words:
        pos_list = []
        start = 0
        while True:
            idx = doc_lower.find(qw, start)
            if idx == -1:
                break
            pos_list.append(idx)
            start = idx + 1
        positions.append(pos_list if pos_list else [-1])

    # 贪心找最长有序连续匹配
    best_seq_len = 0
    n = len(positions)
    for start_word_idx in range(n):
        for start_pos in positions[start_word_idx]:
            if start_pos == -1:
                continue
            run_len = 1
            current_pos = start_pos
            for k in range(start_word_idx + 1, n):
                found = False
                for p in positions[k]:
                    if p > current_pos:
                        run_len += 1
                        current_pos = p
                        found = True
                        break
                if not found:
                    break
            if run_len > best_seq_len:
                best_seq_len = run_len

    if best_seq_len < 2:
        return 0.0, 0

    score = best_seq_len / n
    return min(score, 1.0), best_seq_len


def edit_distance(s1, s2):
    if len(s1) < len(s2):
        return edit_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    prev = list(range(len(s2) + 1))
    curr = [0] * (len(s2) + 1)
    for i, c1 in enumerate(s1):
        curr[0] = i + 1
        for j, c2 in enumerate(s2):
            cost = 0 if c1 == c2 else 1
            curr[j + 1] = min(prev[j + 1] + 1, curr[j] + 1, prev[j] + cost)
        prev, curr = curr, prev
    return prev[len(s2)]


def soft_match_score(query_text, doc_text):
    """
    D. Soft N-gram Match with Dice Coefficient：
    - 提取 query 和 doc 的 CJK 连续字符序列
    - Dice = 2*|intersection| / (|A| + |B|)，替代 F1
    - 对单个 n-gram 更稳定，不受分母膨胀影响
    """
    def extract_cjk_seqs(text):
        seqs = []
        current = []
        for c in text.lower():
            if is_cjk(c):
                current.append(c)
            elif current:
                seqs.append(''.join(current))
                current = []
        if current:
            seqs.append(''.join(current))
        return seqs

    query_lower = query_text.lower()
    doc_lower = doc_text.lower()
    query_seqs = [s for s in extract_cjk_seqs(query_lower) if len(s) >= 2]
    doc_seqs = set(extract_cjk_seqs(doc_lower))

    if not query_seqs or not doc_seqs:
        return 0.0, 0, 0

    matched_count = 0
    total_dice_score = 0.0

    for qs in query_seqs:
        qlen = len(qs)
        best_sim = 0.0
        best_ds = ''
        for ds in doc_seqs:
            if abs(len(ds) - qlen) > max(qlen, len(ds)) * 0.35:
                continue
            ed = edit_distance(qs, ds)
            max_len = max(qlen, len(ds))
            sim = 1.0 - (ed / max_len) if max_len > 0 else 0
            if sim > best_sim:
                best_sim = sim
                best_ds = ds

        if best_sim >= SOFT_EDIT_THRESHOLD:
            matched_count += 1
            # Dice coefficient: 2*|intersection| / (|A| + |B|)
            intersection = 2.0 * min(len(qs), len(best_ds)) * best_sim
            dice = intersection / (len(qs) + len(best_ds)) if (len(qs) + len(best_ds)) > 0 else 0
            total_dice_score += dice

    coverage = matched_count / len(query_seqs) if query_seqs else 0
    # 综合分数：Dice均值 × Coverage
    avg_dice = total_dice_score / matched_count if matched_count > 0 else 0
    score = avg_dice * 0.5 + coverage * 0.5  # Dice 和 Coverage 各占一半
    return min(score, 1.0), matched_count, len(query_seqs)


def exact_phrase_match(query_text, doc_text):
    query_clean = re.sub(r'\s+', '', query_text.lower())
    doc_lower = doc_text.lower()
    if len(query_clean) < 2:
        return 0.0, -1
    pos = doc_lower.find(query_clean)
    if pos != -1:
        return min(1.0 - (pos / max(len(doc_lower), 1)) * 0.3, 1.0), pos
    return 0.0, -1


def ngram_proximity(query_text, doc_text):
    """
    N-gram Proximity：使用长词优先的 query n-gram（已排序）。
    """
    if not query_text or not doc_text:
        return 0.0, 0.0, []
    doc_lower = doc_text.lower()
    query_lower = query_text.lower()

    # 生成 query n-gram（2-6字，仅 CJK），按长度降序
    query_ngrams = []
    for i in range(len(query_lower)):
        for n in range(2, min(7, len(query_lower) - i + 1)):
            if i + n <= len(query_lower):
                ng = query_lower[i:i + n]
                if len([c for c in ng if is_cjk(c)]) == n:
                    query_ngrams.append(ng)

    if not query_ngrams:
        return 0.0, 0.0, []

    # A: 长词优先，去重（最长在前）
    unique_ngrams = list(dict.fromkeys(query_ngrams))
    unique_ngrams.sort(key=lambda t: -len(t))

    matched = []
    exact_bonus = 0.0

    for ng in unique_ngrams:
        pos = doc_lower.find(ng)
        if pos != -1:
            is_exact = len(ng) >= 4
            matched.append((pos, len(ng), is_exact))
            if is_exact:
                exact_bonus += 0.1 * (len(ng) - 3)

    if not matched:
        return 0.0, 0.0, []

    positions = [p for p, _, _ in matched]
    span = max(max(positions) - min(positions), 1)
    coverage_ratio = len(matched) / len(unique_ngrams)
    span_score = coverage_ratio / (span ** 0.25)
    proximity = min(span_score / max(len(matched), 1), 1.0)
    exact_bonus = min(exact_bonus, 0.5)

    return proximity, exact_bonus, [ng for ng, _, _ in matched]


def get_all_files():
    files = []
    for pattern in MEMORY_PATHS:
        files.extend(glob.glob(pattern, recursive=True))
    return [f for f in files if os.path.isfile(f)]


def chunk_file(filepath, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return []
    chunks = []
    lines = content.split('\n')
    i = 0
    while i < len(lines):
        current_lines = []
        current_size = 0
        chunk_start = i
        while i < len(lines) and current_size < chunk_size:
            current_lines.append(lines[i])
            current_size += len(lines[i])
            i += 1
        if chunks:
            overlap_start = max(chunk_start, i - overlap // 2)
            current_lines = lines[overlap_start:i] + current_lines
        text = '\n'.join(current_lines).strip()
        if text:
            chunks.append({
                'text': text,
                'file': filepath,
                'start_line': chunk_start + 1,
                'end_line': i,
                'chunk_idx': len(chunks),
            })
        if i == chunk_start:
            i += 1
    return chunks


def get_all_terms(chunks):
    N = len(chunks)
    doc_freqs = defaultdict(int)
    avg_dl = 0
    for chunk in chunks:
        terms = chunk['terms']
        unique_terms = set(terms)
        for t in unique_terms:
            doc_freqs[t] += 1
        avg_dl += len(terms)
    avg_dl = avg_dl / N if N > 0 else 0
    return N, doc_freqs, avg_dl


def bm25_score(query_terms, doc_tf, N, doc_freqs, avg_dl):
    score = 0.0
    doc_len = sum(doc_tf.values())
    for term in query_terms:
        if term not in doc_tf:
            continue
        tf = doc_tf[term]
        df = doc_freqs.get(term, 0)
        if df == 0:
            continue
        idf = math.log((N - df + 0.5) / (df + 0.5) + 1)
        tf_component = (tf * (BM25_K1 + 1)) / (tf + BM25_K1 * (1 - BM25_B + BM25_B * doc_len / avg_dl))
        score += idf * tf_component
    return score


def idf_coverage(query_set, doc_set, doc_freqs, N):
    if not query_set:
        return 0.0
    idf_sum_all = sum(
        math.log((N - doc_freqs.get(t, 0) + 0.5) / (doc_freqs.get(t, 0) + 0.5) + 1)
        for t in query_set
    )
    if idf_sum_all == 0:
        return 0.0
    matched = query_set & doc_set
    idf_sum_matched = sum(
        math.log((N - doc_freqs.get(t, 0) + 0.5) / (doc_freqs.get(t, 0) + 0.5) + 1)
        for t in matched
    )
    return idf_sum_matched / idf_sum_all


def build_index():
    print("构建记忆索引（效果最佳版 v7）...")

    files = get_all_files()
    print(f"找到 {len(files)} 个文件")

    chunks = []
    for f in files:
        file_chunks = chunk_file(f)
        chunks.extend(file_chunks)

    print(f"共 {len(chunks)} 个文本块（含重叠）")

    print("分词中...")
    token_cache = {}
    for i, chunk in enumerate(chunks):
        key = (chunk['file'], chunk['start_line'])
        if key not in token_cache:
            terms, heading_hit = tokenize(chunk['text'])
            token_cache[key] = (terms, heading_hit)
        else:
            terms, heading_hit = token_cache[key]
        chunks[i]['terms'] = terms
        chunks[i]['heading_hit'] = heading_hit
        if (i + 1) % 20 == 0:
            print(f"  已处理 {i + 1}/{len(chunks)} 块")

    with open(TOKEN_CACHE_PATH, 'w', encoding='utf-8') as f:
        json.dump({f"{k[0]}|||{k[1]}": v for k, v in token_cache.items()}, f, ensure_ascii=False)

    N, doc_freqs, avg_dl = get_all_terms(chunks)

    index = []
    for chunk in chunks:
        term_freqs = Counter(chunk['terms'])
        index.append({
            'text': chunk['text'],
            'file': chunk['file'],
            'start_line': chunk['start_line'],
            'end_line': chunk['end_line'],
            'chunk_idx': chunk['chunk_idx'],
            'heading_hit': chunk['heading_hit'],
            'tf': dict(term_freqs),
            'terms_set': list(set(chunk['terms'])),
        })

    data = {
        'N': N,
        'doc_freqs': dict(doc_freqs),
        'avg_dl': avg_dl,
        'chunks': index,
    }

    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

    size_mb = os.path.getsize(INDEX_PATH) / 1024 / 1024
    print(f"索引构建完成！保存到 {INDEX_PATH}（{size_mb:.1f} MB）")


def search(query, top_k=TOP_K):
    if not os.path.exists(INDEX_PATH):
        print("索引不存在，请先运行: python3 search.py --build")
        return []

    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    N = data['N']
    doc_freqs = data['doc_freqs']
    avg_dl = data['avg_dl']
    chunks = data['chunks']

    query_terms, _ = tokenize(query)
    query_terms = [t for t in query_terms if len(t) > 1]
    # A: 长词优先扩展 + 排序
    query_terms = query_expand_long_first(query_terms)
    query_set = set(query_terms)

    # ========== 第一阶段：BM25 + 多维加权 ==========
    raw_scores = []
    candidates = []
    for item in chunks:
        raw_bm = bm25_score(query_terms, item['tf'], N, doc_freqs, avg_dl)
        raw_scores.append(raw_bm)

        score = raw_bm * (POSITION_DECAY ** item['chunk_idx'])

        if item.get('heading_hit'):
            score *= 1.5

        filename = os.path.basename(item['file'])
        if filename == 'MEMORY.md':
            score *= 1.3
        elif filename.startswith('MEMORY'):
            score *= 1.15

        candidates.append({
            'text': item['text'],
            'file': item['file'],
            'start_line': item['start_line'],
            'end_line': item['end_line'],
            'score': score,
            'raw_bm25': raw_bm,
            'terms_set': set(item['terms_set']),
        })

    min_s = min(raw_scores) if raw_scores else 0
    max_s = max(raw_scores) if raw_scores else 1
    score_range = max_s - min_s if max_s != min_s else 1

    candidates.sort(key=lambda x: x['score'], reverse=True)
    coarse_results = candidates[:RERANK_TOP_K]

    # ========== 第二阶段：四路融合 + A/D 优化 ==========
    scored_results = []
    for item in coarse_results:
        norm_bm25 = (item['raw_bm25'] - min_s) / score_range if score_range > 0 else 0
        coverage = idf_coverage(query_set, item['terms_set'], doc_freqs, N)
        proximity, exact_bonus, _ = ngram_proximity(query, item['text'])
        phrase_bonus, _ = exact_phrase_match(query, item['text'])
        soft_score, soft_m, soft_total = soft_match_score(query, item['text'])
        consecutive_score, consecutive_run = consecutive_match_score(query, item['text'])

        prox_score = min(proximity + exact_bonus, 1.0)
        phrase_combined = phrase_bonus * 0.6 + soft_score * 0.4
        consecutive_bonus = consecutive_score * CONSEC_BONUS_MAX

        final_score = (
            FUSE_BM25 * norm_bm25 +
            FUSE_COVERAGE * coverage +
            FUSE_PROXIMITY * prox_score +
            FUSE_PHRASE * phrase_combined +
            consecutive_bonus
        )

        if final_score < 0.005:
            continue

        item['final_score'] = final_score
        item['norm_bm25'] = norm_bm25
        item['coverage'] = coverage
        item['proximity'] = prox_score
        item['phrase_bonus'] = phrase_bonus
        item['soft_score'] = soft_score
        item['consecutive_score'] = consecutive_score
        scored_results.append(item)

    scored_results.sort(key=lambda x: x['final_score'], reverse=True)

    # ========== 第三阶段：同文件去重 ==========
    file_best = {}
    for r in scored_results:
        fname = r['file']
        if fname not in file_best:
            file_best[fname] = r
        else:
            r['final_score'] *= 0.6
            r['deduped'] = True

    scored_results.sort(key=lambda x: x['final_score'], reverse=True)
    return scored_results[:top_k]


def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 search.py --build     # 构建索引")
        print("  python3 search.py \"查询内容\"  # 搜索")
        return

    if sys.argv[1] == '--build':
        build_index()
        return

    query = ' '.join(sys.argv[1:])
    results = search(query)

    if not results:
        print("未找到相关记忆")
        return

    print(f"\n🔍 搜索: {query}\n")
    print("=" * 60)

    for i, r in enumerate(results):
        rel_path = r['file'].replace(WORKSPACE + '/', '')
        dup_tag = " [去重]" if r.get('deduped') else ""
        print(f"\n[{i + 1}] 综合: {r['final_score']:.3f}{dup_tag}")
        print(f"    BM25n: {r.get('norm_bm25', 0):.3f}  Cover: {r.get('coverage', 0):.3f}  Prox: {r.get('proximity', 0):.3f}  Phrase: {r.get('phrase_bonus', 0):.3f}  Soft: {r.get('soft_score', 0):.3f}  Consec: {r.get('consecutive_score', 0):.3f}")
        print(f"    来源: {rel_path}#{r['start_line']}-{r['end_line']}")
        preview = r['text'][:250].replace('\n', ' ')
        print(f"    内容: {preview}...")


if __name__ == "__main__":
    main()
