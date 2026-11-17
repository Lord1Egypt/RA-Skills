#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wb_health_check.py — WorkBuddy 环境「安全稳定运行」体检脚本（通用版）
=====================================================================
用途：一条命令给 WorkBuddy 环境做全身体检，输出体检报告（md + json）。
     八维体检：磁盘 / 备份新鲜度 / 自动化存活 / 凭据硬编码 / 备份包完整性 /
     配置审计 / 记忆同步 / 跨机同步载体。

铁律（本脚本自身遵守）：
  1. 纯标准库、零网络、只读 + 只写报告文件，不删不改任何东西。
  2. 任何命中的 secret 一律脱敏显示（只露前 4 后 4），绝不输出明文。
  3. 凭据合法存放点（credentials/ connectors/ connector-keys/ 等）不扫。
  4. 报告不含主机名、任务明细等个人信息，只给指标与处置建议。

用法：
  python wb_health_check.py                 # 默认输出 ~/.workbuddy/health-check/
  python wb_health_check.py --out D:/out    # 指定输出目录
  python wb_health_check.py --quick         # 跳过备份包全量哈希校验（快）
  python wb_health_check.py --json          # 额外打印 JSON 结果摘要
  python wb_health_check.py --golden-dir <dir>   # 指定备份包目录（可多次）
  python wb_health_check.py --workspace-root <dir>  # 指定工作区根

退出码：0 = 全部通过；1 = 有 WARN；2 = 有 CRIT（供自动化脚本门禁用）。
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import sqlite3
import sys
import zipfile
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# 常量与配置
# ---------------------------------------------------------------------------
HOME = os.path.expanduser("~")
WB_ROOT = os.path.join(HOME, ".workbuddy")
DB_PATH = os.path.join(WB_ROOT, "workbuddy.db")
DEFAULT_OUT = os.path.join(WB_ROOT, "health-check")
KEEP_REPORTS = 10            # 报告保留份数
MAX_FILE_BYTES = 200 * 1024  # 凭据扫描单文件上限
MAX_SCAN_FILES = 3000        # 凭据扫描文件数上限
ZIP_CHECK_TIMEOUT = 60       # 备份包校验超时（秒），超时降级 WARN

# 备份包候选目录（通用探测；缺失自动跳过；可用 --golden-dir 追加）
GOLDEN_DIRS = [
    os.path.join(WB_ROOT, "skills", "golden-pack-sync", "out"),
    os.path.join(WB_ROOT, "health-check"),
]
# 环境变量可追加（分号分隔，如 WB_GOLDEN_DIRS="D:/bk1;D:/bk2"）
for _p in os.environ.get("WB_GOLDEN_DIRS", "").split(";"):
    if _p.strip():
        GOLDEN_DIRS.append(_p.strip())

# 凭据扫描豁免前缀（合法存放点 / 安装元数据 / 自身）
SKIP_PREFIXES = (
    "_", "__pycache__", "node_modules", "credentials", "connectors",
    "connector-keys", "binaries", "blobs", "logs", ".git",
)
SKIP_DIRNAMES = {"publish", "out", "dist", "build", "venv", "env"}
SELF_SKILL = "workbuddy-health-check"

# 高置信度 secret 正则（值脱敏展示）
SECRET_PATTERNS = [
    (r"sk-[A-Za-z0-9]{20,}", "OpenAI 风格 key"),
    ("AK" + "IA[0-9A-Z]{16}", "AWS Access Key"),
    (r"gh[pousr]_[A-Za-z0-9]{20,}", "GitHub token"),
    (r"xox[baprs]-[A-Za-z0-9-]{10,}", "Slack token"),
    (r"-----BEGIN (RSA |EC |OPENSSH |DSA |ENCRYPTED )?PRIVATE KEY-----", "私钥"),
    (r"(?i)api[_-]?key\s*[:=]\s*[\"'][A-Za-z0-9_\-]{16,}[\"']", "API key 赋值"),
    (r"(?i)secret\s*[:=]\s*[\"'][A-Za-z0-9_\-]{16,}[\"']", "secret 赋值"),
    (r"(?i)password\s*[:=]\s*[\"'][^\"']{8,}[\"']", "password 赋值"),
]
EXAMPLE_HINTS = ("placeholder", "example", "your_", "your-", "xxx", "xxxx",
                 "示例", "占位", "demo", "test_key", "changeme", "<your", "****",
                 "1234567890", "abcdef", "12345678")

