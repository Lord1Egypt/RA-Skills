---

slug: text2sql-engine
name: text2sql-engine
version: 1.0.1
displayName: 自然语言转SQL专业版
summary: 全功能NL2SQL引擎，支持复杂多表查询、性能优化、查询解释与替代方案生成。面向数据工程师与DBA的全功能自然语言转SQL引擎，支持复杂多表关联、窗口函数、查询性能优化与执行计划分析。核心能
summary_zh: 全功能NL2SQL引擎，支持复杂多表查询、性能优化、查询解释与替代方案生成。面向数据工程师与DBA的全功能自然语言转SQL引擎，支持复杂多表关联、窗口函数、查询性能优化与执行计划分析。核心能
license: MIT
edition: pro
description: |- 功能涵盖: text2sql,。Use when 需要数据库操作、SQL查询、数据存储管理时使用。不适用于数据库架构设计决策。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。提供结构化输出和错误处理机制。支持多场景应用和灵活配置。 功能涵盖: engine(引擎)。
  面向数据工程师与DBA的全功能自然语言转SQL引擎，支持复杂多表关联、窗口函数、查询性能优化与执行计划分析。核心能力：在免费版基础上新增多表嵌套JOIN、子查询/CTE/窗口函数、查询解释注释、替代方案对比、执行计划分析、索引优化建议、SQL安全审计等高级特性。Use
  when 需要数...'
tags:
- 数据查询
- SQL优化
- 数据工程
- 性能调优
- 工具
- 效率
- 写作
- 电商
- sql
- created_at
- month
- schema
- select
tools:
- read
- exec
- write
homepage: ''
category: Automation

---

> **核心功能**: 本技能提供化工作流场景等能力。

> **核心功能**: 本技能提供中文交互等能力。

> **核心功能**: 本技能提供时使用等能力。

# 自然语言转SQL专业版
## 付费版进阶功能
| 能力 | 免费版 | 付费版 |
|---|---|---|
| 基础功能 | 支持 | 支持 |
| 自然语言转SQL专业版支持复杂多表查询 | 不支持 | 支持 |
| 自然语言转SQL专业版询解释与替代方案生成 | 不支持 | 支持 |
| 大数据集流式处理 | 不支持 | 支持 |
| 多数据源关联查询 | 不支持 | 支持 |
| 可视化图表自动生成 | 不支持 | 支持 |
## 能力清单
| 能力模块 | 说明 | 专业版增强 |
|:-----|:-----|:-----|
| 自然语言意图解析 | 意图到SQL子句映射 | 支持复杂嵌套意图解析 |
| Schema自动识别 | 表结构提取 | 支持视图、物化视图、分区表 |
| 多表JOIN | 表关联推导 | 无限表数，支持嵌套JOIN |
| 子查询与CTE | 复杂查询结构 | 子查询/CTE/递归CTE |
| 窗口函数 | 分析函数 | RANK/DENSE_RANK/LAG/LEAD/ROW_NUMBER |
| 查询解释 | 内联注释 | 逐子句解释+执行顺序标注 |
| 替代方案 | 多种写法对比 | 3+种方案+性能对比 |
| 执行计划分析 | EXPLAIN解析 | 索引使用/扫描类型/成本估算 |
| 索引优化建议 | 索引推荐 | 复合索引/覆盖索引/部分索引 |
| SQL安全审计 | 安全检查 | 注入风险/权限越界/敏感数据访问 |
| 多方言适配 | 方言兼容 | `关系型数据库`/MySQL/SQLite/SQL Server/Oracle |
## 典型场景
### 场景一：复杂报表生成（数据分析师视角）

某电商平台需要生成"各品类月度销售额环比增长率"报表，涉及商品表、订单表、订单明细表、品类表四张表的关联，并需要窗口函数计算环比.
向Agent描述需求：

```
查询每个品类每月的销售总额，并计算与上月的环比增长率，按品类和月份排序
```

Agent生成：

```sql
WITH monthly_sales AS (
    SELECT
        c.category_name,
        DATE_TRUNC('month', o.created_at) AS month,
        SUM(oi.quantity * oi.unit_price) AS total_sales
    FROM categories c
    INNER JOIN products p ON c.id = p.category_id
    INNER JOIN order_items oi ON p.id = oi.product_id
    INNER JOIN orders o ON oi.order_id = o.id
    WHERE o.status = 'completed'
    GROUP BY c.category_name, DATE_TRUNC('month', o.created_at)
),
sales_with_prev AS (
    SELECT
        category_name,
        month,
        total_sales,
        LAG(total_sales) OVER (
            PARTITION BY category_name
            ORDER BY month
        ) AS prev_month_sales
    FROM monthly_sales
)
SELECT
    category_name,
    month,
    total_sales,
    prev_month_sales,
    CASE
        WHEN prev_month_sales IS NULL THEN NULL
        WHEN prev_month_sales = 0 THEN NULL
        ELSE ROUND(
            (total_sales - prev_month_sales) * 100.0 / prev_month_sales, 2
        )
    END AS growth_rate_pct
FROM sales_with_prev
ORDER BY category_name, month;
```

