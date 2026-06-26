# 实体（Entity）规范

## 核心特征

- **唯一标识**：使用值对象包装业务ID（如 `OrderId`），而非裸 `String` / `Long`
- **生命周期**：状态可变，标识不变
- **连续性**：通过标识而非属性判断是否同一对象

## 构造规范

- 构造函数**私有或受保护**
- 通过**工厂方法**创建实例
- 构造时执行**业务规则校验**，保持有效状态

```java
// 标识使用值对象
private OrderId id;

// 私有构造，强制走工厂
private Order() {}

// 工厂方法封装创建逻辑
public static Order create(CustomerId customerId, List<OrderItem> items) {
    Order order = new Order();
    order.id = OrderId.generate();
    order.customerId = customerId;
    order.status = OrderStatus.PENDING;

    if (items == null || items.isEmpty()) {
        throw new DomainException("Order must have at least one item");
    }
    items.forEach(order::addItem);
    order.registerEvent(new OrderCreatedEvent(order.id));
    return order;
}
```

## 富模型方法

业务方法命名使用**业务动词**，封装状态转换，禁止 public setter。

```java
public void pay(Money payment) {
    // 状态校验（不变量保护）
    if (status != OrderStatus.PENDING) {
        throw new DomainException("Only pending order can be paid");
    }
    if (!payment.equals(this.totalAmount)) {
        throw new DomainException("Payment amount must equal total amount");
    }
    this.status = OrderStatus.PAID;
    registerEvent(new OrderPaidEvent(this.id, payment));
}

public void cancel(String reason) {
    if (status == OrderStatus.SHIPPED || status == OrderStatus.DELIVERED) {
        throw new DomainException("Cannot cancel shipped or delivered order");
    }
    this.status = OrderStatus.CANCELLED;
    registerEvent(new OrderCancelledEvent(this.id, reason));
}

// 禁止：public void setStatus(OrderStatus status) { this.status = status; }
```

## 关联引用

- **聚合内实体**：直接持有对象（生命周期同步）
- **外部聚合**：仅存 ID（防内存泄漏，解耦）

```java
private List<OrderItem> items;          // 聚合内，直接持有
private CustomerId customerId;           // 外部聚合，仅存ID
private PaymentId paymentId;             // 外部聚合，仅存ID
```

## 检查清单

- 有唯一标识，使用值对象包装
- 构造函数私有，通过工厂方法创建
- 业务方法使用业务动词
- 状态变更通过方法封装，禁止 public setter
- 校验逻辑在构造和方法中保持有效状态
- 关联对象仅引用聚合根 ID

## 反模式

- Entity 只有 getter/setter（贫血模型）
- 直接持有其他聚合根对象
- 使用数据库自增 ID 而非业务 ID
