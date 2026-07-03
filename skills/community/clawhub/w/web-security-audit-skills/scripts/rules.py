"""
Web 安全审计规则库 —— 覆盖 PHP / Java / Python / Go
每种语言按漏洞类型组织，每个规则包含：正则模式、严重级别、CWE 编号、描述
"""
from __future__ import annotations
import re
from dataclasses import dataclass, field
from typing import List, Dict, Pattern

# ── 通用数据结构 ──────────────────────────────────────────────
@dataclass
class AuditRule:
    rule_id: str
    category: str               # 漏洞类型
    severity: str               # Critical / High / Medium / Low
    cwe: str
    description: str
    patterns: List[Pattern]     # 正则模式列表
    file_extensions: List[str]  # 适用文件后缀

@dataclass
class Finding:
    rule: AuditRule
    file_path: str
    line_number: int
    line_content: str
    matched_pattern: str


# ── 通用 Web 漏洞规则（跨语言）─────────────────────────────────
_COMMON_PATTERNS: Dict[str, List[str]] = {
    "hardcoded_secrets": [
        # 硬编码密钥/密码/Token
        r"""(?i)(api[_\s-]?key|secret[_\s-]?key|access[_\s-]?key|private[_\s-]?key|token|password|passwd)\s*[:=]\s*['"][\w\-\.\/+=]{8,}['"]""",
        r"""(?i)(AKIA[0-9A-Z]{16})""",  # AWS Access Key
        r"""(?i)(ghp_[0-9a-zA-Z]{36})""", # GitHub Token
        r"""(?i)(sk-[0-9a-zA-Z]{48})""",  # OpenAI Key
        r"""(?i)(-----BEGIN\s(?:RSA\s)?PRIVATE\sKEY-----)""",
    ],
}

# ── PHP 规则 ───────────────────────────────────────────────────
PHP_RULES: List[AuditRule] = []

