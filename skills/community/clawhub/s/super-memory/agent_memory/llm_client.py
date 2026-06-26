from __future__ import annotations
import os
import json
import logging
import re
import urllib.request
from typing import Callable, Optional

from .utils import _validate_url

logger = logging.getLogger(__name__)

# Security: prompt injection detection patterns
_INJECTION_PATTERNS = re.compile(
    r"(?:ignore\s+(?:previous|above|all)\s+instructions?"
    r"|system\s*:"
    r"|you\s+are\s+now"
    r"|new\s+rule\s*:"
    r"|forget\s+(?:all\s+)?(?:previous|above)\s+instructions?"
    r"|disregard\s+(?:all\s+)?(?:previous|above)\s+instructions?)",
    re.IGNORECASE,
)


class LLMClient:

    def __init__(self, config=None):
        self._backends = {}
        self._default_backend = None
        self._llm_fn = None

        if config:
            self._init_from_config(config)

        env_fn = os.environ.get("LLM_FUNCTION")
        if env_fn:
            self._default_backend = "env_fn"

        self._init_auto_detect()

    def _init_from_config(self, config):
        siliconflow = config.get("siliconflow", {})
        if siliconflow:
            key = os.environ.get("SILICONFLOW_API_KEY") or siliconflow.get("api_key", "")
            if key:
                self._backends["siliconflow"] = {
                    "type": "openai_compatible",
                    "api_key": key,
                    "base_url": os.environ.get("SILICONFLOW_BASE_URL") or siliconflow.get("base_url", "https://api.siliconflow.cn/v1"),
                    "model": os.environ.get("SILICONFLOW_MODEL") or siliconflow.get("model", "Qwen/Qwen2.5-72B-Instruct"),
                }
                self._default_backend = "siliconflow"

        openai = config.get("openai", {})
        if openai:
            key = os.environ.get("OPENAI_API_KEY") or openai.get("api_key", "")
            if key:
                self._backends["openai"] = {
                    "type": "openai_compatible",
                    "api_key": key,
                    "base_url": os.environ.get("OPENAI_BASE_URL") or openai.get("base_url", "https://api.openai.com/v1"),
                    "model": os.environ.get("OPENAI_MODEL") or openai.get("model", "gpt-4o-mini"),
                }
                if not self._default_backend:
                    self._default_backend = "openai"

        custom = config.get("custom", {})
        if custom:
            key = os.environ.get("CUSTOM_LLM_API_KEY") or custom.get("api_key", "")
            url = os.environ.get("CUSTOM_LLM_BASE_URL") or custom.get("base_url", "")
            if key and url:
                self._backends["custom"] = {
                    "type": "openai_compatible",
                    "api_key": key,
                    "base_url": url,
                    "model": os.environ.get("CUSTOM_LLM_MODEL") or custom.get("model", ""),
                }
                if not self._default_backend:
                    self._default_backend = "custom"

        llm_fn = config.get("llm_fn")
        if llm_fn and callable(llm_fn):
            self._llm_fn = llm_fn
            self._backends["direct_fn"] = {"type": "direct_fn"}
            if not self._default_backend:
                self._default_backend = "direct_fn"

    def _init_auto_detect(self):
        if self._default_backend:
            return

        sf_key = os.environ.get("SILICONFLOW_API_KEY", "")
        if sf_key:
            self._backends["siliconflow"] = {
                "type": "openai_compatible",
                "api_key": sf_key,
                "base_url": os.environ.get("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1"),
                "model": os.environ.get("SILICONFLOW_MODEL", "Qwen/Qwen2.5-72B-Instruct"),
            }
            self._default_backend = "siliconflow"
            return

        oai_key = os.environ.get("OPENAI_API_KEY", "")
        if oai_key:
            self._backends["openai"] = {
                "type": "openai_compatible",
                "api_key": oai_key,
                "base_url": os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
                "model": os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            }
            self._default_backend = "openai"

    def set_llm_fn(self, fn: Callable[[str], str]):
        self._llm_fn = fn
        self._backends["direct_fn"] = {"type": "direct_fn"}
        self._default_backend = "direct_fn"

    def chat(self, messages) -> Optional[str]:
        # Security: detect potential prompt injection in messages
        for msg in messages:
            content = msg.get("content", "")
            if content and _INJECTION_PATTERNS.search(content):
                logger.warning(
                    "LLMClient: potential prompt injection detected in message. "
                    "Content starting with '%s...' flagged.",
                    content[:50],
                )

        if self._llm_fn:
            try:
                prompt = "\n".join(m.get("content", "") for m in messages)
                return self._llm_fn(prompt)
            except Exception as e:
                logger.error(f"Direct LLM function failed: {e}")
                return None

        if not self._default_backend or self._default_backend not in self._backends:
            logger.error("No LLM backend configured")
            return None

        backend = self._backends[self._default_backend]
        if backend["type"] == "openai_compatible":
            return self._call_openai_compatible(backend, messages)

        logger.error(f"Unknown backend type: {backend['type']}")
        return None

    def _call_openai_compatible(self, backend: dict, messages: list) -> Optional[str]:
        try:
            payload = json.dumps({
                "model": backend["model"],
                "messages": messages,
                "stream": False,
                "max_tokens": 1000,
                "temperature": 0.7,
            }).encode()

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {backend['api_key']}",
            }

            url = f"{backend['base_url']}/chat/completions"
            _validate_url(url)
            req = urllib.request.Request(
                url,
                data=payload,
                headers=headers,
            )

            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read())

            return result["choices"][0]["message"]["content"]

        except Exception as e:
            # Sanitize error message to avoid leaking URLs with API keys
            safe_msg = str(e)
            for backend_cfg in self._backends.values():
                api_key = backend_cfg.get('api_key', '')
                if api_key and api_key in safe_msg:
                    safe_msg = safe_msg.replace(api_key, '[REDACTED]')
                base_url = backend_cfg.get('base_url', '')
                if base_url and base_url in safe_msg:
                    safe_msg = safe_msg.replace(base_url, '[REDACTED_URL]')
            logger.error(f"LLM API call failed ({self._default_backend}): {safe_msg}")
            return None

    def is_available(self) -> bool:
        if self._llm_fn:
            return True
        return bool(self._default_backend and self._default_backend in self._backends)

    def get_backend_info(self) -> dict:
        return {
            "default": self._default_backend,
            "available": list(self._backends.keys()),
            "has_direct_fn": self._llm_fn is not None,
        }
