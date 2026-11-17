---
name: zentao-work-stats
description: 禅道(Zentao)用户工作内容分析工具。通过数据库只读查询分析指定用户在指定时间段内的需求、任务、Bug、工时日志，生成 Markdown 格式的工作报告。仅支持 SQL SELECT 查询，不修改任何数据。
---

# zentao-work-stats — 禅道用户工作内容分析报告生成器

> 连接禅道数据库，通过主表 + zt_action 操作日志综合追踪指定用户在指定时间段内的所有工作内容，生成完整的分析报告。

## 激活条件

**高优先级触发**（明确的统计生成动作）:
- "生成禅道用户工作报告"
- "创建禅道工作统计"
- "输出禅道工作分析报告"

**低优先级触发**（需要确认意图）:
- "分析禅道中某用户的需求/任务/Bug完成情况"（必须指定用户和时间范围）

**不触发的情况**:
- ❌ "查看某人在禅道中做了哪些事"（只是询问，不是生成报告）
- ❌ "这个人在禅道的工作怎么样"（只是询问评价）
- ❌ "禅道统计"（没有明确分析动作）

**激活前必须确认**:
1. 目标用户账号（如 `WHF01089`）
2. 分析的时间范围（如 `2026年`、`2026-01-01 到 2026-07-23`）
3. 用户是否有数据库访问权限

## 核心原则

**只读操作** — 所有数据库操作均为 SELECT 查询，严禁任何 INSERT/UPDATE/DELETE。

**双表追踪** — 不能仅查主表（zt_story/zt_task/zt_bug），必须结合 `zt_action` + `zt_history` 操作日志表，才能完整追踪用户参与的所有记录。原因：禅道流程流转后，主表的 `assignedTo` 等字段可能变为 `closed` 等非用户值，导致遗漏。

**先确认后生成** — 分析前需确认以下信息：
1. 目标用户账号（如 `WHF01089`）
2. 分析的时间范围（如 `2026年`、`2026-01-01 到 2026-07-23`）
3. 报告输出路径（默认当前工作目录）

## 数据库连接配置

从 `config.json` 读取连接信息。配置文件路径：与本 SKILL.md 同目录下的 `config.json`。

**重要**：配置文件中包含数据库凭据，请确保：
- 不要将此文件提交到公共代码仓库
- 使用环境变量或配置管理工具存储敏感信息
- 确保文件权限设置正确，仅限授权用户访问

## 安全和隐私警告

⚠️ **数据敏感性**：本技能访问禅道数据库中的用户工作数据，包括：
- 个人工作记录（需求、任务、Bug 提交和修改历史）
- 工时日志和工作效率数据
- 跨表关联的用户活动轨迹

⚠️ **授权要求**：
- 必须获得用户本人或管理层的明确授权才能分析其工作数据
- 不得用于未经授权的员工监控或绩效评估
- 遵守组织的数据隐私政策和相关法律法规（如 GDPR、个人信息保护法）

⚠️ **报告安全**：
- 生成的报告包含敏感的个人工作信息
- 保存到本地磁盘后，请确保存储位置安全
- 不要通过不安全渠道分享报告
- 及时清理不再需要的报告文件

⚠️ **最小权限原则**：
- 使用只读数据库账号（仅需 SELECT 权限）
- 仅查询必要的表和时间范围
- 避免收集超出分析需求的额外信息

## 禅道核心表说明

### 主表（存储当前状态）

| 表名 | 用途 | 关键字段 |
|------|------|---------|
| `zt_story` | 需求主表 | id, title, pri, status, stage, estimate, openedBy, assignedTo, closedBy |
| `zt_task` | 任务主表 | id, name, type, pri, estimate, consumed, `left`, status, openedBy, assignedTo, finishedBy, closedBy |
| `zt_bug` | Bug主表 | id, title, severity, pri, status, openedBy, assignedTo, resolvedBy, resolution, resolvedDate |
| `zt_effort` | 工时日志表 | id, objectType, objectID, date, consumed, `left`, `work`, account |
| `zt_user` | 用户表 | account, realname, email, dept, role |
| `zt_product` | 产品表 | id, name |
| `zt_execution` | 执行/迭代表 | id, name, project |

### 操作追踪表（存储流转历史，关键！）

| 表名 | 用途 | 关键字段 |
|------|------|---------|
| `zt_action` | 操作日志 | objectType, objectID, actor, action, date, comment |
| `zt_history` | 字段变更明细 | action(关联zt_action.id), field, old, new, diff |

### 操作类型（action字段值）说明

| action 值 | 含义 | 适用对象 |
|-----------|------|---------|
| `opened` | 创建 | story/task/bug |
| `assigned` | 指派 | story/task/bug |
| `started` | 开始 | task/bug |
| `finished` | 完成 | task |
| `resolved` | 解决 | bug |
| `closed` | 关闭 | story/task/bug |
| `commented` | 评论 | story/task/bug |
| `edited` | 编辑 | story/task/bug |
| `linked2project` | 关联项目 | story/bug |
| `linked2execution` | 关联执行 | story/task |

