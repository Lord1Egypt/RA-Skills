---
name: test-engineer
description: |
  数据仓库测试工程师 - 端到端数据仓库测试工作流。
  包含单元测试、集成测试、性能测试三大核心功能。
  当用户需要验证数据仓库质量、执行回归测试、性能基准测试时触发。
  触发词：单元测试、集成测试、性能测试、回归测试、数据验证、测试用例。
---

# 数据仓库测试工程师

端到端数据仓库测试工作流。三个阶段：单元测试 → 集成测试 → 性能测试。

## 架构概览

```
┌─────────────────────────────────────────────────────────────────────┐
│                        数据仓库测试工程师架构                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   输入: dq_package.yaml + 数据模型                                  │
│      │                                                             │
│      ▼                                                             │
│   ┌────────────────────────────────────────────────────┐          │
│   │  阶段1: 单元测试 (unit-test)                        │          │
│   │  Agent: general-purpose                             │          │
│   │  功能：验证单个组件                                 │          │
│   │        - 模型schema验证                             │          │
│   │        - 数据质量断言                               │          │
│   │        - 业务逻辑验证                               │          │
│   │        - 边界条件测试                               │          │
│   └────────────────────┬───────────────────────────────┘          │
│                        │                                           │
│                        ▼                                           │
│   ┌────────────────────────────────────────────────────┐          │
│   │  阶段2: 集成测试 (integration-test)                 │          │
│   │  Agent: general-purpose                             │          │
│   │  功能：验证跨组件数据流                             │          │
│   │        - ETL Pipeline端到端测试                     │          │
│   │        - 血缘数据一致性验证                         │          │
│   │        - SCD2历史追踪验证                           │          │
│   │        - 汇总计算正确性                             │          │
│   └────────────────────┬───────────────────────────────┘          │
│                        │                                           │
│                        ▼                                           │
│   ┌────────────────────────────────────────────────────┐          │
│   │  阶段3: 性能测试 (performance-test)                 │          │
│   │  Agent: general-purpose                             │          │
│   │  功能：性能基准与优化建议                           │          │
│   │        - 查询性能测试                               │          │
│   │        - ETL执行时长基准                            │          │
│   │        - 并发压力测试                               │          │
│   │        - 资源使用分析                               │          │
│   └────────────────────────────────────────────────────┘          │
│                                                                     │
│   输出: test_package.yaml (供上线部署使用)                           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## 参考资料导航

| 何时读取 | 文件 | 内容 | 场景 |
|---------|------|------|------|
| 设计测试策略时 | [references/test-standards.md](references/test-standards.md) | 测试金字塔、命名规范、断言库 | 规划测试覆盖范围 |
| 编写断言语句时 | [references/test-standards.md](references/test-standards.md) | 断言最佳实践、容忍度设置 | 需要清晰错误信息 |
| 设置覆盖率标准时 | [references/test-standards.md](references/test-standards.md) | 覆盖率要求、豁免规则 | 定义最低覆盖率 |
| 查看示例时 | [examples/](examples/) 目录 | 典型测试场景 | 学习测试写法 |

---

## 示例快速索引

| 需求场景 | 推荐命令 | 上游输入 | 详情位置 |
|----------|----------|----------|----------|
| 基于质量规则测试 | `/unit-test --from-dq` | dq_package.yaml | [上游输入](#上游输入) |
| 基于Pipeline测试 | `/integration-test --from-etl` | etl_package.yaml | [上游输入](#上游输入) |
| 验证查询性能 | `/performance-test --from-sql` | sql_package.yaml | [上游输入](#上游输入) |
| 端到端完整测试 | `/test-engineer 端到端测试...` | 所有上游包 | [方式2](#方式2端到端工作流) |
| 部署前验证 | 检查 test_package.yaml | test_package.yaml | [下游联动](#与下游-skill-的联动) |

## 快速开始

### 方式1：分阶段使用（推荐）

```bash
# 阶段1：单元测试
/unit-test 为fct_order_items表生成单元测试

# 阶段2：集成测试
/integration-test 验证DWD到DWS的数据一致性

