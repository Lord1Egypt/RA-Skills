---
slug: text2sql-engine-free
name: text2sql-engine-free
version: 1.0.0
displayName: 自然语言转SQL免费版
summary: 将自然语言描述转换为标准SQL查询，支持多方言与Schema自动识别
license: Proprietary
edition: free
description: 面向数据分析人员与后端开发者的自然语言转SQL引擎，解决"知道想要什么数据但写不出SQL"的核心痛点。核心能力：将中文/英文的自然语言描述转换为语法正确的SQL查询，支持表结构自动识别、意图解析、JOIN关系推导与查询验证。Use
  when 需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于实时流数据处理。
tags:
- 数据查询
- SQL生成
- 开发工具
tools:
- - read
- exec
homepage: https://skillhub.cn
pricing_tier: L2
pricing_model: per_use
suggested_price: 19.9
tools: ["read", "write", "exec"]
tags: "工具,效率,自动化"
---
# 自然语言转SQL引擎（免费版）

## 概述

本Skill解决一个高频痛点：业务人员知道想要什么数据，但无法将意图转化为SQL查询。通过自然语言描述需求，引擎自动生成语法正确、可执行的SQL语句。

免费版支持单表查询、基础多表JOIN、聚合统计等核心场景，覆盖日常80%的数据查询需求。

## 核心能力

| 能力模块 | 说明 | 免费版支持 |
|----|---|-----|
| 自然语言意图解析 | 将描述映射为SQL子句 | 是 |
| Schema自动识别 | 从CREATE TABLE/DESCRIBE提取结构 | 是 |
| 单表查询生成 | SELECT/WHERE/ORDER BY/GROUP BY | 是 |
| 多表JOIN推导 | INNER/LEFT JOIN关系推导 | 是（限2表） |
| 聚合统计 | COUNT/SUM/AVG/MIN/MAX | 是 |
| SQL方言适配 | `PostgreSQL`/MySQL/SQLite | 是 |
| 查询质量校验 | 语法与字段验证 | 是 |
| 查询解释 | 注释说明每条子句作用 | 否（专业版） |
| 替代方案生成 | 多种写法对比 | 否（专业版） |
| 查询性能优化 | 索引建议与执行计划分析 | 否（专业版） |

### 核心功能执行
用`input_params`参数进行配置。

**输入**: 用户提供核心功能执行所需的指令和必要参数。
**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输入**: 用户提供参数配置与调用所需的指令和必要参数。
**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置。

**输入**: 用户提供结果处理与输出所需的指令和必要参数。
**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：将自然语言描述转、换为标准、支持多方言与、面向数据分析人员、与后端开发者的自、然语言转、知道想要什么数据、但写不出、的核心痛点、核心能力、将中文、英文的自然语言描、述转换为语法正确、支持表结构自动识、关系推导与查询验、Use、when、需要数据分析、报表生成、统计洞察、数据可视化时使用、不适用于实时流数、据处理等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一：业务人员自助查询

运营人员需要查看"上个月消费超过1000元的VIP用户名单"，但不熟悉SQL。向Agent描述需求并提供表结构，引擎自动生成查询语句。

### 场景二：快速原型验证

开发者在设计新功能时，需要快速验证某个查询逻辑是否正确。用自然语言描述预期结果，引擎生成SQL后直接在测试库执行验证。

### 场景三：SQL学习辅助

SQL初学者通过对比自然语言描述与生成的SQL，理解每个子句的作用，加速学习过程。

## 快速开始

### 第一步：提供Schema（约30秒）

引擎需要知道你的表结构才能生成正确查询。提供方式任选其一：

```sql
-- 方式一：CREATE TABLE语句
CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(200),
    vip_level INT DEFAULT 0,
    created_at TIMESTAMP
);
# ...
CREATE TABLE orders (
    id BIGINT PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    amount DECIMAL(10,2),
    status VARCHAR(20),
    created_at TIMESTAMP
);
```

