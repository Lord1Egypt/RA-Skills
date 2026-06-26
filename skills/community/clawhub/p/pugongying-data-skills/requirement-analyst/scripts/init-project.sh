#!/bin/bash
#
# 数据开发需求分析项目初始化脚本
# 用法: bash init-project.sh <项目路径> <项目名称>
#

set -e

PROJECT_PATH=${1:-"./data-project"}
PROJECT_NAME=${2:-"数据开发项目"}
TIMESTAMP=$(date +"%Y-%m-%d")

echo "🚀 初始化数据开发需求分析项目: $PROJECT_NAME"
echo "📁 项目路径: $PROJECT_PATH"
echo ""

# 创建目录结构
mkdir -p "$PROJECT_PATH"/{requirements/{raw,parsed,confirmed},specs,clarifications,outputs,docs}

echo "✅ 目录结构创建完成"

# 创建 PROJECT.md 项目中枢
cat > "$PROJECT_PATH/PROJECT.md" << EOF
# $PROJECT_NAME

> 项目创建时间: $TIMESTAMP
> 使用 Skill: requirement-analyst

---

## 项目概述

<!-- 由需求分析师填写 -->
- **业务域**:
- **项目目标**:
- **业务负责人**:
- **技术负责人**:
- **项目状态**: 🟡 需求分析中

## 需求清单

| 需求ID | 需求名称 | 优先级 | 状态 | 关联Spec |
|--------|---------|--------|------|---------|
| REQ-001 | | P0 | 🟡 待分析 | |

## 进度追踪

- [ ] 阶段1: 需求解析
- [ ] 阶段2: 需求澄清
- [ ] 阶段3: 需求转化
- [ ] 阶段4: 技术设计
- [ ] 阶段5: 开发实现
- [ ] 阶段6: 测试验证
- [ ] 阶段7: 上线交付

## 快速开始

