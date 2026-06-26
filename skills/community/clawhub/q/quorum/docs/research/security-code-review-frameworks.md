# Security Code Review Frameworks: Reference for LLM-Based Security Critics

**Purpose:** Ground an LLM security critic's evaluation criteria in established frameworks.  
**Scope:** Code-level and architecture-level security analysis for Python and PowerShell.  
**Sources:** OWASP ASVS 5.0.0, CWE Top 25 (2024), OWASP Code Review Guide v2, SEI CERT Standards, NIST SP 800-53 Rev5 SA-11.  
**Last updated:** 2026-03-06

---

## Table of Contents

1. [OWASP ASVS 5.0.0 — Verification Categories and Levels](#1-owasp-asvs-500)
2. [CWE Top 25 (2024) — Dangerous Weakness Taxonomy](#2-cwe-top-25-2024)
3. [OWASP Code Review Guide — Review Categories](#3-owasp-code-review-guide)
4. [SEI CERT Secure Coding Standards](#4-sei-cert-secure-coding-standards)
5. [NIST SP 800-53 SA-11 — Developer Testing and Evaluation](#5-nist-sp-800-53-sa-11)
6. [Cross-Reference and LLM Critic Coverage Map](#6-cross-reference-and-coverage-map)

---

## 1. OWASP ASVS 5.0.0

**Version:** 5.0.0 (May 2025) — significant restructure from 4.0  
**Total requirements:** ~350, across 17 chapters  
**Reference:** https://github.com/OWASP/ASVS/tree/v5.0.0

### 1.1 Three Assurance Levels

| Level | Focus | Requirement Count | Typical Applicability |
|-------|-------|-------------------|----------------------|
| **L1** | Critical/baseline — first-layer defenses against common attacks that need no preconditions | ~20% of requirements (~70 reqs) | All applications; minimum viable security |
| **L2** | Standard — less common attacks, more complex protections, some preconditions needed | ~50% of requirements (~175 reqs; L2 compliance requires L1+L2 ≈ 70% total) | Most business applications, any app handling sensitive data |
| **L3** | Defense-in-depth — hard-to-implement controls, highest assurance | ~30% of requirements (~105 reqs; full compliance = all ~350) | Banking, healthcare, high-value targets |

**Key insight for LLM critic:** L1 requirements are largely detectable by static analysis + LLM pattern recognition. L2 requires context-aware reasoning. L3 often requires runtime/architecture knowledge.

### 1.2 Verification Chapters (ASVS 5.0.0)

> **Note:** ASVS 5.0 restructured from the 14-chapter 4.0 schema. The new schema has 17 chapters. Chapter numbers/titles below are from v5.0.0.

| Chapter | Title | Primary Focus | Code-Level? | LLM-Reviewable? |
|---------|-------|---------------|-------------|-----------------|
| **V1** | Encoding and Sanitization | Output encoding, injection prevention (XSS, SQL, OS, LDAP, XML) | ✅ Yes | ✅ High |
| **V2** | Validation and Business Logic | Input validation, data type constraints, business rule enforcement | ✅ Yes | ✅ High |
| **V3** | Web Frontend Security | CSP, Subresource Integrity, DOM XSS, iframe security | ⚠️ Mixed | ⚠️ Medium |
| **V4** | API and Web Service | REST/GraphQL security, request/response validation, API keys | ✅ Yes | ✅ High |
| **V5** | File Handling | Upload validation, path traversal, safe extraction | ✅ Yes | ✅ High |
| **V6** | Authentication | Password policies, MFA, credential storage, brute force | ✅ Yes | ✅ High |
| **V7** | Session Management | Token generation, expiry, fixation, logout | ✅ Yes | ✅ High |
| **V8** | Authorization | Access control, IDOR, privilege escalation, RBAC/ABAC | ✅ Yes | ✅ High |
| **V9** | Self-Contained Tokens | JWT security (alg confusion, signature validation, claims) | ✅ Yes | ✅ High |
| **V10** | OAuth and OIDC | Authorization flows, PKCE, state parameter, token exchange | ⚠️ Mixed | ⚠️ Medium |
| **V11** | Cryptography | Algorithm selection, key management, RNG, deprecation | ✅ Yes | ✅ High |
| **V12** | Secure Communication | TLS configuration, certificate validation, HSTS | ⚠️ Mixed | ⚠️ Medium |
| **V13** | Configuration | Security headers, error handling, secrets in config | ✅ Yes | ✅ High |
| **V14** | Data Protection | Sensitive data handling, PII, data classification, caching | ✅ Yes | ✅ High |
| **V15** | Secure Coding and Architecture | Dependency management, SSRF prevention, sandboxing | ✅ Yes | ✅ High |
| **V16** | Security Logging and Error Handling | Log content, error messages, audit trails | ✅ Yes | ✅ High |
| **V17** | WebRTC | Media security, signaling, peer auth (niche) | ❌ Specialized | ❌ Low |

### 1.3 Requirement Type Classification

**Documentation requirements** (what must be decided and documented) appear in chapter section `X.1.*` — these are architecture/process level.

**Implementation requirements** (what code must do) appear in `X.2.*` and beyond — these are code-level.

For an LLM critic focused on code review:
- **High value:** V1 (injection), V2 (validation), V4 (API), V5 (file), V6 (auth), V8 (authz), V9 (tokens), V11 (crypto), V13 (config), V14 (data), V15 (secure coding), V16 (logging)
- **Partial value:** V3 (if reviewing HTML templates), V10 (if reviewing OAuth flows)
- **Low value for code review:** V17 (WebRTC-specific)

---

## 2. CWE Top 25 (2024)

**Source:** https://cwe.mitre.org/top25/archive/2024/2024_cwe_top25.html  
**Dataset:** 31,770 CVE records  
**Scoring:** Frequency × severity (CVSS) normalized score

### 2.1 Full Ranked List

| Rank | CWE ID | Name | SAST? | Dyn? | LLM? |
|------|--------|------|-------|------|------|
| 1 | CWE-79 | Cross-site Scripting (XSS) — improper input neutralization during web page generation | ✅ | ✅ | ✅ |
| 2 | CWE-787 | Out-of-bounds Write | ✅ | ✅ | ⚠️ |
| 3 | CWE-89 | SQL Injection — special elements in SQL commands | ✅ | ✅ | ✅ |
| 4 | CWE-352 | Cross-Site Request Forgery (CSRF) | ⚠️ | ✅ | ✅ |
| 5 | CWE-22 | Path Traversal — improper pathname restriction | ✅ | ✅ | ✅ |
| 6 | CWE-125 | Out-of-bounds Read | ✅ | ✅ | ⚠️ |
| 7 | CWE-78 | OS Command Injection | ✅ | ✅ | ✅ |
| 8 | CWE-416 | Use After Free | ✅ | ✅ | ❌ |
| 9 | CWE-862 | Missing Authorization | ⚠️ | ✅ | ✅ |
| 10 | CWE-434 | Unrestricted Upload of Dangerous File Type | ✅ | ✅ | ✅ |
| 11 | CWE-94 | Code Injection — improper code generation control | ✅ | ✅ | ✅ |
| 12 | CWE-20 | Improper Input Validation | ⚠️ | ✅ | ✅ |
| 13 | CWE-77 | Command Injection — special elements in commands | ✅ | ✅ | ✅ |
| 14 | CWE-287 | Improper Authentication | ⚠️ | ✅ | ✅ |
| 15 | CWE-269 | Improper Privilege Management | ⚠️ | ✅ | ✅ |
| 16 | CWE-502 | Deserialization of Untrusted Data | ✅ | ✅ | ✅ |
| 17 | CWE-200 | Exposure of Sensitive Information to Unauthorized Actor | ⚠️ | ✅ | ✅ |
| 18 | CWE-863 | Incorrect Authorization | ⚠️ | ✅ | ✅ |
| 19 | CWE-918 | Server-Side Request Forgery (SSRF) | ✅ | ✅ | ✅ |
| 20 | CWE-119 | Improper Restriction of Memory Buffer Operations | ✅ | ✅ | ❌ |
| 21 | CWE-476 | NULL Pointer Dereference | ✅ | ✅ | ❌ |
| 22 | CWE-798 | Use of Hard-coded Credentials | ✅ | ❌ | ✅ |
| 23 | CWE-190 | Integer Overflow or Wraparound | ✅ | ✅ | ⚠️ |
| 24 | CWE-400 | Uncontrolled Resource Consumption (DoS) | ⚠️ | ✅ | ✅ |
| 25 | CWE-306 | Missing Authentication for Critical Function | ⚠️ | ✅ | ✅ |

**Legend:** ✅ = primary detection method | ⚠️ = partial/depends on context | ❌ = rarely applies (not applicable language or needs runtime)

### 2.2 Detection Method Analysis

**Reliably detectable by SAST alone:**
- CWE-89 (SQL injection pattern matching), CWE-78/77 (OS command injection), CWE-22 (path traversal), CWE-94 (eval/exec patterns), CWE-79 (output encoding), CWE-798 (hardcoded secrets via regex), CWE-502 (deserialization calls), CWE-919 (SSRF — URL construction patterns)

**Require LLM semantic reasoning (SAST insufficient):**
- CWE-862/863 (authorization logic — requires understanding of access control intent)
- CWE-287 (authentication — requires understanding of authentication flow)
- CWE-306 (missing auth — requires understanding what "critical" means contextually)
- CWE-269 (privilege management — requires understanding role/permission models)
- CWE-400 (resource consumption — requires understanding amplification paths)
- CWE-200 (info exposure — requires understanding data sensitivity classification)
- CWE-352 (CSRF — token presence and binding requires flow analysis)
- CWE-20 (input validation — context-dependent completeness)

**Primarily memory safety (not Python/PowerShell):**
- CWE-787, CWE-125, CWE-416, CWE-119, CWE-476, CWE-190 (C/C++ domain; Python/PS have GC, no raw memory)

### 2.3 Python-Specific CWE Manifestations

| CWE | Python Pattern | Example |
|-----|---------------|---------|
| CWE-89 | String formatting in SQL | `cursor.execute(f"SELECT * FROM users WHERE name='{name}'")` |
| CWE-78 | `os.system()`, `subprocess` without shell=False | `os.system(f"ping {host}")` |
| CWE-77 | `subprocess.run(cmd, shell=True)` | Any shell=True with user input |
| CWE-94 | `eval()`, `exec()`, `compile()` with user input | `eval(user_expression)` |
| CWE-22 | `open()` with unsanitized paths | `open(f"/data/{user_file}")` |
| CWE-502 | `pickle.loads()`, `yaml.load()` (not safe_load) | `pickle.loads(request.data)` |
| CWE-798 | Hardcoded API keys/passwords in source | `password = "admin123"` |
| CWE-918 | `requests.get(user_url)` without validation | SSRF via external URL |
| CWE-400 | Unbounded loops, regex ReDoS | `re.match('^(a+)+$', user_input)` |
| CWE-502 | `marshal`, `shelve`, `jsonpickle` | Any deserialize from untrusted source |

### 2.4 PowerShell-Specific CWE Manifestations

| CWE | PowerShell Pattern | Example |
|-----|-------------------|---------|
| CWE-89 | String concat in Invoke-SqlCmd | `Invoke-Sqlcmd -Query "SELECT * FROM t WHERE id='$id'"` |
| CWE-78 | `Invoke-Expression`, `&` operator with user input | `Invoke-Expression $userInput` |
| CWE-94 | `Invoke-Expression`, `[ScriptBlock]::Create()` | `IEX $cmd` (common PS abbrev) |
| CWE-22 | `Get-Content`, `Set-Content` with unsanitized paths | `Get-Content "C:\data\$file"` |
| CWE-798 | ConvertTo-SecureString with plaintext in script | `$pw = ConvertTo-SecureString "pass" -AsPlainText -Force` |
| CWE-502 | `ConvertFrom-Json` on untrusted + deserialize net objects | Deserializing .NET types from untrusted JSON |
| CWE-287 | Skipping certificate validation | `[System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}` |
| CWE-200 | Write-Host, Write-Output of sensitive data | Logging credentials to stdout |

---

## 3. OWASP Code Review Guide

**Current version:** v2.0 (2017) — still widely referenced  
**PDF:** https://owasp.org/www-project-code-review-guide/assets/OWASP_Code_Review_Guide_v2.pdf  
**Structure:** Two major sections — (1) Why/how of code reviews; (2) Vulnerability types with examples

### 3.1 Major Review Categories

The guide organizes reviews around the OWASP Top 10 (2013 era) plus additional categories:

| Category | Key Items to Check |
|----------|--------------------|
| **Input Validation** | All user-controlled inputs sanitized; whitelist vs blacklist; data type enforcement |
| **Output Encoding** | Context-sensitive encoding (HTML, JS, URL, CSS, SQL); templating engine escaping |
| **Authentication** | Password hashing (bcrypt/argon2), credential transmission, session token strength |
| **Session Management** | Token generation entropy, expiry, binding, cookie attributes (HttpOnly, Secure, SameSite) |
| **Access Control** | Enforce authz server-side; avoid client-side-only checks; least privilege |
| **Cryptography** | Approved algorithms, key length, key storage, IV/nonce handling, RNG |
| **Error Handling** | No stack traces to users; sanitized error messages; consistent error structure |
| **Logging** | Audit logs for security events; no sensitive data in logs; log injection prevention |
| **Data Protection** | Encryption at rest/transit; no cleartext secrets; PII handling |
| **File Management** | Extension allow-listing, size limits, storage outside webroot, antivirus |
| **Memory Management** | Buffer bounds, null checks (less relevant for Python/PS but applies to C extensions) |
| **Third-Party Components** | Known vulnerabilities in dependencies (SCA); license risk |
| **Configuration** | Debug mode off in prod; secrets in env vars not code; least-privilege runtime accounts |

### 3.2 Python-Specific Review Checklist

- **Template injection:** Are Jinja2/Mako templates using autoescaping? User data in template strings?
- **Pickle deserialization:** Any use of `pickle`, `shelve`, `marshal`, `jsonpickle` with external data?
- **YAML loading:** `yaml.load()` (unsafe) vs `yaml.safe_load()` — full class deserialization risk
- **eval/exec:** Any `eval()`, `exec()`, `compile()` with user-influenced strings
- **subprocess calls:** `shell=True` with user input; prefer `shell=False` with list args
- **SQL queries:** Parameterized queries? SQLAlchemy text() with bound params?
- **Path construction:** `os.path.join()` not sufficient alone; need `os.path.abspath()` + chroot check
- **Request library:** External URLs validated before fetching (SSRF)
- **XML parsing:** `defusedxml` used? `lxml` with `resolve_entities=False`?
- **Hash algorithms:** `hashlib.md5()`/`sha1()` for passwords? Use `hashlib.pbkdf2_hmac()` or `bcrypt`
- **Random:** `random.random()` for security vs `secrets` module
- **Debug mode:** Flask `app.run(debug=True)` in production?
- **Environment variables:** Secrets read from `os.environ` not hardcoded
- **Type annotations:** Not a security control but helps catch type confusion bugs

### 3.3 PowerShell-Specific Review Checklist

- **Execution policy bypass:** `-ExecutionPolicy Bypass` or `Unrestricted` in scripts?
- **Invoke-Expression / IEX:** Any use with external or user-controlled input
- **Script block logging:** Are PSScriptBlockLogging and transcription enabled?
- **AMSI bypass attempts:** `[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils')` patterns
- **Certificate validation:** `[Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}` or `-SkipCertificateCheck`
- **Credential handling:** `ConvertTo-SecureString -AsPlainText -Force` with literals; `Get-Credential` vs hardcoded
- **Constrained Language Mode:** Is the script designed to run in CLM? Does it bypass CLM?
- **Download cradles:** `(New-Object Net.WebClient).DownloadString()`, `IEX (iwr ...)` — legitimate vs malicious
- **COM object use:** `New-Object -ComObject Shell.Application` etc. — privilege/sandbox implications
- **SQL injection:** Any `Invoke-Sqlcmd`, ADO.NET calls with string concatenation
- **Registry operations:** Writing to `HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run` or similar
- **Secrets in scripts:** API keys, passwords, connection strings in plaintext
- **Pipeline injection:** User-controlled data flowing into downstream cmdlets without sanitization

---

## 4. SEI CERT Secure Coding Standards

**Organization:** Software Engineering Institute, Carnegie Mellon University  
**Wiki:** https://wiki.sei.cmu.edu/confluence/display/seccode/  
**Structure:** Rules (must-fix) + Recommendations (should-fix), organized by category prefix

### 4.1 Covered Languages

| Language | Status | Published Book? | Notes |
|----------|--------|-----------------|-------|
| **C** | Full standard | Yes (2016 Ed.) | Most mature; reference implementation |
| **C++** | Full standard | Yes (2016 Ed.) | Extends C standard |
| **Java** | Full standard | Yes | Enterprise Java coverage |
| **Perl** | Partial standard | No | Wiki-only |
| **Android (Java)** | Partial standard | No | Mobile-specific extensions |
| **Python** | ❌ Not covered | No | No official CERT Python standard |
| **PowerShell** | ❌ Not covered | No | Not in CERT scope |

**Key gap:** CERT does not have Python or PowerShell standards. The principles transfer, but there is no official mapping. For Python/PS code review, use OWASP resources instead.

### 4.2 CERT Rule Category Structure

Rules follow `XXX-C-NNN` format (e.g., `MEM30-C`, `STR31-C`):

| Prefix | Category | Python/PS Relevance |
|--------|----------|---------------------|
| **ARR** | Arrays | Low (no C arrays) |
| **CON** | Concurrency | Medium (threading, asyncio, race conditions) |
| **DCL** | Declarations and Initialization | Medium (variable shadowing, scope) |
| **ENV** | Environment | High (env vars, PATH, POSIX interface) |
| **ERR** | Error Handling | High (exception handling, error propagation) |
| **EXP** | Expressions | Medium (operator precedence, side effects) |
| **FIO** | File I/O | High (path validation, file descriptors, permissions) |
| **INT** | Integers | Low (Python arbitrary precision; PS Int32 overflow possible) |
| **MEM** | Memory Management | Low (GC languages) |
| **MSC** | Miscellaneous | High (random, time, type confusion) |
| **POS** | POSIX | High (for Python scripts interacting with OS) |
| **PRE** | Preprocessor | N/A |
| **SIG** | Signals | Low |
| **STR** | Strings | High (encoding, format strings, injection) |

### 4.3 CERT Principles Applicable to Python/PS (by Analogy)

Even without official standards, these CERT principles map directly:

| CERT Rule | Language | Python Analog | PowerShell Analog |
|-----------|----------|---------------|-------------------|
| STR02-C: Sanitize data passed to complex subsystems | C | Sanitize before `subprocess`, `os.system` | Sanitize before `Invoke-Expression` |
| FIO02-C: Canonicalize path names from untrusted sources | C | `os.path.realpath()` before file ops | `Resolve-Path` before file ops |
| MSC02-C: Defend against injection | C | Parameterized DB queries | Parameterized SQL in ADO.NET |
| MSC30-C: Do not use rand() for security | C | Use `secrets` not `random` | Use `[System.Security.Cryptography.RNGCryptoServiceProvider]` |
| ERR00-C: Adopt and implement a consistent error handling policy | C | Consistent exception handling | Consistent `try/catch`, `$ErrorActionPreference` |
| ENV33-C: Do not call system() | C | Avoid `os.system()` | Avoid `Invoke-Expression` with input |
| CON01-C: Acquire and release resources in same thread | C | `with` statement, context managers | `try/finally` patterns |

---

## 5. NIST SP 800-53 SA-11

**Control family:** SA — System and Services Acquisition  
**Revision:** 5 (current)  
**Full text:** https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final

### 5.1 SA-11 Base Control Statement

> Require the developer of the system, system component, or system service, at all post-design stages of the system development life cycle, to:
> - Develop and implement a plan for ongoing security and privacy control assessments
> - Perform [unit/integration/system/regression] testing/evaluation at [organization-defined frequency] and [organization-defined depth and coverage]
> - Produce evidence of the execution of the assessment plan and the results of testing and evaluation
> - Implement a verifiable flaw remediation process
> - Correct flaws identified during testing and evaluation

**Baseline:** Included in Moderate and High baselines (SA family)

### 5.2 SA-11 Sub-Controls (Enhancements)

All enhancements are **not part of any baseline** (overlays/tailored additions):

| Enhancement | Name | Code Review Relevance | LLM Critic Relevance |
|-------------|------|----------------------|---------------------|
| **SA-11(1)** | Static Code Analysis | Employ SAST tools; document results | **High** — defines the SAST mandate LLM supplements |
| **SA-11(2)** | Threat Modeling and Vulnerability Analyses | Threat model during development, define tools/methods | **Medium** — LLM can augment threat modeling |
| **SA-11(3)** | Independent Verification of Assessment Plans | Independent agent verifies assessment | **High** — LLM-as-critic is a form of independent assessment |
| **SA-11(4)** | Manual Code Reviews | Manual review of specified code with defined procedures | **High** — LLM directly supplements/automates manual review |
| **SA-11(5)** | Penetration Testing | Pen test with defined breadth/depth/constraints | Low — runtime testing, not code review |
| **SA-11(6)** | Attack Surface Reviews | Review attack surface | **Medium** — LLM can identify and assess attack surface from code |
| **SA-11(7)** | Verify Scope of Testing and Evaluation | Verify complete control coverage | **Medium** — LLM can assess coverage completeness |
| **SA-11(8)** | Dynamic Code Analysis | DAST tools; document results | Low — requires running application |
| **SA-11(9)** | Interactive Application Security Testing (IAST) | IAST tools during execution | Low — requires runtime instrumentation |

### 5.3 What SA-11 Means for an LLM Security Critic

SA-11 provides the **normative mandate** for the activities an LLM critic participates in:
- SA-11(1) → LLM critic supplements SAST where static analysis has false negatives
- SA-11(4) → LLM critic IS a form of automated manual code review
- SA-11(3) → LLM critic provides independent verification when separated from the development team
- SA-11(6) → LLM critic can enumerate the attack surface systematically from code structure

An LLM security critic that documents its findings against these sub-controls can claim SA-11 alignment.

---

## 6. Cross-Reference and Coverage Map

### 6.1 Framework Overlap Matrix

| Security Domain | ASVS Chapter | CWE Top 25 | OWASP CRG | CERT Category | SA-11 Enhancement |
|----------------|-------------|-----------|-----------|---------------|-------------------|
| Injection (SQL, OS, Code) | V1, V2 | 3, 7, 11, 13 | Input Validation, Output Encoding | STR, ENV | SA-11(1), SA-11(4) |
| Authentication | V6 | 14, 25 | Authentication | ERR, MSC | SA-11(4) |
| Authorization | V8 | 9, 18 | Access Control | — | SA-11(4), SA-11(6) |
| Session Management | V7 | — | Session Management | — | SA-11(4) |
| Cryptography | V11 | — | Cryptography | MSC | SA-11(1), SA-11(4) |
| Path Traversal / File | V5 | 5, 10 | File Management | FIO | SA-11(1), SA-11(4) |
| XSS | V1, V3 | 1 | Output Encoding | STR | SA-11(1) |
| CSRF | V3 | 4 | Session Management | — | SA-11(4) |
| Deserialization | V2, V15 | 16 | Input Validation | — | SA-11(1), SA-11(4) |
| SSRF | V4, V15 | 19 | — | — | SA-11(4) |
| Secrets / Hardcoded Creds | V13 | 22 | Configuration | ENV | SA-11(1) |
| Error Handling / Logging | V16 | — | Error Handling, Logging | ERR | SA-11(4) |
| Supply Chain / Dependencies | V15 | — | Third-Party | — | SA-11(2) |
| Tokens (JWT/OAuth) | V9, V10 | — | — | — | SA-11(4) |
| Input Validation (general) | V2 | 12, 20 | Input Validation | — | SA-11(1) |
| Privilege / Priv Management | V8 | 15 | Access Control | — | SA-11(4), SA-11(6) |
| Resource Consumption (DoS) | V4 | 24 | — | CON | SA-11(4) |
| Memory Safety | — | 2, 6, 8, 20, 21, 23 | Memory Mgmt | MEM, INT, ARR | SA-11(1) |
| Info Disclosure | V14 | 17 | Data Protection | — | SA-11(4) |

### 6.2 SAST vs. LLM Detection Capability

| Detection Category | SAST Tools | LLM Critic | Notes |
|-------------------|------------|------------|-------|
| Hardcoded secrets/credentials | ✅ Excellent | ✅ Good | Regex-based; SAST covers most; LLM catches obfuscated variants |
| SQL injection (string concat) | ✅ Excellent | ✅ Good | Pattern matching reliable; LLM helps with dynamic query builders |
| OS command injection (literal) | ✅ Good | ✅ Good | `shell=True`, `Invoke-Expression` patterns |
| Path traversal | ✅ Good | ✅ Good | `open()` with unsanitized paths |
| Unsafe deserialization | ✅ Good | ✅ Good | `pickle.loads`, `yaml.load` |
| eval/exec with user input | ✅ Good | ✅ Good | Direct pattern match |
| XSS (output encoding) | ✅ Good | ⚠️ Medium | Context-dependent; LLM needed for novel contexts |
| SSRF | ✅ Partial | ✅ Good | SAST misses indirect URL construction |
| Insecure crypto (algo choice) | ✅ Good | ✅ Good | `MD5`, `SHA1` for passwords, DES, RC4 |
| **Missing authorization** | ❌ Poor | ✅ Excellent | Requires semantic understanding of access control intent |
| **Incorrect authorization logic** | ❌ Poor | ✅ Excellent | Business logic; SAST cannot understand role models |
| **Authentication bypass** | ❌ Poor | ✅ Good | Flow analysis; SAST misses logical bypasses |
| **Business logic flaws** | ❌ None | ✅ Good | LLM's primary unique contribution |
| **Missing input validation** | ❌ Poor | ✅ Good | Completeness checking requires semantic reasoning |
| CSRF token presence/binding | ❌ Poor | ✅ Good | Requires understanding form/request flow |
| Error message information disclosure | ⚠️ Partial | ✅ Good | SAST catches obvious; LLM catches contextual |
| Resource consumption / DoS | ❌ Poor | ⚠️ Medium | Amplification paths need flow reasoning |
| Supply chain / dependency risk | ✅ Excellent (SCA) | ❌ Poor | SCA tools; LLM has no real-time vuln DB |
| Memory safety | ✅ Good | ❌ Poor | Not relevant for Python/PS; C/C++ domain |
| JWT/token misuse | ✅ Partial | ✅ Excellent | `alg=none`, key confusion — pattern + semantic |
| Privilege escalation paths | ❌ None | ✅ Good | Requires understanding permission model |

### 6.3 Unique Contributions by Framework

| Framework | What It Adds That Others Don't |
|-----------|-------------------------------|
| **ASVS** | Hierarchical levels (L1/L2/L3) enabling severity-stratified review; documentation requirement concept; most comprehensive web app requirement list; JWT/OAuth-specific chapters |
| **CWE Top 25** | Empirically weighted by real CVE prevalence; KEV (exploited in wild) subset for prioritization; memory safety domain coverage |
| **OWASP CRG** | Language-practical "what to look for" guidance; reviewer checklist mentality; most actionable for line-by-line review |
| **SEI CERT** | Formal rule taxonomy for C/C++/Java; language-specific undefined behavior coverage; most rigorous for compiled languages |
| **NIST SA-11** | Normative mandate that positions code review within SDLC; provides sub-control vocabulary for compliance framing; authorization citation for LLM-as-independent-reviewer |

### 6.4 Minimum Viable Coverage for a Framework-Grounded LLM Security Critic

To claim credible framework alignment, an LLM security critic should cover at minimum:

**Tier 1 — Must Cover (SAST complement, highest-value LLM contribution):**
1. **Authorization logic** (ASVS V8, CWE-862, CWE-863) — LLM's biggest unique advantage
2. **Authentication completeness** (ASVS V6, CWE-287, CWE-306)
3. **Input validation completeness** (ASVS V2, CWE-20) — not just pattern, but semantic coverage
4. **Injection family** (ASVS V1, CWE-78, CWE-89, CWE-77, CWE-94) — LLM handles indirect/obfuscated patterns
5. **Secrets and credential handling** (ASVS V13, CWE-798)

**Tier 2 — Should Cover (high value, detectable by LLM):**
6. **Cryptographic misuse** (ASVS V11) — wrong algorithm, weak key, bad RNG
7. **Deserialization** (ASVS V2, CWE-502)
8. **SSRF** (ASVS V4/V15, CWE-918)
9. **Path traversal and file handling** (ASVS V5, CWE-22, CWE-434)
10. **JWT/token security** (ASVS V9, CWE-287 subset)
11. **Error handling and information disclosure** (ASVS V16, CWE-200)

**Tier 3 — Framework Citation Coverage (for compliance framing):**
12. **CSRF** (CWE-352, ASVS V3)
13. **Session management** (ASVS V7)
14. **Logging adequacy** (ASVS V16)
15. **Third-party dependency awareness** (ASVS V15) — flag for SCA, don't solve

**Skip for Python/PS code review (not applicable):**
- Memory safety (CWE-787, CWE-125, CWE-416, CWE-119, CWE-476, CWE-190) — C/C++ domain
- CERT standards (no Python/PS editions)
- WebRTC (ASVS V17) — niche

### 6.5 Citation Vocabulary for LLM Critic Findings

When an LLM critic reports findings, it can ground them as:

```
Finding: [Description]
Framework References:
  - ASVS 5.0.0 §[chapter].[section].[requirement] (Level [1/2/3])
  - CWE-[ID]: [Name]
  - OWASP Code Review Guide: [Category]
  - NIST SP 800-53 SA-11([enhancement])
Severity: [Critical/High/Medium/Low]
Detection Method: [LLM semantic analysis | Pattern match | Architecture review]
```

This citation structure satisfies SA-11(3) (independent assessment), SA-11(4) (manual code review), and SA-11(1) (static analysis) depending on detection method.

---

## Appendix: Key Sources and Version Information

| Document | Version | Date | URL |
|----------|---------|------|-----|
| OWASP ASVS | 5.0.0 | May 2025 | https://github.com/OWASP/ASVS/tree/v5.0.0 |
| CWE Top 25 | 2024 | 2024 | https://cwe.mitre.org/top25/archive/2024/ |
| OWASP Code Review Guide | 2.0 | July 2017 | https://owasp.org/www-project-code-review-guide/ |
| SEI CERT C Standard | 2016 Ed. | 2016 | https://resources.sei.cmu.edu/library/asset-view.cfm?assetID=454220 |
| SEI CERT C++ Standard | 2016 Ed. | 2016 | https://resources.sei.cmu.edu/library/asset-view.cfm?assetID=494932 |
| NIST SP 800-53 | Rev. 5 | Sep 2020 | https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final |
| NIST SP 800-53 SA-11 | Rev. 5 | Sep 2020 | https://csf.tools/reference/nist-sp-800-53/r5/sa/sa-11/ |

---

*Research compiled 2026-03-06 for Quorum security critic design.*
