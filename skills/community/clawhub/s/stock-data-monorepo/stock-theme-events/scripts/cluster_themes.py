#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题材聚类脚本 - 使用语义相似度 + 同义词词典将相似题材合并
"""

import json
import argparse
from collections import defaultdict
from typing import Dict, List, Tuple
import os

try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    HAS_SEMANTIC = True
except ImportError:
    HAS_SEMANTIC = False
    print("警告：sentence-transformers 未安装，将使用简单频次统计")


def load_synonyms(config_path: str) -> Dict[str, List[str]]:
    """加载同义词配置"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def normalize_theme(theme: str, synonyms: Dict[str, List[str]]) -> str:
    """将题材映射到标准名称"""
    theme = theme.strip()
    for standard, variants in synonyms.items():
        if theme in variants or theme == standard:
            return standard
    return theme


def cluster_by_frequency(themes_count: Dict[str, int], top_n: int = 8) -> List[Tuple[str, int]]:
    """简单频次统计聚类"""
    sorted_themes = sorted(themes_count.items(), key=lambda x: x[1], reverse=True)
    return sorted_themes[:top_n]


def cluster_by_semantic(themes_list: List[str], synonyms: Dict[str, List[str]], 
                        top_n: int = 8, threshold: float = 0.7) -> List[Tuple[str, int]]:
    """语义相似度聚类"""
    if not HAS_SEMANTIC:
        return cluster_by_frequency(defaultdict(int, {t: 1 for t in themes_list}), top_n)
    
    # 先使用同义词词典标准化
    normalized = defaultdict(list)
    for theme in themes_list:
        standard = normalize_theme(theme, synonyms)
        normalized[standard].append(theme)
    
    # 统计频次
    themes_count = {k: len(v) for k, v in normalized.items()}
    
    # 如果题材数量少，直接返回频次排序
    if len(themes_count) <= top_n:
        return sorted(themes_count.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    # 使用语义模型进一步聚类
    try:
        model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        theme_names = list(themes_count.keys())
        embeddings = model.encode(theme_names)
        sim_matrix = cosine_similarity(embeddings)
        
        # 合并高相似度题材
        merged = {}
        used = set()
        for i, name1 in enumerate(theme_names):
            if i in used:
                continue
            merged[name1] = themes_count[name1]
            for j, name2 in enumerate(theme_names):
                if j <= i or j in used:
                    continue
                if sim_matrix[i][j] > threshold:
                    merged[name1] += themes_count[name2]
                    used.add(j)
        
        return sorted(merged.items(), key=lambda x: x[1], reverse=True)[:top_n]
    except Exception as e:
        print(f"语义聚类失败：{e}，降级到频次统计")
        return cluster_by_frequency(themes_count, top_n)


def process_themes(input_path: str, output_path: str, config_path: str,
                   top_n: int = 8, threshold: float = 0.7):
    """
    处理题材聚类
    
    Args:
        input_path: 输入 JSON 文件路径（格式：{股票代码：[题材列表]}）
        output_path: 输出 JSON 文件路径
        config_path: 同义词配置文件路径
        top_n: 保留 TOP N 个题材方向
        threshold: 语义相似度阈值
    """
    # 加载输入数据
    with open(input_path, 'r', encoding='utf-8') as f:
        stock_themes = json.load(f)
    
    # 加载同义词配置
    synonyms = load_synonyms(config_path)
    
    # 收集所有题材（带股票信息）
    theme_stocks = defaultdict(list)
    all_themes = []
    
    for stock_code, themes in stock_themes.items():
        for theme in themes:
            standard = normalize_theme(theme, synonyms)
            if stock_code not in theme_stocks[standard]:
                theme_stocks[standard].append(stock_code)
            all_themes.append(standard)
    
    # 聚类
    clustered = cluster_by_semantic(all_themes, synonyms, top_n, threshold)
    
    # 构建输出
    result = {
        "top_themes": [
            {
                "theme": theme,
                "count": count,
                "stocks": theme_stocks.get(theme, [])
            }
            for theme, count in clustered
        ],
        "all_themes": {
            theme: {
                "count": len(stocks),
                "stocks": stocks
            }
            for theme, stocks in theme_stocks.items()
        }
    }
    
    # 保存结果
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"聚类完成，共 {len(theme_stocks)} 个题材方向，保留 TOP {top_n}")
    print(f"结果已保存到：{output_path}")
    
    return result


def main():
    parser = argparse.ArgumentParser(description='题材聚类脚本')
    parser.add_argument('--input', required=True, help='输入题材 JSON 文件')
    parser.add_argument('--output', required=True, help='输出聚类结果')
    parser.add_argument('--config', default='config/theme_synonyms.json', 
                        help='同义词配置文件')
    parser.add_argument('--top', type=int, default=8, help='保留 TOP N 个题材方向')
    parser.add_argument('--threshold', type=float, default=0.7, help='语义相似度阈值')
    
    args = parser.parse_args()
    
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = args.config
    if not os.path.isabs(config_path):
        config_path = os.path.join(script_dir, '..', config_path)
    
    process_themes(args.input, args.output, config_path, args.top, args.threshold)


if __name__ == '__main__':
    main()
