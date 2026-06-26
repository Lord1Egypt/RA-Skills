---
name: session-archiver
description: |
  Session auto-archiver. Automatically archives completed sessions by extracting meaningful user+assistant messages from .reset transcript files and appending to daily memory.
---

# Session Archiver

自动归档对话历史到每日 memory，保留 user + assistant 消息。双保险触发：cron 每小时 + /new 时 spawn。

## 核心要点

1. **双保险触发** — cron 每小时自动运行 + /new 时 spawn subagent，确保不遗漏
2. **去重** — marker + memory 内容双保险，避免重复归档
3. **归档内容** — user + assistant 消息，彻底剥离元数据
4. **自动清理** — 保留最近 30 天日志，超出自动删除
5. **洞察提炼** — 自动提取值得沉淀的洞察候选，供下次会话审查
6. **零感知** — cron 归档静默不通知用户；/new 时 spawn 也不阻塞主窗口
7. **零配置** — 首次运行自动集成到 AGENTS.md，无需手动修改

## 快速集成

**无需手动操作。** 脚本首次运行时自动检测 AGENTS.md 并追加集成内容（搜索 `session-archiver` 关键词判断是否已集成）。

自动写入的内容为 Session Startup 第 5、6 步：
- 第 5 步：spawn 后台 subagent 运行归档脚本
- 第 6 步：主 agent 审查洞察候选文件

## 脚本位置

- 归档脚本：`scripts/session-auto-archive.js`
- 洞察提取：`scripts/extract-insights.js`

## 执行方式

### 机制 1：cron 每小时兜底（主流程）

通过 OpenClaw cron 系统部署，每小时执行一次 isolated subagent 运行归档脚本。delivery=none，静默运行不通知用户。

### 机制 2：/new 时即时触发（补充）

Session Startup 第 5 步 spawn 后台 subagent 运行归档脚本，确保即时性。

> 双保险：两者共享同一个去重 marker（memory/.last_archived_session），不会重复归档。

## 工作流程

1. 扫描 `~/.openclaw/agents/main/sessions/` 找最新 `.reset.*` 文件
2. 去重 A：检查 marker 文件
3. 去重 B：检查 memory 文件是否已有该 sessionId
4. 解析 JSONL，提取 user + assistant 消息
5. 彻底剥离 Conversation info 元数据
6. 短时内容相似去重（hash 前 80 字符）
7. 追加到 `memory/YYYY-MM-DD.md`
8. 更新 marker
9. **自动清理** — 删除 30 天前的 memory 文件
10. **洞察提炼** — 分析归档内容，结果写入 `memory/.insights-candidates-YYYY-MM-DD.md`

## 去重机制

| 检查点 | 文件 | 说明 |
|--------|------|------|
| marker | memory/.last_archived_session | 记录上次处理的 sessionId |
| memory 内容 | memory/YYYY-MM-DD.md | 搜索「来源 session: id」 |

## 洞察候选文件

分析归档内容，识别 6 类值得提炼的信息：

| 类型 | 说明 |
|------|------|
| 🤕 纠正 | 用户纠正了 AI 的行为 |
| 🔄 自我修正 | AI 承认错误或改进 |
| 📌 决策 | 形成了明确结论或建议 |
| 💡 偏好 | 用户表达了明确偏好 |
| ⚙️ 工作流变化 | 任务分工、工具选择发生变化 |
| 📝 教训 | 需要记住避免重蹈的规则 |

输出到 `memory/.insights-candidates-YYYY-MM-DD.md`，主 agent 在下次 Session Startup 时审查，决定是否吸收进 self-improving 文件。

## 注意事项

- 仅沉淀 text 内容，图片/文件不内联存储
- 长期重要内容需人工迁移至 MEMORY.md
- 主窗口永远不直接运行脚本，只 spawn subagent
- cron 归档和 /new spawn 共享 marker，不会重复归档
- 洞察提炼为辅助功能，找不到候选时静默退出
