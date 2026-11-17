"""graph_api.py — 软件工程语义图谱的图操作封装。

基于 axolotl_rs（经 lobster-memory engine 的 MemoryGraph 封装）实现：
- 节点/边 CRUD（字段级，不 dump 全文）
- 定向遍历查询：从任意入口沿语义边正向/反向 BFS，只输出相关上下文
- 索引重建：axolotl 无反向遍历与边枚举 API，查询时自建双向邻接表
  （语义图规模=模块/需求/决策级，几百节点，全量读入内存做 BFS 完全可行；
   注意：读入内存做算法 ≠ dump 给模型，输出仍只取字段级摘要）
"""

import os
import sys
import logging

logger = logging.getLogger("se_semantic_graph")

# 复用 lobster-memory 引擎
SKILL_ENGINE = os.environ.get(
    "SE_SEMANTIC_ENGINE", "/Users/sai/.workbuddy/skills/lobster-memory"
)
if SKILL_ENGINE not in sys.path:
    sys.path.insert(0, SKILL_ENGINE)

try:
    from engine.memory_graph import MemoryGraph  # noqa: E402
    from engine.schema import str_to_id, ts_now  # noqa: E402
except ImportError as e:
    sys.stderr.write(
        "[se-semantic-graph] 无法导入 lobster-memory engine。\n"
        f"  原始错误: {e}\n"
    )
    sys.exit(2)

_SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
if _SKILL_DIR not in sys.path:
    sys.path.insert(0, _SKILL_DIR)

from schema import NODE_TYPES, EDGE_KINDS, DOMAIN_OF_TYPE  # noqa: E402

DEFAULT_GRAPH_FILE = "memory.axeb"

ROOT_ID = "se_project_root"


def _node_defaults(id_str: str, label: str, node_type: str, summary: str = "",
                   detail_ref: str = "", source: str = "") -> dict:
    return {
        "id": id_str,
        "label": label,
        "type": node_type,
        "summary": summary,
        "detail_ref": detail_ref,
        "source": source,
        "domain": DOMAIN_OF_TYPE.get(node_type, "knowledge"),
        "status": "live",
        "weight": 1.0,
        "access_count": 0,
        "last_accessed": None,
        "created_at": ts_now(),
        "updated_at": ts_now(),
    }


def _edge_props(from_id: str, to_id: str, kind: str, note: str = "") -> dict:
    return {
        "from": from_id,
        "to": to_id,
        "kind": kind,
        "note": note,
        "status": "live",
        "weight": 1.0,
        "access_count": 0,
        "last_accessed": None,
        "created_at": ts_now(),
        "updated_at": ts_now(),
    }


