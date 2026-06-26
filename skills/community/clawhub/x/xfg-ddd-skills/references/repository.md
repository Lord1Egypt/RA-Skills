# Repository Pattern - 仓储模式

## 概述

Repository（仓储）是领域层与本地数据存储之间的桥梁。

## 核心职责

| 职责 | 说明 |
|------|------|
| **MySQL** | 数据库 CRUD 操作 |
| **Redis** | 缓存读写 |
| **Config** | 配置中心读取 |
| **本地文件** | 本地文件读写 |

**原则**：Repository 只操作**本地数据**，不进行远程调用。

## 命名规范

```
Domain 层：I{Xxx}Repository.java
Infrastructure 层：XxxRepository.java（无 Impl 后缀）
```

## 目录结构

```
Domain 层/
└── {domain}/
    └── adapter/
        └── repository/
            └── I{Domain}Repository.java    ← 接口定义

Infrastructure 层/
└── adapter/
    └── repository/
        └── {Domain}Repository.java         ← 实现
```

## 接口定义

```java
/**
 * {Domain}仓储接口
 * 
 * 职责：本地数据访问（MySQL / Redis / Config）
 * 定义在 Domain 层，实现 在 Infrastructure 层
 */
public interface I{Domain}Repository {

    // ==================== 单条操作 ====================
    
    /**
     * 根据ID查询
     */
    {Domain}Aggregate findById(Long id);
    
    /**
     * 根据业务ID查询
     */
    {Domain}Aggregate findByBizId(String bizId);
    
    /**
     * 保存（新增）
     */
    void save({Domain}Aggregate aggregate);
    
    /**
     * 更新
     */
    void update({Domain}Aggregate aggregate);
    
    /**
     * 删除
     */
    void delete(Long id);

    // ==================== 批量操作 ====================
    
    /**
     * 批量保存
     */
    void batchSave(List<{Domain}Aggregate> aggregates);
    
    /**
     * 根据ID列表查询
     */
    List<{Domain}Aggregate> findByIds(List<Long> ids);

    // ==================== 条件查询 ====================
    
    /**
     * 条件查询
     */
    List<{Domain}Aggregate> findByCondition({Query}Entity query);
    
    /**
     * 分页查询
     */
    PageResult<{Domain}Aggregate> findPage({Query}Entity query, int page, int size);
}
```

## 实现模板

