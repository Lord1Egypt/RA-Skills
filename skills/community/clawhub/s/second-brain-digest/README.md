# second-brain-digest

> 碎片内容提炼工作流 · Content-to-Knowledge Card Workflow

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-brightgreen)]()

**信息过了脑子不算学到，变成卡片才算你的。**

---

## 解决什么问题

你每天收藏文章、截图、随手记录想法，但这些内容：
- 躺在收藏夹里再也不看
- 总结了但找不到，或找到了看不懂自己在说什么
- 和其他知识完全割裂，没有形成体系

second-brain-digest 把碎片内容提炼成**标准原子卡片**，并发现与已有知识的关联——让你的知识库越用越聪明。

---

## 核心设计：原子卡片

```
标题：[一句陈述句，说明这张卡片的观点]
核心内容：[是什么 + 为什么 + 适用条件]
来源：[出处]
标签：#领域 #概念
强度：强/中/弱
```

**原子原则：** 一张卡片只有一个核心想法。多个想法 = 多张卡片。

**标题必须是陈述句：**
- ❌ "远程办公的优缺点"
- ✅ "远程办公在深度专注类工作中效率高于开放办公室"

---

## 支持的内容类型

| 类型 | 示例 | 提炼重点 |
|------|------|---------|
| 文章 / 长文 | 博客、论文、书摘 | 核心论点 + 证据 |
| 想法片段 | 随手灵感、对话感悟 | 补全逻辑 + 待验证标注 |
| 会议记录 | 会议纪要、访谈 | 决策 + 行动项 + 分歧 |
| 数据 / 研究 | 统计、调研结果 | 数字 + 适用范围 + 局限 |
| 操作经验 | 踩坑记录、最佳实践 | 方法 + 适用条件 |

---

## 输出格式支持

- 标准卡片格式（默认）
- Obsidian Markdown（含 frontmatter）
- Notion 数据库格式

---

## 快速安装

```bash
npx @skill-hub/cli install second-brain-digest --agent claude
clawhub install second-brain-digest
```

---

## 文件结构

```
second-brain-digest/
├── SKILL.md
├── README.md
├── references/
│   └── card-templates.md      # 各类型卡片模板 + 格式规范
├── examples/
│   └── example-article-digest.md
└── tests/
    └── test-cases.md
```

---

MIT License
