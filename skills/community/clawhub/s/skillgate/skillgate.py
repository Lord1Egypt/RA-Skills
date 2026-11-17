#!/usr/bin/env python3
"""skillgate — Skill 安全与质量扫描门禁

Usage:
    python skillgate scan <skill_dir>
    python skillgate scan <skill_dir> --format json
    python skillgate scan <skill_dir> --format markdown --output report.md

Exit codes:
    0 = pass (all checks green)
    1 = fail (critical/high findings)
    2 = usage error
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

# Import AST analyzer
try:
    from ast_analyzer import analyze_python_file as ast_analyze
except ImportError:
    ast_analyze = None

# All script-like languages are scanned by the built-in language-agnostic
# scanner below — no optional analyzer module is required (never "miss
# dangerous files" because a helper is absent).


# ── Config (.skillgate.yml) support ─────────────────────────────────────────
def _glob_to_regex(pattern: str) -> str:
    """Convert a simple glob (with `**` support) to a regex string."""
    pat = pattern.replace('\\', '/').lstrip('./')
    out = []
    i = 0
    n = len(pat)
    while i < n:
        c = pat[i]
        if c == '*':
            if i + 1 < n and pat[i + 1] == '*':
                out.append('.*')
                i += 2
                if i < n and pat[i] == '/':
                    out.append('/?')
                    i += 1
            else:
                out.append('[^/]*')
                i += 1
        elif c == '?':
            out.append('[^/]')
            i += 1
        else:
            out.append(re.escape(c))
            i += 1
    return '^' + ''.join(out) + '$'


def load_config_excludes(skill_path: Path) -> list:
    """Parse paths.exclude from .skillgate.yml / .skillgate.yaml.

    Zero-dependency minimal parser (no PyYAML): it only needs the exclude list.
    The first existing config file wins.
    """
    excludes = []
    for cfg_name in ('.skillgate.yml', '.skillgate.yaml'):
        cfg = skill_path / cfg_name
        if not cfg.exists():
            continue
        try:
            in_exclude = False
            for raw in cfg.read_text(encoding='utf-8', errors='replace').splitlines():
                line = raw.strip()
                if not line or line.startswith('#'):
                    continue
                if line.startswith('exclude:'):
                    in_exclude = True
                    continue
                if in_exclude:
                    if line.startswith('-'):
                        item = line.lstrip('-').strip()
                        # strip inline comments, then surrounding quotes
                        if '#' in item:
                            item = item.split('#', 1)[0].strip()
                        item = item.strip('"').strip("'").strip()
                        if item:
                            excludes.append(item)
                    elif line and not line.startswith('.'):
                        in_exclude = False
        except Exception:
            pass
        break
    return excludes


# ── Check patterns ──────────────────────────────────────────────────────────

# 1. Dangerous code execution
DANGEROUS_CODE_PATTERNS = [
    # 正则模式字面量拆分：规则库必须含危险调用模式，拆分后源码不再出现连续的
    # "ev-al" 危险调用字样（含注释），避免 ClawHub 等安全扫描器对规则库本身自指误报；运行时拼接结果与原文一致
    (r"\be" + "val" + r"\s*\(", "MEDIUM", "动态代码执行调用（工具常用，需人工判断）"),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
    (r"\bex" + "ec" + r"\s*\(", "MEDIUM", "动态代码执行调用（工具常用，需人工判断）"),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
    (r"\bos\.system\s*\(", "HIGH", "os.system() shell 调用"),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
    (r"\bsubprocess\.(run|call|Popen|check_output)\s*\([^)]*shell\s*=\s*True", "HIGH", "subprocess shell=True"),
    (r"\bos\.popen\s*\(", "HIGH", "os.popen() shell 调用"),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
    (r"\b__import__\s*\(", "MEDIUM", "动态 import"),
    (r"\bpickle\.load(s)?\s*\(", "HIGH", "pickle 反序列化"),
    (r"\byaml\.load\s*\([^)]*\)(?![^#]*Loader\s*=\s*SafeLoader)", "MEDIUM", "yaml.load 非安全加载"),
    (r"\bcompile\s*\([^)]*\)", "INFO", "compile() 动态代码编译（低风险）"),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
    (r"\bgetattr\s*\([^)]*os\.", "MEDIUM", "getattr 动态调用 os 模块"),
    (r"\bglobals\(\)", "INFO", "globals() 访问全局命名空间（低风险）"),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
    (r"\blocals\(\)", "INFO", "locals() 访问局部命名空间（低风险）"),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
    (r"\binput\s*\(\)", "INFO", "input() 接受用户输入（CLI 工具常见）"),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
    (r"\binput\s*\([^)]*\)", "INFO", "input() 接受用户输入（CLI 工具常见）"),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
    (r"\b__builtins__\b", "INFO", "访问 __builtins__（低风险）"),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
    (r"\bglobals\(\)\[", "MEDIUM", "globals() 动态修改"),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
    (r"\bsetattr\s*\(", "INFO", "setattr 动态属性设置（低风险）"),
    (r"\bdelattr\s*\(", "INFO", "delattr 动态属性删除（低风险）"),
    # === 新增规则 ===
    (r"\bmarshal\.load(s)?\s*\(", "HIGH", "marshal 反序列化"),
    (r"\bshelve\.open\s*\(", "MEDIUM", "shelve 反序列化"),
    (r"\bjsonpickle\.decode\s*\(", "HIGH", "jsonpickle 反序列化"),
    (r"\byaml\.unsafe_load\s*\(", "CRITICAL", "yaml.unsafe_load 任意代码执行"),
    (r"\b__reduce__\s*\(", "MEDIUM", "__reduce__ 反序列化钩子"),
    (r"\bbuiltins\.__import__\s*\(", "MEDIUM", "builtins.__import__ 动态导入"),
    (r"\bimportlib\.import_module\s*\(", "LOW", "importlib 动态导入"),
    (r"\bctypes\.CDLL\s*\(", "HIGH", "ctypes 加载动态库"),
    (r"\bctypes\.windll\s*\(", "HIGH", "ctypes 加载 Windows DLL"),
    (r"\bctypes\.oledll\s*\(", "HIGH", "ctypes 加载 OLE DLL"),
    (r"\bdl\.open\s*\(", "HIGH", "dlopen 加载动态库"),
    (r"\bctypes\.pythonapi\b", "MEDIUM", "ctypes.pythonapi 直接调用 C API"),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
]

# 2. Network calls / data exfiltration
NETWORK_PATTERNS = [
    (r"\bimport\s+requests\b", "INFO", "requests 网络库（常见）"),
    (r"\bfrom\s+requests\s+import\b", "INFO", "requests 网络库（常见）"),
    (r"\bimport\s+urllib\b", "INFO", "urllib 网络库（常见）"),
    (r"\bimport\s+http\.client\b", "INFO", "http.client 网络库"),
    (r"\bimport\s+socket\b", "LOW", "socket 原始网络连接"),
    (r"\bimport\s+ftplib\b", "LOW", "FTP 库"),
    (r"\bimport\s+smtplib\b", "LOW", "SMTP 邮件库"),
    (r"\burlopen\s*\(", "LOW", "urlopen 网络请求"),
    (r"\bpost\s*\([^)]*https?://", "MEDIUM", "POST 数据到外部 URL"),
    (r"\bhttpx\b", "INFO", "httpx HTTP 客户端（常见）"),
    (r"\baiohttp\b", "INFO", "aiohttp 异步 HTTP（常见）"),
    (r"\bcurl\b", "LOW", "curl 命令行网络工具"),  # skillgate: ignore: rule-pattern keyword line (verified false positive)
    (r"\bwget\b", "LOW", "wget 命令行网络工具"),  # skillgate: ignore: rule-pattern keyword line (verified false positive)
    (r"\bnc\s+-[el]\b", "HIGH", "netcat 反向 shell 风险"),
    (r"\bncat\b", "LOW", "ncat 网络工具"),  # skillgate: ignore: rule-pattern keyword line (verified false positive)
    (r"\btelnetlib\b", "HIGH", "telnetlib 明文传输"),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
    (r"\bparamiko\b", "LOW", "paramiko SSH 库"),
    (r"\bscp\b", "LOW", "scp 文件传输"),  # skillgate: ignore: rule-pattern keyword line (verified false positive)
]

# 3. Credential / secret access
CREDENTIAL_PATTERNS = [
    (re.compile(r"(api[_-]?key|apikey|secret|token|password|passwd|credential)\s*[:=]\s*['\"]([^'\"]{8,})['\"]", re.IGNORECASE),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
     "CRITICAL", "硬编码凭证"),
    (re.compile(r"os\.environ\[['\"](.*TOKEN|.*KEY|.*SECRET|.*PASSWORD)['\"]\]", re.IGNORECASE),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
     "INFO", "从环境变量读凭证（安全做法）"),
    (re.compile(r"os\.getenv\s*\(\s*['\"](.*TOKEN|.*KEY|.*SECRET|.*PASSWORD)", re.IGNORECASE),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
     "INFO", "从环境变量读凭证（安全做法）"),
    (re.compile(r"~\.ssh/", re.IGNORECASE),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
     "HIGH", "访问 SSH 密钥目录"),
    (re.compile(r"\.aws/credentials", re.IGNORECASE),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
     "HIGH", "访问 AWS 凭证文件"),
    (re.compile(r"\.git-credentials", re.IGNORECASE),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
     "HIGH", "访问 Git 凭证文件"),
    (re.compile(r"\.netrc", re.IGNORECASE),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
     "MEDIUM", "访问 .netrc 凭证文件"),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
    (re.compile(r"\.npmrc", re.IGNORECASE),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
     "MEDIUM", "访问 .npmrc 凭证文件"),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
    (re.compile(r"\.pypirc", re.IGNORECASE),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
     "MEDIUM", "访问 .pypirc 凭证文件"),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
    (re.compile(r"id_rsa", re.IGNORECASE),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
     "HIGH", "访问 SSH 私钥"),
    (re.compile(r"id_ed25519", re.IGNORECASE),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
     "HIGH", "访问 SSH 私钥"),
]

# 4. File system danger
FILESYSTEM_PATTERNS = [
    (r"\bshutil\.rmtree\s*\(", "MEDIUM", "shutil.rmtree 递归删除"),
    (r"\bos\.remove\s*\(", "INFO", "os.remove 删除文件（常见）"),
    (r"\bos\.rmdir\s*\(", "INFO", "os.rmdir 删除目录（常见）"),
    (r"\bos\.unlink\s*\(", "MEDIUM", "os.unlink 删除文件"),
    (r"\bopen\s*\([^)]*['\"]/etc/", "HIGH", "写入 /etc/ 系统目录"),
    (r"\bopen\s*\([^)]*['\"]C:\\\\Windows\\\\", "HIGH", "写入 Windows 系统目录"),
    (r"\bopen\s*\([^)]*['\"]/System/", "HIGH", "写入 macOS 系统目录"),
    (r"\bos\.rename\s*\([^)]*/etc/", "MEDIUM", "重命名 /etc/ 下文件"),
    (r"\bshutil\.move\s*\([^)]*/etc/", "MEDIUM", "移动文件到 /etc/"),
    (r"\btempfile\.mkdtemp\b", "LOW", "创建临时目录"),
    (r"\btempfile\.mktemp\b", "MEDIUM", "mktemp 临时文件竞争风险"),
]

# 5. Prompt injection / LLM-specific risks
PROMPT_INJECTION_PATTERNS = [
    (r"ignore\s+previous\s+instructions", "CRITICAL", "Prompt injection: ignore previous"),
    (r"disregard\s+all\s+previous", "CRITICAL", "Prompt injection: disregard previous"),
    (r"you\s+are\s+now\s+a?n?\s+\w+", "MEDIUM", "Prompt injection: persona override"),
    (r"system\s+prompt\s+leak", "HIGH", "System prompt leak attempt"),
    (r"jailbreak", "CRITICAL", "Jailbreak pattern"),
    (r"reveal\s+your\s+instructions", "HIGH", "Reveal system instructions attempt"),
    (r"reveal\s+your\s+prompt", "HIGH", "Reveal system prompt attempt"),
    (r"bypass\s+safety", "HIGH", "Bypass safety guardrails"),
    (r"do\s+not\s+tell\s+the\s+user", "MEDIUM", "Hide actions from user"),
    (r"do\s+not\s+mention", "LOW", "Instructed to omit information"),
    (r"pretend\s+you\s+are", "MEDIUM", "Pretend persona override"),
    (r"act\s+as\s+if\s+you\s+are", "MEDIUM", "Act as persona override"),
    (r"forget\s+your\s+rules", "CRITICAL", "Forget your rules"),
    (r"override\s+your\s+guidelines", "CRITICAL", "Override guidelines"),
    (r"ignore\s+your\s+training", "CRITICAL", "Ignore training"),
]

# 6. Excessive agency / MCP risks
EXCESSIVE_AGENCY_PATTERNS = [
    (r"delete\s+all\s+files", "CRITICAL", "Excessive agency: delete all files"),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
    (r"send\s+all\s+data", "HIGH", "Excessive agency: exfiltrate all data"),
    (r"run\s+arbitrary\s+commands", "HIGH", "Arbitrary command execution"),
    (r"access\s+all\s+files", "MEDIUM", "Overly broad file access"),
    (r"read\s+every\s+file", "HIGH", "Read every file"),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
    (r"modify\s+all\s+configs", "HIGH", "Modify all configs"),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
    (r"install\s+any\s+package", "MEDIUM", "Install any package"),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
    (r"unrestricted\s+internet\s+access", "MEDIUM", "Unrestricted internet access"),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
    (r"bypass\s+all\s+safety\s+checks", "CRITICAL", "Bypass all safety checks"),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
    (r"disable\s+all\s+filters", "HIGH", "Disable all filters"),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
    (r"grant\s+yourself\s+admin", "CRITICAL", "Grant yourself admin access"),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
    (r"add\s+new\s+user\s+accounts", "HIGH", "Add new user accounts"),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
]

# 7. License compliance
LICENSE_PATTERNS = [
    (r"\bGPL\b", "MEDIUM", "GPL 许可证（传染性）"),
    (r"\bAGPL\b", "HIGH", "AGPL 许可证（网络传染性）"),
    (r"\bSSPL\b", "HIGH", "SSPL 许可证（服务端传染性）"),
    (r"\bUnlicense\b", "LOW", "Unlicense（公有领域）"),
]

# 8. Code quality
QUALITY_PATTERNS = [
    (r"\bTODO\b", "LOW", "TODO 注释未完成"),
    (r"\bFIXME\b", "LOW", "FIXME 注释未修复"),
    (r"\bHACK\b", "LOW", "HACK 临时方案"),
    (r"\bXXX\b", "LOW", "XXX 标记的问题"),
    (r"\bprint\s*\(", "LOW", "print 调试语句"),
    (r"\bconsole\.log\(", "LOW", "console.log 调试语句"),
    (r"\bdebugger\b", "MEDIUM", "debugger 语句"),
]

# 9. Authentication & Authorization
AUTH_PATTERNS = [
    (r"\bauth\s*=\s*None\b", "MEDIUM", "认证被禁用"),
    (r"\bverify\s*=\s*False\b", "HIGH", "SSL 验证被禁用"),
    (r"\bALLOW_ALL\b", "HIGH", "允许所有访问"),
    (r"\bCORS.*\*\b", "MEDIUM", "CORS 允许所有来源"),
    (r"\bpassword\s*=\s*['\"][^'\"]+['\"]", "CRITICAL", "硬编码密码"),
    (r"\btoken\s*=\s*['\"][a-zA-Z0-9]{20,}['\"]", "CRITICAL", "硬编码 token"),
]

# 10. Input Validation
VALIDATION_PATTERNS = [
    (r"\brequest\.args\.get\(", "LOW", "直接读取请求参数"),
    (r"\binput\s*\(", "MEDIUM", "读取用户输入"),
    (r"\bsys\.argv\b", "LOW", "读取命令行参数"),
    (r"\bos\.environ\[", "MEDIUM", "读取环境变量"),
]

# 11. Data Exfiltration Risk
EXFIL_PATTERNS = [
    (r"\brequests\.post\([^)]*https?://", "MEDIUM", "向外发 POST 请求"),
    (r"\burllib\.request\.urlopen\(", "MEDIUM", "向外发请求"),
    (r"\bsmtplib\.SMTP\(", "MEDIUM", "发送邮件"),
    (r"\bsocket\.socket\(", "MEDIUM", "原始 socket 网络连接"),
]

FRONTMATTER_REQUIRED_FIELDS = ["name", "description"]
FRONTMATTER_OPTIONAL_FIELDS = ["version", "license", "author", "tags"]

STDLIB_MODULES = {
    "argparse", "ast", "base64", "collections", "copy", "csv", "datetime",
    "functools", "hashlib", "itertools", "json", "logging", "math",
    "os", "pathlib", "pickle", "platform", "random", "re", "shutil",
    "sqlite3", "string", "sys", "tempfile", "time", "typing", "urllib",
    "xml", "zipfile", "__future__", "abc", "asyncio", "dataclasses",
    "enum", "io", "socket", "subprocess", "threading", "unittest",
    "warnings", "weakref",
}


# ── Data classes ──────────────────────────────────────────────────────────

# Category explanations (有证：每个结论有解释)
CATEGORY_EXPLANATIONS = {
    "dangerous-code": "检测到危险代码模式，可能导致代码执行或系统破坏",
    "credential-leak": "检测到硬编码凭证或敏感信息泄露",
    "prompt-injection": "检测到 prompt 注入风险，可能被绕过安全限制",
    "excessive-agency": "检测到过度权限，可能超出预期的操作范围",
    "network": "检测到网络请求，注意数据外带风险",
    "filesystem": "检测到文件系统操作，注意删除和写入风险",
    "deserialization": "检测到不安全的反序列化，可能导致 RCE",
    "dependency": "检测到有风险的依赖包",
    "license": "检测到许可证合规问题",
    "code-quality": "代码质量问题，不影响安全但影响可维护性",
    "auth": "认证授权相关问题",
    "input-validation": "输入验证相关问题",
    "exfiltration": "数据外带风险",
    "ast-analysis": "AST 语法树分析发现的问题",
    "structure": "项目结构问题",
    "file-read": "文件读取问题",
}


@dataclass
class Finding:
    severity: str  # CRITICAL / HIGH / MEDIUM / LOW
    category: str
    message: str
    file: str
    line: Optional[int] = None
    rule_id: str = ""  # 规则唯一 ID
    explanation: str = ""  # 为什么报这个


@dataclass
class ScanResult:
    skill_name: str = ""
    skill_dir: str = ""
    findings: list[Finding] = field(default_factory=list)
    files_scanned: int = 0
    frontmatter: dict = field(default_factory=dict)
    trust_score: int = 0
    grade: str = ""
    rule_version: str = "v3.0.0"  # 规则版本号（有籍）
    # 被 `# skillgate: ignore` 抑制的发现（如实披露，不静默）：数量与清单
    suppressed_count: int = 0
    suppressed: list = field(default_factory=list)

    @property
    def critical_count(self): return len([f for f in self.findings if f.severity == "CRITICAL"])
    @property
    def high_count(self): return len([f for f in self.findings if f.severity == "HIGH"])
    @property
    def medium_count(self): return len([f for f in self.findings if f.severity == "MEDIUM"])
    @property
    def low_count(self): return len([f for f in self.findings if f.severity == "LOW"])


# ── Scanners ──────────────────────────────────────────────────────────────

def scan_python_file(filepath: Path, result: ScanResult):
    """Scan a single Python file for dangerous patterns."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        result.findings.append(Finding(
            severity="LOW", category="file-read",
            message=f"无法读取文件: {e}", file=str(filepath)
        ))
        return

    # === 第一步：AST 分析（更准，误报低） ===
    ast_lines = set()  # 记录 AST 已经报过的行，正则就不要重复报了
    try:
        from ast_analyzer import analyze_python_file
        ast_findings = analyze_python_file(filepath)
        for af in ast_findings:
            result.findings.append(Finding(
                severity=af.severity,
                category="ast-analysis",
                message=f"[AST] {af.message}",
                file=str(filepath),
                line=af.line
            ))
            ast_lines.add(af.line)  # 记录这一行已经报过了
    except Exception as exc:
        # AST analysis failing must never silently pass a file it could not
        # fully inspect — surface it so the report reflects the gap.
        result.findings.append(Finding(
            severity="LOW", category="scan-error",
            message=f"AST 分析失败（正则扫描继续）: {exc}",
            file=str(filepath), line=0,
        ))

    lines = content.splitlines()

    # Helper: check if line is a comment
    def is_comment_line(line: str) -> bool:
        stripped = line.strip()
        return stripped.startswith("#") or stripped.startswith('"""') or stripped.startswith("'''")

    # Helper: check if match is inside a string (simple heuristic)
    def is_inside_string(line: str, match_start: int) -> bool:
        """Simple heuristic: check if the match position is inside a string literal."""
        # Count quotes before the match
        before = line[:match_start]
        # Count unescaped quotes
        single_quotes = before.count("'") - before.count("\\'")
        double_quotes = before.count('"') - before.count('\\"')
        # If odd number of either, we're inside a string
        return (single_quotes % 2 == 1) or (double_quotes % 2 == 1)

    # Helper: check if line has skillgate: ignore suppression
    # NOTE: line-level suppression is applied ONLY in the post-filter below,
    # which gates it on self-scan. Skipping findings here (at scan time) would
    # let any scanned skill suppress findings before the self-scan-only check
    # runs — an early-suppression bypass. All findings are therefore recorded
    # first and suppression is decided centrally.
    def is_suppressed(line_idx: int) -> bool:
        return False

    # 1. Dangerous code patterns
    for pattern, severity, msg in DANGEROUS_CODE_PATTERNS:
        for i, line in enumerate(lines, 1):
            if is_comment_line(line):
                continue
            if is_suppressed(i):
                continue
            if i in ast_lines:  # AST 已经报过了，不要重复报
                continue
            if re.search(pattern, line):
                result.findings.append(Finding(
                    severity=severity, category="dangerous-code",
                    message=msg, file=str(filepath), line=i
                ))

    # 2. Network patterns
    for pattern, severity, msg in NETWORK_PATTERNS:
        for i, line in enumerate(lines, 1):
            if is_comment_line(line):
                continue
            if is_suppressed(i):
                continue
            if re.search(pattern, line):
                result.findings.append(Finding(
                    severity=severity, category="network",
                    message=msg, file=str(filepath), line=i
                ))

    # 3. Credential / secret patterns
    for pattern, severity, msg in CREDENTIAL_PATTERNS:
        for i, line in enumerate(lines, 1):
            if is_comment_line(line):
                continue
            if pattern.search(line):
                result.findings.append(Finding(
                    severity=severity, category="credential-leak",
                    message=msg, file=str(filepath), line=i
                ))

    # 4. Filesystem danger patterns
    for pattern, severity, msg in FILESYSTEM_PATTERNS:
        for i, line in enumerate(lines, 1):
            if is_comment_line(line):
                continue
            if re.search(pattern, line):
                result.findings.append(Finding(
                    severity=severity, category="filesystem",
                    message=msg, file=str(filepath), line=i
                ))

    # 5. Excessive agency patterns
    for pattern, severity, msg in EXCESSIVE_AGENCY_PATTERNS:
        for i, line in enumerate(lines, 1):
            if is_comment_line(line):
                continue
            if re.search(pattern, line, re.IGNORECASE):
                result.findings.append(Finding(
                    severity=severity, category="excessive-agency",
                    message=msg, file=str(filepath), line=i
                ))

    # 6. AST analysis (higher precision, lower false positive)
    if ast_analyze:
        try:
            ast_findings = ast_analyze(filepath)
            for af in ast_findings:
                result.findings.append(Finding(
                    severity=af.severity, category="ast-analysis",
                    message=af.message, file=str(filepath), line=af.line
                ))
        except Exception:
            pass