## 分析流程

### Step 0: 环境准备

1. 读取 `config.json` 获取数据库连接配置
2. 验证 `pymysql` 是否已安装（不要主动安装，如果未安装则提示用户自行安装）：
```python
try:
    import pymysql
    print("pymysql 已安装")
except ImportError:
    print("请先安装 pymysql: pip install pymysql")
    raise
```
3. 测试数据库连通性：
```python
import pymysql
conn = pymysql.connect(**db_config)
cursor = conn.cursor()
cursor.execute("SELECT 1")
print("连接成功")
conn.close()
```

### Step 1: 基础信息收集

查询用户基本信息、产品名称、执行名称、用户列表等基础数据：

```python
# 用户信息
cursor.execute("SELECT account, realname, dept, role FROM zt_user WHERE account = %s", (user,))

# 产品映射
cursor.execute("SELECT id, name FROM zt_product")

# 执行映射
cursor.execute("SELECT id, name, project FROM zt_execution")

# 用户映射
cursor.execute("SELECT account, realname FROM zt_user")
```

### Step 2: 通过 zt_action 追踪所有参与记录

**这是核心步骤。** 对 story/task/bug 分别执行：

```python
# 查询用户在指定时间范围内参与的所有对象ID
cursor.execute("""
    SELECT DISTINCT a.objectID
    FROM zt_action a
    WHERE a.actor = %s
      AND a.objectType = %s  -- 'story' / 'task' / 'bug'
      AND a.date >= %s AND a.date <= %s
    ORDER BY a.objectID
""", (user, object_type, start_date, end_date))
```

然后对每个对象ID：
1. 从主表获取完整信息（标题、状态、优先级等）
2. 从 zt_action 获取该用户的所有操作记录
3. 从 zt_history 获取关键字段变更（如状态流转）

### Step 3: 工时日志查询

```python
# 注意 `left` 和 `work` 是 MySQL 保留字，需用反引号转义
cursor.execute("""
    SELECT id, objectType, objectID, date, consumed, `left`, `work`, `begin`, `end`
    FROM zt_effort
    WHERE account = %s AND date >= %s AND date <= %s
    ORDER BY date ASC
""", (user, start_date, end_date))
```

### Step 4: 月度工作量统计

```python
cursor.execute("""
    SELECT DATE_FORMAT(date, '%Y-%m') as month, objectType, action, COUNT(*) as cnt
    FROM zt_action
    WHERE actor = %s AND date >= %s AND date <= %s
    GROUP BY month, objectType, action
    ORDER BY month, objectType
""", (user, start_date, end_date))
```

### Step 5: 生成分析报告

将收集到的数据整理为 Markdown 格式报告，结构参见 [references/report-template.md](references/report-template.md)。

### Step 6: 输出

1. 将报告写入用户指定路径（默认：`{工作目录}/用户{账号}_{年份}年工作分析报告.md`）
2. 向用户展示报告概要统计
3. 使用 present_files 工具展示报告文件

## SQL 注意事项

1. **保留字转义**：`left`、`work`、`begin`、`end` 等是 MySQL 保留字，SQL 中必须用反引号包裹：`` `left` ``、`` `work` ``
2. **时间范围**：使用 `date >= 'YYYY-MM-DD' AND date <= 'YYYY-MM-DD 23:59:59'` 确保包含结束日期当天
3. **deleted 过滤**：主表查询时注意添加 `deleted = '0'` 排除已删除记录
4. **N+1 查询**：先获取 DISTINCT objectID 列表，再逐个查明细，逻辑清晰但查询量较大；如果数据量很大可考虑 JOIN 优化
5. **只读**：所有 SQL 只能是 SELECT，严禁写操作

## 报告生成规则

1. 需求/任务/Bug 列表按优先级排序（pri ASC），同级按 ID 降序
2. 工时日志按日期正序
3. 统计部分包括：总数、完成数、解决率、总工时、平均耗时
4. 标注用户的操作角色（创建者/执行者/指派者/评论者）
5. 产品/执行名称用映射表翻译，不要显示纯数字 ID

## 常见问题

### 为什么主表查到的记录比 zt_action 少很多？

禅道在流程流转时，`assignedTo` 在关闭后会变成 `closed`，不再保留具体用户名。只有通过 `zt_action` 操作日志才能追踪到所有参与人。

### zt_effort 查询报语法错误？

`work`、`left`、`begin`、`end` 是 MySQL 保留字，SQL 中必须用反引号包裹。在 Python 内联字符串中注意反引号转义。

### zt_execution 表不存在？

某些禅道版本可能没有 `zt_execution` 表（旧版使用 `zt_project`），查询前先检查表是否存在，不存在则跳过。

## 版本

| 版本 | 日期 | 作者 | 变更 |
|------|------|------|------|
| 1.0.0 | 2026-07-23 | - | 初始版本，支持通过主表+zt_action双表追踪生成用户工作内容分析报告 |
