from flask import Flask, render_template, request, jsonify, session, Response
import requests
import os
from dotenv import load_dotenv

# 加载 .env 配置
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
load_dotenv(dotenv_path=os.path.join(root_dir, "config", ".env"))

app = Flask(__name__,
            template_folder=os.path.join(current_dir, 'templates'),
            static_folder=os.path.join(current_dir, 'static'))
app.secret_key = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB for image uploads

# --- 配置区 ---
PORT_AGENT = int(os.getenv("PORT_AGENT", "51200"))
# [已弃用] 旧端点 URL，已被 /v1/chat/completions 替代
# LOCAL_AGENT_URL = f"http://127.0.0.1:{PORT_AGENT}/ask"
# LOCAL_AGENT_STREAM_URL = f"http://127.0.0.1:{PORT_AGENT}/ask_stream"
LOCAL_AGENT_CANCEL_URL = f"http://127.0.0.1:{PORT_AGENT}/cancel"
LOCAL_LOGIN_URL = f"http://127.0.0.1:{PORT_AGENT}/login"
LOCAL_TOOLS_URL = f"http://127.0.0.1:{PORT_AGENT}/tools"
LOCAL_SESSIONS_URL = f"http://127.0.0.1:{PORT_AGENT}/sessions"
LOCAL_SESSION_HISTORY_URL = f"http://127.0.0.1:{PORT_AGENT}/session_history"
LOCAL_DELETE_SESSION_URL = f"http://127.0.0.1:{PORT_AGENT}/delete_session"
LOCAL_TTS_URL = f"http://127.0.0.1:{PORT_AGENT}/tts"
LOCAL_SESSION_STATUS_URL = f"http://127.0.0.1:{PORT_AGENT}/session_status"
# OpenAI 兼容端点
LOCAL_OPENAI_COMPLETIONS_URL = f"http://127.0.0.1:{PORT_AGENT}/v1/chat/completions"
INTERNAL_TOKEN = os.getenv("INTERNAL_TOKEN", "")

# OASIS Forum proxy
PORT_OASIS = int(os.getenv("PORT_OASIS", "51202"))
OASIS_BASE_URL = f"http://127.0.0.1:{PORT_OASIS}"


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/manifest.json")
def manifest():
    """Serve PWA manifest for iOS/Android Add-to-Home-Screen support."""
    manifest_data = {
        "name": "Teamclaw",
        "short_name": "Teamclaw",
        "description": "TeamBot AI Agent - Intelligent Control Assistant",
        "start_url": "/",
        "scope": "/",
        "display": "standalone",
        "orientation": "portrait",
        "background_color": "#111827",
        "theme_color": "#111827",
        "lang": "zh-CN",
        "categories": ["productivity", "utilities"],
        "icons": [
            {
                "src": "https://img.icons8.com/fluency/192/robot-2.png",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "https://img.icons8.com/fluency/512/robot-2.png",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any maskable"
            }
        ]
    }
    return app.response_class(
        response=__import__("json").dumps(manifest_data),
        mimetype="application/manifest+json"
    )


@app.route("/sw.js")
def service_worker():
    """Serve Service Worker for PWA offline support and caching."""
    sw_code = """
// Teamclaw Service Worker v3
const CACHE_NAME = 'teamclaw-v3';
const PRECACHE_URLS = ['/'];

self.addEventListener('install', event => {
    self.skipWaiting();
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => cache.addAll(PRECACHE_URLS))
    );
});

self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(keys =>
            Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
        ).then(() => self.clients.claim())
    );
});

self.addEventListener('fetch', event => {
    // CRITICAL: Only handle GET requests. Non-GET (POST, PUT, DELETE) must pass through directly.
    if (event.request.method !== 'GET') return;

    // API GET requests also pass through without SW interference
    const url = event.request.url;
    if (url.includes('/proxy_') || url.includes('/ask') || url.includes('/v1/') || url.includes('/api/')) return;

    // Cache-first for static GET assets only
    event.respondWith(
        caches.match(event.request).then(cached => {
            const fetched = fetch(event.request).then(response => {
                if (response.ok) {
                    const clone = response.clone();
                    caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
                }
                return response;
            }).catch(() => cached);
            return cached || fetched;
        })
    );
});
"""
    return app.response_class(
        response=sw_code,
        mimetype="application/javascript",
        headers={"Service-Worker-Allowed": "/"}
    )