# 磁盘阈值（使用率 %）
DISK_WARN, DISK_CRIT = 75.0, 90.0

# 备份新鲜度阈值（天）
BK_WARN, BK_CRIT = 7, 14

# 自动化卡死判定（小时）
STUCK_HOURS = 2.0

RESULT = {"ok": True, "warn": 0, "crit": 0, "dimensions": [], "findings": []}


def mask(value: str) -> str:
    """脱敏：只露前 4 后 4，中间打码。"""
    v = value.strip().strip('"').strip("'")
    if len(v) <= 10:
        return v[:2] + "***"
    return v[:4] + "***" + v[-4:]


def add_finding(dim: str, level: str, msg: str):
    RESULT["findings"].append({"dim": dim, "level": level, "msg": msg})
    if level == "CRIT":
        RESULT["crit"] += 1
        RESULT["ok"] = False
    elif level == "WARN":
        RESULT["warn"] += 1


def add_dim(dim_id: str, name: str, level: str, detail: str, advice: str):
    RESULT["dimensions"].append({
        "id": dim_id, "name": name, "level": level,
        "detail": detail, "advice": advice,
    })


def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ---------------------------------------------------------------------------
# H1 磁盘健康
# ---------------------------------------------------------------------------
def check_disk():
    dim_id, name = "H1", "磁盘健康"
    drives = []
    worst = "PASS"
    for d in ("C:", "D:"):
        try:
            u = shutil.disk_usage(d + "\\")
            pct = u.used / u.total * 100
            lv = "PASS" if pct < DISK_WARN else ("WARN" if pct < DISK_CRIT else "CRIT")
            if lv == "CRIT" or (lv == "WARN" and worst == "PASS"):
                worst = lv
            drives.append(f"{d} 盘 {pct:.0f}% 已用 ({u.free/2**30:.0f}G 可用)")
        except OSError:
            drives.append(f"{d} 盘不可读")
    detail = "；".join(drives)
    advice = ("清理 C 盘（日志/缓存/临时包），目标 <75%" if worst != "PASS"
              else "正常")
    add_dim(dim_id, name, worst, detail, advice)
    if worst != "PASS":
        add_finding(dim_id, worst, detail)


# ---------------------------------------------------------------------------
# H2 备份新鲜度
# ---------------------------------------------------------------------------
def find_latest_golden():
    best = None
    for d in GOLDEN_DIRS:
        if not os.path.isdir(d):
            continue
        try:
            for fn in os.listdir(d):
                if fn.startswith("wb_golden_") and fn.endswith(".zip"):
                    p = os.path.join(d, fn)
                    mt = os.path.getmtime(p)
                    if best is None or mt > best[1]:
                        best = (p, mt)
        except OSError:
            continue
    return best


def check_backup():
    dim_id, name = "H2", "备份新鲜度（备份包）"
    hit = find_latest_golden()
    if hit is None:
        add_dim(dim_id, name, "CRIT", "未找到任何备份包", "立即跑备份打包脚本并上传到异地备份位置")
        add_finding(dim_id, "CRIT", "未找到任何备份包")
        return
    path, mt = hit
    age_days = (datetime.now() - datetime.fromtimestamp(mt)).total_seconds() / 86400
    lv = "PASS" if age_days <= BK_WARN else ("WARN" if age_days <= BK_CRIT else "CRIT")
    if age_days > BK_CRIT:
        lv = "CRIT"
    detail = f"最新 {os.path.basename(path)}，龄 {age_days:.1f} 天（阈 WARN>{BK_WARN}d / CRIT>{BK_CRIT}d）"
    advice = ("正常；按你的同步策略/自动化定期上传备份，留意上传是否成功"
              if lv == "PASS" else "重跑备份打包脚本，并上传到你的异地备份位置")
    add_dim(dim_id, name, lv, detail, advice)
    if lv != "PASS":
        add_finding(dim_id, lv, detail)
    return path


