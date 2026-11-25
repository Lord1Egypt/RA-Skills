"""VoooAI OpenAPI 公共模块：共享函数、鉴权、路径白名单校验（Authorization: Bearer <access_key>）"""

import json
import os
import sys
import urllib.request
import urllib.error
import urllib.parse
from urllib.request import HTTPRedirectHandler, build_opener

# ── 环境变量配置 ──────────────────────────────────────────────────────────
BASE_URL = os.environ.get("VOOOAI_BASE_URL", "https://voooai.com")
ACCESS_KEY = os.environ.get("VOOOAI_ACCESS_KEY", "")

# 平台画布地址前缀（用于结果展示）
PLATFORM_URL = "https://voooai.com"


def _ensure_access_key() -> str:
    """
    确保 AccessKey 已设置，返回 AccessKey。
    如果未设置则输出错误并退出。
    """
    key = os.environ.get("VOOOAI_ACCESS_KEY", "")
    if not key:
        print("错误：请设置 VOOOAI_ACCESS_KEY 环境变量", file=sys.stderr)
        sys.exit(1)
    return key

# ── API 路径白名单 ──────────────────────────────────────────────────────────
# 三模式重构（2026-11）：新增图片/视频任务系统（/api/create-task、/api/tasks）
# 与编导模式（/api/director/）前缀；保留 nl2workflow / node-builder / cos 旧前缀。
ALLOWED_PATH_PREFIXES = (
    "/api/agent/",
    "/api/node-builder/",
    "/api/upload",
    "/api/cos/",
    "/api/create-task",
    "/api/tasks",
    "/api/director/",
)


def validate_api_path(path: str) -> None:
    """
    校验 API 路径是否在白名单内。
    如果路径不在允许范围内，输出错误并退出。
    
    Args:
        path: API 路径（如 /api/agent/capabilities）
    """
    if not any(path.startswith(prefix) for prefix in ALLOWED_PATH_PREFIXES):
        print(f"错误：不允许的 API 路径: {path}", file=sys.stderr)
        print(f"允许的路径前缀: {', '.join(ALLOWED_PATH_PREFIXES)}", file=sys.stderr)
        sys.exit(1)


def _headers(content_type: str = "application/json") -> dict:
    """
    构建请求头（Bearer Token 认证）
    
    Args:
        content_type: Content-Type 头，默认 application/json
    
    Returns:
        请求头字典
    """
    access_key = _ensure_access_key()
    headers = {
        "Authorization": f"Bearer {access_key}",
    }
    if content_type:
        headers["Content-Type"] = content_type
    return headers


