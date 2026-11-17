# 测试驱动开发（TDD / Red-Green-Refactor）

> 用 TDD 节奏开发一个功能：先写失败的测试（红），再写最少实现让其通过（绿），最后重构（重构）。保证每一步都有测试护航。

## 何时使用

- 用户说「用 TDD 写这个功能」「测试驱动开发 X」「先写测试再实现」
- 开发一个边界清晰、可独立验证的函数/模块

## 工作流

```
┌─────────┐   ┌─────────┐   ┌─────────┐
│  RED    │ → │  GREEN  │ → │ REFACTOR│ → 回到 RED
│ 写失败测 │   │ 最小实现 │   │ 优化结构 │
└─────────┘   └─────────┘   └─────────┘
```

1. **RED**：写一个描述期望行为的测试，运行确认它**失败**（编译/断言错都算）。
2. **GREEN**：写**刚好够**让测试通过的实现，不做额外设计。
3. **REFACTOR**：在不改测试的前提下优化代码结构（改名、抽函数、去重）。
4. 循环直到功能完整；每轮保持测试全绿。

## 节奏要点

- 测试粒度小：一次只推进一步，避免一次性写一大坨再实现。
- 红→绿之间**不要重构**，重构时**不要加功能**。
- 用 `parametrize`/表驱动把等价类一次铺开，但实现仍逐步通过。
- 卡住时先写一个更小、更简单的用例回到红绿循环。

## 与覆盖率关系

- TDD 天然高覆盖，但覆盖率仍要抽查边界/异常（见 [references/unit-testing.md](unit-testing.md)）。
- 不要为了「绿」而写假断言（`assert True` 之类）。

## 示例（Python）

```python
# RED
def test_discount(): assert price_after_discount(100, 0.1) == 90

# GREEN
def price_after_discount(p, d): return p * (1 - d)

# REFACTOR（加校验，测试仍绿）
def price_after_discount(p, d):
    if not 0 <= d <= 1: raise ValueError("折扣需在 0~1")
    return round(p * (1 - d), 2)
```

## 相关子技能（L3）

- 落地为 TDD 动作（Red-Green-Refactor，覆盖率驱动）→ [skills/unit-test-writer/SKILL.md](../skills/unit-test-writer/SKILL.md)（§与覆盖率关系）

## 限制

- TDD 不适合探索性/UI 强耦合/需求极不稳定的任务；此类先用原型再补测试。
- 重构需测试稳定覆盖，否则易引入回归。