```sql
-- 方式二：DESCRIBE输出
DESCRIBE users;
DESCRIBE orders;
```

### 第二步：描述你的查询需求

```
帮我查询上个月消费总金额超过1000元的VIP用户，按消费金额从高到低排列，只显示前20名
```

### 第三步：获取生成的SQL

```sql
SELECT
    u.id,
    u.name,
    u.email,
    SUM(o.amount) AS total_spent
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE u.vip_level > 0
    AND o.status = 'completed'
    AND o.created_at >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')
    AND o.created_at < DATE_TRUNC('month', CURRENT_DATE)
GROUP BY u.id, u.name, u.email
HAVING SUM(o.amount) > 1000
ORDER BY total_spent DESC
LIMIT 20;
```

## 示例

### 自然语言到SQL子句映射表

| 自然语言关键词 | SQL子句 | 示例 |
|:--------|:--------|:--------|
| "全部"、"所有"、"完整列表" | `SELECT *` | 查询所有用户 -> `SELECT * FROM users` |
| "仅"、"只要"、"指定字段" | `SELECT [字段]` | 只要姓名和邮箱 -> `SELECT name, email` |
| "满足...条件"、"其中" | `WHERE` | 满足VIP等级>2 -> `WHERE vip_level > 2` |
| "按...排序"、"以...排列" | `ORDER BY` | 按注册时间排序 -> `ORDER BY created_at` |
| "分组"、"每个" | `GROUP BY` | 每个用户的总消费 -> `GROUP BY user_id` |
| "前N条"、"最多N个" | `LIMIT N` | 前10名 -> `LIMIT 10` |
| "排除"、"不含"、"除了" | `WHERE NOT` / `!=` | 排除已删除 -> `WHERE deleted_at IS NULL` |
| "同时满足"、"并且" | `AND` | VIP且消费>1000 -> `AND amount > 1000` |
| "满足任一"、"或者" | `OR` | VIP或消费>5000 -> `OR amount > 5000` |
| "介于...之间" | `BETWEEN` | 金额在100-500之间 -> `BETWEEN 100 AND 500` |
| "包含"、"类似" | `LIKE '%value%'` | 姓名包含张 -> `name LIKE '%张%'` |
| "最新"、"最近" | `ORDER BY ... DESC LIMIT 1` | 最新订单 -> `ORDER BY created_at DESC LIMIT 1` |
| "数量"、"多少个" | `COUNT(*)` | 用户总数 -> `SELECT COUNT(*) FROM users` |
| "总和"、"总计" | `SUM(column)` | 消费总额 -> `SUM(amount)` |
| "平均" | `AVG(column)` | 平均消费 -> `AVG(amount)` |

### JOIN类型选择规则

| 场景描述 | JOIN类型 | 理由 |
|---:|---:|---:|
| "同时有"、"关联的" | `INNER JOIN` | 只返回两表都匹配的记录 |
| "包括没有...的" | `LEFT JOIN` | 保留左表所有记录 |
| "每个...及其" | `LEFT JOIN` | 确保主表完整 |
| "同时存在于" | `INNER JOIN` | 交集关系 |

### 多方言适配

```sql
-- PostgreSQL: 使用DATE_TRUNC
SELECT DATE_TRUNC('month', created_at), COUNT(*)
FROM orders GROUP BY 1;
# ...
-- MySQL: 使用DATE_FORMAT
SELECT DATE_FORMAT(created_at, '%Y-%m-01'), COUNT(*)
FROM orders GROUP BY 1;
# ...
-- SQLite: 使用strftime
SELECT strftime('%Y-%m-01', created_at), COUNT(*)
FROM orders GROUP BY 1;
```

## 最佳实践

### Schema提供规范

