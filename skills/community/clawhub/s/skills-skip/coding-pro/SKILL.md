---
name: coding-pro
description: |
  💻 Professional Coding Assistant
  
  Advanced code analysis, debugging, and problem solving.
  
  Features:
  - Debug any code errors
  - Code review & optimization
  - Architecture design
  - Security auditing
  - Performance profiling
  - Test generation
  
  Use when: user wants help with code debugging, optimization, or architecture.
  
metadata:
  openclaw:
    emoji: 💻
---

# 💻 Coding Pro

## Capabilities

| Task | Tools |
|------|-------|
| Debug errors | traceback analysis, stack search |
| Code review | pattern detection, best practices |
| Security audit | vulnerability scanning |
| Performance | profiling, optimization |
| Architecture | system design, patterns |
| Testing | unit tests, integration tests |

## Quick Debug

```bash
# Paste error message
python3 -c "import traceback; traceback.print_exc()"
```

## Code Review

```python
# Check code quality
flake8 your_file.py
pylint your_file.py
```

## Security Scan

```bash
# Scan for secrets
git secrets --scan
bandit -r your_code/
```
