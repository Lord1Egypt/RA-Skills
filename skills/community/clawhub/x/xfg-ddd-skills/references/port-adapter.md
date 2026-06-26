# Port & Adapter - 端口与适配器

## 核心原则

**端口与适配器是基础设施层与领域层之间的桥梁**：

```
┌─────────────────────────────────────────────────────────────┐
│                      领域层 Domain                          │
│                                                          │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  Domain Service / Entity                             │ │
│  │                                                       │ │
│  │  private IUserRepository userRepository;  ← 本地数据  │ │
│  │  private IProductPort productPort;      ← 远程调用    │ │
│  └─────────────────────────────────────────────────────┘ │
│                          │                                  │
│                          ▼                                  │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  适配器接口（定义在 Domain 层）                        │ │
│  │  - I{Xxx}Repository  → 本地数据访问                  │ │
│  │  - I{Xxx}Port        → 远程服务调用                   │ │
│  └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                          │
                          │ implements
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   基础设施层 Infrastructure                   │
│                                                          │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  适配器实现                                            │ │
│  │                                                       │ │
│  │  XxxRepository  → MySQL / Redis / Config              │ │
│  │  XxxPort        → HTTP / RPC / WebSocket              │ │
│  └─────────────────────────────────────────────────────┘ │
│                          │                                  │
│                          ▼                                  │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  DAO / Gateway / PO                                  │ │
│  └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Repository vs Port 职责划分

| 类型 | 命名 | 职责 | 技术栈 |
|------|------|------|--------|
| **Repository** | `IXxxRepository` / `XxxRepository` | 本地数据访问 | MySQL、Redis、Config |
| **Port** | `IXxxPort` / `XxxPort` | 远程服务调用 | HTTP、RPC、WebSocket |

### Repository - 本地数据

```java
/**
 * 用户仓储接口（定义在 Domain 层）
 */
public interface IUserRepository {
    
    UserAggregate findById(Long id);
    
    UserAggregate findByUserId(String userId);
    
    void save(UserAggregate aggregate);
    
    void update(UserAggregate aggregate);
}

/**
 * 用户仓储实现（定义在 Infrastructure 层）
 */
@Repository
public class UserRepository implements IUserRepository {
    
    @Resource
    private IUserDao userDao;
    
    @Resource
    private RedisTemplate<String, Object> redisTemplate;
    
    @Override
    public UserAggregate findById(Long id) {
        // 1. 先查 Redis 缓存
        String cacheKey = "user:id:" + id;
        UserAggregate cached = redisTemplate.opsForValue().get(cacheKey);
        if (cached != null) {
            return cached;
        }
        
        // 2. 缓存未命中，查 MySQL
        UserPO userPO = userDao.selectById(id);
        if (userPO == null) {
            return null;
        }
        
        // 3. 回填缓存
        UserAggregate aggregate = toAggregate(userPO);
        redisTemplate.opsForValue().set(cacheKey, aggregate, Duration.ofHours(24));
        
        return aggregate;
    }
    
    @Override
    @Transactional(rollbackFor = Exception.class)
    public void save(UserAggregate aggregate) {
        UserPO userPO = toPO(aggregate);
        userDao.insert(userPO);
        
        // 写入缓存
        String cacheKey = "user:id:" + userPO.getId();
        redisTemplate.opsForValue().set(cacheKey, aggregate, Duration.ofHours(24));
    }
}
```

### Port - 远程调用

```java
/**
 * 商品服务端口接口（定义在 Domain 层）
 */
public interface IProductPort {
    
    /**
     * 查询商品信息
     */
    ProductVO queryProduct(String productId);
    
    /**
     * 扣减库存
     */
    boolean deductStock(String productId, Integer quantity);
    
    /**
     * 验证商品是否在架
     */
    boolean isProductOnShelf(String productId);
}

/**
 * 商品服务端口实现（定义在 Infrastructure 层）
 */
@Component
public class ProductPort implements IProductPort {
    
    @Resource
    private RestTemplate restTemplate;
    
    @Value("${product.service.url}")
    private String productServiceUrl;

