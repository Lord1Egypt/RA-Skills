# 聚合（Aggregate）规范

## 核心概念

聚合是一组相关对象的集合，作为数据修改的原子单元。

## 设计原则

1. **边界内强一致性**：聚合内的对象在同一事务中保持一致
2. **边界外最终一致性**：聚合间通过领域事件异步同步
3. **聚合根唯一对外引用入口**：外部只能持有聚合根
4. **小聚合优先**：大聚合影响并发性能和事务范围
5. **一事务一聚合**：除非特殊情况，一个事务只修改一个聚合

## 聚合根职责

聚合根是聚合的唯一入口点：
- 维护聚合内对象的不变量
- 控制对内部对象的访问
- 注册领域事件

```java
public class Order extends AggregateRoot<OrderId> {

    private OrderId id;
    private List<OrderItem> items;         // 聚合内实体，直接引用
    private ShippingAddress shippingAddress;
    private CustomerId customerId;          // 外部聚合，仅存ID
    private PaymentId paymentId;            // 外部聚合，仅存ID
    private OrderStatus status;

    // 批量操作保持业务一致性
    public void confirmShipment(TrackingNumber trackingNumber) {
        if (status != OrderStatus.PAID) {
            throw new DomainException("Only paid order can be shipped");
        }
        this.status = OrderStatus.SHIPPED;
        this.trackingNumber = trackingNumber;
        this.shipTime = LocalDateTime.now();

        // 同时更新所有项状态（聚合内一致性）
        this.items.forEach(OrderItem::markAsShipped);

        registerEvent(new OrderShippedEvent(this.id, trackingNumber));
    }

    public void changeShippingAddress(ShippingAddress newAddress) {
        if (status != OrderStatus.PENDING) {
            throw new DomainException("Cannot change address for non-pending order");
        }
        this.shippingAddress = newAddress;
        registerEvent(new ShippingAddressChangedEvent(this.id, newAddress));
    }
}
```

## 聚合内实体

聚合内实体与聚合根生命周期同步，无全局唯一标识，只有局部标识。

```java
public class OrderItem {
    private Long localId;            // 数据库主键，业务无意义
    private ProductId productId;      // 关联其他聚合，存ID
    private String productName;      // 冗余快照（防关联变化）
    private Money price;             // 下单时价格快照
    private int quantity;
    private ItemStatus status;

    void markAsShipped() {
        this.status = ItemStatus.SHIPPED;
    }

    Money getSubTotal() {
        return price.multiply(quantity);
    }
}
```

## 聚合间引用

- **聚合间禁止直接对象引用**，使用 ID
- 聚合内可包含关联对象的价格快照（防止历史数据漂移）

```java
// 错误：直接持有其他聚合根对象
public class Order {
    private Customer customer;     // 错误
    private List<Product> products; // 错误
}

// 正确：通过ID引用
public class Order {
    private CustomerId customerId;
    private List<OrderItem> items; // OrderItem 内含 productId 快照
}
```

## 聚合大小选择

**小聚合原则**：优先设计小聚合，允许跨聚合事件交互。

| 聚合规模 | 优点 | 缺点 |
|---------|------|------|
| 小聚合（1-3个实体） | 加载快、并发好、事务小 | 跨聚合协调多 |
| 大聚合（10+实体） | 事务内一致性高 | 加载慢、并发冲突 |

**经验法则**：如果一个聚合超过 5 个实体，考虑拆分。

## 检查清单

- 聚合根是唯一对外引用入口
- 聚合内对象通过 ID 引用外部聚合
- 聚合内直接持有生命周期同步的对象
- 状态转换通过方法封装
- 业务不变量在聚合根中强制保证
- 一个事务只修改一个聚合

## 反模式

- 万能聚合（包含过多关联对象）
- 聚合间直接对象引用
- 聚合根承担过多职责
