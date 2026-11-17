#!/usr/bin/env python3
"""Shared trust boundary for untrusted SVG input, plus the single funnel for
every external process this skill starts.

Every script in this skill that renders repository-supplied SVG (visual_verify.py,
render_motion_gif.py) must run the same checks before handing a file to a
renderer. This module is the single source of truth for those checks so the two
render paths cannot drift apart again.

Trust model
-----------
A README (and every asset it references) is **untrusted data**. It may be
written by a third party and may embed instructions, external resource
references, or parser-stressing content. Static checks are therefore
fail-closed: anything that could make a renderer talk to the network, reach
outside the isolated render directory, or execute code is refused, and the
script reports the reason instead of rendering.

External processes
------------------
`run_external()` is the only place in this skill that spawns a child process.
Callers pass a pre-validated argument list (never a shell string), and it
enforces `shell=False`, a hard timeout, and a bounded error report — so a
malformed asset cannot hang the run, and there is exactly one code path to
audit for process launching.

Checks
------
1. XML well-formedness (unparseable input is refused).
2. No executable / embedding elements: <script>, <foreignObject>, <iframe>,
   <object>, <embed>, <audio>, <video>, <canvas>.
3. No remote fonts or stylesheets (@font-face, Google Fonts, <link rel=stylesheet>).
4. Every resource-bearing reference (href / xlink:href / src, and CSS `url(...)`)
   must be local: a `#fragment` or a `data:` URI. Remote URLs, protocol-relative
   URLs, root-absolute paths, Windows-drive paths and parent-directory traversal
   are refused. Plain sibling-relative references are permitted but unresolvable
   — they resolve to the throwaway preview origin, which serves exactly one file.
5. No CSS `@import` (always an out-of-band fetch).
6. No event-handler attributes (`onload`, `onclick`, …) and no SMIL animation
   that installs one (`<set attributeName="onload" …>`): a renderer that honours
   them would execute script inside the preview origin.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

# Elements that can execute code, embed foreign content, or pull in a document.
UNSAFE_SVG_TAGS = {
    "script",
    "foreignObject",
    "iframe",
    "object",
    "embed",
    "audio",
    "video",
    "canvas",
}

# Remote fonts / stylesheets: GitHub strips them anyway, and they are an
# out-of-band network fetch when rendered locally.
REMOTE_FONT = r"@font-face|fonts\.(googleapis|gstatic)\.com|<link\b[^>]*stylesheet"

# Attributes that carry a resource reference.
REF_ATTRS = {"href", "src"}

# href/src values that leave the single-file preview origin. `data:` URIs and
# `#fragment` references are intentionally NOT matched here.
DANGEROUS_REF = (
    r"""(?:(?:xlink:)?href|src)\s*=\s*["']\s*(?:(?:https?|file|ftp|javascript|vbscript|blob):|//|/|[A-Za-z]:[\\/]|\.\./)"""
)

# One target inside a CSS url(...) token, e.g. url(#grad) or url("hero.png").
URL_TOKEN = r"""url\(\s*(['"]?)([^'")]*)\1\s*\)"""

# A target that leaves the preview origin (schemes, protocol-relative,
# root-absolute, drive letters, parent-directory traversal).
EXTERNAL_TARGET = r"""(?i)^(?:(?:https?|file|ftp|javascript|vbscript|blob):|//|/|[A-Za-z]:[\\/])|(?:^|[\\/])\.\.(?:[\\/]|$)"""

# Any @import at all — it is always an out-of-band fetch.
IMPORT_RULE = r"@import\b"

# Event-handler attributes (onload, onclick, onerror, …). SVG has no standard
# non-event attribute with an `on` prefix, so anything matching this is refused.
EVENT_HANDLER_ATTR = re.compile(r"^on[a-z]", re.I)

# SMIL animation elements that can install an attribute on another element.
SMIL_ELEMENTS = {"set", "animate", "animateTransform", "animateMotion"}


def _local_tag(tag: str) -> str:
    """Return the local name of a possibly namespaced tag."""
    return tag.rsplit("}", 1)[-1]


