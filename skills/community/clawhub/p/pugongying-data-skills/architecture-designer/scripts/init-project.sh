#!/bin/bash
#
# 数据架构设计项目初始化脚本
# 用法: bash init-project.sh <项目路径> <项目名称>
#

set -e

PROJECT_PATH=${1:-"./data-platform"}
PROJECT_NAME=${2:-"数据平台架构设计"}
TIMESTAMP=$(date +"%Y-%m-%d")

echo "🚀 初始化数据架构设计项目: $PROJECT_NAME"
echo "📁 项目路径: $PROJECT_PATH"
echo ""

# 创建目录结构
mkdir -p "$PROJECT_PATH"/{architecture/{01-decisions,02-layers,03-tech-stack,04-topology},requirements,specs,docs,diagrams}

echo "✅ 目录结构创建完成"

# 创建 PROJECT.md 项目中枢
cat > "$PROJECT_PATH/PROJECT.md" << EOF
# $PROJECT_NAME

> 项目创建时间: $TIMESTAMP
> 使用 Skill: architecture-designer

---

## 项目概述

<!-- 由架构师填写 -->
- **业务域**:
- **架构目标**:
- **约束条件**:
- **项目状态**: 🟡 架构设计中

## 架构决策记录 (ADR)

| ADR编号 | 标题 | 状态 | 日期 |
|---------|------|------|------|
| ADR-001 | 整体架构选型 | 🟡 提案 | |
| ADR-002 | 数据湖格式选择 | ⚪ 待开始 | |
| ADR-003 | 流处理引擎选型 | ⚪ 待开始 | |

## 设计进度

- [ ] 阶段1: 架构选型
  - [ ] 收集约束条件
  - [ ] 评估可选方案
  - [ ] 编写ADR
- [ ] 阶段2: 分层设计
  - [ ] 设计ODS层
  - [ ] 设计DWD层
  - [ ] 设计DWS层
  - [ ] 设计ADS层
- [ ] 阶段3: 技术规划
  - [ ] 存储选型
  - [ ] 计算选型
  - [ ] 中间件选型
  - [ ] 成本估算
- [ ] 阶段4: 拓扑设计
  - [ ] Pipeline分组
  - [ ] 依赖关系设计
  - [ ] 调度策略
  - [ ] 监控告警

## 输入

- [需求包](requirements/requirement_package.yaml) - 来自requirement-analyst

## 输出

- [架构规格](specs/architecture_spec.yaml)
- [基础设施规格](specs/infra_spec.yaml)
- [成本估算](specs/cost_estimate.yaml)

## 文档索引

- [架构决策](architecture/01-decisions/)
- [分层设计](architecture/02-layers/)
- [技术栈](architecture/03-tech-stack/)
- [拓扑设计](architecture/04-topology/)

## 变更记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|---------|------|
| $TIMESTAMP | v0.1 | 项目初始化 | architecture-designer |
EOF

echo "✅ PROJECT.md 创建完成"

# 创建 ADR 模板
cat > "$PROJECT_PATH/architecture/01-decisions/adr-template.md" << 'EOF'
# ADR-XXX: 决策标题

## 状态

- 提案 (Proposed)
- 已接受 (Accepted)
- 已废弃 (Superseded by ADR-YYY)
- 已过时 (Obsolete)

## 背景

描述决策的背景和上下文。

## 决策

明确的决策内容。

## 考虑的选项

### 选项1: [名称]

**优点:**
-

**缺点:**
-

### 选项2: [名称]

**优点:**
-

**缺点:**
-

## 决策结果

选择的选项及理由。

## 影响

### 正面影响
-

### 负面影响
-

## 相关决策

- 前置决策:
- 后续决策:

## 备注

其他相关信息。
EOF

echo "✅ ADR模板创建完成"

# 创建分层设计模板
cat > "$PROJECT_PATH/architecture/02-layers/layer-template.yaml" << 'EOF'
# 分层设计模板
# 由 layer-design 自动生成或手工维护

