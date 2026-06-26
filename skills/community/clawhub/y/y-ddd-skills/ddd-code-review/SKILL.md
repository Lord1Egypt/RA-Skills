---
name: ddd-code-review
description: DDD 代码审查清单与反模式诊断。适用场景：对 DDD 代码进行审查、识别常见反模式、验证分层规范符合性、检查战术设计实现质量。当用户提到代码审查、PR审查、DDD规范检查、反模式识别时使用。
---

# DDD 代码审查

## 审查触发时机

- **PR / MR 提交前**：作者自检
- **Code Review**：reviewer 审查
- **合并前**：最终验证
- **定期审计**：周期性规范检查

## 三阶段检查框架

| 阶段 | 时机 | 重点 |
|------|------|------|
| 设计阶段 | 方案评审、架构决策 | 限界上下文划分、聚合设计、依赖方向 |
| 编码阶段 | 编码过程中 | 战术模式实现、分层规范、命名规范 |
| 提交审查 | PR/MR 审查 | 综合检查、反模式识别 |

## 审查原则

**方法名是否反映业务操作？**
- `order.pay(money)` 优于 `order.updateStatus("PAID")`
- 方法名应该是业务动词，不是技术操作

**是否避免了 getter/setter 泛滥？**
- 业务逻辑应该封装在领域对象内
- Service 不应该只是 getXxx + setXxx

**事务边界是否合理？**
- 一个事务修改一个聚合
- 聚合间通过领域事件保持最终一致性

**领域事件是否最终一致性处理？**
- 事件在事务提交后发布
- 消费者无状态，可重复处理

**防腐层是否隔离了外部系统变化？**
- 外部依赖通过 ACL 隔离
- 领域层无外部系统直接引用

## 反模式快速定位

| 反模式 | 代码特征 | 快速定位关键词 |
|--------|---------|--------------|
| 贫血领域模型 | Entity 只有 getter/setter | `class Order { private Long id; public Long getId()...` |
| 跨聚合直接引用 | 聚合持有其他聚合根对象 | `private Customer customer;` 而非 `private CustomerId customerId;` |
| 领域层依赖基础设施 | Entity 含 Spring/JPA 注解 | `@Entity`, `@Autowired` 在 domain 包 |
| 万能聚合 | 聚合包含过多关联对象 | Order 含 Payment, Shipment, Invoice 对象 |
| 绕过应用层 | Controller 直接调用 Repository | `@Autowired OrderRepository repo;` 在 Controller 中 |

## 审查输出格式

```markdown
## DDD 规范审查报告

### 审查范围
- 文件：Order.java, OrderService.java, OrderRepository.java
- 提交：feat/order-domain

### 检查结果

#### 通过项
- [x] 领域层无框架依赖
- [x] 实体使用业务 ID 值对象
- [x] 业务方法使用业务动词

#### 问题项
- [ ] 贫血模型：Order.java 只有 getter/setter，建议将 pay 逻辑从 Service 移入 Order
- [ ] 跨聚合引用：Order 持有 Customer 对象，建议改为 CustomerId
- [ ] 命名问题：setStatus 应改为 cancel/ship 等业务方法

#### 建议
- 优先级 P1：将 OrderService.pay 中的业务规则下沉到 Order.pay()
- 优先级 P2：将 Customer 引用改为 CustomerId
```

## 参考资料

- 三阶段检查清单详表及反模式诊断树：[references/checklist.md](references/checklist.md)
