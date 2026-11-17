#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""yotta_verify.py — YottaMeta 元信（yotta-verify）装前安全扫描器。

对要安装的 Agent 技能 / npm 包做确定性装前安全校验：
  scan    装前安全扫描（prompt injection + 危险模式 + SKILL.md 完整性 + 权限需求）
  badge   audited 徽章生成（本地 SVG + shields.io URL）
  report  验证报告（Markdown / JSON / text）
  gate    CI 闸门（--max-severity，超出即失败）

设计原则：
- 纯 Python 3.8+ 标准库，零依赖；Windows/Linux/macOS 通用。
- 只读静态检测：绝不执行被测代码、不联网、不装包、不修复。
- 规则复用：危险模式 = 元安 audit_rules 同步副本（verify_rules.AUDIT_PATTERN_RULES）；
  prompt injection = 元信独有规则（verify_rules.PIJ_PATTERN_RULES）。
- 检测器可自扫（dogfooding）：规则表自身为签名数据自动跳过。

exit code 语义（与元安/元审一致）：
  0 = SAFE TO INSTALL（干净 / 仅有 low/info）
  1 = REVIEW REQUIRED（存在 medium）
  2 = INSTALL WITH CAUTION（存在 high）
  3 = DO NOT INSTALL（存在 critical）
  4 = 用法错误 / 致命异常

用法示例：
  python3 yotta_verify.py scan ./some-skill
  python3 yotta_verify.py scan ./some-skill --json --report report.md --badge
  python3 yotta_verify.py badge ./some-skill --tests 49 --version 0.1.1
  python3 yotta_verify.py gate ./some-skill --max-severity medium
