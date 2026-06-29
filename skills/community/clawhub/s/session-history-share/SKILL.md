# Session History Share

openclaw 以 sessionKey 为隔离级别的跨 session 共享对话历史。全部基于 openclaw 内部机制实现。

会话历史使用轻量注入 + 历史召回的二级缓存架构。

[![GitHub](https://img.shields.io/badge/GitHub-ouhaitao%2Fopenclaw--session--history--share-green)](https://github.com/ouhaitao/openclaw-session-history-share)

## 原理

```
3:30 AM → Cron 读取活跃 Session 的 JSONL
        → 提取 compaction summary 或最近消息摘要
        → 存档到 .session_history/<safeKey>/<safeKey>-YYYY-MM-DD.md

4:00 AM → OpenClaw 定时重置 Session

新 Session 每轮 → agent:bootstrap hook 读取最新存档
                → 注入到 bootstrapFiles (BOOTSTRAP.md)
                → 摘要拼入 prompt
```

## 安装

```bash
# 自动安装（创建 hook + 配置 cron）
node skills/session-history-share/scripts/install.sh

# clawhub
openclaw skills install session-history-share

# 或手动安装
# 1. 复制 hook 目录到 ~/.openclaw/hooks/session-history-share/
# 2. 在 openclaw.json 注册 hook
# 3. 创建 cron 定时任务
```

## 配置

### Hook 注册（openclaw.json）
```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "entries": {
        "session-history-share": {
          "enabled": true
        }
      }
    }
  }
}
```

### 定时任务
```bash
openclaw cron add \
  --name "定时压缩活跃会话" \
  --cron "30 3 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "执行以下步骤压缩所有活跃会话：\n\n1. 使用 sessions_list 获取所有活跃 session（排除 cron 和 subagent）\n2. 对每个 session 的 transcriptPath（JSONL 文件），执行以下步骤：\n   a. 使用 read 读取 JSONL 文件尾部（用 limit 从 offset 读取，不要读完整文件）\n   b. 从最后一条消息向前查找，找到最近的 compaction 事件（type=compaction）\n   c. 如果找到 compaction：提取 compaction.summary 字段的纯文本值\n   d. 如果没找到 compaction：提取最近 200 条 user/assistant 消息，生成简要摘要\n   e. 将摘要内容写入 .session_history/<safeSessionKey>/<safeSessionKey>-<YYYY-MM-DD>.md\n      - safeSessionKey 是把 sessionKey 中的冒号替换为下划线\n   f. 生成的摘要在**不丢失关键内容**的情况下尽可能的**简短**\n1. **文件内容只包含摘要正文纯文本，不要写任何 metadata header（不要 Session Key、Date、分隔线、标题等）**\n2. 每个 sessionKey 只保留最近 3 个存档文件，删除旧的\n3. 完成后回复 NO_REPLY"
```

## 技术特点

- **自动压缩**：提取 compaction summary 或生成简要摘要
- **每轮注入**：通过 `agent:bootstrap` hook 每轮注入摘要
- **内存缓存**：同 Session 内只读一次磁盘
- **存档轮转**：每个 Session 保留最近 3 个存档

## 查看日志

```bash
openclaw logs | grep "session-history"
```

## 卸载

```bash
node skills/session-history-share/scripts/uninstall.sh
```

## 文件结构

```
skills/session-history-share/
├── SKILL.md
├── README.md
├── scripts/
│   ├── install.sh
│   └── uninstall.sh
└── hook/
    ├── HOOK.md
    └── handler.js
```

## 版本计划

| 版本 | 功能 | 状态 |
|------|------|------|
| v1.0 | **轻量注入** - 自动压缩 + bootstrap 注入 | ✅ 已发布 |
| v1.1 | **历史召回** - 向量检索 + 智能召回 | 🔄 计划中 |
| v2.0 | **上下文引擎** - 完整 Context Engine 支持 | 📋 规划中 |

### v1.1 - 历史召回（计划中）

基于向量检索的智能历史召回：

- **向量索引**：将历史摘要向量化存储
- **智能召回**：根据当前对话内容，检索最相关的历史片段
- **动态注入**：不再注入全部历史，只注入与当前话题相关的片段
- **相关性排序**：按相关性排序返回 N 个最相关片段

### v2.0 - 上下文引擎（规划中）

完整的 Context Engine 支持：

- **持久化记忆**：Session 间持久化关键信息
- **语义检索**：基于语义相似度的历史搜索
- **主动提醒**：检测关键上下文变化时主动提醒用户
