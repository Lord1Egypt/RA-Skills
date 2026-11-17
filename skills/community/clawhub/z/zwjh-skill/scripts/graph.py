# -*- coding: utf-8 -*-
"""
知识图谱 —— 实体 / 关系图谱。

实体类型：person / project / task / event / document / concept / org / custom
（类型是可插拔的：其他 skill 可直接 upsert 自己的实体类型）

核心能力：
  - upsert 实体（同 type+name 不重复）
  - 添加关系（from -> relation -> to），自动累积权重
  - 写入「事实」并做冲突消解（新值覆盖旧值，旧值保留为历史）
  - 从文本中自动识别实体提及（mention linking），把记忆挂到实体上
"""

from __future__ import annotations

import re

from . import store
from .embeddings import tokenize

# 关系抽取用的轻量模板（可插拔扩展）
_RELATION_PATTERNS = [
    (r"([一-龥A-Za-z0-9_]{1,12})负责([一-龥A-Za-z0-9_]{1,12})", "负责"),
    (r"([一-龥A-Za-z0-9_]{1,12})参与([一-龥A-Za-z0-9_]{1,12})", "参与"),
    (r"([一-龥A-Za-z0-9_]{1,12})隶属于([一-龥A-Za-z0-9_]{1,12})", "隶属于"),
    (r"([一-龥A-Za-z0-9_]{1,12})创建([一-龥A-Za-z0-9_]{1,12})", "创建"),
    (r"([一-龥A-Za-z0-9_]{1,12})依赖([一-龥A-Za-z0-9_]{1,12})", "依赖"),
    (r"([一-龥A-Za-z0-9_]{1,12})导致([一-龥A-Za-z0-9_]{1,12})", "导致"),
    (r"([一-龥A-Za-z0-9_]{1,12})在([一-龥A-Za-z0-9_]{1,12})上", "位于"),
]

# 关系抽取时跳过的泛化词（避免「人/事/物」这类无意义实体）
_GENERIC = {"人", "事", "物", "它", "他", "她", "我们", "你们", "他们",
            "这个", "那个", "什么", "谁", "我", "你", "其", "此", "该", "之"}


def mention_link(text: str, limit: int = 10) -> list[dict]:
    """
    在文本中查找已知实体提及（按实体名 token 命中），返回命中的实体列表。
    这是「让记忆自动挂到知识图谱」的关键一步。
    """
    toks = set(tokenize(text))
    if not toks:
        return []
    entities = store.list_entities(limit=2000)
    hits = []
    for e in entities:
        name_toks = set(tokenize(e["name"]))
        if not name_toks:
            continue
        # 实体名 token 全部出现于文本 => 命中
        if name_toks & toks:
            # 计算重叠程度，过滤太弱的误命中
            overlap = len(name_toks & toks) / len(name_toks)
            if overlap >= 0.5:
                hits.append({"entity_id": e["id"], "name": e["name"], "type": e["type"]})
        if len(hits) >= limit:
            break
    return hits


def _clean_entity(name: str) -> str:
    """清理实体名：去标点、去首尾连接动词、去开头泛化修饰、去结尾无意义后缀。"""
    name = name.strip().strip("，。；;、, ：:").strip()
    # 去开头泛化修饰
    for pre in ["客户", "用户", "我的", "我们", "你们", "他们", "这个", "那个", "该", "此",
               "现在", "目前", "之前", "原来", "其实", "实际上", "确实", "是", "在"]:
        if name.startswith(pre) and len(name) > len(pre):
            name = name[len(pre):]
    # 去结尾连接动词和无意义后缀
    for suf in ["对接", "负责", "处理", "管理", "跟进", "联系", "支持", "推进",
                "协调", "参与", "创建", "开发", "维护", "运营", "其实", "实际上",
                "现在", "目前", "之前"]:
        if name.endswith(suf) and len(name) > len(suf):
            name = name[: -len(suf)]
    if name.endswith("的"):
        name = name[:-1]
    return name.strip()


