"""环境自检 — 让公开发布的 skill 用户能一眼看到缺什么。

检查项：
1. Python 版本（≥ 3.10）
2. ffmpeg 是否在 PATH（视频抽帧必需）
3. TIKHUB_API_TOKEN 是否可解析
4. 网络：tikhub.io API + xhscdn.com CDN（图片/视频走 CDN）
5. 工作区可写

每项 Check 有 ok / fatal / 安装提示三个属性。fatal=True 的不通过会阻断 extract_xhs.py 主流程。
"""

from __future__ import annotations
import platform
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

from .client import TikhubClient
from .llm import ofox_credentials_present


@dataclass
class Check:
    name: str
    ok: bool
    fatal: bool          # 不通过是否阻断 extract_xhs.py
    message: str         # 一句话状态
    fix: str = ""        # 怎么修（多行字符串）
    detail: list[str] = field(default_factory=list)  # 额外诊断信息


# ---------------- 各检查项 ----------------

def check_python_version() -> Check:
    v = sys.version_info
    ok = v >= (3, 10)
    return Check(
        name="Python 版本",
        ok=ok,
        fatal=True,
        message=f"{v.major}.{v.minor}.{v.micro} ({'OK' if ok else '需要 3.10+'})",
        fix=(
            "macOS:   brew install python@3.12\n"
            "Linux:   sudo apt install python3.12  (或 pyenv install 3.12)\n"
            "Windows: 从 https://python.org 下载安装"
        ) if not ok else "",
    )


def check_ffmpeg() -> Check:
    path = shutil.which("ffmpeg")
    if not path:
        return Check(
            name="ffmpeg",
            ok=False,
            fatal=True,  # 视频拆解必需
            message="未找到（视频笔记拆解必需，图文笔记可选）",
            fix=(
                "macOS:   brew install ffmpeg\n"
                "Linux:   sudo apt install ffmpeg  (或 dnf / pacman 对应命令)\n"
                "Windows: choco install ffmpeg  (或从 ffmpeg.org 下载)"
            ),
        )
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        version_line = (result.stdout.splitlines() or [""])[0]
    except (subprocess.SubprocessError, OSError):
        version_line = "?"
    return Check(
        name="ffmpeg",
        ok=True,
        fatal=True,
        message=f"OK ({version_line})",
        detail=[f"path: {path}"],
    )


def check_tikhub_token() -> Check:
    token = TikhubClient._load_token()
    if not token:
        from .client import _help_message
        searched = "\n  ".join(str(p) for p in TikhubClient.token_search_paths())
        return Check(
            name="TIKHUB_API_TOKEN",
            ok=False,
            fatal=True,
            message="未配置（API 调用必需）",
            fix=_help_message(),
            detail=[f"已查找的路径：\n  {searched}"],
        )
    masked = token[:6] + "..." + token[-4:] if len(token) > 12 else "****"
    return Check(
        name="TIKHUB_API_TOKEN",
        ok=True,
        fatal=True,
        message=f"OK ({masked})",
    )


def _http_ping(url: str, timeout: int = 10) -> tuple[bool, str]:
    """返回 (ok, message)。任何 HTTP 响应都算"通"，只有连不通才算 fail。"""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "curl/8.7.1"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status < 500, f"HTTP {resp.status}"
    except urllib.error.HTTPError as e:
        # 拿到响应就说明网络通
        return e.code < 500, f"HTTP {e.code}"
    except (urllib.error.URLError, OSError) as e:
        return False, str(e)


def check_network_tikhub() -> Check:
    """测试 TikHub API 域名是否可达。"""
    ok, msg = _http_ping("https://api.tikhub.io/")
    return Check(
        name="网络 → api.tikhub.io",
        ok=ok,
        fatal=False,
        message=f"OK ({msg})" if ok else f"无法访问：{msg}",
        fix=(
            "如果你在中国大陆，需要配置代理；\n"
            "或在 .env 设置 TIKHUB_BASE_URL=https://api.tikhub.dev 用国内镜像"
        ) if not ok else "",
    )


def check_network_xhs_cdn() -> Check:
    """测试 XHS CDN 域名是否可达（视频/图片下载用）。

    XHS CDN 与 TikHub 是不同 host，可能代理覆盖不全。
    """
    # 用 sns-img-bd.xhscdn.com 探测（图文笔记图片域名）
    ok, msg = _http_ping("https://sns-img-bd.xhscdn.com/")
    return Check(
        name="网络 → xhscdn.com CDN",
        ok=ok,
        fatal=False,
        message=f"OK ({msg})" if ok else f"CDN 不通：{msg}",
        fix=(
            "图片和视频从 xhscdn.com 下载，独立于 TikHub API。\n"
            "如果在墙内，确认你的代理覆盖了 *.xhscdn.com 域名。"
        ) if not ok else "",
    )