def _build_php_rules() -> List[AuditRule]:
    rules = []
    # 1) SQL Injection
    rules.append(AuditRule(
        "PHP-SQLI-001", "SQL Injection", "Critical", "CWE-89",
        "拼接用户输入到 SQL 查询，未使用参数化查询或预处理语句",
        [re.compile(p, re.IGNORECASE) for p in [
            r"""(mysql_query|mysqli_query|pg_query|sqlite_query|odbc_exec)\s*\(\s*['\"].*\$\w+""",
            r"""\$sql\s*=\s*['\"].*\$\w+.*['\"]\s*\.\s*\$""",
            r"""\$sql\s*\.=\s*\$""",
            r"""->(query|exec)\s*\(\s*['\"].*\$\w+""",
        ]],
        [".php", ".phtml", ".php3", ".php4", ".php5", ".inc"],
    ))
    # 2) XSS
    rules.append(AuditRule(
        "PHP-XSS-001", "Cross-Site Scripting (XSS)", "High", "CWE-79",
        "直接输出用户输入到 HTML 页面，未经过滤或转义",
        [re.compile(p, re.IGNORECASE) for p in [
            r"""echo\s+\$\w+""",
            r"""print\s+\$\w+""",
            r"""\bprint_r\s*\(\s*\$\w+\s*\)""",
            r"""\bdie\s*\(\s*\$\w+\s*\)""",
            r"""<[?]=.*\$_(GET|POST|REQUEST|SERVER|COOKIE)""",
        ]],
        [".php", ".phtml", ".inc"],
    ))
    # 3) Command Injection / RCE
    rules.append(AuditRule(
        "PHP-RCE-001", "Command Injection / RCE", "Critical", "CWE-78",
        "用户输入被传入系统命令执行函数",
        [re.compile(p, re.IGNORECASE) for p in [
            r"""(system|exec|shell_exec|passthru|popen|proc_open|pcntl_exec)\s*\(\s*\$""",
            r"""`\s*\$""",
            r"""\beval\s*\(\s*\$""",
            r"""\bassert\s*\(\s*\$""",
            r"""\bpreg_replace\s*\(\s*['\"].*/e['\"]""",
            r"""\bcreate_function\s*\(\s*\$""",
            r"""\binclude\s*\(\s*\$_(GET|POST|REQUEST)""",
            r"""\brequire\s*\(\s*\$_(GET|POST|REQUEST)""",
        ]],
        [".php", ".phtml", ".inc"],
    ))
    # 4) File Inclusion (LFI/RFI)
    rules.append(AuditRule(
        "PHP-LFI-001", "Local/Remote File Inclusion", "Critical", "CWE-98",
        "文件包含函数接收用户可控参数",
        [re.compile(p, re.IGNORECASE) for p in [
            r"""\b(include|require|include_once|require_once)\s*\(\s*\$_(GET|POST|REQUEST|SERVER)""",
            r"""\b(include|require|include_once|require_once)\s*\$\w+""",
            r"""\b(fopen|file_get_contents|readfile|show_source|highlight_file)\s*\(\s*\$_(GET|POST|REQUEST)""",
        ]],
        [".php", ".phtml", ".inc"],
    ))
    # 5) Deserialization
    rules.append(AuditRule(
        "PHP-DESER-001", "Insecure Deserialization", "High", "CWE-502",
        "反序列化用户可控数据",
        [re.compile(p, re.IGNORECASE) for p in [
            r"""\bunserialize\s*\(\s*\$_(GET|POST|REQUEST|COOKIE)""",
            r"""\bunserialize\s*\(\s*\$\w+""",
        ]],
        [".php", ".phtml", ".inc"],
    ))
    # 6) SSRF
    rules.append(AuditRule(
        "PHP-SSRF-001", "Server-Side Request Forgery", "High", "CWE-918",
        "用户可控 URL 被用于服务端请求",
        [re.compile(p, re.IGNORECASE) for p in [
            r"""\b(file_get_contents|curl_exec|fopen|readfile)\s*\(\s*\$_(GET|POST|REQUEST)""",
            r"""\bcurl_setopt\s*\(\s*\$ch\s*,\s*CURLOPT_URL\s*,\s*\$_(GET|POST|REQUEST)""",
        ]],
        [".php", ".phtml", ".inc"],
    ))
    # 7) File Upload
    rules.append(AuditRule(
        "PHP-UPLOAD-001", "Insecure File Upload", "High", "CWE-434",
        "文件上传功能未校验文件类型或内容",
        [re.compile(p, re.IGNORECASE) for p in [
            r"""\bmove_uploaded_file\s*\(.*\$_(FILES|GET|POST|REQUEST)""",
            r"""\$_FILES\s*\[.*\]\s*\[\s*['\"]name['\"]\s*\]""",
        ]],
        [".php", ".phtml", ".inc"],
    ))
    # 8) XXE
    rules.append(AuditRule(
        "PHP-XXE-001", "XML External Entity (XXE)", "High", "CWE-611",
        "XML 解析时未禁用外部实体加载",
        [re.compile(p, re.IGNORECASE) for p in [
            r"""\bsimplexml_load_string\s*\(\s*\$""",
            r"""\bDOMDocument\s*->\s*loadXML\s*\(\s*\$""",
            r"""libxml_disable_entity_loader\s*\(\s*false\s*\)""",
        ]],
        [".php", ".phtml", ".inc"],
    ))
    # 9) Open Redirect
    rules.append(AuditRule(
        "PHP-REDIR-001", "Open Redirect", "Medium", "CWE-601",
        "重定向目标由用户输入控制",
        [re.compile(p, re.IGNORECASE) for p in [
            r"""header\s*\(\s*['\"]Location:\s*['\"].*\$_(GET|POST|REQUEST)""",
            r"""header\s*\(\s*['\"]Location:\s*['\"]\.\s*\$""",
        ]],
        [".php", ".phtml", ".inc"],
    ))
    return rules

PHP_RULES = _build_php_rules()


# ── Java 规则 ──────────────────────────────────────────────────
JAVA_RULES: List[AuditRule] = []