layer_architecture:
  version: "1.0"
  project: ""

  layers:
    - name: "ODS"
      full_name: "Operational Data Store"
      description: "原始数据层"

      tables: []
        # - name: "ods_table_name"
        #   source: ""
        #   format: ""
        #   retention: ""
        #   partition_by: ""
        #   storage: ""

      governance: []

    - name: "DWD"
      full_name: "Data Warehouse Detail"
      description: "明细数据层"

      tables: []
        # - name: "dwd_table_name"
        #   grain: ""
        #   source: ""
        #   cleaning_rules: []
        #   retention: ""

    - name: "DWS"
      full_name: "Data Warehouse Service"
      description: "主题宽表层"

      tables: []
        # - name: "dws_table_name"
        #   grain: ""
        #   aggregation: ""
        #   source: ""
        #   metrics: []

    - name: "ADS"
      full_name: "Application Data Store"
      description: "应用数据层"

      tables: []
        # - name: "ads_table_name"
        #   purpose: ""
        #   source: ""
        #   consumers: []

  data_flow: []
    # - from: ""
    #   to: ""
    #   method: ""
    #   schedule: ""

  lifecycle_policies:
    hot_data: {}
    warm_data: {}
    cold_data: {}
EOF

echo "✅ 分层设计模板创建完成"

# 创建技术栈模板
cat > "$PROJECT_PATH/architecture/03-tech-stack/tech-stack-template.yaml" << 'EOF'
# 技术栈规划模板
# 由 tech-planning 自动生成或手工维护

tech_stack:
  version: "1.0"
  architecture_pattern: ""

  infrastructure:
    cloud_provider: ""
    region: ""
    vpc: {}

  storage:
    data_lake: {}
    data_warehouse: {}
    cache: {}

  compute:
    batch_processing: {}
    stream_processing: {}

  messaging: {}

  orchestration: {}

  data_governance: {}

  cost_estimate:
    monthly: {}
    optimization_suggestions: []
EOF

echo "✅ 技术栈模板创建完成"

# 创建拓扑设计模板
cat > "$PROJECT_PATH/architecture/04-topology/topology-template.yaml" << 'EOF'
# Pipeline拓扑设计模板
# 由 topology-design 自动生成或手工维护

pipeline_topology:
  version: "1.0"

  dag_groups: []
    # - name: "ingestion"
    #   description: "数据采集"
    #   pipelines: []

  dependencies: []
    # - upstream: ""
    #   downstream: ""
    #   type: ""

  scheduling:
    strategy: ""
    timezone: "Asia/Shanghai"

  failure_handling:
    retry_policy: {}
    alert_rules: []
    recovery: []

  monitoring:
    metrics: []
    dashboards: []
EOF

echo "✅ 拓扑设计模板创建完成"

# 创建架构规格模板
cat > "$PROJECT_PATH/specs/ARCHITECTURE_SPEC_TEMPLATE.yaml" << 'EOF'
# 架构规格
# 由 architecture-designer 自动生成

architecture_package:
  version: "1.0"

  metadata:
    project_name: ""
    architect: "architecture-designer"
    generated_at: ""
    based_on_requirement: "requirements/requirement_package.yaml"

  architecture:
    pattern: ""
    decisions: []

  layers:
    ods: {}
    dwd: {}
    dws: {}
    ads: {}

  tech_stack:
    infrastructure: {}
    storage: {}
    compute: {}
    messaging: {}
    orchestration: {}
    governance: {}

  topology:
    dag_groups: []
    dependencies: []
    scheduling: {}

  downstream_specs:
    model_spec:
      file: "specs/model_spec.yaml"
    etl_spec:
      file: "specs/etl_spec.yaml"
    infra_spec:
      file: "specs/infra_spec.yaml"
    cost_estimate:
      file: "specs/cost_estimate.yaml"
EOF

echo "✅ 架构规格模板创建完成"

# 创建需求包占位文件
cat > "$PROJECT_PATH/requirements/README.md" << 'EOF'
# 需求包目录

将 `requirement-analyst` 生成的 `requirement_package.yaml` 放置于此目录。

这是架构设计的输入。
EOF

echo "✅ 需求包README创建完成"

# 创建架构设计文档模板
cat > "$PROJECT_PATH/docs/architecture-overview.md" << 'EOF'
# 架构总览

## 系统上下文

```
[待补充: 系统上下文图 - 展示系统与外部实体的关系]
```

## 架构愿景

一句话描述架构的核心目标和价值。

## 架构原则

