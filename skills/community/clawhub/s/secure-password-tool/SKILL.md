---
slug: secure-password-tool
name: Secure Password Generator
description: "Generate cryptographically secure random passwords. Customizable length, character types, exclude similar characters. Pure Python standard library, no API key required."
keywords: password, generator, security, random, secure, strong password
version: "1.0.0"
author: Qiance
language: en
---

# Secure Password Generator

Generate cryptographically secure random passwords using Python's `secrets` module. No API keys, no external services, completely offline.

## Features

- **Cryptographically secure**: Uses `secrets` module (not `random`)
- **Customizable length**: Default 16 characters
- **Character types**: Uppercase, lowercase, digits, special symbols
- **Exclude similar characters**: Remove 0, O, 1, l, I to avoid confusion
- **Batch generation**: Generate multiple passwords at once
- **Pure standard library**: Zero dependencies, works offline

## Usage

```bash
# Generate a 16-character password (default)
python3 scripts/password_generator.py

# Generate a 20-character password
python3 scripts/password_generator.py 20

# Generate 10 passwords of 24 characters
python3 scripts/password_generator.py 24 10

# Exclude similar characters (0O1lI)
python3 scripts/password_generator.py 16 --exclude-similar

# Password without special symbols
python3 scripts/password_generator.py 16 --no-special
```

## Examples

```
Generate a strong 20-character password
Generate 5 passwords of 16 characters each
Generate a password without special symbols for a website that doesn't allow them
```

## Options

| Option | Description |
|--------|-------------|
| `LENGTH` | Password length (default: 16) |
| `COUNT` | Number of passwords to generate (default: 1) |
| `--no-upper` | Exclude uppercase letters |
| `--no-lower` | Exclude lowercase letters |
| `--no-digits` | Exclude digits |
| `--no-special` | Exclude special symbols |
| `--exclude-similar` | Exclude 0, O, 1, l, I |

## Security Notes

- Uses `secrets.choice()` for cryptographically secure randomness
- Suitable for generating passwords, API keys, tokens
- Not suitable for password hashing (use bcrypt/argon2 for storage)

---

## 中文说明

安全的随机密码生成器，使用Python标准库secrets模块，无需API Key。

- 默认16位强密码
- 支持自定义长度、字符类型
- 可排除相似字符（0O1lI）
- 支持批量生成