# ---------------------------------------------------------------------------
# H3 自动化存活
# ---------------------------------------------------------------------------
def check_automations():
    dim_id, name = "H3", "自动化存活"
    if not os.path.exists(DB_PATH):
        add_dim(dim_id, name, "WARN", "workbuddy.db 不存在", "无法体检自动化")
        add_finding(dim_id, "WARN", "workbuddy.db 缺失")
        return
    con = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    cur = con.cursor()
    try:
        cur.execute("SELECT id,name,status,schedule_type,next_run_at FROM automations WHERE deleted_at IS NULL")
        rows = cur.fetchall()
        cur.execute("SELECT automation_id,last_error,running,running_started_at FROM automation_runtime_state")
        states = {r[0]: r for r in cur.fetchall()}
    finally:
        con.close()
    total = len(rows)
    active = sum(1 for r in rows if r[2] == "ACTIVE")
    paused = [r for r in rows if r[2] != "ACTIVE"]
    stuck = []
    errored = []
    now_ts = datetime.now().timestamp()
    for r in rows:
        st = states.get(r[0])
        if not st:
            continue
        if st[1]:
            errored.append((r[1], str(st[1])[:80]))
        if st[2] and st[3]:
            start = st[3]
            if isinstance(start, (int, float)) and (now_ts - start) > STUCK_HOURS * 3600:
                stuck.append(r[1])
    problems = []
    if paused:
        problems.append(f"{len(paused)} 个非 ACTIVE（PAUSED/停摆）")
    if stuck:
        problems.append(f"{len(stuck)} 个疑似卡死")
    if errored:
        problems.append(f"{len(errored)} 个有 last_error")
    lv = "PASS" if not problems else ("WARN" if not stuck else "CRIT")
    detail = f"{active}/{total} ACTIVE" + ("；" + "；".join(problems) if problems else "")
    advice = "正常" if lv == "PASS" else "查 automation-backups 与 runtime_state，停摆的按需启用"
    add_dim(dim_id, name, lv, detail, advice)
    if problems:
        add_finding(dim_id, lv, detail)
    # 公开版：只保留计数，不含任务名等明细（保护隐私）
    RESULT["_paused_count"] = len(paused)
    RESULT["_stuck_count"] = len(stuck)
    RESULT["_errored_count"] = len(errored)


# ---------------------------------------------------------------------------
# H4 凭据硬编码扫描（对外文本层）
# ---------------------------------------------------------------------------
def iter_scan_files(root):
    """遍历 skills 下的 SKILL.md 与 references 文本，遵守豁免规则。"""
    count = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames
                       if not d.startswith(SKIP_PREFIXES)
                       and d not in SKIP_DIRNAMES]
        rel = os.path.relpath(dirpath, root)
        parts = rel.split(os.sep)
        if parts and (parts[0].startswith(SKIP_PREFIXES) or parts[0] in SKIP_DIRNAMES):
            continue
        if parts and parts[0] == SELF_SKILL:
            continue
        for fn in filenames:
            if fn.startswith(SKIP_PREFIXES) or fn in ("LICENSE.md", "LICENSE"):
                continue
            low = fn.lower()
            if not (low.endswith(".md") or low.endswith(".py") or low == "skill.md"):
                continue
            if dirpath.endswith(os.sep + "references") or "references" in parts:
                pass  # references 下只收 md/py（上面已过滤）
            elif fn.lower() != "skill.md":
                continue  # 非 references 目录只扫 SKILL.md
            p = os.path.join(dirpath, fn)
            try:
                if os.path.getsize(p) > MAX_FILE_BYTES:
                    continue
                yield p
                count += 1
                if count >= MAX_SCAN_FILES:
                    return
            except OSError:
                continue


def is_example_line(line: str) -> bool:
    low = line.lower()
    return any(h in low for h in EXAMPLE_HINTS)


def scan_credentials():
    dim_id, name = "H4", "凭据硬编码扫描（对外文本层）"
    hits = []
    total = 0
    for p in iter_scan_files(os.path.join(WB_ROOT, "skills")):
        total += 1
        try:
            with open(p, "r", encoding="utf-8", errors="replace") as f:
                lines = f.read().splitlines()
        except OSError:
            continue
        for i, ln in enumerate(lines, 1):
            if is_example_line(ln):
                continue
            for pat, label in SECRET_PATTERNS:
                m = re.search(pat, ln)
                if m:
                    hits.append({"file": os.path.relpath(p, WB_ROOT),
                                 "line": i, "type": label,
                                 "val": mask(m.group(0))})
                    break
    if hits:
        lv = "CRIT"
        detail = f"扫描 {total} 个文件，命中 {len(hits)} 处"
        advice = "逐条人工确认：真凭据→移入系统凭证库/凭据目录并清除明文；测试占位→可忽略"
        add_finding(dim_id, lv, detail)
    else:
        lv = "PASS"
        detail = f"扫描 {total} 个文件，0 命中"
        advice = "正常"
    add_dim(dim_id, name, lv, detail, advice)
    RESULT["_cred_hits"] = hits[:20]


