# 数据质量检查标准与规范

## 目录

1. [数据质量维度](#数据质量维度)
2. [数据质量规则库](#数据质量规则库)
3. [评分标准](#评分标准)
4. [检查SQL生成规范](#检查sql生成规范)
5. [常见问题模式](#常见问题模式)

---

## 数据质量维度

### 1. 完整性 (Completeness)

**定义**：数据是否存在缺失值

**检查指标**：
| 指标 | 说明 | 阈值建议 |
|------|------|----------|
| 空值率 | 字段NULL值占比 | < 5% |
| 填充率 | 字段有值记录占比 | > 95% |
| 必填字段缺失 | 业务必填字段的空值 | 0% |
| 记录完整性 | 必填表记录是否完整 | 100% |

**常见检查**：
```sql
-- 空值率检查
SELECT
    column_name,
    COUNT(*) as total_rows,
    COUNT(column_name) as non_null_rows,
    ROUND(COUNT(column_name) * 100.0 / COUNT(*), 2) as fill_rate
FROM table_name;

-- 必填字段缺失检查
SELECT COUNT(*) as missing_count
FROM table_name
WHERE required_column IS NULL;
```

---

### 2. 唯一性 (Uniqueness)

**定义**：数据记录或字段是否存在重复

**检查指标**：
| 指标 | 说明 | 阈值建议 |
|------|------|----------|
| 主键唯一性 | 主键字段无重复 | 100% |
| 业务键唯一性 | 业务唯一字段无重复 | 100% |
| 重复记录率 | 完全重复记录占比 | 0% |

**常见检查**：
```sql
-- 主键重复检查
SELECT primary_key, COUNT(*) as cnt
FROM table_name
GROUP BY primary_key
HAVING COUNT(*) > 1;

-- 完全重复记录检查
SELECT column1, column2, column3, COUNT(*) as cnt
FROM table_name
GROUP BY column1, column2, column3
HAVING COUNT(*) > 1;
```

---

### 3. 有效性 (Validity)

**定义**：数据是否符合预定义的格式、类型、范围规则

**检查类型**：
| 类型 | 说明 | 示例 |
|------|------|------|
| 格式有效性 | 字符串符合格式要求 | 邮箱、手机号、日期格式 |
| 范围有效性 | 数值在合理范围内 | 年龄在0-150之间 |
| 枚举有效性 | 值在预定义集合中 | 状态字段只能是active/inactive |
| 类型有效性 | 数据类型正确 | 数字字段不含字母 |
| 关联有效性 | 外键关联存在 | user_id在users表中存在 |

**常见检查**：
```sql
-- 格式有效性（邮箱）
SELECT COUNT(*) as invalid_count
FROM users
WHERE email NOT LIKE '%@%.%' OR email LIKE '%@%@%';

-- 范围有效性
SELECT COUNT(*) as out_of_range
FROM orders
WHERE amount < 0 OR amount > 1000000;

-- 枚举有效性
SELECT status, COUNT(*) as cnt
FROM orders
GROUP BY status;
-- 检查是否有非预期状态值

-- 外键关联有效性
SELECT COUNT(*) as orphan_records
FROM orders o
LEFT JOIN users u ON o.user_id = u.id
WHERE u.id IS NULL;
```

---

### 4. 一致性 (Consistency)

**定义**：数据在不同表、不同字段之间保持一致

**检查类型**：
| 类型 | 说明 | 示例 |
|------|------|------|
| 跨表一致性 | 关联表数据一致 | 订单金额 = 订单明细金额之和 |
| 字段一致性 | 相关字段逻辑一致 | 结束时间 > 开始时间 |
| 编码一致性 | 编码规则统一 | 状态码大小写一致 |
| 单位一致性 | 数值单位统一 | 金额统一为元或分 |

**常见检查**：
```sql
-- 跨表一致性（金额核对）
SELECT
    o.order_id,
    o.total_amount as order_amount,
    SUM(oi.amount) as items_amount
FROM orders o
LEFT JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id, o.total_amount
HAVING ABS(o.total_amount - COALESCE(SUM(oi.amount), 0)) > 0.01;

-- 字段一致性（时间顺序）
SELECT COUNT(*) as invalid_timeline
FROM events
WHERE end_time < start_time;

-- 状态一致性
SELECT COUNT(*) as inconsistent_status
FROM orders
WHERE status = 'completed' AND completed_at IS NULL;
```

---

### 5. 及时性 (Timeliness)

**定义**：数据是否及时更新，满足业务时效要求

**检查指标**：
| 指标 | 说明 | 阈值建议 |
|------|------|----------|
| 数据新鲜度 | 最新数据时间 | < 1小时（实时）/ < 1天（T+1） |
| 延迟记录数 | 延迟到达的记录数 | 根据业务定义 |
| 更新频率 | 数据更新是否符合预期 | 符合SLA |

**常见检查**：
```sql
-- 数据新鲜度检查
SELECT
    MAX(created_at) as latest_record,
    NOW() - MAX(created_at) as data_delay
FROM table_name;

-- 延迟记录检查
SELECT COUNT(*) as delayed_records
FROM events
WHERE created_at < NOW() - INTERVAL '1 hour'
  AND processed_at IS NULL;
```

---

### 6. 准确性 (Accuracy)

**定义**：数据是否正确反映业务事实

**检查方式**：
| 方式 | 说明 | 示例 |
|------|------|------|
| 抽样验证 | 随机抽样人工核对 | 抽取100条记录核对 |
| 汇总核对 | 与权威数据源对比 | 订单金额与财务系统核对 |
| 交叉验证 | 多字段逻辑验证 | 单价 × 数量 = 金额 |

**常见检查**：
```sql
-- 交叉验证
SELECT COUNT(*) as calculation_errors
FROM order_items
WHERE ABS(price * quantity - total_amount) > 0.01;

-- 异常值检查（3σ原则）
WITH stats AS (
    SELECT
        AVG(amount) as avg_amount,
        STDDEV(amount) as stddev_amount
    FROM orders
)
SELECT COUNT(*) as outliers
FROM orders, stats
WHERE ABS(amount - avg_amount) > 3 * stddev_amount;
```

---

## 数据质量规则库

### 规则定义模板

```yaml
rule_id: RULE_001
rule_name: 用户邮箱格式检查
description: 检查用户邮箱是否符合标准格式
dimension: 有效性
severity: 高
table: users
column: email
rule_type: 格式检查
condition: "email NOT LIKE '%@%.%' OR email LIKE '%@%@%'"
threshold: 0  # 允许0条不符合
sql_template: |
  SELECT
    '{{ column }}' as column_name,
    COUNT(*) as violation_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM {{ table }}), 2) as violation_rate
  FROM {{ table }}
  WHERE {{ condition }}
```

### 常用规则清单

#### 完整性规则
| 规则ID | 规则名称 | 适用场景 | SQL模板 |
|--------|----------|----------|---------|
| COMP_001 | 必填字段检查 | 所有必填业务字段 | 空值计数 |
| COMP_002 | 记录完整性检查 | 全表记录数监控 | COUNT(*) |
| COMP_003 | 关联完整性检查 | 关联表记录对应 | LEFT JOIN + NULL检查 |

#### 唯一性规则
| 规则ID | 规则名称 | 适用场景 | SQL模板 |
|--------|----------|----------|---------|
| UNIQ_001 | 主键唯一性检查 | 所有主键字段 | GROUP BY + HAVING COUNT(*) > 1 |
| UNIQ_002 | 业务键唯一性检查 | 手机号、邮箱等 | GROUP BY + HAVING COUNT(*) > 1 |
| UNIQ_003 | 完全重复记录检查 | 数据去重 | GROUP BY所有字段 |

#### 有效性规则
| 规则ID | 规则名称 | 适用场景 | SQL模板 |
|--------|----------|----------|---------|
| VALID_001 | 邮箱格式检查 | 用户邮箱字段 | LIKE模式匹配 |
| VALID_002 | 手机号格式检查 | 用户手机号字段 | 正则/长度检查 |
| VALID_003 | 日期范围检查 | 日期字段 | 与当前日期比较 |
| VALID_004 | 数值范围检查 | 金额、数量等 | BETWEEN或比较 |
| VALID_005 | 枚举值检查 | 状态、类型字段 | NOT IN预定义值 |
| VALID_006 | 外键有效性检查 | 所有外键字段 | LEFT JOIN + NULL检查 |

#### 一致性规则
| 规则ID | 规则名称 | 适用场景 | SQL模板 |
|--------|----------|----------|---------|
| CONS_001 | 金额汇总一致性 | 订单-明细金额 | SUM对比 |
| CONS_002 | 时间顺序一致性 | 开始-结束时间 | 大小比较 |
| CONS_003 | 状态逻辑一致性 | 状态-时间字段 | 状态与时间匹配 |

---

## 评分标准

### 数据质量评分模型

```
总评分 = Σ(维度得分 × 维度权重)

维度权重建议：
- 完整性：25%
- 唯一性：20%
- 有效性：25%
- 一致性：15%
- 及时性：10%
- 准确性：5%
```

### 维度得分计算

```
维度得分 = 100 - (违规记录数 / 总记录数 × 100)

或

维度得分 = 通过规则数 / 总规则数 × 100
```

### 质量等级

| 等级 | 分数范围 | 说明 | 行动建议 |
|------|----------|------|----------|
| 🟢 优秀 | 95-100 | 数据质量良好 | 持续监控 |
| 🟡 良好 | 85-94 | 有小问题 | 本周修复 |
| 🟠 一般 | 70-84 | 有明显问题 | 立即修复 |
| 🔴 差 | < 70 | 数据质量差 | 停止依赖，紧急修复 |

---

## 检查SQL生成规范

### 标准检查SQL模板

```sql
-- ============================================
-- 规则ID: {RULE_ID}
-- 规则名称: {RULE_NAME}
-- 检查维度: {DIMENSION}
-- 目标表: {TABLE_NAME}
-- 目标字段: {COLUMN_NAME}
-- 严重程度: {SEVERITY}
-- ============================================

WITH check_result AS (
    SELECT
        COUNT(*) as total_records,
        COUNT({{ column }}) as non_null_records,
        SUM(CASE WHEN {{ condition }} THEN 1 ELSE 0 END) as violation_count
    FROM {{ table }}
    {{ where_clause }}
)
SELECT
    '{{ rule_id }}' as rule_id,
    '{{ rule_name }}' as rule_name,
    '{{ dimension }}' as dimension,
    '{{ table }}' as target_table,
    '{{ column }}' as target_column,
    total_records,
    violation_count,
    total_records - violation_count as passed_count,
    ROUND((total_records - violation_count) * 100.0 / total_records, 2) as pass_rate,
    ROUND(violation_count * 100.0 / total_records, 2) as violation_rate,
    CASE
        WHEN violation_count = 0 THEN '🟢 通过'
        WHEN violation_count <= {{ threshold }} THEN '🟡 警告'
        ELSE '🔴 失败'
    END as check_status,
    '{{ severity }}' as severity,
    NOW() as check_time
FROM check_result;
```

### 检查报告输出格式

```sql
-- 汇总报告表结构
CREATE TABLE data_quality_report (
    report_id SERIAL PRIMARY KEY,
    check_time TIMESTAMP DEFAULT NOW(),
    table_name VARCHAR(100),
    rule_id VARCHAR(50),
    rule_name VARCHAR(200),
    dimension VARCHAR(50),
    total_records INTEGER,
    passed_records INTEGER,
    failed_records INTEGER,
    pass_rate DECIMAL(5,2),
    status VARCHAR(20), -- PASS/WARNING/FAIL
    severity VARCHAR(20), -- HIGH/MEDIUM/LOW
    details JSONB
);
```

---

## 常见问题模式

### 问题1：大量NULL值

**现象**：字段空值率 > 20%

**根因**：
- 字段非业务必需，设计问题
- 数据采集不完整
- 默认值设置不当

**解决**：
- 评估字段是否必需
- 完善数据采集流程
- 设置合理默认值

### 问题2：主键重复

**现象**：主键字段存在重复值

**根因**：
- 并发插入未加锁
- 业务逻辑允许重复（设计问题）
- 数据导入时未去重

**解决**：
- 添加数据库唯一约束
- 应用层加分布式锁
- 数据导入前清洗

### 问题3：外键孤儿记录

**现象**：子表存在父表不存在的关联ID

**根因**：
- 删除父表记录时未级联
- 绕过外键约束直接导入数据
- 时序问题（子表先写入）

**解决**：
- 添加外键约束（如果性能允许）
- 删除时级联或软删除
- 数据加载时保证顺序

### 问题4：格式不统一

**现象**：同一字段格式混乱（如手机号有的带+86，有的不带）

**根因**：
- 缺乏输入校验
- 多系统数据来源
- 历史数据遗留

**解决**：
- 统一输入校验规则
- 数据清洗转换
- 建立数据标准

---

## 参考资料

- DAMA-DMBOK 数据管理知识体系
- ISO 8000 数据质量标准
- Google 数据质量白皮书
- Netflix 数据质量监控实践
