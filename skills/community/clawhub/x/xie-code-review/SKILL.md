---
name: code-review
description: Automated code review assistant. Analyzes code changes, PRs, and files for quality issues, best practices, security concerns, and style violations. Provides actionable feedback with line-by-line comments and summary reports.
---

# Code Review

自动化代码审查助手，分析代码变更、PR 和文件，检测质量问题、最佳实践违规、安全隐患和风格问题。

**Version**: 1.1  
**Features**: 多层级分析、AST 解析、安全检查、Git 集成、C/C++ 支持 (NEW)

---

## Quick Start

### 1. 审查单个文件

```bash
python3 scripts/main.py review file src/main.py
```

### 2. 审查暂存区变更

```bash
python3 scripts/main.py review staged
```

### 3. 审查特定提交

```bash
python3 scripts/main.py review commit abc123
```

### 4. 导出 JSON 报告

```bash
python3 scripts/main.py review file src/*.py --format json --output report.json
```

---

## Commands

| 命令 | 说明 | 示例 |
|------|------|------|
| `review file` | 审查文件 | `main.py review file src/*.py` |
| `review staged` | 审查暂存区 | `main.py review staged` |
| `review commit` | 审查提交 | `main.py review commit abc123` |
| `review diff` | 审查 diff 文件 | `main.py review diff changes.patch` |

---

## Checks

### 质量检查 (Quality)
- **圈复杂度** - 函数复杂度超过阈值（默认 10）
- **函数长度** - 函数超过最大行数（默认 50）
- **文件长度** - 文件超过最大行数（默认 500）
- **重复代码** - 检测重复代码块
- **未使用导入** - 检测未使用的 import

### 最佳实践 (Best Practices)
- **Python**: PEP 8、类型提示、文档字符串
- **JavaScript**: 使用 let/const 替代 var、移除 console.log
- **通用**: 命名规范、导入排序

### 安全检查 (Security)
- **硬编码密钥** - 检测 password/secret/api_key/token
- **危险函数** - 检测 eval/exec 使用
- **SQL 注入** - 检测字符串拼接 SQL
- **XSS 风险** - 检测 innerHTML 使用

### 风格检查 (Style)
- **尾随空格** - 检测行尾空格
- **行长度** - 检测超过 100 字符的行
- **文档字符串** - 检测缺少 docstring 的函数/类

---

## Configuration

创建 `.code-review.json` 在项目根目录：

```json
{
  "max_complexity": 10,
  "max_function_lines": 50,
  "max_file_lines": 500,
  "ignore": [
    "tests/**",
    "vendor/**",
    "node_modules/**"
  ],
  "severity": "warning"
}
```

---

## Output Formats

### Markdown (默认)

```bash
python3 main.py review file src/main.py
```

输出包含：
- 问题统计摘要
- 按规则分类的问题列表
- 每个文件的详细问题
- 修复建议

### JSON

```bash
python3 main.py review file src/main.py --format json
```

适合 CI/CD 集成：
```json
{
  "summary": {
    "files_reviewed": 5,
    "total_issues": 12,
    "errors": 0,
    "warnings": 3,
    "info": 9
  },
  "files": [...]
}
```

---

## Git 集成

### Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash
python3 /path/to/code-review/scripts/main.py review staged --fail-on-error
```

### CI/CD 集成

```yaml
# .github/workflows/code-review.yml
name: Code Review
on: [push, pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Code Review
        run: |
          python3 skills/code-review/scripts/main.py review file src/ --format json --output review.json
      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: code-review-report
          path: review.json
```

---

## Examples

### 场景 1：提交前自检

```bash
# 1. 添加变更到暂存区
git add src/

# 2. 审查暂存区代码
python3 main.py review staged

# 3. 如果有错误，修复后再提交
```

### 场景 2：审查 PR

```bash
# 获取 PR 的最新提交
python3 main.py review commit $(git rev-parse HEAD)
```

### 场景 3：批量审查

```bash
# 审查所有 Python 文件
python3 main.py review file src/**/*.py --format json --output report.json

# 设置更严格的阈值
python3 main.py review file src/ --max-complexity 5 --max-function-lines 30
```

---

## Supported Languages

| 语言 | 质量检查 | 安全检查 | 风格检查 |
|------|----------|----------|----------|
| Python | ✅ | ✅ | ✅ |
| JavaScript | ✅ | ✅ | ✅ |
| TypeScript | ⚠️ | ⚠️ | ⚠️ |

---

## Files

```
skills/code-review/
├── SKILL.md                    # 本文件
└── scripts/
    ├── main.py                 # ⭐ 统一入口
    └── analyzer.py             # 核心分析引擎
```

---

## Exit Codes

| 代码 | 含义 |
|------|------|
| 0 | 成功，无错误 |
| 1 | 发现错误或 `--fail-on-error` 且有问题 |

---

## Roadmap

- [x] Python 分析器
- [x] JavaScript 分析器
- [ ] TypeScript 完整支持
- [ ] Go 分析器
- [ ] Rust 分析器
- [ ] PR 评论自动发布
- [ ] 增量审查（只审查变更行）
