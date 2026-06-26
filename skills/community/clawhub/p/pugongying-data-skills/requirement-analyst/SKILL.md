---
name: requirement-analyst
description: |
  数据开发需求分析助手 - 端到端需求分析工作流。将模糊的业务需求转化为结构化的技术规格，
  为后续建模、SQL开发、ETL开发提供清晰输入。
  包含需求解析、需求澄清、需求转化三大核心功能。
  当用户有数据开发需求但不知道如何落地、或需要梳理复杂业务需求时触发。
  触发词：需求分析、业务需求、帮我设计、数据开发需求、需求澄清、需求梳理、需求转化。
---

# 数据开发需求分析助手

从模糊业务需求到可执行技术规格的完整工作流。三个阶段：需求解析 → 需求澄清 → 需求转化。

## 架构概览

```
┌─────────────────────────────────────────────────────────────────────┐
│                     数据开发需求分析助手架构                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   原始业务需求（口语化、模糊、非结构化）                              │
│      │                                                             │
│      ▼                                                             │
│   ┌────────────────────────────────────────────────────┐          │
│   │  阶段1: 需求解析 (requirement-parser)               │          │
│   │  Agent: general-purpose                             │          │
│   │  功能：从原始需求提取结构化信息                      │          │
│   │        - 业务实体识别                               │          │
│   │        - 指标/维度提取                              │          │
│   │        - 数据源推断                                 │          │
│   │        - 技术栈推荐                                 │          │
│   └────────────────────┬───────────────────────────────┘          │
│                        │  [结构化需求描述]                         │
│                        ▼                                           │
│   ┌────────────────────────────────────────────────────┐          │
│   │  阶段2: 需求澄清 (requirement-clarify)              │          │
│   │  Agent: Explore（交互式）                           │          │
│   │  功能：识别需求缺口，生成澄清问题                    │          │
│   │        - 歧义检测                                   │          │
│   │        - 缺失信息识别                               │          │
│   │        - 生成确认清单                               │          │
│   │        - 风险预警                                   │          │
│   └────────────────────┬───────────────────────────────┘          │
│                        │  [经确认的需求规格]                       │
│                        ▼                                           │
│   ┌────────────────────────────────────────────────────┐          │
│   │  阶段3: 需求转化 (requirement-transform)            │          │
│   │  Agent: general-purpose                             │          │
│   │  功能：转化为技术可执行规格                          │          │
│   │        - 数据模型草图                               │          │
│   │        - ETL映射规格                                │          │
│   │        - 质量规则建议                               │          │
│   │        - 下游Skill调用指令                          │          │
│   └────────────────────────────────────────────────────┘          │
│                                                                     │
│   输出: 标准化需求包 (requirement_package.yaml)                      │
│   ──────► 自动传递给 modeling-assistant / sql-assistant 等         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## 参考资料导航

| 需要时读取 | 文件 | 内容 |
|-----------|------|------|
| 需求分析规范 | [references/requirement-standards.md](references/requirement-standards.md) | 需求分类、检查清单、输出规范、术语定义 |
| 使用示例 | [examples/](examples/) 目录 | 典型需求分析场景的完整示例 |

## 项目初始化（推荐）

为团队建立标准化需求分析工作流：

```bash
# 创建需求分析项目骨架
bash .claude/skills/requirement-analyst/scripts/init-project.sh ./data-project "电商销售分析数仓"
```

自动生成目录结构：
```
data-project/
├── PROJECT.md          # 项目中枢（需求清单+进度+规范）
├── requirements/       # 需求文档
│   ├── raw/            # 原始业务需求
│   ├── parsed/         # 解析后的结构化需求
│   └── confirmed/      # 已确认的需求规格
├── specs/              # 技术规格
│   ├── model_spec.yaml # 数据模型规格
│   ├── etl_spec.yaml   # ETL规格
│   └── dq_spec.yaml    # 数据质量规格
├── clarifications/     # 需求澄清记录
└── outputs/            # 最终输出
    └── requirement_package.yaml
```

## 快速开始

### 方式1：分阶段使用（推荐）

```bash
# 阶段1: 需求解析
/requirement-parser 我们需要分析电商销售数据，包括订单、用户、商品，要算销售额、订单量、客单价

# 阶段2: 需求澄清
/requirement-clarify 基于上述解析结果，识别需求缺口

