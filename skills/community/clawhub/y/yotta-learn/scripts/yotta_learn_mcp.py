#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""yotta_learn_mcp.py — 元习知识库 MCP server（yotta-learn MCP）。

stdio MCP server（JSON-RPC 2.0，换行分隔），把元习知识库（KB v1）暴露为 MCP
工具：读 kb_query / kb_get / kb_list / kb_stats / kb_categories；写 kb_add /
kb_review / kb_update / kb_deprecate / kb_category_create /
kb_category_rename / kb_category_merge / kb_category_deprecate；运维 kb_doctor /
kb_index_rebuild。

复用 yotta_kb.py / yotta_kb_index.py 内核（与 CLI 同一真源）：
- 写工具 fail-closed：kb_add 默认草稿；kb_review 走同一审核门（证据必填、
  敏感扫描阻断、查重提示）；身份 = agent（author / verified_by）。
- 位置优先级：工具参数 dir > YOTTA_LEARN_KB > ~/.yottalearn/config.json >
  默认（含 0.3.x 旧位置只读兼容）。

运行：python scripts/yotta_learn_mcp.py
MCP 客户端配置：
  {"mcpServers":{"yotta-learn":{"command":"python",
    "args":["<绝对路径>/scripts/yotta_learn_mcp.py"]}}}
