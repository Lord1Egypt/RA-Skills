# 配置文件模板

## HEARTBEAT.md 模板

```markdown
# HEARTBEAT.md

## 自动存档+重置任务（Token 超限触发）

当 Token 使用率超过 70% 时，自动保存会话摘要、同步长期记忆并**重置会话**

### 执行检查
- [ ] 运行 `session_status` 检查当前 token 使用量
- [ ] 如果使用量 > 70k/100k：
  1. **执行存档流程**：
     - 读取当前会话历史（最近 50 条消息）
     - **AI 生成摘要**：调用 `scripts/generate-ai-summary.ps1` 提取关键决策、待办事项、主题
     - 生成结构化存档（包含 AI 摘要 + 差异标记）
     - 保存到 `memory/session-backups/session-YYYY-MM-DD-HHMM.md`
     - 记录存档时间和 token 使用量
  2. **同步到长期记忆 (MEMORY.md)**：
     - 提取关键决策 → 添加到 "关键决策记录" 章节
     - 提取待办事项 → 更新 "持续待办" 章节
     - 提取重要信息 → 添加到相应章节
     - 记录 "已自动存档: [文件名]"
  3. **执行自动重置**（无需用户确认）
  4. 新会话开始时读取 MEMORY.md，汇报 "Token 超限已自动存档重置，上次我们在做..."
- [ ] 如果已存档重置，回复 "HEARTBEAT_OK: Token 超限，已自动存档并重置"

### 存档格式模板（支持差异标记）
```markdown
# 会话备份 - YYYY-MM-DD HH:MM

## 统计信息
- Token 使用量: XXk/100k
- 触发原因: [token/idle/manual]
- 主要话题: [摘要]

## 关键决策（差异标记）
- [NEW] **新增决策**: 描述
- [UPD] **更新决策**: 描述（原：xxx）
- [KEEP] **保持决策**: 无变化

## 待办事项（当前状态）
- [ ] 进行中
- [x] 已完成

## 与上次存档的差异摘要
- 新增决策: X 个
- 更新决策: X 个
- 新增待办: X 个
- 完成待办: X 个

## 完整上下文引用
- 上次存档: [文件名]
- 长期记忆: MEMORY.md
- 快速索引: index.json

## 已安装/配置的技能
- [技能列表]

## 下次继续
[需要跟进的事项]
```

### 差异标记说明
- `[NEW]` - 本次新增的关键决策
- `[UPD]` - 修改过的关键决策（附带 previousValue）
- `[KEEP]` - 与上次相同，无变化
- 通过对比上次存档自动生成，减少冗余存储

---

## 原始对话存档（每次会话结束）

将本次会话的原始消息记录保存到 `memory/raw-history/`

### 执行检查（重置前自动执行）
- [ ] 会话即将重置前（Token超限/idle/手动）
- [ ] 读取当前会话完整历史（通过 sessions_history 或内部 API）
- [ ] 生成文件名：`raw-YYYY-MM-DD-HHMM.jsonl`
- [ ] 格式：每行一条 JSON 消息对象
- [ ] 包含：timestamp, role, content, message_id

### 文件格式示例
```jsonl
{"timestamp":"2026-03-05T10:17:00+08:00","role":"user","content":"测试一下","message_id":"om_xxx"}
{"timestamp":"2026-03-05T10:17:05+08:00","role":"assistant","content":"收到！测试成功","message_id":"..."}
```

---

## 会话重置前自动存档（idle 触发）

配置已设置为 `idleMinutes: 120`（闲置2小时后自动重置）

每次收到 HEARTBEAT 时：
- [ ] 检查上次用户消息时间
- [ ] 如果即将达到 120 分钟 idle（比如已过 110 分钟）：
  1. **执行存档**：
     - 当前 Token 使用量
     - 本次会话的待办事项
     - 下次继续的关键任务
     - 保存到 `memory/session-backups/idle-reset-YYYY-MM-DD-HHMM.md`
  2. **同步到长期记忆 (MEMORY.md)**：更新待办事项和关键信息
  3. 回复 "HEARTBEAT_OK: 预重置存档完成，会话即将重置"

---

## 手动重置指令存档

当用户发送 "重置" 指令时：
- [ ] **先执行存档**：
  1. 当前 Token 使用量
  2. 本次会话的主要话题和关键决策
  3. 待办事项和未完成的任务
  4. 保存到 `memory/session-backups/manual-reset-YYYY-MM-DD-HHMM.md`
- [ ] **同步到长期记忆 (MEMORY.md)**：更新关键决策和待办事项
- [ ] 在 `memory/reset-log.md` 中记录手动重置事件
- [ ] 回复用户："已存档、同步长期记忆并重置完成 ✅"

---

## 存档状态追踪

在 `memory/reset-log.md` 中记录每次重置：
```markdown
- [2026-03-04 17:25] 自动重置前存档: idle-reset-2026-03-04-1725.md
- [2026-03-04 17:30] Token超限存档: session-2026-03-04-1730.md
```

---

## 索引同步任务（每次更新 MEMORY.md 后）

当 MEMORY.md 更新时，同步更新 `memory/index.json`：

### 执行检查
- [ ] 检查是否有新的关键决策或配置变更
- [ ] 提取：topic, value, date, tags, description
- [ ] 更新 index.json：
  - 新增条目（如果是新配置）
  - 更新条目（如果是修改，保留 previousValue）
  - 更新 lastUpdated 时间戳
- [ ] 更新 tags 索引

### 索引格式
```json
{
  "id": "config-backup-interval",
  "topic": "备份间隔",
  "value": "12小时",
  "previousValue": "1小时",
  "date": "2026-03-05",
  "tags": ["config", "backup"],
  "source": "MEMORY.md#2026-03-05",
  "description": "..."
}
```

### 查询使用
快速查找配置：`index.json` → 按 topic 或 tag 搜索 → 返回 value 和 source

---

## 自动备份任务（每次 HEARTBEAT 检查）

检查是否需要执行自动备份到 GitHub 和 OneDrive

### 执行检查
- [ ] 检查 `memory/backup-status.json`
- [ ] **优先级1**：如果 `pendingChanges == true`：
  - 立即执行备份（忽略12小时间隔）
  - 备份成功后设置 `pendingChanges = false, pendingReason = null`
  - 回复 "HEARTBEAT_OK: 重要变更已立即备份"
- [ ] **优先级2**：如果上次备份超过 **12 小时**：
  - 执行备份脚本：
    ```powershell
    & "C:\Users\will\.openclaw\workspace\scripts\backup.ps1"
    ```
  - 回复 "HEARTBEAT_OK: 自动备份完成"
- [ ] 如果备份失败，回复 "HEARTBEAT: 备份失败，请检查"

### 触发 pendingChanges 的场景
以下变更自动标记 `pendingChanges = true`：
- MEMORY.md 更新（关键决策、配置变更）
- openclaw.json 修改
- 新技能安装/配置
- 用户明确指令："立即备份"

### 备份内容
- `config/`: SOUL.md, USER.md, IDENTITY.md, AGENTS.md, TOOLS.md, HEARTBEAT.md
- `memory/`: 所有历史记录文件
- `backup-status.json`: 备份状态追踪

### 备份目标
1. **GitHub**: https://github.com/[username]/openclaw-backup
2. **OneDrive**: `C:\Users\[username]\OneDrive\openclaw-backup`
```

