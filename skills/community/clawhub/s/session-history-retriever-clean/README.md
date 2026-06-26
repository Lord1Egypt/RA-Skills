# 📜 Session History Retriever

查看历史会话记录并引用导入到本地对话的 OpenClaw 技能。

<div align="center">

**查看历史 • 引用对话 • 快捷工作**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue.svg)](https://docs.openclaw.ai)
[![ClawHub](https://img.shields.io/badge/ClawHub-Ready-green.svg)](https://clawhub.com)

</div>

## 🎯 功能特性

这个技能帮你：

- 🔍 **查找会话** - 列出所有会话，按时间、活跃度筛选
- 📖 **查看历史** - 获取特定会话的完整消息历史
- 📤 **引用导入** - 将历史内容发送到新会话或当前会话
- 🎯 **快捷对话** - 基于历史上下文快速继续工作

## 🚀 快速开始

### 1. 列出所有会话

```bash
# 列出最近的会话
sessions_list --limit 20

# 筛选活跃会话（最后活跃 N 分钟）
sessions_list --activeMinutes 60 --limit 10

# 筛选特定类型的会话
sessions_list --kinds ["acp", "subagent"] --limit 15
```

### 2. 查看会话历史

```bash
# 获取会话历史（最多 N 条消息）
sessions_history --sessionKey agent:main:main --limit 50

# 包含工具调用信息
sessions_history --sessionKey agent:main:main --limit 30 --includeTools=true
```

### 3. 引用导入到对话

```bash
# 向特定会话发送消息
sessions_send --sessionKey agent:main:main --message "基于之前的讨论，继续..."

# 使用标签引用
sessions_send --label "昨天的工作" --message "继续昨天的文章审查工作"
```

## 📚 使用场景

### 场景 1：继续昨天的工作

```bash
# 1. 查看有哪些会话
sessions_list --limit 10

# 2. 查看主要会话的历史
sessions_history --sessionKey agent:main:main --limit 50

# 3. 基于历史继续工作
sessions_send --sessionKey agent:main:main --message \
  "根据昨天审查的结果，继续修改..."
```

### 场景 2：跨会话引用

```bash
# 从旧会话提取信息
history=$(sessions_history --sessionKey agent:main:main --limit 20)

# 发送到新会话
sessions_send --label "历史参考" --message "以下是之前讨论的内容..." "$history"
```

### 场景 3：会话审计

```bash
# 列出所有活跃会话
sessions_list --activeMinutes 1440 --json

# 检查特定会话的 token 使用情况
session_status --sessionKey agent:main:main
```

## 🔑 会话键识别

| 类型 | 格式 | 说明 |
|------|------|------|
| 主会话 | `agent:<agentId>:main` | 直接聊天 |
| 群组会话 | `agent:<agentId>:channel:group:<id>` | 群组聊天 |
| 频道会话 | `agent:<agentId>:channel:channel:<id>` | Discord/Slack |
| 定时任务 | `cron:<job.id>` | Cron 任务 |
| 节点运行 | `node-<nodeId>` | 节点执行 |

## 💡 实用脚本示例

### 查找最近 N 天的会话

```bash
# 查找 7 天内活跃的会话
sessions_list --activeMinutes 10080 --limit 20 --json | \
  jq '.sessions[] | "\(.key): \(.updatedAt | fromdateiso8601)"'
```

### 导出会话历史为文件

```bash
# 导出会话历史到文件
HISTORY_FILE="session_history_$(date +%Y%m%d).json"
sessions_history --sessionKey agent:main:main --limit 100 > "$HISTORY_FILE"
echo "已保存至：$HISTORY_FILE"
```

## ⚠️ 注意事项

- ❌ **不要使用**：需要浏览器自动化（用 browser 工具）
- ❌ **不要使用**：需要外部 API 调用（用其他技能）
- ❌ **不要使用**：只是闲聊不需要历史记录
- ❌ **不要使用**：需要创建新会话（用 sessions_spawn）

## 📖 文档

- [OpenClaw 文档](https://docs.openclaw.ai)
- [会话管理概念](https://docs.openclaw.ai/concepts/session)
- [压缩机制](https://docs.openclaw.ai/concepts/compaction)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 License

MIT License - 详见 [LICENSE](LICENSE)

---

<div align="center">

**让对话历史成为你工作记忆的一部分！** 📚✨

Made with ❤️ for OpenClaw Community

</div>
