#!/usr/bin/env python3
"""
关键词相关性打分工具
使用模糊匹配和余弦相似度计算论文与关键词的相关性

使用方法:
    python3 score_papers.py --keywords "agent,prompt injection,defense" --papers paper_list.csv
    python3 score_papers.py --keywords "LLM,security,attack" --title "xxx" --abstract "xxx"
"""

import argparse
import os
import re
import csv
import json
from typing import List, Dict, Tuple
from collections import Counter

# 尝试导入可选依赖
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

try:
    from rapidfuzz import fuzz
    RAPIDFUZZ_AVAILABLE = True
except ImportError:
    try:
        from fuzzywuzzy import fuzz
        RAPIDFUZZ_AVAILABLE = True
    except ImportError:
        RAPIDFUZZ_AVAILABLE = False
        fuzz = None


def preprocess_text(text: str) -> str:
    """预处理文本：转小写、移除特殊字符"""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def tokenize(text: str) -> List[str]:
    """分词"""
    return preprocess_text(text).split()


def fuzzy_keyword_score(text: str, keywords: List[str]) -> float:
    """
    使用模糊匹配计算关键词相关度
    结合多种模糊匹配策略
    """
    if not text or not keywords:
        return 0.0
    
    text_lower = text.lower()
    scores = []
    
    for keyword in keywords:
        keyword_lower = keyword.lower().strip()
        if not keyword_lower:
            continue
            
        # 1. 简单包含检查
        if keyword_lower in text_lower:
            scores.append(1.0)
            continue
        
        # 2. 模糊匹配 (如果可用)
        if RAPIDFUZZ_AVAILABLE:
            # partial_ratio: 部分匹配
            partial = fuzz.partial_ratio(keyword_lower, text_lower) / 100.0
            # token_sort_ratio: 词序无关匹配
            token_sort = fuzz.token_sort_ratio(keyword_lower, text_lower) / 100.0
            # token_set_ratio: 集合匹配
            token_set = fuzz.token_set_ratio(keyword_lower, text_lower) / 100.0
            
            # 加权平均
            fuzzy_score = max(partial, token_sort, token_set)
            scores.append(fuzzy_score)
        else:
            # 备选：基于字符 n-gram 的简单匹配
            score = simple_ngram_match(keyword_lower, text_lower)
            scores.append(score)
    
    if not scores:
        return 0.0
    
    # 返回最高分和平均分的加权组合
    max_score = max(scores)
    avg_score = sum(scores) / len(scores)
    
    # 组合策略：突出最高匹配，同时考虑整体相关性
    return 0.6 * max_score + 0.4 * avg_score


def simple_ngram_match(keyword: str, text: str, n: int = 3) -> float:
    """简单的 n-gram 匹配 (无外部依赖时使用)"""
    if len(keyword) < n:
        return 1.0 if keyword in text else 0.0
    
    keyword_ngrams = set(keyword[i:i+n] for i in range(len(keyword) - n + 1))
    text_ngrams = set(text[i:i+n] for i in range(len(text) - n + 1))
    
    if not keyword_ngrams:
        return 0.0
    
    intersection = keyword_ngrams & text_ngrams
    return len(intersection) / len(keyword_ngrams)


def tfidf_cosine_similarity(texts: List[str], query: str) -> List[float]:
    """
    使用 TF-IDF 和余弦相似度计算相关性
    """
    if not SKLEARN_AVAILABLE or not texts:
        return [0.0] * len(texts)
    
    try:
        vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words='english',
            ngram_range=(1, 2),
            max_features=5000
        )
        
        # 将查询加入语料库一起向量化
        all_texts = texts + [query]
        tfidf_matrix = vectorizer.fit_transform(all_texts)
        
        # 计算查询与每个文档的余弦相似度
        query_vector = tfidf_matrix[-1]
        doc_vectors = tfidf_matrix[:-1]
        
        similarities = cosine_similarity(query_vector, doc_vectors)[0]
        
        return similarities.tolist()
    except Exception as e:
        print(f"TF-IDF 计算错误: {e}")
        return [0.0] * len(texts)


def hybrid_score(
    title: str, 
    abstract: str, 
    keywords: List[str],
    title_weight: float = 0.6,
    abstract_weight: float = 0.4
) -> Dict:
    """
    混合打分：结合模糊匹配和 TF-IDF 余弦相似度
    
    Args:
        title: 论文标题
        abstract: 论文摘要
        keywords: 关键词列表
        title_weight: 标题权重
        abstract_weight: 摘要权重
    
    Returns:
        包含各项分数的字典
    """
    # 1. 模糊匹配分数
    fuzzy_title_score = fuzzy_keyword_score(title, keywords)
    fuzzy_abstract_score = fuzzy_keyword_score(abstract, keywords)
    
    # 2. TF-IDF 余弦相似度
    combined_text = f"{title} {abstract}"
    tfidf_scores = tfidf_cosine_similarity([combined_text], " ".join(keywords))
    tfidf_score = tfidf_scores[0] if tfidf_scores else 0.0
    
    # 3. 加权组合
    fuzzy_combined = (
        title_weight * fuzzy_title_score + 
        abstract_weight * fuzzy_abstract_score
    )
    
    # 最终分数：模糊匹配 60% + TF-IDF 40%
    final_score = 0.6 * fuzzy_combined + 0.4 * tfidf_score
    
    return {
        "fuzzy_title_score": round(fuzzy_title_score, 4),
        "fuzzy_abstract_score": round(fuzzy_abstract_score, 4),
        "tfidf_score": round(tfidf_score, 4),
        "final_score": round(final_score, 4),
        "match_keywords": find_matched_keywords(title, abstract, keywords)
    }


