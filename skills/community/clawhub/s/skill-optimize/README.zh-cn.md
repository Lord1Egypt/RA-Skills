# Skill Optimizer (技能优化器)

> [EN](README.md) | 中文

一个聚焦的、有主见的工具，用于根据 [agentskills.io](https://agentskills.io/) 标准**审计和改进现有的 Agent Skill**（`SKILL.md` 文件）。`skill-creator` 覆盖了从零开始的完整工作流（访谈 → 起草 → 评估 → 迭代），而本 skill 是其轻量级、更快速的搭档——当你已经有一个 skill 但想让它变得更好时使用。

## 何时使用

- "按规范审计我的 skill"
- "改进我 skill 的触发准确性"
- "重写 frontmatter 里的 description"
- "这个 skill 太长，帮我精简"
- "发布前 review 一下这个 skill"
- "给我的 skill 加点 gotcha 和示例"
- 任何编辑、打磨或改进现有 `SKILL.md` 的请求

如果用户想要**从零创建一个 skill**，请移交给 `skill-creator`。如果他们想要**用 evals 和 baseline 衡量输出质量**，也请移交给 `skill-creator`。本 skill 优化的是*工件*；`skill-creator` 衡量的是*结果*。

## 三维度审计

优化框架建立在 [agentskills.io](https://agentskills.io/) 的三大支柱上：

1. **Specification 合规** — 文件结构是否合法？frontmatter 是否符合规范？命名和长度规则是否被遵守？
2. **Best Practices 对齐** — 内容是否清晰、范围是否合理、组织是否良好？
3. **Description 优化** — skill 是否会在正确的 prompt 上触发，又在错误的 prompt 上保持沉默？

始终按这个顺序运行三个维度：先规范（二元的，会阻断加载），再最佳实践（内容质量），最后 description（触发准确性）。捆绑的 `scripts/audit_skill.py` 自动处理第一维度；第二、第三维度基于判断，使用捆绑的参考清单。

## 目录结构

```
skill-optimizer/
├── SKILL.md                              # 主入口
├── README.md                             # 英文文档
├── README.zh.md                          # 本文件（中文）
├── references/
│   ├── specification-checklist.md       # 第一维度 —— 规范检查
│   ├── best-practices-checklist.md      # 第二维度 —— 内容质量
│   ├── description-guide.md             # 第三维度 —— description 优化
│   └── common-issues.md                 # 18 个常见问题及修复
├── scripts/
│   └── audit_skill.py                   # 程序化规范 + body 审计
└── assets/
    └── report-template.md               # 报告模板
```

## 快速开始

对任何现有 skill 运行自动审计：

```bash
python3 scripts/audit_skill.py /path/to/target-skill
```

或以 JSON 形式输出（用于管道到其他工具）：

```bash
python3 scripts/audit_skill.py /path/to/target-skill --json
```

退出码：`0`（干净），`1`（有 major），`2`（有 blocker），strict 模式下 minor 和 nit 也会失败。

要进行完整的优化——包括 Best Practices 评审和 Description 重写——从你的 agent 调用 `skill-optimizer` skill。skill 会引导你走完整个工作流：捕获意图 → 定位并快照 → 三维度审计 → 生成报告 → 提出编辑 → 获得批准后应用。

## 参考资料

审计清单和最佳实践综合自以下来源：

- [agentskills.io Specification](https://agentskills.io/specification) — 文件结构、frontmatter、命名、长度规则
- [agentskills.io Best Practices](https://agentskills.io/skill-creation/best-practices) — 范围、指令校准、默认项、过程优于声明、gotcha、输出模板、渐进式披露
- [agentskills.io Optimizing Descriptions](https://agentskills.io/skill-creation/optimizing-descriptions) — 触发、评估查询、训练/测试拆分、优化循环
- [OpenClaw skill-format](https://docs.openclaw.ai/clawhub/skill-format) — 包体积约束、声明与实际行为的一致性、成本/凭证透明度（仅通用部分）
- [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) — 本 skill 所补充的上游从零创建工作流

## 许可证

MIT-0。任何人可以自由使用、修改和再分发，包括商业用途。

---

[English version →](README.md)