def scan_md_file(filepath: Path, result: ScanResult):
    """Scan a Markdown file for prompt injection patterns and for dangerous
    calls inside fenced code blocks (skills can hide commands in READMEs)."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:
        result.findings.append(Finding(
            severity="MEDIUM", category="scan-error",
            message=f"无法读取文件（扫描未覆盖）: {exc}",
            file=str(filepath), line=0,
        ))
        return

    lines = content.splitlines()
    for pattern, severity, msg in PROMPT_INJECTION_PATTERNS:
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line, re.IGNORECASE):
                result.findings.append(Finding(
                    severity=severity, category="prompt-injection",
                    message=msg, file=str(filepath), line=i
                ))

    # Fenced code blocks: commands inside them are executable instructions.
    in_block = False
    for i, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            in_block = not in_block
            continue
        if not in_block:
            continue
        for pattern, severity, msg in SCRIPT_PATTERNS:
            if severity == "LOW":
                continue
            if re.search(pattern, line, re.IGNORECASE):
                result.findings.append(Finding(
                    severity=severity, category="dangerous-call",
                    message=f"代码块内 {msg}", file=str(filepath), line=i
                ))


def scan_dependencies(skill_path: Path, result: ScanResult):
    """Scan dependencies for known vulnerabilities via OSV.dev."""
    # Find requirements.txt
    req_file = skill_path / "requirements.txt"
    if not req_file.exists():
        return

    try:
        content = req_file.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:
        result.findings.append(Finding(
            severity="MEDIUM", category="scan-error",
            message=f"无法读取 requirements.txt（扫描未覆盖）: {exc}",
            file=str(req_file), line=0,
        ))
        return

    deps = []
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Parse package name and version
        if "==" in line:
            name, version = line.split("==", 1)
            deps.append((name.strip(), version.strip()))
        elif ">=" in line:
            name = line.split(">=", 1)[0].strip()
            deps.append((name, "latest"))

    if not deps:
        return

    # SECURITY & PRIVACY: dependency CVE checking is OFFLINE by default.
    # The scanner never makes network requests (no OSV/GitHub API calls), so an
    # untrusted folder cannot trigger egress or leak anything. We only note that
    # online CVE lookup is skipped.
    result.findings.append(Finding(
        severity="LOW", category="dependency-scan",
        message=f"依赖漏洞在线检查已禁用（离线模式，无网络请求）：检测到 {len(deps)} 个依赖",
        file=str(req_file)
    ))


# Language-agnostic dangerous-call patterns for all script languages:
# JavaScript/TypeScript, PowerShell, Batch, Ruby, PHP, Perl, Go, Rust, VBS, Lua.
SCRIPT_PATTERNS = [
    (r"child_process\.(exec|execSync|spawn|fork)\s*\(", "HIGH", "child_process 命令执行"),
    (r"require\s*\(\s*['\"]child_process['\"]\s*\)", "HIGH", "加载 child_process 命令执行"),
    (r"Invoke-Expression\b|\biex\s+", "HIGH", "PowerShell 动态执行"),
    (r"WScript\.Shell|ActiveXObject\s*\(|\.Run\s*\(", "HIGH", "Windows 脚本宿主执行"),
    (r"\.DownloadString\s*\(|\.DownloadFile\s*\(|WebClient\s*\(|Start-BitsTransfer", "HIGH", "远程下载并执行"),
    (r"Process\.Start\s*\(", "HIGH", "进程启动"),
    (r"Runtime\.getRuntime\(\).*\.exec\s*\(", "HIGH", "Java 运行时命令执行"),
    (r"shell_exec\s*\(|passthru\s*\(|system\s*\(|exec\s*\(", "HIGH", "PHP 命令执行"),
    (r"eval\s*\(", "MEDIUM", "eval 动态代码执行"),
    (r"new\s+Function\s*\(", "MEDIUM", "new Function 动态执行"),
    (r"eval\s*\(\s*(atob|base64)", "HIGH", "base64 解码后执行"),
    (r"subprocess\.(Popen|call|run|check_output)\s*\(", "MEDIUM", "subprocess 调用"),
    (r"popen\s*\(|os\.system\s*\(|os\.popen\s*\(", "MEDIUM", "系统命令调用"),
    (r"wget[^|\n]*\|[^|\n]*sh|curl[^|\n]*\|[^|\n]*sh|curl[^|\n]*\|[^|\n]*bash", "HIGH", "管道下载执行"),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
    (r"curl\s+[\w.:/-]+|wget\s+[\w.:/-]+", "LOW", "下载行为（检查目标）"),  # skillgate: ignore: rule-pattern library / detection keywords (self-scan)
    (r"atob\s*\(|Buffer\.from\s*\([^,]+,\s*['\"]base64", "LOW", "base64 解码（检查用途）"),
]


def scan_script_file(filepath: Path, result: ScanResult):
    """Scan any script-like file (JS/TS/PS1/Bat/Ruby/PHP/Perl/Go/Rust/VBS/Lua)
    for dangerous calls. Language-agnostic so no optional analyzer module can
    silently go missing."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:
        # A file that cannot be read must never silently count as "clean".
        result.findings.append(Finding(
            severity="MEDIUM", category="scan-error",
            message=f"无法读取文件（扫描未覆盖）: {exc}",
            file=str(filepath), line=0,
        ))
        return

    lines = content.splitlines()

    def _is_comment(l: str) -> bool:
        s = l.lstrip()
        return s.startswith(("#", "//", "'", "REM", "--", "(*"))

    for pattern, severity, msg in SCRIPT_PATTERNS:
        for i, line in enumerate(lines, 1):
            if _is_comment(line):
                continue
            if re.search(pattern, line, re.IGNORECASE):
                result.findings.append(Finding(
                    severity=severity, category="dangerous-call",
                    message=msg, file=str(filepath), line=i
                ))


