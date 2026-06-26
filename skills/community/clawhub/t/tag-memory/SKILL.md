---
name: tag-memory
description: 标签化长期记忆系统。当用户说"记住..."时存储记忆，当用户问"我之前..."时查询记忆，定期生成总结并询问确认，主动核对记忆正确性。支持标签(#偏好、#决定、#项目等)、BM25搜索、时间范围查询、人类审核机制。
disable-model-invocation: false
user-invocable: true
---

# TagMemory - 标签化长期记忆系统

## 版本
- **当前版本**: 1.0.0
- **核心功能**: 标签存储、BM25搜索、人类审核、定期归纳

## 功能描述

让 AI 记住用户的重要信息（偏好、决定、项目等），并支持人类审核确保记忆准确。

## 核心能力

- **🏷️ 标签化存储** - 为记忆打上语义标签
- **🔍 BM25 搜索** - 快速准确的关键词搜索
- **⏰ 时间标签** - 按时间段查询历史记忆
- **🤝 人类审核** - 确认/修正/删除记忆
- **📊 定期归纳** - 生成阶段性总结
- **🛡️ 隐私优先** - 本地存储，不上传云端

## 标签体系

| 标签 | 用途 | 示例 |
|------|------|------|
| `#偏好` | 用户偏好习惯 | "喜欢 tabs 缩进" |
| `#决定` | 重要决策 | "选择了 PostgreSQL" |
| `#项目` | 项目背景 | "在做电商项目" |
| `#人` | 人物信息 | "项目经理是张三" |
| `#事件` | 发生的事情 | "上周系统宕机了" |
| `#知识` | 学到的知识 | "学会了用 Docker" |
| `#错误` | 犯过的错误 | "之前选错了方案" |

## 使用场景

### 场景 1：用户说"记住..."

```
用户: "记住，我喜欢用 tabs 缩进，不喜欢 spaces"
智能体: 
  执行命令存储记忆
  回应: "✅ 已记住！你偏好 tabs 缩进"
```

**调用方式**:
```bash
cd ~/.openclaw/workspace/skills/tag-memory && python3 src/cli.py --json store << EOF
{"content": "用户偏好 tabs 缩进，不喜欢 spaces", "tags": ["#偏好", "#编程"]}
EOF
```

### 场景 2：用户问"我之前..."

```
用户: "我之前为什么选择了 PostgreSQL？"
智能体:
  执行命令查询记忆
  回应: "根据记录，你当时选择 PostgreSQL 是因为性能更好"
```

**调用方式**:
```bash
cd ~/.openclaw/workspace/skills/tag-memory && python3 src/cli.py --json query << EOF
{"query": "PostgreSQL 选择 原因", "tags": ["#决定"]}
EOF
```

### 场景 3：查询偏好

```
用户: "我的编程偏好是什么？"
智能体:
  执行命令查询
  回应: "根据记忆，你的偏好包括：喜欢 tabs 缩进..."
```

### 场景 4：查看所有记忆

```
用户: "我记住了哪些东西？"
智能体:
  执行命令列出
  回应: "📋 你共记住了 10 条记忆..."
```

**调用方式**:
```bash
cd ~/.openclaw/workspace/skills/tag-memory && python3 src/cli.py list
```

### 场景 5：核对记忆

```
用户: "我有哪记忆需要确认？"
智能体:
  执行命令获取待核对列表
  主动询问用户确认
```

**调用方式**:
```bash
cd ~/.openclaw/workspace/skills/tag-memory && python3 src/cli.py --json verify-pending << EOF
{"max_count": 3}
EOF
```

### 场景 6：生成总结

```
用户: "总结一下这周我们讨论了什么"
智能体:
  执行命令生成总结
  展示给用户确认
```

**调用方式**:
```bash
cd ~/.openclaw/workspace/skills/tag-memory && python3 src/cli.py --json summarize << EOF
{"days": 7}
EOF
```

### 场景 7：确认总结

```
智能体: "这是阶段性总结... 这对吗？"
用户: "对，存档"
智能体:
  执行确认命令
  回应: "✅ 总结已存档"
```

**调用方式**:
```bash
cd ~/.openclaw/workspace/skills/tag-memory && python3 src/cli.py --json summarize-confirm << EOF
{"feedback": "confirm"}
EOF
```

## CLI 命令速查

| 命令 | 用途 |
|------|------|
| `store` | 存储记忆 |
| `query <内容>` | 查询记忆 |
| `list` | 列出所有记忆 |
| `stats` | 查看统计 |
| `verify-pending` | 待核对列表 |
| `summarize [--days N]` | 生成总结 |
| `summarize-confirm [feedback]` | 确认总结 |

## Agent 追踪

每条记忆都会记录是哪个 agent 产生的：

| 字段 | 说明 |
|------|------|
| `agent_id` | agent 标识（main/agent-bot2/agent-bot3 等）|
| `🤖` | 在查询结果中显示 |

**存储时指定 agent_id：**
```bash
echo '{"content": "内容", "tags": ["#标签"], "agent_id": "main"}' | python3 src/cli.py --json store
```

**查询结果示例：**
```
1. ❓ [-1.22分] 这是小学蛋 agent 的记忆
   🏷️ #测试 | 📅 2026-03 | 🤖 agent-bot2
```

## 设计理念

TagMemory 的核心理念是**人类参与记忆维护**：

```
存储 ──→ 闲时核对 ──→ 定期归纳 ──→ 确认存档
  │          │            │           │
  ↓          ↓            ↓           ↓
打标签    纠正错误      生成总结     用户确认
```

**为什么这样做？**

1. AI 自动存储的记忆可能有错误
2. 没有人类审核，错误会累积
3. 定期归纳 + 确认 = 确保记忆准确
4. 闲时核对 = 发现错误及时纠正

## 与 LCM 的关系

| 系统 | 用途 | 数据 |
|------|------|------|
| **LCM** | 对话压缩/上下文管理 | AI 自己和用户说了什么 |
| **TagMemory** | 用户记忆/知识管理 | 用户告诉 AI 的重要信息 |

两者互补，不会冲突。
