# CONTEXT.md Format

## Structure

```md
# {Context Name}

{One or two sentence description of what this context is and why it exists.}

## Language

**Order**:
{A one or two sentence description of the term}
_Avoid_: Purchase, transaction

**Invoice**:
A request for payment sent to a customer after delivery.
_Avoid_: Bill, payment request

**Customer**:
A person or organization that places orders.
_Avoid_: Client, buyer, account
```

## Rules

- **Be opinionated.** 当多个词表示同一概念时，选择最合适的那个，并把其他词列在 `_Avoid_` 下。
- **Keep definitions tight.** 最多一两句话。定义它是什么，而不是它做什么。
- **Only include terms specific to this project's context.** 通用编程概念（timeouts、error types、utility patterns）不属于这里，即使项目大量使用。添加 term 前先问：这是当前 context 独有的概念，还是通用编程概念？只有前者属于这里。
- **Group terms under subheadings** when natural clusters emerge. 如果所有 terms 属于单个内聚区域，扁平列表就可以。

## Single vs multi-context repos

**Single context（大多数 repos）：** repo 根目录一个 `CONTEXT.md`。

**Multiple contexts：** repo 根目录一个 `CONTEXT-MAP.md`，列出 contexts、它们的位置以及彼此关系：

```md
# Context Map

## Contexts

- [Ordering](./src/ordering/CONTEXT.md) — receives and tracks customer orders
- [Billing](./src/billing/CONTEXT.md) — generates invoices and processes payments
- [Fulfillment](./src/fulfillment/CONTEXT.md) — manages warehouse picking and shipping

## Relationships

- **Ordering → Fulfillment**: Ordering emits `OrderPlaced` events; Fulfillment consumes them to start picking
- **Fulfillment → Billing**: Fulfillment emits `ShipmentDispatched` events; Billing consumes them to generate invoices
- **Ordering ↔ Billing**: Shared types for `CustomerId` and `Money`
```

Skill 会推断使用哪种结构：

- 如果 `CONTEXT-MAP.md` 存在，读取它来找到 contexts
- 如果只有根目录 `CONTEXT.md`，就是 single context
- 如果两者都不存在，等第一个 term 被解决时再懒创建根目录 `CONTEXT.md`

当存在多个 contexts 时，推断当前话题关联哪一个。如果不清楚，就询问。
