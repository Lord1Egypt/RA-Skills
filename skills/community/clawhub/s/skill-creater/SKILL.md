---
name: skill-creater
description: Generate complete AgentSkills from user requirements. Creates SKILL.md, scripts, references, assets folders, and packages them into a ready-to-upload archive for Clawhub. Use when the user wants to create a new skill, build a custom skill, or package an existing skill for distribution.
---

# Skill Craftsmen

A meta-skill that generates other skills. Transform your ideas into production-ready AgentSkills with proper structure, documentation, and packaging.

## What This Skill Does

1. **Interviews you** to understand what skill you want to build
2. **Generates complete skill structure** including SKILL.md, scripts, references
3. **Packages everything** into a ready-to-upload `.zip` archive
4. **Provides Clawhub upload guidance**

## Quick Start

```
User: "帮我创建一个处理PDF的Skill"
→ This skill interviews → Generates → Packages → Delivers zip file
```

## Usage Flow

### Step 1: Intent Capture (自动)

Skill会自动询问关键问题：
- 这个skill要解决什么问题？
- 用户会怎么描述需求来触发它？
- 需要哪些功能？简单的还是复杂的？
- 需要脚本/工具吗？还是纯文本指导？

### Step 2: Structure Generation

根据需求生成：
```
your-skill/
├── SKILL.md              # 主文档 (name, description, instructions)
├── manifest.json         # Clawhub元数据
├── scripts/              # 可选: 可执行脚本
│   └── (Python/Node.js/Bash)
├── references/           # 可选: 参考文档、示例
│   └── (schemas, examples, guides)
├── assets/               # 可选: 模板、图标等
│   └── (templates, icons, images)
└── README.md             # 安装说明 (可选)
```

### Step 3: Package & Deliver

自动打包为 `your-skill-v1.0.0.zip`，包含：
- 完整目录结构
- 验证过的manifest.json
- 可直接上传Clawhub

## Skill Complexity Levels

| 级别 | 特点 | 包含内容 |
|------|------|---------|
| **Simple** | 纯文本指导 | SKILL.md only |
| **Standard** | 带辅助脚本 | SKILL.md + scripts/ |
| **Advanced** | 完整工具集 | SKILL.md + scripts/ + references/ + assets/ |

## Best Practices Applied

This skill automatically ensures:
- ✅ YAML frontmatter format compliance
- ✅ Description includes "when to use" triggers
- ✅ Proper directory structure
- ✅ Concise SKILL.md (<500 lines)
- ✅ Progressive disclosure design

## Output Example

```
📦 Generated: pdf-master-v1.0.0.zip

📁 Contents:
├── SKILL.md              ✓ Valid YAML frontmatter
├── manifest.json         ✓ Clawhub ready
├── scripts/
│   ├── merge.py
│   ├── split.py
│   └── rotate.py
├── references/
│   ├── examples.md
│   └── api-guide.md
└── README.md

🚀 Next Steps:
1. Extract the zip
2. Test locally: openclaw skill install ./pdf-master
3. Upload to Clawhub: https://clawhub.com/upload
```

## Clawhub Upload Checklist

Generated skills include:
- [x] Valid manifest.json with version, author, tags
- [x] SKILL.md with proper YAML frontmatter
- [x] Scripts are executable (if included)
- [x] No unnecessary files (README optional)
- [x] Compressed with proper structure

---

*Craft your skills. Share with the world.*
