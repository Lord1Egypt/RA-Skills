# 插画风格选项

使用时在 prompt 末尾加入对应的风格块，并说明需要哪种风格。

---

## 风格 A：Sketch 极简手绘风（默认）

**适用场景**：流程图、功能说明、产品配图、技术教程  
**参考**：Notion / Linear / BetterClaw 官网插图  
**特征**：白/浅蓝背景，铅笔线条，低饱和柔和配色，简笔火柴人

### 风格块
```
Whimsical hand-drawn sketch illustration, very soft muted pastel colors, light blue-white background, product explainer style like Notion or Linear website. Pencil sketch lines, light watercolor wash, no harsh colors, gentle pastel palette (light blue, soft peach, pale yellow, light gray), charming and friendly, clean minimal layout, white card background with subtle shadow. Simple cute stick figure for human characters. All text in Chinese.
```

### 负面约束
```
No flat vector poster style, no 3D, no photorealistic, no complex background, no dense small text, no watermarks.
```

---

## 风格 B：Watercolor 奶油彩铅水彩风

**适用场景**：PPT 配图、课程讲义、暖色调内容图、中文信息图  
**参考**：老师 image-assistant skill 风格  
**特征**：奶油色纸张底（纸纹可见），彩铅线稿（笔触可见），淡水彩晕染，暖色调，轻涂鸦装饰

### 风格块
```
画幅：16:9 横版信息图。质感：奶油色纸张底（纸纹可见），彩铅线稿（笔触可见）+ 淡水彩上色（轻晕染）。氛围：暖色调、轻涂鸦装饰、趣味但干净。可读性：中文必须清晰可读、无乱码；大字号；少字短句；避免密集小字/段落。版式：留白充足、层级清晰、卡片对齐、箭头醒目。这是唯一允许的基础风格，不得切换成扁平矢量海报风/3D/摄影写实等其他风格。
```

### 负面约束
```
不要扁平矢量海报风、不要3D、不要摄影写实、不要复杂背景/强渐变光效、不要额外小字注解/水印/署名、不要英文与随机字符
```

### 可用布局模板
见 `references/image-assistant-templates/` 目录：
- `16x9-infographic.md` — 通用信息图
- `16x9-contrast-2cards.md` — 两卡对比
- `16x9-3cards-insights.md` — 三卡洞察
- `16x9-cover-roadmap.md` — 封面路线图
- `16x9-5panel-comic.md` — 五格漫画流程

---

---

## 风格 C：Flat Vector Retro 扁平矢量复古风

**适用场景**：NotebookLM 风格 PPT、课程封面、科普内容、复古感信息图  
**参考**：复古插画海报、填色书线稿风格  
**特征**：黑色统一粗细轮廓线、几何简化（树=棒棒糖、建筑=方块）、2.5D等轴测视角、复古柔和配色、奶油色纸纹背景

### 系统提示词（完整版，直接粘贴到 prompt 前）
```
视觉风格与美术指导 (Visual Style & Art Direction)
插画风格： 扁平化矢量插画（Flat Vector Illustration）。必须包含清晰、统一粗细的黑色轮廓线（Monoline/Stroke）。色彩填涂需简洁，仅使用少量阴影，严禁使用渐变色或3D渲染效果。
构图形式： 横向全景式构图（Panoramic），占据版面顶部 1/3 的空间。
线条风格 (Line Work)： 必须使用统一粗细的黑色单线描边（Monoline/Uniform Stroke）。所有物体（建筑、植物、云朵）都必须有封闭的黑色轮廓，类似填色书的线稿风格。线条末端圆润，避免尖锐的棱角。
几何化处理 (Geometric Simplification)： 将复杂的物体简化为基本几何形状。例如，树木简化为棒棒糖形状或三角形，建筑物简化为简单的矩形块面，窗户简化为整齐的小方格网格。不要追求写实细节，要追求"玩具模型"般的可爱感。
空间与透视： 采用平视或稍微俯视的 2.5D 视角（类似等轴测，但更自由）。通过图层的前后遮挡来表现纵深，不要使用大气透视（即远景不要变模糊或变淡），所有图层清晰度一致。
装饰元素： 在空白处添加装饰性的几何元素，如放射状的线条（代表阳光或能量）、药丸形状的云朵、或者是简单的小圆点和星星，以平衡画面的视觉密度。
配色方案： 复古且柔和的色调。
背景： 米色/奶油色（Cream/Off-white）纸张纹理感底色。
强调色： 珊瑚红、薄荷绿、芥末黄、赭石色（Burnt Orange）和岩石蓝。
字体排版：
主标题： 巨大的、加粗的复古衬线体（Retro Serif），体现权威感与优雅感。
副标题： 位于矩形色块内的全大写无衬线体。
正文： 清晰易读的现代无衬线体。

要处理的内容是：
[在此填入具体内容]
```

