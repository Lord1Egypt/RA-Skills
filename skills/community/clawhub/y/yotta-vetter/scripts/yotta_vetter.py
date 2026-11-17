#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""yotta_vetter.py — YottaMeta 元审（yotta-vetter）技能审查 checker。

安装任何技能前的「安全审查协议」：
  check   四阶段初审（来源/代码/权限/风险）+ 危险模式规则扫描
  source  来源半自动化检查（GitHub 仓库元数据，本地缓存，无网络自动降级）

- 危险模式规则与 yotta-security-audit（元安）共用（scripts/vetter_rules.py
  为 audit_rules.py 的同步副本，勿手改）。
- 初审发现可疑（high 及以上）会输出一条命令引导跑元安深度扫描（联动 V3）。
- 纯 Python 3.8+ 标准库，Windows + Linux 通用。

exit code 语义（与元安一致）：
  0 = 干净 / 仅有 low 提示
  1 = 存在 medium
  2 = 存在 high
  3 = 存在 critical
  4 = 用法错误/致命异常

用法示例：
  python3 yotta_vetter.py check ./some-skill
  python3 yotta_vetter.py check ./some-skill --json --report report.md
  python3 yotta_vetter.py source github:YottaMeta/yotta-memory
"""
import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
try:
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
import vetter_rules  # noqa: E402

VERSION = "0.2.9"
TOOL_NAME = "yotta-vetter"
MAX_FILE_SIZE = 1_000_000
MAX_LINE_LEN = vetter_rules.MAX_LINE_LEN
SKIP_DIRS = {"venv", "node_modules", ".git", "__pycache__", ".mypy_cache",
             ".tox", "dist", "build", ".egg-info", ".venv", ".idea", ".vscode"}
TEXT_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".mjs", ".cjs", ".sh", ".bash", ".zsh",
    ".md", ".txt", ".yaml", ".yml", ".json", ".toml", ".ini", ".cfg",
    ".rb", ".go", ".rs", ".java", ".c", ".cpp", ".h", ".hpp",
    ".html", ".css", ".xml", ".svg", ".plist", ".ps1", ".bat", ".cmd",
    ".env", ".conf", ".properties", ".gradle",
}
DOTFILE_NAMES = {".env", ".env.example", ".netrc", ".pgpass", ".bashrc",
                 ".zshrc", ".profile", ".bash_profile", ".npmrc", ".gitconfig"}
SCRIPT_EXTENSIONS = {".py", ".js", ".ts", ".mjs", ".cjs", ".sh", ".bash", ".zsh",
                     ".ps1", ".bat", ".cmd", ".rb", ".pl"}

_SEVERITY_RANK = {"info": 0, "low": 0, "medium": 1, "high": 2, "critical": 3}
_SEVERITY_ORDER = ("critical", "high", "medium", "low", "info")

# ── 基础工具 ────────────────────────────────────────────────────────────────

class Finding:
    __slots__ = ("detector", "severity", "category", "file_path", "line",
                 "description", "confidence", "rule_id")

    def __init__(self, detector, severity, category, file_path, line=0,
                 description="", confidence=50, rule_id=""):
        self.detector = detector
        self.severity = severity
        self.category = category
        self.file_path = file_path
        self.line = line
        self.description = description
        self.confidence = confidence
        self.rule_id = rule_id

    def to_dict(self):
        return {"detector": self.detector, "severity": self.severity,
                "category": self.category, "file": self.file_path,
                "line": self.line, "description": self.description,
                "confidence": self.confidence, "rule_id": self.rule_id}


def _sev_value(sev):
    return _SEVERITY_RANK.get(sev, 0)


def _worst(findings):
    worst = "info"
    for f in findings:
        if _sev_value(f.severity) > _sev_value(worst):
            worst = f.severity
    return worst


def _read_text(p):
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _is_binary(head):
    return b"\x00" in head[:8192]


# v0.2.6：签名数据文件（家族规则表）白名单 —— 相对路径 + CRLF 归一化 SHA-256 双绑定。
# 任一条不满足即正常扫描（fail-closed），杜绝「改名即豁免」。
PUBLISHED_SIGNATURES = {
    "scripts/verify_rules.py":
        "f060ec1e9d339865db577c074b51b49841a44657f3bea863dbc72ced2d5eed83",
    "scripts/vetter_rules.py":
        "ed0959784c3afc09562686aaac8a0d17679987dbd49a06bedccee2d05f17424c",
    "scripts/audit_rules.py":
        "231e87341816a48fa47573cd4e7a9ecdeb1535c04cab04a4d569443c9db54a8d",
    "scripts/hardening_rules.py":
        "a5d6a14323633ba59f0005e655ec3b0acf5be300db8889fd3fb875cc8c2d9fba",
    "scripts/guardian_rules.py":
        "d83674b9dc41c8f6290964b9d6339dce3840f9c0df564856513bc7f1a9bd94d8",
}


def _sha256_normalized(path):
    """CRLF 归一化后的 SHA-256（跨 Windows / Linux 检出结果一致）。"""
    try:
        data = path.read_bytes().replace(b"\r\n", b"\n")
    except OSError:
        return ""
    return hashlib.sha256(data).hexdigest()


def is_published_signature_data(root, path):
    """判断文件是否为「已发布家族规则表」：路径受限 + 摘要一致（摘要为最终判据）。

    路径接受 `scripts/<规则表名>`，以及「扫描根就是 scripts 目录」时的 `<规则表名>`
    形式（自扫 scripts/ 子目录的场景）。两条路径都必须命中已发布摘要，改名 / 改内容
    一律照常扫描。
    """
    try:
        rel = path.relative_to(root).as_posix()
    except ValueError:
        rel = path.name
    expected = PUBLISHED_SIGNATURES.get(rel)
    if not expected and Path(root).name.lower() == "scripts":
        # 直接扫描 scripts/ 子目录（自扫场景）：按 scripts/<规则表名> 复核
        expected = PUBLISHED_SIGNATURES.get("scripts/" + path.name)
    if not expected:
        return False
    return _sha256_normalized(path) == expected


def collect_files(root):
    files = []
    for dirpath, dirnames, filenames in os.walk(str(root)):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fname in sorted(filenames):
            p = Path(dirpath) / fname
            try:
                if p.suffix.lower() not in TEXT_EXTENSIONS and p.name.lower() not in DOTFILE_NAMES:
                    continue
                # v0.2.6：签名数据文件豁免改为「路径 + 摘要绑定」。旧行为只按文件名跳过，
                # 攻击方把恶意文件命名成 audit_rules.py / verify_rules.py 即可免扫（T09）。
                if is_published_signature_data(Path(root), p):
                    continue
                if p.stat().st_size > MAX_FILE_SIZE:
                    continue
            except OSError:
                continue
            try:
                with open(p, "rb") as fh:
                    if _is_binary(fh.read(8192)):
                        continue
            except OSError:
                continue
            files.append(p)
    return files


# ── 四阶段初审 ─────────────────────────────────────────────────────────────

def inventory_checks(root, files):
    """V2 阶段：结构/权限/风险清单。返回 [Finding]。"""
    findings = []
    root = Path(root)
    skill_md = root / "SKILL.md"
    if not skill_md.is_file():
        findings.append(Finding("Inventory", "medium", "structure", str(skill_md),
                                description="缺少 SKILL.md（技能入口文件）", confidence=70,
                                rule_id="INV-001"))
    else:
        text = _read_text(skill_md)
        m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
        if not m:
            findings.append(Finding("Inventory", "medium", "structure", str(skill_md),
                                    description="SKILL.md 缺少 YAML frontmatter",
                                    confidence=70, rule_id="INV-002"))
        else:
            fm = m.group(1)
            if not re.search(r"^name:", fm, re.M):
                findings.append(Finding("Inventory", "medium", "structure", str(skill_md),
                                        description="frontmatter 缺少 name", confidence=60,
                                        rule_id="INV-003"))
            nm = re.search(r"^name:\s*(.+)$", fm, re.M)
            if nm and nm.group(1).strip() != root.name:
                findings.append(Finding(
                    "Inventory", "medium", "structure", str(skill_md),
                    description="frontmatter name（%s）与目录名（%s）不一致"
                                % (nm.group(1).strip(), root.name),
                    confidence=70, rule_id="INV-004"))
    if not (root / "README.md").is_file():
        findings.append(Finding("Inventory", "info", "structure", str(root),
                                description="缺少 README.md（可读性提示）",
                                confidence=30, rule_id="INV-005"))
    scripts = [p for p in files if p.suffix.lower() in SCRIPT_EXTENSIONS]
    if scripts:
        findings.append(Finding(
            "Inventory", "info", "permissions", str(root),
            description="含可执行脚本 %d 个" % len(scripts), confidence=30,
            rule_id="INV-006"))
    # 权限：Unix 下可执行/全局可写文件
    if os.name != "nt":
        for p in files:
            try:
                mode = p.stat().st_mode
            except OSError:
                continue
            if mode & 0o002:
                findings.append(Finding(
                    "Inventory", "medium", "permissions", str(p),
                    description="全局可写文件", confidence=70, rule_id="PERM-001"))
            if mode & 0o111 and p.suffix.lower() not in SCRIPT_EXTENSIONS:
                findings.append(Finding(
                    "Inventory", "low", "permissions", str(p),
                    description="非脚本文件带可执行位", confidence=40,
                    rule_id="PERM-002"))
    # 符号链接（可能指向目录外）
    for p in files:
        if p.is_symlink():
            findings.append(Finding("Inventory", "medium", "permissions", str(p),
                                    description="符号链接（指向 %s）" % os.readlink(str(p)),
                                    confidence=60, rule_id="SYMLINK-001"))
    return findings


def pattern_scan(files):
    """V1：用共享规则表扫危险模式。返回 [Finding]。"""
    findings = []
    compiled = vetter_rules.compile_rules()
    for p in files:
        content = _read_text(p)
        if not content:
            continue
        for lineno, raw_line in enumerate(content.splitlines(), 1):
            if len(raw_line) > MAX_LINE_LEN:
                raw_line = raw_line[:MAX_LINE_LEN]
            for rule in vetter_rules.PATTERN_RULES:
                cre = compiled[rule.id]
                if cre.search(raw_line):
                    findings.append(Finding(
                        detector=rule.detector, severity=rule.severity,
                        category=rule.detector.lower(), file_path=str(p),
                        line=lineno, description=rule.description,
                        confidence=rule.confidence, rule_id=rule.id))
        base = p.name.lower()
        for pat, desc, sev, conf in vetter_rules.SENSITIVE_FILENAMES:
            if pat.lower() in base:
                findings.append(Finding(
                    detector="CredentialTheft", severity=sev,
                    category="credential_theft", file_path=str(p),
                    description="敏感凭据文件命名: %s" % desc,
                    confidence=conf, rule_id="FIL-SENS"))
        for rule in vetter_rules.get_rules("SocialEngineering"):
            if compiled[rule.id].search(base):
                findings.append(Finding(
                    detector="SocialEngineering", severity=rule.severity,
                    category="social_engineering", file_path=str(p),
                    description=rule.description + "（文件名）",
                    confidence=rule.confidence, rule_id=rule.id))
    return findings


def dedup(findings):
    seen = set()
    out = []
    for f in findings:
        key = (f.file_path, f.line, f.rule_id or f.detector)
        if key in seen:
            continue
        seen.add(key)
        out.append(f)
    return out


def verdict_for(worst):
    if _sev_value(worst) >= 3:
        return "DO NOT INSTALL", "发现 critical 级风险，拒绝安装并人工复核"
    if _sev_value(worst) >= 2:
        return "INSTALL WITH CAUTION", "发现 high 级风险，需人工复核后决定"
    if _sev_value(worst) >= 1:
        return "REVIEW REQUIRED", "发现 medium 级风险，建议复核后安装"
    return "SAFE TO INSTALL", "未发现明显风险（仍建议按协议完整审查）"

# ── 威胁捕获模型视图（2026-08-30 增强：8 检测点 + 13 行为项）────────
_SEV_WEIGHT = {"critical": 40, "high": 20, "medium": 8, "low": 1, "info": 0}
_SEV_CAPS = {"critical": 2, "high": 4, "medium": 6, "low": 10, "info": 0}


def _health_score(findings):
    counts = {}
    for f in findings:
        counts[f.severity] = counts.get(f.severity, 0) + 1
    score = 100
    for sev, w in _SEV_WEIGHT.items():
        score -= w * min(counts.get(sev, 0), _SEV_CAPS[sev])
    return max(0, int(round(score)))


def _taxonomy_view(findings):
    hits = {}
    for f in findings:
        key = vetter_rules.DETECTOR_TO_TAXONOMY.get(f.detector, "other")
        hits.setdefault(key, []).append(f)
    out = []
    for key in vetter_rules.TAXONOMY_ORDER:
        items = hits.get(key, [])
        name = vetter_rules.THREAT_TAXONOMY.get(key, key)
        sev = "info"
        for f in items:
            if _SEV_WEIGHT.get(f.severity, 0) > _SEV_WEIGHT.get(sev, 0):
                sev = f.severity
        if not items:
            verdict = "n/a"
        elif sev in ("critical", "high"):
            verdict = "danger"
        elif sev == "medium":
            verdict = "suspicious"
        else:
            verdict = "safe"
        out.append({"name": name, "verdict": verdict, "count": len(items)})
    return out


def _behavior_view(findings):
    observed = {}
    for f in findings:
        for b in vetter_rules.DETECTOR_TO_BEHAVIORS.get(f.detector, ()):
            observed[b] = observed.get(b, 0) + 1
    return [{"behavior": b, "observed": observed.get(b, 0)}
            for b in vetter_rules.BEHAVIORS]


# ── 输出（文本 / JSON / 报告）──────────────────────────────────────────────

def fmt_report(findings, scope):
    lines = []
    lines.append("=" * 66)
    lines.append("SKILL VETTING REPORT  ·  %s %s" % (TOOL_NAME, VERSION))
    lines.append("=" * 66)
    lines.append("技能: %s" % scope.get("skill", "-"))
    lines.append("路径: %s" % scope.get("path", "-"))
    lines.append("来源: %s" % scope.get("source", "-"))
    lines.append("审查时间: %s" % scope.get("reviewed_at", ""))
    lines.append("审查者: %s" % scope.get("reviewer", "yotta-vetter"))
    lines.append("文件数: %d" % scope.get("files", 0))
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for f in findings:
        counts[f.severity] = counts.get(f.severity, 0) + 1
    lines.append("")
    lines.append("汇总: CRITICAL %d | HIGH %d | MEDIUM %d | LOW %d | INFO %d" % (
        counts["critical"], counts["high"], counts["medium"],
        counts["low"], counts["info"]))
    verdict, note = verdict_for(_worst(findings))
    lines.append("风险等级: %s" % _worst(findings).upper())
    lines.append("结论: %s" % verdict)
    lines.append("决策记录: %s" % note)
    lines.append("安全健康度评分: %d/100" % _health_score(findings))
    lines.append("")
    lines.append("威胁捕获模型（8 类）：")
    for v in _taxonomy_view(findings):
        lines.append("  %-16s %-11s %d" % (v["name"], v["verdict"], v["count"]))
    lines.append("")
    observed = [b["behavior"] for b in _behavior_view(findings) if b["observed"]]
    lines.append("行为项（13 项）：%s" % (
        "、".join(observed) if observed else "未观察到明显系统行为"))
    lines.append("")
    if findings:
        lines.append("发现:")
        order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
        for f in sorted(findings, key=lambda x: (order.get(x.severity, 9), x.file_path, x.line)):
            loc = f.file_path
            if f.line:
                loc = "%s:%d" % (loc, f.line)
            lines.append("  [%s] %s  %s" % (f.severity.upper(), f.rule_id or f.detector, loc))
            lines.append("      %s" % f.description)
    else:
        lines.append("未发现可疑模式。")
    lines.append("=" * 66)
    return "\n".join(lines)


def write_report_md(path, findings, scope):
    lines = []
    lines.append("# SKILL VETTING REPORT")
    lines.append("")
    lines.append("- 技能: %s" % scope.get("skill", "-"))
    lines.append("- 路径: %s" % scope.get("path", "-"))
    lines.append("- 来源: %s" % scope.get("source", "-"))
    lines.append("- 审查时间: %s" % scope.get("reviewed_at", ""))
    lines.append("- 审查者: %s" % scope.get("reviewer", "yotta-vetter"))
    lines.append("- 文件数: %d" % scope.get("files", 0))
    lines.append("")
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for f in findings:
        counts[f.severity] = counts.get(f.severity, 0) + 1
    verdict, note = verdict_for(_worst(findings))
    lines.append("## 结论")
    lines.append("")
    lines.append("- 风险等级: %s" % _worst(findings).upper())
    lines.append("- 结论: %s" % verdict)
    lines.append("- 决策记录: %s" % note)
    lines.append("")
    lines.append("## 汇总")
    lines.append("")
    lines.append("| 级别 | 数量 |")
    lines.append("|---|---|")
    for sev in _SEVERITY_ORDER:
        lines.append("| %s | %d |" % (sev.upper(), counts[sev]))
    lines.append("")
    lines.append("**安全健康度评分：%d/100**" % _health_score(findings))
    lines.append("")
    lines.append("## 威胁捕获模型视图（8 类）")
    lines.append("")
    lines.append("| 检测点 | verdict | 命中 |")
    lines.append("|---|---|---|")
    for v in _taxonomy_view(findings):
        lines.append("| %s | %s | %d |" % (v["name"], v["verdict"], v["count"]))
    lines.append("")
    lines.append("## 行为项（13 项）")
    lines.append("")
    observed = [b["behavior"] for b in _behavior_view(findings) if b["observed"]]
    lines.append("观察到：%s" % ("、".join(observed) if observed else "未观察到明显系统行为"))
    lines.append("")
    if findings:
        lines.append("## 发现")
        lines.append("")
        order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
        for f in sorted(findings, key=lambda x: (order.get(x.severity, 9), x.file_path, x.line)):
            lines.append("### %s · %s" % (f.severity.upper(), f.rule_id or f.detector))
            lines.append("")
            lines.append("- 位置: %s%s" % (f.file_path, ":%d" % f.line if f.line else ""))
            lines.append("- 描述: %s" % f.description)
            lines.append("")
    else:
        lines.append("未发现可疑模式。")
    lines.append("## 决策记录")
    lines.append("")
    lines.append("- [ ] 已人工复核发现项")
    lines.append("- [ ] 已确认来源可信度")
    lines.append("- [ ] 已确认权限范围最小化")
    lines.append("- [ ] 审查结论与理由已记录（时间戳/审查者）")
    try:
        with open(str(path), "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(lines))
        return True
    except OSError as e:
        print("[ERROR] 报告写入失败: %s" % e, file=sys.stderr)
        return False


# ── check 命令 ─────────────────────────────────────────────────────────────

def cmd_check(args):
    root = Path(args.path).resolve()
    if not root.is_dir():
        print("[ERROR] 路径不存在或不是目录: %s" % args.path, file=sys.stderr)
        return 4
    files = collect_files(root)
    findings = inventory_checks(root, files)
    findings.extend(pattern_scan(files))
    findings = dedup(findings)
    min_rank = 0
    if args.severity:
        min_rank = _sev_value(args.severity)
    findings = [f for f in findings if _sev_value(f.severity) >= min_rank]

    scope = {
        "skill": root.name, "path": str(root), "source": args.source or "-",
        "reviewed_at": datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%dT%H:%M:%S%z"),
        "reviewer": args.reviewer or "yotta-vetter", "files": len(files),
    }
    if args.report:
        write_report_md(args.report, findings, scope)
    if args.json:
        print(json.dumps({
            "tool": TOOL_NAME, "version": VERSION, "scope": scope,
            "summary": _summary(findings),
            "findings": [f.to_dict() for f in findings],
            "threat": {
                "health_score": _health_score(findings),
                "taxonomy": _taxonomy_view(findings),
                "behaviors": _behavior_view(findings),
            },
        }, indent=2, ensure_ascii=False))
    else:
        print(fmt_report(findings, scope))
    # V3 联动元安：high 及以上输出深度扫描引导命令（走 stderr，避免污染 --json 输出）
    if _worst(findings) in ("high", "critical"):
        print("", file=sys.stderr)
        print("建议深度扫描（联动元安）：", file=sys.stderr)
        print("  yotta-security-audit --target skill --path %s" % root, file=sys.stderr)
    return _sev_value(_worst(findings))


def _summary(findings):
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for f in findings:
        counts[f.severity] = counts.get(f.severity, 0) + 1
    return counts

# ── source 命令（V4 来源半自动化检查）─────────────────────────────────────

def cache_dir():
    d = Path.home() / ".cache" / "yotta-vetter"
    try:
        d.mkdir(parents=True, exist_ok=True)
    except OSError:
        d = Path(tempfile.gettempdir()) / "yotta-vetter-cache"
        d.mkdir(parents=True, exist_ok=True)
    return d


def cache_file(owner, repo):
    return cache_dir() / ("%s__%s.json" % (owner, repo))


def fetch_github_repo(owner, repo, use_cache=True, timeout=15):
    """拉取 GitHub 仓库元数据；无网络/限速自动降级到本地缓存。"""
    cf = cache_file(owner, repo)
    cached = None
    if use_cache and cf.is_file():
        try:
            cached = json.loads(cf.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            cached = None
    url = "https://api.github.com/repos/%s/%s" % (owner, repo)
    req = urllib.request.Request(url, headers={
        "User-Agent": "yotta-vetter/%s" % VERSION,
        "Accept": "application/vnd.github+json",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="replace"))
        data["_fetched_at"] = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
        try:
            cf.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        except OSError:
            pass
        return data, None
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None, "仓库不存在: %s/%s" % (owner, repo)
        if e.code in (401, 403, 429):
            msg = "GitHub API 限速/鉴权失败（HTTP %d），已回退本地缓存" % e.code
            return cached, msg
        return cached, "GitHub API 错误（HTTP %d），已回退本地缓存" % e.code
    except (urllib.error.URLError, OSError) as e:
        return cached, "网络不可用（%s），已回退本地缓存" % (e or "连接失败")


def source_risk_hints(data):
    hints = []
    stars = data.get("stargazers_count", 0)
    if stars < 10:
        hints.append("stars=%d（<10，可信度信号弱）" % stars)
    lic = (data.get("license") or {}).get("spdx_id")
    if not lic:
        hints.append("无许可证声明")
    if data.get("archived"):
        hints.append("仓库已归档（不再维护）")
    updated = data.get("updated_at", "")
    if updated:
        try:
            t = datetime.strptime(updated[:10], "%Y-%m-%d")
            if (datetime.now() - t).days > 365:
                hints.append("超过一年未更新（%s）" % updated[:10])
        except ValueError:
            pass
    if data.get("description"):
        hints.append("描述: %s" % data["description"][:100])
    return hints


def cmd_source(args):
    spec = args.source
    if spec.startswith("github:"):
        spec = spec[len("github:"):]
    spec = spec.strip().strip("/")
    if "/" not in spec:
        print("[ERROR] 来源格式应为 github:owner/repo 或 owner/repo", file=sys.stderr)
        return 4
    owner, repo = spec.split("/", 1)
    data, warn = fetch_github_repo(owner, repo, use_cache=not args.no_cache)
    if data is None:
        print("[ERROR] %s" % (warn or "获取失败"), file=sys.stderr)
        return 1
    hints = source_risk_hints(data)
    result = {
        "owner": owner, "repo": repo,
        "stars": data.get("stargazers_count", 0),
        "forks": data.get("forks_count", 0),
        "updated_at": data.get("updated_at", ""),
        "license": (data.get("license") or {}).get("spdx_id"),
        "archived": data.get("archived", False),
        "default_branch": data.get("default_branch", ""),
        "description": data.get("description", ""),
        "fetched_at": data.get("_fetched_at", ""),
        "hints": hints,
        "cache": bool((cache_file(owner, repo)).is_file()),
    }
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("来源检查: %s/%s" % (owner, repo))
        print("  stars=%s  forks=%s  updated=%s" % (
            result["stars"], result["forks"], (result["updated_at"] or "-")[:10]))
        print("  license=%s  archived=%s  branch=%s" % (
            result["license"] or "-", result["archived"], result["default_branch"]))
        for h in hints:
            print("  - %s" % h)
        if warn:
            print("  [提示] %s" % warn)
    return 0


# ── 参数解析与入口 ──────────────────────────────────────────────────────────

class _VetterParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(4, "%s: error: %s\n" % (self.prog, message))


def build_parser():
    ap = _VetterParser(prog=TOOL_NAME, description="YottaMeta 元审 —— 技能审查 checker")
    sub = ap.add_subparsers(dest="command", required=True)

    pc = sub.add_parser("check", help="四阶段初审")
    pc.add_argument("path", help="技能目录")
    pc.add_argument("--source", default="", help="来源说明（如 github:owner/repo）")
    pc.add_argument("--reviewer", default="", help="审查者")
    pc.add_argument("--json", action="store_true")
    pc.add_argument("--severity", choices=["low", "medium", "high", "critical"])
    pc.add_argument("--report", metavar="FILE")
    pc.add_argument("--no-color", action="store_true")

    ps = sub.add_parser("source", help="来源半自动化检查")
    ps.add_argument("source", help="github:owner/repo 或 owner/repo")
    ps.add_argument("--json", action="store_true")
    ps.add_argument("--no-cache", action="store_true")
    ps.add_argument("--report", metavar="FILE")

    return ap


def main(argv=None):
    ap = build_parser()
    args = ap.parse_args(argv)
    try:
        if args.command == "check":
            return cmd_check(args)
        if args.command == "source":
            return cmd_source(args)
        ap.error("未知命令: %s" % args.command)
    except OSError as e:
        print("[ERROR] 文件操作失败: %s" % e, file=sys.stderr)
        return 4


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except KeyboardInterrupt:
        sys.exit(4)
    except Exception as e:
        print("[FATAL] %s: %s" % (TOOL_NAME, e), file=sys.stderr)
        sys.exit(4)