\`\`\`bash
# Step 1: 将原始需求写入 requirements/raw/raw-requirement.md

# Step 2: 使用 Skill 进行需求解析
/requirement-parser 基于 requirements/raw/raw-requirement.md 解析需求

# Step 3: 需求澄清
/requirement-clarify 识别需求缺口

# Step 4: 需求转化
/requirement-transform 生成技术规格
\`\`\`

## 文档索引

- [原始需求](requirements/raw/)
- [解析结果](requirements/parsed/)
- [确认需求](requirements/confirmd/)
- [技术规格](specs/)
- [澄清记录](clarifications/)
- [最终输出](outputs/)

## 变更记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|---------|------|
| $TIMESTAMP | v0.1 | 项目初始化 | requirement-analyst |
EOF

echo "✅ PROJECT.md 创建完成"

# 创建原始需求模板
cat > "$PROJECT_PATH/requirements/raw/raw-requirement.md" << 'EOF'
# 原始业务需求

## 业务背景
<!-- 描述当前业务场景和面临的问题 -->

例如：
我们是电商平台，目前销售数据分散在多个系统中，运营团队每天需要手动导出Excel制作日报，效率低下且容易出错。

## 需求描述
<!-- 描述具体的业务需求 -->

例如：
1. 需要建设销售分析数据仓库
2. 支持按日/周/月查看销售业绩
3. 支持按地区/用户等级/商品类目下钻分析
4. 支持订单全生命周期跟踪

## 数据来源
<!-- 描述已知的数据来源 -->

| 系统 | 类型 | 表/Topic | 数据量 | 备注 |
|------|------|---------|--------|------|
| 订单系统 | MySQL | orders, order_items | 日增100万 | |
| 用户系统 | MySQL | users | 总量5000万 | |
| 商品系统 | MySQL | products, categories | 总量100万 | |

## 期望输出
<!-- 描述期望的分析输出 -->

例如：
1. 每日销售日报（自动化生成）
2. 实时销售大屏（可选）
3. 异常订单预警

## 使用方
<!-- 描述谁将使用这些数据 -->

- 主要用户：销售运营团队、数据分析师
- 使用频率：日报每日查看，即席查询随时
- 访问方式：BI报表、SQL查询

## 时间要求
<!-- 描述时间约束 -->

- 期望上线时间：
- 数据更新频率：T+1 / 准实时 / 实时
- 历史数据范围：

## 其他约束
<!-- 其他重要的约束条件 -->

- 安全要求：
- 性能要求：
- 预算限制：
EOF

echo "✅ 原始需求模板创建完成"

# 创建需求变更记录模板
cat > "$PROJECT_PATH/requirements/change-log.md" << 'EOF'
# 需求变更记录

| 变更日期 | 版本 | 变更类型 | 变更内容 | 提出人 | 影响分析 | 审批人 |
|---------|------|---------|---------|--------|---------|--------|
| | | 新增/修改/删除 | | | | |

## 变更类型说明
- **新增**: 新增需求
- **修改**: 修改已有需求
- **删除**: 删除需求
- **范围变更**: 项目范围调整

## 影响分析维度
- 数据模型影响
- ETL Pipeline影响
- 报表影响
- 工期影响
- 成本影响
EOF

echo "✅ 变更记录模板创建完成"

# 创建澄清问题记录模板
cat > "$PROJECT_PATH/clarifications/clarification-template.md" << 'EOF'
# 需求澄清记录

## 澄清会话信息
- **日期**:
- **参与人**:
- **方式**: 会议/邮件/即时通讯

## 待澄清问题清单

### 🔴 高风险问题（阻塞）
- [ ] 问题1:
  - 提问:
  - 回答:
  - 结论:

### 🟡 中风险问题（重要）
- [ ] 问题1:
  - 提问:
  - 回答:
  - 结论:

### 🟢 低风险问题（可选）
- [ ] 问题1:
  - 提问:
  - 回答:
  - 结论:

## 决策记录

| 决策项 | 决策内容 | 决策依据 | 决策人 | 日期 |
|--------|---------|---------|--------|------|
| | | | | |

## 后续行动

- [ ] 行动1:
- [ ] 行动2:
EOF

echo "✅ 澄清记录模板创建完成"

# 创建规格文档模板
cat > "$PROJECT_PATH/specs/MODEL_SPEC_TEMPLATE.yaml" << 'EOF'
# 数据模型规格
# 由 requirement-transform 自动生成或手工维护

model_spec:
  version: "1.0"
  last_updated: ""

  architecture:
    type: "星型模型"  # 星型/雪花/Data Vault
    description: ""

  fact_tables:
    - name: ""
      grain: ""
      description: ""
      source_tables: []
      dimensions: []
      measures: []
      degenerate_dimensions: []

  dimensions:
    - name: ""
      scd_type: 2  # 0/1/2/3
      natural_key: ""
      description: ""
      attributes: []

  relationships: []

  physical_design:
    partitioning: {}
    indexing: {}
    compression: {}
EOF

cat > "$PROJECT_PATH/specs/ETL_SPEC_TEMPLATE.yaml" << 'EOF'
# ETL规格
# 由 requirement-transform 自动生成或手工维护

etl_spec:
  version: "1.0"
  last_updated: ""

  pipelines: []
    # - name: ""
    #   description: ""
    #   source:
    #     type: ""
    #     connection: ""
    #     tables: []
    #   extract:
    #     strategy: "incremental"  # full/incremental/cdc
    #     watermark_column: ""
    #   transform:
    #     logic: []
    #   load:
    #     target: ""
    #     mode: "upsert"  # upsert/append/replace
    #     unique_key: ""
    #   schedule:
    #     frequency: "daily"
    #     start_time: "02:00"

  dependencies: []
EOF

cat > "$PROJECT_PATH/specs/DQ_SPEC_TEMPLATE.yaml" << 'EOF'
# 数据质量规格
# 由 requirement-transform 自动生成或手工维护

dq_spec:
  version: "1.0"
  last_updated: ""

  rules: []
    # - table: ""
    #   column: ""
    #   rules:
    #     - type: "not_null"
    #       severity: "error"
    #     - type: "unique"
    #       severity: "error"

  dimensions:
    completeness: []
    accuracy: []
    consistency: []
    timeliness: []
    validity: []

  alerting:
    channels: []
    thresholds: {}
EOF

echo "✅ 规格模板创建完成"

# 创建 .gitignore
cat > "$PROJECT_PATH/.gitignore" << 'EOF'
# 数据开发需求分析项目忽略文件

# 敏感信息
*.key
*.pem
*.p12
.credentials/
secrets.yaml
secrets.yml

# 临时文件
*.tmp
*.temp
.DS_Store
Thumbs.db

# IDE
.idea/
.vscode/
*.swp
*.swo

# 生成的大型文件
*.csv
*.parquet
*.xlsx
outputs/data/
EOF

echo "✅ .gitignore 创建完成"

# 创建 README
cat > "$PROJECT_PATH/README.md" << EOF
# $PROJECT_NAME

数据开发需求分析项目，使用 requirement-analyst Skill 进行端到端需求分析。

## 项目结构

\`\`\`
.
├── PROJECT.md              # 项目中枢（进度+清单+索引）
├── README.md               # 本文件
├── requirements/           # 需求文档
│   ├── raw/                # 原始业务需求
│   ├── parsed/             # 解析后的结构化需求
│   ├── confirmed/          # 已确认的需求规格
│   └── change-log.md       # 变更记录
├── specs/                  # 技术规格
│   ├── model_spec.yaml     # 数据模型规格
│   ├── etl_spec.yaml       # ETL规格
│   └── dq_spec.yaml        # 数据质量规格
├── clarifications/         # 需求澄清记录
├── outputs/                # 最终输出
│   └── requirement_package.yaml
└── docs/                   # 其他文档
\`\`\`

## 快速开始

### 1. 准备原始需求

编辑 \`requirements/raw/raw-requirement.md\`，填写业务背景和需求描述。

### 2. 启动需求分析

在 Claude Code 中执行：

\`\`\`bash
/requirement-analyst 端到端分析 $PROJECT_NAME 需求
\`\`\`

或分阶段执行：

\`\`\`bash
/requirement-parser 基于 requirements/raw/raw-requirement.md 解析需求
/requirement-clarify 识别需求缺口
/requirement-transform 生成技术规格
\`\`\`

### 3. 查看输出

分析完成后，查看以下文件：
- \`requirements/parsed/requirement_parsed.yaml\` - 结构化需求
- \`clarifications/clarification-report.md\` - 澄清报告
- \`specs/\` - 技术规格
- \`outputs/requirement_package.yaml\` - 完整需求包

## 下一步

需求分析完成后，使用下游 Skill 进行开发：

\`\`\`bash
# 数据建模
/model-design 基于 outputs/requirement_package.yaml 设计维度模型

# SQL开发
/sql-gen 基于模型规格生成ETL SQL

# ETL开发
/etl-template 基于ETL规格生成Pipeline

# 数据质量
/dq-rule-gen 基于质量规格生成质量规则
\`\`\`

## 参考

- [requirement-analyst Skill文档](../../.claude/skills/requirement-analyst/SKILL.md)
- [需求分析规范](../../.claude/skills/requirement-analyst/references/requirement-standards.md)
EOF

echo "✅ README.md 创建完成"

echo ""
echo "✨ 项目初始化完成！"
echo ""
echo "下一步:"
echo "  1. cd $PROJECT_PATH"
echo "  2. 编辑 requirements/raw/raw-requirement.md 填写原始需求"
echo "  3. 在 Claude Code 中运行 /requirement-analyst 开始分析"
