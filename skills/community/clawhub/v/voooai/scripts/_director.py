"""编导模式脚本共享助手（内部模块，非用户直接调用）。

集中处理：会话状态解析、SSE 结果整理、阶段状态查询、编导端点 GET/POST 封装，
供 director_start / director_chat / director_status / director_navigate /
director_confirm / director_export / director_execute_video 复用。
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from _common import (
    http_request,
    format_business_error,
    resolve_session,
    save_session_state,
    load_session_state,
)


def _qs(tab_id: str) -> str:
    """构造 tab_id 查询串。"""
    return f"?tab_id={tab_id}" if tab_id else ""


def director_get_status(session_id: str, tab_id: str = "", full: bool = False):
    """GET /api/director/v2/<sid>/status（或 /full_state）。返回 (status_code, data)。"""
    sub = "full_state" if full else "status"
    return http_request("GET", f"/api/director/v2/{session_id}/{sub}{_qs(tab_id)}")


def director_post(session_id: str, subpath: str, body: dict, tab_id: str = ""):
    """POST /api/director/v2/<sid>/<subpath>（JSON）。返回 (status_code, data)。"""
    return http_request("POST", f"/api/director/v2/{session_id}/{subpath}", body)


def stage_brief(session_id: str, tab_id: str = "") -> dict:
    """取 current_stage / stage_statuses 摘要（尽力而为，失败返回 {}）。"""
    code, data = director_get_status(session_id, tab_id, full=False)
    if code == 200 and isinstance(data, dict) and data.get("success"):
        return {
            "current_stage": data.get("current_stage"),
            "stage_statuses": data.get("stage_statuses", {}),
            "session_status": data.get("status"),
        }
    return {}


def finalize_turn(result: dict, session_id: str = None, tab_id: str = None,
                  with_stage: bool = True) -> dict:
    """
    把 api_post_stream 的聚合结果整理为统一输出 dict（不 sys.exit，始终返回可 JSON 化的结果）。

    - 有 error：返回 {'success': False, 'error', 'error_code', 'message'(友好提示), ...}
    - 成功：返回 {'success', 'session_id', 'tab_id', 'reply', 'actions', 'summaries',
                 'resources', 'points_charged'?, ...}，并可选补 current_stage/stage_statuses
    """
    sid = session_id or result.get("session_id", "")
    tid = tab_id if tab_id is not None else result.get("tab_id", "")

    if result.get("error"):
        err = result["error"]
        code = result.get("http_status", 0)
        if code:
            friendly = format_business_error(
                code, {"error_code": err.get("code", ""), "message": err.get("message", ""), "details": {}}
            )
        else:
            friendly = f"[{err.get('code', '')}] {err.get('message', '')}"
        return {
            "success": False,
            "session_id": sid,
            "tab_id": tid,
            "error": err,
            "error_code": err.get("code", ""),
            "message": friendly,
        }

    out = {
        "success": bool(result.get("ok")),
        "session_id": sid,
        "tab_id": tid,
        "reply": result.get("reply", ""),
        "actions": result.get("actions", []),
        "summaries": result.get("summaries", []),
        "resources": result.get("resources", []),
    }
    if result.get("points_charged") is not None:
        out["points_charged"] = result["points_charged"]
    if result.get("session_points_total") is not None:
        out["session_points_total"] = result["session_points_total"]
    if result.get("archive_id"):
        out["archive_id"] = result["archive_id"]
    if result.get("timed_out"):
        out["timed_out"] = True
        out["hint"] = "SSE 流超时；会话可能仍在推进，请稍后用 director_status.py 查看"

    # ★ 2026-11-16：后端要求先确认全局必填配置（画面比例/分辨率/时长/对白语言等）。
    #   此时本轮不会生成剧本，reply 为空属预期；必须把 questions 交给用户拍板，
    #   再用 director_chat.py 回传 [REQUIRED_CONFIG] 指令，后端才会重走守门流程。
    rc = result.get("required_config")
    if rc:
        out["needs_config"] = True
        out["required_config"] = rc
        out["hint"] = (
            "后端拦截：需先确认全局必填配置，本轮未生成内容（reply 为空属预期）。"
            "请把 required_config.questions 的选项呈现给用户拍板（question / label 为文案，value 为回传值），"
            "然后用 director_chat.py 发送回传指令（content 原样传入、勿改写）："
            '[REQUIRED_CONFIG]{"config":{"<question_id>":"<value>"},"original_message":"<原消息>"}'
            "；original_message 取 required_config.original_message。"
        )

    if with_stage and sid:
        brief = stage_brief(sid, tid)
        if brief:
            out.update(brief)
    return out


def require_session(args) -> tuple:
    """
    从 CLI 参数解析 (session_id, tab_id)：优先 --session-id/--tab-id，否则读状态文件。
    session_id 缺失时友好报错退出。
    """
    from _common import error_exit
    state_file = getattr(args, "state_file", None)
    session_id, tab_id = resolve_session(
        getattr(args, "session_id", None),
        getattr(args, "tab_id", None),
        state_file,
    )
    if not session_id:
        error_exit("缺少 session_id：请先运行 director_start.py，或用 --session-id 指定"
                   f"（状态文件：{state_file or '.voooai_director_session.json'}）")
    return session_id, tab_id
