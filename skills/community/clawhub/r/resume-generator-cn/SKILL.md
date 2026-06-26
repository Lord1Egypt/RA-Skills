---
name: resume-generator-cn
description: 简历生成器 - AI 驱动的中英文简历生成、优化、模板（简历中国版）
metadata:
  openclaw:
    emoji: "📄"
    category: "productivity"
    tags: ["resume", "cv", "job", "career", "china", "ai"]
---

# 简历生成器

AI 驱动的简历生成、优化、模板。

## 功能

- 📄 简历生成
- ✨ AI 优化
- 🌐 中英双语
- 📋 多种模板
- 🔍 ATS 优化

## 使用方法

### 生成简历

```bash
# 交互式生成
./scripts/generate-resume.sh

# 从模板生成
./scripts/generate-resume.sh --template tech

# 中英双语
./scripts/generate-resume.sh --bilingual
```

### AI 优化

```bash
# 优化现有简历
./scripts/optimize-resume.sh resume.md

# 根据 JD 优化
./scripts/optimize-resume.sh resume.md --jd job-description.txt
```

## 简历模板

### 技术类

```markdown
# 姓名
高级软件工程师

## 技能
- Python, JavaScript, Go
- React, Vue, Node.js
- PostgreSQL, Redis

## 工作经历
### 公司A (2020-至今)
- 负责...
- 成就...
```

### 产品类

```markdown
# 姓名
产品经理

## 核心能力
- 需求分析
- 数据驱动
- 用户研究

## 项目经历
### 项目A
- 背景...
- 行动...
- 结果...
```

## AI 优化建议

1. **量化成就**: 将"提升了性能"改为"响应时间从 2s 降至 200ms"
2. **关键词**: 根据 JD 添加相关关键词
3. **结构**: 使用 STAR 法则（Situation-Task-Action-Result）
4. **长度**: 控制在 1-2 页

## ATS 优化

### 关键词优化

```bash
# 分析 JD 关键词
./scripts/analyze-jd.sh job-description.txt

# 输出建议
关键词: Python, API, 微服务, Docker
建议: 在简历中突出这些技能
```

### 格式建议

- ✅ 简洁的 Markdown/Word 格式
- ❌ 复杂的表格/图形
- ✅ 标准的章节标题
- ❌ 自定义的创意布局

## 快速开始

```bash
# 1. 生成简历
./scripts/generate-resume.sh

# 2. 优化简历
./scripts/optimize-resume.sh my-resume.md

# 3. 导出 PDF
pandoc my-resume.md -o my-resume.pdf
```

## 注意事项

1. **真实性**: 不要夸大或虚构经历
2. **针对性**: 根据岗位调整简历
3. **更新**: 定期更新简历

---

*版本: 1.0.0*
