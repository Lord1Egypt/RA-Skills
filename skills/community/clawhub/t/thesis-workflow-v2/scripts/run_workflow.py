#!/usr/bin/env python3
"""
run_workflow.py - thesis-workflow v2 真实入口 CLI（v2.0.6 新增）

P0-2 + P0-3 修复：补 v2 真实入口
  - CLI 入口（`python3 scripts/run_workflow.py <paper_name>`）
  - 9 个 HIL 节点 hard pause
  - 走 v2.0.4 推荐调用模式（write_single_node + apply_user_decision + bypass_scarcity）
  - 不直接调 outline_update_status（避免 B-2 bug）

用法：
  python3 scripts/run_workflow.py <paper_name>               # auto 模式
  python3 scripts/run_workflow.py <paper_name> --phase phase1  # 指定阶段
  python3 scripts/run_workflow.py <paper_name> --status     # 仅查看状态
"""

import argparse
import io
import json
import os
import subprocess
import sys
import threading
import urllib.request
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR))

from orchestrator_v2 import (
    orchestrate, orchestrate_phase1_1, orchestrate_phase2,
    orchestrate_phase3, orchestrate_phase3_5, orchestrate_phase4, orchestrate_phase5,
    confirm_phase3_and_export,
    confirm_phase1_3, write_single_node, apply_user_decision,
    check_info_scarcity, confirm_phase1, skip_phase1_3
)


# ==================== Windows UTF-8 兼容 ====================

def _ensure_utf8_stdout():
    """修复 Windows GBK 编码问题"""
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(
            sys.stdout.buffer,
            encoding='utf-8',
            errors='replace'
        )
        sys.stderr = io.TextIOWrapper(
            sys.stderr.buffer,
            encoding='utf-8',
            errors='replace'
        )
from state_manager_v2 import (
    load_orchestrate_state, save_orchestrate_state,
    outline_load, outline_get_node, init_orchestrate_state
)
from node_writer import write_node, extract_key_conclusion_from_response

WORKSPACE = Path(os.environ.get(
    "THESIS_WORKSPACE",
    os.path.expanduser("~/.openclaw/workspace")
))


# ============================================================
# RuntimeLLM：从当前运行 session 动态获取模型配置
# ============================================================
# 信息来源：
#   1. openclaw sessions list --all-agents --active 30 --json → 当前 session（零硬编码）
#   2. agent plugin catalog → provider baseUrl + apiKey
# ============================================================

