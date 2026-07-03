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
from research_tools import get_runtime_llm
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
    openclaw_path = _find_openclaw()
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



def _check_tavily_mcp():
    # v2.1.2 平台适配:优先检测 OpenClaw,降级到 mcporter (Hermes 兼容)
    if _detect_openclaw_platform():
        return _check_openclaw_tavily_bridge()
    return _check_mcporter_tavily()


def _detect_openclaw_platform() -> bool:
    """检测是否在 OpenClaw runtime 环境(OPENCLAW_RUNTIME env 或 openclaw CLI 可用)"""
    if os.environ.get("OPENCLAW_RUNTIME"):
        return True
    try:
        _find_openclaw()
        return True
    except Exception:
        return False


def _check_openclaw_tavily_bridge() -> bool:
    """检测 OpenClaw 内置 Tavily MCP 桥接是否注册(通过 openclaw skills list)

    v2.1.2 修正:OpenClaw skill 名称是 'tavily-search' (不是 'tavily-mcp'),
    且 name 字段可能含 emoji 前缀,采用模糊匹配。
    """
    openclaw_path = _find_openclaw()
    result = subprocess.run(
        [openclaw_path, "skills", "list", "--json"],
        capture_output=True, text=True, timeout=10
    )
    if result.returncode != 0:
        raise RuntimeError("openclaw skills list failed")
    try:
        data = json.loads(result.stdout)
    except Exception as e:
        raise RuntimeError(f"openclaw skills list 输出解析失败: {e}")
    installed = [s.get("name", "") for s in data.get("skills", [])]
    # 模糊匹配:去除 emoji/空白后检查是否含 tavily
    normalized = [name.strip().lstrip("🔍⚙️🤖📝").strip().lower() for name in installed]
    if not any("tavily" in n for n in normalized):
        raise RuntimeError(
            "OpenClaw 平台下 tavily-search skill 未注册。"
            "请执行: openclaw skills install tavily-search"
        )
    return True


