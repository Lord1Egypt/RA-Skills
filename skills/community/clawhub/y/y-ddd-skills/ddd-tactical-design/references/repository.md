# 仓储（Repository）规范

## 核心概念

仓储是聚合持久化的抽象，隔离领域模型与数据库实现。

## 核心规则

- **领域层定义接口**，基础设施层实现
- **按聚合根设计**，一个聚合一个仓储
- 接口方法使用**领域对象**，非数据库实体
- 复杂查询用 **Specification 模式**或 **CQRS QueryService**

## 接口定义（领域层）

```java
public interface OrderRepository {
    Order findById(OrderId id);
    List<Order> findByCustomerId(CustomerId customerId, TimeRange range);
    Order save(Order order);
    void delete(OrderId id);

    // 返回ID列表（避免大对象）
    List<OrderId> findPendingOrdersBefore(LocalDateTime deadline);
}
```

## 仓储实现（基础设施层）

```java
@Repository
@RequiredArgsConstructor
public class OrderRepositoryImpl implements OrderRepository {

    private final OrderJpaRepository jpaRepository;
    private final OrderDataConverter converter;

    @Override
    public Order findById(OrderId id) {
        OrderPO po = jpaRepository.findById(id.getValue())
            .orElseThrow(() -> new EntityNotFoundException("Order not found: " + id));
        return converter.toDomain(po);
    }

    @Override
    public Order save(Order order) {
        OrderPO po = converter.toPO(order);
        OrderPO saved = jpaRepository.save(po);
        return converter.toDomain(saved);
    }
}
```

## 数据转换器

分离领域对象与 PO 的转换逻辑：

```java
@Component
public class OrderDataConverter {

    public Order toDomain(OrderPO po) {
        List<OrderItem> items = po.getItems().stream()
            .map(this::toItemDomain)
            .collect(Collectors.toList());

        return Order.reconstitute(
            OrderId.of(po.getId()),
            CustomerId.of(po.getCustomerId()),
            po.getStatus(),
            items,
            Money.of(po.getTotalAmount(), Currency.of(po.getCurrency())),
            po.getCreateTime()
        );
    }

    public OrderPO toPO(Order order) {
        OrderPO po = new OrderPO();
        po.setId(order.getId().getValue());
        po.setCustomerId(order.getCustomerId().getValue());
        po.setStatus(order.getStatus().name());
        po.setTotalAmount(order.getTotalAmount().getAmount());
        po.setCurrency(order.getTotalAmount().getCurrency().name());
        po.setItems(order.getItems().stream()
            .map(this::toItemPO)
            .collect(Collectors.toList()));
        return po;
    }
}
```

## CQRS：读写分离

复杂查询不经过领域模型，直接返回 DTO：

```java
@Service
@RequiredArgsConstructor
public class OrderQueryService {

    private final JdbcTemplate jdbcTemplate;

    public List<OrderSummary> searchOrders(OrderSearchCriteria criteria) {
        String sql = """
            SELECT o.id, o.status, o.total_amount, c.name
            FROM orders o
            JOIN customers c ON o.customer_id = c.id
            WHERE o.status = ? AND o.create_time BETWEEN ? AND ?
            """;

        return jdbcTemplate.query(sql,
            (rs, rowNum) -> new OrderSummary(
                rs.getLong("id"),
                rs.getString("status"),
                rs.getBigDecimal("total_amount"),
                rs.getString("name")
            ),
            criteria.getStatus(),
            criteria.getStartTime(),
            criteria.getEndTime()
        );
    }
}
```

## 常见反模式

- **仓储接口放在基础设施层**：导致领域层依赖基础设施
- **按数据库表设计仓储**：而非按聚合根
- **在 Repository 中写业务逻辑**：违反单一职责
- **聚合根未实现时返回 null**：使用 Optional 或抛异常

## 检查清单

- 仓储接口在领域层定义
- 一个聚合一个仓储
- 只持久化聚合根（内部实体由聚合根管理）
- 复杂查询使用 QueryService / Specification
- 实现了领域对象与 PO 的转换器