def _build_java_rules() -> List[AuditRule]:
    rules = []
    ext = [".java", ".jsp", ".jspx"]
    # 1) SQL Injection
    rules.append(AuditRule(
        "JAVA-SQLI-001", "SQL Injection", "Critical", "CWE-89",
        "使用 Statement 拼接用户输入，未使用 PreparedStatement 或 ORM 参数绑定",
        [re.compile(p, re.IGNORECASE) for p in [
            r"""\.(createStatement|executeQuery|executeUpdate)\s*\(\s*['\"].*\+""",
            r"""Statement\s+\w+\s*=\s*\w+\.createStatement\s*\(\s*\)""",
            r"""\.execute\s*\(\s*['\"].*\+\s*(request\.get|@Request|@Param)""",
            r"""jdbcTemplate\.\w+\s*\(\s*['\"].*\+""",
        ]],
        ext,
    ))
    # 2) XSS
    rules.append(AuditRule(
        "JAVA-XSS-001", "Cross-Site Scripting", "High", "CWE-79",
        "未对输出到页面的用户数据进行转义",
        [re.compile(p, re.IGNORECASE) for p in [
            r"""response\.getWriter\s*\(\s*\)\s*\.\s*(print|write|println)\s*\(\s*request\.get""",
            r"""<\%=\s*request\.get""",
            r"""ModelAndView.*request\.get""",
        ]],
        ext,
    ))
    # 3) Command Injection
    rules.append(AuditRule(
        "JAVA-RCE-001", "Command Injection / RCE", "Critical", "CWE-78",
        "用户输入用于执行系统命令",
        [re.compile(p, re.IGNORECASE) for p in [
            r"""Runtime\.getRuntime\s*\(\s*\)\s*\.\s*exec\s*\(\s*request\.get""",
            r"""ProcessBuilder\s*\(\s*.*request\.get""",
            r"""\.exec\s*\(\s*['\"].*\+\s*(request\.get|@Request|@Param)""",
        ]],
        ext,
    ))
    # 4) Deserialization
    rules.append(AuditRule(
        "JAVA-DESER-001", "Insecure Deserialization", "Critical", "CWE-502",
        "反序列化不可信数据源，可能导致 RCE",
        [re.compile(p, re.IGNORECASE) for p in [
            r"""ObjectInputStream\s*\(\s*.*(request\.get|@Request)""",
            r"""\.readObject\s*\(\s*\)""",
            r"""readUnshared\s*\(\s*\)""",
            r"""XStream.*fromXML\s*\(\s*request""",
            r"""@RestController.*@PostMapping.*Serializable""",
        ]],
        ext,
    ))
    # 5) SSRF
    rules.append(AuditRule(
        "JAVA-SSRF-001", "Server-Side Request Forgery", "High", "CWE-918",
        "用户可控 URL 发起 HTTP 请求",
        [re.compile(p, re.IGNORECASE) for p in [
            r"""HttpURLConnection.*URL\s*\(\s*request\.get""",
            r"""RestTemplate.*(getFor|postFor|exchange).*request\.get""",
            r"""OkHttp.*new Request.*request\.get""",
            r"""openConnection\s*\(\s*\).*request\.get""",
        ]],
        ext,
    ))
    # 6) XXE
    rules.append(AuditRule(
        "JAVA-XXE-001", "XML External Entity", "High", "CWE-611",
        "XML 解析器未禁用外部实体",
        [re.compile(p, re.IGNORECASE) for p in [
            r"""DocumentBuilderFactory\.newInstance\s*\(\s*\)""",
            r"""SAXParserFactory\.newInstance\s*\(\s*\)""",
            r"""XMLInputFactory\.newFactory\s*\(\s*\)""",
            r"""SAXReader\s*\(\s*\)""",
        ]],
        ext,
    ))
    # 7) Path Traversal
    rules.append(AuditRule(
        "JAVA-PATH-001", "Path Traversal", "High", "CWE-22",
        "用户输入未过滤即用于文件路径拼接",
        [re.compile(p, re.IGNORECASE) for p in [
            r"""new\s+(File|FileInputStream|FileReader)\s*\(\s*request\.get""",
            r"""Files\.\w+\s*\(\s*Paths\.get\s*\(\s*request\.get""",
        ]],
        ext,
    ))
    # 8) Spring Actuator
    rules.append(AuditRule(
        "JAVA-ACT-001", "Sensitive Endpoint Exposure", "Medium", "CWE-200",
        "Actuator 端点暴露敏感信息",
        [re.compile(p, re.IGNORECASE) for p in [
            r"""management\.endpoints\.web\.exposure\.include\s*=\s*\*""",
            r"""management\.endpoint\.\w+\.enabled\s*=\s*true""",
        ]],
        [".properties", ".yml", ".yaml", ".java"],
    ))
    return rules

JAVA_RULES = _build_java_rules()


# ── Python 规则 ────────────────────────────────────────────────
PYTHON_RULES: List[AuditRule] = []

