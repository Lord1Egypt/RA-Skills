---
title: Combine Filter and Map Into One Pass
impact: LOW
impactDescription: one iteration instead of two or three
tags: perf, iteration, comprehensions
---

## Combine Filter and Map Into One Pass

When you filter a collection and then map (or map and filter, etc.), it's often one comprehension, not two or three chained operations. Each chained step allocates an intermediate list and iterates.

**Incorrect (three passes, two intermediate lists):**

```python
def prices_for_sale_items(items: list[Item]) -> list[Decimal]:
    sale_items = [i for i in items if i.on_sale]
    discounted = [i for i in sale_items if i.discount > 0]
    prices = [i.price * (1 - i.discount) for i in discounted]
    return prices
```

Three allocations, three passes.

**Correct (one pass, one list):**

```python
def prices_for_sale_items(items: list[Item]) -> list[Decimal]:
    return [
        item.price * (1 - item.discount)
        for item in items
        if item.on_sale and item.discount > 0
    ]
```

One pass, one list. Conditions combined; mapping in the expression.

**When chaining is clearer:**

If each step has enough logic that inlining makes the comprehension hard to read, keep them separate — readability wins over a small constant-factor performance gain:

```python
# fine — each step has real logic
eligible = [normalize(u) for u in users if u.tenure_months >= 12]
grouped = group_by_team(eligible)
summaries = [compute_summary(team, members) for team, members in grouped.items()]
```

**For reductions, use the built-in that takes a generator:**

```python
# don't build a list just to sum it
total = sum([i.price for i in items if i.on_sale])

# better — generator, no intermediate list
total = sum(i.price for i in items if i.on_sale)
```

Same for `min`, `max`, `any`, `all`, `''.join(...)`.

For multi-step transforms, `itertools` provides streaming building blocks (`chain`, `islice`, `groupby`). Most of the time, one comprehension is enough.