def check_ofox_credentials() -> Check:
    """Ofox API key（v2 generate mode 用）— 非阻断，v1 拆解 mode 不需要。"""
    if ofox_credentials_present():
        from .llm import _load_ofox_key
        token = _load_ofox_key() or ""
        masked = token[:6] + "..." + token[-4:] if len(token) > 12 else "****"
        return Check(
            name="OFOX_API_KEY (v2 generate)",
            ok=True,
            fatal=False,
            message=f"OK ({masked})",
        )
    return Check(
        name="OFOX_API_KEY (v2 generate)",
        ok=False,
        fatal=False,  # 不阻断 v1 拆解
        message="未配置（v1 拆解 mode 不需要；v2 generate mode 必需）",
        fix=(
            "v2 生成模式需要 Ofox API key（聚合 LLM + Nano Banana 出图）：\n"
            "  1) 注册：https://ofox.ai\n"
            "  2) 在 .env 加：OFOX_API_KEY=ofox-...\n"
            "  3) 兼容：OPENROUTER_API_KEY 也会被识别"
        ),
    )


def check_ark_credentials() -> Check:
    """火山方舟 API key（v0.3.0+ 真生视频用）— 非阻断，--no-real-video 可绕开。"""
    from .seedance import ark_credentials_present, _load_ark_key
    if ark_credentials_present():
        token = _load_ark_key() or ""
        masked = token[:6] + "..." + token[-4:] if len(token) > 12 else "****"
        return Check(
            name="ARK_API_KEY (v0.3.0+ 视频)",
            ok=True,
            fatal=False,
            message=f"OK ({masked})",
        )
    return Check(
        name="ARK_API_KEY (v0.3.0+ 视频)",
        ok=False,
        fatal=False,  # 不阻断；--no-real-video 仍可跑
        message="未配置（仅当 --type video 真生视频时需要；--no-real-video 可绕开）",
        fix=(
            "真生视频需要火山方舟 API key（Seedance 2.0）：\n"
            "  1) 注册：https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey\n"
            "  2) ⚠️ 不要用 IAM AK/SK（两者格式都是 UUID 但不通用）\n"
            "  3) 在 .env 加：ARK_API_KEY=...\n"
            "  4) 在「开通管理 → 视觉模型」开通 Doubao-Seedance-2.0-fast"
        ),
    )


def check_workspace_writable(workspace: Path | None = None) -> Check:
    """工作区是否可写。

    Args:
        workspace: 自定义工作区路径（如 --out 参数）。
                   None 时检查默认路径 {tempdir}/content-engine。
    """
    if workspace is None:
        workspace = Path(tempfile.gettempdir()) / "content-engine"
    try:
        workspace.mkdir(parents=True, exist_ok=True)
        test_file = workspace / ".write-test"
        test_file.write_text("ok")
        test_file.unlink()
        return Check(
            name="工作区可写",
            ok=True,
            fatal=True,
            message=f"OK ({workspace})",
        )
    except OSError as e:
        return Check(
            name="工作区可写",
            ok=False,
            fatal=True,
            message=f"无法写入 {workspace}: {e}",
            fix=f"用 --out 指定其他路径，例如 --out ~/xhs-workspace",
        )


# ---------------- 入口 ----------------

def run_all(workspace: Path | None = None) -> list[Check]:
    """跑所有检查，返回结果列表。

    Args:
        workspace: 自定义工作区路径，如有则检查它而非默认 tempdir。
    """
    return [
        check_python_version(),
        check_ffmpeg(),
        check_workspace_writable(workspace),
        check_tikhub_token(),
        check_network_tikhub(),
        check_network_xhs_cdn(),
        check_ofox_credentials(),
        check_ark_credentials(),
    ]


def print_report(checks: list[Check]) -> int:
    """打印人类友好的报告，返回退出码（0=全通过；2=有 fatal 失败）。"""
    print(f"Content Engine 环境检查 · {platform.system()} {platform.machine()}\n")

    has_fatal_fail = False
    for c in checks:
        icon = "✅" if c.ok else ("❌" if c.fatal else "⚠️ ")
        print(f"  {icon}  {c.name}: {c.message}")
        for line in c.detail:
            for sub in line.splitlines():
                print(f"          {sub}")
        if not c.ok and c.fix:
            print(f"\n      ▸ 修复方法：")
            for line in c.fix.splitlines():
                print(f"          {line}")
            print()
        if not c.ok and c.fatal:
            has_fatal_fail = True

    print()
    if has_fatal_fail:
        print("❌ 有阻断性问题未通过，extract_xhs.py 主流程无法运行。请按上面提示修复。")
        return 2
    if any(not c.ok for c in checks):
        print("⚠️  有非阻断警告，但拆解流程可以跑（视具体功能可能受影响）。")
        return 0
    print("✅ 全部通过，可以开始拆解。")
    return 0
