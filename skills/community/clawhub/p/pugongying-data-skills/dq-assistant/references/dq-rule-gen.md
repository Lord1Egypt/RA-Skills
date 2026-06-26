---
name: dq-rule-gen
description: |
  数据质量规则生成器 - 基于表结构自动生成数据质量检查规则。
  当用户需要为数据表生成质量检查规则、建立数据质量监控体系时触发。
  触发词：生成质量规则、数据质量检查规则、自动规则生成、表质量监控。
argument: { description: "表名或表结构描述（包含字段名、类型、业务含义）", required: true }
agent: general-purpose
allowed-tools: [Read, Grep, Glob, Edit, Write, Bash]
---

# 数据质量规则生成器

基于表结构和业务信息，自动生成全面的数据质量检查规则。

## 工作流程

1. **表结构解析** - 提取字段名、数据类型、约束信息
2. **业务语义识别** - 识别字段业务含义（邮箱、手机号、状态等）
3. **规则生成** - 为每个字段生成适用的检查规则
4. **规则编排** - 组织成可执行的SQL检查脚本

## 输入格式

用户可以提供：

### 格式1：直接描述
```
表名：users
字段：
- id (BIGINT, PK): 用户ID
- email (VARCHAR): 邮箱
- phone (VARCHAR): 手机号
- status (VARCHAR): 状态(active/inactive/banned)
- created_at (TIMESTAMP): 创建时间
```

### 格式2：指定数据库表
```
数据库：PostgreSQL
表名：orders
Schema：public
```

### 格式3：DDL语句
```sql
CREATE TABLE products (
    id BIGINT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    price DECIMAL(10,2),
    category_id BIGINT,
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);
```

## 输出规范

### 规则输出格式

```yaml
# 数据质量规则集
table: table_name
generated_at: YYYY-MM-DD HH:MM:SS
total_rules: N

rules:
  - rule_id: COMP_001
    name: 字段名_必填检查
    dimension: 完整性
    severity: 高
    column: column_name
    rule_type: 非空检查
    condition: column_name IS NULL
    threshold: 0
    sql: |
      SELECT COUNT(*) as violation_count
      FROM table_name
      WHERE column_name IS NULL

  - rule_id: VALID_001
    name: 字段名_格式检查
    dimension: 有效性
    severity: 中
    column: column_name
    rule_type: 格式检查
    condition: "column_name NOT LIKE '%@%.%'"
    threshold: 5
    sql: |
      SELECT COUNT(*) as violation_count
      FROM table_name
      WHERE column_name NOT LIKE '%@%.%'
```

### SQL检查脚本输出

```sql
-- ============================================
-- 数据质量检查规则集
-- 目标表: table_name
-- 生成时间: YYYY-MM-DD
-- 规则数量: N条
-- ============================================

-- 规则1: [规则名称]
-- 维度: [完整性/唯一性/有效性/一致性]
-- 严重程度: [高/中/低]
INSERT INTO data_quality_checks (check_id, check_name, ...)
SELECT
    'RULE_001' as check_id,
    '规则名称' as check_name,
    '完整性' as dimension,
    COUNT(*) as violation_count,
    ...
FROM table_name
WHERE condition;

-- 汇总报告
SELECT
    check_id,
    check_name,
    dimension,
    violation_count,
    CASE
        WHEN violation_count = 0 THEN '🟢 通过'
        WHEN violation_count <= threshold THEN '🟡 警告'
        ELSE '🔴 失败'
    END as status
FROM data_quality_checks
WHERE check_date = CURRENT_DATE;
```

## 规则生成策略

### 按字段类型生成

| 字段类型 | 自动生成的规则 |
|----------|----------------|
| ID/主键 | 唯一性检查、非空检查 |
| 邮箱 | 格式检查、唯一性检查 |
| 手机号 | 格式检查、长度检查 |
| 状态/枚举 | 枚举值检查、非空检查 |
| 金额/价格 | 范围检查（>0）、精度检查 |
| 数量 | 范围检查（>=0）、整数检查 |
| 日期时间 | 范围检查（未来/过去）、格式检查 |
| 外键ID | 关联存在性检查、非空检查 |
| 文本描述 | 长度检查、空值检查 |
| JSON/XML | 格式有效性检查 |

