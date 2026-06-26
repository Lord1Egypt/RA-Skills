# 写作示例

以下是一篇符合规范的流程构建笔记示例，供撰写时参考风格和深度。

---

```markdown
---
type: guide
title: OpenClaw 记忆与反思系统
tags: [OpenClaw, Memory, Agent, 自我改进]
---

# OpenClaw 记忆与反思系统

## 这是什么

AI 助理每次会话醒来都是"全新的"，没有原生记忆。OpenClaw 通过文件系统解决这个问题——Agent 读写文件来延续记忆。

但简单的"什么都往一个文件里塞"很快就会失控。本文介绍一套**分层记忆 + 自动晋升**的方案，让 Agent 既有连续性，又能自我改进。

## 最终效果

- Agent 能记住昨天做了什么、上周的项目进展
- 被纠正过的错误不会再犯（经验晋升为行为规则）
- 记忆不会无限膨胀（每日笔记 + 长期文件分层管理）
- 全自动：每天凌晨自动审查和晋升，无需人工干预

## 整体架构

​\`\`\`
交互发生
  ├─→ memory/YYYY-MM-DD.md              情形记忆（发生了什么）
  └─→ .learnings/LEARNINGS.md           反思记忆（学到了什么）
         │
         ↓  每天 3:00 定时任务自动审查
         │
    SOUL.md    行为风格改进
    AGENTS.md  工作流程优化
    TOOLS.md   工具使用坑点
    USER.md    用户偏好
    MEMORY.md  长期事实
​\`\`\`

## 实操步骤

### 第一步：安装 self-improving-agent 技能并初始化

​\`\`\`bash
openclaw skills install self-improving-agent
​\`\`\`

安装后必须手动初始化：

​\`\`\`bash
mkdir ~/.openclaw/workspace/.learnings
touch ~/.openclaw/workspace/.learnings/LEARNINGS.md
touch ~/.openclaw/workspace/.learnings/ERRORS.md
touch ~/.openclaw/workspace/.learnings/FEATURE_REQUESTS.md
​\`\`\`

### 第二步：在 AGENTS.md 中定义记忆规范

​\`\`\`markdown
## 记忆

### 情形记忆 (Episodic Memory)
- **每日笔记**：memory/YYYY-MM-DD.md
- **规则**：只记事实（发生了什么），不记反思（学到了什么）

### 反思记忆 (Reflective Memory)
- **目录**：.learnings/
- **晋升**：每天夜里 3:00 定时任务审查，符合条件的晋升到核心配置文件
​\`\`\`

### 第三步：创建定时审查任务

（完整 prompt 从实际配置中提取...）

## 踩坑记录

### 1. 反思记忆一直没生效

安装了技能但从未创建 `.learnings/` 目录。技能安装 ≠ 启用，必须手动初始化。

### 2. 心跳重复读取浪费 token

最初设计每次审查读过去 7 天的每日笔记。改用 `.review-state.json` 记录进度，每次只读新的一天的笔记。

## 参考资料

- OpenClaw 文档：https://docs.openclaw.ai
```

---

## 示例解析

| 要素 | 示例中的体现 |
|------|-------------|
| 开头直击痛点 | "每次会话醒来都是全新的" — 读者秒懂问题 |
| 最终效果可感知 | 4 条具体能力，不是"提升效率" |
| 架构图一目了然 | ASCII 图展示数据流向 |
| 步骤可复现 | 每步有具体命令，不是概念描述 |
| 踩坑有细节 | 说了问题和解决方案，不是泛泛而谈 |
| 无流水账 | 没有按时间线堆砌，而是按主题组织 |
