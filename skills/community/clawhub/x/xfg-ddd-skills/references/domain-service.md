# Domain Service - 领域服务

## 概述

Domain Service（领域服务）用于封装**跨多个聚合根**的业务逻辑，或**不适合放在单个实体/聚合根上**的操作。

## 目录结构

参考真实工程（如 `group-buy-market`、`ai-mcp-gateway`）的编码规范：

```
domain/
├── {domain}/
│   ├── adapter/
│   │   ├── port/          # 端口接口（外部系统适配）
│   │   └── repository/    # 仓储接口
│   ├── model/
│   │   ├── aggregate/    # 聚合根
│   │   ├── entity/       # 实体
│   │   └── valobj/       # 值对象
│   └── service/          # ⭐ 领域服务（核心）
│       ├── I{Xxx}Service.java        # 服务接口
│       ├── {子包}/                      # 按业务能力分包
│       │   ├── {Xxx}Service.java      # 服务实现
│       │   ├── factory/               # 工厂模式
│       │   │   └── XxxFactory.java
│       │   ├── filter/                # 责任链模式
│       │   │   └── XxxFilter.java
│       │   ├── strategy/              # 策略模式
│       │   │   ├── IXxxStrategy.java
│       │   │   └── impl/
│       │   │       └── XxxStrategyImpl.java
│       │   └── node/                  # 树形结构模式
│       │       └── XxxNode.java
```

## 何时使用

| 场景 | 是否使用 Domain Service |
|------|------------------------|
| 单个实体/聚合根的职责 | ❌ 放在 Entity/Aggregate 内部 |
| 跨多个聚合根的操作 | ✅ 使用 Domain Service |
| 需要组合多个领域能力 | ✅ 使用 Domain Service |
| 复杂业务规则（策略模式） | ✅ 使用 Domain Service |
| 多步骤过滤（责任链模式） | ✅ 使用 Domain Service |
| 纯计算逻辑 | ✅ 可放在 Domain Service |

## 命名规范

```java
// 接口命名：I{业务能力}Service.java
public interface IAuthLicenseService { }
public interface ITradeLockOrderService { }
public interface ITradeRefundOrderService { }

// 实现类命名：按子包组织
@Service
public class AuthLicenseService implements IAuthLicenseService { }
@Service
public class TradeLockOrderService implements ITradeLockOrderService { }

// 按子包分类（真实工程编码规范）
// service/license/AuthLicenseService.java
// service/lock/TradeLockOrderService.java
// service/refund/TradeRefundOrderService.java
```

## 编码模式

### 模式一：简单领域服务（单一职责）

**适用场景**：业务逻辑相对简单，不需要设计模式。

```java
/**
 * 鉴权许可服务接口
 * @author xiaofuge bugstack.cn @小傅哥
 */
public interface IAuthLicenseService {

    boolean checkLicense(LicenseCommandEntity commandEntity);

}

/**
 * 鉴权许可服务实现
 * @author xiaofuge bugstack.cn @小傅哥
 */
@Slf4j
@Service
public class AuthLicenseService implements IAuthLicenseService {

    @Resource
    private IAuthRepository repository;

    @Override
    public boolean checkLicense(LicenseCommandEntity commandEntity) {
        // 查询网关认证配置信息
        McpGatewayAuthVO mcpGatewayAuthVO = repository.queryEffectiveGatewayAuthInfo(commandEntity);

        // 没有匹配到权限返回 false
        if (null == mcpGatewayAuthVO) return false;

        // 检查是否开启了认证模式
        if (AuthStatusEnum.AuthConfig.DISABLE.equals(mcpGatewayAuthVO.getStatus())) {
            return false;
        }

        // 判断过期时间
        Date expireTime = mcpGatewayAuthVO.getExpireTime();
        if (null == expireTime) return true;

        return new Date().before(expireTime);
    }
}
```

### 模式二：策略模式（Strategy Pattern）

**适用场景**：同一业务操作有多种处理策略，根据条件选择执行。

