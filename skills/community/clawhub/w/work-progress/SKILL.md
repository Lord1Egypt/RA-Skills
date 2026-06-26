---
name: work-progress
description: 工作进度检查技能 - 定期检查待办事项 + 子代理超时/消失检测与自动恢复 + 全量会话监控
version: 4.0.6
author: c32
---

# Work Progress Skill - 工作进度检查技能

**版本**: 4.0.6  
**创建日期**: 2026-03-11  
**更新日期**: 2026-04-14  
**作者**: c32

---

## 📋 技能描述

定期检查工作进度和待办事项完成情况，主动检测子代理超时/消失任务并自动恢复。

---

## 📂 文件结构

```
skills/work-progress/
├── SKILL.md                      # 本文件
├── skill.json                    # 技能元数据 (v4.0.2)
├── _meta.json                    # ClawHub 元数据
├── .clawhub/
│   └── origin.json               # 来源信息
├── state.json                    # 任务状态持久化（自动维护）
└── scripts/
    ├── check-progress.js         # 进度检查（Node.js）
    ├── auto-recover.js           # 自动恢复（Node.js）
    ├── work-monitor.js           # 全量会话监控（Node.js）
    └── install.js                # 安装脚本
```

---

## 🎯 功能

### check-progress.js — 进度检查
- 状态同步：发现/注册子代理任务
- 进度检查：超时检测
- 待办事项：检查 daily 文件
- 终态 GC：自动清理完成任务（5 分钟 grace period）

### auto-recover.js — 自动恢复
- 检查超时/消失/失败任务
- 记录到 error.md
- 建议恢复操作

### work-monitor.js — 全量会话监控
- 扫描所有 Agent 的活跃会话
- 检测超时/卡死/失败会话
- 输出结构化监控报告

---

## 📊 Cron 任务

| 任务 | 频率 | Job ID |
|------|------|--------|
| 工作进度检查 | 10m | `6a4bde16` |
| 全量工作监控 | 5m | `98f5a84a` |

---

## 🔄 状态机

```
pending → running → completed/failed/disappeared → notified → GC
```

---

*技能位置：`~/.openclaw/workspace/skills/work-progress/`*
