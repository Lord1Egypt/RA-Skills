---
name: skillhub-auto-installer
description: |
  搜索 Skillhub 技能市场，发现可用技能。
  此技能仅提供搜索功能，不执行任何安装或本地文件操作。
  关键词: skillhub, 搜索技能, findskill, 技能发现, 技能市场
---

# Skillhub Finder (技能搜索助手)

在 Skillhub 技能市场上搜索和发现可用技能。

⚠️ **重要声明**：
- 此技能 **仅提供搜索功能**
- **不执行安装**、不访问本地文件系统、不读取本地配置
- 如需安装技能，请参考官方文档手动操作

## 运行时依赖

| 依赖项 | 说明 | 必需 |
|--------|------|------|
| `node` | Node.js 运行时 | ✅ 必需 |
| `npx` | Node 包执行器 | ✅ 必需 |
| 网络访问 | 连接 skills.volces.com | ✅ 必需 |

## 能力

- 🔍 **仅搜索** Skillhub 技能（只读操作）
- 📊 展示搜索结果和技能详情

## 不做的事

- ❌ 不执行安装
- ❌ 不访问本地文件系统
- ❌ 不读取本地配置
- ❌ 不运行安全审计

## 使用方式

```
用户: "帮我搜索日历相关的技能"

智能体: [执行 search.sh] → 返回搜索结果 → 展示给用户
```

## 手动安装指南

如需安装搜索到的技能，请手动执行以下命令：

```bash
# 1. 搜索技能
SKILLS_API_URL=https://skills.volces.com/v1 npx -y skills find "关键词"

# 2. 安装技能（请自行审查后执行）
SKILLS_API_URL=https://skills.volces.com/v1 npx -y skills add <URL> -s <skill-name> -a openclaw -y --copy
```

## 安全注意事项

- 此技能 **仅搜索**，无安全风险
- 安装技能前，请仔细阅读目标技能的 SKILL.md
- 建议使用 SkillSentry 进行安全审计后再安装