### 场景二：慢查询优化（DBA视角）

某系统有一条查询响应时间超过30秒，DBA需要定位性能瓶颈并优化。专业版提供执行计划分析：

```sql
-- 原始查询
EXPLAIN ANALYZE
SELECT * FROM orders WHERE customer_id = 12345 ORDER BY created_at DESC;
# ...
-- 专业版分析结果
-- Seq Scan on orders (cost=0.00..45230.00 rows=1500 width=256) (actual time=0.050..850.230)
--   Filter: (customer_id = 12345)
--   Rows Removed by Filter: 1500000
-- Sort (cost=45230.00..45233.75 rows=1500 width=256) (actual time=850.300..850.500)
--   Sort Key: created_at DESC
--   Sort Method: quicksort Memory: 256kB
# ...
-- 优化建议：
-- 1. 添加复合索引：CREATE INDEX idx_orders_customer_created ON orders(customer_id, created_at DESC);
-- 2. 避免SELECT *，只查必要字段
-- 3. 预期优化后响应时间：<50ms
```

优化后查询：

```sql
SELECT id, order_no, amount, status, created_at
FROM orders
WHERE customer_id = 12345
ORDER BY created_at DESC
LIMIT 100;
```

### 场景三：数据迁移与兼容（数据工程师视角）

某团队从MySQL迁移到 `关系型数据库`，需要将现有SQL语法进行转换。专业版支持方言间自动转换：

```sql
-- MySQL原始查询
SELECT
    user_id,
    DATE_FORMAT(created_at, '%Y-%m') AS month,
    COUNT(*) AS order_count,
    GROUP_CONCAT(product_name SEPARATOR ', ') AS products
FROM orders
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
GROUP BY user_id, DATE_FORMAT(created_at, '%Y-%m')
HAVING order_count > 5;
# ...
-- 自动转换为数据库
SELECT
    user_id,
    TO_CHAR(created_at, 'YYYY-MM') AS month,
    COUNT(*) AS order_count,
    STRING_AGG(product_name, ', ') AS products
FROM orders
WHERE created_at >= NOW() - INTERVAL '6 months'
GROUP BY user_id, TO_CHAR(created_at, 'YYYY-MM')
HAVING COUNT(*) > 5;
```
## 使用指南
### 使用流程(补充)

1. **提供完整Schema**：包括表结构、视图、索引、外键关系
2. **描述查询需求**：用自然语言描述，越详细越好
3. **选择目标方言**：指定 `关系型数据库`/MySQL/SQLite等
4. **获取SQL+解释+优化建议**：一次生成完整方案

```
数据库类型：关系型数据库
表结构：[粘贴CREATE TABLE语句]
查询需求：查询过去6个月每月新增用户数、活跃用户数、付费用户数，并计算付费转化率，按月份排序
```

**结果验证**: 任务完成后,查看输出确认状态。成功时返回摘要和数据;失败时根据错误信息排查,参考恢复章节获取修复步骤.
## 输入定义
| 参数名 | 类型 | 必填 | 说明 |
|---:|---:|---:|---:|
| content | string | 否 | 处理的内容输入 |
| mode | string | 否 | 处理模式, 可选值: json/text/markdown |
| style | string | 否 | 输出风格, 参考 `references/style.md` |
## 响应格式
```json
{
  "success": true,
  "data": {
    "result": "处理结果",
    "status": "success",
    "metadata": {
    "metadata": {
      "template_used": "reviewer",
      "word_count": 0,
      "style": "专业"
    }
  },
  "error": null
}
```

输出模板参考: `assets/output.json`
## 异常响应
| 问题现象 | 可能原因 | 排查步骤 | 优先级 |
|:---:|:---:|:---:|:---:|
| 生成的SQL执行报错 | Schema不完整或方言不匹配 | 核对Schema字段，确认数据库版本 | P0 |
| 查询结果不正确 | 意图解析偏差 | 细化需求描述，检查WHERE/HAVING条件 | P0 |
| 查询超时 | 缺少索引或全表扫描 | 查看执行计划，按建议添加索引 | P1 |
| 方言转换失败 | 不支持的特有语法 | 查看转换日志，手动调整不兼容部分 | P1 |
| 安全审计误报 | 规则过于严格 | 查看审计规则配置，调整白名单 | P2 |
| 替代方案性能差异大 | 数据分布不均匀 | 使用真实数据测试，参考执行计划成本 | P2 |
## 安装与配置
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **数据库**: `关系型数据库` 10+ / MySQL 5.7+ / SQLite 3.25+ / SQL Server 2017+ / Oracle 12c+

