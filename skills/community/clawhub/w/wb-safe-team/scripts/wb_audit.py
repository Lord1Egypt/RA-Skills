#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wb_audit.py —— WorkBuddy 安全稳定运行专家团（WB-SAFE）离线巡检脚本
=====================================================================
零积分、纯本地、只读诊断。固化「首次实战四动作」为可复用一键巡检：
  A. 七维健康子集（磁盘/内存/进程）      —— 健康哨兵线
  B. 明文凭据扫描（只报位置/行号/类型，不回显值） —— 凭据官线
  C. 专家团包结构校验（plugin.json/agents/avatar 引用） —— 配置审计官线
  D. 配置快照 SHA256 基线 + 漂移检测     —— 配置审计官线

设计约束（来自实战踩坑沉淀）：
  * Windows 原生 Python 不认 `/c/` 路径，一律用 `C:/` 风格。
  * 不调用任何云端 API，不消耗积分。
  * 凭据值绝不出现在 stdout / 报告文件。
  * baseline 用机器可读 JSON 维护，首次运行建基线，后续比对待漂移。

用法：
  python3 wb_audit.py                 # 巡检 + 生成报告 + 更新 baseline
  python3 wb_audit.py --init-baseline # 仅重建基线（不报漂移）
"""
import os, sys, io, json, glob, hashlib, subprocess, datetime, re, argparse

# ---------- 路径（自动探测，Windows 风格规避 /c/ 坑；可用 WB_WS 环境变量覆盖） ----------
HOME       = os.path.expanduser("~").replace("\\", "/")
WB         = os.environ.get("WB_WS", "") or \
             sorted(glob.glob(os.path.join(HOME, "WorkBuddy", "20*")), reverse=True)[0]
TEAM_ROOT  = os.path.join(HOME, ".workbuddy/plugins/marketplaces/my-experts/plugins").replace("\\", "/")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASELINE   = os.path.join(SCRIPT_DIR, "audit_baseline.json")
REPORT     = os.path.join(WB, "定期巡检报告_WB-SAFE_%s.md" % datetime.date.today().isoformat())

TEAMS = ["wb-safe-team"]

# 敏感文件名（凭据官七类位置精简为文件名命中，避免依赖包噪声）
SENSITIVE_NAMES = [".env", ".env.local", "credentials", "credential",
                   "secrets", "token", "tokens", "*.key", "id_rsa", "id_ed25519"]
# 噪声目录（依赖包/缓存），凭据官扫描时剪枝
EXCLUDE_DIRS = {"node_modules", ".git", "site-packages", "__pycache__",
                ".venv", "venv", "dist", "build"}
def _prune(dirs):
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
# 内容模式（仅对工作目录小范围扫，不扫依赖包）
SECRET_RE = re.compile(
    r"(sk-[A-Za-z0-9]{12,}|api[_-]?key\s*[:=]\s*['\"]?[A-Za-z0-9]{12,}|"
    r"secret\s*[:=]\s*['\"]?[A-Za-z0-9]{8,}|password\s*[:=]\s*['\"]?[^\s]{6,}|"
    r"ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16})",
    re.IGNORECASE)

def h16(p):
    return hashlib.sha256(io.open(p, "rb").read()).hexdigest()[:16]

def ps(cmd):
    try:
        r = subprocess.run(["powershell", "-NoProfile", "-Command", cmd],
                           capture_output=True, text=True, timeout=30)
        return r.stdout.strip()
    except Exception as e:
        return "ERR:%s" % e

# ---------- A. 健康 ----------
def health():
    out = {}
    d = ps("(Get-PSDrive C).Used+(Get-PSDrive C).Free; "
           "(Get-PSDrive C).Used; (Get-PSDrive C).Free")
    lines = [x for x in d.split("\n") if x.strip() and not x.startswith("ERR")]
    try:
        tot = float(lines[0]); used = float(lines[1]); free = float(lines[2])
        out["disk_c_used_pct"] = round(used / tot * 100, 1)
        out["disk_c_free_gb"]  = round(free / 1e9, 1)
    except Exception:
        out["disk_c_used_pct"] = "NA"
    m = ps("$o=Get-CimInstance Win32_OperatingSystem; "
           "$o.TotalVisibleMemorySize; $o.FreePhysicalMemory")
    ml = [x for x in m.split("\n") if x.strip() and not x.startswith("ERR")]
    try:
        out["mem_free_gb"] = round(float(ml[1]) / 1e6, 1)
    except Exception:
        out["mem_free_gb"] = "NA"
    p = ps("(Get-Process).Count")
    try:
        out["proc_count"] = int(p.split("\n")[0])
    except Exception:
        out["proc_count"] = "NA"
    # 评级
    out["disk_level"] = "P2关注" if isinstance(out["disk_c_used_pct"], (int,float)) and out["disk_c_used_pct"] >= 75 else "正常"
    out["mem_level"]  = "P2关注" if isinstance(out["mem_free_gb"], (int,float)) and out["mem_free_gb"] < 4 else "正常"
    return out

# ---------- B. 凭据扫描 ----------
def _classify(fp):
    p = fp.replace("\\", "/")
    if "wb-restore-backup" in p:            return "BACKUP"   # 旧备份副本
    if "/binaries/python/" in p:           return "NOISE"    # Python 标准库
    if ".example" in p or ".template" in p: return "NOISE"    # 模板
    if p.endswith("/secrets.py") or p.endswith("/token.py"): return "NOISE"
    if "/references/secrets.md" in p:      return "NOISE"     # 文档
    if "/credentials/" in p or "/connector-keys/" in p or p.endswith(".master.key"): return "SYSTEM"
    if "/workspace/sessions/" in p:        return "SYSTEM"    # 平台会话备份
    if "/skills/" in p:                    return "OURS"      # 我们自管配置
    return "OTHER"

def cred_scan():
    hits = []
    # B1 敏感文件名（.workbuddy 范围），剪枝依赖包噪声 + 分级
    for pat in SENSITIVE_NAMES:
        for root, dirs, files in os.walk(os.path.join(HOME, ".workbuddy")):
            _prune(dirs)
            if "plugins/cache" in root.replace("\\", "/"):  # 第三方包缓存跳过
                continue
            for f in files:
                fp = os.path.join(root, f)
                tag = None
                if pat == "*.key":
                    if f.endswith(".key"): tag = _classify(fp)
                elif f == pat or f.startswith(pat + "."):
                    tag = _classify(fp)
                if tag is None: continue
                info = "sensitive-name:%s" % pat
                if f.endswith(".env"):
                    # 精确：是否含敏感 key（API_KEY/SECRET/PASSWORD/TOKEN）的真实赋值
                    # 逐行判定，避免 \s 跨行误匹配；读值但绝不输出；URL 配置不算敏感赋值
                    try:
                        txt = io.open(fp, encoding="utf-8", errors="ignore").read()
                        has_secret = False
                        for line in txt.splitlines():
                            m = re.search(r"(API[_-]?KEY|SECRET|PASSWORD|TOKEN|PASSWD)\s*[:=]\s*(\S+)", line, re.I)
                            if m and not m.group(2).startswith("http"):
                                has_secret = True; break
                        info += ":含敏感赋值" if has_secret else ":空值占位"
                    except Exception:
                        info += ":读取失败"
                hits.append((tag, fp, info))
    # B2 内容模式（仅工作目录，避免依赖包噪声）
    for root, _, files in os.walk(WB):
        for f in files:
            if f.endswith((".md", ".txt", ".json", ".py", ".env")):
                fp = os.path.join(root, f)
                try:
                    for i, line in enumerate(io.open(fp, encoding="utf-8", errors="ignore"), 1):
                        if SECRET_RE.search(line):
                            hits.append(("CONTENT", fp, "L%d" % i))  # 不回显文本
                except Exception:
                    pass
    return hits

# ---------- C. 团包校验 ----------
def team_check():
    res = []
    for t in TEAMS:
        base = os.path.join(TEAM_ROOT, t)
        pj = os.path.join(base, ".codebuddy-plugin", "plugin.json")
        row = {"team": t, "ok": False, "agents": 0, "avatar_missing": []}
        try:
            d = json.load(io.open(pj, encoding="utf-8"))
            row["name"] = d.get("name")
            ag = glob.glob(os.path.join(base, "agents", "*.md"))
            row["agents"] = len(ag)
            # avatar 引用完整性（相对 plugin.json 所在团队目录解析）
            miss = []
            def _av(p):
                return p if os.path.isabs(p) else os.path.join(base, p)
            if d.get("avatar") and not os.path.isfile(_av(d["avatar"])): miss.append(d["avatar"])
            for mb in d.get("members", []):
                if mb.get("avatar") and not os.path.isfile(_av(mb["avatar"])): miss.append(mb["avatar"])
            row["avatar_missing"] = miss
            row["ok"] = True
        except Exception as e:
            row["err"] = str(e)
        res.append(row)
    return res

# ---------- D. 快照基线 + 漂移 ----------
def snapshot_and_drift():
    files = []
    for t in TEAMS:
        base = os.path.join(TEAM_ROOT, t)
        files.append(os.path.join(base, ".codebuddy-plugin", "plugin.json"))
        files += sorted(glob.glob(os.path.join(base, "agents", "*.md")))
        files += sorted(glob.glob(os.path.join(base, "avatars", "*.png")))
    # 工作区交付物
    for rel in ["专家团_WorkBuddy安全稳定运行_安全配置.md",
                "配置快照_WB-SAFE_v0.3.md",
                "体检报告_WB-SAFE_v0.1.md",
                "凭据台账_WB-SAFE_v0.1.md",
                "恢复演练报告_WB-SAFE_v0.1.md"]:
        fp = os.path.join(WB, rel)
        if os.path.isfile(fp): files.append(fp)
    cur = {os.path.relpath(f, TEAM_ROOT).replace("\\", "/"): h16(f) for f in files if os.path.isfile(f)}
    drift = []
    if os.path.isfile(BASELINE):
        prev = json.load(io.open(BASELINE, encoding="utf-8"))
        for k, v in cur.items():
            if k not in prev: drift.append((k, "NEW"))
            elif prev[k] != v: drift.append((k, "CHANGED"))
        for k in prev:
            if k not in cur: drift.append((k, "DELETED"))
    return cur, drift

# ---------- 报告 ----------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--init-baseline", action="store_true")
    args = ap.parse_args()

    h  = health()
    cr = cred_scan()
    tc = team_check()
    cur, drift = snapshot_and_drift()

    if args.init_baseline:
        io.open(BASELINE, "w", encoding="utf-8").write(json.dumps(cur, ensure_ascii=False, indent=2))
        print("baseline initialized: %d files" % len(cur)); return

    # 写 baseline
    io.open(BASELINE, "w", encoding="utf-8").write(json.dumps(cur, ensure_ascii=False, indent=2))

    L = []
    L.append("# 定期巡检报告 · WB-SAFE（%s）\n" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    L.append("- 模式：离线只读 · 零积分 · 凭据值不回显\n")
    L.append("## A. 七维健康子集")
    L.append("| 指标 | 读数 | 评级 |")
    L.append("|---|---|---|")
    L.append("| 磁盘 C 占用 | %s%% (剩余 %.1fGB) | %s |" % (h["disk_c_used_pct"], h["disk_c_free_gb"], h["disk_level"]))
    L.append("| 内存空闲 | %.1f GB | %s |" % (h["mem_free_gb"], h["mem_level"]))
    L.append("| 进程数 | %s | 正常偏多(参考) |" % h["proc_count"])
    L.append("\n## B. 明文凭据扫描（仅报告位置/类型，不回显值）")
    ours   = [x for x in cr if x[0]=="OURS"]
    system = [x for x in cr if x[0]=="SYSTEM"]
    backup = [x for x in cr if x[0]=="BACKUP"]
    noise  = [x for x in cr if x[0]=="NOISE"]
    L.append("- **我们自管配置（OURS）**：**%d** 处 ⬅ 重点" % len(ours))
    for _, fp, info in ours:
        L.append("  - `%s` → %s" % (fp.replace(HOME, "~").replace("\\","/"), info))
    L.append("- 平台托管凭据/密钥（SYSTEM，非手写泄露）：%d 处" % len(system))
    L.append("- 旧备份副本（BACKUP，建议清理释放磁盘）：%d 处" % len(backup))
    L.append("- 第三方/源码噪声（NOISE，已忽略）：%d 处" % len(noise))
    L.append("- 内容模式命中（仅工作目录）：**%d** 处" % sum(1 for x in cr if x[0]=="CONTENT"))
    for typ, fp, info in cr:
        if typ == "CONTENT":
            L.append("  - `%s` → %s" % (fp.replace(WB, ".").replace("\\","/"), info))
    if not any(x[0]=="CONTENT" for x in cr):
        L.append("  - 工作目录无明文凭据模式命中 ✅")
    L.append("\n## C. 专家团包校验")
    for r in tc:
        if r["ok"]:
            miss = "无" if not r["avatar_missing"] else str(r["avatar_missing"])
            L.append("- `%s`：解析OK · agents=%d · avatar缺失=%s" % (r["team"], r["agents"], miss))
        else:
            L.append("- `%s`：**FAIL** %s" % (r["team"], r.get("err","")))
    L.append("\n## D. 配置快照基线 + 漂移")
    L.append("- 基线文件数：**%d**" % len(cur))
    if drift:
        L.append("- 漂移：**%d** 处 ⚠️" % len(drift))
        for k, v in drift:
            L.append("  - `%s` → %s" % (k, v))
    else:
        L.append("- 漂移：**无** ✅（与上一基线一致）")
    L.append("\n## 结论")
    p2 = [x for x in [h["disk_level"], h["mem_level"]] if x != "正常"]
    if p2:
        L.append("- 关注项：%s" % "、".join(p2))
    else:
        L.append("- 各维度正常，无新增风险。")
    L.append("- 凭据（OURS 自管）：%s；敏感文件已定位，值未回显。" %
              ("发现 %d 处，需跟进" % len(ours) if ours else "无自管明文泄露 ✅"))
    io.open(REPORT, "w", encoding="utf-8").write("\n".join(L))
    print("报告已生成:", os.path.basename(REPORT))
    print("健康:", h)
    print("凭据 OURS:", len([x for x in cr if x[0]=="OURS"]),
          "| SYSTEM:", len([x for x in cr if x[0]=="SYSTEM"]),
          "| BACKUP:", len([x for x in cr if x[0]=="BACKUP"]),
          "| NOISE:", len([x for x in cr if x[0]=="NOISE"]),
          "| 内容命中:", sum(1 for x in cr if x[0]=="CONTENT"))
    print("团包:", [(r["team"], r["agents"], len(r["avatar_missing"])) for r in tc])
    print("漂移:", len(drift))

if __name__ == "__main__":
    main()
