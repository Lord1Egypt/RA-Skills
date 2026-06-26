# ClawHub 提交指南

> ultra-memory v3.0.0 — 超长会话记忆 Skill for OpenClaw / Claude Code / 所有 LLM 平台

---

## 快速安装

```bash
npx clawhub@latest install ultra-memory
```

安装完成后 OpenClaw 会自动识别 `SKILL.md`，无需额外配置。

---

## 发布到 npm（ClawHub 自动索引）

### 前提条件

- Node.js 18+
- npm account（免费）：https://www.npmjs.com/signup

### 发布步骤

```bash
# 1. 进入项目目录
cd ultra-memory

# 2. 登录 npm
npm login
# 输入用户名、密码、邮箱

# 3. 发布（首次发布用 latest，后续用 patch/minor/major）
npm publish

# 4. 验证发布成功
npm view ultra-memory

# 5. ClawHub 大约 5-10 分钟后自动索引
npx clawhub@latest install ultra-memory
```

### 发布后验证

```bash
# 检查版本
npm view ultra-memory version

# 检查文件是否完整
npm pack ultra-memory
tar -tzf ultra-memory-*.tgz | head -20
```

---

## 提交信息

### ClawHub 标题

```
ultra-memory — 超长会话记忆系统
```

### 简短描述（≤ 120 字符）

```
5层记忆架构 · 零外部依赖 · 自动提取函数/决策/错误 · 跨语言检索 · 支持所有LLM平台
```

### 完整描述

```
ultra-memory 给 AI Agent 提供不遗忘、可检索、跨会话持久化的记忆能力。

核心功能：
• 5层记忆架构：操作日志 → 摘要 → 语义 → 实体索引 → 向量语义
• 零外部依赖：纯 Python stdlib，可选 sentence-transformers 增强
• 结构化实体：自动提取函数、文件、依赖、决策、错误、类
• 分层压缩：O(log n) 上下文增长，永不爆 context window
• 跨语言检索：中英文同义词双向映射（"数据清洗" ↔ "clean_df"）
• 全平台支持：MCP Server / REST API / Claude Code Skill / OpenClaw

适用场景：长编码任务、写长篇小说、跨天继续工作、精确回忆操作细节
开发者：NanJingYa
许可：MIT
```

### 关键词（npm keywords）

```
ai memory long-context claude openclaw mcp llm session-memory
semantic-search ultra-memory agent-memory context-window
mem0-alternative openai gemini qwen
```

---

## ClawHub 平台信息

| 字段 | 内容 |
|------|------|
| **名称** | ultra-memory |
| **版本** | 3.0.0 |
| **格式** | AgentSkill Bundle（SKILL.md + scripts/） |
| **安装命令** | `npx clawhub@latest install ultra-memory` |
| **npm 包** | https://www.npmjs.com/package/ultra-memory |
| **源码** | https://github.com/nanjingya/ultra-memory |
| **开发者** | NanJingYa |
| **许可** | MIT |

---

## 触发词（中英文双语）

**必须触发的场景：**
- "记住" / "别忘了" / "上次我们做了什么" / "回忆"
- "don't forget" / "remember this" / "what did we do" / "recall"
- "继续昨天的任务" / "接着上次做" / "跨会话"
- 操作数超过 30 条，context 使用率逼近阈值

**不触发场景：**
- 单次简短问答（"帮我写个正则"）
- 纯代码补全、文件格式转换等无状态任务
- 用户明确说"不用记录"

---

## 技术规格

| 项目 | 值 |
|------|------|
| Python 版本 | ≥ 3.8 |
| Node.js 版本 | ≥ 18（仅 MCP Server 模式需要） |
| 依赖 | **零硬性依赖**（纯 stdlib） |
| 可选依赖 | sklearn（TF-IDF 增强）、sentence-transformers（向量语义） |
| 存储格式 | JSONL + Markdown + JSON |
| 默认存储 | `~/.ultra-memory/` |
| MCP 工具数 | 9 个 |
| 记忆层数 | 5 层 |

---

## ClawHub 平台要求确认清单

- [x] `package.json` 存在，包含 name/version/description/author
- [x] `SKILL.md` 存在，包含 YAML frontmatter (name + description)
- [x] 触发词已在 SKILL.md frontmatter 的 description 中声明
- [x] README.md 存在，说明安装和使用方式
- [x] npm publish 后 ClawHub 自动索引（无需额外提交到 ClawHub 平台）
- [x] 开发者信息：NanJingYa（无其他贡献者）
- [x] MIT License 文件存在或 package.json 中声明

---

## 维护指南

### 发布新版本

```bash
# 1. 更新版本号
#    patch: bug修复 → npm version patch
#    minor: 新功能   → npm version minor
#    major: 破坏性变更 → npm version major
npm version patch

# 2. 发布
npm publish

# 3. ClawHub 自动更新（通常 5-10 分钟）
npx clawhub@latest install ultra-memory
```

### 版本号规范

遵循 [Semantic Versioning](https://semver.org/)：
- **3.0.0** — 初始正式版（MCP + REST + 5层架构 + TF-IDF）
- 未来：3.1.0（bug修复）、4.0.0（破坏性变更）

---

## 联系开发者

- GitHub Issues: https://github.com/nanjingya/ultra-memory/issues
- 源码：https://github.com/nanjingya/ultra-memory
- 开发者：NanJingYa

---

*本文件供 ClawHub 提交参考，npm 发布后 ClawHub 会自动索引，无需额外操作。*
