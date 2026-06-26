---
name: dq-assistant
description: |
  数据质量检查助手 - 端到端数据质量管理工作流。包含规则生成、质量检查、Schema文档三大核心功能。
  当用户需要建立数据质量监控、执行质量检查、生成数据字典时触发。
  触发词：数据质量、质量检查、数据字典、血缘分析、质量监控。
---

# 数据质量检查助手

从规则定义到质量报告的全流程数据质量管理。三个阶段：规则生成 → 质量检查 → 文档输出。

## 架构概览

```
输入 → [阶段1: 规则生成] → [阶段2: 质量检查] → [阶段3: 文档生成] → 输出
            │                      │                      │
            ▼                      ▼                      ▼
       Agent:通用              Agent:通用              Agent:通用
```

| 阶段 | 命令 | Agent | 功能 |
|------|------|-------|------|
| 1 | /dq-rule-gen | general-purpose | 基于表结构自动生成质量规则 |
| 2 | /dq-check | general-purpose | 执行质量检查并生成报告 |
| 3 | /schema-doc | general-purpose | 生成数据字典和血缘文档 |

**输入**: etl_package.yaml / modeling_package.yaml / sql_package.yaml（可选）  
**输出**: dq_package.yaml（驱动下游测试）

## 参考资料导航

| 何时读取 | 文件 | 内容 | 场景 |
|---------|------|------|------|
| 设计质量规则时 | [references/data-quality-standards.md](references/data-quality-standards.md) | 质量维度、规则库、评分标准 | 建立质量监控体系 |
| 处理异常数据时 | [references/data-quality-standards.md](references/data-quality-standards.md) | 常见模式、修复建议 | 质量问题排查 |
| 查看示例时 | [examples/](examples/) 目录 | 典型场景的输入输出示例 | 学习使用方法 |
| 生成数据字典时 | [references/data-quality-standards.md](references/data-quality-standards.md) | 血缘分析规范 | 文档输出 |

---

## 示例快速索引