@app.route("/v1/chat/completions", methods=["POST", "OPTIONS"])
def proxy_openai_completions():
    """OpenAI 兼容端点透传：前端直接发 OpenAI 格式，原样转发到后端"""
    if request.method == "OPTIONS":
        # CORS preflight
        resp = Response("", status=204)
        resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return resp

    # 直接透传请求体和 Authorization header 到后端
    auth_header = request.headers.get("Authorization", "")
    try:
        r = requests.post(
            LOCAL_OPENAI_COMPLETIONS_URL,
            json=request.get_json(silent=True),
            headers={
                "Authorization": auth_header,
                "Content-Type": "application/json",
            },
            stream=True,
            timeout=120,
        )
        if r.status_code != 200:
            return Response(r.content, status=r.status_code, content_type=r.headers.get("content-type", "application/json"))

        # 判断是否是流式响应
        content_type = r.headers.get("content-type", "")
        if "text/event-stream" in content_type:
            def generate():
                for chunk in r.iter_content(chunk_size=None):
                    if chunk:
                        yield chunk
            return Response(
                generate(),
                mimetype="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no",
                },
            )
        else:
            return Response(r.content, status=r.status_code, content_type=content_type)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/v1/models", methods=["GET"])
def proxy_openai_models():
    """透传 /v1/models"""
    try:
        r = requests.get(f"http://127.0.0.1:{PORT_AGENT}/v1/models", timeout=10)
        return Response(r.content, status=r.status_code, content_type=r.headers.get("content-type", "application/json"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/proxy_login", methods=["POST"])
def proxy_login():
    """代理登录请求到后端 Agent"""
    user_id = request.json.get("user_id", "")
    password = request.json.get("password", "")

    try:
        r = requests.post(LOCAL_LOGIN_URL, json={"user_id": user_id, "password": password}, timeout=10)
        if r.status_code == 200:
            # 登录成功，在 Flask session 中记录
            session["user_id"] = user_id
            session["password"] = password  # 需要传给后端每次验证
            return jsonify(r.json())
        else:
            return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ──────────────────────────────────────────────────────────────
# [已弃用] proxy_ask 和 proxy_ask_stream — 已被前端直接调用
# /v1/chat/completions 替代，以下端点注释保留备查。
# ──────────────────────────────────────────────────────────────
# @app.route("/proxy_ask", methods=["POST"])
# def proxy_ask():
#     ...
#
# @app.route("/proxy_ask_stream", methods=["POST"])
# def proxy_ask_stream():
#     ...

@app.route("/proxy_cancel", methods=["POST"])
def proxy_cancel():
    """代理取消请求到后端 Agent"""
    user_id = session.get("user_id")
    password = session.get("password")
    if not user_id or not password:
        return jsonify({"error": "未登录"}), 401
    session_id = request.json.get("session_id", "default") if request.is_json else "default"
    try:
        r = requests.post(LOCAL_AGENT_CANCEL_URL, json={"user_id": user_id, "password": password, "session_id": session_id}, timeout=5)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/proxy_tts", methods=["POST"])
def proxy_tts():
    """代理 TTS 请求到后端 Agent，返回 mp3 音频流"""
    user_id = session.get("user_id")
    password = session.get("password")
    if not user_id or not password:
        return jsonify({"error": "未登录"}), 401

    text = request.json.get("text", "")
    voice = request.json.get("voice")
    if not text.strip():
        return jsonify({"error": "文本不能为空"}), 400

    try:
        payload = {"user_id": user_id, "password": password, "text": text}
        if voice:
            payload["voice"] = voice
        r = requests.post(LOCAL_TTS_URL, json=payload, timeout=60)
        if r.status_code != 200:
            return jsonify({"error": f"TTS 服务错误: {r.status_code}"}), r.status_code

        return Response(
            r.content,
            mimetype="audio/mpeg",
            headers={"Content-Disposition": "inline; filename=tts_output.mp3"},
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/proxy_tools")
def proxy_tools():
    """代理获取工具列表请求到后端 Agent"""
    try:
        r = requests.get(LOCAL_TOOLS_URL, headers={"X-Internal-Token": INTERNAL_TOKEN}, timeout=10)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e), "tools": []}), 500

