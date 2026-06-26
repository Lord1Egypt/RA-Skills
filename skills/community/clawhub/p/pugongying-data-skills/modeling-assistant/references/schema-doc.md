---
name: schema-doc
description: |
  Schema文档生成器 - 自动生成数据表结构文档，包含字段说明、血缘关系、样例数据。
  当用户需要生成数据字典、表结构文档、数据血缘分析时触发。
  触发词：生成Schema文档、数据字典、表结构说明、血缘分析、数据地图。
argument: { description: "表名列表或数据库连接信息", required: true }
agent: general-purpose
allowed-tools: [Read, Grep, Glob, Edit, Write, Bash]
---

# Schema文档生成器

自动生成专业的数据表结构文档，包含字段说明、数据血缘、样例数据和质量概览。

## 工作流程

1. **元数据提取** - 读取表结构、字段信息、约束
2. **统计分析** - 计算字段分布、空值率、基数
3. **血缘识别** - 分析外键关系、字段依赖
4. **样例采集** - 提取代表性样例数据
5. **文档生成** - 输出Markdown/HTML格式的数据字典

## 输入格式

### 格式1：单表文档
```
/schema-doc 表名: users, 包含样例数据: 是
```

### 格式2：多表文档
```
/schema-doc 表名: users,orders,products, 生成数据血缘: 是
```

### 格式3：整库文档
```
/schema-doc 数据库: ecommerce, Schema: public, 排除表: temp_*,log_*
```

### 格式4：指定输出格式
```
/schema-doc 表名: orders, 输出格式: Markdown, 包含统计: 是
```

## 输出规范

### Markdown文档格式

```markdown
# 数据表: table_name

## 基本信息

| 属性 | 值 |
|------|-----|
| 表名 | table_name |
| 中文名 | 表中文名称 |
| 所属库 | database_name |
| 存储引擎 | PostgreSQL |
| 记录数 | 1,234,567 |
| 数据大小 | 256 MB |
| 索引大小 | 128 MB |
| 创建时间 | 2024-01-15 |
| 最后更新 | 2025-03-17 |
| 负责人 | data-team@company.com |

## 字段说明

| 序号 | 字段名 | 数据类型 | 可空 | 默认值 | 主键 | 外键 | 索引 | 中文名 | 业务说明 |
|------|--------|----------|------|--------|------|------|------|--------|----------|
| 1 | id | BIGINT | NO | auto | PK | - | ✅ | ID | 主键，自增 |
| 2 | user_id | BIGINT | NO | - | - | FK | ✅ | 用户ID | 关联users表 |
| 3 | status | VARCHAR(20) | NO | 'pending' | - | - | ✅ | 状态 | 订单状态 |

## 索引信息

| 索引名 | 类型 | 字段 | 说明 |
|--------|------|------|------|
| pk_orders | PRIMARY | id | 主键索引 |
| idx_user_id | BTREE | user_id | 用户查询 |

## 约束信息

| 约束名 | 类型 | 字段 | 说明 |
|--------|------|------|------|
| pk_orders | PRIMARY KEY | id | 主键约束 |
| fk_orders_user | FOREIGN KEY | user_id → users.id | 外键约束 |

## 数据血缘

### 上游依赖
- users.user_id (1:N)
- products.product_id (N:M via order_items)

### 下游消费
- report_daily_sales (订单ID)
- user_order_stats (用户ID)

## 样例数据

| id | user_id | total_amount | status | created_at |
|----|---------|--------------|--------|------------|
| 1 | 10001 | 299.99 | paid | 2025-03-17 10:00:00 |
| 2 | 10002 | 159.00 | pending | 2025-03-17 10:05:00 |

## 数据统计

### 字段分布

#### status 字段分布
| 值 | 数量 | 占比 |
|----|------|------|
| completed | 890,000 | 72.1% |
| paid | 234,567 | 19.0% |
| pending | 110,000 | 8.9% |

### 空值统计
| 字段 | 空值数 | 空值率 |
|------|--------|--------|
| paid_at | 234,567 | 19.0% |
| ship_at | 890,000 | 72.1% |

## 质量评分

| 维度 | 评分 | 状态 |
|------|------|------|
| 完整性 | 98.5% | 🟢 |
| 唯一性 | 100% | 🟢 |
| 有效性 | 99.8% | 🟢 |
| **综合** | **99.4%** | 🟢 |

## 更新日志

| 时间 | 操作 | 内容 |
|------|------|------|
| 2025-03-01 | 新增字段 | 添加discount_amount字段 |
| 2025-02-15 | 修改索引 | 优化idx_created_at索引 |
```

