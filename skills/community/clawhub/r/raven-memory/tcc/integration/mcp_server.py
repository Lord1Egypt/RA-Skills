"""
Raven MCP Server

Exposes the TCC DAG as MCP tools over stdio (JSON-RPC 2.0).
Compatible with OpenClaw, Claude Desktop, and any MCP client.

Usage:
    python3 -m tcc.integration.mcp_server

Environment variables:
    RAVEN_DB_PATH     path to raven.db (default: ~/.raven/raven.db)
    RAVEN_N_RECENT    recent nodes to inject (default: 10)
    RAVEN_N_SEARCH    semantic search results (default: 5)
"""
from __future__ import annotations

import json
import os
import sys
import traceback
from typing import Any

from tcc.core.dag import TaskDAG
from tcc.core.reconciler import SessionReconciler
from tcc.core.store import TCCStore

# ── configuration ─────────────────────────────────────────────────────────────

DB_PATH = os.environ.get(
    "RAVEN_DB_PATH",
    os.path.expanduser("~/.raven/raven.db"),
)
N_RECENT = int(os.environ.get("RAVEN_N_RECENT", "10"))
N_SEARCH = int(os.environ.get("RAVEN_N_SEARCH", "5"))

# ── global state ──────────────────────────────────────────────────────────────

_store: TCCStore | None = None
_dag: TaskDAG | None = None
_reconciler: SessionReconciler | None = None
_current_session_id: str | None = None


def _init() -> None:
    """Initialize Raven store, DAG, and reconciler."""
    global _store, _dag, _reconciler
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    _store = TCCStore(DB_PATH)
    _dag = TaskDAG(_store)
    _reconciler = SessionReconciler()


# ── tool definitions (MCP schema) ─────────────────────────────────────────────

