#!/usr/bin/env python3
"""
research_tools.py - 研究工具封装（方案B+C）

核心原则：
  - 内容来源 = 开题报告（Phase 1.3 归因结果），多工具检索仅做补充/验证
  - Skill 本身不存储任何论文特定内容
  - 网络不可用时降级，不阻断写作流程

提供：
  - research_enrich(node_id, paper_name) → str：方案C强制前置补充（outline + 多工具检索）
  - research_enrich_from_outline(node_id, paper_name) → str：纯 outline 提取（无网络依赖）
  - multi_search(query) → str：直接调用多工具检索（供 Agent 层使用）
  - get_session_llm_func() → Callable：内部固化 session LLM 函数，供 orchestrator 内部使用

多工具策略（v2 新增）：
  - web_search  ：头条搜索（Agent 内置，Python 层不代理）
  - tavily      ：Tavily MCP（通过 mcporter）
  - arxiv       ：arXiv 论文搜索（通过 mcporter）
  - openalex    ：OpenAlex 学术文献（通过 scholar-search.py）
  四工具并行，取长补短，去重排序
"""

import sys
import os
import json
import subprocess
import threading
import urllib.request
from pathlib import Path
from typing import Optional, Callable, Dict


# ============================================================
# P1-1 修复（废弃，保留兼容性）：可靠的 API Key 加载
# 注意：已由 get_session_llm_func() 替代，此函数保留但不再被 orchestrator 调用
# ============================================================

