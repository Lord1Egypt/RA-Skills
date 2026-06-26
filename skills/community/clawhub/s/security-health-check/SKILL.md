---
name: security-health-check
version: "2.1.2"
description: "Check email breaches and password strength. Generate security score reports."
metadata:
  openclaw:
    emoji: "🔒"
    category: security

Check if your email was compromised in data breaches and evaluate password strength.

## Features

- Email breach check via HaveIBeenPwned API (k-anonymity, data stays local)
- Password strength analysis (local computation)
- Security score report (0-100)
- Enterprise: phishing detection, API key leak scan, password policy audit

## Usage

```bash
python3 scripts/security_check.py --email user@example.com
python3 scripts/security_check.py --password "test"
```

## Requirements

Python 3.7+, certifi package.

## Privacy

Email/password queries use HIBP public API with k-anonymity (only SHA1 prefix sent).

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
