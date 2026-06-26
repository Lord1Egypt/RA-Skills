# 示例：电商数据质量管理完整流程

## 场景描述

为电商核心表（users, orders, products）建立完整的数据质量管理体系。

---

## 阶段1：质量规则生成

### 1.1 users表规则生成

**输入**：
```
/dq-rule-gen
表名：users
字段：
- id (BIGINT, PK): 用户ID
- email (VARCHAR(100)): 邮箱，业务必填
- phone (VARCHAR(20)): 手机号，业务必填
- username (VARCHAR(50)): 用户名，必填，唯一
- status (VARCHAR(20)): 状态，枚举值：active/inactive/banned
- created_at (TIMESTAMP): 创建时间
- last_login_at (TIMESTAMP): 最后登录时间，可空
```

**输出**：

```yaml
# users表质量规则集
table: users
generated_at: 2025-03-17 10:00:00
total_rules: 10

rules:
  # ========== 完整性规则 ==========
  - rule_id: COMP_001
    name: id_非空检查
    dimension: 完整性
    severity: 高
    column: id
    condition: id IS NULL
    threshold: 0
    sql: SELECT COUNT(*) FROM users WHERE id IS NULL

  - rule_id: COMP_002
    name: email_非空检查
    dimension: 完整性
    severity: 高
    column: email
    condition: email IS NULL OR email = ''
    threshold: 0
    sql: SELECT COUNT(*) FROM users WHERE email IS NULL OR email = ''

  - rule_id: COMP_003
    name: phone_非空检查
    dimension: 完整性
    severity: 高
    column: phone
    condition: phone IS NULL OR phone = ''
    threshold: 0
    sql: SELECT COUNT(*) FROM users WHERE phone IS NULL OR phone = ''

  - rule_id: COMP_004
    name: username_非空检查
    dimension: 完整性
    severity: 高
    column: username
    condition: username IS NULL OR username = ''
    threshold: 0
    sql: SELECT COUNT(*) FROM users WHERE username IS NULL OR username = ''

  - rule_id: COMP_005
    name: status_非空检查
    dimension: 完整性
    severity: 高
    column: status
    condition: status IS NULL OR status = ''
    threshold: 0
    sql: SELECT COUNT(*) FROM users WHERE status IS NULL OR status = ''

  # ========== 唯一性规则 ==========
  - rule_id: UNIQ_001
    name: id_唯一性检查
    dimension: 唯一性
    severity: 高
    column: id
    sql: SELECT id, COUNT(*) FROM users GROUP BY id HAVING COUNT(*) > 1

  - rule_id: UNIQ_002
    name: email_唯一性检查
    dimension: 唯一性
    severity: 高
    column: email
    sql: SELECT email, COUNT(*) FROM users GROUP BY email HAVING COUNT(*) > 1

  - rule_id: UNIQ_003
    name: phone_唯一性检查
    dimension: 唯一性
    severity: 高
    column: phone
    sql: SELECT phone, COUNT(*) FROM users WHERE phone IS NOT NULL GROUP BY phone HAVING COUNT(*) > 1

  - rule_id: UNIQ_004
    name: username_唯一性检查
    dimension: 唯一性
    severity: 高
    column: username
    sql: SELECT username, COUNT(*) FROM users GROUP BY username HAVING COUNT(*) > 1

  # ========== 有效性规则 ==========
  - rule_id: VALID_001
    name: email_格式检查
    dimension: 有效性
    severity: 中
    column: email
    condition: email NOT LIKE '%@%.%' OR email LIKE '%@%@%' OR email LIKE '%..%'
    threshold: 5
    sql: |
      SELECT COUNT(*) FROM users
      WHERE email NOT LIKE '%@%.%'
         OR email LIKE '%@%@%'
         OR email LIKE '%..%'

  - rule_id: VALID_002
    name: phone_格式检查
    dimension: 有效性
    severity: 中
    column: phone
    condition: phone NOT LIKE '1__________'
    threshold: 5
    sql: SELECT COUNT(*) FROM users WHERE phone NOT LIKE '1__________'

  - rule_id: VALID_003
    name: status_枚举检查
    dimension: 有效性
    severity: 高
    column: status
    condition: status NOT IN ('active', 'inactive', 'banned')
    threshold: 0
    sql: |
      SELECT status, COUNT(*)
      FROM users
      WHERE status NOT IN ('active', 'inactive', 'banned')
      GROUP BY status

  - rule_id: VALID_004
    name: created_at_范围检查
    dimension: 有效性
    severity: 中
    column: created_at
    condition: created_at > NOW() OR created_at < '2020-01-01'
    threshold: 0
    sql: SELECT COUNT(*) FROM users WHERE created_at > NOW() OR created_at < '2020-01-01'
```

