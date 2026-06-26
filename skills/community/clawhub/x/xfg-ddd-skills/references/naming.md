# Naming Conventions Reference

## Package Naming

| Layer | Package Pattern | Example |
|-------|----------------|---------|
| Trigger | `cn.{company}.trigger.http` | `cn.bugstack.trigger.http` |
| Trigger | `cn.{company}.trigger.mq` | `cn.bugstack.trigger.mq` |
| Trigger | `cn.{company}.trigger.job` | `cn.bugstack.trigger.job` |
| API | `cn.{company}.api` | `cn.bugstack.api` |
| Case | `cn.{company}.cases.{domain}` | `cn.bugstack.cases.trade` |
| Domain | `cn.{company}.domain.{domain}` | `cn.bugstack.domain.trade` |
| Infrastructure | `cn.{company}.infrastructure.adapter` | `cn.bugstack.infrastructure.adapter` |

## Class Naming

| Type | Pattern | Example |
|------|---------|---------|
| Entity | `{Domain}Entity` | `OrderEntity` |
| Aggregate | `{Domain}Aggregate` | `OrderAggregate` |
| Value Object | `{Domain}VO` | `MoneyVO` |
| Enum | `{Domain}Enum` | `OrderStatusEnum` |
| Repository Interface | `I{Domain}Repository` | `IOrderRepository` |
| Repository Impl | `{Domain}Repository` | `OrderRepository` |
| Port Interface | `I{Domain}Port` | `INotificationPort` |
| Port Impl | `{Domain}Port` | `NotificationPort` |
| Domain Service Interface | `I{Domain}Service` | `IOrderService` |
| Domain Service Impl | `{Domain}ServiceImpl` | `OrderServiceImpl` |
| Case Interface | `I{Domain}Case` | `IOrderCase` |
| Case Impl | `{Domain}CaseImpl` | `OrderCaseImpl` |
| Controller | `{Domain}Controller` | `OrderController` |
| MQ Listener | `{Domain}Listener` | `OrderListener` |
| Job | `{Domain}Job` | `OrderJob` |
| DAO | `I{Domain}Dao` | `IOrderDao` |
| PO | `{Domain}PO` | `OrderPO` |
| API Request DTO | `{Xxx}RequestDTO` | `CreateOrderRequestDTO` |
| API Response DTO | `{Xxx}ResponseDTO` | `OrderResponseDTO` |

## Method Naming

| Operation | Pattern | Example |
|-----------|---------|---------|
| Find single | `findById`, `getByXxx` | `findById`, `getByOrderId` |
| Find list | `findXxx`, `listXxx` | `findPending`, `listByUser` |
| Find page | `findPage`, `queryPage` | `findPage` |
| Create | `create`, `save` | `createOrder` |
| Update | `update`, `modify` | `updateStatus` |
| Delete | `delete`, `remove` | `deleteById` |
| Validate | `validate`, `check` | `validateOrder` |
| Query state | `canXxx`, `isXxx`, `hasXxx` | `canPay`, `isPaid` |
| Convert | `toXxx` | `toVO`, `toEntity` |

## Variable Naming

| Type | Pattern | Example |
|------|---------|---------|
| Entity | `{domain}Entity` | `orderEntity` |
| Aggregate | `{domain}Aggregate` | `orderAggregate` |
| Value Object | `{domain}VO` | `moneyVO` |
| DTO | `request`, `response` | `createRequest` |
| PO | `{domain}PO` | `orderPO` |
| Service | `{domain}Service` | `orderService` |

## Database Naming

| Type | Pattern | Example |
|------|---------|---------|
| Table | `{domain}_{entity}` | `trade_order`, `user_account` |
| Column | `snake_case` | `order_id`, `create_time` |
| Index | `idx_{table}_{column}` | `idx_trade_order_user_id` |
| Primary Key | `pk_{table}` | `pk_trade_order` |

## Example

```java
// Entity
public class OrderEntity { }

// Aggregate
public class OrderAggregate { }

// Value Object
public class MoneyVO { }

// Repository Interface
public interface IOrderRepository { }

// Repository Implementation
public class OrderRepository implements IOrderRepository { }

// Domain Service
public interface IOrderService { }
public class OrderServiceImpl implements IOrderService { }

// Port
public interface INotificationPort { }
public class NotificationPort implements INotificationPort { }

// Case
public interface IOrderCase { }
public class OrderCaseImpl implements IOrderCase { }

// Controller
public class OrderController { }

// MQ Listener
public class OrderListener { }

// Job
public class OrderJob { }

// API DTO（必须以 DTO 结尾）
public class CreateOrderRequestDTO { }
public class OrderResponseDTO { }
```

## DTO 命名规范

**API 层（api 模块）的 DTO 必须以 `DTO` 结尾：**

```java
// ✅ 正确
public class CreateOrderRequestDTO { }
public class OrderResponseDTO { }
public class QueryOrderRequestDTO { }

// ❌ 错误
public class CreateOrderRequest { }   // 缺少 DTO 后缀
public class OrderResponse { }        // 缺少 DTO 后缀
public class OrderVO { }              // VO 是领域层值对象，不是 API DTO
```

**各层对象命名对比：**

| 层 | 对象类型 | 命名规范 | 示例 |
|----|---------|---------|------|
| API 层 | 请求对象 | `{Xxx}RequestDTO` | `CreateOrderRequestDTO` |
| API 层 | 响应对象 | `{Xxx}ResponseDTO` | `OrderResponseDTO` |
| Domain 层 | 值对象 | `{Xxx}VO` | `OrderStatusVO` |
| Domain 层 | 实体 | `{Xxx}Entity` | `OrderEntity` |
| Domain 层 | 命令实体 | `{Xxx}CommandEntity` | `CreateOrderCommandEntity` |
| Infrastructure 层 | 持久化对象 | `{Xxx}PO` | `OrderPO` |
| Infrastructure 层 | Gateway DTO | `{Xxx}RequestDTO` / `{Xxx}ResponseDTO` | `PayRequestDTO` |