# Security Rules Reference

This document defines the security rules used by the Skills Firewall to evaluate and filter skills.

## Rule Categories

### 1. Code Injection Rules

#### RULE-001: Block eval() Usage
- **Pattern**: `eval(`
- **Action**: BLOCK
- **Severity**: HIGH
- **Rationale**: eval() can execute arbitrary code from strings, leading to code injection vulnerabilities.

#### RULE-002: Block exec() Usage
- **Pattern**: `exec(`
- **Action**: BLOCK
- **Severity**: HIGH
- **Rationale**: exec() allows arbitrary code execution, a major security risk.

#### RULE-003: Block Dynamic Imports
- **Pattern**: `__import__(`
- **Action**: WARN
- **Severity**: MEDIUM
- **Rationale**: Dynamic imports can load unexpected modules.

### 2. Command Execution Rules

#### RULE-004: Block shell=True
- **Pattern**: `shell=True`
- **Action**: BLOCK
- **Severity**: HIGH
- **Rationale**: Using shell=True in subprocess can lead to command injection.

#### RULE-005: Block os.system()
- **Pattern**: `os.system(`
- **Action**: BLOCK
- **Severity**: HIGH
- **Rationale**: Direct shell command execution is a security risk.

#### RULE-006: Warn on subprocess usage
- **Pattern**: `subprocess.`
- **Action**: WARN
- **Severity**: MEDIUM
- **Rationale**: Subprocess calls should be reviewed for safety.

### 3. Credential Rules

#### RULE-007: Block Hardcoded Passwords
- **Pattern**: `password\s*=\s*["\']`
- **Action**: BLOCK
- **Severity**: CRITICAL
- **Rationale**: Hardcoded credentials are a severe security violation.

#### RULE-008: Block Hardcoded API Keys
- **Pattern**: `api_key\s*=\s*["\']`
- **Action**: BLOCK
- **Severity**: CRITICAL
- **Rationale**: API keys should never be hardcoded.

#### RULE-009: Block Hardcoded Tokens
- **Pattern**: `token\s*=\s*["\']`
- **Action**: BLOCK
- **Severity**: CRITICAL
- **Rationale**: Authentication tokens must not be exposed.

### 4. Network Rules

#### RULE-010: Warn on HTTP Requests
- **Pattern**: `requests\.(get|post|put|delete)`
- **Action**: WARN
- **Severity**: MEDIUM
- **Rationale**: External network requests should be reviewed.

#### RULE-011: Warn on Socket Usage
- **Pattern**: `socket\.`
- **Action**: WARN
- **Severity**: MEDIUM
- **Rationale**: Raw socket connections need review.

#### RULE-012: Block Remote Downloads
- **Pattern**: `(curl|wget)\s+`
- **Action**: BLOCK
- **Severity**: HIGH
- **Rationale**: Downloading remote content is a security risk.

### 5. File Operation Rules

#### RULE-013: Warn on File Deletion
- **Pattern**: `shutil\.rmtree|os\.remove|os\.unlink`
- **Action**: WARN
- **Severity**: MEDIUM
- **Rationale**: Destructive file operations need caution.

#### RULE-014: Warn on File Write
- **Pattern**: `open\([^)]*,\s*["\']w`
- **Action**: WARN
- **Severity**: LOW
- **Rationale**: File modifications should be tracked.

### 6. Deserialization Rules

#### RULE-015: Block Pickle Loads
- **Pattern**: `pickle\.loads?`
- **Action**: BLOCK
- **Severity**: HIGH
- **Rationale**: Pickle deserialization can execute arbitrary code.

#### RULE-016: Warn on YAML Load
- **Pattern**: `yaml\.load\(`
- **Action**: WARN
- **Severity**: MEDIUM
- **Rationale**: Use yaml.safe_load() instead of yaml.load().

### 7. Privilege Rules

#### RULE-017: Block Sudo Commands
- **Pattern**: `sudo\s+`
- **Action**: BLOCK
- **Severity**: HIGH
- **Rationale**: Privilege escalation is a security risk.

#### RULE-018: Block chmod 777
- **Pattern**: `chmod\s+777`
- **Action**: BLOCK
- **Severity**: MEDIUM
- **Rationale**: Overly permissive file permissions are unsafe.

### 8. Obfuscation Rules

#### RULE-019: Warn on Base64 Decode
- **Pattern**: `base64\.b64decode`
- **Action**: WARN
- **Severity**: LOW
- **Rationale**: Base64 decoding may indicate obfuscation.

## Action Types

| Action | Description |
|--------|-------------|
| ALLOW | Skill is safe to use |
| WARN | Skill has potential issues, use with caution |
| BLOCK | Skill is blocked from execution |
| QUARANTINE | Skill is isolated for further review |

## Rule Configuration

Rules can be configured via YAML:

```yaml
rules:
  - name: block_eval
    description: Block eval() usage
    patterns:
      - "eval("
    action: block
    enabled: true

  - name: warn_network
    description: Warn on network access
    patterns:
      - "requests."
      - "urllib"
    action: warn
    enabled: true
```

## Whitelist and Blacklist

### Allowed Skills (Whitelist)
Skills explicitly allowed regardless of rule matches:
- `skill-creator`
- `summarize`
- `weather`

### Blocked Skills (Blacklist)
Skills explicitly blocked:
- `malicious-skill-1`
- `data-exfil-skill`

## Risk Scoring

Risk score is calculated as:

```
Risk Score = (critical_count * 15 + high_count * 7 + medium_count * 3 + low_count * 1) / max_possible * 100
```

### Risk Levels

| Score Range | Level | Action |
|-------------|-------|--------|
| 0-30 | Low | Allow with monitoring |
| 31-70 | Medium | Review recommended |
| 71-100 | High | Block or quarantine |

## Best Practices

1. **Regular Audits**: Run firewall scans regularly
2. **Update Rules**: Keep patterns updated for new threats
3. **Review Warnings**: Investigate warning-level findings
4. **Document Exceptions**: Keep track of allowed skills and reasons
5. **Monitor Blocked**: Review blocked skills for false positives