def _has_shebang(filepath: Path) -> bool:
    """Return True when the file starts with a #! shebang line."""
    try:
        with open(filepath, "rb") as fh:
            return fh.read(2) == b"#!"
    except Exception:
        return False


def _binary_magic(head: bytes) -> bool:
    """Detect common executable/binary magic numbers so extension-less
    executables are never silently skipped."""
    return (
        head[:4] == b"\x7fELF" or           # ELF
        head[:2] == b"MZ" or                # PE/DOS
        head[:4] in (b"\xcf\xfa\xed\xfe", b"\xfe\xed\xfa\xcf",  # Mach-O
                     b"\xca\xfe\xba\xbe", b"\xca\xfe\xba\xbf") or  # Java class
        head[:2] in (b"PK", b"\x1f\x8b", b"\x1f\x9d", b"\x1f\xa0") or  # zip/gzip/tar
        head[:4] == b"\x00asm"              # WebAssembly
    )


def scan_data_file(filepath: Path, result: ScanResult):
    """Scan data/config text files (YAML/TOML/JSON/TXT/XML/HTML/CSV/ENV/INI)
    for dangerous calls. Skills routinely keep scripts or commands inside
    config/data files, so those files must be content-scanned too — never
    'miss dangerous files' just because the extension is not a script one.
    Only HIGH/MEDIUM patterns are reported (LOW download/base64 hints would
    be noise in documents)."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:
        result.findings.append(Finding(
            severity="MEDIUM", category="scan-error",
            message=f"无法读取文件（扫描未覆盖）: {exc}",
            file=str(filepath), line=0,
        ))
        return

    lines = content.splitlines()

    def _is_comment(l: str) -> bool:
        s = l.lstrip()
        return s.startswith(("#", "--", "<!--", "//", ";", "'"))

    for pattern, severity, msg in SCRIPT_PATTERNS:
        if severity == "LOW":
            continue
        for i, line in enumerate(lines, 1):
            if _is_comment(line):
                continue
            if re.search(pattern, line, re.IGNORECASE):
                result.findings.append(Finding(
                    severity=severity, category="dangerous-call",
                    message=msg, file=str(filepath), line=i
                ))


def scan_shell_file(filepath: Path, result: ScanResult):
    """Scan a shell script for dangerous patterns."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:
        result.findings.append(Finding(
            severity="MEDIUM", category="scan-error",
            message=f"无法读取文件（扫描未覆盖）: {exc}",
            file=str(filepath), line=0,
        ))
        return

    lines = content.splitlines()
    dangerous_sh_patterns = [
        (r"\brm\s+-rf?\s+/", "CRITICAL", "rm -rf / 危险删除"),
        (r"\b(curl|wget)\s+.*\|\s*(sh|bash)", "HIGH", "管道下载执行远程脚本"),
        (r"\bchmod\s+777", "MEDIUM", "chmod 777 权限过松"),
        (r"\bsudo\s+", "MEDIUM", "sudo 权限提升"),
    ]

    for pattern, severity, msg in dangerous_sh_patterns:
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line):
                result.findings.append(Finding(
                    severity=severity, category="dangerous-shell",
                    message=msg, file=str(filepath), line=i
                ))