def _build_python_rules() -> List[AuditRule]:
    rules = []
    ext = [".py", ".pyw"]
    # 1) SQL Injection
    rules.append(AuditRule(
        "PY-SQLI-001", "SQL Injection", "Critical", "CWE-89",
        "字符串格式化拼接 SQL 查询，未使用参数化查询",
        [re.compile(p, re.IGNORECASE) for p in [
            r"""\.execute\s*\(\s*f['\"].*\brequest\b""",
            r"""\.execute\s*\(\s*['\"].*%\s*\(.*request""",
            r"""\.execute\s*\(\s*['\"].*\.format\s*\(.*request""",
            r"""cursor\.execute\s*\(\s*['\"].*\+.*request""",
            r"""raw\s*\(\s*['\"].*\brequest\b""",
        ]],
        ext,
    ))
    # 2) XSS (Django/Flask)
    rules.append(AuditRule(
        "PY-XSS-001", "Cross-Site Scripting", "High", "CWE-79",
        "模板中未转义用户输入或使用 mark_safe 绕过转义",
        [re.compile(p, re.IGNORECASE) for p in [
            r"""\|safe""",
            r"""mark_safe\s*\(\s*request""",
            r"""render_template_string\s*\(\s*request""",
            r"""HttpResponse\s*\(\s*request""",
        ]],
        ext + [".html", ".jinja2", ".j2"],
    ))
    # 3) Command Injection
    rules.append(AuditRule(
        "PY-RCE-001", "Command Injection / RCE", "Critical", "CWE-78",
        "用户输入传入 subprocess / os.system / eval 等危险函数",
        [re.compile(p, re.IGNORECASE) for p in [
            r"""os\.system\s*\(\s*.*request""",
            r"""os\.popen\s*\(\s*.*request""",
            r"""subprocess\.\w+\s*\(\s*.*request""",
            r"""\beval\s*\(\s*.*request""",
            r"""\bexec\s*\(\s*.*request""",
            r"""__import__\s*\(\s*.*request""",
            r"""pickle\.loads\s*\(\s*.*request""",
        ]],
        ext,
    ))
    # 4) SSTI (Server-Side Template Injection)
    rules.append(AuditRule(
        "PY-SSTI-001", "Server-Side Template Injection", "Critical", "CWE-1336",
        "用户输入直接传入模板引擎渲染",
        [re.compile(p, re.IGNORECASE) for p in [
            r"""render_template_string\s*\(\s*request""",
            r"""Template\s*\(\s*request""",
            r"""\.from_string\s*\(\s*request""",
        ]],
        ext,
    ))
    # 5) Deserialization
    rules.append(AuditRule(
        "PY-DESER-001", "Insecure Deserialization", "Critical", "CWE-502",
        "反序列化不可信数据（pickle / yaml.unsafe_load）",
        [re.compile(p, re.IGNORECASE) for p in [
            r"""pickle\.loads?\s*\(\s*request""",
            r"""yaml\.load\s*\(\s*request""",
            r"""yaml\.unsafe_load\s*\(\s*request""",
            r"""marshal\.loads\s*\(\s*request""",
        ]],
        ext,
    ))
    # 6) SSRF
    rules.append(AuditRule(
        "PY-SSRF-001", "Server-Side Request Forgery", "High", "CWE-918",
        "用户可控 URL 被用于 HTTP 请求",
        [re.compile(p, re.IGNORECASE) for p in [
            r"""requests\.(get|post|put|delete|head|patch)\s*\(\s*request""",
            r"""httpx\.(get|post)\s*\(\s*request""",
            r"""urlopen\s*\(\s*request""",
        ]],
        ext,
    ))
    # 7) Path Traversal
    rules.append(AuditRule(
        "PY-PATH-001", "Path Traversal", "High", "CWE-22",
        "用户输入用于文件路径未过滤",
        [re.compile(p, re.IGNORECASE) for p in [
            r"""open\s*\(\s*.*request""",
            r"""Path\s*\(\s*.*request""",
            r"""send_file\s*\(\s*.*request""",
            r"""send_from_directory\s*\(\s*.*request""",
        ]],
        ext,
    ))
    # 8) Hardcoded Secret (Django)
    rules.append(AuditRule(
        "PY-SECRET-001", "Hardcoded Secret Key", "High", "CWE-798",
        "Django SECRET_KEY 硬编码",
        [re.compile(p) for p in [
            r"""SECRET_KEY\s*=\s*['\"][\w\-!@#$%^&*()+=]{20,}['\"]""",
        ]],
        ext,
    ))
    return rules

PYTHON_RULES = _build_python_rules()


# ── Go 规则 ────────────────────────────────────────────────────
GO_RULES: List[AuditRule] = []

