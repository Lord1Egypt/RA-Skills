#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WorkBuddy skill 使用管理指南 · 自包含环境诊断脚本
用法：python usage_diag.py [--json] [--fast] [--offline] [--timeout N] [--state <state.md>] [--version]
功能：检查用户画像完整度、连接器状态、自动化、专家、已装 skill、记忆新鲜度、日志错误、模型配置，
      并判定用户阶段（新用户/进阶用户）。
选项：
  --json        以 JSON 输出（供本 skill 解析；默认人类可读文本）
  --fast        跳过网络/代理检测，只查本地配置（弱网环境推荐）
  --offline     完全离线模式：跳过所有网络相关检查，仅做本地文件扫描
  --timeout N   代理探活超时秒数（默认3秒）
  --state P     读取 state.md 的 onboarding_done 字段（用于用户阶段判定；可省略）
  --version     仅输出版本号
注意：本脚本只"读取+报告"，绝不修改任何配置（修复交由 skill 在交互态执行）。
"""
import json
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from version import VERSION  # noqa: E402  单一版本源 = SKILL.md frontmatter

# 统一 UTF-8 输出，避免 Windows GBK 管道乱码
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass  # 有意忽略：防御性处理，失败不阻断
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass  # 有意忽略：防御性处理，失败不阻断

HOME = Path.home()
WORKBUDDY_DIR = HOME / ".workbuddy"
CONNECTORS_DIR = WORKBUDDY_DIR / "connectors"
EXPERTS_DIR = WORKBUDDY_DIR / "plugins" / "marketplaces" / "my-experts" / "plugins"
SKILLS_DIR = WORKBUDDY_DIR / "skills"
LOGS_DIR = WORKBUDDY_DIR / "logs"
MEMORY_DIR = WORKBUDDY_DIR / "MEMORY.md"

OK, FAIL, WARN, INFO = "[OK]", "[FAIL]", "[WARN]", "[INFO]"

# 常见 sqlite 错误 → 用户可读文案（供 check_automations 使用）
SQLITE_ERROR_MAP = [
    ("no such table", "自动化数据表不存在（可能尚未创建过自动化任务，属正常情况）"),
    ("unable to open database file", "数据库文件无法打开（WorkBuddy 正在运行或文件被占用，请稍后重试）"),
    ("database is locked", "数据库被占用（WorkBuddy 正在运行，请稍后重试或先退出再检查）"),
    ("no such column", "自动化数据表结构异常（WorkBuddy 版本升级过？建议重启 WorkBuddy 后重试）"),
]


def _friendly_sqlite_error(e):
    """把 sqlite 原生报错转成用户能看懂的话"""
    msg = str(e)
    for pattern, hint in SQLITE_ERROR_MAP:
        if pattern in msg:
            return hint
    return f"读取自动化数据出错，详情：{msg}（可重启 WorkBuddy 后重试）"


def _read_text(p):
    try:
        return p.read_text(encoding="utf-8")
    except Exception:
        return ""


def check_profile():
    """用户画像完整度：SOUL.md / USER.md / MEMORY.md 存在性与字数"""
    res = {}
    for name, path in (("SOUL.md", WORKBUDDY_DIR / "SOUL.md"),
                        ("USER.md", WORKBUDDY_DIR / "USER.md"),
                        ("MEMORY.md", MEMORY_DIR)):
        if path.exists():
            size = len(_read_text(path))
            res[name] = {"exists": True, "chars": size,
                         "thin": size < 200}
        else:
            res[name] = {"exists": False, "chars": 0, "thin": True}
    return res


def check_connectors():
    """连接器配置与启用状态。

    重要语义澄清（修复"虚报已启用 106 个"）：
      - connector-states.json 的 enabled 列表是**官方连接器目录（catalog）**，代表"可用/已声明"的连接器，
        并不代表实时连接态（实时连接态以本会话注入的 connector-status 为准，脚本无法可靠判定）。
      - 因此 enabled_raw 仅作为信息性字段 `declared`（已声明可用目录数），**绝不**赋给 `connected`。
      - `connected` 只在脚本能拿到明确实时连接证据（states 含 connected:true 标志，或 mcp 健康检查通过）
        时才填充；默认空列表。
      - 设置 `live_status_unreliable: true` 提示调用方：脚本判定的连接态不可靠，请务必以本会话
        connector-status 覆盖（避免把"目录数"误当"已连接数"）。
    """
    res = {"sessions": [], "live_status_unreliable": True}
    if not CONNECTORS_DIR.exists():
        res["error"] = "无连接器目录"
        return res
    sessions = [d for d in CONNECTORS_DIR.iterdir()
                if d.is_dir() and d.name not in ("default", "skills")]
    for session in sorted(sessions):
        item = {"session": session.name, "declared": [], "connected": [], "has_mcp": False}
        states_file = session / "connector-states.json"
        declared_raw = []
        if states_file.exists():
            try:
                states = json.loads(_read_text(states_file))
                declared_raw = states.get("enabled", [])
                item["declared"] = declared_raw
            except json.JSONDecodeError:
                item["states_error"] = True
        mcp_file = session / "mcp.json"
        if mcp_file.exists():
            item["has_mcp"] = True
            try:
                cfg = json.loads(_read_text(mcp_file))
                # 连接器声明可能在 mcpServers 键下（WorkBuddy 实际结构），兜底读顶层
                mcp_map = cfg.get("mcpServers", cfg) if isinstance(cfg, dict) else {}
                item["disabled"] = [k for k, v in mcp_map.items()
                                    if k.startswith("connector:") and isinstance(v, dict)
                                    and v.get("disabled")]
            except json.JSONDecodeError:
                item["mcp_error"] = True
        # 综合判定：脚本无法可靠判定实时连接态，connected 默认空列表。
        # 仅当 states 含明确的 connected:true 实时标志时才填充（极少数实现会有，保留以兼容未来结构）；
        # 绝不可把 declared（目录）当作 connected（实时）。
        connected = []
        if isinstance(declared_raw, dict) and declared_raw.get("connected") is True:
            connected = [k for k, v in declared_raw.items()
                         if k != "connected" and v] or []
        item["connected"] = connected
        res["sessions"].append(item)
    return res


def check_automations():
    res = {"count": 0, "active": 0, "items": []}
    db = WORKBUDDY_DIR / "workbuddy.db"
    if not db.exists():
        res["error"] = "无 workbuddy.db"
        return res
    try:
        import sqlite3
        conn = sqlite3.connect(str(db))
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='automations'")
        if not cur.fetchone():
            res["error"] = "无 automations 表"
            conn.close()
            return res
        cur.execute("SELECT name, status, rrule FROM automations")
        for name, status, rrule in cur.fetchall():
            res["count"] += 1
            if status and status.upper() == "ACTIVE":
                res["active"] += 1
            res["items"].append({"name": name, "status": status,
                                 "rrule": rrule or ""})
        conn.close()
    except Exception as e:
        res["error"] = _friendly_sqlite_error(e)
    return res


def check_experts():
    if not EXPERTS_DIR.exists():
        return {"count": 0}
    experts = [d for d in EXPERTS_DIR.iterdir() if d.is_dir()]
    return {"count": len(experts), "names": [e.name for e in experts]}


def _read_skill_version(skill_md: Path):
    """从 skill 的 SKILL.md frontmatter 读 version 字段（无则 None）。"""
    try:
        text = skill_md.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None
    m = re.search(r"^version:\s*([0-9][^\s\r\n]*)", text, re.MULTILINE)
    return m.group(1).strip().strip('"').strip("'") if m else None


def check_skills():
    """已装 skill 统计（含 version）。

    正确处理命名空间目录（如 `@org-gv4zgi7j/`）：
      - 顶层 `@xxx/` 是命名空间，非 skill，须递归进入统计其下的真实 skill；
      - 顶层普通目录若含 SKILL.md 才算 skill；
      - 命名空间下用 `ns/slug` 命名，便于 install_skill 去重已装。
    返回 {count, names, versions}：versions 为 {name: version}。
    """
    if not SKILLS_DIR.exists():
        return {"count": 0, "names": [], "versions": {}}
    # 本 skill 自身的可能目录名：按 name 装 / skillhub 装（slug 加 __skillhub 后缀）
    # 含新旧 name（auto-assistant→skill-assistant）与两种 skillhub slug，避免把自身误判为第三方 skill
    self_names = {"workbuddy-skill-assistant", "workbuddy-skill-assistant__skillhub",
                  "workbuddy-auto-assistant", "workbuddy-assistant__skillhub"}

    def _is_skill_dir(d):
        return d.is_dir() and (d / "SKILL.md").exists()

    names = []
    versions = {}
    for d in sorted(SKILLS_DIR.iterdir()):
        if d.name in self_names:
            continue
        if not d.is_dir():
            continue
        if d.name.startswith("@"):
            # 命名空间目录：递归统计其下的真实 skill
            for sub in sorted(d.iterdir()):
                if _is_skill_dir(sub):
                    nm = f"{d.name}/{sub.name}"
                    names.append(nm)
                    versions[nm] = _read_skill_version(sub / "SKILL.md")
        elif _is_skill_dir(d):
            names.append(d.name)
            versions[d.name] = _read_skill_version(d / "SKILL.md")
    return {"count": len(names), "names": names, "versions": versions}


def check_memory_freshness():
    """每日 memory 日志新鲜度（.workbuddy/memory/YYYY-MM-DD.md）

    同时扫描两个位置、取较新者，避免"在项目级 .workbuddy/memory/ 写日志"的用户
    被漏判为"记忆不新鲜"而永远封顶 intermediate（F6 修复）：
      - 用户级：~/.workbuddy/memory/（跨项目通用记忆）
      - 项目级：当前工作目录下的 .workbuddy/memory/（本 skill 推荐做法，每日日期日志落此）
    只统计日期命名的日志（YYYY-MM-DD.md），忽略 agent-mail 等会话记忆文件
    （如 bc701f2e-..._memory.md，系统生成、非用户活动），避免误判"每日日志已过期"。
    """
    def _is_date_stem(stem):
        try:
            time.strptime(stem, "%Y-%m-%d")
            return True
        except Exception:
            return False

    user_mem = WORKBUDDY_DIR / "memory"
    proj_mem = Path.cwd() / ".workbuddy" / "memory"   # 当前 workspace 项目级记忆
    candidates = [user_mem]
    if proj_mem != user_mem:
        candidates.append(proj_mem)

    logs = []
    has_any_dir = False
    found_dirs = []
    for d in candidates:
        if not d.exists() or not d.is_dir():
            continue
        has_any_dir = True
        found_dirs.append(str(d))
        for p in d.glob("*.md"):
            if _is_date_stem(p.stem):
                logs.append(p)

    if not has_any_dir:
        return {"has_dir": False, "last": None, "days_since": None, "sources": []}
    if not logs:
        return {"has_dir": True, "last": None, "days_since": None, "sources": found_dirs}
    logs.sort(key=os.path.getmtime, reverse=True)
    last = logs[0].stem
    try:
        last_ts = time.mktime(time.strptime(last, "%Y-%m-%d"))
        days = int((time.time() - last_ts) / 86400)
    except Exception:
        days = None
    return {"has_dir": True, "last": last, "days_since": days,
            "sources": sorted({str(p.parent) for p in logs})}


def check_logs():
    """最近 7 天日志扫描（logs/*.log）。

    返回：
      files_with_errors —— 含错误痕迹的文件数
      recent_errors     —— 例行 ERROR/Error 总行数（封顶 999，避免噪音数字）
      severe_errors     —— 严重痕迹（FATAL/CRITICAL/Traceback）行数，只有它才触发 issue
    """
    if not LOGS_DIR.exists():
        return {"has_dir": False, "files_with_errors": 0, "recent_errors": 0, "severe_errors": 0}
    cutoff = time.time() - 7 * 86400
    files_with_errors = 0
    recent_errors = 0
    severe_errors = 0
    for f in LOGS_DIR.glob("*.log"):
        try:
            if f.stat().st_mtime < cutoff:
                continue
            text = _read_text(f)
        except Exception:
            continue
        has_err = False
        for line in text.splitlines():
            if any(k in line for k in ("FATAL", "CRITICAL", "Traceback")):
                severe_errors += 1
                has_err = True
            elif any(k in line for k in ("ERROR", "Error:")):
                recent_errors += 1
                has_err = True
        if has_err:
            files_with_errors += 1
    return {"has_dir": True,
            "files_with_errors": files_with_errors,
            "recent_errors": min(recent_errors, 999),
            "severe_errors": severe_errors}


def check_models():
    """models.json 存在性与 JSON 合法性"""
    cfg = WORKBUDDY_DIR / "models.json"
    if not cfg.exists():
        return {"exists": False, "valid": False}
    try:
        json.loads(_read_text(cfg))
        return {"exists": True, "valid": True}
    except json.JSONDecodeError:
        return {"exists": True, "valid": False}


def proxy_reachable(timeout=3, retry=2, backoff=(2, 5)):
    """探活 127.0.0.1:51103，支持超时和重试（默认重试 2 次，退避 2s/5s）"""
    import subprocess
    for attempt in range(retry + 1):
        try:
            r = subprocess.run(
                ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
                 "--max-time", str(timeout),
                 "http://127.0.0.1:51103/health"],
                capture_output=True, text=True, timeout=timeout + 2)
            if r.stdout.strip() == "200":
                return True
        except Exception:
            if attempt < retry:
                time.sleep(backoff[min(attempt, len(backoff) - 1)])  # 退避 2s/5s
            continue
    return False


def read_onboarding_done(state_path):
    """从 state.md 读取 onboarding_done 布尔值（缺失视为未完成）。"""
    if not state_path:
        return None
    p = Path(state_path)
    if not p.exists():
        return None
    try:
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("onboarding_done:"):
                return line.split(":", 1)[1].strip().lower() in ("true", "1", "yes")
    except Exception:
        return None
    return None


def classify_user_tier(onboarding_done, profile, skills, automations, memory_freshness=None):
    """综合画像信号判定用户阶段（三级分层，与 checklist.md 的 L1/L2/L3 对应）。

    返回三元组 (tier, reasons, profile_ready)：
      tier          —— "beginner"（初级）/ "intermediate"（进阶·核心受众）/ "advanced"（高级）
      reasons       —— 判定原因列表（初级=命中原因；高级=达标说明；进阶为空）
      profile_ready —— 画像完整度布尔值（SOUL.md / USER.md 均存在且非过薄；
                       内部用，供 report_builder / 上层判断"是否需要初始化引导"）

    初级（任一命中）：
      1. onboarding_done == False
      2. 画像不完整：SOUL.md 或 USER.md 缺失 / 过薄（<200 字）
      3. 完全未起步：已装 skill = 0 且 ACTIVE 自动化 = 0

    高级（全部满足）：
      1. 画像完整（profile_ready）
      2. 已装 skill ≥ 15
      3. ACTIVE 自动化 ≥ 2
      4. 记忆日志新鲜（days_since ≤ 7）

    其余 → 进阶（本 skill 的核心受众）。
    """
    reasons = []
    profile_ready = True

    # 信号 2：画像完整度
    for name in ("SOUL.md", "USER.md"):
        info = profile.get(name, {})
        if not info.get("exists") or info.get("thin"):
            profile_ready = False
            reasons.append(f"{name} 缺失或过薄")

    # 信号 1：初始化引导
    if onboarding_done is False:
        reasons.append("未完成初始化引导")

    # 信号 3：完全未起步
    skills_count = skills.get("count", 0) or 0
    active_auto = automations.get("active", 0) or 0
    if skills_count == 0 and active_auto == 0:
        reasons.append("无已装 skill 且无 ACTIVE 自动化")

    if reasons:
        return "beginner", reasons, profile_ready

    # 高级判定（全部满足才晋升）
    mem_days = (memory_freshness or {}).get("days_since")
    advanced_checks = [
        (profile_ready, "画像完整"),
        (skills_count >= 15, f"已装 skill {skills_count} 个（≥15）"),
        (active_auto >= 2, f"ACTIVE 自动化 {active_auto} 个（≥2）"),
        (mem_days is not None and mem_days <= 7,
         f"记忆日志新鲜（{mem_days} 天前）" if mem_days is not None else "无记忆日志"),
    ]
    if all(ok for ok, _ in advanced_checks):
        return "advanced", [label for _, label in advanced_checks], profile_ready

    return "intermediate", [], profile_ready


# —— 模式 D · 最佳实践达标检查（A 层确定性项）——
# 达标判据的数值阈值就地定义，与 best-practices/checklist.md 的「达标判据」严格对齐。
# 改这里的数 = 改判据，请同步改 checklist.md 对应项的判据文字。
SKILL_MAX = 30          # C-skill-01 · 已装 skill 上限
MEM_MAX_DAYS = 7        # C-mem-02 · 记忆日志新鲜度上限（天）
PROFILE_MIN = 200       # C-mem-01 · SOUL.md / USER.md 最少字数
AUTO_USED_DAYS = 30     # C-auto-03 · 自动化"真在跑"的近用天数
AUTO_STALE_DAYS = 90    # C-auto-03 · 超过此天数没跑过 = 装了没在用
CONN_USED_DAYS = 30     # C-conn-02 · 连接器有调用痕迹的近用天数


def _frontmatter_keys(text):
    """极简 frontmatter 顶层键提取（合法性启发式，非完整 YAML 解析）。"""
    keys = set()
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return keys
    for ln in lines[1:]:
        if ln.strip() == "---":
            break
        m = re.match(r"^([A-Za-z_][\w-]*)\s*:", ln)
        if m:
            keys.add(m.group(1))
    return keys


def check_skill_frontmatter():
    """C-skill-03a：每个已装 SKILL.md frontmatter 含 WorkBuddy 强制字段 name/description。

    说明：WorkBuddy 规范中 SKILL.md 强制 frontmatter 为 name + description（slug 由
    目录名推导、triggers/version 为可选），故仅校验这两项，避免把健康生态误判为不合规。
    """
    res = check_skills()
    invalid = []
    for nm in res.get("names", []):
        parts = nm.split("/")
        p = SKILLS_DIR / parts[0] / parts[1] / "SKILL.md" if len(parts) > 1 \
            else SKILLS_DIR / parts[0] / "SKILL.md"
        if not p.exists():
            invalid.append((nm, "无 SKILL.md")); continue
        keys = _frontmatter_keys(_read_text(p))
        if not keys:
            invalid.append((nm, "frontmatter 非法/缺失")); continue
        missing = [k for k in ("name", "description") if k not in keys]
        if missing:
            invalid.append((nm, "缺字段:" + ",".join(missing)))
    return {"total": len(res.get("names", [])), "invalid": invalid}


def check_duplicate_slugs():
    """C-skill-06：无同 slug 跨命名空间重复（如 @user_x/foo 与 foo 并存）。"""
    res = check_skills()
    slugs = {}
    for nm in res.get("names", []):
        slugs.setdefault(nm.split("/")[-1], []).append(nm)
    return {"dups": [(s, o) for s, o in slugs.items() if len(o) > 1]}


def check_automation_usage(auto_used_days):
    """C-auto-03：ACTIVE 自动化是否真在跑（读 automation_runtime_state.last_run，按近用天数分级）。"""
    db = WORKBUDDY_DIR / "workbuddy.db"
    if not db.exists():
        return {"has_active": False, "days": None, "evidence": "无 workbuddy.db"}
    try:
        import sqlite3
        conn = sqlite3.connect(str(db)); cur = conn.cursor()
        cur.execute("SELECT a.status, COALESCE(rt.last_run_at, a.last_run_at) "
                    "FROM automations a LEFT JOIN automation_runtime_state rt ON a.id=rt.automation_id")
        rows = cur.fetchall(); conn.close()
    except Exception as e:
        return {"has_active": False, "days": None, "evidence": _friendly_sqlite_error(e)}
    active = [r for r in rows if r[0] and r[0].upper() == "ACTIVE"]
    if not active:
        return {"has_active": False, "days": None, "evidence": "无 ACTIVE 自动化（见 C-auto-01）"}
    runs = [r[1] for r in active if r[1] is not None]
    if not runs:
        return {"has_active": True, "days": 9999,
                "evidence": f"ACTIVE 自动化 {len(active)} 个，但均无运行记录"}
    max_run = max(runs)
    days = int((time.time() - (max_run / 1000 if max_run > 1e12 else max_run)) / 86400)
    return {"has_active": True, "days": days,
            "evidence": f"ACTIVE 自动化 {len(active)} 个，最近运行 {days} 天前"}


def check_connector_usage(conn_used_days):
    """C-conn-02：已连接连接器近 N 天是否有调用痕迹（扫 logs 的 mcp__ 调用；保守：无痕迹→na，不 fail）。"""
    if not LOGS_DIR.exists():
        return {"days": None, "evidence": "无 logs 目录"}
    cutoff = time.time() - conn_used_days * 86400
    latest = None; hits = 0
    for f in LOGS_DIR.glob("*.log"):
        try:
            mtime = f.stat().st_mtime
        except Exception:
            continue
        if mtime < cutoff:
            continue
        for line in _read_text(f).splitlines():
            if "mcp__" in line:
                hits += 1
                if latest is None or mtime > latest:
                    latest = mtime
    if hits == 0:
        return {"days": None,
                "evidence": f"近 {conn_used_days} 天日志无连接器(mcp__)调用痕迹 → na"}
    days = int((time.time() - latest) / 86400)
    return {"days": days, "hits": hits,
            "evidence": f"近 {conn_used_days} 天日志有 {hits} 处连接器调用痕迹，最近 {days} 天前"}


def _cl_item(iid, domain, status, evidence, severity="P1"):
    """生成一条 A 层 checklist 项。

    status —— pass / fail / na
    """
    return {"id": iid, "domain": domain, "status": status,
            "evidence": evidence, "severity": severity}


def check_checklist(report, offline=False):
    """A 层确定性 checklist 项（仅这些可由脚本判定；B/C 层由 agent 在会话内判后回写 state.md）。

    返回 dict：
      items      —— [{"id","domain","status","evidence","severity"}, ...]，status ∈ pass/fail/na
      score      —— 二进制达标率 round(passed / applicable * 100)，applicable==0 时 0
      applicable —— 计入分母的项数（na 不计入）
      passed     —— 达标项数
    """
    items = []

    # —— 基础项：画像 / 记忆 / 自动化 / skill / 连接器 / 模型 ——
    # C-mem-01 记忆画像完整（SOUL.md 且 USER.md 均 ≥PROFILE_MIN 字）
    p = report.get("profile", {})
    soul = p.get("SOUL.md", {})
    user = p.get("USER.md", {})
    soul_ok = soul.get("exists") and not soul.get("thin")
    user_ok = user.get("exists") and not user.get("thin")
    items.append(_cl_item(
        "C-mem-01", "记忆", "pass" if (soul_ok and user_ok) else "fail",
        f"SOUL.md {'≥'+str(PROFILE_MIN)+'字' if soul_ok else '缺失/过薄'} · USER.md {'≥'+str(PROFILE_MIN)+'字' if user_ok else '缺失/过薄'}",
        severity="P1"))

    # C-auto-01 至少 1 个 ACTIVE 自动化
    a = report.get("automations", {})
    active = a.get("active", 0) or 0
    items.append(_cl_item(
        "C-auto-01", "自动化", "pass" if active >= 1 else "fail",
        f"ACTIVE 自动化 {active} 个（共 {a.get('count', 0)} 个）",
        severity="P2"))

    # C-skill-01 skill 精简（0 个 → na；≤阈值 → pass；>阈值 → fail）
    skills = report.get("skills", {})
    scount = skills.get("count", 0) or 0
    if scount == 0:
        items.append(_cl_item("C-skill-01", "skill", "na", "未安装任何 skill", severity="P1"))
    elif scount <= SKILL_MAX:
        items.append(_cl_item("C-skill-01", "skill", "pass",
                               f"已装 {scount} 个 skill（≤ {SKILL_MAX}）", severity="P1"))
    else:
        items.append(_cl_item("C-skill-01", "skill", "fail",
                               f"已装 {scount} 个 skill（> {SKILL_MAX}，偏多）", severity="P1"))

    # C-skill-02 生态维护类 skill（skill-check / skill-map）
    names = [str(n) for n in skills.get("names", [])]
    has_maintainer = any("skill-check" in n or "skill-map" in n for n in names)
    items.append(_cl_item(
        "C-skill-02", "skill", "pass" if has_maintainer else "fail",
        ("已装 " + ", ".join(n for n in names if "skill-check" in n or "skill-map" in n)) if has_maintainer else "未装 skill-check / skill-map",
        severity="P2"))

    # C-skill-03a 每个 SKILL.md frontmatter 含关键键
    fm = check_skill_frontmatter()
    if fm["invalid"]:
        items.append(_cl_item("C-skill-03a", "skill", "fail",
                               f"{len(fm['invalid'])}/{fm['total']} 个 SKILL.md frontmatter 不合规："
                               + "；".join(f"{n}:{r}" for n, r in fm["invalid"][:3]),
                               severity="P2"))
    elif fm["total"] == 0:
        items.append(_cl_item("C-skill-03a", "skill", "na", "未安装任何 skill", severity="P2"))
    else:
        items.append(_cl_item("C-skill-03a", "skill", "pass",
                               f"{fm['total']} 个 SKILL.md frontmatter 均含强制字段 name/description",
                               severity="P2"))

    # C-skill-06 无同 slug 跨命名空间重复
    dup = check_duplicate_slugs()
    if dup["dups"]:
        items.append(_cl_item("C-skill-06", "skill", "fail",
                               "重复 slug：" + "；".join(f"{s}→" + "/".join(o) for s, o in dup["dups"][:3]),
                               severity="P2"))
    else:
        items.append(_cl_item("C-skill-06", "skill", "pass", "无同 slug 跨命名空间重复", severity="P2"))

    # C-conn-01 至少 1 个 session 有实时已连接连接器
    conn = report.get("connectors", {})
    if conn.get("error"):
        items.append(_cl_item("C-conn-01", "连接器", "na", conn.get("error", "无连接器目录"), severity="P1"))
    else:
        sessions = conn.get("sessions", [])
        connected_all = []
        for s in sessions:
            connected_all.extend(s.get("connected", []))
        if connected_all:
            preview = "、".join(connected_all[:3])
            items.append(_cl_item("C-conn-01", "连接器", "pass",
                                   f"实时已连接 {len(connected_all)} 个连接器（{preview}…）", severity="P1"))
        else:
            items.append(_cl_item("C-conn-01", "连接器", "fail",
                                   "无实时已连接连接器（脚本读 connector-states.json 的 enabled 仅代表已声明可用目录，非实时连接；请以本会话 connector-status 为准）",
                                   severity="P1"))

    # —— 记忆质量：写得新不新、写得有没有用 ——
    # C-mem-02 记忆日志新鲜（≤ MEM_MAX_DAYS 天）
    mf = report.get("memory_freshness", {})
    days = mf.get("days_since")
    if days is None:
        items.append(_cl_item("C-mem-02", "记忆", "na", "无日期记忆日志", severity="P1"))
    elif days <= MEM_MAX_DAYS:
        items.append(_cl_item("C-mem-02", "记忆", "pass",
                               f"最近记忆日志 {mf.get('last')}（{days} 天前）", severity="P1"))
    else:
        items.append(_cl_item("C-mem-02", "记忆", "fail",
                               f"记忆日志已 {days} 天未更新（> {MEM_MAX_DAYS}）", severity="P1"))

    # —— 配置利用度：装了到底有没有在用 ——
    # C-auto-03 自动化使用度（读 automation_runtime_state.last_run 按近用天数判定）
    auto_use = check_automation_usage(auto_used_days=AUTO_USED_DAYS)
    auto_days = auto_use.get("days")
    if auto_days is None:
        auto_status = "na"
    elif auto_days <= AUTO_STALE_DAYS:
        auto_status = "pass"
    else:
        auto_status = "fail"
    items.append(_cl_item(
        "C-auto-03", "自动化", auto_status, auto_use.get("evidence", ""),
        severity="P2"))

    # C-conn-02 连接器使用度（扫 logs 的 mcp__ 调用痕迹；保守：无痕迹 → na 不 fail）
    conn_use = check_connector_usage(conn_used_days=CONN_USED_DAYS)
    conn_status = "na" if conn_use.get("days") is None else "pass"
    items.append(_cl_item(
        "C-conn-02", "连接器", conn_status, conn_use.get("evidence", ""),
        severity="P2"))

    # —— 聚合 ——
    applicable = [it for it in items if it["status"] != "na"]
    passed = [it for it in applicable if it["status"] == "pass"]
    score = round(len(passed) / len(applicable) * 100) if applicable else 0

    return {
        "items": items,
        "score": score,
        "applicable": len(applicable),
        "passed": len(passed),
    }


def diagnose(fast=False, offline=False, timeout=3, state_path=None):
    report = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "proxy_ok": None if (fast or offline) else proxy_reachable(timeout=timeout),
        "offline_mode": offline,
        "profile": check_profile(),
        "connectors": check_connectors(),
        "automations": check_automations(),
        "experts": check_experts(),
        "skills": check_skills(),
        "memory_freshness": check_memory_freshness(),
        "logs": check_logs(),
        "models": check_models(),
        "version": VERSION,
    }
    # 简单健康评分（供 skill 判断"有无新发现"）
    # 维度扣分封顶（合计 100）：画像20 / 连接器20 / 自动化20 / skill15 / memory10 / logs10 / models5
    # 各维度实际累加值 ≤ cap（如画像每文件 +8、双文件最多 16 ≤ 20），最终 health = 100 - Σ min(实际扣分, cap)
    issues = []
    fix_hints = {}
    issue_items = []  # 结构化：{text, severity(P0/P1/P2), fix_hint}，供 report_builder 分级渲染

    def _add(issue, hint, severity="P1"):
        issues.append(issue)
        fix_hints[issue] = hint
        issue_items.append({"text": issue, "severity": severity, "fix_hint": hint})

    dimension_deductions = {"profile": 0, "connectors": 0, "automations": 0, "skills": 0,
                            "memory": 0, "logs": 0, "models": 0}
    DIM_CAPS = {"profile": 20, "connectors": 20, "automations": 20, "skills": 15,
                "memory": 10, "logs": 10, "models": 5}

    p = report["profile"]
    for f in ("SOUL.md", "USER.md"):
        if not p.get(f, {}).get("exists") or p.get(f, {}).get("thin"):
            _add(f"{f} 缺失或过薄",
                 f"在对话中说「初始化引导」，2 分钟聊天式补齐；或用 config-templates/soul-setup-template.md 手填",
                 "P1")
            dimension_deductions["profile"] += 8
    for s in report["connectors"].get("sessions", []):
        if not s.get("connected"):
            _add(f"会话 {s['session']} 无实时已连接连接器",
                 f"实时连接态以本会话 connector-status 为准：已连接的正常使用；未连接的在连接器管理页启用或重连（OAuth 类点 Trust 重新授权），详见 config-templates/connector-quick-ref.md 新手上路节",
                 "P1")
            dimension_deductions["connectors"] += 8
    a = report["automations"]
    if a.get("count", 0) == 0:
        _add("无任何自动化任务",
             "让主动式检查跑起来：说「启用主动监护」或参考 config-templates/automation-templates.md 建一个每日检查任务",
             "P1")
        dimension_deductions["automations"] += 13
    elif a.get("active", 0) == 0:
        _add("自动化任务全部非 ACTIVE",
             "用 automation_update 把 status 改为 ACTIVE；对照 automation-templates.md 的 rrule 速查检查触发时间",
             "P1")
        dimension_deductions["automations"] += 13
    if report["skills"]["count"] == 0:
        _add("未安装任何 skill",
             "说「推荐 skill」按你的画像装第一个技能；或从 WorkBuddy 推荐市场直接安装",
             "P2")
        dimension_deductions["skills"] += 15
    mf = report["memory_freshness"]
    if mf.get("days_since") is not None and mf["days_since"] > 7:
        _add(f"memory 日志已 {mf['days_since']} 天未更新",
             "今天做点实质工作后记一笔到 .workbuddy/memory/，或让任意 skill 完成任务后自动写日志",
             "P2")
        dimension_deductions["memory"] += 10
    logs = report["logs"]
    # 例行 ERROR 行属噪音，不计 issue；仅 FATAL/CRITICAL/Traceback 才报警（避免误打扰）
    if logs.get("severe_errors", 0) > 0:
        _add(f"最近 7 天日志有 {logs['severe_errors']} 条严重错误痕迹",
             "打开 ~/.workbuddy/logs/ 看最近 .log 的 FATAL/CRITICAL/Traceback，定位后重启或修复对应连接器",
             "P2")
        dimension_deductions["logs"] += 5
    models = report["models"]
    if not models.get("exists"):
        _add("models.json 缺失",
             "属可选项；如用到自定义模型配置，可从 WorkBuddy 设置导出或对照配置模板重建",
             "P2")
        dimension_deductions["models"] += 5
    elif not models.get("valid"):
        _add("models.json JSON 损坏",
             "用 jsonlint 或 python -m json.tool models.json 校验并修正语法",
             "P0")
        dimension_deductions["models"] += 5

    report["issues"] = issues
    report["fix_hints"] = fix_hints  # 与 issues 并行，issues 保持字符串数组（向后兼容）
    report["issue_items"] = issue_items
    report["issue_count"] = len(issues)
    deduction = 0
    for dim, val in dimension_deductions.items():
        deduction += min(val, DIM_CAPS[dim])
    report["health_score"] = max(0, 100 - deduction)

    # 用户阶段判定（综合画像信号 → tier）
    ob_done = read_onboarding_done(state_path)
    tier, tier_reasons, profile_ready = classify_user_tier(
        ob_done, report["profile"], report["skills"], report["automations"],
        report.get("memory_freshness"))
    report["onboarding_done"] = ob_done
    report["profile_ready"] = profile_ready
    report["tier"] = tier
    report["tier_reasons"] = tier_reasons

    # 模式 D · 最佳实践达标检查（A 层确定性项）
    cl = check_checklist(report, offline=offline)
    report["checklist"] = cl["items"]
    report["checklist_score"] = cl["score"]          # 二进制达标率（向后兼容）
    report["checklist_applicable"] = cl["applicable"]
    report["checklist_pass"] = cl["passed"]

    return report


def main():
    if "--version" in sys.argv:
        print(VERSION)
        return
    fast = "--fast" in sys.argv
    offline = "--offline" in sys.argv
    as_json = "--json" in sys.argv

    # parse --timeout N
    timeout = 3
    for i, arg in enumerate(sys.argv):
        if arg == "--timeout" and i + 1 < len(sys.argv):
            try:
                timeout = int(sys.argv[i + 1])
            except ValueError:
                pass  # 有意忽略：防御性处理，失败不阻断

    # parse --state <path>
    state_path = None
    for i, arg in enumerate(sys.argv):
        if arg == "--state" and i + 1 < len(sys.argv):
            state_path = sys.argv[i + 1]

    rep = diagnose(fast=fast, offline=offline, timeout=timeout, state_path=state_path)
    if as_json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
        return
    # 人类可读
    print("=== WorkBuddy skill 使用管理指南 · 环境诊断 ===")
    if offline:
        print(f"{INFO} 离线模式：跳过所有网络检查")
    if rep["proxy_ok"] is True:
        print(f"{OK} 代理正常")
    elif rep["proxy_ok"] is False:
        print(f"{FAIL} 代理无响应（建议重启 WorkBuddy 后重试；弱网环境可加 --offline 跳过网络检查，本地检查不受影响）")
    elif rep.get("offline_mode"):
        print(f"{INFO} 代理检测跳过(--offline)")
    else:
        print(f"{INFO} 代理检测跳过(--fast)")
    p = rep["profile"]
    for f in ("SOUL.md", "USER.md", "MEMORY.md"):
        st = p.get(f, {})
        flag = OK if st.get("exists") and not st.get("thin") else WARN
        print(f"{flag} {f}: {'存在 '+str(st.get('chars'))+'字' if st.get('exists') else '缺失'}")
    c = rep["connectors"]
    if "error" in c:
        print(f"{WARN} 连接器: {c['error']}")
    else:
        for s in c["sessions"]:
            n = len(s.get("connected", []))
            flag = OK if n > 0 else WARN
            print(f"{flag} 连接器会话 {s['session']}: 已启用 {n} 个" + (
                f"，禁用 {s.get('disabled')}" if s.get("disabled") else ""))
    a = rep["automations"]
    if "error" in a:
        print(f"{WARN} 自动化: {a['error']}")
    else:
        print(f"{OK if a['active']>0 else WARN} 自动化: {a['active']}/{a['count']} ACTIVE")
    print(f"{OK if rep['experts']['count']>0 else WARN} 专家: {rep['experts']['count']} 个")
    print(f"{OK if rep['skills']['count']>0 else WARN} 已装 skill: {rep['skills']['count']} 个")
    mf = rep["memory_freshness"]
    if mf.get("last"):
        print(f"{OK if (mf.get('days_since') or 99)<=7 else WARN} memory 日志最新: {mf['last']} ({mf.get('days_since')}天前)")
    else:
        print(f"{WARN} memory 日志: 无")
    logs = rep["logs"]
    sev = logs.get("severe_errors", 0)
    print(f"{WARN if sev>0 else OK} 日志(7天): 例行错误 {logs.get('recent_errors',0)} 行 / 严重痕迹 {sev} 条")
    models = rep["models"]
    if models.get("exists") and models.get("valid"):
        print(f"{OK} models.json: 存在且合法")
    elif models.get("exists"):
        print(f"{WARN} models.json: 存在但 JSON 损坏")
    else:
        print(f"{INFO} models.json: 缺失(可选项)")
    print(f"版本: {rep.get('version', VERSION)}")
    tier_label = {"beginner": "初级用户(beginner)", "intermediate": "进阶用户(intermediate)",
                  "advanced": "高级用户(advanced)"}.get(rep.get("tier"), "未判定")
    reasons = rep.get("tier_reasons") or []
    print(f"用户阶段: {tier_label}" + (f"（{'；'.join(reasons)}）" if reasons else ""))
    print(f"\n健康评分: {rep['health_score']}/100")
    cl = rep.get("checklist") or []
    if cl:
        print(f"最佳实践达标(A层): {rep.get('checklist_pass', 0)}/{rep.get('checklist_applicable', 0)} 项达标")
        for it in cl:
            mark = {"pass": "[OK]", "fail": "[FAIL]", "na": "[NA]"}.get(it.get("status"), "[?]")
            print(f"  {mark} {it.get('id')} [{it.get('domain')}] {it.get('evidence','')}")
    if rep["issues"]:
        print("发现项（附修复建议）:")
        sev_map = {x["text"]: x["severity"] for x in rep.get("issue_items", [])}
        hints = rep.get("fix_hints", {})
        for i in rep["issues"]:
            sev = sev_map.get(i, "P1")
            print(f"  - [{sev}] {i}")
            if i in hints:
                print(f"    建议: {hints[i]}")
    else:
        print("未发现明显问题。")


if __name__ == "__main__":
    main()