### 1.2 orders表规则生成

**输入**：
```
/dq-rule-gen
表名：orders
字段：
- order_id (BIGINT, PK): 订单ID
- user_id (BIGINT, FK): 用户ID，关联users.id
- order_no (VARCHAR(32)): 订单编号，业务唯一
- total_amount (DECIMAL(12,2)): 订单金额
- status (VARCHAR(20)): 状态(pending/paid/shipped/completed/cancelled/refunded)
- created_at (TIMESTAMP): 创建时间
- paid_at (TIMESTAMP): 支付时间，可空
- shipped_at (TIMESTAMP): 发货时间，可空
```

**生成规则**：
- 完整性规则：5条（order_id, user_id, order_no, total_amount, status必填）
- 唯一性规则：2条（order_id, order_no唯一）
- 有效性规则：4条（金额范围、状态枚举、时间有效性）
- 一致性规则：2条（时间顺序、金额正数）
- **总计：13条规则**

---

## 阶段2：质量检查执行

### 2.1 执行users表检查

**输入**：
```
/dq-check 对users表执行全量质量检查
```

**输出**：

```
============================================================
数据质量检查报告 - users表
============================================================
检查时间: 2025-03-17 10:30:00
记录总数: 1,000,000
规则数量: 13
执行耗时: 12.45s

------------------------------------------------------------
【完整性检查】5条规则
------------------------------------------------------------
✅ COMP_001 id_非空检查            通过  (0/1000000)
✅ COMP_002 email_非空检查          通过  (0/1000000)
✅ COMP_003 phone_非空检查          通过  (0/1000000)
✅ COMP_004 username_非空检查       通过  (0/1000000)
✅ COMP_005 status_非空检查         通过  (0/1000000)
维度得分: 100.0/100 🟢

------------------------------------------------------------
【唯一性检查】4条规则
------------------------------------------------------------
✅ UNIQ_001 id_唯一性检查           通过  (0重复)
✅ UNIQ_002 email_唯一性检查        通过  (0重复)
⚠️ UNIQ_003 phone_唯一性检查        警告  (23条重复)
   重复号码: 138****1234(2条), 139****5678(2条), ...
✅ UNIQ_004 username_唯一性检查     通过  (0重复)
维度得分: 99.8/100 🟢

------------------------------------------------------------
【有效性检查】4条规则
------------------------------------------------------------
✅ VALID_001 email_格式检查         通过  (0/1000000)
⚠️ VALID_002 phone_格式检查         警告  (156条异常)
   异常样例: '1381234567'(少一位), '021-12345678'(固话), ''
✅ VALID_003 status_枚举检查        通过  (0异常)
✅ VALID_004 created_at_范围检查    通过  (0异常)
维度得分: 99.8/100 🟢

------------------------------------------------------------
【综合评分】
------------------------------------------------------------
完整性:   100.0/100  🟢
唯一性:    99.8/100  🟢
有效性:    99.8/100  🟢
一致性:   100.0/100  🟢 (无检查规则)
及时性:   100.0/100  🟢 (无检查规则)
------------------------------------------------------------
综合评分:  99.9/100  🟢 优秀
质量等级:  🟢 优秀 (符合预期)
------------------------------------------------------------

【问题汇总】
- 严重问题 (高): 0个
- 警告问题 (中): 2个
- 建议优化 (低): 0个

【行动建议】
1. 【中优先级】处理手机号重复问题 (23条)
   重复原因分析：可能是测试数据或家庭成员共用号码
   查看SQL: SELECT phone, COUNT(*), STRING_AGG(id::text, ',')
            FROM users GROUP BY phone HAVING COUNT(*) > 1

2. 【中优先级】处理手机号格式异常 (156条)
   异常类型：
   - 位数不足：89条
   - 包含非手机号：45条
   - 为空字符串：22条

   修复建议：
   - 位数不足的：人工核实补全
   - 固话号码：考虑单独存储或标记
   - 空字符串：更新为NULL或补充

【历史趋势】
vs 上周:
- 完整性: 100.0% (→ 持平)
- 唯一性: 99.8% (↑ 0.1%) - 修复了15条重复
- 有效性: 99.8% (→ 持平)
- 综合评分: 99.9% (↑ 0.02%)
```