def _build_go_rules() -> List[AuditRule]:
    rules = []
    ext = [".go"]
    # 1) SQL Injection
    rules.append(AuditRule(
        "GO-SQLI-001", "SQL Injection", "Critical", "CWE-89",
        "使用 fmt.Sprintf 拼接 SQL，未使用参数占位符",
        [re.compile(p, re.IGNORECASE) for p in [
            r"""fmt\.Sprintf\s*\(\s*['\"].*SELECT.*%[sv]""",
            r"""db\.(Query|Exec|QueryRow)\s*\(\s*['\"].*\+.*(r\.|req\.|ctx\.)""",
            r"""db\.(Query|Exec|QueryRow)\s*\(\s*['\"].*%[sv].*['\"]\s*,\s*.*(r\.|req\.)""",
        ]],
        ext,
    ))
    # 2) XSS
    rules.append(AuditRule(
        "GO-XSS-001", "Cross-Site Scripting", "High", "CWE-79",
        "未转义直接写入 HTTP 响应",
        [re.compile(p, re.IGNORECASE) for p in [
            r"""w\.Write\s*\(\s*\[\]byte\s*\(\s*.*(r\.|req\.|ctx\.)""",
            r"""fmt\.Fprintf\s*\(\s*w\s*,\s*.*(r\.|req\.|ctx\.)""",
            r"""template\.HTML\s*\(\s*.*(r\.|req\.)""",
        ]],
        ext,
    ))
    # 3) Command Injection
    rules.append(AuditRule(
        "GO-RCE-001", "Command Injection / RCE", "Critical", "CWE-78",
        "用户输入用于 exec.Command",
        [re.compile(p, re.IGNORECASE) for p in [
            r"""exec\.Command\s*\(\s*.*(r\.|req\.|ctx\.)""",
            r"""exec\.CommandContext\s*\(\s*.*(r\.|req\.|ctx\.)""",
            r"""os\.Exec\s*\(\s*.*(r\.|req\.)""",
        ]],
        ext,
    ))
    # 4) SSTI
    rules.append(AuditRule(
        "GO-SSTI-001", "Server-Side Template Injection", "Critical", "CWE-1336",
        "用户输入传入模板渲染",
        [re.compile(p, re.IGNORECASE) for p in [
            r"""template\.(New|Must|ParseFiles|ParseGlob).*(r\.|req\.|ctx\.)""",
            r"""\.Execute\s*\(\s*\w+\s*,\s*.*(r\.|req\.)""",
        ]],
        ext,
    ))
    # 5) SSRF
    rules.append(AuditRule(
        "GO-SSRF-001", "Server-Side Request Forgery", "High", "CWE-918",
        "用户可控 URL 发起请求",
        [re.compile(p, re.IGNORECASE) for p in [
            r"""http\.(Get|Post|NewRequest)\s*\(\s*.*(r\.|req\.|ctx\.)""",
            r"""client\.(Get|Post|Do)\s*\(\s*.*(r\.|req\.)""",
        ]],
        ext,
    ))
    # 6) Path Traversal
    rules.append(AuditRule(
        "GO-PATH-001", "Path Traversal", "High", "CWE-22",
        "用户输入用于文件操作",
        [re.compile(p, re.IGNORECASE) for p in [
            r"""os\.Open\s*\(\s*.*(r\.|req\.|ctx\.)""",
            r"""ioutil\.ReadFile\s*\(\s*.*(r\.|req\.)""",
            r"""http\.ServeFile\s*\(\s*\w+\s*,\s*\w+\s*,\s*.*(r\.|req\.)""",
        ]],
        ext,
    ))
    return rules

GO_RULES = _build_go_rules()


# ── 跨语言通用规则 ────────────────────────────────────────────
COMMON_RULES: List[AuditRule] = []

def _build_common_rules() -> List[AuditRule]:
    rules = []
    for i, pat in enumerate(_COMMON_PATTERNS["hardcoded_secrets"]):
        rules.append(AuditRule(
            f"SECRET-{i+1:03d}", "Hardcoded Credentials", "High", "CWE-798",
            "代码中硬编码密钥、Token 或密码",
            [re.compile(pat)],
            [".php", ".java", ".py", ".go", ".js", ".ts", ".rb", ".yaml", ".yml", ".json", ".xml", ".properties"],
        ))
    return rules

COMMON_RULES = _build_common_rules()

# ── 聚合 ───────────────────────────────────────────────────────
ALL_RULES: Dict[str, List[AuditRule]] = {
    "php": PHP_RULES + COMMON_RULES,
    "java": JAVA_RULES + COMMON_RULES,
    "python": PYTHON_RULES + COMMON_RULES,
    "go": GO_RULES + COMMON_RULES,
}


def get_rules(language: str) -> List[AuditRule]:
    """获取指定语言的规则列表"""
    lang = language.lower()
    if lang in ALL_RULES:
        return ALL_RULES[lang]
    # 尝试通用兜底
    return COMMON_RULES
