#!/usr/bin/env python3
"""
lexiang_api.py - 乐享目录、探活和独立附件客户端

默认机制：复用 WorkBuddy / QClaw 等 Agent 内置乐享连接器的 OAuth 凭证，
以 X-Oneid-Access-Token 调用乐享 MCP。显式选择 uploader 个人凭证时，
改用带 company_from 的 MCP URL 与 Authorization: Bearer 鉴权。

降级机制：当 token 文件不可用（过期/不存在）时，自动检测 Agent 本地 MCP
代理，通过代理调用乐享工具（无需 token）。代理模式从进程列表自动提取
认证头，兼容 WorkBuddy / QClaw / CodeBuddy。

本模块禁止实现 Markdown page 创建、覆盖或正文图片上传；这些能力统一由
upload-markdown-to-lexiang 提供。

token 文件发现：
  ~/.workbuddy/connectors/<profile>/tokens/lexiang-ol.txt   (WorkBuddy)
  环境变量 LEXIANG_ONEID_TOKEN 可显式覆盖

仅依赖 Python 标准库。
"""

import glob
import json
import os
import re
import time
import urllib.parse
import urllib.request
import urllib.error
import uuid
from dataclasses import dataclass
from pathlib import Path

MCP_URL = "https://mcp.lexiang-app.com/mcp"
DEFAULT_PERSONAL_CREDENTIALS = Path(
    "~/.config/lexiang-upload/credentials.json"
).expanduser()
PERSONAL_PROFILE_DIR = Path(
    "~/.config/lexiang-upload/profiles"
).expanduser()
PROFILE_RE = re.compile(r"^[A-Za-z0-9._-]+$")

# token 文件搜索路径（按优先级），支持 WorkBuddy 多 profile
TOKEN_GLOBS = [
    "~/.workbuddy/connectors/*/tokens/lexiang-ol.txt",
    "~/.qclaw/connectors/*/tokens/lexiang-ol.txt",
    "~/.codebuddy/connectors/*/tokens/lexiang-ol.txt",
]

# ── 重试配置（应对 WAF 403 / 限流 429 / 5xx / 瞬时网络错误）──
# WAF 拦截、限流、网关错误多为瞬时，指数退避重试可救回大部分。
RETRY_MAX = 3                      # 最多重试次数（不含首次）
RETRY_BACKOFF = [2, 5, 10]         # 各次重试前的等待秒数
RETRY_HTTP_CODES = {403, 408, 429, 500, 502, 503, 504}  # 可重试的 HTTP 状态码


class LexiangError(Exception):
    """乐享调用错误。retryable 标记该错误是否属于可重试类型（重试耗尽后仍失败）。"""
    def __init__(self, message, retryable=False, code=None):
        super().__init__(message)
        self.retryable = retryable
        self.code = code


@dataclass(frozen=True)
class PersonalCredentialSelector:
    """已解析的个人凭证位置；不包含 token。"""

    profile: str
    path: Path


def _validate_profile(profile):
    value = str(profile).strip()
    if not value or not PROFILE_RE.fullmatch(value):
        raise LexiangError(
            "乐享 profile 名称只能包含 A-Z、a-z、0-9、点、下划线和连字符，且不能为空"
        )
    return value


def resolve_personal_credential_selector(
        profile=None, credential_file=None, environ=None):
    """
    解析 sync 的个人凭证选择器。

    优先级：显式 file > 显式 profile > 环境 file > 环境 profile。
    与公共 uploader 不同，无任何选择时返回 None，以保留原连接器默认逻辑。
    """
    env = os.environ if environ is None else environ
    explicit_file = str(credential_file or "").strip()
    explicit_profile = None if profile is None else str(profile).strip()
    if explicit_file and explicit_profile:
        raise LexiangError(
            "lexiang_profile 与 lexiang_credential_file 不能同时设置"
        )
    if explicit_file:
        return PersonalCredentialSelector(
            "", Path(explicit_file).expanduser()
        )
    if profile is not None:
        selected = _validate_profile(profile)
    else:
        env_file = str(env.get("LEXIANG_UPLOAD_CREDENTIALS", "")).strip()
        if env_file:
            return PersonalCredentialSelector("", Path(env_file).expanduser())
        env_profile = str(env.get("LEXIANG_UPLOAD_PROFILE", "")).strip()
        if not env_profile:
            return None
        selected = _validate_profile(env_profile)
    path = (
        DEFAULT_PERSONAL_CREDENTIALS
        if selected == "default"
        else PERSONAL_PROFILE_DIR / f"{selected}.json"
    )
    return PersonalCredentialSelector(selected, path)


