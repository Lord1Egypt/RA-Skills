---
name: requirement-agent
description: "需求澄清与执行确认。用于日常代码任务（修改、重构、优化、添加注释等）。当用户提出需求时，先通过快速追问（3-5 轮）完善需求，执行前根据规则判断是否需要确认。与 brainstorming（复杂系统设计）互补。"
---

# Requirement Agent

轻量级需求澄清 + 执行前确认控制。

## 与 brainstorming 的区分

| 场景 | Skill |
|------|-------|
| "帮我设计一个微服务架构" | [brainstorming](file:///Users/async/.trae-cn/skills/brainstorming) — 10+ 轮深度追问，强制设计流程，输出 design doc |
| "帮我优化一下这个函数" | **requirement-agent** — 3-5 轮快速澄清，方案确认后执行 |
| "帮我重构用户模块" | **requirement-agent** — 追问澄清范围，执行前确认 |
| "帮我写一个支付系统" | [brainstorming](file:///Users/async/.trae-cn/skills/brainstorming) — 复杂系统，需要完整设计 |

## 触发场景

**使用 requirement-agent 当：**

- 用户说"优化一下"、"重构"、"改进"
- 用户说"加个注释"、"格式化"
- 用户说"帮我改改这个文件"
- 用户说"删掉 XXX"、"重命名 YYY"
- 任何**日常代码任务**，而非全新系统设计

**触发 brainstorming 当：**

- 用户说"帮我设计 XXX"
- 用户说"帮我规划 XXX"
- 用户说"帮我创建一个新系统"
- 需求涉及全新架构、技术选型、多模块协调

## 工作流程

### 1. 需求澄清（Questioning）

当检测到模糊需求时，按 `references/questioning-guide.md` 进行追问：

- 第一轮：结构化快速确认（多选题）
- 第 2-3 轮：针对模糊点深入提问
- 第 4-5 轮：查漏补缺

**跳过条件**：需求已足够明确（包含具体文件、目标、技术栈）

### 2. 执行前确认（Confirmation）

根据 `config/rules.yaml` 判断是否需要确认：

**自动执行（无需确认）：**
- 纯文本修改（注释、格式化）
- 单文件小改动
- 明确安全的操作（如"加注释"、"格式化"）

**需要确认：**
- 多文件修改（2+ 文件）
- 删除操作
- 逻辑变更
- 添加依赖
- 不可逆操作

### 3. 方案展示（可选）

如果需要确认但情况复杂，先展示方案再执行：

```
🤔 在执行之前，我想确认一下：

📝 变更摘要：
- 文件：A.js（第 10-15 行）
- 操作：将 foo() 改为 bar()

✅ 确认执行？
   [继续执行]  [修改方案]  [取消]
```

## 配置文件

规则定义：`config/rules.yaml`
配置说明：`references/config-guide.md`

## 参考文档

- `references/questioning-guide.md` - 追问流程详解
- `references/config-guide.md` - 配置文件说明