### 依赖说明(补充)

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| LLM API | API | 必需 | 由Agent平台内置LLM提供 |
| `关系型数据库` | 数据库 | 推荐 | 官方安装或云服务 |
| MySQL | 数据库 | 可选 | 官方安装或云服务 |
| pg_stat_statements | PG扩展 | 推荐 | `关系型数据库`自带 contrib 模块 |
| psql客户端 | CLI工具 | 推荐 | 随 `关系型数据库` 安装 |

### API Key 配置
- **数据库连接串**: 存储于环境变量 `DATABASE_URL`，格式 `关系型数据库://user:pass@host:port/dbname`
- **只读连接**: 建议使用只读账户进行查询验证，避免误操作
- **禁止**: 在代码或脚本中硬编码数据库密码
- **推荐**: 使用密钥管理服务（如HashiCorp Vault）管理数据库凭证

### 可用性分类
- **分类**: MD+EXEC（）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent生成企业级SQL查询
## 案例展示

### 递归CTE配置（组织架构查询）

```sql
WITH RECURSIVE org_tree AS (
    -- 基础查询：优秀管理者
    SELECT id, name, manager_id, 1 AS level
    FROM employees
    WHERE manager_id IS NULL
# ...
    UNION ALL
# ...
    -- 递归查询：下属员工
    SELECT e.id, e.name, e.manager_id, ot.level + 1
    FROM employees e
    INNER JOIN org_tree ot ON e.manager_id = ot.id
)
SELECT level, COUNT(*) AS headcount, STRING_AGG(name, ', ') AS members
FROM org_tree
GROUP BY level
ORDER BY level;
```

### 窗口函数配置（用户留存分析）

```sql
SELECT
    signup_date,
    user_count,
    day1_retention,
    ROUND(day1_retention * 100.0 / user_count, 2) AS day1_rate,
    day7_retention,
    ROUND(day7_retention * 100.0 / user_count, 2) AS day7_rate
FROM (
    SELECT
        signup_date,
        COUNT(DISTINCT user_id) AS user_count,
        COUNT(DISTINCT CASE WHEN last_active >= signup_date + INTERVAL '1 day'
            THEN user_id END) AS day1_retention,
        COUNT(DISTINCT CASE WHEN last_active >= signup_date + INTERVAL '7 days'
            THEN user_id END) AS day7_retention
    FROM user_activity
    GROUP BY signup_date
) t
ORDER BY signup_date;
```

### 索引优化建议模板

```sql
-- 专业版自动生成的索引建议
-- 查询模式：WHERE status = 'active' AND created_at > '2024-01-01'
-- 当前问题：Seq Scan，扫描全表500万行
# ...
-- 建议索引1：复合索引（覆盖查询条件）
CREATE INDEX CONCURRENTLY idx_orders_status_created
    ON orders(status, created_at DESC)
    WHERE status = 'active';  -- 部分索引，减小体积
# ...
-- 建议索引2：覆盖索引（包含查询字段）
CREATE INDEX CONCURRENTLY idx_orders_covering
    ON orders(status, created_at DESC)
    INCLUDE (order_no, amount, customer_id);
# ...
-- 预期效果：
-- Seq Scan -> Index Only Scan
-- 扫描行数：500万 -> 约2000
-- 响应时间：2.5s -> <10ms
```
## 问答合集
### Q1：专业版支持多少张表的JOIN？

A：无限制。专业版支持任意数量的表关联，自动推导JOIN关系。对于超过5张表的复杂查询，会生成可视化的关系图帮助理解.
### Q2：执行计划分析支持哪些数据库？

A：支持 `关系型数据库`（EXPLAIN ANALYZE）、MySQL（EXPLAIN FORMAT=JSON）、SQLite（EXPLAIN QUERY PLAN）。分析结果包括扫描类型、索引使用、成本估算、实际耗时等.
### Q3：索引优化建议是否自动执行？

A：不会自动执行。专业版只生成建议（CREATE INDEX语句），需DBA审核后手动执行。建议使用 `CONCURRENTLY` 选项避免锁表.
### Q4：SQL安全审计能检测哪些风险？

