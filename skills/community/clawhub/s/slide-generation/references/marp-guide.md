# Marp Slide Format Reference

## Complete Slide Examples

### Cover Page (cover_c)

```markdown
---
marp: true
size: 16:9
theme: am_blue_course
paginate: true
headingDivider: [2,3]
footer: '*敬业乐群*'
---

<!-- _class: cover_c -->
<!-- _paginate: "" -->
<!-- _footer: 敬业乐群 -->
<!-- _header: ![](images/logo.png) -->

###### 初识智能体

# "从定义到实践，开启智能体之旅"

@曹尚
<2025101550@niit.edu.cn>
```

### Table of Contents (toc_a)

```markdown
## 本节内容

<!-- _class: toc_a -->
<!-- _header: "CONTENTS" -->
<!-- _footer: 敬业乐群 -->
<!-- _paginate: "" -->

- [什么是智能体？](#3)
- [传统视角下的智能体演进](#4)
- [大语言模型驱动的新范式](#7)
- [智能体的分类](#9)
```

### Content Page with Image (fig-top)

```markdown
## 智能体与环境的交互

<!-- _class: fig-top -->

<div class=fig-container>

![width:850px](images/1757242319667-0.png)

</div>

<div class=text-container>

- 智能体通过传感器持续感知环境状态，经过内部处理后通过执行器改变环境。这个**感知→决策→行动→观察**的闭环是所有智能体行为的基础模型。

**关键点：** 环境不仅是"背景"，更是智能体的"反馈源"
</div>
```

### Two-Column Layout (cols-2-64, image on left)

```markdown
## 《春》（两栏六四分）

<!-- _class: cols-2-64 -->

<div class=limg>

![#c](images/spring.png)
</div>

<div class=rdiv>

盼望着，盼望着，东风来了，春天的脚步近了。

一切都像刚睡醒的样子，欣欣然张开了眼。
</div>
```

### Two-Column Layout (cols-2, text only)

```markdown
## 内容概览

<!-- _class: cols-2 -->

<div class=ldiv>

**第一部分**
- 概念定义
- 核心原理
- 关键特征

</div>

<div class=rdiv>

**第二部分**
- 应用场景
- 实践案例
- 总结思考

</div>
```

### Table Layout

```markdown
## PEAS 模型实例分析

| PEAS 要素 | 具体内容 |
|---|---|
| **性能度量（P）** | 安全性、合规性、效率 |
| **环境（E）** | 道路、交通、天气 |
| **执行器（A）** | 方向盘、油门、刹车 |
| **传感器（S）** | 摄像头、激光雷达 |
```

### Callout Box

```markdown
<!-- _class: bq-blue -->

> 合成控制法 (Synthetic Control Method)
>
> SCM 最早由 Abadie and Gardeazabal (2003) 提出...
```

### Dense Content Page

```markdown
## 智能体的五级演进模型

<!-- _class: tinytext -->

**智能体的五级演进模型：**

1. **反射智能体（Reflex Agent）**
   - 最简单的"条件-动作"规则，无记忆

2. **基于模型的反射智能体**
   - 拥有内部世界模型

3. **基于目标的智能体**
   - 主动规划行动序列

4. **基于效用的智能体**
   - 最大化物期望效用

5. **学习型智能体**
   - 自主改进决策策略
```

### Code Block

````markdown
```python
# 智能体循环示例
while True:
    perception = sense()
    thought = plan(perception)
    action = execute(thought)
    observe(action)
```
````

### Math Inline

```markdown
损失函数定义为：$L = \sum_{i=1}^{n}(y_i - \hat{y}_i)^2$

其中 $\hat{y}_i$ 是模型预测值
```

### Last Page

```markdown
<!-- _class: lastpage -->
<!-- _footer: 敬业乐群 -->
<!-- _paginate: "" -->

###### 谢谢大家！
```

## Key Syntax Reminders

| Element | Syntax |
|---------|--------|
| Page break | automatic via `headingDivider: [2,3]` — do NOT use `---` |
| Local class | `<!-- _class: toc_a -->` |
| Local header | `<!-- _header: content -->` |
| Local footer | `<!-- _footer: content -->` |
| Hide header | `<!-- _header: "" -->` |
| Hide footer | `<!-- _footer: "" -->` |
| Hide page number | `<!-- _paginate: "" -->` |
| Fit text | `<!-- fit -->` (auto-size text to fit) |

## Image Path Best Practices

Always use output-relative paths:
- Output: `images/logo.png`
- Source images: `images/8-1.png`

In source markdown, images might be `../images/xxx.png` — remap to `images/xxx.png` in output.
