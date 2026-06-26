# Skill Review

用于审查 Agent Skills 的规范性、完整性和代码质量。

## 功能

- ✅ 验证 SKILL.md 格式（frontmatter、必需字段）
- ✅ 检查目录结构（命名规范、嵌套深度）
- ✅ 审查脚本代码（shebang、敏感信息、错误处理）
- ✅ 验证文件引用（存在性、大小）
- ✅ 生成详细的审查报告（Markdown/JSON 格式）

## 快速开始

### 基本用法

```bash
# 审查单个 skill
bash scripts/review.sh /path/to/your-skill

# 详细审查
bash scripts/review.sh /path/to/your-skill --verbose

# 生成 JSON 格式报告
bash scripts/review.sh /path/to/your-skill --json
```

### Python API

```python
from scripts.review_skill import SkillReviewer

reviewer = SkillReviewer()
result = reviewer.review("/path/to/your-skill")
print(result.to_markdown())
```

## 评分标准

| 类别 | 满分 | 通过线 |
|------|------|--------|
| SKILL.md 格式 | 25 | 20 |
| 目录结构 | 20 | 15 |
| 脚本代码 | 35 | 25 |
| 文件引用 | 20 | 15 |
| **总分** | **100** | **75** |

## 目录结构

```
skill-review/
├── SKILL.md              # Skill 主文档
├── scripts/
│   ├── review.sh         # Bash 入口脚本
│   └── review_skill.py   # Python 审查核心
├── references/
│   ├── SPECIFICATION.md  # Agent Skills 规范
│   ├── RULES.md          # 审查规则详解
│   └── FAQ.md            # 常见问题解答
└── README.md             # 本文件
```

## 依赖

- Python 3.7+
- Bash

可选依赖：
- `yamllint` - YAML 格式检查
- `jq` - JSON 处理

## 许可证

MIT
