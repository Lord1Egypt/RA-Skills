---
name: research-daily-push
description: [已整合] 每日文献推送已整合到 research 统一入口技能
argument-hint: "[研究领域]"
---

# ⚠️ 已整合 - 请使用 research 统一入口

> **本技能保留用于向后兼容，功能已整合到 `research` 统一入口技能**
>
> **推荐使用：** `research daily [领域]` 或直接使用本技能（自动转发）

---

# Research Daily Push（兼容层）

科研文献每日推送 - 每天自动检索指定领域最新 arXiv 论文，生成结构化总结并推送。

## 迁移指南

**新用法：**
```
research daily RTHS
research daily 结构健康监测
research daily 深度学习 振动控制
```

**旧用法（仍然可用）：**
```
daily RTHS
```

## 特点
- ✅ 自动检索最近 24-48 小时论文
- ✅ 结构化总结（标题/作者/核心创新点/方法/结果）
- ✅ 重要性评估（引用潜力/创新度/相关性打分 1-10）
- ✅ Markdown 表格 + 详细总结
- ✅ 支持飞书/微信/邮件推送

## 执行流程
1. 读取用户研究方向
2. 检索论文（arXiv API，最近 2 天，5-10 篇）
3. 论文分析（标题/作者/创新点/方法/结果/重要性评分）
4. 生成推送（概览 + 详细列表+PDF 链接）

## 定时任务设置
```bash
openclaw cron add --name "daily-paper-push" --cron "0 8 * * *" --message "推送今日最新文献"
```