| 需求场景 | 推荐命令 | 详情位置 |
|----------|----------|----------|
| 为新表建立质量规则 | `/dq-rule-gen [表结构]` | [功能1](#功能1质量规则生成器-dq-rule-gen) |
| 执行质量检查 | `/dq-check [表名]` | [功能2](#功能2质量检查执行器-dq-check) |
| 生成数据字典 | `/schema-doc [表名]` | [功能3](#功能3schema文档生成器-schema-doc) |
| 端到端质量体系建设 | `/dq-assistant 建立监控体系...` | [方式2](#方式2端到端工作流) |
| 基于检查结果生成测试 | 调用 `/test-engineer` | [下游联动](#与下游-skill-的联动) |

## 快速开始

### 方式1：分阶段使用（推荐）

```bash
# 阶段1: 生成质量规则
/dq-rule-gen 为orders表生成质量检查规则，包含字段：order_id,user_id,total_amount,status,created_at

# 阶段2: 执行质量检查
/dq-check 对orders表执行全量质量检查

# 阶段3: 生成Schema文档
/schema-doc 生成orders表的完整数据字典，包含样例数据和质量评分
```

### 方式2：端到端工作流

```bash
# 启动完整数据质量管理工作流
/dq-assistant 为users表建立完整的质量监控体系
```

## 核心功能详解

### 功能1：质量规则生成器 (/dq-rule-gen)

**Agent类型**：general-purpose
**工具权限**：Read, Grep, Glob, Edit, Write, Bash

**使用场景**：
- 新表上线前建立质量规则
- 批量生成质量检查SQL
- 建立质量监控体系

**输入格式**：
```
/dq-rule-gen [表结构描述或DDL语句]
```

**输出内容**：
- YAML格式规则定义
- 可执行的SQL检查脚本
- 规则优先级建议

**示例**：
```
/dq-rule-gen
表名：users
字段：
- id (BIGINT, PK): 用户ID
- email (VARCHAR): 邮箱
- phone (VARCHAR): 手机号
- status (VARCHAR): 状态(active/inactive)
- created_at (TIMESTAMP): 创建时间
```

**生成规则示例**：
```yaml
rules:
  - rule_id: COMP_001
    name: email_必填检查
    dimension: 完整性
    severity: 高
    sql: SELECT COUNT(*) FROM users WHERE email IS NULL

  - rule_id: VALID_001
    name: email_格式检查
    dimension: 有效性
    severity: 中
    sql: SELECT COUNT(*) FROM users WHERE email NOT LIKE '%@%.%'

  - rule_id: UNIQ_001
    name: email_唯一性检查
    dimension: 唯一性
    severity: 高
    sql: SELECT email, COUNT(*) FROM users GROUP BY email HAVING COUNT(*) > 1
```

---

### 功能2：质量检查执行器 (/dq-check)

**Agent类型**：general-purpose
**工具权限**：Read, Grep, Glob, Edit, Write, Bash

**使用场景**：
- 日常质量监控
- 数据上线前检查
- 质量问题排查

**输入格式**：
```
/dq-check [表名] [检查模式] [可选：规则文件]
```

**检查模式**：
- `全量检查` - 检查所有规则（默认）
- `快速检查` - 只检查完整性+唯一性
- `增量检查` - 只检查新增数据
- `专项检查` - 针对特定维度

**输出内容**：
- 各维度检查明细
- 综合质量评分
- 问题汇总与修复SQL
- 趋势对比（如有历史）

**报告示例**：
```
============================================================
数据质量检查报告 - orders表
============================================================
检查时间: 2025-03-17 10:30:00
规则数量: 12

【综合评分】
完整性:    98.5/100  🟡
唯一性:   100.0/100  🟢
有效性:    99.8/100  🟢
一致性:    99.9/100  🟢
------------------------------------------------------------
综合评分:  99.6/100  🟢 良好
------------------------------------------------------------

【发现问题】
❌ VALID_002 status枚举检查 (23条异常)
⚠️ COMP_003 paid_at非空检查 (1500条空值)

【修复建议】
1. 查看异常记录：
   SELECT * FROM orders WHERE status NOT IN (...)

2. 修复异常值：
   UPDATE orders SET status='pending' WHERE status='unknown'
```

---

### 功能3：Schema文档生成器 (/schema-doc)

**Agent类型**：general-purpose
**工具权限**：Read, Grep, Glob, Edit, Write, Bash

**使用场景**：
- 生成数据字典
- 数据血缘分析
- 新成员 onboarding

**输入格式**：
```
/schema-doc [表名或表列表] [选项]
```

**选项**：
- `--include-samples` - 包含样例数据
- `--include-stats` - 包含统计信息
- `--include-lineage` - 包含血缘关系
- `--include-quality` - 包含质量评分
- `--format=markdown|html` - 输出格式

**输出内容**：
- 表基础信息
- 字段详细说明
- 索引和约束
- 数据血缘关系
- 样例数据
- 质量概览

**文档示例**：
```markdown
# 数据表: orders

## 基本信息
| 属性 | 值 |
|------|-----|
| 表名 | orders |
| 记录数 | 1,234,567 |
| 数据大小 | 256 MB |
| 质量评分 | 99.6% 🟢 |

## 字段说明
| 字段名 | 类型 | 可空 | 主键 | 外键 | 说明 |
|--------|------|------|------|------|------|
| id | BIGINT | NO | PK | - | 订单ID |
| user_id | BIGINT | NO | - | FK | 关联users表 |
| status | VARCHAR | NO | - | - | 订单状态 |

## 数据血缘
### 上游
- users.user_id (1:N)

### 下游
- report_daily_sales (订单统计)
```

---

## 上游输入

本 Skill 可消费以下标准包自动识别需要检查的表：

| 来源 Skill | 输入文件 | 关键字段 | 使用方式 |
|-----------|----------|----------|----------|
| etl-assistant | etl_package.yaml | pipeline.target_tables | 自动为ETL目标表生成质量规则 |
| modeling-assistant | modeling_package.yaml | schemas | 基于模型Schema生成字段级规则 |
| sql-assistant | sql_package.yaml | content.tables_involved | 为SQL涉及表生成检查规则 |
| architecture-designer | architecture_package.yaml | layers.ads | 为应用层表建立监控 |

### 基于上游包的自动规则生成

```bash
# 方式1: 显式引用上游包
/dq-rule-gen 基于 etl_package.yaml 为所有目标表生成质量规则

# 方式2: 自动发现上游包
/dq-rule-gen --auto  # 自动查找 outputs/ 中的上游包并生成对应规则
```

---

## 标准输出格式

每个数据质量任务输出标准化的 `dq_package.yaml`，便于下游 Skill 消费：

```yaml
dq_package:
  version: "1.0"
  metadata:
    generated_by: "dq-assistant"
    generated_at: "2024-01-15T10:00:00Z"
    target_table: "table_name"
    check_scope: "full|incremental"

  rules:
    - rule_id: "COMP_001"
      name: "email_必填检查"
      dimension: "完整性"
      severity: "高"
      sql: "SELECT COUNT(*) FROM users WHERE email IS NULL"
      threshold: 0

    - rule_id: "VALID_001"
      name: "email_格式检查"
      dimension: "有效性"
      severity: "中"
      sql: "SELECT COUNT(*) FROM users WHERE email NOT LIKE '%@%.%'"
      threshold: 0.01

  check_results:
    check_time: "2024-01-15T10:00:00Z"
    overall_score: 99.6
    dimensions:
      完整性: 98.5
      唯一性: 100.0
      有效性: 99.8
      一致性: 99.9
    violations:
      - rule_id: "VALID_002"
        count: 23
        sample_values: ["unknown", "null"]
    recommendations:
      - "修复 status 异常值"
      - "补充 paid_at 缺失数据"

  data_dictionary:
    table_name: "users"
    record_count: 1234567
    quality_score: 99.6
    columns:
      - name: "id"
        type: "BIGINT"
        nullable: false
        primary_key: true
        description: "用户ID"

  downstream_specs:
    - target: "test-engineer"
      input_file: "dq_package.yaml"
      mapping:
        - "rules → test_assertions"
        - "violations → test_cases"
```

---

## 与下游 Skill 的联动

数据质量检查完成后，自动触发下游 Skill：

```bash
## 质量检查后的下一步

# 步骤1: 生成数据测试（推荐）
/test-engineer 基于以下质量规则生成测试用例：
- 规则文件: outputs/dq_package.yaml
- 测试类型: 数据质量测试、回归测试
- 重点: violations 中发现的异常模式

# 步骤2: 更新数据文档
/modeling-assistant 基于质量检查结果更新：
- 数据血缘: 问题数据的上游来源
- 模型文档: 字段质量评分说明
```

---

## 配合使用流程

```
新表上线流程:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Schema设计评审
        │
        ▼
2. 规则生成 (/dq-rule-gen)
   └─ 自动生成质量检查规则
   └─ 输出 dq_package.yaml
        │
        ▼
3. 初始数据加载
        │
        ▼
4. 质量检查 (/dq-check)
   └─ 执行全量质量检查
   └─ 更新 dq_package.yaml 的 check_results
   └─ 确认无严重问题
        │
        ▼
5. 文档生成 (/schema-doc)
   └─ 生成数据字典
   └─ 更新 dq_package.yaml 的 data_dictionary
        │
        ▼
6. 测试生成（联动 /test-engineer）
   └─ 基于质量规则生成测试用例
        │
        ▼
7. 上线发布
   └─ 配置定期质量监控
   └─ 接入告警系统

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

日常监控流程:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

定时任务 /dq-check 快速检查
        │
        ├─ 🟢 通过 → 记录日志 → 更新 dq_package.yaml
        │
        └─ 🔴 异常 → 告警通知
                   │
                   ▼
              人工介入排查
                   │
                   ▼
              修复数据问题
                   │
                   ▼
              重新检查验证 → 更新 dq_package.yaml

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 项目初始化

为团队建立标准化数据质量管理工作流：

```bash
# 创建数据质量管理项目
bash .claude/skills/dq-assistant/scripts/init-project.sh ./dq-project "电商数据质量"
```

自动生成：
```
dq-project/
├── PROJECT.md          # 项目中枢（表清单+规则+进度）
├── standards.md        # 团队数据规范
├── rules/              # 质量规则文件
│   ├── users_rules.yaml
│   ├── orders_rules.yaml
│   └── ...
├── reports/            # 质量报告存档
│   └── YYYY-MM/        # 按月归档
├── docs/               # 数据字典
│   ├── users.md
│   ├── orders.md
│   └── ...
└── scripts/            # 检查脚本
    └── run_checks.sh
```

---

## 多Agent协作

复杂数据质量管理任务可拆分为多Agent并行：

```
协调Agent (主会话)
    │
    ├─► dq-rule-gen Agent #1 ──► 生成表A规则
    ├─► dq-rule-gen Agent #2 ──► 生成表B规则
    ├─► dq-rule-gen Agent #3 ──► 生成表C规则
    │
    ▼ (收集所有规则)
    │
    ├─► dq-check Agent #1 ──► 检查表A
    ├─► dq-check Agent #2 ──► 检查表B
    ├─► dq-check Agent #3 ──► 检查表C
    │
    ▼ (汇总检查结果)
    │
    └─► 生成整体质量报告
```

启动并行检查：
```
/dq-assistant 并行检查所有核心表的质量状态
表列表: users,orders,products,payments,shipments
```

---

## 最佳实践

### 1. 规则设计原则

**高优先级规则**（必须100%通过）：
- 主键非空且唯一
- 外键关联有效性
- 核心业务字段非空

**中优先级规则**（允许<5%异常）：
- 格式规范（邮箱、手机号）
- 枚举值有效性
- 数值范围

**低优先级规则**（允许<10%异常）：
- 描述字段长度
- 可选字段完整性

### 2. 检查频率建议

| 表类型 | 检查模式 | 频率 |
|--------|----------|------|
| 核心交易表 | 全量检查 | 每日 |
| 核心维度表 | 快速检查 | 每日 |
| 日志表 | 抽样检查 | 每周 |
| 报表表 | 一致性检查 | 每日 |

### 3. 问题修复流程

```
发现问题
    │
    ▼
评估影响范围
    │
    ├─ 影响小 → 记录待修复
    │
    └─ 影响大 → 立即处理
              │
              ▼
         确定修复方案
              │
              ▼
         测试环境验证
              │
              ▼
         生产环境执行
              │
              ▼
         重新检查验证
```

---

## 故障排除

### Skill未触发
1. 检查skill文件路径是否正确
2. 确认Frontmatter格式正确
3. 重启Claude Code

### 规则生成不准确
1. 提供更详细的字段业务说明
2. 明确指定字段的枚举值范围
3. 说明字段间的业务关系

### 检查执行失败
1. 确认数据库连接权限
2. 检查表名和字段名是否正确
3. 大数据量表建议使用增量检查

---

## 示例场景

详见 [examples/](examples/) 目录：

| 示例 | 场景 | 流程 |
|------|------|------|
| example-ecommerce-dq.md | 电商数据质量管理 | 规则生成 → 质量检查 → 文档输出 |
| example-lineage-analysis.md | 数据血缘分析 | 多表血缘识别与可视化 |

---

## 路线图

### v1.0.0 (当前)
- ✅ 质量规则生成器 (dq-rule-gen)
- ✅ 质量检查执行器 (dq-check)
- ✅ Schema文档生成器 (schema-doc)
- ✅ 六维度质量评估

### v1.1.0 (计划)
- 🔄 质量趋势分析（历史对比）
- 🔄 智能异常检测（基于统计）
- 🔄 质量规则市场（共享规则模板）

### v2.0.0 (计划)
- 📝 实时质量监控（流式检查）
- 📝 自动修复建议（AI驱动）
- 📝 与Airflow/dbt集成

---

**提示**：本Skill与《AI编程与数据开发工程师融合实战手册》§06 数据Pipeline与仓库建模章节配套使用。
