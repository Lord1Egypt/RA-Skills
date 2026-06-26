# Agent Memory SDK 快速入门

3分钟上手，5个方法，零配置启动。

## 安装

```bash
pip install -e .
# 或完整安装（含语义搜索、中文分词）
pip install -e ".[all]"
```

## 30秒体验

```python
from agent_memory import Memory

mem = Memory()  # 零配置，自动创建 ~/.agent_memory/default.db

# 记住
result = mem.remember("部署了v2.1版本，修复了登录Bug")
print(result.memory_id)  # mem_abc123

# 回忆
results = mem.recall("部署")
for r in results.items:
    print(r["content"])  # "部署了v2.1版本，修复了登录Bug"

# 忘记
mem.forget(result.memory_id)  # 软删除，30天内可恢复
```

## 核心方法

### remember() — 记住

```python
result = mem.remember(
    content="用户偏好深色主题",     # 必填：记忆内容
    importance="high",              # 可选：high/medium/low
    topics=["用户偏好", "UI设置"],   # 可选：主题标签
    metadata={"source": "chat"},    # 可选：元数据
)
```

返回 `SaveResult`：
- `memory_id` — 记忆ID
- `accepted` — 是否成功存入
- `status` — 状态（stored/duplicate/filtered/cooldown）
- `message` — 中文消息
- `tip` — 使用建议
- `quality_score` — 质量评分（0-1）

### recall() — 回忆

```python
results = mem.recall(
    query="用户喜欢什么",    # 必填：搜索查询
    limit=10,               # 可选：返回数量（1-100）
    mode="hybrid",          # 可选：hybrid/keyword/semantic
)
```

返回 `SearchResult`：
- `items` — 记忆列表
- `suggestions` — 空结果时的建议
- `explore` — 推荐浏览的记忆
- `tip` — 搜索建议
- `degraded` — 降级组件列表

### forget() — 忘记

```python
result = mem.forget(
    memory_id="mem_abc123",  # 必填：记忆ID
    permanent=False,          # 可选：是否永久删除
)
```

返回 `DeleteResult`：
- `deleted` — 是否成功删除
- `status` — 状态（deleted/not_found/already_deleted）
- `restorable` — 是否可恢复

### update() — 更新

```python
mem.update(
    memory_id="mem_abc123",
    content="更新后的内容",  # 版本化，保留历史
)
```

### status() — 状态

```python
info = mem.status()
# {"healthy": True, "total_memories": 42, "components": {...}}
```

## 更多方法

```python
mem.revert(memory_id, version=2)   # 回滚到指定版本
mem.bookmark(memory_id)            # 收藏记忆
mem.unbookmark(memory_id)          # 取消收藏
mem.bookmarks()                    # 查看所有收藏
mem.echo()                         # 主动推荐相关记忆
mem.milestones()                   # 查看成就
mem.share_card()                   # 生成分享卡片
mem.close()                        # 释放资源
```

## 多项目隔离

```python
# 每个项目独立数据库
project_a = Memory(db_path="project_a.db")
project_b = Memory(db_path="project_b.db")
```

## 远程服务模式

```bash
# 先启动服务端
agent-memory serve
```

```python
# 任何项目连接远程服务
mem = Memory(server="http://localhost:8000", api_key="<YOUR_API_KEY>")
```

## 高级配置

```python
# 预设场景
mem = Memory(profile="chatbot")     # 高召回、快速响应
mem = Memory(profile="knowledge")   # 高精度、深度检索

# 细粒度覆盖
mem = Memory(
    profile="chatbot",
    recall_config={"max_results": 20},
)

# 上下文管理器
with Memory() as mem:
    mem.remember("临时记忆")
# 自动释放资源
```

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `AGENT_MEMORY_DB_PATH` | `~/.agent_memory/default.db` | 数据库路径 |
| `AGENT_MEMORY_PROFILE` | `personal` | 预设场景 |
| `AGENT_MEMORY_LOG_FORMAT` | `standard` | 日志格式（standard/json） |
| `AGENT_MEMORY_AUTO_PURGE_DAYS` | — | 自动清理天数 |
| `AGENT_MEMORY_PII_CHECK_ON_WRITE` | `false` | 写入时PII检测 |

## 兼容别名

SDK同时支持两套方法名：

| 品牌方法 | 兼容别名 | 说明 |
|----------|---------|------|
| `remember()` | `save()` | 记住 |
| `recall()` | `search()` | 回忆 |
| `forget()` | `delete()` | 忘记 |

推荐使用品牌方法名，更符合"记忆管家"的产品定位。