def api_get(path: str, timeout: int = 30) -> dict:
    """
    GET 请求 VoooAI OpenAPI
    
    Args:
        path: API 路径（如 /api/agent/capabilities）
        timeout: 请求超时秒数
    
    Returns:
        JSON 响应字典
    """
    validate_api_path(path)
    url = _build_url(path)
    req = urllib.request.Request(url, method="GET", headers=_headers())
    try:
        with _open(req, timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8") if e.fp else ""
        print(f"API 错误 {e.code}: {err_body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"网络错误: {e.reason}", file=sys.stderr)
        sys.exit(1)


def api_post(path: str, body: dict, timeout: int = 60) -> dict:
    """
    POST 请求 VoooAI OpenAPI（JSON body）
    
    Args:
        path: API 路径（如 /api/agent/nl2workflow/analyze）
        body: 请求体字典
        timeout: 请求超时秒数
    
    Returns:
        JSON 响应字典
    """
    validate_api_path(path)
    url = _build_url(path)
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers=_headers(),
    )
    try:
        with _open(req, timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8") if e.fp else ""
        print(f"API 错误 {e.code}: {err_body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"网络错误: {e.reason}", file=sys.stderr)
        sys.exit(1)


def json_output(data: dict) -> None:
    """
    统一 JSON 输出格式
    
    Args:
        data: 要输出的字典
    """
    print(json.dumps(data, ensure_ascii=False, indent=2))


def error_exit(message: str, code: int = 1) -> None:
    """
    错误退出（输出到 stderr）
    
    Args:
        message: 错误消息
        code: 退出码
    """
    print(f"错误：{message}", file=sys.stderr)
    sys.exit(code)


# ── 传输安全加固（2026-11-25，回应 ClawHub SkillSpector 凭据外泄发现）────────
# 仅允许 HTTPS 远端 / 回环 HTTP；禁止 URL 携带凭据；拦截跨域重定向，
# 避免 Authorization 被 urllib 默认重定向转发到非预期 origin。
_LOOPBACK_HOSTS = {"localhost", "127.0.0.1", "::1"}


def _validate_base_url(base: str):
    """校验 VOOOAI_BASE_URL：scheme/主机/凭据边界。返回 urlsplit 结果。"""
    parsed = urllib.parse.urlsplit(base)
    host = (parsed.hostname or "").lower()
    if parsed.scheme not in ("http", "https") or not host:
        error_exit(f"VOOOAI_BASE_URL 无效（须为 http/https 且含主机）: {base}")
    if parsed.username or parsed.password:
        error_exit("VOOOAI_BASE_URL 不允许携带用户名/密码")
    if parsed.scheme == "http" and host not in _LOOPBACK_HOSTS:
        error_exit("VOOOAI_BASE_URL 非回环地址必须使用 HTTPS（防止凭据明文外泄）")
    return parsed


_BASE_PARSED = _validate_base_url(BASE_URL)


class _SameOriginRedirectOnly(HTTPRedirectHandler):
    """仅放行同 origin 重定向；跨域重定向直接拒绝，防止 Bearer 凭据被转发。"""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        old = urllib.parse.urlsplit(req.full_url)
        new = urllib.parse.urlsplit(newurl)
        if (old.scheme, old.netloc) != (new.scheme, new.netloc):
            raise urllib.error.URLError(f"已拦截跨域重定向（保护 AccessKey）: {new.netloc}")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


_OPENER = build_opener(_SameOriginRedirectOnly())


def _build_url(path: str) -> str:
    """白名单 + origin 一致性双重校验后拼接请求 URL。"""
    validate_api_path(path)
    url = f"{BASE_URL.rstrip('/')}{path}"
    p = urllib.parse.urlsplit(url)
    if (p.scheme, p.netloc) != (_BASE_PARSED.scheme, _BASE_PARSED.netloc):
        error_exit(f"请求目标 origin 与 VOOOAI_BASE_URL 不一致: {url}")
    return url


def _open(req, timeout: int):
    """经安全 opener 发起请求（跨域重定向被拦截）。"""
    return _OPENER.open(req, timeout=timeout)


def load_json_arg(arg: str) -> dict:
    """
    加载 JSON 参数（支持 JSON 字符串或文件路径）
    
    Args:
        arg: JSON 字符串或文件路径
    
    Returns:
        解析后的字典
    """
    # 尝试作为文件路径加载
    if os.path.isfile(arg):
        try:
            with open(arg, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            error_exit(f"无法读取文件 {arg}: {e}")
    
    # 尝试作为 JSON 字符串解析
    try:
        return json.loads(arg)
    except json.JSONDecodeError as e:
        error_exit(f"无效的 JSON: {e}")
    
    return {}  # 不会执行到这里，但为了类型检查


def parse_set_params(params: list) -> dict:
    """
    解析 --set-param 参数列表（格式：node_id.param_name=value）
    
    Args:
        params: --set-param 参数列表，如 ["node_1.prompt=hello", "node_2.duration=10"]
    
    Returns:
        解析后的参数字典，如 {"node_1": {"prompt": "hello"}, "node_2": {"duration": "10"}}
    """
    result = {}
    for param in params:
        if "=" not in param:
            print(f"警告：忽略无效参数格式 '{param}'（应为 key=value）", file=sys.stderr)
            continue
        key, value = param.split("=", 1)
        
        if "." in key:
            node_id, param_name = key.split(".", 1)
        else:
            # 如果没有 node_id 前缀，使用通用键
            node_id = "_global_"
            param_name = key
        
        if node_id not in result:
            result[node_id] = {}
        
        # 尝试解析为数字或布尔值
        try:
            if value.lower() == "true":
                value = True
            elif value.lower() == "false":
                value = False
            elif "." in value:
                value = float(value)
            else:
                value = int(value)
        except ValueError:
            pass  # 保持为字符串
        
        result[node_id][param_name] = value
    
    return result


def apply_params_to_workflow(workflow: dict, params: dict) -> dict:
    """
    将参数应用到工作流的节点中
    
    Args:
        workflow: 工作流数据（包含 nodes 列表）
        params: 参数字典（由 parse_set_params 返回）
    
    Returns:
        更新后的工作流数据
    """
    if not params or "nodes" not in workflow:
        return workflow
    
    for node in workflow.get("nodes", []):
        node_id = node.get("id", "")
        
        # 应用全局参数
        if "_global_" in params:
            if "widget_values" not in node:
                node["widget_values"] = {}
            node["widget_values"].update(params["_global_"])
        
        # 应用节点特定参数
        if node_id in params:
            if "widget_values" not in node:
                node["widget_values"] = {}
            node["widget_values"].update(params[node_id])
    
    return workflow


# ── 非退出式 HTTP 请求（供图片/视频/编导脚本优雅处理业务错误）──────────────
def _safe_json(raw: str):
    """尽力解析 JSON 字符串，失败返回 None。"""
    if not raw:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def http_request(method: str, path: str, body: dict = None, timeout: int = 60):
    """
    发起 HTTP 请求但**不在错误时 sys.exit**，返回 (status_code, data)。

    - 成功：(2xx, 解析后的 JSON dict)
    - HTTP 错误（4xx/5xx）：(状态码, 解析后的错误 JSON 或 {'success': False, 'error': ...})
    - 网络错误：(0, {'success': False, 'error': '网络错误: ...'})

    与 api_get/api_post 的区别：后者遇错即退出，本函数把错误交回调用方判断，
    便于新脚本处理 INSUFFICIENT_POINTS / MEMBERSHIP_REQUIRED / 并发限制等业务错误。

    Args:
        method: HTTP 方法（GET/POST/PATCH/DELETE）
        path: API 路径（须在白名单内）
        body: 请求体字典（GET 可为 None）
        timeout: 超时秒数

    Returns:
        (status_code:int, data:dict)
    """
    validate_api_path(path)
    url = _build_url(path)
    headers = _headers()
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method.upper(), headers=headers)
    try:
        with _open(req, timeout) as resp:
            return resp.status, _safe_json(resp.read().decode("utf-8")) or {}
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8") if e.fp else ""
        return e.code, (_safe_json(err_body) or {"success": False, "error": err_body})
    except urllib.error.URLError as e:
        return 0, {"success": False, "error": f"网络错误: {e.reason}"}
    except Exception as e:
        return 0, {"success": False, "error": f"请求异常: {e}"}


def format_business_error(status_code: int, data: dict, locale: str = None) -> str:
    """把后端业务错误转成用户友好提示（含充值/升级引导）。

    语言可选：locale 参数或 VOOOAI_LOCALE 环境变量（'zh' 默认 / 'en'），
    回应 SkillSpector「错误文案硬编码中文、无语言选择」发现。
    """
    loc = (locale or os.environ.get("VOOOAI_LOCALE") or "zh").lower()
    en = loc.startswith("en")
    if not isinstance(data, dict):
        return f"HTTP {status_code}: unknown error" if en else f"HTTP {status_code}: 未知错误"
    error_code = data.get("error_code", "")
    message = data.get("message") or data.get("error") or ""
    details = data.get("details", {}) or {}

    # 免费用户（VIP0）不允许通过 AccessKey 调用 API
    if status_code == 403 and error_code == "MEMBERSHIP_REQUIRED":
        if en:
            return ("AccessKey requires a paid membership (free VIP0 is rejected). "
                    "Upgrade at https://voooai.com/subscription and retry.")
        return ("AccessKey 需付费会员才能调用 API（免费 VIP0 被拒绝）。"
                "请到 https://voooai.com/subscription 升级后重试。")
    # 积分不足（create-task 返回 400 + details.shortage；或显式 error_code）
    if error_code == "INSUFFICIENT_POINTS" or (status_code == 400 and "shortage" in details):
        parts = ["Insufficient points."] if en else ["积分不足。"]
        if details.get("required") is not None:
            parts.append(f"required {details['required']}" if en else f"需要 {details['required']} 点")
        avail = details.get("total_available", details.get("available"))
        if avail is not None:
            parts.append(f"available {avail}" if en else f"可用 {avail} 点")
        if details.get("shortage") is not None:
            parts.append(f"shortage {details['shortage']}" if en else f"缺口 {details['shortage']} 点")
        parts.append("Top up at https://voooai.com/subscription and retry." if en
                     else "请到 https://voooai.com/subscription 充值后重试。")
        return " ".join(parts)
    if status_code == 429:
        return (f"Rate/concurrency limit: {message or 'please retry later'}" if en
                else f"并发/频率限制：{message or '请稍后重试'}")
    if status_code == 401:
        return ("Authentication failed: check VOOOAI_ACCESS_KEY (must start with vooai_)." if en
                else "鉴权失败：请检查 VOOOAI_ACCESS_KEY 是否有效（须以 vooai_ 开头）。")
    return f"HTTP {status_code}: {message or ('request failed' if en else '请求失败')}"


# ── 任务轮询（图片/视频生成走 /api/tasks 任务系统）──────────────────────────
DEFAULT_TASK_POLL_INTERVAL = 5   # 秒
DEFAULT_TASK_TIMEOUT = 300       # 5 分钟


def extract_task_media(task: dict) -> list:
    """
    从 /api/tasks/<id> 的 task 对象提取媒体 URL 列表。

    任务结果按媒体类型分字段（image_url/video_url/audio_url），
    与 node-builder 的 outputs 结构不同，需独立提取。

    Returns:
        [{'type': 'image|video|audio', 'url': str}, ...]
    """
    media = []
    if not isinstance(task, dict):
        return media
    for key, mtype in (("image_url", "image"), ("video_url", "video"), ("audio_url", "audio")):
        url = task.get(key)
        if url:
            media.append({"type": mtype, "url": url})
    return media


def poll_task(task_id: str, timeout: int = DEFAULT_TASK_TIMEOUT,
              interval: int = DEFAULT_TASK_POLL_INTERVAL, verbose: bool = True):
    """
    轮询 GET /api/tasks/<task_id> 直到 completed/failed/cancelled 或超时。

    网络/瞬时错误不中断轮询（与 http_request 非退出语义一致）。

    Args:
        task_id: 任务 ID（由 /api/create-task 返回）
        timeout: 超时秒数（默认 300）
        interval: 轮询间隔秒数（默认 5）
        verbose: 是否向 stderr 打印进度

    Returns:
        (final_status:str, task:dict)
        final_status ∈ {'completed','failed','cancelled','timeout','unknown'}
    """
    import time
    start = time.time()
    last_status = None
    task = {}
    while True:
        elapsed = time.time() - start
        if elapsed > timeout:
            return "timeout", task
        status_code, data = http_request("GET", f"/api/tasks/{task_id}")
        if status_code == 200 and isinstance(data, dict) and data.get("success"):
            task = data.get("task", {}) or {}
            status = task.get("status", "unknown")
            if status != last_status:
                if verbose:
                    print(f"[{int(elapsed)}s] 任务状态: {status}", file=sys.stderr)
                last_status = status
            if status in ("completed", "failed", "cancelled", "canceled"):
                return ("cancelled" if status == "canceled" else status), task
        elif verbose:
            print(f"[{int(elapsed)}s] 查询暂无结果（HTTP {status_code}），继续轮询...", file=sys.stderr)
        time.sleep(interval)


# ── SSE 流读取（编导模式 start/chat 返回 text/event-stream）────────────────
DEFAULT_SSE_STALL_TIMEOUT = 120   # 单次 socket 读超时（后端每 ~10-30s 发心跳）
DEFAULT_SSE_MAX_TIMEOUT = 300     # 整体最大时长


def _dispatch_sse(result: dict, event_type: str, data_str: str, verbose: bool = False) -> None:
    """把单个 SSE 事件归集到 result。事件契约见 framework/stream_builder.py。"""
    payload = _safe_json(data_str)
    if payload is None:
        payload = {}
    if event_type == "session_start":
        result["session_id"] = payload.get("session_id", result["session_id"])
        result["tab_id"] = payload.get("tab_id", result["tab_id"])
    elif event_type == "token":
        content = payload.get("content", "")
        result["reply"] += content
        if verbose and content:
            print(content, end="", file=sys.stderr, flush=True)
    elif event_type == "action":
        result["actions"].append(payload)
    elif event_type == "summary":
        result["summaries"].append(payload)
    elif event_type == "resource":
        result["resources"].append(payload)
    elif event_type == "archive_bound":
        if payload.get("archive_id"):
            result["archive_id"] = payload.get("archive_id")
    elif event_type == "done":
        result["done"] = payload
        if payload.get("points_charged") is not None:
            result["points_charged"] = payload.get("points_charged")
        if payload.get("session_points_total") is not None:
            result["session_points_total"] = payload.get("session_points_total")
        if payload.get("archive_id"):
            result["archive_id"] = payload.get("archive_id")
    elif event_type == "error":
        result["error"] = {
            "code": payload.get("code", ""),
            "message": payload.get("message", ""),
            "retryable": payload.get("retryable"),
            "trace_id": payload.get("trace_id"),
        }
    elif event_type == "required_config":
        # 全局必填配置确认：首次创建剧本时后端拦截 task 执行，下发选项弹窗。
        # ★ 2026-11-16 真实联调修复：此前落入「未知事件静默跳过」，Agent 只看到
        #   空 reply + stage 不推进，无从知道要补哪些配置（实测 chat 已扣积分却无产出）。
        #   questions[].question 与 quick_options[].label 是后端按 locale 本地化后的文案，
        #   quick_options[].value 才是回传值；question_id 为 config 的键。
        result["required_config"] = {
            "questions": payload.get("questions", []),
            "original_message": payload.get("original_message", ""),
        }
    # ping / tool_calls_begin / retry / 未知事件 → 静默跳过


def api_post_stream(path: str, body: dict = None,
                    stall_timeout: int = DEFAULT_SSE_STALL_TIMEOUT,
                    max_timeout: int = DEFAULT_SSE_MAX_TIMEOUT,
                    verbose: bool = False) -> dict:
    """
    POST 一个 SSE 端点（如 /api/director/v2/start、/chat），把事件流聚合为一次性 dict。

    SSE wire 格式：`event: <type>\ndata: <json>\n\n`（空行分隔，`:` 开头为心跳注释）。

    非 200 响应（401/402/400/404 等按 JSON 错误返回）会被捕获并填入 error/http_status，
    不 sys.exit（与 http_request 非退出语义一致）。

    Returns:
        {
          'ok': bool,            # 收到 done 且无 error
          'http_status': int,
          'session_id': str, 'tab_id': str,
          'reply': str,          # 聚合的 token 文本
          'actions': [...], 'summaries': [...], 'resources': [...],
          'done': dict|None, 'error': dict|None,
          'points_charged': n|None, 'session_points_total': n|None,
          'archive_id': str|None, 'timed_out': bool,
        }
    """
    validate_api_path(path)
    url = _build_url(path)
    headers = _headers()
    headers["Accept"] = "text/event-stream"
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method="POST", headers=headers)

    result = {
        "ok": False, "http_status": 0, "session_id": "", "tab_id": "",
        "reply": "", "actions": [], "summaries": [], "resources": [],
        "done": None, "error": None, "points_charged": None,
        "session_points_total": None, "archive_id": None, "timed_out": False,
        "required_config": None,
    }

    try:
        resp = _open(req, stall_timeout)
    except urllib.error.HTTPError as e:
        result["http_status"] = e.code
        err_body = e.read().decode("utf-8") if e.fp else ""
        parsed = _safe_json(err_body) or {}
        result["error"] = {
            "code": parsed.get("error_code") or parsed.get("error") or str(e.code),
            "message": parsed.get("message") or parsed.get("error") or err_body or str(e),
        }
        # 积分不足统一 402；会员门槛 403
        return result
    except urllib.error.URLError as e:
        result["error"] = {"code": "NETWORK", "message": f"网络错误: {e.reason}"}
        return result
    except Exception as e:
        result["error"] = {"code": "REQUEST_FAILED", "message": str(e)}
        return result

    result["http_status"] = getattr(resp, "status", 200)

    import time
    start = time.time()
    event_type = None
    data_lines = []
    try:
        while True:
            if time.time() - start > max_timeout:
                result["timed_out"] = True
                break
            raw = resp.readline()
            if not raw:
                break  # EOF
            line = raw.decode("utf-8", errors="replace").rstrip("\r\n")
            if line.startswith(":"):
                continue  # 心跳注释
            if line == "":
                if event_type and data_lines:
                    _dispatch_sse(result, event_type, "\n".join(data_lines), verbose)
                event_type = None
                data_lines = []
                # done/error 后流通常即结束；不主动 break，依赖 EOF/超时兵底
                continue
            if line.startswith("event:"):
                event_type = line[len("event:"):].strip()
            elif line.startswith("data:"):
                data_lines.append(line[len("data:"):].strip())
        # 处理末尾无空行的残留事件
        if event_type and data_lines:
            _dispatch_sse(result, event_type, "\n".join(data_lines), verbose)
    except Exception as e:
        if result["done"] is None and result["error"] is None:
            result["error"] = {"code": "STREAM_INTERRUPTED", "message": str(e)}
    finally:
        try:
            resp.close()
        except Exception:
            pass

    result["ok"] = (result["done"] is not None) and (result["error"] is None)
    return result


# ── 编导会话本地状态（agent 无状态 vs 编导有状态的桥）───────────────
DEFAULT_SESSION_STATE_FILE = ".voooai_director_session.json"


def save_session_state(session_id: str, tab_id: str = "", state_file: str = None, extra: dict = None) -> str:
    """将编导会话 session_id/tab_id 写入本地状态文件，返回路径。"""
    path = state_file or DEFAULT_SESSION_STATE_FILE
    data = {"session_id": session_id, "tab_id": tab_id or ""}
    if extra:
        data.update(extra)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except IOError as e:
        print(f"警告：无法写入会话状态文件 {path}: {e}", file=sys.stderr)
    return path


def load_session_state(state_file: str = None) -> dict:
    """读本地会话状态文件；不存在或损坏时返回 {}。"""
    path = state_file or DEFAULT_SESSION_STATE_FILE
    if not os.path.isfile(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f) or {}
    except (json.JSONDecodeError, IOError):
        return {}


def resolve_session(explicit_session_id: str = None, explicit_tab_id: str = None,
                    state_file: str = None):
    """优先用显式 session_id/tab_id，否则从状态文件读。返回 (session_id, tab_id)。"""
    st = load_session_state(state_file)
    session_id = explicit_session_id or st.get("session_id", "")
    tab_id = explicit_tab_id if explicit_tab_id is not None else st.get("tab_id", "")
    return session_id, tab_id


# ── ReactFlow 工作流 → node-builder 执行格式归一化 ────────────────────
def _normalize_rf_node(n: dict) -> dict:
    """将 ReactFlow 节点 {id, type:'custom', data:{nodeType, widgetValues}} 转为
    node-builder 执行格式 {instance_id, node_class, widget_values}（镜像前端转换）。
    已是执行格式（含 node_class/instance_id）则原样返回。"""
    if not isinstance(n, dict):
        return n
    if n.get("node_class") or n.get("instance_id"):
        return n  # 已归一化，幂等
    data = n.get("data") or {}
    # node_class 取自 data.nodeType（ReactFlow 顶层 type='custom' 无用）
    node_class = data.get("nodeType") or data.get("node_class") or n.get("nodeType")
    if not node_class or node_class == "custom":
        node_class = n.get("type") if n.get("type") not in (None, "custom") else node_class
    out = {
        "instance_id": n.get("id") or n.get("instance_id"),
        "node_class": node_class,
        "widget_values": data.get("widgetValues") or data.get("widget_values") or n.get("widget_values") or {},
        "enabled": n.get("enabled", True),
        "position": n.get("position") or {"x": 0, "y": 0},
    }
    for k in ("storyboard_id", "node_role"):
        v = data.get(k, n.get(k))
        if v is not None:
            out[k] = v
    return out


def _normalize_rf_edges(edges: list) -> list:
    """ReactFlow edges {source,target,sourceHandle,targetHandle} → connections
    {source_node_id,target_node_id,source_port,target_port}（镜像前端转换）。"""
    conns = []
    for e in edges or []:
        if not isinstance(e, dict):
            continue
        src = e.get("source_node_id") or e.get("source")
        tgt = e.get("target_node_id") or e.get("target")
        if not src or not tgt:
            continue
        conns.append({
            "source_node_id": src,
            "target_node_id": tgt,
            "source_port": e.get("source_port") or e.get("sourceHandle") or "output",
            "target_port": e.get("target_port") or e.get("targetHandle") or "input",
        })
    return conns


def reactflow_to_workflow(workflow: dict, director_session_id: str = None) -> dict:
    """
    把编导 export-workflow 的 ReactFlow {nodes, edges} 归一化为
    /api/node-builder/execute 期望的 {nodes, connections} 执行格式。

    幂等：若已是执行格式（含 connections 且节点含 node_class），基本原样返回。
    保留原 workflow 的其他键（viewport/metadata 等）。

    Args:
        workflow: export-workflow 返回的 workflow 字典
        director_session_id: 可选，注入 director_session_id（后端执行期据此回补 prompt）

    Returns:
        归一化后的新 workflow 字典
    """
    if not isinstance(workflow, dict):
        return workflow
    out = dict(workflow)
    nodes = out.get("nodes") or []
    out["nodes"] = [_normalize_rf_node(n) for n in nodes]
    # connections 优先；缺失则从 edges 转换
    if out.get("connections"):
        out["connections"] = _normalize_rf_edges(out["connections"])
    else:
        out["connections"] = _normalize_rf_edges(out.get("edges") or [])
    if director_session_id:
        out["director_session_id"] = director_session_id
    return out
