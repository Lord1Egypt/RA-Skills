---
name: skill-finder
description: Multi-platform skill ranking and discovery system with 25,000+ skills. Supports Tencent SkillHub, Xfyun SkillHub, and local skills. Use when the user asks about skill rankings, best skills, skill recommendations, discovering new skills, or wants to install skills. Triggers on phrases like "rank skills", "best skills", "top skills", "skill recommendations", "install skill", "search skills", "热度最高", "最受欢迎的技能", "技能排名", "推荐技能".
---

# Skill Rank - Multi-Platform Skill Ranking & Discovery

A meta-skill that ranks **25,000+ skills** from multiple platforms and helps users discover and install high-quality skills.

## Supported Platforms

| Platform | Skills Count | Status | API |
|----------|-------------|--------|-----|
| **Tencent SkillHub** | 25,264 | ✅ Real-time | `https://lightmake.site/api/skills` |
| **Xfyun SkillHub** | 891 | ✅ Real-time | `https://skill.xfyun.cn/api/v1/skills` |
| **Local Installed** | Auto-detect | ✅ Auto-scan | N/A |

## Commands

### List Top Skills
```bash
skill-rank --list [--top N] [--source tencent|xfyun|local]
```

### Search Skills
```bash
skill-rank --search <keyword>
```

### View Skill Details
```bash
skill-rank --info <skill-name>
```

### Install a Skill
```bash
# Preview installation (dry run)
skill-rank --install <skill-name> --dry-run

# Actually install
skill-rank --install <skill-name>
```

### Update Database
```bash
skill-rank --update
```

### Show Configuration
```bash
skill-rank --config
```

## Workflow

When user asks about skill rankings or recommendations:

1. **Check database** - If empty or outdated, run `--update` first
2. **List or search** - Show ranked results
3. **Provide details** - Use `--info` for specific skills
4. **Help install** - Use `--install` to guide or execute installation

## Ranking Algorithm

Skills are scored based on:
- **Downloads** (60%) - Popularity indicator
- **Stars** (40%) - Community endorsement

Score = min(log₁₀(downloads + 1) × 15, 60) + min(log₁₀(stars + 1) × 20, 40)

## Installation Feature

The `--install` command supports:

1. **Automatic CLI detection** - Checks if `skillhub` or `clawhub` is installed
2. **Dry run mode** - Preview what would be installed with `--dry-run`
3. **Real-time output** - Streams installation progress
4. **Error handling** - Provides helpful installation instructions if CLI is missing

### CLI Installation

```bash
# For Tencent SkillHub
npm install -g @clawdbot/skillhub

# For ClawHub
npm install -g clawhub
```

## Example Usage

**User**: "What are the most popular skills?"
**Action**: Run `skill-rank --list --top 10`

**User**: "Find me a skill for PDF editing"
**Action**: Run `skill-rank --search pdf`

**User**: "Tell me about the github skill"
**Action**: Run `skill-rank --info github`

**User**: "Install the summarize skill"
**Action**: 
```bash
# First preview
skill-rank --install summarize --dry-run

# Then install
skill-rank --install summarize
```

**User**: "更新技能排名"
**Action**: Run `skill-rank --update`

**User**: "小红书相关的技能"
**Action**: Run `skill-rank --search 小红书`

## Data Sources

- **Tencent SkillHub**: https://skillhub.tencent.com
- **Xfyun SkillHub**: https://skill.xfyun.cn
- **Local**: `~/.openclaw/workspace/skills/`

## Top 10 Skills (by downloads)

1. **self-improving-agent** - 持续改进学习 (253K downloads)
2. **find-skills** - 发现并安装技能 (234K downloads)
3. **summarize** - URL/文件总结 (177K downloads)
4. **agent-browser** - 浏览器自动化 (147K downloads)
5. **gog** - Google Workspace CLI (119K downloads)
6. **github** - GitHub CLI (118K downloads)
7. **ontology** - 知识图谱 (117K downloads)
8. **skill-vetter** - 技能安全预审 (113K downloads)
9. **proactive-agent** - 主动智能体 (112K downloads)
10. **weather** - 天气预报 (101K downloads)

## No Dependencies

This skill uses only Python standard library:
- `urllib.request` - HTTP requests
- `sqlite3` - Local database
- `json` - JSON parsing
- `subprocess` - CLI execution

No pip install required!

## Limitations

- First `--update` may take 2-3 minutes to fetch all 25K+ skills
- Install commands require `skillhub` or `clawhub` CLI tools to be installed
- Network access required for real-time data
