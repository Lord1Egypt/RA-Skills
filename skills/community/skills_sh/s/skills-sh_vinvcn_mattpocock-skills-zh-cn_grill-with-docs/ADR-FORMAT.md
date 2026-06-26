# ADR Format

ADRs 放在 `docs/adr/` 中，并使用连续编号：`0001-slug.md`、`0002-slug.md`，以此类推。

懒创建 `docs/adr/` 目录：只有在第一个 ADR 确实需要时才创建。

## Template

```md
# {Short title of the decision}

{1-3 sentences: what's the context, what did we decide, and why.}
```

就这些。一个 ADR 可以只有一段。价值在于记录*做出了*某个决策以及*为什么*做，而不是填满各个 section。

## Optional sections

只在它们带来真实价值时包含。大多数 ADR 不需要这些。

- **Status** frontmatter (`proposed | accepted | deprecated | superseded by ADR-NNNN`) — 决策被重新审视时有用
- **Considered Options** — 只有被拒绝的替代方案值得记住时才写
- **Consequences** — 只有需要说明非显而易见的下游影响时才写

## Numbering

扫描 `docs/adr/`，找到现有最大编号并加一。

## When to offer an ADR

以下三点必须全部为真：

1. **Hard to reverse** — 之后改主意的成本有意义
2. **Surprising without context** — 未来读者看到代码会想“为什么会这样做？”
3. **The result of a real trade-off** — 确实存在可选方案，并且你基于具体原因选择了其中一个

如果决策很容易撤销，就跳过；你之后直接撤销即可。如果它并不出人意料，没人会追问为什么。如果没有真实替代方案，除了“我们做了显而易见的事”之外就没什么可记录。

### What qualifies

- **Architectural shape.** “我们使用 monorepo。”“write model 是 event-sourced，read model 投影到 Postgres。”
- **Integration patterns between contexts.** “Ordering 和 Billing 通过 domain events 通信，而不是 synchronous HTTP。”
- **Technology choices that carry lock-in.** 数据库、message bus、auth provider、deployment target。不是每个 library；只记录那些替换起来会花一个季度的选择。
- **Boundary and scope decisions.** “Customer data 由 Customer context 拥有；其他 contexts 只通过 ID 引用它。”明确的 no 和 yes 一样有价值。
- **Deliberate deviations from the obvious path.** “我们不用 ORM 而用 manual SQL，因为 X。”任何合理读者会默认相反做法的地方都值得记录。这能阻止下一位工程师把刻意选择“修掉”。
- **Constraints not visible in the code.** “由于合规要求，我们不能使用 AWS。”“由于 partner API contract，响应时间必须低于 200ms。”
- **Rejected alternatives when the rejection is non-obvious.** 如果你考虑过 GraphQL，但因为细微原因选择 REST，就记录下来；否则六个月后还会有人再次建议 GraphQL。