@app.route("/proxy_logout", methods=["POST"])
def proxy_logout():
    session.clear()
    return jsonify({"status": "success"})


LOCAL_SETTINGS_URL = f"http://127.0.0.1:{PORT_AGENT}/settings"


@app.route("/proxy_settings", methods=["GET"])
def proxy_get_settings():
    """代理获取系统配置"""
    user_id = session.get("user_id")
    password = session.get("password")
    if not user_id or not password:
        return jsonify({"error": "未登录"}), 401
    try:
        r = requests.get(LOCAL_SETTINGS_URL, params={"user_id": user_id, "password": password}, timeout=10)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/proxy_settings", methods=["POST"])
def proxy_update_settings():
    """代理更新系统配置"""
    user_id = session.get("user_id")
    password = session.get("password")
    if not user_id or not password:
        return jsonify({"error": "未登录"}), 401
    try:
        data = request.get_json(force=True)
        data["user_id"] = user_id
        data["password"] = password
        r = requests.post(LOCAL_SETTINGS_URL, json=data, timeout=10)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/proxy_sessions")
def proxy_sessions():
    """代理获取用户会话列表"""
    user_id = session.get("user_id")
    password = session.get("password")
    if not user_id or not password:
        return jsonify({"error": "未登录"}), 401
    try:
        r = requests.post(LOCAL_SESSIONS_URL, json={"user_id": user_id, "password": password}, timeout=15)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/proxy_sessions_status")
def proxy_sessions_status():
    """代理获取用户所有 session 的忙碌状态"""
    user_id = session.get("user_id")
    password = session.get("password")
    if not user_id or not password:
        return jsonify({"error": "未登录"}), 401
    try:
        r = requests.post(
            f"http://127.0.0.1:{PORT_AGENT}/sessions_status",
            json={"user_id": user_id, "password": password},
            timeout=5,
        )
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/proxy_openclaw_sessions")
def proxy_openclaw_sessions():
    """Proxy to fetch OpenClaw session list from OASIS server."""
    filter_kw = request.args.get("filter", "")
    try:
        r = requests.get(
            f"{OASIS_BASE_URL}/sessions/openclaw",
            params={"filter": filter_kw},
            timeout=10,
        )
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e), "sessions": [], "available": False}), 500


@app.route("/proxy_session_history", methods=["POST"])
def proxy_session_history():
    """代理获取指定会话的历史消息"""
    user_id = session.get("user_id")
    password = session.get("password")
    if not user_id or not password:
        return jsonify({"error": "未登录"}), 401
    sid = request.json.get("session_id", "")
    try:
        r = requests.post(LOCAL_SESSION_HISTORY_URL, json={
            "user_id": user_id, "password": password, "session_id": sid
        }, timeout=15)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/proxy_session_status", methods=["POST"])
def proxy_session_status():
    """代理检查会话是否有系统触发的新消息"""
    user_id = session.get("user_id")
    password = session.get("password")
    if not user_id or not password:
        return jsonify({"has_new_messages": False}), 200
    sid = request.json.get("session_id", "") if request.is_json else ""
    try:
        r = requests.post(LOCAL_SESSION_STATUS_URL, json={
            "user_id": user_id, "password": password, "session_id": sid
        }, timeout=5)
        return jsonify(r.json()), r.status_code
    except Exception:
        return jsonify({"has_new_messages": False}), 200


@app.route("/proxy_delete_session", methods=["POST"])
def proxy_delete_session():
    """代理删除会话请求到后端 Agent"""
    user_id = session.get("user_id")
    password = session.get("password")
    if not user_id or not password:
        return jsonify({"error": "未登录"}), 401
    sid = request.json.get("session_id", "") if request.is_json else ""
    try:
        r = requests.post(LOCAL_DELETE_SESSION_URL, json={
            "user_id": user_id, "password": password, "session_id": sid
        }, timeout=15)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ===== Group Chat Proxy Routes =====

