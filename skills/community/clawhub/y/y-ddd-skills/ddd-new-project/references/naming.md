# 命名规范参考

## 分层命名

| 层级 | 类名后缀 | 示例 |
|------|---------|------|
| 用户界面 | Controller, Resource, Handler | OrderController, OrderEventHandler |
| 应用服务 | ApplicationService, QueryService | OrderApplicationService, OrderQueryService |
| 领域服务 | Service, Policy, Calculator | PricingService, DiscountPolicy |
| 仓储接口 | Repository | OrderRepository |
| 仓储实现 | RepositoryImpl, Mapper | OrderRepositoryImpl, OrderMapper |
| 领域事件 | Event（过去时） | OrderCreatedEvent, PaymentCompletedEvent |
| 命令对象 | Command | CreateOrderCommand, PayOrderCommand |
| 查询对象 | Query, Criteria | OrderSummaryQuery, OrderSearchCriteria |
| DTO | DTO, VO（视图对象） | OrderDTO, OrderVO |

## 方法命名

### 应用层：业务用例（动词 + 名词）

```java
public OrderId createOrder(CreateOrderCommand cmd);
public void cancelOrder(OrderId id, String reason);
public List<OrderSummary> queryOrderHistory(CustomerId customerId);
public void applyCoupon(OrderId orderId, Coupon coupon);
```

### 领域层：业务行为（业务动词）

```java
order.pay(money);              // 支付
order.confirmShipment();       // 确认发货
order.applyCoupon(coupon);     // 应用优惠券
order.archive();               // 归档
inventory.reserve(productId, qty);  // 预留库存
customer.upgradeLevel();        // 升级等级
```

### 避免的命名模式

| 避免 | 原因 | 改进 |
|------|------|------|
| `order.updateStatus()` | 太泛，无业务含义 | `order.pay()`, `order.cancel()` |
| `order.setPaid()` | 只是状态设置，无过程 | `order.pay(payment)` |
| `order.save()` | 持久化操作，非领域行为 | `orderRepository.save(order)` |
| `service.process()` | 无具体业务含义 | `service.calculateShippingFee()` |
| `dao.getData()` | 技术词汇混入领域 | `repository.findOrder()` |

## 聚合根 ID 命名

```java
// 聚合根Id统一使用值对象包装
public class OrderId extends DomainObjectId { }
public class CustomerId extends DomainObjectId { }
public class ProductId extends DomainObjectId { }
public class PaymentId extends DomainObjectId { }
```

## 领域事件命名

```java
// 过去时态
public class OrderCreatedEvent { }
public class OrderPaidEvent { }
public class OrderCancelledEvent { }
public class PaymentFailedEvent { }
public class InventoryReservedEvent { }

// 避免现在时或未来时
// OrderCreateEvent (错误)
// OrderWillBePaidEvent (错误)
```

## 包命名

```java
// 按聚合组织包结构
com.company.project.domain.order.       // 订单聚合
com.company.project.domain.customer.     // 客户聚合
com.company.project.domain.inventory.    // 库存聚合
com.company.project.domain.shared.      // 共享内核

// 按层组织包结构（不推荐，但可接受）
com.company.project.application.order.   // 订单应用服务
com.company.project.infrastructure.order // 订单仓储实现
```

## 常量枚举命名

```java
// 状态使用枚举
public enum OrderStatus {
    PENDING,      // 待支付
    PAID,         // 已支付
    SHIPPED,      // 已发货
    DELIVERED,    // 已送达
    CANCELLED     // 已取消
}

// 避免：String status = "PENDING"
```

## 异常命名

```java
// 领域异常：业务语义
public class DomainException extends RuntimeException { }
public class OrderDomainException extends DomainException { }

// 应用异常：用例级别
public class OrderNotFoundException extends RuntimeException { }
public class InvalidOrderStateException extends RuntimeException { }
```
