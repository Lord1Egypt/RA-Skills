#!/usr/bin/env python3
"""Validated Markdown-to-Lexiang page uploader."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import getpass
import json
import mimetypes
import os
from pathlib import Path
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

from lexiang_upload_core import (
    LEXIANG_MATH_RE,
    PreflightError,
    UploadPlan,
    VerificationError,
    build_plan,
    convert_math,
    count_remote_callouts,
    count_remote_images,
    verify_remote,
)


VERSION = "1.3.1"
CLI_API = "1"
CREDENTIAL_HELP_URL = "https://lexiangla.com/ai/claw"
MCP_BASE_URL = "https://mcp.lexiang-app.com/mcp"
DEFAULT_CREDENTIALS = Path("~/.config/lexiang-upload/credentials.json").expanduser()
PROFILE_CREDENTIALS_DIR = Path("~/.config/lexiang-upload/profiles").expanduser()
PROFILE_RE = re.compile(r"^[A-Za-z0-9._-]+$")
SKIP_MD_NAMES = {"parsed_raw.md", "source.md"}


class AuthError(RuntimeError):
    pass


class MCPError(RuntimeError):
    pass


@dataclass
class PersonalCredential:
    mcp_token: str
    company_from: str

    @classmethod
    def from_dict(cls, data: dict) -> "PersonalCredential":
        candidates = [data]
        candidates.extend(
            value
            for key in ("mcp", "credential", "credentials", "auth")
            if isinstance((value := data.get(key)), dict)
        )

        def pick(*keys: str) -> str:
            for candidate in candidates:
                for key in keys:
                    if candidate.get(key):
                        return str(candidate[key]).strip()
            return ""

        return cls(
            mcp_token=pick("mcp_token", "access_token", "token", "LEXIANG_TOKEN"),
            company_from=pick("company_from", "mcp_company_from"),
        )

    @classmethod
    def from_text(cls, raw: str) -> "PersonalCredential":
        """Parse copied JSON, URL parameters, or an ai/claw install command."""
        try:
            value = json.loads(raw)
        except json.JSONDecodeError:
            value = None
        if isinstance(value, dict):
            return cls.from_dict(value)
        token_match = re.search(r"\blxmcp_[A-Za-z0-9_-]+\b", raw)
        company_match = re.search(r"(?:[?&\s\"']|^)company_from[=\s]+([A-Za-z0-9_-]+)", raw)
        return cls(
            mcp_token=token_match.group(0) if token_match else "",
            company_from=urllib.parse.unquote(company_match.group(1)) if company_match else "",
        )

    def validate_shape(self) -> None:
        missing = [
            label
            for label, value in (
                ("mcp_token", self.mcp_token),
                ("company_from", self.company_from),
            )
            if not value
        ]
        if missing:
            raise AuthError("个人凭证缺少字段：" + ", ".join(missing))
        if not self.mcp_token.startswith("lxmcp_"):
            raise AuthError("mcp_token 格式无效，应为 ai/claw 页面提供的 lxmcp_ Token")

    def to_dict(self) -> dict:
        return {
            "mcp_token": self.mcp_token,
            "company_from": self.company_from,
        }


@dataclass(frozen=True)
class CredentialSelector:
    """A resolved credential location without any credential secrets."""

    profile: str | None
    path: Path

    def json_fields(self) -> dict:
        return {
            "credential_profile": self.profile,
            "credential_file": str(self.path),
        }


def _validated_profile(profile: str) -> str:
    value = profile.strip()
    if not value or not PROFILE_RE.fullmatch(value):
        raise AuthError(
            "profile 名称只能包含 A-Z、a-z、0-9、点、下划线和连字符，且不能为空"
        )
    return value


def resolve_credential_selector(
    profile: str | None = None,
    credential_file: str | None = None,
    environ: dict[str, str] | None = None,
) -> CredentialSelector:
    """Resolve CLI and environment selectors in documented precedence order."""
    env = os.environ if environ is None else environ
    explicit_file = (credential_file or "").strip()
    env_file = env.get("LEXIANG_UPLOAD_CREDENTIALS", "").strip()
    env_profile = env.get("LEXIANG_UPLOAD_PROFILE", "").strip()

    if explicit_file:
        return CredentialSelector(None, Path(explicit_file).expanduser())
    if profile is not None:
        selected_profile = _validated_profile(profile)
    elif env_file:
        return CredentialSelector(None, Path(env_file).expanduser())
    elif env_profile:
        selected_profile = _validated_profile(env_profile)
    else:
        selected_profile = "default"

    path = (
        DEFAULT_CREDENTIALS
        if selected_profile == "default"
        else PROFILE_CREDENTIALS_DIR / f"{selected_profile}.json"
    )
    return CredentialSelector(selected_profile, path)


def credentials_path(selector: CredentialSelector | None = None) -> Path:
    return (selector or resolve_credential_selector()).path


def save_credential(
    credential: PersonalCredential,
    selector: CredentialSelector | None = None,
) -> None:
    path = credentials_path(selector)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(credential.to_dict(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.chmod(0o600)
    temporary.replace(path)
    path.chmod(0o600)


def load_credential(selector: CredentialSelector | None = None) -> PersonalCredential:
    path = credentials_path(selector)
    if not path.is_file():
        raise AuthError(
            f"尚未配置乐享个人凭证。请访问 {CREDENTIAL_HELP_URL} 获取后运行："
            " lexiang_upload.py auth login"
        )
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise AuthError(f"个人凭证文件无法读取：{path}") from error
    credential = PersonalCredential.from_dict(data)
    credential.validate_shape()
    return credential


class MCPClient:
    def __init__(self, credential: PersonalCredential, retries: int = 3) -> None:
        self.credential = credential
        self.retries = retries
        self.access_token = credential.mcp_token
        self.session_id = ""
        self._initialize()

    @property
    def url(self) -> str:
        return f"{MCP_BASE_URL}?company_from={urllib.parse.quote(self.credential.company_from)}"

    @staticmethod
    def _parse_transport(raw: str) -> dict:
        candidates = [raw.strip()]
        candidates.extend(
            line[5:].strip() for line in raw.splitlines() if line.strip().startswith("data:")
        )
        for candidate in candidates:
            if not candidate or candidate == "[DONE]":
                continue
            try:
                outer = json.loads(candidate)
            except json.JSONDecodeError:
                continue
            if "error" in outer:
                raise MCPError(f"MCP JSON-RPC error: {outer['error']}")
            result = outer.get("result", outer)
            if isinstance(result, dict) and result.get("isError"):
                content = result.get("content", [])
                message = content[0].get("text", "unknown error") if content else "unknown error"
                raise MCPError(message)
            return result
        raise MCPError("MCP 返回无法解析")

    def _post(self, payload: dict, *, initialize: bool = False) -> dict:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "Authorization": f"Bearer {self.access_token}",
        }
        if self.session_id:
            headers["Mcp-Session-Id"] = self.session_id
        last_error: Exception | None = None
        for attempt in range(self.retries):
            request = urllib.request.Request(
                self.url,
                data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                headers=headers,
                method="POST",
            )
            try:
                with urllib.request.urlopen(request, timeout=180) as response:
                    if initialize:
                        self.session_id = response.headers.get("Mcp-Session-Id", "")
                    return self._parse_transport(response.read().decode("utf-8"))
            except urllib.error.HTTPError as error:
                detail = error.read().decode("utf-8", errors="replace")
                if error.code == 401:
                    raise AuthError(
                        f"乐享个人凭证无效、已过期或已撤销（401）。请访问 {CREDENTIAL_HELP_URL} 续期或重新获取"
                    ) from error
                if error.code < 500 or attempt == self.retries - 1:
                    raise MCPError(f"MCP HTTP {error.code}: {detail[:300]}") from error
                last_error = error
            except (urllib.error.URLError, TimeoutError) as error:
                last_error = error
                if attempt == self.retries - 1:
                    break
            time.sleep(2**attempt)
        raise MCPError(f"MCP 网络请求失败，已重试 {self.retries} 次：{last_error}")

    def _initialize(self) -> None:
        self._post(
            {
                "jsonrpc": "2.0",
                "id": uuid.uuid4().hex,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-03-26",
                    "capabilities": {},
                    "clientInfo": {"name": "lexiang-upload", "version": VERSION},
                },
            },
            initialize=True,
        )

    def _request(self, tool: str, arguments: dict) -> dict:
        return self._post(
            {
                "jsonrpc": "2.0",
                "id": uuid.uuid4().hex,
                "method": "tools/call",
                "params": {"name": tool, "arguments": arguments},
            }
        )

    def text(self, tool: str, arguments: dict) -> str:
        result = self._request(tool, arguments)
        content = result.get("content", [])
        return content[0].get("text", "") if content else ""

    def json(self, tool: str, arguments: dict) -> dict:
        text = self.text(tool, arguments)
        try:
            value = json.loads(text)
        except json.JSONDecodeError as error:
            raise MCPError(f"{tool} 应返回 JSON，实际为：{text[:300]}") from error
        if value.get("code", 0) != 0:
            raise MCPError(f"{tool}: {value.get('message', value)}")
        return value


def resolve_markdown(work_dir: Path | None, markdown_arg: str | None) -> Path:
    if markdown_arg:
        candidate = Path(markdown_arg)
        if not candidate.is_absolute() and work_dir:
            candidate = work_dir / candidate
        candidate = candidate.resolve()
        if not candidate.is_file():
            raise PreflightError(f"Markdown 不存在：{candidate}")
        return candidate
    if not work_dir:
        raise PreflightError("请指定 Markdown 文件或 --work-dir")
    candidates = sorted(path for path in work_dir.glob("*.md") if path.name not in SKIP_MD_NAMES)
    if len(candidates) != 1:
        names = ", ".join(path.name for path in candidates) or "无"
        raise PreflightError(f"无法唯一确定待上传 Markdown：{names}")
    return candidates[0]


def load_meta(path: str | None, base: Path) -> dict:
    if not path:
        return {}
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = base / candidate
    if not candidate.is_file():
        raise PreflightError(f"meta 文件不存在：{candidate}")
    try:
        return json.loads(candidate.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise PreflightError(f"meta 文件不是有效 JSON：{candidate}") from error


def first_heading(markdown: str) -> str:
    match = re.search(r"^#\s+(.+?)\s*$", markdown, re.MULTILINE)
    return match.group(1).strip() if match else ""


def prepend_source_link(markdown: str, source_url: str, source_title: str) -> str:
    if (
        not source_url
        or source_url in markdown
        or re.search(r"(?:\*\*)?原文链接(?:\*\*)?\s*[：:]", markdown)
    ):
        return markdown
    title = source_title or "原文"
    return f"**原文链接**：[{title}]({source_url})\n\n{markdown}"


def resolve_source(
    explicit_url: str,
    explicit_title: str,
    meta: dict,
    source_from_meta: bool,
    credential_loader=load_credential,
) -> tuple[str, str]:
    """Resolve source fields while preserving the cli_api=1 precedence rules."""
    source_url = explicit_url
    source_title = explicit_title
    if source_from_meta:
        source_url = source_url or str(meta.get("source_url") or "")
        source_title = (
            source_title
            or str(meta.get("source_title") or "")
            or str(meta.get("title") or "")
        )
        if not source_url and meta.get("entry_id"):
            source_url = f"https://lexiangla.com/pages/{meta['entry_id']}"
            if credential_loader is not None:
                credential = credential_loader()
                source_url += f"?company_from={credential.company_from}"
    else:
        source_title = source_title or str(meta.get("title") or "")
    return source_url, source_title


def _mathtext_compatible(latex: str) -> str:
    return re.sub(
        r"\\text\{([^{}]*)\}",
        lambda match: r"\mathrm{" + match.group(1).replace(" ", r"\ ") + "}",
        latex,
    )


def render_formula_png(latex: str, destination: Path) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        from matplotlib.mathtext import math_to_image
    except ImportError as error:
        raise PreflightError("公式图片模式需要 matplotlib") from error
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        math_to_image(
            f"${_mathtext_compatible(latex)}$",
            str(destination),
            dpi=180,
            format="png",
            color="#111111",
        )
    except Exception as error:
        raise PreflightError(f"公式无法渲染：{latex[:100]}（{error}）") from error


_SUBSCRIPT = str.maketrans("0123456789+-=()aehijklmnoprstuvxV", "₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑₕᵢⱼₖₗₘₙₒₚᵣₛₜᵤᵥₓᵥ")
_SUPERSCRIPT = str.maketrans("0123456789+-=()ain", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ᵃⁱⁿ")
_GREEK = {
    "alpha": "α", "beta": "β", "gamma": "γ", "delta": "δ", "epsilon": "ε",
    "theta": "θ", "lambda": "λ", "mu": "μ", "pi": "π", "rho": "ρ",
    "sigma": "σ", "phi": "φ", "Phi": "Φ", "omega": "ω",
}
_OPERATORS = {
    "log": "log", "ln": "ln", "exp": "exp", "min": "min", "max": "max",
    "cdot": "·", "times": "×", "approx": "≈", "sim": "∼", "propto": "∝",
    "equiv": "≡", "le": "≤", "ge": "≥", "neq": "≠", "infty": "∞",
}


def latex_to_unicode(latex: str) -> str:
    text = re.sub(r"\\(?:text|mathrm)\{([^{}]*)\}", r"\1", latex)
    text = re.sub(
        r"\\frac\{((?:[^{}]|\{[^{}]*\})+)\}\{((?:[^{}]|\{[^{}]*\})+)\}",
        r"\1/\2",
        text,
    )
    text = re.sub(r"\\sqrt\{([^{}]+)\}", r"√(\1)", text)
    text = re.sub(r"\\bar\{([^{}]+)\}", lambda match: match.group(1) + "\u0304", text)
    text = re.sub(r"\\(?:quad|qquad)\b|\\[,;!]", " ", text)
    text = re.sub(r"\\(?:left|right)\b", "", text)
    text = re.sub(
        r"\\([A-Za-z]+)",
        lambda match: _GREEK.get(match.group(1), _OPERATORS.get(match.group(1), "\\" + match.group(1))),
        text,
    )
    text = re.sub(
        r"_\{([^{}]+)\}|_([A-Za-z0-9])",
        lambda match: (match.group(1) or match.group(2)).translate(_SUBSCRIPT),
        text,
    )
    text = re.sub(
        r"\^\{([^{}]+)\}|\^([A-Za-z0-9])",
        lambda match: (match.group(1) or match.group(2)).translate(_SUPERSCRIPT),
        text,
    )
    return re.sub(r"\s+", " ", text.replace("{", "").replace("}", "")).strip()


def materialize_formula_fallback(markdown: str, base_dir: Path, *, render_images: bool) -> tuple[str, int]:
    converted, formulas = convert_math(markdown)
    formula_iter = iter(enumerate(formulas))
    output: list[str] = []
    formula_dir = base_dir / ".lexiang-formulas"
    for line in converted.splitlines():
        is_table_row = line.lstrip().startswith("|")

        def replace(match: re.Match[str]) -> str:
            try:
                index, formula = next(formula_iter)
            except StopIteration as error:
                raise PreflightError("公式转换计数不一致") from error
            if is_table_row or not render_images:
                return latex_to_unicode(formula.latex)
            filename = f"formula_{index:04d}.png"
            render_formula_png(formula.latex, formula_dir / filename)
            return f"![公式：{formula.latex}](.lexiang-formulas/{filename})"

        output.append(LEXIANG_MATH_RE.sub(replace, line))
    try:
        next(formula_iter)
    except StopIteration:
        pass
    else:
        raise PreflightError("存在未物化的公式")
    return "\n".join(output), len(formulas)


def create_page(client: MCPClient, parent_id: str, name: str) -> str:
    result = client.json(
        "entry_create_entry",
        {"parent_entry_id": parent_id, "name": name, "entry_type": "page"},
    )
    entry_id = result.get("data", {}).get("entry", {}).get("id")
    if not entry_id:
        raise MCPError("创建页面成功响应中没有 entry_id")
    return entry_id


def pin_page(client: MCPClient, entry_id: str, parent_id: str) -> None:
    result = client.json(
        "entry_list_children",
        {"parent_id": parent_id, "limit": 5, "_mcp_fields": "-html_content,-staffs"},
    )
    for entry in result.get("data", {}).get("entries", []):
        sibling_id = entry.get("id")
        if sibling_id and sibling_id != entry_id:
            client.json(
                "entry_move_entry",
                {"entry_id": entry_id, "parent_id": parent_id, "before": sibling_id},
            )
            return


def fetch_markdown(client: MCPClient, entry_id: str) -> str:
    return client.text("block_fetch_page", {"entry_id": entry_id, "render_mode": "markdown"})


def replace_page_text(client: MCPClient, entry_id: str, markdown: str) -> str:
    message = client.text(
        "block_update_page",
        {
            "entry_id": entry_id,
            "command": "replace_content",
            "content_format": "markdown",
            "new_str": markdown,
        },
    )
    if "succeeded" not in message.lower():
        raise MCPError(f"replace_content 未确认成功：{message}")
    return fetch_markdown(client, entry_id)


def append_page_text(client: MCPClient, entry_id: str, addition: str) -> str:
    converted = client.json(
        "block_convert_content_to_blocks",
        {"content": addition, "content_type": "markdown"},
    )
    data = converted.get("data", {})
    descendants = data.get("descendant") or data.get("blocks")
    if not descendants:
        raise MCPError("Markdown 转换没有产生可追加的 block")
    arguments = {"entry_id": entry_id, "index": -1, "descendant": descendants}
    children = data.get("children")
    if children:
        arguments["children"] = children
    client.json("block_create_block_descendant", arguments)
    return fetch_markdown(client, entry_id)


def append_callout(client: MCPClient, entry_id: str, markdown: str, icon: str) -> None:
    converted = client.json(
        "block_convert_content_to_blocks",
        {"content": markdown, "content_type": "markdown"},
    )
    data = converted.get("data", {})
    descendants = data.get("descendant") or data.get("blocks")
    if not descendants:
        raise MCPError("callout 内容转换没有产生 block")
    child_ids = list(data.get("children") or [])
    if not child_ids:
        child_ids = []
        for index, block in enumerate(descendants):
            block_id = block.get("block_id") or f"co_child_{uuid.uuid4().hex[:10]}_{index}"
            block["block_id"] = block_id
            child_ids.append(block_id)
    callout_id = f"co_{uuid.uuid4().hex[:12]}"
    callout = {
        "block_id": callout_id,
        "block_type": "callout",
        "callout": {"icon": icon},
        "children": child_ids,
    }
    client.json(
        "block_create_block_descendant",
        {"entry_id": entry_id, "index": -1, "descendant": [callout, *descendants]},
    )


def upload_image(client: MCPClient, entry_id: str, path: Path) -> None:
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    applied = client.json(
        "block_apply_block_attachment_upload",
        {
            "entry_id": entry_id,
            "name": path.name,
            "size": str(path.stat().st_size),
            "mime_type": mime,
        },
    )
    data = applied.get("data", {})
    session_id, upload_url = data.get("session_id"), data.get("upload_url")
    if not session_id or not upload_url:
        raise MCPError(f"图片 {path.name} 未获得上传会话")
    request = urllib.request.Request(
        upload_url,
        data=path.read_bytes(),
        headers={"Content-Type": mime, "Content-Length": str(path.stat().st_size)},
        method="PUT",
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        if response.status not in (200, 201, 204):
            raise MCPError(f"图片 {path.name} PUT 失败：HTTP {response.status}")
    temp_id = f"img_{uuid.uuid4().hex[:10]}"
    client.json(
        "block_create_block_descendant",
        {
            "entry_id": entry_id,
            "index": -1,
            "descendant": [
                {
                    "block_id": temp_id,
                    "block_type": "image",
                    "image": {"session_id": session_id},
                }
            ],
            "children": [temp_id],
        },
    )


def clear_existing_page(client: MCPClient, entry_id: str) -> None:
    result = client.json(
        "block_list_block_children",
        {"entry_id": entry_id, "with_descendants": False},
    )
    ids = [
        block.get("block_id")
        for block in result.get("data", {}).get("blocks", [])
        if block.get("block_id")
    ]
    if ids:
        client.json("block_delete_block_children", {"entry_id": entry_id, "ids": ids})


def execute_plan(client: MCPClient, entry_id: str, plan: UploadPlan) -> None:
    initialized = False
    for index, segment in enumerate(plan.segments):
        print(
            f"[{index + 1}/{len(plan.segments)}] {segment.kind}",
            file=sys.stderr,
            flush=True,
        )
        if segment.kind == "text":
            if not initialized:
                replace_page_text(client, entry_id, segment.value)
                initialized = True
            else:
                append_page_text(client, entry_id, segment.value)
        elif segment.kind == "image":
            if not initialized:
                replace_page_text(client, entry_id, "\u200b")
                initialized = True
            upload_image(client, entry_id, Path(segment.value))
        else:
            if not initialized:
                replace_page_text(client, entry_id, "\u200b")
                initialized = True
            append_callout(client, entry_id, segment.value, segment.icon)


def remote_blocks(client: MCPClient, entry_id: str) -> list[dict]:
    result = client.json(
        "block_list_block_children",
        {"entry_id": entry_id, "with_descendants": True},
    )
    return result.get("data", {}).get("blocks", [])


def verify_page(
    client: MCPClient,
    entry_id: str,
    plan: UploadPlan,
    attempts: int = 4,
) -> tuple[int, int]:
    for attempt in range(attempts):
        clean = client.text("block_fetch_page", {"entry_id": entry_id, "render_mode": "clean"})
        markdown = fetch_markdown(client, entry_id)
        blocks = remote_blocks(client, entry_id)
        remote_images = count_remote_images(blocks)
        remote_callouts = count_remote_callouts(blocks)
        try:
            verify_remote(plan, clean, markdown, remote_images, remote_callouts)
        except VerificationError:
            if attempt + 1 >= attempts:
                raise
            time.sleep(2**attempt)
            continue
        return remote_images, remote_callouts
    raise VerificationError("线上对账重试次数必须大于零")


def auth_login(
    source_file: str | None,
    selector: CredentialSelector | None = None,
) -> int:
    selector = selector or resolve_credential_selector()
    print(f"请先访问 {CREDENTIAL_HELP_URL} 获取个人凭证。", file=sys.stderr)
    print("可读取页面导出的文件、粘贴凭证/安装指令，或逐项输入。", file=sys.stderr)
    raw = ""
    if source_file:
        try:
            raw = Path(source_file).expanduser().read_text(encoding="utf-8")
        except OSError as error:
            raise AuthError(f"无法读取个人凭证文件：{source_file}") from error
    else:
        raw = getpass.getpass("个人凭证或安装指令（输入隐藏，留空逐项输入）: ").strip()
    if raw:
        credential = PersonalCredential.from_text(raw)
    else:
        credential = PersonalCredential(
            mcp_token=getpass.getpass("MCP API Token（lxmcp_...）: ").strip(),
            company_from=input("company_from: ").strip(),
        )
    credential.validate_shape()
    client = MCPClient(credential)
    client.text("whoami", {})
    save_credential(credential, selector)
    print(json.dumps({"ok": True, **selector.json_fields()}, ensure_ascii=False))
    return 0


def auth_status(check: bool, selector: CredentialSelector | None = None) -> int:
    selector = selector or resolve_credential_selector()
    credential = load_credential(selector)
    if check:
        client = MCPClient(credential)
        client.text("whoami", {})
    print(
        json.dumps(
            {
                "ok": True,
                "configured": True,
                "checked": check,
                **selector.json_fields(),
                "company_from": credential.company_from,
            },
            ensure_ascii=False,
        )
    )
    return 0


def auth_logout(selector: CredentialSelector | None = None) -> int:
    selector = selector or resolve_credential_selector()
    path = credentials_path(selector)
    if path.exists():
        path.unlink()
    print(
        json.dumps(
            {"ok": True, "removed": str(path), **selector.json_fields()},
            ensure_ascii=False,
        )
    )
    return 0


def upload(args: argparse.Namespace) -> int:
    selector = resolve_credential_selector(
        getattr(args, "profile", None),
        getattr(args, "credential_file", None),
    )
    credential = None if args.dry_run else load_credential(selector)
    work_dir = Path(args.work_dir).resolve() if args.work_dir else None
    markdown_path = resolve_markdown(work_dir, args.md_name or args.md_path)
    meta = load_meta(args.meta_file, work_dir or markdown_path.parent)
    markdown = markdown_path.read_text(encoding="utf-8")
    source_url, source_title = resolve_source(
        args.source_url,
        args.source_title,
        meta,
        args.source_from_meta,
        credential_loader=(None if credential is None else lambda: credential),
    )
    markdown = prepend_source_link(
        markdown,
        source_url,
        source_title,
    )
    formula_count = 0
    if args.formula_mode in ("unicode", "hybrid", "image"):
        markdown, formula_count = materialize_formula_fallback(
            markdown,
            markdown_path.parent,
            render_images=args.formula_mode == "image",
        )
    plan = build_plan(markdown, markdown_path.parent)
    if args.formula_mode == "native":
        formula_count = len(plan.formulas)
    base_name = args.name or str(meta.get("title") or "") or first_heading(markdown) or markdown_path.stem
    name = base_name
    suffix = args.name_suffix or ""
    if suffix and not name.endswith(suffix):
        name += suffix
    parent_id = args.parent_id or (str(meta.get("parent_id") or "") if args.parent_from_meta else "")
    if not args.entry_id and not parent_id:
        raise PreflightError("新建页面需要 --parent-id，或显式启用 --parent-from-meta")
    summary = {
        "ok": True,
        "action": "dry-run" if args.dry_run else ("updated" if args.entry_id else "created"),
        "dry_run": args.dry_run,
        "markdown": str(markdown_path),
        "title": name,
        "headings": len(plan.headings),
        "formulas": formula_count,
        "formula_mode": args.formula_mode,
        "local_images": len(plan.image_paths),
        "local_callouts": len(plan.callouts),
        "remote_image_references": plan.remote_image_references,
        "segments": len(plan.segments),
        "verified": False,
        "cli_api": CLI_API,
        "version": VERSION,
        **selector.json_fields(),
    }
    if args.dry_run:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0
    assert credential is not None
    client = MCPClient(credential)
    entry_id = args.entry_id or create_page(client, parent_id, name)
    if args.entry_id:
        clear_existing_page(client, entry_id)
    if not args.entry_id and args.pin:
        pin_page(client, entry_id, parent_id)
    execute_plan(client, entry_id, plan)
    remote_images, remote_callouts = verify_page(client, entry_id, plan)
    summary.update(
        {
            "entry_id": entry_id,
            "page_url": (
                f"https://lexiangla.com/pages/{entry_id}"
                f"?company_from={credential.company_from}"
            ),
            "remote_images": remote_images,
            "remote_callouts": remote_callouts,
            "verified": True,
            "company_from": credential.company_from,
        }
    )
    print(json.dumps(summary, ensure_ascii=False) if args.json else summary["page_url"])
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", action="store_true")
    subparsers = parser.add_subparsers(dest="command")
    auth = subparsers.add_parser("auth", help="管理乐享个人凭证")
    auth_subparsers = auth.add_subparsers(dest="auth_command", required=True)
    login = auth_subparsers.add_parser("login")
    login.add_argument(
        "--file",
        help="从页面导出的文件读取凭证内容（不是凭证保存路径）",
    )
    add_credential_selector_arguments(login)
    status = auth_subparsers.add_parser("status")
    status.add_argument("--check", action="store_true")
    add_credential_selector_arguments(status)
    logout = auth_subparsers.add_parser("logout")
    add_credential_selector_arguments(logout)
    upload_parser = subparsers.add_parser("upload", help="上传 Markdown")
    add_upload_arguments(upload_parser)
    return parser


def add_upload_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("md_path", nargs="?")
    parser.add_argument("--work-dir")
    parser.add_argument("--md", dest="md_name")
    parser.add_argument("--entry-id")
    parser.add_argument("--parent-id")
    parser.add_argument("--name")
    parser.add_argument("--name-suffix", default="")
    parser.add_argument("--pin", action="store_true")
    parser.add_argument("--source-url", default="")
    parser.add_argument("--source-title", default="")
    parser.add_argument("--meta-file")
    parser.add_argument("--source-from-meta", action="store_true")
    parser.add_argument("--parent-from-meta", action="store_true")
    parser.add_argument(
        "--formula-mode",
        choices=("unicode", "image", "native", "hybrid"),
        default="unicode",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true")
    add_credential_selector_arguments(parser)


def add_credential_selector_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--profile",
        metavar="NAME",
        help="使用命名凭证 profile；default 对应旧 credentials.json",
    )
    parser.add_argument(
        "--credential-file",
        metavar="PATH",
        help="使用指定凭证文件；优先级高于 --profile",
    )


def main() -> int:
    # Backward-friendly convenience: a Markdown path implies the upload subcommand.
    arguments = sys.argv[1:]
    if arguments and arguments[0] not in {"auth", "upload", "-h", "--help", "--version"}:
        arguments = ["upload", *arguments]
    parser = build_parser()
    args = parser.parse_args(arguments)
    if args.version:
        print(json.dumps({"name": "upload-markdown-to-lexiang", "version": VERSION, "cli_api": CLI_API}))
        return 0
    try:
        if args.command == "auth":
            selector = resolve_credential_selector(
                getattr(args, "profile", None),
                getattr(args, "credential_file", None),
            )
            if args.auth_command == "login":
                return auth_login(args.file, selector)
            if args.auth_command == "status":
                return auth_status(args.check, selector)
            return auth_logout(selector)
        if args.command == "upload":
            return upload(args)
        parser.print_help()
        return 0
    except AuthError as error:
        print(f"AUTH_ERROR: {error}", file=sys.stderr)
        return 3
    except PreflightError as error:
        print(f"PREFLIGHT_ERROR: {error}", file=sys.stderr)
        return 2
    except VerificationError as error:
        print(f"VERIFY_ERROR: {error}", file=sys.stderr)
        return 5
    except (MCPError, OSError, urllib.error.URLError) as error:
        print(f"UPLOAD_ERROR: {error}", file=sys.stderr)
        return 4


if __name__ == "__main__":
    raise SystemExit(main())
