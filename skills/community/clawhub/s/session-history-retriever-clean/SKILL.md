---
name: session-history-retriever
description: "查看历史会话记录并引用导入到本地对话。使用 sessions_list、sessions_history 和 sessions_send 工具管理会话历史。适用于：(1) 查找过往对话，(2) 回顾工作进度，(3) 导入历史上下文到当前会话。NOT for: 需要浏览器自动化或外部 API 的会话管理。"
metadata:
  {
    "openclaw":
      {
        "emoji": "📜",
        "requires": {},
        "install": [],
      },
  }
---

# Session History Retriever 技能

使用 OpenClaw 的会话管理工具查看历史对话、检索消息，并引用导入到本地对话中。

## 核心功能

这个技能帮你：
- 🔍 **查找会话**：列出所有会话，按时间、活跃度筛选
- 📖 **查看历史**：获取特定会话的完整消息历史
- 📤 **引用导入**：将历史内容发送到新会话或当前会话
- 🎯 **快捷对话**：基于历史上下文快速继续工作

## When to Use

✅ **使用这个技能当：**
- 需要查看昨天的工作记录
- 想回顾之前的对话内容
- 需要导入历史上下文继续工作
- 查找特定会话的消息
- 审计会话使用情况
- 恢复中断的工作流

## When NOT to Use

❌ **不要使用这个技能当：**
- 需要浏览器自动化（用 browser 工具）
- 需要外部 API 调用（用其他技能）
- 只是闲聊不需要历史记录
- 需要创建新会话（用 sessions_spawn）

## 会话列表

### 列出所有会话

```bash
# 列出最近的会话
sessions_list --limit 20

# 筛选活跃会话（最后活跃 N 分钟）
sessions_list --activeMinutes 60 --limit 10

# 筛选特定类型的会话
sessions_list --kinds ["acp", "subagent"] --limit 15
```

### 会话列表输出示例

```json
{
  "count": 1,
  "sessions": [
    {
      "key": "agent:main:main",
      "kind": "other",
      "channel": "webchat",
      "updatedAt": 1773620866778,
      "sessionId": "22e7d1aa-7f9d-4d7e-9bed-821466ed8d51",
      "model": "Qwen3.5-9B-Q8_0.gguf",
      "contextTokens": 160000
    }
  ]
}
```

**关键字段**：
- `key`: 会话键（如 `agent:main:main`）
- `sessionId`: 当前 transcript ID
- `updatedAt`: 最后更新时间
- `contextTokens`: 当前上下文 token 数

## 查看会话历史

### 获取完整历史

```bash
# 获取会话历史（最多 N 条消息）
sessions_history --sessionKey agent:main:main --limit 50

# 包含工具调用信息
sessions_history --sessionKey agent:main:main --limit 30 --includeTools=true
```

### 历史输出结构

```json
{
  "sessionKey": "agent:main:main",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "昨天的文章写好了吗？"
        }
      ],
      "timestamp": 1773619868563
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "好的，我找到了文章..."
        }
      ],
      "timestamp": 1773619927993
    }
  ],
  "truncated": true
}
```

## 引用导入到对话

### 发送消息到新会话

```bash
# 向特定会话发送消息
sessions_send --sessionKey agent:main:main --message "基于之前的讨论，继续..."

# 使用标签引用
sessions_send --label "昨天的工作" --message "继续昨天的文章审查工作"
```

### 发送消息参数

- `sessionKey`: 目标会话键（如 `agent:main:main`）
- `label`: 会话标签（用于识别）
- `message`: 要发送的消息内容
- `agentId`: 目标 agent ID（可选）
- `timeoutSeconds`: 超时时间（秒）

## 常用工作流程

### 1. 回顾昨天的工作

```bash
# 第一步：列出会话
sessions_list --limit 10

# 第二步：找到昨天的会话（通过 updatedAt 时间）
# 第三步：获取历史
sessions_history --sessionKey agent:main:main --limit 50

# 第四步：分析内容，找到相关工作
# 第五步：发送新消息继续
sessions_send --sessionKey agent:main:main --message "根据昨天的审查结果，继续修改..."
```

### 2. 跨会话引用

```bash
# 从旧会话提取信息
history=$(sessions_history --sessionKey agent:main:main --limit 20)

# 发送到新会话
sessions_send --label "历史参考" --message "以下是之前讨论的内容..." "$history"
```