```java
/**
 * {Domain}Repository
 * 
 * 职责：本地数据访问（MySQL + Redis）
 */
@Slf4j
@Repository
public class {Domain}Repository implements I{Domain}Repository {

    @Resource
    private I{Domain}Dao {domain}Dao;
    
    @Resource
    private RedisTemplate<String, Object> redisTemplate;
    
    private static final String CACHE_KEY_PREFIX = "{domain}:";
    private static final Duration CACHE_EXPIRE = Duration.ofHours(24);

    @Override
    public {Domain}Aggregate findById(Long id) {
        // 1. 查询缓存
        String cacheKey = CACHE_KEY_PREFIX + "id:" + id;
        {Domain}Aggregate cached = redisTemplate.opsForValue().get(cacheKey);
        if (cached != null) {
            log.debug("缓存命中, id={}", id);
            return cached;
        }
        
        // 2. 缓存未命中，查询 MySQL
        {PO} po = {domain}Dao.selectById(id);
        if (po == null) {
            return null;
        }
        
        // 3. 转换并回填缓存
        {Domain}Aggregate aggregate = toAggregate(po);
        redisTemplate.opsForValue().set(cacheKey, aggregate, CACHE_EXPIRE);
        
        return aggregate;
    }

    @Override
    public {Domain}Aggregate findByBizId(String bizId) {
        {PO} po = {domain}Dao.selectByBizId(bizId);
        if (po == null) {
            return null;
        }
        return findById(po.getId());
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void save({Domain}Aggregate aggregate) {
        {PO} po = toPO(aggregate);
        {domain}Dao.insert(po);
        
        // 更新缓存
        String cacheKey = CACHE_KEY_PREFIX + "id:" + po.getId();
        redisTemplate.opsForValue().set(cacheKey, aggregate, CACHE_EXPIRE);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void update({Domain}Aggregate aggregate) {
        {PO} po = toPO(aggregate);
        int count = {domain}Dao.update(po);
        if (count != 1) {
            throw new BusinessException("更新失败，记录不存在");
        }
        
        // 删除缓存（Cache Aside 模式）
        String cacheKey = CACHE_KEY_PREFIX + "id:" + aggregate.getId();
        redisTemplate.delete(cacheKey);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void delete(Long id) {
        {domain}Dao.deleteById(id);
        
        // 删除缓存
        String cacheKey = CACHE_KEY_PREFIX + "id:" + id;
        redisTemplate.delete(cacheKey);
    }

    @Override
    public PageResult<{Domain}Aggregate> findPage({Query}Entity query, int page, int size) {
        int offset = (page - 1) * size;
        
        // MySQL 分页查询
        List<{PO}> pos = {domain}Dao.selectPage(query, offset, size);
        long total = {domain}Dao.count(query);
        
        // 转换
        List<{Domain}Aggregate> aggregates = pos.stream()
            .map(this::toAggregate)
            .collect(Collectors.toList());
        
        return PageResult.of(aggregates, total, page, size);
    }

    // ==================== 转换方法 ====================
    
    private {Domain}Aggregate toAggregate({PO} po) {
        return {Domain}Aggregate.builder()
            .id(po.getId())
            .bizId(po.getBizId())
            .status(StatusEnum.valueOf(po.getStatus()))
            .build();
    }
    
    private {PO} toPO({Domain}Aggregate aggregate) {
        return {PO}.builder()
            .id(aggregate.getId())
            .bizId(aggregate.getBizId())
            .status(aggregate.getStatus().getCode())
            .build();
    }
}
```

## 完整示例