def safety_issues(path: Path) -> list[str]:
    """Return the list of blocking trust-boundary violations for `path`.

    An empty list means the file is safe to hand to a renderer. The first item
    is a short machine-friendly reason, suitable for a SKIPPED/FAILED line.
    """
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        return [f"invalid SVG XML: {exc}"]
    except OSError as exc:
        return [f"unreadable SVG: {exc}"]

    issues: list[str] = []

    for node in root.iter():
        tag = _local_tag(node.tag)
        if tag in UNSAFE_SVG_TAGS:
            issues.append(f"contains <{tag}>")
        if tag in SMIL_ELEMENTS:
            target_attr = ""
            for key, val in node.attrib.items():
                if _local_tag(key).lower() == "attributename":
                    target_attr = str(val).strip()
                    break
            if target_attr and EVENT_HANDLER_ATTR.match(target_attr):
                issues.append(f"SMIL animation installs event handler: {target_attr}")
        for name, value in node.attrib.items():
            if not isinstance(value, str) or not value.strip():
                continue
            local = _local_tag(name).lower()
            if EVENT_HANDLER_ATTR.match(local):
                issues.append(f"event-handler attribute {_local_tag(name)}")
            if local in REF_ATTRS:
                if re.match(EXTERNAL_TARGET, value.strip()):
                    issues.append(
                        f"external/absolute reference in {_local_tag(name)}: {value.strip()[:60]}"
                    )
            if "url(" in value.lower():
                for _, target in re.findall(URL_TOKEN, value, re.I):
                    target = target.strip()
                    if target == "" or target.startswith("#"):
                        continue
                    if re.match(EXTERNAL_TARGET, target):
                        issues.append(f"external resource in url(): {target[:60]}")
            if IMPORT_RULE in value or re.search(IMPORT_RULE, value, re.I):
                issues.append("CSS @import (out-of-band stylesheet fetch)")

    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return [f"unreadable SVG: {exc}"]

    if re.search(REMOTE_FONT, text, re.I):
        issues.append("remote font or stylesheet reference")
    if re.search(IMPORT_RULE, text, re.I):
        issues.append("CSS @import (out-of-band stylesheet fetch)")
    if re.search(DANGEROUS_REF, text, re.I):
        issues.append(
            "external/absolute reference detected (http, file, //, /, drive, or ../)"
        )
    # CSS `url(...)` tokens also appear in stylesheet *text* (inside <style> or
    # CDATA), not only in attributes — so scan the raw document as well.
    for _, target in re.findall(URL_TOKEN, text, re.I):
        target = target.strip()
        if target == "" or target.startswith("#"):
            continue
        if re.match(EXTERNAL_TARGET, target):
            issues.append(f"external resource in url(): {target[:60]}")

    # De-duplicate while keeping order.
    seen: set[str] = set()
    ordered: list[str] = []
    for issue in issues:
        if issue not in seen:
            seen.add(issue)
            ordered.append(issue)
    return ordered


def is_safe_to_render(path: Path) -> tuple[bool, str]:
    """Gate before rendering. Returns (safe, reason).

    Structural quality problems (missing viewBox/title/desc) do not block
    rendering; only trust-boundary violations do.
    """
    issues = safety_issues(path)
    if issues:
        return False, "; ".join(issues[:3])
    return True, ""


def assert_safe_to_render(path: Path) -> None:
    """Raise SystemExit with a clear message when `path` must not be rendered."""
    safe, reason = is_safe_to_render(path)
    if not safe:
        raise SystemExit(
            f"ERROR: refusing to render {path.name}: {reason}\n"
            "       Untrusted SVG input must be local-only (data: URIs or "
            "#fragment references); reauthor the asset without remote or "
            "external references."
        )


ALLOWED_STEMS = {
    # 浏览器
    "chrome", "chromeheadlessshell", "chromium", "chromiumbrowser",
    "googlechrome", "googlechromestable", "msedge", "microsoftedge",
    "microsoftedge", "edge",
    # 渲染 / 编码工具
    "ffmpeg", "rsvgconvert", "sips",
}

# 允许的安装根 —— **绝对目录**，判定方式是「解析后的真实路径是否位于该目录之下」
# （Path 包含关系），不是字符串里出现过某个片段。写具体子目录而非整个用户目录：
# 否则被审计仓库里放一个 `chrome.exe` 就能冒充。
ALLOWED_ROOTS = (
    # Windows：Program Files 下的浏览器 / 包管理器
    r"C:\Program Files\Google\Chrome",
    r"C:\Program Files (x86)\Google\Chrome",
    r"C:\Program Files\Microsoft\Edge",
    r"C:\Program Files (x86)\Microsoft\Edge",
    r"C:\Program Files\Chromium",
    r"C:\ProgramData\chocolatey",
    # Windows：用户级安装（仅这几个具体子目录）
    r"%LOCALAPPDATA%\Google\Chrome",
    r"%LOCALAPPDATA%\Microsoft\Edge",
    r"%LOCALAPPDATA%\Chromium",
    r"%USERPROFILE%\scoop\apps",
    # macOS / Linux
    "/Applications/Google Chrome.app",
    "/Applications/Microsoft Edge.app",
    "/Applications/Chromium.app",
    "/usr/bin",
    "/usr/local/bin",
    "/opt/google",
    "/snap/chromium",
    "/snap/bin",
    "/nix/store",
)


def _expand_root(raw: str) -> Path:
    """把安装根展开成绝对路径（支持 %LOCALAPPDATA% 这类占位）。"""
    expanded = os.path.expandvars(os.path.expanduser(raw))
    try:
        return Path(expanded).resolve()
    except OSError:
        return Path(expanded).absolute()


