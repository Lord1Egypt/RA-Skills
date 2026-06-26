# Language

这个 skill 的所有建议都使用这套共享词汇。精确使用这些 terms，不要替换成 “component”、“service”、“API” 或 “boundary”。一致语言就是全部重点。

## Terms

**Module**
任何有 interface 和 implementation 的东西。刻意保持尺度无关，同样适用于 function、class、package 或跨 tier 的 slice。
_Avoid_: unit, component, service.

**Interface**
caller 为正确使用 module 必须知道的一切。包括 type signature，也包括 invariants、ordering constraints、error modes、required configuration 和 performance characteristics。
_Avoid_: API, signature（太窄，只指 type-level surface）。

**Implementation**
module 内部的代码主体。不同于 **Adapter**：一个东西可以是小 adapter 但有大 implementation（Postgres repo），也可以是大 adapter 但小 implementation（in-memory fake）。当 seam 是主题时用 “adapter”，其他时候用 “implementation”。

**Depth**
interface 上的 leverage：caller（或 test）每学习一单位 interface 能触达多少 behaviour。大量 behaviour 位于小 interface 后面时，module 是 **deep**。interface 几乎和 implementation 一样复杂时，module 是 **shallow**。

**Seam** _(from Michael Feathers)_
一个可以不在原地编辑就改变 behaviour 的地方。也就是 module interface 所在的_位置_。seam 放在哪里本身就是 design decision，和它背后放什么不同。
_Avoid_: boundary（与 DDD 的 bounded context 混用过载）。

**Adapter**
在 seam 处满足 interface 的具体东西。描述的是_角色_（填哪个 slot），不是内容（里面有什么）。

**Leverage**
callers 从 depth 获得的东西。每学习一单位 interface，获得更多能力。一个 implementation 回报 N 个 call sites 和 M 个 tests。

**Locality**
maintainers 从 depth 获得的东西。change、bugs、knowledge 和 verification 集中在一个地方，而不是散布到 callers。修一次，到处都修好。

## Principles

- **Depth is a property of the interface, not the implementation.** deep module 内部可以由小的、mockable、swappable parts 组成，只是它们不是 interface 的一部分。module 可以有 **internal seams**（implementation 私有，由自己的 tests 使用），也可以有 interface 上的 **external seam**。
- **The deletion test.** 想象删除 module。如果复杂性消失，module 没隐藏任何东西（只是 pass-through）。如果复杂性在 N 个 callers 中重新出现，module 就在发挥价值。
- **The interface is the test surface.** Callers 和 tests 跨越同一个 seam。如果你想测试 interface _后面_的东西，module 形状可能不对。
- **One adapter means a hypothetical seam. Two adapters means a real one.** 除非确实有东西会跨 seam 变化，否则不要引入 seam。

## Relationships

- 一个 **Module** 恰好有一个 **Interface**（它呈现给 callers 和 tests 的 surface）。
- **Depth** 是 **Module** 的属性，针对其 **Interface** 衡量。
- **Seam** 是 **Module** 的 **Interface** 所在的位置。
- **Adapter** 位于 **Seam**，并满足 **Interface**。
- **Depth** 为 callers 产生 **Leverage**，为 maintainers 产生 **Locality**。

## Rejected framings

- **把 Depth 当作 implementation-lines 与 interface-lines 的比例**（Ousterhout）：这会奖励给 implementation 填水。我们使用 depth-as-leverage。
- **把 “Interface” 当作 TypeScript `interface` keyword 或 class public methods**：太窄。这里的 interface 包含 caller 必须知道的每个事实。
- **“Boundary”**：与 DDD 的 bounded context 混用过载。说 **seam** 或 **interface**。
