# Risk Assessment & Vulnerability Patterns

This document details the risk assessment algorithm and common vulnerability patterns used by the QA Architecture Auditor to identify high-risk areas in a codebase.

## Risk Scoring Algorithm

Each module is scored from 0-100 based on weighted risk factors:

### Primary Risk Factors

| Factor | Weight | Description |
|--------|--------|-------------|
| **Cyclomatic Complexity** | 2 points per unit | More paths = higher risk of defects |
| **External Calls** | 3 points per call | Network I/O, API calls increase failure surface |
| **Authentication Handling** | 15 points | Security-critical, requires rigorous testing |
| **Data Persistence** | 10 points | Database operations prone to SQL injection, data loss |
| **Cryptography Usage** | 20 points | Easy to implement incorrectly, high impact |
| **File I/O** | 5 points | Path traversal, injection, permissions risks |
| **High Coupling** | 5 points per 10 imports | Many dependencies = brittle, hard to test |
| **Public API Surface** | 2 points per exported function | More public interfaces = more attack vectors |

### Risk Levels

| Score | Level | Action |
|-------|-------|--------|
| 70-100 | **Critical** | Immediate attention, exhaustive testing, security review |
| 50-69 | **High** | Prioritized testing, code review, security assessment |
| 30-49 | **Medium** | Standard testing coverage |
| 0-29 | **Low** | Basic testing acceptable |

## Vulnerability Patterns by Language

### Python

| Pattern | Risk | Example | Test Focus |
|---------|------|---------|------------|
| **SQL Injection via string concatenation** | Critical | `cursor.execute(f"SELECT * FROM users WHERE id={user_id}")` | Parameterized queries, input validation |
| **Arbitrary code execution with eval/exec** | Critical | `eval(user_input)` | Never use, sandbox alternatives |
| **Pickle deserialization of untrusted data** | Critical | `pickle.loads(untrusted_data)` | Use JSON, validate sources |
| **Command injection with subprocess** | Critical | `subprocess.run(f"ls {user_dir}")` | Use list form: `['ls', user_dir]`, sanitize |
| **Timing attacks in password comparison** | High | `if password == stored_hash:` | Use `hmac.compare_digest()` |
| **YAML loading without safe loader** | High | `yaml.load(user_file)` | Use `yaml.safe_load()` |
| **Hardcoded secrets** | High | `API_KEY = "sk_live_..."` | Environment variables, secret managers |
| **Path traversal** | High | `open(user_path + "/file.txt")` | Use `os.path.join()`, validate paths |
| **Insecure deserialization with pickle** | Critical | `pickle.loads(data)` | Avoid pickle, use JSON/MessagePack |
| **XML External Entity (XXE)** | High | `xml.etree.parse(untrusted.xml)` | Disable DTD, use `defusedxml` |

**Python Static Analysis Tools**: bandit, safety, semgrep, snyk

### JavaScript/TypeScript

| Pattern | Risk | Example | Test Focus |
|---------|------|---------|------------|
| **Cross-Site Scripting (XSS)** | Critical | `element.innerHTML = user_input` | Use `textContent`, DOMPurify, CSP |
| **Eval/Function constructor** | Critical | `eval(user_code); new Function(user_code)` | Never use, strict CSP |
| **Prototype pollution** | High | `Object.assign(obj, user_input)` | Validate/merge safely, `Object.create(null)` |
| **Node.js command injection** | Critical | `child_process.exec(`ls ${dir}`)` | Use `execFile` with args array |
| **Insecure JWT handling** | High | `jwt.decode(token)` without signature check | Verify signature, use short expiry |
| **Regular expression DoS (ReDoS)** | Medium | `/(a+)+b/.test(user_input)` | Limit input size, use safer patterns |
| **Hardcoded secrets** | High | `const API_KEY = "secret";` | Environment variables, config management |
| **Insecure randomness** | High | `Math.random()` for tokens | Use `crypto.randomBytes()` |
| **DOM-based XSS** | Critical | `location.hash.substr(1)` used in `innerHTML` | Sanitize, avoid `innerHTML` |
| **Prototype chain pollution via merge** | High | `lodash.merge({}, obj1, userObj)` | Use `mergeWith` or deep validate |

**JS/TS Static Analysis**: ESLint security plugin, SonarJS, Snyk, npm audit

### Java

