# 事件风暴（Event Storming）工作坊

## 参与人员

- 领域专家（业务人员）
- 开发团队（技术实现）
- 领域驱动设计教练（引导流程）

## 所需材料

- 大幅白板或墙面空间
- 不同颜色的便签纸（至少 6 种颜色）
- 马克笔
- 投影或大屏（用于数字化工具）

## 便签颜色约定

| 颜色 | 含义 | 示例 |
|------|------|------|
| 橙色 | 领域事件（Domain Event） | OrderCreated, PaymentReceived |
| 蓝色 | 命令（Command） | CreateOrder, CancelOrder |
| 黄色 | 聚合（Aggregate） | Order, Customer, Payment |
| 紫色 | 策略/业务规则（Policy） | VIPDiscount, OverduePenalty |
| 粉色 | 外部系统 | PaymentGateway, ERP |
| 绿色 | 用户/角色（Actor） | Customer, Admin |
| 灰色 | 读模型（Read Model） | OrderListView, Dashboard |

## 工作坊步骤

### 步骤 1：识别领域事件（30-60 分钟）

从业务流程的起点开始，逐步添加所有已发生的、值得记录的事件。

规则：
- 事件名使用**过去时态**
- 按时间顺序从左到右排列
- 每个事件用一张橙色便签

示例（电商场景）：
```
OrderPlaced → PaymentReceived → InventoryReserved → OrderShipped → DeliveryConfirmed
```

### 步骤 2：识别触发事件的命令（15-30 分钟）

在每个事件左侧添加触发它的命令。

规则：
- 命令名使用**动词短语**
- 一个事件可能由多个命令触发
- 用箭头连接命令和事件

```
[CreateOrder] ──→ [OrderPlaced]
[PlaceOrderViaCart] ──→ [OrderPlaced]
```

### 步骤 3：分配到聚合（30-45 分钟）

找出处理每个命令、维护事件背后不变量的对象。

规则：
- 聚合是命令的处理者
- 一个命令只能由一个聚合处理
- 用黄色便签标记聚合

```
[CreateOrder] ──→ [OrderPlaced] ←── [Order聚合]
[CancelOrder]  ──→ [OrderCancelled] ←── [Order聚合]
```

### 步骤 4：识别业务策略（15-30 分钟）

添加条件性的业务规则。

规则：
- 策略是触发额外命令的条件
- 用紫色便签标记
- 连接到相关的事件或命令

```
[OrderPlaced] ──[if VIP customer]─→ [ApplyDiscount] ──→ [DiscountApplied]
```

### 步骤 5：识别外部系统（15 分钟）

标记与外部系统的交互点。

规则：
- 用粉色便签标记
- 放置在与外部系统交互的命令旁边

```
[PaymentGateway] ──→ [PaymentReceived]
```

### 步骤 6：识别读模型（15 分钟）

了解不同用户需要查看哪些信息。

规则：
- 用绿色便签标记读模型
- 放置在需要展示的事件下方

```
[OrderPlaced]
[OrderCancelled]
[OrderSummary] ← 读模型（运营后台展示）
```

## 产出物模板

### 聚合清单

| 聚合名 | 职责 | 关联事件 | 关联命令 |
|--------|------|---------|---------|
| Order | 管理订单生命周期 | OrderPlaced, OrderPaid, OrderShipped, OrderCancelled | CreateOrder, PayOrder, ShipOrder, CancelOrder |
| Customer | 管理客户信息和等级 | CustomerRegistered, LevelUpgraded | RegisterCustomer |
| Inventory | 管理库存 | InventoryReserved, InventoryReleased | ReserveInventory |

### 限界上下文候选

| 上下文名 | 包含聚合 | 核心能力 |
|----------|---------|---------|
| 订单上下文 | Order, OrderItem | 订单全生命周期管理 |
| 客户上下文 | Customer | 客户信息与等级管理 |
| 库存上下文 | Inventory, Stock | 库存实时管理 |
| 支付上下文 | Payment, Transaction | 支付流程管理 |

## 常见问题处理

**Q：两个聚合处理同一个命令怎么办？**
A：重新审视业务边界，可能需要拆分上下文或合并聚合。

**Q：发现很多跨聚合的事件流怎么办？**
A：这是正常的，通过领域事件异步交互。确保聚合间通过 ID 而非对象引用。

**Q：某些事件不知道属于哪个聚合？**
A：回到业务本质——哪个实体维护这些事件背后的不变量？