A：覆盖6类安全风险：SQL注入、权限越界、敏感数据暴露、危险操作（全表删除/更新）、笛卡尔积、资源消耗过大。审计结果按严重程度分级.
### Q5：方言转换的准确率如何？

A：对于标准SQL语法，转换准确率>95%。部分数据库特有语法（如Oracle的CONNECT BY）会转换为标准CTE等价写法，并标注转换说明.
### Q6：如何处理超大型表的查询？

A：专业版建议使用分区策略：(1) 按时间范围分区（时序数据）；(2) 按Hash分区（均匀分布）；(3) 使用物化视图预聚合。同时生成对应的分区DDL语句.
### Q7：窗口函数和GROUP BY有什么区别？

A：GROUP BY会折叠行（每组一行），窗口函数保留原始行并添加聚合值。窗口函数适合需要在明细数据旁边展示聚合值的场景，如"每个员工薪资与部门平均薪资的差值".
### 错误恢复步骤
| 错误场景 | 原因 | 处理方式 |
|---:|:---|---:|
| LLM响应超时或无响应 | 网络延迟或模型负载过高 | 请求重试；确认Agent平台LLM服务正常 |
| 输入内容格式不正确 | 用户输入不符合skill预期格式 | 检查输入是否符合skill使用说明中的格式要求，参考示例章节 |
| 执行结果与预期不符 | 指令描述不够明确或上下文不足 | 提供更详细的指令描述，补充必要的上下文信息 |
| 命令执行失败 | 运行环境不满足要求或权限不足 | 确认运行环境符合依赖说明中的要求；检查命令权限设置 |
## 限制条件
A：数据库层面有限制（`关系型数据库`默认100层），可在查询中设置 `SET max_recursion_depth = N`。专业版会检测递归深度并在接近限制时发出警告.
### Q9：专业版是否支持NoSQL查询转换？

A：当前版本不支持。专业版专注于关系型SQL。如需MongoDB/ES等NoSQL查询，请关注后续版本更新.
### Q10：如何获取优先技术支持？

A：专业版用户提供7x24小时优先支持通道，可通过专属工单系统提交问题，平均响应时间<4小时，关键问题<1小时.
## 补充限制说明

- 需要LLM支持
- 依赖Agent平台的LLM能力与运行环境配置
- 免费版功能受限，高级能力需升级专业版
## 安全规则
| 风险项 | 等级 | 防护措施 | 验证方法 |
| --- | --- | --- | --- |
| SQL注入攻击 | 高 | 使用参数化查询，避免直接拼接SQL语句 | 定期进行安全审计，检测SQL注入风险 |
| 权限越界 | 中 | 严格管理数据库用户权限，使用最小权限原则 | 定期检查用户权限，确保权限设置正确 |
| 敏感数据泄露 | 高 | 对敏感数据进行加密存储和传输 | 定期进行数据安全检查，确保敏感数据安全 |
| 危险操作 | 高 | 对危险操作进行监控和审计 | 实施操作日志记录，定期审计操作记录 |
| 笛卡尔积 | 中 | 优化查询逻辑，避免不必要的笛卡尔积 | 优化查询语句，避免笛卡尔积产生 |
| 资源消耗过大 | 中 | 监控系统资源使用情况，优化查询性能 | 定期监控资源使用，优化查询性能 |
## 技术创新
| 场景 | 效率提升量化分析 | 差异化对比 |
| --- | --- | --- |
| 复杂报表生成 | 将报表生成时间从数小时缩短至数分钟 | 传统方法需要手动编写SQL，效率低，易出错 |
| 慢查询优化 | 将查询优化时间从数小时缩短至数分钟 | 传统方法需要手动分析执行计划，效率低，易出错 |
| 数据迁移与兼容 | 将数据迁移时间从数周缩短至数小时 | 传统方法需要手动编写转换脚本，效率低，易出错 |
| 查询解释与替代方案生成 | 将查询解释时间从数小时缩短至数分钟 | 传统方法需要手动分析查询逻辑，效率低，易出错 |
| 执行计划分析 | 将执行计划分析时间从数小时缩短至数分钟 | 传统方法需要手动分析执行计划，效率低，易出错 |
## 功能介绍
- **自动化执行**: 全功能NL2SQL引擎，支持复杂多表查询、性能优化、查询解释与替代方案生成。面向数据工程师与DBA的全功能自然语言转SQ
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据
## 效率指标
| 操作场景 | 手动耗时 | 自动化耗时 | 效率提升 |
|----------|---------|-----------|---------|
| 文件解析与提取 | 5-10分钟/个 | <5秒/个 | 60-120x |
| 批量文件处理(100个) | 8-16小时 | <5分钟 | 96-192x |
| API调用与响应解析 | 2-3分钟/次 | <1秒/次 | 120-180x |
| 多接口数据聚合 | 15-30分钟 | <10秒 | 90-180x |
| 命令执行与结果收集 | 3-5分钟/次 | <2秒/次 | 90-150x |
| 重复任务批量执行 | 因任务而异 | 线性缩减 | 5-50x |
| 错误排查与修复 | 10-30分钟 | <30秒 | 20-60x |
## 优势分析
| 对比维度 | 自然语言转SQL专业版 | 传统手动方式 | 通用脚本工具 |
|---------|------------|-------------|------------|
| 自动化程度 | 全流程自动 | 完全手动 | 部分自动 |
| 错误处理 | 内置错误恢复 | 依赖人工经验 | 基本try-catch |
| 可复用性 | 参数化配置 | 一次性脚本 | 模板化 |
| 安全合规 | 内置安全检查 | 无安全保障 | 无安全保障 |
| 适用场景 | 全功能NL2SQL引擎，支持复杂多表查询、性能优化、查询解释与替代方案生成。面向 | 通用场景 | 通用场景 |
## 协助指南
### Q1: 自然语言转SQL专业版支持哪些输入格式？

