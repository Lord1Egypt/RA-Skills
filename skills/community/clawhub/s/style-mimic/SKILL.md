---
name: style-mimic
version: 1.0.0
author: Titan Cheung
description: 模仿社会洞察类文章风格进行写作的AI助手
license: MIT
homepage: https://github.com/openclaw/openclaw
metadata:
  {
    "openclaw":
      {
        "emoji": "📝",
        "requires": { "bins": [] },
        "categories": ["writing", "style", "chinese"],
        "tags": ["写作", "风格模仿", "社会洞察", "中文写作"]
      },
  }
---

# style-mimic 技能

## 简介
模仿用户收藏的社会洞察类文章风格进行写作。

## 风格特征

### 思维模式
- 结构化思维：善用框架、坐标系分析复杂问题
- 概念创新：创造新概念来定义现象
- 二元对立：对比理想与现实、旧秩序与新秩序
- 系统视角：从宏观结构看个体困境

### 论证方式
- 先立后破：先承认合理性，再指出结构性问题
- 层层递进：现象→原因→影响→解决方案
- 数据/案例支撑：用具体数字、真实场景增强说服力
- 引用经典：适时引用古籍、名言

### 语言风格
- 术语化表达：专业但不晦涩
- 短句为主：短促有力，节奏感强
- 排比结构：多段排比增强气势
- 直白批判：直指问题核心
- 金句收尾：每节结尾有记忆点

### 情感基调
- 理性中带着悲悯
- 批判但不偏激
- 危机感与希望并存

## 文章结构模板

```
【开头】
- 以对比强烈的场景/现象切入
- 提出核心问题
- 预告文章要做的事（第一、第二、第三）

【主体】
1. 概念定义（创造核心概念）
2. 分类讨论（建立分析框架）
3. 逐层深入（从表面到本质）
4. 未来推演（趋势预测）
5. 解决方案（可落地建议）

【结尾】
- 引用经典升华
- 回到开头的意象
- 开放式收束
```

## 常用句式
- "你觉得这公平吗？大多数人觉得不公平。但大多数人也觉得没办法。"
- "这篇文章要做三件事：第一... 第二... 第三..."
- "在没有路灯的夜晚... 现在灯亮了，他还攥着不放。"
- "不是... 而是..."
- "过去是... 现在是..."

## 使用方式

### 基础使用
当用户想要用这个风格写作时：

1. **确认主题**：询问用户想写什么主题
2. **收集素材**：了解相关背景、数据、案例
3. **构建框架**：按照模板构建文章结构
4. **模仿写作**：运用上述风格特征进行创作
5. **检查调性**：确保符合理性深刻、结构清晰的特点

### 工具辅助
本技能提供以下工具辅助写作：

#### 1. 写作助手 (`scripts/writing_assistant.py`)
```bash
# 列出所有模板
python3 scripts/writing_assistant.py --list-templates

# 生成文章开头
python3 scripts/writing_assistant.py --topic "主题" --type analysis --action opening

# 生成文章结构
python3 scripts/writing_assistant.py --topic "主题" --type analysis --action structure

# 获取常用句式
python3 scripts/writing_assistant.py --action phrase
```

#### 2. 风格检测 (`scripts/style_analyzer.py`)
```bash
# 分析文本风格
python3 scripts/style_analyzer.py --file 文章.md

# 简要输出
python3 scripts/style_analyzer.py --file 文章.md --output brief

# 分析直接输入的文本
python3 scripts/style_analyzer.py --text "文章内容..."
```

#### 3. 模板系统
提供5种专业模板：
- `templates/analysis-template.md` - 分析类文章
- `templates/commentary-template.md` - 评论文
- `templates/report-template.md` - 报告文
- `templates/story-template.md` - 故事文
- `templates/interview-template.md` - 访谈文

## 注意事项
- 保持客观理性，避免情绪化宣泄
- 善用"我们"拉近距离，但保持批判距离
- 每个观点都要有逻辑支撑
- 结尾要有升华，不能戛然而止
