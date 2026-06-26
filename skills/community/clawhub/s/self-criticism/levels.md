# Critique Depth Levels

Choose the lightest level that can still catch the likely error.

## Light

Use for routine work with small blast radius.

Ask:
- What is the most likely wrong assumption?
- What obvious omission would be annoying to fix later?

Target:
- 10 to 20 seconds
- one or two hard questions

## Standard

Use for multi-step work, user-visible deliverables, or decisions that shape follow-on tasks.

Ask:
- Is the frame correct enough to branch from?
- What dependency, edge case, or user expectation is missing?
- If this is wrong, where will the rework show up first?

Target:
- 30 to 90 seconds
- short rewrite if the frame changes

## Deep

Use only for high-stakes, novel, or failure-prone work.

Ask:
- What would an adversarial reviewer attack first?
- What hidden trade-off is being ignored?
- What simpler or safer frame should replace the current one?

Target:
- a compact stress test, not a full retrospective
- produce a revised frame before execution continues
