---
name: tdd
description: 使用 red-green-refactor loop 做 test-driven development。Use when user wants to build features or fix bugs using TDD, mentions "red-green-refactor", wants integration tests, or asks for test-first development.
---

# Test-Driven Development

## Philosophy

**核心原则**：测试应该通过 public interfaces 验证行为，而不是验证 implementation details。代码可以完全改变；测试不该因此改变。

**好测试**偏 integration-style：它们通过 public APIs 执行真实 code paths。它们描述系统做_什么_，而不是_怎么做_。好测试读起来像 spec，比如 “user can checkout with valid cart” 清楚说明已有能力。这些测试能经受 refactor，因为它们不关心内部结构。

**坏测试**和 implementation 绑定。它们 mock 内部 collaborators、测试 private methods，或通过外部手段验证（例如直接查询 database，而不是使用 interface）。警示信号是：你 refactor 了，行为没变，但测试坏了。如果重命名内部函数导致测试失败，那些测试测的是 implementation，不是 behavior。

示例见 [tests.md](tests.md)，mocking 指南见 [mocking.md](mocking.md)。

## Anti-Pattern: Horizontal Slices

**不要先写所有测试，再写所有实现。** 这是 “horizontal slicing”，把 RED 当成“写所有测试”，把 GREEN 当成“写所有代码”。

这会产生**糟糕测试**：

- 批量写出的测试验证的是_想象中_的行为，不是_实际_行为
- 你最终测的是事物的_shape_（data structures、function signatures），而不是 user-facing behavior
- 测试对真实变化不敏感：行为坏了仍通过，行为没坏却失败
- 你跑得比车灯还远，在理解 implementation 之前就承诺了 test structure

**正确方式**：通过 tracer bullets 做 vertical slices。一个 test → 一个 implementation → 重复。每个 test 都响应上一轮学到的东西。因为代码是你刚写的，你知道什么行为重要，以及该如何验证。

```
WRONG (horizontal):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (vertical):
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
  RED→GREEN: test3→impl3
  ...
```

## Workflow

### 1. Planning

写任何代码之前：

- [ ] 与用户确认需要哪些 interface changes
- [ ] 与用户确认要测试哪些 behaviors（排序优先级）
- [ ] 识别 [deep modules](deep-modules.md) 的机会（小 interface，深 implementation）
- [ ] 为 [testability](interface-design.md) 设计 interfaces
- [ ] 列出要测试的 behaviors（不是 implementation steps）
- [ ] 获得用户对计划的批准

问：“public interface 应该长什么样？哪些 behaviors 最值得测试？”

**你无法测试所有东西。** 与用户确认最重要的 behaviors。把测试精力放在 critical paths 和复杂逻辑上，而不是每一个边缘情况。

### 2. Tracer Bullet

写一个只确认系统一件事的测试：

```
RED:   Write test for first behavior → test fails
GREEN: Write minimal code to pass → test passes
```

这是你的 tracer bullet，证明路径可以 end-to-end 工作。

### 3. Incremental Loop

对每个剩余 behavior：

```
RED:   Write next test → fails
GREEN: Minimal code to pass → passes
```

规则：

- 一次只写一个 test
- 只写足够让当前 test 通过的代码
- 不预判未来 tests
- 让测试专注于 observable behavior

### 4. Refactor

所有 tests 通过后，寻找 [refactor candidates](refactoring.md)：

- [ ] 提取重复
- [ ] Deepen modules（把复杂性移到简单 interfaces 后面）
- [ ] 在自然处应用 SOLID principles
- [ ] 思考新代码暴露了 existing code 的哪些问题
- [ ] 每个 refactor step 后都运行 tests

**RED 状态永远不要 refactor。** 先到 GREEN。

## Checklist Per Cycle

```
[ ] Test describes behavior, not implementation
[ ] Test uses public interface only
[ ] Test would survive internal refactor
[ ] Code is minimal for this test
[ ] No speculative features added
```
