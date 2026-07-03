#!/usr/bin/env python3
"""
lexiang_api.py - 乐享客户端（连接器模式，零配置零 token）

核心机制：复用 WorkBuddy / QClaw 等 Agent 内置乐享连接器的 OAuth 凭证，
脚本直接调用乐享 MCP 端点（https://mcp.lexiang-app.com/mcp），
鉴权头为 X-Oneid-Access-Token（从本地连接器 token 文件读取）。

用户无需安装额外 skill、无需获取任何 app_key/secret —— 只要 Agent 里
已经授权了乐享连接器，脚本就能直接用。

token 文件发现：
  ~/.workbuddy/connectors/<profile>/tokens/lexiang-ol.txt   (WorkBuddy)
  环境变量 LEXIANG_ONEID_TOKEN 可显式覆盖

仅依赖 Python 标准库。
"""

import glob
import json
import os
import time
import urllib.request
import urllib.error
import uuid

MCP_URL = "https://mcp.lexiang-app.com/mcp"

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


class LexiangConnector:
    """通过 WorkBuddy 内置连接器调用乐享 MCP（零配置）"""

    def __init__(self, token=None, token_path=None):
        if token:
            self.token, self.token_path = token, token_path or "(explicit)"
        else:
            self.token, self.token_path = discover_token()
        if not self.token:
            raise LexiangError(
                "未发现乐享连接器 token。请确认在 WorkBuddy/QClaw 中已授权乐享连接器。"
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
            "X-Oneid-Access-Token": self.token,
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }
        if self._session_id:
            headers["Mcp-Session-Id"] = self._session_id
        req = urllib.request.Request(
            MCP_URL, data=json.dumps(body).encode("utf-8"),
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
                raise LexiangError(
                    "连接器 token 已过期或无效（401）。请在 WorkBuddy 中重新授权乐享连接器后重试。",
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
            "clientInfo": {"name": "sync-obsidian-to-lexiang", "version": "2.0"},
        })
        self._post("notifications/initialized", notification=True)
        self._initialized = True

    def _call_tool_once(self, name, arguments):
        """单次工具调用（_post 已含网络层重试；此处处理业务错误码）。"""
        self._ensure_init()
        resp = self._post("tools/call", {"name": name, "arguments": arguments})
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

    def create_page_with_content(self, space_id, name, content, parent_id=None,
                                 content_type="markdown"):
        """创建 page 并写入 markdown 内容（一步到位）。返回 entry_id"""
        args = {"space_id": space_id, "name": name, "content": content,
                "content_type": content_type}
        if parent_id:
            args["parent_id"] = parent_id
        data = self.call_tool("entry_import_content", args)
        entry = data.get("data", {}).get("entry", {}) if isinstance(data, dict) else {}
        eid = entry.get("id")
        if not eid:
            raise LexiangError(f"创建文档失败: {json.dumps(data, ensure_ascii=False)[:200]}")
        return eid

    def update_page_content(self, entry_id, content, content_type="markdown",
                            force_write=True):
        """覆盖/追加更新已有 page 内容"""
        args = {"entry_id": entry_id, "content": content,
                "content_type": content_type, "force_write": force_write}
        return self.call_tool("entry_import_content_to_entry", args)

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

    # ── 块级操作：图文混排（正文内嵌本地图片）────────────────────

    def convert_to_blocks(self, content, content_type="markdown"):
        """把 markdown/html 文本转成与 create_block_descendant 兼容的 block 列表。"""
        data = self.call_tool("block_convert_content_to_blocks",
                              {"content": content, "content_type": content_type})
        return data.get("data", {}).get("descendant", []) if isinstance(data, dict) else []

    def upload_block_image(self, entry_id, file_path):
        """
        上传一张正文内嵌图片（block 附件上传：apply → PUT → 返回 session_id）。
        随后把 session_id 放进 image block 的 image.session_id 字段即可内嵌。
        返回 session_id。失败抛 LexiangError。
        """
        import mimetypes
        name = os.path.basename(file_path)
        size = os.path.getsize(file_path)
        mime = mimetypes.guess_type(name)[0] or "image/png"

        apply = self.call_tool("block_apply_block_attachment_upload", {
            "entry_id": entry_id, "name": name,
            "size": str(size), "mime_type": mime,
        })
        d = apply.get("data", {}) if isinstance(apply, dict) else {}
        session_id = d.get("session_id")
        upload_url = d.get("upload_url")
        if not (session_id and upload_url):
            raise LexiangError(f"申请块图片上传失败: {json.dumps(apply, ensure_ascii=False)[:200]}")

        with open(file_path, "rb") as f:
            data_bytes = f.read()
        put_req = urllib.request.Request(
            upload_url, data=data_bytes, method="PUT",
            headers={"Content-Type": mime, "Content-Length": str(len(data_bytes))},
        )
        try:
            with urllib.request.urlopen(put_req, timeout=300) as r:
                if r.status not in (200, 204):
                    raise LexiangError(f"块图片 PUT 失败 status={r.status}")
        except urllib.error.HTTPError as e:
            raise LexiangError(
                f"块图片 PUT 失败 [{e.code}]: {e.read().decode('utf-8','replace')[:200]}")
        return session_id

    def create_blocks(self, entry_id, descendant, index="-1", parent_block_id=None):
        """在 entry（或指定父块）下按序创建一批 block。descendant 为有序数组。"""
        if not descendant:
            return {}
        args = {"entry_id": entry_id, "descendant": descendant, "index": str(index)}
        if parent_block_id:
            args["parent_block_id"] = parent_block_id
        return self.call_tool("block_create_block_descendant", args)

    def clear_page(self, entry_id):
        """清空 page 的全部 block（用于更新覆盖前）。逐个删除直接子块。"""
        children = self.call_tool("block_list_block_children",
                                  {"entry_id": entry_id, "with_descendants": False})
        blocks = children.get("data", {}).get("blocks", []) if isinstance(children, dict) else []
        for b in blocks:
            bid = b.get("block_id")
            if bid:
                try:
                    self.call_tool("block_delete_block", {"entry_id": entry_id, "block_id": bid})
                except LexiangError:
                    pass

    def write_segments(self, entry_id, segments):
        """
        把有序的图文片段写入已存在的 page（追加到末尾，保持原始顺序）。

        segments: converter.split_into_segments 的结果，每项有 .kind / .text /
                  .image_abs_path / .image_alt。
        - text 片段：convert_to_blocks 转成 block 数组
        - image 片段：upload_block_image 拿 session_id → image block

        为保证「文本 → 图片 → 文本」的顺序绝对正确，逐片段按序 append。
        返回 (success_images, fail_images)。
        """
        img_ok = img_fail = 0
        for seg in segments:
            kind = getattr(seg, "kind", None) or seg.get("kind")
            if kind == "text":
                text = getattr(seg, "text", "") or seg.get("text", "")
                if not text.strip():
                    continue
                blocks = self.convert_to_blocks(text, "markdown")
                if blocks:
                    self.create_blocks(entry_id, blocks, index="-1")
            elif kind == "image":
                path = getattr(seg, "image_abs_path", "") or seg.get("image_abs_path", "")
                alt = getattr(seg, "image_alt", "") or seg.get("image_alt", "")
                try:
                    session_id = self.upload_block_image(entry_id, path)
                    img_block = {"block_type": "image",
                                 "image": {"session_id": session_id, "align": "center"}}
                    if alt:
                        img_block["image"]["caption"] = alt
                    self.create_blocks(entry_id, [img_block], index="-1")
                    img_ok += 1
                except LexiangError:
                    img_fail += 1
        return img_ok, img_fail

    def create_page_with_segments(self, space_id, name, segments, parent_id=None):
        """
        创建一篇图文混排 page：先建空 page，再按序写入文本/图片片段。
        返回 (entry_id, img_ok, img_fail)。
        """
        # entry_import_content 要求 content 非空；用占位文本建骨架，随后清空，
        # 保证后续完全由 write_segments 按序掌控（文本+图片）。
        entry_id = self.create_page_with_content(space_id, name, "\u200b", parent_id)
        try:
            self.clear_page(entry_id)
        except LexiangError:
            pass
        img_ok, img_fail = self.write_segments(entry_id, segments)
        return entry_id, img_ok, img_fail

    def update_page_with_segments(self, entry_id, segments):
        """覆盖更新图文 page：清空后按序重写。返回 (img_ok, img_fail)。"""
        self.clear_page(entry_id)
        return self.write_segments(entry_id, segments)


# 向后兼容别名
LexiangAPI = LexiangConnector