"""
import argparse
import base64
import hashlib
import json
import re
import sys
import tempfile
import tarfile
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
import verify_rules  # noqa: E402
import threat_engine  # noqa: E402

VERSION = "0.4.7"
TOOL_NAME = "yotta-verify"
CN_NAME = "元信"

SKIP_DIRS = {
    "venv", "node_modules", ".git", "__pycache__", ".mypy_cache", ".tox",
    "dist", "build", ".egg-info", ".venv", ".idea", ".vscode", ".tmp",
}
TEXT_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".mjs", ".cjs", ".sh", ".bash", ".zsh",
    ".md", ".txt", ".yaml", ".yml", ".json", ".toml", ".ini", ".cfg",
    ".rb", ".go", ".rs", ".java", ".c", ".cpp", ".h", ".hpp",
    ".html", ".css", ".xml", ".svg", ".plist", ".ps1", ".bat", ".cmd",
    ".env", ".conf", ".properties", ".gradle",
}
DOTFILE_NAMES = {
    ".env", ".env.example", ".netrc", ".pgpass", ".bashrc", ".zshrc",
    ".profile", ".bash_profile", ".npmrc", ".gitconfig",
}
MAX_FILE_SIZE = 1_000_000
MAX_LINE_LEN = verify_rules.MAX_LINE_LEN
MAX_FILES = 2000
# v0.4.4：不可静态分析的可执行 / 二进制载荷不再静默跳过（fail-closed）。
# 旧行为只对 TEXT_EXTENSIONS 做内容分析，`.exe` / `.dll` / `.jar` / 无扩展名二进制
# 会被直接忽略——攻击方可以把载荷放进这些文件逃避扫描。现在按扩展名 + 魔数识别，
# 命中即出 STR-009（medium），扫描结论至少为「需复核」。
OPAQUE_EXTENSIONS = {
    ".exe", ".dll", ".sys", ".com", ".msi", ".scr", ".cab", ".cpl",
    ".so", ".dylib", ".bin", ".o", ".a",
    ".jar", ".class", ".apk", ".dex", ".wasm", ".node",
}
OPAQUE_MAGIC = (b"\x7fELF", b"MZ", b"\xca\xfe\xba\xbe", b"\xcf\xfa\xed\xfe")
# tarball 解包上限（防资源耗尽）
MAX_TARBALL_MEMBERS = 2000
MAX_TARBALL_MEMBER_BYTES = 50 * 1024 * 1024
MAX_TARBALL_TOTAL_BYTES = 200 * 1024 * 1024
# 签名数据文件：规则表是扫描器自身与家族检测技能的签名数据库，不是被测技能行为。
# v0.3.2 收紧（旧行为 = 按文件名全局豁免，`scripts/<同名>.py` 可被随意伪造以逃避扫描）：
#   ① 相对路径必须恰为 scripts/<规则表名>.py；
#   ② 文件 SHA-256（CRLF 归一化）必须命中「已发布规则表摘要表」。
# 任一条不满足 → 正常扫描（fail-closed），杜绝「改名即豁免」与「放标记文件即降级」。
SIGNATURE_DATA_FILES = {"verify_rules.py", "audit_rules.py", "vetter_rules.py", "hardening_rules.py"}
SIGNATURE_DATA_DIGESTS = {
    "verify_rules.py": {"f060ec1e9d339865db577c074b51b49841a44657f3bea863dbc72ced2d5eed83"},
    "vetter_rules.py": {"ed0959784c3afc09562686aaac8a0d17679987dbd49a06bedccee2d05f17424c"},
    "audit_rules.py": {"231e87341816a48fa47573cd4e7a9ecdeb1535c04cab04a4d569443c9db54a8d"},
    "hardening_rules.py": {"a5d6a14323633ba59f0005e655ec3b0acf5be300db8889fd3fb875cc8c2d9fba"},
    "guardian_rules.py": {"d83674b9dc41c8f6290964b9d6339dce3840f9c0df564856513bc7f1a9bd94d8"},
}


def _sha256_normalized(path):
    """CRLF 归一化后的 SHA-256（跨 Windows / Linux 检出结果一致）。"""
    try:
        data = path.read_bytes().replace(b"\r\n", b"\n")
    except OSError:
        return None
    return hashlib.sha256(data).hexdigest()


def is_signature_data(rel, path):
    """是否为「已发布」的家族规则表：路径 + 内容摘要双绑定。"""
    known = SIGNATURE_DATA_DIGESTS.get(path.name)
    if not known:
        return False
    parts = str(rel).replace("\\", "/").split("/")
    if len(parts) != 2 or parts[0] != "scripts":
        return False
    digest = _sha256_normalized(path)
    return bool(digest) and digest in known


def has_published_signature_data(root):
    """目标包是否持有已发布签名数据（用于测试夹具跳过与文档降级判定）。"""
    for name in SIGNATURE_DATA_DIGESTS:
        p = Path(root) / "scripts" / name
        if p.is_file() and is_signature_data("scripts/" + name, p):
            return True
    return False

# ── 严重级 / verdict ───────────────────────────────────────────────────────
_SEVERITY_VALUE = verify_rules.SEVERITY_VALUE
_SEVERITY_ORDER = verify_rules.SEVERITY_ORDER
VERDICT_SAFE = "SAFE TO INSTALL"
VERDICT_CAUTION = "INSTALL WITH CAUTION"
VERDICT_REVIEW = "REVIEW REQUIRED"
VERDICT_BLOCK = "DO NOT INSTALL"
VERDICT_BY_SEVERITY = {
    "critical": VERDICT_BLOCK,
    "high": VERDICT_CAUTION,
    "medium": VERDICT_REVIEW,
    "low": VERDICT_SAFE,
    "info": VERDICT_SAFE,
}
VERDICT_EXIT = {
    VERDICT_SAFE: 0,
    VERDICT_REVIEW: 1,
    VERDICT_CAUTION: 2,
    VERDICT_BLOCK: 3,
}
BADGE_COLORS = {
    VERDICT_SAFE: "4c1",
    VERDICT_REVIEW: "fe7d37",
    VERDICT_CAUTION: "dfb317",
    VERDICT_BLOCK: "e05d44",
}

# ── Finding ─────────────────────────────────────────────────────────────────

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
        return {
            "detector": self.detector,
            "severity": self.severity,
            "category": self.category,
            "file": self.file_path,
            "line": self.line,
            "description": self.description,
            "confidence": self.confidence,
            "rule_id": self.rule_id,
        }


# ── 文件收集 ───────────────────────────────────────────────────────────────

def is_text_file(name):
    p = name.lower()
    if p in DOTFILE_NAMES:
        return True
    return Path(p).suffix in TEXT_EXTENSIONS


def walk_files(root, base="", trusted_tests=None, scan_root=None):
    """递归收集可扫描文本文件（跳过 SKIP_DIRS / 已发布签名数据 / 超限）。

    trusted_tests 只在「目标包持有已发布签名数据」时为真——此时 `test_*.py`
    视为自家测试夹具跳过；第三方包的同名文件照常扫描（v0.3.2 起）。
    """
    out = []
    if scan_root is None:
        scan_root = root
        trusted_tests = has_published_signature_data(scan_root)
    try:
        entries = sorted(root.iterdir())
    except OSError:
        return out
    for entry in entries:
        if entry.name in SKIP_DIRS:
            continue
        rel = entry.name if not base else base + "/" + entry.name
        if entry.is_dir():
            out.extend(walk_files(entry, rel, trusted_tests, scan_root))
        elif entry.is_file():
            try:
                size = entry.stat().st_size
            except OSError:
                continue
            if size > MAX_FILE_SIZE:
                continue
            # 已发布规则表（路径 + 摘要绑定）不是被测技能行为，跳过
            if is_signature_data(rel, entry):
                continue
            # 自家包的测试夹具（含构造样例）跳过；第三方包不豁免
            if trusted_tests and entry.name.startswith("test_") and entry.name.endswith(".py"):
                continue
            if is_text_file(entry.name):
                out.append((entry, rel))
            if len(out) >= MAX_FILES:
                break
    return out


def _read_magic(path, size=4):
    try:
        with open(str(path), "rb") as fh:
            return fh.read(size)
    except OSError:
        return b""


def find_opaque_files(root):
    """列出无法静态分析、但带可执行 / 二进制特征的文件（v0.4.4，fail-closed）。"""
    out = []
    if root.is_file():
        candidates = [(root, root.name)]
    else:
        candidates = []
        stack = [root]
        while stack:
            cur = stack.pop()
            try:
                entries = sorted(cur.iterdir())
            except OSError:
                continue
            for entry in entries:
                if entry.name in SKIP_DIRS:
                    continue
                if entry.is_dir():
                    stack.append(entry)
                elif entry.is_file():
                    rel = str(entry.relative_to(root)).replace("\\", "/")
                    candidates.append((entry, rel))
    for path, rel in candidates:
        name = path.name.lower()
        if name in DOTFILE_NAMES or Path(name).suffix in TEXT_EXTENSIONS:
            continue
        suffix = Path(name).suffix
        opaque = suffix in OPAQUE_EXTENSIONS
        if not opaque:
            magic = _read_magic(path)
            opaque = any(magic.startswith(sig) for sig in OPAQUE_MAGIC)
        if not opaque:
            continue
        try:
            size = path.stat().st_size
        except OSError:
            size = 0
        out.append((rel, size))
        if len(out) >= 50:
            break
    return out


def read_lines(path):
    """读取文本文件行列表（容错编码；超长行截断）。"""
    try:
        raw = path.read_bytes()
    except OSError:
        return []
    for enc in ("utf-8", "utf-8-sig", "gb18030", "latin-1"):
        try:
            text = raw.decode(enc)
            break
        except (UnicodeDecodeError, ValueError):
            continue
    else:
        text = raw.decode("utf-8", errors="replace")
    lines = text.split("\n")
    out = []
    for line in lines:
        if len(line) > MAX_LINE_LEN:
            out.append(line[:MAX_LINE_LEN])
        else:
            out.append(line)
    return out


def find_skill_md(root):
    """在根下找 SKILL.md（优先根目录，其次任意一层）。"""
    p = root / "SKILL.md"
    if p.is_file():
        return p
    for candidate in sorted(root.rglob("SKILL.md")):
        parts = candidate.relative_to(root).parts
        if len(parts) <= 2 and "__pycache__" not in parts:
            return candidate
    return None


# ── 规则扫描 ───────────────────────────────────────────────────────────────

_COMPILED = {}


def _compile():
    if _COMPILED:
        return _COMPILED
    for r in verify_rules.PATTERN_RULES:
        try:
            _COMPILED[r.id] = re.compile(r.pattern)
        except re.error as e:
            raise ValueError("规则 %s 正则编译失败: %s" % (r.id, e))
    return _COMPILED


_B64_RE = re.compile(r"[A-Za-z0-9+/]{24,}={0,2}")
_B64_SUSPICIOUS = verify_rules.B64_SUSPICIOUS_WORDS


def _check_base64(line):
    """base64 长串解码后含命令/下载特征 → 编码指令注入提示。"""
    for m in _B64_RE.finditer(line):
        s = m.group(0)
        if len(s) % 4 == 1:
            continue
        try:
            pad = s + "=" * (-len(s) % 4)
            dec = base64.b64decode(pad, validate=False)
        except Exception:
            continue
        try:
            text = dec.decode("utf-8", errors="ignore")
        except Exception:
            continue
        if len(text) < 8:
            continue
        printable = sum(1 for ch in text if 32 <= ord(ch) < 127)
        if printable < len(text) * 0.7:
            continue
        low = text.lower()
        hits = [k for k in _B64_SUSPICIOUS if k in low]
        if len(hits) >= 2:
            return "base64 编码内容含命令/网络特征（%s）" % ", ".join(hits[:3])
    return None


def scan_patterns(files):
    """对文件跑全量规则，返回 Findings 列表。"""
    compiled = _compile()
    findings = []
    seen = set()
    for path, rel in files:
        lines = read_lines(path)
        for idx, line in enumerate(lines, start=1):
            if not line.strip():
                continue
            # base64 编码指令检查（独立启发式，非正则规则）
            hint = _check_base64(line)
            if hint:
                key = ("PIJ-B64", rel, idx)
                if key not in seen:
                    seen.add(key)
                    findings.append(Finding(
                        "PromptInjection", "high", "编码指令",
                        rel, idx, hint, 60, "PIJ-B64"))
            for rule in verify_rules.PATTERN_RULES:
                pat = compiled[rule.id]
                try:
                    if pat.search(line):
                        key = (rule.id, rel, idx)
                        if key in seen:
                            continue
                        seen.add(key)
                        findings.append(Finding(
                            rule.detector, rule.severity,
                            _category_of(rule.detector), rel, idx,
                            rule.description, rule.confidence, rule.id))
                except re.error:
                    continue
    # 敏感文件名级匹配
    for path, rel in files:
        base = Path(rel).name.lower()
        for fname, desc, sev, conf in verify_rules.SENSITIVE_FILENAMES:
            if base == fname.lower() or (fname.startswith(".") and rel.lower().endswith(fname.lower())):
                key = ("SENS", fname, rel)
                if key not in seen:
                    seen.add(key)
                    findings.append(Finding(
                        "CredentialTheft", sev, "凭据文件",
                        rel, 0, "存在敏感文件名: %s（%s）" % (fname, desc),
                        conf, "SENS-" + fname.upper()))
    return findings


_CATEGORY_MAP = {
    "DownloadExec": "下载即执行",
    "Obfuscation": "混淆执行",
    "Persistence": "持久化",
    "Exfiltration": "数据外传",
    "CredentialTheft": "凭据窃取",
    "NetworkCall": "网络调用",
    "PrivilegeEscalation": "权限提升",
    "SocialEngineering": "社会工程",
    "PromptInjection": "提示注入",
}


def _category_of(detector):
    return _CATEGORY_MAP.get(detector, detector)


# ── SKILL.md 完整性 ────────────────────────────────────────────────────────

_FM_RE = re.compile(r"^---\s*$")


def parse_frontmatter(text):
    lines = text.split("\n")
    if not lines or not _FM_RE.match(lines[0].strip()):
        return None
    end = None
    for i in range(1, len(lines)):
        if _FM_RE.match(lines[i].strip()):
            end = i
            break
    if end is None:
        return None
    fm = {}
    for line in lines[1:end]:
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip().lower()] = v.strip()
    return fm


def check_skill_integrity(root, findings, name_hint):
    """SKILL.md 完整性检查（结构类，severity low/medium）。"""
    skill_md = find_skill_md(root)
    if skill_md is None:
        findings.append(Finding(
            "Structure", "medium", "技能结构",
            "SKILL.md", 0,
            "未找到 SKILL.md（技能入口缺失）", 80, "STR-001"))
        return
    try:
        text = skill_md.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return
    fm = parse_frontmatter(text)
    if fm is None:
        findings.append(Finding(
            "Structure", "medium", "技能结构",
            str(skill_md), 0,
            "SKILL.md 缺少 YAML frontmatter（--- 开头）", 80, "STR-002"))
        return
    required = {"name", "description"}
    missing = [k for k in required if not fm.get(k)]
    if missing:
        findings.append(Finding(
            "Structure", "medium", "技能结构",
            str(skill_md), 0,
            "SKILL.md frontmatter 缺少字段: %s" % ", ".join(sorted(missing)),
            80, "STR-003"))
    name = fm.get("name", "")
    if name_hint and name and name != name_hint:
        findings.append(Finding(
            "Structure", "medium", "技能结构",
            str(skill_md), 0,
            "frontmatter name（%s）与目录名（%s）不一致" % (name, name_hint),
            75, "STR-004"))
    # markdown 围栏平衡
    fences = text.count("```")
    if fences % 2 == 1:
        findings.append(Finding(
            "Structure", "low", "技能结构",
            str(skill_md), 0,
            "markdown 代码围栏数量为奇数（可能截断）", 60, "STR-005"))
    # 占位符 / 未完成标记
    for pat, label in ((r"<\s*技能slug\s*>", "未替换占位符 <技能slug>"),
                       (r"TODO|FIXME|TBD|XXX", "未完成标记 TODO/FIXME")):
        if re.search(pat, text):
            findings.append(Finding(
                "Structure", "low", "技能结构",
                str(skill_md), 0, label, 55, "STR-006"))
    # description 触发/边界要素
    desc = fm.get("description", "")
    if desc and not re.search(r"触发|何时|trigger|when", desc, re.I):
        findings.append(Finding(
            "Structure", "low", "技能结构",
            str(skill_md), 0,
            "description 缺少触发条件（触发/何时/when）", 50, "STR-007"))
    if desc and not re.search(r"边界|Do\s*NOT\s*trigger|do not trigger|勿", desc, re.I):
        findings.append(Finding(
            "Structure", "low", "技能结构",
            str(skill_md), 0,
            "description 缺少边界声明（边界/Do NOT trigger）", 50, "STR-008"))


# ── 权限需求分析（info 级汇总；模式定义在 verify_rules.py 签名区）─────────
_PERM_NET = verify_rules.PERM_NET_RE
_PERM_EXEC = verify_rules.PERM_EXEC_RE
_PERM_WRITE = verify_rules.PERM_WRITE_RE
_PERM_READ_SENS = verify_rules.PERM_READ_SENS_RE


_DETECTOR_SIG_FILES = {"audit_rules.py", "verify_rules.py", "vetter_rules.py", "hardening_rules.py"}
_DOC_EXT = {".md", ".txt", ".markdown", ".rst"}


def is_detector_skill(root):
    """目标是否为家族检测技能（v0.3.2：须持「已发布」规则表，路径 + 摘要绑定）。

    旧行为 = 只看目录里有没有同名文件（放一个标记文件即可把整包文档命中降级为
    info）。现改为内容摘要绑定：未验证的同名文件不构成检测器签名。
    """
    return has_published_signature_data(root)


def downgrade_detector_docs(findings, root):
    """检测技能文档中的检测模式描述命中 → 降级为 info（固有属性，非实际行为）。

    对「安全检测技能」区分『检测能力文档』与『实际行为』。
    仅降级文档文件（.md/.txt）中的命中；脚本代码命中保持原判级。
    """
    if not is_detector_skill(root):
        return
    for f in findings:
        if f.detector == "Structure":
            continue
        if f.severity in ("critical", "high", "medium"):
            if Path(f.file_path).suffix.lower() in _DOC_EXT:
                f.severity = "info"
                f.rule_id = (f.rule_id or f.detector) + "-DOC"
                f.description = f.description + "（检测技能文档描述，非实际行为）"
                f.confidence = 30


def permission_summary(files, findings):
    """扫描脚本中声明的权限需求（info 级提示，不入 verdict 决策）。"""
    hits = {"网络调用": 0, "命令执行": 0, "文件写入": 0, "读取敏感文件": 0}
    for path, rel in files:
        if not path.suffix.lower() in TEXT_EXTENSIONS and path.name not in DOTFILE_NAMES:
            continue
        for line in read_lines(path):
            if _PERM_NET.search(line):
                hits["网络调用"] += 1
            if _PERM_EXEC.search(line):
                hits["命令执行"] += 1
            if _PERM_WRITE.search(line):
                hits["文件写入"] += 1
            if _PERM_READ_SENS.search(line):
                hits["读取敏感文件"] += 1
    for label, count in hits.items():
        if count:
            findings.append(Finding(
                "Permission", "info", "权限需求",
                "SUMMARY", 0,
                "%s：命中 %d 处（仅供人工评估权限范围）" % (label, count),
                40, "PERM"))


# ── verdict / 统计 ─────────────────────────────────────────────────────────

def summarize(findings):
    counts = {sev: 0 for sev in _SEVERITY_ORDER}
    by_severity = {}
    for f in findings:
        counts[f.severity] = counts.get(f.severity, 0) + 1
        by_severity.setdefault(f.severity, []).append(f)
    highest = None
    for sev in ("critical", "high", "medium", "low", "info"):
        if counts.get(sev, 0):
            highest = sev
            break
    verdict = VERDICT_BY_SEVERITY.get(highest, VERDICT_SAFE)
    return counts, by_severity, highest, verdict


def exit_code_of(verdict):
    return VERDICT_EXIT.get(verdict, 4)


# ── 扫描主流程 ─────────────────────────────────────────────────────────────

def _safe_extract(tf, dest):
    """提取 tarball（Python 3.8 兼容；拒绝路径穿越、链接与特殊文件；v0.4.4 加解包上限）。"""
    safe_members = []
    root = Path(dest).resolve()
    members = tf.getmembers()
    if len(members) > MAX_TARBALL_MEMBERS:
        raise ValueError("tarball 成员数超过上限: %d > %d"
                         % (len(members), MAX_TARBALL_MEMBERS))
    total_bytes = 0
    for member in members:
        name = member.name.replace("\\", "/")
        drive_path = len(name) >= 2 and name[1] == ":" and name[0].isalpha()
        if (not name or name.startswith("/") or drive_path
                or any(part == ".." for part in name.split("/"))):
            raise ValueError("tarball 含危险路径: %s" % name)
        if member.issym() or member.islnk() or member.isdev() or member.isfifo():
            raise ValueError("tarball 含链接或特殊文件成员: %s" % member.name)
        size = int(member.size or 0)
        if size > MAX_TARBALL_MEMBER_BYTES:
            raise ValueError("tarball 单成员过大: %s（%d 字节）" % (member.name, size))
        total_bytes += size
        if total_bytes > MAX_TARBALL_TOTAL_BYTES:
            raise ValueError("tarball 解包总量超过上限: %d 字节" % total_bytes)
        parts = [part for part in name.split("/") if part not in ("", ".")]
        target = root.joinpath(*parts).resolve()
        try:
            target.relative_to(root)
        except ValueError:
            raise ValueError("tarball 成员越出临时目录: %s" % member.name)
        member.mode = member.mode & 0o777
        safe_members.append(member)
    if sys.version_info >= (3, 12):
        tf.extractall(dest, members=safe_members, filter="data")
    else:
        tf.extractall(dest, members=safe_members)


def _package_slug_from_root(root):
    """从包根 package.json 读取 npm 包名并归一为技能 slug。"""
    try:
        data = json.loads((root / "package.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    name = data.get("name") if isinstance(data, dict) else None
    if not isinstance(name, str):
        return None
    slug = name.strip().rsplit("/", 1)[-1]
    if not slug or slug in (".", "..") or "/" in slug or "\\" in slug:
        return None
    return slug


def resolve_name_hint(target, root, from_archive=False):
    """解析 STR-004 的期望名称：安装目录用目录名，npm 包输入用包名。"""
    if from_archive:
        package_root = root / "package"
        if package_root.is_dir():
            root = package_root
        slug = _package_slug_from_root(root)
        if slug:
            return slug
        return Path(target).name
    if root.name == "package":
        slug = _package_slug_from_root(root)
        if slug:
            return slug
        return root.name
    return root.name


def scan_core(target, name_hint=None, auto_name_hint=False):
    """扫描目录/tarball，返回 (findings, counts, verdict, scan_meta)。"""
    tmpdir = None
    root = Path(target)
    from_archive = False
    if root.is_file() and str(root).lower().endswith((".tgz", ".tar.gz")):
        from_archive = True
        tmpdir = tempfile.mkdtemp(prefix="yotta-verify-")
        with tarfile.open(str(root), "r:gz") as tf:
            _safe_extract(tf, tmpdir)
        root = Path(tmpdir)
    if not root.is_dir():
        if tmpdir:
            import shutil
            shutil.rmtree(tmpdir, ignore_errors=True)
        raise SystemExit("目标不存在或不是目录: %s" % target)
    if auto_name_hint and name_hint is None:
        name_hint = resolve_name_hint(target, root, from_archive=from_archive)
    files = walk_files(root)
    findings = scan_patterns(files)
    # v0.4.4：不可静态分析的可执行 / 二进制载荷按 fail-closed 处理（不再静默跳过）
    for rel, size in find_opaque_files(root):
        findings.append(Finding(
            "Structure", "medium", "不可扫描内容",
            rel, 0,
            "包内含无法静态分析的可执行 / 二进制文件（%d 字节），需人工确认来源与用途"
            % size, 70, "STR-009"))
    check_skill_integrity(root, findings, name_hint)
    permission_summary(files, findings)
    # 检测技能文档降级（2026-08-30）：目标含检测器签名文件（audit_rules 等）→
    # 文档中命中「检测能力描述」（注入模式/凭据等字面）属固有属性，降级为 info，非实际行为。
    downgrade_detector_docs(findings, root)
    # L2/L3 威胁捕获引擎（2026-08-30 增强：数据流 + MCP 工具面）
    for fd in threat_engine.analyze_mcp_tool_surface(files, read_lines):
        findings.append(Finding(
            fd["detector"], fd["severity"], fd["category"], fd["file"],
            fd["line"], fd["description"], fd["confidence"], fd["rule_id"]))
    for fd in threat_engine.analyze_dataflow(files, read_lines):
        findings.append(Finding(
            fd["detector"], fd["severity"], fd["category"], fd["file"],
            fd["line"], fd["description"], fd["confidence"], fd["rule_id"]))
    counts, by_severity, highest, verdict = summarize(findings)
    meta = {
        "target": str(target),
        "files_scanned": len(files),
        "scanned_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "content_hash": threat_engine.build_content_hash(files, read_lines),
        "engine": "yotta-verify v%s + threat_engine" % VERSION,
    }
    if tmpdir:
        import shutil
        shutil.rmtree(tmpdir, ignore_errors=True)
    return findings, counts, verdict, meta


# ── 报告渲染 ───────────────────────────────────────────────────────────────

def render_text(findings, counts, verdict, meta, tool_version=VERSION):
    fdicts = [f.to_dict() for f in findings]
    lines = []
    lines.append("%s %s v%s —— 装前安全扫描" % (CN_NAME, TOOL_NAME, tool_version))
    lines.append("目标：%s（扫描 %d 个文件）" % (meta["target"], meta["files_scanned"]))
    lines.append("")
    lines.append("verdict: %s" % verdict)
    parts = ["%s %d" % (k, counts.get(k, 0)) for k in ("critical", "high", "medium", "low", "info")]
    lines.append("发现：%s" % " / ".join(parts))
    lines.append("安全健康度评分：%d/100" % threat_engine.health_score(fdicts))
    lines.append("")
    lines.append("威胁捕获模型（8 类）：")
    tv = threat_engine.taxonomy_view(
        fdicts, verify_rules.THREAT_TAXONOMY, verify_rules.TAXONOMY_ORDER,
        verify_rules.DETECTOR_TO_TAXONOMY)
    for key in verify_rules.TAXONOMY_ORDER:
        v = tv[key]
        lines.append("  %-16s %-11s %d" % (v["name"], v["verdict"], v["count"]))
    lines.append("")
    lines.append("行为项（13 项）：")
    bv = threat_engine.behavior_view(
        fdicts, verify_rules.BEHAVIORS, verify_rules.DETECTOR_TO_BEHAVIORS)
    observed = [b["behavior"] for b in bv if b["observed"]]
    lines.append("  %s" % ("、".join(observed) if observed else "未观察到明显系统行为"))
    lines.append("")
    if findings:
        by = {}
        for f in sorted(findings, key=lambda x: _SEVERITY_ORDER.index(x.severity) if x.severity in _SEVERITY_ORDER else 0):
            by.setdefault(f.severity, []).append(f)
        for sev in _SEVERITY_ORDER:
            items = by.get(sev, [])
            if not items:
                continue
            lines.append("[%s] %d" % (sev.upper(), len(items)))
            for f in items[:15]:
                loc = "%s:%s" % (f.file_path, f.line) if f.line else f.file_path
                lines.append("  %-12s %-6s %s（%s，置信 %d%%）"
                             % (f.rule_id or f.detector, f.severity, f.description, loc, f.confidence))
            if len(items) > 15:
                lines.append("  … 其余 %d 条（见 --json / --report）" % (len(items) - 15))
    else:
        lines.append("未发现任何可疑项。")
    lines.append("")
    lines.append("提示：verdict 仅供人工决策参考，请结合元安（深度扫描）/ 元审（四阶段审查）复核。")
    return "\n".join(lines)


def render_json(findings, counts, verdict, meta, tool_version=VERSION):
    fdicts = [f.to_dict() for f in findings]
    return json.dumps({
        "tool": {"name": TOOL_NAME, "cn": CN_NAME, "version": tool_version},
        "meta": meta,
        "verdict": verdict,
        "counts": counts,
        "findings": [f.to_dict() for f in findings],
        "threat": {
            "health_score": threat_engine.health_score(fdicts),
            "taxonomy": threat_engine.taxonomy_view(
                fdicts, verify_rules.THREAT_TAXONOMY, verify_rules.TAXONOMY_ORDER,
                verify_rules.DETECTOR_TO_TAXONOMY),
            "behaviors": threat_engine.behavior_view(
                fdicts, verify_rules.BEHAVIORS, verify_rules.DETECTOR_TO_BEHAVIORS),
            "files": threat_engine.file_view(fdicts),
            "repair_guide": threat_engine.repair_guide(fdicts),
        },
    }, ensure_ascii=False, indent=2)


def render_markdown(findings, counts, verdict, meta, tool_version=VERSION):
    fdicts = [f.to_dict() for f in findings]
    lines = []
    lines.append("# SKILL VERIFY REPORT")
    lines.append("")
    lines.append("- 工具：%s %s v%s" % (CN_NAME, TOOL_NAME, tool_version))
    lines.append("- 目标：%s（扫描 %d 个文件）" % (meta["target"], meta["files_scanned"]))
    lines.append("- 扫描时间：%s" % meta["scanned_at"])
    lines.append("")
    lines.append("## Verdict")
    lines.append("")
    lines.append("**%s**" % verdict)
    lines.append("")
    lines.append("| 严重级 | 数量 |")
    lines.append("|---|---|")
    for sev in ("critical", "high", "medium", "low", "info"):
        lines.append("| %s | %d |" % (sev, counts.get(sev, 0)))
    lines.append("")
    lines.append("**安全健康度评分：%d/100**" % threat_engine.health_score(fdicts))
    lines.append("")
    lines.append("## 威胁捕获模型视图（8 类）")
    lines.append("")
    lines.append("| 检测点 | verdict | 命中 |")
    lines.append("|---|---|---|")
    tv = threat_engine.taxonomy_view(
        fdicts, verify_rules.THREAT_TAXONOMY, verify_rules.TAXONOMY_ORDER,
        verify_rules.DETECTOR_TO_TAXONOMY)
    for key in verify_rules.TAXONOMY_ORDER:
        v = tv[key]
        lines.append("| %s | %s | %d |" % (v["name"], v["verdict"], v["count"]))
    lines.append("")
    lines.append("## 行为项（13 项）")
    lines.append("")
    bv = threat_engine.behavior_view(
        fdicts, verify_rules.BEHAVIORS, verify_rules.DETECTOR_TO_BEHAVIORS)
    observed = [b["behavior"] for b in bv if b["observed"]]
    lines.append("观察到：%s" % ("、".join(observed) if observed else "未观察到明显系统行为"))
    lines.append("")
    guide = threat_engine.repair_guide(fdicts)
    if guide:
        lines.append("## 修复建议指南")
        lines.append("")
        for i, g in enumerate(guide, 1):
            lines.append("%d. %s" % (i, g))
        lines.append("")
    lines.append("## Findings")
    lines.append("")
    if not findings:
        lines.append("未发现任何可疑项。")
    else:
        lines.append("| 规则 | 严重级 | 位置 | 说明 | 置信度 |")
        lines.append("|---|---|---|---|---|")
        for f in sorted(findings, key=lambda x: _SEVERITY_ORDER.index(x.severity) if x.severity in _SEVERITY_ORDER else 0):
            loc = "%s:%s" % (f.file_path, f.line) if f.line else f.file_path
            lines.append("| %s | %s | %s | %s | %d%% |"
                         % (f.rule_id or f.detector, f.severity, loc, f.description, f.confidence))
    lines.append("")
    lines.append("> 结论仅供人工决策参考；最终判断由用户。建议结合元安（深度扫描）与元审（四阶段审查）。")
    return "\n".join(lines)


# ── 徽章生成（零依赖 SVG，shields.io flat 风格）──────────────────────────

def _text_width(text):
    # 近似宽度：ASCII ~7px，CJK ~11px（font-size 11px）
    w = 0
    for ch in text:
        w += 11 if ord(ch) > 0x2E7F else 7
    return w


def _seg_width(label, value):
    return 10 + _text_width(label) + 10 + _text_width(value) + 6


def badge_svg(segments, height=20):
    """segments: [(label, value, color)]  → 扁平徽章 SVG（shields.io 风格）。"""
    widths = [_seg_width(l, v) for l, v, _ in segments]
    total = sum(widths)
    pad = 4
    x = pad
    parts = []
    parts.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d">'
                 % (total + pad * 2, height))
    for (label, value, color), w in zip(segments, widths):
        lw = 10 + _text_width(label)
        vw = 10 + _text_width(value) + 6
        # 标签段
        parts.append('<rect x="%d" y="0" width="%d" height="%d" fill="#555" rx="3"/>' % (x, lw, height))
        # 值段
        parts.append('<rect x="%d" y="0" width="%d" height="%d" fill="%s" rx="3"/>'
                     % (x + lw - 3, vw + 3, height, color))
        # 文本
        parts.append('<text x="%d" y="%d" fill="#fff" font-family="Verdana,DejaVu Sans,sans-serif" font-size="11" font-weight="bold">%s</text>'
                     % (x + 5, height - 6, _xml(label)))
        parts.append('<text x="%d" y="%d" fill="#fff" font-family="Verdana,DejaVu Sans,sans-serif" font-size="11" font-weight="bold">%s</text>'
                     % (x + lw + 3, height - 6, _xml(value)))
        x += w
    parts.append('</svg>')
    return "".join(parts)


def _xml(text):
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def build_badges(verdict, extra=None):
    """构造徽章 SVG + shields.io URL。extra: {validate, vetter, audit, version, tests}"""
    extra = extra or {}
    color = BADGE_COLORS.get(verdict, "lightgrey")
    url_label = "verified"
    url_value = verdict.replace(" ", "%20")
    url = "https://img.shields.io/badge/%s-%s-%s" % (url_label, url_value, color)
    segs = [("verified", verdict, color)]
    if extra.get("validate") is not None:
        segs.append(("validate-skill", extra["validate"], "3c8" if extra["validate"].upper() == "PASS" else "e05d44"))
    if extra.get("vetter") is not None:
        segs.append(("vetter", extra["vetter"], BADGE_COLORS.get(extra["vetter"], "9f9f9f")))
    if extra.get("audit") is not None:
        segs.append(("audit", extra["audit"], BADGE_COLORS.get(extra["audit"], "9f9f9f")))
    if extra.get("version"):
        segs.append(("version", extra["version"], "007ec6"))
    if extra.get("tests") is not None:
        segs.append(("tests", str(extra["tests"]), "007ec6"))
    return badge_svg(segs), url


def shields_url(verdict):
    color = BADGE_COLORS.get(verdict, "lightgrey")
    return "https://img.shields.io/badge/verified-%s-%s" % (verdict.replace(" ", "%20"), color)


# ── CLI ─────────────────────────────────────────────────────────────────────

def cmd_scan(args):
    findings, counts, verdict, meta = scan_core(args.path, auto_name_hint=True)
    code = exit_code_of(verdict)
    # gate 模式
    if args.max_severity:
        limit = _SEVERITY_VALUE.get(args.max_severity.lower(), 1)
        worst = _SEVERITY_VALUE.get(verdict_worst(findings), 0)
        if worst > limit:
            print("gate 失败：最大严重级 %s 超过阈值 %s" % (verdict_worst(findings), args.max_severity))
            code = max(code, 1)
    if args.json:
        print(render_json(findings, counts, verdict, meta))
    else:
        print(render_text(findings, counts, verdict, meta))
    if args.report:
        Path(args.report).write_text(render_markdown(findings, counts, verdict, meta),
                                     encoding="utf-8")
        print("\n报告已写入: %s" % args.report)
    if args.badge:
        extra = {"validate": "PASS" if code <= 1 else "FAIL",
                 "version": VERSION,
                 "tests": None}
        svg, url = build_badges(verdict, extra)
        out = args.badge if isinstance(args.badge, str) else "assets/audited.svg"
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        Path(out).write_text(svg, encoding="utf-8")
        print("audited 徽章已生成: %s" % out)
        print("shields.io: %s" % url)
    return code


def verdict_worst(findings):
    worst = "info"
    for f in findings:
        if _SEVERITY_VALUE.get(f.severity, 0) > _SEVERITY_VALUE.get(worst, 0):
            worst = f.severity
    return worst


def cmd_badge(args):
    extra = {
        "validate": getattr(args, "validate_skill", None),
        "vetter": getattr(args, "vetter_verdict", None),
        "audit": getattr(args, "audit_verdict", None),
        "version": getattr(args, "version", None) or VERSION,
        "tests": getattr(args, "tests", None),
    }
    # 若给目录：先扫描拿 verdict；否则默认 SAFE
    if args.path and Path(args.path).exists():
        findings, counts, verdict, meta = scan_core(args.path, auto_name_hint=True)
    else:
        verdict = VERDICT_SAFE
        counts = {s: 0 for s in _SEVERITY_ORDER}
    svg, url = build_badges(verdict, extra)
    out = args.out or "assets/audited.svg"
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(svg, encoding="utf-8")
    print("audited 徽章已生成: %s" % out)
    print("shields.io: %s" % url)
    return 0


def cmd_report(args):
    findings, counts, verdict, meta = scan_core(args.path, auto_name_hint=True)
    if args.json:
        print(render_json(findings, counts, verdict, meta))
    else:
        print(render_markdown(findings, counts, verdict, meta))
    if args.out:
        Path(args.out).write_text(
            render_json(findings, counts, verdict, meta) if args.json
            else render_markdown(findings, counts, verdict, meta),
            encoding="utf-8")
        print("报告已写入: %s" % args.out)
    return exit_code_of(verdict)


def cmd_gate(args):
    findings, counts, verdict, meta = scan_core(args.path, auto_name_hint=True)
    code = exit_code_of(verdict)
    limit = _SEVERITY_VALUE.get((args.max_severity or "medium").lower(), 1)
    worst = _SEVERITY_VALUE.get(verdict_worst(findings), 0)
    if args.json:
        print(render_json(findings, counts, verdict, meta))
    else:
        print(render_text(findings, counts, verdict, meta))
    if worst > limit:
        print("gate 失败：最严重级 %s 超过阈值 %s（exit %d）" % (verdict_worst(findings), args.max_severity, max(code, 1)))
        return max(code, 1)
    print("gate 通过：最严重级 %s ≤ 阈值 %s" % (verdict_worst(findings), args.max_severity))
    return code


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog=TOOL_NAME,
        description="%s %s —— 装前安全扫描器（确定性静态校验 + audited 徽章）" % (CN_NAME, TOOL_NAME))
    parser.add_argument("--version", action="store_true", help="显示版本")
    sub = parser.add_subparsers(dest="command")

    p_scan = sub.add_parser("scan", help="装前安全扫描（prompt injection + 危险模式 + SKILL 完整性）")
    p_scan.add_argument("path")
    p_scan.add_argument("--json", action="store_true")
    p_scan.add_argument("--report")
    p_scan.add_argument("--badge", nargs="?", const="assets/audited.svg", default=None)
    p_scan.add_argument("--max-severity")
    p_scan.set_defaults(func=cmd_scan)

    p_badge = sub.add_parser("badge", help="生成 audited 徽章（本地 SVG + shields.io URL）")
    p_badge.add_argument("path", nargs="?", default=None)
    p_badge.add_argument("--out")
    p_badge.add_argument("--validate-skill", choices=["pass", "fail"])
    p_badge.add_argument("--vetter-verdict")
    p_badge.add_argument("--audit-verdict")
    p_badge.add_argument("--tests", type=int)
    p_badge.add_argument("--version")
    p_badge.set_defaults(func=cmd_badge)

    p_report = sub.add_parser("report", help="生成验证报告（Markdown / JSON）")
    p_report.add_argument("path")
    p_report.add_argument("--json", action="store_true")
    p_report.add_argument("--out")
    p_report.set_defaults(func=cmd_report)

    p_gate = sub.add_parser("gate", help="CI 闸门（默认阈值 medium，超出即失败）")
    p_gate.add_argument("path")
    p_gate.add_argument("--max-severity", default="medium")
    p_gate.add_argument("--json", action="store_true")
    p_gate.set_defaults(func=cmd_gate)

    args = parser.parse_args(argv)
    if args.version and not getattr(args, "command", None):
        print("%s %s v%s" % (CN_NAME, TOOL_NAME, VERSION))
        return 0
    if not getattr(args, "command", None):
        parser.print_help()
        return 4
    try:
        return args.func(args)
    except SystemExit as e:
        return e.code if isinstance(e.code, int) else 4
    except Exception as e:  # noqa: BLE001
        print("错误：%s" % e, file=sys.stderr)
        return 4


if __name__ == "__main__":
    sys.exit(main())
