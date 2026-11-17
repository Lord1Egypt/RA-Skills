# Skill Guidelines

编写、审查和优化 Agent Skill 的顶层原则。**11 条原则，分四层**：

| 层 | 原则 |
|----|------|
| 一 · 通用 Cross-Cutting | 1 想清楚再动手 · 2 最小充分 · 3 避免过度内耗 |
| 二 · 结构 Structure | 4 模块化复用（DRY） · 5 渐进式披露 |
| 三 · 流程 Flow Control | 6 交付物锚定 · 7 优雅降级 · 8 推进必过门 |
| 四 · 编写 Craft | 9 张弛有度 · 10 解释为什么 · 11 示例胜于说教 |

元规则：两条原则冲突时，优先保障输出准确性，其次可维护性，最后简洁。

## 使用

将本目录整体放入支持 SKILL.md 规范的 Agent 技能目录即可：

```
Kilo:         ~/.kilo/skills/skill-guidelines/
Claude Code:  ~/.claude/skills/skill-guidelines/
```

创建、审查或优化 skill 时，通过技能名 `skill-guidelines` 触发加载。

## 致谢

本技能受以下项目启发：

- [skill-creator](https://github.com/anthropics/skills) — Anthropic 官方的 skill 创建与迭代方法论
- [karpathy-guidelines](https://x.com/karpathy/status/2015883857489522876) — 源自 Andrej Karpathy 对 LLM 编码常见失误的观察

## License

[MIT](LICENSE)