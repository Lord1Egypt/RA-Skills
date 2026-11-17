# -*- coding: utf-8 -*-
"""
知识图谱 Web 可视化服务器 —— 零依赖，Python 标准库 http.server。

提供 REST API + 静态前端文件服务。
启动方式：python scripts/web_server.py [--port 8080]

API 端点：
  GET /api/graph?type=&relation=&from=&to=&limit=&offset=  图谱数据（过滤+分页）
  GET /api/entity/{id}                                         实体详情+关联
  GET /api/path?from={id}&to={id}                              最短路径（BFS）
  GET /api/timeline/{entity_id}                                实体时间线
  GET /api/stats                                               图谱统计
  GET /api/search?q={keyword}                                  搜索实体
  GET /api/neighbors/{id}?depth=2                              邻居节点（分层加载）
  GET /api/types                                               实体类型列表
  GET /                                                       静态前端文件
"""

from __future__ import annotations

import json
import os
import re
import sys
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from collections import deque
from datetime import datetime, timedelta

# 确保能 import 同级模块
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SKILL_DIR)

from scripts import store, graph, config, archive, health, setup

# ── 大规模图谱优化阈值 ────────────────────────────────────────────────────
CORE_IMPORTANCE = 0.7     # 默认只加载 importance > 此值的核心节点
MAX_GRAPH_NODES = 300    # 超过此数量启用聚合
MAX_GRAPH_LINKS = 1000   # 超过此数量启用分页
NEIGHBOR_BATCH = 30      # 邻居分批返回数量


