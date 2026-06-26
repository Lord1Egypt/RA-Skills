---
name: smart-prompt-builder
description: 智能提示构建器 - 根据语料库检索结果生成优化的写作提示。当需要为小说创作场景生成结构化提示词时使用，支持描写/对话/动作/情感 4 种场景类型，可注入 Voice Profile 和上下文信息。
---

# Smart Prompt Builder - 智能提示构建器

## Overview

根据语料库检索结果和上下文信息，生成结构化的写作提示词，包含系统提示、用户提示和约束条件。支持 Voice Profile 注入，确保生成内容符合作者风格。

**使用场景**：
- 需要为小说章节生成写作提示
- 需要保持作者风格一致性（Voice Profile）
- 需要结合语料库检索结果进行创作
- 需要结构化提示词用于后续生成任务

## 场景类型

支持 4 种写作场景：

| 场景类型 | 参数值 | 用途 |
|----------|--------|------|
| 描写 | `description` | 环境/场景描写，营造氛围 |
| 对话 | `dialogue` | 人物对话，展现性格 |
| 动作 | `action` | 动作场景，展现紧张感 |
| 情感 | `emotion` | 心理描写，刻画内心世界 |

## CLI 使用

```bash
# 基本用法 - 描写场景
python3 scripts/build_prompt.py --scene-type description \
  --context '{"scene": "雨中的街道"}'

# 使用 Voice Profile
python3 scripts/build_prompt.py --scene-type dialogue \
  --style-file assets/style.yml \
  --context '{"characters": {"主角": "侦探"}}'

# 结合语料库结果
python3 scripts/build_prompt.py --scene-type action \
  --corpus-results '[{"title": "范例", "content": "...", "relevance_score": 0.9}]'

# 输出到文件
python3 scripts/build_prompt.py --scene-type emotion \
  --output prompt.txt
```

## 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--scene-type` | ✅ | 场景类型：description/dialogue/action/emotion |
| `--context` | ❌ | 上下文信息（JSON 格式） |
| `--style-file` | ❌ | Voice Profile 配置文件（YAML） |
| `--corpus-results` | ❌ | 语料库检索结果（JSON 数组） |
| `--output` | ❌ | 输出文件路径 |

## Context JSON 格式

```json
{
  "summary": "前文摘要",
  "scene": "当前场景",
  "characters": {
    "角色名": "角色状态/身份"
  }
}
```

## Corpus Results JSON 格式

```json
[
  {
    "title": "语料标题",
    "content": "语料内容",
    "relevance_score": 0.95
  }
]
```

## Voice Profile (style.yml) 格式

```yaml
voice_profile:
  style_tags: ["温柔", "叙事性", "略带忧伤"]
  speech_rate: 0.9
  tone: "亲切的讲述者语气"
  emotion: 0.3
  anti_ai_rules:
    - "避免过度使用形容词"
    - "减少'的'字频率"
```

## 输出结构

生成的提示词包含 4 部分：

1. **系统提示** - 定义 AI 角色和专长
2. **用户提示** - 具体写作需求 + 上下文 + 语料参考
3. **约束条件** - 写作规范和技巧要求
4. **元数据** - 场景类型、语料数量等

## 依赖

- Python 3.8+
- rich (终端渲染)
- PyYAML (配置文件解析)

安装依赖：
```bash
pip install -r scripts/requirements.txt
```

## 示例输出

```
============================================================
【系统提示】
============================================================
你是一名专业的环境描写大师，擅长通过细腻的笔触营造氛围。

============================================================
【用户提示】
============================================================
请根据以下描述需求生成一段富有画面感的环境描写：

[角色状态]
- 主角：疲惫的侦探

[当前场景]
雨中的街道

[Voice Profile]
风格标签：温柔，叙事性，略带忧伤，缓慢节奏
语速：0.9
语气：亲切的讲述者语气
情感倾向：0.3

============================================================
【约束条件】
============================================================
• 使用五感描写法（视觉、听觉、嗅觉、味觉、触觉）
• 包含至少 3 个具体的细节描写
• 使用比喻或拟人手法增强表现力
• 保持描写节奏的层次感
```

## 与其他技能集成

### 与 corpus-search 集成

```bash
# 1. 检索语料库
python3 ../corpus-search/scripts/search_corpus.py \
  --corpus xuanhuan-full \
  --query "环境描写" \
  --top-k 5 \
  --output corpus_results.json

# 2. 构建提示词
python3 scripts/build_prompt.py \
  --scene-type description \
  --corpus-results "$(cat corpus_results.json)" \
  --style-file assets/style.yml
```

### 与 novel-writer 集成

```bash
# 1. 构建提示词
python3 scripts/build_prompt.py \
  --scene-type dialogue \
  --context '{"scene": "咖啡馆", "characters": {"林风": "侦探"}}' \
  --output prompt.txt

# 2. 使用提示词生成内容（由 novel-writer skill 执行）
```

## 注意事项

- 上下文 JSON 必须有效，否则报错退出
- Voice Profile 文件必须存在且为有效 YAML
- 语料库结果为 JSON 数组格式
- 输出文件会自动创建（如不存在）