# 阶段3: 需求转化
/requirement-transform 将确认后的需求转化为技术规格
```

### 方式2：端到端工作流

```bash
# 启动完整需求分析工作流
/requirement-analyst 端到端分析：电商销售数据仓库建设需求
```

## 核心功能详解

### 功能1：需求解析助手 (/requirement-parser)

**Agent类型**：general-purpose
**工具权限**：Read, Grep, Glob, Edit, Write, Bash

**使用场景**：
- 业务方提出初步需求，需要结构化梳理
- 需求文档整理和标准化
- 从会议纪要提取数据需求

**输入格式**：
```
/requirement-parser 业务场景描述和需求
```

**解析维度**：

| 维度 | 说明 | 输出示例 |
|------|------|---------|
| **业务实体** | 识别核心数据实体 | `订单`、`用户`、`商品` |
| **业务过程** | 识别业务流程 | `下单`、`支付`、`发货` |
| **分析指标** | 提取可量化指标 | `销售额`、`订单数`、`客单价` |
| **分析维度** | 提取分析视角 | `时间`、`地区`、`用户等级` |
| **数据源** | 推断数据来源 | `业务库`、`埋点日志` |
| **时效要求** | 识别实时性要求 | `T+1`、`准实时`、`实时` |
| **数据量** | 估算数据规模 | `日增100万`、`总量10亿` |
| **用户群体** | 识别使用方 | `管理层`、`分析师`、`运营` |

**输出示例**：
```yaml
# requirements/parsed/requirement_parsed.yaml
version: "1.0"
parse_result:
  business_domain: "电商销售分析"
  business_goal: "监控销售业绩，支持运营决策"

  entities:
    - name: "订单"
      type: "业务实体"
      attributes: ["订单ID", "用户ID", "订单金额", "下单时间", "订单状态"]
    - name: "用户"
      type: "业务实体"
      attributes: ["用户ID", "注册时间", "用户等级", "所在城市"]
    - name: "商品"
      type: "业务实体"
      attributes: ["商品ID", "类目", "品牌", "价格"]

  business_processes:
    - name: "下单"
      entities_involved: ["订单", "用户", "商品"]
    - name: "支付"
      entities_involved: ["订单"]

  metrics:
    - name: "GMV"
      alias: "成交总额"
      formula: "SUM(订单金额)"
      dimensions: ["日期", "地区", "用户等级", "类目"]
      frequency: "每日"
    - name: "订单量"
      formula: "COUNT(DISTINCT 订单ID)"
      dimensions: ["日期", "地区", "类目"]

  data_sources:
    - type: "MySQL"
      system: "订单系统"
      tables: ["orders", "order_items", "users"]
      estimated_size: "日增100万订单"
    - type: "埋点日志"
      system: "行为分析系统"
      format: "JSON"

  requirements:
    freshness: "T+1"
    retention: "3年"
    accuracy: "精确到分"
    users: ["销售运营", "数据分析师", "管理层"]
```

---

### 功能2：需求澄清助手 (/requirement-clarify)

**Agent类型**：Explore
**工具权限**：Read, Grep, Glob

**使用场景**：
- 需求解析后发现信息缺失
- 需要与业务方确认细节
- 风险评估和前置识别

**检查清单模板**：

```yaml
# clarifications/checklist.yaml
clarification_dimensions:
  scope:  # 范围边界
    questions:
      - "数据时间范围？（历史多久，增量还是全量）"
      - "分析粒度要求？（订单级、用户级、商品级）"
      - "是否需要跨系统数据整合？"

  quality:  # 质量要求
    questions:
      - "数据一致性要求？（精确/可接受误差范围）"
      - "异常数据处理策略？（过滤/标记/估算）"
      - "空值/缺省值如何处理？"

  security:  # 安全合规
    questions:
      - "是否有敏感数据？（PII、财务数据）"
      - "数据访问权限如何划分？"
      - "是否需要脱敏/加密？"

  technical:  # 技术约束
    questions:
      - "目标技术栈有偏好？"
      - "现有基础设施约束？"
      - "源系统性能限制？"

  business_rules:  # 业务规则
    questions:
      - "指标计算口径是否有明确定义？"
      - "特殊情况如何处理？（退款、取消订单）"
      - "历史数据变更是否需要追溯？"
```

**交互示例**：
```
/requirement-clarify 基于以下解析结果识别需求缺口：
[粘贴 requirement_parsed.yaml 内容]

系统输出：
## 需求缺口识别报告

### 🔴 高风险缺口（必须澄清）
1. **订单金额口径**：是否包含运费？是否扣除优惠券？
2. **退款订单处理**：GMV计算是否包含已退款订单？
3. **用户等级变化**：是否需要保留用户等级历史？

### 🟡 中等风险缺口（建议澄清）
4. **数据时效**：T+1的具体时间点？（凌晨2点 vs 早上8点）
5. **历史数据范围**：需要回溯多久的历史数据？

### 🟢 低风险缺口（可选澄清）
6. **技术栈偏好**：是否有指定的数仓平台？
7. **数据保留策略**：3年后数据如何处置？

