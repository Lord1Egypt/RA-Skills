#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path('/Users/zhouyi0415126.com/ai_matrix/vault/01_core')
INDEX = ROOT / 'memory/palace/watchdog/index/watchdog_vectors_v1_2026-04-08.jsonl'
LINK_RE = re.compile(r'\[\[([^\]]+)\]\]')


def read_text(rel_path: str) -> str:
    p = ROOT / rel_path
    if not p.exists():
        return ''
    return p.read_text(encoding='utf-8', errors='ignore')


def is_cold_zone_path(path: str) -> bool:
    """判断路径是否属于冷区（archive_basement）"""
    return "archive_basement" in path


def extract_links(text: str):
    return list(dict.fromkeys(LINK_RE.findall(text)))


def build_alias_map(rows):
    alias = {}
    for r in rows:
        stem = Path(r['path']).stem
        alias[stem] = r['path']
        alias[r['path']] = r['path']
    return alias


def main():
    rows = [json.loads(line) for line in INDEX.read_text(encoding='utf-8').splitlines() if line.strip()]
    alias = build_alias_map(rows)
    graph = {}
    for r in rows:
        # 冷区盲化：跳过冷区文件
        if is_cold_zone_path(r['path']):
            continue
            
        text = read_text(r['path'])
        links = []
        for raw in extract_links(text):
            key = raw.split('/')[-1]
            if key in alias:
                target = alias[key]
                # 冷区盲化：不链接到冷区文件
                if not is_cold_zone_path(target):
                    links.append(target)
        graph[r['path']] = links[:2]
    out = ROOT / 'memory/palace/watchdog/index/graph_neighbors_v1_2026-04-08.json'
    out.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'[GRAPH_ROUTER_READY] nodes={len(graph)} out={out}')


if __name__ == '__main__':
    main()