```java
/**
 * 退单策略接口
 * @author xiaofuge bugstack.cn @小傅哥
 */
public interface IRefundOrderStrategy {

    void refundOrder(TradeRefundOrderEntity tradeRefundOrderEntity) throws Exception;

    void reverseStock(TeamRefundSuccess teamRefundSuccess) throws Exception;

}

/**
 * 退单策略抽象基类 - 模板方法模式
 * 提供共用的依赖注入和通用逻辑
 * @author xiaofuge bugstack.cn @小傅哥
 */
@Slf4j
public abstract class AbstractRefundOrderStrategy implements IRefundOrderStrategy {

    @Resource
    protected ITradeRepository repository;

    @Resource
    protected ThreadPoolExecutor threadPoolExecutor;

    /**
     * 异步发送MQ消息
     */
    protected void sendRefundNotifyMessage(NotifyTaskEntity notifyTaskEntity, String refundType) {
        if (null != notifyTaskEntity) {
            threadPoolExecutor.execute(() -> {
                // 发送MQ消息逻辑
            });
        }
    }

    /**
     * 通用库存恢复逻辑
     */
    protected void doReverseStock(TeamRefundSuccess teamRefundSuccess, String refundType) throws Exception {
        log.info("退单；恢复锁单量 - {}", refundType);
        // 恢复库存逻辑
    }
}

/**
 * 已支付、未成团退单策略
 * @author xiaofuge bugstack.cn @小傅哥
 */
@Slf4j
@Service("paid2RefundStrategy")
public class Paid2RefundStrategy extends AbstractRefundOrderStrategy {

    @Override
    public void refundOrder(TradeRefundOrderEntity tradeRefundOrderEntity) throws Exception {
        log.info("退单；已支付，未成团 userId:{} teamId:{}", 
                tradeRefundOrderEntity.getUserId(), tradeRefundOrderEntity.getTeamId());

        // 1. 执行业务逻辑
        NotifyTaskEntity notifyTaskEntity = repository.paid2Refund(
                GroupBuyRefundAggregate.buildPaid2RefundAggregate(tradeRefundOrderEntity, -1, -1));

        // 2. 发送MQ消息
        sendRefundNotifyMessage(notifyTaskEntity, "已支付，未成团");
    }

    @Override
    public void reverseStock(TeamRefundSuccess teamRefundSuccess) throws Exception {
        doReverseStock(teamRefundSuccess, "已支付，未成团，但有锁单记录");
    }
}

/**
 * 未支付退单策略
 * @author xiaofuge bugstack.cn @小傅哥
 */
@Slf4j
@Service("unpaid2RefundStrategy")
public class Unpaid2RefundStrategy extends AbstractRefundOrderStrategy {

    @Override
    public void refundOrder(TradeRefundOrderEntity tradeRefundOrderEntity) throws Exception {
        log.info("退单；未支付 userId:{} teamId:{}", 
                tradeRefundOrderEntity.getUserId(), tradeRefundOrderEntity.getTeamId());
        // 只需恢复锁单库存，无需发送MQ
    }

    @Override
    public void reverseStock(TeamRefundSuccess teamRefundSuccess) throws Exception {
        doReverseStock(teamRefundSuccess, "未支付，直接恢复锁单库存");
    }
}
```

### 模式三：责任链模式（Chain Pattern）

**适用场景**：多步骤过滤/校验，每个步骤可独立、可组合。