| Pattern | Risk | Example | Test Focus |
|---------|------|---------|------------|
| **SQL Injection with Statement** | Critical | `stmt.executeQuery("SELECT * FROM users WHERE id=" + id)` | Use PreparedStatement |
| **XXE with default parser** | Critical | `DocumentBuilder.parse(xml)` | Set features to disable DTD/external entities |
| **Insecure deserialization** | Critical | `ObjectInputStream.readObject()` | Validate classes, signing |
| **Command injection with Runtime.exec** | Critical | `Runtime.getRuntime().exec("cmd " + input)` | Use parameterized exec |
| **Path traversal with File** | High | `new File(basePath + userPath)` | Use `Path.normalize()`, validate |
| **Hardcoded passwords** | High | `String pwd = "password";` | Secure configuration |
| **Weak cryptography** | Medium | `MD5`, `DES` | Use SHA-256+, AES |
| **Insufficient session timeout** | Medium | Session never expires | Configure appropriate timeout |
| **Missing access control checks** | Critical | No `@PreAuthorize` on methods | Audit all endpoints |
| **Logging sensitive data** | Medium | `logger.info("Password: " + password)` | Never log secrets |

**Java Static Analysis**: SpotBugs, FindSecBugs, SonarQube, OWASP Dependency Check

### Go

| Pattern | Risk | Example | Test Focus |
|---------|------|---------|------------|
| **SQL injection with string concatenation** | Critical | `db.Query("SELECT * FROM users WHERE id=" + id)` | Use parameterized queries |
| **Command injection with exec.Command** | Critical | `exec.Command("sh", "-c", "ls "+dir)` | Pass args as separate strings |
| **Path traversal with filepath.Join** | High | `filepath.Join(base, userPath)` | Use `filepath.Clean()`, validate |
| **Hardcoded secrets** | High | `const APIKey = "secret"` | Environment or config server |
| **Insecure randomness** | High | `rand.Int()` for tokens | Use `crypto/rand` |
| **Integer overflow/underflow** | Medium | Arithmetic without checks | Use `math/big` or checks |
| **Timing attacks with string comparison** | High | `if token == expected` | Use `subtle.ConstantTimeCompare` |
| **Race conditions** | High | Unsynchronized map access | Use mutexes, channels |
| **Unhandled errors** | Medium | Ignoring error returns | Always check errors |
| **Template injection** | High | `template.Parse(userInput)` | Avoid parsing user templates |

**Go Static Analysis**: staticcheck, gosec, govet

### C#/.NET

| Pattern | Risk | Example | Test Focus |
|---------|------|---------|------------|
| **SQL Injection with string concat** | Critical | `cmd.CommandText = "SELECT * FROM Users WHERE Id=" + id` | Parameterized queries |
| **XXE with default settings** | Critical | `XmlReader.Create(stream)` | Set `DtdProcessing = Prohibit` |
| **Insecure deserialization** | Critical | `BinaryFormatter.Deserialize()` | Use safe serializers |
| **Path traversal with Path.Combine** | High | `Path.Combine(basePath, userPath)` | Validate final path |
| **Command injection with Process.Start** | Critical | `Process.Start("cmd " + input)` | Use `ArgumentList` |
| **Hardcoded secrets** | High | `connectionString = "..."` | Secure configuration |
| **OWASP Top 10 in Razor views** | High | `@Html.Raw(UserInput)` | Encode output |
| **Weak cipher usage** | High | ` TripleDES` | Use AES |
| **Insufficient anti-forgery** | Medium | Missing `[ValidateAntiForgeryToken]` | Enable CSRF protection |
| **Overly broad exceptions** | Medium | `catch (Exception)` without handling | Specific exception types |

**.NET Static Analysis**: SonarAnalyzer, Security Code Scan, OWASP .NET Rules

### PHP

| Pattern | Risk | Example | Test Focus |
|---------|------|---------|------------|
| **SQL Injection with mysql_* (deprecated)** | Critical | `mysql_query("SELECT * FROM users WHERE id=$id")` | Use PDO with prepared statements |
| **RFI/LFI with include/require** | Critical | `include($_GET['page'] . ".php")` | Whitelist, realpath validation |
| **Unserialize with user data** | Critical | `unserialize($_POST['data'])` | Avoid, use JSON |
| **Command injection with backticks/system** | Critical | `system("ls " . $_GET['dir'])` | escapeshellarg, avoid |
| **XSS with echo/print** | High | `echo $_GET['name'];` | `htmlspecialchars()` |
| **File upload vulnerabilities** | High | `move_uploaded_file($tmp, $user_path)` | Validate type, name, path |
| **Session fixation** | Medium | Not regenerating session ID on login | `session_regenerate_id()` |
| **Hardcoded credentials** | High | `$db_pass = "secret";` | Environment variables |
| **Insecure direct object references** | High | `?file=../../etc/passwd` | Path validation |
| **Missing CSRF tokens** | Medium | No anti-forgery on forms | Use CSRF tokens |