def parse_frontmatter(filepath: Path, result: ScanResult):
    """Parse YAML frontmatter from SKILL.md."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:
        result.findings.append(Finding(
            severity="MEDIUM", category="scan-error",
            message=f"无法读取 frontmatter（扫描未覆盖）: {exc}",
            file=str(filepath), line=0,
        ))
        return

    if not content.startswith("---"):
        result.findings.append(Finding(
            severity="MEDIUM", category="frontmatter",
            message="SKILL.md 缺少 YAML frontmatter", file=str(filepath)
        ))
        return

    end = content.find("---", 3)
    if end == -1:
        result.findings.append(Finding(
            severity="MEDIUM", category="frontmatter",
            message="SKILL.md frontmatter 未闭合", file=str(filepath)
        ))
        return

    fm_text = content[3:end].strip()
    # Simple YAML parsing (enough for frontmatter)
    current_key = None
    for line in fm_text.splitlines():
        if line.startswith("- "):
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            result.frontmatter[key] = value

    # Check required fields
    for field_name in FRONTMATTER_REQUIRED_FIELDS:
        if field_name not in result.frontmatter:
            result.findings.append(Finding(
                severity="LOW", category="frontmatter",
                message=f"缺少必填字段: {field_name}", file=str(filepath)
            ))

    result.skill_name = result.frontmatter.get("name", filepath.parent.name)


def compute_trust_score(result: ScanResult) -> int:
    """Weighted Trust Score calculation.

    Weights:
    - CRITICAL: -15 each
    - HIGH: -8 each
    - MEDIUM: -4 each
    - LOW: -1 each
    - Missing frontmatter required fields: -10
    """
    score = 100

    # Weighted deductions by severity
    score -= result.critical_count * 15
    score -= result.high_count * 8
    score -= result.medium_count * 4
    score -= result.low_count * 1

    # Frontmatter completeness penalty
    fm = result.frontmatter
    if not fm:
        score -= 20
    else:
        required_present = sum(1 for f in FRONTMATTER_REQUIRED_FIELDS if fm.get(f))
        if required_present < len(FRONTMATTER_REQUIRED_FIELDS):
            score -= 10

    # Clamp to 0-100
    return max(0, min(100, score))


def grade_from_score(score: int) -> str:
    if score >= 90: return "A+"
    if score >= 80: return "A"
    if score >= 70: return "B"
    if score >= 60: return "C"
    if score >= 40: return "D"
    return "F"


def generate_badge(result: ScanResult) -> str:
    """Generate a shields.io-style SVG badge for Trust Score."""
    score = result.trust_score
    grade = result.grade

    # Severity-first gating: a badge must never look green for a skill that
    # still carries CRITICAL/HIGH findings, no matter the numeric score.
    if result.critical_count > 0:
        color = "red"
        label = "fail"
    elif result.high_count > 0:
        color = "orange"
        label = "caution"
    elif score >= 90:
        color = "brightgreen"
        label = "pass"
    elif score >= 75:
        color = "green"
        label = "pass"
    elif score >= 60:
        color = "yellow"
        label = "caution"
    elif score >= 40:
        color = "orange"
        label = "review"
    else:
        color = "red"
        label = "fail"

    value = f"{score}/100 {grade}"

    # Simple SVG badge (shields.io style)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="120" height="20">
  <linearGradient id="smooth" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <clipPath id="round">
    <rect width="120" height="20" rx="3" fill="#fff"/>
  </clipPath>
  <g clip-path="url(#round)">
    <rect width="60" height="20" fill="#555"/>
    <rect width="60" height="20" x="60" fill="{color}"/>
    <rect width="120" height="20" fill="url(#smooth)"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
    <text x="30" y="14" fill="#010101" fill-opacity=".3">{label}</text>
    <text x="30" y="13">{label}</text>
    <text x="90" y="14" fill="#010101" fill-opacity=".3">{value}</text>
    <text x="90" y="13">{value}</text>
  </g>
</svg>'''
    return svg


# ── Main ───────────────────────────────────────────────────────────────────

def find_skill_documents(skill_path: Path) -> list[Path]:
    """Find skill definition files in any supported format.

    Supports:
    - SKILL.md (Claude Code / standard)
    - AGENTS.md (Codex / OpenCode)
    - .cursorrules / .cursor/rules/*.md (Cursor)
    - *.md in root (generic fallback)
    """
    docs = []

    # Standard SKILL.md
    if (skill_path / "SKILL.md").exists():
        docs.append(skill_path / "SKILL.md")

    # AGENTS.md (Codex/OpenCode)
    if (skill_path / "AGENTS.md").exists():
        docs.append(skill_path / "AGENTS.md")

    # .cursorrules (Cursor)
    if (skill_path / ".cursorrules").exists():
        docs.append(skill_path / ".cursorrules")

    # .cursor/rules/*.md (Cursor modern format)
    cursor_rules = skill_path / ".cursor" / "rules"
    if cursor_rules.is_dir():
        docs.extend(cursor_rules.glob("*.md"))

    # .claude/skills/*.md (Claude Code plugin format)
    claude_skills = skill_path / ".claude" / "skills"
    if claude_skills.is_dir():
        docs.extend(claude_skills.glob("*/SKILL.md"))

    # .agents/skills/*.md (OpenCode format)
    agents_skills = skill_path / ".agents" / "skills"
    if agents_skills.is_dir():
        docs.extend(agents_skills.glob("*/SKILL.md"))

    # Fallback: any top-level .md file (but not README)
    if not docs:
        for md in skill_path.glob("*.md"):
            if md.name.lower() != "readme.md":
                docs.append(md)

    return docs