def _group_auth_headers():
    """构造群聊API的Authorization header"""
    user_id = session.get("user_id")
    password = session.get("password")
    if not user_id or not password:
        return None, None
    return user_id, {"Authorization": f"Bearer {user_id}:{password}"}


@app.route("/proxy_groups", methods=["GET"])
def proxy_list_groups():
    """代理列出用户群聊"""
    uid, headers = _group_auth_headers()
    if not uid:
        return jsonify([]), 200
    try:
        r = requests.get(f"http://127.0.0.1:{PORT_AGENT}/groups", headers=headers, timeout=10)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/proxy_groups", methods=["POST"])
def proxy_create_group():
    """代理创建群聊"""
    uid, headers = _group_auth_headers()
    if not uid:
        return jsonify({"error": "未登录"}), 401
    try:
        headers["Content-Type"] = "application/json"
        r = requests.post(f"http://127.0.0.1:{PORT_AGENT}/groups", json=request.get_json(silent=True), headers=headers, timeout=10)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/proxy_groups/<group_id>", methods=["GET"])
def proxy_get_group(group_id):
    """代理获取群聊详情"""
    uid, headers = _group_auth_headers()
    if not uid:
        return jsonify({"error": "未登录"}), 401
    try:
        r = requests.get(f"http://127.0.0.1:{PORT_AGENT}/groups/{group_id}", headers=headers, timeout=10)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/proxy_groups/<group_id>", methods=["PUT"])
def proxy_update_group(group_id):
    """代理更新群聊"""
    uid, headers = _group_auth_headers()
    if not uid:
        return jsonify({"error": "未登录"}), 401
    try:
        headers["Content-Type"] = "application/json"
        r = requests.put(f"http://127.0.0.1:{PORT_AGENT}/groups/{group_id}", json=request.get_json(silent=True), headers=headers, timeout=10)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/proxy_groups/<group_id>", methods=["DELETE"])
def proxy_delete_group(group_id):
    """代理删除群聊"""
    uid, headers = _group_auth_headers()
    if not uid:
        return jsonify({"error": "未登录"}), 401
    try:
        r = requests.delete(f"http://127.0.0.1:{PORT_AGENT}/groups/{group_id}", headers=headers, timeout=10)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/proxy_groups/<group_id>/messages", methods=["GET"])
def proxy_group_messages(group_id):
    """代理获取群聊消息（支持增量 after_id）"""
    uid, headers = _group_auth_headers()
    if not uid:
        return jsonify({"messages": []}), 200
    try:
        after_id = request.args.get("after_id", "0")
        r = requests.get(
            f"http://127.0.0.1:{PORT_AGENT}/groups/{group_id}/messages",
            params={"after_id": after_id},
            headers=headers, timeout=10,
        )
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/proxy_groups/<group_id>/messages", methods=["POST"])
def proxy_post_group_message(group_id):
    """代理发送群聊消息"""
    uid, headers = _group_auth_headers()
    if not uid:
        return jsonify({"error": "未登录"}), 401
    try:
        headers["Content-Type"] = "application/json"
        r = requests.post(
            f"http://127.0.0.1:{PORT_AGENT}/groups/{group_id}/messages",
            json=request.get_json(silent=True),
            headers=headers, timeout=10,
        )
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/proxy_groups/<group_id>/mute", methods=["POST"])
def proxy_mute_group(group_id):
    """代理静音群聊"""
    uid, headers = _group_auth_headers()
    if not uid:
        return jsonify({"error": "未登录"}), 401
    try:
        r = requests.post(
            f"http://127.0.0.1:{PORT_AGENT}/groups/{group_id}/mute",
            headers=headers, timeout=10,
        )
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/proxy_groups/<group_id>/unmute", methods=["POST"])
def proxy_unmute_group(group_id):
    """代理取消静音群聊"""
    uid, headers = _group_auth_headers()
    if not uid:
        return jsonify({"error": "未登录"}), 401
    try:
        r = requests.post(
            f"http://127.0.0.1:{PORT_AGENT}/groups/{group_id}/unmute",
            headers=headers, timeout=10,
        )
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/proxy_groups/<group_id>/mute_status", methods=["GET"])
def proxy_group_mute_status(group_id):
    """代理查询群聊静音状态"""
    uid, headers = _group_auth_headers()
    if not uid:
        return jsonify({"muted": False}), 200
    try:
        r = requests.get(
            f"http://127.0.0.1:{PORT_AGENT}/groups/{group_id}/mute_status",
            headers=headers, timeout=10,
        )
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/proxy_groups/<group_id>/sessions", methods=["GET"])
def proxy_group_sessions(group_id):
    """代理获取可加入群聊的sessions"""
    uid, headers = _group_auth_headers()
    if not uid:
        return jsonify({"sessions": []}), 200
    try:
        r = requests.get(
            f"http://127.0.0.1:{PORT_AGENT}/groups/{group_id}/sessions",
            headers=headers, timeout=15,
        )
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"sessions": [], "error": str(e)}), 500


