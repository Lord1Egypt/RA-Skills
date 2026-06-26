#!/usr/bin/env python3
"""
Memory Palace 向量查询 + 复合评分 + 元数据过滤。

复合评分 = 0.5 * 语义相似度 + 0.25 * 时效性 + 0.25 * 重要性

用法:
  python3 query_bge.py "查询内容"
  python3 query_bge.py --type palace "查询内容"
  python3 query_bge.py --priority high "查询内容"
  python3 query_bge.py --type palace --priority high "查询内容"
"""
import argparse
import json
import math
import time
from pathlib import Path
from FlagEmbedding import BGEM3FlagModel

ROOT = Path('/Users/zhouyi0415126.com/ai_matrix/vault/01_core')
INDEX = ROOT / 'memory/palace/watchdog/index/watchdog_vectors_v1_2026-04-08.jsonl'
GRAPH = ROOT / 'memory/palace/watchdog/index/graph_neighbors_v1_2026-04-08.json'

# 重要性权重映射
PRIORITY_MAP = {
    'high': 1.0,
    'medium': 0.6,
    'low': 0.3,
}
PRIORITY_DEFAULT = 0.5  # 无 priority 字段时的默认值


def get_importance(priority: str) -> float:
    """将 priority 字符串映射为 [0, 1] 重要性分数"""
    if priority is None:
        return PRIORITY_DEFAULT
    return PRIORITY_MAP.get(priority.lower(), PRIORITY_DEFAULT)


def get_recency(mtime: float) -> float:
    """
    时效性衰减：30 天半衰期。
    recency = exp(-days_since_mod / 30)
    今天修改的 → 1.0，30 天前 → 0.37，1年前 → 0.00005
    """
    if mtime is None or mtime <= 0:
        return 0.5  # 无 mtime 的默认中等时效性
    days_since = (time.time() - mtime) / 86400
    if days_since < 0:
        days_since = 0
    return math.exp(-days_since / 30)


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def is_cold_zone_path(path: str) -> bool:
    return "archive_basement" in path


def compound_score(semantic: float, recency: float, importance: float) -> float:
    """
    复合评分公式：
    - semantic: 余弦相似度（clamped to [0, 1]）
    - recency: 时效性衰减
    - importance: 重要性权重
    """
    sem = max(0.0, semantic)  # 负值 clamp 到 0
    return 0.5 * sem + 0.25 * recency + 0.25 * importance


def main():
    parser = argparse.ArgumentParser(description='Memory Palace 向量查询 + 复合评分')
    parser.add_argument('query', nargs='*', default=[], help='查询文本')
    parser.add_argument('--type', '-t', default=None, help='按 type 过滤（如 palace, project）')
    parser.add_argument('--priority', '-p', default=None, help='按 priority 过滤（如 high, medium）')
    parser.add_argument('--top-k', '-k', type=int, default=3, help='返回前 K 条（默认 3）')
    parser.add_argument('--raw', action='store_true', help='只输出原始余弦相似度（不使用复合评分）')
    parser.add_argument('--details', action='store_true', help='输出每条的分项得分')
    args = parser.parse_args()

    query = ' '.join(args.query).strip()
    if not query and not (args.type or args.priority):
        print('usage: query_bge.py [--type TYPE] [--priority PRIORITY] "查询内容"')
        print('       query_bge.py --type palace --priority high "查询内容"')
        return

    # ---- 加载数据 ----
    rows = []
    by_path = {}

    for line in INDEX.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        # 冷区盲化
        if is_cold_zone_path(row['path']):
            continue
        # 元数据预过滤
        if args.type and row.get('type') != args.type:
            continue
        if args.priority and row.get('priority') != args.priority:
            continue
        rows.append(row)
        by_path[row['path']] = row

    if not rows:
        print('[WATCHDOG_EMPTY] 过滤后无匹配文件')
        return

    # ---- 查询编码 ----
    if query:
        model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=False)
        qv = model.encode([query], batch_size=1, max_length=128)['dense_vecs'][0]
        if hasattr(qv, 'tolist'):
            qv = qv.tolist()
    else:
        qv = None

    # ---- 评分 ----
    for row in rows:
        if qv is not None:
            cos = cosine(qv, row['embedding'])
        else:
            cos = 0.5  # 无查询时，所有文件同权

        if args.raw:
            row['score'] = max(0.0, cos)
        else:
            row['score'] = compound_score(
                semantic=cos,
                recency=get_recency(row.get('mtime', 0)),
                importance=get_importance(row.get('priority')),
            )
        row['_cosine'] = cos
        row['_recency'] = get_recency(row.get('mtime', 0))
        row['_importance'] = get_importance(row.get('priority'))

    rows.sort(key=lambda x: x['score'], reverse=True)
    top = rows[:args.top_k]

    # ---- 输出 ----
    graph = json.loads(GRAPH.read_text(encoding='utf-8')) if GRAPH.exists() else {}
    printed = set()

    for r in top:
        printed.add(r['path'])
        if args.details:
            print(json.dumps({
                'role': 'core',
                'path': r['path'],
                'type': r.get('type'),
                'priority': r.get('priority'),
                'score': round(r['score'], 6),
                'semantic': round(r['_cosine'], 4),
                'recency': round(r['_recency'], 4),
                'importance': round(r['_importance'], 4),
            }, ensure_ascii=False))
        else:
            print(json.dumps({
                'role': 'core',
                'path': r['path'],
                'type': r.get('type'),
                'priority': r.get('priority'),
                'score': round(r['score'], 6),
            }, ensure_ascii=False))

        # 1-hop 邻居
        for n in graph.get(r['path'], [])[:2]:
            if n in printed or n not in by_path:
                continue
            printed.add(n)
            nr = by_path[n]
            print(json.dumps({
                'role': 'neighbor',
                'path': n,
                'type': nr.get('type'),
                'priority': nr.get('priority'),
                'score': round(nr.get('score', 0.0), 6),
            }, ensure_ascii=False))

    if not top:
        print('[WATCHDOG_NO_MATCH]')


if __name__ == '__main__':
    main()
