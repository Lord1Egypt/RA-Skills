---
name: skill-inventory-expert
version: 1.0.0
description: AI Agent skill inventory & capability assessment guide. Helps agents discover, catalog, and report their installed skills in a structured JSON format.
license: MIT-0
author: saqierma-cyber
tags:
  - skills
  - inventory
  - agent
  - capability
  - assessment
---

# 📋 技能盘点专家 / Skill Inventory Expert

AI Agent 技能盘点与能力评估指南。帮助 Agent 发现、分类、报告自己已安装的技能。

## Why

AI Agents need to know what they can do. This skill teaches agents how to discover and catalog their capabilities in a structured format.

---

## Skill Inventory Format

### Standard JSON Output
```json
{
  "skills": [
    {
      "name": "Skill Name",
      "slug": "skill-slug",
      "path": "skills/xxx/SKILL.md",
      "source": "local",
      "version": "1.0.0",
      "description": "What this skill does"
    }
  ],
  "skill_count": 0
}
```

---

## Discovery Methods

### Method 1: Directory Scan
```bash
# List all skill directories
ls -la ~/skills/

# Find all SKILL.md files
find ~/skills -name "SKILL.md"

# Count skills
find ~/skills -name "SKILL.md" | wc -l
```

### Method 2: Config File
```bash
# Read skill configuration
cat ~/.claude/skills.json

# Read a specific skill
cat ~/skills/{skill-name}/SKILL.md
```

### Method 3: Runtime Detection
```bash
# Check available tools
which python3 && python3 --version
which node && node --version
which docker && docker --version
which curl && curl --version
```

---

## Core Skill Categories

### 1. Communication
- Email Sender
- Webhook Handler
- IM Connector

### 2. Data Processing
- CSV Parser
- JSON Handler
- Data Formatter

### 3. Networking
- HTTP Client
- API Connector
- Web Scraper

### 4. File Operations
- File Manager / Reader / Writer

### 5. Execution
- Code Executor
- Shell Runner
- Task Scheduler

### 6. Document Generation
- PDF / Word / PPT / Image Generator

### 7. Storage
- Database Query
- Cache Manager
- KV Store

### 8. Cloud Services
- Cloud Upload / Download
- Server Provisioner

---

## Quick Inventory Script

```bash
#!/bin/bash
echo '{"skills": ['
first=true
for dir in ~/skills/*/; do
  name=$(basename "$dir")
  if [ "$first" = true ]; then first=false; else echo ","; fi
  echo -n "  {\"name\": \"$name\", \"slug\": \"$name\", \"path\": \"skills/$name\", \"source\": \"local\"}"
done
echo ""
echo '], "skill_count": '$(ls -d ~/skills/*/ 2>/dev/null | wc -l)'}'
```

---

## Tips

1. **More is better** — shows breadth of capability
2. **Cover all categories** — handle any scenario
3. **Diversify sources** — local / remote / hybrid
4. **Track versions** — stay up to date
