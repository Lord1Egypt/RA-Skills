#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""skill-admission-gate · 技能上架安全闸门（LGD 有籍·有证·有门禁 的实现）

对一个技能目录做确定性安全审查，输出：
  - 分级发现（BLOCK / WARN / INFO）
  - 闸门判定（通过 / 有保留通过 / 拒绝）
  - 证据记录（文件哈希 + 时间戳 + 规则版本）→ 作为“有证”产物

用法:
  python scan_skill.py <技能目录> [--json out.json] [--quiet]
  python scan_skill.py --batch <技能根目录> [--json out.json]
"""
import os, re, sys, json, hashlib, datetime, argparse

RULE_VERSION = "1.0.0"

# ---------------- 规则集 ----------------
# 每条: (id, 级别, 说明, 正则)
RULES = [
    # —— 破坏性操作 ——
    ("DES-01", "BLOCK", "递归强制删除", r"\brm\s+-[a-zA-Z]*[rf][a-zA-Z]*\s+(/|\*|~|\$HOME|\.\.)"),
    ("DES-02", "BLOCK", "Windows 递归删除", r"\bdel\s+/[sf]\b|Remove-Item[^\n]*-Recurse[^\n]*-Force"),
    ("DES-03", "BLOCK", "脚本内递归删目录", r"shutil\.rmtree\s*\("),
    ("DES-04", "BLOCK", "磁盘格式化/写设备", r"\bmkfs(\.|\s)|\bformat\s+[a-zA-Z]:|dd\s+if=.*of=/dev/"),
    ("DES-05", "BLOCK", "Fork 炸弹", r":\(\)\s*\{\s*:\|\s*:&\s*\}\s*;\s*:"),

    # —— 远程执行 / 动态求值 ——
    ("EXE-01", "BLOCK", "下载即执行（管道进 shell）", r"(curl|wget)[^\n|]{0,120}\|\s*(ba)?sh\b"),
    ("EXE-02", "BLOCK", "PowerShell 编码命令执行", r"powershell[^\n]{0,40}-(enc|encodedcommand)\b|\biex\s*\("),
    ("EXE-03", "WARN",  "动态求值（eval/exec）", r"\beval\s*\(|\bexec\s*\("),
    ("EXE-04", "WARN",  "Base64 解码后执行", r"b64decode[^\n]{0,60}(exec|eval|system)|atob\([^\n]{0,60}\)"),

    # —— 数据外泄 ——
    ("EXF-01", "BLOCK", "读取私钥/凭据文件", r"id_rsa|\.ssh/|\.aws/credentials|\.netrc|\.pgpass|\.kdbx"),
    ("EXF-02", "BLOCK", "读取本地保险库/密钥投递工具", r"ucvault|key_drop|_localmem_memories"),
    ("EXF-03", "WARN",  "读取 .env / 环境凭据", r"\.env\b|os\.environ\[[^\]]*(KEY|TOKEN|SECRET|PASS)"),
    ("EXF-04", "WARN",  "向外部端点发送数据", r"requests\.(post|put)\s*\(|curl[^\n]{0,80}-[Xd]|Invoke-RestMethod[^\n]*-Method\s+(POST|PUT)"),

    # —— 提示注入 / 隐蔽行为（主要在 SKILL.md / 指令文本）——
    ("INJ-01", "BLOCK", "要求忽略既有指令", r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions|忽略(以上|之前|先前)(所有)?(的)?指令"),
    ("INJ-02", "BLOCK", "要求对用户隐瞒", r"do\s+not\s+(tell|inform|mention|reveal)[^\n]{0,40}(user|human)|不要(告诉|告知|提及|透露)[^\n]{0,10}用户|不得告知用户"),
    ("INJ-03", "WARN",  "静默/隐藏执行", r"\bsilently\b|without\s+(notifying|telling)\s+the\s+user|静默执行|悄悄(执行|运行)"),
    ("INJ-04", "WARN",  "绕过安全/审批", r"bypass\s+(security|approval|permission|hook)|绕过(安全|审批|权限|检查)|--no-verify"),
    ("INJ-05", "WARN",  "索取/诱导用户粘贴密钥", r"(粘贴|发送|告诉我)[^\n]{0,12}(api\s*key|密钥|token|密码)|paste[^\n]{0,20}(api[_\s]?key|token|password)"),

    # —— 混淆 ——
    ("OBF-01", "WARN",  "长 Base64 字串（疑似混淆载荷）", r"['\"][A-Za-z0-9+/]{180,}={0,2}['\"]"),

    # —— 作用域越界 ——
    ("SCP-01", "WARN",  "写入技能目录之外", r"(open|write_text|Write)\s*\(\s*['\"]([A-Za-z]:[\\/]|/|~)"),
]

# 扫描文件类型
TEXT_EXT = {".py", ".sh", ".bash", ".ps1", ".bat", ".cmd", ".js", ".mjs", ".cjs",
            ".ts", ".rb", ".pl", ".php", ".md", ".txt", ".json", ".yaml", ".yml", ".toml"}
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv", "_backup"}

SEV_ORDER = {"BLOCK": 3, "WARN": 2, "INFO": 1}

# 文档型扩展名：其中的危险模式多为「描述/规则/反面教材」，非实际行为 → 降一级
DOC_EXT = {".md", ".txt", ".rst", ".json", ".yaml", ".yml", ".toml"}


def downgrade(sev):
    return {"BLOCK": "WARN", "WARN": "INFO", "INFO": "INFO"}.get(sev, sev)


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


def scan_file(path, rel):
    findings = []
    is_doc = os.path.splitext(path)[1].lower() in DOC_EXT
    try:
        txt = open(path, encoding="utf-8-sig", errors="replace").read()
    except Exception:
        return findings
    lines = txt.splitlines()
    for rid, sev, desc, pat in RULES:
        try:
            rx = re.compile(pat, re.I)
        except re.error:
            continue
        for i, line in enumerate(lines, 1):
            m = rx.search(line)
            if m:
                eff = downgrade(sev) if is_doc else sev
                findings.append({
                    "rule": rid,
                    "severity": eff,
                    "severity_raw": sev,
                    "downgraded": is_doc and eff != sev,
                    "desc": desc,
                    "file": rel, "line": i,
                    "excerpt": line.strip()[:160],
                })
    return findings


def load_allow(root):
    """读取 <root>/.admission-allow.json —— 已接受风险声明。
    格式：{"allow":[{"rule":"EXF-02","reason":"...","approved_by":"...","date":"YYYY-MM-DD"}]}
    这是“有证”的一部分：接受风险必须留痕、必须署名。"""
    p = os.path.join(root, ".admission-allow.json")
    if not os.path.isfile(p):
        return {}, None
    try:
        d = json.load(open(p, encoding="utf-8-sig"))
    except Exception as e:
        return {}, {"error": str(e)[:200]}
    m = {}
    for it in d.get("allow", []):
        r = it.get("rule")
        if r:
            m.setdefault(r, []).append(it)
    return m, {"file": ".admission-allow.json", "entries": sum(len(v) for v in m.values())}


def scan_skill(root):
    root = os.path.abspath(root)
    name = os.path.basename(root.rstrip("\\/"))
    allow, allow_meta = load_allow(root)
    files, findings, hashes, accepted = 0, [], [], []
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in SKIP_DIRS]
        for fn in sorted(fns):
            p = os.path.join(dp, fn)
            rel = os.path.relpath(p, root).replace("\\", "/")
            ext = os.path.splitext(fn)[1].lower()
            try:
                hashes.append({"path": rel, "sha256": sha256_file(p), "bytes": os.path.getsize(p)})
            except Exception:
                pass
            if ext not in TEXT_EXT:
                continue
            # 声明文件自身不参与扫描（否则自计数）
            if rel == ".admission-allow.json":
                continue
            files += 1
            findings += scan_file(p, rel)

    # 分流：已声明接受的规则 → accepted（仍留痕，但不再计入判定）
    kept = []
    for f in findings:
        if f["rule"] in allow:
            f["accepted_by"] = allow[f["rule"]][0].get("approved_by", "?")
            f["accepted_reason"] = allow[f["rule"]][0].get("reason", "")
            accepted.append(f)
        else:
            kept.append(f)
    findings = kept

    worst = max([SEV_ORDER.get(f["severity"], 0) for f in findings], default=0)
    verdict = "PASS" if worst == 0 else ("BLOCK" if worst >= 3 else "WARN")

    # 包指纹（对文件哈希求和再哈希）
    agg = hashlib.sha256()
    for h in sorted(hashes, key=lambda x: x["path"]):
        agg.update(("%s:%s" % (h["path"], h["sha256"])).encode())
    pkg_fp = agg.hexdigest()

    return {
        "skill": name,
        "path": root.replace("\\", "/"),
        "scanned_files": files,
        "total_files": len(hashes),
        "verdict": verdict,
        "counts": {
            "BLOCK": sum(1 for f in findings if f["severity"] == "BLOCK"),
            "WARN": sum(1 for f in findings if f["severity"] == "WARN"),
            "INFO": sum(1 for f in findings if f["severity"] == "INFO"),
            "DOWNGRADED": sum(1 for f in findings if f.get("downgraded")),
            "ACCEPTED": len(accepted),
        },
        "findings": findings,
        "accepted_risks": accepted,
        "allow_file": allow_meta,
        "evidence": {                      # ← “有证”产物
            "package_fingerprint_sha256": pkg_fp,
            "rule_version": RULE_VERSION,
            "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "file_hashes": hashes,
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target", help="技能目录，或 --batch 时的技能根目录")
    ap.add_argument("--batch", action="store_true", help="对根目录下每个子目录分别审查")
    ap.add_argument("--json", help="结果写入 JSON")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    if a.batch:
        root = a.target
        results = []
        for n in sorted(os.listdir(root)):
            p = os.path.join(root, n)
            if os.path.isdir(p) and os.path.isfile(os.path.join(p, "SKILL.md")):
                r = scan_skill(p)
                results.append(r)
                if not a.quiet:
                    print("%-8s %-40s B=%d W=%d" % (r["verdict"], r["skill"], r["counts"]["BLOCK"], r["counts"]["WARN"]))
        summary = {
            "generated": datetime.date.today().isoformat(),
            "root": root.replace("\\", "/"),
            "counts": {
                "total": len(results),
                "PASS": sum(1 for r in results if r["verdict"] == "PASS"),
                "WARN": sum(1 for r in results if r["verdict"] == "WARN"),
                "BLOCK": sum(1 for r in results if r["verdict"] == "BLOCK"),
            },
            "results": results,
        }
        if a.json:
            json.dump(summary, open(a.json, "w", encoding="utf-8-sig"), ensure_ascii=False, indent=2)
        print("\n合计 %d ｜ PASS %d ｜ WARN %d ｜ BLOCK %d" % (
            summary["counts"]["total"], summary["counts"]["PASS"],
            summary["counts"]["WARN"], summary["counts"]["BLOCK"]))
        return 0

    r = scan_skill(a.target)
    if a.json:
        json.dump(r, open(a.json, "w", encoding="utf-8-sig"), ensure_ascii=False, indent=2)
    if not a.quiet:
        print("技能: %s" % r["skill"])
        print("判定: %s ｜ BLOCK %d ｜ WARN %d ｜ 已接受 %d ｜ 扫描 %d 文件" % (
            r["verdict"], r["counts"]["BLOCK"], r["counts"]["WARN"],
            r["counts"]["ACCEPTED"], r["scanned_files"]))
        print("包指纹: %s" % r["evidence"]["package_fingerprint_sha256"][:16])
        for f in r["findings"][:30]:
            print("  [%s] %s %s:%d  %s" % (f["severity"], f["rule"], f["file"], f["line"], f["excerpt"][:80]))
        for f in r["accepted_risks"][:10]:
            print("  [接受] %s %s:%d  理由：%s（批准：%s）" % (
                f["rule"], f["file"], f["line"], f.get("accepted_reason", "")[:50], f.get("accepted_by", "")))
    return 0 if r["verdict"] != "BLOCK" else 1


if __name__ == "__main__":
    raise SystemExit(main())
