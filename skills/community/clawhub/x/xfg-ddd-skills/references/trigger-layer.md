# Trigger Layer - 触发层

## 概述

Trigger 层（触发层/接入层）是 DDD 六边形架构的最外层，负责接收外部请求并触发业务流程。

## 职责

Trigger 层只做三件事：

1. **接收请求** - HTTP/MQ/Job 接收外部输入
2. **调用 Case** - 将请求委托给 Case 层处理
3. **封装响应** - 将 Case 返回结果转换为外部格式

**核心原则**：Trigger 层**不包含任何业务逻辑**，只负责路由。

## 三种触发方式

### 1. HTTP Controller

```java
/**
 * 订单触发器 - HTTP 接入
 */
@Slf4j
@RestController
@RequestMapping("/api/v1/orders")
public class OrderTrigger {

    @Resource
    private IOrderCase orderCase;

    @PostMapping("/create")
    public Response<OrderDTO> create(@RequestBody @Valid CreateOrderRequest request) {
        log.info("创建订单请求: {}", request);
        return orderCase.createOrder(request);
    }

    @PostMapping("/cancel/{orderId}")
    public Response<Void> cancel(@PathVariable Long orderId) {
        log.info("取消订单请求: orderId={}", orderId);
        return orderCase.cancelOrder(orderId);
    }

    @GetMapping("/{orderId}")
    public Response<OrderDTO> getOrder(@PathVariable Long orderId) {
        return orderCase.getOrder(orderId);
    }
}
```

### 2. MQ Listener

```java
/**
 * 订单事件监听器 - MQ 接入
 */
@Slf4j
@Service
public class OrderEventListener {

    @Resource
    private IOrderCase orderCase;

    @RabbitListener(queues = "order.created.queue")
    public void onOrderCreated(OrderCreatedEvent event) {
        log.info("收到订单创建事件: {}", event);
        try {
            orderCase.handleOrderCreated(event);
        } catch (Exception e) {
            log.error("处理订单创建事件异常", e);
            // 可选：发送到死信队列
        }
    }

    @RabbitListener(queues = "order.paid.queue")
    public void onOrderPaid(OrderPaidEvent event) {
        log.info("收到订单支付事件: {}", event);
        orderCase.handleOrderPaid(event);
    }
}
```

### 3. Scheduled Job

```java
/**
 * 订单定时任务 - Job 接入
 */
@Slf4j
@Component
public class OrderJob {

    @Resource
    private IOrderCase orderCase;

    /**
     * 每天凌晨2点执行：自动取消超时未支付订单
     */
    @Scheduled(cron = "0 0 2 * * ?")
    public void cancelTimeoutOrders() {
        log.info("开始执行超时订单取消任务");
        try {
            orderCase.cancelTimeoutOrders();
            log.info("超时订单取消任务执行完成");
        } catch (Exception e) {
            log.error("超时订单取消任务执行异常", e);
        }
    }

    /**
     * 每小时执行：订单状态同步
     */
    @Scheduled(fixedRate = 3600000)
    public void syncOrderStatus() {
        log.info("开始执行订单状态同步任务");
        orderCase.syncOrderStatus();
    }
}
```

## 请求对象校验

使用 `@Valid` 和 `@Validated` 进行请求参数校验：

```java
@PostMapping("/create")
public Response<OrderDTO> create(@RequestBody @Valid CreateOrderRequest request) {
    // 如果校验失败，Spring 会自动返回 400 错误
    return orderCase.createOrder(request);
}
```

```java
@Data
public class CreateOrderRequest {

    @NotNull(message = "用户ID不能为空")
    private Long userId;

    @NotEmpty(message = "订单项不能为空")
    private List<OrderItemDTO> items;

    @Min(value = 1, message = "数量最小为1")
    private Integer quantity;

    @DecimalMin(value = "0.01", message = "金额最小为0.01")
    private BigDecimal amount;
}
```

## 响应封装

统一使用 Response 包装返回值：

