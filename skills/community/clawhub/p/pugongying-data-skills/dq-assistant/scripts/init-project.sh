#!/bin/bash
# 数据质量管理项目初始化脚本
# 用法: bash init-project.sh <项目目录> <项目名称>
# 示例: bash init-project.sh ./dq-project "电商数据质量"

set -e

PROJECT_DIR="$1"
PROJECT_NAME="${2:-Data Quality Project}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

if [ -z "$PROJECT_DIR" ]; then
    echo "❌ 错误: 请指定项目目录"
    echo "用法: bash init-project.sh <项目目录> [项目名称]"
    echo "示例: bash init-project.sh ./my-dq-project "运营数据质量""
    exit 1
fi

# 创建目录结构
echo "🚀 创建数据质量管理项目: $PROJECT_NAME"
echo "📁 项目目录: $PROJECT_DIR"
mkdir -p "$PROJECT_DIR"/{rules,reports/{daily,weekly,monthly},docs,scripts}

# 复制规范文件
cp "$SKILL_DIR/references/data-quality-standards.md" "$PROJECT_DIR/standards.md"

# 创建 PROJECT.md
cat > "$PROJECT_DIR/PROJECT.md" << 'EOF'
# PROJECT - 数据质量管理项目中枢

## 项目信息

- **项目名称**: PROJECT_NAME_PLACEHOLDER
- **创建时间**: CREATE_TIME_PLACEHOLDER
- **负责团队**: [填写团队名]
- **项目目标**: 建立核心表数据质量监控体系

## 管理表清单

| 表名 | 中文名 | 质量评分 | 规则数 | 检查频率 | 负责人 |
|------|--------|----------|--------|----------|--------|
| | | | | | |

## 质量规则索引

| 规则文件 | 目标表 | 规则数 | 更新日期 | 状态 |
|----------|--------|--------|----------|------|
| | | | | |

## 质量报告存档

| 日期 | 报告类型 | 综合评分 | 问题数 | 文件路径 |
|------|----------|----------|--------|----------|
| | | | | reports/YYYY-MM/ |

## 待办事项

### 规则建设
- [ ] 核心表规则生成
- [ ] 规则Review
- [ ] 规则上线

### 监控体系
- [ ] 配置定时检查
- [ ] 配置告警通知
- [ ] 建立修复流程

### 文档建设
- [ ] 数据字典生成
- [ ] 质量报告模板
- [ ] 问题处理手册

## 快速链接

- [数据质量标准](./standards.md)
- [rules/](./rules/) - 质量规则文件
- [reports/](./reports/) - 质量报告存档
- [docs/](./docs/) - 数据字典文档

## 使用流程

```bash
# 1. 进入项目目录
cd PROJECT_DIR_PLACEHOLDER

# 2. 启动 Claude Code
claude

# 3. 生成表规则
/dq-rule-gen [表结构描述]

# 4. 执行质量检查
/dq-check [表名] [检查模式]

# 5. 生成数据字典
/schema-doc [表名]
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

数据质量管理项目，使用 Claude DQ Assistant Skill 管理。

## 项目结构

\`\`\`
.
├── PROJECT.md          # 项目中枢（表清单+规则+进度）
├── standards.md        # 数据质量标准规范
├── README.md           # 本文件
├── rules/              # 质量规则文件
│   ├── {table}_rules.yaml
│   └── ...
├── reports/            # 质量报告存档
│   ├── daily/          # 日报
│   ├── weekly/         # 周报
│   └── monthly/        # 月报
├── docs/               # 数据字典
│   ├── {table}.md
│   └── ...
└── scripts/            # 辅助脚本
\`\`\`

## 快速开始

### 1. 生成质量规则

\`\`\`bash
cd $PROJECT_DIR
claude

# 为新表生成规则
/dq-rule-gen
表名：users
字段：
- id (BIGINT, PK)
- email (VARCHAR)
- ...
\`\`\`

### 2. 执行质量检查

\`\`\`bash
# 执行检查
/dq-check 对users表执行全量质量检查

# 输出报告保存到 reports/daily/
\`\`\`

### 3. 生成数据字典

\`\`\`bash
# 生成数据字典
/schema-doc 生成users表的数据字典，包含样例数据

# 输出文档保存到 docs/
\`\`\`

## 开发流程

1. **规则生成**: /dq-rule-gen → 保存规则到 rules/
2. **规则审查**: 人工Review规则合理性
3. **执行检查**: /dq-check → 保存报告到 reports/
4. **问题修复**: 根据报告修复数据问题
5. **文档更新**: /schema-doc → 保存文档到 docs/

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

# 大型报告文件
reports/**/*.json
reports/**/*.xlsx

# 临时文件
*.tmp
*.bak
.DS_Store

# IDE
.idea/
.vscode/
*.swp
EOF

# 创建示例规则文件模板
cat > "$PROJECT_DIR/rules/example_table_rules.yaml" << 'EOF'
# 数据质量规则模板
table: example_table
generated_at: YYYY-MM-DD

rules:
  # 完整性规则
  - rule_id: COMP_001
    name: id_非空检查
    dimension: 完整性
    severity: 高
    column: id
    condition: id IS NULL
    threshold: 0
    sql: SELECT COUNT(*) FROM example_table WHERE id IS NULL

  # 唯一性规则
  - rule_id: UNIQ_001
    name: id_唯一性检查
    dimension: 唯一性
    severity: 高
    column: id
    sql: SELECT id, COUNT(*) FROM example_table GROUP BY id HAVING COUNT(*) > 1

  # 有效性规则
  - rule_id: VALID_001
    name: status_枚举检查
    dimension: 有效性
    severity: 中
    column: status
    condition: status NOT IN ('active', 'inactive')
    threshold: 5
    sql: |
      SELECT status, COUNT(*)
      FROM example_table
      WHERE status NOT IN ('active', 'inactive')
      GROUP BY status
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
echo "   /dq-rule-gen 你的第一个表规则"
echo ""
