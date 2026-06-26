---
name: unified-self-improving
description: 统一自我进化系统，整合 self-improving-agent、self-improving、mulch 三个技能的优势，提供结构化日志、三层存储、自动升级、模式检测、命名空间隔离和 token 高效的 JSONL 格式支持。
version: 1.0.3
tags: [memory, self-improvement, learning, lifecycle]
trigger: session-end, error, correction, pattern-detected, manual-trigger, heartbeat
---

# 统一自我进化系统 (Unified Self-Improving)

## 概述

本技能整合了以下三个自我进化相关技能的核心功能：

| 技能 | 核心优势 |
|------|----------|
| **self-improving-agent** | Markdown 格式、结构化日志（ID/优先级/状态）、promote 机制、重复模式检测 |
| **self-improving** | 三层存储（HOT/WARM/COLD）、自动升级规则（3次）、命名空间隔离 |
| **mulch** | JSONL 格式、token 效率高（-54%）、prime/query CLI |

整合后的系统提供统一的 CLI 接口，所有命令统一为 `unified-self-improving <command>` 格式。

---

## 架构

### 存储层级

| 层级 | 位置 | 访问频率 | 格式 | 保留时间 |
|------|------|----------|------|----------|
| **HOT** | `memory/hot/` | 实时/每次会话 | Markdown + JSONL 双格式 | 最近 3 次会话 |
| **WARM** | `memory/warm/learnings/` | 频繁查询 | JSONL | 3-10 次会话 |
| **COLD** | `memory/cold/archive/` | 归档参考 | JSONL | 10+ 次会话 |

---

## CLI 命令

```
unified-self-improving <command> [options]
```

| 命令 | 功能 |
|------|------|
| `log` | 记录 correction/error/pattern |
| `query` | 查询学习项 |
| `move` | 移动层级（合并 promote/upgrade） |
| `recall` | 从 COLD 召回 |
| `namespace` | 命名空间管理 |
| `index` | 索引管理（合并 mulch prime） |
| `import` | 批量导入 |
| `session` | 会话 start/end |
| `detect-pattern` | 模式检测 |

---

### 记录学习项

```bash
# 记录用户纠正
unified-self-improving log -t correction -c "用户纠正了我"

# 记录错误
unified-self-improving log -t error -c "命令执行失败" -p high

# 指定命名空间
unified-self-improving log -t pattern -c "检测到重复行为" -n myproject
```

### 查询

```bash
# 查询所有
unified-self-improving query

# 按关键词搜索
unified-self-improving query --pattern "correction"

# 按 ID 查询
unified-self-improving query --id learn-20260315-001

# 按优先级/层级过滤
unified-self-improving query --priority high --level hot
```

### 层级移动

```bash
# 移动到指定层级 (合并 promote/upgrade)
unified-self-improving move --id learn-xxx --to warm
```

### 命名空间

```bash
# 创建命名空间
unified-self-improving namespace create myproject

# 列出命名空间
unified-self-improving namespace list

# 删除命名空间
unified-self-improving namespace delete myproject
```

### 索引

```bash
# 重建索引
unified-self-improving index rebuild
```

### 导入导出

```bash
# 批量导入
unified-self-improving import learnings.jsonl

# 指定目标层级和命名空间
unified-self-improving import -n myproject -l warm data.jsonl
```

### 会话管理

```bash
# 开始会话
unified-self-improving session start

# 结束会话 (自动执行升级和清理)
unified-self-improving session end
```

### 模式检测

```bash
# 检测重复模式
unified-self-improving detect-pattern

# 指定最小出现次数
unified-self-improving detect-pattern -m 3
```

---

## 工作流

### Session Start（会话开始）

1. 加载 `memory/index.jsonl` 建立全局索引
2. 检查 HOT 层是否有未处理的 `corrections` 或 `patterns`
3. 如有需要，从 WARM/COLD 层召回相关历史学习
4. 初始化会话日志文件

```bash
# 加载索引
cat ~/.openclaw/workspace/memory/index.jsonl | jq -s 'from_entries'

# 召回相关学习
unified-self-improving recall --id learn-xxx
```

### Session End（会话结束）

1. 合并会话日志到 HOT 层
2. 执行自动升级检查（HOT → WARM）
3. 更新全局索引
4. 清理过期会话（超过 3 次会话的 HOT 内容）

```bash
# 会话结束处理
unified-self-improving session end
```

---

## 存储结构

```
~/.openclaw/workspace/memory/
├── hot/
│   ├── session-{YYYY-MM-DD}-{HHMMSS}.md
│   ├── session-{YYYY-MM-DD}-{HHMMSS}.jsonl
│   ├── corrections.md
│   ├── errors.md
│   └── patterns.md
├── warm/learnings/{namespace}/
├── cold/archive/{namespace}/
├── namespace/{namespace}/hot|warm|cold/
└── index.jsonl
```

### JSONL 记录格式

```json
{"id": "learn-20260315-001", "namespace": "default", "content": "学习内容", "priority": "high", "status": "active", "access_count": 0, "created_at": "2026-03-15T04:00:00Z", "updated_at": "2026-03-15T04:00:00Z"}
```

---

## 配置

可在 `scripts/lib/config.sh` 中修改：

- `HOT_RETENTION`: HOT 层保留会话数 (默认 3)
- `WARM_RETENTION`: WARM 层保留会话数 (默认 10)
- `AUTO_UPGRADE_THRESHOLD`: 自动升级阈值 (默认 3)
- `DEFAULT_NAMESPACE`: 默认命名空间 (default)

---

## 文件位置

- 技能目录: `~/.openclaw/workspace/skills/unified-self-improving/`
- 存储根目录: `~/.openclaw/workspace/memory/`
- 脚本目录: `~/.openclaw/workspace/scripts/unified-self-improving/`