```java
/**
 * 锁单规则过滤器接口
 */
public interface ITradeLockRuleFilter {

    /**
     * 执行过滤规则
     * @param command 过滤命令
     * @param context 动态上下文
     * @return 过滤结果
     */
    TradeLockRuleFilterBackEntity filter(TradeLockRuleFilterCommandEntity command, 
                                         TradeLockRuleFilterFactory.DynamicContext context);
}

/**
 * 活动可用性规则过滤器
 * @author xiaofuge bugstack.cn @小傅哥
 */
@Slf4j
@Service
public class ActivityUsabilityRuleFilter implements ITradeLockRuleFilter {

    @Resource
    private IActivityRepository activityRepository;

    @Override
    public TradeLockRuleFilterBackEntity filter(TradeLockRuleFilterCommandEntity command,
                                                TradeLockRuleFilterFactory.DynamicContext context) {
        log.info("规则过滤-活动可用性校验 activityId:{}", command.getActivityId());

        // 1. 查询活动信息
        ActivityEntity activity = activityRepository.findById(command.getActivityId());

        // 2. 校验活动状态
        if (!ActivityStatusEnum.ONLINE.equals(activity.getStatus())) {
            throw new AppException("活动未上线");
        }

        // 3. 校验活动时间
        if (new Date().before(activity.getStartTime())) {
            throw new AppException("活动未开始");
        }

        if (new Date().after(activity.getEndTime())) {
            throw new AppException("活动已结束");
        }

        return TradeLockRuleFilterBackEntity.builder().build();
    }
}

/**
 * 用户参与限制规则过滤器
 * @author xiaofuge bugstack.cn @小傅哥
 */
@Slf4j
@Service
public class UserTakeLimitRuleFilter implements ITradeLockRuleFilter {

    @Resource
    private ITradeRepository tradeRepository;

    @Override
    public TradeLockRuleFilterBackEntity filter(TradeLockRuleFilterCommandEntity command,
                                                TradeLockRuleFilterFactory.DynamicContext context) {
        log.info("规则过滤-用户参与限制校验 userId:{}", command.getUserId());

        // 1. 查询用户已参与次数
        Integer userTakeCount = tradeRepository.queryUserTakeOrderCount(
                command.getActivityId(), command.getUserId());

        // 2. 获取活动限制
        Integer limitCount = command.getLimitCount();

        // 3. 超出限制则拦截
        if (userTakeCount >= limitCount) {
            throw new AppException("用户参与次数已达上限");
        }

        return TradeLockRuleFilterBackEntity.builder()
                .userTakeOrderCount(userTakeCount)
                .build();
    }
}

/**
 * 锁单规则过滤器工厂 - 负责组装责任链
 * @author xiaofuge bugstack.cn @小傅哥
 */
@Slf4j
@Service
public class TradeLockRuleFilterFactory {

    @Resource
    private ActivityUsabilityRuleFilter activityUsabilityRuleFilter;

    @Resource
    private UserTakeLimitRuleFilter userTakeLimitRuleFilter;

    @Resource
    private TeamStockOccupyRuleFilter teamStockOccupyRuleFilter;

    /**
     * 构建责任链并执行
     */
    public TradeLockRuleFilterBackEntity doFilter(TradeLockRuleFilterCommandEntity command) {
        log.info("开始执行锁单规则过滤...");

        // 顺序执行多个过滤器
        TradeLockRuleFilterBackEntity result = activityUsabilityRuleFilter.filter(command, null);
        result = userTakeLimitRuleFilter.filter(command, null);
        result = teamStockOccupyRuleFilter.filter(command, null);

        return result;
    }
}
```

### 模式四：树形结构模式（Tree Pattern）

**适用场景**：复杂业务流程需要多个分支处理。

