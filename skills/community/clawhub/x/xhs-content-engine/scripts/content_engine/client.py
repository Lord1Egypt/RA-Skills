"""agent.delu.cn crawler HTTP client — stdlib urllib only, no external deps.

设计原则：
- 默认走 https://agent.delu.cn 的爬虫接口
- 不把具体接口细节写死：base URL、endpoint path、认证 header、请求方法都可用 env 覆盖
- token 多源解析：env > XDG config > 项目 .env
- 无 token 时允许无认证请求，兼容内网 / IP allowlist 场景
"""

from __future__ import annotations
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

# 可通过 AGENT_DELU_USER_AGENT 环境变量覆盖。
DEFAULT_USER_AGENT = "curl/8.7.1"
DEFAULT_BASE_URL = "https://agent.delu.cn"
DEFAULT_NOTE_PATH = "/api/v1/xiaohongshu/app/get_note_info"
DEFAULT_COMMENT_PATHS = (
    "/api/v1/xiaohongshu/app/get_note_comments",
    "/api/v1/xiaohongshu/web/get_note_comments",
)


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


def _env_file_value(keys: tuple[str, ...]) -> str | None:
    """按优先级从 env / .env 文件读取第一个命中的配置值。"""
    for key in keys:
        if value := os.environ.get(key):
            return value.strip()

    for path_fn in _TOKEN_SEARCH_PATHS:
        try:
            env_path = path_fn()
        except Exception:
            continue
        if not env_path.exists() or not env_path.is_file():
            continue
        try:
            for raw_line in env_path.read_text(encoding="utf-8").splitlines():
                line = raw_line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                if key.strip() in keys:
                    return value.strip().strip('"').strip("'")
        except (OSError, UnicodeDecodeError):
            continue
    return None


def _split_paths(value: str | None, fallback: tuple[str, ...]) -> tuple[str, ...]:
    if not value:
        return fallback
    paths = tuple(part.strip() for part in value.split(",") if part.strip())
    return paths or fallback


def _help_message() -> str:
    """agent.delu.cn 爬虫接口配置说明。"""
    config_dir = _xdg_config_dir()
    return (
        "agent.delu.cn 爬虫接口配置：\n\n"
        "  1) 默认接口地址：\n"
        "     AGENT_DELU_BASE_URL=https://agent.delu.cn\n\n"
        "  2) 如接口需要 token，任选其一配置：\n"
        "     export AGENT_DELU_API_TOKEN='你的_token'\n\n"
        f"  3) 或写入配置文件（推荐长期使用）：\n"
        f"     mkdir -p {config_dir}\n"
        f"     echo 'AGENT_DELU_API_TOKEN=你的_token' > {config_dir}/.env\n\n"
        "  4) 如路径不同，可覆盖：\n"
        "     AGENT_DELU_NOTE_PATH=/api/v1/xiaohongshu/app/get_note_info\n"
        "     AGENT_DELU_COMMENT_PATHS=/api/v1/xiaohongshu/app/get_note_comments,/api/v1/xiaohongshu/web/get_note_comments\n"
        "     AGENT_DELU_NOTE_ID_PARAM=note_id"
    )


class DeluCrawlerError(RuntimeError):
    """agent.delu.cn crawler API 错误（非 200 / 解析失败）。"""

    def __init__(self, message: str, status: int | None = None, body: str = ""):
        super().__init__(message)
        self.status = status
        self.body = body