# 阶段3：性能测试
/performance-test 测试销售日报查询性能
```

### 方式2：端到端工作流

```bash
# 启动完整测试工作流
/test-engineer 端到端测试电商销售分析数仓
```

## 核心功能详解

### 功能1：单元测试生成器 (/unit-test)

**Agent类型**：general-purpose
**工具权限**：Read, Grep, Glob, Edit, Write, Bash

**使用场景**：
- 新模型上线前的验证
- 模型变更后的回归测试
- 数据质量规则验证

**输入格式**：
```
/unit-test [测试对象] [测试类型]
```

**测试类型**：
| 类型 | 说明 | 示例 |
|------|------|------|
| schema | schema验证 | 字段存在性、类型匹配 |
| not_null | 非空验证 | 主键、必填字段 |
| unique | 唯一性验证 | 主键、业务键 |
| relationship | 外键验证 | 维度表关联 |
| accepted_values | 枚举值验证 | 状态字段 |
| custom | 自定义SQL验证 | 业务逻辑 |

**示例**：
```
/unit-test 表: fct_order_items
测试内容:
- 代理键唯一性
- 维度外键有效性
- 金额计算正确性 (paid_amount = item_amount - discount_amount)
- 时间范围合理性
```

**输出**：
- pytest测试脚本 (.py)
- 测试数据 fixtures
- 执行报告

---

### 功能2：集成测试生成器 (/integration-test)

**Agent类型**：general-purpose
**工具权限**：Read, Grep, Glob, Edit, Write, Bash

**使用场景**：
- ETL Pipeline验证
- 跨层级数据一致性
- SCD2历史追踪验证
- 端到端数据流测试

**输入格式**：
```
/integration-test [测试场景]
```

**测试场景**：
1. **ETL Pipeline测试**
   - ODS→DWD数据完整性
   - DWD→FCT转换正确性
   - FCT→DWS汇总准确性

2. **SCD2验证**
   - 历史记录保留
   - 当前记录标记
   - 时间范围连续性

3. **血缘一致性**
   - 上下游数据量匹配
   - 金额汇总一致性
   - 维度属性传递

**示例**：
```
/integration-test 场景: DWD到DWS汇总对账
验证:
- DWD.paid_amount总和 = DWS.gmv
- 按日期+省份+用户等级分组验证
- 容忍度: 0.1%
```

**输出**：
- 集成测试脚本
- 测试数据集
- 对账SQL

---

### 功能3：性能测试生成器 (/performance-test)

**Agent类型**：general-purpose
**工具权限**：Read, Grep, Glob, Edit, Write, Bash

**使用场景**：
- 查询性能基准
- ETL执行时长监控
- 并发压力测试
- 资源使用分析

**输入格式**：
```
/performance-test [测试目标] [基准要求]
```

**测试维度**：
| 维度 | 指标 | 目标值 |
|------|------|--------|
| 查询响应 | P50/P95/P99 | <3s/<5s/<10s |
| ETL执行 | 总时长 | 按SLA要求 |
| 并发能力 | QPS | 按业务需求 |
| 资源使用 | CPU/Memory | <80% |

**示例**：
```
/performance-test 目标: ADS层销售日报查询
基准:
- P50 < 2秒
- P95 < 5秒
- 并发10用户
- 数据量: 1年历史
```

**输出**：
- 性能测试脚本
- 基准报告
- 优化建议

---

## 标准输出格式

每个测试任务输出标准化的 `test_package.yaml`：

```yaml
test_package:
  version: "1.0"
  metadata:
    generated_by: "test-engineer"
    generated_at: "2024-01-15T10:00:00Z"
    target_project: "project_name"
    upstream_packages:
      - "dq_package.yaml"
      - "etl_package.yaml"

  test_suites:
    unit_tests:
      - name: "test_fct_orders_schema"
        file: "unit/test_fct_orders.py"
        status: "passed|failed|pending"
        coverage: 95
      - name: "test_dim_user_scd2"
        file: "unit/test_dim_user.py"
        status: "passed"

    integration_tests:
      - name: "test_ods_to_dwd_pipeline"
        file: "integration/test_pipeline_orders.py"
        status: "passed"
        duration: "45s"

    performance_tests:
      - name: "test_sales_report_query_perf"
        file: "performance/test_query_perf.py"
        status: "passed"
        metrics:
          p50: "1.2s"
          p95: "3.5s"
          p99: "5.1s"

  summary:
    total_tests: 25
    passed: 24
    failed: 1
    skipped: 0
    overall_status: "failed"  # 任何失败即失败
    block_deployment: true    # 是否阻塞部署

  reports:
    html_report: "reports/2024-01-15/report.html"
    junit_xml: "reports/2024-01-15/junit.xml"
    coverage_report: "reports/2024-01-15/coverage.html"

  downstream_specs:
    - target: "deployment-assistant"  # 或 release-manager
      input_file: "test_package.yaml"
      conditions:
        - "overall_status == 'passed'"
        - "block_deployment == false"
