# 🛡️ summarize — Error Immune System for AI Coding Agents

> **永不重复犯错** — AI 编程助手的错误免疫系统。
> **Never repeat the same mistake** — Error immune system for AI coding agents.

[![Version](https://img.shields.io/badge/version-6.6.3-blue)](VERSION)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-ZCode%20%7C%20CodeBuddy%20%7C%20Claude%20Code%20%7C%20Codex%20%7C%20Reasonix-lightgrey)]()

---

## 🧠 What Makes This Different / 独特价值

**Not just another "summarize" tool.** This is a complete **error immune system** for AI coding agents:

| What others do | What THIS does |
|---------------|----------------|
| 📝 Summarize conversation | 🛡️ **Harvest errors** → classify → store in 3-tier memory |
| ❌ Forget after session | 🧬 **Self-evolve** — generates prevention rules, tracks adoption |
| 🔁 Repeat same mistakes | ⚡ **Convergence alerts** — warns when error types spike |
| 📄 Flat log file | 🔥🔶🔵 **3-tier auto-tiering** — hot/warm/cold with Git versioning |

**Trigger**: `总结` or `summarize` (standalone word only, unchanged)

### Why "Immune System"?

> Biological immune system: detects pathogen → classifies → remembers → responds faster next time.
>
> **This skill**: detects agent error → 5-dimension classification → 3-tier storage → multi-signal retrieval → auto-evolves prevention rules.

## Overview / 概述

**EN**: An error immune system for AI coding agents (ZCode / CodeBuddy / Claude Code / Codex / Reasonix). Automatically harvests errors → 5-dimension classification → multi-signal retrieval → self-evolving prevention rules → adoption tracking → convergence alerts. Also condenses long sessions into structured progress reports with primary/sub-task breakdown, progress bars, and actionable next steps. Triggered ONLY by standalone `summarize` (not in a sentence, no auto-reminder).

**CN**: AI 编程助手的错误免疫系统。自动收割每次错误 → 5维分类 → 多信号检索 → 生成预防规则 → 追踪遵守 → 收敛预警。同时精炼长对话为结构化进度报告，含主/次任务分层、进度条、可执行下一步建议。**仅**独立词`总结`触发（句中不触发）。

### Core Capabilities / 核心能力

| Feature | 功能 |
|---------|------|
| 🗜️ **Session Condense** | 会话精炼 — 主/次任务分层 + ASCII进度条 + 文件清单 + 关键决策 |
| 📋 **Task Progress** | 任务进度 — 完成/待办/下一步 + 压力等级 |
| ⚡ **Error Self-Evolve** | 错误自进化 — 5维分类 + 规则回测 + 全局/项目分流 |
| ⚡ **Success Harvest** | 成功经验收割 — 工具效用对比 + 最佳执行路径 + 6类标签 |
| 📝 **Layered Write** | 分层写入 — 6级决策树 + 待确认队列 + 跨平台路径适配 |
| 📊 **Skill Analytics** | 技能调用统计 — 调用次数 + token 估算 + 效果评估 |

**设计原则**: 一句话能表达清楚绝不用两句。`总结`完整输出≤25行（自动折叠超限内容到归档），`总结 统计`≤6行。

---

## Installation / 安装

### 一键安装（全平台通用，自动检测目标平台）

```bash
curl -sL https://raw.githubusercontent.com/gtbwpkwjnb-alt/summarize-skill/master/scripts/install.sh | bash
```

Windows PowerShell:

```powershell
iwr https://raw.githubusercontent.com/gtbwpkwjnb-alt/summarize-skill/master/scripts/install.ps1 | iex
```

安装脚本会自动检测当前平台（ZCode / CodeBuddy / Claude Code / Codex / Reasonix）并安装到对应目录。如果检测不到，会回退到 `~/.agent-skills/summarize`。

### 手动安装

```bash
# ZCode
git clone git@github.com:gtbwpkwjnb-alt/summarize-skill.git ~/.agents/skills/summarize

# CodeBuddy
git clone git@github.com:gtbwpkwjnb-alt/summarize-skill.git ~/.codebuddy/skills/summarize

# Claude Code
git clone git@github.com:gtbwpkwjnb-alt/summarize-skill.git ~/.claude/skills/summarize

# Codex
git clone git@github.com:gtbwpkwjnb-alt/summarize-skill.git ~/.codex/skills/summarize

# Reasonix
git clone git@github.com:gtbwpkwjnb-alt/summarize-skill.git ~/.reasonix/skills/summarize
```

### 更新

```bash
cd ~/.agent-skills/summarize && git pull
```

安装后输入`总结`或`summarize`即可触发。

---

## File Structure / 文件结构

```
summarize/
├── SKILL.md                    # 技能主文件 / Main skill definition
├── VERSION                     # 版本号 / Version
├── README.md                   # 本文件 / This file
├── LICENSE                     # MIT
├── scripts/
│   ├── install.ps1             # Windows 安装脚本
│   └── install.sh              # Linux/macOS 安装脚本
├── references/
│   ├── CHANGELOG.md            # 完整变更日志
│   ├── trigger-examples.md     # 触发规则与输出示例
│   ├── installation.md         # 安装方式与平台前置条件
│   └── ...
└── harvests/                   # 运行时数据 / Runtime data
    ├── index.md                # 收割索引
    ├── error-ledger.md         # 全局错误账本
    ├── _self-stats.md          # 自反馈统计
    └── {project}/
        ├── errors.md           # 项目错误账本
        └── {session-id}.md     # 会话归档（覆盖更新）
```

---

## Platform Requirements / 平台前置条件

| 能力 | 是否必需 | 说明 |
|------|---------|------|
| 自定义技能/命令注入 | ✅ 必需 | 用于注入触发方式 |
| 文件系统读写 | ✅ 必需 | 存储收割数据和规则文件 |
| 会话历史访问 | ✅ 必需 | 模块1/2/3/4都需要读取当前会话 |
| 上下文使用率数据 | 🟡 可选 | 模块4 token统计；无数据时自动降级为字符估算 |

如果平台不支持某些能力，对应模块会自动降级。

---

## 反馈 / Feedback

🐛 [GitHub Issues](https://github.com/gtbwpkwjnb-alt/summarize-skill/issues/new)

---

## License

MIT — see [LICENSE](LICENSE) file.