A1: 全功能NL2SQL引擎，支持复杂多表查询、性能优化、查询解释与替代方案生成。面向数据工程师与DBA的全功能自然语言转SQL引擎，支持复杂多表关联、窗口函数、查询。支持文本指令和结构化参数输入，具体格式参考使用流程章节。

### Q2: 需要配置API Key吗？

A2: 是的，部分功能需要配置对应平台的API Key。请在依赖说明章节查看具体要求，并通过环境变量安全配置。

### Q3: 命令行执行失败怎么办？

A3: 检查命令参数是否正确，确认运行环境支持exec能力。如遇权限问题，请参照错误处理章节排查。
## 错误恢复方案
针对自然语言转SQL专业版使用中可能遇到的常见问题,提供以下排查方案:

| 错误类型 | 原因分析 | 解决方案 |
|---------|---------|---------|
| API认证失败(401) | API密钥错误或过期 | 检查密钥配置,重新生成token |
| 接口限流(429) | 请求频率超出限制 | 降低调用频率,启用重试退避策略 |
| 响应超时(504) | 网络延迟或服务端负载过高 | 增加超时阈值,检查网络连接 |
| 文件不存在 | 路径错误或文件未创建 | 检查路径拼写,确认文件已生成 |
| 文件格式不支持 | 扩展名不在支持列表中 | 转换为支持的格式后重试 |
| 权限不足 | 当前用户无读写权限 | 检查文件权限,以管理员身份运行 |
| 命令执行失败 | 参数错误或环境依赖缺失 | 检查命令语法,确认依赖已安装 |
| 进程超时 | 命令执行时间过长 | 增加超时设置,优化命令参数 |
| 网络连接失败 | DNS解析失败或防火墙拦截 | 检查网络配置,确认代理设置 |

### 自然语言转SQL专业版通用排查步骤

1. **检查输入参数**: 确认所有必填参数已提供且格式正确
2. **查看日志输出**: 定位具体错误行和异常类型
3. **验证环境配置**: 确认依赖库版本和运行环境满足要求
4. **逐步调试**: 缩小问题范围,隔离故障模块

## 用户常见咨询
## 异常恢复方案
针对自然语言转SQL专业版使用中可能遇到的常见问题,提供以下排查方案:

| 错误类型 | 原因分析 | 解决方案 |
|---------|---------|---------|
| API认证失败(401) | API密钥错误或过期 | 检查密钥配置,重新生成token |
| 接口限流(429) | 请求频率超出限制 | 降低调用频率,启用重试退避策略 |
| 响应超时(504) | 网络延迟或服务端负载过高 | 增加超时阈值,检查网络连接 |
| 文件不存在 | 路径错误或文件未创建 | 检查路径拼写,确认文件已生成 |
| 文件格式不支持 | 扩展名不在支持列表中 | 转换为支持的格式后重试 |
| 权限不足 | 当前用户无读写权限 | 检查文件权限,以管理员身份运行 |
| 命令执行失败 | 参数错误或环境依赖缺失 | 检查命令语法,确认依赖已安装 |
| 进程超时 | 命令执行时间过长 | 增加超时设置,优化命令参数 |
| 网络连接失败 | DNS解析失败或防火墙拦截 | 检查网络配置,确认代理设置 |