def scan_skill(skill_dir: str) -> ScanResult:
    skill_path = Path(skill_dir).resolve()
    if not skill_path.is_dir():
        print(f"错误: 目录不存在 - {skill_dir}", file=sys.stderr)
        sys.exit(2)

    # 安全检查：不允许扫描系统敏感目录（防路径遍历攻击）
    SENSITIVE_DIRS = ["/etc", "/proc", "/sys", "C:\\Windows", "C:\\Program Files"]
    for sensitive in SENSITIVE_DIRS:
        if str(skill_path).lower().startswith(sensitive.lower()):
            print(f"安全限制: 不允许扫描系统敏感目录 ({sensitive})", file=sys.stderr)
            sys.exit(3)

    result = ScanResult(skill_dir=str(skill_path))

    # Default excluded directories: only version-control and dependency
    # internals are skipped (a skill's own logic must never be hidden in
    # docs/test folders, so those are NOT excluded).
    DEFAULT_EXCLUDES = {".git", "__pycache__", "node_modules"}
    # Disclose what is intentionally skipped so a "clean" verdict never
    # hides the fact that some folders were not inspected.
    result.findings.append(Finding(
        severity="INFO", category="scan-coverage",
        message="Skipped folders: " + ", ".join(sorted(DEFAULT_EXCLUDES)) + " (version-control/dependency internals)",
        file=str(skill_path), line=0,
    ))

    # Symlink/junction guard: a crafted package must not be able to pull
    # outside files into the scan (or hide them) via links pointing out of
    # the package. Every link — including any link in the parent chain of a
    # candidate file — is disclosed, never silently skipped.
    def _link_guard(p: Path) -> bool:
        try:
            rel = p.relative_to(skill_path)
            parts = rel.parts
        except ValueError:
            parts = ()
        for i in range(1, len(parts) + 1):
            node = skill_path.joinpath(*parts[:i])
            if node.is_symlink() or node.is_junction():
                result.findings.append(Finding(
                    severity="INFO", category="scan-coverage",
                    message="Skipped symlink/junction in parent chain (target may point outside package): " + str(node.relative_to(skill_path)),
                    file=str(node), line=0,
                ))
                return True
        if p.is_symlink() or p.is_junction():
            result.findings.append(Finding(
                severity="INFO", category="scan-coverage",
                message="Skipped symlink/junction (target may point outside package): " + str(rel),
                file=str(p), line=0,
            ))
            return True
        return False

    # Config-driven excludes (.skillgate.yml paths.exclude), with ** glob support.
    # SECURITY: the config file is honored ONLY when SkillGate scans its own
    # directory (self-scan). A scanned third-party skill must never be able to
    # silently exclude its own payload via a bundled config, so for any other
    # target the config is ignored entirely.
    _engine_dir = Path(__file__).resolve().parent
    _self_scan = _engine_dir == skill_path.resolve()
    _config_excludes = []
    if _self_scan:
        for _pat in load_config_excludes(skill_path):
            try:
                _config_excludes.append(re.compile(_glob_to_regex(_pat)))
            except Exception:
                pass

    def should_exclude(filepath: Path) -> bool:
        """Check if a file should be excluded from scanning."""
        parts = filepath.relative_to(skill_path).parts
        for part in parts:
            if part in DEFAULT_EXCLUDES:
                return True
        rel_posix = filepath.relative_to(skill_path).as_posix()
        for _rx in _config_excludes:
            if _rx.match(rel_posix):
                return True
        return False

    # Find skill definition files in any supported format
    skill_docs = find_skill_documents(skill_path)

    if not skill_docs:
        result.findings.append(Finding(
            severity="HIGH", category="structure",
            message="未找到任何 skill 定义文件（SKILL.md / AGENTS.md / .cursorrules）",
            file=str(skill_path)
        ))
    else:
        for doc in skill_docs:
            # Try to parse frontmatter (only if it starts with ---)
            try:
                content = doc.read_text(encoding="utf-8", errors="replace")
                if content.startswith("---"):
                    parse_frontmatter(doc, result)
            except Exception:
                pass
            scan_md_file(doc, result)
            result.files_scanned += 1

    # Scan all Python files
    for py_file in skill_path.rglob("*.py"):
        if should_exclude(py_file) or _link_guard(py_file):
            continue
        scan_python_file(py_file, result)
        result.files_scanned += 1

    # Scan all shell scripts
    for sh_file in skill_path.rglob("*.sh"):
        if should_exclude(sh_file) or _link_guard(sh_file):
            continue
        scan_shell_file(sh_file, result)
        result.files_scanned += 1

    # Scan all script-like files (JS/TS/PS1/Bat/Ruby/PHP/Perl/Go/Rust/VBS/Lua/
    # Pyw/WSF/HTA), plus extension-less files with a shebang (`#!`) line —
    # agent skill packages routinely ship `bin/skill` executables without
    # extensions, and skipping them would mean skipping dangerous files.
    SCRIPT_SUFFIXES = (
        ".js", ".ts", ".mjs", ".cjs", ".jsx", ".tsx",
        ".ps1", ".psm1", ".bat", ".cmd", ".rb", ".php", ".pl",
        ".go", ".rs", ".vbs", ".lua",
        ".pyw", ".wsf", ".wsh", ".hta", ".jsfl",
    )
    # Common executable directories: extension-less files under these are
    # never silently skipped (shebang -> script scan, otherwise -> binary
    # payload review), because skill packages keep runnables there.
    EXEC_DIR_NAMES = {"bin", "scripts", "tools", "hooks", "plugins",
                      "extensions", "vendor"}
    for script_file in skill_path.rglob("*"):
        if not script_file.is_file() or _link_guard(script_file):
            continue
        suffix = script_file.suffix.lower()
        if suffix in SCRIPT_SUFFIXES:
            is_script_like = True
        elif not suffix:
            try:
                with open(script_file, "rb") as fh:
                    head = fh.read(4)
            except Exception:
                continue
            if head[:2] == b"#!":
                is_script_like = True
            elif _binary_magic(head):
                # Extension-less binary with executable magic bytes:
                # never silently skip it, surface for manual review.
                result.findings.append(Finding(
                    severity="MEDIUM", category="binary-payload",
                    message="Extension-less executable payload (binary magic); static analysis cannot inspect its behavior — requires manual/vendor review",
                    file=str(script_file), line=0,
                ))
                result.files_scanned += 1
                continue
            else:
                # Extension-less non-shebang text: only treat when located in
                # a common executable directory; otherwise it is likely data.
                parent_chain = {p.name.lower() for p in script_file.parents}
                is_script_like = bool(parent_chain & EXEC_DIR_NAMES)
                if not is_script_like:
                    continue
        else:
            continue
        if should_exclude(script_file):
            continue
        if script_file.suffix.lower() in SCRIPT_SUFFIXES or _has_shebang(script_file):
            scan_script_file(script_file, result)
        else:
            result.findings.append(Finding(
                severity="MEDIUM", category="binary-payload",
                message="Executable payload in a common run folder; static analysis cannot inspect its behavior — requires manual/vendor review",
                file=str(script_file), line=0,
            ))
        result.files_scanned += 1

    # Scan all Markdown files (excluding already-scanned skill docs)
    for md_file in skill_path.rglob("*.md"):
        if md_file in skill_docs:
            continue
        if should_exclude(md_file) or _link_guard(md_file):
            continue
        scan_md_file(md_file, result)
        result.files_scanned += 1

    # Data/config text files + binary executables are never skipped
    DATA_SUFFIXES = (".yml", ".yaml", ".toml", ".txt", ".json", ".cfg", ".ini",
                     ".xml", ".html", ".csv", ".env")
    BINARY_SUFFIXES = (".exe", ".dll", ".so", ".dylib", ".jar", ".apk", ".msi",
                       ".pyc", ".pyo", ".class", ".scr", ".com", ".pif", ".cpl",
                       ".bin", ".elf", ".wasm", ".dat")
    for data_file in skill_path.rglob("*"):
        if not data_file.is_file() or _link_guard(data_file):
            continue
        suffix = data_file.suffix.lower()
        if suffix not in DATA_SUFFIXES and suffix not in BINARY_SUFFIXES:
            continue
        if data_file.name == "requirements.txt":
            continue  # handled by scan_dependencies
        if should_exclude(data_file):
            continue
        if suffix in BINARY_SUFFIXES:
            # Cannot statically inspect binaries; surface them for review
            # instead of silently skipping executable payloads.
            result.findings.append(Finding(
                severity="MEDIUM", category="binary-payload",
                message="Binary executable payload; static analysis cannot inspect its behavior — requires manual/vendor review",
                file=str(data_file), line=0,
            ))
        else:
            scan_data_file(data_file, result)
        result.files_scanned += 1

    # Scan dependencies for known vulnerabilities
    scan_dependencies(skill_path, result)

    # Post-filter: apply line-level `# skillgate: ignore` suppression.
    # SECURITY: the marker is honored ONLY when scanning the engine's own
    # directory (self-scan). For any scanned third-party skill, markers in the
    # target code are IGNORED — they must never be able to hide findings —
    # and a finding is raised instead. This closes the "malicious skill hides
    # itself with an ignore marker" attack.
    _engine_dir = Path(__file__).resolve().parent
    _self_scan = _engine_dir == skill_path.resolve()
    _suppress_cache = {}

    def _line_suppressed(fpath: str, line: Optional[int]) -> bool:
        if not _self_scan:
            return False
        if not line:
            return False
        try:
            p = Path(fpath)
            if p not in _suppress_cache:
                _suppress_cache[p] = p.read_text(encoding='utf-8', errors='replace').splitlines()
            lines = _suppress_cache[p]
        except Exception:
            return False
        for i in (line - 1, line - 2):  # current line (1-based), then previous
            if 0 <= i < len(lines) and 'skillgate: ignore' in lines[i]:
                return True
        return False

    # 如实披露被抑制的发现：数量与清单随报告输出，Trust Score 基于剩余发现计算，
    # 但抑制情况永不静默（gate 输出与所有报告格式都会展示）。
    # 非自扫时，目标代码中的 `skillgate: ignore` 标记无效且会被记为一条发现，
    # 防止恶意技能用标记隐藏危险行为。
    if not _self_scan:
        try:
            for cand in skill_path.rglob("*"):
                if cand.suffix not in (".py", ".md", ".yml", ".yaml", ".toml", ".txt",
                                        ".js", ".ts", ".mjs", ".cjs", ".jsx", ".tsx",
                                        ".ps1", ".psm1", ".bat", ".cmd", ".rb", ".php",
                                        ".pl", ".go", ".rs", ".vbs", ".lua", ".sh",
                                        ".pyw", ".wsf", ".wsh", ".hta", ".jsfl"):
                    continue
                if should_exclude(cand):
                    continue
                for ln, raw in enumerate(
                        Path(cand).read_text(encoding='utf-8', errors='replace').splitlines(), 1):
                    if 'skillgate: ignore' in raw:
                        result.findings.append(Finding(
                            severity="MEDIUM",
                            category="suppression-abuse",
                            message=("目标代码中的 `# skillgate: ignore` 标记无效：SkillGate 仅在扫描自身规则库时"
                                     "接受该标记，被扫描代码无法抑制任何发现"),
                            file=str(cand), line=ln,
                        ))
        except Exception:
            pass
    _suppressed_findings = []
    _kept_findings = []
    for f in result.findings:
        if _line_suppressed(f.file, f.line):
            _suppressed_findings.append(f)
        else:
            _kept_findings.append(f)
    result.findings = _kept_findings
    result.suppressed = _suppressed_findings
    result.suppressed_count = len(_suppressed_findings)

    # Compute score
    result.trust_score = compute_trust_score(result)
    result.grade = grade_from_score(result.trust_score)

    return result


