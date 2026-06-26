---
name: quality-checker
description: 章节质量检测器 - 检测章节正文的质量问题并生成评分报告。当需要评估章节质量、发现问题时使用，支持字数/段落/对话/标点/重复用词检测。
---

# Quality Checker - 章节质量检测器

## Overview

分析章节正文，检测潜在质量问题并生成详细报告，包含评分（0-100 分）和具体改进建议。

**使用场景**：
- 需要评估章节质量
- 需要发现写作问题（字数不足、段落过长、对话比例异常等）
- 需要量化质量指标进行对比
- 需要在发布前进行质量把关

## 检测项目

| 检测项 | 说明 | 阈值 |
|--------|------|------|
| **字数检测** | 检查是否达到目标字数 | ≥ 目标字数 80% |
| **段落长度** | 检测过长段落（影响阅读节奏） | ≤ 200 字/段 |
| **对话比例** | 检测对话占比是否合理 | 20%-60% |
| **标点滥用** | 检测感叹号/问号过度使用 | ≤ 10% |
| **重复用词** | 检测高频重复词汇 | ≤ 5 次/词 |

## 质量评分

| 分数 | 等级 | 说明 |
|------|------|------|
| 90-100 | 优秀 | 可直接发布 |
| 80-89 | 良好 | 少量问题 |
| 70-79 | 中等 | 需要修改 |
| 60-69 | 及格 | 建议修改 |
| <60 | 不合格 | 需要大修 |

## CLI 使用

```bash
# 基本用法
python3 scripts/check_quality.py --input chapters/chapter-01.md

# 指定目标字数
python3 scripts/check_quality.py \
  --input chapters/chapter-01.md \
  --word-count 3000

# 输出报告到文件
python3 scripts/check_quality.py \
  --input chapters/chapter-01.md \
  --output reports/chapter-01-quality.md

# 简写
python3 scripts/check_quality.py -i chapter.md -w 3000 -o report.md
```

## 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--input` / `-i` | ✅ | 章节正文文件路径（Markdown） |
| `--word-count` / `-w` | ❌ | 目标字数（默认 3000） |
| `--output` / `-o` | ❌ | 输出报告文件路径 |

## 输出报告格式

```markdown
# 章节质量检测报告

**章节**: chapter-01.md
**检测时间**: 2026-04-04 23:50:00
**质量评分**: 85/100 (良好)

## 检测结果

| 检测项 | 状态 | 详情 |
|--------|------|------|
| 字数 | ✅ 通过 | 2850/3000 (95%) |
| 段落长度 | ⚠️ 警告 | 3 个段落超过 200 字 |
| 对话比例 | ✅ 通过 | 35% (正常范围 20%-60%) |
| 标点滥用 | ✅ 通过 | 感叹号占比 3% |
| 重复用词 | ⚠️ 警告 | "突然" 出现 8 次 |

## 问题详情

### 段落过长
- 第 3 段：256 字
- 第 7 段：234 字
- 第 12 段：218 字

### 重复用词
- "突然": 8 次
- "仿佛": 6 次
- "感觉": 5 次

## 改进建议

1. 拆分第 3、7、12 段，每段控制在 200 字以内
2. 减少"突然"的使用频率，尝试同义替换
3. 增加 150 字达到目标字数
```

## 依赖

- Python 3.8+
- rich (终端渲染)

安装依赖：
```bash
pip install -r scripts/requirements.txt
```

## 与其他技能集成

### 与 novel-writer 集成

```bash
# 1. 生成章节正文
python3 ../novel-writer/scripts/write_chapter.py \
  --book-dir projects/my-novel \
  --chapter 1 \
  --outline outlines/chapter-1.md \
  --output chapters/chapter-01.md

# 2. 检测质量
python3 scripts/check_quality.py \
  --input chapters/chapter-01.md \
  --word-count 3000 \
  --output reports/chapter-01-quality.md
```

### 批量检测

```bash
# 检测全部章节
for chapter in chapters/chapter-*.md; do
    python3 scripts/check_quality.py \
        --input "$chapter" \
        --word-count 3000 \
        --output "reports/$(basename "$chapter" .md)-quality.md"
done
```

## 注意事项

- 支持 UTF-8 和 GBK 编码的 Markdown 文件
- 质量评分仅供参考，具体标准可根据项目调整
- 对话检测基于引号识别，可能不完全准确
- 重复用词检测自动过滤常见虚词（的、了、是等）