```

---

## 上游输入

本 Skill 可消费以下标准包自动生成测试：

| 来源 Skill | 输入文件 | 自动生成的测试 | 触发命令 |
|-----------|----------|----------------|----------|
| dq-assistant | dq_package.yaml | 基于 rules 的数据质量单元测试 | `/unit-test --from-dq` |
| etl-assistant | etl_package.yaml | 基于 pipeline 的集成测试 | `/integration-test --from-etl` |
| sql-assistant | sql_package.yaml | 基于 query 的性能测试 | `/performance-test --from-sql` |
| modeling-assistant | modeling_package.yaml | 基于 schema 的模型测试 | `/unit-test --from-model` |

### 基于上游包的自动测试生成

```bash
# 方式1: 显式引用上游包
/unit-test 基于 dq_package.yaml 生成单元测试

# 方式2: 自动发现上游包
/unit-test --auto  # 自动查找 outputs/ 中的上游包并生成对应测试
```

---

## 与下游 Skill 的联动

测试完成后，自动触发部署流程：

```bash
## 测试通过后的下一步

# 步骤1: 部署准备（如果测试通过）
/deployment-assistant 基于以下测试包准备部署：
- 测试文件: outputs/test_package.yaml
- 检查项:
  - overall_status == "passed"
  - 关键路径测试全部通过
  - 覆盖率 > 80%

# 步骤2: 生成部署报告
/deployment-assistant 生成部署检查清单：
- 代码变更: [diff summary]
- 测试结果: [test summary]
- 回滚方案: [rollback plan]
```

---

## 配合使用流程

```
数据质量包 (dq_package.yaml)
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│  阶段1: 单元测试 (/unit-test)                                │
│  ├─ 输入: 表Schema、质量规则                                 │
│  ├─ 处理: general-purpose Agent                             │
│  └─ 输出: pytest单元测试脚本                                 │
│       - schema验证                                           │
│       - 数据质量断言                                         │
│       - 边界条件测试                                         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  阶段2: 集成测试 (/integration-test)                         │
│  ├─ 输入: ETL Pipeline定义、血缘关系                         │
│  ├─ 处理: general-purpose Agent                             │
│  └─ 输出: 集成测试脚本                                       │
│       - Pipeline端到端测试                                   │
│       - 跨层级对账验证                                       │
│       - SCD2历史追踪验证                                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  阶段3: 性能测试 (/performance-test)                         │
│  ├─ 输入: 查询SQL、ETL配置、性能目标                         │
│  ├─ 处理: general-purpose Agent                             │
│  └─ 输出: 性能基准报告                                       │
│       - 查询性能指标                                         │
│       - ETL执行时长                                          │
│       - 优化建议                                             │
└─────────────────────────────────────────────────────────────┘
                     │
                     ▼
              test_package.yaml
                     │
                     ▼
              上线部署阶段
```

---

## 项目初始化

为团队建立标准化测试工作流：

```bash
# 创建测试项目骨架
bash .claude/skills/test-engineer/scripts/init-project.sh ./test-project "电商数仓测试"
```

自动生成：
```
test-project/
├── PROJECT.md          # 项目中枢（测试清单+进度+规范）
├── standards.md        # 团队测试规范
├── unit/               # 单元测试
│   ├── test_dim_*.py   # 维度表测试
│   ├── test_fct_*.py   # 事实表测试
│   └── fixtures/       # 测试数据
├── integration/        # 集成测试
│   ├── test_pipeline_*.py
│   └── test_reconciliation_*.py
├── performance/        # 性能测试
│   ├── test_query_perf.py
│   └── test_etl_perf.py
├── reports/            # 测试报告
│   └── YYYY-MM-DD/
└── README.md
```

---

## 测试金字塔

```
                    ┌─────────┐
                    │  UI测试 │  ← 少量 (可选)
                   ┌┴─────────┴┐
                   │ 集成测试  │  ← 中等 (Pipeline验证)
                  ┌┴───────────┴┐
                  │   单元测试   │  ← 大量 (模型验证)
                 ┌┴─────────────┴┐
                 │   数据质量     │  ← Great Expectations
                 └───────────────┘
```

### 各层比例建议
| 层级 | 比例 | 执行频率 |
|------|------|----------|
| 数据质量 | 40% | 每次ETL后 |
| 单元测试 | 35% | 模型变更时 |
| 集成测试 | 20% | 每日/发布前 |
| UI测试 | 5% | 发布前 |

---

## 最佳实践

### 1. 测试数据管理

**Fixture策略**：
```python
# conftest.py
@pytest.fixture
def sample_orders():
    """标准测试订单数据"""
    return pd.DataFrame({
        'order_id': [1, 2, 3],
        'user_id': [101, 102, 103],
        'total_amount': [100.0, 200.0, 300.0],
        'status': ['paid', 'completed', 'cancelled']
    })
