---
name: sql-reflect
description: 快速定位 SQL 语句在 PHP/Laravel 代码中的触发位置，通过分析 SQL 结构反向追踪到具体的代码文件、方法和行号
version: 1.0.0
---

## 触发条件

当用户使用以下表述时触发此技能：
- "帮我查找一下这句 sql 语句是在哪个地方的代码触发的"
- "查询这个 SQL 代码位置"
- "这条 SQL 是从哪里调用的"
- "定位这条 SQL 的触发代码"
- "查找 SQL 触发位置"

## 执行流程

### 1. 提取关键信息

从 SQL 语句中提取：
- **主表名**：FROM 后的表名（如 `pk_transaction_meet_records`）
- **关联表名**：JOIN、EXISTS 子句中的表名
- **关键条件**：WHERE 中的特殊字段组合
- **查询特征**：特殊结构（如嵌套 EXISTS、特定字段组合）

### 2. 搜索代码位置

使用 grep 工具执行以下搜索（按优先级）：

1. **搜索表名**（最精确）
   - 搜索模式：`pk_表名`
   - 文件类型：`*.php`
   - 搜索范围：`app/`

2. **搜索模型类名**
   - 转换规则：去掉 `pk_` 前缀，转 PascalCase
   - 如：`pk_transaction_meet_records` → `TransactionMeetRecord`

3. **搜索特殊字段组合**
   - 提取 WHERE 条件中的 2-3 个特征字段
   - 搜索这些字段的组合出现位置

### 3. 分析搜索结果

对比 SQL 特征和代码：
- 字段匹配：SQL 中的字段是否在代码的 select/where 中出现
- 条件匹配：WHERE 条件是否与代码一致
- 结构匹配：JOIN/EXISTS 结构是否对应 whereHas/join 等
- 参数匹配：绑定参数的位置和数量

### 4. 定位关联关系

查找涉及的模型关联定义：
- 搜索 `function 关联名()` 在 Models 目录
- 分析 belongsTo/hasMany 等关联类型
- 确认外键字段

### 5. 追踪调用链路

从找到的代码位置向上追踪：
- 哪个 Controller 调用了这个 Service
- 哪个方法实例化了这个 Model
- 完整的调用路径

## 输出格式

```markdown
## SQL 语句触发位置分析

### 📍 触发代码位置

**文件路径：** `/path/to/file.php`

**方法：** `methodName`（第 X 行开始）

**具体代码段：** 第 X-Y 行

---

### 🔍 SQL 生成逻辑

这段代码通过 [Laravel Eloquent 特性] 生成：

```php
// 关键代码片段（10-20 行）
```

---

### 🔗 关联关系链

查询涉及的模型关联：

1. **`关联名`** - `模型类::关联方法()`（第 X 行）

---

### 📋 生成的 SQL 结构

```sql
-- SQL 结构说明
```

---

### 📂 调用链路

```
Controller.php:行号
  ↓ (调用说明)
Service.php:行号
  ↓
Model::query()
  ↓
最终 SQL
```

---

### 💡 使用场景

这个查询用于 [业务场景说明]
```

## 表名映射参考

| 表名 | 模型类 |
|------|--------|
| pk_transaction_meet_records | TransactionMeetRecord |
| pk_customer | Customers |
| pk_customer_card | CustomerCard |
| pk_order_offline | OrderOffline |
| pk_order_offline_refund_logs | OrderOfflineRefundLogs |
| pk_order_online | OrderOnline |
| pk_template_activity | TemplateActivity |
| pk_guide | StoreGuide |
| pk_store | Store |
| pk_customer_goods_attribute_tag | CustomerGoodsAttributeTag |
| pk_guide_customer | GuideCustomer |
| pk_promotion_goods | PromotionGoods |
| pk_order_goods_online | OrderGoodsOnline |
| pk_order_goods_online_records | OrderGoodsOnlineRecord |

## SQL 结构对应

| SQL 结构 | Laravel 写法 |
|---------|-------------|
| EXISTS (SELECT...) | whereHas() / whereExists() |
| LEFT JOIN | leftJoin() / with() |
| INNER JOIN | join() |
| BETWEEN ... AND ... | whereBetween() |
| IN (...) | whereIn() |
| NOT EXISTS | whereDoesntHave() |

## 特殊字段组合

| 字段组合 | 可能业务 |
|---------|---------|
| business_no + source_type + is_met | TransactionMeetRecord |
| order_no + refund_order_no + is_valid | OrderOfflineRefundLogs |
| customer_id + first_consume_time + second_consume_time | CustomerCard |
| guide_id + customer_id + relation_type | GuideCustomer |
| attribute_pid + attribute_id + num | CustomerGoodsAttributeTag |

## 注意事项

1. 优先使用精确搜索（完整表名），再使用模糊搜索
2. 注意表名前缀（pk_）和模型命名规则
3. 如果找到多个匹配位置，按匹配度排序并说明差异
4. SQL 中的 `?` 在代码中对应变量或请求参数
5. 某些 SQL 可能由多个代码位置生成，需列出所有可能