### 💡 建议的确认问题
请向业务方确认以下问题：

Q1: "GMV的计算口径是什么？是下单金额、支付金额，还是扣除退款后的净额？"

Q2: "用户等级如果发生变化，分析时需要看当时的等级还是最新等级？"
...
```

---

### 功能3：需求转化助手 (/requirement-transform)

**Agent类型**：general-purpose
**工具权限**：Read, Grep, Glob, Edit, Write, Bash

**使用场景**：
- 需求确认后转化为技术规格
- 生成下游 Skill 的调用指令
- 创建可执行的项目计划

**输出物**：

#### 1. 数据模型规格 (specs/model_spec.yaml)
```yaml
model_spec:
  architecture: "星型模型"

  fact_tables:
    - name: fct_orders
      grain: "订单项级别"
      description: "订单事实表"
      dimensions:
        - dim_date
        - dim_user
        - dim_product
      measures:
        - name: quantity
          type: "integer"
        - name: amount
          type: "decimal"

  dimensions:
    - name: dim_user
      scd_type: 2
      natural_key: user_id
      attributes:
        - name: user_level
          track_history: true
        - name: city
          track_history: true
```

#### 2. ETL规格 (specs/etl_spec.yaml)
```yaml
etl_spec:
  pipelines:
    - name: order_sync
      source:
        type: "MySQL"
        connection: "order_db"
        tables: ["orders", "order_items"]
      extract:
        strategy: "incremental"
        watermark_column: "updated_at"
      transform:
        logic:
          - "join_orders_items"
          - "calculate_amount"
      load:
        target: "Snowflake"
        mode: "upsert"
        unique_key: "order_id"
```

#### 3. 数据质量规格 (specs/dq_spec.yaml)
```yaml
quality_rules:
  - table: fct_orders
    column: order_id
    rules:
      - type: not_null
        severity: error
      - type: unique
        severity: error

  - table: fct_orders
    column: amount
    rules:
      - type: positive
        severity: error
      - type: range
        min: 0
        max: 1000000
        severity: warning
```

#### 4. 下游 Skill 调用指令 (outputs/skill_commands.md)
```bash
# 根据需求转化结果，建议按以下顺序调用下游 Skill：

## Step 1: 数据建模
/model-design 基于以下规格设计维度模型：
- 业务域：电商销售分析
- 事实表：订单项级别，包含数量、金额度量
- 维度：用户(SCD2)、商品(SCD2)、日期
- 数据源：MySQL订单系统

## Step 2: SQL开发
/sql-gen 生成订单事实表抽取SQL，要求：
- 从MySQL orders表和order_items表抽取
- 增量同步，使用updated_at识别变更
- 关联用户表获取用户维度属性

## Step 3: ETL开发
/etl-template 生成订单同步Pipeline，配置：
- 源：MySQL (orders, order_items)
- 目标：Snowflake
- 策略：增量UPSERT
- 调度：每日凌晨2点

## Step 4: 数据质量
/dq-rule-gen 为fct_orders表生成质量规则：
- 订单ID非空唯一
- 金额正数且在合理范围
```

---

## 配合使用流程

```
原始业务需求 (业务方口述/文档)
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│  阶段1: 需求解析 (/requirement-parser)                        │
│  ├─ 输入：原始需求描述                                        │
│  ├─ 处理：general-purpose Agent                              │
│  └─ 输出：结构化需求文档 (parsed/)                             │
│       - 业务实体识别                                          │
│       - 指标/维度提取                                         │
│       - 数据源推断                                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  阶段2: 需求澄清 (/requirement-clarify)                       │
│  ├─ 输入：解析后的需求                                        │
│  ├─ 处理：Explore Agent (交互式分析)                         │
│  └─ 输出：需求缺口报告 + 确认问题清单                          │
│       - 歧义检测                                              │
│       - 缺失信息识别                                          │
│       - 风险预警                                              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼ (人工确认)
┌─────────────────────────────────────────────────────────────┐
│  阶段3: 需求转化 (/requirement-transform)                     │
│  ├─ 输入：经确认的需求                                        │
│  ├─ 处理：general-purpose Agent                              │
│  └─ 输出：技术规格包 (specs/)                                  │
│       - 数据模型规格                                          │
│       - ETL映射规格                                           │
│       - 质量规则建议                                          │
│       - 下游Skill调用指令                                      │
└─────────────────────────────────────────────────────────────┘
                     │
                     ▼
              驱动下游Skill开发
                     │
                     ▼
              完整数据系统交付
