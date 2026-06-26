---
name: session-recover
version: 1.0.0
description: 短期记忆恢复技能。用于快速回顾当前 session 或上一个 session 的完整内容。适用于：想知道"这次 session 聊了什么"、session 被意外重置后需要恢复上下文、或想提取对话精华。
---

# Session Recover — 短期记忆恢复

## 何时使用

- 想知道"这次 session 聊了什么"
- session 被意外重置，想恢复丢失的上下文
- 想把当前 session 的要点整理成摘要
- 任何人想知道任意一个 session 的完整对话记录

## 核心思想

通过 `sessions_list` + JSONL 文件解析，还原 session 的完整对话内容。无需任何 hook 或预置机制。

## 触发指令

发送 `/recover`

## 执行步骤

### Step 1：确定目标 session

**场景 A — 恢复当前 session（从文件恢复）**

当前 session 的历史不完整，但 JSONL 存档文件通常还在：

```bash
# 找到当前 session 对应的存档文件
AGENT_DIR="$HOME/.openclaw/agents/{当前agent名}/sessions"
ls -lt "$AGENT_DIR" | grep "$(session_status | grep 'sessionId' | awk '{print $2}')"
```

**场景 B — 恢复被重置的上一个 session**

上一个 session 被重置后会变成 `.reset.*` 存档文件：

```bash
# 列出最近的 reset 存档
ls -lt "$HOME/.openclaw/agents/main/sessions/"*.reset.* | head -5
```

**场景 C — 查找特定 channel 的 session**

```javascript
sessions_list({
  kinds: ["group"],    // group | main | private
  limit: 10,
  messageLimit: 0      // 不需要摘要，只要 session key
})
```

从返回找到目标 channel 的 session key 和 sessionId。

### Step 2：解析 JSONL 文件

```bash
# 解析最近 N 条消息
python3 skills/session-recover/references/parse_session.py \
  /path/to/session.jsonl \
  --tail 20

# 关键词搜索（用于找特定内容）
python3 skills/session-recover/references/parse_session.py \
  /path/to/session.jsonl \
  --keyword "待完成" \
  --context 3
```

JSONL 文件结构（跳过头部 metadata 行，只处理 `type=message` 的行）：
- 消息内容在 `message.content[].text`
- thinking 内容在 `message.content[].thinking`
- 每条消息有 `timestamp`

### Step 3：综合摘要

从解析结果中提取：
1. **摘要** — 本次 session 的主题（一句话）
2. **要点** — 关键结论、决策、技术细节
3. **未完成** — 任何未解决的事项或后续步骤
4. **下一步** — 最近一条 user message 或明确的 next step

## 输出格式

```markdown
## Session 回忆报告
**来源**：{session key 或文件路径}
**时间**：YYYY-MM-DD HH:mm

### 一句话摘要
[本次 session 核心主题]

### 对话要点
- [要点1]
- [要点2]
- [要点3]

### 未完成事项
- [ ] [事项1]
- [ ] [事项2]

### 关键上下文
[技术细节、配置值、代码片段等]

---
原始素材：{文件路径或 session key}
```

## 常用命令速查

| 需求 | 命令 |
|------|------|
| 最近 10 条 | `parse_session.py {file} --tail 10` |
| 搜关键词+3行上下文 | `parse_session.py {file} --keyword "关键词" --context 3` |
| 找所有 reset 存档 | `ls -lt agents/main/sessions/*.reset.* \| head -10` |

## 参考文件

- `references/parse_session.py` — JSONL 解析器，支持 `--tail N`、`--keyword`、`--context`