### 按业务语义生成

通过字段名识别业务类型：

| 字段名模式 | 识别的业务类型 | 生成的规则 |
|------------|----------------|------------|
| email/e_mail | 邮箱 | 邮箱格式、唯一性 |
| phone/mobile/tel | 手机号 | 手机号格式、唯一性 |
| status/state | 状态 | 枚举值有效性 |
| amount/price/fee | 金额 | 非负、精度、范围 |
| count/num/qty | 数量 | 非负、整数 |
| date/time/at | 日期时间 | 范围、格式 |
| id/user_id/order_id | ID | 唯一性、关联存在性 |
| name/title | 名称 | 非空、长度 |
| is_*/has_* | 布尔标志 | 0/1有效性 |
| url/link | URL | 格式检查 |
| ip | IP地址 | 格式检查 |

## 规则维度分类

### 完整性规则 (COMP_*)
- 非空检查
- 默认值检查
- 记录完整性

### 唯一性规则 (UNIQ_*)
- 主键唯一性
- 业务键唯一性
- 组合唯一性

### 有效性规则 (VALID_*)
- 格式检查（正则）
- 范围检查
- 枚举值检查
- 类型检查
- 关联存在性

### 一致性规则 (CONS_*)
- 时间顺序
- 金额平衡
- 状态逻辑

### 及时性规则 (TIME_*)
- 数据新鲜度
- 延迟检查

## 严重程度定义

| 级别 | 定义 | 阈值建议 | 响应时间 |
|------|------|----------|----------|
| 🔴 高 | 核心业务字段，影响数据可用性 | 0% | 立即修复 |
| 🟡 中 | 重要业务字段，影响数据质量 | <5% | 本周修复 |
| 🟢 低 | 一般字段，轻微影响 | <10% | 择机修复 |

## 使用示例

### 示例1：电商订单表

**输入**：
```
为orders表生成质量检查规则：
- order_id (BIGINT, PK): 订单ID
- user_id (BIGINT, FK): 用户ID
- order_no (VARCHAR): 订单编号
- total_amount (DECIMAL): 订单金额
- status (VARCHAR): 状态(pending/paid/shipped/completed/cancelled)
- created_at (TIMESTAMP): 创建时间
- paid_at (TIMESTAMP): 支付时间
```

**输出**：
```yaml
rules:
  # 完整性规则
  - rule_id: COMP_001
    name: order_id_非空检查
    dimension: 完整性
    severity: 高
    ...

  - rule_id: COMP_002
    name: user_id_非空检查
    dimension: 完整性
    severity: 高
    ...

  # 唯一性规则
  - rule_id: UNIQ_001
    name: order_id_唯一性检查
    dimension: 唯一性
    severity: 高
    ...

  - rule_id: UNIQ_002
    name: order_no_唯一性检查
    dimension: 唯一性
    severity: 高
    ...

  # 有效性规则
  - rule_id: VALID_001
    name: total_amount_范围检查
    dimension: 有效性
    severity: 高
    condition: total_amount <= 0 OR total_amount > 99999999
    ...

  - rule_id: VALID_002
    name: status_枚举检查
    dimension: 有效性
    severity: 高
    condition: status NOT IN ('pending','paid','shipped','completed','cancelled')
    ...

  # 一致性规则
  - rule_id: CONS_001
    name: 时间顺序一致性
    dimension: 一致性
    severity: 中
    condition: paid_at < created_at
    ...
```

## 当前任务

$ARGUMENTS

---

**生成规则时**：
1. 首先确认表结构和字段理解正确
2. 为每个字段生成适用的检查规则
3. 按维度组织规则（完整性/唯一性/有效性/一致性）
4. 输出YAML格式的规则定义和可执行的SQL脚本
5. 提供规则优先级建议
