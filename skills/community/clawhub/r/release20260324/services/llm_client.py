"""
Multi-provider LLM client — unified interface via OpenAI-compatible API.

Supports 20+ providers (US & Chinese). All use the same openai SDK with different
base_url and api_key. Auto-detects provider from environment variables, or accepts
explicit configuration via LLM_PROVIDER / LLM_MODEL / LLM_API_KEY / LLM_BASE_URL.

Usage:
    from services.llm_client import llm_chat, is_llm_available
    if is_llm_available():
        response = llm_chat("Summarize these papers: ...")
"""
import os
import sys
from dataclasses import dataclass
from typing import Optional

# ---------------------------------------------------------------------------
# Provider Registry
# ---------------------------------------------------------------------------

@dataclass
class Provider:
    name: str
    env_key: str           # environment variable for API key
    base_url: str
    default_model: str
    display_name: str      # human-readable name

# Order matters: first match wins in auto-detect
PROVIDERS = [
    # --- US Providers ---
    Provider("openai",      "OPENAI_API_KEY",      "https://api.openai.com/v1",                            "gpt-4o-mini",                                          "OpenAI"),
    Provider("anthropic",   "ANTHROPIC_API_KEY",    "https://api.anthropic.com/v1/",                        "claude-sonnet-4-20250514",                             "Anthropic (Claude)"),
    Provider("gemini",      "GEMINI_API_KEY",       "https://generativelanguage.googleapis.com/v1beta/openai/", "gemini-2.0-flash",                                 "Google (Gemini)"),
    Provider("deepseek",    "DEEPSEEK_API_KEY",     "https://api.deepseek.com",                             "deepseek-chat",                                        "DeepSeek"),
    Provider("groq",        "GROQ_API_KEY",         "https://api.groq.com/openai/v1",                       "llama-3.1-8b-instant",                                 "Groq"),
    Provider("together",    "TOGETHER_API_KEY",     "https://api.together.xyz/v1",                          "meta-llama/Llama-3.1-8B-Instruct-Turbo",               "Together AI"),
    Provider("fireworks",   "FIREWORKS_API_KEY",    "https://api.fireworks.ai/inference/v1",                 "accounts/fireworks/models/llama-v3p1-8b-instruct",     "Fireworks AI"),
    Provider("mistral",     "MISTRAL_API_KEY",      "https://api.mistral.ai/v1",                            "mistral-small-latest",                                 "Mistral"),
    Provider("xai",         "XAI_API_KEY",          "https://api.x.ai/v1",                                  "grok-3-mini-fast",                                     "xAI (Grok)"),
    Provider("perplexity",  "PERPLEXITY_API_KEY",   "https://api.perplexity.ai",                            "sonar",                                                "Perplexity"),
    Provider("openrouter",  "OPENROUTER_API_KEY",   "https://openrouter.ai/api/v1",                         "meta-llama/llama-3.1-8b-instruct:free",                "OpenRouter"),
    # --- Chinese Providers ---
    Provider("zhipu",       "ZHIPUAI_API_KEY",      "https://open.bigmodel.cn/api/paas/v4/",                "glm-4-flash",                                          "Zhipu (智谱)"),
    Provider("moonshot",    "MOONSHOT_API_KEY",     "https://api.moonshot.cn/v1",                            "moonshot-v1-8k",                                       "Moonshot (月之暗面)"),
    Provider("baichuan",    "BAICHUAN_API_KEY",     "https://api.baichuan-ai.com/v1",                        "Baichuan2-Turbo",                                      "Baichuan (百川)"),
    Provider("yi",          "YI_API_KEY",           "https://api.lingyiwanwu.com/v1",                        "yi-lightning",                                         "Yi (零一万物)"),
    Provider("qwen",        "DASHSCOPE_API_KEY",    "https://dashscope.aliyuncs.com/compatible-mode/v1",     "qwen-turbo",                                           "Qwen (通义千问)"),
    Provider("doubao",      "ARK_API_KEY",          "https://ark.cn-beijing.volces.com/api/v3",              "doubao-lite-32k",                                      "Doubao (豆包)"),
    Provider("minimax",     "MINIMAX_API_KEY",      "https://api.minimax.io/v1",                             "MiniMax-Text-01",                                      "MiniMax"),
    Provider("stepfun",     "STEPFUN_API_KEY",      "https://api.stepfun.com/v1",                            "step-1-flash",                                         "Stepfun (阶跃星辰)"),
    Provider("sensenova",   "SENSENOVA_API_KEY",    "https://api.sensenova.cn/compatible-mode/v1",           "SenseChat-Turbo",                                      "SenseTime (商汤日日新)"),
]

