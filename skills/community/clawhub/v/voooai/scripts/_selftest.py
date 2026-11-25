#!/usr/bin/env python3
"""离线自检（dev/CI 用，无需凭证与网络）。

覆盖 _common.py 的纯函数：ReactFlow 归一化、任务媒体提取、SSE 事件聚合、
业务错误格式化、路径白名单。运行：
    python3 _selftest.py
全部通过退出码 0，任一失败退出码 1。
"""

import os
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import _common  # noqa: E402

_PASS = 0
_FAIL = 0


def check(name, cond):
    global _PASS, _FAIL
    if cond:
        _PASS += 1
        print(f"  ✓ {name}")
    else:
        _FAIL += 1
        print(f"  ✗ {name}")


# ── 1. ReactFlow → 执行格式归一化 ──────────────────────────────────────────
def test_reactflow():
    print("[reactflow_to_workflow]")
    wf = {
        "nodes": [
            {"id": "n1", "type": "custom", "position": {"x": 1, "y": 2},
             "data": {"nodeType": "engine", "widgetValues": {"engine_type": "evolink_seedance"},
                      "storyboard_id": "sb1", "node_role": "video"}},
            {"id": "n2", "type": "custom", "position": {"x": 3, "y": 4},
             "data": {"nodeType": "prompt_input", "widgetValues": {"prompt": "hi"}}},
        ],
        "edges": [
            {"id": "e1", "source": "n2", "target": "n1", "sourceHandle": "output", "targetHandle": "input"},
        ],
        "viewport": {"x": 0, "y": 0, "zoom": 0.75},
    }
    out = _common.reactflow_to_workflow(wf, director_session_id="dv2_abc")
    n1 = out["nodes"][0]
    check("node.id → instance_id", n1["instance_id"] == "n1")
    check("data.nodeType → node_class", n1["node_class"] == "engine")
    check("data.widgetValues → widget_values", n1["widget_values"]["engine_type"] == "evolink_seedance")
    check("storyboard_id 保留", n1.get("storyboard_id") == "sb1")
    check("node_role 保留", n1.get("node_role") == "video")
    check("enabled 默认 True", n1["enabled"] is True)
    conns = out["connections"]
    check("edges → connections 数量", len(conns) == 1)
    check("source → source_node_id", conns[0]["source_node_id"] == "n2")
    check("target → target_node_id", conns[0]["target_node_id"] == "n1")
    check("sourceHandle → source_port", conns[0]["source_port"] == "output")
    check("director_session_id 注入", out["director_session_id"] == "dv2_abc")
    check("其他键(viewport)保留", out.get("viewport", {}).get("zoom") == 0.75)
    # 幂等：已是执行格式（含 node_class/instance_id）应原样保留
    again = _common.reactflow_to_workflow(out)
    check("幂等：node_class 不被破坏", again["nodes"][0]["node_class"] == "engine")
    check("幂等：connections 仍可用", len(again["connections"]) == 1)


# ── 2. 任务媒体提取 ────────────────────────────────────────────────────────
def test_extract_media():
    print("[extract_task_media]")
    task = {"status": "completed", "image_url": "https://a/1.png", "video_url": "", "audio_url": None}
    media = _common.extract_task_media(task)
    check("仅提取非空 URL", len(media) == 1 and media[0]["type"] == "image")
    task2 = {"video_url": "https://a/v.mp4", "audio_url": "https://a/s.mp3"}
    media2 = _common.extract_task_media(task2)
    check("视频+音频双提取", len(media2) == 2)
    check("空/非 dict 安全", _common.extract_task_media({}) == [] and _common.extract_task_media(None) == [])


# ── 3. SSE 事件聚合 ────────────────────────────────────────────────────────
def test_sse_dispatch():
    print("[_dispatch_sse]")
    r = {"session_id": "", "tab_id": "", "reply": "", "actions": [], "summaries": [],
         "resources": [], "done": None, "error": None, "points_charged": None,
         "session_points_total": None, "archive_id": None}
    _common._dispatch_sse(r, "session_start", '{"session_id":"dv2_x","tab_id":"t1"}')
    check("session_start 捕获 session_id", r["session_id"] == "dv2_x")
    check("session_start 捕获 tab_id", r["tab_id"] == "t1")
    _common._dispatch_sse(r, "token", '{"content":"你好"}')
    _common._dispatch_sse(r, "token", '{"content":"世界"}')
    check("token 文本聚合", r["reply"] == "你好世界")
    _common._dispatch_sse(r, "action", '{"type":"add_character","stage":2}')
    check("action 收集", len(r["actions"]) == 1 and r["actions"][0]["type"] == "add_character")
    _common._dispatch_sse(r, "summary", '{"id":"s1","stage":1}')
    check("summary 收集", len(r["summaries"]) == 1)
    _common._dispatch_sse(r, "resource", '{"file_id":"res1","url":"https://a/x.png"}')
    check("resource 收集", len(r["resources"]) == 1)
    _common._dispatch_sse(r, "ping", '{"ts":123}')
    check("ping 被跳过（不入任何列表）", len(r["actions"]) == 1 and r["reply"] == "你好世界")
    _common._dispatch_sse(r, "done", '{"message_id":"m1","points_charged":5,"archive_id":"ar1"}')
    check("done 记录", r["done"] is not None and r["done"]["message_id"] == "m1")
    check("done.points_charged 提取", r["points_charged"] == 5)
    check("done.archive_id 提取", r["archive_id"] == "ar1")
    # error 事件
    r2 = dict(r, error=None)
    _common._dispatch_sse(r2, "error", '{"code":"INSUFFICIENT_POINTS","message":"积分不足"}')
    check("error 事件解析", r2["error"]["code"] == "INSUFFICIENT_POINTS")
    # 非法 JSON 不崩溃
    r3 = dict(r)
    _common._dispatch_sse(r3, "token", "not-json")
    check("非法 data 不崩溃", isinstance(r3["reply"], str))
    # required_config 事件（2026-11-16 真实联调回归：曾被归为「未知事件」静默丢弃，
    # 导致 chat 已扣积分却只回空 reply、Agent 无从知道要补配置）
    r4 = dict(r)
    _common._dispatch_sse(
        r4, "required_config",
        '{"type":"ask_clarification","questions":[{"question_id":"aspect_ratio",'
        '"question":"画面尺寸","quick_options":[{"label":"横屏 16:9","value":"16:9"}]}],'
        '"original_message":"写个剧本"}')
    check("required_config 不被丢弃", r4.get("required_config") is not None)
    check("required_config.questions 保留",
          r4["required_config"]["questions"][0]["question_id"] == "aspect_ratio")
    check("required_config.original_message 保留",
          r4["required_config"]["original_message"] == "写个剧本")


