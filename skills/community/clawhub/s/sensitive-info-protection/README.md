# sensitive-info-protection

[English](#english) | [简体中文](#简体中文)

---

## English

A general-purpose sensitive information real-time protection Skill for OpenClaw. Automatically detects, alerts, and handles sensitive data in user interactions.

## Features

- **Real-time detection** - Scans text for multiple types of sensitive information
- **Custom rules** - Add your own detection rules with regex patterns
- **Interactive processing** - Standard output format with operation options
- **Desensitization** - One-click replacement of sensitive content
- **Built-in rules** for common sensitive types:
  - API Keys & tokens (OpenAI, GitHub, AWS)
  - Credit card, bank card numbers
  - Chinese ID card, phone numbers
  - Emails, passwords, secrets

## Installation

In OpenClaw:
```
clawhub install sensitive-info-protection
```

Or clone to your skills directory:
```
git clone https://github.com/LeeFJ0606/sensitive-info-protection.git /path/to/sensitive-info-protection
```

## Quick Start

### Python API

```python
from scripts.detector import SensitiveDetector

detector = SensitiveDetector()
result = detector.scan("My API key is sk-1234567890abcdef1234567890abcdef1234567890abcdef")

if result.has_sensitive:
    print(result.to_markdown())
    # Get desensitized text
    clean = detector.desensitize(result.content)
    print("\nDesensitized:")
    print(clean)
```

### CLI

```bash
# Scan a file
python scripts/cli.py /path/to/file.txt

# Desensitize and output
python scripts/cli.py --desensitize /path/to/file.txt
```

## Documentation

- [Configuration Guide](references/configuration.md)
- [API Documentation](references/api.md)

## Structure

```
sensitive-info-protection/
├── SKILL.md                 # Skill definition for OpenClaw
├── scripts/
│   ├── detector.py          # Main detection engine
│   ├── models.py            # Data models
│   ├── cli.py               # Command-line interface
│   └── default_rules.json   # Built-in detection rules
├── references/
│   ├── configuration.md     # Configuration guide
│   └── api.md               # API documentation
├── assets/
│   └── default_config.json  # Default settings template
└── tests/
    └── test_basic.py        # Basic functionality tests
```

## License

MIT

---

## 简体中文

OpenClaw 通用敏感信息实时防护 Skill，可自动识别、告警并处理用户交互中的敏感数据，支持灵活配置与外部数据源接入。

## 核心功能

- **实时检测** - 监控文本内容，识别多类型敏感信息
- **自定义规则** - 支持通过正则表达式添加自定义检测规则
- **交互式处理** - 标准化输出格式，提供清晰操作选项
- **一键脱敏** - 快速替换敏感内容，防止信息泄露
- **内置规则** - 开箱即用，支持常见敏感类型：
  - API 密钥 / 访问令牌（OpenAI、GitHub、AWS 等）
  - 信用卡号、银行卡号
  - 中国身份证号、手机号码
  - 电子邮箱、密码、机密信息

## 安装

在 OpenClaw 中使用：
```
clawhub install sensitive-info-protection
```

或者直接克隆到你的 Skills 目录：
```
git clone https://github.com/LeeFJ0606/sensitive-info-protection.git /path/to/sensitive-info-protection
```

## 快速开始

### Python API

```python
from scripts.detector import SensitiveDetector

detector = SensitiveDetector()
result = detector.scan("我的 API 密钥是 sk-1234567890abcdef1234567890abcdef1234567890abcdef")

if result.has_sensitive:
    print(result.to_markdown())  # 输出标准检测结果
    # 获取脱敏后的文本
    clean = detector.desensitize(result.content)
    print("\n脱敏结果：")
    print(clean)
```

### 命令行使用

```bash
# 扫描文件
python scripts/cli.py /path/to/file.txt

# 输出脱敏结果
python scripts/cli.py --desensitize /path/to/file.txt
```

## 文档

- [配置指南](references/configuration.md)
- [API 文档](references/api.md)

## 项目结构

```
sensitive-info-protection/
├── SKILL.md                 # OpenClaw Skill 定义
├── scripts/
│   ├── detector.py          # 核心检测引擎
│   ├── models.py            # 数据模型定义
│   ├── cli.py               # 命令行接口
│   └── default_rules.json   # 内置检测规则
├── references/
│   ├── configuration.md     # 详细配置指南
│   └── api.md               # API 文档
├── assets/
│   └── default_config.json  # 默认配置模板
└── tests/
    └── test_basic.py        # 基础功能测试
```

## 许可证

MIT