---

## MEMORY.md 模板

```markdown
# MEMORY.md - 长期记忆

_精选需要跨会话保持的关键信息_

---

## 用户档案

- **姓名**: [用户姓名]
- **称呼**: [如何称呼]
- **时区**: [时区]
- **对话风格偏好**: [风格偏好]

## 重要背景

### 当前探索方向
- [方向1]
- [方向2]

### 已安装技能
| Skill | 用途 | 状态 |
|-------|------|------|
| [skill-name] | [用途] | [状态] |

## 关键决策记录

### YYYY-MM-DD
- **[决策标题]**: [决策内容]

## 持续待办

### 高优先级
- [ ] [任务1]

### 中优先级
- [ ] [任务2]

### 低优先级
- [ ] [任务3]

## 重要文件位置

| 文件 | 用途 |
|------|------|
| `memory/session-backups/*.md` | 结构化会话存档 |
| `memory/raw-history/*.jsonl` | 原始对话记录 |
| `memory/reset-log.md` | 重置历史追踪 |
| `memory/backup-status.json` | 备份状态 |
| `memory/index.json` | **快速索引** |

## 自动存档配置

- **Token 超限阈值**: [X]k/100k
- **闲置重置时间**: [X] 分钟
- **备份目标**: [GitHub/OneDrive/双备份]
- **原始对话**: 每次会话结束自动存档

---

_最后更新: YYYY-MM-DD_
```

---

## index.json 模板

```json
{
  "version": "1.0",
  "lastUpdated": "YYYY-MM-DDTHH:MM:SS+08:00",
  "entries": [
    {
      "id": "config-token-threshold",
      "topic": "Token 超限阈值",
      "value": "70k/100k",
      "date": "YYYY-MM-DD",
      "tags": ["config", "token", "reset"],
      "source": "MEMORY.md",
      "description": "Token超过70k时自动存档并重置会话"
    }
  ],
  "tags": {
    "config": ["Token 超限阈值"],
    "token": ["Token 超限阈值"],
    "reset": ["Token 超限阈值"]
  }
}
```

---

## backup-status.json 模板

```json
{
  "pendingChanges": false,
  "pendingReason": null,
  "durationSeconds": 0,
  "lastBackup": "YYYY-MM-DDTHH:MM:SSZ",
  "totalFiles": 0,
  "github": {
    "uploaded": 0,
    "repo": "[username]/openclaw-backup",
    "failed": 0
  },
  "nextBackup": "YYYY-MM-DDTHH:MM:SSZ",
  "onedrive": {
    "path": "C:\\Users\\[username]\\OneDrive\\openclaw-backup",
    "failed": 0,
    "copied": 0
  }
}
```

---

## reset-log.md 模板

```markdown
# 会话重置日志

追踪每次自动重置和存档记录

## 重置记录

| 时间 | 类型 | 存档文件 | Token 使用量 | 备注 |
|------|------|----------|-------------|------|
| YYYY-MM-DD HH:MM | [token/idle/manual] | [文件名] | XXk/100k | [备注] |

## 配置信息

- **idleMinutes**: [X]
- **自动重置前存档**: [启用/禁用]
- **Token 超限存档+重置阈值**: [X]k
- **备份间隔**: [X]小时
- **存档目录**: `memory/session-backups/`
- **原始对话目录**: `memory/raw-history/`
- **长期记忆**: `MEMORY.md`

## 待办事项追踪（跨会话保持）

### 进行中
- [ ] [任务]

### 已完成
- [x] [任务]

## 下次会话开始

每次新会话开始时，我会：
1. 读取 `memory/reset-log.md` 了解上次状态
2. 读取最新的存档文件，了解待办事项
3. 主动汇报："上次我们在做 XXX，继续吗？"
```
