"""
yumnb AI provider — single interface over OpenAI / Anthropic / Gemini /
Ollama / arbitrary CLI agent / no-op.

Each provider implements `.complete(system, user) -> str`.

The skill itself decides what to ask the LLM. This module just routes the
prompt to whatever backend the user configured in `config.yaml`.
"""
from __future__ import annotations

import json
import os
import subprocess
from typing import Any, Dict


class AIError(RuntimeError):
    pass


# ── Provider implementations ──────────────────────────────────────────────

class _NoneProvider:
    """No-op: yumnb operates in step-by-step mode; the agent does AI work."""

    def complete(self, system: str, user: str) -> str:
        raise AIError(
            "ai.provider is 'none' — yumnb expects you (or another agent) to "
            "write summary.md / deck.json manually. Use the step-by-step "
            "workflow described in README.md."
        )


class _OpenAIProvider:
    def __init__(self, cfg: Dict[str, Any]):
        try:
            from openai import OpenAI  # type: ignore
        except ImportError as e:
            raise AIError(
                "openai package not installed. Install it inside yumnb's venv with: "
                "pip install openai"
            ) from e
        api_key = cfg.get("api_key") or os.environ.get("OPENAI_API_KEY")
        base_url = cfg.get("base_url") or os.environ.get("OPENAI_BASE_URL")
        if not api_key and not base_url:
            raise AIError(
                "ai.provider is 'openai' but no OPENAI_API_KEY (or ai.openai.api_key) was found. "
                "Either set a key, set a compatible OPENAI_BASE_URL, or switch ai.provider to 'none' for step-by-step mode."
            )
        kwargs: Dict[str, Any] = {}
        if api_key:
            kwargs["api_key"] = api_key
        if base_url:
            kwargs["base_url"] = base_url
        self.client = OpenAI(**kwargs)
        self.model = cfg.get("model", "gpt-4o-mini")

    def complete(self, system: str, user: str) -> str:
        r = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": user}],
        )
        return (r.choices[0].message.content or "").strip()


class _AnthropicProvider:
    def __init__(self, cfg: Dict[str, Any]):
        try:
            import anthropic  # type: ignore
        except ImportError as e:
            raise AIError(
                "anthropic package not installed. Install it inside yumnb's venv with: pip install anthropic"
            ) from e
        api_key = cfg.get("api_key") or os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise AIError(
                "ai.provider is 'anthropic' but no ANTHROPIC_API_KEY (or ai.anthropic.api_key) was found. "
                "Set the key or switch ai.provider to 'none'."
            )
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = cfg.get("model", "claude-3-5-sonnet-latest")

    def complete(self, system: str, user: str) -> str:
        r = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        # response.content is a list of content blocks
        out = []
        for block in r.content:
            text = getattr(block, "text", None)
            if text:
                out.append(text)
        return "".join(out).strip()


class _GeminiProvider:
    def __init__(self, cfg: Dict[str, Any]):
        try:
            import google.generativeai as genai  # type: ignore
        except ImportError as e:
            raise AIError(
                "google-generativeai package not installed. Install it inside yumnb's venv with: pip install google-generativeai"
            ) from e
        api_key = cfg.get("api_key") or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise AIError(
                "ai.provider is 'gemini' but no GEMINI_API_KEY / GOOGLE_API_KEY was found. "
                "Set the key or switch ai.provider to 'none'."
            )
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(cfg.get("model", "gemini-1.5-flash"))

    def complete(self, system: str, user: str) -> str:
        r = self.model.generate_content([system, user])
        return (getattr(r, "text", "") or "").strip()


class _OllamaProvider:
    def __init__(self, cfg: Dict[str, Any]):
        try:
            import ollama  # type: ignore
        except ImportError as e:
            raise AIError(
                "ollama package not installed. Install it inside yumnb's venv with: pip install ollama"
            ) from e
        host = cfg.get("host", "http://localhost:11434")
        self.client = ollama.Client(host=host)
        self.model = cfg.get("model", "qwen2.5:7b")

    def complete(self, system: str, user: str) -> str:
        r = self.client.chat(
            model=self.model,
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": user}],
        )
        return r["message"]["content"].strip()


class _CLIProvider:
    """Shell out to an external agent CLI. Prompt goes to stdin, answer
    comes from stdout. Works with copilot, claude, aider, ollama run, etc."""

    def __init__(self, cfg: Dict[str, Any]):
        cmd = cfg.get("command")
        if not cmd or not isinstance(cmd, list):
            raise AIError("ai.cli.command must be a non-empty list, e.g. ['claude', '-p']")
        self.cmd = cmd
        self.timeout = int(cfg.get("timeout_seconds", 300))

    def complete(self, system: str, user: str) -> str:
        prompt = f"<system>\n{system}\n</system>\n\n<user>\n{user}\n</user>\n"
        try:
            r = subprocess.run(self.cmd, input=prompt, capture_output=True,
                               text=True, encoding="utf-8", timeout=self.timeout)
        except subprocess.TimeoutExpired as e:
            raise AIError(f"CLI provider timed out after {self.timeout}s: {e}")
        if r.returncode != 0:
            raise AIError(f"CLI provider exited {r.returncode}: {r.stderr[:500]}")
        return r.stdout.strip()


# ── Factory ────────────────────────────────────────────────────────────────

def get_provider(ai_cfg: Dict[str, Any]):
    name = (ai_cfg or {}).get("provider", "none")
    if not name or name == "none":
        return _NoneProvider()
    sub = (ai_cfg or {}).get(name, {}) or {}
    if name == "openai":
        return _OpenAIProvider(sub)
    if name == "anthropic":
        return _AnthropicProvider(sub)
    if name == "gemini":
        return _GeminiProvider(sub)
    if name == "ollama":
        return _OllamaProvider(sub)
    if name == "cli":
        return _CLIProvider(sub)
    raise AIError(f"Unknown ai.provider: {name!r}")


# ── Convenience: ask the provider for JSON, with one retry on parse error ──

def complete_json(provider, system: str, user: str) -> Any:
    text = provider.complete(system, user)
    text = text.strip()
    # Strip code fences if model wrapped output
    if text.startswith("```"):
        text = text.split("```", 2)[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip("` \n")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # one retry asking the model to fix it
        fix = provider.complete(
            "You output only valid JSON. No prose. No code fences.",
            f"The previous output was not valid JSON:\n\n{text}\n\nReturn the same data as strict JSON.",
        )
        return json.loads(fix.strip().strip("` \n"))