**PHP Static Analysis**: PHPStan, Psalm, RIPS, SonarQube

## Architecture-Level Risk Patterns

### Microservices

| Risk | Description | Mitigation |
|------|-------------|------------|
| **Distributed transactions** | Data consistency across services | SAGA pattern, eventual consistency |
| **Network latency** | Service-to-service calls | Circuit breakers, timeouts, retries |
| **Authentication propagation** | Token passing between services | JWT, OAuth2, mutual TLS |
| **Service discovery failures** | DNS or registry outage | Local caching, fallbacks |
| **API versioning** | Breaking changes affect clients | Versioned APIs, backward compatibility |

### Serverless

| Risk | Description | Mitigation |
|------|-------------|------------|
| **Cold starts** | Latency on first invocation | Provisioned concurrency |
| **Function timeouts** | Long-running tasks fail | Chunking, step functions |
| **Resource limits** | Memory, timeout, payload size limits | Design around limits |
| **Vendor lock-in** | Cloud-specific features | Abstraction layers, multi-cloud |
| **Secrets management** | Environment variables exposure | Cloud secret managers |

### Monolithic

| Risk | Description | Mitigation |
|------|-------------|------------|
| **Tight coupling** | Changes ripple through code | Modular design, clean architecture |
| **Deployment risk** | Entire app deployed together | Canary releases, feature flags |
| **Scalability limitations** | Cannot scale components independently | Vertical scaling, eventual decomposition |
| **Database bottlenecks** | Single DB for all features | Read replicas, query optimization |

## Third-Party Dependency Risks

| Risk | Description | Test Focus |
|------|-------------|------------|
| **Vulnerable dependencies** | Known CVEs in libraries | SCA scanning, dependency upgrades |
| **Unmaintained packages** | No recent updates, abandoned | Evaluate alternatives, fork if needed |
| **License incompatibility** | Copyleft licenses in commercial product | License scanning, legal review |
| **Supply chain attacks** | Malicious code injected into packages | Pinning, checksum verification |
| **Transitive dependencies** | Vulnerabilities deep in dependency tree | Full SCA scan, not just direct deps |

## Data-Handling Risks

| Risk | Description | Test Focus |
|------|-------------|------------|
| **PII storage** | Personal data at rest | Encryption at rest, access logs |
| **Data leakage in logs** | Secrets, PII written to logs | Log scrubbing, structured logging |
| **Insufficient backup** | Data loss on failure | Backup schedules, restore tests |
| **Inadequate retention** | Keeping data too long or not long enough | Data retention policies |
| **Cross-border transfer** | GDPR restrictions on data location | Data residency compliance |

---

## Risk Prioritization Matrix

Use this to prioritize testing effort:

```
                Impact
                High    Medium   Low
Likelihood  High   CRITICAL HIGH    MEDIUM
             Medium HIGH     MEDIUM  LOW
             Low    MEDIUM  LOW     IGNORE
```

- **Critical**: Test exhaustively using all methodologies. Red team exercises. Penetration testing.
- **High**: Strong testing. Focus on integration, security, and edge cases.
- **Medium**: Standard functional testing. Unit tests and some integration.
- **Low**: Smoke tests only. May defer.

---

## Sample Risk Assessment Output

```yaml
risk_assessment:
  - type: code_complexity
    severity: high
    module: src/auth/login.py
    risk_score: 78.5
    description: High complexity module with risk score 78.5
    factors:
      - high_complexity
      - authentication_handling
      - many_external_calls
  - type: security
    severity: critical
    module: src/payment/processor.py
    risk_score: 95.0
    description: Payment processing module - maximum security testing required
    factors:
      - cryptography
      - data_persistence
      - external_calls
```

Each identified risk should trigger:

1. **Additional test cases** targeting that risk factor
2. **Code review** by senior engineer
3. **Security assessment** if severity is critical/high
4. **Monitoring** in production for anomalies

---

## Continuous Risk Monitoring

Risk is not static. Re-assess when:

- New features added to module
- Dependencies updated (new CVEs)
- Production incidents occur
- Performance degrades
- Security threats evolve

Automate risk scoring in CI to flag high-risk changes for extra scrutiny.