    @Override
    public ProductVO queryProduct(String productId) {
        try {
            ResponseEntity<ProductDTO> response = restTemplate.getForEntity(
                productServiceUrl + "/api/product/" + productId,
                ProductDTO.class
            );
            
            if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
                return toVO(response.getBody());
            }
            return null;
            
        } catch (Exception e) {
            log.error("查询商品失败, productId={}", productId, e);
            throw new ExternalServiceException("商品服务调用失败");
        }
    }

    @Override
    public boolean deductStock(String productId, Integer quantity) {
        try {
            Map<String, Object> params = Map.of("productId", productId, "quantity", quantity);
            restTemplate.postForEntity(
                productServiceUrl + "/api/product/deductStock",
                params,
                Void.class
            );
            return true;
            
        } catch (HttpClientErrorException e) {
            log.warn("扣减库存失败, productId={}, quantity={}", productId, quantity);
            return false;
        }
    }
}
```

## 命名规范

| 层级 | 接口命名 | 实现命名 | 示例 |
|------|---------|---------|------|
| **Domain** | `I{Xxx}Repository` | - | `IUserRepository` |
| **Domain** | `I{Xxx}Port` | - | `IProductPort` |
| **Infrastructure** | - | `XxxRepository` | `UserRepository` |
| **Infrastructure** | - | `XxxPort` | `ProductPort` |

**注意**：实现类**不使用 `Impl` 后缀**，直接用业务名称。

## Domain 层结构

```
domain/
└── {domain1}/
    ├── adapter/                    # 适配器接口（定义在领域层）
    │   ├── port/
    │   │   ├── IProductPort.java   # 远程调用接口
    │   │   ├── IOrderPort.java
    │   │   └── IPaymentPort.java
    │   └── repository/
    │       ├── IUserRepository.java    # 本地仓储接口
    │       ├── IOrderRepository.java
    │       └── IProductRepository.java
    ├── model/
    │   ├── aggregate/
    │   ├── entity/
    │   └── valobj/
    └── service/
        ├── I{Xxx}Service.java
        └── impl/
```

## Infrastructure 层结构

```
infrastructure/
├── adapter/
│   ├── port/                       # 端口实现（远程）
│   │   ├── ProductPort.java        # HTTP 调用
│   │   ├── OrderPort.java
│   │   └── PaymentPort.java
│   └── repository/                 # 仓储实现（本地）
│       ├── UserRepository.java    # MySQL + Redis
│       ├── OrderRepository.java
│       └── ProductRepository.java
├── dao/                           # DAO 接口
│   ├── IUserDao.java
│   └── IOrderDao.java
├── dataobject/                    # PO 类
│   ├── UserPO.java
│   └── OrderPO.java
├── gateway/                       # 外部网关
│   └── GenericHttpGateway.java
└── config/                        # 配置类
    └── RedisConfig.java
```

## 设计要点

### 1. 接口定义在 Domain，实现在 Infrastructure

```java
// Domain 层 - 只定义接口
public interface IUserRepository {
    UserAggregate findById(Long id);
}

// Infrastructure 层 - 实现接口
@Repository
public class UserRepository implements IUserRepository {
    // 实现...
}
```

### 2. Repository 和 Port 区分清楚

```java
// ❌ 错误：把远程调用放在 Repository
public interface IUserRepository {
    UserVO getRemoteUserInfo(String openId);  // ❌ 应该用 Port
}

// ✅ 正确：本地和远程分开
public interface IUserRepository {
    UserAggregate findById(Long id);      // 本地 MySQL/Redis
}
public interface IUserPort {
    UserVO getRemoteUserInfo(String openId);  // 远程 HTTP/RPC
}
```

### 3. 防腐层转换

```java
// Port 实现中进行格式转换，防止外部概念侵入 Domain

// 外部系统返回的状态码
public class ExternalProductService {
    public Map<String, Object> getProduct(String productId) {
        // 返回 {status: "ON_SALE", stock: 100, ...}
    }
}

// Domain 层只认自己的枚举
public interface IProductPort {
    ProductStatus getStatus(String productId);  // 返回 ProductStatus 枚举
}

// Port 实现中做转换
@Component
public class ProductPort implements IProductPort {
    
    @Override
    public ProductStatus getStatus(String productId) {
        ExternalProductDTO dto = externalService.getProduct(productId);
        
        // 外部状态码 → 领域状态枚举
        return switch (dto.getStatus()) {
            case "ON_SALE" -> ProductStatus.AVAILABLE;
            case "OFF_SALE" -> ProductStatus.UNAVAILABLE;
            case "SOLD_OUT" -> ProductStatus.OUT_OF_STOCK;
            default -> ProductStatus.UNKNOWN;
        };
    }
}
```

### 4. 异常处理

```java
@Component
public class ProductPort implements IProductPort {
    
