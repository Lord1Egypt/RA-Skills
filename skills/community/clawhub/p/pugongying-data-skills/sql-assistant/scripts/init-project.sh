#!/bin/bash
# SQL Assistant 项目初始化脚本
# 用法: bash init-project.sh <项目目录> <项目名称>
# 示例: bash init-project.sh ./report-sql "运营报表SQL库"

set -e

PROJECT_DIR="$1"
PROJECT_NAME="${2:-SQL Project}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

if [ -z "$PROJECT_DIR" ]; then
    echo "❌ 错误: 请指定项目目录"
    echo "用法: bash init-project.sh <项目目录> [项目名称]"
    echo "示例: bash init-project.sh ./my-sql-project "运营报表SQL库""
    exit 1
fi

# 创建目录结构
echo "🚀 创建 SQL Assistant 项目: $PROJECT_NAME"
echo "📁 项目目录: $PROJECT_DIR"
mkdir -p "$PROJECT_DIR"/{queries/{generated,reviewed,production},explain,docs,scripts}

# 复制规范文件
cp "$SKILL_DIR/references/sql-standards.md" "$PROJECT_DIR/standards.md"

# 创建 PROJECT.md
cat > "$PROJECT_DIR/PROJECT.md" << 'EOF'
# PROJECT - SQL项目中枢

## 项目信息

- **项目名称**: PROJECT_NAME_PLACEHOLDER
- **创建时间**: CREATE_TIME_PLACEHOLDER
- **数据库类型**: [PostgreSQL/MySQL/SQL Server/Oracle]
- **版本**: 1.0.0

## SQL清单

| 文件名 | 状态 | 数据库 | 用途 | 负责人 | 创建时间 | 更新时间 |
|--------|------|--------|------|--------|----------|----------|
| | 🟡生成 | | | | | |
| | 🟡审查 | | | | | |
| | 🟢生产 | | | | | |

状态说明:
- 🟡 generated: AI生成待审查
- 🟡 reviewed: 已审查待上线
- 🟢 production: 已上线
- 🔴 deprecated: 已废弃

## 执行计划存档

| 查询 | 执行时间 | 扫描行数 | 执行时长 | 存档路径 |
|------|----------|----------|----------|----------|
| | | | | explain/YYYY-MM/ |

## 待办事项

- [ ] 初始化数据库连接配置
- [ ] 定义命名规范
- [ ] 创建第一个查询
- [ ] 建立CI/CD流程

## 规范速查

### 命名规范
- 表名: `小写下划线_复数`
- 字段名: `小写下划线`
- 索引名: `idx_表名_字段名`
- CTE名: `描述性名词`

### 文件命名
```
{模块}_{描述}_v{版本}.sql

示例:
- report_sales_daily_v1.0.0.sql
- report_sales_daily_v1.0.1.sql  # 优化版本
```

## 快速链接

- [SQL编写规范](./standards.md)
- [queries/generated/](./queries/generated/) - 待审查SQL
- [queries/reviewed/](./queries/reviewed/) - 已审查SQL
- [queries/production/](./queries/production/) - 生产SQL
- [explain/](./explain/) - 执行计划存档
EOF

# 替换占位符
sed -i.bak "s/PROJECT_NAME_PLACEHOLDER/$PROJECT_NAME/g" "$PROJECT_DIR/PROJECT.md"
sed -i.bak "s/CREATE_TIME_PLACEHOLDER/$(date '+%Y-%m-%d')/g" "$PROJECT_DIR/PROJECT.md"
rm -f "$PROJECT_DIR/PROJECT.md.bak"

# 创建 README.md
cat > "$PROJECT_DIR/README.md" << EOF
# $PROJECT_NAME

SQL智能开发项目，使用 Claude SQL Assistant Skill 管理。

## 快速开始

### 生成SQL
\`\`\`bash
# 在项目目录下启动 Claude Code
claude

# 生成SQL
/sql-gen 查询过去30天销售数据
\`\`\`

### 审查SQL
\`\`\`bash
/sql-review queries/generated/report_sales_daily_v1.0.0.sql
\`\`\`

### 分析执行计划
\`\`\`bash
# 先在数据库执行 EXPLAIN (ANALYZE, BUFFERS)
# 然后粘贴结果
/sql-explain
[paste explain output]
\`\`\`

## 项目结构

\`\`\`
.
├── PROJECT.md          # 项目中枢（SQL清单、进度、规范）
├── standards.md        # SQL编写规范
├── README.md           # 本文件
├── queries/
│   ├── generated/      # AI生成的SQL（待审查）
│   ├── reviewed/       # 已审查的SQL
│   └── production/     # 生产环境SQL
├── explain/            # 执行计划存档
│   └── YYYY-MM/        # 按月归档
└── docs/               # 文档
\`\`\`

## 开发流程

1. **生成**: 使用 \`/sql-gen\` 生成初始SQL → 保存到 queries/generated/
2. **审查**: 使用 \`/sql-review\` 审查代码 → 移动到 queries/reviewed/
3. **测试**: 在测试环境执行，收集执行计划
4. **分析**: 使用 \`/sql-explain\` 分析性能 → 存档到 explain/
5. **上线**: 优化通过后 → 移动到 queries/production/

## 规范

详见 [standards.md](./standards.md)

## 更新日志

### v1.0.0 ($(date '+%Y-%m-%d'))
- 项目初始化
EOF

# 创建 .gitignore
cat > "$PROJECT_DIR/.gitignore" << 'EOF'
# 数据库配置文件（可能包含敏感信息）
*.env
config/local.*

# 大型执行计划文件
explain/**/*.json
!explain/**/*.md

# 临时文件
*.tmp
*.bak
.DS_Store

# IDE
.idea/
.vscode/
*.swp
EOF

echo ""
echo "✅ 项目创建成功!"
echo ""
echo "📁 项目结构:"
tree -L 2 "$PROJECT_DIR" 2>/dev/null || find "$PROJECT_DIR" -maxdepth 2 -print | sed -e 's;[^/]*/;|____;g;s;____|; |;g'
echo ""
echo "📝 下一步:"
echo "   cd $PROJECT_DIR"
echo "   claude"
echo "   /sql-gen 你的第一个查询"
echo ""