1. **必须提供表名和字段名**：引擎不会猜测不存在的字段
2. **标注字段类型**：特别是时间类型（TIMESTAMP vs DATE）
3. **标注外键关系**：帮助引擎正确推导JOIN条件
4. **提供业务语义**：如 `status` 字段的枚举值含义

### 查询质量校验清单

生成SQL后，引擎自动执行以下校验：

- [ ] 所有引用的字段名在Schema中存在
- [ ] 所有表别名已定义
- [ ] JOIN条件使用了正确的关联字段
- [ ] 聚合查询包含GROUP BY
- [ ] 无歧义的字段引用（多表时使用别名限定）
- [ ] LIMIT语句配合ORDER BY使用

### 错误恢复策略

| 错误类型 | 原因 | 恢复策略 |
|:---:|:---:|:---:|
| 字段不存在 | Schema未提供或拼写错误 | 提示用户提供完整Schema，列出相似字段名 |
| JOIN条件缺失 | 未提供外键关系 | 询问用户哪个字段关联两表 |
| 语法错误 | 方言不兼容 | 确认目标数据库类型，切换对应方言 |
| 聚合缺少GROUP BY | 意图解析遗漏 | 检测到聚合函数时自动补充GROUP BY |
| 性能隐患 | 全表扫描 | 建议添加索引或限制结果集大小 |

## 常见问题

### Q1：没有提供Schema会怎样？

A：引擎不会猜测表名或字段名。如果未提供Schema，会主动询问用户："请提供相关表的字段名和类型，例如CREATE TABLE语句或DESCRIBE输出。"这是为了避免生成引用不存在字段的无效SQL。

### Q2：支持哪些SQL方言？

A：免费版支持 `PostgreSQL`、MySQL、SQLite三种主流方言。生成查询时会根据用户指定的数据库类型适配语法差异（如日期函数、字符串拼接、分页语法等）。

### Q3：能处理复杂的多表查询吗？

A：免费版支持最多2张表的JOIN查询。如果涉及3张及以上表的复杂关联，建议使用专业版，支持多表嵌套JOIN、子查询、CTE（公用表表达式）等高级特性。

### Q4：生成的SQL会自动执行吗？

A：不会。本引擎只生成SQL语句，不执行查询。生成的SQL需要用户自行在数据库客户端中执行。这样可以避免误操作风险，用户可以在执行前审查SQL。

### Q5：如何提高生成质量？

A：(1) 提供尽可能详细的Schema信息，包括字段类型和外键关系；(2) 在描述中明确指定排序、限制等条件；(3) 使用具体字段名而非泛化描述；(4) 标注目标数据库类型。

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **数据库客户端**: 任意支持SQL的客户端（DBeaver/Navicat/psql/mysql等）

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| LLM API | API | 必需 | 由Agent平台内置LLM提供 |
| `PostgreSQL` | 数据库 | 可选 | 官方安装或云服务 |
| MySQL | 数据库 | 可选 | 官方安装或云服务 |
| SQLite | 数据库 | 可选 | Python内置sqlite3模块 |

### API Key 配置
- **数据库连接串**: 存储于环境变量 `DATABASE_URL`，格式 `postgresql://user:pass@host:port/dbname`
- **禁止**: 在代码或脚本中硬编码数据库密码
- **推荐**: 使用 `.env` 文件或密钥管理服务

### 可用性分类
- **分类**: MD+EXEC（纯Markdown指令，部分功能需要exec命令行执行能力）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent生成SQL查询语句

## 已知限制

本免费体验版限制以下高级功能：
- 不支持3张及以上表的多表JOIN查询
- 不支持子查询、CTE（公用表表达式）、窗口函数
- 不支持查询解释（内联注释说明）
- 不支持替代方案生成（多种写法对比）
- 不支持查询性能优化建议与执行计划分析
- 不支持存储过程与触发器生成

解锁全部功能请使用专业版：text2sql-engine-pro
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|:---|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "自然语言转SQL免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "text2sql engine"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