```java
/**
 * 营销试算策略处理器接口
 */
public interface IMarketStrategyHandler {

    /**
     * 执行业务处理
     * @param request 请求参数
     * @param context 动态上下文
     * @return 处理结果
     */
    TrialBalanceResult handle(MarketTrialRequest request, DynamicContext context);
}

/**
 * 根节点处理器
 * @author xiaofuge bugstack.cn @小傅哥
 */
@Slf4j
@Service
public class RootNode implements IMarketStrategyHandler {

    @Resource
    private MarketNode marketNode;

    @Override
    public TrialBalanceResult handle(MarketTrialRequest request, DynamicContext context) {
        log.info("营销试算-根节点处理 activityId:{}", request.getActivityId());
        return marketNode.handle(request, context);
    }
}

/**
 * 标签节点处理器
 * @author xiaofuge bugstack.cn @小傅哥
 */
@Slf4j
@Service
public class TagNode implements IMarketStrategyHandler {

    @Resource
    private SwitchNode switchNode;

    @Override
    public TrialBalanceResult handle(MarketTrialRequest request, DynamicContext context) {
        log.info("营销试算-标签节点处理 tag:{}", request.getTag());

        // 标签匹配逻辑
        if (request.getTag().matches(".*团长.*")) {
            return switchNode.handle(request, context);
        }

        return null;
    }
}

/**
 * 营销节点处理器
 * @author xiaofuge bugstack.cn @小傅哥
 */
@Slf4j
@Service
public class MarketNode implements IMarketStrategyHandler {

    @Resource
    private TagNode tagNode;

    @Override
    public TrialBalanceResult handle(MarketTrialRequest request, DynamicContext context) {
        log.info("营销试算-营销节点处理 activityId:{}", request.getActivityId());

        // 执行营销计算
        TrialBalanceResult result = new TrialBalanceResult();
        // ... 营销逻辑

        return tagNode.handle(request, context);
    }
}

/**
 * 开关节点处理器
 * @author xiaofuge bugstack.cn @小傅哥
 */
@Slf4j
@Service
public class SwitchNode implements IMarketStrategyHandler {

    @Resource
    private EndNode endNode;

    @Override
    public TrialBalanceResult handle(MarketTrialRequest request, DynamicContext context) {
        log.info("营销试算-开关节点处理");

        // 根据开关状态决定下一步
        if (Boolean.TRUE.equals(request.getFeatureSwitch())) {
            return endNode.handle(request, context);
        }

        return null;
    }
}

/**
 * 结束节点处理器
 * @author xiaofuge bugstack.cn @小傅哥
 */
@Slf4j
@Service
public class EndNode implements IMarketStrategyHandler {

    @Override
    public TrialBalanceResult handle(MarketTrialRequest request, DynamicContext context) {
        log.info("营销试算-结束节点");
        return TrialBalanceResult.builder()
                .success(true)
                .message("试算完成")
                .build();
    }
}
```

## 真实工程示例

### ai-mcp-gateway 项目 - 鉴权域

```
auth/
├── adapter/
│   └── repository/IAuthRepository.java
├── model/
│   ├── aggregate/
│   ├── entity/
│   │   ├── LicenseCommandEntity.java
│   │   ├── RateLimitCommandEntity.java
│   │   └── RegisterCommandEntity.java
│   └── valobj/
│       ├── McpGatewayAuthVO.java
│       └── enums/AuthStatusEnum.java
└── service/
    ├── IAuthLicenseService.java         # 接口
    ├── IAuthRateLimitService.java       # 接口
    ├── IAuthRegisterService.java        # 接口
    ├── license/
    │   └── AuthLicenseService.java      # 实现
    ├── ratelimit/
    │   └── AuthRateLimitService.java    # 实现
    └── register/
        └── AuthRegisterService.java     # 实现
```

### group-buy-market 项目 - 交易域

