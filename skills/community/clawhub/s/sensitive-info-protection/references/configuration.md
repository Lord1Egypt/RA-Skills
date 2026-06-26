# Configuration Guide

## Rule Format

Each detection rule is defined as a JSON object with the following fields:

| Field          | Type    | Required | Default | Description |
|----------------|---------|----------|---------|-------------|
| `name`         | string  | Yes      | -       | Unique rule name |
| `pattern`      | string  | Yes      | -       | Regular expression pattern |
| `sensitivity`  | string  | No       | medium  | One of: `high`, `medium`, `low` |
| `description`  | string  | No       | ""      | Human-readable description |
| `enabled`      | boolean | No       | true    | Whether the rule is enabled |
| `priority`     | integer | No       | 0       | Higher priority rules match first |

## Example Configuration

```json
[
  {
    "name": "company_internal_id",
    "pattern": "INT-[0-9]{6}-[A-Z]{2}",
    "sensitivity": "high",
    "description": "Company internal document ID",
    "priority": 8
  },
  {
    "name": "internal_url",
    "pattern": "https://internal\\.company\\.com/[a-zA-Z0-9-_]+",
    "sensitivity": "medium",
    "description": "Internal company URL",
    "enabled": true
  }
]
```

## Regex Tips

- Use word boundaries `\b` to avoid partial matches
- Escape special characters with double backslash: `\\b`, `\\d`
- Test your regex patterns before adding them to the configuration

## Loading Configuration

### Python API

```python
from sensitive_info_protection import SensitiveDetector

detector = SensitiveDetector()
detector.load_config('/path/to/your/custom-rules.json')
```

### CLI

```bash
python scripts/cli.py --config /path/to/config.json input.txt
```

## Management Commands

### Disable a built-in rule

```python
detector.disable_rule('phone')
```

### Enable a disabled rule

```python
detector.enable_rule('phone')
```

### Remove a rule completely

```python
detector.remove_rule('email')
```

### Add a custom rule at runtime

```python
from sensitive_info_protection.models import DetectionRule

rule = DetectionRule(
    name="my_secret",
    pattern="MY_SECRET=\\w+",
    sensitivity="high"
)
detector.add_rule(rule)
```
