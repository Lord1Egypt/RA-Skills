#!/usr/bin/env python3
"""
ultra-memory HTTP REST Server
将 9 个记忆工具暴露为标准 HTTP 端点，供任意 LLM 平台通过 function calling 调用。

零外部依赖，纯 Python stdlib。

启动：
    python3 platform/server.py                  # 默认 localhost:3200
    python3 platform/server.py --port 8080
    python3 platform/server.py --host 0.0.0.0   # 局域网访问（谨慎使用）

端点一览：
    GET  /health                          服务健康检查
    GET  /tools                           列出所有工具
    POST /tools/{tool_name}               调用工具
    GET  /session/current                 获取当前活跃会话

支持的工具（POST /tools/xxx）：
    memory_init            初始化会话
    memory_status          查询会话状态与 context 压力
    memory_log             记录操作（自动提取实体）
    memory_recall          四层统一检索
    memory_summarize       触发摘要压缩（含元压缩）
    memory_restore         恢复上次会话
    memory_profile         读写用户画像
    memory_entities        查询实体索引
    memory_extract_entities 全量重提取实体

请求格式（JSON body）：
    {"project": "my-project", "resume": false}

响应格式：
    {"success": true, "output": "...", "tool": "memory_init"}
    {"success": false, "error": "...", "tool": "memory_init"}
"""

import os
import sys
import json
import subprocess
import argparse
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")

# ── 路径配置 ──────────────────────────────────────────────────────────────
PLATFORM_DIR = Path(__file__).parent
SCRIPTS_DIR  = PLATFORM_DIR.parent / "scripts"
PYTHON       = sys.executable
ULTRA_MEMORY_HOME = Path(os.environ.get("ULTRA_MEMORY_HOME", Path.home() / ".ultra-memory"))

VERSION = "3.0.0"

# Bearer Token（可选）：由 --token 参数或 ULTRA_MEMORY_TOKEN 环境变量设置
_BEARER_TOKEN: str = os.environ.get("ULTRA_MEMORY_TOKEN", "")

logging.basicConfig(
    level=logging.INFO,
    format="[ultra-memory] %(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("ultra-memory")


# ── 工具路由表 ────────────────────────────────────────────────────────────

_SUBPROCESS_ENV_ALLOWLIST = frozenset({
    # 进程执行必需
    "PATH", "PATHEXT", "SYSTEMROOT",
    # Python 运行时
    "PYTHONPATH", "PYTHONIOENCODING", "PYTHONUTF8",
    # 用户/家目录（脚本用 Path.home() 回落）
    "HOME", "USERPROFILE",
    # 编码/本地化
    "LANG", "LC_ALL", "LC_CTYPE", "LC_MESSAGES",
    # Windows 临时目录
    "TEMP", "TMP", "APPDATA", "LOCALAPPDATA",
})


def _build_child_env() -> dict[str, str]:
    """返回子进程所需的最小 env，不透传父进程的敏感变量（如 API Key、DB 连接串等）。"""
    child = {k: v for k, v in os.environ.items() if k in _SUBPROCESS_ENV_ALLOWLIST}
    child["ULTRA_MEMORY_HOME"] = str(ULTRA_MEMORY_HOME)
    return child


def _run_script(script: str, args: list[str], timeout: int = 20) -> tuple[bool, str]:
    """运行 Python 脚本，返回 (success, output)"""
    cmd = [PYTHON, str(SCRIPTS_DIR / script)] + args
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True,
            encoding="utf-8", errors="replace",
            env=_build_child_env(),
            timeout=timeout,
        )
        output = (result.stdout + result.stderr).strip()
        return result.returncode == 0, output
    except subprocess.TimeoutExpired:
        return False, f"脚本执行超时（>{timeout}s）"
    except Exception as e:
        return False, str(e)


def tool_memory_init(body: dict) -> tuple[bool, str]:
    args = ["--project", body.get("project", "default")]
    if body.get("resume"):
        args.append("--resume")
    return _run_script("init.py", args)


