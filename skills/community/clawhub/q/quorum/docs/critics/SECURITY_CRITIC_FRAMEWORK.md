# Quorum Security Critic Framework
## Unified Reference for the Security Critic

**Version:** 1.0  
**Date:** 2026-03-05  
**Scope:** Python and PowerShell code-level security evaluation  
**Grounded in:** OWASP ASVS 5.0.0, CWE Top 25 (2024), OWASP Code Review Guide v2, SEI CERT (analogical), NIST SP 800-53 SA-11, ISO/IEC 25010:2023 (Security characteristic), CISQ ASCSM  
**Companion document:** `CODE_HYGIENE_FRAMEWORK.md`

---

## Status

**v0.7.3 State:** Framework design complete. All features shipped.

- [x] Framework design and documentation
- [x] 14 evaluation categories (SEC-01–SEC-14) specified
- [x] OWASP ASVS 5.0, CWE Top 25, NIST SP 800-53 SA-11 grounding
- [x] Detection capability matrix for SAST vs LLM judgment boundaries
- [x] Full SAST tool integration (Ruff/Bandit/PSScriptAnalyzer) — shipped in pre-screen
- [x] Threat model context feeding for SEC-04 (Authorization) — `threat_context` type in relationship manifest, runtime integration shipped
- [x] Learning memory wiring (issue tracking) — shipped v0.5.3

**Known Limitations:**
- SAST rule coverage varies by language: Python ~85%+, PowerShell ~70% (tooling ecosystem gap)
- Authorization review (SEC-04) benefits from threat model context — users can define `threat_context` in the relationship manifest (roles, trust boundaries, sensitive operations)

---

## Table of Contents

