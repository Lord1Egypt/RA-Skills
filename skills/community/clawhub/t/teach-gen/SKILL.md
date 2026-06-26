---
name: teach-gen
description: 根据教案、教材或课件生成交互式教学HTML网页
version: 1.0.0
author: Claude Code
tags: [education, html-generator, interactive, animation]
requirements: []
---

# teach-gen: 交互式教学网页生成器

根据教案、教材或课件自动生成交互式教学HTML网页，支持公式推导动画、概念演示和现代化简约设计。

## 功能特性

- 📄 **多格式输入**: 支持 PDF、Word、PPT、Markdown
- 🎨 **学科适配**: 针对数学、物理、化学优化
- 🎬 **智能动画**: 公式推导、图形变换自动动画化
- 📱 **响应式设计**: 现代简约风格，适配各种设备
- 💾 **单文件输出**: 生成独立HTML，可离线使用

## 使用方法

### 基础用法

```
/teach-gen "输入文件路径" --subject math --grade high-school
```

### 参数说明

| 参数 | 说明 | 可选值 |
|------|------|--------|
| `--subject` | 学科 | `math` \| `physics` \| `chemistry` |
| `--grade` | 学龄 | `elementary` \| `middle` \| `high` \| `college` |
| `--theme` | 主题 | `light` \| `dark` \| `auto` |
| `--output` | 输出路径 | 默认: `output.html` |

### 示例

```bash
# 生成高中数学课件
/teach-gen "lesson.md" --subject math --grade high

# 生成物理演示页
/teach-gen "physics.pdf" --subject physics --grade college

# 使用深色主题
/teach-gen "chemistry.docx" --theme dark
```

## 输入格式要求

### Markdown 格式

```markdown
# 课程标题

[动画: 公式推导]
$$
\int_0^1 x^2 dx = \frac{x^3}{3}\Big|_0^1 = \frac{1}{3}
$$

[动画: 函数图像]
@graph{y = x^2, domain: [-2, 2]}
```

### 支持的动画标签

- `[动画: 公式推导]` - 逐步展开数学公式
- `[动画: 几何变换]` - 图形旋转、缩放、平移
- `[动画: 函数图像]` - 动态绘制函数曲线
- `[动画: 概念图解]` - 流程图、思维导图
- `[交互: 参数滑块]` - 用户可调参数
