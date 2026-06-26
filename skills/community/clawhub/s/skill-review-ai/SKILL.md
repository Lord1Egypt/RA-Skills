---
name: skill-review
description: 审查 Agent Skills 的规范性、完整性和代码质量。在安装或发布 skills 时使用，验证 SKILL.md 格式、目录结构、脚本代码和文件引用是否符合 Agent Skills 规范。
license: MIT
metadata:
  author: skill-reviewer
  version: "1.0"
---

# Skill Review

审查 Agent Skills 的规范性、完整性和代码质量。

## 使用场景

- 安装 skills 前进行质量检查
- 发布 skills 前的合规验证
- 代码审查和最佳实践检查
- 目录结构和文件引用验证

## 审查项目

### 1. SKILL.md 格式审查

- [ ] YAML frontmatter 存在且格式正确
- [ ] `name` 字段符合命名规范（小写字母、数字、连字符，1-64字符）
- [ ] `description` 字段存在且长度在 1-1024 字符之间
- [ ] `license` 字段（如有）格式正确
- [ ] `compatibility` 字段（如有）长度在 500 字符以内
- [ ] `metadata` 字段（如有）为键值对格式
- [ ] `allowed-tools` 字段（如有）格式正确

### 2. 目录结构审查

- [ ] 技能目录名与 `name` 字段一致
- [ ] `SKILL.md` 文件存在于根目录
- [ ] `scripts/` 目录（如有）结构合理
- [ ] `references/` 目录（如有）结构合理
- [ ] `assets/` 目录（如有）结构合理
- [ ] 无深层嵌套（建议不超过 2 层）

### 3. 脚本代码审查

- [ ] 脚本文件有执行权限（如需要）
- [ ] 脚本包含清晰的错误处理
- [ ] 脚本有适当的注释说明
- [ ] 脚本依赖关系明确
- [ ] 无硬编码的敏感信息
- [ ] 代码风格一致

### 4. 文件引用审查

- [ ] 所有引用的文件存在
- [ ] 相对路径正确（从 skill 根目录开始）
- [ ] 无循环引用
- [ ] 引用的文件大小合理

## 使用方法

### 基本用法

```bash
# 审查单个 skill
bash scripts/review.sh /path/to/skill-name

# 详细审查（包含代码分析）
bash scripts/review.sh /path/to/skill-name --verbose

# 生成 JSON 格式报告
bash scripts/review.sh /path/to/skill-name --json
```

### Python API

```python
from scripts.review_skill import SkillReviewer

reviewer = SkillReviewer()
result = reviewer.review("/path/to/skill-name")
print(result.to_markdown())
```

## 审查报告格式

### Markdown 报告

```markdown
# Skill 审查报告: skill-name

## 概要
- 总分: 85/100
- 状态: ✅ 通过 / ❌ 未通过
- 审查时间: 2024-01-01 12:00:00

## 详细结果

### SKILL.md 格式
- 状态: ✅ 通过
- 得分: 25/25
- 问题: 无

### 目录结构
- 状态: ✅ 通过
- 得分: 20/20
- 问题: 无

### 脚本代码
- 状态: ⚠️ 警告
- 得分: 30/35
- 问题:
  - [WARN] 脚本缺少错误处理: scripts/process.py:15
  - [WARN] 建议添加注释: scripts/helper.sh:8

### 文件引用
- 状态: ❌ 失败
- 得分: 10/20
- 问题:
  - [ERROR] 引用的文件不存在: references/MISSING.md
  - [WARN] 文件过大: assets/large-file.bin (5.2MB)
```

### JSON 报告

```json
{
  "skill_name": "skill-name",
  "overall_score": 85,
  "status": "passed",
  "timestamp": "2024-01-01T12:00:00Z",
  "categories": {
    "skill_md": {
      "score": 25,
      "max_score": 25,
      "status": "passed",
      "issues": []
    },
    "directory_structure": {
      "score": 20,
      "max_score": 20,
      "status": "passed",
      "issues": []
    },
    "script_code": {
      "score": 30,
      "max_score": 35,
      "status": "warning",
      "issues": [
        {
          "level": "warn",
          "message": "脚本缺少错误处理",
          "file": "scripts/process.py",
          "line": 15
        }
      ]
    },
    "file_references": {
      "score": 10,
      "max_score": 20,
      "status": "failed",
      "issues": [
        {
          "level": "error",
          "message": "引用的文件不存在",
          "file": "references/MISSING.md"
        }
      ]
    }
  }
}
```

## 评分标准

| 类别 | 满分 | 通过线 | 说明 |
|------|------|--------|------|
| SKILL.md 格式 | 25 | 20 | frontmatter 和正文格式 |
| 目录结构 | 20 | 15 | 目录组织和命名 |
| 脚本代码 | 35 | 25 | 代码质量和安全性 |
| 文件引用 | 20 | 15 | 引用完整性和正确性 |
| **总分** | **100** | **75** | 综合评分 |

## 常见问题

### SKILL.md 问题

**问题**: `name` 字段包含大写字母
```yaml
# ❌ 错误
name: PDF-Processing

# ✅ 正确
name: pdf-processing
```

**问题**: `description` 过短
```yaml
# ❌ 错误
description: Helps with PDFs.

# ✅ 正确
description: Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDF documents.
```

### 目录结构问题

**问题**: 目录名与 `name` 字段不匹配
```
# ❌ 错误
my-skill/
  SKILL.md (name: different-name)

# ✅ 正确
my-skill/
  SKILL.md (name: my-skill)
```

### 脚本问题

**问题**: 缺少错误处理
```bash
# ❌ 错误
rm -rf $TARGET_DIR

# ✅ 正确
if [ -d "$TARGET_DIR" ]; then
  rm -rf "$TARGET_DIR" || { echo "无法删除目录"; exit 1; }
fi
```

### 文件引用问题

**问题**: 引用的文件不存在
```markdown
# ❌ 错误
See [reference](references/NONEXISTENT.md)

# ✅ 正确
See [reference](references/EXISTING.md)
```

## 参考文档

- [Agent Skills 规范](references/SPECIFICATION.md)
- [审查规则详解](references/RULES.md)
- [常见问题解答](references/FAQ.md)

## 最佳实践

1. **在安装 skill 前运行审查**: 确保 skill 质量符合预期
2. **在 CI/CD 中集成**: 自动化 skill 发布流程
3. **定期更新审查规则**: 跟随 Agent Skills 规范更新
4. **结合人工审查**: 自动化审查不能替代人工判断