def tool_memory_status(body: dict) -> tuple[bool, str]:
    session_id = body.get("session_id", "")
    if not session_id:
        return False, "缺少 session_id 参数"

    meta_file = ULTRA_MEMORY_HOME / "sessions" / session_id / "meta.json"
    if not meta_file.exists():
        return False, f"会话不存在: {session_id}"

    with open(meta_file, encoding="utf-8") as f:
        meta = json.load(f)

    ok, pressure_out = _run_script("init.py", ["--check-pressure", session_id])
    lines = [
        f"会话 ID: {session_id}",
        f"项目: {meta.get('project', 'default')}",
        f"操作数: {meta.get('op_count', 0)}",
        f"最后里程碑: {meta.get('last_milestone', '（无）')}",
        f"上次压缩: {meta.get('last_summary_at', '（未压缩）')}",
        pressure_out,
    ]
    return True, "\n".join(lines)


def tool_memory_log(body: dict) -> tuple[bool, str]:
    session_id = body.get("session_id", "")
    op_type    = body.get("op_type", "")
    summary    = body.get("summary", "")
    if not all([session_id, op_type, summary]):
        return False, "缺少必填参数: session_id / op_type / summary"

    args = [
        "--session", session_id,
        "--type",    op_type,
        "--summary", summary,
        "--detail",  json.dumps(body.get("detail", {}), ensure_ascii=False),
        "--tags",    ",".join(body.get("tags", [])),
    ]
    return _run_script("log_op.py", args)


def tool_memory_recall(body: dict) -> tuple[bool, str]:
    session_id = body.get("session_id", "")
    query      = body.get("query", "")
    if not all([session_id, query]):
        return False, "缺少必填参数: session_id / query"

    args = [
        "--session", session_id,
        "--query",   query,
        "--top-k",   str(body.get("top_k", 5)),
    ]
    return _run_script("recall.py", args)


def tool_memory_summarize(body: dict) -> tuple[bool, str]:
    session_id = body.get("session_id", "")
    if not session_id:
        return False, "缺少 session_id 参数"

    args = ["--session", session_id]
    if body.get("force"):
        args.append("--force")
    return _run_script("summarize.py", args)


def tool_memory_restore(body: dict) -> tuple[bool, str]:
    args = ["--project", body.get("project", "default")]
    if body.get("verbose"):
        args.append("--verbose")
    return _run_script("restore.py", args)


