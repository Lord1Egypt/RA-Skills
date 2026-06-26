# SlowMist 安全审查 🛡️

[![Claude Code 技能](https://img.shields.io/badge/Claude%20Code-Skill-blue)](https://claude.com/claude-code)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Security: 安全审查](https://img.shields.io/badge/Security-%E5%AE%89%E5%85%A8%E5%AE%A1%E6%9F%A5-red.svg)](#)

> **核心原则：所有外部输入在验证之前都不可信。**
>
> 🛡️ 这是 [SlowMist Agent Security](https://github.com/slowmist/slowmist-agent-security) 框架的 Claude Code 适配版本。

面向对抗性环境中运行的 Claude Code Agent 的全面安全审查框架。涵盖 6 种审查类型、11 类代码红旗模式、8 类社会工程学模式和 7 类供应链攻击模式。

**其他语言**: [English](README.md) · 中文

---

## 快速决策卡

```
  检测到外部输入 → 选择审查类型 → 按步骤执行 → 输出报告
```

| 场景 | 路由至 | 记住 |
|------|--------|------|
| 安装 Skill/MCP/npm 包 | `skill-mcp.md` | 先列文件清单 |
| GitHub 仓库 | `repository.md` | 先看 commit 历史 |
| URL / 文档 / Gist | `url-document.md` | 逐行扫描代码块 |
| 链上地址 / 合约 | `onchain.md` | 先查 AML 评分 |
| 产品 / 服务 / API | `product-service.md` | 先看私钥管理 |
| 群聊分享的工具 | `message-share.md` | 永远先验证来源 |

**4 级评级**: 🟢 LOW → 🟡 MEDIUM → 🔴 HIGH → ⛔ REJECT
**信任原则**: 信任层级仅调整审查强度，绝不跳过审查步骤。

---

## 激活触发

在以下场景时**自动**激活此框架：

- 用户说"审查"、"检查安全"、"安全评估"、"安全吗"
- 用户说"install"、"帮我检查这个"、"review"、"trust this"
- 安装 Skill、MCP Server、npm/pip/cargo 包之前
- 评估 GitHub 仓库、URL、链上地址、产品之前
- 群聊或社交频道中有人推荐工具时

---

## 6 种审查

### 1. Skill / MCP 安装审查
`references/skill-mcp.md`

文件清单 → 代码审计 → 架构评估 → 评级。
**MCP 专项覆盖**：工具定义、资源访问、提示模板中的注入。

### 2. GitHub 仓库审查
`references/repository.md`

元数据 → 代码审计 → GitHub Actions 安全 → 依赖审查 → Fork 分析。

### 3. URL / 文档审查
`references/url-document.md`

URL 安全 → **18 类提示注入扫描** → 评级。
**关键**：逐行扫描代码块。混合载荷（合法命令 + 恶意命令混合）是最危险的模式。

### 4. 链上地址 / 合约审查
`references/onchain.md`

AML 风险评分 → 智能合约审计 → DApp 前端审查 → 交易前检查清单。
**MistTrack + Dune MCP** 备选方案。

### 5. 产品 / 服务 / API 审查
`references/product-service.md`

提供商评估 → 架构安全 → 权限范围分析 → 信任链评估。

### 6. 群聊分享审查
`references/message-share.md`

来源评估 → 内容路由 → 社会工程学检测 → 响应框架。
**私信"支持"几乎肯定是诈骗。**

---

## 模式库

所有审查类型共享：

| 模式 | 覆盖 |
|------|------|
| [red-flags.md](references/red-flags.md) | 11 类代码级红旗模式 |
| [social-engineering.md](references/social-engineering.md) | 8 类社工与提示注入模式 |
| [supply-chain.md](references/supply-chain.md) | 7 类供应链攻击模式 |

---

## 风险评级系统

| 等级 | 含义 | Agent 行动 |
|------|------|-----------|
| 🟢 LOW | 仅信息、无执行能力、无数据收集、已知可信来源 | 告知用户，如请求则继续 |
| 🟡 MEDIUM | 能力有限、范围明确、存在风险因素 | 完整报告，建议谨慎 |
| 🔴 HIGH | 涉及凭证、资金、系统修改、未知来源或架构缺陷 | 详细报告，**必须获得人类批准** |
| ⛔ REJECT | 匹配红旗模式、确认恶意或不可接受的设计 | 拒绝执行，说明原因 |

---

## 信任层级

| 层级 | 来源类型 | 基础审查强度 |
|------|---------|------------|
| 1 | 官方项目/交易所组织 | 中等——仍需验证 |
| 2 | 已知安全团队（SlowMist、Trail of Bits） | 中等 |
| 3 | 高下载 + 多版本迭代的 Claude Code 技能 | 中高 |
| 4 | 高 star + 活跃维护的 GitHub 仓库 | 高——必须验证代码 |
| 5 | 未知来源、新账户、无记录 | 最高审查 |

---

## Claude Code 适配说明

| 原框架（OpenClaw） | Claude Code |
|---------------------|-----------|
| `~/.openclaw/` | `~/.claude/` |
| ClawHub 安装 | Claude Code Skills |
| `openclaw.json` | `CLAUDE.md` |

---

## 安装

**方式一：Claude Code Skills（推荐）**
```
# 激活即自动注册
/slowmist-security-cc
```

**方式二：克隆到 skills 目录**
```bash
git clone https://github.com/0xcjl/slowmist-security-cc.git ~/.claude/skills/slowmist-security-cc
```

---

## 文件结构

```
slowmist-security-cc/
├── SKILL.md                           # 主入口
├── README.md                          # 英文版
├── README.zh-CN.md                    # 本文件（中文版）
├── _meta.json                         # ClawHub 元数据
├── LICENSE                            # MIT 许可证
└── references/
    ├── skill-mcp.md                   # Skill/MCP 审查
    ├── repository.md                  # GitHub 仓库审查
    ├── url-document.md                # URL/文档审查
    ├── onchain.md                     # 链上地址审查
    ├── product-service.md             # 产品/服务审查
    ├── message-share.md               # 群聊分享审查
    ├── red-flags.md                   # 代码红旗模式
    ├── social-engineering.md          # 社会工程学模式
    └── supply-chain.md                # 供应链攻击模式
```

---

## 致谢

- **原始框架**: [SlowMist / slowmist-agent-security](https://github.com/slowmist/slowmist-agent-security) — 灵感来自 [skill-vetter](https://clawhub.ai/spclaudehome/skill-vetter)
- **攻击模式**: 基于 [OpenClaw Security Practice Guide](https://github.com/slowmist/openclaw-security-practice-guide)
- **提示注入模式**: 基于真实世界 PoC 研究
- **Claude Code 适配**: 0xcjl

---

*安全不是功能——是前提。* 🛡️

**SlowMist** · https://slowmist.com