class DeluCrawlerClient:
    """同步 agent.delu.cn 爬虫客户端。

    Usage:
        client = DeluCrawlerClient()  # token 自动从 env / 配置文件读
        raw = client.fetch_note(note_id)
    """

    BASE_URL = DEFAULT_BASE_URL
    DEFAULT_TIMEOUT = 30

    # XHS 评论端点候选（第一个返回 200 就用）
    XHS_COMMENT_ENDPOINTS = DEFAULT_COMMENT_PATHS

    def __init__(
        self,
        token: str | None = None,
        base_url: str | None = None,
        timeout: int = DEFAULT_TIMEOUT,
        user_agent: str | None = None,
    ):
        self.token = token if token is not None else self._load_token()
        self.base_url = (
            base_url
            or _env_file_value(("AGENT_DELU_BASE_URL",))
            or self.BASE_URL
        ).rstrip("/")
        self.timeout = timeout
        self.user_agent = (
            user_agent
            or _env_file_value(("AGENT_DELU_USER_AGENT",))
            or DEFAULT_USER_AGENT
        )
        self.auth_header = _env_file_value(("AGENT_DELU_AUTH_HEADER",)) or "Authorization"
        self.auth_scheme = _env_file_value(("AGENT_DELU_AUTH_SCHEME",)) or "Bearer"
        self.note_path = _env_file_value(("AGENT_DELU_NOTE_PATH",)) or DEFAULT_NOTE_PATH
        self.comment_paths = _split_paths(
            _env_file_value(("AGENT_DELU_COMMENT_PATHS",)),
            self.XHS_COMMENT_ENDPOINTS,
        )
        self.note_id_param = _env_file_value(("AGENT_DELU_NOTE_ID_PARAM",)) or "note_id"
        self.note_method = (_env_file_value(("AGENT_DELU_NOTE_METHOD", "AGENT_DELU_METHOD")) or "GET").upper()
        self.comment_method = (
            _env_file_value(("AGENT_DELU_COMMENT_METHOD", "AGENT_DELU_METHOD")) or "GET"
        ).upper()

    @staticmethod
    def _load_token() -> str | None:
        """按优先级解析 token：env > 多个 .env 路径。"""
        return _env_file_value(("AGENT_DELU_API_TOKEN", "AGENT_DELU_TOKEN"))

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

    @classmethod
    def configured_base_url(cls) -> str:
        return (_env_file_value(("AGENT_DELU_BASE_URL",)) or cls.BASE_URL).rstrip("/")

    def _headers(self) -> dict[str, str]:
        headers = {
            "Accept": "application/json",
            "User-Agent": self.user_agent,
        }
        if self.token:
            scheme = self.auth_scheme.strip()
            value = self.token if not scheme or scheme.lower() == "raw" else f"{scheme} {self.token}"
            headers[self.auth_header] = value
        return headers

    def _url_for(self, endpoint_path: str, params: dict[str, str], method: str) -> str:
        if endpoint_path.startswith(("http://", "https://")):
            base = endpoint_path
        else:
            base = f"{self.base_url}{endpoint_path}"
        if method == "GET":
            return base + "?" + urllib.parse.urlencode(params)
        return base

    def _request(self, endpoint_path: str, params: dict[str, str], method: str = "GET") -> dict:
        """同步请求，返回解析后的 JSON dict。失败 raise DeluCrawlerError。"""
        method = method.upper()
        if method not in ("GET", "POST"):
            raise DeluCrawlerError(f"Unsupported AGENT_DELU request method: {method}")

        url = self._url_for(endpoint_path, params, method)
        headers = self._headers()
        data = None
        if method == "POST":
            headers["Content-Type"] = "application/json"
            data = json.dumps(params).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers=headers,
            method=method,
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                body = resp.read().decode("utf-8")
                return json.loads(body)
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")[:500]
            raise DeluCrawlerError(
                f"HTTP {e.code} from {endpoint_path}: {err_body}",
                status=e.code,
                body=err_body,
            ) from e
        except urllib.error.URLError as e:
            raise DeluCrawlerError(f"Network error for {endpoint_path}: {e.reason}") from e
        except json.JSONDecodeError as e:
            raise DeluCrawlerError(f"Invalid JSON from {endpoint_path}: {e}") from e

    def fetch_note(self, note_id: str) -> dict:
        """拉取笔记元数据（原始 API 响应）。"""
        return self._request(self.note_path, {self.note_id_param: note_id}, self.note_method)

    def fetch_comments(self, note_id: str) -> dict:
        """拉取评论。按候选端点顺序 try，第一个 200 即用。

        全部失败时累积所有 endpoint 的错误信息一起 raise，方便诊断。
        """
        errors: list[str] = []
        for endpoint_path in self.comment_paths:
            try:
                return self._request(
                    endpoint_path,
                    {self.note_id_param: note_id},
                    self.comment_method,
                )
            except DeluCrawlerError as e:
                errors.append(f"  - {endpoint_path}: {e}")
                continue
        # 全失败 → 一次性给出所有 endpoint 的状态
        joined = "\n".join(errors)
        raise DeluCrawlerError(
            f"All {len(self.comment_paths)} comment endpoints failed:\n{joined}",
            status=None,
        )