def tool_memory_profile(body: dict) -> tuple[bool, str]:
    action       = body.get("action", "read")
    profile_file = ULTRA_MEMORY_HOME / "semantic" / "user_profile.json"

    if action == "read":
        try:
            content = profile_file.read_text(encoding="utf-8")
            return True, content
        except FileNotFoundError:
            return True, "{}"

    elif action == "update":
        profile = {}
        if profile_file.exists():
            try:
                profile = json.loads(profile_file.read_text(encoding="utf-8"))
            except Exception:
                pass
        profile.update(body.get("updates", {}))
        from datetime import date
        profile["last_updated"] = str(date.today())
        profile_file.parent.mkdir(parents=True, exist_ok=True)
        profile_file.write_text(
            json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return True, "用户画像已更新"

    return False, f"未知 action: {action}，支持 read / update"


def tool_memory_entities(body: dict) -> tuple[bool, str]:
    entities_file = ULTRA_MEMORY_HOME / "semantic" / "entities.jsonl"
    target_type   = body.get("entity_type", "all").lower()
    query         = body.get("query", "").lower()
    top_k         = int(body.get("top_k", 10))

    if not entities_file.exists():
        return True, "实体索引尚未建立，请先记录操作（memory_log）"

    all_entities = []
    for line in entities_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            all_entities.append(json.loads(line))
        except json.JSONDecodeError:
            continue

    # 类型过滤
    filtered = [e for e in all_entities
                if target_type == "all" or e.get("entity_type") == target_type]

    # 关键词过滤
    if query:
        filtered = [e for e in filtered
                    if query in e.get("name", "").lower()
                    or query in e.get("context", "").lower()]

    # 去重（同类型同名保留最新）
    seen: set[str] = set()
    deduped = []
    for e in reversed(filtered):  # 倒序 → 最新优先
        key = f"{e.get('entity_type')}:{e.get('name')}"
        if key not in seen:
            seen.add(key)
            deduped.append(e)
    deduped = deduped[:top_k]

    if not deduped:
        return True, "未找到匹配实体"

    lines = [f"找到 {len(deduped)} 个实体：\n"]
    for e in deduped:
        et   = e.get("entity_type", "?")
        name = e.get("name", "?")
        ctx  = e.get("context", "")
        extra = ""
        if et == "dependency" and e.get("manager"):
            extra = f" [via {e['manager']}]"
        elif et == "decision" and e.get("rationale"):
            extra = f"\n    依据: {e['rationale']}"
        elif et == "error" and e.get("message"):
            extra = f" ← {e['message']}"
        lines.append(f"[{et}] {name}{extra}")
        if ctx:
            lines.append(f"    来源: {ctx}")
    return True, "\n".join(lines)


def tool_memory_extract_entities(body: dict) -> tuple[bool, str]:
    session_id = body.get("session_id", "")
    if not session_id:
        return False, "缺少 session_id 参数"
    return _run_script("extract_entities.py", ["--session", session_id, "--all"])


def tool_memory_knowledge_add(body: dict) -> tuple[bool, str]:
    title = body.get("title", "")
    content = body.get("content", "")
    if not title or not content:
        return False, "缺少 title 或 content 参数"
    project = body.get("project", "default")
    tags = body.get("tags", [])
    args = ["--title", title, "--content", content, "--project", project]
    if tags:
        args.extend(["--tags", ",".join(tags)])
    return _run_script("log_knowledge.py", args)


# ── 工具注册表 ────────────────────────────────────────────────────────────

TOOL_HANDLERS = {
    "memory_init":             tool_memory_init,
    "memory_status":           tool_memory_status,
    "memory_log":              tool_memory_log,
    "memory_recall":           tool_memory_recall,
    "memory_summarize":        tool_memory_summarize,
    "memory_restore":          tool_memory_restore,
    "memory_profile":          tool_memory_profile,
    "memory_entities":         tool_memory_entities,
    "memory_extract_entities": tool_memory_extract_entities,
    "memory_knowledge_add":    tool_memory_knowledge_add,
}

TOOL_DESCRIPTIONS = {
    "memory_init":             "初始化会话，返回 session_id",
    "memory_status":           "查询会话状态与 context 压力级别",
    "memory_log":              "记录一条操作到日志（自动提取实体）",
    "memory_recall":           "四层统一检索：ops / summary / semantic / entity",
    "memory_summarize":        "触发摘要压缩（含分层元压缩）",
    "memory_restore":          "恢复上次会话，输出自然语言总结",
    "memory_profile":          "读写用户画像（技术栈、偏好）",
    "memory_entities":         "查询结构化实体索引（函数/文件/依赖/决策/错误）",
    "memory_extract_entities": "对整个 ops.jsonl 全量重提取实体",
    "memory_knowledge_add":    "追加知识库条目（bug解决方案、技术选型、工具技巧、可复用代码模式）",
}


# ── HTTP 请求处理 ─────────────────────────────────────────────────────────

class MemoryHandler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        log.info(f"{self.address_string()} {fmt % args}")

    def _check_auth(self) -> bool:
        """如果配置了 Bearer Token，验证请求头；否则放行。"""
        if not _BEARER_TOKEN:
            return True
        auth = self.headers.get("Authorization", "")
        if auth.startswith("Bearer ") and auth[7:] == _BEARER_TOKEN:
            return True
        self._send_json(401, {"error": "Unauthorized: 需要有效的 Bearer Token"})
        return False

    def _send_json(self, status: int, data: dict):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        # CORS：允许本地 web 客户端调用
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        raw = self.rfile.read(length)
        try:
            return json.loads(raw.decode("utf-8"))
        except Exception:
            return {}

    def do_OPTIONS(self):
        """CORS 预检"""
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if not self._check_auth():
            return
        parsed = urlparse(self.path)
        path   = parsed.path.rstrip("/")

        if path == "/health":
            self._send_json(200, {
                "status": "ok",
                "version": VERSION,
                "scripts_dir": str(SCRIPTS_DIR),
                "storage": str(ULTRA_MEMORY_HOME),
            })

        elif path == "/tools":
            self._send_json(200, {
                "tools": [
                    {"name": name, "description": desc,
                     "endpoint": f"POST /tools/{name}"}
                    for name, desc in TOOL_DESCRIPTIONS.items()
                ]
            })

        elif path == "/session/current":
            # 返回最近活跃会话（跨项目）
            sessions_dir = ULTRA_MEMORY_HOME / "sessions"
            if not sessions_dir.exists():
                self._send_json(200, {"session": None, "message": "尚无会话记录"})
                return
            latest = None
            latest_ts = ""
            for d in sessions_dir.iterdir():
                if not d.is_dir():
                    continue
                meta_f = d / "meta.json"
                if not meta_f.exists():
                    continue
                try:
                    m = json.loads(meta_f.read_text(encoding="utf-8"))
                    ts = m.get("last_op_at") or m.get("started_at", "")
                    if ts > latest_ts:
                        latest_ts = ts
                        latest = m
                except Exception:
                    continue
            self._send_json(200, {"session": latest})

        else:
            self._send_json(404, {"error": f"路径不存在: {path}"})

    def do_POST(self):
        if not self._check_auth():
            return
        parsed = urlparse(self.path)
        path   = parsed.path.rstrip("/")

        # POST /tools/{tool_name}
        if path.startswith("/tools/"):
            tool_name = path[len("/tools/"):]

            if tool_name not in TOOL_HANDLERS:
                self._send_json(404, {
                    "error": f"未知工具: {tool_name}",
                    "available": list(TOOL_HANDLERS.keys()),
                })
                return

            body    = self._read_body()
            handler = TOOL_HANDLERS[tool_name]

            try:
                success, output = handler(body)
                self._send_json(200 if success else 500, {
                    "success": success,
                    "tool":    tool_name,
                    "output":  output,
                })
            except Exception as e:
                log.exception(f"工具 {tool_name} 执行异常")
                self._send_json(500, {
                    "success": False,
                    "tool":    tool_name,
                    "error":   str(e),
                })
        else:
            self._send_json(404, {"error": f"路径不存在: {path}"})


# ── 主入口 ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="ultra-memory HTTP REST Server")
    parser.add_argument("--host", default="127.0.0.1",
                        help="监听地址（默认 127.0.0.1，仅本机访问）")
    parser.add_argument("--port", type=int, default=3200,
                        help="监听端口（默认 3200）")
    parser.add_argument("--storage", default=None,
                        help="覆盖 ULTRA_MEMORY_HOME 路径")
    parser.add_argument("--token", default=None,
                        help="Bearer Token 认证密钥（不设则无需认证）")
    args = parser.parse_args()

    global ULTRA_MEMORY_HOME, _BEARER_TOKEN
    if args.storage:
        ULTRA_MEMORY_HOME = Path(args.storage)
        os.environ["ULTRA_MEMORY_HOME"] = str(ULTRA_MEMORY_HOME)
    if args.token:
        _BEARER_TOKEN = args.token

    _local_hosts = {"127.0.0.1", "::1", "localhost"}
    if args.host not in _local_hosts:
        log.warning("⚠️  监听地址为 %s，服务将对外网络暴露，请确认这是预期行为。", args.host)
        if not _BEARER_TOKEN:
            log.warning(
                "⚠️  当前未设置 Bearer Token，任意客户端均可无需认证访问此服务！"
                " 请通过 --token 或环境变量 ULTRA_MEMORY_TOKEN 设置认证密钥。"
            )

    server = HTTPServer((args.host, args.port), MemoryHandler)

    log.info(f"ultra-memory REST Server v{VERSION} 已启动")
    log.info(f"地址: http://{args.host}:{args.port}")
    log.info(f"认证: {'已启用 Bearer Token' if _BEARER_TOKEN else '未启用（仅本机访问）'}")
    log.info(f"存储: {ULTRA_MEMORY_HOME}")
    log.info(f"脚本: {SCRIPTS_DIR}")
    log.info(f"工具: {list(TOOL_HANDLERS.keys())}")
    log.info("按 Ctrl+C 停止服务")
    log.info("")
    log.info("快速测试:")
    log.info(f"  curl http://{args.host}:{args.port}/health")
    log.info(f"  curl http://{args.host}:{args.port}/tools")
    log.info(f'  curl -X POST http://{args.host}:{args.port}/tools/memory_init \\')
    log.info(f'       -H "Content-Type: application/json" \\')
    log.info(f'       -d \'{{"project": "my-project"}}\'')

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log.info("服务已停止")


if __name__ == "__main__":
    main()