### 3. 会话审计

```bash
# 列出所有活跃会话
sessions_list --activeMinutes 1440 --json

# 检查特定会话的 token 使用情况
sessions_status --sessionKey agent:main:main

# 查看模型使用情况
session_status --sessionKey agent:main:main
```

## 会话键识别

### 主会话（直接聊天）
```
agent:<agentId>:main
```

### 群组会话
```
agent:<agentId>:channel:group:<id>
```

### 频道会话（Discord/Slack）
```
agent:<agentId>:channel:channel:<id>
```

### 定时任务
```
cron:<job.id>
```

### 节点运行
```
node-<nodeId>
```

## 会话状态检查

### 检查会话状态

```bash
session_status --sessionKey agent:main:main

# 输出示例
{
  "key": "agent:main:main",
  "model": "Qwen3.5-9B-Q8_0.gguf",
  "contextTokens": 160000,
  "inputTokens": 45000,
  "outputTokens": 12000,
  "totalTokens": 57000,
  "updatedAt": 1773620866778
}
```

## 实用脚本示例

### 查找最近 N 天的会话

```bash
#!/bin/bash
# 查找 7 天内活跃的会话
sessions_list --activeMinutes 10080 --limit 20 --json | \
  jq '.sessions[] | "\(.key): \(.updatedAt | fromdateiso8601)"'
```

### 导出会话历史为文件

```bash
#!/bin/bash
# 导出会话历史到文件
HISTORY_FILE="session_history_$(date +%Y%m%d).json"
sessions_history --sessionKey agent:main:main --limit 100 > "$HISTORY_FILE"
echo "已保存至：$HISTORY_FILE"
```

### 快速继续中断的工作

```bash
#!/bin/bash
# 1. 列出会话
echo "📋 可用会话："
sessions_list --limit 10 --json

# 2. 选择会话后继续
echo "继续工作..."
sessions_send --sessionKey agent:main:main --message "继续昨天的文章修改工作..."
```

## 常见问题

### Q: 如何找到昨天的会话？
A: 查看 `updatedAt` 时间戳，昨天的会话会在时间上接近但早于今天。

### Q: 会话历史被截断怎么办？
A: 使用更大的 `limit` 值，如 `--limit 200`。如果仍然被截断，说明会话很长，可能需要分次查看。

### Q: 如何在多个会话间切换？
A: 使用 `sessionKey` 指定目标会话，或在新会话中引用旧会话的内容。

### Q: 如何知道会话使用了多少 token？
A: 使用 `session_status --sessionKey <key>` 查看详细的 token 使用情况。

### Q: 会话超过上下文限制怎么办？
A: 发送 `/compact` 命令让系统自动压缩旧对话，或使用 `sessions_send` 选择性地导入关键内容。

## 最佳实践

1. **定期整理**：定期清理不活跃的会话
2. **合理使用**：不要导入过长的历史，只引用相关内容
3. **标注清晰**：使用 `label` 参数给会话添加描述性标签
4. **及时保存**：重要工作完成后，导出或保存到记忆文件
5. **注意隐私**：不要将敏感内容发送到新的会话

## 相关工具

- `sessions_spawn` - 创建新会话
- `session_status` - 查看会话状态
- `memory_get` - 读取记忆文件
- `read` - 读取本地文件

## 示例：完整工作流程

```bash
# 场景：想继续昨天的文章审查工作

# 1. 查看有哪些会话
sessions_list --limit 10

# 2. 查看主要会话的历史
sessions_history --sessionKey agent:main:main --limit 50

# 3. 找到昨天关于文章审查的讨论
# （搜索关键词如"审查"、"文章"、"修改"）

# 4. 基于上下文继续工作
sessions_send --sessionKey agent:main:main --message \
  "根据昨天审查的结果，我发现了以下问题需要修改：\n1. 导入语句不完整\n2. User-Agent 字符串有省略号\n3. 代码缩进需要统一\n\n请帮我生成修改后的版本..."

# 5. 或者创建新会话继续
sessions_spawn --task "继续修改浏览器搜索技能文章，基于昨天的审查报告" \
  --label "文章修改工作"
```

---

**提示**：记住，会话历史是工作记忆的重要组成部分。定期回顾和引用历史，可以让你的工作流程更加连贯高效！📚✨
