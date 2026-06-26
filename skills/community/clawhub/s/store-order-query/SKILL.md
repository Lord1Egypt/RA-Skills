---
name: store-order-query
description: query store order information from database
---

# Store Order Query Skill

## 技能描述

这是一个通过连接MySQL数据库查询店铺订单的 Skill。当用户询问店铺订单情况时(如"查询今天店铺订单"、"今天的订单怎么样"、"店铺经营情况"),使用此 Skill 连接数据库查询订单数据,并生成分析报告。

## 使用场景

- 用户想查询特定时间段的订单数据
- 用户想了解店铺经营状况
- 用户想分析订单中的商品销售情况
- 用户想查看支付方式分布

## 工作流程

### step1. 检查配置文件

首先检查是否存在数据库配置文件 `~/openclaw-skill-data/store-order-query/config.json`。

**如果配置文件不存在**,需要询问用户以下信息:
- MySQL数据库主机地址
- 数据库端口（默认3306）
- 数据库名称
- 数据库用户名
- 数据库密码

然后基于 `config.example.json` 创建 `config.json` 文件。

### step2. 解析用户查询意图

从用户的查询中提取:
- **时间范围**: 今天、昨天、最近7天、最近30天等
- **查询维度**: 订单量、金额、商品、支付方式等

如果用户说"今天",则查询当天的订单数据。

### step3. 执行查询脚本

调用以下命令查询订单数据，传递参数：
- `--date-range`: 时间范围 (today/yesterday/last7days/last30days 或 custom)
- `--start-date`: 开始日期 (YYYY-MM-DD 格式，可选)
- `--end-date`: 结束日期 (YYYY-MM-DD 格式，可选)

```
node dist/index.js --date-range today
```

脚本会：
1. 读取配置文件连接MySQL数据库
2. 查询Order表获取订单数据
3. 根据订单号查询OrderItems表获取商品信息
4. 将数据保存到 `~/openclaw-skill-data/store-order-query/orders_data.json`

### step4. 分析数据并生成报告

调用以下命令分析订单数据并生成报告：

```
node dist/analyze-orders.js
```

脚本会：
1. 读取 `~/openclaw-skill-data/store-order-query/orders_data.json`
2. 进行数据分析（订单量、总金额、支付方式分布、商品分析等）
3. 生成 Markdown 格式的报告保存到 `~/openclaw-skill-data/store-order-query/order_report.md`

### 5. 呈现报告

读取生成的报告文件,向用户展示分析结果。

## 配置文件格式

`~/openclaw-skill-data/store-order-query/config.json` 示例:

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

## 数据库表结构

### Order 表（订单表）

| 字段 | 类型 | 说明 |
|------|------|------|
| orderSn | VARCHAR(50) | 订单号(主键) |
| createdAt | DATETIME | 创建时间 |
| orderActualAmount | DECIMAL(10,2) | 订单实际金额 |
| payType | VARCHAR(50) | 支付方式 |
| orderStatus | VARCHAR(20) | 订单状态 |

### OrderItems 表（订单商品表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 主键ID |
| orderSn | VARCHAR(50) | 订单号(外键) |
| name | VARCHAR(200) | 商品名称 |
| sku | VARCHAR(100) | SKU |
| counts | INT | 数量 |
| actualPrice | DECIMAL(10,2) | 实际价格 |

## 注意事项

1. 确保已在根目录安装依赖：`pnpm install`
2. 配置文件包含敏感信息，不要将其提交到公共仓库
3. 首次使用时需要配置数据库信息
4. 确保MySQL数据库用户有读取Order和OrderItems表的权限
5. 生成的报告会保存在 output 目录中,可以重复查看

## 错误处理

- 如果数据库连接失败,提示用户检查配置信息
- 如果查询结果为空,提示用户该时间段没有订单数据
- 如果表或字段不存在,提示用户检查配置文件中的字段映射