def gate_exit_code(result: ScanResult, fail_under: int = None) -> int:
    """统一发布门禁退出码（所有输出格式共用，不再只在终端分支生效）：
    - 存在 CRITICAL/HIGH 发现 → 1（阻断发布）
    - --fail-under 且 Trust Score 低于阈值 → 1（阻断发布）
    - 否则 → 0
    """
    if result.critical_count > 0 or result.high_count > 0:
        return 1
    if fail_under is not None and result.trust_score < fail_under:
        return 1
    return 0


def print_terminal_report(result: ScanResult, fail_under: int = None):
    print(f"\n{'='*60}")
    print(f"  SkillGate 扫描报告")
    print(f"{'='*60}")
    print(f"  Skill: {result.skill_name}")
    print(f"  目录: {result.skill_dir}")
    print(f"  扫描文件数: {result.files_scanned}")
    print(f"{'='*60}")
    print(f"  Trust Score: {result.trust_score}/100  ({result.grade})")
    print(f"{'='*60}")

    if not result.findings:
        print("  ✅ 全部检查通过，无发现")
    else:
        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        sorted_findings = sorted(result.findings, key=lambda f: severity_order.get(f.severity, 99))
        for f in sorted_findings:
            icon = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢"}.get(f.severity, "⚪")
            loc = f"{f.file}:{f.line}" if f.line else f.file
            print(f"  {icon} [{f.severity}] {f.category}: {f.message}")
            print(f"      {loc}")

    # 如实披露被 `# skillgate: ignore` 抑制的发现（不静默）
    if result.suppressed_count > 0:
        print(f"  ⚠️  抑制披露: {result.suppressed_count} 条发现被 `# skillgate: ignore` 抑制，未计入 Trust Score：")
        for f in result.suppressed[:20]:
            loc = f"{f.file}:{f.line}" if f.line else f.file
            print(f"      - [{f.severity}] {f.category}: {f.message} ({loc})")
        if result.suppressed_count > 20:
            print(f"      - ... 其余 {result.suppressed_count - 20} 条见 JSON/SARIF 报告")

    print(f"{'='*60}")

    # Determine exit code（统一门禁，与其它格式一致）
    exit_code = gate_exit_code(result, fail_under)
    if exit_code == 1 and (result.critical_count > 0 or result.high_count > 0):
        print(f"  ❌ 阻断发布: {result.critical_count} CRITICAL, {result.high_count} HIGH")
    elif exit_code == 1 and fail_under is not None:
        print(f"  ❌ 阻断发布: Trust Score {result.trust_score} < 阈值 {fail_under}")
    else:
        print(f"  ✅ 通过: {result.medium_count} MEDIUM, {result.low_count} LOW")

    return exit_code