# ===== OASIS Proxy Routes =====

@app.route("/proxy_oasis/topics")
def proxy_oasis_topics():
    """Proxy: list OASIS discussion topics for the logged-in user."""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify([]), 200
    try:
        print(f"[OASIS Proxy] Fetching topics from {OASIS_BASE_URL}/topics for user={user_id}")
        r = requests.get(f"{OASIS_BASE_URL}/topics", params={"user_id": user_id}, timeout=10)
        print(f"[OASIS Proxy] Response status: {r.status_code}, count: {len(r.json()) if r.text else 0}")
        return jsonify(r.json()), r.status_code
    except Exception as e:
        print(f"[OASIS Proxy] Error fetching topics: {e}")
        return jsonify([]), 200  # Return empty list on error


@app.route("/proxy_oasis/topics/<topic_id>")
def proxy_oasis_topic_detail(topic_id):
    """Proxy: get full detail of a specific OASIS discussion."""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "未登录"}), 401
    try:
        url = f"{OASIS_BASE_URL}/topics/{topic_id}"
        print(f"[OASIS Proxy] Fetching topic detail from {url} for user={user_id}")
        r = requests.get(url, params={"user_id": user_id}, timeout=10)
        print(f"[OASIS Proxy] Detail response status: {r.status_code}")
        return jsonify(r.json()), r.status_code
    except Exception as e:
        print(f"[OASIS Proxy] Error fetching topic detail: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/proxy_oasis/topics/<topic_id>/stream")
def proxy_oasis_topic_stream(topic_id):
    """Proxy: SSE stream for real-time OASIS discussion updates."""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "未登录"}), 401
    try:
        r = requests.get(
            f"{OASIS_BASE_URL}/topics/{topic_id}/stream",
            params={"user_id": user_id},
            stream=True, timeout=300,
        )
        if r.status_code != 200:
            return jsonify({"error": f"OASIS returned {r.status_code}"}), r.status_code

        def generate():
            for line in r.iter_lines(decode_unicode=True):
                if line:
                    yield line + "\n\n"

        return Response(
            generate(),
            mimetype="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/proxy_oasis/experts")
def proxy_oasis_experts():
    """Proxy: list all OASIS expert agents."""
    user_id = session.get("user_id", "")
    try:
        r = requests.get(f"{OASIS_BASE_URL}/experts", params={"user_id": user_id}, timeout=10)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/proxy_oasis/topics/<topic_id>/cancel", methods=["POST"])
def proxy_oasis_cancel_topic(topic_id):
    """Proxy: force-cancel a running OASIS discussion."""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "未登录"}), 401
    try:
        r = requests.delete(f"{OASIS_BASE_URL}/topics/{topic_id}", params={"user_id": user_id}, timeout=10)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/proxy_oasis/topics/<topic_id>/purge", methods=["POST"])
def proxy_oasis_purge_topic(topic_id):
    """Proxy: permanently delete an OASIS discussion record."""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "未登录"}), 401
    try:
        r = requests.post(f"{OASIS_BASE_URL}/topics/{topic_id}/purge", params={"user_id": user_id}, timeout=10)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/proxy_oasis/topics", methods=["DELETE"])
