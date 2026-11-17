"""优稿 API 客户端与命令行。仅使用 Python 标准库；预览不会启动任务。"""
from __future__ import annotations

import argparse
import base64
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import json
import os
from pathlib import Path
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

VERSION = "1.4.1"
DEFAULT_BASE = "https://yougao.top/api/v1"
KEY_URL = "https://yougao.top/app/api-keys"
MAX_RESPONSE = 20 * 1024 * 1024


def normalize_base(value: str) -> str:
    value = value.strip().rstrip("/")
    parsed = urllib.parse.urlsplit(value)
    if not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise APIError("站点地址不正确，请使用 https://yougao.top/api/v1。")
    if parsed.scheme != "https" and not (
        parsed.scheme == "http" and parsed.hostname in ("127.0.0.1", "localhost", "::1")
    ):
        raise APIError("请使用 HTTPS；本机开发仅允许回环地址使用 HTTP。")
    if parsed.path not in ("", "/api/v1"):
        raise APIError("站点地址只能包含 /api/v1，不要填文档或网页地址。")
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc.lower(), "/api/v1", "", ""))


def config_path() -> Path:
    override = os.environ.get("YOUGAO_CONFIG_FILE")
    if override:
        return Path(override).expanduser().resolve()
    return Path.home() / ".yougao" / "connection.json"


def _protect(data: bytes, decrypt: bool = False) -> bytes:
    """Windows DPAPI, bound to the current OS user; no third-party dependency."""
    import ctypes
    from ctypes import wintypes
    class Blob(ctypes.Structure):
        _fields_ = [("size", wintypes.DWORD), ("data", ctypes.POINTER(ctypes.c_ubyte))]
    buffer = ctypes.create_string_buffer(data)
    source = Blob(len(data), ctypes.cast(buffer, ctypes.POINTER(ctypes.c_ubyte)))
    target = Blob()
    library = ctypes.WinDLL("crypt32", use_last_error=True)
    function = library.CryptUnprotectData if decrypt else library.CryptProtectData
    function.argtypes = [ctypes.POINTER(Blob), ctypes.c_void_p, ctypes.c_void_p,
                         ctypes.c_void_p, ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(Blob)]
    function.restype = wintypes.BOOL
    if not function(ctypes.byref(source), None, None, None, None, 1, ctypes.byref(target)):
        raise APIError("无法读取或保护本机密钥，请在当前电脑重新连接优稿。")
    try:
        return ctypes.string_at(target.data, target.size)
    finally:
        free = ctypes.WinDLL("kernel32", use_last_error=True).LocalFree
        free.argtypes = [ctypes.c_void_p]
        free.restype = ctypes.c_void_p
        free(target.data)


def private_write(path: Path, value: dict):
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    temp = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
    try:
        fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as out:
            json.dump(value, out, ensure_ascii=False, indent=2)
            out.flush()
            os.fsync(out.fileno())
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)


def load_connection() -> dict:
    path = config_path()
    if not path.exists():
        return {}
    try:
        if os.name != "nt" and path.stat().st_mode & 0o077:
            raise APIError("本机密钥文件权限过宽，请由助手改为仅本人可读写（0600）。")
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("storage") == "windows-dpapi":
            if os.name != "nt":
                raise APIError("此连接属于另一台 Windows 电脑，请重新配置。")
            secret = _protect(base64.b64decode(data["secret"], validate=True), True).decode("utf-8")
        elif data.get("storage") == "user-file" and os.name != "nt":
            secret = data["secret"]
        else:
            raise ValueError()
        return {"base": normalize_base(data["base"]), "key": secret}
    except (ValueError, KeyError, TypeError, OSError):
        raise APIError("本机连接文件无法读取，请重新连接；不要把该文件粘贴到对话或日志。") from None


