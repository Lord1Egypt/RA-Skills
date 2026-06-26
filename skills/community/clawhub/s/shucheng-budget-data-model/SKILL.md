---
name: budget-data-model
description: "提供预算系统数据模型的完整定义，包括所有表名、字段名、数据类型等。当用户需要查询预算相关数据模型结构、编写数据查询脚本、或需要了解特定表的字段信息时使用此技能。"
metadata: { "openclaw": { "emoji": "📊", "requires": { "bins": [] } } }
---

# 预算系统数据模型技能

提供预算系统的完整数据模型定义，包含 68 个数据表的详细结构信息。

## 何时使用

✅ **使用此技能的情况：**

- "预算管理表有哪些字段？"
- "查询预算数据需要用到哪些表？"
- "帮我写一个查询预算数据的脚本"
- "预算表的表名是什么？"
- "需要了解预算系统的数据库结构"
- "某字段在哪个表里？"

## 数据模型结构

每个数据模型包含以下信息：

- **table_id**: 表标识（数据库表名）
- **table_name**: 表显示名（中文别名）
- **fields**: 字段列表，每个字段包含：
  - **field_id**: 字段标识（数据库字段名）
  - **field_name**: 字段显示名（中文别名）
  - **data_type**: 数据类型（string/number/integer/datetime/date/array）
  - **length**: 长度/精度
  - **is_required**: 是否必填
  - **is_editable**: 是否可编辑

## 主要数据表分类

### 预算基础表
- 预算主表
- 预算版本
- 预算公式
- 预算科目

### 费用预算表
- 单位成本
- 成本预算
- 毛利预算
- 费用明细

### 业务预算表
- 维修计划
- 培训计划
- 附加服务
- 航材储备

### 报表相关表
- 预算报表主表
- 预算报表明细
- 预算执行报表

### 辅助表
- 预算科目值表
- 预算公式明细
- 飞机预算方案

## 数据查询规范

### 1. 使用 DataModelUtils 查询

```groovy
// 单条查询
def 数据 = DataModelUtils.getCIByPK("表名", ['ID': 值])

// 多条查询
def 数据列表 = DataModelUtils.getCIByAttr("表名", ['字段名': 值])

// SQL 查询
def sql = """SELECT * FROM "表名" WHERE 条件"""
def 结果 = DataModelUtils.queryForListMap(sql, null)
```

### 2. 字段命名规范

- 使用中文变量名（如 `def 预算数据`）
- 字段访问使用 `dataFieldMap.字段名`
- ID 字段通常为 `ID` 或 `表名 id`

### 3. 常见字段类型

| 类型 | 说明 | 示例 |
|------|------|------|
| string | 字符串 | '预算名称' |
| number | 数字（含小数） | 1000.00 |
| integer | 整数 | 2024 |
| datetime | 日期时间 | ${currTime} |
| date | 日期 | '2024-01-01' |
| array | 数组 | ['值 1', '值 2'] |

## 常用数据表说明

### 预算主表
用于存储预算的基本信息，包含预算名称、状态、创建时间等。

### 预算版本表
用于存储预算的不同版本，支持版本管理和历史追溯。

### 单位成本表
存储各单位的成本数据，包含月份、项目、金额等字段。

### 成本预算表
存储成本预算数据，支持多维度预算编制。

### 维修计划表
存储飞机维修计划，包含飞机号、客户编号、维修项目等。

### 培训计划表
存储培训计划信息，包含培训人员、时间、项目等。

## 数据模型文件

完整的数据模型定义存储在 `references/data_models.json` 文件中，包含所有 68 个数据表的详细字段信息。

## 使用示例

### 示例 1：查询预算主表数据

```groovy
def 预算数据 = DataModelUtils.getCIByPK("预算主表", ['ID': 预算 ID])
def 预算名称 = 预算数据.dataFieldMap.预算名称
def 状态 = 预算数据.dataFieldMap.状态
```

### 示例 2：查询某飞机的维修计划

```groovy
def 维修计划列表 = DataModelUtils.getCIByAttr("维修计划表", ['飞机号': 飞机号])
for (计划 in 维修计划列表) {
    println "维修项目：" + 计划.dataFieldMap.维修项目
}
```

### 示例 3：汇总某单位某月的成本

```groovy
def sql = """
    SELECT SUM("金额") AS 总成本
    FROM "单位成本表"
    WHERE "单位 id" = ? AND "月份" = ?
"""
def 结果 = DataModelUtils.queryForListMap(sql, [单位 ID, 月份])
def 总成本 = 结果 [0].总成本
```

## 注意事项

1. **表名和字段名**：使用数据模型中定义的准确名称
2. **数据类型**：注意区分 string、number、integer 等类型
3. **必填字段**：创建数据时确保必填字段有值
4. **ID 字段**：主键字段通常为 ID 或 表名 id，长度为 128
5. **关联查询**：通过 id 字段进行表间关联

## 相关文件

- `references/data_models.json` - 完整数据模型定义（68 个表）
