# OpenClaw Session History Share

openclaw以sessionKey为隔离级别的跨session共享对话历史。全部基于openclaw内部机制实现。

会话历史使用轻量注入+历史召回的二级缓存架构。

[![ClawHub](https://img.shields.io/badge/ClawHub-session--history--share-blue)](https://clawhub.com/session-history-share)

## 功能说明

### v1.0 - 轻量注入 ✅ 已实现

在每日重置后，自动将旧 Session 的压缩摘要注入新 Session 上下文。

#### 工作流程

```
每天 3:30 AM
  → Cron 读取所有活跃 Session 的 JSONL 尾部
  → 向前查找最近的 compaction 事件提取 summary
  → 或提取最近 200 条消息生成简要摘要
  → 写入 .session_history/<safeKey>/<safeKey>-YYYY-MM-DD.md

每天 4:00 AM
  → OpenClaw 定时重置 Session

新 Session 每轮对话
  → agent:bootstrap hook 读取最新存档
  → 注入到 bootstrapFiles (BOOTSTRAP.md)
  → 摘要拼入 prompt，模型"记住"之前的对话
```

**如果使用空闲时间重置，或者修改了定时重置的时间，可以自己修改一下定时任务的cron即可。**

#### 技术特点

- **自动压缩**：提取 compaction summary 或生成简要摘要
- **每轮注入**：通过 `agent:bootstrap` hook 每轮注入摘要
- **内存缓存**：同 Session 内只读一次磁盘
- **存档轮转**：每个 Session 保留最近 3 个存档

## 版本计划

| 版本 | 功能 | 状态 |
|------|------|------|
| v1.0 | **轻量注入** - 自动压缩 + bootstrap 注入 | ✅ 已发布 |
| v1.1 | **会话召回** - 向量检索 + 智能召回 | 🔄 计划中 |
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

## 安装

```bash
# 自动安装
node skills/session-history-share/scripts/install.sh

# clawhub
openclaw skills install session-history-share

# 手动安装
# 1. 复制 hook 目录到 ~/.openclaw/hooks/session-history-share/
# 2. 在 openclaw.json 注册 hook
# 3. 创建 cron 定时任务
```

## 卸载

```bash
node skills/session-history-share/scripts/uninstall.sh
```