# ---------------------------------------------------------------------------
# H5 备份包完整性
# ---------------------------------------------------------------------------
def check_golden_zip(zip_path, quick: bool):
    dim_id, name = "H5", "备份包完整性"
    if zip_path is None:
        add_dim(dim_id, name, "WARN", "无包可验", "先补 H2 再验")
        return
    leaked = []
    try:
        with zipfile.ZipFile(zip_path) as zf:
            names = zf.namelist()
            for n in names:
                bn = os.path.basename(n.rstrip("/"))
                if (bn.startswith("_") and not bn.startswith("__")) or "_meta" in bn or "lock.json" in bn:
                    leaked.append(("安装元数据", n))
                elif n.startswith(("credentials/", "connector-keys/", "app/connector-keys/", "config/ima")):
                    leaked.append(("凭据目录", n))
            if leaked:
                lv = "CRIT"
                detail = f"包内发现 {len(leaked)} 个泄露项（元数据/凭据目录）"
                advice = "重新打包（剔除安装元数据与凭据目录）并复核"
                add_finding(dim_id, lv, detail)
                RESULT["_zip_leak_count"] = len(leaked)
            else:
                # 校验 manifest 哈希（抽样 20 个，quick 模式跳过）
                manifest_ok = None
                if "_manifest.json" in names:
                    data = json.loads(zf.read("_manifest.json").decode("utf-8"))
                    files_map = data.get("files") or {}
                    entries = list(files_map.items())
                    sample = entries[:20] if quick else entries[:200]
                    bad = 0
                    for arc, sha in sample:
                        try:
                            h = hashlib.sha256(zf.read(arc)).hexdigest()
                            if h != sha:
                                bad += 1
                        except KeyError:
                            bad += 1
                    manifest_ok = bad == 0
                if manifest_ok is False:
                    lv = "CRIT"
                    detail = f"manifest 哈希校验失败（抽样 {len(sample)} 项含 {bad} 项不符）"
                    advice = "包已损坏，重新打包"
                    add_finding(dim_id, lv, detail)
                else:
                    lv = "PASS"
                    detail = (f"{len(names)} 个文件，无泄露项"
                              + (f"，manifest 抽样校验通过" if manifest_ok is True else "，无 manifest（跳过校验）"))
                    advice = "正常"
    except (zipfile.BadZipFile, KeyError, json.JSONDecodeError) as e:
        lv = "WARN"
        detail = f"包读取失败：{type(e).__name__}"
        advice = "重打包"
    add_dim(dim_id, name, lv, detail, advice)


# ---------------------------------------------------------------------------
# H6 配置审计
# ---------------------------------------------------------------------------
def check_config_audit():
    dim_id, name = "H6", "配置审计"
    try:
        n_skills = len([d for d in os.listdir(os.path.join(WB_ROOT, "skills"))
                        if os.path.isdir(os.path.join(WB_ROOT, "skills", d))])
    except OSError:
        n_skills = -1
    try:
        n_conn = len([d for d in os.listdir(os.path.join(WB_ROOT, "connectors"))
                      if os.path.isdir(os.path.join(WB_ROOT, "connectors", d))])
    except OSError:
        n_conn = -1
    try:
        n_exp = len([d for d in os.listdir(os.path.join(WB_ROOT, "plugins", "marketplaces", "my-experts", "plugins"))
                     if os.path.isdir(os.path.join(WB_ROOT, "plugins", "marketplaces", "my-experts", "plugins", d))])
    except OSError:
        n_exp = -1
    mcp_n = 0
    mcp_path = os.path.join(WB_ROOT, "mcp.json")
    if os.path.exists(mcp_path):
        try:
            mcp_n = len(json.load(open(mcp_path, encoding="utf-8")).get("mcpServers", {}))
        except Exception:
            mcp_n = -1
    flags = []
    if n_skills > 150:
        flags.append("技能过多，警惕「规划过剩、激活不足」")
    if n_conn < 3:
        flags.append("连接器偏少（可能不敢连，检查是否该连未连）")
    lv = "PASS" if not flags else "WARN"
    detail = (f"技能 {n_skills} / 连接器 {n_conn} / 自建专家 {n_exp} / MCP {mcp_n} 服务"
              + ("；" + "；".join(flags) if flags else ""))
    advice = "正常" if lv == "PASS" else "按「前提验证+配置审计」三棱镜审计（盘点→对标→诊断→分级），敏感项待用户确认"
    add_dim(dim_id, name, lv, detail, advice)
    if flags:
        add_finding(dim_id, "WARN", detail)