### 2.2 执行orders表检查

**输入**：
```
/dq-check 对orders表执行全量质量检查
```

**关键发现**：
- 完整性：99.2%（有8000条paid_at为空，但这是正常的未支付订单）
- 唯一性：100%
- 有效性：99.9%
- 一致性：99.95%（3条记录paid_at < created_at，数据异常）

**综合评分**：99.7/100 🟢

---

## 阶段3：Schema文档生成

### 3.1 生成users表数据字典

**输入**：
```
/schema-doc 生成users表的完整数据字典，包含样例数据、血缘关系、质量评分
```

**输出**：

```markdown
# 数据表: users

## 基本信息

| 属性 | 值 |
|------|-----|
| 表名 | users |
| 中文名 | 用户表 |
| 所属库 | ecommerce |
| 存储引擎 | PostgreSQL 15 |
| 记录数 | 1,000,000 |
| 数据大小 | 256 MB |
| 索引大小 | 128 MB |
| 创建时间 | 2024-01-15 |
| 最后更新 | 2025-03-17 |
| 负责人 | data-team@company.com |
| 质量评分 | 99.9% 🟢 |

## 字段说明

| 序号 | 字段名 | 数据类型 | 可空 | 默认值 | 主键 | 索引 | 中文名 | 业务说明 |
|------|--------|----------|------|--------|------|------|--------|----------|
| 1 | id | BIGINT | NO | auto | PK | ✅ | 用户ID | 主键，自增 |
| 2 | email | VARCHAR(100) | NO | - | - | ✅ | 邮箱 | 用户邮箱，唯一 |
| 3 | phone | VARCHAR(20) | NO | - | - | ✅ | 手机号 | 用户手机号 |
| 4 | username | VARCHAR(50) | NO | - | - | ✅ | 用户名 | 用户昵称，唯一 |
| 5 | status | VARCHAR(20) | NO | 'active' | - | ✅ | 状态 | active/inactive/banned |
| 6 | created_at | TIMESTAMP | NO | NOW() | - | ✅ | 创建时间 | 注册时间 |
| 7 | last_login_at | TIMESTAMP | YES | - | - | - | 最后登录 | 最近一次登录时间 |

## 索引信息

| 索引名 | 类型 | 字段 | 说明 |
|--------|------|------|------|
| pk_users | PRIMARY | id | 主键索引 |
| uk_users_email | UNIQUE | email | 邮箱唯一 |
| uk_users_username | UNIQUE | username | 用户名唯一 |
| uk_users_phone | UNIQUE | phone | 手机号唯一 |
| idx_users_status | BTREE | status | 状态筛选 |
| idx_users_created | BTREE | created_at | 时间筛选 |

## 约束信息

| 约束名 | 类型 | 字段 | 说明 |
|--------|------|------|------|
| pk_users | PRIMARY KEY | id | 主键约束 |
| uk_users_email | UNIQUE | email | 邮箱唯一约束 |
| uk_users_username | UNIQUE | username | 用户名唯一约束 |
| chk_status | CHECK | status | 状态值检查 |

## 数据血缘

### 上游依赖
无（users是核心维度表）

### 下游消费
| 表名 | 关联字段 | 关系类型 | 说明 |
|------|----------|----------|------|
| orders | user_id | 1:N | 用户订单 |
| user_profiles | user_id | 1:1 | 用户扩展信息 |
| user_stats | user_id | 1:1 | 用户统计 |
| login_logs | user_id | 1:N | 登录日志 |
| report_daily_active | user_id | N:1 | 日活报表 |

## 样例数据

| id | email | phone | username | status | created_at | last_login_at |
|----|-------|-------|----------|--------|------------|---------------|
| 1 | user1@example.com | 138****1234 | 用户001 | active | 2025-03-17 10:00:00 | 2025-03-17 09:30:00 |
| 2 | user2@example.com | 139****5678 | UserTwo | active | 2025-03-17 09:55:00 | 2025-03-17 09:00:00 |
| 3 | user3@example.com | 137****9012 | 用户_3 | inactive | 2025-03-16 15:20:00 | 2025-03-10 08:00:00 |

## 数据统计

### status 分布
| 值 | 数量 | 占比 |
|----|------|------|
| active | 850,000 | 85.0% |
| inactive | 140,000 | 14.0% |
| banned | 10,000 | 1.0% |

### 创建时间分布
| 时间段 | 新增用户数 |
|--------|------------|
| 本月 | 50,000 |
| 上月 | 45,000 |
| 近3月 | 140,000 |
| 今年 | 400,000 |

### 空值统计
| 字段 | 空值数 | 空值率 |
|------|--------|--------|
| last_login_at | 200,000 | 20.0% |
| 其他字段 | 0 | 0% |

## 质量概览

| 维度 | 评分 | 状态 | 问题数 |
|------|------|------|--------|
| 完整性 | 100.0% | 🟢 | 0 |
| 唯一性 | 99.8% | 🟢 | 23 |
| 有效性 | 99.8% | 🟢 | 156 |
| **综合** | **99.9%** | 🟢 | 179 |

## 更新日志

| 时间 | 操作 | 内容 |
|------|------|------|
| 2025-03-01 | 新增字段 | 添加last_login_at字段 |
| 2025-02-15 | 新增索引 | 优化idx_users_created索引 |
| 2025-01-10 | 约束变更 | 添加status字段CHECK约束 |
```

---

## 完整工作流程总结

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
电商数据质量管理流程
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

阶段1: 规则生成 (30分钟)
├─ users表: 13条规则
├─ orders表: 13条规则
└─ products表: 10条规则

阶段2: 质量检查 (15分钟)
├─ users表检查: 99.9分 🟢
├─ orders表检查: 99.7分 🟢
└─ products表检查: 99.5分 🟢

阶段3: 文档输出 (20分钟)
├─ users数据字典: 完成
├─ orders数据字典: 完成
└─ 整体质量报告: 完成

总耗时: 约65分钟
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

产出物:
✅ 36条质量检查规则
✅ 3份数据字典文档
✅ 1份综合质量报告
✅ 5个待修复问题清单
```

---

## 持续监控建议

### 每日检查
```bash
# 快速检查核心表
/dq-check users 快速检查
/dq-check orders 快速检查
```

### 每周检查
```bash
# 全量检查所有表
/dq-check users 全量检查
/dq-check orders 全量检查
/dq-check products 全量检查

# 生成周报
/dq-assistant 生成本周数据质量周报
```

### 每月检查
```bash
# 更新Schema文档
/schema-doc users,orders,products --include-quality

# 质量趋势分析
/dq-assistant 分析近3个月质量趋势
```
