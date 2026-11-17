#!/usr/bin/env python3
"""skill-to-http Doctor

自检工具，检查环境、依赖、配置、Skills 注册、运行时状态。
支持两种模式：
  - scan  (默认): 只检测，输出报告
  - fix:          自动修复可修复项

用法:
  python3 doctor.py           # 扫描报告
  python3 doctor.py --fix     # 扫描 + 自动修复
  python3 doctor.py --json    # JSON 输出（API 用）
"""

from __future__ import annotations

import importlib.metadata
import importlib.util
import json
import os
import shutil
import socket
import subprocess
import sys
import time
import urllib.request
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path

# ── 常量 ──────────────────────────────────────────────────────────────
from _paths import CONFIG_PATH
from _paths import PID_FILE
from _paths import PORT_FILE
from _paths import LOG_FILE
from _paths import HISTORY_DB
OPENCLAW_CONFIG  = Path.home() / ".openclaw" / "openclaw.json"

GATEWAY_URL      = "http://localhost:18789"
PYPI_MIRROR      = "https://pypi.tuna.tsinghua.edu.cn/simple"

REQUIRED_PYTHON  = (3, 10)
DISK_WARN_MB     = 200

VALID_EXECUTORS  = {"auto", "openclaw", "cc", "claude_cli", "codex", "llm"}
VALID_FALLBACKS  = {"disable", "default"}


