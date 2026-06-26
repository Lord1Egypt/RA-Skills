# Secretary Memory Hook

秘书记忆系统的核心 Hook，将功能3、4、8的自动化从"不存在的事件"改为基于 OpenClaw 真实事件。

## 功能

| 事件 | 触发脚本 | 实现功能 |
|------|---------|---------|
| `session:compact:before` | `session_summary.py` | 功能3：会话自动摘要 |
| `session:compact:before` | `profile_miner.py` | 功能4：偏好自动提取 |
| `session:compact:after` | `context_loader.py` | 功能8：跨会话召回 |

## 背景

Secretary Memory v3.0 设计时假设 OpenClaw 支持 `session:start` 和 `session:end` 事件，但这些事件**实际上不存在**。本 Hook 利用真实存在的 `session:compact:before/after` 事件来实现相同效果。

## 安装

```bash
openclaw skills install secretary-memory-hook
```

或者克隆后手动安装：
```bash
cp -r secretary-memory-hook ~/.openclaw/hooks/
openclaw hooks enable secretary-memory
```

## 验证

```bash
openclaw hooks list
# 应看到 ✓ ready 状态的 secretary-memory

openclaw hooks check
# Hooks Status: 6/6 ready
```

## 依赖

- Node.js（运行 TypeScript handler）
- Python3（运行记忆脚本）
- secretary-memory skill（脚本目录）

## 工作原理

当对话过长触发压缩时：

```
compact:before → 压缩前 → 存摘要 + 提取偏好
compact:after  → 压缩后 → 加载上下文到新对话
```

## 注意事项

- 功能4（profile_miner.py）存在循环导入 bug，暂时跳过
- 功能3、功能8 已验证可用
