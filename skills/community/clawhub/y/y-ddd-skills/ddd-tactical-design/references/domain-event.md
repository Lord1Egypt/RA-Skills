# 领域事件（Domain Event）规范

## 核心概念

领域事件表示领域中已发生的、值得关注的事件，用于解耦聚合间通信。

## 命名规范

事件名使用**过去时态**（表示已发生的事情）：
- `OrderCreatedEvent` 而非 `OrderCreateEvent`
- `PaymentCompletedEvent` 而非 `PaymentCompleteEvent`
- `InventoryReservedEvent` 而非 `InventoryReserveEvent`

## 事件结构

事件包含：事件ID、时间戳、来源聚合ID、必要业务数据。

```java
public class OrderPaidEvent implements DomainEvent {

    private final EventId eventId;
    private final LocalDateTime occurredOn;
    private final OrderId orderId;
    private final Money paymentAmount;
    private final LocalDateTime payTime;

    public OrderPaidEvent(OrderId orderId, Money paymentAmount) {
        this.eventId = EventId.generate();
        this.occurredOn = LocalDateTime.now();
        this.orderId = orderId;
        this.paymentAmount = paymentAmount;
        this.payTime = LocalDateTime.now();
    }

    // getter...
}
```

## 聚合内注册事件

```java
public abstract class AggregateRoot<T extends DomainObjectId> {

    private List<DomainEvent> domainEvents = new ArrayList<>();

    protected void registerEvent(DomainEvent event) {
        this.domainEvents.add(event);
    }

    public List<DomainEvent> getDomainEvents() {
        return Collections.unmodifiableList(domainEvents);
    }

    public void clearEvents() {
        this.domainEvents.clear();
    }
}
```

## 应用层发布

**关键原则**：在事务提交后发布事件，避免事务回滚但事件已发出的情况。

```java
@Service
@RequiredArgsConstructor
public class OrderApplicationService {

    private final OrderRepository orderRepository;
    private final TransactionTemplate transactionTemplate;

    @Transactional
    public void payOrder(PayOrderCommand cmd) {
        Order order = orderRepository.findById(cmd.getOrderId());
        order.pay(cmd.getPayment());
        orderRepository.save(order);

        // 事务提交后发布
        transactionTemplate.executeWithoutResult(status -> {
            eventPublisher.publish(order.getDomainEvents());
            order.clearEvents();
        });
    }
}
```

## 事件处理器

```java
@Component
@RequiredArgsConstructor
public class OrderEventHandler {

    private final NotificationService notificationService;
    private final LogisticsContextClient logisticsClient;
    private final StatsService statsService;

    @EventListener
    public void onOrderPaid(OrderPaidEvent event) {
        // 发送通知
        notificationService.sendPaymentConfirmation(event.getOrderId());

        // 触发物流（跨限界上下文）
        logisticsClient.createShipment(event.getOrderId());
    }

    @EventListener
    public void onOrderPaid_UpdateStats(OrderPaidEvent event) {
        // 更新统计（最终一致性）
        statsService.incrementDailyRevenue(event.getPaymentAmount());
    }
}
```

## 事件总线配置（Spring）

```java
@Configuration
public class DomainEventConfig {

    @Bean
    public ApplicationEventMulticaster applicationEventMulticaster(
            SimpleApplicationEventMulticaster simpleApplicationEventMulticaster) {
        // 异步发布，提升性能
        simpleApplicationEventMulticaster.setTaskExecutor(
            new ThreadPoolTaskExecutor() {{
                setCorePoolSize(4);
                setMaxPoolSize(16);
                setQueueCapacity(1000);
            }}
        );
        return simpleApplicationEventMulticaster;
    }
}
```

## 事件设计原则

1. **只包含必要数据**：事件 ID + 关键属性，不携带完整聚合
2. **不可变**：事件一旦发布不可修改
3. **幂等处理**：消费者应能处理重复事件
4. **最终一致性**：跨聚合的变更通过事件异步同步

## 反模式

- 事件命名用现在时或未来时
- 事件包含完整聚合对象（序列化问题）
- 在聚合内直接发布事件（事务边界问题）
- 事件携带过多数据（耦合）

## 检查清单

- 事件命名使用过去时态
- 包含事件ID、时间戳、来源聚合ID
- 只包含必要数据（ID + 关键属性）
- 在事务提交后发布
- 事件处理器无状态