TOOLS = [
    {
        "name": "raven_start_session",
        "description": (
            "Start a new Raven session and get project summary. "
            "Call this at the beginning of every conversation to load "
            "persistent memory. Returns a summary of recent events and "
            "semantically relevant history."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "search_query": {
                    "type": "string",
                    "description": (
                        "Optional: the user's first message or topic. "
                        "Used for semantic search over history to find "
                        "relevant past history beyond recent nodes."
                    ),
                },
                "n_recent": {
                    "type": "integer",
                    "description": "Number of recent nodes to include (default 10).",
                    "default": 10,
                },
            },
            "required": [],
        },
    },
    {
        "name": "raven_record_event",
        "description": (
            "Record an event to the Raven chain. Call this when "
            "something significant happens — a decision, an action, "
            "a tool result, a user preference, or any state change "
            "worth remembering across sessions."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "event": {
                    "type": "string",
                    "description": "What happened (natural language, concise).",
                },
                "actor": {
                    "type": "string",
                    "enum": ["user", "agent", "tool", "system"],
                    "description": "Who or what caused this event.",
                },
                "result_summary": {
                    "type": "string",
                    "description": "Optional: short summary of the result (max 200 chars).",
                },
                "tool_name": {
                    "type": "string",
                    "description": "Optional: name of the tool that was called.",
                },
            },
            "required": ["event", "actor"],
        },
    },
    {
        "name": "raven_end_session",
        "description": (
            "End the current session and save a closing note. "
            "Call this when the conversation is wrapping up or the "
            "user says goodbye. Records a session-end node so future "
            "sessions know where things stood."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "notes": {
                    "type": "string",
                    "description": "Summary of what was accomplished this session.",
                    "default": "",
                },
            },
            "required": [],
        },
    },
    {
        "name": "raven_search",
        "description": (
            "Semantic search over Raven's full history. Use this when "
            "the user asks about something that might be in past sessions "
            "but isn't in the current prompt window. Returns the most "
            "relevant nodes by meaning, not just recency."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "What to search for (natural language).",
                },
                "n": {
                    "type": "integer",
                    "description": "Number of results to return (default 5).",
                    "default": 5,
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "raven_rollback",
        "description": (
            "Roll the chain back N steps. Use this when the user says "
            "'that was wrong', 'undo that decision', or wants to go back "
            "to a previous state. History is preserved — rollback just "
            "moves the current tip pointer."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "steps": {
                    "type": "integer",
                    "description": "Number of steps to roll back (default 1).",
                    "default": 1,
                },
            },
            "required": [],
        },
    },
    {
        "name": "raven_get_status",
        "description": (
            "Get the current status of the Raven chain — tip event, "
            "total nodes, current session, and whether vec search is "
            "enabled. Useful for debugging and health checks."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
]


# ── tool handlers ─────────────────────────────────────────────────────────────

def handle_raven_start_session(params: dict) -> dict:
    global _current_session_id
    search_query = params.get("search_query")
    n_recent = params.get("n_recent", N_RECENT)

    ctx = _reconciler.start_session(
        _dag,
        n_recent=n_recent,
        search_query=search_query,
        n_search=N_SEARCH,
    )
    _current_session_id = ctx["session_id"]

    return {
        "session_id": ctx["session_id"],
        "is_fresh": ctx["is_fresh"],
        "summary": ctx["summary"],
        "message": (
            "Session started. Inject the 'summary' field into your "
            "system prompt so the agent has project history."
        ),
    }


def handle_raven_record_event(params: dict) -> dict:
    global _current_session_id

    if _current_session_id is None:
        ctx = _reconciler.start_session(_dag)
        _current_session_id = ctx["session_id"]

    node = _reconciler.record_event(
        dag=_dag,
        session_id=_current_session_id,
        event=params["event"],
        actor=params["actor"],
        status="done",
        result_summary=params.get("result_summary"),
        tool_name=params.get("tool_name"),
    )

    return {
        "hash": node.hash,
        "event": node.event,
        "recorded": True,
    }


def handle_raven_end_session(params: dict) -> dict:
    global _current_session_id

    if _current_session_id is None:
        return {"recorded": False, "message": "No active session to end."}

    notes = params.get("notes", "")
    node = _reconciler.end_session(_dag, _current_session_id, notes=notes)

    # Batch embed new nodes after session
    if _store.is_vec_enabled:
        n = _store.embed_all(batch_size=32)
        embedded_msg = f" Embedded {n} new nodes." if n > 0 else ""
    else:
        embedded_msg = ""

    prev_session = _current_session_id
    _current_session_id = None

    return {
        "session_id": prev_session,
        "recorded": node is not None,
        "message": f"Session ended.{embedded_msg}",
    }


def handle_raven_search(params: dict) -> dict:
    query = params["query"]
    n = params.get("n", N_SEARCH)

    if not _store.is_vec_enabled:
        return {
            "results": [],
            "message": "sqlite-vec not available. Install sqlite-vec for semantic search.",
        }

    nodes = _store.search(query, n=n)
    return {
        "results": [
            {
                "hash": node.hash,
                "event": node.event,
                "actor": node.actor,
                "timestamp": node.timestamp,
                "node_type": node.node_type,
                "result_summary": node.result_summary,
            }
            for node in nodes
        ],
        "n": len(nodes),
    }


def handle_raven_rollback(params: dict) -> dict:
    steps = params.get("steps", 1)
    try:
        node = _dag.rollback(steps)
        return {
            "rolled_back_to": node.event,
            "hash": node.hash,
            "message": f"Rolled back {steps} step(s). Now at: {node.event}",
        }
    except Exception as exc:
        return {"error": str(exc), "rolled_back": False}


def handle_raven_get_status(params: dict) -> dict:
    del params
    tip = _dag.tip()
    all_nodes = _store.load_all()
    return {
        "tip_event": tip.event if tip else None,
        "tip_hash": tip.hash if tip else None,
        "total_nodes": len(all_nodes),
        "current_session_id": _current_session_id,
        "db_path": DB_PATH,
        "vec_enabled": _store.is_vec_enabled,
        "is_fresh": tip is None,
    }


HANDLERS = {
    "raven_start_session": handle_raven_start_session,
    "raven_record_event": handle_raven_record_event,
    "raven_end_session": handle_raven_end_session,
    "raven_search": handle_raven_search,
    "raven_rollback": handle_raven_rollback,
    "raven_get_status": handle_raven_get_status,
}


# ── MCP protocol (JSON-RPC 2.0 over stdio) ────────────────────────────────────

def send(obj: dict) -> None:
    """Write a JSON-RPC response to stdout."""
    line = json.dumps(obj) + "\n"
    sys.stdout.write(line)
    sys.stdout.flush()


def send_error(id: Any, code: int, message: str) -> None:
    send({
        "jsonrpc": "2.0",
        "id": id,
        "error": {"code": code, "message": message},
    })


def send_result(id: Any, result: Any) -> None:
    send({
        "jsonrpc": "2.0",
        "id": id,
        "result": result,
    })


def handle_request(req: dict) -> None:
    """Dispatch a single JSON-RPC request."""
    req_id = req.get("id")
    method = req.get("method", "")
    params = req.get("params", {})

    # MCP initialization
    if method == "initialize":
        send_result(req_id, {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {
                "name": "raven-memory",
                "version": "1.0.0",
            },
        })
        return

    if method == "initialized":
        # Notification — no response needed
        return

    # Tool listing
    if method == "tools/list":
        send_result(req_id, {"tools": TOOLS})
        return

    # Tool execution
    if method == "tools/call":
        tool_name = params.get("name", "")
        tool_input = params.get("arguments", {})

        if tool_name not in HANDLERS:
            send_error(req_id, -32601, f"Unknown tool: {tool_name}")
            return

        try:
            result = HANDLERS[tool_name](tool_input)
            send_result(req_id, {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(result, indent=2),
                    }
                ],
                "isError": False,
            })
        except Exception as exc:
            send_result(req_id, {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error: {exc}\n{traceback.format_exc()}",
                    }
                ],
                "isError": True,
            })
        return

    # Ping
    if method == "ping":
        send_result(req_id, {})
        return

    send_error(req_id, -32601, f"Method not found: {method}")


def main() -> None:
    """Main stdio loop — read JSON-RPC requests, dispatch, respond."""
    _init()

    # Log to stderr only (stdout is reserved for MCP protocol)
    print(
        f"Raven MCP server started. DB: {DB_PATH}",
        file=sys.stderr,
    )

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            handle_request(req)
        except json.JSONDecodeError as exc:
            send_error(None, -32700, f"Parse error: {exc}")
        except Exception as exc:
            send_error(None, -32603, f"Internal error: {exc}")


if __name__ == "__main__":
    main()
