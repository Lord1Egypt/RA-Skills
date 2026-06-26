"""TikHub HTTP client — stdlib urllib only, no external deps.

设计原则：
- UA 像 curl（Cloudflare 拦截 Python-urllib，但拒绝未知自定义 UA）
- 不强 raise，让调用者决定怎么处理失败
- token 多源解析：env > XDG config > 项目 .env
- 所有路径通过 helper 函数解析，避免硬编码
"""

from __future__ import annotations
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

# 模拟 curl 默认 UA，绕过 Cloudflare 1010 拦截。
# 可通过 TIKHUB_USER_AGENT 环境变量覆盖（如 Cloudflare 升级了规则）。
DEFAULT_USER_AGENT = "curl/8.7.1"


def _xdg_config_dir() -> Path:
    """返回 XDG 标准配置目录下的 content-engine 子目录路径（不创建）。"""
    base = Path(os.environ.get("XDG_CONFIG_HOME") or (Path.home() / ".config"))
    return base / "content-engine"


def _skill_root_dir() -> Path:
    """返回 skill 包根目录路径（content-engine/）。"""
    return Path(__file__).resolve().parent.parent.parent


# Token 自动查找路径（按优先级，第一个找到即用）
_TOKEN_SEARCH_PATHS = [
    lambda: Path.cwd() / ".env",                # 1. 当前工作目录
    lambda: _xdg_config_dir() / ".env",         # 2. XDG 标准位置
    lambda: _skill_root_dir() / ".env",         # 3. Skill 根目录
]


def _help_message() -> str:
    """无 token 时的友好错误。"""
    config_dir = _xdg_config_dir()
    return (
        "TIKHUB_API_TOKEN 未配置。三种方法任选其一：\n\n"
        "  1) 环境变量（推荐临时使用）：\n"
        "     export TIKHUB_API_TOKEN='你的_token'\n\n"
        f"  2) 写入配置文件（推荐长期使用）：\n"
        f"     mkdir -p {config_dir}\n"
        f"     echo 'TIKHUB_API_TOKEN=你的_token' > {config_dir}/.env\n\n"
        "  3) 在当前工作目录放一个 .env 文件，含一行：\n"
        "     TIKHUB_API_TOKEN=你的_token\n\n"
        "TikHub API 是付费第三方服务，注册地址：https://tikhub.io"
    )


class TikhubError(RuntimeError):
    """TikHub API 错误（非 200 / 解析失败）。"""

    def __init__(self, message: str, status: int | None = None, body: str = ""):
        super().__init__(message)
        self.status = status
        self.body = body


class TikhubClient:
    """同步 TikHub 客户端。

    Usage:
        client = TikhubClient()  # token 自动从 env / 配置文件读
        raw = client.fetch_note(note_id)
    """

    BASE_URL = "https://api.tikhub.io"
    DEFAULT_TIMEOUT = 30

    # XHS 评论端点候选（按文档顺序，第一个返回 200 就用）
    XHS_COMMENT_ENDPOINTS = (
        "/api/v1/xiaohongshu/app/get_note_comments",
        "/api/v1/xiaohongshu/web/get_note_comments",
    )

    def __init__(
        self,
        token: str | None = None,
        base_url: str | None = None,
        timeout: int = DEFAULT_TIMEOUT,
        user_agent: str | None = None,
    ):
        self.token = token or self._load_token()
        if not self.token:
            raise TikhubError(_help_message())
        # 国内镜像支持：TIKHUB_BASE_URL 优先
        self.base_url = (base_url or os.environ.get("TIKHUB_BASE_URL") or self.BASE_URL).rstrip("/")
        self.timeout = timeout
        # UA 可覆盖（应对 Cloudflare 规则升级）
        self.user_agent = user_agent or os.environ.get("TIKHUB_USER_AGENT") or DEFAULT_USER_AGENT

    @staticmethod
    def _load_token() -> str | None:
        """按优先级解析 token：env > 多个 .env 路径。"""
        if env_tok := os.environ.get("TIKHUB_API_TOKEN"):
            return env_tok.strip()

        for path_fn in _TOKEN_SEARCH_PATHS:
            try:
                path = path_fn()
            except Exception:
                continue
            if not path.exists() or not path.is_file():
                continue
            try:
                for line in path.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if line.startswith("TIKHUB_API_TOKEN="):
                        val = line.split("=", 1)[1].strip()
                        return val.strip('"').strip("'")
            except (OSError, UnicodeDecodeError):
                continue
        return None

    @classmethod
    def token_search_paths(cls) -> list[Path]:
        """对外暴露用于诊断/preflight 显示。"""
        out = []
        for fn in _TOKEN_SEARCH_PATHS:
            try:
                out.append(fn())
            except Exception:
                continue
        return out

    def _get(self, path: str, params: dict[str, str]) -> dict:
        """同步 GET，返回解析后的 JSON dict。失败 raise TikhubError。"""
        url = f"{self.base_url}{path}?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {self.token}",
                "User-Agent": self.user_agent,
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                body = resp.read().decode("utf-8")
                return json.loads(body)
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")[:500]
            raise TikhubError(
                f"HTTP {e.code} from {path}: {err_body}",
                status=e.code,
                body=err_body,
            ) from e
        except urllib.error.URLError as e:
            raise TikhubError(f"Network error for {path}: {e.reason}") from e
        except json.JSONDecodeError as e:
            raise TikhubError(f"Invalid JSON from {path}: {e}") from e

    def fetch_note(self, note_id: str) -> dict:
        """拉取笔记元数据（原始 API 响应）。"""
        return self._get(
            "/api/v1/xiaohongshu/app/get_note_info",
            {"note_id": note_id},
        )

    def fetch_comments(self, note_id: str) -> dict:
        """拉取评论。按候选端点顺序 try，第一个 200 即用。

        全部失败时累积所有 endpoint 的错误信息一起 raise，方便诊断。
        """
        errors: list[str] = []
        for path in self.XHS_COMMENT_ENDPOINTS:
            try:
                return self._get(path, {"note_id": note_id})
            except TikhubError as e:
                errors.append(f"  - {path}: {e}")
                continue
        # 全失败 → 一次性给出所有 endpoint 的状态
        joined = "\n".join(errors)
        raise TikhubError(
            f"All {len(self.XHS_COMMENT_ENDPOINTS)} comment endpoints failed:\n{joined}",
            status=None,
        )
