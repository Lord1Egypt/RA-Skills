---
name: xiaohongshu-content
description: >
  将文章、技术文档等内容转换为适合小红书发布的 HTML 格式，生成封面图和内容截图，配好标题和正文摘要。
  用户提供原始内容（Markdown 或纯文本）后，AI 生成适配小红书风格的多图 HTML 页面，并调用截图工具生成可直接发布的图片。
  适用于：技术博客分享、知识干货、產品介绍、营销内容等。
---

# 小红书内容生成技能

## 功能概述

将任意文章/内容转换为**小红书风格**的 HTML 页面，输出多张可截图发布的图片，并附上**标题 + 正文摘要**。

支持**两种风格**：
- 🎨 **热情风**（红色系）：#FF6B6B → #FF8E53 橙红渐变，适合激情、励志、营销类内容
- 🔬 **科技风**（蓝紫系）：#4A90E2 → #7B68EE 蓝紫渐变，适合技术干货、科普、编程类内容

---

## 风格选择

| 风格 | 主色调 | 渐变 | 适用场景 |
|------|--------|------|----------|
| **热情风** | #FF6B6B (珊瑚红) | #FF6B6B → #FF8E53 | 营销/励志/个人成长/情感类 |
| **科技风** | #4A90E2 (科技蓝) | #4A90E2 → #7B68EE | 技术干货/编程/数据库/架构类 |

生成内容时，根据内容主题自动选择风格：
- 数据库、缓存、架构、编程 → **科技风**
- 营销、增长、个人IP、情感 → **热情风**
- 可通过指令指定风格，如"用热情风生成"

---

## 使用方式

### 方式一：发送内容给 AI

直接把你的文章内容发给我（可以是 Markdown 或纯文本），告诉我"帮我生成小红书内容"或"做成适合小红书的格式"。

**示例：**
> "帮我把这篇关于 Redis 缓存的文章做成小红书风格的内容"

**我会自动：**
1. 分析内容结构，提取核心要点
2. 根据内容类型选择合适风格（科技风/热情风）
3. 生成适配小红书的 HTML 页面（封面 + 多个内容区块）
4. 截图并发送给你
5. 提供标题和正文建议

### 方式二：命令行调用

```bash
cd ~/.openclaw/workspace/skills/xiaohongshu-content
bash scripts/generate_content.sh "你的内容" "输出标题" [tech|passion]
```

---

## 输出规格

| 项目 | 说明 |
|------|------|
| **图片数量** | 1张完整长图（包含所有内容） |
| **图片格式** | PNG |
| **图片宽度** | 680px（小红书标准宽度） |
| **图片高度** | 自动（根据内容长度） |
| **HTML输出** | 可在浏览器打开查看完整效果 |
| **截图工具** | wkhtmltoimage |

---

## HTML 模板

技能包含两个预设模板：

### 科技风 (tech_style.html)
- **主色**: #4A90E2 (科技蓝)
- **渐变**: #4A90E2 → #7B68EE (蓝紫渐变)
- **背景**: #F0F4FF / #F8F0FF (淡蓝/淡紫)
- **强调色**: #4A90E2 (蓝), #7B68EE (紫)
- **适用**: 技术干货、编程、数据库、架构、DevOps 等

### 热情风 (passion_style.html)
- **主色**: #FF6B6B (珊瑚红)
- **渐变**: #FF6B6B → #FF8E53 (橙红渐变)
- **背景**: #FFF5F5 / #FFF9F0 (淡粉/淡黄)
- **强调色**: #FF6B6B (红), #FF8E53 (橙)
- **适用**: 营销、个人成长、情感、励志等

### 通用组件

两种风格共用相同的组件结构：
- **封面卡片**：emoji + 标题 + 副标题 + 标签
- **内容卡片**：图标 + 标题 + 副标题 + 要点列表 + 类比框
- **对比表格**：渐变色表头 + 斑马纹行
- **流程图**：渐变按钮 + 箭头
- **徽章标签**：圆角胶囊样式
- **总结网格**：2列 Summary Card

---

## 截图脚本用法