class SEManticGraph:
    """软件工程语义图谱操作入口。"""

    def __init__(self, data_path: str = DEFAULT_GRAPH_FILE):
        self._path = data_path
        self._g = MemoryGraph(data_path)
        self._ensure_root()

    # ── root ──────────────────────────────────────────

    def _ensure_root(self):
        if self._g.get_vertex(ROOT_ID) is None:
            self._g.upsert_vertex({
                "id": ROOT_ID,
                "label": "软件工程语义图谱根",
                "type": "project_root",
                "summary": "项目级根锚点，供 walk 遍历枚举",
                "domain": "knowledge",
                "status": "live",
                "weight": 0.0,
            })

    # ── 底层 edge 访问（MemoryGraph 未暴露，直接用 axolotl）──

    def _raw_edge(self, a: str, b: str):
        """底层 get_edge: (weight, props) or None"""
        try:
            return self._g._g.get_edge(str_to_id(a), str_to_id(b))
        except Exception:
            return None

    def _raw_add_edge(self, a: str, b: str, kind: str, note: str = ""):
        self._g._g.add_edge(
            str_to_id(a), str_to_id(b), 1.0,
            {k: v for k, v in _edge_props(a, b, kind, note).items() if v is not None},
        )

    # ── Write: node ───────────────────────────────────

    def upsert_node(self, id_str: str, label: str, node_type: str,
                    summary: str = "", detail_ref: str = "", source: str = "",
                    weight: float = 1.0) -> dict:
        """新增或更新一个语义节点。字段级摘要，不存全文。"""
        if node_type not in NODE_TYPES:
            raise ValueError(
                f"未知节点类型 '{node_type}'，可选: {', '.join(NODE_TYPES)}"
            )
        existing = self._g.get_vertex(id_str)
        props = _node_defaults(id_str, label, node_type, summary, detail_ref, source)
        if existing:
            for k, v in existing.items():
                props.setdefault(k, v)
            props["weight"] = existing.get("weight", 1.0) + weight
            props["updated_at"] = ts_now()
        self._g.upsert_vertex(props)

        # 挂到根（walk 枚举用）
        if self._raw_edge(ROOT_ID, id_str) is None:
            self._raw_add_edge(ROOT_ID, id_str, "has_member")
        return {"id": id_str, "label": label, "type": node_type}

    def get_node(self, id_str: str) -> dict:
        v = self._g.get_vertex(id_str)
        if v is None:
            return {}
        return {k: v.get(k) for k in
                ("id", "label", "type", "summary", "detail_ref", "source", "status")}

    def list_nodes(self, node_type: str = None, limit: int = 500) -> list:
        out = []
        for props in self._iter_all_vertices().values():
            if props.get("status") != "live":
                continue
            if node_type and props.get("type") != node_type:
                continue
            out.append({
                "id": props.get("id"),
                "label": props.get("label"),
                "type": props.get("type"),
                "summary": props.get("summary", ""),
            })
            if len(out) >= limit:
                break
        return out

    # ── Read: enumerate ────────────────────────────────

    def _iter_all_vertices(self) -> dict:
        """全量枚举顶点：从根 walk。返回 {id_str: props}。"""
        result = {}
        try:
            visited_ids = self._g.walk(ROOT_ID, 10)
        except Exception as e:
            logger.warning("walk from root failed: %s", e)
            visited_ids = []
        if ROOT_ID not in result and self._g.get_vertex(ROOT_ID) is not None:
            result[ROOT_ID] = self._g.get_vertex(ROOT_ID)
        for id_str in visited_ids:
            if id_str in result:
                continue
            v = self._g.get_vertex(id_str)
            if v is not None:
                result[id_str] = v
        return result

    # ── Write: edge ────────────────────────────────────

    def connect(self, from_id: str, to_id: str, kind: str, note: str = "") -> dict:
        """新增跨域语义边。两节点必须已存在。

        只建一条正向边即可——EdgeBlock 存储层 add_edge 时同时写
        正向块（出边）与反向块（入边），in_neighbors 原生支持反向遍历，
        无需技能层建反向边。
        """
        if kind not in EDGE_KINDS:
            raise ValueError(
                f"未知边类型 '{kind}'，可选: {', '.join(EDGE_KINDS)}"
            )
        for v_id in (from_id, to_id):
            if self._g.get_vertex(v_id) is None:
                raise ValueError(f"节点不存在: {v_id}（先用 upsert_node 创建）")
        if self._raw_edge(from_id, to_id) is not None:
            return {"status": "exists", "from": from_id, "to": to_id, "kind": kind}
        self._raw_add_edge(from_id, to_id, kind, note)
        return {"status": "created", "from": from_id, "to": to_id, "kind": kind}

    # ── Read: directed traversal（定向查询，原生 API）──

    def _neighbors(self, id_str: str, direction: str) -> list:
        """沿指定方向取邻居（含边 kind）。原生 out_neighbors/in_neighbors。"""
        nid = str_to_id(id_str)
        result = []
        try:
            if direction == "in":
                raw = self._g._g.in_neighbors(nid)
                # 入边：邻居 nb -> 当前 id，边存于 (nb, id)
                for nb_nid in raw:
                    nb_id = self._id_by_nid(nb_nid)
                    if nb_id is None:
                        continue
                    edge = self._raw_edge(nb_id, id_str)
                    kind = edge[1].get("kind", "relates_to") if edge else "relates_to"
                    if kind == "has_member":
                        continue  # 根锚点边不参与语义追溯
                    result.append((nb_id, kind))
            else:
                raw = self._g._g.out_neighbors(nid)
                # 出边：当前 id -> 邻居 nb，边存于 (id, nb)
                for nb_nid in raw:
                    nb_id = self._id_by_nid(nb_nid)
                    if nb_id is None:
                        continue
                    edge = self._raw_edge(id_str, nb_id)
                    kind = edge[1].get("kind", "relates_to") if edge else "relates_to"
                    if kind == "has_member":
                        continue
                    result.append((nb_id, kind))
        except Exception as e:
            logger.warning("neighbors(%s, %s) failed: %s", id_str, direction, e)
        return result

    def _id_by_nid(self, nid: int) -> str:
        """数字 nid → id_str。用 walk 全图构建 nid→id 映射（一次遍历，O(n)）。"""
        if not hasattr(self, "_nid_map"):
            self._nid_map = {}
            for id_str, _props in self._iter_all_vertices().items():
                self._nid_map[str_to_id(id_str)] = id_str
        return self._nid_map.get(nid)

    def trace(self, start_id: str, direction: str = "up",
              max_depth: int = 4, max_results: int = 50,
              kind_filter: str = None, node_type_filter: str = None) -> dict:
        """
        从任意入口定向遍历，返回相关上下文子图（字段级摘要）。

        图库原生支持双向：up 用 in_neighbors（反向追溯为什么做），
        down 用 out_neighbors（正向展开影响什么）。逐层扩展，只取相关节点，
        不 dump 全库。
        """
        if self._g.get_vertex(start_id) is None:
            return {"error": f"起点节点不存在: {start_id}", "nodes": [], "paths": []}

        self._direction = direction
        neighbor_dir = "in" if direction == "up" else "out"

        visited = {start_id: 0}
        paths = []
        queue = [start_id]
        while queue:
            cur = queue.pop(0)
            depth = visited[cur]
            if depth >= max_depth:
                continue
            for (nb, kind) in self._neighbors(cur, neighbor_dir):
                if kind_filter:
                    if kind != kind_filter:
                        continue
                if nb in visited:
                    continue
                if node_type_filter:
                    props = self._g.get_vertex(nb)
                    if props is None or props.get("type") != node_type_filter:
                        continue
                visited[nb] = depth + 1
                queue.append(nb)
                # 语义归一化：up 方向时边为 nb -> cur（入边），路径展示为正
                if direction == "up":
                    paths.append((depth + 1, nb, cur, kind))
                else:
                    paths.append((depth + 1, cur, nb, kind))
                if len(paths) >= max_results:
                    return self._render_trace(start_id, visited, paths)

        return self._render_trace(start_id, visited, paths)

    def _render_trace(self, start_id, visited, paths) -> dict:
        nodes = []
        seen = {start_id}  # 起点先去重，paths 里可能再次扫到
        # 起点排最前（仅当存在）
        start_props = self._g.get_vertex(start_id)
        if start_props is not None:
            nodes.append({
                "id": start_props.get("id"),
                "label": start_props.get("label"),
                "type": start_props.get("type"),
                "summary": start_props.get("summary", ""),
                "depth": 0,
            })
        for (_depth, frm, to, _kind) in paths:
            for vid in (frm, to):
                if vid in seen:
                    continue
                seen.add(vid)
                props = self._g.get_vertex(vid)
                if props is None or props.get("status") != "live":
                    continue
                if props.get("type") == "project_root":
                    continue
                nodes.append({
                    "id": props.get("id"),
                    "label": props.get("label"),
                    "type": props.get("type"),
                    "summary": props.get("summary", ""),
                    "depth": visited.get(vid, 0),
                })
        return {
            "start": start_id,
            "direction": self._direction,
            "nodes": nodes,
            "paths": paths,
            "total_nodes": len(nodes),
        }

    # ── misc ──────────────────────────────────────────

    def stats(self) -> dict:
        vertices = self._iter_all_vertices()
        live = [v for v in vertices.values() if v.get("status") == "live"]
        by_type = {}
        for v in live:
            t = v.get("type", "?")
            by_type[t] = by_type.get(t, 0) + 1
        try:
            edge_count = self._g._g.edge_count()
        except Exception:
            edge_count = 0
        return {
            "vertices": len(live),
            "edges": edge_count,
            "by_type": by_type,
            "path": self._path,
        }

    def close(self):
        try:
            self._g.close()
        except Exception:
            pass