# ---------------------------------------------------------------------------
# H7 记忆同步
# ---------------------------------------------------------------------------
def check_memory(ws_root=None):
    dim_id, name = "H7", "记忆同步"
    notes = []
    mem_md = os.path.join(WB_ROOT, "MEMORY.md")
    if os.path.exists(mem_md):
        age = (datetime.now() - datetime.fromtimestamp(os.path.getmtime(mem_md))).total_seconds() / 86400
        notes.append(f"用户级 MEMORY.md 龄 {age:.1f} 天")
    today = datetime.now().strftime("%Y-%m-%d")
    today_logs = 0
    if ws_root and os.path.isdir(ws_root):
        for d in os.listdir(ws_root):
            m = os.path.join(ws_root, d, ".workbuddy", "memory", today + ".md")
            if os.path.exists(m):
                today_logs += 1
    if today_logs:
        notes.append(f"今日工作区日志 {today_logs} 份")
    else:
        notes.append("今日工作区日志 0 份（可 --workspace-root 指定工作区根）")
    lv = "PASS"
    advice = "正常"
    detail = "；".join(notes)
    if not today_logs:
        lv = "WARN"
        advice = "收工前补今日工作日志，保持记忆连续性"
        add_finding(dim_id, "WARN", "今日无工作区日志")
    add_dim(dim_id, name, lv, detail, advice)


# ---------------------------------------------------------------------------
# H8 跨机同步载体（automation-backups）
# ---------------------------------------------------------------------------
def check_sync_carrier():
    dim_id, name = "H8", "跨机同步载体"
    bk = os.path.join(WB_ROOT, "automation-backups")
    best = None
    if os.path.isdir(bk):
        try:
            for fn in os.listdir(bk):
                if fn.endswith(".json"):
                    mt = os.path.getmtime(os.path.join(bk, fn))
                    if best is None or mt > best[1]:
                        best = (fn, mt)
        except OSError:
            pass
    if best is None:
        add_dim(dim_id, name, "WARN", "automation-backups 为空", "自动化配置 JSON 不随包=异地机拿不到自动化定义")
        add_finding(dim_id, "WARN", "automation-backups 为空")
        return
    age = (datetime.now() - datetime.fromtimestamp(best[1])).total_seconds() / 86400
    lv = "PASS" if age <= BK_WARN else "WARN"
    detail = f"最新 {best[0]}，龄 {age:.1f} 天"
    advice = "正常（随备份包同步到异地机）" if lv == "PASS" else "检查备份包是否含 automation-backups"
    add_dim(dim_id, name, lv, detail, advice)
    if lv != "PASS":
        add_finding(dim_id, lv, detail)


# ---------------------------------------------------------------------------
# 报告生成
# ---------------------------------------------------------------------------
def render_md(zip_path=None):
    lines = []
    lines.append("# WorkBuddy 环境安全稳定体检报告")
    lines.append("")
    lines.append(f"- 时间：{now_str()}（本地）")
    lines.append(f"- 体检维度：8 维（磁盘/备份/自动化/凭据/备份包/配置/记忆/同步载体）")
    lines.append("")
    n_pass = sum(1 for d in RESULT["dimensions"] if d["level"] == "PASS")
    n_warn = RESULT["warn"]
    n_crit = RESULT["crit"]
    if n_crit:
        verdict = f"🔴 危急 {n_crit} 项，先处置 P0"
    elif n_warn:
        verdict = f"🟡 警告 {n_warn} 项，按 P1 处置"
    else:
        verdict = "🟢 全部通过"
    lines.append(f"## 总体结论：{verdict}（{n_pass}/{len(RESULT['dimensions'])} 维通过）")
    lines.append("")
    lines.append("## 八维体检表")
    lines.append("")
    lines.append("| 维度 | 状态 | 指标 | 处置建议 |")
    lines.append("|------|------|------|----------|")
    for d in RESULT["dimensions"]:
        icon = {"PASS": "🟢", "WARN": "🟡", "CRIT": "🔴"}.get(d["level"], "⚪")
        lines.append(f"| {d['id']} {d['name']} | {icon} {d['level']} | {d['detail']} | {d['advice']} |")
    lines.append("")
    p0 = [f for f in RESULT["findings"] if f["level"] == "CRIT"]
    p1 = [f for f in RESULT["findings"] if f["level"] == "WARN"]
    lines.append("## 处置清单（P0 危急 → P1 建议 → P2 长效）")
    lines.append("")
    if p0:
        lines.append("### P0（立即）")
        for f in p0:
            lines.append(f"- [{f['dim']}] {f['msg']}")
        lines.append("")
    if p1:
        lines.append("### P1（建议）")
        for f in p1:
            lines.append(f"- [{f['dim']}] {f['msg']}")
        lines.append("")
    lines.append("### P2（长效）")
    lines.append("- 每周跑一次本体检，报告留档对比趋势")
    lines.append("- 技能/连接器定期做「前提验证+配置审计」三棱镜盘点（现状→对标→诊断→分级）")
    lines.append("- 对外发布物走发布质量门禁（版权/免责/时间戳/指纹/安全测试）")
    lines.append("")
    if RESULT.get("_cred_hits"):
        lines.append("## 凭据扫描命中明细（值已脱敏，需人工确认）")
        lines.append("")
        lines.append("| 文件 | 行 | 类型 | 值(脱敏) |")
        lines.append("|------|----|------|----------|")
        for h in RESULT["_cred_hits"]:
            lines.append(f"| {h['file']} | {h['line']} | {h['type']} | {h['val']} |")
        lines.append("")
    if RESULT.get("_paused_count"):
        lines.append(f"## 非 ACTIVE 自动化：{RESULT['_paused_count']} 个（明细不展示，保护隐私）")
        lines.append("")
    if zip_path:
        lines.append(f"## 校验对象")
        lines.append(f"- 备份包：`{zip_path}`")
        lines.append("")
    lines.append("---")
    lines.append("*本报告由 workbuddy-health-check 体检脚本生成，只读不改；任何敏感命中值均已脱敏。*")
    return "\n".join(lines)


