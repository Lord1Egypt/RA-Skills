---
name: style-analyzer
description: 文本风格分析器 - 分析写作风格特征并生成 Voice Profile 配置文件。当需要捕捉作者风格、创建 Voice Profile 或分析文本特征时使用。
---

# Style Analyzer - 文本风格分析器

## Overview

分析文本的写作风格特征，自动生成 Voice Profile 配置文件，包含风格标签、语速、语气、情感倾向等。用于保持小说创作的风格一致性。

**使用场景**：
- 需要捕捉作者的写作风格
- 需要为小说项目创建 Voice Profile
- 需要分析文本的句式/词汇/节奏特征
- 需要量化风格特征用于后续生成

## 分析维度

| 维度 | 分析内容 | 输出 |
|------|----------|------|
| **Voice Profile** | 风格标签、语速、语气、情感倾向 | labels, pace, tone, sentiment |
| **句式特征** | 平均句长、长短句比例、修辞手法 | average_length, ratios, rhetorical_devices |
| **词汇特征** | 词性比例、高频词、词汇丰富度 | adj/verb/noun_ratio, frequent_words |
| **节奏特征** | 段落长度、标点分布、对话比例 | paragraph_length, punctuation, dialogue_ratio |

## CLI 使用

```bash
# 基本用法
python3 scripts/analyze_style.py --input novel.txt --output style.yml

# 指定样本大小
python3 scripts/analyze_style.py \
  --input novel.txt \
  --output style.yml \
  --sample-size 2000

# 分析结果输出到终端 + 保存 YAML
python3 scripts/analyze_style.py -i text.txt -o style.yml
```

## 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--input` / `-i` | ✅ | 输入文本文件路径 |
| `--output` / `-o` | ✅ | 输出 YAML 配置文件路径 |
| `--sample-size` / `-s` | ❌ | 分析样本大小（默认 1000 字符） |

## 输出 YAML 格式

```yaml
voice_profile:
  labels:
  - 简洁
  - 快速
  - 紧凑
  - 对话性强
  pace: 快速
  tone: 随意
  sentiment: 0.15

sentence_features:
  average_length: 28.5
  long_sentence_ratio: 0.15
  short_sentence_ratio: 0.65
  rhetorical_devices:
    metaphor: 3
    simile: 2

vocabulary_features:
  adj_ratio: 0.12
  verb_ratio: 0.18
  noun_ratio: 0.35
  most_frequent_words:
  - - 主角
    - 15
  - - 说道
    - 12
  unique_words_ratio: 0.68

rhythm_features:
  average_paragraph_length: 156
  punctuation_distribution:
    period: 45
    comma: 78
    question: 12
    exclamation: 5
  dialogue_ratio: 0.35
```

## 风格标签说明

| 标签 | 含义 | 触发条件 |
|------|------|----------|
| 简洁 | 句子简短 | 平均句长 ≤ 40 字符 |
| 复杂 | 句子较长 | 平均句长 > 40 字符 |
| 快速 | 节奏紧凑 | 平均句长 < 30 字符 |
| 舒缓 | 节奏缓慢 | 平均句长 ≥ 30 字符 |
| 紧凑 | 标点密集 | 每句平均字符 < 30 |
| 娓娓道来 | 叙述舒缓 | 每句平均字符 ≥ 30 |
| 互动性 | 有问句 | 包含？或! |
| 对话性强 | 对话多 | 包含引号对话 |
| 节奏感强 | 标点丰富 | 包含，、； |

## 语速分类

| 语速 | 条件 |
|------|------|
| 缓慢 | 平均句长 > 50 字符 |
| 适中 | 平均句长 30-50 字符 |
| 快速 | 平均句长 < 30 字符 |

## 语气分类

| 语气 | 条件 |
|------|------|
| 正式 | 正式标记词 > 随意标记词 × 2 |
| 随意 | 随意标记词 > 正式标记词 × 2 |
| 中性 | 介于两者之间 |

**正式标记词**：因此、然而、综上所述、基于此、由此可见

**随意标记词**：我觉得、我想、你知道、其实、就是说

## 情感倾向

范围：-1.0 到 1.0

- **正值**：积极情感（好、美、喜欢、爱、快乐等）
- **负值**：消极情感（坏、丑、讨厌、恨、悲伤等）
- **0 附近**：中性情感

## 依赖

- Python 3.8+
- rich (终端渲染)
- PyYAML (配置文件解析)

安装依赖：
```bash
pip install -r scripts/requirements.txt
```

## 与其他技能集成

### 与 smart-prompt-builder 集成

```bash
# 1. 分析风格
python3 ../style-analyzer/scripts/analyze_style.py \
  --input reference_text.txt \
  --output style.yml

# 2. 使用生成的 Voice Profile 构建提示词
python3 ../smart-prompt-builder/scripts/build_prompt.py \
  --scene-type description \
  --style-file style.yml \
  --context '{"scene": "森林"}'
```

### 与 novel-writer 集成

```bash
# 1. 分析参考文本风格
python3 ../style-analyzer/scripts/analyze_style.py \
  --input author_sample.txt \
  --output style.yml

# 2. novel-writer 使用 style.yml 保持风格一致
```

## 注意事项

- 样本大小建议 ≥ 500 字符，以获得准确的风格分析
- 支持 UTF-8 和 GBK 编码的文本文件
- 输出 YAML 可直接用于 smart-prompt-builder 的 --style-file 参数
- 修辞手法检测基于关键词匹配，可能不完全准确
