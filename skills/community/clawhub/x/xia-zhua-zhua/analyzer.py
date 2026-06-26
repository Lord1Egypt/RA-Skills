#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analyzer.py - 文章自动分析（摘要 + 关键洞察）
使用 TextRank 算法做 extractive summarization，不依赖外部 API

分析维度：
1. 摘要（3-5句）
2. 关键洞察（3-5条）
3. 主题标签
4. 适合读者群体
"""

import sys
import os
import json
import re
import io
import argparse
from collections import Counter

# 修复 Windows 终端 GBK 编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False


STOPWORDS_CN = set('的了是在有和就都不人家还这个进行那么那些如果应该知道开始因此因为所以但是以及对于其他或其然后非常进入关于以及所以与其通过并且或者因为由于与为而却也已被让从到把被给但但已让所把从这那之中向外在向里')
STOPWORDS_EN = set('the a an is are was were be been being have has had do does did will would shall should can could may might must i you he she it we they this that which who what when where how there here all each every some any no nor not only same so than too very just and but or if then because while although though for with about into through during before after above below between under over is was were are been being have has had do does did can could will would shall should may might must')


def tokenize(text):
    """简单分词"""
    text = re.sub(r'[#*`\[\]()>_\-\|]', ' ', text)
    chinese = re.findall(r'[\u4e00-\u9fff]+', text)
    chinese_words = [c for c in ' '.join(chinese) if c not in STOPWORDS_CN]
    english = re.findall(r'[a-zA-Z]{2,}', text.lower())
    english_words = [w for w in english if w not in STOPWORDS_EN]
    return chinese_words + english_words


def split_sentences(text):
    """将文本分割成句子"""
    sents = re.split(r'(?<=[。！？.!?])\s+', text)
    return [s.strip() for s in sents if len(s.strip()) > 10]


def score_sentences_tfidf(sentences, top_n=5):
    """使用 TF-IDF TextRank 找出最重要的句子"""
    if not sentences or len(sentences) < 2:
        return []

    if HAS_SKLEARN:
        try:
            vec = TfidfVectorizer(tokenizer=lambda x: tokenize(x), lowercase=True)
            tfidf = vec.fit_transform(sentences)
            sim_matrix = cosine_similarity(tfidf, tfidf)

            scores = [1.0] * len(sentences)
            damping = 0.85
            for _ in range(50):
                new_scores = []
                for i in range(len(sentences)):
                    sim_sum = sum(sim_matrix[i][j] * scores[j]
                                  for j in range(len(sentences)) if j != i)
                    new_scores.append((1 - damping) + damping * sim_sum)
                scores = new_scores

            ranked = sorted(zip(scores, sentences), reverse=True)
            return [s for _, s in ranked[:top_n]]
        except:
            pass

    # 降级：基于关键词密度
    all_words = ' '.join(sentences)
    keywords = set(tokenize(all_words))
    scored = []
    for sent in sentences:
        words = tokenize(sent)
        if not words:
            scored.append((0, sent))
            continue
        density = sum(1 for w in words if w in keywords) / len(words)
        idx = sentences.index(sent)
        pos_bonus = 1.2 if idx < 3 else (1.1 if idx >= len(sentences) - 2 else 1.0)
        scored.append((density * pos_bonus, sent))

    scored.sort(reverse=True)
    return [s for _, s in scored[:top_n]]


def extract_keywords(text, top_n=5):
    """提取关键词"""
    words = tokenize(text)
    freq = Counter(w for w in words if len(w) >= 2)
    return [w for w, _ in freq.most_common(top_n)]


def extract_insights(sentences):
    """提取关键洞察"""
    insights = []

    # 数据类句子
    number_sents = [s for s in sentences if re.search(r'\d+[万分/百千万亿]+', s)]
    for s in number_sents[:2]:
        insights.append(f'[DATA] {s[:80]}')

    # 关键结论
    key_patterns = ['重要', '核心', '关键', '主要', '本质', '重点']
    for s in sentences:
        if any(p in s for p in key_patterns):
            insights.append(f'[INSIGHT] {s[:80]}')
            break

    # 结论性句子
    conclusion_patterns = ['因此', '所以', '总之', '结论是', '也就是说', '换句话说']
    for s in sentences:
        if any(p in s for p in conclusion_patterns):
            insights.append(f'[CONCLUSION] {s[:80]}')
            break

    return insights[:5]


def analyze_article(md_text):
    """分析一篇 markdown 文章"""
    # 去除 frontmatter
    body = re.sub(r'^---[\s\S]*?---\n', '', md_text).strip()
    body = re.sub(r'!\[.*?\]\(.*?\)', '', body)
    body = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', body)
    body = re.sub(r'```.*?```', '', body, flags=re.DOTALL)
    body = re.sub(r'`[^`]+`', '', body)

    sentences = split_sentences(body)
    if not sentences:
        return None

    summary_sents = score_sentences_tfidf(sentences, top_n=5)
    summary = ' '.join(summary_sents[:5])
    keywords = extract_keywords(body, top_n=5)
    insights = extract_insights(sentences)
    char_count = len(body.replace('\n', '').replace(' ', ''))

    return {
        'summary': summary[:500] if summary else '',
        'keywords': keywords,
        'insights': insights,
        'char_count': char_count,
        'reading_time_minutes': max(1, round(char_count / 800)),
        'sentences_count': len(sentences),
    }


def main():
    parser = argparse.ArgumentParser(description='analyzer - 文章自动分析')
    parser.add_argument('--file', required=True, help='Markdown 文件路径')
    parser.add_argument('--json', action='store_true', help='输出 JSON')
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f'File not found: {args.file}', file=sys.stderr)
        sys.exit(1)

    with open(args.file, 'r', encoding='utf-8', errors='replace') as f:
        md_text = f.read()

    result = analyze_article(md_text)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print('=' * 50)
        print('[SUMMARY] Article Analysis Report')
        print('=' * 50)
        if result['summary']:
            print(f'\n[Summary]\n{result["summary"]}')
        if result['keywords']:
            print(f'\n[Keywords] {" / ".join(result["keywords"])}')
        if result['insights']:
            print(f'\n[Key Insights]')
            for insight in result['insights']:
                print(f'  {insight}')
        print(f'\n[Stats] {result["char_count"]} chars | {result["sentences_count"]} sentences | ~{result["reading_time_minutes"]} min read')


if __name__ == '__main__':
    main()
