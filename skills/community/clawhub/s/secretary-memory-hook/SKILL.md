---
name: secretary-memory-hook
description: 秘书记忆系统核心 Hook — 会话压缩时自动触发摘要/偏好提取/上下文召回。基于 session:compact:before 和 session:compact:after 事件，实现功能3（会话摘要）、功能4（偏好提取）、功能8（跨会话召回）的自动化。
---

# Secretary Memory Hook

秘书式记忆系统的核心 Hook，将原本依赖"不存在的事件"的自动逻辑，改为基于真实的 `session:compact:before` 和 `session:compact:after` 事件触发。

## 事件映射

| 功能 | 原设计（不可用） | 现设计（可用）|
|------|----------------|--------------|
| 功能3：会话自动摘要 | session:end（不存在）| session:compact:before ✅ |
| 功能4：偏好自动提取 | session:end（不存在）| session:compact:before ✅ |
| 功能8：跨会话召回 | session:start（不存在）| session:compact:after ✅ |

## 触发时机

```
对话进行中...
  ↓ 对话太长，触发 compact
session:compact:before
  → 运行 session_summary.py（生成摘要）
  → 运行 profile_miner.py（提取偏好）
  → 压缩历史
session:compact:after
  → 运行 context_loader.py（加载历史上下文）
  → 对话继续
```

## 依赖

需要先安装 secretary-memory skill（脚本所在目录）：
```
/root/.openclaw/workspace/skills/secretary-memory/scripts/
```

## 安装后

Hook 会自动被 OpenClaw 发现并启用：
```bash
openclaw hooks list  # 确认 secretary-memory 在列表中
openclaw hooks check # 确认状态为 ready
```

## 文件结构

```
~/.openclaw/hooks/secretary-memory/
├── HOOK.md      # Hook 元数据
└── handler.ts  # TypeScript 处理器
```