### HTML文档格式

生成可交互的HTML数据字典，包含：
- 搜索功能
- 字段筛选
- 血缘关系图
- 数据预览

## 文档组件

### 1. 表基础信息
- 表名、中文名、描述
- 存储信息（记录数、大小）
- 生命周期信息（创建时间、更新时间）
- 责任人/团队

### 2. 字段详情表
- 字段名、数据类型、可空性
- 约束（PK/FK/Default）
- 索引信息
- 中文名、业务说明
- 示例值

### 3. 血缘关系图
```
[users] ──1:N──▶ [orders] ──1:N──▶ [order_items] ◀──N:1── [products]
                              │
                              ▼
                         [payments]
```

### 4. 数据分布
- 枚举字段的分布统计
- 数值字段的分位数
- 时间字段的时间分布

### 5. 质量概览
- 各维度质量评分
- 已知问题清单
- 改进建议

## 字段语义识别

通过字段名自动识别业务含义：

| 字段名模式 | 识别类型 | 自动添加的说明 |
|------------|----------|----------------|
| id | 主键 | 主键，唯一标识 |
| *_id | 外键 | 关联{表名}表 |
| created_at | 创建时间 | 记录创建时间 |
| updated_at | 更新时间 | 最后更新时间 |
| deleted_at | 删除标记 | 软删除时间戳 |
| status | 状态 | 业务状态字段 |
| type | 类型 | 分类类型 |
| amount/price | 金额 | 单位：元 |
| count/qty | 数量 | 计数/数量 |
| email | 邮箱 | 邮箱地址 |
| phone/mobile | 手机号 | 手机号码 |
| name | 名称 | 名称/标题 |
| desc/description | 描述 | 详细描述 |
| remark/comment | 备注 | 备注信息 |
| is_*/has_* | 布尔 | 是否标志 |

## 数据血缘识别

### 外键关系
```sql
-- 查找外键约束
SELECT
    tc.table_name,
    kcu.column_name,
    ccu.table_name AS foreign_table,
    ccu.column_name AS foreign_column
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
    ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage ccu
    ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY';
```

### 字段级血缘
分析SQL查询中的字段依赖关系。

## 样例数据提取

智能提取有代表性的样例：

```sql
-- 策略1: 最近N条
SELECT * FROM table ORDER BY created_at DESC LIMIT 5;

-- 策略2: 各状态一条
SELECT DISTINCT ON (status) * FROM table;

-- 策略3: 随机抽样
SELECT * FROM table ORDER BY RANDOM() LIMIT 5;

-- 策略4: 边界值
SELECT * FROM table WHERE amount = (SELECT MAX(amount) FROM table);
```

## 输出选项

| 选项 | 说明 | 默认 |
|------|------|------|
| 包含样例数据 | 输出样例数据 | 是 |
| 包含统计信息 | 字段分布统计 | 是 |
| 包含血缘关系 | 上下游依赖 | 是 |
| 包含质量评分 | 质量检查结果 | 否 |
| 输出格式 | Markdown/HTML | Markdown |
| 语言 | 中文/英文 | 中文 |

## 批量生成

为多表生成统一格式的数据字典：

```markdown
# 数据仓库数据字典

## 表清单

| 表名 | 中文名 | 记录数 | 质量评分 |
|------|--------|--------|----------|
| dim_users | 用户维度表 | 1M | 99.5% 🟢 |
| dim_products | 商品维度表 | 100K | 98.2% 🟢 |
| fact_orders | 订单事实表 | 10M | 97.8% 🟢 |

## 详细说明

### dim_users
...

### dim_products
...

### fact_orders
...
```

## 当前生成任务

$ARGUMENTS

---

**生成文档时**：
1. 提取表结构元数据
2. 识别字段业务语义
3. 统计字段分布和空值
4. 分析外键血缘关系
5. 提取代表性样例数据
6. 生成格式化的文档
7. 如需要，包含质量评分