def write_reports(out_dir: str, zip_path):
    os.makedirs(out_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    md = render_md(zip_path)
    md_path = os.path.join(out_dir, f"wb_health_{ts}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)
    out = {k: v for k, v in RESULT.items() if not k.startswith("_")}
    out["generated_at"] = now_str()
    out["_cred_hits_count"] = len(RESULT.get("_cred_hits", []))
    out["_paused_count"] = RESULT.get("_paused_count", 0)
    out["_stuck_count"] = RESULT.get("_stuck_count", 0)
    out["_errored_count"] = RESULT.get("_errored_count", 0)
    out["_zip_leak_count"] = RESULT.get("_zip_leak_count", 0)
    json_path = os.path.join(out_dir, f"wb_health_{ts}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    # 只保留最近 KEEP_REPORTS 份
    for kind in ("wb_health_*.md", "wb_health_*.json"):
        import glob
        files = sorted(glob.glob(os.path.join(out_dir, kind)), reverse=True)
        for old in files[KEEP_REPORTS:]:
            try:
                os.remove(old)
            except OSError:
                pass
    return md_path, json_path


def main():
    ap = argparse.ArgumentParser(description="WorkBuddy 环境安全稳定体检")
    ap.add_argument("--out", default=DEFAULT_OUT, help="报告输出目录")
    ap.add_argument("--quick", action="store_true", help="跳过备份包全量哈希校验")
    ap.add_argument("--json", action="store_true", help="打印 JSON 摘要")
    ap.add_argument("--golden-dir", action="append", default=[], help="备份包目录（可多次指定）")
    ap.add_argument("--workspace-root", default=None, help="工作区根目录（用于检测今日记忆日志）")
    args = ap.parse_args()

    if args.golden_dir:
        for d in args.golden_dir:
            if d not in GOLDEN_DIRS:
                GOLDEN_DIRS.append(d)

    print("🔍 WorkBuddy 环境安全稳定体检开始...")
    check_disk()
    zip_path = check_backup()
    check_automations()
    scan_credentials()
    check_golden_zip(zip_path, args.quick)
    check_config_audit()
    check_memory(args.workspace_root)
    check_sync_carrier()

    md_path, json_path = write_reports(os.path.abspath(args.out), zip_path)
    print(f"📄 报告：{md_path}")
    print(f"📄 JSON：{json_path}")
    print(f"结论：PASS {sum(1 for d in RESULT['dimensions'] if d['level']=='PASS')}/"
          f"{len(RESULT['dimensions'])} 维通过，WARN {RESULT['warn']}，CRIT {RESULT['crit']}")
    if args.json:
        summary = {k: v for k, v in RESULT.items() if not k.startswith("_")}
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    sys.exit(2 if RESULT["crit"] else (1 if RESULT["warn"] else 0))


if __name__ == "__main__":
    main()