1. **原则1**: 描述
2. **原则2**: 描述
3. **原则3**: 描述

## 架构分层

### Level 1: 系统上下文
展示系统如何融入整体IT环境。

### Level 2: 容器图
展示系统内的主要容器（应用、数据存储等）。

### Level 3: 组件图
展示容器内的主要组件。

## 关键技术决策

| 决策 | 选择 | 理由 |
|------|------|------|
| 数据架构 | | |
| 流处理 | | |
| 批处理 | | |
| 存储 | | |

## 非功能需求

### 性能
- 吞吐量:
- 延迟:
- 并发:

### 可靠性
- 可用性:
- RTO:
- RPO:

### 安全
- 认证:
- 授权:
- 审计:

## 风险与缓解

| 风险 | 可能性 | 影响 | 缓解措施 |
|------|--------|------|---------|
| | | | |
EOF

echo "✅ 架构总览文档模板创建完成"

# 创建 .gitignore
cat > "$PROJECT_PATH/.gitignore" << 'EOF'
# 数据架构设计项目忽略文件

# 敏感信息
*.key
*.pem
*.p12
.credentials/
secrets.yaml
secrets.yml
.env

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

# 生成的图片(可选提交)
# diagrams/*.png
# diagrams/*.svg
EOF

echo "✅ .gitignore 创建完成"

# 创建 README
cat > "$PROJECT_PATH/README.md" << EOF
# $PROJECT_NAME

数据平台架构设计项目，使用 architecture-designer Skill 进行端到端架构设计。

## 项目结构

\`\`\`
.
├── PROJECT.md                    # 项目中枢（进度+清单+索引）
├── README.md                     # 本文件
├── requirements/                 # 输入需求
│   └── requirement_package.yaml  # 来自requirement-analyst
├── architecture/                 # 架构设计
│   ├── 01-decisions/             # 架构决策记录(ADR)
│   ├── 02-layers/                # 分层设计
│   ├── 03-tech-stack/            # 技术栈规划
│   └── 04-topology/              # Pipeline拓扑
├── specs/                        # 输出规格
│   ├── architecture_spec.yaml
│   ├── infra_spec.yaml
│   └── cost_estimate.yaml
├── docs/                         # 架构文档
│   └── architecture-overview.md
└── diagrams/                     # 架构图
\`\`\`

## 快速开始

### 1. 准备需求

确保 requirements/requirement_package.yaml 已存在（来自requirement-analyst）。

### 2. 启动架构设计

在 Claude Code 中执行：

\`\`\`bash
# 端到端设计
/architecture-designer 基于需求包设计完整数据平台架构

# 或分阶段执行
/arch-select 选择整体数据架构
/layer-design 设计ODS/DWD/DWS/ADS分层
/tech-planning 选择存储和计算引擎
/topology-design 设计Pipeline拓扑
\`\`\`

### 3. 查看输出

设计完成后，查看以下文件：
- \`architecture/01-decisions/\` - 架构决策记录
- \`architecture/02-layers/layer-design.yaml\` - 分层设计
- \`architecture/03-tech-stack/tech-stack.yaml\` - 技术栈规划
- \`architecture/04-topology/pipeline-topology.yaml\` - 拓扑设计
- \`specs/architecture_package.yaml\` - 完整架构包

## 下一步

架构设计完成后，使用下游 Skill 进行开发：

\`\`\`bash
# 数据建模（基于架构分层）
/model-design 基于architecture/02-layers设计维度模型

# ETL开发（基于拓扑设计）
/etl-template 基于architecture/04-topology生成Pipeline

# 基础设施部署（基于技术栈）
# 使用infra_spec.yaml进行Terraform/CloudFormation部署
\`\`\`

## 参考

- [architecture-designer Skill文档](../../.claude/skills/architecture-designer/SKILL.md)
- [架构设计规范](../../.claude/skills/architecture-designer/references/architecture-standards.md)
EOF

echo "✅ README.md 创建完成"

echo ""
echo "✨ 项目初始化完成！"
echo ""
echo "下一步:"
echo "  1. cd $PROJECT_PATH"
echo "  2. 将requirement_package.yaml放入requirements/目录"
echo "  3. 在 Claude Code 中运行 /architecture-designer 开始设计"
