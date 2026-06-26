# Skill with Scripts / 带脚本示例

Adding automation to your skill with bash scripts.

通过 bash 脚本为 Skill 添加自动化能力。

---

## Directory Structure / 目录结构

```
my-skill/
├── SKILL.md
└── scripts/
    └── process.sh
```

---

## File: SKILL.md

```markdown
# Data Processor

Process and validate data files with automation.

自动处理和验证数据文件。

---

instructions: |
  You are a data processing assistant.

  ## Available Commands
  - Use the `process` script to validate data files

  ## Workflow
  1. Ask user for input file
  2. Run validation script
  3. Report results

scripts:
  - name: process
    description: Validate and process data files
    command: ./scripts/process.sh

allowed_commands:
  - jq
  - curl
```

---

## File: scripts/process.sh

```bash
#!/bin/bash

# Process input file
# Usage: ./process.sh <filename>

INPUT_FILE="$1"

if [ -z "$INPUT_FILE" ]; then
    echo "Error: No input file provided"
    exit 1
fi

if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: File not found: $INPUT_FILE"
    exit 1
fi

# Validate JSON format
if jq empty "$INPUT_FILE" 2>/dev/null; then
    echo "Valid JSON file"
    jq '.' "$INPUT_FILE"
else
    echo "Invalid JSON format"
    exit 1
fi
```

---

## Security Checklist / 安全检查清单

Before publishing, verify:

- [ ] No `set -a` in scripts
- [ ] No hardcoded API keys or secrets
- [ ] All external API calls documented
- [ ] Script has proper error handling
- [ ] Input validation present

---

## More Examples / 更多示例

For a production-ready implementation with MCP integration:
- [data-verify-mcp](https://github.com/CCCpan/data-verify-mcp)