def save_connection(key: str, base: str = DEFAULT_BASE) -> dict:
    key = key.strip()
    if not key or len(key) > 4096 or any(c.isspace() for c in key):
        raise APIError("请输入完整的优稿 API Key，不要附加 Bearer 或说明文字。")
    normalized = normalize_base(base)
    storage = "windows-dpapi" if os.name == "nt" else "user-file"
    secret = base64.b64encode(_protect(key.encode())).decode() if os.name == "nt" else key
    private_write(config_path(), {"version": 1, "base": normalized, "storage": storage, "secret": secret})
    return {"configured": True, "base": normalized, "storage": storage,
            "message": "连接已保存，优稿技能共用。下一步检查连接；密钥不会显示。"}


def retry_seconds(value: str) -> int:
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        try:
            return max(0, int((parsedate_to_datetime(value) - datetime.now(timezone.utc)).total_seconds()) + 1)
        except (TypeError, ValueError, OverflowError):
            return 0


class APIError(Exception):
    def __init__(self, message: str, status: int = 0, retry_after: int = 0):
        super().__init__(message)
        self.status = status
        self.retry_after = retry_after


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class Client:
    def __init__(self, base: str | None = None, key: str | None = None):
        explicit_key = key or os.environ.get("YOUGAO_API_KEY", "")
        saved = {} if explicit_key else load_connection()
        self.base = normalize_base(base or os.environ.get("YOUGAO_API_BASE") or saved.get("base") or DEFAULT_BASE)
        if saved and saved["base"] != self.base:
            raise APIError("保存的密钥属于另一个站点，请明确为新站点配置连接。")
        self.key = explicit_key or saved.get("key", "")
        if not self.key:
            raise APIError("尚未连接优稿。请打开 " + KEY_URL + "，注册或登录后点击「复制给 AI」，将内容交给助手即可。")
        if len(self.key) > 4096 or any(c.isspace() for c in self.key):
            raise APIError("API Key 格式不正确，请从「我的 API Keys」重新复制。")
        self.opener = urllib.request.build_opener(NoRedirect())

    def request(self, method: str, path: str, payload=None, request_id: str | None = None):
        if not path.startswith("/") or path.startswith("//") or "://" in path:
            raise APIError("请使用以 / 开头的 API 相对路径。")
        headers = {"Authorization": "Bearer " + self.key, "Accept": "application/json",
                   "User-Agent": "Yougao-Skills/" + VERSION + " (+https://yougao.top/ai.md)"}
        data = None
        if payload is not None:
            data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json"
        if request_id:
            headers["Idempotency-Key"] = request_id
        request = urllib.request.Request(self.base + path, data=data, headers=headers, method=method)
        try:
            with self.opener.open(request, timeout=35) as response:
                raw = response.read(MAX_RESPONSE + 1)
                if len(raw) > MAX_RESPONSE:
                    raise APIError("响应超过客户端大小上限，请在优稿查看原任务。")
                try:
                    result = json.loads(raw.decode("utf-8"))
                    if not isinstance(result, (dict, list)):
                        raise ValueError()
                    return result
                except (ValueError, UnicodeError):
                    raise APIError("服务返回了无法识别的内容，请保留原任务记录后查询，不要重新创建付费任务。") from None
        except urllib.error.HTTPError as exc:
            gateway_blocked = False
            try:
                problem = json.loads(exc.read(65536).decode("utf-8"))
                message = problem.get("error", problem.get("title", "API 请求未完成"))
                gateway_blocked = "cloudflare" in str(problem.get("type", "")).lower()
            except (ValueError, UnicodeError, AttributeError):
                message = "API 请求未完成"
            retry = exc.headers.get("Retry-After", "0")
            hints = {401: "请在「我的 API Keys」检查密钥是否有效。", 402: "请检查账户点数及预留，充值后接续原任务。",
                     403: "请检查密钥权限及账户状态。", 429: "请求较频繁，请按 retryAfter 等待。"}
            if 300 <= exc.code < 400:
                message = "站点要求跳转，已停止发送凭据，请核对 API 地址。"
            if gateway_blocked:
                message = "站点入口拒绝了此连接，请使用最新技能包或稍后重试；这不是 Key 权限不足。"
            safe = str(message).replace(self.key, "[已隐藏]")[:500]
            raise APIError(safe + ("" if gateway_blocked else hints.get(exc.code, "")), exc.code, retry_seconds(retry)) from None
        except (urllib.error.URLError, TimeoutError, OSError):
            raise APIError("连接结果未知。请查询原运行，或沿用原提交编号；不要创建替代付费运行。") from None

    def call(self, feature: str, action: str, params: dict | None = None, request_id: str | None = None):
        """按功能调用，action 选择操作；原有调用方法继续兼容。"""
        if feature not in ("generation", "rewriting", "detection", "formatting", "workflow", "publishing"):
            raise APIError("请选择生成、改写、检测、排版、流程或发布功能。")
        payload = dict(params or {})
        if "action" in payload:
            raise APIError("请将 action 作为单独参数，不放入 params。")
        payload["action"] = action
        return self.request("POST", "/" + feature, payload, request_id)

    def plan(self, request: dict):
        payload = dict(request)
        tool = payload.pop("tool", "")
        if tool in ("generation", "rewriting", "detection", "formatting"):
            return self.call(tool, "preview", payload)
        if tool:
            # Compatibility for legacy single-step import/review callers.
            return self.request("POST", "/plans", request)
        return self.call("workflow", "preview", payload)

    def start(self, plan_id: str, request_id: str):
        if not request_id:
            raise APIError("请提供并保存本次操作的 request_id，重试时沿用。")
        return self.call("workflow", "start", {"planId": plan_id}, request_id)

    def run(self, run_id: str):
        return self.call("workflow", "get", {"runId": run_id})

    def publishing_plan(self, request: dict):
        return self.call("publishing", "preview", request)

    def publishing_start(self, plan_id: str, request_id: str):
        if not request_id:
            raise APIError("请提供并保存本次操作的 request_id，重试时沿用。")
        return self.call("publishing", "start", {"planId": plan_id}, request_id)

    def publishing_run(self, run_id: str):
        return self.call("publishing", "get", {"runId": run_id})

    def wait(self, run_id: str, timeout: int = 60, feature: str = "workflow"):
        deadline = time.monotonic() + timeout
        latest = {"id": run_id, "status": "waiting"}
        while True:
            try:
                latest = self.call(feature, "get", {"runId": run_id})
                if latest["status"] not in ("queued", "running"):
                    return latest
                delay = 3
            except APIError as exc:
                if exc.status != 429:
                    raise
                delay = max(3, exc.retry_after)
            if time.monotonic() + delay > deadline:
                return latest
            time.sleep(delay)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", action="version", version=VERSION)
    sub = parser.add_subparsers(dest="command", required=True)
    action_call = sub.add_parser("call", help="按功能调用，操作由 JSON 的 action 参数指定")
    action_call.add_argument("feature", choices=("generation", "rewriting", "detection", "formatting", "workflow", "publishing"))
    action_call.add_argument("--file", required=True, help="包含 action 的 UTF-8 JSON 文件")
    action_call.add_argument("--request-id", help="开始执行时保存并传入的幂等键")
    for name in ("tools", "workflows", "runs"):
        sub.add_parser(name)
    for name in ("platforms", "profiles", "manuscripts", "runs"):
        sub.add_parser("publish-" + name)
    publication_plan = sub.add_parser("publish-plan")
    publication_plan.add_argument("--file", required=True, help="UTF-8 JSON 发布计划文件")
    publication_start = sub.add_parser("publish-start")
    publication_start.add_argument("--plan-id", required=True)
    publication_start.add_argument("--request-id", required=True)
    for name in ("run", "manuscript", "bundle", "decision"):
        p = sub.add_parser("publish-" + name)
        p.add_argument("--id", required=True)
        if name == "decision":
            p.add_argument("--file", required=True, help="用户已确认的结果或取消决定，需当前 revision")
            p.add_argument("--request-id", required=True)
    plan = sub.add_parser("plan")
    plan.add_argument("--file", required=True, help="UTF-8 JSON 计划请求文件")
    start = sub.add_parser("start")
    start.add_argument("--plan-id", required=True)
    start.add_argument("--request-id", required=True, help="保存此编号，提交结果不明时使用它接续")
    for name in ("run", "wait", "approve", "cancel", "supply", "resume", "deliver", "download"):
        p = sub.add_parser(name)
        p.add_argument("--id", required=True, help="已有运行编号")
        if name == "wait":
            p.add_argument("--timeout", type=int, default=60)
        if name in ("approve", "cancel", "supply", "resume"):
            p.add_argument("--revision", type=int, required=True)
        if name in ("approve", "supply", "resume"):
            p.add_argument("--text-file", help="可选：经审阅的替换正文文件；supply 时必填")
        if name == "download":
            p.add_argument("--format", choices=("txt", "html", "json"), required=True)
            p.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    client = Client()
    if args.command == "call":
        payload = json.loads(Path(args.file).read_text(encoding="utf-8-sig"))
        action = payload.pop("action", "")
        result = client.call(args.feature, action, payload, args.request_id)
    elif args.command in ("publish-platforms", "publish-profiles", "publish-manuscripts", "publish-runs"):
        action = {"publish-platforms": "platforms", "publish-profiles": "accounts", "publish-manuscripts": "manuscripts", "publish-runs": "history"}[args.command]
        result = client.call("publishing", action)
    elif args.command == "publish-plan":
        result = client.publishing_plan(json.loads(Path(args.file).read_text(encoding="utf-8-sig")))
    elif args.command == "publish-start":
        result = client.publishing_start(args.plan_id, args.request_id)
    elif args.command == "publish-run":
        result = client.publishing_run(args.id)
    elif args.command == "publish-manuscript":
        result = client.call("publishing", "manuscripts", {"manuscriptId": args.id})
    elif args.command == "publish-bundle":
        result = client.request("GET", "/publishing/deliveries/" + urllib.parse.quote(args.id, safe="") + "/bundle")
    elif args.command == "publish-decision":
        result = client.request("POST", "/publishing/deliveries/" + urllib.parse.quote(args.id, safe="") + "/decisions", json.loads(Path(args.file).read_text(encoding="utf-8-sig")), args.request_id)
    elif args.command in ("tools", "workflows", "runs"):
        result = client.request("GET", "/tools") if args.command == "tools" else client.call("workflow", "list" if args.command == "workflows" else "history")
    elif args.command == "plan":
        result = client.plan(json.loads(Path(args.file).read_text(encoding="utf-8-sig")))
    elif args.command == "start":
        result = client.start(args.plan_id, args.request_id)
    elif args.command == "wait":
        if not 1 <= args.timeout <= 600:
            raise APIError("轮询时间应为 1–600 秒。")
        result = client.wait(args.id, args.timeout)
    elif args.command in ("approve", "cancel", "supply", "resume"):
        payload = {"action": args.command, "revision": args.revision}
        if args.command in ("approve", "supply", "resume") and args.text_file:
            payload["text"] = Path(args.text_file).read_text(encoding="utf-8-sig")
        action = payload.pop("action")
        payload["runId"] = args.id
        result = client.call("workflow", action, payload)
    elif args.command == "deliver":
        result = client.call("workflow", "deliver", {"runId": args.id})
    else:
        result = client.run(args.id)
        if args.command == "download":
            if args.format == "json":
                content = json.dumps(result, ensure_ascii=False, indent=2)
            else:
                content = result.get("state", {}).get("html" if args.format == "html" else "text", "")
            if not content:
                raise APIError("此运行尚未产出所需格式，请先查询实际状态。")
            target = Path(args.output).resolve()
            with target.open("x", encoding="utf-8") as out:
                out.write(content)
            result = {"id": args.id, "status": result["status"], "output": str(target)}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    try:
        main()
    except (APIError, ValueError, OSError) as exc:
        print(json.dumps({"error": str(exc), "status": getattr(exc, "status", 0), "retryAfter": getattr(exc, "retry_after", 0)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
