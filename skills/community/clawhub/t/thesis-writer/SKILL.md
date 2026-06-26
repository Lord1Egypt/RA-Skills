---
name: thesis-writer
description: [已整合] 学位论文写作已整合到 paper 统一入口技能
argument-hint: "[章节] [内容]"
---

# ⚠️ 已整合 - 请使用 paper 统一入口

> **本技能保留用于向后兼容，功能已整合到 `paper` 统一入口技能**
>
> **推荐使用：** `paper thesis [章节] [内容]` 或直接使用本技能（自动转发）

---

# Thesis Writer（兼容层）

学位论文撰写助手 - 基于 Claude Code 论文工作流理念，帮助硕士研究生高效完成学位论文。

## 迁移指南

**新用法：**
```
paper thesis chapter1 绪论
paper thesis abstract 硕士论文
paper thesis consistency 全文一致性检查
```

**旧用法（仍然可用）：**
```
thesis chapter1 绪论
```

## 核心功能
- 章节扩写
- 一致性修订
- 导师意见落实
- 降重去 AI 味
- 术语统一管理

## 推荐工作区结构
```
thesis-workspace/
├── drafts/                 # 当前论文正文
├── papers/                 # 已有小论文或方法原稿
├── reference/              # 范文、优秀论文、章节参考
├── templates/              # LaTeX/Word 模板和章节模板
├── notes/                  # 术语表、导师意见、图表索引
└── .openclaw/skills/paper/ # 本技能
```

## 写作规范（硬约束）
- ✅ 使用正式学术表达，避免口语化
- ✅ 不用"我们"，改用"本文""本章"
- ✅ 缩写首次出现必须写中英文全称
- ✅ 术语翻译全文统一
- ✅ 不得编造实验数据
- ✅ 不得新增不存在的引用
