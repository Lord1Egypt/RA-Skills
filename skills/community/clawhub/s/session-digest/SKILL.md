---
name: session-digest
description: "自动总结当天对话到 memory/YYYY-MM-DD.md。cron 23:00 自动运行，提取对话让 agent 自己总结。"
version: "4.1.3"
---

# Session Digest - 每日对话总结

自动总结当天所有 session 对话，生成精简的每日记忆。

## 工作方式

1. cron 23:00 触发
2. 运行 `extract.js` 提取当天对话到临时文件
3. agent 读临时文件，自己总结
4. 写入 `memory/YYYY-MM-DD.md`

## 手动使用

```bash
# 提取对话
node ~/.openclaw/workspace/skills/session-digest/scripts/extract.js [YYYY-MM-DD]

# 然后让 agent 读 /tmp/session-digest-YYYY-MM-DD.txt 并总结
```

## 输出格式

```markdown
# YYYY-MM-DD Weekday

### 做成了什么
- xxx

### 改了什么
- xxx

### 学到了什么
- xxx

### 待办
- [ ] xxx

---
N 个 session，M 条消息
```

## 隐私 & 安全

- **不调外部 API**：extract.js 只读本地文件，不联网
- **读取所有 agents**：main、claude、gemini 等所有存活的 session
- **数据不离开本地**：所有数据都在 `~/.openclaw/` 目录内

## 文件

- `scripts/extract.js` - 提取对话到临时文件
- `SKILL.md` - 本文件
