---
name: skills-finder
version: 1.6.0
description: Intelligent skill matcher that searches multiple skill marketplaces (ClawHub & Skills.sh) in real-time. Supports ANY language for user input, multi-step skill chaining, and one-click installation.
---

# Skills Finder 🔍

**Intelligent skill discovery engine that searches multiple skill marketplaces and recommends the best skills for your task.**

---

## 🎯 When to Use

**Automatically triggers when user wants to find or install skills:**

| User Intent | Examples |
|-------------|----------|
| Find skills | "帮我找个...", "find a skill", "buscar herramienta", "スキルを探して" |
| Search for capability | "有什么skill能做...", "what can you do", "有什么工具" |
| Install skill | "安装...", "install", "instalar", "インストール" |
| Get recommendations | "推荐...", "recommend", "recomendar", "おすすめ" |

---

## 🌍 Universal Language Support

**This skill supports ANY language for user input!**

### Supported Languages (Truly Universal)

This skill supports **ALL languages and scripts** including but not limited to:

| Language Family | Examples |
|-----------------|----------|
| **European** | English, Spanish, French, German, Italian, Portuguese, Russian |
| **Asian** | Chinese (中文), Japanese (日本語), Korean (한국어), Vietnamese, Thai |
| **Middle Eastern** | Arabic, Hebrew, Persian, Turkish |
| **South Asian** | Hindi, Bengali, Tamil, Urdu |
| **African** | Swahili, Zulu, Amharic |
| **Special** | Emoji queries 📱💻🔍 |

---

## 🌐 Supported Skill Marketplaces

### 1. ClawHub (clawhub.ai)
```bash
npx clawhub@latest search "<query>"
npx clawhub@latest install <name>
```
- **5,400+** skills available
- Open-source AI assistant skills
- Rating-based recommendations

### 2. Skills CLI (skills.sh)
```bash
npx skills find "<query>"
npx skills add <package>
```
- **Skills.sh** - The package manager for open agent skills
- Modular packages that extend agent capabilities
- Specialized knowledge, workflows, and tools

---

## ⚡ Quick Commands

```bash
# Search skills (supports ANY language)
~/.openclaw/workspace/skills/skills-finder/scripts/skill-finder.sh search "your query"

# Search specific marketplace
~/.openclaw/workspace/skills/skills-finder/scripts/skill-finder.sh search "query" --source clawhub
~/.openclaw/workspace/skills/skills-finder/scripts/skill-finder.sh search "query" --source skills

# Search both (default)
~/.openclaw/workspace/skills/skills-finder/scripts/skill-finder.sh search "query" --source all

# Install from specific source
~/.openclaw/workspace/skills/skills-finder/scripts/skill-finder.sh install <name> --source clawhub
~/.openclaw/workspace/skills/skills-finder/scripts/skill-finder.sh install <package> --source skills

# List installed skills
~/.openclaw/workspace/skills/skills-finder/scripts/skill-finder.sh list
```

---

## 🔗 Multi-Step Skill Chaining

**For complex tasks requiring multiple skills, the search automatically detects and suggests a skill chain.**

### Chain Detection

| Task Type | Example | Result |
|-----------|---------|--------|
| Single skill | "天气skill" | Direct recommendation |
| Multi-step | "搜索新闻发送到微信" | Skill chain + composite suggestion |

---

## 📋 Usage Examples

### Example 1: Search Both Sources
```
User: 找个天气skill

→ ClawHub: weather (3.898⭐)
→ Skills: @skills/weather

Results from both marketplaces shown!
```

### Example 2: Search Specific Source
```
User: find a skill for GitHub

→ Searching ClawHub only:
  - github (3.636⭐)
  - github-cli (3.538⭐)
```

### Example 3: Multi-language
```
User: 天気を調べて
→ ClawHub: weather
→ Skills: @skills/weather
```

---

## 🔧 Implementation

### Dual Source Search

```bash
# Search ClawHub
npx clawhub@latest search "<query>"

# Search Skills.sh
npx skills find "<query>"

# Both results merged and ranked
```

### Source Priority

| Source | Priority | Use Case |
|--------|----------|----------|
| ClawHub | Default | General AI assistant skills |
| Skills.sh | Alternative | Specialized workflows |

---

## ⚠️ Important Notes

### Why Two Sources?

1. **ClawHub** - Large collection of AI assistant skills (5,400+)
2. **Skills.sh** - Specialized workflows and tools for agents

Both are searched by default for comprehensive results.

### Rate Limits

- **ClawHub**: 60 requests/hour (logged in: higher)
- **Skills.sh**: Check with `npx skills --help`

---

## 📦 Dependencies

- Node.js + npx
- curl
- jq

---

## 🦞 Summary

**One line: User writes in ANY language → Search both ClawHub & Skills.sh → Respond in user's language → Suggest chain for complex tasks**

---