def auto_relate_from_text(text: str, default_type: str = "concept") -> list[dict]:
    """
    轻量关系抽取（保守版，避免噪声）：
      1) 已知实体在同一段文本中「共现」-> 弱关联边（图谱随使用自然生长）。
      2) 显式关系模板（负责/参与/隶属于…），端点需为短实词且非泛化词。
    返回新建/更新的关系列表（供日志）。
    """
    created: list[dict] = []

    # 1) 已知实体共现（仅在提及实体较少时建立，避免组合爆炸污染图谱）
    mentions = mention_link(text, limit=20)
    if 1 < len(mentions) <= 8:
        for i in range(len(mentions)):
            for j in range(i + 1, len(mentions)):
                rid = store.add_relation(
                    mentions[i]["entity_id"], mentions[j]["entity_id"],
                    "共现", weight=0.3, confidence=0.5,
                )
                if rid:
                    created.append({"from": mentions[i]["name"], "relation": "共现",
                                    "to": mentions[j]["name"]})

    # 2) 显式关系模板（保守）
    for pat, rel in _RELATION_PATTERNS:
        for m in re.finditer(pat, text):
            a, b = _clean_entity(m.group(1)), _clean_entity(m.group(2))
            if not a or not b:
                continue
            if len(a) > 12 or len(b) > 12:
                continue
            if a in _GENERIC or b in _GENERIC:
                continue
            a_id = store.upsert_entity(_guess_type(a), a, importance=0.6)
            b_id = store.upsert_entity(_guess_type(b), b, importance=0.6)
            rid = store.add_relation(a_id, b_id, rel, weight=1.0, confidence=0.6)
            if rid:
                created.append({"from": a, "relation": rel, "to": b})
    return created


def _guess_type(name: str) -> str:
    """根据名称简单猜测实体类型（可被显式类型覆盖）。"""
    n = name.strip()
    cjk = re.findall(r"[一-龥]", n)
    # 2~4 个汉字且不含项目类关键词 -> 多半是人名
    if 2 <= len(cjk) <= 4 and not any(
        k in n for k in ["项目", "系统", "平台", "任务", "文档", "公司", "团队"]
    ):
        return "person"
    if any(k in n for k in ["项目", "project", "系统", "平台", "app"]):
        return "project"
    if any(k in n for k in ["任务", "task", "todo", "issue", "bug"]):
        return "task"
    if any(k in n for k in ["会议", "事件", "event", "发布", "上线"]):
        return "event"
    if any(k in n for k in ["文档", "doc", "报告", "readme", "设计稿"]):
        return "document"
    if any(k in n for k in ["公司", "团队", "部门", "org"]):
        return "org"
    return "concept"


def export_graph() -> dict:
    """导出整个图谱为可序列化结构（供可视化 / 备份）。"""
    entities = store.list_entities(limit=5000)
    nodes = [
        {"id": e["id"], "name": e["name"], "type": e["type"],
         "importance": e["importance"]}
        for e in entities
    ]
    links = []
    for e in entities:
        for r in store.relations_of(e["id"], direction="out"):
            links.append(
                {"source": e["id"], "target": r["to_id"],
                 "relation": r["relation"], "weight": r["weight"]}
            )
    return {"nodes": nodes, "links": links}


def render_mermaid() -> str:
    """导出 Mermaid 图（在 SKILL.md / 终端直接渲染）。"""
    g = export_graph()
    lines = ["graph LR"]
    id_map = {n["id"]: f'N{n["id"]}' for n in g["nodes"]}
    for n in g["nodes"]:
        label = f'{n["name"]}<br><{n["type"]}>'
        lines.append(f'  {id_map[n["id"]]}["{label}"]')
    for l in g["links"]:
        s = id_map.get(l["source"])
        t = id_map.get(l["target"])
        if s and t:
            lines.append(f'  {s} -->|{l["relation"]}| {t}')
    return "\n".join(lines)


def find_shortest_path(from_name: str, to_name: str) -> dict | None:
    """BFS 查找两实体间的最短路径。"""
    from . import store
    f = store.find_entity(None, from_name)
    t = store.find_entity(None, to_name)
    if not f or not t:
        return None
    if f["id"] == t["id"]:
        return {"path": [f["name"]], "text": f["name"], "hops": 0}
    from collections import deque
    queue = deque([(f["id"], [f["id"]])])
    visited = {f["id"]}
    while queue:
        cur, path = queue.popleft()
        rels = store.relations_of(cur, direction="both")
        for r in rels:
            nid = r["from_id"] if r["to_id"] == cur else r["to_id"]
            if nid in visited:
                continue
            visited.add(nid)
            new_path = path + [nid]
            if nid == t["id"]:
                # 构建可读路径
                names = []
                conn = store.get_conn()
                for pid in new_path:
                    row = conn.execute("SELECT name FROM entities WHERE id=?", (pid,)).fetchone()
                    names.append(row["name"] if row else "?")
                return {
                    "path": names,
                    "hops": len(names) - 1,
                    "text": " → ".join(names),
                }
            queue.append((nid, new_path))
    return None


if __name__ == "__main__":
    print(render_mermaid())