def _check_mcporter_tavily() -> bool:
    """mcporter 路径(Hermes 兼容,可能需要 ~/.local/bin/mcporter 桥接)"""
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
    openclaw_path = _find_openclaw()
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
    openclaw_path = _find_openclaw()
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

        Dependency(
            "Tavily MCP", _check_tavily_mcp,
            install_cmd="mcp install tavily-mcp",
            install_fn=_install_tavily_mcp,
            required=False, block_on_fail=False,
            description="网络搜索增强（v2.1.2:OpenClaw 走内置桥接；Hermes 走 mcporter）",
            install_category="none"  # v2.1.2:truly optional,不再卡 needs_ai_deps 流程
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

def hil_pause(hil_id: str, message: str, options: Optional[Dict[str, str]] = None,
             allow_extra: bool = False) -> str:
    """HIL 硬暂停:打印清晰提示,等用户输入决策

    Args:
        hil_id: HIL 编号(如 "1")
        message: 提示消息
        options: 选项字典 {key: description}
        allow_extra: 是否允许 key 后接附加内容(v2.1.2 公司映射用)
                   True 时,输入 "[1] vivo" 返回完整字符串 "[1] vivo"
                   False 时,只接受纯 key,附加内容会被拒绝
    """
    print()
    print("=" * 60)
    print(f"🛑 HIL #{hil_id}")
    print("=" * 60)
    print(message)
    if options:
        print("\n可选决策:")
        for k, v in options.items():
            print(f"  [{k}] {v}")
    print()

    while True:
        try:
            choice = input("请输入决策(输入 quit 退出): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n⚠️ 输入中断,退出")
            sys.exit(0)

        if choice == "quit":
            sys.exit(0)

        if options:
            # v2.1.2:allow_extra 模式:接受 "[key] extra" 格式
            if allow_extra:
                matched = next((k for k in options if choice.startswith(f"[{k}]") or choice == k), None)
                if matched:
                    return choice
            # 标准模式:只接受纯 key
            elif choice in options:
                return choice

        if not options and choice in ("", "y", "yes", "确认", "ok"):
            return choice

        print(f"⚠️ 无效输入: {choice},请重新选择")


def get_paper_status(paper_name: str) -> Optional[Dict[str, Any]]:
    """打印当前 paper 状态"""
    state = load_orchestrate_state(paper_name)
    if not state:
        print(f"⚠️ 论文 {paper_name} 状态文件不存在（尚未初始化）")
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

def run_phase1(paper_name: str) -> bool:
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
                          input_type="docx", input_data=docx_path)
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
                          input_type="text", input_data=outline_text)

        if not r.get("ok"):
            print(f"❌ Phase 1.1 失败: {r.get('error')}")
            return False

        node_count = len(r.get("outline", {}).get("outline_tree", {}).get("nodes", []))
        print(f"✅ Phase 1.1 完成: 解析 {node_count} 个节点")

        if r.get("hil_message"):
            print(f"\n{r['hil_message']}")

    # HIL #1: 大纲确认 + 公司映射(v2.1.2 新增)
    outline = outline_load(paper_name)
    nodes = outline["outline"]["outline_tree"]["nodes"]
    print(f"\n📋 论文大纲（共 {len(nodes)} 节点）:")
    for n in nodes[:30]:
        marker = " [虚拟]" if n.get("is_virtual") else ""
        print(f"  - {n['id']:10s} | L{n['level']} | {n['title']}{marker}")
    if len(nodes) > 30:
        print(f"  ... 还有 {len(nodes) - 30} 节点")

    # v2.1.2:从 state 读取公司映射信息以决定 HIL #1 选项
    state_pre_hil1 = load_orchestrate_state(paper_name) or {}
    company_info = state_pre_hil1.get("company_info") or {}
    code_name = company_info.get("code_name") or "(未提取)"

    print(f"\n📌 公司映射确认（v2.1.2 新增，HIL #1 必填）:")
    print(f"   code_name: {code_name}（已从开题报告自动提取）")
    print(f"   actual_name: ? ← 必须填写或显式跳过")
    print(f"   说明：该信息仅用于数据检索 + 写作锚定 + 脱敏校验")
    print(f"         不会进入最终 Word 文档")

    choice = hil_pause("1", "以上大纲结构是否准确？（需同时完成公司映射）",
                     {"1": f"确认 [填入 actual_name,例如:[1] vivo]",
                      "2": "跳过公司映射(actual_name=None,仅适用于纯理论论文)",
                      "3": "取消(修改后重跑)"},
                     allow_extra=True)

    # Phase 1.2: 大纲确认（带公司映射决策）
    r = orchestrate(paper_name, action="phase1_confirm", user_input=choice)
    if not r.get("ok"):
        print(f"❌ Phase 1.2 confirm 失败: {r.get('error')}")
        if "公司映射未填写" in r.get("error", ""):
            print(f"\n💡 提示：请重新运行脚本，输入 [1] <公司名> 或 [2] 跳过")
        return False
    ci_confirmed = r.get("company_info", {})
    actual_name = ci_confirmed.get("actual_name") or "(跳过)"
    print(f"✅ Phase 1.2 完成: 大纲已确认，公司映射 actual_name={actual_name}")

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
                       docx_path=existing_path)
        if not r.get("ok"):
            print(f"❌ Phase 1.3 submit 失败: {r.get('error')}")
            return False
        if r.get("hil_message"):
            print(f"\n{r['hil_message']}")
        print(f"✅ Phase 1.3 submit 完成")
        # 重新加载 state（orchestrate 写入了新 state）
        state = load_orchestrate_state(paper_name)

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
        if r.get("hil_message"):
            print(f"\n{r['hil_message']}")
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

