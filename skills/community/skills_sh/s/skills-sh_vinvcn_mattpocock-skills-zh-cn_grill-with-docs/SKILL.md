---
name: grill-with-docs
description: Grilling session that challenges your plan against the existing domain model, sharpens terminology, and updates documentation (CONTEXT.md, ADRs) inline as decisions crystallise. Use when user wants to stress-test a plan against their project's language and documented decisions.
---

<what-to-do>

围绕这个计划的每个方面持续追问我，直到我们达成共同理解。沿着 design tree 的每个分支往下走，逐一解决决策之间的依赖。对每个问题，都提供你推荐的答案。

一次只问一个问题，并等待我对每个问题的反馈后再继续。

如果某个问题可以通过探索 codebase 来回答，就去探索 codebase，而不是问我。

</what-to-do>

<supporting-info>

## Domain awareness

探索 codebase 时，也查找现有文档：

### File structure

大多数 repos 只有一个 context：

```
/
├── CONTEXT.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

如果根目录存在 `CONTEXT-MAP.md`，说明 repo 有多个 contexts。这个 map 指向每个 context 的位置：

```
/
├── CONTEXT-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── CONTEXT.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── CONTEXT.md
│       └── docs/adr/
```

懒创建文件：只有在有内容可写时才创建。如果没有 `CONTEXT.md`，在第一个 term 被解决时创建。如果没有 `docs/adr/`，在第一个 ADR 需要时创建。

## During the session

### Challenge against the glossary

当用户使用的 term 与 `CONTEXT.md` 中的现有语言冲突时，立即指出。“Your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?”

### Sharpen fuzzy language

当用户使用含糊或 overloaded terms 时，提出一个精确的 canonical term。“You're saying 'account' — do you mean the Customer or the User? Those are different things.”

### Discuss concrete scenarios

讨论 domain relationships 时，用具体场景做 stress-test。发明能探测 edge cases 的场景，迫使用户精确说明概念之间的边界。

### Cross-reference with code

当用户说明某件事如何工作时，检查代码是否一致。如果发现矛盾，指出来：“Your code cancels entire Orders, but you just said partial cancellation is possible — which is right?”

### Update CONTEXT.md inline

当一个 term 被解决时，立即更新 `CONTEXT.md`。不要攒到最后；随着发生就捕获。使用 [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md) 中的格式。

`CONTEXT.md` 应完全不包含实现细节。不要把 `CONTEXT.md` 当作 spec、scratch pad 或实现决策仓库。它只是 glossary，除此之外不承担别的职责。

### Offer ADRs sparingly

只有以下三点全部为真时，才提议创建 ADR：

1. **Hard to reverse** — 之后改主意的成本有意义
2. **Surprising without context** — 未来读者会疑惑“为什么这样做？”
3. **The result of a real trade-off** — 确实有真实替代方案，并且你基于具体原因选择了一个

如果三者缺一，就跳过 ADR。使用 [ADR-FORMAT.md](./ADR-FORMAT.md) 中的格式。

</supporting-info>
