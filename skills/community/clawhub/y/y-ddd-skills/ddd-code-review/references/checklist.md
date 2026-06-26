# 三阶段检查清单及反模式诊断树

## 设计阶段检查清单

- [ ] **限界上下文划分合理**：上下文边界清晰，无重叠的通用语言
- [ ] **聚合职责明确**：每个聚合有单一的、高内聚的职责
- [ ] **核心域 / 支撑域 / 通用域已识别**：资源分配有优先级
- [ ] **上下文映射图已绘制**：集成关系、信任边界清晰
- [ ] **通用语言词汇表已建立**：术语定义一致，无歧义

## 编码阶段检查清单

- [ ] **领域层代码不依赖 Spring/JPA 等框架**：纯 Java/Kotlin，可独立测试
- [ ] **实体使用业务 ID（值对象）**：非数据库自增 ID
- [ ] **所有业务规则在领域层校验**：构造方法、领域方法中执行
- [ ] **应用服务无 if/switch 业务判断**：仅编排，不含业务逻辑
- [ ] **跨聚合调用通过 ID + 仓储，或领域事件**：无直接对象引用
- [ ] **复杂查询使用 CQRS**：不污染领域模型

## 代码审查检查清单

- [ ] **方法名反映业务操作**：使用业务动词，非 CRUD 词汇
- [ ] **避免了 getter/setter 泛滥**：富模型，业务逻辑在领域对象内
- [ ] **事务边界合理**：一个事务一个聚合
- [ ] **领域事件最终一致性处理**：事务提交后发布，消费者幂等
- [ ] **防腐层隔离外部系统**：ACL 保护领域模型不受污染

---

## 反模式诊断树

### 反模式 1：贫血领域模型

**诊断特征**：
```
Entity 中：
- 只有 getter/setter（或 Lombok @Data）
- 无业务方法
- 构造函数是 public 的，无工厂方法

Service 中：
- 大量 if/switch 判断状态
- 直接操作 entity.getXxx() 和 setXxx()
- 单个 Service 方法超过 50 行
```

**修复方向**：
1. 将 Service 中的业务规则下沉到对应的 Entity
2. 为 Entity 添加业务方法（使用业务动词命名）
3. 将 public 构造函数改为 private，添加工厂方法
4. 在 Entity 中维护不变量，构造时校验

---

### 反模式 2：跨聚合直接引用

**诊断特征**：
```
public class Order {
    private Customer customer;           // 错误：直接持有其他聚合根
    private List<Product> products;     // 错误：直接持有大量对象
}

public class OrderItem {
    private Product product;            // 错误：持有完整 Product 对象
}
```

**修复方向**：
1. 将对象引用改为 ID 值对象：`private CustomerId customerId;`
2. 聚合内实体可持有快照数据：`private String productName; private Money price;`
3. 如需完整数据，通过 ID 查询：`Customer customer = customerRepo.findById(customerId);`

---

### 反模式 3：领域层依赖基础设施

**诊断特征**：
```
domain 包内出现：
- @Entity, @Table, @Column 等 JPA 注解
- @Autowired, @Service, @Repository 等 Spring 注解
- 数据库访问代码（JDBC, JdbcTemplate）
- Redis/MQ 客户端调用
```

**修复方向**：
1. 移除所有框架注解和依赖
2. 使用依赖倒置：领域层定义接口，基础设施层实现
3. 领域服务需访问外部资源时，通过接口注入：
   ```java
   // 领域层
   public interface IdGenerator { String nextId(); }

   // 领域对象
   private OrderId id = idGenerator.nextId();

   // 基础设施层实现
   @Component
   public class UUIDGenerator implements IdGenerator { ... }
   ```

---

### 反模式 4：万能聚合

**诊断特征**：
```
public class Order {
    private List<OrderItem> items;
    private Payment payment;         // 应为 PaymentId
    private Shipment shipment;      // 应为 ShipmentId
    private Invoice invoice;         // 应为 InvoiceId
    private List<Comment> comments;  // 应为独立聚合
    private List<Promotion> promos;  // 应为 OrderPromotions 聚合
    // ... 超过 10 个关联对象
}
```

**修复方向**：
1. 识别聚合内耦合紧密的对象子集
2. 拆分出独立聚合，通过 ID 关联
3. 通过领域事件保持聚合间最终一致性
4. 经验法则：聚合内实体超过 3 个，考虑拆分

---

### 反模式 5：绕过应用层

**诊断特征**：
```
@Controller 或 @RestController 中：
- 直接注入 Repository（应通过 ApplicationService）
- 直接暴露领域对象作为 Response（应转换为 DTO）
- 包含业务判断逻辑（if/switch）

public class OrderController {
    @Autowired private OrderRepository repo; // 错误
    @Autowired private OrderService service; // 错误：应为 ApplicationService
}
```

**修复方向**：
1. Controller 只做协议转换和输入校验
2. 业务逻辑通过 ApplicationService 编排
3. Response 使用 DTO，禁止直接暴露领域对象
4. ApplicationService 处理事务边界

---

## 严重程度分级

| 级别 | 标识 | 说明 |
|------|------|------|
| 严重 | **[S]** | 违反核心原则，必须修复才能合并 |
| 中等 | **[M]** | 规范偏差，建议修复，可讨论 |
| 轻微 | **[L]** | 优化建议，可后续处理 |