def _under_allowed_root(real: Path) -> bool:
    """真实路径是否**确实位于**某个已知安装目录之下。

    用路径包含关系（`root` 是 `real` 的祖先目录）而不是子串匹配：
    子串匹配会把 `/tmp/repo/opt/chrome` 当成落在 `/opt/` 下——那正是
    "仓库里的同名可执行文件冒充已安装工具" 的入口。
    """
    try:
        real = real.resolve()
    except OSError:
        return False
    for raw in ALLOWED_ROOTS:
        root = _expand_root(raw)
        if real == root or root in real.parents:
            return True
    return False


def _normalized_stem(name: str) -> str:
    stem = name.lower().replace(" ", "").replace("_", "").replace("-", "")
    for suffix in (".exe", ".cmd", ".bat"):
        if stem.endswith(suffix):
            return stem[: -len(suffix)]
    return stem


def _is_allowed_binary(exe: str) -> bool:
    """True only for a renderer/encoder this skill is allowed to launch.

    Checks **identity, not just the name**:
      1. 裸命令名先在白名单内解析成绝对路径（`shutil.which`），否则拒绝；
      2. 必须是存在的普通文件；
      3. 解析后的 **真实路径** 必须落在已知安装根下（防符号链接绕道）；
      4. 归一化后的可执行名必须在白名单内。
    仅在旁边放一个叫 `chrome.exe` 的文件不会被放行 —— 这正是要害：被审计的
    仓库不能替换掉真正要执行的程序。
    """
    if not isinstance(exe, str) or not exe.strip():
        return False
    exe = exe.strip()
    if not os.path.dirname(exe):                      # 裸名：只在白名单内解析
        if _normalized_stem(exe) not in ALLOWED_STEMS:
            return False
        exe = shutil.which(exe) or ""
        if not exe:
            return False
    try:
        p = Path(exe)
    except (TypeError, ValueError):
        return False
    if not p.is_absolute():
        return False
    try:
        real = p.resolve(strict=True)
    except (OSError, RuntimeError):
        return False
    if not real.is_file():
        return False
    if _normalized_stem(real.name) not in ALLOWED_STEMS:
        return False
    return _under_allowed_root(real)


def _validate_argv(command, label: str) -> list[str]:
    """把调用方的参数列表校验成一份**可安全启动**的 argv。

    每个参数都必须是字符串、非空、不含 NUL / 换行（这两类字符在跨平台进程
    边界上语义最不可控），并有长度上限。任何一项不合格就整体拒绝，不做
    "过滤后继续"——静默改写参数会让调用方以为执行了另一条命令。
    配合 `shell=False` 与显式参数列表，杜绝命令注入与元字符展开。
    """
    if not isinstance(command, (list, tuple)) or not command:
        raise SystemExit(f"ERROR: {label}: invalid argument list")
    argv: list[str] = []
    for part in command:
        if not isinstance(part, str):
            raise SystemExit(f"ERROR: {label}: non-string argument {part!r}")
        if not part:
            raise SystemExit(f"ERROR: {label}: empty argument")
        if "\x00" in part or "\n" in part or "\r" in part:
            raise SystemExit(f"ERROR: {label}: argument contains control characters")
        if len(part) > 4096:
            raise SystemExit(f"ERROR: {label}: argument too long ({len(part)} chars)")
        argv.append(part)
    return argv


def run_external(
    command: list[str],
    *,
    timeout: int,
    label: str,
    check: bool = True,
) -> subprocess.CompletedProcess:
    """Run one external tool. The only process-launching path in this skill.

    The caller supplies an explicit argument list built from locally validated
    values — never a shell string — and it is passed to subprocess with
    `shell=False`, so no shell interpretation, globbing, or metacharacter
    expansion can occur. A hard timeout bounds every run, so malformed or
    computationally expensive input cannot hang the skill. Errors carry the
    tool label and a truncated stderr instead of an opaque traceback.

    Raises SystemExit when the tool is missing, times out, or exits non-zero
    (with check=True).
    """
    argv = _validate_argv(command, label)
    # Only known binaries may be launched. The executable path comes from local
    # browser discovery (or an absolute path the user pointed at), never from
    # document/README content, so a repository under review cannot introduce a
    # different program here.
    if not _is_allowed_binary(argv[0]):
        raise SystemExit(
            f"ERROR: {label}: refusing to launch unrecognised executable "
            f"{Path(argv[0]).name!r} — only Chrome/Edge/Chromium/ffmpeg are permitted"
        )

    try:
        return subprocess.run(
            argv,
            check=check,
            shell=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
    except FileNotFoundError:
        raise SystemExit(f"ERROR: {label}: executable not found: {command[0]}") from None
    except subprocess.TimeoutExpired:
        raise SystemExit(f"ERROR: {label}: timed out after {timeout}s") from None
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or "").strip()[:400]
        raise SystemExit(f"ERROR: {label}: exited {exc.returncode}. {detail}") from None
