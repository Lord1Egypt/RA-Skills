---
name: team-shared-memory
description: 多实例记忆共享，多个 Agent 之间同步记忆
version: 1.0.1
---

# Team Memory — 多实例记忆共享

**版本**: 1.0.1  
**创建日期**: 2026-03-11  
**更新日期**: 2026-04-14  
**作者: c32

---

## 📋 功能

| 功能 | 说明 |
|------|------|
| 记忆同步 | 跨 Agent 同步记忆数据 |
| 冲突解决 | 自动检测和处理记忆冲突 |
| 安全扫描 | secret-scan 检测敏感信息泄露 |
| 增量同步 | 只同步变更部分 |

---

## 📂 文件结构

```
skills/team-memory/
├── SKILL.md
├── skill.json
└── scripts/
    ├── sync.js              # 记忆同步主程序
    └── secret-scan.js       # 敏感信息扫描
```

---

## 📊 Cron 任务

| 任务名 | 频率 | Job ID |
|--------|------|--------|
| Team Memory 同步 | 每 12 小时 | `f47e2a9d` |

---

## ⚠️ 注意事项

- 同步间隔可配置
- 冲突时优先保留最新版本
- 安全扫描检测 API 密钥等敏感信息
