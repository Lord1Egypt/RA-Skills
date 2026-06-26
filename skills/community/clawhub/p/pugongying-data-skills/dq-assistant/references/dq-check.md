---
name: dq-check
description: |
  数据质量检查执行器 - 执行质量检查规则，生成详细报告。
  当用户需要执行数据质量检查、生成质量报告、监控数据质量时触发。
  触发词：执行质量检查、数据质量报告、质量监控、跑质检规则。
argument: { description: "检查配置（表名、规则集、时间范围等）或规则文件路径", required: true }
agent: general-purpose
allowed-tools: [Read, Grep, Glob, Edit, Write, Bash]
---

# 数据质量检查执行器

执行数据质量检查规则，生成详细的检查报告和趋势分析。

## 工作流程

1. **加载规则** - 读取检查规则配置
2. **执行检查** - 在目标数据库执行SQL检查
3. **收集结果** - 汇总各规则执行结果
4. **生成报告** - 输出结构化质量报告
5. **趋势分析** - 对比历史数据（如有）

## 输入格式

### 格式1：使用预定义规则
```
/dq-check 表名: orders, 规则集: 全量检查
```

### 格式2：指定规则文件
```
/dq-check 使用规则文件: ./dq-rules/orders_rules.yaml
```

### 格式3：自定义检查项
```
/dq-check
表: orders
检查项:
- 完整性: user_id非空, total_amount非空
- 有效性: status枚举值, total_amount>0
- 唯一性: order_id唯一
```

### 格式4：快速检查
```
/dq-check 快速检查 orders 表的完整性
```

## 输出规范

### 检查执行输出

```
============================================================
数据质量检查执行报告
============================================================
检查时间: 2025-03-17 10:30:00
目标表: orders
规则数量: 12
执行耗时: 3.45s

------------------------------------------------------------
【完整性检查】
------------------------------------------------------------
✅ COMP_001 order_id非空检查        通过  (0/100000)
✅ COMP_002 user_id非空检查          通过  (0/100000)
⚠️ COMP_003 paid_at非空检查         警告  (1500/100000, 1.5%)

------------------------------------------------------------
【唯一性检查】
------------------------------------------------------------
✅ UNIQ_001 order_id唯一性检查       通过  (0重复)
✅ UNIQ_002 order_no唯一性检查       通过  (0重复)

------------------------------------------------------------
【有效性检查】
------------------------------------------------------------
✅ VALID_001 total_amount范围检查    通过  (0/100000)
❌ VALID_002 status枚举检查          失败  (23/100000, 0.23%)
   异常值: unknown(15), temp(8)

------------------------------------------------------------
【一致性检查】
------------------------------------------------------------
⚠️ CONS_001 时间顺序一致性           警告  (3/100000)
   问题: paid_at < created_at

------------------------------------------------------------
【综合评分】
------------------------------------------------------------
完整性:    98.5/100  🟡
唯一性:   100.0/100  🟢
有效性:    99.8/100  🟢
一致性:    99.9/100  🟢
及时性:   100.0/100  🟢
------------------------------------------------------------
综合评分:  99.6/100  🟢 良好
质量等级:  🟢 良好 (符合预期)
------------------------------------------------------------

【问题汇总】
- 严重问题 (高): 0个
- 警告问题 (中): 2个
- 建议优化 (低): 0个

【行动建议】
1. 【高优先级】处理status字段异常值 (23条)
   SQL: SELECT * FROM orders WHERE status NOT IN (...)

2. 【中优先级】处理paid_at空值 (1500条)
   建议: 确认未支付订单是否合理

3. 【中优先级】检查时间顺序异常 (3条)
   SQL: SELECT * FROM orders WHERE paid_at < created_at
```

### JSON报告格式

```json
{
  "report_id": "dq_20250317_103000",
  "check_time": "2025-03-17T10:30:00",
  "target_table": "orders",
  "summary": {
    "total_rules": 12,
    "passed": 9,
    "warning": 2,
    "failed": 1,
    "overall_score": 99.6,
    "quality_level": "良好"
  },
  "dimension_scores": {
    "completeness": 98.5,
    "uniqueness": 100.0,
    "validity": 99.8,
    "consistency": 99.9,
    "timeliness": 100.0
  },
  "results": [
    {
      "rule_id": "COMP_001",
      "rule_name": "order_id非空检查",
      "dimension": "完整性",
      "status": "通过",
      "total_records": 100000,
      "violation_count": 0,
      "pass_rate": 100.0
    }
  ],
  "issues": [
    {
      "severity": "高",
      "rule_id": "VALID_002",
      "description": "status字段存在异常值",
      "violation_count": 23,
      "sample_values": ["unknown", "temp"],
      "remediation_sql": "SELECT * FROM orders WHERE status NOT IN (...)"
    }
  ]
}
```

