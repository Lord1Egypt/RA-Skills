"""来源元数据采集（来源透明度的落地端）。

契约（docs/COLLAB_API_CONTRACT.md §0.1）：来源元数据必须放在请求体 client 对象内：
    { "agentVersion": "...", "skillVersion": "...", "model": "...", "modelVersion": "..." }

硬约束（§4.14 / §14.11）：
  - skillVersion **自动采集**（包版本），无需用户配置
  - agentVersion / model / modelVersion 从本地配置或 --model 参数读取
  - **模型标识是必填项，不是可选项**：缺失时**拒绝执行写操作**（requireModel，默认 true）。
    理由：Skill 是智能体与平台之间唯一的通道，一切会谈都从这里过；
    既然是唯一入口，入口就必须要求把来源信息带上，而不是等出了问题再去猜。
    平台会公开每条内容的「来源透明度」，缺模型就只能记成「未申报」——
    那等于在公开记录里留了一块空白，而这块空白本可以避免。
  - **绝不猜测模型名**：不从任何环境变量推断 model / modelVersion。
    这是与上一条并存的：本端**无法自行得知**调用方用的是哪个模型（那是调用方运行时的信息），
    所以正确的做法是「要求调用方显式提供」，而不是「猜一个填上」——
    猜错等于虚假标识，比未申报更严重。因此本模块是**拒绝**，不是**兜底猜测**。
  - 显式放行才允许以未申报上报：`zhiqi config set provenance.requireModel false`
    （或单次 `--allow-undeclared`）。防御性记录仍保留 UNKNOWN + declared=false，
    但它不再是正常路径，只用于绕过入口的异常情况。
"""  

import importlib
import importlib.metadata
import json
import logging
import os
import platform
import re
import shutil
import subprocess
from typing import Any, Dict, Optional

from .errors import ZhiQiConfigError

log = logging.getLogger("zhiqi.provenance")

UNKNOWN = "UNKNOWN"

REQUIRE_UNDECLARED = (
    "未能确定当前使用的大模型，已拒绝本次写入。\n"
    "\n"
    "本端按这个顺序解析（每次调用都重新解析，模型切换会自动跟随）：\n"
    "  1. 命令行的 --model\n"
    "  2. 宿主运行时配置（例如 openclaw config get agents.defaults.model.primary）\n"
    "  3. 本地配置 provenance.model（手动兜底）\n"
    "三处都拿不到，就拒绝写入 —— 而不是记一条「未申报」，也不是沿用上一次的值。\n"
    "\n"
    "为什么不让本端猜：模型随时可以在宿主里切换且不会通知本技能。"
    "写一个过期的或猜错的名字，是**看起来像已申报的假标识**，比留白更严重。\n"
    "\n"
    "怎么修（任选其一）：\n"
    "  ① 确认宿主可用并已配置模型：openclaw config get agents.defaults.model.primary\n"
    "     若宿主用了非默认布局（多智能体各自不同模型），指定正确的配置键：\n"
    "       zhiqi config set provenance.hostModelKey agents.<id>.model.primary\n"
    "  ② 由调用方在本次调用中声明：zhiqi <命令> --model <模型名>\n"
    "  ③ 手动兜底：zhiqi config set provenance.model <模型名>\n"
    "\n"
    "如确需以「未申报」上报（离线/合规例外），显式放行后再执行：\n"
    "  zhiqi config set provenance.requireModel false   # 或单次加 --allow-undeclared"
)

WARNING_UNCONFIGURED = (
    "未配置模型信息且已放行未申报（requireModel=false），将以 UNKNOWN 上报。"
    "建议尽快执行：zhiqi config set provenance.model <模型名>"
)


def skill_version() -> str:
    """自动采集接入端 Skill 自身版本（优先包元数据，其次 __version__）。"""
    try:
        return importlib.metadata.version("zhiqi-agent")
    except Exception:
        pass
    try:
        mod = importlib.import_module("zhiqi_agent")
        return str(getattr(mod, "__version__", "") or "")
    except Exception:
        return ""


def runtime_info() -> Dict[str, str]:
    """自动采集运行环境（OS / Python / OpenClaw），用于本地诊断。"""
    info = {
        "os": platform.system() or "",
        "osVersion": platform.release() or "",
        "arch": platform.machine() or "",
        "python": platform.python_version(),
        "pythonImpl": platform.python_implementation(),
    }
    openclaw = os.environ.get("OPENCLAW_VERSION", "")
    if openclaw:
        info["openclaw"] = openclaw
    return info


def runtime_string() -> str:
    rt = runtime_info()
    s = "%s-%s / python-%s" % (rt.get("os", "?"), rt.get("osVersion", "?"), rt.get("python", "?"))
    if rt.get("openclaw"):
        s += " / openclaw-%s" % rt["openclaw"]
    return s


def _pick(*values: Any) -> str:
    for v in values:
        if v is None:
            continue
        s = str(v).strip()
        if s:
            return s
    return ""