def find_matched_keywords(title: str, abstract: str, keywords: List[str]) -> List[str]:
    """找出匹配的关键词"""
    text = f"{title} {abstract}".lower()
    matched = []
    
    for kw in keywords:
        kw_lower = kw.lower().strip()
        if kw_lower in text:
            matched.append(kw)
        elif RAPIDFUZZ_AVAILABLE:
            if fuzz.partial_ratio(kw_lower, text) > 80:
                matched.append(kw)
    
    return matched


def score_papers_from_file(paper_file: str, keywords: List[str]) -> List[Dict]:
    """
    从 CSV 文件读取论文并打分
    
    CSV 格式:
    title,abstract,arxiv_id,year
    """
    papers = []
    
    # 尝试不同编码
    for encoding in ['utf-8', 'gbk', 'latin-1']:
        try:
            with open(paper_file, 'r', encoding=encoding) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    papers.append(row)
            break
        except UnicodeDecodeError:
            continue
    
    results = []
    for i, paper in enumerate(papers):
        title = paper.get('title', '')
        abstract = paper.get('abstract', '')
        
        scores = hybrid_score(title, abstract, keywords)
        scores['arxiv_id'] = paper.get('arxiv_id', f'paper_{i}')
        scores['title'] = title[:100] + '...' if len(title) > 100 else title
        scores['year'] = paper.get('year', 'N/A')
        
        results.append(scores)
    
    # 按分数排序
    results.sort(key=lambda x: x['final_score'], reverse=True)
    
    return results


def print_results(results: List[Dict], top_n: int = 10):
    """打印结果"""
    print(f"\n{'='*80}")
    print(f"{'arXiv ID':<15} {'年份':<6} {'最终分':<8} {'标题':<45}")
    print(f"{'='*80}")
    
    for r in results[:top_n]:
        title = r['title'][:42] + '...' if len(r['title']) > 45 else r['title']
        print(f"{r['arxiv_id']:<15} {r['year']:<6} {r['final_score']:<8.4f} {title}")
    
    print(f"{'='*80}")
    print(f"匹配关键词统计:")
    
    # 统计关键词匹配频率
    kw_counter = Counter()
    for r in results:
        for kw in r['match_keywords']:
            kw_counter[kw] += 1
    
    for kw, count in kw_counter.most_common(10):
        print(f"  {kw}: {count}")


def main():
    parser = argparse.ArgumentParser(
        description="论文关键词相关性打分工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 单篇论文打分
  python3 score_papers.py --keywords "agent,LLM,security" --title "xxx" --abstract "xxx"
  
  # 批量打分
  python3 score_papers.py --keywords "agent,LLM,security" --papers papers.csv
  
  # 输出 JSON
  python3 score_papers.py --keywords "agent,LLM" --papers papers.csv --output results.json
        """
    )
    
    parser.add_argument('--keywords', type=str, required=True,
                        help='关键词，用逗号分隔')
    parser.add_argument('--title', type=str,
                        help='论文标题')
    parser.add_argument('--abstract', type=str,
                        help='论文摘要')
    parser.add_argument('--papers', type=str,
                        help='CSV 文件路径，包含 title,abstract,arxiv_id,year 列')
    parser.add_argument('--output', type=str,
                        help='输出 JSON 文件路径')
    parser.add_argument('--top-n', type=int, default=10,
                        help='显示前 N 个结果 (默认: 10)')
    parser.add_argument('--title-weight', type=float, default=0.6,
                        help='标题权重 (默认: 0.6)')
    parser.add_argument('--abstract-weight', type=float, default=0.4,
                        help='摘要权重 (默认: 0.4)')
    
    args = parser.parse_args()
    
    # 解析关键词
    keywords = [k.strip() for k in args.keywords.split(',') if k.strip()]
    
    if not keywords:
        print("错误: 请提供至少一个关键词")
        return
    
    print(f"关键词: {keywords}")
    print(f"使用库: sklearn={'是' if SKLEARN_AVAILABLE else '否'}, rapidfuzz={'是' if RAPIDFUZZ_AVAILABLE else '否'}")
    
    # 单一论文模式
    if args.title:
        result = hybrid_score(
            args.title, 
            args.abstract or "", 
            keywords,
            args.title_weight,
            args.abstract_weight
        )
        
        print(f"\n论文: {args.title}")
        print(f"模糊匹配分数 (标题): {result['fuzzy_title_score']:.4f}")
        print(f"模糊匹配分数 (摘要): {result['fuzzy_abstract_score']:.4f}")
        print(f"TF-IDF 余弦相似度: {result['tfidf_score']:.4f}")
        print(f"最终分数: {result['final_score']:.4f}")
        print(f"匹配关键词: {result['match_keywords']}")
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"\n结果已保存到: {args.output}")
    
    # 批量模式
    elif args.papers:
        if not os.path.exists(args.papers):
            print(f"错误: 文件不存在: {args.papers}")
            return
        
        results = score_papers_from_file(args.papers, keywords)
        
        print_results(results, args.top_n)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"\n结果已保存到: {args.output}")
    
    else:
        print("错误: 请提供 --title 或 --papers 参数")
        parser.print_help()


if __name__ == '__main__':
    main()
