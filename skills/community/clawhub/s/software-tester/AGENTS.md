# AGENTS.md

## 仓库性质

`software-tester` 是一个 **单一、完整的 AI Agent 测试技能**，采用 Superpowers 架构（薄 SKILL.md + 按需加载的 references + 确定性 scripts + assets 模板）。

它不再是多技能集合目录，而是一个可被 WorkBuddy / Claude Code 直接装载的技能包。

## 目录约定

```
software-tester/
├── SKILL.md          # 入口：frontmatter(name/description/agent_created) + 路由与原则
├── README.md         # 人类可读的介绍与快速开始
├── AGENTS.md         # 本文件
├── references/       # 完整 playbook，按需由 SKILL.md 路由加载
│   └── <topic>.md
├── scripts/          # 确定性、可重复执行的脚本（纯 stdlib）
│   └── *.py
└── assets/           # 输出用模板与配置（不进上下文）
    └── *
```

## SKILL.md 格式

```markdown
---
name: software-tester
description: <第三人称触发描述，决定何时被调用>
agent_created: true
metadata:
  version: <语义化版本>
  category: 软件测试
  difficulty: 专家
---

# Software Tester
> <一句话简介>
## 何时使用
## 能力索引（路由到 references/）
## 内置脚本
## 模板资源
## 核心原则
```

## 工作约定

- 所有内容用中文编写。
- SKILL.md 保持「薄」：只做路由与原则，详细流程放 `references/`。
- `references/` 中每个文件是**自包含 playbook**：能力、何时用、工作流、示例、限制。
- `scripts/` 只放确定性、可重复的任务脚本，优先用脚本而非每次重写代码。
- `assets/` 放配置/模板，不依赖上下文加载。
- 新增测试域：在 `references/` 加 `<topic>.md`，并在 SKILL.md 路由表与 README 同步登记。

## 不做什么

- 不创建测试管理平台类技能（那是 SaaS 产品的事）。
- 不替代 QA 团队的测试策略拍板（只提供方法论与门禁）。
- 不维护与具体 SaaS 强绑定的私有工具链（保持框架中立）。