def run_phase2(paper_name: str) -> bool:
    """Phase 2: 写作循环（v2.0.4 推荐调用模式）"""
    state = load_orchestrate_state(paper_name)
    if not state:
        print("❌ 状态文件不存在，请先跑 Phase 1")
        return False
    if state.get("phase1_3_status") != "confirmed":
        print(f"❌ Phase 1.3 未确认（当前: {state.get('phase1_3_status')}）")
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
        result = write_single_node(paper_name, next_node_id, bypass_scarcity=False)

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
                result = write_single_node(paper_name, next_node_id, bypass_scarcity=True)

            elif choice == "2":
                apply_user_decision(paper_name, next_node_id, "2")
                # 重新调 write_single_node
                result = write_single_node(paper_name, next_node_id, bypass_scarcity=True)

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
            # v2.x.x 改进（v2.0.21-beta）：HIL 暂停消息改为人话版（摘要+路径+动作）
            # 背景: 之前用 jq 命令对 MBA 学生门槛高
            # 格式: 【节点ID 写完：质量X】\nAI 总结：...\n要细看：路径\n[1] 接受 / [2] 重写 / [3] 跳过
            quality = result.get("review_result", {}).get("quality")
            summary = result.get("review_result", {}).get("summary", "")

            # 计算论文工作目录路径（仅显示给用户看，不包含 jq 命令）
            from pathlib import Path as _Path
            _workspace = os.environ.get("THESIS_WORKSPACE", os.path.expanduser("~/.openclaw/workspace"))
            _paper_dir = _Path(_workspace) / paper_name
            _review_file = _paper_dir / "_phase2_review.json"

            print(f"\n【{next_node_id} 写完：质量{quality}】")
            if summary:
                # 限制为一句话长度，避免刷屏
                summary_short = summary.split("。")[0] + "。" if "。" in summary else summary[:100]
                print(f"\nAI 总结：{summary_short}")
            print(f"\n要细看：{_review_file}")

            print()
            choice = hil_pause("4", f"节点 {next_node_id} 评审结果",
                             {"1": "接受 → 继续",
                              "2": "重写 → 让 AI 再写一遍",
                              "3": "跳过 → 留空 phase 4 补"})

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
                rewrite_result = write_single_node(paper_name, next_node_id, bypass_scarcity=True)
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

    # 生成 Phase 2 HIL 消息（从 PhaseManager 文件读取状态）
    from orchestrator_v2 import _get_pm
    pm = _get_pm(paper_name)
    hil_msg = pm.generate_hil_message(phase=2, next_phase=3)
    print(f"\n{hil_msg}")

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

    if r.get("hil_message"):
        print(f"\n{r['hil_message']}")

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
    if r.get("hil_message"):
        print(f"\n{r['hil_message']}")
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
    # --status 是纯查询，不需要检查依赖，提前处理
    if args.status:
        get_paper_status(paper_name)
        return 0

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

    # llm_func 由 orchestrator 内部通过 get_session_llm_func() 固化获取
    # run_workflow.py 不再需要获取和传递 llm_func

    # 按 phase 执行
    if args.phase in ("phase1", "auto"):
        if not run_phase1(paper_name):
            return 1

    if args.phase in ("phase2", "auto"):
        if not run_phase2(paper_name):
            return 1

    if args.phase in ("phase3", "auto"):
        if not run_phase3(paper_name):
            return 1

    if args.phase in ("phase3_5", "auto"):
        print(f"\n📝 Phase 3.5: 深度学术评审")
        r = orchestrate_phase3_5(paper_name)
        if not r.get("ok"):
            print(f"❌ Phase 3.5 失败: {r.get('error')}")
            return 1

        # 审核 Loop：有 P0 → 自动修复 → 重审，直到无新 P0 或超 3 轮
        max_rounds = 3
        review_round = r.get("review_round", 1)
        while r.get("p0_count", 0) > 0 and review_round <= max_rounds:
            print(f"\n🔄 审核 Loop 第 {review_round} 轮：发现 {r.get('p0_count', 0)} 个 P0，自动修复...")
            from orchestrator_v2 import auto_fix_p0_issues
            fix_r = auto_fix_p0_issues(paper_name)
            if not fix_r.get("ok"):
                print(f"❌ P0 修复失败: {fix_r.get('error')}")
                break
            print(f"   已修复 {fix_r.get('fixed', 0)}/{fix_r.get('total', 0)} 个 P0")
            # 重审
            r = orchestrate_phase3_5(paper_name)
            if not r.get("ok"):
                print(f"❌ 重审失败: {r.get('error')}")
                break
            review_round = r.get("review_round", review_round + 1)

        if r.get("p0_count", 0) == 0:
            print(f"✅ Phase 3.5 通过（连续 2 轮无新 P0）")
        else:
            print(f"⚠️ Phase 3.5 超 {max_rounds} 轮仍有 P0，需人工介入")
        if r.get("hil_message"):
            print(f"\n{r['hil_message']}")
        print(f"✅ Phase 3.5 完成")

    if args.phase in ("phase4", "auto"):
        print(f"\n📝 Phase 4: 整合修复")
        r = orchestrate_phase4(paper_name)
        if not r.get("ok"):
            print(f"❌ Phase 4 失败: {r.get('error')}")
            return 1
        if r.get("hil_message"):
            print(f"\n{r['hil_message']}")
        print(f"✅ Phase 4 完成")

    if args.phase in ("phase5", "auto"):
        print(f"\n📝 Phase 5: 终审 + Word 输出")
        r = orchestrate_phase5(paper_name)
        if not r.get("ok"):
            print(f"❌ Phase 5 失败: {r.get('error')}")
            return 1
        if r.get("hil_message"):
            print(f"\n{r['hil_message']}")
        print(f"✅ Phase 5 完成")

    print(f"\n🎉 全部完成")
    return 0


if __name__ == "__main__":
    _ensure_utf8_stdout()
    sys.exit(main())