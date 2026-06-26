# 包结构规范（Package Structure）

## 按聚合组织（Package by Feature）

每个聚合内保持四层结构，整体按业务聚合划分包。

```
com.company.project.
├── interfaces/                      # 用户界面层
│   ├── rest/                        # REST API
│   │   ├── OrderController.java
│   │   └── dto/                     # Request/Response DTO
│   │       ├── CreateOrderRequest.java
│   │       └── OrderResponse.java
│   ├── mq/                          # 消息消费者
│   └── scheduler/                   # 定时任务
│
├── application/                     # 应用层
│   ├── service/                     # 应用服务
│   │   ├── OrderApplicationService.java
│   │   └── OrderQueryService.java
│   ├── command/                     # 命令对象（写操作）
│   │   ├── CreateOrderCommand.java
│   │   └── PayOrderCommand.java
│   ├── query/                       # 查询对象（读操作，CQRS）
│   │   └── OrderSummaryQuery.java
│   ├── dto/                         # 应用层 DTO
│   └── eventhandler/                # 领域事件处理器
│
├── domain/                          # 领域层 ★核心
│   ├── order/                       # 订单聚合
│   │   ├── Order.java               # 聚合根（实体）
│   │   ├── OrderId.java             # 标识值对象
│   │   ├── OrderItem.java           # 聚合内实体
│   │   ├── OrderStatus.java         # 状态值对象（枚举）
│   │   ├── ShippingAddress.java     # 值对象
│   │   ├── Money.java               # 通用值对象
│   │   ├── OrderRepository.java     # 仓储接口
│   │   └── event/                   # 领域事件
│   │       ├── OrderCreatedEvent.java
│   │       └── OrderPaidEvent.java
│   ├── customer/                    # 客户聚合
│   │   ├── Customer.java
│   │   ├── CustomerId.java
│   │   ├── CustomerLevel.java
│   │   └── CustomerRepository.java
│   ├── shared/                     # 共享内核
│   │   ├── DomainException.java
│   │   └── AggregateRoot.java       # 基类
│   └── service/                     # 跨聚合领域服务
│       └── PricingService.java
│
└── infrastructure/                 # 基础设施层
    ├── repository/                  # 仓储实现
    │   ├── OrderRepositoryImpl.java
    │   ├── CustomerRepositoryImpl.java
    │   └── jpa/                     # ORM 映射
    │       ├── OrderJpaRepository.java
    │       └── OrderPO.java
    ├── messaging/                   # 消息实现
    │   └── DomainEventPublisher.java
    ├── external/                    # 外部服务防腐层
    │   ├── payment/
    │   │   ├── PaymentGateway.java              # 接口（领域层定义）
    │   │   └── AlipayGatewayAdapter.java        # 实现
    │   └── logistics/
    │       └── LogisticsClient.java
    └── config/                       # 配置类
        ├── JpaConfig.java
        └── EventConfig.java
```

## 包内文件类型说明

| 包 | 文件类型 | 归属层 |
|----|---------|--------|
| `domain/{aggregate}/` | Entity、VO、Repository接口、DomainEvent | 领域层 |
| `domain/service/` | DomainService（跨聚合） | 领域层 |
| `application/{feature}/` | ApplicationService、Command、Query、DTO | 应用层 |
| `application/eventhandler/` | EventHandler | 应用层 |
| `interfaces/rest/` | Controller、Request/Response DTO | 接口层 |
| `infrastructure/repository/` | RepositoryImpl、PO/Entity、JpaRepository | 基础设施层 |
| `infrastructure/external/` | ACL适配器、外部Client | 基础设施层 |

## 分层文件数量建议

单个聚合的文件数量（参考）：
- 领域层：5-8 个文件（1 个聚合根 + 2-4 个值对象/枚举 + 1 个仓储接口 + 0-1 个领域服务 + 0-2 个事件）
- 应用层：3-5 个文件（1 个应用服务 + 1-2 个 Command/Query + 0-1 个 DTO）
- 基础设施层：3-6 个文件（1 个仓储实现 + 1 个 PO + 1 个 JpaRepository + 0-2 个外部适配器）

## 常见错误

- 按技术层划分（`domain/entity/`、`domain/service/`、`domain/repository/`）而非按聚合划分
- 将 JPA 注解放在领域层实体上（污染领域模型）
- 在领域层直接引用 Spring 注解或 Bean
- 应用服务承担业务逻辑判断