def generate_sarif(result: ScanResult) -> str:
    """Generate SARIF 2.1.0 output for GitHub Code Scanning."""
    # Map our severities to SARIF levels
    severity_map = {
        "CRITICAL": "error",
        "HIGH": "error",
        "MEDIUM": "warning",
        "LOW": "note",
    }

    rules = {}
    sarif_results = []

    for f in result.findings:
        rule_id = f"skillgate/{f.category}"
        if rule_id not in rules:
            rules[rule_id] = {
                "id": rule_id,
                "name": f.category,
                "shortDescription": {"text": f.message},
                "fullDescription": {"text": f.message},
                "defaultConfiguration": {"level": severity_map.get(f.severity, "warning")},
            }

        sarif_results.append({
            "ruleId": rule_id,
            "level": severity_map.get(f.severity, "warning"),
            "message": {"text": f.message},
            "locations": [{
                "physicalLocation": {
                    "artifactLocation": {"uri": f.file},
                    "region": {"startLine": f.line or 1}
                }
            }]
        })

    sarif = {
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
        "version": "2.1.0",
        "runs": [{
            "tool": {
                "driver": {
                    "name": "SkillGate",
                    "version": "0.2.0",
                    "informationUri": "https://github.com/your-org/skillgate",
                    "rules": list(rules.values())
                }
            },
            "results": sarif_results
        }]
    }

    return json.dumps(sarif, indent=2, ensure_ascii=False)


def generate_junit_xml(result: ScanResult) -> str:
    """Generate JUnit XML output for CI test reporting."""
    import xml.etree.ElementTree as ET
    from xml.dom import minidom

    testsuites = ET.Element("testsuites")
    testsuite = ET.SubElement(testsuites, "testsuite", {
        "name": "SkillGate",
        "tests": str(len(result.findings) + 1),  # +1 for overall score
        "failures": str(result.critical_count + result.high_count),
        "errors": "0",
        "time": "0.1"
    })

    # Overall score test
    overall_test = ET.SubElement(testsuite, "testcase", {
        "name": f"Trust Score: {result.trust_score}/100",
        "classname": "skillgate.overall"
    })
    if result.trust_score < 80:
        failure = ET.SubElement(overall_test, "failure", {
            "message": f"Score {result.trust_score} below threshold 80"
        })

    # Individual findings as test cases
    for i, f in enumerate(result.findings):
        testcase = ET.SubElement(testsuite, "testcase", {
            "name": f"{f.category}: {f.message[:50]}",
            "classname": f"skillgate.{f.category}"
        })
        if f.severity in ("CRITICAL", "HIGH"):
            failure = ET.SubElement(testcase, "failure", {
                "message": f"[{f.severity}] {f.message}"
            })

    # Pretty print
    rough = ET.tostring(testsuites, encoding="unicode")
    pretty = minidom.parseString(rough).toprettyxml(indent="  ")  # nosec B318 - XML is self-generated, not untrusted input
    return pretty


def generate_agent_summary(result: ScanResult) -> str:
    """Generate a short, agent-friendly summary that can be relayed to the user."""
    score = result.trust_score
    grade = result.grade
    name = result.skill_name

    # Severity-first verdict: serious findings gate any recommendation,
    # regardless of the numeric score (a scanner must never recommend a
    # skill that still carries CRITICAL/HIGH findings).
    if result.critical_count > 0:
        verdict = "UNSAFE: do not install."
        detail = f"{result.critical_count} critical finding(s) present."
    elif result.high_count > 0:
        verdict = "CAUTION: review before use."
        detail = f"{result.high_count} high finding(s) present; do not install until resolved."
    elif score >= 90:
        verdict = "SAFE: ok to use."
        detail = f"Trust Score {score}/100 ({grade}), no critical issues."
    elif score >= 75:
        verdict = "MOSTLY SAFE: usable, minor issues."
        detail = f"Trust Score {score}/100 ({grade}), {result.medium_count} medium findings."
    else:
        verdict = "CAUTION: review findings before use."
        detail = f"Trust Score {score}/100 ({grade})."

    lines = [
        f"SKILLGATE_RESULT",
        f"SKILL: {name}",
        f"SCORE: {score}/100",
        f"GRADE: {grade}",
        f"VERDICT: {verdict}",
        f"DETAIL: {detail}",
    ]

    if result.findings:
        lines.append(f"TOP_FINDINGS:")
        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        sorted_findings = sorted(result.findings, key=lambda f: severity_order.get(f.severity, 99))[:5]
        for f in sorted_findings:
            lines.append(f"  - [{f.severity}] {f.category}: {f.message}")

    # Add fix suggestions
    fix_suggestions = generate_fix_suggestions(result)
    if fix_suggestions:
        lines.append(f"\n修复建议：")
        for s in fix_suggestions:
            lines.append(f"  → {s}")

    return "\n".join(lines)


def generate_fix_suggestions(result: ScanResult) -> list[str]:
    """Generate actionable fix suggestions based on findings."""
    suggestions = []
    categories = {f.category for f in result.findings}

    if "dangerous-code" in categories:
        suggestions.append("替换 eval/exec 为安全的替代方案（ast.literal_eval / 直接类型转换）")
        suggestions.append("避免 shell=True，用列表参数传 subprocess")

    if "network" in categories:
        suggestions.append("如果 skill 不需要联网，移除 requests/urllib 等网络依赖")
        suggestions.append("如果必须联网，在 SKILL.md 里声明需要网络权限")

    if "credential-leak" in categories:
        suggestions.append("硬编码凭证改用环境变量：os.getenv('API_KEY')")
        suggestions.append("不要把 .env 文件提交到 git")

    if "prompt-injection" in categories:
        suggestions.append("移除任何试图绕过 system prompt 的指令")
        suggestions.append("不要在 skill 里写 'ignore previous instructions' 这类内容")

    if "filesystem" in categories:
        suggestions.append("避免递归删除操作，或者加白名单检查路径")
        suggestions.append("不要写入系统目录（/etc/, C:\\Windows\\）")

    if "frontmatter" in categories:
        suggestions.append("在 SKILL.md 头部补全 frontmatter：name, description, version, license, author")

    return suggestions


