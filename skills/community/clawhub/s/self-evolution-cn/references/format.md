# 记录格式说明

## 学习记录格式

```markdown
## [LRN-YYYYMMDD-XXX] 类别

- Agent: <agent_id>
- Logged: 2026-03-26T10:00:00+08:00
- Priority: low|medium|high|critical
- Status: pending|in_progress|resolved|promoted|promoted:all
- Promoted: SOUL.md  # 提升后添加
- Promoted-By: agent1, agent2  # 提升后添加
- Area: frontend|backend|infra|tests|docs|config

### 摘要
一句话描述

### 详情
完整上下文

### 建议行动
具体修复或改进

### 元数据
- Source: conversation|error|user_feedback
- Related Files: path/to/file.ext
- Pattern-Key: simplify.dead_code  # 用于重复模式跟踪
- Recurrence-Count: 1
- First-Seen: 2026-03-26
- Last-Seen: 2026-03-26

---
```

## 错误记录格式

```markdown
## [ERR-YYYYMMDD-XXX] 技能或命令名称

- Agent: <agent_id>
- Logged: 2026-03-26T10:00:00+08:00
- Priority: high
- Status: pending
- Area: frontend|backend|infra|tests|docs|config

### 摘要
简要描述失败内容

### 错误
```
实际错误消息或输出
```

### 上下文
- 尝试的命令/操作
- 使用的输入或参数

### 建议修复
如果可识别，如何解决

### 元数据
- Reproducible: yes|no|unknown
- Related Files: path/to/file.ext

---
```

## 字段说明

| 字段 | 说明 | 示例 |
|------|------|------|
| Agent | 触发记录的 agent 标识 | agent1, agent2 |
| Logged | ISO-8601 时间戳 | 2026-03-26T10:00:00+08:00 |
| Priority | 优先级 | low, medium, high, critical |
| Status | 状态 | pending, in_progress, resolved, promoted, promoted:all |
| Promoted | 提升到的文件 | SOUL.md |
| Promoted-By | 已提升的 agent 列表 | agent1, agent2 |
| Area | 代码库区域 | frontend, backend, infra, tests, docs, config |
| Source | 来源 | conversation, error, user_feedback |
| Pattern-Key | 模式标识 | simplify.dead_code |
| Recurrence-Count | 重复次数 | 1, 2, 3... |
| First-Seen | 首次出现日期 | 2026-03-26 |
| Last-Seen | 最近出现日期 | 2026-03-26 |

## ID 生成

格式：`TYPE-YYYYMMDD-XXX`
- TYPE: `LRN`（学习）、`ERR`（错误）、`FEAT`（功能）
- YYYYMMDD: 当前日期
- XXX: 序号或随机 3 个字符

示例：`LRN-20260326-001`、`ERR-20260326-A3F`

## 状态说明

| 状态 | 说明 |
|------|------|
| `pending` | 待处理 |
| `in_progress` | 正在处理 |
| `resolved` | 已解决 |
| `promoted` | 已提升到 SOUL.md（部分 agent） |
| `promoted:all` | 已提升到 SOUL.md（所有 agent） |

## 解决条目

当问题被修复时，更新条目：

1. 更改 `Status: pending` → `Status: resolved`
2. 添加解决块：

```markdown
### 解决方案
- **Resolved**: 2026-03-27T09:00:00Z
- **Commit/PR**: abc123 或 #42
- **Notes**: 简要描述做了什么
```

## 提升条目

当条目被提升到 SOUL.md 时：

1. 更改 `Status: pending` → `Status: promoted`
2. 添加 `Promoted: SOUL.md`
3. 添加 `Promoted-By: <agent_id>`

**多 agent 场景：**
- 每个 agent 提升后，将自己的 ID 添加到 `Promoted-By`
- 当所有 agent 都提升后，Status 改为 `promoted:all`
