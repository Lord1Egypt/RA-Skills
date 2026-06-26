# Store Order Query Skill

通过连接MySQL数据库实现 **查询店铺订单** 的 OpenClaw Skill。

该 Skill 会读取数据库配置信息，连接MySQL数据库进行订单数据查询，最后对数据进行呈现和分析。

## 功能特性

- 专为MySQL数据库设计
- 支持实际业务表结构（Order、OrderItems）
- 多种查询时间范围：今天、昨天、最近7天、最近30天、自定义日期
- 自动生成详细的 Markdown 分析报告
- 订单数据、商品销售、SKU分析全面覆盖

## 交互形态

1. 用户输入查询诉求（如："查询今天店铺订单"、"今天的订单怎么样"）
2. Agent 检查是否有配置文件，如无则引导用户配置数据库信息
3. Agent 执行查询脚本获取订单数据
4. Agent 执行分析脚本生成报告并展示给用户

## 快速开始

### 1. 配置数据库

复制 `config.example.json` 为 `config.json`，并修改数据库配置：

```bash
cp config.example.json config.json
```

编辑 `config.json`，填入你的MySQL数据库信息：

```json
{
  "database": {
    "type": "mysql",
    "host": "localhost",
    "port": 3306,
    "database": "shop_db",
    "user": "root",
    "password": "your_password"
  },
  "tables": {
    "orders": "Order",
    "order_items": "OrderItems"
  },
  "fields": {
    "orders": {
      "id": "orderSn",
      "created_at": "createdAt",
      "total_amount": "orderActualAmount",
      "payment_method": "payType",
      "status": "orderStatus"
    },
    "order_items": {
      "order_id": "orderSn",
      "product_name": "name",
      "sku": "sku",
      "quantity": "counts",
      "price": "actualPrice"
    }
  }
}
```

### 2. 测试数据库（可选）

如果你想快速测试，可以使用提供的示例数据库脚本：

```bash
mysql -u root -p < scripts/example_database.sql
```

这会创建 `Order` 和 `OrderItems` 表，并插入一些测试数据。

### 3. 查询订单

```bash
# 查询今天的订单
pnpm run query -- --date-range today

# 查询昨天的订单
pnpm run query -- --date-range yesterday

# 查询最近7天的订单
pnpm run query -- --date-range last7days

# 查询自定义日期范围
pnpm run query -- --date-range custom --start-date 2024-01-01 --end-date 2024-01-31
```

### 4. 生成分析报告

```bash
pnpm run analyze
```

**一键查询并分析：**

```bash
pnpm run query-today
```

报告将保存到 `output/order_report.md`。

## 生成的数据

1. **订单原始数据** (`output/orders_data.json`)
   - 符合查询条件的订单数据
   - 关联的商品信息

2. **分析报告** (`output/order_report.md`)
   - 总体概况：订单量、总金额、平均订单金额、商品总数
   - 支付方式分布
   - 订单状态分布
   - 热销商品 TOP 10
   - SKU 销售分析（尺码、颜色等）

## 目录结构

```
store-order-query/
├── SKILL.md                    # Skill 定义文件
├── README.md                   # 使用说明
├── package.json                # 依赖配置
├── tsconfig.json               # TypeScript 配置
├── config.example.json         # 配置文件示例
├── config.json                 # 实际配置文件（需自行创建）
├── src/
│   ├── index.ts                # 订单查询入口
│   └── analyze-orders.ts       # 数据分析入口
├── scripts/
│   └── example_database.sql   # 示例数据库脚本
└── output/                     # 输出目录（自动创建）
    ├── orders_data.json        # 订单原始数据
    └── order_report.md         # 分析报告
```

## 数据库表结构

### Order 表（订单表）

```sql
CREATE TABLE `Order` (
    `orderSn` VARCHAR(50) PRIMARY KEY COMMENT '订单号',
    `createdAt` DATETIME NOT NULL COMMENT '创建时间',
    `orderActualAmount` DECIMAL(10, 2) NOT NULL COMMENT '订单实际金额',
    `payType` VARCHAR(50) COMMENT '支付方式',
    `orderStatus` VARCHAR(20) COMMENT '订单状态',
    INDEX `idx_createdAt` (`createdAt`)
);
```

### OrderItems 表（订单商品表）

```sql
CREATE TABLE `OrderItems` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `orderSn` VARCHAR(50) NOT NULL COMMENT '订单号',
    `name` VARCHAR(200) NOT NULL COMMENT '商品名称',
    `sku` VARCHAR(100) COMMENT 'SKU',
    `counts` INT NOT NULL COMMENT '数量',
    `actualPrice` DECIMAL(10, 2) NOT NULL COMMENT '实际价格',
    INDEX `idx_orderSn` (`orderSn`)
);
```

## Scripts

| 命令 | 说明 |
|------|------|
| `pnpm run query` | 运行查询脚本 |
| `pnpm run analyze` | 运行分析脚本 |
| `pnpm run query-today` | 一键查询今天的订单并分析 |

## 技术栈

- **Node.js**: 运行环境（>= 18）
- **TypeScript**: 开发语言
- **mysql2**: MySQL 数据库驱动

## 注意事项

1. **数据库权限**：确保数据库用户有读取 Order 和 OrderItems 表的权限
2. **安全性**：配置文件包含敏感信息，请勿提交到公共仓库，已添加到 `.gitignore`
3. **日期字段**：确保 `createdAt` 字段是 DATETIME 类型，支持 `DATE()` 函数
4. **字段映射**：如果你的表结构不同，请修改 `config.json` 中的字段映射

## 常见问题

### Q: 数据库连接失败？

检查：
1. MySQL 服务是否启动
2. 配置文件中的用户名和密码是否正确
3. 数据库名称是否存在
4. 端口号是否正确（默认 3306）

### Q: 查询结果为空？

检查：
1. 日期范围是否正确
2. 数据库中是否有该时间段的数据
3. Order 表中 `createdAt` 字段是否有值

### Q: 字段不匹配错误？

检查 `config.json` 中的字段映射是否与实际表结构一致。

---

**作者**: liwentao
**仓库**: https://github.com/bondli/my-claw-skills.git
