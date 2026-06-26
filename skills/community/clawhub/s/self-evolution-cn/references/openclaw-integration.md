# OpenClaw 集成

## 工作区结构

```
~/.openclaw/
├── workspace-agent1/
│   ├── SOUL.md                 # 行为准则（所有 agent 加载）
│   ├── TOOLS.md                # 工具能力
│   ├── MEMORY.md               # 长期记忆（仅主会话）
│   ├── .learnings/             # 学习记录（软链接 → 共享目录）
│   └── memory/                 # 每日记忆
├── shared-learning/            # 共享学习目录
│   ├── ERRORS.md
│   ├── LEARNINGS.md
│   └── FEATURE_REQUESTS.md
├── skills/self-evolution-cn/   # 技能目录
│   ├── SKILL.md
│   ├── scripts/
│   ├── hooks/openclaw/
│   ├── references/
│   ├── logs/
│   └── heartbeat-state.json
└── hooks/self-evolution-cn/    # Hook 安装目录
    ├── HOOK.md
    └── handler.js
```

## 快速设置

详见 `SKILL.md` 快速开始部分。

## 学习工作流

### 捕获学习

1. **会话内**：记录到 `.learnings/`
2. **跨会话**：提升到 SOUL.md（所有 agent 加载）

### 提升决策树

```
学习是否项目特定？
├── 是 → 保留在 .learnings/
└── 否 → 提升到 SOUL.md
```

详见 `references/promotion.md`

## 可用的 Hook 事件

| 事件 | 何时触发 |
|------|---------|
| `agent:bootstrap` | 在工作区文件注入之前 |
| `message:received` | 收到用户消息时 |
| `tool:after` | 工具执行之后 |

## 验证

检查 hook 是否已注册：

```bash
openclaw hooks list
```

## 故障排除

### Hook 未触发

1. 确保启用了 hook：`openclaw hooks enable self-evolution-cn`
2. 配置更改后重启 gateway
3. 检查 gateway 日志

### 学习未持久化

1. 验证 `.learnings/` 目录存在
2. 检查文件权限
3. 确保工作区路径配置正确

### Cron 任务未运行

1. 检查 crontab：`crontab -l`
2. 检查日志：`cat ~/.openclaw/skills/self-evolution-cn/logs/heartbeat-daily.log`
3. 手动运行：`bash scripts/trigger-daily-review.sh`

### 软链接问题

1. 检查软链接：`ls -la ~/.openclaw/workspace-agent1/.learnings`
2. 检查共享目录：`ls -la $SHARED_LEARNING_DIR`
3. 重新运行配置脚本：`./scripts/setup.sh`

## Cron 任务

### 查看当前 Cron 任务

```bash
crontab -l | grep trigger-daily-review
```

### 手动触发检查

```bash
bash ~/.openclaw/skills/self-evolution-cn/scripts/daily_review.sh
```

### 查看执行日志

```bash
tail -f ~/.openclaw/skills/self-evolution-cn/logs/heartbeat-daily.log
```

## 最佳实践

1. **定期检查**：每天运行日检查以识别重复模式
2. **及时提升**：当学习被证明时立即提升
3. **保持简洁**：保持学习记录简洁，只包含必要信息
4. **使用模板**：使用提供的模板确保一致性

## 相关文档

- `SKILL.md` - 主要文档
- `references/format.md` - 记录格式
- `references/promotion.md` - 提升机制
- `references/multi-agent.md` - 多 agent 支持
- `references/hooks-setup.md` - Hook 配置
- `hooks/openclaw/HOOK.md` - Hook 说明
