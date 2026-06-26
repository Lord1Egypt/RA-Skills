---
name: research-review-assistant
description: [已整合] 文献综述已整合到 research 统一入口技能
argument-hint: "[研究领域] [参数]"
---

# ⚠️ 已整合 - 请使用 research 统一入口

> **本技能保留用于向后兼容，功能已整合到 `research` 统一入口技能**
>
> **推荐使用：** `research review [领域] [参数]` 或直接使用本技能（自动转发）

---

# Research Review Assistant（兼容层）

科研文献综述与迭代助手 - 自动检索、结构化总结文献，支持多轮优化和综述草稿生成。

## 迁移指南

**新用法：**
```
research review RTHS 时滞补偿 max_papers=20
research review 振动控制 detailed
research review 深度学习 结构健康监测 iteration_rounds=3
```

**旧用法（仍然可用）：**
```
review RTHS 时滞补偿 max_papers=20
```

## 核心功能
- ✅ 自动检索指定领域最新论文（arXiv/PubMed/Google Scholar）
- ✅ 结构化总结（标题/作者/方法/创新点/结果/局限性）
- ✅ 相关性评估（与用户研究方向的关联度 1-10 分）
- ✅ 多轮迭代优化（根据用户反馈修订）
- ✅ 生成 SCI 格式综述草稿
- ✅ 支持基金申请文献支持模块

## 配置参数
- `max_papers` - 最大检索论文数（默认 30）
- `summary_length` - 总结长度（short/detailed/expert）
- `iteration_rounds` - 迭代轮次（默认 3 轮）

## 输出格式
Markdown（默认）| LaTeX（可选）| 国标格式（基金申请用）
