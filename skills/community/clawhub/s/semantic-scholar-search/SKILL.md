---
name: semantic-scholar-search
description: [已整合] Semantic Scholar 搜索已整合到 search 统一入口技能
argument-hint: "[搜索关键词]"
---

# ⚠️ 已整合 - 请使用 search 统一入口

> **本技能保留用于向后兼容，功能已整合到 `search` 统一入口技能**
>
> **推荐使用：** `search scholar [关键词]` 或直接使用本技能（自动转发）

---

# Semantic Scholar Search（兼容层）

免费、高质量的学术论文检索工具 - 基于 Semantic Scholar API。

## 迁移指南

**新用法：**
```
search scholar machine learning
search scholar attention mechanism year=2020-
search scholar Yann LeCun
```

**旧用法（仍然可用）：**
```
scholar machine learning
```

## 特点
- ✅ 免费使用，无需注册
- ✅ 覆盖计算机科学、生物医学、物理等多个领域
- ✅ 提供论文引用数、作者信息、摘要等详细元数据
- ✅ 支持高级搜索和过滤

## 技术实现
- **API:** Semantic Scholar API v2
- **速率限制:** 免费层 100 次/小时