def proxy_oasis_purge_all_topics():
    """Proxy: delete all OASIS topics for the current user."""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "未登录"}), 401
    try:
        r = requests.delete(f"{OASIS_BASE_URL}/topics", params={"user_id": user_id}, timeout=30)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ──────────────────────────────────────────────────────────────
# Visual Orchestration – proxy endpoints
# ──────────────────────────────────────────────────────────────
import sys as _sys, math as _math, re as _re, yaml as _yaml

# Import expert pool & conversion helpers from visual/main.py
_VISUAL_DIR = os.path.join(root_dir, "visual")
if _VISUAL_DIR not in _sys.path:
    _sys.path.insert(0, _VISUAL_DIR)

try:
    from main import (
        DEFAULT_EXPERTS as _VIS_EXPERTS,
        TAG_EMOJI as _VIS_TAG_EMOJI,
        layout_to_yaml as _vis_layout_to_yaml,
        _build_llm_prompt as _vis_build_llm_prompt,
        _extract_yaml_from_response as _vis_extract_yaml,
        _validate_generated_yaml as _vis_validate_yaml,
    )
except Exception:
    # Fallback: define minimal versions if visual module unavailable
    _VIS_EXPERTS = []
    _VIS_TAG_EMOJI = {}
    _vis_layout_to_yaml = None
    _vis_build_llm_prompt = None
    _vis_extract_yaml = None
    _vis_validate_yaml = None

# Import YAML→Layout converter (used for on-the-fly layout generation from saved YAML)
try:
    from mcp_oasis import _yaml_to_layout_data as _vis_yaml_to_layout
except Exception:
    _vis_yaml_to_layout = None


@app.route("/proxy_visual/experts", methods=["GET"])
def proxy_visual_experts():
    """Return available expert pool for orchestration canvas (public + user custom)."""
    user_id = session.get("user_id", "")
    # Fetch full expert list from OASIS server (public + user custom)
    all_experts = []
    try:
        r = requests.get(f"{OASIS_BASE_URL}/experts", params={"user_id": user_id}, timeout=5)
        if r.ok:
            all_experts = r.json().get("experts", [])
    except Exception:
        pass

    # Fallback to static list if OASIS unavailable
    if not all_experts:
        all_experts = [{**e, "source": "public"} for e in _VIS_EXPERTS]

    result = []
    for e in all_experts:
        emoji = _VIS_TAG_EMOJI.get(e.get("tag", ""), "⭐")
        if e.get("source") == "custom":
            emoji = "🛠️"
        result.append({**e, "emoji": emoji})
    return jsonify(result)


@app.route("/proxy_visual/experts/custom", methods=["POST"])
def proxy_visual_add_custom_expert():
    """Add a custom expert via OASIS server."""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "未登录"}), 401
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data"}), 400
    try:
        r = requests.post(
            f"{OASIS_BASE_URL}/experts/user",
            json={"user_id": user_id, **data},
            timeout=10,
        )
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/proxy_visual/experts/custom/<tag>", methods=["DELETE"])
def proxy_visual_delete_custom_expert(tag):
    """Delete a custom expert via OASIS server."""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "未登录"}), 401
    try:
        r = requests.delete(
            f"{OASIS_BASE_URL}/experts/user/{tag}",
            params={"user_id": user_id},
            timeout=10,
        )
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/proxy_visual/generate-yaml", methods=["POST"])
def proxy_visual_generate_yaml():
    """Convert canvas layout to OASIS YAML (rule-based)."""
    data = request.get_json()
    if not data or not _vis_layout_to_yaml:
        return jsonify({"error": "No data or visual module unavailable"}), 400
    try:
        yaml_out = _vis_layout_to_yaml(data)
        return jsonify({"yaml": yaml_out})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/proxy_visual/agent-generate-yaml", methods=["POST"])
