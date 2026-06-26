#!/bin/bash
# 数据建模项目初始化脚本
# 用法: bash init-project.sh <项目目录> <项目名称>
# 示例: bash init-project.sh ./modeling-project "数据仓库建模"

set -e

PROJECT_DIR="$1"
PROJECT_NAME="${2:-Data Modeling Project}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

if [ -z "$PROJECT_DIR" ]; then
    echo "❌ 错误: 请指定项目目录"
    echo "用法: bash init-project.sh <项目目录> [项目名称]"
    echo "示例: bash init-project.sh ./my-dw-project "电商数据仓库""
    exit 1
fi

# 创建目录结构
echo "🚀 创建数据建模项目: $PROJECT_NAME"
echo "📁 项目目录: $PROJECT_DIR"
mkdir -p "$PROJECT_DIR"/{models/{staging,intermediate,marts/{dimensions,facts},reports},lineage,docs,seeds,snapshots,tests,macros,scripts}

# 复制规范文件
cp "$SKILL_DIR/references/data-modeling-standards.md" "$PROJECT_DIR/standards.md"

# 创建 PROJECT.md
cat > "$PROJECT_DIR/PROJECT.md" << 'EOF'
# PROJECT - 数据建模项目中枢

## 项目信息

- **项目名称**: PROJECT_NAME_PLACEHOLDER
- **创建时间**: CREATE_TIME_PLACEHOLDER
- **建模方法**: 维度建模（星型模型）
- **dbt版本**: 1.7.x
- **数据库**: PostgreSQL 15

## 模型清单

| 模型名 | 层级 | 类型 | 粒度 | 状态 | 负责人 |
|--------|------|------|------|------|--------|
| | staging | | | 🟡设计 | |
| | dimension | | | 🟡设计 | |
| | fact | | | 🟡设计 | |

状态说明:
- 🟡 设计: 设计阶段
- 🟡 开发: 开发阶段
- 🟢 测试: 测试中
- 🟢 上线: 已上线
- 🔴 废弃: 已废弃

## 血缘关系

```
Sources → Staging → Intermediate → Marts → Reports
```

## 待办事项

### 模型设计
- [ ] 完成业务需求分析
- [ ] 确定模型粒度
- [ ] 设计维度表
- [ ] 设计事实表

### dbt开发
- [ ] 配置sources
- [ ] 开发staging模型
- [ ] 开发mart模型
- [ ] 配置测试

### 文档
- [ ] 生成模型文档
- [ ] 生成血缘文档
- [ ] 编写使用手册

## 快速链接

- [数据建模规范](./standards.md)
- [models/](./models/) - dbt模型目录
- [seeds/](./seeds/) - 种子数据
- [lineage/](./lineage/) - 血缘文档

## 使用流程

```bash
# 1. 进入项目目录
cd PROJECT_DIR_PLACEHOLDER

# 2. 启动 Claude Code
claude

# 3. 模型设计
/model-design 业务场景描述

# 4. dbt开发
/dbt-model 生成staging模型...

# 5. 血缘分析
/lineage-doc 分析模型血缘
```
EOF

# 替换占位符
sed -i.bak "s/PROJECT_NAME_PLACEHOLDER/$PROJECT_NAME/g" "$PROJECT_DIR/PROJECT.md"
sed -i.bak "s/CREATE_TIME_PLACEHOLDER/$(date '+%Y-%m-%d')/g" "$PROJECT_DIR/PROJECT.md"
sed -i.bak "s|PROJECT_DIR_PLACEHOLDER|$PROJECT_DIR|g" "$PROJECT_DIR/PROJECT.md"
rm -f "$PROJECT_DIR/PROJECT.md.bak"

# 创建 README.md
cat > "$PROJECT_DIR/README.md" << EOF
# $PROJECT_NAME

dbt数据建模项目，使用 Claude Modeling Assistant Skill 管理。

## 项目结构