# ── 4. 业务错误格式化 ──────────────────────────────────────────────────────
def test_format_error():
    print("[format_business_error]")
    m1 = _common.format_business_error(403, {"error_code": "MEMBERSHIP_REQUIRED", "message": "x"})
    check("会员门槛提示含 subscription", "付费会员" in m1 and "subscription" in m1)
    m2 = _common.format_business_error(400, {"message": "积分不足", "details": {"required": 10, "total_available": 3, "shortage": 7}})
    check("积分不足含缺口", "积分不足" in m2 and "缺口 7" in m2)
    m3 = _common.format_business_error(429, {"message": "too many"})
    check("429 频率限制", "并发" in m3 or "频率" in m3)
    m4 = _common.format_business_error(401, {})
    check("401 鉴权提示", "VOOOAI_ACCESS_KEY" in m4)


# ── 5. 路径白名单 ──────────────────────────────────────────────────────────
def test_whitelist():
    print("[validate_api_path]")
    for ok in ("/api/create-task", "/api/tasks/abc", "/api/director/v2/start",
               "/api/agent/capabilities", "/api/node-builder/execute", "/api/cos/request-upload"):
        try:
            _common.validate_api_path(ok)
            check(f"放行 {ok}", True)
        except SystemExit:
            check(f"放行 {ok}", False)
    for bad in ("/api/subscription/charge", "/api/admin/users", "/api/user/profile"):
        try:
            _common.validate_api_path(bad)
            check(f"拒绝 {bad}", False)
        except SystemExit:
            check(f"拒绝 {bad}", True)


# ── 6. 传输安全（origin/HTTPS/跨域重定向）──────────────────────────────
def test_transport_security():
    print("[transport security]")
    for ok in ("https://voooai.com", "https://www.voooai.com",
               "http://localhost:17966", "http://127.0.0.1:7966"):
        try:
            _common._validate_base_url(ok)
            check(f"放行 base {ok}", True)
        except SystemExit:
            check(f"放行 base {ok}", False)
    for bad in ("http://evil.com", "ftp://voooai.com",
                "https://user:pass@voooai.com", "https://"):
        try:
            _common._validate_base_url(bad)
            check(f"拒绝 base {bad}", False)
        except SystemExit:
            check(f"拒绝 base {bad}", True)
    u = _common._build_url("/api/agent/capabilities")
    check("_build_url 拼接正确", u == _common.BASE_URL.rstrip("/") + "/api/agent/capabilities")
    h = _common._SameOriginRedirectOnly()
    req = urllib.request.Request("https://voooai.com/api/tasks/x",
                                 headers={"Authorization": "Bearer k"})
    try:
        h.redirect_request(req, None, 302, "Found", {}, "https://evil.com/steal")
        check("跨域重定向被拦截", False)
    except urllib.error.URLError:
        check("跨域重定向被拦截", True)
    try:
        r2 = h.redirect_request(req, None, 302, "Found", {}, "https://voooai.com/api/tasks/y")
        check("同域重定向放行", r2 is not None)
    except Exception:
        check("同域重定向放行", False)


# ── 7. 错误文案多语言 ──────────────────────────────────────────────────
def test_locale():
    print("[format_business_error locale]")
    en = _common.format_business_error(403, {"error_code": "MEMBERSHIP_REQUIRED"}, locale="en")
    check("en 会员提示", "paid membership" in en)
    zh = _common.format_business_error(403, {"error_code": "MEMBERSHIP_REQUIRED"}, locale="zh")
    check("zh 会员提示", "付费会员" in zh)
    en2 = _common.format_business_error(400, {"details": {"shortage": 7}}, locale="en")
    check("en 积分不足含缺口", "Insufficient points" in en2 and "shortage 7" in en2)


def main():
    print("=== VoooAI skill 离线自检 ===")
    test_reactflow()
    test_extract_media()
    test_sse_dispatch()
    test_format_error()
    test_whitelist()
    test_transport_security()
    test_locale()
    print(f"\n结果: {_PASS} passed, {_FAIL} failed")
    sys.exit(1 if _FAIL else 0)


if __name__ == "__main__":
    main()