def proxy_visual_agent_generate_yaml():
    """Build prompt + send to main agent using session credentials → get YAML."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data"}), 400

    user_id = session.get("user_id")
    password = session.get("password")
    if not user_id or not password:
        return jsonify({"error": "Not logged in"}), 401

    try:
        prompt = _vis_build_llm_prompt(data) if _vis_build_llm_prompt else "Error: visual module unavailable"

        # Call main agent with user credentials
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {user_id}:{password}",
        }
        payload = {
            "model": "mini-timebot",
            "messages": [
                {"role": "system", "content": (
                    "You are a YAML schedule generator for the OASIS expert orchestration engine. "
                    "Output ONLY valid YAML, no markdown fences, no explanations, no commentary. "
                    "The YAML must start with 'version: 1' and contain a 'plan:' section."
                )},
                {"role": "user", "content": prompt},
            ],
            "stream": False,
            "session_id": data.get("target_session_id") or "visual_orchestrator",
            "temperature": 0.3,
        }
        resp = requests.post(LOCAL_OPENAI_COMPLETIONS_URL, json=payload, headers=headers, timeout=60)
        if resp.status_code != 200:
            return jsonify({"prompt": prompt, "error": f"Agent returned HTTP {resp.status_code}: {resp.text[:500]}", "agent_yaml": None})

        result = resp.json()
        agent_reply = ""
        try:
            agent_reply = result["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            agent_reply = str(result)

        agent_yaml = _vis_extract_yaml(agent_reply) if _vis_extract_yaml else agent_reply
        validation = _vis_validate_yaml(agent_yaml) if _vis_validate_yaml else {"valid": False, "error": "validator unavailable"}

        # Auto-save valid YAML to user's oasis/yaml directory
        saved_path = None
        if validation.get("valid"):
            try:
                import time as _time
                yaml_dir = os.path.join(root_dir, "data", "user_files", user_id, "oasis", "yaml")
                os.makedirs(yaml_dir, exist_ok=True)
                fname = data.get("save_name") or f"orch_{_time.strftime('%Y%m%d_%H%M%S')}"
                if not fname.endswith((".yaml", ".yml")):
                    fname += ".yaml"
                fpath = os.path.join(yaml_dir, fname)
                with open(fpath, "w", encoding="utf-8") as _yf:
                    _yf.write(f"# Auto-generated from visual orchestrator\n{agent_yaml}")
                saved_path = fname
            except Exception as save_err:
                saved_path = f"save_error: {save_err}"

        return jsonify({"prompt": prompt, "agent_yaml": agent_yaml, "agent_reply_raw": agent_reply, "validation": validation, "saved_file": saved_path})

    except requests.exceptions.ConnectionError:
        prompt = _vis_build_llm_prompt(data) if _vis_build_llm_prompt else ""
        return jsonify({"prompt": prompt, "error": "Cannot connect to main agent. Is mainagent.py running?", "agent_yaml": None})
    except requests.exceptions.Timeout:
        prompt = _vis_build_llm_prompt(data) if _vis_build_llm_prompt else ""
        return jsonify({"prompt": prompt, "error": "Agent request timed out (60s).", "agent_yaml": None})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/proxy_visual/save-layout", methods=["POST"])
def proxy_visual_save_layout():
    """Save canvas layout as YAML (no separate layout JSON stored)."""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data"}), 400
    if not _vis_layout_to_yaml:
        return jsonify({"error": "Layout-to-YAML converter unavailable"}), 500
    name = data.get("name", "untitled")
    safe = "".join(c for c in name if c.isalnum() or c in "-_ ").strip() or "untitled"
    try:
        yaml_out = _vis_layout_to_yaml(data)
    except Exception as e:
        return jsonify({"error": f"YAML conversion failed: {e}"}), 500
    yaml_dir = os.path.join(root_dir, "data", "user_files", user_id, "oasis", "yaml")
    os.makedirs(yaml_dir, exist_ok=True)
    fpath = os.path.join(yaml_dir, f"{safe}.yaml")
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(f"# Saved from visual orchestrator\n{yaml_out}")
    return jsonify({"saved": True})


@app.route("/proxy_visual/load-layouts", methods=["GET"])
def proxy_visual_load_layouts():
    """List saved YAML workflows as available layouts."""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify([])
    yaml_dir = os.path.join(root_dir, "data", "user_files", user_id, "oasis", "yaml")
    if not os.path.isdir(yaml_dir):
        return jsonify([])
    return jsonify([f.replace('.yaml', '').replace('.yml', '') for f in sorted(os.listdir(yaml_dir)) if f.endswith((".yaml", ".yml"))])


@app.route("/proxy_visual/load-layout/<name>", methods=["GET"])
def proxy_visual_load_layout(name):
    """Load a layout by reading the YAML file and converting to layout on-the-fly."""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401
    if not _vis_yaml_to_layout:
        return jsonify({"error": "YAML-to-layout converter unavailable"}), 500
    safe = "".join(c for c in name if c.isalnum() or c in "-_ ").strip()
    yaml_dir = os.path.join(root_dir, "data", "user_files", user_id, "oasis", "yaml")
    # Try .yaml then .yml
    fpath = os.path.join(yaml_dir, f"{safe}.yaml")
    if not os.path.isfile(fpath):
        fpath = os.path.join(yaml_dir, f"{safe}.yml")
    if not os.path.isfile(fpath):
        return jsonify({"error": "Not found"}), 404
    with open(fpath, "r", encoding="utf-8") as f:
        yaml_content = f.read()
    try:
        layout = _vis_yaml_to_layout(yaml_content)
        layout["name"] = safe
        return jsonify(layout)
    except Exception as e:
        return jsonify({"error": f"YAML-to-layout conversion failed: {e}"}), 500


@app.route("/proxy_visual/delete-layout/<name>", methods=["DELETE"])
def proxy_visual_delete_layout(name):
    """Delete a saved YAML workflow."""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401
    safe = "".join(c for c in name if c.isalnum() or c in "-_ ").strip()
    yaml_dir = os.path.join(root_dir, "data", "user_files", user_id, "oasis", "yaml")
    fpath = os.path.join(yaml_dir, f"{safe}.yaml")
    if not os.path.isfile(fpath):
        fpath = os.path.join(yaml_dir, f"{safe}.yml")
    if os.path.isfile(fpath):
        os.remove(fpath)
        return jsonify({"deleted": True})
    return jsonify({"error": "Not found"}), 404


@app.route("/proxy_visual/upload-yaml", methods=["POST"])
def proxy_visual_upload_yaml():
    """Upload a YAML file: save it and convert to layout data for canvas import."""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401
    data = request.get_json()
    if not data or not data.get("content"):
        return jsonify({"error": "No content"}), 400

    filename = data.get("filename", "upload.yaml")
    content = data["content"]

    # Validate YAML syntax
    try:
        _yaml.safe_load(content)
    except Exception as e:
        return jsonify({"error": f"Invalid YAML: {e}"}), 400

    # Save the file
    safe = "".join(c for c in os.path.splitext(filename)[0] if c.isalnum() or c in "-_ ").strip() or "upload"
    yaml_dir = os.path.join(root_dir, "data", "user_files", user_id, "oasis", "yaml")
    os.makedirs(yaml_dir, exist_ok=True)
    fpath = os.path.join(yaml_dir, f"{safe}.yaml")
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

    # Convert to layout data if converter available
    layout = None
    if _vis_yaml_to_layout:
        try:
            layout = _vis_yaml_to_layout(content)
            layout["name"] = safe
        except Exception:
            layout = None

    return jsonify({"saved": True, "name": safe, "layout": layout})


@app.route("/proxy_visual/sessions-status", methods=["GET"])
def proxy_visual_sessions_status():
    """Return all sessions with their running status for the canvas display."""
    user_id = session.get("user_id")
    password = session.get("password")
    if not user_id or not password:
        return jsonify([])
    try:
        r = requests.post(LOCAL_SESSIONS_URL, json={"user_id": user_id, "password": password}, timeout=10)
        if r.status_code != 200:
            return jsonify([])
        sessions_data = r.json()
        return jsonify(sessions_data if isinstance(sessions_data, list) else [])
    except Exception:
        return jsonify([])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT_FRONTEND", "51209")), debug=False, threaded=True)