PROVIDER_MAP = {p.name: p for p in PROVIDERS}

# ---------------------------------------------------------------------------
# Auto-detection & Configuration
# ---------------------------------------------------------------------------

def _detect_provider() -> Optional[Provider]:
    """Auto-detect provider from environment variables.

    Priority:
    1. LLM_PROVIDER env var (explicit selection)
    2. First provider whose API key env var is set
    """
    # Explicit provider selection
    explicit = os.environ.get("LLM_PROVIDER", "").strip().lower()
    if explicit and explicit in PROVIDER_MAP:
        p = PROVIDER_MAP[explicit]
        # Check if key is available (via provider-specific or generic LLM_API_KEY)
        if os.environ.get(p.env_key) or os.environ.get("LLM_API_KEY"):
            return p

    # Auto-detect: scan providers in order
    for p in PROVIDERS:
        if os.environ.get(p.env_key):
            return p

    # Generic fallback: LLM_API_KEY + LLM_BASE_URL
    if os.environ.get("LLM_API_KEY") and os.environ.get("LLM_BASE_URL"):
        return Provider(
            name="custom",
            env_key="LLM_API_KEY",
            base_url=os.environ["LLM_BASE_URL"],
            default_model=os.environ.get("LLM_MODEL", "default"),
            display_name="Custom Provider",
        )

    return None


def is_llm_available() -> bool:
    """Check if any LLM provider is configured."""
    return _detect_provider() is not None


def get_provider_info() -> Optional[dict]:
    """Return info about the detected LLM provider (for diagnostics)."""
    p = _detect_provider()
    if not p:
        return None
    model = os.environ.get("LLM_MODEL", p.default_model)
    return {"provider": p.name, "display_name": p.display_name, "model": model}


# ---------------------------------------------------------------------------
# Chat Completion
# ---------------------------------------------------------------------------

def llm_chat(
    prompt: str,
    system: str = "You are a research assistant that analyzes academic papers.",
    model: Optional[str] = None,
    temperature: float = 0.3,
    max_tokens: int = 2000,
) -> Optional[str]:
    """Send a chat completion request to the detected LLM provider.

    Returns the response text, or None if no provider is available or call fails.
    """
    provider = _detect_provider()
    if not provider:
        return None

    try:
        from openai import OpenAI
    except ImportError:
        print("[llm] openai package not installed — run: pip install openai", file=sys.stderr)
        return None

    # Resolve API key: provider-specific env var, or generic LLM_API_KEY
    api_key = os.environ.get(provider.env_key) or os.environ.get("LLM_API_KEY", "")
    base_url = os.environ.get("LLM_BASE_URL", provider.base_url)
    model = model or os.environ.get("LLM_MODEL", provider.default_model)

    try:
        print(f"[llm] Using {provider.display_name} ({model})...", file=sys.stderr)
        client = OpenAI(api_key=api_key, base_url=base_url, timeout=60.0)
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content
    except Exception as e:
        print(f"[llm] {provider.display_name} call failed: {e}", file=sys.stderr)
        return None


def list_providers() -> list:
    """Return all supported providers with availability status."""
    result = []
    for p in PROVIDERS:
        has_key = bool(os.environ.get(p.env_key))
        result.append({
            "name": p.name,
            "display_name": p.display_name,
            "env_key": p.env_key,
            "default_model": p.default_model,
            "available": has_key,
        })
    # Custom provider
    if os.environ.get("LLM_API_KEY") and os.environ.get("LLM_BASE_URL"):
        result.append({
            "name": "custom",
            "display_name": "Custom Provider",
            "env_key": "LLM_API_KEY",
            "default_model": os.environ.get("LLM_MODEL", "default"),
            "available": True,
        })
    return result