# ── 数据结构 ──────────────────────────────────────────────────────────
class Severity(str, Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"
    INFO = "INFO"


@dataclass
class CheckResult:
    domain: str               # 环境 / 依赖 / 配置 / Skills / 运行时
    name: str                 # 简短名称（用于 --fix 定位）
    severity: Severity
    message: str              # 人类可读描述
    fix_hint: str = ""        # 修复提示（WARN/FAIL 专用）
    fix_cmd: str  = ""        # 可执行的 shell 修复命令（doctor --fix 用）
    fixable: bool = False     # 是否支持 --fix 自动修复
    detail: str = ""          # 附加详情（可选）


@dataclass
class DoctorReport:
    results: list[CheckResult] = field(default_factory=list)

    def add(self, r: CheckResult) -> None:
        self.results.append(r)

    def summary(self) -> dict[str, int]:
        cnt: dict[str, int] = {s.value: 0 for s in Severity}
        for r in self.results:
            cnt[r.severity.value] += 1
        return cnt

    def has_failures(self) -> bool:
        return any(r.severity in (Severity.FAIL, Severity.WARN) for r in self.results)


# ── 工具函数 ─────────────────────────────────────────────────────────
def _pkg_version(name: str) -> str | None:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def _can_import(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def _http_ok(url: str, timeout: int = 3) -> bool:
    try:
        proxy = urllib.request.ProxyHandler({})
        opener = urllib.request.build_opener(proxy)
        req = urllib.request.Request(url, method="GET")
        with opener.open(req, timeout=timeout) as resp:
            return resp.status == 200
    except Exception:
        return False


def _load_config() -> dict | None:
    if not CONFIG_PATH.exists():
        return None
    try:
        return json.loads(CONFIG_PATH.read_text())
    except (FileNotFoundError, PermissionError, json.JSONDecodeError):
        return None


def _read_pid() -> tuple[int, int] | None:
    try:
        data = json.loads(PID_FILE.read_text())
        return int(data["pid"]), int(data["port"])
    except Exception:
        return None


def _is_running() -> bool:
    info = _read_pid()
    if not info:
        return False
    pid, _ = info
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def _run_fix(cmd: str) -> tuple[bool, str]:
    """执行修复命令，返回 (成功, 输出)。"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=120
        )
        out = (result.stdout + result.stderr).strip()
        return result.returncode == 0, out
    except Exception as e:
        return False, str(e)


# ═══════════════════════════════════════════════════════════════════════
# 域 1: 环境
# ═══════════════════════════════════════════════════════════════════════
def check_environment(report: DoctorReport) -> None:
    domain = "环境"

    # Python 版本
    vi = sys.version_info
    if vi >= REQUIRED_PYTHON:
        report.add(CheckResult(domain, "python_version", Severity.PASS,
                               f"Python {vi.major}.{vi.minor}.{vi.micro}"))
    else:
        report.add(CheckResult(domain, "python_version", Severity.FAIL,
                               f"Python {vi.major}.{vi.minor} 低于最低要求 {REQUIRED_PYTHON[0]}.{REQUIRED_PYTHON[1]}",
                               fix_hint="请升级 Python 至 3.10+"))

    # openclaw CLI
    openclaw_bin = shutil.which("openclaw")
    if openclaw_bin:
        try:
            r = subprocess.run(["openclaw", "--version"], capture_output=True, text=True, timeout=5)
            ver = (r.stdout + r.stderr).strip().splitlines()[0] if r.returncode == 0 else "unknown"
        except Exception:
            ver = "unknown"
        report.add(CheckResult(domain, "openclaw_cli", Severity.PASS,
                               f"openclaw CLI 可用（{ver}）"))
    else:
        report.add(CheckResult(domain, "openclaw_cli", Severity.FAIL,
                               "openclaw CLI 未找到（executor=openclaw 将不可用）",
                               fix_hint="请确认 openclaw 已安装并在 PATH 中"))

    # Gateway 可达
    gw_ok = _http_ok(f"{GATEWAY_URL}/health")
    if gw_ok:
        report.add(CheckResult(domain, "gateway", Severity.PASS,
                               f"OpenClaw Gateway 可达（{GATEWAY_URL}）"))
    else:
        report.add(CheckResult(domain, "gateway", Severity.WARN,
                               f"OpenClaw Gateway 不可达（{GATEWAY_URL}/health 无响应）",
                               fix_hint="执行 `openclaw gateway start` 启动 Gateway",
                               fix_cmd="openclaw gateway start",
                               fixable=True))

    # Gateway token
    try:
        SCRIPTS = Path(__file__).parent
        if str(SCRIPTS) not in sys.path:
            sys.path.insert(0, str(SCRIPTS))
        from skill_runner import _get_gateway_token
        token = _get_gateway_token()
        if token and len(token) >= 32:
            report.add(CheckResult(domain, "gateway_token", Severity.PASS,
                                   f"Gateway token 有效（长度 {len(token)}）"))
        elif token:
            report.add(CheckResult(domain, "gateway_token", Severity.WARN,
                                   f"Gateway token 长度异常（{len(token)}，预期 ≥ 32）",
                                   fix_hint="执行 `openclaw login` 重新获取 token",
                                   fix_cmd="openclaw login",
                                   fixable=True))
        else:
            report.add(CheckResult(domain, "gateway_token", Severity.WARN,
                                   "未找到 Gateway token，openclaw executor 可能无法鉴权",
                                   fix_hint="执行 `openclaw login` 重新登录",
                                   fix_cmd="openclaw login",
                                   fixable=True))
    except Exception as e:
        report.add(CheckResult(domain, "gateway_token", Severity.WARN,
                               f"无法读取 Gateway token: {e}"))

    # claude CLI 或 codex CLI（至少一个）
    has_claude = shutil.which("claude") is not None
    has_codex  = shutil.which("codex") is not None
    if has_claude and has_codex:
        report.add(CheckResult(domain, "fallback_cli", Severity.PASS,
                               "claude CLI ✅  codex CLI ✅  (执行备选完整)"))
    elif has_claude:
        report.add(CheckResult(domain, "fallback_cli", Severity.INFO,
                               "claude CLI ✅  codex CLI ✗  (有 claude 备选，codex 可选)"))
    elif has_codex:
        report.add(CheckResult(domain, "fallback_cli", Severity.INFO,
                               "claude CLI ✗  codex CLI ✅  (有 codex 备选，claude 可选)"))
    else:
        report.add(CheckResult(domain, "fallback_cli", Severity.WARN,
                               "claude CLI 和 codex CLI 均未安装；当 openclaw executor 不可用时无备选，skill 执行将降级到 LLM 模式（无工具能力）",
                               fix_hint="安装 claude CLI: `npm install -g @anthropic-ai/claude-code`  或  codex CLI: `npm install -g @openai/codex`",
                               fix_cmd="npm install -g @anthropic-ai/claude-code",
                               fixable=True))

    # 磁盘空间
    try:
        usage = shutil.disk_usage(Path.home())
        free_mb = usage.free // (1024 * 1024)
        if free_mb < DISK_WARN_MB:
            report.add(CheckResult(domain, "disk_space", Severity.WARN,
                                   f"磁盘剩余空间 {free_mb} MB，低于 {DISK_WARN_MB} MB 警戒线",
                                   fix_hint="清理磁盘空间，建议保留至少 500 MB"))
        else:
            report.add(CheckResult(domain, "disk_space", Severity.PASS,
                                   f"磁盘剩余 {free_mb} MB"))
    except Exception as e:
        report.add(CheckResult(domain, "disk_space", Severity.WARN, f"无法检测磁盘空间: {e}"))


# ═══════════════════════════════════════════════════════════════════════
# 域 2: 依赖安装
# ═══════════════════════════════════════════════════════════════════════
def check_dependencies(report: DoctorReport) -> None:
    domain = "依赖"

    # fastapi
    fav = _pkg_version("fastapi")
    if fav:
        report.add(CheckResult(domain, "fastapi", Severity.PASS, f"fastapi {fav}"))
    else:
        report.add(CheckResult(domain, "fastapi", Severity.FAIL,
                               "fastapi 未安装（服务无法启动）",
                               fix_hint=f"pip install -i {PYPI_MIRROR} 'fastapi>=0.110.0'",
                               fix_cmd=f"pip install -i {PYPI_MIRROR} 'fastapi>=0.110.0'",
                               fixable=True))

    # uvicorn
    uv = _pkg_version("uvicorn")
    if uv:
        report.add(CheckResult(domain, "uvicorn", Severity.PASS, f"uvicorn {uv}"))
    else:
        report.add(CheckResult(domain, "uvicorn", Severity.FAIL,
                               "uvicorn 未安装（服务无法启动）",
                               fix_hint=f"pip install -i {PYPI_MIRROR} 'uvicorn[standard]>=0.29.0'",
                               fix_cmd=f"pip install -i {PYPI_MIRROR} 'uvicorn[standard]>=0.29.0'",
                               fixable=True))

    # cryptography（HTTPS 可选，非必须，INFO 级别）
    cv = _pkg_version("cryptography")
    if cv:
        report.add(CheckResult(domain, "cryptography", Severity.PASS, f"cryptography {cv}（HTTPS 就绪）"))
    else:
        report.add(CheckResult(domain, "cryptography", Severity.INFO,
                               "cryptography 未安装（仅 HTTPS 模式需要）",
                               fix_hint=f"pip install -i {PYPI_MIRROR} 'cryptography>=42.0.0'",
                               fix_cmd=f"pip install -i {PYPI_MIRROR} 'cryptography>=42.0.0'",
                               fixable=True))

    # claude_agent_sdk（影响 cc executor 速度，WARN）
    has_sdk = _can_import("claude_agent_sdk")
    if has_sdk:
        try:
            import claude_agent_sdk
            ok = hasattr(claude_agent_sdk, "query")
            report.add(CheckResult(domain, "claude_agent_sdk", Severity.PASS,
                                   f"claude_agent_sdk 可用（query API {'✅' if ok else '⚠️ 无 query 方法'}）"))
        except Exception as e:
            report.add(CheckResult(domain, "claude_agent_sdk", Severity.WARN,
                                   f"claude_agent_sdk 导入异常: {e}"))
    else:
        report.add(CheckResult(domain, "claude_agent_sdk", Severity.WARN,
                               "claude_agent_sdk 未安装；cc executor 不可用，执行速度受影响（无本地 SDK 直连能力）",
                               fix_hint=f"pip install -i {PYPI_MIRROR} claude-agent-sdk",
                               fix_cmd=f"pip install -i {PYPI_MIRROR} claude-agent-sdk",
                               fixable=True))

    # 内部模块（scripts 目录）
    SCRIPTS = Path(__file__).parent
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))

    for mod_name, desc in [
        ("dep_scanner",    "依赖扫描"),
        ("history_store",  "Job 历史"),
        ("speed_mode",     "极速模式"),
        ("skill_registry", "Skill 注册"),
        ("skill_runner",   "Skill 执行引擎"),
    ]:
        if _can_import(mod_name):
            report.add(CheckResult(domain, f"module_{mod_name}", Severity.PASS,
                                   f"{mod_name} 可导入（{desc}）"))
        else:
            report.add(CheckResult(domain, f"module_{mod_name}", Severity.FAIL,
                                   f"{mod_name} 无法导入（{desc} 功能不可用）",
                                   fix_hint=f"确认 {SCRIPTS}/{mod_name}.py 存在，或检查 PYTHONPATH"))


# ═══════════════════════════════════════════════════════════════════════
# 域 3: 配置
# ═══════════════════════════════════════════════════════════════════════
def check_config(report: DoctorReport) -> None:
    domain = "配置"

    if not CONFIG_PATH.exists():
        default_cfg = {
            "executor": "auto",
            "skill_dirs": [str(Path.home() / ".openclaw" / "workspace" / "skills")],
            "expose_skills": [],
            "speed_mode": False,
            "speed_mode_fallback": "disable",
            "max_concurrent": 0,
        }
        fix_cmd = (
            f"python3 -c \""
            f"import json, pathlib; "
            f"p = pathlib.Path('{CONFIG_PATH}'); "
            f"p.parent.mkdir(parents=True, exist_ok=True); "
            f"p.write_text(json.dumps({json.dumps(default_cfg)}, indent=2))"
            f"\""
        )
        report.add(CheckResult(domain, "config_exists", Severity.WARN,
                               f"config.json 不存在（{CONFIG_PATH}）",
                               fix_hint="--fix 将自动创建默认 config.json，请再根据实际情况修改 skill_dirs 和 executor",
                               fix_cmd=fix_cmd,
                               fixable=True))
        return

    # JSON 合法性
    try:
        cfg = json.loads(CONFIG_PATH.read_text())
        report.add(CheckResult(domain, "config_json", Severity.PASS, "config.json 格式合法"))
    except Exception as e:
        report.add(CheckResult(domain, "config_json", Severity.FAIL,
                               f"config.json JSON 解析失败: {e}",
                               fix_hint="用文本编辑器修复 JSON 语法错误"))
        return

    # executor 合法性
    executor = cfg.get("executor", "auto")
    if executor in VALID_EXECUTORS:
        report.add(CheckResult(domain, "config_executor", Severity.PASS,
                               f"executor = {executor}"))
    else:
        fix_cmd_exec = (
            f"python3 -c \""
            f"import json, pathlib; "
            f"p = pathlib.Path('{CONFIG_PATH}'); "
            f"d = json.loads(p.read_text()); "
            f"d['executor'] = 'auto'; "
            f"p.write_text(json.dumps(d, indent=2, ensure_ascii=False))"
            f"\""
        )
        report.add(CheckResult(domain, "config_executor", Severity.FAIL,
                               f"executor = '{executor}' 非法，合法值: {sorted(VALID_EXECUTORS)}",
                               fix_hint="--fix 将自动将 executor 改为 'auto'",
                               fix_cmd=fix_cmd_exec,
                               fixable=True))

    # executor 与环境一致性
    if executor in ("openclaw", "auto"):
        gw_ok = _http_ok(f"{GATEWAY_URL}/health")
        if not gw_ok:
            # fix 逻辑：先尝试 start Gateway，等待 5s，再检测；若仍不通就降级 executor=auto
            fix_cmd_gw = (
                "openclaw gateway start && sleep 5 || true"
            )
            report.add(CheckResult(domain, "config_executor_env", Severity.WARN,
                                   f"executor={executor} 但 Gateway 不可达，openclaw 路径将降级",
                                   fix_hint="--fix 将尝试启动 Gateway；若启动失败，请手动执行 `openclaw gateway start` 或将 executor 改为 auto",
                                   fix_cmd=fix_cmd_gw,
                                   fixable=True))
        else:
            report.add(CheckResult(domain, "config_executor_env", Severity.PASS,
                                   f"executor={executor}，Gateway 已就绪"))

    # skill_dirs
    skill_dirs = cfg.get("skill_dirs", [])
    if not skill_dirs:
        default_skill_dir = str(Path.home() / ".openclaw" / "workspace" / "skills")
        fix_cmd_dirs = (
            f"python3 -c \""
            f"import json, pathlib; "
            f"p = pathlib.Path('{CONFIG_PATH}'); "
            f"d = json.loads(p.read_text()); "
            f"d['skill_dirs'] = ['{default_skill_dir}']; "
            f"p.write_text(json.dumps(d, indent=2, ensure_ascii=False))"
            f"\""
        )
        report.add(CheckResult(domain, "config_skill_dirs", Severity.WARN,
                               "skill_dirs 未配置，无法发现任何 skill",
                               fix_hint=f"--fix 将自动写入默认目录 {default_skill_dir}，请再根据实际情况修改",
                               fix_cmd=fix_cmd_dirs,
                               fixable=True))
    else:
        report.add(CheckResult(domain, "config_skill_dirs", Severity.PASS,
                               f"skill_dirs 配置了 {len(skill_dirs)} 个目录"))
        for d in skill_dirs:
            expanded = Path(d).expanduser().resolve()
            if not expanded.exists():
                report.add(CheckResult(domain, f"skill_dir_{expanded.name}", Severity.WARN,
                                       f"skill_dirs 路径不存在: {d}",
                                       fix_hint=f"--fix 将自动创建目录 {expanded}",
                                       fix_cmd=f"mkdir -p '{expanded}'",
                                       fixable=True))
            else:
                report.add(CheckResult(domain, f"skill_dir_{expanded.name}", Severity.PASS,
                                       f"skill_dirs 路径存在: {d}"))

    # speed_mode_fallback
    fallback = cfg.get("speed_mode_fallback", "disable")
    if fallback in VALID_FALLBACKS:
        report.add(CheckResult(domain, "config_fallback", Severity.PASS,
                               f"speed_mode_fallback = {fallback}"))
    else:
        fix_cmd_fallback = (
            f"python3 -c \""
            f"import json, pathlib; "
            f"p = pathlib.Path('{CONFIG_PATH}'); "
            f"d = json.loads(p.read_text()); "
            f"d['speed_mode_fallback'] = 'disable'; "
            f"p.write_text(json.dumps(d, indent=2, ensure_ascii=False))"
            f"\""
        )
        report.add(CheckResult(domain, "config_fallback", Severity.FAIL,
                               f"speed_mode_fallback = '{fallback}' 非法，合法值: {sorted(VALID_FALLBACKS)}",
                               fix_hint="--fix 将自动将 speed_mode_fallback 改为 'disable'",
                               fix_cmd=fix_cmd_fallback,
                               fixable=True))

    # api_key 长度校验
    api_key = cfg.get("api_key", "")
    if api_key and len(api_key) < 16:
        fix_cmd_key = (
            f"python3 -c \""
            f"import json, pathlib, secrets; "
            f"p = pathlib.Path('{CONFIG_PATH}'); "
            f"d = json.loads(p.read_text()); "
            f"d['api_key'] = secrets.token_hex(32); "
            f"p.write_text(json.dumps(d, indent=2, ensure_ascii=False)); "
            f"print('new api_key:', d['api_key'])"
            f"\""
        )
        report.add(CheckResult(domain, "config_api_key", Severity.WARN,
                               f"api_key 长度 {len(api_key)} 过短（建议 ≥ 32 位随机字符串）",
                               fix_hint="--fix 将自动用 secrets.token_hex(32) 生成新 key 并写回配置，请更新调用方的 key",
                               fix_cmd=fix_cmd_key,
                               fixable=True))
    elif api_key:
        report.add(CheckResult(domain, "config_api_key", Severity.PASS,
                               f"api_key 已配置（长度 {len(api_key)}）"))
    else:
        report.add(CheckResult(domain, "config_api_key", Severity.INFO,
                               "api_key 未配置（服务无认证，仅内网部署时可接受）"))

    # max_concurrent
    mc = cfg.get("max_concurrent", 0)
    if isinstance(mc, int) and 0 <= mc <= 50:
        report.add(CheckResult(domain, "config_max_concurrent", Severity.PASS,
                               f"max_concurrent = {mc} ({'不限' if mc == 0 else mc})"))
    else:
        fix_cmd_mc = (
            f"python3 -c \""
            f"import json, pathlib; "
            f"p = pathlib.Path('{CONFIG_PATH}'); "
            f"d = json.loads(p.read_text()); "
            f"d['max_concurrent'] = 0; "
            f"p.write_text(json.dumps(d, indent=2, ensure_ascii=False))"
            f"\""
        )
        report.add(CheckResult(domain, "config_max_concurrent", Severity.WARN,
                               f"max_concurrent = {mc} 异常（合理范围: 0-50）",
                               fix_hint="--fix 将自动重置为 0（不限并发）",
                               fix_cmd=fix_cmd_mc,
                               fixable=True))

    # 极速模式配置一致性
    if cfg.get("speed_mode") and cfg.get("speed_mode_agent"):
        agent_id = cfg["speed_mode_agent"]
        oc_cfg_ok = False
        if OPENCLAW_CONFIG.exists():
            try:
                oc_cfg = json.loads(OPENCLAW_CONFIG.read_text())
                agents = oc_cfg.get("agents", {}).get("list", [])
                oc_cfg_ok = any(a.get("id") == agent_id for a in agents)
            except Exception:
                pass
        if oc_cfg_ok:
            report.add(CheckResult(domain, "speed_mode_agent", Severity.PASS,
                                   f"极速模式 agent '{agent_id}' 已注册"))
        else:
            report.add(CheckResult(domain, "speed_mode_agent", Severity.WARN,
                                   f"极速模式已开启但 agent '{agent_id}' 未在 openclaw.json 中注册",
                                   fix_hint="重新执行极速模式 setup: POST /api/speed_mode/enable 或通过控制台开启"))


# ═══════════════════════════════════════════════════════════════════════
# 域 4: Skills
# ═══════════════════════════════════════════════════════════════════════
def check_skills(report: DoctorReport) -> None:
    domain = "Skills"

    cfg = _load_config()
    if not cfg:
        report.add(CheckResult(domain, "skills_config", Severity.WARN,
                               "无法加载 config.json，跳过 Skill 检查"))
        return

    skill_dirs = [str(Path(d).expanduser().resolve()) for d in cfg.get("skill_dirs", [])]
    expose_skills = cfg.get("expose_skills", [])

    # 发现 skill 总数
    all_skills: dict[str, Path] = {}
    for d in skill_dirs:
        p = Path(d)
        if not p.is_dir():
            continue
        for subdir in p.iterdir():
            if subdir.is_dir() and (subdir / "SKILL.md").exists():
                all_skills[subdir.name] = subdir

    if not all_skills:
        report.add(CheckResult(domain, "skills_found", Severity.WARN,
                               "未在 skill_dirs 中发现任何 Skill（缺少带 SKILL.md 的子目录）",
                               fix_hint="检查 skill_dirs 路径是否正确"))
    else:
        report.add(CheckResult(domain, "skills_found", Severity.PASS,
                               f"发现 {len(all_skills)} 个 Skill：{', '.join(sorted(all_skills)[:8])}"
                               + ("..." if len(all_skills) > 8 else "")))

    # 已暴露 skill 数量
    is_wildcard = "*" in expose_skills
    if is_wildcard:
        report.add(CheckResult(domain, "skills_exposed", Severity.PASS,
                               f"expose_skills = * （全部 {len(all_skills)} 个 skill 均已暴露）"))
        exposed_names = list(all_skills.keys())
    elif expose_skills:
        report.add(CheckResult(domain, "skills_exposed", Severity.PASS,
                               f"已暴露 {len(expose_skills)} 个 Skill：{', '.join(expose_skills)}"))
        exposed_names = expose_skills
    else:
        report.add(CheckResult(domain, "skills_exposed", Severity.WARN,
                               "expose_skills 为空，没有任何 Skill 被暴露为 API",
                               fix_hint="在控制台或 config.json 中暴露至少 1 个 Skill"))
        exposed_names = []

    # 逐一检查已暴露 skill
    for name in exposed_names:
        skill_dir = all_skills.get(name)
        if not skill_dir:
            report.add(CheckResult(domain, f"skill_{name}_dir", Severity.WARN,
                                   f"已暴露 skill '{name}' 在 skill_dirs 中未找到对应目录",
                                   fix_hint=f"检查 skill '{name}' 是否已安装到 skill_dirs 中"))
            continue

        # params.json
        params_path = skill_dir / "params.json"
        if not params_path.exists():
            # 自动生成一个骨架 params.json 的脚本
            fix_py = (
                f"python3 -c \""
                f"import json, pathlib; "
                f"p = pathlib.Path('{params_path}'); "
                f"p.write_text(json.dumps({{"
                f"  'name': '{name}', "
                f"  'description': '（待补充）', "
                f"  'params': []"
                f"}}, ensure_ascii=False, indent=2))\""
            )
            report.add(CheckResult(domain, f"skill_{name}_params", Severity.WARN,
                                   f"skill '{name}' 缺少 params.json（参数描述不可用，调用时需手动传参）",
                                   fix_hint=(
                                       "--fix 将自动生成骨架文件 " + str(params_path) + "，"
                                       "但骨架中 params 数组为空、description 为占位符——"
                                       "生成后必须手动补充，否则接口调用者将看不到可用参数。"
                                       '\n参考格式: {"name": "skill-name", "description": "...", '
                                       '"params": [{"name": "task", "type": "string", "required": true, "description": "..."}]}'
                                   ),
                                   fix_cmd=fix_py,
                                   fixable=True))
        else:
            # 校验 params.json 格式合法
            try:
                pdata = json.loads(params_path.read_text())
                if not isinstance(pdata, dict):
                    raise ValueError("root must be object")
                report.add(CheckResult(domain, f"skill_{name}_params", Severity.PASS,
                                       f"skill '{name}' params.json 存在且格式合法"))
            except Exception as e:
                report.add(CheckResult(domain, f"skill_{name}_params", Severity.FAIL,
                                       f"skill '{name}' params.json JSON 解析失败: {e}",
                                       fix_hint=f"手动修复 {params_path} 的 JSON 格式"))

    # stt-runner 极速模式 workspace（若已开启）
    if cfg.get("speed_mode"):
        runner_ws = Path.home() / ".openclaw" / "workspace" / "stt-runner"
        if (runner_ws / "SYSTEM.md").exists():
            report.add(CheckResult(domain, "speed_mode_workspace", Severity.PASS,
                                   f"stt-runner workspace 就绪（{runner_ws}）"))
        else:
            report.add(CheckResult(domain, "speed_mode_workspace", Severity.WARN,
                                   "极速模式已开启但 stt-runner workspace 缺少 SYSTEM.md",
                                   fix_hint="重新执行极速模式 setup"))


# ═══════════════════════════════════════════════════════════════════════
# 域 5: 运行时
# ═══════════════════════════════════════════════════════════════════════
def check_runtime(report: DoctorReport) -> None:
    domain = "运行时"

    running = _is_running()
    pid_info = _read_pid()

    if not running:
        report.add(CheckResult(domain, "server_process", Severity.INFO,
                               "主服务未运行（非错误，可能本次只做离线检查）",
                               fix_hint="执行 `python3 server.py start` 启动服务"))
        return

    pid, port = pid_info  # type: ignore[misc]
    report.add(CheckResult(domain, "server_process", Severity.PASS,
                           f"主服务进程存活（PID {pid}，端口 {port}）"))

    # /health 端点
    health_url = f"http://localhost:{port}/health"
    if _http_ok(health_url):
        report.add(CheckResult(domain, "server_health", Severity.PASS,
                               f"/health 响应正常（{health_url}）"))
    else:
        report.add(CheckResult(domain, "server_health", Severity.FAIL,
                               f"/health 无响应（{health_url}），服务可能僵死",
                               fix_hint="执行 `python3 server.py restart` 重启服务",
                               fix_cmd="python3 server.py restart",
                               fixable=True))

    # 历史库可写
    try:
        import sqlite3 as _sqlite3
        if HISTORY_DB.exists():
            conn = _sqlite3.connect(str(HISTORY_DB), timeout=2)
            cnt = conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
            conn.close()
            report.add(CheckResult(domain, "history_db", Severity.PASS,
                                   f"历史库可读写（{cnt} 条 Job 记录）"))
        else:
            report.add(CheckResult(domain, "history_db", Severity.INFO,
                                   "历史库文件不存在（首次启动后自动创建）"))
    except Exception as e:
        report.add(CheckResult(domain, "history_db", Severity.WARN,
                               f"历史库异常: {e}"))

    # 日志文件可写
    try:
        with open(LOG_FILE, "a") as _f:
            pass
        report.add(CheckResult(domain, "log_file", Severity.PASS,
                               f"日志文件可写（{LOG_FILE}）"))
    except Exception as e:
        report.add(CheckResult(domain, "log_file", Severity.WARN,
                               f"日志文件不可写: {e}"))


# ═══════════════════════════════════════════════════════════════════════
# 主检查入口
# ═══════════════════════════════════════════════════════════════════════
def check_tls(report: DoctorReport) -> None:
    """检查 TLS 证书状态：存在/过期/SAN 匹配"""
    cfg = _load_config() or {}
    tls_enabled = cfg.get("tls_enabled", False) or cfg.get("https", {}).get("enabled", False)
    if not tls_enabled:
        report.add(CheckResult(
            domain="tls",
            name="tls_enabled",
            severity=Severity.INFO,
            message="HTTPS 未启用，跳过证书检查（如需启用：python3 server.py upgrade-to-https）",
        ))
        return

    try:
        import sys as _sys
        from pathlib import Path as _P
        _sys.path.insert(0, str(_P(__file__).parent))
        from gen_cert import get_cert_status
    except ImportError as e:
        report.add(CheckResult(
            domain="tls",
            name="gen_cert_module",
            severity=Severity.FAIL,
            message=f"gen_cert 模块不可用：{e}",
        ))
        return

    status = get_cert_status()
    gen_cert_path = str(Path(__file__).parent / 'gen_cert.py')

    if not status["exists"]:
        report.add(CheckResult(
            domain="tls",
            name="cert_exists",
            severity=Severity.FAIL,
            message=f"TLS 已启用但证书不存在：{status['cert_path']}",
            fix_hint="生成自签证书（含本机 IP 嗅探）",
            fix_cmd=f"python3 {gen_cert_path} --san auto --force",
            fixable=True,
        ))
        return

    # 检查过期
    days = status.get("days_until_expiry")
    if days is not None:
        if days <= 0:
            report.add(CheckResult(
                domain="tls",
                name="cert_expired",
                severity=Severity.FAIL,
                message=f"证书已过期 {-days} 天：{status['cert_path']}",
                fix_hint="重新生成证书",
                fix_cmd=f"python3 {gen_cert_path} renew --san auto",
                fixable=True,
            ))
        elif days <= 30:
            report.add(CheckResult(
                domain="tls",
                name="cert_expiring_soon",
                severity=Severity.WARN,
                message=f"证书将在 {days} 天后过期",
                fix_hint="提前续期证书",
                fix_cmd=f"python3 {gen_cert_path} renew --san auto",
                fixable=True,
            ))
        else:
            report.add(CheckResult(
                domain="tls",
                name="cert_validity",
                severity=Severity.PASS,
                message=f"证书有效，剩余 {days} 天",
            ))

    # 检查 SAN 匹配
    if status.get("san_mismatch"):
        report.add(CheckResult(
            domain="tls",
            name="cert_san_mismatch",
            severity=Severity.WARN,
            message=f"本机 IP 部分不在证书 SAN 中（当前 SAN: {status.get('san', [])}）。外部访问可能因证书校验失败而拒绝",
            fix_hint="重新生成证书并嗅探本机 IP",
            fix_cmd=f"python3 {gen_cert_path} renew --san auto",
            fixable=True,
        ))


def run_scan() -> DoctorReport:
    report = DoctorReport()
    check_environment(report)
    check_dependencies(report)
    check_config(report)
    check_skills(report)
    check_tls(report)
    check_runtime(report)
    return report


# ═══════════════════════════════════════════════════════════════════════
# --fix 自动修复
# ═══════════════════════════════════════════════════════════════════════
def run_fix(report: DoctorReport) -> list[dict]:
    """对所有 fixable=True 且 severity != PASS 的项目执行修复。"""
    fix_log: list[dict] = []
    for r in report.results:
        if not r.fixable or not r.fix_cmd or r.severity == Severity.PASS:
            continue
        print(f"\n🔧 修复 [{r.domain}] {r.name}...")
        print(f"   命令: {r.fix_cmd}")
        ok, out = _run_fix(r.fix_cmd)
        status = "✅ 成功" if ok else "❌ 失败"
        print(f"   {status}" + (f"\n   {out[:200]}" if out else ""))
        fix_log.append({
            "domain": r.domain,
            "name": r.name,
            "fix_cmd": r.fix_cmd,
            "success": ok,
            "output": out[:500],
        })
    return fix_log


# ═══════════════════════════════════════════════════════════════════════
# 输出渲染
# ═══════════════════════════════════════════════════════════════════════
_SEV_ICON = {
    Severity.PASS: "✅",
    Severity.WARN: "⚠️ ",
    Severity.FAIL: "❌",
    Severity.INFO: "ℹ️ ",
}


def print_report(report: DoctorReport) -> None:
    current_domain = ""
    for r in report.results:
        if r.domain != current_domain:
            current_domain = r.domain
            print(f"\n[{current_domain}]")
        icon = _SEV_ICON[r.severity]
        line = f"  {icon} {r.message}"
        print(line)
        if r.fix_hint and r.severity in (Severity.WARN, Severity.FAIL):
            print(f"      → {r.fix_hint}")

    s = report.summary()
    total = sum(s.values())
    print("\n" + "=" * 60)
    print(f"Doctor 完成：{s['PASS']} PASS  {s['WARN']} WARN  {s['FAIL']} FAIL  {s['INFO']} INFO  （共 {total} 项）")

    fails  = [r for r in report.results if r.severity == Severity.FAIL]
    warns  = [r for r in report.results if r.severity == Severity.WARN]
    fixable = [r for r in report.results if r.fixable and r.severity != Severity.PASS]

    if fails:
        print(f"\n必须修复: {', '.join(r.name for r in fails)}")
    if warns:
        print(f"建议修复: {', '.join(r.name for r in warns)}")
    if fixable:
        print(f"\n（运行 `python3 doctor.py --fix` 可自动修复以下项: {', '.join(r.name for r in fixable)}）")


def to_json_dict(report: DoctorReport) -> dict:
    return {
        "summary": report.summary(),
        "results": [
            {
                "domain": r.domain,
                "name": r.name,
                "severity": r.severity.value,
                "message": r.message,
                "fix_hint": r.fix_hint,
                "fixable": r.fixable,
                "detail": r.detail,
            }
            for r in report.results
        ],
        "has_failures": report.has_failures(),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


# ═══════════════════════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════════════════════
def main(argv: list[str] | None = None) -> None:
    import argparse
    p = argparse.ArgumentParser(description="skill-to-http Doctor — 自检工具")
    p.add_argument("--fix",  action="store_true", help="扫描后自动执行可修复项")
    p.add_argument("--json", action="store_true", help="以 JSON 格式输出（供 API 调用）")
    p.add_argument("--domain", type=str, default=None,
                   choices=["环境", "依赖", "配置", "Skills", "运行时"],
                   help="只检查指定域（默认全部）")
    args = p.parse_args(argv)

    report = run_scan()

    # 单域过滤
    if args.domain:
        report.results = [r for r in report.results if r.domain == args.domain]

    if args.json:
        print(json.dumps(to_json_dict(report), ensure_ascii=False, indent=2))
    else:
        print_report(report)
        if args.fix:
            fixable = [r for r in report.results if r.fixable and r.severity != Severity.PASS]
            if not fixable:
                print("\n✅ 没有可自动修复的项目。")
            else:
                fix_log = run_fix(report)
                # 修复完成后重新扫描
                print("\n🔄 重新扫描验证修复结果...")
                report2 = run_scan()
                if args.domain:
                    report2.results = [r for r in report2.results if r.domain == args.domain]
                print_report(report2)

    sys.exit(1 if report.has_failures() else 0)


if __name__ == "__main__":
    main()