1. [Evaluation Categories](#1-evaluation-categories)
2. [Python-Specific Security Checklist](#2-python-specific-security-checklist)
3. [PowerShell-Specific Security Checklist](#3-powershell-specific-security-checklist)
4. [Detection Capability Matrix](#4-detection-capability-matrix)
5. [Minimum Viable Coverage (Tier 1/2/3)](#5-minimum-viable-coverage)
6. [Framework Cross-Reference](#6-framework-cross-reference)
7. [Finding Citation Vocabulary](#7-finding-citation-vocabulary)

---

## 1. Evaluation Categories

Each category has:
- **Framework grounding**: ASVS chapter, CWE IDs, SA-11 enhancement
- **Deterministic checks**: SAST tool rules that run in pre-screen layer
- **LLM judgment checks**: what the critic evaluates that SAST cannot

---

### SEC-01: Injection (SQL, OS Command, Code, LDAP, XPath)

**ASVS 5.0.0:** V1 (Encoding and Sanitization), V2 (Validation)  
**CWE Top 25 (2024):** CWE-89 (#3), CWE-78 (#7), CWE-94 (#11), CWE-77 (#13), CWE-79 (#1)  
**CISQ ASCSM:** CWE-22, CWE-77, CWE-78, CWE-79, CWE-89, CWE-90, CWE-91, CWE-611, CWE-643, CWE-652  
**ISO 25010:** Security → Integrity  
**SA-11:** SA-11(1) Static Analysis, SA-11(4) Manual Code Review  
**Default Tier:** Tier 1

#### Deterministic Checks

**Python (Ruff/Bandit):**

| Rule | What It Catches |
|------|----------------|
| `S608` | SQL injection via string concatenation (`f"SELECT... {var}"`) |
| `S324` | MD5/SHA1 used in non-security contexts (CWE-328 — weak hash; injection-adjacent for integrity) |
| `S102` | `exec()` with user input — code injection (CWE-94) |
| `S307` | `eval()` usage — code injection (CWE-94) |
| `S603` + `S604` | `subprocess` call with `shell=True` — OS command injection (CWE-78) |
| `S605`, `S606` | Shell injection via `os.system()`, `os.popen()` |
| `S611` | `os.system()` usage — prefer `subprocess.run` |
| `S612` | `logging.config.listen()` — code injection via logging config |
| `S701`, `S702`, `S703` | Jinja2/Mako template injection (XSS/server-side template injection) |
| `S704` | Jinja2 `autoescape=False` — XSS |

**PowerShell (PSScriptAnalyzer):**

| Rule | What It Catches |
|------|----------------|
| `PSAvoidUsingInvokeExpression` | `Invoke-Expression` (IEX) — primary code injection vector (CWE-78, CWE-94) |

**Note:** PowerShell SQL injection via `Invoke-Sqlcmd` has no PSSA rule — **GAP** requiring LLM detection.

#### LLM Judgment Checks

| Check | Specific Signal to Evaluate | Why SAST Is Insufficient |
|-------|---------------------------|--------------------------|
| Indirect SQL injection | SQL built via helper functions, ORM `text()` with string format, multi-step query construction — taint analysis breaks at function boundaries | SAST taint analysis is intraprocedural; can't track across module boundaries |
| Template injection via dynamic templates | Jinja2 `Template(user_string).render()` — dynamic template compilation from user input | Requires understanding that the template itself is the attack vector, not just the render args |
| PowerShell injection via pipeline | User input flowing through pipeline into cmdlets that accept scriptblock or expression args | PSSA has no taint analysis |
| `Invoke-Expression` equivalent patterns | `&` operator with user-controlled string, `[ScriptBlock]::Create($userInput)` | PSSA only flags literal `Invoke-Expression` |
| Parameterization coverage | Is every database operation using parameterized queries or ORM-level binding? `cursor.execute()` with positional `?` is safe; with `%s` format may not be | Requires reading the DB call pattern and its argument construction in context |
| LDAP/XPath injection | Python `ldap3` queries, `lxml` XPath with user input — no Ruff/Bandit rules | No dedicated SAST rules exist |

---

### SEC-02: Input Validation & Sanitization

**ASVS 5.0.0:** V2 (Validation and Business Logic)  
**CWE Top 25 (2024):** CWE-20 (#12), CWE-434 (#10), CWE-606  
**CISQ ASCSM:** CWE-129, CWE-434, CWE-606  
**ISO 25010:** Security → Integrity; Interaction Capability → User Error Protection  
**SA-11:** SA-11(1), SA-11(4)  
**Default Tier:** Tier 1

#### Deterministic Checks

**Python:**

| Rule | What It Catches |
|------|----------------|
| `S604`, `S606` | User-controlled input to shell/exec without validation |
| `S324` | Weak hash (MD5/SHA1) for file integrity checking |

**PowerShell:**

| Rule | What It Catches |
|------|----------------|
| `PSAvoidDefaultValueSwitchParameter` | Switch parameters default `$true` — breaks expected input semantics |
| `PSAvoidDefaultValueForMandatoryParameter` | Mandatory parameter with default — contradictory input contract |

**Note:** General input validation coverage by SAST is **weak** for both languages. This is primarily an LLM domain.

#### LLM Judgment Checks

| Check | Specific Signal to Evaluate | Framework Citation |
|-------|---------------------------|-------------------|
| Whitelist vs. blacklist validation | Does the code validate against an allow-list of acceptable values, or just reject known-bad values? Blacklists are always incomplete. | OWASP CRG: Input Validation; ASVS V2 |
| Type coercion validation | Is user input validated before type conversion? `int(user_input)` without try/except is a crash; `float()` then range check is better. | ASVS V2.2.* |
| File upload validation | For any file upload path: (a) extension allow-listing, (b) content-type verification, (c) file content scanning, (d) size limits, (e) storage outside webroot | ASVS V5, CWE-434 |
| Numeric range validation | For numeric inputs: are bounds checked? Can negative values, zero, or overflow values cause logic errors? | CWE-20, CERT INT (analog) |
| Business logic validation | Does the code enforce that a user can't order -1 items, set a future birth date, or request data for a different user's account? | ASVS V2 (Business Logic) |
| PowerShell `[ValidateNotNull]`, `[ValidateSet]`, `[ValidateRange]` | Are parameter validation attributes used on public function parameters? Or is validation done ad-hoc inside the function body? | PSSA best practice (no rule) |

---

### SEC-03: Authentication

**ASVS 5.0.0:** V6 (Authentication)  
**CWE Top 25 (2024):** CWE-287 (#14), CWE-306 (#25)  
**CISQ ASCSM:** CWE-798 (credential exposure)  
**ISO 25010:** Security → Authenticity, Accountability  
**SA-11:** SA-11(4) Manual Code Review, SA-11(6) Attack Surface  
**Default Tier:** Tier 1

#### Deterministic Checks

**Python:**

| Rule | What It Catches |
|------|----------------|
| `S105`, `S106`, `S107` | Hardcoded passwords, secret keys, API tokens |
| `S323` | SSL certificate verification bypass (`verify=False`) — allows MITM attacks on auth traffic |
| `S501` | `requests.get(..., verify=False)` — same |

**PowerShell:**

| Rule | What It Catches |
|------|----------------|
| `PSAvoidUsingConvertToSecureStringWithPlainText` | `ConvertTo-SecureString -AsPlainText -Force` with literals — hardcoded creds (CWE-798) |
| `PSAvoidUsingUsernameAndPasswordParams` | String-typed username/password parameters |
| `PSAvoidUsingPlainTextForPassword` | Variable names signaling plaintext credential handling |
| `PSUsePSCredentialType` | Credential parameters not typed as `[PSCredential]` |
| `PSAvoidUsingAllowUnencryptedAuthentication` | HTTP credential transmission |

#### LLM Judgment Checks

| Check | Specific Signal to Evaluate | Framework Citation |
|-------|---------------------------|-------------------|
| Password hashing correctness | Is `bcrypt`, `argon2`, or `hashlib.pbkdf2_hmac()` used for password storage? NOT `MD5`, `SHA1`, or unsalted `SHA256`. | ASVS V6.2.*, OWASP CRG: Authentication |
| Authentication bypass paths | Are there any routes, endpoints, or code paths where authentication is conditionally skipped? Look for `if debug_mode: skip_auth()` or early return patterns. | CWE-306, ASVS V6 |
| Credential logging | Are usernames, passwords, or auth tokens logged at any level? | CWE-798 (indirect), ASVS V16 |
| Token generation entropy | Are session tokens, CSRF tokens, or API keys generated using `secrets.token_urlsafe()` or equivalent? NOT `random.random()`. | ASVS V6.3.*, CERT MSC30-C analog |
| Brute force protection | Is there rate limiting, account lockout, or CAPTCHA on authentication endpoints? | ASVS V6.1.* |
| Multi-factor authentication | Does the code indicate MFA is implemented, or is it single-factor? | ASVS V6.4.* |
| PowerShell certificate validation bypass | `[Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}` or `-SkipCertificateCheck` | ASVS V12, CWE-295 |

---

### SEC-04: Authorization & Access Control

**ASVS 5.0.0:** V8 (Authorization)  
**CWE Top 25 (2024):** CWE-862 (#9), CWE-863 (#18), CWE-269 (#15)  
**ISO 25010:** Security → Accountability, Authenticity  
**SA-11:** SA-11(4), SA-11(6)  
**Default Tier:** Tier 1  
**LLM primary advantage — SAST cannot evaluate authorization logic**

#### Deterministic Checks

| Tool | Rule | What It Catches |
|------|------|----------------|
| Ruff | `S611` | Limited — no general authorization rule |
| PSScriptAnalyzer | `PSAvoidUsingComputerNameHardcoded` | Hardcoded target systems bypass environment-based access control |

**Note:** SAST coverage for authorization is fundamentally **poor**. This is the security critic's highest-value LLM contribution.

#### LLM Judgment Checks

| Check | Specific Signal to Evaluate | Framework Citation |
|-------|---------------------------|-------------------|
| Authorization enforcement location | Is authorization checked server-side, or only in client-side code/UI? Look for functions that perform sensitive operations without checking the caller's identity. | CWE-862, ASVS V8.1.* |
| IDOR (Insecure Direct Object Reference) | Does the code use user-supplied IDs to retrieve records without verifying the requesting user owns those records? e.g., `get_document(doc_id)` without `where owner_id = current_user.id` | CWE-862, ASVS V8.2.* |
| Privilege escalation paths | Is there any code path where a lower-privilege user can trigger actions reserved for higher-privilege users? Horizontal (same role, different user) and vertical (lower role → higher role). | CWE-269, ASVS V8.3.* |
| Authorization applied to all sensitive operations | Are DELETE, UPDATE, and sensitive READ operations all authorization-gated? Is there an administrative function without auth check? | CWE-862, ASVS V8 |
| Function-level access control | For REST APIs: does each endpoint/function check auth, or only at the route level? Route-level middleware can be bypassed. | CWE-863, ASVS V8 |
| PowerShell privilege check | Does the script check `[Security.Principal.WindowsIdentity]::GetCurrent()` or `$env:USERNAME` before performing privileged operations? | CWE-269 |

---

### SEC-05: Session & Token Management

**ASVS 5.0.0:** V7 (Session Management), V9 (Self-Contained Tokens)  
**CWE Top 25 (2024):** CWE-352 (#4), CWE-287 (#14)  
**ISO 25010:** Security → Authenticity  
**SA-11:** SA-11(4)  
**Default Tier:** Tier 2

#### Deterministic Checks

**Python:**

| Rule | What It Catches |
|------|----------------|
| Ruff `S324` | Weak hashing for token generation |
| Ruff `S105–S107` | Hardcoded JWT secrets or session keys |

**PowerShell:**

No PSSA rules cover session management directly — **GAP**.

#### LLM Judgment Checks

| Check | Specific Signal to Evaluate | Framework Citation |
|-------|---------------------------|-------------------|
| JWT `alg=none` vulnerability | Does JWT verification code accept `alg=none`? Is the algorithm pinned in verification? Does the code use library defaults or explicitly set `algorithms=["HS256"]`? | ASVS V9.2.*, CWE-327 |
| JWT signature verification | Is `jwt.decode()` called with signature verification, or with `verify=False`? | ASVS V9.2.3 |
| JWT secret strength | Is the JWT signing key derived from a high-entropy secret (32+ bytes), not a short human-readable string? | ASVS V9.2.1 |
| Token expiry enforcement | Are JWT/session tokens checked for expiry? Is `exp` claim validated? | ASVS V9.2.*, ASVS V7 |
| CSRF token implementation | Are state-changing requests protected by CSRF tokens? Is the token bound to the session? | CWE-352, ASVS V3 |
| Session fixation prevention | Is the session token regenerated upon successful authentication? | ASVS V7.2.* |
| Cookie security attributes | Are cookies set with `HttpOnly`, `Secure`, `SameSite` attributes? | ASVS V7.3.* |

---

### SEC-06: Cryptography

**ASVS 5.0.0:** V11 (Cryptography)  
**CWE Top 25 (2024):** (Not top 25 but CWE-327, CWE-328, CWE-330 are high-value)  
**CISQ ASCSM:** CWE-321 (hard-coded crypto key)  
**ISO 25010:** Security → Confidentiality, Integrity  
**SA-11:** SA-11(1), SA-11(4)  
**Default Tier:** Tier 2

#### Deterministic Checks

**Python:**

| Rule | What It Catches |
|------|----------------|
| `S303` | `hashlib.md5()` or `hashlib.sha1()` — weak hash for security context (CWE-328) |
| `S304` | `DES`, `3DES` cipher usage |
| `S305` | Cipher using ECB mode — deterministic, pattern-leaking |
| `S413` | `pycrypto` import (deprecated, unmaintained) |
| `S501–S509` | Weak TLS/SSL: `SSLv2`, `SSLv3`, short key sizes, cert bypass |
| `S321` | FTP (plaintext) usage — use SFTP/FTPS |
| `S107` | Hardcoded cryptographic key literals |

**PowerShell:**

| Rule | What It Catches |
|------|----------------|
| `PSAvoidUsingBrokenHashAlgorithms` | MD5, SHA1 for integrity checking (CWE-328) |

#### LLM Judgment Checks

| Check | Specific Signal to Evaluate | Framework Citation |
|-------|---------------------------|-------------------|
| Algorithm selection for context | Is `SHA256` used for integrity, `bcrypt`/`argon2` for passwords, `AES-256-GCM` for encryption? The algorithm must match the use case. Ruff catches MD5/SHA1; LLM catches using SHA256 for password hashing (wrong category, still wrong). | ASVS V11.3.*, CWE-327 |
| IV/nonce uniqueness | For AES-GCM or similar: is the nonce/IV generated freshly for each encryption? A reused nonce in GCM is catastrophic. | ASVS V11.3.* |
| Key derivation function | When deriving encryption keys from passwords, is `PBKDF2`, `bcrypt`, `scrypt`, or `Argon2` used? Not raw `SHA256(password)`. | ASVS V11.4.* |
| Random number generator | Is `secrets.token_bytes()` used for cryptographic randomness, not `random.random()`? | ASVS V11.6.*, CERT MSC30-C analog |
| Key storage | Are cryptographic keys stored in memory after use without zeroing? Are they stored in plaintext files or databases? | ASVS V11.5.* |
| PowerShell RNG for security | Is `[System.Security.Cryptography.RNGCryptoServiceProvider]` or `Get-Random -SetSeed` (insecure) used? | ASVS V11.6.* |

---

### SEC-07: Secrets & Credential Handling

**ASVS 5.0.0:** V13 (Configuration)  
**CWE Top 25 (2024):** CWE-798 (#22)  
**CISQ ASCSM:** CWE-798, CWE-259, CWE-321  
**ISO 25010:** Security → Confidentiality  
**SA-11:** SA-11(1)  
**Default Tier:** Tier 1

#### Deterministic Checks

**Python:**

| Rule | What It Catches |
|------|----------------|
| `S105` | Hardcoded password in assignment or comparison |
| `S106` | Hardcoded password in function call argument |
| `S107` | Hardcoded API key, secret key, auth token patterns |
| `S108` | Temporary file with predictable name (secrets written to predictable paths) |

**PowerShell:**

| Rule | What It Catches |
|------|----------------|
| `PSAvoidUsingConvertToSecureStringWithPlainText` | Plaintext secret in `ConvertTo-SecureString` call |
| `PSAvoidUsingUsernameAndPasswordParams` | Credential-named parameters typed as strings |
| `PSAvoidUsingComputerNameHardcoded` | Infrastructure topology disclosure |

#### LLM Judgment Checks

| Check | Specific Signal to Evaluate | Framework Citation |
|-------|---------------------------|-------------------|
| Environment variable loading correctness | `os.environ["API_KEY"]` raises if missing (safe pattern); `os.environ.get("API_KEY", "fallback-key")` hardcodes a fallback (unsafe). | OWASP CRG: Configuration, ASVS V13 |
| Secrets in exception messages | `raise ValueError(f"Authentication failed for key: {api_key}")` — exception message leaks secret | CWE-209, ASVS V16 |
| Secrets in log output | Any `logging.*` or `print()` call that includes credential values | ASVS V16, CWE-200 |
| `.env` file handling | Are `.env` files excluded from version control? Is the `.env.example` file checked in but `.env` is not? | ASVS V13, OWASP CRG |
| Secrets in URL parameters | API keys passed as query parameters (`?api_key=...`) instead of headers — appear in access logs | ASVS V13, CWE-598 |
| PowerShell SecureString misuse | `$secureStr = ConvertTo-SecureString $plain -AsPlainText -Force; $plain2 = [Runtime.InteropServices.Marshal]::PtrToStringAuto(...)` — round-trip to plaintext | CWE-312, ASVS V13 |
| Default credentials | Does code rely on default usernames/passwords for services (e.g., `admin`/`admin`)? | CWE-798, ASVS V6 |

---

### SEC-08: Path Traversal & File Handling

**ASVS 5.0.0:** V5 (File Handling)  
**CWE Top 25 (2024):** CWE-22 (#5), CWE-434 (#10)  
**CISQ ASCSM:** CWE-22  
**ISO 25010:** Security → Integrity, Confidentiality  
**SA-11:** SA-11(1), SA-11(4)  
**Default Tier:** Tier 2

#### Deterministic Checks

**Python:**

| Rule | What It Catches |
|------|----------------|
| `S324` | Hash algorithm — file integrity context |
| `S101` | `assert` for security checks — assertions disabled with `-O` flag |
| No dedicated Ruff rule for path traversal — **GAP** | (`PTH*` rules are about using `pathlib`, not security) |

**PowerShell:**

No PSSA rules for path traversal — **GAP**.

**Note:** Path traversal detection in both languages depends primarily on LLM semantic analysis and taint-aware SAST tools (Semgrep, CodeQL). Standard Ruff/PSSA provide minimal coverage.

#### LLM Judgment Checks

| Check | Specific Signal to Evaluate | Framework Citation |
|-------|---------------------------|-------------------|
| Path canonicalization | After joining user input with a base path, is `os.path.realpath()` or `Path.resolve()` called? Does the code verify the result starts with the expected prefix? | CWE-22, ASVS V5.1.*, CERT FIO02-C analog |
| Archive extraction safety | Does code extract zip/tar files without checking for path traversal (`../`) in archive member names? `zipfile.extractall()` without member validation is unsafe. | CWE-22, ASVS V5.4.* |
| File upload validation | (1) Extension allow-list not deny-list; (2) MIME type verified from content not filename; (3) File stored outside webroot; (4) Filename sanitized before storage; (5) Size limit enforced. | CWE-434, ASVS V5.2.* |
| Symlink following | Does the code follow symlinks that could point outside the intended directory? | CWE-22, ASVS V5.1.* |
| PowerShell path validation | `Get-Content "C:\data\$file"` where `$file` is user-controlled — traverse via `..\..\Windows\System32\` | CWE-22, OWASP CRG: File Management |
| Temp file safety | Temporary files created in shared directories with predictable names — race condition / symlink attack | CWE-377, ASVS V5 |

---

### SEC-09: Deserialization

**ASVS 5.0.0:** V2 (Validation), V15 (Secure Coding)  
**CWE Top 25 (2024):** CWE-502 (#16)  
**CISQ ASCSM:** CWE-502  
**ISO 25010:** Security → Integrity  
**SA-11:** SA-11(1), SA-11(4)  
**Default Tier:** Tier 2

#### Deterministic Checks

**Python:**

| Rule | What It Catches |
|------|----------------|
| `S301` | `pickle` or `cPickle` deserialization |
| `S302` | `marshal` module deserialization |
| `S403` | Imports of `pickle`, `cPickle`, `dill`, or `shelve` modules |
| `S506` | `yaml.load()` without `Loader=yaml.SafeLoader` |
| *(none)* | No dedicated Ruff rule for `jsonpickle` — **LLM detection required** |

**PowerShell:**

No PSSA rules for deserialization — **GAP**.  
Risk vector: `ConvertFrom-Json` with subsequent type casting of untrusted data; `Import-CliXml` from untrusted sources.

#### LLM Judgment Checks

| Check | Specific Signal to Evaluate | Framework Citation |
|-------|---------------------------|-------------------|
| Pickle from untrusted sources | Is `pickle.loads()` called with data that originates from network, file upload, or user input? Even indirect — if a cached object could be tampered with. | CWE-502, ASVS V2, OWASP CRG |
| YAML loading | Is `yaml.load()` used anywhere? It must be `yaml.safe_load()` unless there is explicit justification. Full YAML loader executes arbitrary Python. | CWE-502, ASVS V15.2.* |
| JSON with type hydration | `json.loads()` is safe; `jsonpickle.decode()`, Pydantic `model_validate()` with `arbitrary_types_allowed=True` from untrusted input, or custom `object_hook` that instantiates classes — these are unsafe. | CWE-502 |
| PowerShell `Import-CliXml` | If importing XML from network or user-controlled source, is there validation before import? CliXml can reconstitute .NET objects. | CWE-502 |
| Deserialization gadget chains | Does the codebase include classes that, when deserialized, trigger dangerous side effects (file operations, shell execution)? | CWE-502, ASVS V15.2.* |

---

### SEC-10: Server-Side Request Forgery (SSRF)

**ASVS 5.0.0:** V4 (API), V15 (Secure Coding)  
**CWE Top 25 (2024):** CWE-918 (#19)  
**ISO 25010:** Security → Integrity, Resistance  
**SA-11:** SA-11(4), SA-11(6)  
**Default Tier:** Tier 2

#### Deterministic Checks

**Python:**

| Rule | What It Catches |
|------|----------------|
| No dedicated Ruff rule for SSRF — **PARTIAL GAP** | Semgrep/CodeQL detect `requests.get(user_url)` patterns |

**PowerShell:**

No PSSA rules for SSRF — **GAP**.

**Note:** SSRF detection requires taint analysis from user input to URL construction. Standard SAST tools provide partial coverage at best. This is primarily an LLM domain.

#### LLM Judgment Checks

| Check | Specific Signal to Evaluate | Framework Citation |
|-------|---------------------------|-------------------|
| User-controlled URL fetching | Is any user-supplied URL, webhook, or redirect target used in `requests.get()`, `httpx.get()`, `Invoke-WebRequest`, or similar without validation? | CWE-918, ASVS V4.2.* |
| URL allowlisting | If external URLs are fetched based on user input, is there an allowlist of permitted domains/IP ranges? | ASVS V15.3.*, CWE-918 |
| Cloud metadata endpoint protection | For cloud-hosted code: is there explicit blocking of requests to `169.254.169.254` (AWS IMDS) or similar metadata endpoints? | CWE-918, ASVS V15 |
| Redirect following | Does the HTTP client follow redirects automatically? Could an attacker redirect a whitelisted initial URL to an internal resource? | CWE-918, ASVS V4 |
| DNS rebinding protection | Is there protection against DNS rebinding where a permitted hostname resolves to an internal IP? | CWE-918 |
| Webhook URL validation | For any feature that accepts webhook URLs: are URLs validated before first use? Is SSRF to internal services possible? | CWE-918 |

---

### SEC-11: Error Handling & Information Disclosure

**ASVS 5.0.0:** V16 (Security Logging and Error Handling)  
**CWE Top 25 (2024):** CWE-200 (#17)  
**CISQ ASCSM:** CWE-778 (insufficient logging)  
**ISO 25010:** Security → Confidentiality; Reliability → Fault Tolerance  
**SA-11:** SA-11(4)  
**Default Tier:** Tier 2

#### Deterministic Checks

**Python:**

| Rule | What It Catches |
|------|----------------|
| `S110` | `try-except-pass` — exceptions swallowed (security implications) |
| `LOG007` | `.exception()` with `exc_info=False` — stack trace lost |
| `BLE001` | Blind `except:` — includes security-relevant exceptions |

**PowerShell:**

| Rule | What It Catches |
|------|----------------|
| `PSAvoidUsingEmptyCatchBlock` | Empty catch silences security-relevant exceptions |

#### LLM Judgment Checks

| Check | Specific Signal to Evaluate | Framework Citation |
|-------|---------------------------|-------------------|
| Stack traces in responses | Does error handling return raw exception messages or stack traces to the caller/HTTP response? Stack traces reveal file paths, library versions, internal logic. | CWE-200, ASVS V16.1.* |
| Verbose error messages | Error messages that say "User john@example.com not found" (confirms user existence) vs. "Invalid credentials" (opaque). | CWE-203, ASVS V16.1.* |
| Sensitive data in exceptions | Exception messages or wrapped errors that include passwords, API keys, SQL queries, or internal paths. | CWE-200, CWE-209 |
| Logging security events | Are authentication failures, authorization denials, and input validation failures logged? With what detail? | ASVS V16.2.*, SA-11 |
| Log injection prevention | Is user input sanitized before inclusion in log messages? Newline characters in log entries can forge log events. | CWE-117, ASVS V16.3.* |
| Debug mode in production | Flask `debug=True`, Django `DEBUG=True`, verbose error pages enabled — are these gated on environment? | CWE-200, ASVS V13 |

---

### SEC-12: Security Logging & Audit

**ASVS 5.0.0:** V16 (Security Logging and Error Handling)  
**CWE Top 25 (2024):** (Not top 25; CWE-778 in CISQ)  
**CISQ ASCSM:** CWE-778  
**ISO 25010:** Security → Non-repudiation, Accountability  
**SA-11:** SA-11(4)  
**Default Tier:** Tier 3

#### Deterministic Checks

**Python:**

| Rule | What It Catches |
|------|----------------|
| `LOG001–LOG015` | Logging configuration errors (wrong logger, wrong level) |
| `G004` | f-string in log — performance but also signal of poor log hygiene |

**PowerShell:**

| Rule | What It Catches |
|------|----------------|
| `PSAvoidUsingWriteHost` | Output bypassing pipeline and logging infrastructure |
| `PSDSCUseVerboseMessageInDSCResource` | Missing verbose logging in DSC resources |

**Note:** Whether security events are *correctly* logged cannot be determined by static analysis. This is primarily LLM territory.

#### LLM Judgment Checks

| Check | Specific Signal to Evaluate | Framework Citation |
|-------|---------------------------|-------------------|
| Authentication event logging | Is every successful login, failed login, and logout logged with timestamp, user identifier, and source IP? | ASVS V16.2.1, SA-11(4) |
| Authorization failure logging | Is every denied access attempt logged? With the resource attempted and the requesting identity? | ASVS V16.2.2, CWE-778 |
| Audit trail completeness | For sensitive operations (data deletion, privilege change, configuration update): is there a before/after audit log? | ASVS V16.2.*, SA-11 |
| Log tampering protection | Are logs written to an append-only destination? Can a compromised application process modify past logs? | ASVS V16.4.* |
| PII in logs | Are user PII fields (email, SSN, full name, IP addresses) in logs? Do privacy requirements mandate omission or pseudonymization? | ASVS V16, V14 |
| PowerShell transcript sensitivity | If PowerShell transcription is enabled, does the script suppress sensitive output before logging to transcript? | ASVS V16, CWE-200 |

---

### SEC-13: Dependency & Supply Chain

**ASVS 5.0.0:** V15 (Secure Coding and Architecture)  
**CWE Top 25 (2024):** (Not top 25; covered by ASVS V15)  
**ISO 25010:** Security → Integrity  
**SA-11:** SA-11(2) Threat Modeling, SA-11(2) Dynamic Analysis / Attack Simulation  
**Default Tier:** Tier 3  
**Note:** SCA (Software Composition Analysis) tools handle CVE database lookup; LLM flags for SCA
and adds semantic detection of supply chain patterns (unpinned deps, non-standard registries,
dynamic code loading, known-dangerous libraries) that SCA tools may miss. Complementary, not redundant.

#### Deterministic Checks

| Tool | Rule | What It Catches |
|------|------|----------------|
| Ruff `S411–S415` | Suspicious imports (telnet, FTP, pycrypto, pycryptodome — deprecated) |
| `pip-audit` / `safety` | Known CVEs in dependencies — external SCA tool, not part of critic |
| PSScriptAnalyzer `PSAvoidUsingWMICmdlet` | Deprecated WMI cmdlets (not a CVE, but signals unmaintained dependency pattern) |

#### LLM Judgment Checks

| Check | Specific Signal to Evaluate | Framework Citation |
|-------|---------------------------|-------------------|
| Unpinned dependency versions | `requirements.txt` with `requests` (no version) vs. `requests==2.31.0` — unpinned allows automatic upgrade to vulnerable version | ASVS V15.5.* |
| Known dangerous libraries | `pycrypto` (deprecated, CWE-327), `yaml` without `safe_load` (CWE-502), `pickle` for general serialization | ASVS V15.2.* |
| Dependency count justification | Unusually large dependency trees for simple functionality — increased attack surface | ASVS V15.5.* |
| Flag for SCA | When any third-party library is used for security-sensitive functions (crypto, auth, serialization), flag for SCA tool verification | SA-11(2) |

---

### SEC-14: Resource Consumption & DoS

**ASVS 5.0.0:** V4 (API)  
**CWE Top 25 (2024):** CWE-400 (#24)  
**CISQ ASCSM:** CWE-789 (uncontrolled memory allocation), CWE-835 (infinite loop)  
**ISO 25010:** Security → Resistance; Performance Efficiency → Capacity  
**SA-11:** SA-11(4)  
**Default Tier:** Tier 3

#### Deterministic Checks

**Python:**

| Rule | What It Catches |
|------|----------------|
| `S113` | HTTP requests without timeout — DoS via slow responses |
| `PERF203` | `try/except` in tight loops — performance degradation |
| `B015` | Pointless comparison — loop condition always true |

**PowerShell:**

| Rule | What It Catches |
|------|----------------|
| No PSSA rules for DoS patterns — **GAP** | |

#### LLM Judgment Checks

| Check | Specific Signal to Evaluate | Framework Citation |
|-------|---------------------------|-------------------|
| Regex catastrophic backtracking | Does the code use complex regex patterns (`^(a+)+$`, nested quantifiers) on user-controlled input? ReDoS can cause CPU exhaustion. | CWE-400, ASVS V2 |
| Unbounded data loading | Does the code read entire files, database results, or API responses into memory without pagination or size limits? | CWE-400, CWE-789 |
| Rate limiting | For any publicly accessible endpoint or API function: is there rate limiting? Token bucket, leaky bucket, or request count? | ASVS V4.4.*, CWE-400 |
| Request size limits | Are file uploads, request bodies, and query results size-limited before processing? | CWE-400, ASVS V5.2.* |
| Algorithmic complexity with user input | Does user input control loop iterations, recursion depth, or data structure size? Can an attacker trigger O(n²) or worse behavior? | CWE-407, CWE-400 |

---

## 2. Python-Specific Security Checklist

Concrete items for Python code review, with framework citations.

| # | Check | Ruff/Pylint Rule | Framework | Tier |
|---|-------|-----------------|-----------|------|
| P-01 | `eval()` or `exec()` with user-controlled input | `S307`, `S102` | CWE-94, ASVS V1, OWASP CRG | T1 |
| P-02 | `subprocess` with `shell=True` and user input | `S603`, `S605` | CWE-78, ASVS V1 | T1 |
| P-03 | `os.system()` usage | `S605`, `S611` | CWE-78, CERT ENV33-C analog | T1 |
| P-04 | SQL query built with string formatting | `S608` | CWE-89, ASVS V1 | T1 |
| P-05 | `pickle.loads()` with non-local data | `S301` | CWE-502, ASVS V2, V15 | T1 |
| P-06 | `yaml.load()` without `Loader=yaml.SafeLoader` | `S506` | CWE-502, ASVS V2 | T1 |
| P-07 | Hardcoded API keys, passwords, tokens | `S105`, `S106`, `S107` | CWE-798, CWE-259, ASVS V13 | T1 |
| P-08 | HTTP request without timeout | `S113` | CWE-1088, ASVS V4 | T1 |
| P-09 | SSL certificate verification disabled | `S323`, `S501` | CWE-295, ASVS V12 | T1 |
| P-10 | Jinja2 `autoescape=False` | `S701`, `S704` | CWE-79, ASVS V1, V3 | T1 |
| P-11 | `MD5`/`SHA1` for password hashing | `S303` | CWE-328, ASVS V11 | T2 |
| P-12 | Weak cipher or ECB mode | `S304`, `S305` | CWE-327, ASVS V11 | T2 |
| P-13 | `random.random()` for security tokens | *(no Ruff rule)* | CWE-330, ASVS V11.6, CERT MSC30-C analog | T2 |
| P-14 | Flask `debug=True` | `S201` | CWE-200, ASVS V13 | T2 |
| P-15 | Insecure `tarfile.extractall()` (path traversal) | `S202` | CWE-22, ASVS V5 | T2 |
| P-16 | SSRF via user-controlled URL | *(no Ruff rule)* | CWE-918, ASVS V4, V15 | T2 |
| P-17 | Path traversal in file open | *(no Ruff rule — use `os.path.realpath()`)* | CWE-22, ASVS V5, CERT FIO02-C analog | T2 |
| P-18 | `marshal` deserialization | `S302` | CWE-502 | T2 |
| P-19 | FTP usage (plaintext protocol) | `S321` | CWE-321, ASVS V12 | T2 |
| P-20 | Missing authorization on sensitive operations | *(LLM only)* | CWE-862, CWE-863, ASVS V8 | T1 (LLM) |
| P-21 | JWT `alg=none` accepted | *(LLM only)* | CWE-347, ASVS V9 | T2 (LLM) |
| P-22 | Regex catastrophic backtracking on user input | *(LLM only)* | CWE-400, ASVS V2 | T3 (LLM) |
| P-23 | Stack traces returned in HTTP responses | *(LLM only)* | CWE-200, ASVS V16 | T2 (LLM) |
| P-24 | Password stored without KDF (bcrypt/argon2) | *(LLM + S303)* | CWE-916, ASVS V6.2 | T1 (LLM) |
| P-25 | IDOR — user-supplied ID without ownership check | *(LLM only)* | CWE-862, ASVS V8.2 | T1 (LLM) |

---

## 3. PowerShell-Specific Security Checklist

Concrete items for PowerShell code review, with framework citations.

| # | Check | PSSA Rule | Framework | Tier |
|---|-------|-----------|-----------|------|
| PS-01 | `Invoke-Expression` (IEX) with user input | `PSAvoidUsingInvokeExpression` | CWE-78, CWE-94, ASVS V1 | T1 |
| PS-02 | `ConvertTo-SecureString -AsPlainText -Force` with literals | `PSAvoidUsingConvertToSecureStringWithPlainText` | CWE-798, ASVS V13 | T1 |
| PS-03 | String-typed `$Username`/`$Password` parameters | `PSAvoidUsingUsernameAndPasswordParams` | CWE-798, CWE-312, ASVS V13 | T1 |
| PS-04 | HTTP credential transmission (`-AllowUnencryptedAuthentication`) | `PSAvoidUsingAllowUnencryptedAuthentication` | CWE-319, ASVS V12 | T1 |
| PS-05 | MD5/SHA1 for integrity verification | `PSAvoidUsingBrokenHashAlgorithms` | CWE-328, ASVS V11 | T1 |
| PS-06 | `[Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}` | *(LLM + PSSA gap)* | CWE-295, ASVS V12 | T1 (LLM) |
| PS-07 | `-SkipCertificateCheck` on web requests | *(no PSSA rule)* | CWE-295, ASVS V12 | T1 (LLM) |
| PS-08 | Hardcoded `-ComputerName` (topology disclosure) | `PSAvoidUsingComputerNameHardcoded` | CWE-798 analog, ASVS V13 | T1 |
| PS-09 | `$Password` without `[SecureString]` type | `PSAvoidUsingPlainTextForPassword` | CWE-312, ASVS V13 | T1 |
| PS-10 | Credential params not typed `[PSCredential]` | `PSUsePSCredentialType` | CWE-312, ASVS V13 | T2 |
| PS-11 | SQL injection via `Invoke-Sqlcmd` string concat | *(no PSSA rule — LLM)* | CWE-89, ASVS V1 | T1 (LLM) |
| PS-12 | Empty `catch {}` silencing security exceptions | `PSAvoidUsingEmptyCatchBlock` | CWE-390, CWE-703 | T1 |
| PS-13 | Missing `-ErrorAction Stop` in try/catch | *(no PSSA rule)* | CWE-390, ASVS V16 | T2 (LLM) |
| PS-14 | Execution policy bypass (`-ExecutionPolicy Bypass`) | *(no PSSA rule)* | ASVS V15, OWASP CRG: PS | T2 (LLM) |
| PS-15 | AMSI bypass patterns (`AmsiUtils` reflection) | *(no PSSA rule)* | ASVS V15, OWASP CRG: PS | T2 (LLM) |
| PS-16 | Download cradle patterns (`iwr | iex`, `DownloadString`) | *(no PSSA rule)* | CWE-78, CWE-94, ASVS V15 | T2 (LLM) |
| PS-17 | Registry persistence paths (Run keys) | *(no PSSA rule)* | CWE-269, ASVS V8 | T2 (LLM) |
| PS-18 | COM object abuse for privilege escalation | *(no PSSA rule)* | CWE-269, ASVS V8 | T3 (LLM) |
| PS-19 | Missing authorization before privileged operations | *(no PSSA rule)* | CWE-862, ASVS V8 | T1 (LLM) |
| PS-20 | Secrets in `Write-Host`, `Write-Output`, or `Out-String` | *(no PSSA rule)* | CWE-200, ASVS V16 | T2 (LLM) |
| PS-21 | Path traversal in `Get-Content`/`Set-Content` | *(no PSSA rule)* | CWE-22, ASVS V5, CERT FIO02-C analog | T2 (LLM) |
| PS-22 | `ConvertFrom-Json` on untrusted network data with type hydration | *(no PSSA rule)* | CWE-502, ASVS V2 | T3 (LLM) |
| PS-23 | `[ScriptBlock]::Create()` with user-controlled string | *(no PSSA rule)* | CWE-94, ASVS V1 | T1 (LLM) |
| PS-24 | `Invoke-WebRequest` without `-TimeoutSec` | *(no PSSA rule)* | CWE-1088 | T1 (LLM) |

---

## 4. Detection Capability Matrix

| Security Category | SAST (Ruff/Pylint/PSSA) | LLM Advantage | Recommendation |
|------------------|------------------------|---------------|----------------|
| Injection — SQL | ✅ Strong (S608) | ✅ Indirect patterns | Both — SAST for direct, LLM for indirect |
| Injection — OS Command | ✅ Strong (S603–S606, PSSA IEX) | ✅ Chained patterns | Both |
| Injection — Code (eval/exec) | ✅ Strong (S102, S307, PSSA IEX) | ✅ Indirect calls | Both |
| Injection — Template | ✅ Moderate (S701–S704) | ✅ Dynamic templates | Both |
| Injection — LDAP/XPath | ❌ No rules | ✅ Sole detector | LLM-ONLY |
| Input Validation completeness | ❌ Weak | ✅ Strong | LLM-HEAVY |
| File upload validation | ❌ Weak | ✅ Strong | LLM-HEAVY |
| Authorization logic | ❌ None | ✅ Excellent | **LLM-ONLY** |
| IDOR | ❌ None | ✅ Excellent | **LLM-ONLY** |
| Privilege escalation | ❌ None | ✅ Good | **LLM-ONLY** |
| Authentication — hardcoded creds | ✅ Strong (S105–S107, PSSA rules) | ✅ Obfuscated patterns | Both |
| Authentication — bypass paths | ❌ None | ✅ Excellent | **LLM-ONLY** |
| Password hashing algorithm | ✅ Partial (S303 — MD5/SHA1) | ✅ Context (wrong category) | Both |
| SSL/TLS cert bypass | ✅ Strong (S323, S501, PSSA) | ✅ Obfuscated patterns | Both |
| Session/Token — JWT `alg=none` | ❌ None | ✅ Strong | **LLM-ONLY** |
| JWT expiry validation | ❌ None | ✅ Strong | **LLM-ONLY** |
| CSRF token presence | ❌ None | ✅ Good | **LLM-ONLY** |
| Cryptography — weak algorithm | ✅ Strong (S303–S305, PSSA) | ✅ Context-dependent misuse | Both |
| Cryptography — IV/nonce reuse | ❌ None | ✅ Moderate | LLM-HEAVY |
| Cryptography — RNG | ❌ No Ruff rule | ✅ Strong | **LLM-ONLY** |
| Secrets — hardcoded | ✅ Strong (S105–S107, PSSA) | ✅ Env var misuse, logging | Both |
| Secrets — in logs/exceptions | ❌ Weak | ✅ Strong | LLM-HEAVY |
| Path traversal | ❌ No Ruff/PSSA rule | ✅ Strong | LLM-HEAVY |
| Archive extraction safety | ❌ None | ✅ Strong | **LLM-ONLY** |
| Deserialization — pickle/yaml | ✅ Strong (S301, S302, S506) | ✅ Indirect paths | Both |
| Deserialization — JSON type hydration | ❌ None | ✅ Good | LLM-HEAVY |
| SSRF | ❌ No Ruff/PSSA rule | ✅ Strong | **LLM-ONLY** |
| ReDoS (regex DoS) | ❌ None | ✅ Good | **LLM-ONLY** |
| Unbounded data loading | ❌ None | ✅ Good | **LLM-ONLY** |
| Rate limiting | ❌ None | ✅ Moderate | LLM-HEAVY |
| Information disclosure — error messages | ❌ Weak | ✅ Strong | LLM-HEAVY |
| Information disclosure — debug mode | ✅ Partial (S201 Flask only) | ✅ Framework-agnostic | Both |
| Security logging completeness | ❌ None | ✅ Good | **LLM-ONLY** |
| Log injection | ❌ None | ✅ Moderate | LLM-HEAVY |
| Supply chain / SCA | ✅ Partial (S4xx imports) | ✅ Semantic patterns (unpinned deps, non-standard registries, dynamic loading) | Both — SAST for known-bad imports, LLM for semantic supply chain patterns; defer CVE lookup to dedicated SCA tools |
| PowerShell — AMSI bypass | ❌ None | ✅ Pattern recognition | **LLM-ONLY** |
| PowerShell — download cradles | ❌ None | ✅ Good | **LLM-ONLY** |

---

## 5. Minimum Viable Coverage

To claim framework-grounded security assessment, the Security Critic must cover:

### Tier 1 — Must Evaluate (Every Validation)

| Requirement | Categories | Framework Basis |
|-------------|-----------|-----------------|
| Run SAST pre-screen (Ruff `S*`, PSSA security rules) before LLM invocation | SEC-01, SEC-03, SEC-07, SEC-09 | SA-11(1) |
| Evaluate authorization logic — IDOR, privilege escalation, missing auth checks | SEC-04 | CWE-862, CWE-863, ASVS V8 |
| Evaluate authentication patterns — credential handling, bypass paths | SEC-03 | CWE-287, CWE-306, ASVS V6 |
| Check injection completeness — direct and indirect injection into all sinks | SEC-01 | CWE-78, CWE-89, CWE-94, ASVS V1 |
| Verify secrets handling — not in source, logs, or exception messages | SEC-07 | CWE-798, ASVS V13 |
| Check error handling for information disclosure | SEC-11 | CWE-200, ASVS V16 |

**LLM Tier 1 focus:** Authorization and authentication — where SAST is blind and LLM has maximum unique advantage.

### Tier 2 — Should Evaluate (Standard Depth)

| Requirement | Categories | Framework Basis |
|-------------|-----------|-----------------|
| Cryptographic algorithm and usage correctness | SEC-06 | CWE-327, ASVS V11 |
| Deserialization of untrusted data | SEC-09 | CWE-502, ASVS V2, V15 |
| SSRF — user-controlled URL fetching | SEC-10 | CWE-918, ASVS V4 |
| Path traversal and file handling | SEC-08 | CWE-22, ASVS V5 |
| JWT/token security (if tokens present in code) | SEC-05 | ASVS V9, CWE-347 |
| Information disclosure in error responses | SEC-11 | CWE-200, CWE-209 |
| Input validation completeness | SEC-02 | CWE-20, ASVS V2 |

### Tier 3 — Deep Analysis (Thorough Depth Only)

| Requirement | Categories | Framework Basis |
|-------------|-----------|-----------------|
| CSRF token implementation | SEC-05 | CWE-352, ASVS V3 |
| Session management lifecycle | SEC-05 | ASVS V7 |
| Security logging completeness | SEC-12 | CWE-778, ASVS V16 |
| Resource consumption / DoS resistance | SEC-14 | CWE-400, ASVS V4 |
| Supply chain dependency awareness | SEC-13 | ASVS V15 (flag for SCA) |
| PowerShell-specific: AMSI bypass, download cradles, execution policy patterns | PS-14, PS-15, PS-16 | ASVS V15, OWASP CRG: PS |

### What Must NOT Be Claimed Without Coverage

Do not claim SA-11 alignment without:
- SA-11(1): Evidence that SAST pre-screen ran (at minimum Ruff `S*` rules, PSSA security rules)
- SA-11(4): Evidence that LLM evaluated authorization logic (SEC-04)
- Documented findings with framework citations (see Section 7)

---

## 6. Framework Cross-Reference

### Where Frameworks Overlap

| Overlap Zone | ASVS 5.0 | CWE Top 25 | OWASP CRG | SEI CERT | SA-11 |
|-------------|---------|-----------|-----------|---------|-------|
| SQL injection | V1.2.* | #3 (CWE-89) | Input Validation | STR analog | SA-11(1), SA-11(4) |
| OS command injection | V1.2.* | #7 (CWE-78), #13 (CWE-77) | Input Validation | ENV33-C analog | SA-11(1), SA-11(4) |
| Code injection (eval) | V1.2.*, V15 | #11 (CWE-94) | Input Validation | — | SA-11(1), SA-11(4) |
| Path traversal | V5.1.* | #5 (CWE-22) | File Management | FIO02-C analog | SA-11(1), SA-11(4) |
| File upload | V5.2.* | #10 (CWE-434) | File Management | — | SA-11(4) |
| Hardcoded credentials | V13.1.* | #22 (CWE-798) | Configuration | ENV analog | SA-11(1) |
| Deserialization | V2.*, V15 | #16 (CWE-502) | Input Validation | — | SA-11(1), SA-11(4) |
| XSS | V1.*, V3.* | #1 (CWE-79) | Output Encoding | STR analog | SA-11(1) |
| CSRF | V3.* | #4 (CWE-352) | Session Mgmt | — | SA-11(4) |
| Broken auth | V6.* | #14 (CWE-287), #25 (CWE-306) | Authentication | ERR, MSC analog | SA-11(4), SA-11(6) |
| Missing authorization | V8.* | #9 (CWE-862), #18 (CWE-863) | Access Control | — | SA-11(4), SA-11(6) |
| Cryptographic weakness | V11.* | (off-list but CISQ-covered) | Cryptography | MSC30-C analog | SA-11(1), SA-11(4) |

### Where Frameworks Contribute Uniquely

| Framework | Unique Contribution | Value to Security Critic |
|-----------|--------------------|-----------------------|
| **OWASP ASVS 5.0** | L1/L2/L3 stratification; JWT/OAuth chapters (V9, V10); WebRTC (V17); formal documentation vs. implementation distinction in `X.1.*` vs `X.2.*` structure | Severity stratification; token-specific coverage; compliance-level vocabulary |
| **CWE Top 25 (2024)** | Empirical prevalence weighting from real CVEs; KEV (Known Exploited Vulnerabilities) overlap for prioritization; memory safety domain (C/C++ only) | Frequency-based prioritization; exploitability context |
| **OWASP Code Review Guide** | Line-by-line reviewer mentality; Python/PS-specific patterns (most actionable for language-specific review); download cradle and AMSI bypass patterns for PowerShell | Practical "what to look for" at code level; language-specific checklists |
| **SEI CERT** | Formal rule taxonomy for C/C++/Java; most rigorous for undefined behavior; function-level rule naming | **Limited direct value for Python/PS** — principles transfer but no official mapping; use for analogical reasoning only |
| **NIST SA-11** | Normative mandate within NIST/FedRAMP compliance framing; sub-control vocabulary (SA-11(1)/(4)/(3)/(6)); positions LLM critic as "independent reviewer" (SA-11(3)) | Compliance citation vocabulary; justification for LLM-as-independent-assessor; SA-11(4) = authorization basis for manual code review role |

### CERT Applicability Limitation (Important)

SEI CERT has **no official Python or PowerShell standard**. Covered languages: C, C++, Java, Perl, Android.

Usage guidance for this critic:
- **DO** cite CERT analogies in findings (`CERT FIO02-C analog`) when a direct pattern maps
- **DO NOT** cite CERT as a grounding standard for Python/PS security assessment
- **DO** use OWASP ASVS + CWE as primary frameworks for Python/PS

### Memory Safety Exclusion

CWE Top 25 positions 2, 6, 8, 20, 21, 23 (CWE-787, 125, 416, 119, 476, 190) are primarily C/C++ domain. Python and PowerShell are garbage-collected. The Security Critic should:
- Acknowledge these categories do not apply to Python/PS code
- Exception: Python C extensions (`.pyd`, `ctypes`, `cffi`) — flag for separate C/C++ analysis

---

## 7. Finding Citation Vocabulary

When the Security Critic reports a finding, ground it using this format:

```
Finding: [Specific description of the issue and location]
Severity: [Critical | High | Medium | Low]

Framework References:
  - ASVS 5.0.0 §[V#].[section].[requirement]: [Requirement text]
  - CWE-[ID]: [Name]
  - OWASP Code Review Guide: [Category]
  - NIST SP 800-53 SA-11([1|4|6]): [Sub-control name]
  [Note: CERT cited as analog only when applicable]

Detection Method: [SAST pre-screen | LLM semantic analysis | Both]
Language: [Python | PowerShell | Both]
Remediation: [Specific fix, not generic advice]
```

**Severity calibration:**
- **Critical:** CWE Top 25 top-10 + direct exploitability from code as written; Tier 1 ASVS L1 failure
- **High:** CWE Top 25 #11–25; ASVS L1 requirement failure; direct auth/authz bypass
- **Medium:** ASVS L2 requirement failure; indirect vulnerability (requires additional conditions)
- **Low:** ASVS L3 or L2 defense-in-depth; configuration hardening; logging adequacy

**SA-11 sub-control mapping for findings:**
- Finding detected by SAST rules → cite `SA-11(1)` (Static Code Analysis)
- Finding detected by LLM reasoning → cite `SA-11(4)` (Manual Code Review)
- Finding assessing attack surface → cite `SA-11(6)` (Attack Surface Reviews)
- Finding verifying independent of development context → cite `SA-11(3)` (Independent Verification)

---

*Framework version: 1.0 · Generated: 2026-03-05*  
*Sources: OWASP ASVS 5.0.0, CWE Top 25 (2024), OWASP Code Review Guide v2.0, SEI CERT (C/C++/Java standards — analogical only for Python/PS), NIST SP 800-53 Rev5 SA-11, ISO/IEC 25010:2023, ISO/IEC 5055:2021 (CISQ ASCSM), Ruff v0.9.x, Pylint v4.0.x, PSScriptAnalyzer latest*
