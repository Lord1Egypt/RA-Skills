"""LLM 适配层 — 12 个供应商统一接口（OpenAI 兼容）"""
import os
import sys
import json
from typing import Optional

# 全局标记：避免每次调用都打印警告
_RELAY_WARNING_SHOWN = False

PROVIDERS = {
    # 国内主流
    "deepseek":  {"base": "https://api.deepseek.com/v1",
                  "default_model": "deepseek-chat",
                  "key_env": "DEEPSEEK_API_KEY"},
    "doubao":    {"base": "https://ark.cn-beijing.volces.com/api/v3",
                  "default_model": "doubao-pro-32k",
                  "key_env": "DOUBAO_API_KEY"},
    "kimi":      {"base": "https://api.moonshot.cn/v1",
                  "default_model": "moonshot-v1-32k",
                  "key_env": "KIMI_API_KEY"},
    "qwen":      {"base": "https://dashscope.aliyuncs.com/compatible-mode/v1",
                  "default_model": "qwen-plus",
                  "key_env": "QWEN_API_KEY"},
    "zhipu":     {"base": "https://open.bigmodel.cn/api/paas/v4",
                  "default_model": "glm-4-plus",
                  "key_env": "ZHIPU_API_KEY"},
    "yi":        {"base": "https://api.lingyiwanwu.com/v1",
                  "default_model": "yi-large",
                  "key_env": "YI_API_KEY"},
    "baichuan":  {"base": "https://api.baichuan-ai.com/v1",
                  "default_model": "Baichuan4",
                  "key_env": "BAICHUAN_API_KEY"},
    "minimax":   {"base": "https://api.minimax.chat/v1",
                  "default_model": "abab6.5s-chat",
                  "key_env": "MINIMAX_API_KEY"},
    # 国际
    "openai":    {"base": "https://api.openai.com/v1",
                  "default_model": "gpt-4o",
                  "key_env": "OPENAI_API_KEY"},
    "claude":    {"base": "https://api.anthropic.com/v1",
                  "default_model": "claude-sonnet-4-6",
                  "key_env": "ANTHROPIC_API_KEY",
                  "format": "anthropic"},
    "gemini":    {"base": "https://generativelanguage.googleapis.com/v1beta",
                  "default_model": "gemini-2.0-flash",
                  "key_env": "GEMINI_API_KEY",
                  "format": "gemini"},
    # 中转（OpenAI 兼容）
    "relay":     {"base": "https://apiport.cc.cd/v1",
                  "default_model": "claude-opus-4-7",
                  "key_env": "CLAUDE_RELAY_KEY"},
}


class LLMClient:
    def __init__(self, provider: str = None, api_key: str = None,
                 model: str = None, base_url: str = None):
        self.provider = provider or os.getenv("LLM_PROVIDER", "none").lower()

        if self.provider == "none" or self.provider not in PROVIDERS:
            self.enabled = False
            return

        cfg = PROVIDERS[self.provider]
        self.base = base_url or os.getenv(f"{self.provider.upper()}_API_BASE", cfg["base"])
        self.model = model or os.getenv(f"{self.provider.upper()}_MODEL", cfg["default_model"])
        self.api_key = api_key or os.getenv(cfg["key_env"], "")
        self.format = cfg.get("format", "openai")
        self.enabled = bool(self.api_key)

        # 第三方中转运行时警告（每个进程只显示一次）
        global _RELAY_WARNING_SHOWN
        if self.enabled and self.provider == "relay" and not _RELAY_WARNING_SHOWN:
            print(
                "\n⚠️  [zhuge-skill] LLM relay mode is enabled.\n"
                f"   Your prompts and API key will transit through {self.base}\n"
                "   This is a THIRD-PARTY proxy — the operator can technically see your data.\n"
                "   For production use, prefer direct official APIs "
                "(DEEPSEEK_API_KEY / OPENAI_API_KEY / ANTHROPIC_API_KEY).\n"
                "   See PRIVACY.md for details.\n",
                file=sys.stderr,
            )
            _RELAY_WARNING_SHOWN = True

    @staticmethod
    def _sanitize(text: str, max_len: int = 8000) -> str:
        """Defensive clamp: strip control chars, cap length. Called on ALL external-facing fields.

        For prompt-injection defense per Semgrep audit: even though this skill's prompts
        are constructed from structured data (hexagrams/yao/match names), not raw user text,
        we still clamp as defense-in-depth for future callers that may pass user input.
        """
        if not isinstance(text, str):
            text = str(text)
        # Drop ASCII control chars except \n \t
        cleaned = "".join(ch for ch in text if ch.isprintable() or ch in ("\n", "\t"))
        return cleaned[:max_len]

    def chat(self, prompt: str, system: str = None,
             max_tokens: int = 500, timeout: int = 30) -> Optional[str]:
        """调 LLM，返回文本。失败/未启用返回 None。
        Inputs are sanitized + all providers use structured message format (no raw concat)."""
        if not self.enabled:
            return None

        try:
            import requests
        except ImportError:
            return None

        # Defense-in-depth: clamp inputs before any transport (see _sanitize docstring)
        prompt = self._sanitize(prompt)
        if system:
            system = self._sanitize(system, max_len=2000)

        try:
            if self.format == "anthropic":
                return self._call_anthropic(prompt, system, max_tokens, timeout, requests)
            elif self.format == "gemini":
                return self._call_gemini(prompt, system, max_tokens, timeout, requests)
            else:
                return self._call_openai(prompt, system, max_tokens, timeout, requests)
        except Exception as e:
            try:
                import sys
                from pathlib import Path
                sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
                from scripts.error_log import log_error
                log_error("llm_call", e, {"format": self.format,
                                          "provider": getattr(self, "provider", "?")})
            except Exception:
                pass
            return f"[LLM error: {e}]"

    def _call_openai(self, prompt, system, max_tokens, timeout, requests):
        msgs = []
        if system:
            msgs.append({"role": "system", "content": system})
        msgs.append({"role": "user", "content": prompt})
        r = requests.post(
            f"{self.base}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}",
                     "Content-Type": "application/json"},
            json={"model": self.model, "messages": msgs,
                  "max_tokens": max_tokens, "temperature": 0.7},
            timeout=timeout,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]

    def _call_anthropic(self, prompt, system, max_tokens, timeout, requests):
        body = {"model": self.model, "max_tokens": max_tokens,
                "messages": [{"role": "user", "content": prompt}]}
        if system:
            body["system"] = system
        r = requests.post(
            f"{self.base}/messages",
            headers={"x-api-key": self.api_key, "anthropic-version": "2023-06-01",
                     "Content-Type": "application/json"},
            json=body, timeout=timeout,
        )
        r.raise_for_status()
        return r.json()["content"][0]["text"]

    def _call_gemini(self, prompt, system, max_tokens, timeout, requests):
        # Per Semgrep audit fix: use structured systemInstruction instead of concat.
        # Prevents prompt from overriding system role even with untrusted input.
        body = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"maxOutputTokens": max_tokens, "temperature": 0.7},
        }
        if system:
            body["systemInstruction"] = {"parts": [{"text": system}]}
        r = requests.post(
            f"{self.base}/models/{self.model}:generateContent?key={self.api_key}",
            json=body,
            timeout=timeout,
        )
        r.raise_for_status()
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
