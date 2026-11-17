# -*- coding: utf-8 -*-
"""
技能缺失依赖收集
数据源：openclaw skills list --json 的 missing 字段（bins/anyBins/env/config/os）
"""
import re
from typing import Any, Dict, List


def get_dependency_edges(skills: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """
    收集缺失依赖边

    Returns:
        [{'skill', 'dep', 'kind'}]；kind: bin / anBin / env / config / os
    """
    edges = []
    for s in skills:
        missing = s.get('missing') or {}
        kind_map = (('bins', 'bin'), ('anyBins', 'anBin'), ('env', 'env'),
                    ('config', 'config'), ('os', 'os'))
        for field, kind in kind_map:
            for dep in missing.get(field) or []:
                edges.append({'skill': s.get('name', ''), 'dep': str(dep), 'kind': kind})
    return edges


def _mermaid_id(prefix: str, text: str) -> str:
    """mermaid 节点 ID：仅保留字母数字"""
    cleaned = re.sub(r'[^A-Za-z0-9]', '', text)
    return (prefix + (cleaned or 'x'))[:40]


def render_mermaid(edges: List[Dict[str, str]]) -> str:
    """把依赖边渲染为 mermaid graph LR 源码块（嵌入 Markdown 输出）"""
    if not edges:
        return ''
    lines = ['```mermaid', 'graph LR']
    for e in edges:
        sid = _mermaid_id('S', e['skill'])
        did = _mermaid_id('D', e['kind'] + ':' + e['dep'])
        lines.append(f'    {sid}["{e["skill"]}"] -->|{e["kind"]}| {did}["{e["dep"]}"]')
    lines.append('```')
    return '\n'.join(lines)
