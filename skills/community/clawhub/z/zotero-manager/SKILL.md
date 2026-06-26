---
name: zotero-manager
description: [已整合] Zotero 文献管理已整合到 knowledge 统一入口技能
argument-hint: "[操作] [参数]"
---

# ⚠️ 已整合 - 请使用 knowledge 统一入口

> **本技能保留用于向后兼容，功能已整合到 `knowledge` 统一入口技能**
>
> **推荐使用：** `knowledge zotero [操作]` 或直接使用本技能（自动转发）

---

# Zotero Manager（兼容层）

Zotero 文献管理技能，支持文献检索、导入、分类管理。

## 迁移指南

**新用法：**
```
knowledge zotero search 关键词
knowledge zotero import DOI
knowledge zotero list 分类
knowledge zotero export 格式
```

**旧用法（仍然可用）：**
```
zotero search 关键词
```

## 配置要求

**获取 API Key:**
1. 访问 https://www.zotero.org/settings/keys
2. 点击 "Create a new personal access token"
3. 勾选权限：Read Library

**存储凭据:**
```bash
mkdir -p ~/.config/zotero
echo "your_api_key" > ~/.config/zotero/api_key
```

## 核心功能
- ✅ 文献检索（关键词/分类/标签）
- ✅ DOI 导入
- ✅ 分类管理
- ✅ 参考文献导出（BibTeX/RIS）

## 安全说明
- ✅ 仅发送到官方 API（api.zotero.org）
- ❌ 不要分享 API Key
- ❌ 不要硬编码在脚本中