    @Override
    public ProductVO queryProduct(String productId) {
        try {
            // 调用远程服务
            return externalService.getProduct(productId);
            
        } catch (HttpClientErrorException.NotFound e) {
            log.warn("商品不存在, productId={}", productId);
            return null;
            
        } catch (HttpServerErrorException e) {
            log.error("商品服务不可用, productId={}", productId, e);
            throw new ExternalServiceException("商品服务暂时不可用");
            
        } catch (Exception e) {
            log.error("查询商品异常, productId={}", productId, e);
            throw new ExternalServiceException("商品查询失败");
        }
    }
}
```

## Repository 实现模板

```java
/**
 * {Domain}Repository
 * 
 * 职责：
 * - MySQL 数据库访问
 * - Redis 缓存操作
 * - 配置中心读取
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
        
        // 2. 查询数据库
        {PO} po = {domain}Dao.selectById(id);
        if (po == null) {
            return null;
        }
        
        // 3. 转换并缓存
        {Domain}Aggregate aggregate = toAggregate(po);
        redisTemplate.opsForValue().set(cacheKey, aggregate, CACHE_EXPIRE);
        
        return aggregate;
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
        {domain}Dao.update(po);
        
        // 删除缓存（Cache Aside 模式）
        String cacheKey = CACHE_KEY_PREFIX + "id:" + aggregate.getId();
        redisTemplate.delete(cacheKey);
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

## Port 实现模板

```java
/**
 * {Domain}Port
 * 
 * 职责：
 * - HTTP 远程调用
 * - RPC 远程调用
 * - WebSocket 通信
 */
@Slf4j
@Component
public class {Domain}Port implements I{Domain}Port {

    @Resource
    private RestTemplate restTemplate;
    
    @Resource
    private GenericHttpGateway gateway;
    
    @Value("${remote.service.{domain}.url}")
    private String remoteServiceUrl;

    @Override
    public {Domain}VO query{Domain}(String bizId) {
        try {
            ResponseEntity<Remote{Domain}DTO> response = restTemplate.getForEntity(
                remoteServiceUrl + "/api/{domain}/" + bizId,
                Remote{Domain}DTO.class
            );
            
            if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
                return toVO(response.getBody());
            }
            return null;
            
        } catch (Exception e) {
            log.error("查询{领域}信息失败, bizId={}", bizId, e);
            throw new ExternalServiceException("{领域}服务调用失败");
        }
    }

    @Override
    public boolean executeOperation(String bizId, OperationCommand command) {
        try {
            HttpEntity<OperationCommand> request = new HttpEntity<>(command);
            restTemplate.postForEntity(
                remoteServiceUrl + "/api/{domain}/operation",
                request,
                Void.class
            );
            return true;
            
        } catch (HttpClientErrorException e) {
            log.warn("操作执行失败, bizId={}, status={}", bizId, e.getStatusCode());
            return false;
        }
    }

    // ==================== 转换方法 ====================
    
    private {Domain}VO toVO(Remote{Domain}DTO dto) {
        return {Domain}VO.builder()
                .bizId(dto.getId())
                .name(dto.getName())
                .status(DomainStatusEnum.valueOf(dto.getStatus()))
                .build();
    }
}
```

## 最佳实践

### ✅ 推荐做法

1. **接口定义在 Domain，实现放在 Infrastructure**
2. **Repository 处理本地数据（MySQL、Redis、Config）**
3. **Port 处理远程调用（HTTP、RPC、WebSocket）**
4. **实现类不使用 Impl 后缀，直接用业务名称**
5. **在 Port 中做防腐层转换**

### ❌ 避免做法

1. **不要在 Domain 层依赖 Infrastructure 的实现**
2. **不要把远程调用放在 Repository 里**
3. **不要让 PO/DTO 泄漏到 Domain 层**
4. **不要在适配器中写业务逻辑**

```java
// ❌ 错误示例
public class UserRepository {  // 在 Infrastructure 层
    
    // 业务逻辑不应该在这里
    public void createUser(CreateUserCommand command) {
        if (userService.hasPermission(command.getUserId())) {  // ❌ 领域逻辑
            throw new BusinessException("无权限");
        }
        // ...
    }
}

// ✅ 正确做法：业务逻辑在 Domain 层
public class UserDomainService {  // 在 Domain 层
    public void createUser(CreateUserCommand command) {
        if (!hasPermission(command.getUserId())) {  // ✅ 领域逻辑
            throw new BusinessException("无权限");
        }
        // ...
    }
}
```