def load_personal_credential(path):
    """读取 uploader 兼容的 JSON 个人凭证，返回无额外字段的安全字典。"""
    credential_path = Path(path).expanduser()
    if not credential_path.is_file():
        raise LexiangError(f"乐享个人凭证文件不存在: {credential_path}")
    try:
        data = json.loads(credential_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise LexiangError(f"乐享个人凭证文件无法读取: {credential_path}") from error
    if not isinstance(data, dict):
        raise LexiangError(f"乐享个人凭证格式无效: {credential_path}")
    candidates = [data]
    candidates.extend(
        value
        for key in ("mcp", "credential", "credentials", "auth")
        if isinstance((value := data.get(key)), dict)
    )

    def pick(*keys):
        for candidate in candidates:
            for key in keys:
                if candidate.get(key):
                    return str(candidate[key]).strip()
        return ""

    token = pick("mcp_token", "access_token", "token", "LEXIANG_TOKEN")
    company_from = pick("company_from", "mcp_company_from")
    missing = [
        name for name, value in (
            ("mcp_token", token), ("company_from", company_from)
        ) if not value
    ]
    if missing:
        raise LexiangError(
            f"乐享个人凭证缺少字段 {', '.join(missing)}: {credential_path}"
        )
    if not token.startswith("lxmcp_"):
        raise LexiangError(
            f"乐享个人凭证 mcp_token 格式无效: {credential_path}"
        )
    return {"mcp_token": token, "company_from": company_from}


def _log(msg):
    """诊断日志走 stderr（不污染 stdout 的 JSON 摘要）"""
    import sys
    print(msg, file=sys.stderr, flush=True)


def _decode_jwt_exp(token):
    """解析 JWT 的 exp 字段（unix 秒），失败返回 0"""
    import base64
    try:
        payload = token.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        data = json.loads(base64.urlsafe_b64decode(payload))
        return int(data.get("exp", 0))
    except Exception:
        return 0


def discover_token():
    """
    发现可用的连接器 token。
    优先级：环境变量 > 各 profile 中最新且未过期的 token 文件。
    返回 (token, source_path) 或 (None, None)。
    """
    env_tok = os.environ.get("LEXIANG_ONEID_TOKEN", "").strip()
    if env_tok:
        return env_tok, "env:LEXIANG_ONEID_TOKEN"

    candidates = []
    for pattern in TOKEN_GLOBS:
        for path in glob.glob(os.path.expanduser(pattern)):
            try:
                tok = open(path, "r", encoding="utf-8").read().strip()
            except IOError:
                continue
            if not tok or len(tok) < 20:
                continue
            exp = _decode_jwt_exp(tok)
            mtime = os.path.getmtime(path)
            candidates.append((exp, mtime, tok, path))

    if not candidates:
        return None, None

    now = int(time.time())
    # 优先选未过期且 exp 最大的；都过期则选 mtime 最新的（仍可能被服务端刷新）
    valid = [c for c in candidates if c[0] > now + 30]
    pool = valid if valid else candidates
    pool.sort(key=lambda c: (c[0], c[1]), reverse=True)
    return pool[0][2], pool[0][3]


def _is_token_expired(token):
    """检查 token 是否已过期（JWT exp 字段）。"""
    exp = _decode_jwt_exp(token)
    if exp == 0:
        return False  # 无法解析，假设未过期（让服务端判断）
    return exp < int(time.time()) + 30


def discover_mcp_proxy():
    """
    自动检测 Agent 本地 MCP 代理 URL 和认证头（降级方案）。
    从 WorkBuddy / QClaw / CodeBuddy 进程列表提取。

    返回 (url, auth_headers_dict) 或 (None, None)。
    auth_headers_dict 包含代理所需的 Authorization 和 X-*-Session-Id 头。
    """
    import subprocess, re

    # 环境变量覆盖（仅 URL，不含认证头）
    env_url = os.environ.get("LEXIANG_MCP_PROXY_URL", "").strip()
    if env_url:
        _log(f"   [代理] 使用环境变量 LEXIANG_MCP_PROXY_URL={env_url}")
        return env_url, {}

    # 从进程列表解析（macOS / Linux 通用）
    try:
        out = subprocess.check_output(["ps", "aux"], text=True, stderr=subprocess.DEVNULL)
        for line in out.splitlines():
            # 匹配 WorkBuddy / QClaw / CodeBuddy 进程，且包含 mcp-config
            lower = line.lower()
            if not ("mcp-config" in lower and
                    any(k in lower for k in ("workbuddy", "qclaw", "codebuddy"))):
                continue
            url_m = re.search(r'"url"\s*:\s*"http://127\.0\.0\.1:\d+/mcp"', line)
            auth_m = re.search(r'"Authorization"\s*:\s*"([^"]+)"', line)
            sid_m = re.search(r'"X-WorkBuddy-Session-Id"\s*:\s*"([^"]+)"', line)
            if url_m and auth_m and sid_m:
                url = url_m.group(0).split('"')[3]
                headers = {
                    "Authorization": auth_m.group(1),
                    "X-WorkBuddy-Session-Id": sid_m.group(1),
                }
                _log(f"   [代理] 从进程列表检测到: {url}")
                return url, headers
    except Exception as e:
        _log(f"   [代理] 进程检测失败: {e}")

    return None, None


class LexiangConnector:
    """通过个人凭证或 WorkBuddy / QClaw 连接器调用乐享 MCP。

    鉴权优先级：
      1. 显式个人凭证文件 / credential dict
      2. 显式传入连接器 token
      3. 环境变量 LEXIANG_ONEID_TOKEN / 磁盘 token 文件（原逻辑）
      4. 自动检测 MCP 代理（降级方案，无需 token）
    """

    # 代理模式下的工具名前缀
    _PROXY_TOOL_PREFIX = "lexiang_"

    def __init__(self, token=None, token_path=None,
                 personal_credential_file=None, credential=None):
        if personal_credential_file and credential:
            raise LexiangError(
                "personal_credential_file 与 credential 不能同时传入"
            )
        personal = (
            load_personal_credential(personal_credential_file)
            if personal_credential_file else credential
        )
        self.personal_mode = bool(personal)
        if personal:
            personal_token = str(personal.get("mcp_token", "")).strip()
            company_from = str(personal.get("company_from", "")).strip()
            if not personal_token.startswith("lxmcp_") or not company_from:
                raise LexiangError("乐享个人凭证缺少有效的 mcp_token/company_from")
            self.token = personal_token
            self.token_path = (
                str(Path(personal_credential_file).expanduser())
                if personal_credential_file else "(personal credential)"
            )
            self.use_proxy = False
            self.mcp_url = (
                f"{MCP_URL}?company_from="
                f"{urllib.parse.quote(company_from, safe='')}"
            )
            self.proxy_headers = {}
        elif token:
            # 显式传入 token（最高优先级）
            self.token = token
            self.token_path = token_path or "(explicit)"
            self.use_proxy = False
            self.mcp_url = MCP_URL
            self.proxy_headers = {}
        else:
            # 尝试发现 token（原逻辑，完全不变）
            self.token, self.token_path = discover_token()

            if self.token and not _is_token_expired(self.token):
                # Token 有效，使用直连模式
                self.use_proxy = False
                self.mcp_url = MCP_URL
                self.proxy_headers = {}
            else:
                # Token 不可用或已过期 → 降级到 MCP 代理
                if self.token:
                    _log(f"   [token] token 已过期（来源: {self.token_path}），尝试 MCP 代理模式")
                else:
                    _log(f"   [token] 未找到有效 token，尝试 MCP 代理模式")

                proxy_url, proxy_headers = discover_mcp_proxy()
                if proxy_url:
                    self.use_proxy = True
                    self.mcp_url = proxy_url
                    self.proxy_headers = proxy_headers
                    self.token = None
                    self.token_path = f"(proxy: {proxy_url})"
                    _log(f"   [代理模式] 使用 MCP 代理: {proxy_url}")
                else:
                    raise LexiangError(
                        "未发现有效的乐享连接器 token，且未找到 MCP 代理。\n"
                        "请确认在 WorkBuddy/QClaw 中已授权乐享连接器，"
                        "或设置环境变量 LEXIANG_ONEID_TOKEN。"
                    )

        self._session_id = None
        self._initialized = False

    # ── MCP 协议层 ────────────────────────────────────────────

    def _post_once(self, method, params=None, notification=False):
        """单次 MCP POST 请求（不含重试）。"""
        body = {"jsonrpc": "2.0", "method": method, "params": params or {}}
        if not notification:
            body["id"] = str(uuid.uuid4())
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }
        if self.use_proxy:
            # 代理模式：附加代理认证头
            headers.update(self.proxy_headers)
        elif self.personal_mode:
            headers["Authorization"] = f"Bearer {self.token}"
        else:
            # 直连模式：附加乐享 OAuth token
            headers["X-Oneid-Access-Token"] = self.token
        if self._session_id:
            headers["Mcp-Session-Id"] = self._session_id
        req = urllib.request.Request(
            self.mcp_url, data=json.dumps(body).encode("utf-8"),
            method="POST", headers=headers,
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                sid = resp.headers.get("Mcp-Session-Id")
                if sid:
                    self._session_id = sid
                raw = resp.read().decode("utf-8")
                if not raw.strip():
                    return {}
                # SSE 格式解析
                if "data:" in raw and raw.lstrip().startswith(("event:", "data:")):
                    for line in raw.splitlines():
                        if line.startswith("data:"):
                            return json.loads(line[5:].strip())
                    return {}
                return json.loads(raw)
        except urllib.error.HTTPError as e:
            err = e.read().decode("utf-8", errors="replace")
            if e.code == 401:
                # 鉴权问题，重试无意义
                auth_name = "个人凭证" if self.personal_mode else "连接器 token"
                raise LexiangError(
                    f"乐享{auth_name}已过期或无效（401）。请重新授权后重试。",
                    retryable=False, code=401,
                )
            retryable = e.code in RETRY_HTTP_CODES
            tag = "WAF拦截/限流/网关" if retryable else ""
            raise LexiangError(
                f"MCP HTTP 错误 [{e.code}] {tag} {method}: {err[:200]}",
                retryable=retryable, code=e.code,
            )
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            # 瞬时网络错误（连接重置、超时、DNS 抖动等）→ 可重试
            raise LexiangError(f"MCP 网络错误 {method}: {e}", retryable=True)

    def _post(self, method, params=None, notification=False):
        """带指数退避重试的 MCP POST。仅对可重试错误（WAF 403/限流/5xx/网络）重试。"""
        last_err = None
        for attempt in range(RETRY_MAX + 1):
            try:
                return self._post_once(method, params, notification)
            except LexiangError as e:
                last_err = e
                if not e.retryable or attempt >= RETRY_MAX:
                    # 网络/HTTP 层已重试耗尽 → 标记不再重试，避免上层 call_tool 二次重试
                    e.retryable = False
                    raise
                wait = RETRY_BACKOFF[min(attempt, len(RETRY_BACKOFF) - 1)]
                _log(f"  ⟳ 请求失败可重试（{e}），{wait}s 后第 {attempt + 1}/{RETRY_MAX} 次重试…")
                time.sleep(wait)
        if last_err:
            raise last_err

    def _ensure_init(self):
        if self._initialized:
            return
        self._post("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "sync-obsidian-to-lexiang", "version": "2.1"},
        })
        self._post("notifications/initialized", notification=True)
        self._initialized = True

    def _call_tool_once(self, name, arguments):
        """单次工具调用（_post 已含网络层重试；此处处理业务错误码）。"""
        self._ensure_init()
        # 代理模式：工具名需要加连接器前缀（entry_create_entry → lexiang_entry_create_entry）
        actual_name = name
        if self.use_proxy and not name.startswith(self._PROXY_TOOL_PREFIX):
            actual_name = self._PROXY_TOOL_PREFIX + name
        resp = self._post("tools/call", {"name": actual_name, "arguments": arguments})
        if "error" in resp:
            raise LexiangError(f"工具 {name} 调用失败: {resp['error']}")
        result = resp.get("result", {})
        content = result.get("content", [])
        if content and content[0].get("type") == "text":
            text = content[0]["text"]
            try:
                parsed = json.loads(text)
            except json.JSONDecodeError:
                return text
            # 乐享业务错误码
            if isinstance(parsed, dict) and parsed.get("code") not in (None, 0):
                code = parsed.get("code")
                msg = str(parsed.get("message", ""))
                # WAF/限流以业务码形式返回时也判定为可重试
                retryable = (code in RETRY_HTTP_CODES) or any(
                    kw in msg for kw in ("WAF", "403", "拦截", "频繁", "限流", "rate limit")
                )
                raise LexiangError(
                    f"乐享返回错误 code={code}: {msg}",
                    retryable=retryable, code=code,
                )
            return parsed
        return result

    def call_tool(self, name, arguments):
        """调用 MCP 工具（带业务码层重试），返回解析后的业务数据。"""
        last_err = None
        for attempt in range(RETRY_MAX + 1):
            try:
                return self._call_tool_once(name, arguments)
            except LexiangError as e:
                last_err = e
                if not e.retryable or attempt >= RETRY_MAX:
                    raise
                wait = RETRY_BACKOFF[min(attempt, len(RETRY_BACKOFF) - 1)]
                _log(f"  ⟳ 工具 {name} 失败可重试（{e}），{wait}s 后第 {attempt + 1}/{RETRY_MAX} 次重试…")
                time.sleep(wait)
        if last_err:
            raise last_err

    # ── 业务封装 ──────────────────────────────────────────────

    def whoami(self):
        return self.call_tool("whoami", {})

    def get_space_info(self, space_id):
        """获取知识库信息，返回 dict（含 root_entry_id 等）。"""
        data = self.call_tool("space_describe_space", {"space_id": space_id})
        return data.get("data", {}).get("space", {}) if isinstance(data, dict) else {}

    def resolve_root_entry_id(self, space_id):
        """获取知识库的 root_entry_id。失败时返回 None。"""
        try:
            space = self.get_space_info(space_id)
            return space.get("root_entry_id") or None
        except (LexiangError, KeyError, TypeError):
            return None

    def create_folder(self, space_id, name, parent_id=None):
        args = {"entry_type": "folder", "name": name}
        if parent_id:
            args["parent_entry_id"] = parent_id
        data = self.call_tool("entry_create_entry", args)
        entry = data.get("data", {}).get("entry", {}) if isinstance(data, dict) else {}
        eid = entry.get("id")
        if not eid:
            raise LexiangError(f"创建文件夹失败: {json.dumps(data, ensure_ascii=False)[:200]}")
        return eid

    def describe_entry(self, entry_id):
        data = self.call_tool("entry_describe_entry",
                              {"entry_id": entry_id, "_mcp_fields": "-html_content,-staffs"})
        return data.get("data", {}).get("entry", {}) if isinstance(data, dict) else {}

    def get_entry_edited_at(self, entry_id):
        """获取条目最后编辑时间戳（int 秒），失败返回 0"""
        try:
            entry = self.describe_entry(entry_id)
            v = entry.get("edited_at") or entry.get("updated_at") or 0
            return int(v) if v else 0
        except (LexiangError, ValueError, TypeError):
            return 0

    def probe_entry(self, entry_id):
        """
        探活 + 取父：返回 {"exists": bool, "parent_id": str, "edited_at": int}。
        entry 不存在（被删除）时 exists=False。供中断恢复与移动检测使用。
        """
        try:
            entry = self.describe_entry(entry_id)
        except LexiangError as e:
            msg = str(e).lower()
            # 乐享对「不存在」返回 code=403「拒绝访问」或「不存在」类错误。
            # 对本工具创建的 entry 而言，403/404/不存在 都意味着该 entry 已不可用，
            # 应视为失效并重建（而非中断同步）。
            if any(k in msg for k in ("不存在", "拒绝访问", "403", "404", "not found")):
                return {"exists": False, "parent_id": "", "edited_at": 0}
            raise
        if not entry or not entry.get("id"):
            return {"exists": False, "parent_id": "", "edited_at": 0}
        edited = entry.get("edited_at") or entry.get("updated_at") or 0
        try:
            edited = int(edited)
        except (ValueError, TypeError):
            edited = 0
        return {
            "exists": True,
            "parent_id": entry.get("parent_id", ""),
            "edited_at": edited,
        }

    def list_children(self, parent_id, limit=100):
        data = self.call_tool("entry_list_children",
                              {"parent_id": parent_id, "limit": limit,
                               "_mcp_fields": "-html_content,-staffs,-source"})
        return data.get("data", {}).get("entries", []) if isinstance(data, dict) else []

    # ── 附件上传（3 步流程）──────────────────────────────────

    def _upload_3step(self, file_path, parent_entry_id):
        """
        通用文件上传（apply → PUT → commit），返回 commit 后的 entry dict。
        既用于 markdown 引用的附件，也用于独立文件型 entry（PDF/Office/图片等）。
        失败抛 LexiangError。
        """
        import mimetypes
        name = os.path.basename(file_path)
        size = os.path.getsize(file_path)
        mime = mimetypes.guess_type(name)[0] or "application/octet-stream"

        # Step 1: apply_upload，请求预签名 URL
        apply = self.call_tool("file_apply_upload", {
            "name": name, "size": size, "mime_type": mime,
            "parent_entry_id": parent_entry_id,
            "upload_type": 2,  # PRE_SIGNED_URL
        })
        data = apply.get("data", apply) if isinstance(apply, dict) else {}
        session = data.get("session", data)
        session_id = session.get("session_id") or session.get("id")
        # 预签名 URL 在 session.objects[0].upload_url（单文件场景）
        upload_url = ""
        objects = session.get("objects") or []
        if objects:
            upload_url = objects[0].get("upload_url") or objects[0].get("url", "")
            # mime 以 apply 返回为准（影响签名一致性）
            mime = objects[0].get("mime_type") or mime
        if not upload_url:  # 兼容可能的扁平结构
            upload_url = session.get("upload_url") or session.get("url", "")
        if not (session_id and upload_url):
            raise LexiangError(f"申请上传失败: {json.dumps(apply, ensure_ascii=False)[:200]}")

        # Step 2: PUT 文件内容到预签名 URL
        # 签名要求 content-length + content-type + host，必须严格匹配
        with open(file_path, "rb") as f:
            file_data = f.read()
        put_req = urllib.request.Request(
            upload_url, data=file_data, method="PUT",
            headers={"Content-Type": mime, "Content-Length": str(len(file_data))},
        )
        try:
            with urllib.request.urlopen(put_req, timeout=300) as r:
                if r.status not in (200, 204):
                    raise LexiangError(f"文件 PUT 失败 status={r.status}")
        except urllib.error.HTTPError as e:
            raise LexiangError(f"文件 PUT 失败 [{e.code}]: {e.read().decode('utf-8','replace')[:200]}")

        # Step 3: commit_upload，返回正式创建的文件 entry
        commit = self.call_tool("file_commit_upload", {"session_id": session_id})
        cdata = commit.get("data", commit) if isinstance(commit, dict) else {}
        return cdata.get("entry", cdata)

    def upload_attachment(self, file_path, parent_entry_id):
        """上传 markdown 引用的附件，返回访问 URL（用于替换正文引用）"""
        entry = self._upload_3step(file_path, parent_entry_id)
        return (entry.get("download") or entry.get("url")
                or entry.get("access_url") or "")

    def upload_file_entry(self, file_path, parent_entry_id):
        """
        把独立文件（PDF/Office/图片等）作为文件型 entry 上传到指定目录。
        返回 entry_id（用于 manifest 映射）。
        """
        entry = self._upload_3step(file_path, parent_entry_id)
        eid = entry.get("id")
        if not eid:
            raise LexiangError(f"上传文件 entry 失败: {json.dumps(entry, ensure_ascii=False)[:200]}")
        return eid

# 向后兼容别名
LexiangAPI = LexiangConnector