class RuntimeLLM:
    """
    复用当前运行 session 的模型配置，构造 llm_func。

    完全零硬编码 agent_id / model / API key。
    动态从以下位置读取：
      - openclaw sessions list --all-agents --active 30 --json → 当前 session 模型名 + provider
      - agent plugin catalog → provider baseUrl + apiKey + apiType
    """

    def __init__(self, agent_id: Optional[str] = None):
        self._session_info: Optional[Dict] = None
        self._lock = threading.Lock()

    # ---- 内部：获取当前 agent 的 openclaw 可执行文件路径 ----
    @staticmethod
    def _find_openclaw() -> str:
        """查找 openclaw CLI 路径"""
        # 1. 尝试 nvm node 目录下的 openclaw
        home = Path.home()
        nvm_openclaw = (
            home / ".nvm/versions/node/v24.14.0/bin/openclaw"
        )
        if nvm_openclaw.exists():
            return str(nvm_openclaw)

        # 2. 尝试 PATH 中的 openclaw
        for path in os.environ.get("PATH", "").split(os.pathsep):
            candidate = Path(path) / "openclaw"
            if candidate.exists() and not candidate.is_dir():
                return str(candidate)

        raise RuntimeError("找不到 openclaw CLI，请确保已安装并位于 PATH 中")

    # ---- 内部：从当前运行 session 获取模型信息 ----
    def _get_session_info(self) -> Dict:
        """
        通过 openclaw sessions list --all-agents --active 30 获取当前 session 信息。

        零硬编码：不传 --agent 参数，由 Gateway 自动识别当前调用者 session。
        """
        try:
            openclaw_path = self._find_openclaw()
            result = subprocess.run(
                [openclaw_path, "sessions", "list",
                 "--all-agents",
                 "--active", "30",
                 "--json"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode != 0:
                raise RuntimeError(f"openclaw sessions list failed: {result.stderr}")

            data = json.loads(result.stdout)
            sessions = data.get("sessions", [])
            if not sessions:
                raise RuntimeError("未找到活跃 session（30分钟内）")

            # sessions[0] 就是当前调用者的 session（Gateway 自动路由）
            current = sessions[0]
            session_key = current.get("key", "")  # e.g. agent:zz:feishu:direct:ou_xxx

            # 从 session key 解析 agent_id
            parts = session_key.split(":")
            agent_id = parts[1] if len(parts) >= 2 else "unknown"

            return {
                "model": current.get("model", ""),
                "provider": current.get("modelProvider", ""),
                "agent_id": agent_id,
                "session_key": session_key,
            }
        except subprocess.TimeoutExpired:
            raise RuntimeError("openclaw sessions list 超时")
        except Exception as e:
            raise RuntimeError(f"读取 session 信息失败: {e}")

    # ---- 内部：从 agent plugin catalog 读取 provider 凭证 ----
    def _get_provider_config(self, provider: str, agent_id: str) -> Dict:
        """
        从 ~/.openclaw/agents/{agent_id}/agent/plugins/*/catalog.json 读取凭证。

        plugin 目录名（如 minimax）可能与 provider 名（如 minimax-cn）不同，
        所以需要扫描 plugins/ 下所有子目录，找包含目标 provider 的 catalog。
        """
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
                        # 找到了包含目标 provider 的 catalog
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
        # 精确匹配 provider，再尝试 minimax-cn 作为 fallback
        cfg = providers.get(provider) or providers.get("minimax-cn", {})

        if not cfg:
            raise RuntimeError(f"provider '{provider}' 未在 catalog 中找到")

        return {
            "base_url": cfg["baseUrl"],
            "api_key": cfg["apiKey"],
            "api_type": cfg.get("api", "anthropic-messages"),
        }

    # ---- 公开接口：构造 llm_func ----
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
                # openai-completions 格式（deepseek 等）
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

        # 从 content 数组中提取 type=="text" 的块
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
        return result["choices"][0]["message"]["content"]

    def current_model(self) -> str:
        """返回当前 session 使用的模型"""
        if self._session_info is None:
            with self._lock:
                if self._session_info is None:
                    self._session_info = self._get_session_info()
        return self._session_info["model"]

    def current_agent_id(self) -> str:
        """返回当前 agent ID"""
        if self._session_info is None:
            with self._lock:
                if self._session_info is None:
                    self._session_info = self._get_session_info()
        return self._session_info["agent_id"]


# 全局单例（延迟初始化）
_runtime_llm: Optional[RuntimeLLM] = None


def get_runtime_llm() -> RuntimeLLM:
    """获取 RuntimeLLM 全局单例"""
    global _runtime_llm
    if _runtime_llm is None:
        _runtime_llm = RuntimeLLM()
    return _runtime_llm


# ============================================================
# Pre-flight Check：依赖检测 + 自动安装
# ============================================================

from enum import Enum


class DepStatus(Enum):
    OK = "ok"          # 可用
    MISSING = "missing" # 缺失（不可安装）
    INSTALLABLE = "installable"  # 可安装
    FAILED = "failed"   # 检测失败（不阻断）


class Dependency:
    def __init__(self, name: str, check_fn, install_cmd: str = None,
                 install_fn=None, required: bool = False,
                 block_on_fail: bool = False,
                 description: str = "",
                 install_category: str = "silent"):
        """
        install_category:
          - "silent":   pip/pipx 等无交互命令，可直接 subprocess 自动执行
          - "needs_ai": openclaw skills / mcp 等可能有交互式确认，需 AI 触发
        """
        self.name = name
        self.check_fn = check_fn
        self.install_cmd = install_cmd
        self.install_fn = install_fn
        self.required = required
        self.block_on_fail = block_on_fail
        self.description = description
        self.install_category = install_category  # "silent" | "needs_ai"
        self.status: DepStatus = DepStatus.MISSING
        self.version: str = ""
        self.error: str = ""
        self.can_auto_install: bool = install_fn is not None

    def check(self) -> "Dependency":
        try:
            result = self.check_fn()
            self.status = DepStatus.OK
            self.version = str(result) if result and result is not True else ""
        except Exception as e:
            self.error = str(e)
            if self.can_auto_install:
                self.status = DepStatus.INSTALLABLE
            else:
                self.status = DepStatus.MISSING if self.required else DepStatus.FAILED
        return self

    def try_install(self) -> "Dependency":
        """
        仅执行 silent 类安装。needs_ai 类由 AI 触发，不在此执行。
        """
        if self.status != DepStatus.INSTALLABLE:
            return self
        if not self.install_fn:
            return self
        # needs_ai 类不在这儿执行，留给 AI
        if self.install_category == "needs_ai":
            return self
        try:
            print(f"\n📦 正在安装 {self.name}...")
            self.install_fn()
            self.check()
            if self.status == DepStatus.OK:
                print(f"✅ {self.name} 安装成功")
            else:
                print(f"❌ {self.name} 安装失败: {self.error}")
        except Exception as e:
            self.error = str(e)
            self.status = DepStatus.FAILED
            print(f"❌ {self.name} 自动安装失败: {e}")
        return self

    def status_icon(self) -> str:
        if self.status == DepStatus.OK:
            return "🟢"
        elif self.status == DepStatus.INSTALLABLE:
            return "🔴"
        elif self.status == DepStatus.MISSING:
            return "🔴"
        else:
            return "🟡"


# ---- 各依赖检测函数 ----

def _check_openclaw_cli():
    # 环境变量 THESIS_SKIP_CLI_CHECK=1 时跳过 OpenClaw CLI 检测
    if os.environ.get("THESIS_SKIP_CLI_CHECK") == "1":
        return True
    openclaw_path = RuntimeLLM._find_openclaw()
    result = subprocess.run(
        [openclaw_path, "gateway", "status", "--deep"],
        capture_output=True, text=True, timeout=15
    )
    if result.returncode != 0:
        raise RuntimeError("gateway not responding")
    return True


def _check_python_docx():
    import docx
    return True


def _check_hermes():
    result = subprocess.run(
        ["hermes", "--version"],
        capture_output=True, text=True, timeout=10
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr or "not found")
    return result.stdout.strip()


def _install_hermes():
    # 优先用 pipx，其次 pip
    for cmd in [["pipx", "install", "hermes-ai"], ["pip", "install", "hermes-ai"]]:
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if r.returncode == 0:
                return
        except Exception:
            continue
    raise RuntimeError("pipx/pip 安装均失败，请手动安装 hermes-ai")


def _check_tavily_mcp():
    result = subprocess.run(
        ["mcporter", "call", "tavily-mcp.tavily_search",
         '{"query":"test","max_results":1}'],
        capture_output=True, text=True, timeout=20
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr or "tavily-mcp not available")
    # 验证返回数据
    data = json.loads(result.stdout)
    if "error" in data:
        raise RuntimeError(data["error"])
    return True


def _install_tavily_mcp():
    r = subprocess.run(
        ["mcp", "install", "tavily-mcp"],
        capture_output=True, text=True, timeout=60
    )
    if r.returncode != 0:
        raise RuntimeError(r.stderr or "mcp install failed")


def _check_mineru():
    import importlib
    m = importlib.import_module("mineru_open_api")
    return getattr(m, "__version__", "unknown")


def _install_mineru():
    r = subprocess.run(
        [sys.executable, "-m", "pip", "install", "mineru-open-api>=0.5.0"],
        capture_output=True, text=True, timeout=120
    )
    if r.returncode != 0:
        raise RuntimeError(r.stderr or "pip install failed")


def _check_skill(name: str):
    """检查 skill 是否已安装"""
    openclaw_path = RuntimeLLM._find_openclaw()
    result = subprocess.run(
        [openclaw_path, "skills", "list", "--json"],
        capture_output=True, text=True, timeout=10
    )
    if result.returncode != 0:
        raise RuntimeError("openclaw skills list failed")
    data = json.loads(result.stdout)
    installed = [s.get("name") for s in data.get("skills", [])]
    if name not in installed:
        raise RuntimeError(f"skill '{name}' not installed")
    return True


def _install_skill(name: str):
    openclaw_path = RuntimeLLM._find_openclaw()
    r = subprocess.run(
        [openclaw_path, "skills", "install", name],
        capture_output=True, text=True, timeout=60
    )
    if r.returncode != 0:
        raise RuntimeError(r.stderr or "install failed")


def _install_python_pkg(cmd: list):
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError(r.stderr or "pip install failed")


# ---- Pre-flight Check 主函数 ----

def preflight_check(skip_install: bool = False) -> Tuple[bool, list, list]:
    """
    执行所有依赖检测。

    - silent 类依赖：自动安装
    - needs_ai 类依赖：返回 needs_ai_deps，由 AI 触发安装

    返回 (can_proceed, deps_list, needs_ai_deps)
    """
    deps = [
        # P0: 必需环境
        Dependency(
            "OpenClaw CLI", _check_openclaw_cli,
            required=True, block_on_fail=True,
            description="RuntimeLLM 和 Skill 管理依赖"
        ),
        Dependency(
            "python-docx", _check_python_docx,
            install_fn=lambda: _install_python_pkg(
                [sys.executable, "-m", "pip", "install", "python-docx"]
            ),
            required=True, block_on_fail=True,
            description="Word 文档读写"
        ),

        # P1: 建议安装（可降级）
        Dependency(
            "Hermes CLI", _check_hermes,
            install_cmd="pipx install hermes-ai  或  pip install hermes-ai",
            install_fn=_install_hermes,
            required=False, block_on_fail=False,
            description="版本H起草引擎（深度逻辑链），可降级到版本O",
            install_category="silent"
        ),
        Dependency(
            "Tavily MCP", _check_tavily_mcp,
            install_cmd="mcp install tavily-mcp",
            install_fn=_install_tavily_mcp,
            required=False, block_on_fail=False,
            description="网络搜索增强（可选，web_search 可替代）",
            install_category="needs_ai"  # 可能有交互式确认
        ),
        Dependency(
            "mineru-open-api", _check_mineru,
            install_cmd="pip install mineru-open-api>=0.5.0",
            install_fn=_install_mineru,
            required=False, block_on_fail=False,
            description="docx 解析增强（可选，降级到 python-docx）",
            install_category="silent"
        ),

        # P2: Skill（可选）
        Dependency(
            "academic-research (Skill)",
            lambda: _check_skill("academic-research"),
            install_cmd="openclaw skills install academic-research",
            install_fn=lambda: _install_skill("academic-research"),
            required=False, block_on_fail=False,
            description="学术文献检索",
            install_category="needs_ai"  # skill 安装需 AI 确认
        ),
        Dependency(
            "arxiv-search-collector (Skill)",
            lambda: _check_skill("arxiv-search-collector"),
            install_cmd="openclaw skills install arxiv-search-collector",
            install_fn=lambda: _install_skill("arxiv-search-collector"),
            required=False, block_on_fail=False,
            description="前沿论文追踪",
            install_category="needs_ai"  # skill 安装需 AI 确认
        ),
    ]

    # 执行检测
    print("\n" + "=" * 60)
    print("🔍 Pre-flight Check：依赖检测")
    print("=" * 60)

    for dep in deps:
        dep.check()
        icon = dep.status_icon()
        req_tag = " [必须]" if dep.required else ""
        if dep.status == DepStatus.OK:
            version_info = f" ({dep.version})" if dep.version else ""
            print(f"  {icon} {dep.name}{version_info}{req_tag}")
        elif dep.status == DepStatus.INSTALLABLE:
            print(f"  {icon} {dep.name}{req_tag} — 可自动安装")
            print(f"     安装命令: {dep.install_cmd}")
        elif dep.status == DepStatus.MISSING:
            print(f"  {icon} {dep.name}{req_tag} — 缺失")
        else:
            print(f"  {icon} {dep.name} — 检测失败（{dep.error[:40]}）")

    # 统计
    missing_required = [d for d in deps if d.required and d.status != DepStatus.OK]
    installable = [d for d in deps if d.status == DepStatus.INSTALLABLE]

    print()

    # 统计
    missing_required = [d for d in deps if d.required and d.status != DepStatus.OK]
    installable_silent = [d for d in deps if d.status == DepStatus.INSTALLABLE and d.install_category == "silent"]
    installable_ai = [d for d in deps if d.status == DepStatus.INSTALLABLE and d.install_category == "needs_ai"]

    print()

    # silent 类：自动安装
    if installable_silent and not skip_install:
        print(f"📦 尝试自动安装 {len(installable_silent)} 个依赖...")
        for dep in installable_silent:
            dep.try_install()
            icon = dep.status_icon()
            if dep.status == DepStatus.OK:
                print(f"  {icon} {dep.name} ✅ 已安装")
            else:
                print(f"  {icon} {dep.name} ❌ 安装失败（{dep.error[:40]}）")
        print()

    # needs_ai 类：返回给 AI 触发（不在这儿执行）
    if installable_ai:
        print(f"🤖 以下 {len(installable_ai)} 个依赖需要 AI 触发安装：")
        for d in installable_ai:
            print(f"   🔸 {d.name}: {d.install_cmd}")
        print()

    # 最终判断
    failed_required = [d for d in deps if d.required and d.status != DepStatus.OK]
    if failed_required:
        names = ", ".join(d.name for d in failed_required)
        print(f"❌ Pre-flight 失败：缺少必须依赖 {names}")
        print("   请手动安装后重试")
        return False, deps

    # 最终判断
    failed_required = [d for d in deps if d.required and d.status != DepStatus.OK]
    if failed_required:
        names = ", ".join(d.name for d in failed_required)
        print(f"❌ Pre-flight 失败：缺少必须依赖 {names}")
        print("   请手动安装后重试")
        return False, deps, []

    # 重新统计（安装后可能有些变成了 OK）
    still_installable = [d for d in deps if d.status == DepStatus.INSTALLABLE]
    needs_ai_deps = [d for d in still_installable if d.install_category == "needs_ai"]

    if needs_ai_deps:
        print(f"🤖 以下依赖需要 AI 触发安装：")
        for d in needs_ai_deps:
            print(f"   🔸 {d.name}: {d.install_cmd}")
        print()

    if installable_silent and not skip_install:
        still_failed = [d for d in installable_silent if d.status != DepStatus.OK]
        if still_failed:
            print(f"🟡 以下依赖自动安装失败，可降级使用：")
            for d in still_failed:
                print(f"   - {d.name}: {d.install_cmd}")
            print()

    print("✅ Pre-flight Check 通过")
    return True, deps, needs_ai_deps


# ============================================================
# HIL 硬暂停工具
# ============================================================

def hil_pause(hil_id: str, message: str, options: Optional[Dict[str, str]] = None) -> str:
    """HIL 硬暂停：打印清晰提示，等用户输入决策"""
    print()
    print("=" * 60)
    print(f"🛑 HIL #{hil_id}")
    print("=" * 60)
    print(message)
    if options:
        print("\n可选决策：")
        for k, v in options.items():
            print(f"  [{k}] {v}")
    print()

    while True:
        try:
            choice = input("请输入决策（输入 quit 退出）: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n⚠️ 输入中断，退出")
            sys.exit(0)

        if choice == "quit":
            sys.exit(0)

        if options and choice in options:
            return choice

        if not options and choice in ("", "y", "yes", "确认", "ok"):
            return choice

        print(f"⚠️ 无效输入: {choice}，请重新选择")


def get_paper_status(paper_name: str) -> Optional[Dict[str, Any]]:
    """打印当前 paper 状态"""
    state = load_orchestrate_state(paper_name)
    if not state:
        print(f"❌ 论文 {paper_name} 状态文件不存在")
        return None

    print(f"=== {paper_name} 状态 ===")
    print(f"  phase: {state.get('phase')}")
    print(f"  phase1_confirmed: {state.get('phase1_confirmed')}")
    print(f"  phase1_3_status: {state.get('phase1_3_status')}")
    print(f"  current_node_id: {state.get('current_node_id')}")
    print(f"  completed_nodes: {state.get('completed_nodes', [])}")
    print(f"  pending_review: {state.get('pending_review', [])}")
    print(f"  failed_nodes: {state.get('failed_nodes', [])}")
    progress = state.get('progress', {})
    print(f"  progress: {progress.get('completed', 0)}/{progress.get('total', 0)}")
    audit = state.get('audit_log', [])
    if audit:
        print(f"  audit_log: {len(audit)} 条")
    return state


# ============================================================
# Phase 1: 规划与归因
# ============================================================

def run_phase1(paper_name: str, llm_func: Optional[Callable] = None) -> bool:
    """Phase 1: 解析 + 大纲确认 + Phase 1.3"""
    state = load_orchestrate_state(paper_name)

    # Phase 1.1: 解析入口
    if not state:
        print(f"\n📝 Phase 1.1: 初始化论文 {paper_name}")
        print("  请提供开题报告 docx 路径（直接回车 = 手动录入文本）")
        try:
            docx_path = input("  docx 路径: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n⚠️ 输入中断")
            return False

        if docx_path and Path(docx_path).exists():
            r = orchestrate(paper_name, action="phase1_1_init",
                          input_type="docx", input_data=docx_path,
                          llm_func=llm_func)
        elif docx_path:
            print(f"❌ 文件不存在: {docx_path}")
            return False
        else:
            print("\n请粘贴开题报告文本（Ctrl+D 结束）:")
            lines = []
            try:
                while True:
                    line = input()
                    lines.append(line)
            except EOFError:
                pass
            outline_text = "\n".join(lines)
            if not outline_text.strip():
                print("❌ 文本为空，无法解析")
                return False
            r = orchestrate(paper_name, action="phase1_1_init",
                          input_type="text", input_data=outline_text,
                          llm_func=llm_func)

        if not r.get("ok"):
            print(f"❌ Phase 1.1 失败: {r.get('error')}")
            return False

        node_count = len(r.get("outline", {}).get("outline_tree", {}).get("nodes", []))
        print(f"✅ Phase 1.1 完成: 解析 {node_count} 个节点")

    # HIL #1: 大纲确认
    outline = outline_load(paper_name)
    nodes = outline["outline"]["outline_tree"]["nodes"]
    print(f"\n📋 论文大纲（共 {len(nodes)} 节点）:")
    for n in nodes[:30]:
        marker = " [虚拟]" if n.get("is_virtual") else ""
        print(f"  - {n['id']:10s} | L{n['level']} | {n['title']}{marker}")
    if len(nodes) > 30:
        print(f"  ... 还有 {len(nodes) - 30} 节点")

    hil_pause("1", "以上大纲结构是否准确？",
             {"1": "确认（进入归因分析）",
              "2": "取消（修改后重跑）"})

    # Phase 1.2: 大纲确认
    r = orchestrate(paper_name, action="phase1_confirm")
    if not r.get("ok"):
        print(f"❌ Phase 1.2 confirm 失败: {r.get('error')}")
        return False
    print(f"✅ Phase 1.2 完成: 大纲已确认")

    # ── Phase 1.3 归因分析（两步走：先 submit，再等用户确认归因） ──
    state = load_orchestrate_state(paper_name)

    # 处理旧状态（v2.0.6 前的 skipped 状态需重新走）
    if state.get("phase1_3_status") == "skipped":
        print(f"\n⚠️ Phase 1.3 状态为 skipped（需重新走）")
        state["phase1_3_status"] = "pending"

    if state.get("phase1_3_status") == "confirmed":
        print(f"\n✅ Phase 1.3 已确认，跳过")
        print(f"\n✅ Phase 1 全部完成")
        return True

    if state.get("phase1_3_status") == "submitted":
        print(f"\n📄 Phase 1.3 已提交，显示归因结果...")
    else:
        # phase1_3_status == "pending"：需要 submit
        existing_path = state.get("phase1_3_docx_path")
        if not existing_path or not Path(existing_path).exists():
            print(f"\n📄 Phase 1.3: 需要开题报告做归因")
            print(f"  ⚠️ 拍板 #1：Phase 1.3 不允许跳过")
            try:
                new_path = input("  请输入开题报告 docx 路径（必填）: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n⚠️ 输入中断")
                return False
            if not new_path or not Path(new_path).exists():
                print("❌ 必须提供有效的 docx 路径，无法继续")
                return False
            existing_path = new_path
        else:
            print(f"\n📄 发现已有 docx: {existing_path}")

        # 提交归因分析（silent）
        r = orchestrate(paper_name, action="phase1_3_submit",
                       docx_path=existing_path, llm_func=llm_func)
        if not r.get("ok"):
            print(f"❌ Phase 1.3 submit 失败: {r.get('error')}")
            return False
        print(f"✅ Phase 1.3 submit 完成")

    # 显示归因结果（章节 → 研究问题映射表）
    p13_result = state.get("phase1_3_result", {})
    summary = p13_result.get("summary", {})
    node_details = p13_result.get("node_details", {})

    print(f"\n" + "=" * 60)
    print(f"📊 Phase 1.3 归因分析")
    print(f"=" * 60)
    print(f"  总段落数: {summary.get('total_paragraphs', '?')}")
    print(f"  直接匹配段落: {summary.get('matched_paragraphs', '?')}")
    print(f"  AI 补充分类: {summary.get('ai_classified', '?')}")

    # 章节 → 研究问题 映射表（静态硬编码，与 outline 一致）
    outline = outline_load(paper_name)
    nodes = outline["outline"]["outline_tree"]["nodes"]

    print(f"\n  研究问题 → 章节映射:")
    print(f"  ┌──────────────────────────────────────────────────────────┐")
    print(f"  │ 子问题1（环境与痛点识别）                               │")
    print(f"  │   → 第3章：外部环境分析（PEST + 波特五力 + EFE矩阵）    │")
    print(f"  │   → 第4章：内部环境分析（RBV + VRIO + IFE矩阵）        │")
    print(f"  ├──────────────────────────────────────────────────────────┤")
    print(f"  │ 子问题2（战略匹配与选择）                               │")
    print(f"  │   → 第5章：竞争战略选择（SWOT + QSPM）                 │")
    print(f"  ├──────────────────────────────────────────────────────────┤")
    print(f"  │ 子问题3（战略实施与保障）                               │")
    print(f"  │   → 第6章：战略实施与保障（AI分发 + 组织/技术/合规）   │")
    print(f"  └──────────────────────────────────────────────────────────┘")
    print(f"  逻辑链：分析（第3-4章）→ 决策（第5章）→ 落地（第6章）")

    if node_details:
        print(f"\n  各节点 content_hint（前 10 个）:")
        for nid, info in list(node_details.items())[:10]:
            hint_preview = (info.get("content_hint", "") or "")[:70]
            matched = info.get("matched_paragraphs", [])
            src = "[直接匹配]" if matched else "[AI 补充]"
            print(f"    {nid:10s} {src} {hint_preview}...")

    print()

    # HIL #2: 归因确认（关键：用户必须明确回复才能推进）
    choice = hil_pause("2", "以上归因分析是否与你的开题初衷一致？",
                     {"1": "一致（确认归因，进入 Phase 2）",
                      "2": "调整 hint（暂停，人工修改后继续）",
                      "3": "取消"})

    if choice == "1":
        # 接受归因 → confirm_phase1_3
        r = orchestrate(paper_name, action="phase1_3_confirm")
        if not r.get("ok"):
            print(f"❌ Phase 1.3 confirm 失败: {r.get('error')}")
            return False
        print(f"✅ Phase 1.3 完成: 归因已确认，进入 Phase 2")

    elif choice == "2":
        # 用户要手动调整 hint → 告知路径，退出等待人工干预
        print(f"\n⏸️ 已暂停。请人工修改 content_hint 后重新运行本脚本。")
        print(f"   状态已保存，修改后从当前断点继续。")
        return False

    elif choice == "3":
        print(f"\n❌ 用户取消，退出")
        return False

    print(f"\n✅ Phase 1 全部完成")
    return True


# ============================================================
# Phase 2: 写作循环
# ============================================================

def run_phase2(paper_name: str, llm_func: Callable) -> bool:
    """Phase 2: 写作循环（v2.0.4 推荐调用模式）"""
    state = load_orchestrate_state(paper_name)
    if not state:
        print("❌ 状态文件不存在，请先跑 Phase 1")
        return False
    if state.get("phase1_3_status") != "confirmed":
        print(f"❌ Phase 1.3 未确认（当前: {state.get('phase1_3_status')}）")
        return False
    if not llm_func:
        print("❌ Phase 2 需要 llm_func 参数")
        return False

    total = state.get('progress', {}).get('total', 0)
    print(f"\n📝 Phase 2: 逐节点写作（共 {total} 节点）")

    iteration_count = 0
    max_iterations = total * 3  # 防止无限循环

    while iteration_count < max_iterations:
        iteration_count += 1

        # 找下一个未完成节点
        outline = outline_load(paper_name)
        nodes = outline["outline"]["outline_tree"]["nodes"]
        state = load_orchestrate_state(paper_name)

        next_node_id = None
        for n in nodes:
            if n.get("is_virtual"):
                continue  # 虚拟节点跳过
            if n["id"] not in state.get("completed_nodes", []) and \
               n["id"] not in state.get("failed_nodes", []):
                next_node_id = n["id"]
                break

        if not next_node_id:
            print(f"\n✅ 所有节点已完成")
            break

        # v2.0.4 推荐路径：write_single_node（内部含 check_info_scarcity + LLM + review）
        result = write_single_node(paper_name, next_node_id, llm_func, bypass_scarcity=False)

        if not result.get("ok"):
            print(f"❌ 节点 {next_node_id} 失败: {result.get('error')}")
            return False

        action = result.get("action")

        if action == "needs_user_input":
            # HIL #3: info_scarcity 触发
            scarcity = check_info_scarcity(paper_name, next_node_id)
            missing = scarcity.get("missing_sources", [])
            current_info = scarcity.get("current_info", {})
            node_title = scarcity.get("node_title", next_node_id)

            print(f"\n⚠️ 节点 {next_node_id} ({node_title}) 信息贫瘠")
            print(f"  缺失项: {missing}")
            print(f"  现有信息:")
            print(f"    content_hint: {(current_info.get('content_hint') or '(空)')[:80]}")
            print(f"    user_hints: {current_info.get('user_hints', [])}")
            print(f"    bridge_source: {current_info.get('bridge_source', '(无)')}")

            choice = hil_pause("3", f"节点 {next_node_id} 决策",
                             {"1": "用户提供 content_hint",
                              "2": "AI 自行生成",
                              "3": "跳过该节点"})

            if choice == "1":
                try:
                    new_hint = input(f"  请输入 {next_node_id} 的 content_hint: ").strip()
                except (EOFError, KeyboardInterrupt):
                    return False
                apply_user_decision(paper_name, next_node_id, "1", user_hint=new_hint)
                # 重新调 write_single_node（bypass_scarcity=True 因为 hint 已更新）
                result = write_single_node(paper_name, next_node_id, llm_func, bypass_scarcity=True)
                action = result.get("action")

            elif choice == "2":
                apply_user_decision(paper_name, next_node_id, "2")
                # 重新调 write_single_node
                result = write_single_node(paper_name, next_node_id, llm_func, bypass_scarcity=True)
                action = result.get("action")

            elif choice == "3":
                apply_user_decision(paper_name, next_node_id, "3")
                print(f"  ⏭️ 节点 {next_node_id} 已跳过（failed_nodes）")
                continue

        if action == "completed":
            quality = result.get("review_result", {}).get("quality", "medium")
            wc = result.get("word_count", 0)
            print(f"  ✅ {next_node_id} 完成 | 质量: {quality} | 字数: {wc}")

        elif action == "pending_review":
            # HIL #4: 评审质量 medium/low
            quality = result.get("review_result", {}).get("quality")
            summary = result.get("review_result", {}).get("summary", "")
            weaknesses = result.get("review_result", {}).get("weaknesses", [])
            suggestions = result.get("review_result", {}).get("suggestions", [])

            print(f"\n⚠️ 节点 {next_node_id} 评审质量: {quality}")
            if summary:
                print(f"  总结: {summary[:200]}")
            if weaknesses:
                print(f"  问题: {weaknesses}")
            if suggestions:
                print(f"  建议: {suggestions}")

            choice = hil_pause("4", f"节点 {next_node_id} 评审结果",
                             {"1": "接受（标记 completed）",
                              "2": "重写（再调一次 write_single_node）",
                              "3": "跳过该节点"})

            if choice == "1":
                # 接受：同步 outline state（reviewing → completed）+ orchestrate state
                from state_manager_v2 import outline_update_status
                outline_update_status(paper_name, next_node_id, "completed", force=True)
                state = load_orchestrate_state(paper_name)
                if next_node_id not in state.get("completed_nodes", []):
                    state["completed_nodes"].append(next_node_id)
                if next_node_id in state.get("pending_review", []):
                    state["pending_review"].remove(next_node_id)
                from state_manager_v2 import update_progress
                update_progress(state)
                save_orchestrate_state(paper_name, state)
                print(f"  ✅ {next_node_id} 已接受")

            elif choice == "2":
                # 重写：调 write_single_node 一次（bypass_scarcity=True 跳过信息检查）
                rewrite_result = write_single_node(paper_name, next_node_id, llm_func, bypass_scarcity=True)
                rewrite_action = rewrite_result.get("action")
                if rewrite_action == "completed":
                    # 重写后评审 high → 直接 completed
                    from state_manager_v2 import outline_update_status
                    outline_update_status(paper_name, next_node_id, "completed", force=True)
                    state = load_orchestrate_state(paper_name)
                    if next_node_id not in state.get("completed_nodes", []):
                        state["completed_nodes"].append(next_node_id)
                    if next_node_id in state.get("pending_review", []):
                        state["pending_review"].remove(next_node_id)
                    from state_manager_v2 import update_progress
                    update_progress(state)
                    save_orchestrate_state(paper_name, state)
                    print(f"  ✅ {next_node_id} 重写后评审通过")
                elif rewrite_action == "pending_review":
                    # 重写后仍 medium/low → 保持 pending_review，等用户再次决策
                    print(f"  🔄 {next_node_id} 已重写，仍需确认（质量: {rewrite_result.get('review_result', {}).get('quality', 'medium')}）")
                else:
                    # error 或 needs_user_input
                    print(f"  ⚠️ {next_node_id} 重写异常: {rewrite_result.get('error', rewrite_action)}")

            elif choice == "3":
                # 跳过
                state = load_orchestrate_state(paper_name)
                if next_node_id not in state.get("failed_nodes", []):
                    state["failed_nodes"].append(next_node_id)
                if next_node_id in state.get("pending_review", []):
                    state["pending_review"].remove(next_node_id)
                from state_manager_v2 import update_progress
                update_progress(state)
                save_orchestrate_state(paper_name, state)
                print(f"  ⏭️ {next_node_id} 已跳过")

        elif action == "error":
            print(f"❌ 节点 {next_node_id} 写入失败")
            return False

    # HIL #5: Phase 2 完成确认
    state = load_orchestrate_state(paper_name)
    progress = state.get("progress", {})
    completed_count = progress.get('completed', 0)
    failed_count = progress.get('failed', 0)
    total = progress.get('total', 0)

    print(f"\n📊 Phase 2 完成: {completed_count}/{total} 节点 completed，{failed_count} failed")
    hil_pause("5", "Phase 2 内容是否接受？",
             {"1": "确认（进入 Phase 3）",
              "2": "返回修改（重新跑某个节点）"})

    # 推进 phase 到 phase3
    state["phase"] = "phase3"
    save_orchestrate_state(paper_name, state)
    print(f"✅ Phase 2 确认完成")
    return True


# ============================================================
# Phase 3: 整合
# ============================================================

def run_phase3(paper_name: str) -> bool:
    """Phase 3: 整合 + 导出"""
    state = load_orchestrate_state(paper_name)
    if state.get("phase") != "phase3":
        print(f"❌ Phase 2 未完成（当前 phase: {state.get('phase')}）")
        return False

    # 整合
    print(f"\n📝 Phase 3: 整合所有节点内容")
    r = orchestrate_phase3(paper_name)
    if not r.get("ok"):
        print(f"❌ Phase 3 整合失败: {r.get('error')}")
        return False

    # HIL #6: 整合版预览
    content = r.get("content", "")
    word_count = r.get("word_count", 0)
    print(f"\n📊 整合版生成: {word_count} 字符")
    print(f"\n--- 前 1000 字预览 ---")
    print(content[:1000])
    print(f"\n...（共 {word_count} 字符）...")

    hil_pause("6", "整合版是否接受？",
             {"1": "确认（进入 Phase 5 导出）",
              "2": "取消（修改）"})

    # Phase 5 export
    print(f"\n📤 Phase 5: 导出 Word")
    r = confirm_phase3_and_export(paper_name)
    if not r.get("ok"):
        print(f"❌ Phase 5 export 失败: {r.get('error')}")
        return False

    output_path = r.get("output_path")
    print(f"✅ 论文已导出: {output_path}")
    print(f"   字数: {r.get('word_count')}")

    # HIL #9: Word 输出确认
    hil_pause("9", "Word 文档是否接受？\n"
                  "（如需 md → docx 转换，请运行 md2docx_strict.py）",
             {"1": "接受（流程结束）",
              "2": "修改"})

    print(f"\n🎉 流程结束")
    return True


# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="thesis-workflow v2 真实入口 CLI（v2.0.6 新增）"
    )
    parser.add_argument("paper_name", help="论文标识（与 orchestrate_state 文件名一致）")
    parser.add_argument("--phase", choices=["phase1", "phase2", "phase3", "phase3_5", "phase4", "phase5", "auto"],
                       default="auto", help="指定阶段")
    parser.add_argument("--status", action="store_true", help="仅查看状态")
    parser.add_argument("--llm", help="指定 LLM 模型（留空则自动从当前 session 获取）")
    parser.add_argument("--agent-id", default=None,
                       help="agent ID（留空则从当前 session 自动推断，仅用于多 agent 场景）")
    args = parser.parse_args()

    paper_name = args.paper_name

    print(f"=== thesis-workflow v2.0.6 CLI ===")
    print(f"  论文: {paper_name}")
    print(f"  模式: {args.phase}")

    # ── Pre-flight Check ──────────────────────────────────────
    can_proceed, deps, needs_ai_deps = preflight_check()
    if not can_proceed:
        return 1

    # needs_ai 类依赖：打印安装指令，由调用方 AI 触发
    if needs_ai_deps:
        print()
        print("=" * 60)
        print("🤖 需要 AI 触发安装以下依赖：")
        print("=" * 60)
        for d in needs_ai_deps:
            print(f"  🔸 {d.name}")
            print(f"     命令: {d.install_cmd}")
        print()
        print("请在 OpenClaw 主 session 中执行安装命令后，再运行本脚本。")
        print("=" * 60)
        return 2  # 返回特殊码，告知调用方需要 AI 介入

    if args.status:
        get_paper_status(paper_name)
        return 0

    llm_func = None

    if args.phase in ("phase1", "auto"):
        # Phase 1.3 需要 llm_func
        try:
            rllm = get_runtime_llm()
            if args.llm:
                # 用户指定了模型
                model = args.llm
                llm_func = rllm.make_llm_func(model=model)
                print(f"✅ 使用指定模型: {model}")
            else:
                # 自动从当前 session 获取
                model = rllm.current_model()
                llm_func = rllm.make_llm_func()
                print(f"✅ 自动使用当前 session 模型: {model}")
        except Exception as e:
            print()
            print("=" * 60)
            print("❌ 无法获取运行中 session 配置（Phase 1.3 需要 llm_func）")
            print("=" * 60)
            print(f"   错误: {e}")
            print()
            print("解决方案：")
            print("   1. 确保从 OpenClaw session 内调用本脚本（自动获取配置）")
            print("   2. 或通过 --llm 参数指定模型：")
            print("      python3 scripts/run_workflow.py <paper> --phase phase1 \\")
            print("        --llm MiniMax-M2.7")
            print()
            return 1

    if args.phase in ("phase2", "auto"):
        # Phase 2 llm_func：优先用 --llm 指定模型，否则自动从 session 获取
        if not llm_func:
            if args.llm:
                # 用户指定了模型名
                llm_func = get_runtime_llm().make_llm_func(model=args.llm)
                print(f"✅ 使用指定模型: {args.llm}")
            else:
                # 自动从 session 获取
                try:
                    rllm = get_runtime_llm()
                    model = rllm.current_model()
                    llm_func = rllm.make_llm_func()
                    print(f"✅ 自动使用当前 session 模型: {model}")
                except Exception as e:
                    print(f"❌ Phase 2 需要 llm_func，但无法获取 session 配置: {e}")
                    print("   请用 --llm 参数指定模型，或从 OpenClaw session 内调用")
                    return 1

    # 按 phase 执行
    if args.phase in ("phase1", "auto"):
        if not run_phase1(paper_name, llm_func):
            return 1

    if args.phase in ("phase2", "auto"):
        if not run_phase2(paper_name, llm_func):
            return 1

    if args.phase in ("phase3", "auto"):
        if not run_phase3(paper_name):
            return 1

    if args.phase in ("phase3_5", "auto"):
        print(f"\n📝 Phase 3.5: 深度学术评审")
        r = orchestrate_phase3_5(paper_name, llm_func=llm_func)
        if not r.get("ok"):
            print(f"❌ Phase 3.5 失败: {r.get('error')}")
            return 1

        # 审核 Loop：有 P0 → 自动修复 → 重审，直到无新 P0 或超 3 轮
        max_rounds = 3
        review_round = r.get("review_round", 1)
        while r.get("p0_count", 0) > 0 and review_round <= max_rounds:
            print(f"\n🔄 审核 Loop 第 {review_round} 轮：发现 {r.get('p0_count', 0)} 个 P0，自动修复...")
            from orchestrator_v2 import auto_fix_p0_issues
            fix_r = auto_fix_p0_issues(paper_name, llm_func=llm_func)
            if not fix_r.get("ok"):
                print(f"❌ P0 修复失败: {fix_r.get('error')}")
                break
            print(f"   已修复 {fix_r.get('fixed', 0)}/{fix_r.get('total', 0)} 个 P0")
            # 重审
            r = orchestrate_phase3_5(paper_name, llm_func=llm_func)
            if not r.get("ok"):
                print(f"❌ 重审失败: {r.get('error')}")
                break
            review_round = r.get("review_round", review_round + 1)

        if r.get("p0_count", 0) == 0:
            print(f"✅ Phase 3.5 通过（连续 2 轮无新 P0）")
        else:
            print(f"⚠️ Phase 3.5 超 {max_rounds} 轮仍有 P0，需人工介入")
        print(f"✅ Phase 3.5 完成")

    if args.phase in ("phase4", "auto"):
        print(f"\n📝 Phase 4: 整合修复")
        r = orchestrate_phase4(paper_name, llm_func=llm_func)
        if not r.get("ok"):
            print(f"❌ Phase 4 失败: {r.get('error')}")
            return 1
        print(f"✅ Phase 4 完成")

    if args.phase in ("phase5", "auto"):
        print(f"\n📝 Phase 5: 终审 + Word 输出")
        r = orchestrate_phase5(paper_name)
        if not r.get("ok"):
            print(f"❌ Phase 5 失败: {r.get('error')}")
            return 1
        print(f"✅ Phase 5 完成")

    print(f"\n🎉 全部完成")
    return 0


if __name__ == "__main__":
    _ensure_utf8_stdout()
    sys.exit(main())