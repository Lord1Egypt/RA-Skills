# Skill Registry | 技能注册表

> Last updated: YYYY-MM-DD
> Usage: When user asks "what skills" / "有什么技能", read this file and summarize by category.

## Quick Commands | 快捷命令

| Command | Effect |
|---------|--------|
| /skills | List all skills by category |
| /skills keyword | Find related skills |
| /技能 | 列出所有技能（分类） |
| /技能 关键词 | 查找相关技能 |

---

## Content Creation | 内容创作类

| Skill | Triggers | Description |
|-------|----------|-------------|
| example-skill | example, demo | Example skill template |

## Information | 信息获取类

| Skill | Triggers | Description |
|-------|----------|-------------|
| | | |

## Tools | 工具类

| Skill | Triggers | Description |
|-------|----------|-------------|
| | | |

## System | 系统类

| Skill | Triggers | Description |
|-------|----------|-------------|
| skill-registry | skills, 技能 | Skill discovery and routing |

---

## Discovery Guide | 发现指南

When user asks about skills:
1. "All skills" → List by category (brief)
2. Specific domain (e.g., "video skills") → Return that category only
3. "How to use XX" → Read `skills/XX/SKILL.md`

用户询问技能时：
1. "所有技能" → 按分类简要列出
2. 特定领域（如"视频技能"）→ 只返回相关类别
3. "XX怎么用" → 读取 `skills/XX/SKILL.md`

---

## Adding New Skills | 添加新技能

1. Create skill directory under `skills/`
2. Write `SKILL.md` (refer to existing skills)
3. Add entry to this file under appropriate category
4. Add triggers to RULES routing table (if auto-routing needed)