\`\`\`
.
├── PROJECT.md          # 项目中枢（模型清单+进度+规范）
├── standards.md        # 数据建模规范
├── README.md           # 本文件
├── dbt_project.yml     # dbt项目配置
├── packages.yml        # dbt包依赖
├── models/
│   ├── staging/        # Staging模型 (stg_*)
│   ├── intermediate/   # Intermediate模型 (int_*)
│   ├── marts/
│   │   ├── dimensions/ # 维度模型 (dim_*)
│   │   └── facts/      # 事实模型 (fct_*)
│   └── reports/        # 报表模型 (rpt_*)
├── seeds/              # 种子数据
├── snapshots/          # 快照
├── tests/              # 测试
├── macros/             # 宏
├── lineage/            # 血缘文档
└── docs/               # 模型文档
\`\`\`

## 快速开始

### 1. 模型设计

\`\`\`bash
cd $PROJECT_DIR
claude

# 设计维度模型
/model-design 为[业务场景]设计数据模型
\`\`\`

### 2. dbt开发

\`\`\`bash
# 生成dbt模型
/dbt-model 生成staging模型，源表raw.orders...

# 生成维度模型
/dbt-model 生成dimension模型，实体user，SCD Type 2...

# 生成事实模型
/dbt-model 生成fact模型，粒度订单项级别...
\`\`\`

### 3. 血缘分析

\`\`\`bash
# 分析血缘
/lineage-doc 分析models/marts/fct_orders.sql的血缘关系
\`\`\`

### 4. dbt运行

\`\`\`bash
# 运行所有模型
dbt run

# 运行测试
dbt test

# 生成文档
dbt docs generate
dbt docs serve
\`\`\`

## 开发流程

1. **设计**: /model-design → 输出模型设计方案
2. **开发**: /dbt-model → 生成dbt模型代码
3. **测试**: dbt test → 验证模型正确性
4. **文档**: /lineage-doc → 生成血缘文档
5. **上线**: dbt run → 部署到生产

## 规范

详见 [standards.md](./standards.md)

## 更新日志

### v1.0.0 ($(date '+%Y-%m-%d'))
- 项目初始化
EOF

# 创建 .gitignore
cat > "$PROJECT_DIR/.gitignore" << 'EOF'
# dbt
target/
dbt_packages/
logs/

# 环境配置
.env
profiles.yml

# 大型文件
seeds/*.csv
!seeds/.gitkeep

# 临时文件
*.tmp
*.bak
.DS_Store

# IDE
.idea/
.vscode/
*.swp
EOF

# 创建示例模型文件
cat > "$PROJECT_DIR/models/staging/.gitkeep" << 'EOF'
# Staging models go here
# Example: stg_orders.sql
EOF

cat > "$PROJECT_DIR/models/marts/dimensions/.gitkeep" << 'EOF'
# Dimension models go here
# Example: dim_users.sql
EOF

cat > "$PROJECT_DIR/models/marts/facts/.gitkeep" << 'EOF'
# Fact models go here
# Example: fct_orders.sql
EOF

# 创建示例 dbt_project.yml
cat > "$PROJECT_DIR/dbt_project.yml" << 'EOF'
name: 'my_data_warehouse'
version: '1.0.0'
config-version: 2

profile: 'default'

model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

target-path: "target"
clean-targets:
  - "target"
  - "dbt_packages"

models:
  my_data_warehouse:
    staging:
      +materialized: view
      +tags: ["staging"]

    intermediate:
      +materialized: view
      +tags: ["intermediate"]

    marts:
      dimensions:
        +materialized: table
        +tags: ["dimension"]
        +incremental_strategy: merge

      facts:
        +materialized: incremental
        +tags: ["fact"]
        +incremental_strategy: merge

    reports:
      +materialized: table
      +tags: ["report"]

seeds:
  my_data_warehouse:
    +schema: seeds
    +tags: ["seed"]

snapshots:
  my_data_warehouse:
    +target_schema: snapshots
    +tags: ["snapshot"]
EOF

echo ""
echo "✅ 项目创建成功!"
echo ""
echo "📁 项目结构:"
tree -L 3 "$PROJECT_DIR" 2>/dev/null || find "$PROJECT_DIR" -maxdepth 3 -print | sed -e 's;[^/]*/;|____;g;s;____|; |;g'
echo ""
echo "📝 下一步:"
echo "   cd $PROJECT_DIR"
echo "   claude"
echo "   /model-design 开始你的第一个模型设计"
echo ""