### 负面约束
```
严禁使用渐变色、3D渲染效果、写实风格、复杂背景、大气透视（远景模糊）
```

### 使用方式
把系统提示词完整复制，将最后一行 `[在此填入具体内容]` 替换成要画的内容描述即可。

---

## 风格 D：Doodle Infographic 白纸手绘知识图风

**适用场景**：概念对比图、方法论海报、拖延机制图、知识卡片、课堂板书感信息图、公众号配图
**参考**：白纸手绘知识图、doodle infographic、拟人蜗牛/脑子、手账/课堂笔记海报
**特征**：白纸背景、铅笔/马克笔线条、便签框/箭头/胶带、小模块很多但不乱、可爱拟人角色、高信息密度、少长段文字

### 风格块
```
Hand-drawn doodle infographic on white paper, pencil sketch outlines, marker highlights, sticky notes, arrows, boxed modules, tape decoration, cute anthropomorphic mascot characters, playful but smart, high-information-density but clean composition, classroom board / notebook poster feeling, Chinese labels, educational editorial illustration, not childish, not photorealistic.
```

### 负面约束
```
No photorealistic, no glossy 3D, no flat corporate vector poster, no dark background, no dense unreadable paragraphs, no messy watermark, no random English text.
```

### 推荐结构
- **对比图**：左右两栏（人类 vs AI / 旧方案 vs 新方案）
- **机制图**：中心主题 + 多个原因/环节模块 + 箭头回路
- **知识海报**：标题 + 4~8 个信息卡片 + 1~2 个拟人角色
- **流程图**：从左到右或从上到下，关键步骤用短句+图标

### 常用角色灵感
- 蜗牛：拖延、慢、磨蹭
- 拟人大脑：心理机制、防御、自我解释
- 小龙虾：AI 代理、认真臭脸、会先分析后动手
- 小人/学生：用户、执行者、学习者

---

## 风格 E：NotebookLM Tech 技术图解风

**适用场景**：产品功能介绍、流程说明、概念图解、技术产品说明书、中等信息密度信息图  
**参考**：NotebookLM 生成的信息图、技术产品说明图  
**特征**：低饱和莫兰迪色系（灰绿、米白、浅棕）、扁平2.5D插画带轻微投影、模块化布局清晰、思源黑体类字体、线性图标+填充色块、右下角可放logo/水印区域

### 风格块
```
Technical infographic illustration, NotebookLM style, low-saturation Morandi color palette (sage green, cream white, light brown), flat 2.5D illustration with subtle drop shadows, modular layout with clear sections, clean geometric icons, minimal line icons + filled color blocks, Source Han Sans / PingFang style typography, professional but friendly, medium information density, not overwhelming, suitable for product feature explanation and process diagrams. All text in Chinese.
```

### 负面约束
```
No high-density small text, no photorealistic, no 3D rendering, no glossy effects, no neon/bright colors, no messy overlapping elements, no complex gradients.
```

### 布局建议
- **左右分栏**：左图右文，或左文右图
- **上下分区**：顶部标题+主图，底部2-4个功能模块
- **模块化卡片**：每个功能一个卡片，图标+短标题+一句话说明
- **流程箭头**：步骤之间用清晰箭头连接

### 与风格C的区别
- 风格C（Flat Vector Retro）：黑色轮廓线、复古配色、填色书感
- 风格E（NotebookLM Tech）：无黑色轮廓线、莫兰迪配色、更现代柔和、适合技术产品说明

---

## 风格选择指南

| 需求 | 推荐风格 |
|------|---------|
| 技术流程图、产品功能说明 | Sketch A |
| 有小人/吉祥物互动的场景 | Sketch A |
| PPT 配图、课程讲义 | Watercolor B |
| 温暖感、故事感的内容 | Watercolor B |
| 需要多张成套配图 | Watercolor B（用模板） |
| 快速单张、现代极简 | Sketch A |
| NotebookLM PPT、复古感封面 | Flat Vector C |
| 科普内容、课程封面、海报 | Flat Vector C |
| 几何简化、填色书线稿风 | Flat Vector C |
| 白纸手绘知识图、方法论、概念对比 | Doodle D |
| 拖延机制、知识卡片、课堂板书感 | Doodle D |
| 拟人蜗牛/脑子/龙虾的高信息密度图 | Doodle D |
| 产品功能说明、技术图解、中等信息密度 | NotebookLM Tech E |
| 现代技术产品说明书风格 | NotebookLM Tech E |
