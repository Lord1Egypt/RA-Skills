#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""yotta_audit.py — YottaMeta 元安（yotta-security-audit）安全扫描引擎。

双模式（--target）：
  skill   扫描 AI 技能目录中的恶意模式（13 类检测器，默认）
  system  系统安全基线扫描（Windows/Linux，平台感知，只读）

设计原则：
- 纯 Python 3.8+ 标准库，零依赖；Windows/Linux 通用。
- 只读检测：绝不做修复、删除、杀毒等变更动作。
- 报告默认脱敏：不打印私钥、环境变量值、完整凭据，只给路径+模式+建议。
- 检测器可自扫（dogfooding）：扫描自身不产生中高危误报。

exit code 语义（三技能统一）：
  0 = 干净 / 仅有 low 提示
  1 = 存在 medium
  2 = 存在 high
  3 = 存在 critical
  4 = 扫描器自身错误（参数错误/致命异常）

用法示例：
  python3 yotta_audit.py --target skill                  # 扫描所有已发现技能
  python3 yotta_audit.py --path ./some-skill             # 扫描单个技能目录
  python3 yotta_audit.py --target system --platform auto # 系统安全基线
  python3 yotta_audit.py --json --report report.md       # JSON + 报告文件
"""
import argparse
import base64
import csv
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

try:
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# 引入共享规则表（audit_rules.py 与脚本同目录）
_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
import audit_rules  # noqa: E402

VERSION = "0.3.3"
TOOL_NAME = "yotta-security-audit"

# ── 技能目录发现（17 类智能体权威映射，与 install.js 一致）──────────────
AGENT_USER_DIRS = [
    ".claude/skills",          # Claude Code
    ".cursor/skills",          # Cursor
    ".codex/skills",           # Codex（特判 $CODEX_HOME）
    ".gemini/skills",          # Gemini CLI
    ".config/goose/skills",    # Goose
    ".config/agents/skills",   # Amp
    ".config/opencode/skills", # OpenCode（特判 $XDG_CONFIG_HOME）
    ".codeium/windsurf/skills",  # Windsurf
    ".workbuddy/skills",       # WorkBuddy
    ".kiro/skills",            # Kiro
    ".traecli/skills",         # Trae Code CLI
    ".trae-cn/skills",         # Trae IDE（国内）
    ".qwen/skills",            # Qwen Code
    ".comate/skills",          # Comate 文心快码
    ".codebuddy/skills",       # CodeBuddy Code
    ".kimi/skills",            # Kimi Code CLI
    ".agents/skills",          # 通用 AGENTS.md
]
AGENT_PROJECT_DIRS = [d for d in AGENT_USER_DIRS if not d.startswith(".config/")]

SKIP_DIRS = {
    "venv", "node_modules", ".git", "__pycache__", ".mypy_cache", ".tox",
    "dist", "build", ".egg-info", ".venv", ".idea", ".vscode",
}
TEXT_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".mjs", ".cjs", ".sh", ".bash", ".zsh",
    ".md", ".txt", ".yaml", ".yml", ".json", ".toml", ".ini", ".cfg",
    ".rb", ".go", ".rs", ".java", ".c", ".cpp", ".h", ".hpp",
    ".html", ".css", ".xml", ".svg", ".plist", ".ps1", ".bat", ".cmd",
    ".env", ".conf", ".properties", ".gradle",
}
MAX_FILE_SIZE = 1_000_000  # 1 MB
# 签名数据文件：规则表是扫描器自身的签名数据库，不是被测技能行为，扫描时跳过
SIGNATURE_DATA_FILES = {
    "audit_rules.py", "vetter_rules.py", "verify_rules.py", "hardening_rules.py",
    "student_data_rules.json",
}

# 无扩展名的点文件也纳入扫描（.env 等凭据文件常见形态）
DOTFILE_NAMES = {
    ".env", ".env.example", ".netrc", ".pgpass", ".bashrc", ".zshrc",
    ".profile", ".bash_profile", ".npmrc", ".gitconfig",
}
MAX_FILES_PER_SKILL = 1000
MAX_LINE_LEN = audit_rules.MAX_LINE_LEN

# ── 脱敏 ───────────────────────────────────────────────────────────────────
_SECRET_RE = re.compile(
    r"(?i)(password|passwd|pwd|token|secret|api[_-]?key|private[_-]?key|"
    r"authorization|bearer|client[_-]?secret|access[_-]?key)"
    r"\s*[=:]\s*\S+"
)
_PRIVKEY_RE = re.compile(r"(?is)-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----")


def redact(text):
    """脱敏：掩掉常见凭据形态；保留路径/模式/建议。"""
    if not text:
        return text
    text = _PRIVKEY_RE.sub("[REDACTED: private key]", text)
    text = _SECRET_RE.sub(lambda m: m.group(1) + "=<redacted>", text)
    return text

# ── Finding ─────────────────────────────────────────────────────────────────

class Finding:
    __slots__ = ("detector", "severity", "category", "file_path", "line",
                 "description", "confidence", "rule_id", "detail", "extra")

    def __init__(self, detector, severity, category, file_path, line=0,
                 description="", confidence=50, rule_id="", detail="", extra=None):
        self.detector = detector
        self.severity = severity
        self.category = category
        self.file_path = file_path
        self.line = line
        self.description = description
        self.confidence = confidence
        self.rule_id = rule_id
        self.detail = detail
        self.extra = extra

    def to_dict(self):
        data = {
            "detector": self.detector,
            "severity": self.severity,
            "category": self.category,
            "file": self.file_path,
            "line": self.line,
            "description": self.description,
            "confidence": self.confidence,
            "rule_id": self.rule_id,
        }
        if self.extra:
            data["extra"] = self.extra
        return data


# ── IOC 数据库 ────────────────────────────────────────────────────────────

class IOCDatabase:
    """加载 ioc_database.json；缺失/损坏时降级为空库（不阻断扫描）。"""

    def __init__(self, db_path=None):
        if db_path is None:
            db_path = _HERE / "ioc_database.json"
        self.path = Path(db_path)
        self.ips = set()
        self.domains = set()
        self.url_patterns = []
        self.hashes = {}
        self.warning = ""
        self._load()

    def _load(self):
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except Exception as e:
            self.warning = "IOC 数据库加载失败（%s）：%s" % (self.path, e)
            return
        for entry in data.get("malicious_ips", []):
            ip = str(entry.get("ip", "")).strip()
            if ip and not entry.get("example"):
                self.ips.add(ip)
        for entry in data.get("malicious_domains", []):
            dom = str(entry.get("domain", "")).strip().lower()
            if dom and not entry.get("example"):
                self.domains.add(dom)
        for entry in data.get("malicious_url_patterns", []):
            if entry.get("example"):
                continue
            try:
                self.url_patterns.append(re.compile(entry["pattern"]))
            except (re.error, KeyError):
                pass
        for entry in data.get("malicious_hashes", []):
            h = str(entry.get("sha256", "")).strip().lower()
            if h and not entry.get("example"):
                self.hashes[h] = entry.get("filename", "")


# ── 文件收集 ───────────────────────────────────────────────────────────────

def _is_binary(head):
    """按文件头判断是否二进制（含 NUL 字节即视为二进制）。"""
    return b"\x00" in head[:8192]


def collect_files(root):
    """递归收集可扫描文本文件，返回 [Path]。"""
    files = []
    count = 0
    try:
        for dirpath, dirnames, filenames in os.walk(str(root)):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fname in sorted(filenames):
                if count >= MAX_FILES_PER_SKILL:
                    return files
                p = Path(dirpath) / fname
                try:
                    if (p.suffix.lower() not in TEXT_EXTENSIONS
                            and p.name.lower() not in DOTFILE_NAMES):
                        continue
                    if p.name in SIGNATURE_DATA_FILES:
                        continue  # 签名数据（规则表），非被测行为
                    if p.stat().st_size > MAX_FILE_SIZE:
                        continue
                except OSError:
                    continue
                try:
                    with open(p, "rb") as fh:
                        head = fh.read(8192)
                    if _is_binary(head):
                        continue
                except OSError:
                    continue
                files.append(p)
                count += 1
    except OSError:
        pass
    return files


def read_text(p):
    """按 UTF-8 读取，非 UTF-8 用 errors=replace 兜底，绝不崩。"""
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def sha256_of(p):
    try:
        h = hashlib.sha256()
        with open(p, "rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    except OSError:
        return ""


# ── 技能目录发现 ───────────────────────────────────────────────────────────

def _codex_user_skills():
    base = os.environ.get("CODEX_HOME") or str(Path.home() / ".codex")
    return Path(base) / "skills"


def _opencode_user_skills():
    base = os.environ.get("XDG_CONFIG_HOME") or str(Path.home() / ".config")
    return Path(base) / "opencode" / "skills"


def _resolve_user_dir(rel):
    if rel == ".codex/skills":
        return _codex_user_skills()
    if rel == ".config/opencode/skills":
        return _opencode_user_skills()
    return Path.home() / rel


def _is_own_package(path):
    """判断目录是否为元安自身安装目录（含 scripts/yotta_audit.py）。"""
    try:
        if (Path(path) / "scripts" / "yotta_audit.py").is_file():
            return True
    except OSError:
        pass
    return False


def discover_skills(explicit_path=None, include_self=False):
    """发现技能目录，返回 [{'name','path','files'}]。

    explicit_path：扫描单个目录（视为一个技能）。
    自动发现：用户级 + 项目级 17 类目录的每个直接子目录视为一个技能；
    元安自身目录默认跳过（--include-self 强制包含）。
    """
    if explicit_path:
        p = Path(explicit_path).resolve()
        if not p.is_dir():
            raise SystemExit("路径不存在或不是目录: %s" % explicit_path)
        return [{"name": p.name, "path": p, "files": collect_files(p)}]

    roots = []
    for rel in AGENT_USER_DIRS:
        roots.append(_resolve_user_dir(rel))
    for rel in AGENT_PROJECT_DIRS:
        roots.append(Path.cwd() / rel)
    # 兼容：当前目录下的 .skills 与 .claude/skills 等已被覆盖，无需额外

    seen = set()
    skills = []
    for root in roots:
        if not root.is_dir():
            continue
        try:
            children = sorted(root.iterdir())
        except OSError:
            continue
        for child in children:
            if not child.is_dir():
                continue
            if child.name in SKIP_DIRS:
                continue
            try:
                rp = child.resolve()
            except OSError:
                continue
            if rp in seen:
                continue
            if _is_own_package(rp) and not include_self:
                continue
            seen.add(rp)
            skills.append({"name": child.name, "path": child, "files": collect_files(child)})
    return skills

# ── 检测器（13 类）─────────────────────────────────────────────────────────

class PatternRuleDetector:
    """表驱动检测器：从 audit_rules 读取指定检测器的全部规则，逐行匹配。

    覆盖 8 类：DownloadExec / Obfuscation / Persistence / Exfiltration /
    CredentialTheft / NetworkCall / PrivilegeEscalation / SocialEngineering。
    """

    def __init__(self, detector_name, category):
        self.detector_name = detector_name
        self.category = category
        self.rules = audit_rules.get_rules(detector_name)
        self.compiled = [(r, audit_rules.compile_rules()[r.id]) for r in self.rules]

    def scan_file(self, content, file_path):
        findings = []
        basename = os.path.basename(str(file_path))
        for lineno, raw_line in enumerate(content.splitlines(), 1):
            if len(raw_line) > MAX_LINE_LEN:
                raw_line = raw_line[:MAX_LINE_LEN]
            for rule, cre in self.compiled:
                m = cre.search(raw_line)
                if not m:
                    continue
                # SocialEngineering：仅对文件名/路径命中更可靠，行命中给低置信度
                confidence = rule.confidence
                snippet = redact(raw_line.strip())[:160]
                findings.append(Finding(
                    detector=self.detector_name,
                    severity=rule.severity,
                    category=self.category,
                    file_path=str(file_path),
                    line=lineno,
                    description=rule.description,
                    confidence=confidence,
                    rule_id=rule.id,
                    detail=snippet,
                ))
        return findings


class Base64Detector:
    """检测超长 Base64 编码串；解码后含敏感关键字 → high，否则 low。"""

    name = "Base64Detector"
    category = "obfuscation"
    _blob = re.compile(r"[A-Za-z0-9+/]{60,}={0,2}")
    _hex_hash = re.compile(r"^[0-9a-fA-F]{60,}$")
    _skip_ctx = re.compile(
        r"(?i)(data:\s*(image|text|application)|integrity\s*[=:]|sha(256|384|512)-|sha1-|"
        r"\"hash\"\s*[=:]|longitude|latitude)"
    )
    _suspicious = re.compile(
        r"(?i)(exec|eval|subprocess|os\.system|curl|wget|/bin/sh|socket|"
        r"reverse|powershell|download)"
    )
    _lockfiles = {"package-lock.json", "yarn.lock", "pnpm-lock.yaml", "npm-shrinkwrap.json"}

    def scan_file(self, content, file_path):
        findings = []
        basename = os.path.basename(str(file_path))
        if basename in self._lockfiles:
            return findings
        for lineno, raw_line in enumerate(content.splitlines(), 1):
            if len(raw_line) > MAX_LINE_LEN:
                raw_line = raw_line[:MAX_LINE_LEN]
            if self._skip_ctx.search(raw_line):
                continue
            for m in self._blob.finditer(raw_line):
                blob = m.group()
                if self._hex_hash.match(blob):
                    continue  # 十六进制长串更像哈希/摘要，交给 Entropy 判断
                try:
                    decoded = base64.b64decode(blob, validate=False)
                except Exception:
                    continue
                if not decoded:
                    continue
                try:
                    text = decoded.decode("utf-8")
                    suspicious = bool(self._suspicious.search(text))
                except UnicodeDecodeError:
                    text = ""
                    suspicious = False
                if suspicious:
                    sev, conf = "high", 85
                elif text and len(text) > 20:
                    sev, conf = "low", 40
                else:
                    sev, conf = "low", 30
                findings.append(Finding(
                    detector=self.name, severity=sev, category=self.category,
                    file_path=str(file_path), line=lineno,
                    description="Base64 编码串（%d 字符）%s" % (
                        len(blob), "，解码含敏感关键字" if suspicious else "，需结合上下文"),
                    confidence=conf, rule_id="B64-001",
                    detail=redact(raw_line.strip())[:160],
                ))
        return findings


class IOCMatchDetector:
    """命中已知 IOC（IP/域名/URL 模式/文件哈希）。"""

    name = "IOCMatchDetector"
    category = "threat_intelligence"

    def __init__(self, ioc_db):
        self.ioc_db = ioc_db

    def scan_file(self, content, file_path):
        findings = []
        for lineno, raw_line in enumerate(content.splitlines(), 1):
            if len(raw_line) > MAX_LINE_LEN:
                raw_line = raw_line[:MAX_LINE_LEN]
            for ip in self.ioc_db.ips:
                if ip in raw_line:
                    findings.append(self._mk("已知恶意 IP: %s" % ip, file_path, lineno, raw_line, 95))
            for dom in self.ioc_db.domains:
                if dom in raw_line.lower():
                    findings.append(self._mk("已知恶意域名: %s" % dom, file_path, lineno, raw_line, 95))
            for pat in self.ioc_db.url_patterns:
                if pat.search(raw_line):
                    findings.append(self._mk(
                        "命中恶意 URL 模式: %s" % pat.pattern, file_path, lineno, raw_line, 90))
        # 文件哈希比对
        h = sha256_of(file_path)
        if h in self.ioc_db.hashes:
            findings.append(Finding(
                detector=self.name, severity="critical", category=self.category,
                file_path=str(file_path), line=0,
                description="文件 SHA256 命中已知恶意哈希（%s）" % self.ioc_db.hashes[h],
                confidence=99, rule_id="IOC-HASH", detail=""))
        return findings

    def _mk(self, desc, file_path, lineno, raw_line, conf):
        return Finding(
            detector=self.name, severity="critical", category=self.category,
            file_path=str(file_path), line=lineno, description=desc, confidence=conf,
            rule_id="IOC-MATCH", detail=redact(raw_line.strip())[:160],
        )


class PostInstallHookDetector:
    """安装钩子：npm lifecycle scripts / Python setup.py cmdclass。"""

    name = "PostInstallHookDetector"
    category = "supply_chain"
    _susp = re.compile(audit_rules.POSTINSTALL_SUSPICIOUS)
    _hooks = ("postinstall", "preinstall", "install", "prepare")

    def scan_file(self, content, file_path):
        findings = []
        basename = os.path.basename(str(file_path))
        lines = content.splitlines()
        if basename == "package.json":
            try:
                pkg = json.loads(content)
            except json.JSONDecodeError:
                return findings
            scripts = pkg.get("scripts") or {}
            for hook in self._hooks:
                val = scripts.get(hook)
                if not val:
                    continue
                suspicious = bool(self._susp.search(str(val)))
                sev = "critical" if suspicious else "high"
                conf = 90 if suspicious else 60
                for i, line in enumerate(lines, 1):
                    if re.search(r'["\']%s["\']\s*:' % hook, line):
                        findings.append(Finding(
                            detector=self.name, severity=sev, category=self.category,
                            file_path=str(file_path), line=i,
                            description="npm 生命周期钩子 %s（%s）" % (
                                hook, "含下载/执行行为" if suspicious else "存在安装期脚本"),
                            confidence=conf, rule_id="PIH-001",
                            detail=redact(line.strip())[:160],
                        ))
                        break
        if basename == "setup.py":
            for i, line in enumerate(lines, 1):
                if re.search(r"cmdclass\s*=", line):
                    findings.append(Finding(
                        detector=self.name, severity="high", category=self.category,
                        file_path=str(file_path), line=i,
                        description="Python setup.py 自定义命令类（潜在安装钩子）",
                        confidence=55, rule_id="PIH-002",
                        detail=redact(line.strip())[:160],
                    ))
        return findings


class HiddenCharDetector:
    """零宽字符与 Unicode 双向覆盖字符。"""

    name = "HiddenCharDetector"
    category = "obfuscation"
    _zwc = re.compile(r"[\u200b\u200c\u200d\u2060]")
    _bidi = re.compile(r"[\u202a\u202b\u202c\u202d\u202e\u2066\u2067\u2068\u2069]")

    def scan_file(self, content, file_path):
        findings = []
        lines = content.splitlines()
        for i, raw_line in enumerate(lines, 1):
            body = raw_line
            # 文件首行的 BOM（U+FEFF）不算零宽隐藏字符
            if i == 1 and body.startswith("\ufeff"):
                body = body[1:]
            kinds = []
            if self._zwc.search(body):
                kinds.append("零宽字符")
            if self._bidi.search(body):
                kinds.append("双向覆盖字符")
            if kinds:
                findings.append(Finding(
                    detector=self.name, severity="medium", category=self.category,
                    file_path=str(file_path), line=i,
                    description="发现%s（可用于隐藏恶意代码）" % "、".join(kinds),
                    confidence=70, rule_id="HID-001",
                    detail=repr(body.strip()[:120]),
                ))
        return findings


def shannon_entropy(s):
    if not s:
        return 0.0
    freq = {}
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1
    n = float(len(s))
    return -sum((c / n) * math.log2(c / n) for c in freq.values())


class EntropyDetector:
    """高熵编码串检测：长行 + 高熵 + 编码字母表占比高。"""

    name = "EntropyDetector"
    category = "obfuscation"
    _blob_chars = set(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ" + "abcdefghijklmnopqrstuvwxyz"
        + "0123456789" + "+/=_-"
    )

    def scan_file(self, content, file_path):
        findings = []
        for lineno, raw_line in enumerate(content.splitlines(), 1):
            line = raw_line.strip()
            if len(line) < 40 or len(line) > MAX_LINE_LEN:
                continue
            if '"' in line or "'" in line:
                continue  # 带引号的行是代码/文本字面量，不是未引用的编码载荷
            blob_ratio = sum(1 for ch in line if ch in self._blob_chars) / len(line)
            if blob_ratio < 0.85:
                continue
            ent = shannon_entropy(line)
            if ent < 5.0:
                continue
            findings.append(Finding(
                detector=self.name, severity="medium", category=self.category,
                file_path=str(file_path), line=lineno,
                description="高熵编码串（熵 %.2f，疑似混淆/加密载荷）" % ent,
                confidence=55, rule_id="ENT-001",
                detail=redact(line[:160]),
            ))
        return findings

class FilenameDetector:
    """按文件名匹配：敏感凭据文件名（CredentialTheft）+ 社会工程命名（SocialEngineering）。

    社会工程规则只作用于文件名而非正文，避免文档示例造成误报。
    """

    name = "FilenameDetector"
    category = "filename"

    def scan_file(self, content, file_path):
        findings = []
        base = os.path.basename(str(file_path))
        base_l = base.lower()
        for pat, desc, sev, conf in audit_rules.SENSITIVE_FILENAMES:
            if pat.lower() in base_l:
                findings.append(Finding(
                    detector="CredentialTheft", severity=sev, category="credential_theft",
                    file_path=str(file_path), line=0,
                    description="发现敏感凭据文件命名: %s" % desc,
                    confidence=conf, rule_id="FIL-SENS",
                    detail=redact(base)[:120],
                ))
        for rule in audit_rules.get_rules("SocialEngineering"):
            cre = audit_rules.compile_rules()[rule.id]
            if cre.search(base_l):
                findings.append(Finding(
                    detector="SocialEngineering", severity=rule.severity,
                    category="social_engineering",
                    file_path=str(file_path), line=0,
                    description=rule.description + "（文件名）",
                    confidence=rule.confidence, rule_id=rule.id,
                    detail=redact(base)[:120],
                ))
        return findings


# ══════════════════════════════════════════════════════════════════════════
# 教育版（--target edu）：学生数据隐私风险扫描
# ══════════════════════════════════════════════════════════════════════════
# 设计口径（docs/元安-教育版S1设计-2026-09-27.md）：
# - 只读、零网络、不执行被扫描内容；显式 --path，不做自动发现；
# - 报告一律不回显原文（不提供 --show-raw），只给脱敏样例、位置与计数；
# - 规则包是只读 JSON 数据，不执行表达式；级别是风险提示分级，不是法律定性。

EDU_MAX_FILE_SIZE = 4 * 1024 * 1024   # 单文件 4 MB
EDU_MAX_FILES = 2000
EDU_MAX_ROWS = 5000                   # 单表最多解析行数
EDU_TEXT_EXTENSIONS = {
    ".csv", ".tsv", ".txt", ".md", ".markdown", ".json", ".jsonl",
    ".xml", ".html", ".htm", ".yaml", ".yml",
}
EDU_CONTAINER_EXTENSIONS = {".xlsx", ".docx"}
EDU_BINARY_NOTICE_EXTENSIONS = {
    ".pdf", ".doc", ".xls", ".ppt", ".pptx", ".png", ".jpg", ".jpeg", ".gif",
    ".bmp", ".webp", ".tif", ".tiff", ".zip", ".rar", ".7z", ".gz", ".db",
    ".sqlite", ".mp3", ".mp4", ".mov",
}

EDU_CATEGORY_NAMES = {
    "direct_identifier": "直接标识符",
    "quasi_identifier": "准标识符与组合",
    "sensitive_attribute": "敏感属性",
    "handling_risk": "存放与流转风险",
}
EDU_CATEGORY_ORDER = ("direct_identifier", "quasi_identifier",
                      "sensitive_attribute", "handling_risk")
EDU_RULE_SEVERITIES = ("low", "medium", "high", "critical")
EDU_CONTENT_KINDS = ("id_card", "phone", "email", "keyword_any")
EDU_VALUE_KINDS = ("any", "alnum", "phone")
EDU_PATH_MATCH_KINDS = ("substring", "segment")
EDU_DISCLAIMER = (
    "本报告只做基于规则的隐私风险提示，不回显原文，不构成法律意见或合规结论；"
    "条款级判断请使用元规 yotta-compliance，处置动作由用户决定。"
)
EDU_UNPARSED_NOTE = "未解析格式（PDF / 图片 / 旧版 Office / 压缩包等）请先转为文本或导出 CSV"


class RulePackError(Exception):
    """规则包缺失、不可读或结构不合法。"""


_ID_CARD_WEIGHTS = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)
_ID_CARD_CHECK = "10X98765432"
_ID_CARD_RE = re.compile(r"(?<![0-9A-Za-z])[1-9]\d{16}[0-9Xx](?![0-9A-Za-z])")
_PHONE_RE = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
_EMAIL_RE = re.compile(
    r"[A-Za-z0-9._%+-]{1,64}@[A-Za-z0-9-]{1,63}(?:\.[A-Za-z0-9-]{1,63}){0,4}\.[A-Za-z]{2,24}")
_ALNUM_RE = re.compile(r"^[0-9A-Za-z][0-9A-Za-z-]{7,24}$")
_XLSX_SHEET_RE = re.compile(r"^xl/worksheets/sheet\d+\.xml$")
_EDU_DIGIT_RUN_RE = re.compile(r"\d{8,}")


def edu_id_card_valid(value):
    """18 位身份证号 + GB 11643 校验位（MOD 11-2）。"""
    if len(value) != 18:
        return False
    body = value[:17]
    if not body.isdigit():
        return False
    total = sum(int(body[i]) * _ID_CARD_WEIGHTS[i] for i in range(17))
    return value[17].upper() == _ID_CARD_CHECK[total % 11]


# ── 脱敏（固定规则、可复算；报告永不回显原文）───────────────────────────

def _mask_keep_tail(value, keep=4):
    text = str(value)
    if len(text) <= keep:
        return "*" * len(text)
    return "*" * (len(text) - keep) + text[-keep:]


def edu_mask_id_card(value):
    return _mask_keep_tail(value, 4)


def edu_mask_phone(value):
    return _mask_keep_tail(value, 4)


def edu_mask_email(value):
    text = str(value)
    if "@" not in text:
        return "***"
    local, domain = text.split("@", 1)
    return (local[:1] or "*") + "***@" + domain


def edu_mask_name(value):
    text = str(value)
    return (text[:1] + "*") if len(text) >= 2 else "*"


def edu_mask_address(value):
    text = str(value)
    return (text[:3] + "**") if len(text) > 5 else "***"


def edu_mask_generic(value):
    text = str(value)
    return (text[:1] + "***") if text else "***"


def edu_mask_score(value):
    return "**"


def edu_mask_birth(value):
    m = re.match(r"^(\d{4})", str(value).strip())
    return (m.group(1) + "-**-**") if m else "****"


def edu_mask_student_no(value):
    text = str(value).strip()
    if len(text) < 6:
        return "***"
    return text[:2] + "***" + text[-2:]


_EDU_FIELD_MASKERS = {
    "student_name": edu_mask_name,
    "id_card": edu_mask_id_card,
    "student_no": edu_mask_student_no,
    "phone": edu_mask_phone,
    "address": edu_mask_address,
    "birth": edu_mask_birth,
    "guardian": edu_mask_phone,
    "score": edu_mask_score,
    "health": edu_mask_generic,
    "welfare": edu_mask_generic,
    "biometric": edu_mask_generic,
}


# ── 规则包加载与校验 ───────────────────────────────────────────────────────

def _edu_default_rules_path():
    return _HERE / "student_data_rules.json"


def load_edu_rule_pack(path=None):
    """加载并校验教育版规则包；失败抛 RulePackError（fail-closed）。"""
    p = Path(path) if path else _edu_default_rules_path()
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise RulePackError("规则包不存在: %s" % p)
    except (OSError, ValueError) as e:
        raise RulePackError("规则包读取或解析失败（%s）：%s" % (p, e))
    validate_edu_rule_pack(data, source=str(p))
    return data


def validate_edu_rule_pack(data, source="<memory>"):
    def fail(msg):
        raise RulePackError("规则包不合法（%s）：%s" % (source, msg))

    if not isinstance(data, dict):
        fail("顶层必须是 JSON 对象")
    if data.get("schema_version") != "1.0":
        fail("schema_version 必须为 1.0")
    vocab = data.get("field_vocab")
    if not isinstance(vocab, dict) or not vocab:
        fail("field_vocab 必须是非空对象")
    for key, terms in vocab.items():
        if not isinstance(terms, list) or not terms:
            fail("field_vocab.%s 必须是非空字符串数组" % key)
        if not all(isinstance(t, str) and t.strip() for t in terms):
            fail("field_vocab.%s 含空项或非字符串" % key)

    seen_ids = set()

    def check_common(rule, section):
        if not isinstance(rule, dict):
            fail("%s 的规则必须是对象" % section)
        rule_id = rule.get("id")
        if not isinstance(rule_id, str) or not rule_id.strip():
            fail("%s 存在缺少 id 的规则" % section)
        if rule_id in seen_ids:
            fail("rule_id 重复: %s" % rule_id)
        seen_ids.add(rule_id)
        if not isinstance(rule.get("title"), str) or not rule["title"].strip():
            fail("%s 规则 %s 缺少 title" % (section, rule_id))
        if rule.get("category") not in EDU_CATEGORY_NAMES:
            fail("%s 规则 %s 的 category 非法" % (section, rule_id))
        if rule.get("severity") not in EDU_RULE_SEVERITIES:
            fail("%s 规则 %s 的 severity 非法" % (section, rule_id))
        if not isinstance(rule.get("remediation", ""), str):
            fail("%s 规则 %s 的 remediation 必须是字符串" % (section, rule_id))

    def check_list(section):
        items = data.get(section)
        if not isinstance(items, list):
            fail("%s 必须是数组" % section)
        return items

    for rule in check_list("content_rules"):
        check_common(rule, "content_rules")
        if rule.get("kind") not in EDU_CONTENT_KINDS:
            fail("content_rules 规则 %s 的 kind 非法" % rule.get("id"))
        if rule["kind"] == "keyword_any":
            kws = rule.get("keywords")
            if not isinstance(kws, list) or not kws:
                fail("content_rules 规则 %s 缺少 keywords" % rule.get("id"))

    for rule in check_list("field_rules"):
        check_common(rule, "field_rules")
        if rule.get("field") not in vocab:
            fail("field_rules 规则 %s 引用了未定义词表" % rule.get("id"))
        if rule.get("value_kind", "any") not in EDU_VALUE_KINDS:
            fail("field_rules 规则 %s 的 value_kind 非法" % rule.get("id"))

    for rule in check_list("combo_rules"):
        check_common(rule, "combo_rules")
        fields = rule.get("fields")
        if not isinstance(fields, list) or len(fields) < 2:
            fail("combo_rules 规则 %s 的 fields 至少两项" % rule.get("id"))
        if not all(f in vocab for f in fields):
            fail("combo_rules 规则 %s 引用了未定义词表" % rule.get("id"))

    for rule in check_list("path_rules"):
        check_common(rule, "path_rules")
        if rule.get("match") not in EDU_PATH_MATCH_KINDS:
            fail("path_rules 规则 %s 的 match 非法" % rule.get("id"))
        patterns = rule.get("patterns")
        if not isinstance(patterns, list) or not patterns:
            fail("path_rules 规则 %s 缺少 patterns" % rule.get("id"))

    for rule in check_list("filename_rules"):
        check_common(rule, "filename_rules")
        for key in ("keywords", "surnames"):
            items = rule.get(key)
            if not isinstance(items, list) or not items:
                fail("filename_rules 规则 %s 缺少 %s" % (rule.get("id"), key))

    return True


# ── 文件收集与解析（只读）─────────────────────────────────────────────────

def _edu_is_binary(path):
    try:
        with open(path, "rb") as fh:
            return _is_binary(fh.read(8192))
    except OSError:
        return True


def collect_edu_files(root):
    """收集教育版可扫描文件；返回 (files, skipped_ext)。"""
    files = []
    skipped = {}
    count = 0
    root = Path(root)

    def skip(ext):
        key = ext or "(无扩展名)"
        skipped[key] = skipped.get(key, 0) + 1

    if root.is_file():
        ext = root.suffix.lower()
        if ext in EDU_TEXT_EXTENSIONS or ext in EDU_CONTAINER_EXTENSIONS:
            files.append(root)
        else:
            skip(ext)
        return files, skipped

    for dirpath, dirnames, filenames in os.walk(str(root)):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for fname in sorted(filenames):
            if count >= EDU_MAX_FILES:
                skipped["(超出文件数上限)"] = skipped.get("(超出文件数上限)", 0) + 1
                continue
            p = Path(dirpath) / fname
            ext = p.suffix.lower()
            if ext not in EDU_TEXT_EXTENSIONS and ext not in EDU_CONTAINER_EXTENSIONS:
                skip(ext)
                continue
            try:
                if p.stat().st_size > EDU_MAX_FILE_SIZE:
                    skip(ext)
                    continue
            except OSError:
                skip(ext)
                continue
            if ext in EDU_TEXT_EXTENSIONS and _edu_is_binary(p):
                skip(ext)
                continue
            files.append(p)
            count += 1
    return files, skipped


def _edu_read_text(path):
    """UTF-8（含 BOM）→ GBK → 替换兜底，绝不崩。"""
    try:
        raw = Path(path).read_bytes()
    except OSError as e:
        raise RulePackError("文件不可读: %s" % e)
    for enc in ("utf-8-sig", "gbk"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def _edu_parse_delimited(text, ext):
    lines = text.splitlines()
    first = next((l for l in lines if l.strip()), "")
    if ext == ".tsv":
        delim = "\t"
    else:
        delim = "," if first.count(",") >= first.count("\t") else "\t"
    rows = []
    for i, row in enumerate(csv.reader(lines, delimiter=delim)):
        if i >= EDU_MAX_ROWS:
            break
        rows.append([str(c).strip() for c in row])
    return rows


def _edu_col_index(letters):
    idx = 0
    for ch in letters.upper():
        idx = idx * 26 + (ord(ch) - ord("A") + 1)
    return idx - 1


def _edu_xml_text(elem):
    return "".join(t.text or "" for t in elem.iter() if t.tag.endswith("}t"))


def _edu_parse_xlsx(path):
    """标准库读取 xlsx 文本（共享字符串 / 内联字符串）；返回表格列表。"""
    with zipfile.ZipFile(str(path)) as z:
        names = set(z.namelist())
        shared = []
        if "xl/sharedStrings.xml" in names:
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in root:
                shared.append(_edu_xml_text(si))
        tables = []
        for name in sorted(n for n in names if _XLSX_SHEET_RE.match(n)):
            sheet = ET.fromstring(z.read(name))
            rows = []
            for row in sheet.iter():
                if not row.tag.endswith("}row"):
                    continue
                if len(rows) >= EDU_MAX_ROWS:
                    break
                cells = {}
                fallback = 0
                for cell in row:
                    if not cell.tag.endswith("}c"):
                        continue
                    ref = cell.get("r") or ""
                    m = re.match(r"^([A-Za-z]+)", ref)
                    idx = _edu_col_index(m.group(1)) if m else fallback
                    fallback = idx + 1
                    ctype = (cell.get("t") or "").lower()
                    value = ""
                    for child in cell:
                        if child.tag.endswith("}v"):
                            value = child.text or ""
                        elif child.tag.endswith("}is"):
                            value = _edu_xml_text(child)
                    if ctype == "s":
                        try:
                            value = shared[int(value)]
                        except (ValueError, IndexError, TypeError):
                            value = ""
                    cells[idx] = str(value).strip()
                width = (max(cells) + 1) if cells else 0
                rows.append([cells.get(i, "") for i in range(width)])
            tables.append(rows)
    return tables


def _edu_parse_docx(path):
    """标准库读取 docx 正文段落文本；返回行列表。"""
    with zipfile.ZipFile(str(path)) as z:
        if "word/document.xml" not in z.namelist():
            raise RulePackError("docx 缺少 word/document.xml: %s" % path)
        root = ET.fromstring(z.read("word/document.xml"))
    lines = []
    for para in root.iter():
        if not para.tag.endswith("}p"):
            continue
        text = _edu_xml_text(para).strip()
        if text:
            lines.append(text)
        if len(lines) >= EDU_MAX_ROWS:
            break
    return lines


# ── 匹配与聚合 ─────────────────────────────────────────────────────────────

def _edu_match_content(rule, text):
    """返回 (命中数, 脱敏样例列表)。"""
    kind = rule["kind"]
    if kind == "id_card":
        samples = [edu_mask_id_card(m.group()) for m in _ID_CARD_RE.finditer(text)
                   if edu_id_card_valid(m.group())]
        return len(samples), samples
    if kind == "phone":
        samples = [edu_mask_phone(m.group()) for m in _PHONE_RE.finditer(text)]
        return len(samples), samples
    if kind == "email":
        samples = [edu_mask_email(m.group()) for m in _EMAIL_RE.finditer(text)]
        return len(samples), samples
    count = 0
    samples = []
    for kw in rule.get("keywords", []):
        n = text.count(kw)
        if n:
            count += n
            if not samples:
                samples.append(kw)  # 类别词本身不是个人数据，可原样提示
    return count, samples


def _edu_find_column(header, terms):
    for idx, cell in enumerate(header):
        compact = re.sub(r"\s+", "", str(cell))
        if not compact:
            continue
        for term in terms:
            if term in compact:
                return idx
    return None


def _edu_path_rule_hit(rule, rel_path):
    text = rel_path.replace("\\", "/")
    lowered = text.lower()
    segments = [s.lower() for s in text.split("/") if s]
    for pattern in rule.get("patterns", []):
        p = str(pattern)
        if rule.get("match") == "segment":
            if p.lower() in segments:
                return True
        elif p.lower() in lowered:
            return True
    return False


def _edu_filename_rule_hit(rule, name):
    """返回 (原始姓名或编号, 脱敏后文件名)；未命中返回 (None, None)。"""
    stem = Path(name).stem
    if not any(k in stem for k in rule.get("keywords", [])):
        return None, None
    token = None
    for surname in rule.get("surnames", []):
        start = 0
        while True:
            idx = stem.find(surname, start)
            if idx < 0:
                break
            tail = stem[idx + len(surname): idx + len(surname) + 2]
            given = "".join(ch for ch in tail if "\u4e00" <= ch <= "\u9fff")
            if given:
                token = surname + given
                break
            start = idx + 1
        if token:
            break
    if not token:
        m = _EDU_DIGIT_RUN_RE.search(stem)
        if not m:
            return None, None
        token = m.group()
    masked = name.replace(token, edu_mask_generic(token))
    return token, masked


def _edu_confidence(severity):
    return {"critical": 80, "high": 72, "medium": 60, "low": 45}.get(severity, 50)


def run_edu_scan(root, pack):
    """执行教育版扫描；返回 (findings, scope)。只读、零网络、不回显原文。"""
    root = Path(root)
    is_dir = root.is_dir()
    files, skipped = collect_edu_files(root)
    aggregated = {}
    records = 0
    parsed = 0

    def emit(rule, rel, key_suffix, line, location, count, sample=""):
        key = (rule["id"], rel, key_suffix)
        item = aggregated.get(key)
        if item is None:
            aggregated[key] = {
                "rule": rule, "rel": rel, "line": line, "location": location,
                "count": count, "sample": sample,
            }
        else:
            item["count"] += count
            if not item["sample"] and sample:
                item["sample"] = sample

    content_rules = pack.get("content_rules", [])
    field_rules = pack.get("field_rules", [])
    combo_rules = pack.get("combo_rules", [])
    path_rules = pack.get("path_rules", [])
    filename_rules = pack.get("filename_rules", [])
    vocab = pack.get("field_vocab", {})

    for p in files:
        try:
            rel = os.path.relpath(str(p), str(root)) if is_dir else p.name
        except ValueError:
            rel = p.name
        rel = rel.replace("\\", "/")
        ext = p.suffix.lower()
        file_hit_count = 0
        display_rel = rel
        filename_hits = []
        for rule in filename_rules:
            token, masked_name = _edu_filename_rule_hit(rule, p.name)
            if not token:
                continue
            # 文件名里的姓名/编号同样属于待脱敏内容：本文件所有条目的路径都改用脱敏名
            display_rel = rel.replace(token, edu_mask_generic(token))
            filename_hits.append((rule, masked_name, token))
        try:
            if ext == ".xlsx":
                tables = _edu_parse_xlsx(p)
            elif ext == ".docx":
                tables = [None]
                lines = _edu_parse_docx(p)
            else:
                text = _edu_read_text(p)
                if ext in (".csv", ".tsv"):
                    tables = [_edu_parse_delimited(text, ext)]
                else:
                    tables = [None]
                    lines = text.splitlines()
        except (RulePackError, OSError, ValueError, zipfile.BadZipFile, ET.ParseError):
            skipped[ext] = skipped.get(ext, 0) + 1
            continue
        parsed += 1

        for table in tables:
            table_findings = 0
            if table is None:
                records += len(lines)
                for rule in content_rules:
                    count = 0
                    sample = ""
                    first_line = 0
                    for lineno, raw in enumerate(lines, 1):
                        hits, samples = _edu_match_content(rule, raw)
                        if not hits:
                            continue
                        if not first_line:
                            first_line = lineno
                        count += hits
                        if not sample and samples:
                            sample = samples[0]
                    if count:
                        emit(rule, display_rel, "line", first_line,
                             "第 %d 行（同文件共 %d 处）" % (first_line, count),
                             count, sample)
                        table_findings += 1
            else:
                header_idx = None
                for i, row in enumerate(table):
                    if any(str(c).strip() for c in row):
                        header_idx = i
                        break
                if header_idx is None:
                    continue
                header = [str(c).strip() for c in table[header_idx]]
                data_rows = table[header_idx + 1:]
                records += len(data_rows)

                for rule in field_rules:
                    col = _edu_find_column(header, vocab.get(rule["field"], []))
                    if col is None:
                        continue
                    values = [str(r[col]).strip() for r in data_rows if col < len(r)]
                    values = [v for v in values if v]
                    if not values:
                        continue
                    value_kind = rule.get("value_kind", "any")
                    if value_kind == "alnum":
                        values = [v for v in values if _ALNUM_RE.match(v)]
                    elif value_kind == "phone":
                        values = [v for v in values if _PHONE_RE.search(v)]
                    if not values:
                        continue
                    masker = _EDU_FIELD_MASKERS.get(rule["field"], edu_mask_generic)
                    emit(rule, display_rel, "col:%d" % col, header_idx + 1,
                         "列「%s」" % header[col], len(values), masker(values[0]))
                    table_findings += 1

                for rule in combo_rules:
                    cols = [_edu_find_column(header, vocab.get(f, []))
                            for f in rule.get("fields", [])]
                    if any(c is None for c in cols) or not data_rows:
                        continue
                    first_row = data_rows[0]
                    parts = []
                    for field, col in zip(rule["fields"], cols):
                        value = str(first_row[col]) if col < len(first_row) else ""
                        masker = _EDU_FIELD_MASKERS.get(field, edu_mask_generic)
                        parts.append(masker(value))
                    emit(rule, display_rel, "combo", header_idx + 1,
                         "列「%s」" % "」「".join(header[c] for c in cols),
                         len(data_rows), " / ".join(parts))
                    table_findings += 1

                for rule in content_rules:
                    for col in range(len(header)):
                        count = 0
                        sample = ""
                        hits, samples = _edu_match_content(rule, header[col])
                        count += hits
                        if samples:
                            sample = samples[0]
                        for row in data_rows:
                            value = str(row[col]).strip() if col < len(row) else ""
                            if not value:
                                continue
                            hits, samples = _edu_match_content(rule, value)
                            if not hits:
                                continue
                            count += hits
                            if not sample and samples:
                                sample = samples[0]
                        if count:
                            emit(rule, display_rel, "col:%d" % col, header_idx + 1,
                                 "列「%s」" % header[col], count, sample)
                            table_findings += 1
            file_hit_count += table_findings

        for rule, masked_name, token in filename_hits:
            emit(rule, masked_name, "filename", 0,
                 "文件名（已部分脱敏）", 1, edu_mask_name(token))
            file_hit_count += 1

        if file_hit_count:
            abs_path = str(p)
            for rule in path_rules:
                if not _edu_path_rule_hit(rule, abs_path):
                    continue
                if rule.get("require_content_hit", True) and not file_hit_count:
                    continue
                emit(rule, display_rel, "path", 0, "所在路径命中规则", 1, "")

    findings = []
    for item in aggregated.values():
        rule = item["rule"]
        detail = item["location"]
        if item["sample"]:
            detail += " · 样例 %s" % item["sample"]
        findings.append(Finding(
            detector="StudentData",
            severity=rule["severity"],
            category=rule["category"],
            file_path=item["rel"],
            line=item["line"],
            description=rule["title"] + "（需人工复核）",
            confidence=_edu_confidence(rule["severity"]),
            rule_id=rule["id"],
            detail=detail,
            extra={
                "masked_sample": item["sample"],
                "count": item["count"],
                "location": item["location"],
                "remediation": rule.get("remediation", ""),
            },
        ))
    order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
    findings.sort(key=lambda f: (order.get(f.severity, 9), f.file_path, f.rule_id))
    scope = {
        "target": "edu",
        "platform": "auto",
        "path": str(root.resolve()),
        "files_scanned": parsed,
        "files_skipped": sum(skipped.values()),
        "skipped_ext": skipped,
        "records_scanned": records,
        "rules": {
            "schema_version": pack.get("schema_version"),
            "pack_version": pack.get("pack_version"),
            "rule_count": sum(len(pack.get(k, [])) for k in (
                "content_rules", "field_rules", "combo_rules", "path_rules", "filename_rules")),
        },
    }
    return findings, scope


def edu_category_view(findings):
    """4 类风险类别视图：命中数 + 最高级别 verdict。"""
    hits = {}
    for f in findings:
        hits.setdefault(f.category, []).append(f)
    out = []
    for key in EDU_CATEGORY_ORDER:
        items = hits.get(key, [])
        sev = "info"
        for f in items:
            if audit_rules.severity_rank(f.severity) > audit_rules.severity_rank(sev):
                sev = f.severity
        if not items:
            verdict = "n/a"
        elif sev in ("critical", "high"):
            verdict = "danger"
        elif sev == "medium":
            verdict = "suspicious"
        else:
            verdict = "safe"
        out.append({"key": key, "name": EDU_CATEGORY_NAMES.get(key, key),
                    "verdict": verdict, "count": len(items)})
    return out


def _edu_scope_lines(scope):
    lines = []
    lines.append("目标: edu（学生数据隐私）  路径: %s" % scope.get("path", ""))
    lines.append("时间: %s" % scope.get("scanned_at", ""))
    rules = scope.get("rules") or {}
    lines.append("范围: 解析文件 %d 个 / 跳过 %d 个 / 记录 %d 条（规则包 %s）" % (
        scope.get("files_scanned", 0), scope.get("files_skipped", 0),
        scope.get("records_scanned", 0), rules.get("pack_version", "-")))
    skipped = scope.get("skipped_ext") or {}
    if skipped:
        items = ", ".join("%s ×%d" % (k, v) for k, v in sorted(skipped.items()))
        lines.append("未解析/跳过: %s" % items)
    return lines


def format_edu_text_report(findings, scope, use_color=False):
    lines = []
    lines.append("=" * 70)
    lines.append("%s %s 学生数据隐私风险扫描报告" % (TOOL_NAME, VERSION))
    lines.append("=" * 70)
    lines.extend(_edu_scope_lines(scope))
    lines.append("")
    counts = _summary_counts(findings)
    lines.append("汇总: CRITICAL %d | HIGH %d | MEDIUM %d | LOW %d | INFO %d" % (
        counts["critical"], counts["high"], counts["medium"],
        counts["low"], counts["info"]))
    lines.append("风险类别（4 类）：")
    for v in edu_category_view(findings):
        lines.append("  %-16s %-11s %d" % (v["name"], v["verdict"], v["count"]))
    lines.append("")
    if not findings:
        lines.append("未发现学生数据隐私风险。")
    order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
    for f in sorted(findings, key=lambda x: (order.get(x.severity, 9), x.file_path, x.rule_id)):
        extra = f.extra or {}
        lines.append("%s %s (%s)" % (_sev_label(f.severity), f.description, f.rule_id))
        lines.append("  位置: %s · %s" % (f.file_path, extra.get("location", "")))
        sample = extra.get("masked_sample") or ""
        lines.append("  样例: %s   命中: %d 处" % (sample or "-", extra.get("count", 1)))
        if extra.get("remediation"):
            lines.append("  建议: %s" % extra["remediation"])
        lines.append("")
    lines.append("说明: %s" % EDU_DISCLAIMER)
    lines.append("=" * 70)
    return "\n".join(lines)


def _edu_markdown_lines(findings, scope):
    lines = ["# %s 学生数据隐私风险扫描报告" % TOOL_NAME, ""]
    for line in _edu_scope_lines(scope):
        lines.append("- %s" % line)
    lines.append("")
    counts = _summary_counts(findings)
    lines.append("## 汇总")
    lines.append("")
    lines.append("| 级别 | 数量 |")
    lines.append("|---|---|")
    for sev in ("critical", "high", "medium", "low", "info"):
        lines.append("| %s | %d |" % (sev.upper(), counts[sev]))
    lines.append("")
    lines.append("## 风险类别")
    lines.append("")
    lines.append("| 类别 | verdict | 命中 |")
    lines.append("|---|---|---|")
    for v in edu_category_view(findings):
        lines.append("| %s | %s | %d |" % (v["name"], v["verdict"], v["count"]))
    lines.append("")
    lines.append("## 发现")
    lines.append("")
    if not findings:
        lines.append("未发现学生数据隐私风险。")
        lines.append("")
    order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
    for f in sorted(findings, key=lambda x: (order.get(x.severity, 9), x.file_path, x.rule_id)):
        extra = f.extra or {}
        lines.append("### %s · %s" % (f.severity.upper(), f.description))
        lines.append("")
        lines.append("- 规则: %s" % f.rule_id)
        lines.append("- 位置: %s · %s" % (f.file_path, extra.get("location", "")))
        lines.append("- 样例: %s（命中 %d 处）" % (
            extra.get("masked_sample") or "-", extra.get("count", 1)))
        if extra.get("remediation"):
            lines.append("- 建议: %s" % extra["remediation"])
        lines.append("")
    lines.append("## 说明")
    lines.append("")
    lines.append(EDU_DISCLAIMER)
    lines.append("")
    return lines


def edu_report_conflicts(report_path, root):
    """报告不得写入被扫描目录内，也不得与输入文件相同（防自污染）。"""
    try:
        rp = Path(report_path).resolve()
        target = Path(root).resolve()
    except OSError:
        return False
    if target.is_file():
        return rp == target
    try:
        rp.relative_to(target)
        return True
    except ValueError:
        return False


# ── 扫描编排 ────────────────────────────────────────────────────────────────

class SkillScanner:
    """对技能目录跑 13 类检测器。"""

    def __init__(self, ioc_db):
        self.ioc_db = ioc_db
        self.detectors = [
            PatternRuleDetector("DownloadExec", "code_execution"),
            PatternRuleDetector("Obfuscation", "obfuscation"),
            PatternRuleDetector("Persistence", "persistence"),
            PatternRuleDetector("Exfiltration", "data_exfiltration"),
            PatternRuleDetector("CredentialTheft", "credential_theft"),
            PatternRuleDetector("NetworkCall", "network"),
            PatternRuleDetector("PrivilegeEscalation", "privilege_escalation"),
            FilenameDetector(),
            Base64Detector(),
            IOCMatchDetector(ioc_db),
            PostInstallHookDetector(),
            HiddenCharDetector(),
            EntropyDetector(),
        ]

    def scan_skill(self, skill):
        """返回该技能的 [Finding]。"""
        findings = []
        for p in skill["files"]:
            content = read_text(p)
            if not content:
                continue  # 空文件或读取失败，跳过
            for det in self.detectors:
                try:
                    findings.extend(det.scan_file(content, p))
                except Exception as e:  # 单文件异常不阻断整体扫描
                    findings.append(Finding(
                        detector=det.name, severity="info", category="scanner_error",
                        file_path=str(p), line=0,
                        description="检测器异常（已跳过）: %s" % e,
                        confidence=0, rule_id="ERR-001", detail=""))
        return findings


def dedup_findings(findings):
    """同文件+同行+同规则去重。"""
    seen = set()
    out = []
    for f in findings:
        key = (f.file_path, f.line, f.rule_id or f.detector)
        if key in seen:
            continue
        seen.add(key)
        out.append(f)
    return out


def _max_severity(findings):
    worst = "info"
    for f in findings:
        if audit_rules.severity_rank(f.severity) > audit_rules.severity_rank(worst):
            worst = f.severity
    return worst


# ── 系统安全基线（S2，只读）──────────────────────────────────────────────

def _decode_out(data):
    """按优先级尝试解码命令输出：UTF-8 → 系统区域编码 → latin-1（绝不崩）。"""
    if not data:
        return ""
    for enc in ("utf-8", "gbk", "cp1252", "latin-1"):
        try:
            return data.decode(enc)
        except (UnicodeDecodeError, LookupError):
            continue
    return data.decode("utf-8", errors="replace")


def _run(cmd, timeout=30):
    """执行只读命令；返回 (returncode, stdout, stderr)；失败返回 (None,'','')。"""
    kwargs = {}
    if os.name == "nt":
        kwargs["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    try:
        r = subprocess.run(cmd, shell=False, capture_output=True, timeout=timeout, **kwargs)
        out = _decode_out(r.stdout)
        err = _decode_out(r.stderr)
        return r.returncode, out, err
    except (subprocess.TimeoutExpired, OSError) as e:
        return None, "", str(e)


def _sys_finding(check, severity, location, detail, recommendation):
    return Finding(
        detector="SystemBaseline", severity=severity, category="system_baseline",
        file_path=location, line=0, description=check,
        confidence=70, rule_id="SYS-" + check[:16], detail=redact(detail)[:200],
    )

# ── Windows 基线检查 ───────────────────────────────────────────────────────

def _reg_query(key, timeout=20):
    code, out, err = _run(["reg", "query", key], timeout=timeout)
    if code is None or code != 0:
        return []
    entries = []
    current = None
    for line in out.splitlines():
        line = line.rstrip()
        if not line:
            continue
        if line.startswith("HKEY_"):
            current = line.strip()
            continue
        m = re.match(r"^\s+(\S.*?)\s+REG_\S+\s+(.*)$", line)
        if m and current:
            entries.append((current, m.group(1), m.group(2)))
    return entries


def _win_startup_items(findings):
    keys = [
        r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run",
        r"HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce",
        r"HKLM\Software\Microsoft\Windows\CurrentVersion\Run",
        r"HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce",
        r"HKLM\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run",
        r"HKLM\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\RunOnce",
    ]
    _tmpish = re.compile(r"(?i)(temp|\\appdata\\local\\temp|/tmp|%tmp%|%temp%)")
    for key in keys:
        for hive, name, data in _reg_query(key):
            if _tmpish.search(data):
                sev, rec = "high", "启动项指向临时目录，疑似恶意自启动，建议人工核查"
            else:
                sev, rec = "low", "启动项属正常配置但建议周期性核查"
            findings.append(_sys_finding(
                "注册表启动项 %s\\%s" % (hive, name), sev,
                hive, "%s = %s" % (name, data[:200]), rec))


def _win_scheduled_tasks(findings):
    code, out, err = _run(["schtasks", "/query", "/fo", "LIST"])
    if code is None:
        findings.append(_sys_finding("计划任务枚举", "info", "schtasks",
                                     "命令不可用: %s" % err, "跳过该检查"))
        return
    tasks = []
    for line in out.splitlines():
        m = re.match(r"^TaskName:\s+(.+)$", line)
        if m:
            tasks.append(m.group(1).strip())
    user_tasks = [t for t in tasks if not t.lower().startswith("\\microsoft\\")]
    if user_tasks:
        findings.append(_sys_finding(
            "计划任务（非 Microsoft 内置 %d 项）" % len(user_tasks), "medium",
            "schtasks", "; ".join(user_tasks[:20])[:200],
            "非系统内置的计划任务需人工确认来源与触发条件"))
    else:
        findings.append(_sys_finding("计划任务枚举", "info", "schtasks",
                                     "未发现非 Microsoft 内置任务", "无"))


def _win_services(findings):
    code, out, err = _run(["wmic", "service", "get", "name,state,startmode", "/format:csv"])
    if code is None or "Name" not in out:
        # 兜底：sc query 只给状态
        code2, out2, _ = _run(["sc", "query", "type=", "service", "state=", "all"])
        n = out2.count("SERVICE_NAME:")
        findings.append(_sys_finding("服务枚举", "info", "sc query",
                                     "共 %d 个服务（wmic 不可用，仅统计数量）" % n, "无"))
        return
    auto = []
    for line in out.splitlines():
        parts = [p.strip() for p in line.split(",")]
        if len(parts) >= 4 and parts[1] and parts[3] == "Auto":
            auto.append(parts[1])
    findings.append(_sys_finding(
        "自动启动服务 %d 项" % len(auto), "low", "wmic service",
        "; ".join(sorted(auto)[:20])[:200], "自动启动服务需定期核查新增项"))


def _win_firewall(findings):
    code, out, err = _run(["netsh", "advfirewall", "show", "allprofiles", "state"])
    if code is None:
        findings.append(_sys_finding("防火墙状态", "info", "netsh",
                                     "命令不可用: %s" % err, "跳过该检查"))
        return
    # netsh 输出解析：按 Profile 块判断
    profile_off = []
    cur = None
    for line in out.splitlines():
        m = re.match(r"^(\w+)\s+Profile Settings:", line)
        if m:
            cur = m.group(1)
            continue
        m = re.match(r"^\s*State\s+(ON|OFF)\s*$", line)
        if m and cur and m.group(1) == "OFF":
            profile_off.append(cur)
    if profile_off:
        findings.append(_sys_finding(
            "防火墙状态（%s 关闭）" % "/".join(profile_off), "high",
            "netsh advfirewall", "profile off: " + ", ".join(profile_off),
            "建议开启防火墙：netsh advfirewall set allprofiles state on"))
    else:
        findings.append(_sys_finding("防火墙状态", "info", "netsh advfirewall",
                                     "全部配置文件已开启", "无"))


def _win_shares(findings):
    code, out, err = _run(["net", "share"])
    if code is None:
        return
    shares = []
    for line in out.splitlines():
        m = re.match(r"^\s*(\S+)\s+.*", line)
        if not m:
            continue
        name = m.group(1)
        if name.endswith("$") or name in ("Share name", "共享名", "--------", ""):
            continue
        if "命令成功完成" in line or "The command completed" in line:
            continue
        shares.append(name)
    if shares:
        findings.append(_sys_finding(
            "共享目录 %d 项" % len(shares), "medium", "net share",
            "; ".join(shares)[:200], "非默认共享可能暴露文件到局域网，需确认必要性"))
    else:
        findings.append(_sys_finding("共享目录", "info", "net share", "无用户共享", "无"))


def _win_admin_members(findings):
    code, out, err = _run(["net", "localgroup", "administrators"])
    if code is None:
        return
    members = []
    start = False
    for line in out.splitlines():
        if line.strip() == "---":
            start = True
            continue
        if start and line.strip():
            members.append(line.strip())
        if "The command completed" in line:
            break
    findings.append(_sys_finding(
        "管理员组成员 %d 人" % len(members), "low", "net localgroup administrators",
        "; ".join(members)[:200], "管理员组成员应最小化"))


def _win_persistence_points(findings):
    # Userinit
    for hive, name, data in _reg_query(
            r"HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon"):
        if name.lower() == "userinit":
            parts = [p.strip().lower() for p in data.split(",") if p.strip()]
            std = {"userinit.exe", r"c:\windows\system32\userinit.exe"}
            extra_parts = [p for p in parts if p not in std]
            if extra_parts:
                findings.append(_sys_finding(
                    "UserInit 登录脚本被扩展", "high", hive,
                    "Userinit = %s" % data[:200],
                    "Userinit 应仅含 userinit.exe；发现额外条目: %s" % "; ".join(extra_parts)))
    # AppInit_DLLs
    for hive, name, data in _reg_query(
            r"HKLM\Software\Microsoft\Windows NT\CurrentVersion\Windows"):
        if name.lower() == "appinit_dlls" and data.strip():
            findings.append(_sys_finding(
                "AppInit_DLLs 非空（全局 DLL 注入点）", "high", hive,
                "AppInit_DLLs = %s" % data[:200],
                "AppInit_DLLs 应保持为空；非空多为恶意持久化"))
    # 环境变量持久化点（只报告键名，值脱敏）
    for env_key in (r"HKCU\Environment",
                    r"HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment"):
        entries = _reg_query(env_key)
        if entries:
            names = "; ".join(n for _, n, _ in entries)
            findings.append(_sys_finding(
                "环境变量持久化点 %s" % env_key, "low", env_key,
                "键名: %s（值已脱敏）" % names[:200],
                "环境变量可被用于持久化，注意异常键名"))


def _win_browser_cred(findings):
    appdata = os.environ.get("LOCALAPPDATA", "")
    apdata = os.environ.get("APPDATA", "")
    marks = [
        ("Chrome 登录数据", Path(appdata) / "Google" / "Chrome" / "User Data" / "Default" / "Login Data"),
        ("Edge 登录数据", Path(appdata) / "Microsoft" / "Edge" / "User Data" / "Default" / "Login Data"),
        ("Firefox 登录数据", Path(apdata) / "Mozilla" / "Firefox" / "Profiles"),
    ]
    present = []
    for label, p in marks:
        try:
            ok = p.exists()
        except OSError:
            ok = False
        if ok:
            present.append(label)
    if present:
        findings.append(_sys_finding(
            "浏览器凭据存储位置存在", "info", "; ".join(str(p) for _, p in marks),
            "存在: %s（仅提示位置，不扫描内容）" % ", ".join(present),
            "浏览器保存的密码与登录态应受系统账户保护"))


def run_windows_baseline():
    findings = []
    _win_startup_items(findings)
    _win_scheduled_tasks(findings)
    _win_services(findings)
    _win_firewall(findings)
    _win_shares(findings)
    _win_admin_members(findings)
    _win_persistence_points(findings)
    _win_browser_cred(findings)
    return findings

# ── Linux 基线检查 ─────────────────────────────────────────────────────────

def _linux_suid_sgid(findings):
    code, out, err = _run(
        ["find", "/usr", "/bin", "/sbin", "/opt", "/home", "-xdev",
         "-type", "f", "-perm", "/6000", "-print"], timeout=60)
    if code is None:
        findings.append(_sys_finding("SUID/SGID 扫描", "info", "find",
                                     "命令不可用/超时: %s" % err, "跳过该检查"))
        return
    files = [l for l in out.splitlines() if l.strip()]
    suspicious = [f for f in files if re.search(r"(?i)(/tmp/|/home/|/dev/shm)", f)]
    if suspicious:
        findings.append(_sys_finding(
            "可疑 SUID/SGID 文件 %d 个" % len(suspicious), "high", "find -perm /6000",
            "; ".join(suspicious[:20])[:200], "可写目录下的 SUID/SGID 文件是提权风险"))
    elif files:
        findings.append(_sys_finding(
            "SUID/SGID 文件 %d 个（常规位置）" % len(files), "low", "find -perm /6000",
            "; ".join(files[:20])[:200], "常规 SUID 文件属正常，需关注新增项"))


def _linux_world_writable(findings):
    code, out, err = _run(
        ["find", "/usr", "/etc", "/opt", "/home", "-xdev",
         "-type", "d", "-perm", "-0002", "-print"], timeout=60)
    if code is None:
        return
    dirs = [l for l in out.splitlines() if l.strip()]
    if dirs:
        findings.append(_sys_finding(
            "全局可写目录 %d 个" % len(dirs), "medium", "find -perm -0002",
            "; ".join(dirs[:20])[:200], "全局可写目录可被低权限用户劫持"))


def _linux_startup(findings):
    # systemd enabled units
    code, out, err = _run(["systemctl", "list-unit-files", "--type=service",
                           "--state=enabled", "--no-legend"])
    if code is not None and code == 0:
        units = [l.split()[0] for l in out.splitlines() if l.strip()]
        findings.append(_sys_finding(
            "systemd 启用服务 %d 项" % len(units), "low", "systemctl list-unit-files",
            "; ".join(sorted(units)[:20])[:200], "启用服务需定期核查新增项"))
    # cron
    for path in ("/etc/cron.d", "/etc/cron.daily", "/etc/cron.hourly"):
        p = Path(path)
        if p.is_dir():
            try:
                items = [x.name for x in p.iterdir() if x.is_file()]
            except OSError:
                items = []
            if items:
                findings.append(_sys_finding(
                    "cron 配置目录 %s（%d 项）" % (path, len(items)), "medium", path,
                    "; ".join(items[:20])[:200], "cron 脚本是常见持久化位置"))


def _linux_ssh(findings):
    sshd = Path("/etc/ssh/sshd_config")
    if sshd.is_file():
        try:
            content = sshd.read_text(encoding="utf-8", errors="replace")
        except OSError:
            content = ""
        for pat, msg, sev in (
            (r"(?i)^\s*PermitRootLogin\s+yes\b", "SSH 允许 root 登录", "high"),
            (r"(?i)^\s*PasswordAuthentication\s+yes\b", "SSH 允许密码认证", "medium"),
        ):
            if re.search(pat, content, re.M):
                findings.append(_sys_finding(msg, sev, str(sshd), msg,
                                             "建议禁用：PermitRootLogin no / 密钥认证"))
    ssh_cfg = Path.home() / ".ssh" / "config"
    if ssh_cfg.is_file():
        try:
            content = ssh_cfg.read_text(encoding="utf-8", errors="replace")
        except OSError:
            content = ""
        if re.search(r"(?i)ProxyCommand\s+\S+", content):
            findings.append(_sys_finding(
                "SSH config 含 ProxyCommand", "medium", str(ssh_cfg),
                "ProxyCommand 存在", "ProxyCommand 可被用于隐蔽外联，需确认"))


def _linux_open_ports(findings):
    code, out, err = _run(["ss", "-tln"])
    listeners = []
    if code is not None and code == 0:
        for line in out.splitlines()[1:]:
            parts = line.split()
            if len(parts) >= 4 and "LISTEN" in parts[0]:
                listeners.append(parts[3])
    else:
        # 兜底 /proc/net/tcp
        try:
            raw = Path("/proc/net/tcp").read_text(encoding="utf-8", errors="replace")
        except OSError:
            raw = ""
        for line in raw.splitlines()[1:]:
            parts = line.split()
            if len(parts) >= 4 and parts[3] == "0A":
                addr = parts[1]
                try:
                    ip, port = addr.rsplit(":", 1)
                    ip = ".".join(str(int(ip[i:i+2], 16)) for i in (6, 4, 2, 0))
                    listeners.append("%s:%d" % (ip, int(port, 16)))
                except Exception:
                    pass
    wild = [l for l in listeners if l.startswith("0.0.0.0:") or l.startswith("[::]:")]
    if wild:
        findings.append(_sys_finding(
            "对外监听端口 %d 个" % len(wild), "medium", "ss -tln",
            "; ".join(wild[:20])[:200], "监听 0.0.0.0 的端口对局域网/公网可见"))
    else:
        findings.append(_sys_finding("开放端口", "info", "ss -tln",
                                     "未发现对外（非回环）监听端口", "无"))


def _linux_crontab(findings):
    code, out, err = _run(["crontab", "-l"])
    if code is not None and out.strip():
        findings.append(_sys_finding(
            "用户 crontab 存在 %d 行" % len(out.strip().splitlines()), "medium",
            "crontab -l", out.strip()[:200], "用户 crontab 可被用于持久化，需确认"))


def _linux_read_lines(path):
    """读取文本配置文件；不存在/不可读返回 None（不阻断基线扫描）。"""
    p = Path(path)
    if not p.is_file():
        return None
    try:
        return p.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None


def _linux_cis_empty_passwd(findings):
    """CIS 1.1.5 / 5.4.x：/etc/shadow 中密码字段为空 = 无需密码即可登录。"""
    lines = _linux_read_lines("/etc/shadow")
    if lines is None:
        findings.append(_sys_finding(
            "CIS：/etc/shadow 不可读", "info", "/etc/shadow",
            "文件不存在或当前用户无权限", "以 root 运行扫描以读取影子文件"))
        return
    users = []
    for line in lines:
        if not line or line.startswith("#"):
            continue
        if line.startswith("+"):
            continue  # 服务账号（如 + ::: 占位）
        m = re.match(r"^([^:]+):([^:]*):", line)
        if not m:
            continue
        name, pwd = m.group(1), m.group(2)
        # 密码字段为空且不是锁定（!/*）形态 = 空密码账号
        if pwd == "":
            users.append(name)
    if users:
        findings.append(_sys_finding(
            "CIS：空密码账号 %d 个" % len(users), "high", "/etc/shadow",
            "账号: " + "; ".join(users[:20])[:200],
            "空密码账号可被直接登录，立即设置密码或锁定账号"))


def _linux_cis_sudoers(findings):
    """CIS 5.x：sudoers 中 NOPASSWD = 无密码提权（sudoers.d 一并检查）。"""
    # 候选文件固定列：/etc/sudoers 与 /etc/sudoers.d 下全部文件。
    # 存在性交给 _linux_read_lines（文件不存在返回 None 即跳过），
    # 便于跨平台单测（mock _linux_read_lines）且不依赖真实目录状态。
    paths = ["/etc/sudoers", "/etc/sudoers.d"]
    targets = []
    for path in paths:
        p = Path(path)
        if p.is_dir():
            try:
                targets.extend(str(x) for x in p.iterdir() if x.is_file())
            except OSError:
                targets.append(path)
        else:
            targets.append(path)
    hits = []
    for path in targets:
        lines = _linux_read_lines(path)
        if lines is None:
            continue
        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if re.search(r"(?i)NOPASSWD", stripped):
                # !authenticate 也会以 NOPASSWD 形式出现，同样弱化认证
                hits.append("%s: %s" % (path, stripped[:120]))
    if hits:
        findings.append(_sys_finding(
            "CIS：sudo 存在 NOPASSWD 条目 %d 处" % len(hits), "medium",
            "/etc/sudoers", "; ".join(hits[:20])[:200],
            "NOPASSWD 允许免密提权，建议改为 requiretty + 密码认证"))


_CIS_SYSCTL = [
    # (key, 安全值, 描述, 级别, 建议)
    ("fs.suid_dumpable", "0", "允许对 SUID 程序产生 core dump", "high",
     "设为 0：sysctl -w fs.suid_dumpable=0"),
    ("kernel.randomize_va_space", "2", "ASLR 未完全启用（应=2）", "medium",
     "设为 2：sysctl -w kernel.randomize_va_space=2"),
    ("net.ipv4.conf.all.accept_redirects", "0", "接受 ICMP 重定向", "medium",
     "设为 0：sysctl -w net.ipv4.conf.all.accept_redirects=0"),
    ("net.ipv4.conf.all.send_redirects", "0", "发送 ICMP 重定向", "low",
     "设为 0：sysctl -w net.ipv4.conf.all.send_redirects=0"),
    ("net.ipv4.ip_forward", "0", "主机启用了 IP 转发（路由行为）", "low",
     "非路由器应设为 0：sysctl -w net.ipv4.ip_forward=0"),
]


def _linux_sysctl_values(keys):
    """读取 sysctl 键值（只读）。返回 {key: value}；sysctl 缺失/键不存在记 NA。"""
    code, out, err = _run(["sysctl"] + list(keys), timeout=20)
    if code is None or code != 0:
        return {}
    result = {}
    for line in out.splitlines():
        m = re.match(r"^([^=\s]+)\s*=\s*(\S+)", line.strip())
        if m:
            result[m.group(1)] = m.group(2)
    return result


def _linux_cis_sysctl(findings):
    """CIS 1.5 / 3.x：内核参数加固检查（fs.suid_dumpable / ASLR / ICMP 重定向等）。"""
    keys = [t[0] for t in _CIS_SYSCTL]
    values = _linux_sysctl_values(keys)
    if not values:
        findings.append(_sys_finding(
            "CIS：sysctl 不可用", "info", "sysctl",
            "命令缺失或执行失败，跳过内核参数检查", "安装 procps 或确认 sysctl 可用"))
        return
    for key, safe, desc, sev, rec in _CIS_SYSCTL:
        val = values.get(key)
        if val is None:
            continue  # 键不存在，跳过
        if val != safe:
            findings.append(_sys_finding(
                "CIS：%s=%s" % (key, val), sev, "sysctl " + key,
                desc, rec))


def _linux_cis_login_history(findings):
    """CIS 6.2.x：登录历史检查——lastb 失败登录次数、last 异常来源提示。"""
    code, out, err = _run(["lastb", "-n", "50"], timeout=20)
    if code is not None and out.strip():
        lines = [l for l in out.strip().splitlines() if l.strip()]
        findings.append(_sys_finding(
            "CIS：失败登录记录 %d 条" % len(lines), "medium", "lastb -n 50",
            "最近失败登录 %d 条，含用户名与来源 IP" % len(lines),
            "大量失败登录 = 暴力破解迹象，核查来源并考虑 fail2ban"))
    else:
        findings.append(_sys_finding(
            "CIS：失败登录记录", "info", "lastb",
            "无失败登录记录（或 lastb 不可用/无权限）", "无"))
    code2, out2, err2 = _run(["last", "-n", "10"], timeout=20)
    if code2 is not None and out2.strip():
        lines = [l for l in out2.strip().splitlines() if l.strip()]
        findings.append(_sys_finding(
            "CIS：近期登录 %d 条" % len(lines), "low", "last -n 10",
            "最近登录 %d 条，含用户名与来源" % len(lines),
            "核查是否有陌生账号/陌生来源登录"))


def _linux_cis(findings):
    """CIS 合规基线（只读）：空密码 / sudo NOPASSWD / 内核参数 / 登录历史。"""
    _linux_cis_empty_passwd(findings)
    _linux_cis_sudoers(findings)
    _linux_cis_sysctl(findings)
    _linux_cis_login_history(findings)


def _linux_path_hijack(findings):
    path = os.environ.get("PATH", "")
    writable = [p for p in path.split(os.pathsep)
                if p in (".", "~", "/tmp") or p.startswith(("/tmp", "./"))]
    if writable:
        findings.append(_sys_finding(
            "PATH 含可写目录", "high", "PATH",
            "可写目录: " + "; ".join(writable)[:200],
            "PATH 前部含可写目录可导致命令劫持"))


def run_linux_baseline():
    findings = []
    _linux_suid_sgid(findings)
    _linux_world_writable(findings)
    _linux_startup(findings)
    _linux_ssh(findings)
    _linux_open_ports(findings)
    _linux_crontab(findings)
    _linux_path_hijack(findings)
    _linux_cis(findings)
    return findings

# ── 报告输出 ────────────────────────────────────────────────────────────────

# 威胁捕获模型视图（2026-08-30 增强：8 检测点 + 13 行为项）
_SEV_WEIGHT = {"critical": 40, "high": 20, "medium": 8, "low": 1, "info": 0}
_SEV_CAPS = {"critical": 2, "high": 4, "medium": 6, "low": 10, "info": 0}


def _health_score(findings):
    """安全健康度评分 0-100（100 起扣 + 封顶；低危密集不扣光）。"""
    counts = {}
    for f in findings:
        counts[f.severity] = counts.get(f.severity, 0) + 1
    score = 100
    for sev, w in _SEV_WEIGHT.items():
        score -= w * min(counts.get(sev, 0), _SEV_CAPS[sev])
    return max(0, int(round(score)))


def _taxonomy_view(findings):
    """8 类威胁图谱：每类 verdict（danger/suspicious/safe/n/a）。"""
    hits = {}
    for f in findings:
        key = audit_rules.DETECTOR_TO_TAXONOMY.get(f.detector, "other")
        hits.setdefault(key, []).append(f)
    out = []
    for key in audit_rules.TAXONOMY_ORDER:
        items = hits.get(key, [])
        name = audit_rules.THREAT_TAXONOMY.get(key, key)
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
    """13 行为项：observed / none。"""
    observed = {}
    for f in findings:
        for b in audit_rules.DETECTOR_TO_BEHAVIORS.get(f.detector, ()):
            observed[b] = observed.get(b, 0) + 1
    return [{"behavior": b, "observed": observed.get(b, 0)}
            for b in audit_rules.BEHAVIORS]


def _sev_label(sev):
    return "[%s]" % sev.upper()


def format_text_report(findings, scope, use_color=True):
    lines = []
    lines.append("=" * 70)
    lines.append("%s %s 安全扫描报告" % (TOOL_NAME, VERSION))
    lines.append("=" * 70)
    lines.append("目标: %s  平台: %s" % (scope.get("target", "skill"), scope.get("platform", "auto")))
    lines.append("时间: %s" % scope.get("scanned_at", ""))
    if scope.get("skills_scanned") is not None:
        lines.append("范围: 技能 %d 个 / 文件 %d 个" % (
            scope["skills_scanned"], scope["files_scanned"]))
    if scope.get("note"):
        lines.append("说明: %s" % scope["note"])
    lines.append("")
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for f in findings:
        counts[f.severity] = counts.get(f.severity, 0) + 1
    lines.append("汇总: CRITICAL %d | HIGH %d | MEDIUM %d | LOW %d | INFO %d" % (
        counts["critical"], counts["high"], counts["medium"],
        counts["low"], counts["info"]))
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
    if not findings:
        lines.append("未发现安全问题。")
        lines.append("")
        lines.append("=" * 70)
        return "\n".join(lines)

    # 按严重级降序、文件分组
    order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
    for f in sorted(findings, key=lambda x: (order.get(x.severity, 9), x.file_path, x.line)):
        lines.append("%s %s" % (_sev_label(f.severity), f.detector))
        if f.rule_id:
            lines.append("  规则: %s  置信度: %d%%" % (f.rule_id, f.confidence))
        loc = f.file_path
        if f.line:
            loc = "%s:%d" % (loc, f.line)
        lines.append("  位置: %s" % loc)
        lines.append("  描述: %s" % f.description)
        if f.detail:
            lines.append("  证据: %s" % f.detail[:160])
        lines.append("")
    lines.append("=" * 70)
    return "\n".join(lines)


def build_json_report(findings, scope):
    data = {
        "tool": TOOL_NAME,
        "version": VERSION,
        "target": scope.get("target", "skill"),
        "platform": scope.get("platform", "auto"),
        "scanned_at": scope.get("scanned_at", ""),
        "scope": {k: v for k, v in scope.items() if k not in ("target", "platform", "scanned_at")},
        "summary": _summary_counts(findings),
        "findings": [f.to_dict() for f in findings],
    }
    if scope.get("target") == "edu":
        data["edu"] = {
            "categories": edu_category_view(findings),
            "note": EDU_DISCLAIMER,
        }
    else:
        data["threat"] = {
            "health_score": _health_score(findings),
            "taxonomy": _taxonomy_view(findings),
            "behaviors": _behavior_view(findings),
        }
    return data


def _summary_counts(findings):
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for f in findings:
        counts[f.severity] = counts.get(f.severity, 0) + 1
    return counts


def _skill_markdown_lines(findings, scope):
    lines = []
    lines.append("# %s 安全扫描报告" % TOOL_NAME)
    lines.append("")
    lines.append("- 版本: %s" % VERSION)
    lines.append("- 目标: %s" % scope.get("target", "skill"))
    lines.append("- 平台: %s" % scope.get("platform", "auto"))
    lines.append("- 时间: %s" % scope.get("scanned_at", ""))
    if scope.get("skills_scanned") is not None:
        lines.append("- 范围: 技能 %d 个 / 文件 %d 个" % (
            scope["skills_scanned"], scope["files_scanned"]))
    lines.append("")
    c = _summary_counts(findings)
    lines.append("## 汇总")
    lines.append("")
    lines.append("| 级别 | 数量 |")
    lines.append("|---|---|")
    for sev in ("critical", "high", "medium", "low", "info"):
        lines.append("| %s | %d |" % (sev.upper(), c[sev]))
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
            lines.append("### %s · %s" % (f.severity.upper(), f.detector))
            lines.append("")
            lines.append("- 规则: %s（置信度 %d%%）" % (f.rule_id or "-", f.confidence))
            lines.append("- 位置: %s%s" % (f.file_path, ":%d" % f.line if f.line else ""))
            lines.append("- 描述: %s" % f.description)
            if f.detail:
                lines.append("- 证据: %s" % f.detail[:160])
            lines.append("")
    else:
        lines.append("未发现安全问题。")
    return lines


def write_markdown_report(path, findings, scope):
    """写 Markdown 报告：edu 模式用教育版模板，其余保持原模板。"""
    if scope.get("target") == "edu":
        lines = _edu_markdown_lines(findings, scope)
    else:
        lines = _skill_markdown_lines(findings, scope)
    try:
        with open(str(path), "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(lines))
        return True
    except OSError as e:
        print("[ERROR] 报告写入失败: %s" % e, file=sys.stderr)
        return False


# ── 主入口 ──────────────────────────────────────────────────────────────────

class _AuditParser(argparse.ArgumentParser):
    """参数错误统一 exit 4（扫描器错误），与结果 exit code 语义区分。"""

    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(4, "%s: error: %s\n" % (self.prog, message))


def parse_args(argv=None):
    ap = _AuditParser(
        prog=TOOL_NAME,
        description="YottaMeta 元安 —— 技能恶意模式 / 系统安全基线 / 学生数据隐私风险扫描（只读）",
    )
    ap.add_argument("--target", choices=["skill", "system", "edu"], default="skill",
                    help="扫描目标：skill（默认，技能恶意模式）/ system（系统安全基线）/ "
                         "edu（学生数据隐私风险，必须显式 --path）")
    ap.add_argument("--path", "-p", metavar="PATH",
                    help="扫描单个目录或文件（技能模式：视为一个技能；edu 模式：必填；系统模式忽略）")
    ap.add_argument("--edu-rules", metavar="FILE",
                    help="edu 模式自定义规则包 JSON（默认 scripts/student_data_rules.json）")
    ap.add_argument("--platform", choices=["auto", "windows", "linux"], default="auto",
                    help="系统扫描平台（默认 auto=当前系统）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--severity", choices=["low", "medium", "high", "critical"],
                    help="最低报告级别（过滤更低级别）")
    ap.add_argument("--report", metavar="FILE", help="同时生成 Markdown 报告文件")
    ap.add_argument("--ioc-db", metavar="FILE", help="自定义 IOC 数据库 JSON")
    ap.add_argument("--no-color", action="store_true", help="禁用颜色输出")
    ap.add_argument("--include-self", action="store_true",
                    help="自动发现时包含元安自身（默认跳过，避免自扫噪声）")
    return ap.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    scanned_at = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")

    if args.target == "system":
        platform = args.platform
        if platform == "auto":
            platform = "windows" if os.name == "nt" else "linux"
        if platform == "windows" and os.name != "nt":
            print("[WARN] 当前系统不是 Windows，windows 基线命令将不可用（预期）", file=sys.stderr)
        if platform == "linux" and os.name == "nt":
            print("[WARN] 当前系统不是 Linux，linux 基线命令将不可用（预期）", file=sys.stderr)
        findings = run_windows_baseline() if platform == "windows" else run_linux_baseline()
        scope = {"target": "system", "platform": platform, "scanned_at": scanned_at}
        return _emit(args, findings, scope)

    if args.target == "edu":
        if not args.path:
            print("[ERROR] edu 模式必须显式指定 --path（不做自动发现，避免扫描无关或他人目录）",
                  file=sys.stderr)
            return 4
        root = Path(args.path)
        if not root.exists():
            print("[ERROR] 路径不存在: %s" % args.path, file=sys.stderr)
            return 4
        try:
            pack = load_edu_rule_pack(args.edu_rules)
        except RulePackError as e:
            print("[ERROR] %s" % e, file=sys.stderr)
            return 4
        if args.report and edu_report_conflicts(args.report, root):
            print("[ERROR] 报告输出路径不得位于被扫描目录内，也不得与输入文件相同",
                  file=sys.stderr)
            return 4
        findings, scope = run_edu_scan(root, pack)
        scope["scanned_at"] = scanned_at
        min_rank = audit_rules.severity_rank(args.severity) if args.severity else 0
        filtered = [f for f in findings
                    if audit_rules.severity_rank(f.severity) >= min_rank]
        return _emit(args, filtered, scope)

    # skill 模式
    ioc_db = IOCDatabase(args.ioc_db)
    skills = discover_skills(explicit_path=args.path, include_self=args.include_self)
    if not skills:
        print("[INFO] 未发现技能目录%s。" % (
            "（指定路径不存在或为空）" if args.path else "（可先安装技能或用 --path 指定）"),
            file=sys.stderr)
        scope = {"target": "skill", "platform": "auto", "scanned_at": scanned_at,
                 "skills_scanned": 0, "files_scanned": 0}
        if ioc_db.warning:
            print("[WARN] %s" % ioc_db.warning, file=sys.stderr)
        if args.report:
            write_markdown_report(args.report, [], scope)
        return 0

    scanner = SkillScanner(ioc_db)
    all_findings = []
    files_scanned = 0
    for skill in skills:
        files_scanned += len(skill["files"])
        all_findings.extend(scanner.scan_skill(skill))

    all_findings = dedup_findings(all_findings)

    min_rank = 0
    if args.severity:
        min_rank = audit_rules.severity_rank(args.severity)
    filtered = [f for f in all_findings
                if audit_rules.severity_rank(f.severity) >= min_rank]

    scope = {"target": "skill", "platform": "auto", "scanned_at": scanned_at,
             "skills_scanned": len(skills), "files_scanned": files_scanned}
    if ioc_db.warning:
        scope["note"] = ioc_db.warning
    if args.path:
        scope["path"] = str(Path(args.path).resolve())

    rc = _emit(args, filtered, scope)
    return rc


def _emit(args, findings, scope):
    """输出报告并返回 exit code。"""
    if args.report:
        write_markdown_report(args.report, findings, scope)
    if args.json:
        print(json.dumps(build_json_report(findings, scope), indent=2, ensure_ascii=False))
    elif scope.get("target") == "edu":
        print(format_edu_text_report(findings, scope))
    else:
        use_color = not args.no_color and sys.stdout.isatty()
        print(format_text_report(findings, scope, use_color=use_color))
    worst = _max_severity(findings)
    return audit_rules.severity_value(worst)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except KeyboardInterrupt:
        sys.exit(4)
    except Exception as e:
        print("[FATAL] 扫描器异常: %s" % e, file=sys.stderr)
        sys.exit(4)