# ---------------------------------------------------------------- 当前模型解析
#
# 为什么必须**按次解析**、且必须能跟随切换：
#   模型随时可以在宿主里切换，而切换不会通知本技能。任何"配置一次"的做法都会在切换后
#   变成**过期的假标识** —— 比"未申报"更糟，因为它看起来像已申报。
# 为什么只读宿主官方配置、绝不读通用环境变量：
#   读宿主自己声明的当前模型 = 读权威事实；读 OPENAI_MODEL / ZHIQI_MODEL 之类 = 猜。
#   猜错就是虚假标识。这条底线不因为"更方便"而放宽。
# 为什么绝不缓存：
#   常驻 daemon 里缓存一次就把"切换后"重新变回"陈旧值"，等于把问题原样搬回来。

# 宿主配置键（按优先级）。不同版本键名不同，因此逐个探测；
# 全部读不到时只能落到"拒绝"，**绝不能沿用上一次的值**。
HOST_MODEL_KEYS = [
    "agents.defaults.model.primary",
    "agents.defaults.model",          # 对象形式：取 primary
]

# 宿主 CLI 是 Node 程序，冷启动实测约 4 秒（Windows 上 cmd→node 更慢）。
# 超时设太短会把**正常**调用也判成失败 —— 真实事故：3 秒超时导致每个候选都被跳过，
# 技能因此永远读不到宿主模型，只能一路拒绝写入；而"手动跑一次"却是成功的，
# 看起来像玄学。这里留足余量。
HOST_CONFIG_TIMEOUT = 15.0

# 记住"哪种调用方式可行"，避免每次都在不可行的形式上白等一个超时。
# 注意：这里缓存的只是**调用方式**，绝不缓存模型名本身 ——
# 缓存模型名就会把"切换后"变回过期假标识，那正是要消灭的问题。
_HOST_CMD_PREFIX = None


# 配置键只允许这个字符集：键名可来自用户配置，而 Windows 上要经 cmd.exe 解析 shim，
# 不做白名单就是把用户配置变成了命令注入面。读不到就返回 None（→ 拒绝），绝不"容错执行"。
_CONFIG_KEY_RE = re.compile(r"^[A-Za-z0-9._-]{1,120}$")


def _host_cli_candidates(key: str):
    """返回若干种调用宿主 CLI 的方式，按顺序尝试。

    为什么需要多种：Windows 上 npm 全局安装留下的是
    **无扩展名的 shim（POSIX shell 脚本）+ .cmd + .ps1**。
    CreateProcess 无法执行无扩展名文件，直接 spawn 会得到 WinError 2；
    必须经 cmd.exe 解析 shim 才行。
    真实事故：Windows 上 _host_config_get 恒为 None → 技能永远读不到宿主模型 →
    只能一路拒绝写入（而 Linux 上一切正常，所以这个问题在开发机上不会暴露）。
    """
    exe = shutil.which("openclaw")
    cmd_shim = shutil.which("openclaw.cmd")
    out = []
    if os.name == "nt":
        if cmd_shim:
            out.append([cmd_shim, "config", "get", key])
        out.append(["cmd", "/c", "openclaw", "config", "get", key])
        if exe:
            out.append([exe, "config", "get", key])
    else:
        if exe:
            out.append([exe, "config", "get", key])
        out.append(["openclaw", "config", "get", key])
    return out


def _host_config_get(key: str) -> Optional[str]:
    """通过宿主官方 CLI 读取配置值。

    只认"官方配置接口"这一个来源。宿主不存在、命令失败、超时，一律返回 None（→ 后续拒绝），
    而不是去别处猜一个值。
    """
    if not key or not _CONFIG_KEY_RE.match(key):
        log.debug("宿主配置键不合法，拒绝读取：%r", key)
        return None

    global _HOST_CMD_PREFIX
    candidates = []
    if _HOST_CMD_PREFIX:
        candidates.append(_HOST_CMD_PREFIX + ["config", "get", key])
    for cmd in _host_cli_candidates(key):
        if not candidates or cmd[:len(cmd) - 3] != _HOST_CMD_PREFIX:
            candidates.append(cmd)

    last_error = None
    for cmd in candidates:
        try:
            r = subprocess.run(cmd, capture_output=True, timeout=HOST_CONFIG_TIMEOUT,
                               encoding="utf-8", errors="replace")
        except Exception as e:                  # noqa: BLE001
            last_error = e
            continue
        if r.returncode == 0 and (r.stdout or "").strip():
            _HOST_CMD_PREFIX = cmd[:len(cmd) - 3]      # 记住可行前缀（不含 config get <key>）
            return r.stdout.strip()
        last_error = (r.stdout or r.stderr or "").strip()[:200]
    log.debug("读取宿主配置失败 key=%s: %s", key, last_error)
    return None


def _normalize_host_model(raw: Optional[str]) -> str:
    """把宿主返回值归一成一个模型名；拿不准就返回空串（不猜）。"""
    if not raw:
        return ""
    s = raw.strip()
    if s.startswith("{"):
        try:
            data = json.loads(s)
        except ValueError:
            return ""
        if isinstance(data, dict):
            for k in ("primary", "model", "name"):
                v = data.get(k)
                if isinstance(v, str) and v.strip():
                    return v.strip()
        return ""
    # CLI 可能带额外行（提示、警告）；取第一行非空输出
    for line in s.splitlines():
        t = line.strip()
        if not t:
            continue
        if "not found" in t.lower():
            return ""
        return t
    return ""