```java
@Data
@Builder
public class Response<T> {

    private boolean success;
    private String code;
    private String info;
    private T data;

    public static <T> Response<T> ok(T data) {
        return Response.<T>builder()
                .success(true)
                .code("0000")
                .info("success")
                .data(data)
                .build();
    }

    public static <T> Response<T> fail(String code, String info) {
        return Response.<T>builder()
                .success(false)
                .code(code)
                .info(info)
                .build();
    }
}
```

## 全局异常处理

配合 `@ControllerAdvice` 处理系统异常：

```java
@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(BusinessException.class)
    public Response<Void> handleBusinessException(BusinessException e) {
        log.warn("业务异常: {}", e.getMessage());
        return Response.fail(e.getCode(), e.getMessage());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public Response<Void> handleValidException(MethodArgumentNotValidException e) {
        String message = e.getBindingResult().getFieldError().getDefaultMessage();
        log.warn("参数校验异常: {}", message);
        return Response.fail("VALIDATION_ERROR", message);
    }

    @ExceptionHandler(Exception.class)
    public Response<Void> handleException(Exception e) {
        log.error("系统异常", e);
        return Response.fail("SYSTEM_ERROR", "系统繁忙，请稍后重试");
    }
}
```

## 设计要点

### 1. 保持轻量

```java
// ❌ 错误：Trigger 包含业务逻辑
@PostMapping("/create")
public Response<OrderDTO> create(CreateOrderRequest request) {
    // 查库存
    InventoryEntity inventory = inventoryService.get(request.getItemId());
    if (inventory.getStock() < request.getQuantity()) {
        return Response.fail("STOCK_NOT_ENOUGH", "库存不足");
    }
    // 创建订单
    OrderAggregate order = new OrderAggregate();
    order.create(request);
    // 保存
    orderRepository.save(order);
    // 发消息
    mqProducer.send("order.created", order);
    return Response.ok(OrderDTO.from(order));
}

// ✅ 正确：委托给 Case 层
@PostMapping("/create")
public Response<OrderDTO> create(CreateOrderRequest request) {
    return orderCase.createOrder(request);
}
```

### 2. 日志规范

```java
@Slf4j
@RestController
@RequestMapping("/api/v1/orders")
public class OrderTrigger {

    @PostMapping("/create")
    public Response<OrderDTO> create(@RequestBody @Valid CreateOrderRequest request) {
        // 请求入口记录日志
        log.info("创建订单请求: userId={}, items={}", request.getUserId(), request.getItems());
        
        Response<OrderDTO> response = orderCase.createOrder(request);
        
        // 响应出口记录日志（敏感信息脱敏）
        log.info("创建订单响应: success={}, orderId={}", 
                response.isSuccess(), 
                response.getData() != null ? response.getData().getOrderId() : null);
        
        return response;
    }
}
```

### 3. 统一前缀

```java
// HTTP API 统一前缀
@RequestMapping("/api/v1/orders")

// 内部接口统一前缀（区分外部和内部）
@RequestMapping("/inner/api/v1/orders")
```

## 与其他层的关系

```
┌─────────────────────────────────────────────────────────────┐
│                      Trigger 层                             │
│                  HTTP / MQ / Job                             │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          │ 只调用 Case 层
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                       Case 层                               │
│                   业务编排与流程控制                          │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                      Domain 层                              │
│                   领域模型与业务规则                          │
└─────────────────────────────────────────────────────────────┘
```

## 常见问题

### Q: 什么时候用 MQ Listener 而不是 HTTP？

- 需要异步处理时
- 需要保证消息可靠性时
- 跨系统事件驱动时
- 需要消息重试机制时

### Q: Job 和 MQ Listener 的区别？

- Job 是定时任务，适合周期性处理
- MQ Listener 是事件驱动，适合实时响应

### Q: 如何选择 @GetMapping 还是 @PostMapping？

- GET：查询操作，幂等
- POST：创建/更新操作，非幂等
