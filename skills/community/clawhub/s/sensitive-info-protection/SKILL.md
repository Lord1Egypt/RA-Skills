---
name: sensitive-info-protection
description: "Sensitive information real-time protection skill that automatically detects, alerts, and handles sensitive data in user interactions. Supports custom detection rules, external data source integration, and interactive processing. Use when you need to: (1) Scan text content for sensitive information, (2) Configure custom sensitive data detection rules, (3) Protect against accidental exposure of credentials, personal info, or business secrets."
metadata:
  openclaw:
    requires:
      bins:
      - python3
---

# Sensitive Info Protection

## Overview

A general-purpose sensitive information protection skill that provides real-time scanning, detection, and interactive handling of sensitive data in conversation content. It helps prevent accidental exposure of personal information, authentication credentials, and commercial secrets through configurable detection rules.

## Core Capabilities

### 1. Sensitive Information Detection
- Real-time scanning of user input and output content
- Detection of multiple sensitive information types by default
- Support for custom user-defined detection rules with regex patterns
- Priority-based rule matching

### 2. Configuration Management
- Built-in default sensitive type library with common patterns
- Support for adding/removing/enabling/disabling custom rules
- Rule priority adjustment for conflict resolution

### 3. External Data Integration
- Import sensitive keyword/pattern lists from external data sources
- Support for dynamic rule updates
- JSON/YAML configuration format

### 4. Interactive Processing
- Standardized output format for detection results
- Clear operation options for user decision-making
- Support for one-click desensitization or manual editing

## Default Sensitive Types

Built-in detection for the following types:
- `api_key` - API keys, access tokens, authentication credentials
- `credit_card` - Credit card numbers
- `id_card` - National ID card numbers (Chinese)
- `phone` - Mobile phone numbers (Chinese)
- `email` - Email addresses
- `bank_card` - Bank card numbers
- `password` - Password patterns in code or logs
- `secret` - Commercial secrets, confidential information markers

## Usage

### Scanning Content for Sensitive Information

```python
from scripts.detector import SensitiveDetector

detector = SensitiveDetector()
results = detector.scan(text_content)

if results:
    # Print detection results in standard format
    detector.print_results(results)
    # Wait for user decision to proceed
else:
    # No sensitive information detected
    pass
```

### Adding Custom Rule

```python
from scripts.models import DetectionRule

new_rule = DetectionRule(
    name="custom_secret",
    pattern=r"MY_SECRET=\w+",
    sensitivity="high",
    description="Custom secret pattern"
)
detector.add_rule(new_rule)
```

### Loading Configuration from File

```python
detector.load_config("path/to/config.json")
```

## Output Format

When sensitive information is detected, the following format is used:

```
## 检测结果
- 敏感类型: [type]
- 位置: [start:end]
- 原文: [original content]
- 敏感度: [high/medium/low]

## 操作选项
1. 确认放行
2. 修改后发送
3. 取消发送
```

## Resources

### scripts/
- `detector.py` - Main detection engine class
- `models.py` - Data models for detection rules and results
- `cli.py` - Command-line interface
- `default_rules.json` - Built-in default detection rules

### references/
- `configuration.md` - Detailed configuration guide
- `api.md` - API documentation for integration

### assets/
- `default_config.json` - Default configuration template

