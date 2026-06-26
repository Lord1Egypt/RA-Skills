# stock-data-monorepo 发布报告

**发布时间**: 2026-03-22  
**发布类型**: Monorepo 结构重构，支持独立安装

---

## ✅ 发布成功 - 全部 4 个技能

| 技能名称 | 新版本 | Skill ID | ClawHub 链接 | 状态 |
|----------|--------|----------|--------------|------|
| **cn-stock-volume** | v2.1.0 | `k97ekrd0xh6t7z33p4523psahd83czv7` | https://clawhub.ai/k97ekrd0xh6t7z33p4523psahd83czv7/cn-stock-volume | ✅ 已发布 |
| **stock-top-gainers** | v2.0.0 | `k972trnt3hbvcsebckva57wy3x83ct4f` | https://clawhub.ai/k972trnt3hbvcsebckva57wy3x83ct4f/stock-top-gainers | ✅ 已发布 |
| **ths-stock-themes** | v2.0.0 | `k97bz4gabx2t4dy3sg5m4pp1d983d9s5` | https://clawhub.ai/k97bz4gabx2t4dy3sg5m4pp1d983d9s5/ths-stock-themes | ✅ 已发布 |
| **stock-theme-events** | v2.0.0 | `k977h4vk7qn6qfh4aydtbxy7bn83c4kj` | https://clawhub.ai/k977h4vk7qn6qfh4aydtbxy7bn83c4kj/stock-theme-events | ✅ 已发布 |

---

## 📦 安装方式

用户可以单独安装任意技能：

```bash
# 安装成交量查询
npx clawhub@latest install cn-stock-volume

# 安装涨幅排名
npx clawhub@latest install stock-top-gainers

# 安装同花顺题材
npx clawhub@latest install ths-stock-themes

# 安装题材事件分析
npx clawhub@latest install stock-theme-events
```

---

## 📝 发布说明

### 版本号策略

- **cn-stock-volume**: v2.1.0（原有功能 + Monorepo 独立支持）
- **stock-top-gainers**: v2.0.0（major 版本，Monorepo 独立版本）
- **ths-stock-themes**: v2.0.0（major 版本，Monorepo 独立版本）
- **stock-theme-events**: v2.0.0（major 版本，Monorepo 独立版本）

### 变更内容

1. **Monorepo 结构** - 4 个技能统一在 stock-data-monorepo 仓库管理
2. **独立发布** - 每个技能可单独安装使用
3. **完整文档** - 每个技能都有独立的 README.md、package.json、_meta.json
4. **Git 同步** - 所有更改已提交并推送到 GitHub

### Git 提交记录

```
v2.0.0: Monorepo 独立版本，支持单独安装
v1.3.0: Monorepo 结构重构，支持独立安装使用
v1.2.3: Monorepo 结构重构，独立发布版本
v1.0.4: stock-theme-events 独立发布
v1.0.1: stock-top-gainers/ths-stock-themes 独立发布
```

---

## 🔗 相关链接

- **GitHub 仓库**: https://github.com/shinelp100/cn-stock-volume
- **ClawHub**: https://clawhub.ai
- **skill-publish-tool**: https://clawhub.ai/k976nx1d2sxx6a13t1ncfatc1s83bbdr/skill-publish-tool

---

## 📊 技能功能概览

### cn-stock-volume
- 获取四市（沪市/深市/创业板/北交所）成交金额
- 涨跌家数统计
- 增缩量分析

### stock-top-gainers
- 近 10 日涨幅排名前 20
- 自动排除 ST 股票
- 包含行业分类

### ths-stock-themes
- 同花顺个股题材查询
- 概念板块分类
- 人气排名榜单

### stock-theme-events
- 题材聚类分析
- 新闻事件关联
- 题材 - 事件报告生成

---

**发布完成时间**: 2026-03-22 10:35
