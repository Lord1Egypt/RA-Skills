# YouMind 风格 Prompt 模板

本文档提供 AI 图片生成的 Prompt 模板和示例。所有 Prompt 均为英文，以获得最佳生成效果。

---

## 基础模板

```
[IP角色描述], [视觉动作], [视觉结构描述], [UI装饰元素],
2D flat vector illustration, YouMind style, professional infographic aesthetic,
clean lines, soft shadows, vibrant gradient background (blue to yellow OR blue to purple),
16:9 aspect ratio, ample copy space on the [left/right/bottom] side,
floating UI elements, cute and friendly, minimal and clean composition
```

---

## 各场景 Prompt 示例

### 封面页

```
[IP角色描述] standing confidently in the center, waving hello,
surrounded by floating UI elements (code editor window, chat bubbles, notification badges, network dots),
2D flat vector illustration, YouMind style, professional infographic aesthetic,
clean lines, soft shadows, vibrant blue-to-yellow gradient background,
16:9 aspect ratio, large copy space on the bottom for title text,
floating UI elements, cute and friendly, minimal and clean, hero shot composition
```

### 递进/成长页

```
[IP角色描述] walking along a winding path from bottom-left to top-right,
passing through 4 milestone markers (each with a small icon),
the path glows progressively brighter from start to end,
2D flat vector illustration, YouMind style, professional infographic aesthetic,
clean lines, vibrant blue-to-purple gradient background,
16:9 aspect ratio, copy space on the right side,
floating progress bar at top, small achievement badges floating nearby,
cute and friendly, growth journey visualization
```

### 数据/成就页

```
[IP角色描述] standing next to a giant floating number "1,157",
looking up with amazed expression, small sparkles around the number,
floating stat bubbles nearby showing percentages and trend arrows,
2D flat vector illustration, YouMind style, professional infographic aesthetic,
clean lines, vibrant blue-to-yellow gradient background,
16:9 aspect ratio, copy space on the left side,
floating UI notification badges, data dashboard elements in background,
cute and friendly, celebration moment
```

### 对比页

```
[IP角色描述] standing in the center between two floating screens,
left screen shows old/grey interface (faded), right screen shows new/colorful interface (glowing),
a large arrow points from left to right,
2D flat vector illustration, YouMind style, professional infographic aesthetic,
clean lines, vibrant blue-to-purple gradient background,
16:9 aspect ratio, copy space at the bottom,
floating comparison labels, before/after indicators,
cute and friendly, transformation visualization
```

### 流程页

```
[IP角色描述] operating a control panel at the start of a pipeline,
3 connected modules flowing left to right with arrows between them,
each module is a rounded rectangle with an icon inside,
2D flat vector illustration, YouMind style, professional infographic aesthetic,
clean lines, vibrant blue-to-yellow gradient background,
16:9 aspect ratio, copy space on the right side,
floating code snippet window, gear icons, data flow particles,
cute and friendly, workflow visualization
```

### 并列/多项页

```
[IP角色描述] in the center, surrounded by 4 floating info cards,
each card has a colorful icon and a short label,
cards are arranged in a semi-circle above and around the character,
2D flat vector illustration, YouMind style, professional infographic aesthetic,
clean lines, vibrant blue-to-purple gradient background,
16:9 aspect ratio, copy space on the bottom,
floating tag bubbles, small decorative dots and lines,
cute and friendly, feature showcase layout
```

### 结尾页

```
[IP角色描述] standing on a hilltop with arms raised in victory pose,
looking toward a bright sunrise on the horizon,
small confetti and star particles floating around,
2D flat vector illustration, YouMind style, professional infographic aesthetic,
clean lines, vibrant blue-to-yellow gradient background,
16:9 aspect ratio, large copy space on the top for closing message,
floating heart and star icons, celebration mood,
cute and friendly, inspiring conclusion
```

---

## Prompt 组装规则

1. **IP 角色描述**必须在 Prompt 最前面，确保角色是画面主体
2. **视觉动作**紧跟角色描述，要具体（不是 "standing"，而是 "standing on top of a giant bar chart, pointing upward"）
3. **风格关键词**必须包含：`2D flat vector`, `YouMind style`, `professional infographic`
4. **背景**只用两种：`blue to yellow` 或 `blue to purple`，根据情绪选择（暖/成就用蓝黄，冷静/专业用蓝紫）
5. **Copy Space**必须指定方向，确保文字有地方放
6. **禁止出现的词**：`realistic`, `3D`, `photographic`, `dark`, `complex background`, `text`（避免 AI 在图中生成文字）

## 背景色选择指南

| 情绪/场景 | 推荐渐变 |
|---------|---------|
| 开场/欢迎/温暖 | blue to yellow |
| 成就/庆祝/能量 | blue to yellow |
| 分析/技术/冷静 | blue to purple |
| 挑战/对比/转折 | blue to purple |
| 结尾/展望/希望 | blue to yellow |
