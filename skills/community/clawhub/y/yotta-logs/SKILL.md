---
name: yotta-logs
slug: yotta-logs
version: 0.3.5
displayName: 元史·会话日志检索
summary: 跨会话历史日志检索：解析多格式会话与记忆文件，回溯旧对话与上下文，为追溯提供原始依据。
description: '元史 —— 跨智能体的历史会话 / 记忆日志检索技能：零依赖检索 / 分析 JSONL、JSON、SQLite、Markdown 多格式会话与记忆文件，回溯旧对话与父会话上下文，为跨会话追溯提供原始日志依据。触发：用户问起先前聊过的内容 / 父会话 / 历史上下文、要查以前说过的结论、跨会话回溯某次讨论、需要从会话日志或记忆文件定位某段决策时。边界：仅读取本机自己的会话日志 / 记忆文件；不修改、不删除；只查本地不联网上传。'
tags: [日志检索, 历史会话, 上下文回溯, 会话日志, logs, 追溯]
category: knowledge-management
license: MIT
homepage: https://github.com/YottaMeta/yotta-logs
---
# 元史（yotta-logs）

跨智能体的历史会话 / 记忆日志检索技能：**零依赖检索 / 分析多格式日志记录**（JSONL / 单文件 JSON / SQLite / Markdown / 二进制），回溯旧对话与父会话上下文，为跨会话追溯提供原始日志依据。

零依赖（Python 3.8+ 标准库），Windows + Linux + macOS 通用；Claude Code / Cursor / Codex / opencode / 通用 Agent 均可调用。

## 何时使用

- 用户引用先前聊过的内容 / 父会话 / 历史上下文；
- 要查以前说过的结论、决策、命令或结果（无论存在 JSONL 会话、SQLite（如 opencode）还是记忆 md）；
- 需要从会话日志定位某段讨论发生在哪个会话、什么时间、谁说的。

**Do NOT trigger**：

- 只读：不修改、不删除任何会话 / 记忆记录；
- 只查本地日志，不联网上传；
- 语义记忆 / 长期知识请用元忆（yotta-memory）；本技能只管原始日志 / 记忆文件检索，二者互补。

## 快速使用

Windows 用 python，Linux/macOS 用 python3。

```bash
# 全源登记：发现本机所有日志 / 记忆源（来源 / 格式 / 类型 / 默认开关）
python3 scripts/yotta_logs.py locate

# 跨源检索关键词（默认范围 = 会话源 + 结构化记忆源；自由笔记默认关）
python3 scripts/yotta_logs.py search "部署方案"

# 指定目录 / 文件（目录自动嗅探格式族）
python3 scripts/yotta_logs.py scan --dir ~/.clawdbot/agents/<agentId>/sessions
python3 scripts/yotta_logs.py search "CI 失败" --regex --date 2026-08-26 --dir /path/to/logs

# 按来源 / 类型 / 格式过滤
python3 scripts/yotta_logs.py search "记住" --kind memory
python3 scripts/yotta_logs.py search "XSS" --source opencode-db
python3 scripts/yotta_logs.py search "部署" --format sqlite

# 自由笔记显式开（默认关）
python3 scripts/yotta_logs.py search "推送闸门" --kind note

# 提取单个会话原文
python3 scripts/yotta_logs.py session abc123 --dir /path/to/sessions

# 统计（消息 / token / 成本 / 每日汇总 / 分源）
python3 scripts/yotta_logs.py stats --dir /path/to/sessions --daily

# 工具调用排行
python3 scripts/yotta_logs.py tools --dir /path/to/logs --format sqlite
```

退出码（与元安 / 元审 / 元盾 / 元真家族一致）：0 = 成功；1 = 无匹配 / 空结果集；4 = 用法错误 / 致命异常。

## 工作流程（AI 智能体回溯历史时）

1. **定位**：locate 全源登记或 scan 列出会话（跨源，含来源 / 格式）；
2. **检索**：search 按关键词 / 正则跨源命中，先看时间线片段；
3. **提取**：命中后 session <sid> 提取该会话原文；
4. **核对**：需要精确出处时用 --json 拿结构化结果（来源 / 会话 ID / 行号 / 时间戳 / 角色）；
5. **统计**：需要成本 / token / 工具使用回顾时用 stats / tools。

## 能力

- **零依赖检索**：Python 3.8+ 标准库，不依赖 jq / rg 等外部工具；
- **多格式通用**：JSONL / 单文件 JSON / SQLite（opencode 等）/ Markdown（记忆 md + 自由笔记）/ 二进制（只读标题），统一 Record 模型 + 字段别名归一 + 配置兜底；
- **全源登记**：locate / discover 自动发现本机常见日志与记忆源（Codex / Claude Code / Clawdbot / opencode / Gemini / yotta-memory / Codex 笔记…）；
- **默认检索范围**：会话源 + 结构化记忆源默认开，自由笔记默认关可显式开（--kind note / --kind log / 配置 default_scope）；
- **容错解析**：坏行 / 坏字段自动跳过并计数；二进制 / 加密文件只回退标题不崩；
- **默认脱敏**：输出自动打码疑似密钥 / token / 口令（--no-redact 关闭）；
- **多维度过滤**：关键词 / 正则 / 日期 / 会话 ID / 别名 / 角色 / 来源 / 类型 / 格式；
- **结构化输出**：--json 输出纯净 JSON（含来源 / 行号 / 时间戳 / 角色）；
- **只读安全**：只读本地日志与记忆文件，不修改、不删除、不联网。

## 参考文档

- references/agent-formats.md — 6 大格式族普查登记表 + 字段别名映射 + 已知根 + 配置兜底
- references/format.md — 统一 Record 模型与各格式族读取规则
- references/cli.md — CLI 子命令 / 参数 / 退出码 / JSON schema / 配置详解
- references/security.md — 安全边界 / 脱敏规则 / 与元忆的差异化
- references/faq.md — 常见问题与安装排障

## 责任声明

本技能只做本地会话日志 / 记忆文件的只读检索；输出原文片段可能包含隐私，默认脱敏且仅用于本机回溯，请勿将检索结果外传。