## 检查维度

### 1. 完整性检查 (COMP_*)

```sql
-- 模板
SELECT
    '{{ rule_name }}' as check_name,
    '完整性' as dimension,
    COUNT(*) as total_records,
    SUM(CASE WHEN {{ column }} IS NULL THEN 1 ELSE 0 END) as null_count,
    ROUND((1 - SUM(CASE WHEN {{ column }} IS NULL THEN 1 ELSE 0 END) * 1.0 / COUNT(*)) * 100, 2) as completeness_rate
FROM {{ table }}
{{ where_clause }};
```

### 2. 唯一性检查 (UNIQ_*)

```sql
-- 模板
SELECT
    '{{ rule_name }}' as check_name,
    '唯一性' as dimension,
    COUNT(*) as total_records,
    COUNT(*) - COUNT(DISTINCT {{ column }}) as duplicate_count,
    COUNT(DISTINCT {{ column }}) as unique_count
FROM {{ table }}
{{ where_clause }};
```

### 3. 有效性检查 (VALID_*)

```sql
-- 模板
SELECT
    '{{ rule_name }}' as check_name,
    '有效性' as dimension,
    COUNT(*) as total_records,
    SUM(CASE WHEN {{ condition }} THEN 1 ELSE 0 END) as invalid_count,
    ROUND((1 - SUM(CASE WHEN {{ condition }} THEN 1 ELSE 0 END) * 1.0 / COUNT(*)) * 100, 2) as validity_rate
FROM {{ table }}
{{ where_clause }};
```

### 4. 一致性检查 (CONS_*)

```sql
-- 模板
SELECT
    '{{ rule_name }}' as check_name,
    '一致性' as dimension,
    COUNT(*) as total_records,
    SUM(CASE WHEN {{ condition }} THEN 1 ELSE 0 END) as inconsistent_count
FROM {{ table }}
{{ where_clause }};
```

## 评分计算

### 维度得分
```
维度得分 = (1 - 违规记录数/总记录数) × 100
```

### 综合得分
```
综合得分 = Σ(维度得分 × 维度权重)

默认权重:
- 完整性: 25%
- 唯一性: 20%
- 有效性: 25%
- 一致性: 15%
- 及时性: 10%
- 准确性: 5%
```

### 质量等级
- 🟢 优秀: 95-100分
- 🟡 良好: 85-94分
- 🟠 一般: 70-84分
- 🔴 差: <70分

## 趋势分析

对比历史检查结果：

```
趋势对比 (vs 上周):
- 完整性: 98.5% (↑ 0.5%)
- 唯一性: 100.0% (→ 持平)
- 有效性: 99.8% (↓ 0.1%)
- 综合评分: 99.6% (↑ 0.2%)

新增问题:
- VALID_002 status枚举检查 (新增23条异常)

已修复:
- COMP_004 address非空检查 (上周150条 → 本周0条)
```

## 问题修复SQL生成

自动生成修复SQL：

```sql
-- 问题1: status字段异常值
-- 发现23条异常记录，异常值: unknown(15), temp(8)

-- 查看异常记录
SELECT order_id, status, created_at
FROM orders
WHERE status NOT IN ('pending', 'paid', 'shipped', 'completed', 'cancelled');

-- 修复建议 (根据实际情况选择)
-- 方案A: 更新为默认值
UPDATE orders
SET status = 'pending'
WHERE status NOT IN ('pending', 'paid', 'shipped', 'completed', 'cancelled');

-- 方案B: 删除测试数据
DELETE FROM orders
WHERE status = 'temp';
```

## 检查模式

### 模式1: 全量检查
检查所有规则，生成完整报告。

### 模式2: 快速检查
只检查关键规则（完整性+唯一性），适合日常监控。

### 模式3: 增量检查
只检查新增/修改的数据，适合大数据量表。

### 模式4: 专项检奁
针对特定维度（如只检查有效性）。

## 当前检查配置

$ARGUMENTS

---

**执行检查时**：
1. 解析检查配置，加载规则
2. 按维度执行检查SQL
3. 收集并汇总结果
4. 计算各维度和综合评分
5. 对比历史趋势（如有）
6. 生成修复SQL建议
7. 输出结构化的检查报告
