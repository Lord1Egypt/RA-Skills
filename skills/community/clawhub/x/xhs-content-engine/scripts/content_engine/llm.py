"""Ofox LLM client — stdlib urllib, OpenAI-compatible.

Ofox 是聚合网关，支持 Claude / GPT / Gemini 等多家模型，
endpoint 走 OpenAI compat 标准。一个 key 还能用 Nano Banana 出图（见 nano_banana.py）。

设计原则：
- stdlib 不引入 openai SDK
- token 走 v1 同款多源解析（env / cwd .env / XDG / skill 根）
- 重试 1 次 + 友好错误
"""

from __future__ import annotations
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

# 默认值
OFOX_BASE_URL = "https://api.ofox.ai"
DEFAULT_MODEL = "claude-sonnet-4-6"   # 可被 OFOX_LLM_MODEL 覆盖
DEFAULT_TIMEOUT = 120                  # LLM 长 prompt 可能慢


class OfoxError(RuntimeError):
    """Ofox API 错误。"""

    def __init__(self, message: str, status: int | None = None, body: str = ""):
        super().__init__(message)
        self.status = status
        self.body = body


def _xdg_config_dir() -> Path:
    """复用 client.py 的 helper，避免循环依赖单独实现。"""
    base = Path(os.environ.get("XDG_CONFIG_HOME") or (Path.home() / ".config"))
    return base / "content-engine"


def _skill_root_dir() -> Path:
    return Path(__file__).resolve().parent.parent.parent


_TOKEN_SEARCH_PATHS = [
    lambda: Path.cwd() / ".env",
    lambda: _xdg_config_dir() / ".env",
    lambda: _skill_root_dir() / ".env",
]


def _load_ofox_key() -> str | None:
    """env > .env 文件三源。允许 OPENROUTER_API_KEY 作为兼容备选。"""
    for var in ("OFOX_API_KEY", "OPENROUTER_API_KEY"):
        if v := os.environ.get(var):
            return v.strip()
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
                for var in ("OFOX_API_KEY", "OPENROUTER_API_KEY"):
                    if line.startswith(f"{var}="):
                        val = line.split("=", 1)[1].strip()
                        return val.strip('"').strip("'")
        except (OSError, UnicodeDecodeError):
            continue
    return None


def _help_message() -> str:
    config_dir = _xdg_config_dir()
    return (
        "OFOX_API_KEY 未配置。Ofox 是聚合 LLM + 图片生成的网关，注册：https://ofox.ai\n\n"
        "  1) 环境变量：\n"
        "     export OFOX_API_KEY='ofox-...'\n\n"
        f"  2) 配置文件：\n"
        f"     mkdir -p {config_dir}\n"
        f"     echo 'OFOX_API_KEY=ofox-...' > {config_dir}/.env\n\n"
        "  3) 兼容：OPENROUTER_API_KEY 也会被识别"
    )


def ofox_credentials_present() -> bool:
    """preflight 用。"""
    return bool(_load_ofox_key())


class OfoxLLMClient:
    """同步 LLM 客户端。

    Usage:
        llm = OfoxLLMClient()
        text = llm.chat([
            {"role": "system", "content": "你是..."},
            {"role": "user", "content": "..."},
        ])
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        self.api_key = api_key or _load_ofox_key()
        if not self.api_key:
            raise OfoxError(_help_message())
        self.base_url = (base_url or os.environ.get("OFOX_BASE_URL") or OFOX_BASE_URL).rstrip("/")
        self.model = model or os.environ.get("OFOX_LLM_MODEL") or DEFAULT_MODEL
        self.timeout = timeout

    def chat(
        self,
        messages: list[dict],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        retry: int = 1,
    ) -> str:
        """OpenAI compat /v1/chat/completions。返回 assistant 消息内容。

        Args:
            messages: [{"role": "system|user|assistant", "content": "..."}]
            model: 模型名（覆盖默认）
            temperature: 0-2
            max_tokens: 上限
            retry: 网络/5xx 失败时重试次数

        Returns:
            assistant 消息的纯文本内容
        """
        url = f"{self.base_url}/v1/chat/completions"
        payload: dict = {
            "model": model or self.model,
            "messages": messages,
            "temperature": temperature,
        }
        if max_tokens:
            payload["max_tokens"] = max_tokens

        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")

        last_err: OfoxError | None = None
        for attempt in range(retry + 1):
            try:
                req = urllib.request.Request(
                    url, data=body,
                    headers={
                        "Content-Type": "application/json; charset=utf-8",
                        "Authorization": f"Bearer {self.api_key}",
                    },
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    data = json.loads(resp.read())
                # OpenAI compat: data.choices[0].message.content
                choices = data.get("choices") or []
                if not choices:
                    raise OfoxError(f"Empty choices: {json.dumps(data)[:300]}")
                msg = (choices[0].get("message") or {}).get("content", "")
                if not msg:
                    raise OfoxError(f"Empty content: {json.dumps(data)[:300]}")
                return msg
            except urllib.error.HTTPError as e:
                err_body = e.read().decode("utf-8", errors="replace")[:500]
                last_err = OfoxError(
                    f"HTTP {e.code} from /v1/chat/completions: {err_body}",
                    status=e.code, body=err_body,
                )
                # 5xx 重试，4xx 直接 raise
                if e.code < 500 or attempt >= retry:
                    raise last_err from e
                time.sleep(2 ** attempt)  # 指数退避
            except (urllib.error.URLError, OSError) as e:
                last_err = OfoxError(f"Network error: {e}")
                if attempt >= retry:
                    raise last_err from e
                time.sleep(2 ** attempt)
            except json.JSONDecodeError as e:
                raise OfoxError(f"Invalid JSON response: {e}") from e

        raise last_err or OfoxError("Unknown failure")