class GraphAPI:
    """API 处理逻辑（与 HTTP 解耦，便于单测）。"""

    @staticmethod
    def _json_response(data: dict | list, status: int = 200) -> tuple:
        body = json.dumps(data, ensure_ascii=False, default=str).encode("utf-8")
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Content-Length": str(len(body)),
            "Access-Control-Allow-Origin": "*",
            "Cache-Control": "no-store",
        }
        return status, headers, body

    @staticmethod
    def _err(message: str, status: int = 400) -> tuple:
        return GraphAPI._json_response({"error": message}, status)

    # ── 图谱数据 ─────────────────────────────────────────────────────────
    def get_graph(self, params: dict) -> tuple:
        type_filter = params.get("type", [None])[0]
        relation_filter = params.get("relation", [None])[0]
        importance_min = float(params.get("importance_min", [0])[0])
        limit = min(int(params.get("limit", [200])[0]), MAX_GRAPH_NODES)
        offset = max(int(params.get("offset", [0])[0]), 0)

        # 加载实体
        entities = store.list_entities(limit=5000)
        if type_filter:
            entities = [e for e in entities if e["type"] == type_filter]
        if importance_min > 0:
            entities = [e for e in entities if e["importance"] >= importance_min]

        # 分页
        total = len(entities)
        entities_page = entities[offset:offset + limit]

        # 加载关系（只包含当前页实体的关系）
        entity_ids = {e["id"] for e in entities_page}
        links = []
        seen_links = set()
        for e in entities_page:
            for r in store.relations_of(e["id"], direction="out"):
                if r["to_id"] in entity_ids:
                    key = (e["id"], r["to_id"], r["relation"])
                    if key in seen_links:
                        continue
                    seen_links.add(key)
                    if relation_filter and r["relation"] != relation_filter:
                        continue
                    links.append({
                        "source": e["id"],
                        "target": r["to_id"],
                        "relation": r["relation"],
                        "weight": r.get("weight", 1.0),
                        "confidence": r.get("confidence", 1.0),
                    })
                    if len(links) >= MAX_GRAPH_LINKS:
                        break
            if len(links) >= MAX_GRAPH_LINKS:
                break

        # 大规模聚合：节点数 > 阈值时按类型聚类
        nodes = [
            {"id": e["id"], "name": e["name"], "type": e["type"],
             "importance": e["importance"], "value": e["importance"] * 10}
            for e in entities_page
        ]

        return self._json_response({
            "nodes": nodes,
            "links": links,
            "total": total,
            "returned": len(nodes),
            "aggregated": total > MAX_GRAPH_NODES,
        })

    # ── 实体详情 ─────────────────────────────────────────────────────────
    def get_entity(self, entity_id: int) -> tuple:
        conn = store.get_conn()
        row = conn.execute("SELECT * FROM entities WHERE id=?", (entity_id,)).fetchone()
        if not row:
            return self._err("实体不存在", 404)
        e = dict(row)
        e["aliases"] = json.loads(e.get("aliases_json", "[]"))
        e["relations"] = store.relations_of(entity_id, direction="both")
        e["facts"] = store.current_facts(entity_id)
        return self._json_response(e)

    # ── 最短路径（BFS） ─────────────────────────────────────────────────
    def get_path(self, params: dict) -> tuple:
        try:
            from_id = int(params.get("from", [0])[0])
            to_id = int(params.get("to", [0])[0])
        except (ValueError, TypeError):
            return self._err("from/to 必须为实体 ID（整数）", 400)
        if not from_id or not to_id:
            return self._err("缺少 from 或 to 参数", 400)
        if from_id == to_id:
            return self._json_response({"path": [], "distance": 0})

        # BFS（带深度限制）
        MAX_DEPTH = 6
        visited = {from_id}
        queue = deque([(from_id, [])])
        while queue:
            cur_id, path = queue.popleft()
            if len(path) >= MAX_DEPTH:
                continue
            conn = store.get_conn()
            rows = conn.execute(
                "SELECT r.to_id, r.relation, e.name AS to_name FROM relations r "
                "JOIN entities e ON e.id=r.to_id WHERE r.from_id=?", (cur_id,)
            ).fetchall()
            for r in rows:
                nid = r["to_id"]
                new_path = path + [{"from": cur_id, "to": nid,
                                    "relation": r["relation"], "to_name": r["to_name"]}]
                if nid == to_id:
                    return self._json_response({"path": new_path, "distance": len(new_path)})
                if nid not in visited:
                    visited.add(nid)
                    queue.append((nid, new_path))
        return self._json_response({"path": [], "distance": -1, "msg": "无关联路径"})

    # ── 时间线 ─────────────────────────────────────────────────────────
    def get_timeline(self, entity_id: int) -> tuple:
        conn = store.get_conn()
        row = conn.execute("SELECT * FROM entities WHERE id=?", (entity_id,)).fetchone()
        if not row:
            return self._err("实体不存在", 404)
        e = dict(row)

        facts = store.current_facts(entity_id)
        # 按时间排列的事实变更
        events = []
        for f in facts:
            events.append({
                "date": f.get("valid_from", "")[:10],
                "type": "fact",
                "predicate": f["predicate"],
                "value": f["value"],
            })

        # 关系创建时间线
        conn = store.get_conn()
        rel_rows = conn.execute(
            "SELECT r.*, e.name AS other_name FROM relations r "
            "JOIN entities e ON e.id = CASE WHEN r.from_id=? THEN r.to_id ELSE r.from_id END "
            "WHERE r.from_id=? OR r.to_id=? ORDER BY r.created_at",
            (entity_id, entity_id, entity_id)
        ).fetchall()
        for r in rel_rows:
            events.append({
                "date": (r["created_at"] or "")[:10],
                "type": "relation",
                "relation": r["relation"],
                "other_name": r["other_name"],
            })

        events.sort(key=lambda x: x.get("date", ""), reverse=True)
        return self._json_response({
            "entity": {"id": e["id"], "name": e["name"], "type": e["type"]},
            "events": events,
            "total": len(events),
        })

    # ── 统计 ───────────────────────────────────────────────────────────
    def get_stats(self) -> tuple:
        conn = store.get_conn()
        # 实体类型分布
        type_counts = {}
        for t in config.ENTITY_TYPES:
            cnt = conn.execute("SELECT COUNT(*) FROM entities WHERE type=?", (t,)).fetchone()[0]
            if cnt:
                type_counts[t] = cnt
        # 关系类型分布
        rel_types = {}
        rows = conn.execute("SELECT relation, COUNT(*) as cnt FROM relations GROUP BY relation ORDER BY cnt DESC").fetchall()
        for r in rows:
            rel_types[r["relation"]] = r["cnt"]

        return self._json_response({
            "entities_total": store.count_entities(),
            "relations_total": store.count_relations(),
            "memories_total": store.count_memories(),
            "type_distribution": type_counts,
            "relation_distribution": rel_types,
        })

    # ── 搜索 ───────────────────────────────────────────────────────────
    def search(self, params: dict) -> tuple:
        q = params.get("q", [""])[0].strip()
        limit = min(int(params.get("limit", [20])[0]), 50)
        if not q:
            return self._err("缺少搜索词 q", 400)
        results = store.search_entities_by_name(q, limit=limit)
        return self._json_response({"query": q, "results": results, "count": len(results)})

    # ── 邻居（分层加载） ─────────────────────────────────────────────
    def get_neighbors(self, entity_id: int, params: dict) -> tuple:
        depth = min(int(params.get("depth", [1])[0]), 3)
        batch = min(int(params.get("batch", [NEIGHBOR_BATCH])[0]), 100)
        offset = max(int(params.get("offset", [0])[0]), 0)

        conn = store.get_conn()
        row = conn.execute("SELECT * FROM entities WHERE id=?", (entity_id,)).fetchone()
        if not row:
            return self._err("实体不存在", 404)

        # BFS 收集邻居
        visited = {entity_id}
        frontier = {entity_id}
        for _ in range(depth):
            new_frontier = set()
            for fid in list(frontier)[:50]:  # 限制每层广度，避免爆炸
                rows = conn.execute(
                    "SELECT to_id FROM relations WHERE from_id=? UNION "
                    "SELECT from_id FROM relations WHERE to_id=?",
                    (fid, fid)
                ).fetchall()
                for r in rows:
                    nid = r[0]
                    if nid not in visited:
                        visited.add(nid)
                        new_frontier.add(nid)
            frontier = new_frontier

        # 分页返回邻居实体
        neighbor_ids = list(visited - {entity_id})
        total = len(neighbor_ids)
        page_ids = neighbor_ids[offset:offset + batch]
        nodes = []
        for nid in page_ids:
            nr = conn.execute("SELECT * FROM entities WHERE id=?", (nid,)).fetchone()
            if nr:
                nodes.append({"id": nr["id"], "name": nr["name"],
                              "type": nr["type"], "importance": nr["importance"]})

        # 邻居之间的链接
        id_set = set(page_ids) | {entity_id}
        links = []
        for nid in page_ids:
            for r in store.relations_of(nid, direction="out"):
                if r["to_id"] in id_set:
                    links.append({"source": nid, "target": r["to_id"],
                                  "relation": r["relation"], "weight": r.get("weight", 1.0)})

        return self._json_response({
            "entity_id": entity_id,
            "depth": depth,
            "total": total,
            "nodes": nodes,
            "links": links,
            "has_more": offset + batch < total,
        })

    # ── 任务状态面板 ──────────────────────────────────────────────────
    def get_task_status(self) -> tuple:
        """获取定时任务状态 + 系统健康度。"""
        setup_status = setup.status()
        health_report = health.audit()
        archive_stats = archive.get_archive_stats()
        return self._json_response({
            "setup": setup_status,
            "health": health_report,
            "archive": archive_stats,
        })

    # ── 归档统计 ──────────────────────────────────────────────────────
    def get_archive_stats(self) -> tuple:
        """获取归档统计。"""
        return self._json_response(archive.get_archive_stats())

    # ── 实体类型列表 ─────────────────────────────────────────────────
    def get_types(self) -> tuple:
        return self._json_response({"types": config.ENTITY_TYPES})