```

**数据隔离**：
- 使用独立测试Schema
- 测试后清理数据
- 避免污染生产数据

### 2. 测试命名规范

```
测试文件: test_{layer}_{table_name}.py
测试函数: test_{scenario}_{expected_behavior}

示例:
- test_fct_order_items.py
- test_dws_trade_summary_reconciliation.py
def test_paid_amount_calculation_should_be_correct():
def test_scd2_should_track_user_level_changes():
```

### 3. 断言规范

```python
# 好的断言 - 清晰的失败信息
assert actual_gmv == expected_gmv, \
    f"GMV mismatch: expected {expected_gmv}, got {actual_gmv}, diff={actual_gmv-expected_gmv}"

# 容忍度断言
assert abs(diff_rate) < 0.001, \
    f"Reconciliation diff {diff_rate:.4%} exceeds tolerance 0.1%"
```

---

## 故障排除

### 测试执行失败
1. 检查数据库连接配置
2. 确认测试Schema存在
3. 验证测试数据fixtures

### 集成测试数据不一致
1. 检查ETL执行状态
2. 验证源数据时间范围
3. 排查SCD2处理逻辑

### 性能测试不达标
1. 检查查询执行计划
2. 验证索引有效性
3. 考虑数据分区策略

---

## 路线图

### v1.0.0 (当前)
- ✅ 单元测试生成器 (unit-test)
- ✅ 集成测试生成器 (integration-test)
- ✅ 性能测试生成器 (performance-test)
- ✅ pytest集成

### v1.1.0 (计划)
- 🔄 自动化测试发现
- 🔄 测试覆盖率报告
- 🔄 CI/CD集成

### v2.0.0 (计划)
- 📝 智能测试用例推荐
- 📝 历史测试趋势分析
- 📝 自动回归测试选择

---

## 与其他Skill联动

### 上游输入

| Skill | 传递内容 | 使用场景 |
|-------|----------|----------|
| **dq-assistant** | quality_rules, table_schemas | 基于质量规则生成单元测试断言 |
| **etl-assistant** | pipeline_code, topology | 基于Pipeline生成集成测试 |
| **sql-assistant** | sql_queries, query_plans | 基于SQL生成性能测试 |
| **modeling-assistant** | model_schemas, lineage | 基于模型生成测试fixtures |

### 下游输出

| Skill | 接收内容 | 使用场景 |
|-------|----------|----------|
| **上线部署** | test_package.yaml | 测试通过后才允许部署 |

### 联动示例

#### 联动1: 数据质量 → 单元测试

```bash
# 先执行数据质量阶段
/dq-assistant 基于ETL包生成质量规则

# 再执行测试阶段，复用质量规则
/unit-test 基于质量规则为fct_order_items生成单元测试
```

**自动传递**：
- dq-assistant 输出: `expectation_suites` (GE规则配置)
- test-engineer 输入: 将GE规则转化为pytest断言

#### 联动2: ETL开发 → 集成测试

```bash
# 先完成ETL开发
/etl-assistant 基于SQL包生成Pipeline

# 再验证Pipeline
/integration-test 验证ODS到DWS的数据一致性
```

**自动传递**：
- etl-assistant 输出: `pipeline_dependencies` (DAG依赖关系)
- test-engineer 输入: 生成对应的集成测试场景

#### 联动3: SQL开发 → 性能测试

```bash
# 先生成分析查询
/sql-gen 生成销售日报查询SQL

# 再测试性能
/performance-test 验证该查询性能是否达标
```

**自动传递**：
- sql-assistant 输出: `query_sql` + `execution_plan`
- test-engineer 输入: 生成性能基准测试

### 完整工作流

```
requirement-analyst
    ↓ [requirement_package.yaml]
architecture-designer
    ↓ [architecture_package.yaml]
modeling-assistant
    ↓ [modeling_package.yaml]
sql-assistant
    ↓ [sql_package.yaml]
etl-assistant
    ↓ [etl_package.yaml]
dq-assistant
    ↓ [dq_package.yaml + schemas]
test-engineer ← 当前阶段
    ↓ [test_package.yaml]
上线部署
```

---

**提示**：本Skill与《AI编程与数据开发工程师融合实战手册》§07 AI辅助测试验证实战章节配套使用。