```java
/**
 * 订单仓储接口
 */
public interface IOrderRepository {
    
    // 单条操作
    OrderAggregate findById(Long id);
    OrderAggregate findByOrderId(String orderId);
    void save(OrderAggregate aggregate);
    void update(OrderAggregate aggregate);
    void delete(Long id);
    
    // 条件查询
    List<OrderAggregate> findByUserId(Long userId);
    List<OrderAggregate> findByStatus(OrderStatusEnum status);
    PageResult<OrderAggregate> findPage(OrderQuery query, int page, int size);
    
    // 存在性检查
    boolean existsByOrderId(String orderId);
}

/**
 * 订单仓储实现
 */
@Slf4j
@Repository
public class OrderRepository implements IOrderRepository {

    @Resource
    private IOrderDao orderDao;
    
    @Resource
    private IOrderItemDao orderItemDao;
    
    @Resource
    private RedisTemplate<String, Object> redisTemplate;

    @Override
    public OrderAggregate findById(Long id) {
        // 1. 查缓存
        String cacheKey = "order:id:" + id;
        OrderAggregate cached = redisTemplate.opsForValue().get(cacheKey);
        if (cached != null) {
            return cached;
        }
        
        // 2. 查 MySQL
        OrderPO orderPO = orderDao.selectById(id);
        if (orderPO == null) {
            return null;
        }
        
        // 3. 查关联表
        List<OrderItemPO> itemPOs = orderItemDao.selectByOrderId(id);
        
        // 4. 转换并缓存
        OrderAggregate aggregate = toAggregate(orderPO, itemPOs);
        redisTemplate.opsForValue().set(cacheKey, aggregate, Duration.ofHours(24));
        
        return aggregate;
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void save(OrderAggregate aggregate) {
        // 1. 保存主表
        OrderPO orderPO = toOrderPO(aggregate);
        orderDao.insert(orderPO);
        
        // 2. 保存明细表
        for (OrderItemEntity item : aggregate.getItems()) {
            OrderItemPO itemPO = toItemPO(item, orderPO.getId());
            orderItemDao.insert(itemPO);
        }
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void update(OrderAggregate aggregate) {
        OrderPO orderPO = toOrderPO(aggregate);
        int count = orderDao.update(orderPO);
        if (count != 1) {
            throw new BusinessException("订单不存在: " + aggregate.getOrderId());
        }
        
        // 删除缓存
        redisTemplate.delete("order:id:" + aggregate.getId());
    }

    @Override
    public PageResult<OrderAggregate> findPage(OrderQuery query, int page, int size) {
        int offset = (page - 1) * size;
        List<OrderPO> orderPOs = orderDao.selectPage(query, offset, size);
        long total = orderDao.count(query);
        
        List<OrderAggregate> aggregates = orderPOs.stream()
            .map(po -> findById(po.getId()))
            .collect(Collectors.toList());
        
        return PageResult.of(aggregates, total, page, size);
    }

    // ==================== 转换方法 ====================
    
    private OrderAggregate toAggregate(OrderPO orderPO, List<OrderItemPO> itemPOs) {
        return OrderAggregate.builder()
            .order(toOrderEntity(orderPO))
            .items(toItemEntities(itemPOs))
            .build();
    }
    
    private OrderEntity toOrderEntity(OrderPO po) {
        return OrderEntity.builder()
            .id(po.getId())
            .orderId(po.getOrderId())
            .userId(po.getUserId())
            .status(OrderStatusEnum.valueOf(po.getStatus()))
            .totalAmount(po.getTotalAmount())
            .build();
    }
    
    private OrderPO toOrderPO(OrderAggregate aggregate) {
        OrderEntity order = aggregate.getOrder();
        return OrderPO.builder()
            .id(order.getId())
            .orderId(order.getOrderId())
            .userId(order.getUserId())
            .status(order.getStatus().getCode())
            .totalAmount(order.getTotalAmount())
            .build();
    }
}
```

## 对象转换规则

```
Domain Object (Aggregate / Entity / VO)
              ↕
Persistence Object (PO)
```

| 转换方向 | 方法 | 说明 |
|----------|------|------|
| Aggregate → PO | `toPO()` | `save()` / `update()` 时调用 |
| PO → Aggregate | `toAggregate()` | `findById()` 时调用 |
| Entity → PO | 私有方法 | 内部转换 |
| PO → Entity | 私有方法 | 内部转换 |

## 最佳实践

### ✅ 推荐

```java
// ✅ 接口定义在 Domain 层
public interface IOrderRepository {
    OrderAggregate findById(Long id);
}

// ✅ 实现在 Infrastructure 层
@Repository
public class OrderRepository implements IOrderRepository { }

// ✅ 操作聚合根
void save(OrderAggregate aggregate);

// ✅ 语义化命名
List<OrderAggregate> findPendingOrders();
```

### ❌ 避免

```java
// ❌ 返回 PO
OrderPO findById(Long id);

// ❌ 包含业务逻辑
public void save(OrderAggregate aggregate) {
    if (aggregate.getTotal() > 10000) {
        throw new BusinessException("金额过大");  // ❌ 业务逻辑
    }
}

// ❌ 暴露 DAO
IOrderDao getOrderDao();

// ❌ 通用方法
<T> T find(String query);  // ❌ 过于通用
```

## Repository vs Port

| 维度 | Repository | Port |
|------|-----------|------|
| **职责** | 本地数据访问 | 远程服务调用 |
| **数据源** | MySQL、Redis、Config | HTTP、RPC、WebSocket |
| **命名** | `I{Xxx}Repository` | `I{Xxx}Port` |
| **实现** | `XxxRepository` | `XxxPort` |
| **示例** | 用户信息查询 | 用户信息远程校验 |