"""

import json
import os
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

import yotta_kb  # noqa: E402
import yotta_kb_index  # noqa: E402

VERSION = "0.6.6"
TOOL_NAME = "yotta-learn"
CN_NAME = "元习"
MCP_PROTOCOL_MODERN = "2026-07-28"
MCP_PROTOCOL_LEGACY = "2025-11-25"
SERVER_INFO = {"name": TOOL_NAME, "version": VERSION}


# ── 公共 ────────────────────────────────────────────────────────────────────

def _ok(payload):
    return {"content": [{"type": "text",
                         "text": json.dumps(payload, ensure_ascii=False, indent=2)}],
            "isError": False}


def _tool_error(message, extra=None):
    payload = {"error": message}
    if extra:
        payload.update(extra)
    return {"content": [{"type": "text",
                         "text": json.dumps(payload, ensure_ascii=False, indent=2)}],
            "isError": True}


def _root(params):
    explicit = str(params.get("dir") or "").strip() or None
    root, source = yotta_kb.resolve_kb_root(explicit)
    yotta_kb.load_kb(root)
    return root, source


def _actor(params):
    agent = str(params.get("agent") or os.environ.get("YOTTA_LEARN_AGENT")
                or "mcp").strip() or "mcp"
    return yotta_kb.resolve_actor(agent)


def _as_list(value):
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        out = []
        for item in value:
            out.extend(_as_list(item))
        return out
    return [v.strip() for v in str(value).split(",") if v.strip()]


# ── 读工具 ──────────────────────────────────────────────────────────────────

def _tool_kb_query(params):
    root, source = _root(params)
    keywords = params.get("keywords")
    if keywords is None:
        keywords = params.get("query")
    if isinstance(keywords, (list, tuple)):
        keywords = " ".join(str(k) for k in keywords)
    if not keywords or not str(keywords).strip():
        return _tool_error("kb_query 需要 keywords 参数（关键词或短语）")
    statuses = _as_list(params.get("status")) or None
    result = yotta_kb_index.query(
        root, str(keywords), category=params.get("category"),
        statuses=statuses, tags=_as_list(params.get("tags")),
        limit=int(params.get("limit") or 10),
        include_draft=bool(params.get("include_draft")),
        include_deprecated=bool(params.get("include_deprecated")))
    result["root"] = str(root)
    result["origin"] = source
    return _ok(result)


def _tool_kb_get(params):
    root, source = _root(params)
    eid = str(params.get("id") or "").strip()
    if not eid:
        return _tool_error("kb_get 需要 id 参数（KB-YYYYMMDD-XXX）")
    entry = yotta_kb.find_entry(root, eid)
    if entry is None:
        return _tool_error("未找到条目：%s" % eid, {"id": eid, "root": str(root)})
    data = entry.to_dict(include_body=True)
    data["path"] = str(entry.path)
    data["root"] = str(root)
    data["origin"] = source
    return _ok(data)


def _tool_kb_list(params):
    root, source = _root(params)
    cat_slug = None
    if params.get("category"):
        cat_slug = yotta_kb.resolve_category(root, str(params["category"]))["slug"]
    status = str(params.get("status") or "").strip()
    tags = [t.lower() for t in _as_list(params.get("tags"))]
    entries = []
    for entry in yotta_kb.iter_entries(root, category=cat_slug):
        if status and entry.status != status:
            continue
        if tags and not any(t in [x.lower() for x in entry.tags] for t in tags):
            continue
        entries.append(entry)
    entries.sort(key=lambda e: (e.updated, e.id), reverse=True)
    limit = int(params.get("limit") or 50)
    if limit > 0:
        entries = entries[:limit]
    return _ok({"root": str(root), "origin": source, "count": len(entries),
                "entries": [e.to_dict() for e in entries]})


def _tool_kb_stats(params):
    root, source = _root(params)
    data = yotta_kb_index.stats(root)
    data["origin"] = source
    return _ok(data)


def _tool_kb_categories(params):
    root, source = _root(params)
    cats = yotta_kb.list_categories(root)
    return _ok({"root": str(root), "origin": source, "count": len(cats),
                "categories": cats})


# ── 写工具（fail-closed：草稿 / 审核门 / 敏感扫描与 CLI 同源） ───────────────

def _tool_kb_add(params):
    root, _source = _root(params)
    actor = _actor(params)
    category = str(params.get("category") or "").strip()
    title = str(params.get("title") or "").strip()
    message = params.get("message") or ""
    source = str(params.get("source") or "").strip()
    if not category:
        return _tool_error("kb_add 需要 category 参数（分类 slug）")
    if not title:
        return _tool_error("kb_add 需要 title 参数")
    if not str(message).strip():
        return _tool_error("kb_add 需要 message 参数（正文）")
    entry = yotta_kb.add_entry(
        root, category, title, message, _as_list(params.get("tags")),
        source, params.get("evidence") or "",
        str(params.get("confidence") or "medium"), actor)
    text = "\n".join([entry.title, " ".join(entry.tags), entry.body])
    findings = yotta_kb.scan_sensitive(text)
    similar = yotta_kb.similar_titles(root, entry)
    return _ok({
        "id": entry.id, "path": str(entry.path), "status": entry.status,
        "category": entry.category, "sensitive": findings, "similar": similar,
        "next": ("kb_review --decision pass --evidence <证据>"
                 "（敏感命中需 --force 显式放行）"),
    })


def _tool_kb_review(params):
    root, _source = _root(params)
    actor = _actor(params)
    eid = str(params.get("id") or "").strip()
    decision = str(params.get("decision") or "").strip().lower()
    if not eid:
        return _tool_error("kb_review 需要 id 参数")
    if decision not in ("pass", "reject"):
        return _tool_error("kb_review 的 decision 只能为 pass 或 reject")
    entry, extra = yotta_kb.review_entry(
        root, eid, decision, params.get("note") or "",
        params.get("evidence") or "", actor, force=bool(params.get("force")))
    return _ok({
        "id": entry.id, "status": entry.status, "title": entry.title,
        "decision": decision, "findings": extra.get("findings") or [],
        "similar": extra.get("similar") or [],
    })


def _tool_kb_update(params):
    root, _source = _root(params)
    actor = _actor(params)
    eid = str(params.get("id") or "").strip()
    if not eid:
        return _tool_error("kb_update 需要 id 参数")
    changes = {}
    for key in ("title", "message", "source", "evidence", "confidence"):
        if params.get(key) is not None:
            changes[key] = params[key]
    if params.get("tags") is not None:
        changes["tags"] = _as_list(params.get("tags"))
    if not changes:
        return _tool_error("kb_update 至少需要一个可更新字段"
                           "（title/message/tags/source/evidence/confidence）")
    entry = yotta_kb.update_entry(root, eid, changes, actor)
    return _ok({"id": entry.id, "updated": sorted(changes.keys()),
                "status": entry.status})


def _tool_kb_deprecate(params):
    root, _source = _root(params)
    actor = _actor(params)
    eid = str(params.get("id") or "").strip()
    if not eid:
        return _tool_error("kb_deprecate 需要 id 参数")
    entry = yotta_kb.deprecate_entry(root, eid, params.get("reason") or "", actor)
    return _ok({"id": entry.id, "status": entry.status})


def _tool_kb_category_create(params):
    root, _source = _root(params)
    actor = _actor(params)
    slug = str(params.get("slug") or "").strip()
    name = str(params.get("name") or "").strip()
    description = str(params.get("description") or "").strip()
    if not slug or not name or not description:
        return _tool_error("kb_category_create 需要 slug / name / description 参数")
    cat = yotta_kb.create_category(root, slug, name, description,
                                   _as_list(params.get("aliases")), actor)
    return _ok({"slug": cat["slug"], "name": cat["name"],
                "status": cat.get("status")})


def _tool_kb_category_rename(params):
    root, _source = _root(params)
    actor = _actor(params)
    slug = str(params.get("slug") or "").strip()
    name = str(params.get("name") or "").strip()
    if not slug or not name:
        return _tool_error("kb_category_rename 需要 slug / name 参数")
    cat = yotta_kb.rename_category(root, slug, name, actor)
    return _ok({"slug": cat["slug"], "name": cat["name"],
                "status": cat.get("status")})


def _tool_kb_category_merge(params):
    root, _source = _root(params)
    actor = _actor(params)
    from_slug = str(params.get("from") or "").strip()
    into_slug = str(params.get("into") or "").strip()
    if not from_slug or not into_slug:
        return _tool_error("kb_category_merge 需要 from / into 参数")
    merged = yotta_kb.merge_category(root, from_slug, into_slug, actor)
    return _ok({"from": merged["from"], "into": merged["into"],
                "moved": merged["moved"]})


def _tool_kb_category_deprecate(params):
    root, _source = _root(params)
    actor = _actor(params)
    slug = str(params.get("slug") or "").strip()
    if not slug:
        return _tool_error("kb_category_deprecate 需要 slug 参数")
    force = bool(params.get("force"))
    cat = yotta_kb.deprecate_category(root, slug, actor,
                                      reason=params.get("reason") or "",
                                      force=force)
    return _ok({"slug": cat["slug"], "status": cat.get("status")})


# ── 运维工具 ────────────────────────────────────────────────────────────────

def _tool_kb_doctor(params):
    root, source = _root(params)
    report = yotta_kb.doctor(root, backup_dir=params.get("backup_dir"))
    report["origin"] = source
    return _ok(report)


def _tool_kb_index_rebuild(params):
    root, _source = _root(params)
    actor = _actor(params)
    with yotta_kb.KbLock(root):
        stats = yotta_kb_index.rebuild_all(root)
        yotta_kb.audit(root, actor, "kb.index.rebuild", str(root), "ok",
                       {"entries": stats["total_entries"], "terms": stats["terms"]})
    return _ok({"total_entries": stats["total_entries"], "terms": stats["terms"]})


TOOL_HANDLERS = {
    "kb_query": _tool_kb_query,
    "kb_get": _tool_kb_get,
    "kb_list": _tool_kb_list,
    "kb_stats": _tool_kb_stats,
    "kb_categories": _tool_kb_categories,
    "kb_add": _tool_kb_add,
    "kb_review": _tool_kb_review,
    "kb_update": _tool_kb_update,
    "kb_deprecate": _tool_kb_deprecate,
    "kb_category_create": _tool_kb_category_create,
    "kb_category_rename": _tool_kb_category_rename,
    "kb_category_merge": _tool_kb_category_merge,
    "kb_category_deprecate": _tool_kb_category_deprecate,
    "kb_doctor": _tool_kb_doctor,
    "kb_index_rebuild": _tool_kb_index_rebuild,
}


def _dir_prop():
    return {"type": "string",
            "description": "可选：知识库根目录（默认按 --dir 优先级解析："
                           "YOTTA_LEARN_KB > ~/.yottalearn/config.json > 默认）"}


def _agent_prop():
    return {"type": "string",
            "description": "可选：写入身份 agent（默认 YOTTA_LEARN_AGENT，兜底 mcp）"}


def mcp_tools():
    """返回 MCP tools 列表（name / description / inputSchema）。"""
    return [
        {
            "name": "kb_query",
            "description": ("知识库关键词查询（元习 yotta-learn）。中文 bigram + 单字兜底，"
                            "默认只返回已核验（verified）条目；索引漂移自动降级线性扫描"
                            "（结果附 stale / mode）。"),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "keywords": {"type": "string", "description": "查询关键词或短语（必填）"},
                    "category": {"type": "string", "description": "可选：限定分类 slug"},
                    "tags": {"type": "array", "items": {"type": "string"},
                             "description": "可选：限定标签（任一命中）"},
                    "status": {"type": "string",
                               "description": "可选：限定状态（draft / verified / deprecated，逗号分隔）"},
                    "limit": {"type": "integer", "description": "返回上限（默认 10）"},
                    "include_draft": {"type": "boolean", "description": "包含草稿"},
                    "include_deprecated": {"type": "boolean", "description": "包含已停用"},
                    "dir": _dir_prop(),
                },
                "required": ["keywords"],
            },
        },
        {
            "name": "kb_get",
            "description": "按 ID 读取知识条目全文（含 frontmatter 字段与正文）。",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "条目 ID（KB-YYYYMMDD-XXX）"},
                    "dir": _dir_prop(),
                },
                "required": ["id"],
            },
        },
        {
            "name": "kb_list",
            "description": "列出知识条目（管理视图，可按分类 / 状态 / 标签过滤）。",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "category": {"type": "string", "description": "可选：分类 slug"},
                    "status": {"type": "string", "description": "可选：draft / verified / deprecated"},
                    "tags": {"type": "array", "items": {"type": "string"}, "description": "可选：标签"},
                    "limit": {"type": "integer", "description": "返回上限（默认 50）"},
                    "dir": _dir_prop(),
                },
            },
        },
        {
            "name": "kb_stats",
            "description": "知识库统计（分类 / 条目分布 / 状态 / 回收站 / 索引健康）。",
            "inputSchema": {"type": "object", "properties": {"dir": _dir_prop()}},
        },
        {
            "name": "kb_categories",
            "description": "列出知识库分类（含别名与状态）。",
            "inputSchema": {"type": "object", "properties": {"dir": _dir_prop()}},
        },
        {
            "name": "kb_add",
            "description": ("写入知识条目（默认草稿 draft，需经 kb_review 核验后才可被默认查询命中）。"
                            "返回 ID / 路径 / 敏感扫描命中 / 标题查重提示。"),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "category": {"type": "string", "description": "分类 slug（必填，需已存在）"},
                    "title": {"type": "string", "description": "标题（必填）"},
                    "message": {"type": "string", "description": "正文（必填，Markdown）"},
                    "source": {"type": "string", "description": "出处 / 来源"},
                    "tags": {"type": "array", "items": {"type": "string"}, "description": "标签"},
                    "evidence": {"type": "string", "description": "证据（核验时必填）"},
                    "confidence": {"type": "string", "enum": ["high", "medium", "low"],
                                   "description": "置信度（默认 medium）"},
                    "agent": _agent_prop(),
                    "dir": _dir_prop(),
                },
                "required": ["category", "title", "message"],
            },
        },
        {
            "name": "kb_review",
            "description": ("审核门：pass 核验 / reject 拒绝（拒绝移入回收站）。"
                            "与 CLI 同一门禁：pass 需证据，敏感扫描命中会被阻断"
                            "（force=true 显式放行并记审计，需同时提供 note 说明）。"),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "条目 ID"},
                    "decision": {"type": "string", "enum": ["pass", "reject"], "description": "核验或拒绝"},
                    "evidence": {"type": "string", "description": "核验证据（pass 必填）"},
                    "note": {"type": "string",
                             "description": "拒绝原因 / 备注（force=true 时必填）"},
                    "force": {"type": "boolean", "description": "敏感命中时显式放行（记审计）"},
                    "agent": _agent_prop(),
                    "dir": _dir_prop(),
                },
                "required": ["id", "decision"],
            },
        },
        {
            "name": "kb_update",
            "description": "更新条目字段（title / message / tags / source / evidence / confidence）。",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "条目 ID"},
                    "title": {"type": "string"},
                    "message": {"type": "string"},
                    "tags": {"type": "array", "items": {"type": "string"}},
                    "source": {"type": "string"},
                    "evidence": {"type": "string"},
                    "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
                    "agent": _agent_prop(),
                    "dir": _dir_prop(),
                },
                "required": ["id"],
            },
        },
        {
            "name": "kb_deprecate",
            "description": "停用条目（保留可查，原因记入审计）。",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "条目 ID"},
                    "reason": {"type": "string", "description": "停用原因"},
                    "agent": _agent_prop(),
                    "dir": _dir_prop(),
                },
                "required": ["id"],
            },
        },
        {
            "name": "kb_category_create",
            "description": "创建知识库分类（slug 小写连字符；名称与一句话说明必填）。",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "slug": {"type": "string", "description": "分类 slug"},
                    "name": {"type": "string", "description": "中文名"},
                    "description": {"type": "string", "description": "一句话说明"},
                    "aliases": {"type": "array", "items": {"type": "string"}, "description": "别名"},
                    "agent": _agent_prop(),
                    "dir": _dir_prop(),
                },
                "required": ["slug", "name", "description"],
            },
        },
        {
            "name": "kb_category_rename",
            "description": "重命名分类显示名（slug 与条目不变；写审计）。",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "slug": {"type": "string", "description": "分类 slug"},
                    "name": {"type": "string", "description": "新中文名"},
                    "agent": _agent_prop(),
                    "dir": _dir_prop(),
                },
                "required": ["slug", "name"],
            },
        },
        {
            "name": "kb_category_merge",
            "description": ("合并分类：from 的条目迁入 into，from 变别名并停用"
                            "（先建快照；同名冲突 fail-closed；写审计）。"),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "from": {"type": "string", "description": "源分类 slug"},
                    "into": {"type": "string", "description": "目标分类 slug（可为别名）"},
                    "agent": _agent_prop(),
                    "dir": _dir_prop(),
                },
                "required": ["from", "into"],
            },
        },
        {
            "name": "kb_category_deprecate",
            "description": ("停用分类：空分类直接停用；非空需 force=true 显式确认，"
                            "或先 kb_category_merge 迁移条目（写审计）。"),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "slug": {"type": "string", "description": "分类 slug"},
                    "reason": {"type": "string", "description": "停用原因"},
                    "force": {"type": "boolean",
                              "description": "非空分类时显式确认停用（记审计）"},
                    "agent": _agent_prop(),
                    "dir": _dir_prop(),
                },
                "required": ["slug"],
            },
        },
        {
            "name": "kb_doctor",
            "description": "知识库体检（kb.json / 分类 / 条目 / 索引 / 锁 / 回收站 / 容量；可带独立备份目录）。",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "backup_dir": {"type": "string", "description": "可选：独立备份目录"},
                    "dir": _dir_prop(),
                },
            },
        },
        {
            "name": "kb_index_rebuild",
            "description": "全量重建知识库索引（分片索引 + 全局索引；写审计）。",
            "inputSchema": {
                "type": "object",
                "properties": {"agent": _agent_prop(), "dir": _dir_prop()},
            },
        },
    ]


# ── MCP 协议（dual-era：2026-07-28 无状态 / 2025-11-25 及更早握手） ─────────

def _req_version(params):
    meta = (params or {}).get("_meta") or {}
    return meta.get("io.modelcontextprotocol/protocolVersion")


def _modern_ok(payload, cache=None):
    out = {"resultType": "complete"}
    out.update(payload)
    out["_meta"] = {"io.modelcontextprotocol/serverInfo": dict(SERVER_INFO)}
    if cache:
        out["ttlMs"] = cache[0]
        out["cacheScope"] = cache[1]
    return out


def _unsupported_version(rid, pv):
    return {
        "jsonrpc": "2.0", "id": rid,
        "error": {
            "code": -32022,
            "message": "Unsupported protocol version",
            "data": {"supported": [MCP_PROTOCOL_MODERN], "requested": pv},
        },
    }


def _call_tool(name, arguments):
    handler = TOOL_HANDLERS.get(name)
    if not handler:
        return _tool_error("未知工具: %s" % name)
    try:
        return handler(arguments or {})
    except yotta_kb.KbError as exc:
        return _tool_error(exc.message, {"code": exc.code})
    except Exception as exc:  # noqa: BLE001
        return _tool_error("工具执行异常：%s" % exc)


def handle_message(msg):
    """处理一行 JSON-RPC 消息，返回响应 dict；通知返回 None。"""
    if not isinstance(msg, dict) or msg.get("jsonrpc") != "2.0":
        rid = msg.get("id") if isinstance(msg, dict) else None
        return {"jsonrpc": "2.0", "id": rid,
                "error": {"code": -32600, "message": "invalid request"}}
    method = msg.get("method")
    rid = msg.get("id")
    if rid is None or method is None:  # JSON-RPC 通知不响应
        return None
    params = msg.get("params") or {}
    pv = _req_version(params)

    if pv is not None:
        # ---- modern（2026-07-28 无状态）----
        if pv != MCP_PROTOCOL_MODERN:
            return _unsupported_version(rid, pv)
        if method == "server/discover":
            return {
                "jsonrpc": "2.0", "id": rid,
                "result": _modern_ok({
                    "supportedVersions": [MCP_PROTOCOL_MODERN],
                    "capabilities": {"tools": {}},
                    "instructions": (
                        "元习知识库 MCP（MCP 2026-07-28，向后兼容 2025-11-25 及更早握手）："
                        "读 kb_query/kb_get/kb_list/kb_stats/kb_categories；"
                        "写 kb_add/kb_review/kb_update/kb_deprecate/"
                        "kb_category_create/kb_category_rename/kb_category_merge/"
                        "kb_category_deprecate；"
                        "运维 kb_doctor/kb_index_rebuild。写工具 fail-closed：默认草稿 + 审核门。"
                    ),
                }, (3600000, "public")),
            }
        if method == "tools/list":
            return {"jsonrpc": "2.0", "id": rid,
                    "result": _modern_ok({"tools": mcp_tools()}, (300000, "public"))}
        if method == "tools/call":
            return {"jsonrpc": "2.0", "id": rid,
                    "result": _modern_ok(_call_tool(params.get("name"),
                                                    params.get("arguments")))}
        if method == "initialize":
            return {
                "jsonrpc": "2.0", "id": rid,
                "error": {
                    "code": -32601,
                    "message": ("initialize removed in MCP 2026-07-28; "
                                "use server/discover. supported: ['2026-07-28']"),
                },
            }
        return {"jsonrpc": "2.0", "id": rid,
                "error": {"code": -32601, "message": "Method not found: " + str(method)}}

    # ---- legacy（<=2025-11-25 握手）----
    if method == "initialize":
        return {
            "jsonrpc": "2.0", "id": rid,
            "result": {
                "protocolVersion": MCP_PROTOCOL_LEGACY,
                "capabilities": {"tools": {}},
                "serverInfo": SERVER_INFO,
            },
        }
    if method == "ping":
        return {"jsonrpc": "2.0", "id": rid, "result": {}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": rid, "result": {"tools": mcp_tools()}}
    if method == "tools/call":
        return {"jsonrpc": "2.0", "id": rid,
                "result": _call_tool(params.get("name"), params.get("arguments"))}
    return {"jsonrpc": "2.0", "id": rid,
            "error": {"code": -32601, "message": "Method not found: " + str(method)}}


def main():
    """stdio 主循环：读行 -> JSON-RPC -> 响应行。"""
    try:
        sys.stdin.reconfigure(encoding="utf-8")
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            sys.stdout.write(json.dumps(
                {"jsonrpc": "2.0", "id": None,
                 "error": {"code": -32700, "message": "parse error"}},
                ensure_ascii=False) + "\n")
            sys.stdout.flush()
            continue
        resp = handle_message(msg)
        if resp is not None:
            sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
