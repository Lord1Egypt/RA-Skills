---
slug: uuid-generator-tool
name: UUID Toolkit
description: "Generate and parse UUIDs (v1, v4, v5). Batch generation, validation, format conversion. Pure Python standard library, no API key required."
keywords: uuid, guid, unique, identifier, generator
version: "1.0.0"
author: Qiance
language: en
---

# UUID Toolkit

Generate, validate, and parse UUIDs. Supports UUID v1 (time-based), v4 (random), and v5 (namespace-based).

## Features

- **UUID v1**: Time-based UUID (includes MAC address)
- **UUID v4**: Random UUID (default, most common)
- **UUID v5**: Namespace-based UUID (deterministic)
- **Validation**: Check if string is valid UUID
- **Batch generation**: Generate multiple UUIDs at once
- **Format conversion**: With/without hyphens, uppercase/lowercase

## Usage

```bash
# Generate UUID v4 (random, default)
python3 scripts/uuid_toolkit.py

# Generate UUID v1 (time-based)
python3 scripts/uuid_toolkit.py --v1

# Generate 10 UUIDs
python3 scripts/uuid_toolkit.py --count 10

# Validate a UUID
python3 scripts/uuid_toolkit.py --validate "550e8400-e29b-41d4-a716-446655440000"

# Without hyphens
python3 scripts/uuid_toolkit.py --no-hyphens

# Uppercase
python3 scripts/uuid_toolkit.py --upper
```

## Options

| Option | Description |
|--------|-------------|
| `--v1` | Generate UUID v1 (time-based) |
| `--v4` | Generate UUID v4 (random, default) |
| `--v5 NAMESPACE NAME` | Generate UUID v5 |
| `--count N` | Generate N UUIDs |
| `--validate UUID` | Validate UUID format |
| `--no-hyphens` | Output without hyphens |
| `--upper` | Output uppercase |

---

## 中文说明

UUID生成和解析工具，支持v1/v4/v5版本，批量生成，格式验证。
