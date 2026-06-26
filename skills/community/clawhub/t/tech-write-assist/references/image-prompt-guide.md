# AI 配图 Prompt 工程指南

## 通用原则

1. **使用英文 prompt** — Seedream 5.0 Lite 对英文 prompt 效果最佳
2. **自然语言描述** — 用完整句子描述期望画面，而非关键词堆砌
3. **不要求中文文字渲染** — AI 生成中文文字效果差，封面文字后期叠加
4. **明确指定风格和氛围** — 具体的风格关键词比模糊描述效果好
5. **指定构图和色调** — 帮助保持一组配图的视觉统一性

## 各平台配图 Prompt 模板

### X Thread 配图

**封面图 (x_cover)** — 16:9

```
A modern, clean technical illustration showing [核心技术概念的视觉描述]. 
Minimalist design with a dark navy background, featuring [关键视觉元素]. 
Subtle geometric patterns and data flow lines. Professional tech company 
presentation style. High contrast, crisp edges, digital art.
```

**技术图 (x_tech)** — 16:9

```
A professional technical diagram illustrating [技术方法/架构的具体描述]. 
Clean layout with labeled components, directional arrows showing data flow. 
Light background, modern flat design style. Colors: blue, teal, and grey 
palette. Suitable for academic presentation.
```

### 小红书-好物推荐配图

**封面图 (xhs_casual_cover)** — 1:1

```
Eye-catching social media graphic with a vibrant gradient background 
(purple to blue or orange to pink). Central visual element: [与技术相关的
友好图标或插画]. Modern, playful design aesthetic. Clean composition with 
ample white space for text overlay. Trendy, youthful, tech-lifestyle vibe.
```

**功能展示图 (xhs_casual_N)** — 3:4

```
Clean infographic-style illustration showing [功能/亮点的可视化描述]. 
Soft pastel color scheme with [accent color] highlights. Rounded corners, 
friendly icons, modern UI elements. The mood should feel approachable and 
exciting, like discovering a useful new app. Vertical portrait layout.
```

### 小红书-技术揭秘配图

**封面图 (xhs_tech_cover)** — 1:1

```
Dramatic tech-reveal style graphic with a dark background and glowing 
[neon blue / electric purple] accents. Central visual: [技术核心概念的
戏剧化表现]. Futuristic UI elements, holographic effects, data streams. 
The mood should evoke "breaking tech news" or "insider knowledge". 
High-impact, bold composition.
```

**技术拆解图 (xhs_tech_N)** — 3:4

```
Technical breakdown illustration showing [技术组件/流程的具体描述]. 
Dark theme with glowing connection lines and node highlights. Layered 
architecture visualization with labeled sections. Futuristic digital 
art style, cyberpunk-lite aesthetic. Vertical portrait format.
```

**数据对比图 (xhs_tech_data)** — 3:4

```
Visually striking data comparison graphic showing [对比内容描述]. 
Bar charts or radar charts with glowing [color] bars against a dark 
background. Clear visual hierarchy highlighting the winning metric. 
Modern dashboard aesthetic. Vertical portrait format.
```

### 微信公众号配图

**头图/Banner (wechat_banner)** — 16:9

```
Cinematic wide-angle visualization of [文章主题的视觉概念]. Rich, 
editorial-quality digital art. Deep blue and dark tones with [accent 
color] highlights. Evokes cutting-edge technology and innovation. 
Professional magazine cover quality. Dramatic lighting with depth.
```

**技术解读图 (wechat_tech_N)** — 16:9

```
Professional technical illustration for a tech article, showing 
[技术要点的具体描述]. Clean, informative design with clear visual 
hierarchy. Color palette: professional blues and grays with [accent] 
highlights. Style reference: high-quality tech blog illustration. 
Wide landscape format suitable for article embedding.
```

**Benchmark 图 (wechat_benchmark)** — 16:9

```
Professional performance comparison visualization showing [数据对比
的具体描述]. Clean chart design with clearly labeled axes and data 
points. Highlighted winning results in [accent color]. White or light 
gray background, corporate presentation quality. Wide landscape format.
```

**氛围图 (wechat_impact)** — 16:9

```
Conceptual digital art representing [行业影响/未来愿景的描述]. 
Cinematic composition with depth and atmosphere. Abstract representation 
of [AI/technology concept]. Rich color palette, dramatic lighting. 
Editorial illustration quality suitable for a prestigious tech publication.
```

## Prompt 优化技巧

### 风格关键词参考

| 风格目标 | 推荐关键词 |
|---------|-----------|
| 专业技术 | `professional, technical, clean, minimalist, diagram, schematic` |
| 科技未来 | `futuristic, digital, cyberpunk, holographic, neon, glowing` |
| 温暖友好 | `warm, friendly, approachable, soft colors, rounded, playful` |
| 编辑出版 | `editorial, cinematic, magazine quality, rich, atmospheric` |
| 数据可视化 | `data visualization, chart, graph, dashboard, infographic` |

### 色调搭配建议

| 平台 | 主色调 | 辅助色 | 情绪 |
|------|--------|--------|------|
| X | 深蓝 #1a1a2e | 青色 #00d2ff | 专业冷静 |
| 小红书-好物 | 渐变粉紫 | 亮橙/亮蓝 | 活泼时尚 |
| 小红书-揭秘 | 深黑 #0a0a0a | 电光蓝/霓虹紫 | 神秘硬核 |
| 微信公众号 | 深蓝 #0d1b2a | 金色/橙色 | 权威大气 |

### 常见问题

- **Q: 图片中需要文字怎么办？**
  A: 不要在 prompt 中要求中文文字。生成纯视觉图片，文字后期叠加。如需英文文字，用双引号包裹: `with text "AI"`

- **Q: 如何保持一组图片风格统一？**
  A: 在所有图片的 prompt 中使用相同的色调描述和风格关键词。例如都加上 `dark navy background, blue and teal accents, flat design`

- **Q: 技术架构图 AI 能画好吗？**
  A: AI 生成的架构图适合做氛围和概念展示。如需精确标注的架构图，建议 AI 生成基础构图后手动标注，或直接使用论文原图。
