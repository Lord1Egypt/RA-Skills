---
name: ddd-tactical-design
description: DDD 领域驱动设计战术模式详解。适用场景：实现实体、值对象、聚合、仓储、领域服务、领域事件等战术模式时，参考具体编码规范和代码示例。当用户提到 DDD 编码、实体设计、值对象、聚合规范、仓储模式、领域事件时使用。
---

# DDD 战术设计模式

战术设计是将战略建模（限界上下文、通用语言）落地为具体代码的过程。

## 六大战术模式

| 模式 | 作用 | 边界 |
|------|------|------|
| 实体（Entity） | 有唯一标识的生命周期对象 | 聚合内或聚合根 |
| 值对象（Value Object） | 无标识、由属性定义的不可变对象 | 可共享 |
| 聚合（Aggregate） | 一致性边界，内部强一致，外部最终一致 | 事务边界 |
| 领域服务（Domain Service） | 跨实体的业务行为 | 无状态 |
| 仓储（Repository） | 聚合的持久化抽象 | 仅聚合根 |
| 领域事件（Domain Event） | 已发生的业务事件 | 解耦 |

## 模式选择指引

**这个业务概念有唯一标识吗？**
- 是 → **实体**
- 否 → 值对象

**这个逻辑属于哪个实体？**
- 单一实体 → 放入实体方法
- 跨多个实体 → **领域服务**
- 需要访问外部资源 → **领域服务**（或考虑防腐层）

**谁负责这个聚合的持久化？**
- 仅聚合根 → **仓储**
- 复杂查询 → CQRS QueryService

## 参考资料

- 实体规范：[references/entity.md](references/entity.md)
- 值对象规范：[references/value-object.md](references/value-object.md)
- 聚合规范：[references/aggregate.md](references/aggregate.md)
- 仓储规范：[references/repository.md](references/repository.md)
- 领域事件规范：[references/domain-event.md](references/domain-event.md)
