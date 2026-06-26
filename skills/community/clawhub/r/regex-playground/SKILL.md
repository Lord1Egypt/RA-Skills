---
name: regex-playground
description: Learn, test, and debug regular expressions with real-time matching, explanations, and common patterns. Perfect for developers learning regex or debugging complex patterns.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": [] },
        "install": [],
      },
  }
---

# Regex Playground

Interactive regular expression learning and testing tool.

## Usage

```
regex "pattern" "test string"
```

## Features

- 🎯 Real-time matching
- 📖 Plain English explanation
- 🔍 Match groups extraction
- 📋 Common patterns library
- 🧪 Test cases generator

## Example

```
Input: regex "(\w+)@(\w+)\.(\w+)" "test@example.com"

Output:
✓ Match: test@example.com
Group 1: test
Group 2: example  
Group 3: com

Explanation:
- (\w+) - capture word characters (test)
- @ - literal @
- (\w+) - capture word characters (example)
- \. - literal dot
- (\w+) - capture word characters (com)
```

## Common Patterns

| Pattern | Meaning | Example |
|---------|---------|---------|
| `\d+` | One or more digits | 123 |
| `\w+` | Word characters | hello_123 |
| `[a-z]` | Letter range | a, b, c |
| `^start` | Starts with | start... |
| `end$` | Ends with | ...end |
| `a|b` | OR | a or b |
| `a*` | Zero or more a | '', a, aaa |
| `a+` | One or more a | a, aaa |

## Commands

- `regex explain <pattern>` - Explain pattern in plain English
- `regex test <pattern> <string>` - Test pattern against string
- `regex library` - Show common patterns
- `regex generate <type>` - Generate test cases (email, url, phone, etc.)

## Use Cases

- Debug regex in code
- Learn regex by seeing matches
- Validate input patterns
- Extract data from strings