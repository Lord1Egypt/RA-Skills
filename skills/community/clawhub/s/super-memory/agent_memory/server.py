"""
server.py - Memory-as-a-Service HTTP 服务

将 agent-memory 变成一个 HTTP API，任何程序都能写入/检索记忆：
  POST /remember  → 写入记忆
  POST /recall    → 检索记忆
  GET  /context   → 组装上下文
  GET  /stream    → SSE 实时记忆流（替代 WS）
  GET  /stats     → 统计信息
  POST /feedback  → 反馈
  POST /maintain  → 触发维护

启动:
  python3 server.py                          # 默认 127.0.0.1:8976（仅本地访问）
  python3 server.py --port 9000              # 自定义端口
  python3 server.py --host 0.0.0.0           # 开放网络访问（需配合 --api-key）
  python3 server.py --db /data/memory.db     # 自定义数据库路径
  python3 server.py --api-key <secret>       # 启用 API Key 认证（生产必须）
  AGENT_MEMORY_API_KEY=<secret> python3 server.py  # 环境变量方式

设计原则:
  - 零外部依赖（纯 stdlib）
  - 每个请求独立处理，无全局可变状态
  - SSE 替代 WebSocket（协议简单，curl 可调试）
  - 与 cli.py 共享同一数据库，不冲突
  - API Key 认证保护（--api-key 或 AGENT_MEMORY_API_KEY）
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import logging
import os
import sys
import time
import threading
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from io import BytesIO
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logger = logging.getLogger(__name__)

# ── 常量 ────────────────────────────────────────────────

_MAX_REQUEST_SIZE = 1 * 1024 * 1024        # 1MB 单请求上限
_MAX_BATCH_TOTAL_SIZE = 5 * 1024 * 1024     # 5MB batch 总内容上限
_MAX_SSE_CLIENTS = 500                       # SSE 连接数上限
_MAX_EXPORT_LIMIT = 1000                     # export 单次最大条数
_SSE_CLIENT_TIMEOUT = 300                    # SSE 客户端最大存活时间 (秒)
_SSE_STALE_CLEANUP_INTERVAL = 60             # 清理过期 SSE 客户端的间隔 (秒)


class SSEBroker:
    """Server-Sent Events 事件总线：管理所有订阅客户端"""

    def __init__(self):
        self._clients: dict[str, dict] = {}
        self._lock = threading.Lock()

    def subscribe(self, client_id: str, filters: dict = None) -> bool:
        """注册客户端，超出上限返回 False"""
        with self._lock:
            if len(self._clients) >= _MAX_SSE_CLIENTS:
                logger.warning(f"SSE 客户端数已达上限 ({_MAX_SSE_CLIENTS})，拒绝新连接")
                return False
            self._clients[client_id] = {
                "filters": filters or {},
                "connected_at": time.time(),
                "events_sent": 0,
                "queue": [],
            }
        return True

    def unsubscribe(self, client_id: str):
        with self._lock:
            self._clients.pop(client_id, None)

    def broadcast(self, event_type: str, data: dict):
        """广播事件到所有匹配的订阅者。

        安全：不传播原始记忆内容到 SSE，防止敏感信息泄漏。
        """
        # 深拷贝并移除可能的敏感字段
        safe_data = {}
        for k, v in data.items():
            if k in ("content", "content_preview", "message"):
                # 不通过 SSE 传播原始内容
                continue
            safe_data[k] = v

        msg = f"event: {event_type}\ndata: {json.dumps(safe_data, ensure_ascii=False)}\n\n"
        with self._lock:
            for cid, client in list(self._clients.items()):
                filt = client.get("filters", {})
                if filt.get("importance") and safe_data.get("importance") != filt["importance"]:
                    continue
                if filt.get("topic") and filt["topic"] not in str(safe_data.get("topics", [])):
                    continue
                client["queue"].append(msg)
                client["events_sent"] += 1

    def get_queue(self, client_id: str) -> list:
        with self._lock:
            client = self._clients.get(client_id)
            if not client:
                return []
            queue = list(client["queue"])
            client["queue"].clear()
            return queue

    def cleanup_stale(self) -> int:
        """清理超时的 SSE 客户端，返回清理数量"""
        now = time.time()
        removed = 0
        with self._lock:
            stale = [
                cid for cid, c in self._clients.items()
                if now - c["connected_at"] > _SSE_CLIENT_TIMEOUT
            ]
            for cid in stale:
                del self._clients[cid]
                removed += 1
        if removed:
            logger.info(f"SSE 清理: 移除 {removed} 个超时客户端")
        return removed

    def get_stats(self) -> dict:
        with self._lock:
            return {
                "clients": len(self._clients),
                "max_clients": _MAX_SSE_CLIENTS,
                "details": {
                    cid: {
                        "connected_sec": round(time.time() - c["connected_at"], 1),
                        "events_sent": c["events_sent"],
                    }
                    for cid, c in self._clients.items()
                },
            }


sse_broker = SSEBroker()


# ── API Key 认证 ────────────────────────────────────────

_API_KEY = None  # 由 main() 在启动时设置
_API_KEYS_BY_ROLE = {}  # {role: hashed_key} — 角色分离的 API Key
_KEY_AGENT_BINDINGS = {}  # {hashed_key: agent_id} — API Key 到 Agent ID 的绑定
_api_keys_lock = threading.Lock()


def _snapshot_api_keys():
    with _api_keys_lock:
        return dict(_API_KEYS_BY_ROLE), dict(_KEY_AGENT_BINDINGS)


def _has_api_keys_configured():
    with _api_keys_lock:
        return _API_KEY is not None or bool(_API_KEYS_BY_ROLE)

_ROLE_PERMISSIONS = {
    "read": {"GET", "POST /recall"},
    "write": {"GET", "POST"},
    "admin": {"GET", "POST", "DELETE", "PATCH"},
}

_WRITE_ENDPOINTS = {"/remember", "/remember/batch", "/feedback", "/maintain"}
_ADMIN_ENDPOINTS = {"/maintain", "/export"}


def _parse_api_key(raw_key: str):
    """解析 API Key，支持 key:role 和 key:role:agent_id 格式。

    格式:
      mysecret           → admin 角色（向后兼容）
      mysecret:read      → 只读角色（recall, context, stats, graph）
      mysecret:write     → 读写角色（read + remember, feedback）
      mysecret:admin     → 管理员角色（全部端点）
      mysecret:read:agent-01   → 只读角色 + 绑定 agent-01 身份
      mysecret:write:agent-02  → 读写角色 + 绑定 agent-02 身份
      mysecret:admin:_system   → 管理员角色 + 绑定 _system（可跨 Agent 操作）
    """
    parts = raw_key.split(":")
    if len(parts) == 1:
        return raw_key, "admin", None
    if len(parts) == 2:
        key_part, role = parts
        role = role.lower().strip()
        if role not in _ROLE_PERMISSIONS:
            logger.warning(f"Unknown role '{role}' in API key, defaulting to 'admin'")
            role = "admin"
        return key_part, role, None
    # key:role:agent_id
    key_part, role, agent_id = parts[0], parts[1].lower().strip(), parts[2].strip()
    if role not in _ROLE_PERMISSIONS:
        logger.warning(f"Unknown role '{role}' in API key, defaulting to 'admin'")
        role = "admin"
    return key_part, role, agent_id


def _check_auth(headers) -> bool:
    """检查请求是否携带正确的 API Key。

    如果未配置 API Key，跳过认证（开发模式）。
    """
    keys_by_role, _ = _snapshot_api_keys()
    if _API_KEY is None and not keys_by_role:
        return True

    provided = _extract_key(headers)
    if not provided:
        return False

    provided_hash = hashlib.sha256(provided.encode()).hexdigest()

    if _API_KEY and hmac.compare_digest(provided_hash, hashlib.sha256(_API_KEY.encode()).hexdigest()):
        return True

    for role, hashed in keys_by_role.items():
        if hmac.compare_digest(provided_hash, hashed):
            return True

    return False


def _resolve_agent_id(headers) -> tuple:
    """解析并验证请求的 Agent ID，绑定到凭证。

    返回: (agent_id: str, authorized: bool)
      - agent_id: 最终使用的 agent_id
      - authorized: 身份覆盖是否被授权

    规则:
      1. 如果 API Key 绑定了 agent_id，则使用绑定的 agent_id
      2. 非 admin 角色不能通过 X-Agent-ID 或请求参数覆盖绑定的 agent_id
      3. admin 角色可以通过 X-Agent-ID 覆盖（用于管理操作）
      4. 未绑定 agent_id 的 API Key，使用 X-Agent-ID header（保持现有行为）
      5. 未配置 API Key 时，使用 X-Agent-ID header（开发模式）
    """
    header_agent_id = headers.get("X-Agent-ID", "_anonymous").strip() or "_anonymous"

    keys_by_role, key_bindings = _snapshot_api_keys()
    if _API_KEY is None and not keys_by_role:
        return header_agent_id, True

    provided = _extract_key(headers)
    if not provided:
        return "_anonymous", False

    provided_hash = hashlib.sha256(provided.encode()).hexdigest()

    if _API_KEY and provided_hash == hashlib.sha256(_API_KEY.encode()).hexdigest():
        return header_agent_id, True

    for role, hashed in keys_by_role.items():
        if provided_hash == hashed:
            bound_agent_id = key_bindings.get(hashed)
            if bound_agent_id is not None:
                if role == "admin":
                    return header_agent_id, True
                if header_agent_id != bound_agent_id and header_agent_id != "_anonymous":
                    logger.warning(
                        f"Agent ID override rejected: key bound to '{bound_agent_id}' "
                        f"but header claims '{header_agent_id}' (role: {role})"
                    )
                    return bound_agent_id, False
                return bound_agent_id, True
            return header_agent_id, True

    return "_anonymous", False


def _check_role_access(headers, endpoint: str, method: str) -> tuple:
    """检查请求的 API Key 是否有权限访问指定端点。

    参数:
        headers: 请求头
        endpoint: 端点路径（如 /remember）
        method: HTTP 方法（GET, POST）

    返回: (allowed: bool, role: str)
    """
    keys_by_role, _ = _snapshot_api_keys()
    if _API_KEY is None and not keys_by_role:
        return True, "admin"

    provided = _extract_key(headers)
    if not provided:
        return False, "none"

    provided_hash = hashlib.sha256(provided.encode()).hexdigest()

    if _API_KEY and provided_hash == hashlib.sha256(_API_KEY.encode()).hexdigest():
        return True, "admin"

    for role, hashed in keys_by_role.items():
        if provided_hash == hashed:
            perms = _ROLE_PERMISSIONS.get(role, set())
            if endpoint in _ADMIN_ENDPOINTS and role not in ("admin",):
                return False, role
            if endpoint in _WRITE_ENDPOINTS and method == "POST" and "POST" not in perms:
                return False, role
            if method == "GET" and "GET" not in perms:
                return False, role
            return True, role

    return False, "none"


def _extract_key(headers) -> str:
    """从请求头提取 API Key"""
    auth = headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        return auth[7:].strip()
    return headers.get("X-API-Key", "").strip()


def _get_agent_id(headers) -> str:
    """从请求头提取 Agent 身份标识（已绑定凭证验证）。

    通过 X-Agent-ID header 传递，用于多 Agent 场景下的身份验证和访问控制。
    如果未提供，默认为 '_anonymous'。

    ⚠️ 安全: agent_id 与 API Key 绑定。非 admin 角色的 API Key 不能覆盖绑定的 agent_id。
    认证仍由 API Key 负责，agent_id 用于区分不同 Agent 的记忆边界。
    """
    agent_id, authorized = _resolve_agent_id(headers)
    return agent_id


def _validate_agent_access(headers, required_agent_id: str = None) -> tuple:
    """验证 Agent 对指定资源的访问权限。

    参数:
        headers: 请求头
        required_agent_id: 资源所属的 agent_id（None 表示不检查）

    返回: (allowed: bool, agent_id: str)
    """
    agent_id, authorized = _resolve_agent_id(headers)
    if not authorized:
        return False, agent_id
    if required_agent_id and required_agent_id != "_system":
        if agent_id != required_agent_id and agent_id != "_system":
            return False, agent_id
    return True, agent_id


class MemoryAPIHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        logger.debug(format % args)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "http://localhost:* http://127.0.0.1:*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-API-Key, X-Agent-ID")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()

    def _send_auth_error(self):
        self._json_response(401, {"error": "unauthorized", "hint": "Provide API key via Authorization: Bearer <key> or X-API-Key header"})

    def do_GET(self):
        # 认证检查（health 和 index 跳过认证，方便监控和探活）
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")
        if path not in ("/", "/health") and not _check_auth(self.headers):
            self._send_auth_error()
            return

        params = parse_qs(parsed.query)
        routes = {
            "/": self._handle_index,
            "/health": self._handle_health,
            "/context": self._handle_context,
            "/stream": self._handle_stream,
            "/stats": self._handle_stats,
            "/export": self._handle_export,
            "/graph": self._handle_graph,
            "/metrics": self._handle_metrics,
            "/versions": self._handle_versions,
        }
        handler = routes.get(path)
        if handler:
            handler(params)
        else:
            self._json_response(404, {"error": f"unknown path: {path}"})

    def do_POST(self):
        # 认证检查
        if not _check_auth(self.headers):
            self._send_auth_error()
            return

        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")
        body = self._read_body()
        routes = {
            "/remember": self._handle_remember,
            "/recall": self._handle_recall,
            "/feedback": self._handle_feedback,
            "/maintain": self._handle_maintain,
            "/remember/batch": self._handle_remember_batch,
        }
        handler = routes.get(path)
        if handler:
            handler(body)
        else:
            self._json_response(404, {"error": f"unknown path: {path}"})

    def do_PUT(self):
        """PUT 请求 — 记忆更新（版本化）"""
        if not _check_auth(self.headers):
            self._send_auth_error()
            return

        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")
        body = self._read_body()

        if path == "/remember":
            self._handle_update_memory(body)
        else:
            self._json_response(404, {"error": f"unknown path: {path}"})

    # ── Handlers ─────────────────────────────────────

    def _handle_index(self, params):
        auth_enabled = _API_KEY is not None
        doc = {
            "service": "agent-memory",
            "version": "6.0.0",
            "mode": "Memory-as-a-Service",
            "auth": "enabled" if auth_enabled else "disabled (set --api-key for production)",
            "endpoints": {
                "POST /remember": {
                    "desc": "Write a memory",
                    "body": {
                        "content": "(required)",
                        "importance": "(optional) high/medium/low",
                        "topics": "(optional) topic list",
                        "person_code": "(optional) default main",
                        "nature_code": "(optional)",
                        "owner_agent_id": "(optional)",
                        "visibility": "(optional) private/team/public",
                    },
                },
                "POST /remember/batch": {
                    "desc": "Batch write (max 50 items, max 5MB total content)",
                    "body": {"messages": [{"content": "...", "importance": "..."}]},
                },
                "POST /recall": {
                    "desc": "Search memories",
                    "body": {
                        "query": "(required)",
                        "top_k": "(optional) default 10",
                        "importance": "(optional) filter",
                        "topic_code": "(optional) filter",
                        "query_agent_id": "(optional) permission filter",
                    },
                },
                "GET /context": {
                    "desc": "Build context string",
                    "params": {"q": "(required)", "max_tokens": "(optional) default 1500", "query_agent_id": "(optional)"},
                },
                "GET /stream": {
                    "desc": "SSE real-time memory stream",
                    "params": {"client_id": "(optional)", "importance": "(optional) filter", "topic": "(optional) filter"},
                },
                "POST /feedback": {"desc": "Submit feedback", "body": {"memory_id": "...", "useful": True, "note": "..."}},
                "GET /stats": {"desc": "System statistics"},
                "GET /export": {"desc": "Export memories (max 1000)", "params": {"format": "json/markdown", "limit": "(optional) default 100"}},
                "GET /graph": {"desc": "Memory association graph"},
                "POST /maintain": {"desc": "Trigger maintenance"},
                "PUT /remember": {
                    "desc": "Update a memory (versioned, preserves history)",
                    "body": {
                        "memory_id": "(required)",
                        "content": "(required) new content",
                        "change_reason": "(optional) reason for change",
                        "importance": "(optional) high/medium/low",
                        "topics": "(optional) new topic list",
                    },
                },
                "GET /versions": {
                    "desc": "Get version history of a memory",
                    "params": {"memory_id": "(required)"},
                },
            },
        }
        self._json_response(200, doc)

    def _handle_health(self, params):
        try:
            store = _get_store()
            count = store.conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
            self._json_response(200, {
                "status": "ok",
                "memories": count,
                "timestamp": int(time.time()),
                "uptime_sec": round(time.time() - _SERVER_START, 1),
            })
        except Exception as e:
            logger.exception("Unhandled error in request handler: %s", e)
            self._json_response(500, {"error": "Internal server error"})

    def _handle_remember(self, body):
        if not _has_api_keys_configured():
            self._json_response(403, {"error": "Write endpoint requires API Key authentication. Start server with --api-key."})
            return
        allowed, role = _check_role_access(self.headers, "/remember", "POST")
        if not allowed:
            self._json_response(403, {"error": f"Insufficient permissions (role: {role}). Write access requires 'write' or 'admin' role."})
            return
        # v8.2 安全：验证 Agent ID 与凭证绑定
        resolved_agent_id, agent_authorized = _resolve_agent_id(self.headers)
        if not agent_authorized:
            self._json_response(403, {"error": "Agent ID override not authorized. Your API key is bound to a specific agent identity."})
            return
        content = body.get("content", "").strip()
        if not content:
            self._json_response(400, {"error": "content is required"})
            return
        # HTTP 层长度校验（pipeline 层也会截断，但这里提前拒绝避免浪费资源）
        if len(content) > 50000:
            self._json_response(400, {"error": f"content too long: {len(content)} chars (max 50000)"})
            return
        try:
            pipeline = _get_pipeline()
            owner_agent_id = body.get("owner_agent_id") or resolved_agent_id
            if owner_agent_id != resolved_agent_id and role != "admin":
                logger.warning(f"owner_agent_id override rejected: {resolved_agent_id} -> {owner_agent_id} (role: {role})")
                owner_agent_id = resolved_agent_id
            result = pipeline.ingest(
                content=content,
                person_code=body.get("person_code", "main"),
                importance=body.get("importance", "medium"),
                topics=body.get("topics"),
                nature_code=body.get("nature_code"),
                tool_codes=body.get("tool_codes"),
                knowledge_codes=body.get("knowledge_codes"),
                owner_agent_id=owner_agent_id,
                visibility=body.get("visibility", "team"),
            )
            # SSE 广播不含敏感内容
            sse_broker.broadcast("memory_created", {
                "memory_id": result.get("memory_id"),
                "topics": result.get("topics", []),
                "importance": result.get("importance"),
                "timestamp": int(time.time()),
            })
            self._json_response(201, result)
        except Exception as e:
            logger.error(f"remember failed: {e}", exc_info=True)
            self._json_response(500, {"error": "Internal server error"})

    def _handle_remember_batch(self, body):
        if not _has_api_keys_configured():
            self._json_response(403, {"error": "Batch write endpoint requires API Key authentication. Start server with --api-key."})
            return
        allowed, role = _check_role_access(self.headers, "/remember/batch", "POST")
        if not allowed:
            self._json_response(403, {"error": f"Insufficient permissions (role: {role}). Write access requires 'write' or 'admin' role."})
            return
        # v8.2 安全：验证 Agent ID 与凭证绑定
        resolved_agent_id, agent_authorized = _resolve_agent_id(self.headers)
        if not agent_authorized:
            self._json_response(403, {"error": "Agent ID override not authorized. Your API key is bound to a specific agent identity."})
            return
        messages = body.get("messages", [])
        if not messages:
            self._json_response(400, {"error": "messages array is required"})
            return
        if len(messages) > 50:
            self._json_response(400, {"error": f"too many messages: {len(messages)} (max 50)"})
            return
        # batch 总大小检查
        total_size = sum(len(m.get("content", "")) for m in messages)
        if total_size > _MAX_BATCH_TOTAL_SIZE:
            self._json_response(400, {"error": f"batch total content size {total_size} exceeds limit ({_MAX_BATCH_TOTAL_SIZE})"})
            return
        # 单条长度检查
        for i, msg in enumerate(messages):
            clen = len(msg.get("content", ""))
            if clen > 50000:
                self._json_response(400, {"error": f"message[{i}] content too long: {clen} chars (max 50000)"})
                return
        try:
            pipeline = _get_pipeline()
            results = []
            for msg in messages[:50]:
                msg_agent_id = msg.get("owner_agent_id") or resolved_agent_id
                if msg_agent_id != resolved_agent_id and role != "admin":
                    msg_agent_id = resolved_agent_id
                r = pipeline.ingest(
                    content=msg.get("content", ""),
                    person_code=msg.get("person_code", "main"),
                    importance=msg.get("importance", "medium"),
                    topics=msg.get("topics"),
                    nature_code=msg.get("nature_code"),
                    owner_agent_id=msg_agent_id,
                    visibility=msg.get("visibility", "team"),
                    skip_throttle=True,
                )
                results.append(r)
            sse_broker.broadcast("batch_created", {
                "count": len(results),
                "ids": [r.get("memory_id") for r in results if r.get("memory_id")],
                "timestamp": int(time.time()),
            })
            self._json_response(201, {"written": len(results), "results": results})
        except Exception as e:
            logger.error(f"batch remember failed: {e}", exc_info=True)
            self._json_response(500, {"error": "Internal server error"})

    def _handle_recall(self, body):
        query = body.get("query", "").strip()
        if not query:
            self._json_response(400, {"error": "query is required"})
            return
        if len(query) > 10000:
            self._json_response(400, {"error": f"query too long: {len(query)} chars (max 10000)"})
            return
        try:
            store = _get_store()
            emb = _get_embedding_store()
            top_k = min(body.get("top_k", 10), 100)
            # v8.2 安全：Agent ID 与凭证绑定，非 admin 不能覆盖
            resolved_agent_id, agent_authorized = _resolve_agent_id(self.headers)
            query_agent_id = body.get("query_agent_id") or resolved_agent_id
            if query_agent_id != resolved_agent_id and not agent_authorized:
                query_agent_id = resolved_agent_id
            _, role = _check_role_access(self.headers, "/recall", "POST")
            if query_agent_id != resolved_agent_id and role != "admin":
                logger.warning(f"query_agent_id override rejected: {resolved_agent_id} -> {query_agent_id} (role: {role})")
                query_agent_id = resolved_agent_id
            team_id = body.get("team_id", "default")

            struct_results = store.query(
                keyword=query,
                importance=body.get("importance"),
                topic_code=body.get("topic_code"),
                limit=top_k,
                query_agent_id=query_agent_id,
                team_id=team_id,
            )
            semantic_results = []
            if emb:
                try:
                    semantic_results = emb.search(query, top_k=top_k)
                except Exception as e:
                    logger.warning("server: %s", e)

            fused = _rrf_fuse(struct_results, semantic_results, top_k)

            quality = _get_quality()
            if quality:
                for mem in fused:
                    q = quality.compute_quality(mem)
                    mem["_quality_score"] = q["quality_score"]

            self._json_response(200, {
                "query": query,
                "count": len(fused),
                "results": [
                    {
                        "memory_id": m.get("memory_id"),
                        "content": m.get("content", "")[:500],
                        "importance": m.get("importance"),
                        "topics": m.get("topics", []),
                        "time_ts": m.get("time_ts"),
                        "quality_score": m.get("_quality_score"),
                        "rank_score": m.get("_rank_score", 0),
                    }
                    for m in fused
                ],
            })
        except Exception as e:
            logger.error(f"recall failed: {e}", exc_info=True)
            self._json_response(500, {"error": "Internal server error"})

    def _handle_context(self, params):
        q = params.get("q", [""])[0].strip()
        if not q:
            self._json_response(400, {"error": "q parameter is required"})
            return
        if len(q) > 10000:
            self._json_response(400, {"error": f"q too long: {len(q)} chars"})
            return
        try:
            max_tokens = min(int(params.get("max_tokens", ["1500"])[0]), 10000)
            # v8.2 安全：Agent ID 与凭证绑定，非 admin 不能覆盖
            resolved_agent_id, agent_authorized = _resolve_agent_id(self.headers)
            query_agent_id = params.get("query_agent_id", [None])[0] or resolved_agent_id
            if query_agent_id != resolved_agent_id and not agent_authorized:
                query_agent_id = resolved_agent_id
            _, role = _check_role_access(self.headers, "/context", "GET")
            if query_agent_id != resolved_agent_id and role != "admin":
                query_agent_id = resolved_agent_id
            team_id = params.get("team_id", ["default"])[0]
            store = _get_store()
            results = store.query(keyword=q, limit=10, query_agent_id=query_agent_id, team_id=team_id)

            lines = []
            token_count = 0
            for mem in results:
                content = mem.get("content", "")
                est_tokens = len(content) * 1.5
                if token_count + est_tokens > max_tokens:
                    break
                ts_str = datetime.fromtimestamp(mem.get("time_ts", 0)).strftime("%m-%d %H:%M")
                imp = mem.get("importance", "medium")
                prefix = {"high": "⚡", "medium": "📝", "low": "📎"}.get(imp, "")
                lines.append(f"{prefix}[{ts_str}] {content}")
                token_count += est_tokens

            self._json_response(200, {
                "query": q,
                "context": "\n".join(lines),
                "memories_used": len(lines),
                "estimated_tokens": int(token_count),
                "max_tokens": max_tokens,
            })
        except Exception as e:
            self._json_response(500, {"error": "Internal server error"})

    def _handle_stream(self, params):
        if not _has_api_keys_configured():
            self._json_response(403, {"error": "SSE stream requires API Key authentication. Start server with --api-key."})
            return
        if not _check_auth(self.headers):
            self._send_auth_error()
            return
        client_id = params.get("client_id", [uuid.uuid4().hex[:8]])[0]
        filters = {}
        if "importance" in params:
            filters["importance"] = params["importance"][0]
        if "topic" in params:
            filters["topic"] = params["topic"][0]

        # 注册客户端（检查上限）
        if not sse_broker.subscribe(client_id, filters):
            self._json_response(503, {"error": "SSE client limit reached", "max_clients": _MAX_SSE_CLIENTS})
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.send_header("Access-Control-Allow-Origin", "http://localhost:* http://127.0.0.1:*")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()

        hello = f"event: connected\ndata: {json.dumps({'client_id': client_id, 'timestamp': int(time.time())})}\n\n"
        self.wfile.write(hello.encode("utf-8"))
        self.wfile.flush()

        try:
            deadline = time.time() + _SSE_CLIENT_TIMEOUT
            while time.time() < deadline:
                queue = sse_broker.get_queue(client_id)
                for msg in queue:
                    self.wfile.write(msg.encode("utf-8"))
                    self.wfile.flush()
                # 心跳
                if not queue:
                    try:
                        self.wfile.write(b": heartbeat\n\n")
                        self.wfile.flush()
                    except Exception:
                        break
                time.sleep(0.5)
            bye = f"event: timeout\ndata: {json.dumps({'reason': 'max_duration'})}\n\n"
            self.wfile.write(bye.encode("utf-8"))
            self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError) as e:
            logger.debug("server: SSE client disconnect: %s", e)
        finally:
            sse_broker.unsubscribe(client_id)

    def _handle_stats(self, params):
        try:
            store = _get_store()
            total = store.conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
            by_imp = {}
            for row in store.conn.execute("SELECT importance, COUNT(*) as cnt FROM memories GROUP BY importance"):
                by_imp[row["importance"]] = row["cnt"]
            result = {
                "total_memories": total,
                "by_importance": by_imp,
                "io_stats": store.get_io_stats(),
                "sse_clients": sse_broker.get_stats(),
            }
            try:
                result["storage"] = store.get_storage_stats()
            except Exception as e:
                logger.warning("server: %s", e)
            self._json_response(200, result)
        except Exception as e:
            self._json_response(500, {"error": "Internal server error"})

    def _handle_feedback(self, body):
        if not _has_api_keys_configured():
            self._json_response(403, {"error": "Feedback endpoint requires API Key authentication. Start server with --api-key."})
            return
        allowed, role = _check_role_access(self.headers, "/feedback", "POST")
        if not allowed:
            self._json_response(403, {"error": f"Insufficient permissions (role: {role}). Write access requires 'write' or 'admin' role."})
            return
        memory_id = body.get("memory_id")
        if not memory_id:
            self._json_response(400, {"error": "memory_id is required"})
            return
        try:
            quality = _get_quality()
            if quality:
                quality.record_feedback(memory_id, body.get("useful", True), body.get("note"))
            sse_broker.broadcast("feedback", {"memory_id": memory_id, "useful": body.get("useful"), "timestamp": int(time.time())})
            self._json_response(200, {"ok": True})
        except Exception as e:
            self._json_response(500, {"error": "Internal server error"})

    def _handle_maintain(self, body):
        if not _has_api_keys_configured():
            self._json_response(403, {"error": "Maintain endpoint requires API Key authentication. Start server with --api-key."})
            return
        allowed, role = _check_role_access(self.headers, "/maintain", "POST")
        if not allowed:
            self._json_response(403, {"error": f"Insufficient permissions (role: {role}). Admin access required."})
            return
        try:
            store = _get_store()
            results = {}
            store.auto_maintain()
            results["db_optimize"] = "ok"
            # 定期清理过期 SSE 客户端
            cleaned = sse_broker.cleanup_stale()
            if cleaned:
                results["sse_cleaned"] = cleaned
            self._json_response(200, {"ok": True, "results": results})
        except Exception as e:
            self._json_response(500, {"error": "Internal server error"})

    def _handle_update_memory(self, body):
        """PUT /remember — 版本化更新记忆内容"""
        memory_id = body.get("memory_id")
        if not memory_id:
            self._json_response(400, {"error": "memory_id is required"})
            return
        new_content = body.get("content", "").strip()
        if not new_content:
            self._json_response(400, {"error": "content is required"})
            return
        if len(new_content) > 50000:
            self._json_response(400, {"error": f"content too long: {len(new_content)} chars (max 50000)"})
            return
        try:
            store = _get_store()
            result = store.update_memory(
                memory_id=memory_id,
                new_content=new_content,
                change_reason=body.get("change_reason"),
                importance=body.get("importance"),
                topics=body.get("topics"),
            )
            if result.get("error"):
                self._json_response(404, {"error": result["error"]})
                return

            # 同步更新向量
            if result.get("changed"):
                emb = _get_embedding_store()
                if emb:
                    try:
                        emb.delete(memory_id)
                        emb.add(
                            memory_id=memory_id,
                            content=new_content,
                            metadata={
                                "importance": body.get("importance", "medium"),
                                "nature_id": body.get("nature_id", ""),
                            },
                        )
                    except Exception as e:
                        logger.warning("server: %s", e)

                sse_broker.broadcast("memory_updated", {
                    "memory_id": memory_id,
                    "version": result.get("version"),
                    "timestamp": int(time.time()),
                })

            self._json_response(200, result)
        except Exception as e:
            logger.error(f"update memory failed: {e}", exc_info=True)
            self._json_response(500, {"error": "Internal server error"})

    def _handle_versions(self, params):
        """GET /versions?memory_id=xxx — 查看记忆版本历史"""
        memory_id = params.get("memory_id", [""])[0].strip()
        if not memory_id:
            self._json_response(400, {"error": "memory_id parameter is required"})
            return
        try:
            store = _get_store()
            versions = store.get_memory_versions(memory_id)
            if not versions:
                self._json_response(404, {"error": "memory not found or no version history"})
                return
            self._json_response(200, {
                "memory_id": memory_id,
                "total_versions": len(versions),
                "versions": versions,
            })
        except Exception as e:
            self._json_response(500, {"error": "Internal server error"})

    def _handle_export(self, params):
        if not _has_api_keys_configured():
            self._json_response(403, {"error": "Export endpoint requires API Key authentication. Start server with --api-key."})
            return
        allowed, role = _check_role_access(self.headers, "/export", "GET")
        if not allowed:
            self._json_response(403, {"error": f"Insufficient permissions (role: {role}). Admin access required."})
            return
        try:
            fmt = params.get("format", ["json"])[0]
            limit = min(int(params.get("limit", ["100"])[0]), _MAX_EXPORT_LIMIT)
            store = _get_store()
            memories = store.query(limit=limit)
            if fmt == "markdown":
                lines = ["# Agent Memory Export", f"\n**Total**: {len(memories)} memories\n"]
                for m in memories:
                    ts = datetime.fromtimestamp(m.get("time_ts", 0)).strftime("%Y-%m-%d %H:%M")
                    lines.append(f"### [{ts}] {m.get('importance','')} | {m.get('content','')[:80]}\n")
                output = "\n".join(lines)
                self.send_response(200)
                self.send_header("Content-Type", "text/markdown; charset=utf-8")
                self.end_headers()
                self.wfile.write(output.encode("utf-8"))
            else:
                self._json_response(200, {"exported_at": int(time.time()), "total": len(memories), "memories": memories})
        except Exception as e:
            self._json_response(500, {"error": "Internal server error"})

    def _handle_graph(self, params):
        try:
            store = _get_store()
            limit = min(int(params.get("limit", ["50"])[0]), 500)
            memories = store.query(limit=limit)
            nodes = [{"id": m["memory_id"], "label": m.get("content", "")[:30], "importance": m.get("importance")} for m in memories]
            edges = []
            for m in memories:
                for link in m.get("links", []):
                    if link.get("source_id") == m["memory_id"]:
                        edges.append({"source": link["source_id"], "target": link["target_id"], "type": link.get("link_type")})
            self._json_response(200, {"nodes": nodes, "edges": edges})
        except Exception as e:
            self._json_response(500, {"error": "Internal server error"})

    def _handle_metrics(self, params):
        """Prometheus 格式指标导出"""
        try:
            fmt = params.get("format", ["prometheus"])[0]
            store = _get_store()
            emb = _get_embedding_store()

            # 基础指标
            total = store.conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
            uptime = round(time.time() - _SERVER_START)

            by_imp = {}
            for row in store.conn.execute("SELECT importance, COUNT(*) as cnt FROM memories GROUP BY importance"):
                by_imp[row[0]] = row[1]

            if fmt == "json":
                data = {
                    "uptime_seconds": uptime,
                    "memories_total": total,
                    "memories_by_importance": by_imp,
                    "vectors": emb.count() if emb else 0,
                }
                self._json_response(200, data)
            else:
                # Prometheus text format
                lines = [
                    "# HELP agent_memory_uptime_seconds Service uptime",
                    "# TYPE agent_memory_uptime_seconds gauge",
                    f"agent_memory_uptime_seconds {uptime}",
                    "",
                    "# HELP agent_memory_total Total memories",
                    "# TYPE agent_memory_total gauge",
                    f"agent_memory_total {total}",
                    "",
                ]
                for imp, cnt in by_imp.items():
                    lines.append(f"agent_memory_by_importance{{importance=\"{imp}\"}} {cnt}")
                if emb:
                    try:
                        lines.append("")
                        lines.append("# HELP agent_memory_vectors Vector count")
                        lines.append("# TYPE agent_memory_vectors gauge")
                        lines.append(f"agent_memory_vectors {emb.count()}")
                    except Exception as e:
                        logger.warning("server: %s", e)
                lines.append("")

                body = "\n".join(lines).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/plain; version=0.0.4; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
        except Exception as e:
            self._json_response(500, {"error": "Internal server error"})

    # ── Utils ────────────────────────────────────────

    def _read_body(self) -> dict:
        try:
            length = int(self.headers.get("Content-Length", 0))
            if length == 0:
                return {}
            # 请求体大小限制
            if length > _MAX_REQUEST_SIZE:
                logger.warning(f"Request body too large: {length} bytes (max {_MAX_REQUEST_SIZE})")
                return {"_oversized": True, "size": length}
            raw = self.rfile.read(length).decode("utf-8")
            return json.loads(raw)
        except Exception as e:
            logger.debug("server: json parse: %s", e)
            return {}

    def _json_response(self, code: int, data: dict):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "http://localhost:* http://127.0.0.1:*")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("X-XSS-Protection", "1; mode=block")
        self.end_headers()
        self.wfile.write(body)


# ── RRF Fusion ───────────────────────────────────────────

def _rrf_fuse(struct_results, semantic_results, top_k, k=60):
    scores = {}
    details = {}
    for rank, mem in enumerate(struct_results):
        mid = mem.get("memory_id", "")
        if mid:
            scores[mid] = scores.get(mid, 0) + 1.0 / (k + rank + 1)
            details[mid] = mem
    for rank, hit in enumerate(semantic_results):
        mid = hit.get("memory_id", "")
        if mid:
            scores[mid] = scores.get(mid, 0) + 1.0 / (k + rank + 1)
            if mid not in details:
                details[mid] = hit
    ranked = sorted(scores.items(), key=lambda x: -x[1])
    result = []
    for mid, score in ranked[:top_k]:
        mem = details.get(mid, {})
        mem["_rank_score"] = round(score, 6)
        result.append(mem)
    return result


# ── Global lazy init (thread-safe) ──────────────────────

_STORE = _PIPELINE = _EMBEDDING_STORE = _QUALITY = None
_INIT_LOCK = threading.Lock()
_SERVER_START = time.time()
_DB_PATH = None


def _get_store():
    global _STORE
    if _STORE is None:
        with _INIT_LOCK:
            if _STORE is None:  # double-checked locking
                from store import MemoryStore
                _STORE = MemoryStore(db_path=_DB_PATH)
    return _STORE


def _get_pipeline():
    global _PIPELINE
    if _PIPELINE is None:
        with _INIT_LOCK:
            if _PIPELINE is None:
                from encoder import DimensionEncoder
                from pipeline import IngestPipeline
                _PIPELINE = IngestPipeline(store=_get_store(), encoder=DimensionEncoder(), embedding_store=_get_embedding_store())
    return _PIPELINE


def _get_embedding_store():
    global _EMBEDDING_STORE
    if _EMBEDDING_STORE is None:
        with _INIT_LOCK:
            if _EMBEDDING_STORE is None:
                try:
                    from embedding_store import EmbeddingStore
                    # Fix (Issue #8/#9): 使用 conn_provider 动态获取当前线程的连接，
                    # 解决 ThreadingMixIn 下多线程共享固定连接的问题
                    _EMBEDDING_STORE = EmbeddingStore(
                        db_path=_DB_PATH,
                        conn_provider=lambda: _get_store().conn,
                    )
                    logger.info("Embedding store loaded (thread-safe connection provider)")
                except Exception as e:
                    logger.warning("server: %s", e)
    return _EMBEDDING_STORE


def _get_quality():
    global _QUALITY
    if _QUALITY is None:
        with _INIT_LOCK:
            if _QUALITY is None:
                try:
                    from quality import MemoryQuality
                    _QUALITY = MemoryQuality(store=_get_store())
                except Exception as e:
                    logger.warning("server: %s", e)
    return _QUALITY


def main():
    global _DB_PATH, _API_KEY, _API_KEYS_BY_ROLE, _KEY_AGENT_BINDINGS
    parser = argparse.ArgumentParser(description="Agent Memory HTTP Service")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8976)
    parser.add_argument("--db", default=None)
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    parser.add_argument("--api-key", default=None, help="API key for authentication (format: key, key:role, or key:role:agent_id)")
    args = parser.parse_args()

    from logging_config import configure_logging
    configure_logging(level=args.log_level)
    _DB_PATH = args.db

    # API Key: CLI 参数 > 环境变量 > None (无认证)
    # 支持角色分离和 Agent 绑定:
    #   --api-key "myreadkey:read:agent-01"
    #   --api-key "mywritekey:write:agent-02"
    #   --api-key "myadminkey:admin:_system"
    raw_key = args.api_key or os.environ.get("AGENT_MEMORY_API_KEY")
    if raw_key:
        key_part, role, bound_agent_id = _parse_api_key(raw_key)
        _API_KEY = key_part
        hashed = hashlib.sha256(key_part.encode()).hexdigest()
        with _api_keys_lock:
            _API_KEYS_BY_ROLE[role] = hashed
            if bound_agent_id is not None:
                _KEY_AGENT_BINDINGS[hashed] = bound_agent_id
        if bound_agent_id is not None:
            logger.info(f"🔐 API Key authentication enabled (role: {role}, bound agent: {bound_agent_id})")
        else:
            logger.info(f"🔐 API Key authentication enabled (default role: {role})")
    else:
        extra_keys_configured = False
        for env_var in ["AGENT_MEMORY_API_KEY_READ", "AGENT_MEMORY_API_KEY_WRITE"]:
            env_val = os.environ.get(env_var)
            if env_val:
                role = "read" if "READ" in env_var else "write"
                env_parts = env_val.split(":", 1)
                key_val = env_parts[0]
                hashed = hashlib.sha256(key_val.encode()).hexdigest()
                with _api_keys_lock:
                    _API_KEYS_BY_ROLE[role] = hashed
                    if len(env_parts) == 2:
                        _KEY_AGENT_BINDINGS[hashed] = env_parts[1]
                if len(env_parts) == 2:
                    logger.info(f"🔐 Additional API Key configured: {role} role, bound agent: {env_parts[1]}")
                else:
                    logger.info(f"🔐 Additional API Key configured: {role} role")
                extra_keys_configured = True

        if not extra_keys_configured:
            logger.warning("⚠️  No API key set — all endpoints are open! Set --api-key or AGENT_MEMORY_API_KEY for production.")
        else:
            logger.info("🔐 API Key authentication enabled (role-based)")

        if args.host not in ("127.0.0.1", "localhost", "::1") and not _has_api_keys_configured():
            logger.error("🚫 FATAL: Binding to %s without API key is not allowed. Use --api-key or bind to 127.0.0.1.", args.host)
            sys.exit(1)

    from http.server import HTTPServer, BaseHTTPRequestHandler
    from socketserver import ThreadingMixIn

    class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
        """多线程 HTTP 服务器 — 每个请求独立线程处理"""
        daemon_threads = True  # 主线程退出时自动终止工作线程

    server = ThreadingHTTPServer((args.host, args.port), MemoryAPIHandler)
    logger.info(f"🧠 Agent Memory Service on http://{args.host}:{args.port} (threaded)")
    logger.info(f"   Docs:   http://localhost:{args.port}/")
    logger.info(f"   Health: http://localhost:{args.port}/health")
    logger.info(f"   Stream: http://localhost:{args.port}/stream")

    # 后台线程：定期清理过期 SSE 客户端
    def _sse_cleanup_loop():
        while True:
            time.sleep(_SSE_STALE_CLEANUP_INTERVAL)
            try:
                sse_broker.cleanup_stale()
            except Exception as e:
                logger.warning("server: %s", e)

    cleanup_thread = threading.Thread(target=_sse_cleanup_loop, daemon=True, name="sse-cleanup")
    cleanup_thread.start()

    # Fix (#15): 后台线程 — 轮询 tasks 表，超时任务通过 SSE 广播
    _TASK_POLL_INTERVAL = 60  # 每 60 秒检查一次
    _notified_task_ids: set = set()  # 避免重复通知

    def _task_poll_loop():
        while True:
            time.sleep(_TASK_POLL_INTERVAL)
            try:
                store = _get_store()
                now_ts = int(time.time())
                # 查找已超时但未完成的任务
                rows = store.conn.execute(
                    """SELECT task_id, memory_id, title, deadline, topic_code
                       FROM tasks
                       WHERE status = 'pending' AND deadline IS NOT NULL AND deadline <= ?""",
                    (now_ts,)
                ).fetchall()

                for row in rows:
                    task_id = row["task_id"]
                    if task_id in _notified_task_ids:
                        continue
                    _notified_task_ids.add(task_id)

                    deadline_dt = datetime.fromtimestamp(row["deadline"]).strftime("%H:%M")
                    sse_broker.broadcast("task_overdue", {
                        "task_id": task_id,
                        "memory_id": row["memory_id"],
                        "title": row["title"],
                        "deadline": deadline_dt,
                        "topic": row.get("topic_code"),
                    })
                    logger.info(f"📢 超时任务通知: {row['title']} (deadline {deadline_dt})")

                # 清理已完成任务的通知缓存（避免 _notified_task_ids 无限增长）
                if len(_notified_task_ids) > 10000:
                    completed = store.conn.execute(
                        "SELECT task_id FROM tasks WHERE status = 'completed'"
                    ).fetchall()
                    completed_ids = {r["task_id"] for r in completed}
                    _notified_task_ids.intersection_update(completed_ids)

            except Exception as e:
                logger.debug(f"Task poll error: {e}")

    task_thread = threading.Thread(target=_task_poll_loop, daemon=True, name="task-poll")
    task_thread.start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        # 优雅关闭：清理连接 + WAL checkpoint
        try:
            store = _get_store()
            if store:
                # WAL checkpoint：将 WAL 文件数据写入主库
                try:
                    store.conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
                except Exception as e:
                    logger.warning("server: %s", e)
                # Fix (#17): 关闭所有线程的连接，不只是当前线程
                store.close_all()
                logger.info("  ✓ All store connections closed")
        except Exception as e:
            logger.warning("server: %s", e)

        try:
            emb = _get_embedding_store()
            if emb and hasattr(emb, "close"):
                emb.close()
                logger.info("  ✓ Embedding store closed")
        except Exception as e:
            logger.warning("server: %s", e)

        # 通知 SSE 客户端断开
        try:
            sse_broker.broadcast("shutdown", {"message": "Server shutting down"})
            logger.info(f"  ✓ SSE shutdown broadcast sent ({len(sse_broker._clients)} clients)")
        except Exception as e:
            logger.warning("server: %s", e)

        server.server_close()
        logger.info("🧠 Agent Memory Service stopped")


if __name__ == "__main__":
    main()
