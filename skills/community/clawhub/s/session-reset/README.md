# Session Reset Skill

安全地重置 OpenClaw agent sessions，支持备份、预览、恢复和批量操作。

[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.ai)
[![Version](https://img.shields.io/badge/version-1.0.0-green)]()

---

## 快速开始

### 安装

```bash
# 方式一：通过 OpenClaw CLI 安装
openclaw skill install session-reset

# 方式二：手动安装
openclaw skill load session-reset.skill

# 方式三：直接从源码
openclaw skill load ~/.openclaw/skills/session-reset/
```

### 首次使用 - 初始化配置

**重要**：首次使用前必须执行初始化，配置默认 agents：

```bash
# 运行初始化（自动发现 agents，交互式选择）
openclaw session-reset --init

# 初始化流程：
# 1. 扫描 ~/.openclaw/ 发现所有 agents
# 2. 选择导入方式：[1]导入全部 [2]多选 [3]取消
# 3. 保存配置到 ~/.openclaw/session-reset-config.json
```

### 验证安装

```bash
# 查看帮助
openclaw session-reset --help

# 测试预览模式（不执行实际重置）
openclaw session-reset --scope default --dry-run
```

---

## 功能特性

| 特性 | 说明 |
|------|------|
| 🔒 **安全备份** | 每次重置前自动创建带时间戳的备份 |
| 👁️ **预览模式** | `--dry-run` 先预览，确认后再执行 |
| 🎯 **灵活范围** | 支持 default/all/agents/cron/subagent/指定 agents |
| 🔄 **一键恢复** | `--restore` 从任意历史备份恢复 |
| 🧹 **自动清理** | `--cleanup` 清理过期备份（默认30天/10个） |
| ⚡ **批量操作** | 一键重置六部+秘书，或自定义 agent 列表 |
| 🚀 **初始化向导** | `--init` 自动发现 agents，交互式配置 |

---

## 初始化配置（首次使用必做）

### 为什么需要初始化

`--scope agents` 需要知道你的默认 agents 列表。初始化过程会：

1. **自动发现**：扫描 `~/.openclaw/` 目录找到所有 agents
2. **交互选择**：选择导入全部、多选或取消
3. **保存配置**：将选择保存到配置文件，后续直接使用

### 初始化流程

```bash
# 运行初始化
openclaw session-reset --init
```

交互示例：

```
🔍 发现以下 agents:
  1. main (秘书)
  2. hubu (户部)
  3. libu (礼部)
  4. xingbu (刑部)
  5. bingbu (兵部)
  6. libu_hr (吏部)
  7. gongbu (工部)

请选择操作:
  [1] 导入全部 agents
  [2] 多选（自定义）
  [3] 取消

输入选项 (1-3): 1

✅ 已保存配置: ~/.openclaw/session-reset-config.json
```

### 配置文件说明

```json
{
  "default_agents": ["main", "hubu", "libu", "xingbu", "bingbu", "libu_hr", "gongbu"],
  "initialized_at": "2025-03-05T14:58:00"
}
```

> 💡 如需修改 agents 列表，重新运行 `openclaw session-reset --init` 即可。

---

## 使用场景

### 场景 1：首次使用（初始化）

新安装 skill 后，先初始化配置：

```bash
# 初始化（自动发现 agents）
openclaw session-reset --init

# 然后即可使用 agents scope
openclaw session-reset --scope agents --dry-run
```

### 场景 2：修改 SOUL.md 后让配置生效

当你修改了 Agent 的 `SOUL.md` 或 `AGENTS.md`，需要重置 session 才能加载新配置：

```bash
# 先预览将要重置哪些 sessions
openclaw session-reset --scope default --dry-run

# 确认无误后执行重置
openclaw session-reset --scope default
```

> 💡 重置后，Agent 下次收到消息时会自动创建新 session，加载最新的配置文件。

### 场景 3：批量重置六部+秘书

团队配置大规模更新后，需要批量重置所有 agents：

```bash
# 重置六部+秘书的所有 Discord sessions
openclaw session-reset --scope agents
```

### 场景 4：清理过期会话释放空间

定期维护，清理不再需要的 sessions：

```bash
# 清理并查看释放的空间
openclaw session-reset --scope default --cleanup
```

### 场景 5：恢复误删的会话

如果重置后发现有问题，可以从备份恢复：

```bash
# 查看可用备份
openclaw session-reset --list-backups

# 恢复到指定时间点
openclaw session-reset --restore 20250305_143022
```

---

## 命令详解

### 初始化命令

```bash
# 首次使用 - 交互式初始化
openclaw session-reset --init

# 初始化流程说明：
# 1. 扫描 ~/.openclaw/agents/ 目录发现所有 agents
# 2. 交互选择：[1]导入全部 [2]多选 [3]取消
# 3. 保存配置到 ~/.openclaw/session-reset-config.json
# 4. 后续 --scope agents 将使用此配置
```

### 基本命令

```bash
# 重置所有 Discord 频道 sessions（默认，不含 Cron/Subagent）
openclaw session-reset --scope default

# 预览模式（不执行实际重置，仅显示统计信息）
openclaw session-reset --scope default --dry-run

# 重置六部+秘书的 sessions
openclaw session-reset --scope agents

# 重置指定 agents（逗号分隔）
openclaw session-reset --scope main,hubu,libu

# 重置所有 sessions（含 Cron + Subagent）
openclaw session-reset --scope all

# 仅重置 Cron 任务
openclaw session-reset --scope cron

# 仅重置 Subagent
openclaw session-reset --scope subagent
```

### 备份管理

```bash
# 查看所有备份
openclaw session-reset --list-backups

# 从指定备份恢复
openclaw session-reset --restore 20250305_143022

# 清理旧备份（默认：30天前，最多保留10个）
openclaw session-reset --cleanup

# 自定义清理策略
openclaw session-reset --cleanup --cleanup-days 7 --cleanup-max 5
```

### 高级选项

```bash
# 强制执行，跳过确认提示
openclaw session-reset --scope default --force
```

---

## Scope 参数详解

| Scope 值 | 说明 | 适用场景 |
|----------|------|----------|
| `default` | 所有 Discord 频道 sessions | 日常清理，最常用的选项 |
| `all` | 全部 sessions（含 Cron/Subagent） | 彻底重置，包含所有类型 |
| `agents` | 仅六部+秘书的 Discord 频道 | 批量重置团队 agents |
| `cron` | 仅 Cron 任务 sessions | 重置定时任务状态 |
| `subagent` | 仅 Subagent sessions | 清理子代理会话 |
| `agent1,agent2` | 指定 agents（逗号分隔） | 精确控制重置范围 |

---

## 安全机制

### 1. 强制备份

任何重置操作前，自动创建带时间戳的备份：

```
备份位置：~/.openclaw/session-backups/YYYYMMDD_HHMMSS/
├── manifest.json          # 备份清单
├── agent:main:...jsonl    # session 文件
├── agent:hubu:...jsonl
└── ...
```

### 2. 二次确认

执行前显示统计信息，需输入 `yes` 确认：

```
⚠️  即将重置以下 sessions:
   - Discord Channel Sessions: 12
   - Agents affected: main, hubu, libu, ...
   - Estimated size: 2.5MB

   此操作将删除上述 sessions，下次消息触发时自动重建。
   备份已创建: ~/.openclaw/session-backups/20250305_143022/

确认重置? 输入 'yes' 继续: yes
```

### 3. 预览模式

`--dry-run` 仅显示将要重置的内容，不产生实际影响：

```bash
openclaw session-reset --scope default --dry-run

# 输出示例：
[DRY RUN] 将要重置的 sessions:
  - agent:main:discord:channel:xxx (main)
  - agent:hubu:discord:channel:xxx (hubu)
  ...

[DRY RUN] 总计: 12 sessions
```

### 4. 可恢复性

支持从任意历史备份恢复：

```bash
# 查看备份列表
openclaw session-reset --list-backups

Available backups:
  1. 20250305_143022 (24.5 MB, 7 days ago)
  2. 20250304_091530 (18.2 MB, 8 days ago)
  ...

# 恢复
openclaw session-reset --restore 20250305_143022
```

---

## 备份策略

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--cleanup-days` | 30 | 保留最近 N 天的备份 |
| `--cleanup-max` | 10 | 最多保留 N 个备份 |

```bash
# 使用默认策略清理
openclaw session-reset --cleanup

# 自定义策略：保留7天，最多5个备份
openclaw session-reset --cleanup --cleanup-days 7 --cleanup-max 5
```

---

## 注意事项

⚠️ **重要提示**

- 重置后 agents 会**丢失当前会话上下文**
- 下次收到消息时会**自动创建新的 session**
- 建议在**低峰期**执行批量重置
- 重要操作前使用 `--dry-run` 预览
- 无法重置**当前正在运行的 session**（需从外部终端执行）

---

## 故障排查

### 问题：命令未找到

```bash
# 检查 skill 是否已安装
openclaw skill list

# 如果没有，重新安装
openclaw skill install session-reset
```

### 问题：权限不足

```bash
# 确保对 ~/.openclaw 目录有写权限
ls -la ~/.openclaw/

# 如果需要，修改权限
chmod -R u+rw ~/.openclaw/
```

### 问题：备份恢复失败

```bash
# 检查备份是否存在
openclaw session-reset --list-backups

# 检查备份文件完整性
ls -la ~/.openclaw/session-backups/YYYYMMDD_HHMMSS/
```

---

## 相关链接

- [SKILL.md](./SKILL.md) - 详细功能文档
- [examples/](./examples/) - 使用示例
- [OpenClaw 文档](https://docs.openclaw.ai) - 官方文档

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2025-03-05 | 初始版本，支持基础重置、备份、恢复功能 |

---

## License

MIT License - 详见 [LICENSE](./LICENSE)

---

*Built with ❤️ for OpenClaw*
