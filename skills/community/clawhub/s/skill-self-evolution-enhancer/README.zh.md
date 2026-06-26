# Skill Self-Evolution Enhancer

为任意 Cursor Skill 赋予自进化能力的增强技能。基于 self-improving-agent，让原本不具备自进化的技能获得：日志记录、从用户反馈学习、经验提升为规则、以及 Review→Apply→Report 循环——全部按目标技能的领域定制。

[English](README.md)

## 功能

- **领域分析**：深度分析目标技能的能力、场景与进化方向
- **生成 .learnings/**：领域化的 LEARNINGS.md、ERRORS.md、FEATURE_REQUESTS.md
- **生成 EVOLUTION.md**：触发条件、Review-Apply-Report 流程、OpenClaw 反馈规则
- **多技能扩展**：支持为多个技能分别配置各自的进化逻辑

## 使用场景

- 用户说：「给 skill X 加上自进化能力」
- 需要将自改进能力扩展到多个技能（每个技能有独立进化方向）
- 目标技能为非编程类（如洗稿能手、电脑加速），需要领域特定的触发条件

## 快速开始

1. 在 Cursor 中启用本技能
2. 提供目标技能的路径（如 `skills/xxx`、`~/.cursor/skills/xxx`）
3. 按提示完成：读取目标技能 → 领域分析 → 生成 .learnings/ 与 EVOLUTION.md

## 目录结构

```
skill-self-evolution-enhancer/
├── SKILL.md              # 技能主文档
├── assets/               # 模板
│   ├── DOMAIN-CONFIG-TEMPLATE.md
│   ├── EVOLUTION-RULES-TEMPLATE.md
│   ├── LEARNINGS-TEMPLATE.md
│   ├── ERRORS-TEMPLATE.md
│   └── FEATURE_REQUESTS-TEMPLATE.md
├── references/           # 参考示例
│   ├── domain-examples.md
│   └── openclaw-feedback.md
└── scripts/
    └── generate-evolution.sh   # 可选脚手架生成脚本
```

## 参考

- [SKILL.md](SKILL.md) — 完整工作流与说明
- [references/domain-examples.md](references/domain-examples.md) — 洗稿能手、电脑加速等示例

## 来源

- 基于：self-improving-agent 3.0.1
- 用途：让任意技能获得与 self-improving-agent 类似的自进化能力