```
trade/
├── adapter/
│   ├── port/ITradePort.java
│   └── repository/ITradeRepository.java
├── model/
│   ├── aggregate/
│   │   ├── GroupBuyOrderAggregate.java
│   │   ├── GroupBuyRefundAggregate.java
│   │   └── GroupBuyTeamSettlementAggregate.java
│   ├── entity/
│   │   ├── GroupBuyActivityEntity.java
│   │   ├── GroupBuyTeamEntity.java
│   │   ├── MarketPayOrderEntity.java
│   │   ├── PayActivityEntity.java
│   │   └── TradeRefundOrderEntity.java
│   └── valobj/
│       ├── GroupBuyProgressVO.java
│       └── TradeOrderStatusEnumVO.java
└── service/
    ├── ITradeLockOrderService.java          # 接口
    ├── ITradeRefundOrderService.java        # 接口
    ├── ITradeSettlementOrderService.java    # 接口
    ├── ITradeTaskService.java               # 接口
    ├── lock/
    │   ├── TradeLockOrderService.java       # 实现
    │   ├── factory/
    │   │   └── TradeLockRuleFilterFactory.java
    │   └── filter/
    │       ├── ActivityUsabilityRuleFilter.java
    │       ├── TeamStockOccupyRuleFilter.java
    │       └── UserTakeLimitRuleFilter.java
    ├── refund/
    │   ├── TradeRefundOrderService.java     # 实现
    │   ├── business/
    │   │   ├── AbstractRefundOrderStrategy.java   # 模板方法
    │   │   ├── IRefundOrderStrategy.java            # 策略接口
    │   │   └── impl/
    │   │       ├── Paid2RefundStrategy.java
    │   │       ├── Unpaid2RefundStrategy.java
    │   │       └── PaidTeam2RefundStrategy.java
    │   ├── factory/
    │   │   └── TradeRefundRuleFilterFactory.java
    │   └── filter/
    │       ├── DataNodeFilter.java
    │       ├── RefundOrderNodeFilter.java
    │       └── UniqueRefundNodeFilter.java
    ├── settlement/
    │   ├── TradeSettlementOrderService.java # 实现
    │   └── filter/
    │       ├── EndRuleFilter.java
    │       ├── SCRuleFilter.java
    │       └── SettableRuleFilter.java
    └── task/
        └── TradeTaskService.java
```

## 设计原则

### 1. 保持 Domain Service 职责单一

```java
// ❌ 错误：一个 Service 承担过多职责
@Service
public class OrderServiceImpl {
    // 订单、支付、退款、库存、通知... 全都在一起
}

// ✅ 正确：按业务能力拆分
public interface IOrderDomainService { }     // 订单管理
public interface IPaymentDomainService { }    // 支付处理
public interface IRefundDomainService { }     // 退款处理
```

### 2. 依赖方向严格遵守

```
Domain Service 只依赖：
├── Repository 接口（domain/adapter/repository/）
├── Port 接口（domain/adapter/port/）
└── 其他 Domain Service 接口

Domain Service 不依赖：
├── Infrastructure 层实现类
├── DAO、Mapper 实现
└── 第三方框架类
```

### 3. 事务边界在 Case 层控制

```java
// Case 层 - 控制事务
@Service
public class OrderCaseImpl implements IOrderCase {

    @Resource
    private ITradeLockOrderService tradeLockOrderService;

    @Override
    @Transactional(rollbackFor = Exception.class)
    public MarketPayOrderEntity lockOrder(OrderLockRequest request) {
        // 整个业务在一个事务中
        return tradeLockOrderService.lockMarketPayOrder(...);
    }
}
```

## 常见问题

### Q: Domain Service 和 Entity Method 的区别？

| 维度 | Entity Method | Domain Service |
|------|---------------|----------------|
| 范围 | 单个实体/聚合根内部 | 跨多个聚合根 |
| 依赖 | 只操作自身状态 | 依赖多个仓储/端口 |
| 事务 | 可在方法内控制 | 通常由调用方控制 |

### Q: Domain Service 可以有几种实现方式？

| 模式 | 适用场景 | 示例 |
|------|---------|------|
| 直接实现 | 简单业务逻辑 | `AuthLicenseService` |
| 策略模式 | 多种处理策略 | `IRefundOrderStrategy` + 实现类 |
| 责任链模式 | 多步骤过滤 | `IFilter` + Filter链 |
| 树形模式 | 分支流程处理 | `INodeHandler` + Node链 |
| 模板方法 | 通用逻辑+子类扩展 | `AbstractXxxStrategy` |

### Q: Service 接口定义在哪个包？

始终定义在 `service/` 目录下，实现类放在子包中：

```
service/
├── IAuthLicenseService.java      # 接口放这里
├── license/                       # 按业务能力分包
│   └── AuthLicenseService.java   # 实现放子包
└── ratelimit/
    └── AuthRateLimitService.java
```
