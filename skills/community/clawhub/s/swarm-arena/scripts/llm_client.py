#!/usr/bin/env python3
"""llm_client.py — stdlib-only multi-provider LLM chat client.

One function, every provider. API keys come from per-model env vars (never
from files). Supported providers:

  anthropic   POST {base}/v1/messages            header x-api-key
  openai      POST {base}/v1/chat/completions    header Authorization: Bearer
  xai         same shape as openai (api.x.ai)
  deepseek    same shape as openai (api.deepseek.com)
  qwen        same shape as openai (dashscope, compatible mode)
  gemini      POST {base}/v1beta/models/{model}:generateContent?key=KEY

Module:  from llm_client import chat
CLI:     MODEL_CFG='{"provider":"anthropic","model":"claude-sonnet-5",...}' \
         python3 llm_client.py prompt.txt
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

DEFAULT_BASE_URLS = {
    "anthropic": "https://api.anthropic.com",
    "openai": "https://api.openai.com",
    "xai": "https://api.x.ai",
    "deepseek": "https://api.deepseek.com",
    "qwen": "https://dashscope.aliyuncs.com/compatible-mode",
    "gemini": "https://generativelanguage.googleapis.com",
}
DEFAULT_ENV_KEYS = {
    "anthropic": "ANTHROPIC_API_KEY",
    "openai": "OPENAI_API_KEY",
    "xai": "XAI_API_KEY",
    "deepseek": "DEEPSEEK_API_KEY",
    "qwen": "QWEN_API_KEY",
    "gemini": "GEMINI_API_KEY",
}
DEFAULT_MAX_TOKENS = 4000


class LLMError(Exception):
    pass


def _post(url, payload, headers, timeout):
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(),
        headers=dict({"Content-Type": "application/json"}, **headers),
        method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            text = resp.read().decode()
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:400]
        raise LLMError("HTTP %d: %s" % (e.code, body))
    except (urllib.error.URLError, TimeoutError) as e:
        raise LLMError(str(e))
    try:
        return json.loads(text)
    except ValueError:
        pass
    # Some gateways append an SSE terminator ("data: [DONE]") or framing junk
    # after the JSON body on non-streaming replies — parse the first object.
    try:
        obj, _ = json.JSONDecoder().raw_decode(text.lstrip())
        return obj
    except ValueError as e:
        raise LLMError("unparseable response: %s" % e)


def _anthropic(base, key, model, system, user, max_tokens, timeout):
    data = _post(base + "/v1/messages", {
        "model": model, "max_tokens": max_tokens, "system": system,
        "messages": [{"role": "user", "content": user}],
    }, {"x-api-key": key, "anthropic-version": "2023-06-01"}, timeout)
    parts = [b.get("text", "") for b in data.get("content", [])
             if isinstance(b, dict) and b.get("type") == "text"]
    if not parts:
        raise LLMError("anthropic: empty content")
    return "".join(parts)


def _openai_shape(base, key, model, system, user, max_tokens, timeout):
    data = _post(base + "/v1/chat/completions", {
        "model": model, "max_tokens": max_tokens,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": user}],
    }, {"Authorization": "Bearer " + key}, timeout)
    try:
        msg = data["choices"][0]["message"]
    except (KeyError, IndexError, TypeError):
        raise LLMError("openai-shape: malformed response")
    # Reasoning models may return content=None (token budget spent on
    # reasoning_content); fall back to it, and treat empty as a hard error
    # so the failure feeds the circuit breaker instead of passing silently.
    content = msg.get("content") or msg.get("reasoning_content")
    if not content:
        raise LLMError("openai-shape: empty content (finish=%r)"
                       % (data["choices"][0].get("finish_reason"),))
    return content


def _gemini(base, key, model, system, user, max_tokens, timeout):
    url = "%s/v1beta/models/%s:generateContent?key=%s" % (base, model, key)
    data = _post(url, {
        "systemInstruction": {"parts": [{"text": system}]},
        "contents": [{"role": "user", "parts": [{"text": user}]}],
        "generationConfig": {"maxOutputTokens": max_tokens},
    }, {}, timeout)
    try:
        parts = data["candidates"][0]["content"]["parts"]
        return "".join(p.get("text", "") for p in parts)
    except (KeyError, IndexError, TypeError):
        raise LLMError("gemini: malformed response")


def chat(model_cfg, system, user, timeout=120):
    """model_cfg: {"provider","model","api_key_env","base_url"?,"max_tokens"?,
    "timeout_sec"?}. Returns the raw assistant text. Raises LLMError on
    transport/API failure."""
    timeout = int(model_cfg.get("timeout_sec") or timeout)
    provider = (model_cfg.get("provider") or "").lower()
    if provider not in DEFAULT_BASE_URLS:
        raise LLMError("unknown provider %r" % provider)
    model = model_cfg.get("model")
    if not model:
        raise LLMError("model name missing")
    env_name = model_cfg.get("api_key_env") or DEFAULT_ENV_KEYS[provider]
    key = os.environ.get(env_name)
    if not key:
        raise LLMError("env %s not set" % env_name)
    base = (model_cfg.get("base_url") or DEFAULT_BASE_URLS[provider]).rstrip("/")
    max_tokens = int(model_cfg.get("max_tokens") or DEFAULT_MAX_TOKENS)

    if provider == "anthropic":
        return _anthropic(base, key, model, system, user, max_tokens, timeout)
    if provider == "gemini":
        return _gemini(base, key, model, system, user, max_tokens, timeout)
    return _openai_shape(base, key, model, system, user, max_tokens, timeout)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Send a prompt to an arena model")
    parser.add_argument("prompt", help="user prompt file (default: stdin)", nargs="?")
    args = parser.parse_args(argv)
    model_cfg = json.loads(os.environ.get("MODEL_CFG", "{}"))
    user = open(args.prompt).read() if args.prompt else sys.stdin.read()
    try:
        print(chat(model_cfg, "You are a trading agent.", user))
    except LLMError as e:
        print(json.dumps({"error": str(e)}))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