```bash
cd /root/.openclaw/workspace/skills/xiaohongshu-content/outputs

# 生成长图（完整内容）
wkhtmltoimage --width 680 --quality 90 input.html output.png

# Python 截图（可获取精确尺寸）
python3 scripts/take_screenshot.py --input input.html --output output.png --width 680
```

---

## 标题与摘要生成规则

### 标题公式

```
[符号] + [核心关键词] + [效果词] + [平台词]

示例（科技风）：
🔍 一文搞懂MySQL索引核心原理
💡 5分钟理解Redis缓存雪崩
🚀 微服务架构避坑指南

示例（热情风）：
🔥 这个思维模式，悄悄拉开了差距
✨ 3个技巧，让你的效率翻倍
💪 坚持30天，发生惊人变化
```

### 摘要公式

```
[一句话概括价值] + [时间/难度暗示] + [行动引导]

示例：
Redis缓存穿透、击穿、雪崩一篇全搞懂，收藏慢慢看～
#Redis #缓存技术 #后端开发 #知识分享
```

### 标签策略

- 3-5个标签
- 结构：1个领域词 + 1-2个技术词 + 1个平台词 + 1个情绪词
- 示例：#MySQL #数据库索引 #技术干货 #知识分享

---

## 依赖项

| 依赖 | 用途 | 安装 |
|------|------|------|
| Python3 | 截图脚本 | 系统自带 |
| wkhtmltoimage | HTML渲染引擎 | `apt install wkhtmltopdf` |
| ImageMagick | 图片裁剪 | `apt install imagemagick` |

---

## 文件结构

```
xiaohongshu-content/
├── SKILL.md                    # 本技能说明
├── scripts/
│   ├── generate_content.sh     # 内容生成主脚本
│   ├── take_screenshot.py      # Python截图工具
│   └── open_preview.sh         # 浏览器打开预览
├── templates/
│   ├── tech_style.html         # 科技风模板（蓝紫渐变）
│   └── passion_style.html      # 热情风模板（红橙渐变）
└── outputs/                    # 生成的内容目录
```

---

## 示例输出

用户提供内容 → AI 生成以下内容：

**标题：** 🔍 MySQL 索引全景图解｜用图书馆类比秒懂索引底层逻辑

**正文：**
> 聚簇索引、非聚簇索引、ICP、MRR、GROUP BY、最左前缀 —— 这篇用"图书馆"类比帮你彻底搞懂！
> 收藏慢慢看 💪
> #MySQL #数据库索引 #技术干货 #知识分享 #后端开发

**图片：** 1 张完整长图（可发布到小红书）

---

## 数学公式渲染

如果内容包含数学公式，需要使用 **katex** 进行渲染。

### 引入方式

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
```

### 渲染方式

公式使用 `katex.render()` 渲染到指定的 `<span>` 或 `<div>` 元素中：

```javascript
katex.render(
  "\\text{score}(t,d) = IDF(t) \\times \\frac{f(t,d) \\cdot (k_1 + 1)}{f(t,d) + k_1 \\cdot (1 - b + b \\cdot \\frac{|d|}{avgdl})}",
  document.getElementById("formula-main"),
  { displayMode: true, throwOnError: false }
);
```

### 注意事项

- **注意大小写**：CDN 加载的是小写 `katex`，调用时也要用小写
- **使用 `window.onload`**：确保 DOM 加载完成后再渲染公式
- **给公式留空容器**：先在 HTML 中放一个空的 `<span id="formula-xxx"></span>`，JS 渲染到容器中
- **设置 `displayMode: true`**：公式较长时使用行内显示模式

### 示例公式容器

```html
<div class="formula-box">
  <span id="formula-main"></span>
</div>
```

---

## 注意事项

1. **图片宽度固定 680px**，适配小红书笔记宽度
2. **长图高度根据内容自动增长**，完整包含所有信息
3. **标签使用 emoji + 文字**，增加视觉吸引力
4. **摘要控制在 100 字以内**，小红书显示完整
5. **标题控制在 20 字以内**，超过会被截断
6. **风格默认选择**：技术类 → 科技风，营销/个人类 → 热情风
7. **代码块格式**：代码语句之间用 `<br>` 换行保持独立行，函数体/回调/链式调用使用 2 空格缩进，禁止所有代码挤在一行