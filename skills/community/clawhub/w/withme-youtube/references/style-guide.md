# With me. — 视觉风格指南 & Prompt 模板

> 逆向还原自第一批 5 张场景插画（Gemini 3.1 Flash 生成）

---

## 核心风格定义

**画风：** 超写实数字摄影（Photorealistic Digital Photography），模拟高端无反相机拍摄效果。

**关键特征：**
- 镜头暗角（vignetting）
- 浅景深（shallow DOF, ~f/1.4-f/2.8）
- 窗外散景光斑（bokeh）
- 丁达尔效应（蒸汽在灯光中发光）
- 体积光（volumetric lighting）
- 轻微提升黑色（lifted blacks），电影胶片感
- 明暗对照法（chiaroscuro）

---

## 色彩体系

| 区域 | 色温 | 颜色 |
|------|------|------|
| 室内主色 | 2700-3200K | 深琥珀、焦糖棕、暖橘黄 |
| 窗外冷色 | 6500K+ | 冷蓝灰、深青色 |
| 散景 | 混合 | 暖黄、冷白、红色（车灯）、绿色（信号灯） |
| 暗部 | — | 深巧克力棕，非纯黑 |

**核心：室内暖色 vs 窗外冷色，冷暖互补**

---

## 固定元素（每张必须）

1. ☕ 陶瓷咖啡杯 + 热气升腾
2. 📖 翻开的书本/笔记本
3. 💡 黑色极简工业风台灯（With me. 品牌核心元素）
4. 🪟 大面积雨窗 + 雨滴流痕
5. 🪵 做旧实木家具，可见木纹
6. 💡 爱迪生灯泡/串灯（辅助氛围光）

可选：🍂秋叶 | 🪴绿植 | 🧱砖墙 | 📚书架 | 🧣毯子靠枕

---

## 构图规则

- **视角：** 桌面平视或略俯视（0°-20°），第一人称坐姿 POV
- **景深：** 前景清晰 → 中景虚化 → 背景散景
- **无人物：** 但暗示"人正在使用"
- **允许大面积暗区**

---

## 光影规则

1. 主光源 = 台灯（定向聚光 → 咖啡杯+书本）
2. 辅助光 = 爱迪生灯泡/串灯（多点散射暖光）
3. 背景光 = 窗外街灯（透过雨水 → 散景）
4. 蒸汽必须在灯光中可见（丁达尔效应）
5. Low-key 画面，最亮处仅 5-10%
6. 阴影柔和，暗部保留细节

---

## Gemini Prompt 模板

### 通用前缀（每次必加）

```
Photorealistic digital photography, shot on high-end mirrorless camera. 
Shallow depth of field, cinematic color grading, warm amber interior lighting 
(2700-3200K) contrasting with cool blue-grey rainy exterior. Chiaroscuro 
lighting, volumetric light through steam, lens vignetting, lifted blacks. 
No people visible, but scene implies someone is present.
```

### 5 个原始场景还原 Prompt

**Scene 1 — 窗边全景**
```
[通用前缀]
A cozy industrial-style coffee shop interior on a rainy night. POV from a seated position at a wooden table by a large floor-to-ceiling window. On the aged wooden table: a ceramic coffee cup with latte art on a saucer, an open book, and a minimalist black metal desk lamp casting warm directional light downward. Exposed Edison bulbs hang from the ceiling providing ambient warm glow. Exposed brick wall with built-in wooden bookshelves filled with books, small potted ferns. Through the rain-streaked window, blurred rainy street with soft streetlight bokeh in warm amber and cool blue. Coffee steam visible in lamplight. 35mm lens, table-level POV with slight 15-20° downward angle. 4K, 16:9.
```

**Scene 2 — 秋叶桌面特写**
```
[通用前缀, very shallow DOF f/1.4-f/2.0]
Close-up still life on an aged wooden café table. 3-5 fallen autumn maple leaves in gold and copper-red scattered on the table. A ceramic latte cup with rosetta art on a wooden tray, steam rising catching the light (Tyndall effect). An antique book with yellowed pages open beside it. Minimalist black desk lamp with LED panel head casting side light from upper left. Dark cloth napkin with metal spoon. Through rain-covered window, large soft circular bokeh in warm amber, cool white, red and green. 85-135mm lens, eye-level with table surface. 4K, 16:9.
```

**Scene 3 — 黑咖啡蒸汽特写**
```
[通用前缀, Rembrandt lighting, heavy chiaroscuro]
Dramatic low-key close-up of a dark matte ceramic mug with black coffee, prominent steam spiraling upward illuminated by desk lamp creating volumetric god-ray effect. Black cone-shaped lampshade directs focused warm light from upper left. Brown leather notebook with gold fountain pen beside the mug. Rain-streaked window with large soft warm amber bokeh. Dark aged wood table. 60% of frame in deep shadow. 85mm lens, slightly looking up at the mug. 4K, 16:9.
```

**Scene 4 — 书架阅读角**
```
[通用前缀]
A cozy bookstore-café reading nook. Low angle POV from table level. Foreground: open book on wooden table with steaming coffee cup and minimalist black desk lamp. Mid-ground: armchair/sofa with draped blanket and cushions. Background: floor-to-ceiling bookshelves, Edison string lights draped along shelves. Monstera plant and potted greenery. Through large rain-streaked window on left, rainy city nightscape with neon and car light bokeh in cyan and red. Warm wood flooring. 35mm lens, slightly below eye level. 4K, 16:9.
```

**Scene 5 — 宽景全景**
```
[通用前缀]
Wide establishing shot of a cozy reading corner in a rainy night café. Left 40%: large floor-to-ceiling window with dense rain streaks, city street outside with neon and car lights creating cyan and red bokeh. Right 60%: intimate indoor space with wooden coffee table holding open book, steaming coffee, minimalist black desk lamp. Behind: sofa with blankets, built-in bookshelf alcove with fairy lights, monstera plant. Cold-warm split composition. 28-35mm wide angle, seated eye-level POV. 4K, 16:9.
```

---

## 情绪×空间 — 变量替换指南

制作新场景时替换以下变量，核心元素（台灯、咖啡、书、雨窗）不变：

| 变量 | Melancholy/Café ✅ | Solitude/Study | Warmth/Café |
|------|-------------------|----------------|-------------|
| 情绪词 | melancholy, rainy, cozy | solitude, quiet, late-night, alone | warmth, sunny, golden hour |
| 空间 | coffee shop, café | study room, desk corner | sunny terrace café |
| 窗外 | rainy street, streetlights | empty 3am street, distant lights | afternoon sunlit street |
| 环境音暗示 | rain on window | silence, distant sounds | birds, gentle breeze |
| 特殊元素 | Edison bulbs, brick wall | single lamp, clock | plants, open window |
| 色调微调 | 琥珀暖棕 | 偏冷，加深蓝/靛蓝 | 偏暖金黄，高饱和 |

---

*逆向还原于 2026-03-01 | Gemini 3.1 Flash*