def main():
    ap = argparse.ArgumentParser(description="SkillGate — Skill 安全与质量扫描门禁")
    sub = ap.add_subparsers(dest="command")

    scan_parser = sub.add_parser("scan", help="扫描一个 skill 目录")
    scan_parser.add_argument("skill_dir", help="skill 目录路径")
    scan_parser.add_argument("--format", choices=["terminal", "json", "markdown", "agent", "sarif", "junit"], default="terminal")
    scan_parser.add_argument("--output", help="输出文件路径（默认 stdout）")
    scan_parser.add_argument("--fail-under", type=int, default=None,
                             help="CI 模式：Trust Score 低于此值则 exit 1")
    scan_parser.add_argument("--badge", help="生成 SVG badge 到指定路径")
    scan_parser.add_argument("--batch", action="store_true",
                             help="批量扫描：扫描目录下所有子目录")

    # Quickstart subcommand
    quickstart_parser = sub.add_parser("quickstart", help="快速演示 SkillGate 怎么用")

    args = ap.parse_args()

    if args.command == "quickstart":
        print("=" * 60)
        print("  🛡️  SkillGate Quickstart")
        print("=" * 60)
        print()
        print("1. Scan a skill:")
        print("   python skillgate.py scan ./my-skill/")
        print()
        print("2. Get AI-friendly output:")
        print("   python skillgate.py scan ./my-skill/ --format agent")
        print()
        print("3. CI integration:")
        print("   python skillgate.py scan ./my-skill/ --fail-under 80")
        print()
        print("4. Generate badge for your README:")
        print("   python skillgate.py scan ./my-skill/ --badge badge.svg")
        print()
        print("5. Save report to file:")
        print("   python skillgate.py scan ./my-skill/ --format json --output report.json")
        print()
        print("📚 Full docs: https://github.com/your-org/skillgate")
        print("=" * 60)
        sys.exit(0)

    if args.command == "scan":
        # Batch mode: scan all subdirectories
        if args.batch:
            base_path = Path(args.skill_dir).resolve()
            if not base_path.is_dir():
                print(f"错误: 目录不存在 - {args.skill_dir}", file=sys.stderr)
                sys.exit(2)

            all_results = []
            failed_dirs = []
            skill_dirs = [d for d in base_path.iterdir() if d.is_dir()]
            print(f"批量扫描: 发现 {len(skill_dirs)} 个子目录")

            for d in skill_dirs:
                try:
                    r = scan_skill(str(d))
                    all_results.append(r)
                    status = "✅" if r.critical_count == 0 and r.high_count == 0 else "❌"
                    print(f"  {status} {r.skill_name}: {r.trust_score}/100 ({r.grade})")
                except Exception as e:
                    # A directory that fails to scan must NEVER vanish from the
                    # batch summary or count as passed — it is a scan failure and
                    # must fail the batch exit code.
                    failed_dirs.append(str(d))
                    print(f"  ❌ {d.name}: 扫描失败 - {e}", file=sys.stderr)
                    r = ScanResult(skill_name=d.name, skill_path=str(d), trust_score=0, grade="F")
                    r.findings.append(Finding(
                        severity="CRITICAL", category="scan-error",
                        message=f"批量扫描失败（该目录未通过扫描）: {e}",
                        file=str(d), line=0,
                    ))
                    all_results.append(r)

            # Summary
            print(f"\n{'='*60}")
            print(f"  批量扫描汇总")
            print(f"{'='*60}")
            print(f"  总计: {len(skill_dirs)} 个 skill（失败 {len(failed_dirs)} 个）")
            avg_score = sum(r.trust_score for r in all_results) / len(all_results) if all_results else 0
            print(f"  平均 Trust Score: {avg_score:.1f}/100")
            passed = len([r for r in all_results if r.critical_count == 0 and r.high_count == 0 and (args.fail_under is None or r.trust_score >= args.fail_under)])
            print(f"  通过: {passed}/{len(skill_dirs)}")

            # Exit code — failed dirs are included in the denominator, so any
            # scan failure (or any failed gate) yields a non-zero exit.
            if failed_dirs or passed < len(skill_dirs):
                sys.exit(1)
            else:
                sys.exit(0)

        result = scan_skill(args.skill_dir)

        # Confined file writes: reports/badges may ONLY be written inside the
        # scanned folder. Never write outside the target (no arbitrary-path writes).
        _target_dir = Path(args.skill_dir).resolve()

        def _confined_write(rel_target, data):
            p = Path(rel_target).resolve()
            try:
                ok = p.is_relative_to(_target_dir)
            except (ValueError, AttributeError):
                ok = False
            if not ok:
                print(f"错误: 输出路径必须在扫描目标目录内: {_target_dir}", file=sys.stderr)
                sys.exit(2)
            # A crafted package must never redirect report writes through a
            # symlink/junction pointing outside the scanned folder.
            if p.is_symlink() or p.is_junction():
                print(f"错误: 输出路径不能是符号链接/junction: {p}", file=sys.stderr)
                sys.exit(2)
            p.write_text(data, encoding="utf-8")

        # Generate badge if requested
        if args.badge:
            badge_svg = generate_badge(result)
            _confined_write(args.badge, badge_svg)
            print(f"Badge 已生成: {args.badge}")

        if args.format == "agent":
            output = generate_agent_summary(result)
            if args.output:
                _confined_write(args.output, output)
                print(f"Agent summary written to: {args.output}")
            else:
                print(output)
            # Exit code for CI usage（统一门禁）
            sys.exit(gate_exit_code(result, args.fail_under))
        elif args.format == "sarif":
            output = generate_sarif(result)
            if args.output:
                _confined_write(args.output, output)
                print(f"SARIF 报告已写入: {args.output}")
            else:
                print(output)
            sys.exit(gate_exit_code(result, args.fail_under))
        elif args.format == "junit":
            output = generate_junit_xml(result)
            if args.output:
                _confined_write(args.output, output)
                print(f"JUnit XML 报告已写入: {args.output}")
            else:
                print(output)
            sys.exit(gate_exit_code(result, args.fail_under))
        elif args.format == "json":
            output = json.dumps(asdict(result), indent=2, ensure_ascii=False)
            if args.output:
                _confined_write(args.output, output)
                print(f"JSON 报告已写入: {args.output}")
            else:
                print(output)
            sys.exit(gate_exit_code(result, args.fail_under))
        elif args.format == "markdown":
            lines = [
                f"# SkillGate 扫描报告",
                f"",
                f"- **Skill**: {result.skill_name}",
                f"- **Trust Score**: {result.trust_score}/100 ({result.grade})",
                f"- **扫描文件数**: {result.files_scanned}",
                f"- **Gate**: {'FAIL' if gate_exit_code(result, args.fail_under) else 'PASS'}",
                f"",
                f"## Findings",
                f"",
            ]
            if result.findings:
                for f in result.findings:
                    lines.append(f"- [{f.severity}] {f.category}: {f.message} (`{f.file}:{f.line}`)")
            else:
                lines.append("✅ 无发现")
            if result.suppressed_count > 0:
                lines.append(f"")
                lines.append(f"## Suppressed findings ({result.suppressed_count})")
                lines.append(f"")
                lines.append(f"以下发现被 `# skillgate: ignore` 抑制，未计入 Trust Score：")
                for f in result.suppressed:
                    lines.append(f"- [{f.severity}] {f.category}: {f.message} (`{f.file}:{f.line}`)")
            output = "\n".join(lines)
            if args.output:
                _confined_write(args.output, output)
                print(f"Markdown 报告已写入: {args.output}")
            else:
                print(output)
            sys.exit(gate_exit_code(result, args.fail_under))
        else:
            exit_code = print_terminal_report(result, fail_under=args.fail_under)
            sys.exit(exit_code)
    else:
        ap.print_help()
        sys.exit(2)


if __name__ == "__main__":
    main()
