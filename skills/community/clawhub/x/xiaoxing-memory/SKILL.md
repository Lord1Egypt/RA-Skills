---
name: agent-memory
description: 记忆模块管理系统，让 AI Agent 拥有持久化记忆能力。当需要保存跨会话信息、检索历史记录、建立个人知识库、或执行记忆相关操作（搜索/读取/保存）时触发本技能。
---

# agent-memory

提供跨会话持久化记忆的架构和工作流。

## 核心架构

```
MEMORY.md          — 索引文件（总入口）
memory/            — 记忆存储目录
  YYYY-MM-DD.md    — 每日会话日志
  topic-*.md       — 主题记忆文件（可扩展）
openclaw-kk/memory/private/  — 用户私有记忆（可选）
```

## 工作流

### 保存记忆（两步走）

1. **写主题文件**（带 YAML frontmatter）：
```markdown
---
name: topic-name
description: 一句话描述该记忆内容
type: infrastructure|security|documentation|reference|automation
created: 2026-04-01
---

正文内容...
```

2. **更新索引**（在 MEMORY.md 中加入条目）：
```markdown
- [标题](文件名.md) 一句话语义钩子
```

### 检索记忆

使用 `memory_search` 工具搜索 MEMORY.md 和 memory/ 下的所有 .md 文件，返回语义相关的结果（top snippets + path + lines）。

**搜索时机**：回答任何关于历史任务、偏好、日期、人名等问题前，必须先 `memory_search`。

### 访问主题文件

搜索后若需要详细内容，用 `memory_get` 按 path/from/lines 读取对应行，避免将整个文件加载到上下文。

## 索引规则

- 索引行数控制在 200 行以内
- 详细内容不直接写入索引，只写"语义钩子"
- 定期整理：每日日志 → 提炼 → 并入主题文件 → 清理过时条目

## 禁止事项

- 禁止"记住这个"这类心理笔记，所有信息必须写文件
- 禁止在索引中直接写入大段详细内容

详见 [references/architecture.md](references/architecture.md)