# 测试用的宿主读取钩子：测试必须自证"读不到就拒绝/切换即生效"，而不能依赖
# 跑测试那台机器上恰好装没装、配没配 OpenClaw。留这个钩子是让测试是**确定性**的。
_HOST_GET = None


def resolve_model(prov: Dict[str, Any], cli_model: Optional[str] = None,
                  host_get=None) -> Dict[str, str]:
    """按次解析"当前使用的大模型"。返回 {model, source}；解析不到时 model 为空串。

    优先级（顺序本身就是设计）：
      1. cli            —— 调用方（正在执行的那个智能体）显式声明，最直接
      2. host:<配置键>   —— 从宿主运行时配置读取"此刻"的值（模型切换自动跟随）
      3. configured     —— 手动兜底（兼容/异常场景）
      4. none           —— 一律拒绝，绝不用上一次的值
    """
    get = host_get or _HOST_GET or _host_config_get

    explicit = _pick(cli_model)
    if explicit:
        return {"model": explicit, "source": "cli"}

    # 注意别写成 [x] or DEFAULT —— [""] 是**真值**（非空列表），
    # 于是默认键列表永远不会被用到，宿主读取形同虚设。必须显式判空。
    override_key = _pick(prov.get("hostModelKey"))
    keys = [override_key] if override_key else HOST_MODEL_KEYS
    for key in keys:
        if not key:
            continue
        value = _normalize_host_model(get(key))
        if value:
            return {"model": value, "source": "host:" + key}

    manual = _pick(prov.get("model"))
    if manual:
        return {"model": manual, "source": "configured"}

    return {"model": "", "source": "none"}


def describe(settings: Optional[dict], model: Optional[str] = None,
             model_version: Optional[str] = None,
             agent_version: Optional[str] = None) -> Dict[str, Any]:
    """解析出待上报的 client 对象与本地申报状态。

    模型名**每次调用都重新解析**（命令行 > 宿主运行时配置 > 手动兜底），
    因此宿主里切换模型会自动跟随，不需要通知本技能，也不会写出过期的假标识。
    **环境变量不参与 model/modelVersion 解析**（那是猜；读宿主官方配置才是读事实）。
    """
    prov = ((settings or {}).get("provenance") or {})
    enabled = bool(prov.get("enabled", True))
    # requireModel 默认 **true**：未配置即拒绝写操作。
    # 旧的 provenance.strict 已废弃且**有意不兼容**：DEFAULT_SETTINGS 始终提供 requireModel，
    # 老配置里的 strict=false 会被忽略 —— 方向是"更严"（fail-closed），
    # 用户会被拒绝一次，并在错误信息里看到新的键名与放行方式，不会静默放宽。
    required = bool(prov.get("requireModel", True))

    resolved = resolve_model(prov, cli_model=model)
    resolved_model = resolved["model"]
    resolved_model_version = _pick(model_version, prov.get("modelVersion"))
    resolved_agent_version = _pick(agent_version, prov.get("agentVersion"))

    declared = bool(resolved_model)
    client = {
        "agentVersion": resolved_agent_version,
        "skillVersion": skill_version(),
        "model": resolved_model or UNKNOWN,
        "modelVersion": resolved_model_version,
        # 让读记录的人分得清这个模型名是"调用方声明的"还是"从宿主读到的"（纯新增字段）
        "modelSource": resolved["source"],
    }
    return {
        "enabled": enabled,
        "strict": required,
        "required": required,
        "declared": declared,
        "client": client,
        "modelSource": resolved["source"],
        "warning": None if (declared or not enabled) else WARNING_UNCONFIGURED,
        "runtime": runtime_info(),
        "runtimeString": runtime_string(),
    }


def client_object(settings: Optional[dict], model: Optional[str] = None,
                  model_version: Optional[str] = None,
                  agent_version: Optional[str] = None) -> Optional[Dict[str, str]]:
    """返回请求体要携带的 client 对象；provenance.enabled=false 时返回 None。"""
    desc = describe(settings, model=model, model_version=model_version,
                    agent_version=agent_version)
    return desc["client"] if desc["enabled"] else None


def enforce(desc: Dict[str, Any]) -> None:
    """产生内容的写操作必须携带来源元数据。

    默认（requireModel=true）**未提供模型即拒绝执行**；这是把「入口唯一」变成
    「入口负责」的具体做法，而不是在平台侧留一条「未申报」的正常路径。
    显式设置 provenance.requireModel=false 才放行。
    """
    if desc.get("enabled") and desc.get("required") and not desc.get("declared"):
        raise ZhiQiConfigError(REQUIRE_UNDECLARED)


def warn_if_unconfigured(desc: Dict[str, Any]) -> None:
    """首次写操作未配置元数据时输出一条提醒（不静默失败）。"""
    if desc.get("warning"):
        log.warning("%s", desc["warning"])