def load_minimax_api_key() -> str:
    """
    可靠加载 MiniMax API Key（方案 A:显式 source ~/.zshrc）

    解决：subprocess 中 bash -c 'source ~/.zshrc' 不加载 zsh 特有配置的问题
    用户环境中 MINIMAX_API_KEY 写在 ~/.zshrc，用 bash -lc 才能可靠读取
    """
    # 方案 A: bash -lc 加载 zshrc（-l=login shell, -c=执行命令）
    try:
        result = subprocess.run(
            ['bash', '-lc', 'printf "%s" "$MINIMAX_API_KEY"'],
            capture_output=True, text=True, timeout=5
        )
        key = result.stdout.strip()
        if key and len(key) > 10:
            return key
    except Exception:
        pass

    # 方案 B: 直接读 ~/.zshrc 文本（兜底）
    try:
        zshrc_path = os.path.expanduser('~/.zshrc')
        with open(zshrc_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip().startswith('export MINIMAX_API_KEY='):
                    val = line.strip().split('=', 1)[1].strip()
                    if val.startswith('"') and val.endswith('"'):
                        return val[1:-1]
                    elif val.startswith("'") and val.endswith("'"):
                        return val[1:-1]
    except Exception:
        pass

    return ''


# ============================================================
# RuntimeLLM：内部固化 session LLM 函数（替代外部传 llm_func）
# ============================================================

_runtime_llm: Optional["RuntimeLLM"] = None
_lll_func_cached: Optional[Callable[[str], str]] = None


class RuntimeLLM:
    """
    从当前 agent session 获取 LLM 凭证并构造 llm_func。

    核心逻辑：
      1. openclaw sessions list --agent <agent_id> --active 30 → 获取当前 session 的 model + provider
      2. 从 ~/.openclaw/agents/<agent_id>/agent/plugins/*/catalog.json → 获取 baseUrl + apiKey + apiType
      3. 构造 llm_func(prompt) -> str 闭包（不依赖 session 本身，session 退出后仍可用）

    使用方式：
      llm_func = get_session_llm_func()  # 一次性固化，后续直接用
    """

    def __init__(self, agent_id: Optional[str] = None):
        self._session_info: Optional[Dict] = None
        self._lock = threading.Lock()
        self._agent_id = agent_id

    @staticmethod
    def _find_openclaw() -> str:
        """查找 openclaw CLI 路径"""
        home = Path.home()
        nvm_openclaw = home / ".nvm/versions/node/v24.14.0/bin/openclaw"
        if nvm_openclaw.exists():
            return str(nvm_openclaw)
        for path in os.environ.get("PATH", "").split(os.pathsep):
            candidate = Path(path) / "openclaw"
            if candidate.exists() and not candidate.is_dir():
                return str(candidate)
        raise RuntimeError("找不到 openclaw CLI，请确保已安装并位于 PATH 中")

    def _get_session_info(self) -> Dict:
        """通过 openclaw sessions list 获取当前 session 信息"""
        try:
            openclaw_path = self._find_openclaw()
            cmd = [openclaw_path, "sessions", "list", "--active", "30", "--json"]
            if self._agent_id:
                cmd.extend(["--agent", self._agent_id])
            else:
                cmd.append("--all-agents")

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                raise RuntimeError(f"openclaw sessions list failed: {result.stderr}")

            data = json.loads(result.stdout)
            sessions = data.get("sessions", [])
            if not sessions:
                raise RuntimeError("未找到活跃 session（30分钟内）")

            current = sessions[0]
            session_key = current.get("key", "")
            parts = session_key.split(":")
            resolved_agent_id = parts[1] if len(parts) >= 2 else "unknown"

            if self._agent_id and resolved_agent_id != self._agent_id:
                raise RuntimeError(
                    f"session agent 不匹配：期望 {self._agent_id}，实际 {resolved_agent_id}。"
                    f"session_key={session_key}"
                )

            return {
                "model": current.get("model", ""),
                "provider": current.get("modelProvider", ""),
                "agent_id": resolved_agent_id,
                "session_key": session_key,
            }
        except subprocess.TimeoutExpired:
            raise RuntimeError("openclaw sessions list 超时")
        except Exception as e:
            raise RuntimeError(f"读取 session 信息失败: {e}")

    def _get_provider_config(self, provider: str, agent_id: str) -> Dict:
        """从 agent plugin catalog 读取 provider 凭证"""
        plugins_base = Path.home() / ".openclaw" / "agents" / agent_id / "agent" / "plugins"
        if not plugins_base.exists():
            raise RuntimeError(f"plugins 目录不存在: {plugins_base}")

        catalog_path = None
        for subdir in plugins_base.iterdir():
            if not subdir.is_dir():
                continue
            candidate = subdir / "catalog.json"
            if candidate.exists():
                try:
                    with open(candidate) as f:
                        catalog = json.load(f)
                    providers = catalog.get("providers", {})
                    if provider in providers or "minimax-cn" in providers:
                        catalog_path = candidate
                        break
                except Exception:
                    continue

        if not catalog_path:
            raise RuntimeError(
                f"在 {plugins_base} 下未找到包含 provider '{provider}' 的 catalog"
            )

        with open(catalog_path) as f:
            catalog = json.load(f)

        providers = catalog.get("providers", {})
        cfg = providers.get(provider) or providers.get("minimax-cn", {})

        if not cfg:
            raise RuntimeError(f"provider '{provider}' 未在 catalog 中找到")

        return {
            "base_url": cfg["baseUrl"],
            "api_key": cfg["apiKey"],
            "api_type": cfg.get("api", "anthropic-messages"),
        }

    def make_llm_func(self, model: Optional[str] = None) -> Callable[[str], str]:
        """
        返回 llm_func(prompt: str) -> str。

        参数 model 为 None 时，自动使用当前 session 的模型。
        """
        if self._session_info is None:
            with self._lock:
                if self._session_info is None:
                    self._session_info = self._get_session_info()

        target_model = model or self._session_info["model"]
        provider = self._session_info["provider"]
        agent_id = self._session_info["agent_id"]

        provider_cfg = self._get_provider_config(provider, agent_id)
        base_url = provider_cfg["base_url"]
        api_key = provider_cfg["api_key"]
        api_type = provider_cfg["api_type"]

        def llm_func(prompt: str) -> str:
            if api_type == "anthropic-messages":
                return self._call_anthropic(base_url, api_key, target_model, prompt)
            else:
                return self._call_openai(base_url, api_key, target_model, prompt)

        return llm_func

    def _call_anthropic(self, base_url: str, api_key: str, model: str, prompt: str) -> str:
        """调用 Anthropic-format API（minimax-cn 等）"""
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 4096,
        }
        data = json.dumps(payload).encode()
        req = urllib.request.Request(
            f"{base_url}/v1/messages",
            data=data,
            headers={
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
            },
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())

        for block in result.get("content", []):
            if block.get("type") == "text":
                return block["text"]

        stop_reason = result.get("stop_reason", "")
        if stop_reason == "max_tokens":
            raise RuntimeError("LLM 返回被截断（max_tokens），请增加 max_tokens 参数")
        raise RuntimeError(f"LLM 响应为空，stop_reason={stop_reason}")

    def _call_openai(self, base_url: str, api_key: str, model: str, prompt: str) -> str:
        """调用 OpenAI-completions-format API（deepseek 等）"""
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 4096,
        }
        data = json.dumps(payload).encode()
        req = urllib.request.Request(
            f"{base_url}/chat/completions",
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())

        choices = result.get("choices", [])
        if choices:
            return choices[0].get("message", {}).get("content", "")

        raise RuntimeError(f"LLM 响应为空，choices={choices}")


def get_runtime_llm(agent_id: Optional[str] = None) -> RuntimeLLM:
    """获取 RuntimeLLM 全局单例"""
    global _runtime_llm
    if _runtime_llm is None:
        _runtime_llm = RuntimeLLM(agent_id=agent_id)
    return _runtime_llm


def get_session_llm_func(agent_id: Optional[str] = None) -> Callable[[str], str]:
    """
    获取固化到内存的 llm_func（一次固化，后续直接用）。

    依赖 openclaw sessions list + agent plugin catalog。
    必须在 OpenClaw session 上下文中调用（需要能访问 ~/.openclaw/agents/）。

    外部调用异常时返回友好错误：
      "无法获取 session LLM 配置，请确保从 OpenClaw session 内调用"
    """
    global _lll_func_cached

    if _lll_func_cached is not None:
        return _lll_func_cached

    try:
        rllm = get_runtime_llm(agent_id=agent_id)
        _lll_func_cached = rllm.make_llm_func()
        return _lll_func_cached
    except Exception as e:
        error_msg = str(e)
        # 构造友好错误供调用方捕获
        raise RuntimeError(
            f"无法获取 session LLM 配置，请确保从 OpenClaw session 内调用。详情: {error_msg}"
        )


# ============================================================
# 以下为原有研究工具函数（保留不动）
# ============================================================

# 兼容旧路径引用
try:
    from multi_search import multi_search_text, multi_search
except ImportError:
    pass