```

---

## 需求分析与下游Skill的关系

```
┌─────────────────────────────────────────────────────────────────────┐
│                        数据开发Skill生态                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌──────────────────────────────────────────────────────────┐     │
│   │                需求分析助手 (requirement-analyst)         │     │
│   │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │     │
│   │  │ requirement │  │ requirement │  │ requirement │       │     │
│   │  │   -parser   │→ │  -clarify   │→ │ -transform  │       │     │
│   │  └─────────────┘  └─────────────┘  └─────────────┘       │     │
│   └────────────────────────┬─────────────────────────────────┘     │
│                            │  [requirement_package.yaml]            │
│                            ▼                                       │
│   ┌──────────────┬──────────────┬──────────────┬──────────────┐   │
│   │              │              │              │              │   │
│   ▼              ▼              ▼              ▼              ▼   │
│ ┌──────┐    ┌──────┐    ┌──────┐    ┌──────┐    ┌──────┐        │
│ │model-│    │ sql- │    │ etl- │    │ dq-  │    │其他   │        │
│ │design│    │ -gen │    │-template│  │-rule │    │Skill │        │
│ └──┬───┘    └──┬───┘    └──┬───┘    └──┬───┘    └──────┘        │
│    │           │           │           │                        │
│    └───────────┴───────────┴───────────┘                        │
│                   │                                              │
│                   ▼                                              │
│           完整数据系统交付                                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 上下文传递协议

```yaml
# requirement_package.yaml 标准格式
requirement_package:
  version: "1.0"
  metadata:
    project_name: "电商销售分析数仓"
    analyst: "requirement-analyst"
    generated_at: "2024-01-15T10:00:00Z"
    confirmed: true

  business:
    domain: "电商"
    owner: "销售运营部"
    goal: "监控销售业绩，支持运营决策"
    success_criteria: ["日报自动生成", "异常自动告警"]

  functional:
    entities: [...]
    processes: [...]
    metrics: [...]
    dimensions: [...]

  non_functional:
    freshness: "T+1"
    retention: "3年"
    availability: "99.9%"
    compliance: ["PII脱敏", "访问审计"]

  technical:
    preferred_stack: ["Snowflake", "dbt", "Airflow"]
    existing_systems: ["MySQL订单库", "Redis缓存"]
    constraints: ["不能影响源库性能"]

  specifications:
    model_spec: {...}
    etl_spec: {...}
    dq_spec: {...}
```

---

## 最佳实践

### 1. 需求描述原则

**高效需求描述公式**：
```
[业务场景] + [分析目标] + [数据来源] + [使用方] + [特殊要求]

示例：
"我们是电商平台，需要分析销售业绩（GMV、订单量、客单价），
数据来自MySQL订单库和用户库，主要给运营团队做日报，
需要保留用户等级变化历史，T+1更新即可"
```

### 2. 需求澄清原则

- **先澄清后转化**：确保关键问题得到确认再进入技术设计
- **书面确认**：重要澄清点要求业务方书面确认
- **风险评估**：识别可能导致项目失败的需求风险

### 3. 需求变更管理

```yaml
# requirements/change_log.yaml
changes:
  - date: "2024-01-20"
    type: "范围变更"
    description: "增加商品类目分析维度"
    impact: "需要新增dim_category维度表"
    approved_by: "产品经理"
```

---

## 故障排除

### 需求解析不准确
1. 提供更详细的业务场景描述
2. 说明已有的系统现状
3. 列举期望的分析报表样例

### 需求澄清后仍有歧义
1. 要求业务方提供具体数据样例
2. 通过示例场景验证理解
3. 分阶段确认，先核心后边缘

### 下游Skill无法直接使用输出
1. 检查 requirement_package.yaml 格式
2. 确认版本兼容性
3. 手动调整转化输出

---

## 示例场景

详见 [examples/](examples/) 目录：

| 示例 | 场景 | 流程 |
|------|------|------|
| [example-ecommerce-requirement.md](examples/example-ecommerce-requirement.md) | 电商销售分析需求分析 | 解析 → 澄清 → 转化 |
| [example-user-behavior-requirement.md](examples/example-user-behavior-requirement.md) | 用户行为分析需求分析 | 解析 → 澄清 → 转化 |

---

## 路线图

### v1.0.0 (当前)
- ✅ 需求解析助手 (requirement-parser)
- ✅ 需求澄清助手 (requirement-clarify)
- ✅ 需求转化助手 (requirement-transform)
- ✅ 标准化需求包输出
- ✅ 下游Skill调用指令生成

### v1.1.0 (计划)
- 🔄 需求版本管理
- 🔄 变更影响分析
- 🔄 需求追踪矩阵

### v2.0.0 (计划)
- 📝 AI驱动需求预测
- 📝 智能需求补全
- 📝 与数据治理平台集成

---

**提示**：本Skill是数据开发Skill生态的起点，建议配合 skill-hub 使用以实现端到端自动化。
