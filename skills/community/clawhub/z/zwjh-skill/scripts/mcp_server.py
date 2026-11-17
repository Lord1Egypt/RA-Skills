# -*- coding: utf-8 -*-
"""
MCP (Model Context Protocol) 服务器 —— 跨 skill 记忆总线 v2.6.0。

把 zwjh-skill 的核心能力暴露为 7 个 MCP Tool，让其他 skill / Agent 直接调用：
  - zwjh_query:        语义检索长期记忆
  - zwjh_deposit:      沉淀知识点到记忆底座
  - zwjh_health:       获取记忆健康度报告
  - zwjh_graph_query:  知识图谱查询（实体/关系/事实）
  - zwjh_timeline:     时间线检索
  - zwjh_forget:       遗忘（软删除）指定记忆
  - zwjh_export_stream: 流式导出记忆（分批返回，避免内存爆炸）

另支持 mcp_version 协商（tools/list 附赠版本元数据）。

协议: MCP over stdio (JSON-RPC 2.0)
零依赖: 纯 Python 标准库实现，不引入任何第三方包。

启动方式: python scripts/mcp_server.py
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any

# 确保能 import 同级模块
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
if SKILL_DIR not in sys.path:
    sys.path.insert(0, SKILL_DIR)

from scripts import retrieval, deposit, health, store, graph, export


# ── MCP 协议常量 ────────────────────────────────────────────────────────────
MCP_VERSION = "2024-11-05"
SERVER_VERSION = "2.6.0"
SERVER_NAME = "zwjh-skill"

# 错误码
ERR_INVALID_PARAMS = -32602
ERR_INTERNAL = -32603
ERR_NOT_FOUND = -32001
ERR_WRITE_CONFLICT = -32002
ERR_PERMISSION_DENIED = -32003


# ── MCP 消息构建 ────────────────────────────────────────────────────────────
def _rpc_result(request_id: Any, result: dict) -> dict:
    """构建 JSON-RPC 成功响应。"""
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def _rpc_error(request_id: Any, code: int, message: str) -> dict:
    """构建 JSON-RPC 错误响应。"""
    return {"jsonrpc": "2.0", "id": request_id,
            "error": {"code": code, "message": message}}


def _tool_result(content: str, is_error: bool = False,
                 structured: dict | None = None) -> dict:
    """构建 MCP tool 调用结果。"""
    r: dict = {"content": [{"type": "text", "text": content}],
               "isError": is_error}
    if structured is not None:
        r["structuredContent"] = structured
    return r


# ── MCP Tool 定义 ──────────────────────────────────────────────────────────
TOOL_LIST: list[dict] = [
    {
        "name": "zwjh_query",
        "description": "语义检索长期记忆。输入问题/关键词，返回最相关的记忆片段（含日期、来源、相似度、命中理由）。纯本地、零密钥。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "question": {"type": "string", "description": "要搜索的问题或关键词"},
                "top_k": {"type": "integer", "description": "返回结果数量（1-20，默认 8）", "default": 8},
            },
            "required": ["question"],
        },
    },
    {
        "name": "zwjh_deposit",
        "description": "沉淀一段文本到长期记忆底座。自动去重、事实抽取、关系建立。支持命名空间隔离。返回抽取到的事实和冲突信息。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "要沉淀的文本内容"},
                "source": {"type": "string", "description": "来源标识（默认 conversation）", "default": "conversation"},
                "namespace": {"type": "string", "description": "命名空间（默认 public），用于权限隔离", "default": "public"},
            },
            "required": ["text"],
        },
    },
    {
        "name": "zwjh_health",
        "description": "获取记忆底座健康度报告。包含：记忆数/实体数/关系数/健康度评分(0-100)/DB体积/硬件档位/归档统计。",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "zwjh_graph_query",
        "description": "查询知识图谱。支持：search（按名称搜索实体）、entity（获取实体详情含关系）、facts（获取实体事实）、path（两实体最短路径）。纯本地、零密钥。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "查询动作",
                    "enum": ["search", "entity", "facts", "path"],
                },
                "name": {"type": "string", "description": "实体名称（search/facts 用）"},
                "entity_id": {"type": "integer", "description": "实体 ID（entity/facts 用）"},
                "from_name": {"type": "string", "description": "起始实体名（path 用）"},
                "to_name": {"type": "string", "description": "目标实体名（path 用）"},
                "limit": {"type": "integer", "description": "返回数量上限（默认 20）", "default": 20},
            },
            "required": ["action"],
        },
    },
    {
        "name": "zwjh_timeline",
        "description": "时间线检索。按日期区间 + 关键词过滤记忆，还原「某段时间发生了什么」。纯本地、零密钥。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "from_day": {"type": "string", "description": "起始日期（YYYY-MM-DD）"},
                "to_day": {"type": "string", "description": "结束日期（YYYY-MM-DD）"},
                "keyword": {"type": "string", "description": "关键词过滤（可选）"},
                "limit": {"type": "integer", "description": "返回数量上限（默认 50）", "default": 50},
            },
        },
    },
    {
        "name": "zwjh_forget",
        "description": "遗忘（软删除）指定记忆。支持按 memory_id 单条删除或按 day 批量删除某天记忆。删除的记忆移入 archive 表可恢复。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "memory_id": {"type": "integer", "description": "要遗忘的记忆 ID"},
                "day": {"type": "string", "description": "要遗忘的日期（YYYY-MM-DD，批量删除该天所有记忆）"},
                "reason": {"type": "string", "description": "遗忘原因（可选，审计用）"},
            },
        },
    },
    {
        "name": "zwjh_export_stream",
        "description": "流式导出记忆（分批返回，避免大内存占用）。支持格式：json / markdown / csv。每批最多 batch_size 条。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "format": {"type": "string", "description": "导出格式", "enum": ["json", "markdown", "csv"]},
                "batch_size": {"type": "integer", "description": "每批条数（默认 50，最大 200）", "default": 50},
                "day_from": {"type": "string", "description": "起始日期过滤（可选）"},
                "day_to": {"type": "string", "description": "结束日期过滤（可选）"},
            },
            "required": ["format"],
        },
    },
]


# ── MCP Tool 实现 ──────────────────────────────────────────────────────────

def _handle_zwjh_query(arguments: dict) -> dict:
    """处理 zwjh_query tool 调用。"""
    question = arguments.get("question", "")
    if not question:
        return _tool_result("错误：缺少 question 参数", is_error=True)
    top_k = min(max(int(arguments.get("top_k", 8)), 1), 20)

    hits = retrieval.semantic_search(question, top_k=top_k)
    if not hits:
        return _tool_result("未找到与「%s」相关的记忆。" % question)

    lines = []
    for h in hits:
        exp = h.get("explanation", {})
        exp_str = ""
        if exp:
            exp_str = " [语义:%.2f 关键词:%.2f 时间:%.2f]" % (
                exp.get("semantic", 0), exp.get("keyword", 0), exp.get("time", 0))
        lines.append("[%s · %s · %.4f%s] %s" % (
            h["day"], h["source"], h["score"], exp_str, h["snippet"]))

    return _tool_result("找到 %d 条相关记忆：\n\n%s" % (len(lines), "\n\n".join(lines)))


def _handle_zwjh_deposit(arguments: dict) -> dict:
    """处理 zwjh_deposit tool 调用。"""
    text = arguments.get("text", "")
    if not text:
        return _tool_result("错误：缺少 text 参数", is_error=True)
    source = arguments.get("source", "conversation")
    namespace = arguments.get("namespace", "public")

    r = deposit.deposit_text(text, source=source, namespace=namespace)
    lines = ["沉淀完成："]
    lines.append("  状态：%s" % r.get("status", "?"))
    if r.get("memory_id"):
        lines.append("  记忆ID：%d" % r["memory_id"])
    if r.get("facts"):
        lines.append("  抽取到 %d 个事实：" % len(r["facts"]))
        for f in r["facts"]:
            lines.append("    - %s 的 %s 是 %s" % (
                f.get("entity", "?"), f.get("predicate", "?"), f.get("value", "?")))
    if r.get("relations"):
        lines.append("  建立 %d 个关系" % len(r["relations"]))
    if r.get("namespace"):
        lines.append("  命名空间：%s" % r["namespace"])
    conflict = r.get("conflict")
    if conflict:
        lines.append("  ⚠️ 检测到冲突 → %s" % r.get("conflict_resolution", "待仲裁"))
    if r.get("error"):
        lines.append("  ❌ 错误：%s" % r["error"])
    return _tool_result("\n".join(lines))


def _handle_zwjh_health(arguments: dict) -> dict:
    """处理 zwjh_health tool 调用。"""
    h = health.audit()
    lines = [
        "记忆健康度报告",
        "=" * 30,
        "  记忆条目 : %d" % h.get("memories", 0),
        "  实体数   : %d" % h.get("entities", 0),
        "  关系数   : %d" % h.get("relations", 0),
        "  健康度   : %.1f / 100" % h.get("score", 0),
        "  DB 体积  : %.2f MB" % h.get("db_size_mb", 0),
        "  硬件档位 : %s" % h.get("tier", "?"),
    ]
    if h.get("stale_memories"):
        lines.append("  ⚠️ 陈旧记忆 : %d 条" % h["stale_memories"])
    if h.get("orphan_entities"):
        lines.append("  ⚠️ 孤儿实体 : %d 个" % h["orphan_entities"])
    if h.get("conflicting_facts"):
        lines.append("  ⚠️ 冲突事实 : %d 条" % h["conflicting_facts"])
    if h.get("archived_memories"):
        lines.append("  归档记忆 : %d 条" % h["archived_memories"])
    return _tool_result("\n".join(lines))


def _handle_zwjh_graph_query(arguments: dict) -> dict:
    """处理 zwjh_graph_query tool 调用。"""
    action = arguments.get("action", "")
    if not action:
        return _tool_result("错误：缺少 action 参数", is_error=True)

    if action == "search":
        name = arguments.get("name", "")
        if not name:
            return _tool_result("错误：缺少 name 参数", is_error=True)
        limit = min(max(int(arguments.get("limit", 20)), 1), 100)
        results = store.search_entities_by_name(name, limit=limit)
        if not results:
            return _tool_result("未找到包含「%s」的实体。" % name)
        lines = ["找到 %d 个实体：" % len(results)]
        for e in results:
            lines.append("  [%s] %s (id=%d, 重要度=%.1f)" % (
                e["type"], e["name"], e["id"], e["importance"]))
        return _tool_result("\n".join(lines), structured={"entities": results})

    elif action == "entity":
        eid = arguments.get("entity_id")
        if eid is None:
            return _tool_result("错误：缺少 entity_id 参数", is_error=True)
        conn = store.get_conn()
        row = conn.execute("SELECT * FROM entities WHERE id=?", (eid,)).fetchone()
        if not row:
            return _tool_result("实体 #%d 不存在。" % eid, is_error=True)
        ent = dict(row)
        rels = store.relations_of(eid, direction="both")
        facts = store.current_facts(eid)
        lines = ["实体详情：%s [%s] (id=%d)" % (ent["name"], ent["type"], ent["id"])]
        if facts:
            lines.append("\n事实：")
            for f in facts:
                lines.append("  - %s = %s" % (f["predicate"], f["value"]))
        if rels:
            lines.append("\n关系：")
            for r in rels:
                if r.get("to_name") and r["from_id"] == eid:
                    lines.append("  → %s --%s--> %s" % (
                        ent["name"], r["relation"], r["to_name"]))
                elif r.get("from_name") and r["to_id"] == eid:
                    lines.append("  ← %s --%s--> %s" % (
                        r["from_name"], r["relation"], ent["name"]))
        return _tool_result("\n".join(lines),
                           structured={"entity": ent, "relations": rels, "facts": facts})

    elif action == "facts":
        eid = arguments.get("entity_id")
        name = arguments.get("name")
        if eid is None and not name:
            return _tool_result("错误：缺少 entity_id 或 name 参数", is_error=True)
        if name and eid is None:
            ent = store.find_entity(None, name)
            if not ent:
                return _tool_result("实体「%s」不存在。" % name, is_error=True)
            eid = ent["id"]
        facts = store.current_facts(int(eid))
        if not facts:
            return _tool_result("实体 #%d 暂无事实记录。" % int(eid))
        lines = ["实体 #%d 的当前事实：" % int(eid)]
        for f in facts:
            lines.append("  - %s = %s" % (f["predicate"], f["value"]))
        return _tool_result("\n".join(lines), structured={"facts": facts})

    elif action == "path":
        from_name = arguments.get("from_name", "")
        to_name = arguments.get("to_name", "")
        if not from_name or not to_name:
            return _tool_result("错误：缺少 from_name 或 to_name 参数", is_error=True)
        path_result = graph.find_shortest_path(from_name, to_name)
        if not path_result:
            return _tool_result("未找到「%s」到「%s」的路径。" % (from_name, to_name))
        return _tool_result(path_result["text"], structured=path_result)

    else:
        return _tool_result("未知 action: %s" % action, is_error=True)


def _handle_zwjh_timeline(arguments: dict) -> dict:
    """处理 zwjh_timeline tool 调用。"""
    from_day = arguments.get("from_day")
    to_day = arguments.get("to_day")
    keyword = arguments.get("keyword")
    limit = min(max(int(arguments.get("limit", 50)), 1), 200)

    hits = retrieval.timeline_search(from_day, to_day, keyword=keyword, limit=limit)
    if not hits:
        rng = "%s ~ %s" % (from_day or "最早", to_day or "最新")
        return _tool_result("时间线 [%s] 内未找到相关记忆。" % rng)

    lines = ["时间线 %s ~ %s（共 %d 条）：" % (
        from_day or "最早", to_day or "最新", len(hits))]
    for h in hits:
        lines.append("[%s · %s] %s" % (h["day"], h["source"], h["snippet"]))
    return _tool_result("\n".join(lines), structured={"timeline": hits})


def _handle_zwjh_forget(arguments: dict) -> dict:
    """处理 zwjh_forget tool 调用。"""
    memory_id = arguments.get("memory_id")
    day = arguments.get("day")
    reason = arguments.get("reason", "MCP forget request")

    if memory_id is None and not day:
        return _tool_result("错误：需要 memory_id 或 day 参数", is_error=True)

    conn = store.get_conn()
    now = __import__("datetime").datetime.now().isoformat(timespec="seconds")

    if memory_id is not None:
        # 单条软删除
        row = conn.execute("SELECT * FROM memories WHERE id=?", (memory_id,)).fetchone()
        if not row:
            return _tool_result("记忆 #%d 不存在。" % memory_id, is_error=True)
        d = dict(row)
        # 移入 archive 表（幂等：重复归档跳过）
        existing = conn.execute("SELECT id FROM memories_archive WHERE original_id=?",
                                (memory_id,)).fetchone()
        if not existing:
            conn.execute(
                """INSERT INTO memories_archive(original_id, day, source, raw_text,
                   norm_hash, tokens_json, importance, archived_at, reason)
                   VALUES(?,?,?,?,?,?,?,?,?)""",
                (memory_id, d["day"], d["source"], d["raw_text"], d["norm_hash"],
                 d["tokens_json"], d["importance"], now, reason))
        conn.execute("DELETE FROM memories WHERE id=?", (memory_id,))
        conn.commit()
        return _tool_result("已遗忘记忆 #%d（%s · %s）。归档可恢复。" % (
            memory_id, d["day"], d["source"]),
            structured={"forgotten_id": memory_id, "archived": True})

    if day:
        # 按日期批量删除
        rows = conn.execute("SELECT * FROM memories WHERE day=?", (day,)).fetchall()
        if not rows:
            return _tool_result("日期 %s 没有记忆。" % day)
        count = 0
        for row in rows:
            d = dict(row)
            existing = conn.execute("SELECT id FROM memories_archive WHERE original_id=?",
                                    (d["id"],)).fetchone()
            if not existing:
                conn.execute(
                    """INSERT INTO memories_archive(original_id, day, source, raw_text,
                       norm_hash, tokens_json, importance, archived_at, reason)
                       VALUES(?,?,?,?,?,?,?,?,?)""",
                    (d["id"], d["day"], d["source"], d["raw_text"], d["norm_hash"],
                     d["tokens_json"], d["importance"], now, reason))
            conn.execute("DELETE FROM memories WHERE id=?", (d["id"],))
            count += 1
        conn.commit()
        return _tool_result("已遗忘 %s 的 %d 条记忆。归档可恢复。" % (day, count),
                            structured={"forgotten_day": day, "count": count})


def _handle_zwjh_export_stream(arguments: dict) -> dict:
    """处理 zwjh_export_stream tool 调用。"""
    fmt = arguments.get("format", "")
    if fmt not in ("json", "markdown", "csv"):
        return _tool_result("错误：format 必须是 json / markdown / csv", is_error=True)
    batch_size = min(max(int(arguments.get("batch_size", 50)), 1), 200)
    day_from = arguments.get("day_from")
    day_to = arguments.get("day_to")

    rows = store.list_memories(day_from=day_from, day_to=day_to, limit=100000, offset=0)
    if not rows:
        return _tool_result("没有可导出的记忆。")

    # 取第一批
    batch = rows[:batch_size]
    remaining = len(rows) - len(batch)

    if fmt == "json":
        content = json.dumps(batch, ensure_ascii=False, indent=2)
    elif fmt == "markdown":
        lines = ["# 记忆导出\n\n共 %d 条\n" % len(rows)]
        for r in batch:
            lines.append("## [%s] %s (id=%d)\n\n%s\n" % (
                r["day"], r["source"], r["id"], r["raw_text"]))
        content = "\n".join(lines)
    else:  # csv
        lines = ["id,day,source,importance,raw_text"]
        for r in batch:
            txt = r["raw_text"].replace('"', '""').replace('\n', ' ')
            lines.append('%d,%s,%s,%.2f,"%s"' % (
                r["id"], r["day"], r["source"], r["importance"], txt))
        content = "\n".join(lines)

    msg = "第 1 批（%d 条）" % len(batch)
    if remaining > 0:
        msg += "，剩余 %d 条未导出（缩小日期范围或分批请求）" % remaining

    return _tool_result("%s\n\n%s" % (msg, content),
                        structured={"batch_count": len(batch),
                                    "total": len(rows), "remaining": remaining})


# Tool 名称到处理函数的映射
TOOL_HANDLERS = {
    "zwjh_query": _handle_zwjh_query,
    "zwjh_deposit": _handle_zwjh_deposit,
    "zwjh_health": _handle_zwjh_health,
    "zwjh_graph_query": _handle_zwjh_graph_query,
    "zwjh_timeline": _handle_zwjh_timeline,
    "zwjh_forget": _handle_zwjh_forget,
    "zwjh_export_stream": _handle_zwjh_export_stream,
}


# ── MCP 消息处理 ────────────────────────────────────────────────────────────

def _handle_initialize(request_id: Any, params: dict) -> dict:
    """处理 initialize 请求。"""
    client_version = params.get("protocolVersion", "")
    # 版本协商：服务端支持 MCP 2024-11-05，客户端版本不匹配时仍兼容
    negotiated = MCP_VERSION
    warnings: list[str] = []
    if client_version and client_version != MCP_VERSION:
        warnings.append(
            "客户端协议版本 %s 与服务端 %s 不同，已协商使用 %s" % (
                client_version, MCP_VERSION, negotiated))
    result: dict = {
        "protocolVersion": negotiated,
        "capabilities": {"tools": {}},
        "serverInfo": {
            "name": SERVER_NAME,
            "version": SERVER_VERSION,
            "description": "跨 skill 记忆总线 v%s（长期记忆 + 知识图谱 + 健康度 + 权限隔离 + 并发门禁）" % SERVER_VERSION,
        },
    }
    if warnings:
        result["warnings"] = warnings
    return _rpc_result(request_id, result)


def _handle_tools_list(request_id: Any) -> dict:
    """处理 tools/list 请求。附赠版本元数据。"""
    meta = {"serverVersion": SERVER_VERSION, "toolCount": len(TOOL_LIST)}
    return _rpc_result(request_id, {"tools": TOOL_LIST, **meta})


def _handle_tools_call(request_id: Any, params: dict) -> dict:
    """处理 tools/call 请求。"""
    tool_name = params.get("name", "")
    arguments = params.get("arguments", {})

    handler = TOOL_HANDLERS.get(tool_name)
    if not handler:
        return _rpc_error(request_id, -32601, "未知 tool: %s" % tool_name)

    try:
        result = handler(arguments)
        return _rpc_result(request_id, result)
    except Exception as e:
        return _rpc_error(request_id, ERR_INTERNAL, "%s" % str(e))


def _handle_request(request: dict) -> dict | None:
    """处理单个 JSON-RPC 请求。返回 None 表示是 notification（无需响应）。"""
    if not isinstance(request, dict):
        return None

    request_id = request.get("id")
    method = request.get("method", "")
    params = request.get("params", {})

    if method == "initialize":
        return _handle_initialize(request_id, params)
    elif method == "notifications/initialized":
        return None
    elif method == "tools/list":
        return _handle_tools_list(request_id)
    elif method == "tools/call":
        return _handle_tools_call(request_id, params)
    elif method == "ping":
        return _rpc_result(request_id, {})
    else:
        if request_id is not None:
            return _rpc_error(request_id, -32601, "未知方法: %s" % method)
        return None


# ── stdio 读写 ─────────────────────────────────────────────────────────────
def _read_message() -> dict | None:
    """从 stdin 读取一行 JSON-RPC 消息。"""
    line = sys.stdin.readline()
    if not line:
        return None
    line = line.strip()
    if not line:
        return None
    try:
        return json.loads(line)
    except json.JSONDecodeError:
        return None


def _send_message(msg: dict) -> None:
    """发送 JSON-RPC 消息到 stdout。"""
    body = json.dumps(msg, ensure_ascii=False, default=str)
    sys.stdout.write(body + "\n")
    sys.stdout.flush()


# ── 主循环 ──────────────────────────────────────────────────────────────────
def run() -> None:
    """运行 MCP 服务器（stdio 模式主循环）。"""
    while True:
        request = _read_message()
        if request is None:
            break

        if isinstance(request, list):
            for req in request:
                response = _handle_request(req)
                if response is not None:
                    _send_message(response)
        else:
            response = _handle_request(request)
            if response is not None:
                _send_message(response)


if __name__ == "__main__":
    run()
