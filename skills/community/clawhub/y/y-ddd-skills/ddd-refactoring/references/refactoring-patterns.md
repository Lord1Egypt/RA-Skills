# 重构模式对比表

## 1. 贫血模型 → 富模型

**贫血模型（重构前）**：

```java
// 实体只有数据，无行为
public class Order {
    private Long id;
    private String status;
    private BigDecimal amount;

    // 只有 getter/setter
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    public BigDecimal getAmount() { return amount; }
    public void setAmount(BigDecimal amount) { this.amount = amount; }
}
```

```java
// 逻辑在 Service 中，散落各处
@Service
public class OrderService {
    public void pay(Long orderId, BigDecimal payment) {
        Order order = orderDao.findById(orderId);
        if (!"PENDING".equals(order.getStatus())) {
            throw new RuntimeException("Invalid status");
        }
        order.setStatus("PAID");
        orderDao.update(order);
    }
}
```

**富模型（重构后）**：

```java
// 实体封装状态和行为
public class Order extends AggregateRoot<OrderId> {
    private OrderId id;
    private OrderStatus status;
    private Money totalAmount;

    private Order() {} // 私有构造

    public static Order create(CustomerId customerId, List<OrderItem> items) {
        // 工厂方法
    }

    public void pay(Money payment) {
        if (status != OrderStatus.PENDING) {
            throw new DomainException("Only pending order can be paid");
        }
        if (!payment.equals(this.totalAmount)) {
            throw new DomainException("Payment amount mismatch");
        }
        this.status = OrderStatus.PAID;
        registerEvent(new OrderPaidEvent(this.id, payment));
    }
}
```

## 2. 跨聚合直接引用 → ID 引用

**错误（重构前）**：

```java
public class Order {
    private Customer customer;      // 直接持有其他聚合根
    private List<Product> products; // 直接持有大量对象
}
```

**正确（重构后）**：

```java
public class Order {
    private CustomerId customerId;  // 仅存 ID
    private List<OrderItem> items; // 聚合内实体含产品快照
}
```

## 3. 领域层依赖基础设施 → 依赖倒置

**错误（重构前）**：

```java
@Entity
public class Order {  // JPA 注解污染领域层
    @Autowired
    private PriceService priceService; // 依赖 Spring

    public void calculate() {
        redisTemplate.get("key"); // 直接访问基础设施
    }
}
```

**正确（重构后）**：

```java
// 领域层：纯 Java，无任何框架依赖
public class Order extends AggregateRoot<OrderId> {
    // 业务方法，不依赖任何框架
    public Money calculateTotal(PricingService pricingService) {
        return pricingService.calculate(this.items);
    }
}

// 领域服务接口（领域层定义）
public interface PricingService {
    Money calculate(List<OrderItem> items);
}

// 基础设施层实现
@Service
public class PricingServiceImpl implements PricingService {
    @Override
    public Money calculate(List<OrderItem> items) {
        // 依赖注入，可访问数据库、缓存等
    }
}
```

## 4. 万能聚合 → 小聚合

**错误（重构前）**：

```java
public class Order {
    private List<OrderItem> items;
    private Payment payment;       // 应为 PaymentId
    private Shipment shipment;     // 应为 ShipmentId
    private Invoice invoice;       // 应为 InvoiceId
    private List<Comment> comments; // 应为独立聚合
    // ... 几十个字段
}
```

**正确（重构后）**：

```java
// Order 聚合：只包含核心业务
public class Order extends AggregateRoot<OrderId> {
    private CustomerId customerId;
    private List<OrderItem> items;
    private OrderStatus status;
    private Money totalAmount;
    // 仅包含订单核心信息
}

// Payment 独立聚合
public class Payment extends AggregateRoot<PaymentId> {
    private OrderId orderId;
    private Money amount;
    private PaymentMethod method;
}

// Shipment 独立聚合
public class Shipment extends AggregateRoot<ShipmentId> {
    private OrderId orderId;
    private TrackingNumber trackingNumber;
    private Address shippingAddress;
}
```

## 5. 绕过应用层 → 正确分层

**错误（重构前）**：

```java
@RestController
public class OrderController {
    @Autowired
    private OrderRepository repo; // Controller 直接调用 Repository

    @PostMapping("/orders")
    public Order create(@RequestBody Order order) {
        return repo.save(order); // 直接暴露领域对象
    }
}
```

**正确（重构后）**：

```java
// Controller 只做协议转换
@RestController
public class OrderController {

    @Autowired
    private OrderApplicationService orderService;

    @PostMapping("/orders")
    public ResponseEntity<OrderResponse> create(@RequestBody CreateOrderRequest request) {
        CreateOrderCommand cmd = toCommand(request);
        OrderId orderId = orderService.createOrder(cmd);
        return ResponseEntity.created(uri(orderId)).build();
    }
}

// ApplicationService 编排用例
@Service
public class OrderApplicationService {

    private final OrderRepository orderRepository;
    private final CustomerRepository customerRepository;
    private final DomainEventPublisher eventPublisher;

    @Transactional
    public OrderId createOrder(CreateOrderCommand cmd) {
        // 用例编排，不含业务判断
        Customer customer = customerRepository.findById(cmd.getCustomerId());
        List<OrderItem> items = buildItems(cmd.getItems());
        Order order = Order.create(customer.getId(), items);
        orderRepository.save(order);
        eventPublisher.publish(order.getDomainEvents());
        return order.getId();
    }
}
```

## 重构优先级建议

| 优先级 | 模式 | 风险 | 收益 |
|--------|------|------|------|
| 1 | 贫血模型 → 富模型 | 低 | 高 |
| 2 | 跨聚合引用 → ID引用 | 低 | 中 |
| 3 | 万能聚合 → 小聚合 | 中 | 高 |
| 4 | 领域依赖基础设施 → DIP | 中 | 中 |
| 5 | 绕过应用层 → 正确分层 | 低 | 高 |