# ── HTTP 处理器 ──────────────────────────────────────────────────────────

class Handler(BaseHTTPRequestHandler):
    """路由分发。"""
    api = GraphAPI()
    # 前端静态文件目录（相对于本脚本）
    WEB_UI_DIR = os.path.join(SKILL_DIR, "web_ui")

    def log_message(self, format, *args):
        # 静默日志
        pass

    def _send(self, status: int, headers: dict, body: bytes) -> None:
        self.send_response(status)
        for k, v in headers.items():
            self.send_header(k, v)
        self.end_headers()
        if body:
            self.wfile.write(body)

    def _send_json(self, data: dict | list, status: int = 200) -> None:
        s, h, b = self.api._json_response(data, status)
        self._send(s, h, b)

    def _send_file(self, path: str, content_type: str) -> None:
        try:
            with open(path, "rb") as f:
                body = f.read()
            headers = {"Content-Type": content_type, "Content-Length": str(len(body))}
            self._send(200, headers, body)
        except FileNotFoundError:
            self._send_json({"error": "Not Found"}, 404)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"
        params = parse_qs(parsed.query, keep_blank_values=True)

        # ── API 路由 ─────────────────────────────────────────────────────
        if path == "/api/graph":
            s, h, b = self.api.get_graph(params)
            self._send(s, h, b)
        elif path == "/api/stats":
            s, h, b = self.api.get_stats()
            self._send(s, h, b)
        elif path == "/api/types":
            s, h, b = self.api.get_types()
            self._send(s, h, b)
        elif path.startswith("/api/entity/"):
            try:
                eid = int(path.split("/")[-1])
            except ValueError:
                self._send_json({"error": "实体 ID 必须为整数"}, 400)
                return
            s, h, b = self.api.get_entity(eid)
            self._send(s, h, b)
        elif path == "/api/path":
            s, h, b = self.api.get_path(params)
            self._send(s, h, b)
        elif path.startswith("/api/timeline/"):
            try:
                eid = int(path.split("/")[-1])
            except ValueError:
                self._send_json({"error": "实体 ID 必须为整数"}, 400)
                return
            s, h, b = self.api.get_timeline(eid)
            self._send(s, h, b)
        elif path == "/api/search":
            s, h, b = self.api.search(params)
            self._send(s, h, b)
        elif path.startswith("/api/neighbors/"):
            try:
                eid = int(path.split("/")[-1])
            except ValueError:
                self._send_json({"error": "实体 ID 必须为整数"}, 400)
                return
            s, h, b = self.api.get_neighbors(eid, params)
            self._send(s, h, b)
        elif path == "/api/task-status":
            s, h, b = self.api.get_task_status()
            self._send(s, h, b)
        elif path == "/api/archive-stats":
            s, h, b = self.api.get_archive_stats()
            self._send(s, h, b)

        # ── 静态前端文件 ─────────────────────────────────────────────────
        elif path == "/" or path == "/index.html":
            self._send_file(os.path.join(self.WEB_UI_DIR, "index.html"), "text/html; charset=utf-8")
        elif path == "/css/style.css":
            self._send_file(os.path.join(self.WEB_UI_DIR, "css/style.css"), "text/css; charset=utf-8")
        elif path == "/js/app.js":
            self._send_file(os.path.join(self.WEB_UI_DIR, "js/app.js"), "application/javascript; charset=utf-8")
        else:
            self._send_json({"error": "Not Found"}, 404)


def run_server(port: int = 8080) -> None:
    """启动服务器。"""
    server = HTTPServer(("127.0.0.1", port), Handler)
    print(f"知识图谱可视化已启动: http://127.0.0.1:{port}")
    print(f"前端目录: {Handler.WEB_UI_DIR}")
    print("按 Ctrl+C 停止")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")
        server.server_close()


if __name__ == "__main__":
    port = 8080
    if "--port" in sys.argv:
        idx = sys.argv.index("--port")
        if idx + 1 < len(sys.argv):
            try:
                port = int(sys.argv[idx + 1])
            except ValueError:
                pass
    run_server(port)
