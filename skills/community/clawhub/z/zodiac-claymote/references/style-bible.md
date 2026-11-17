# 画风规范 · Style Bible

黏土软萌风（噜噜系内核）的技术拆解。同一套表情包必须**全程锁定同一组参数**，否则画风会飘。

---

## 1. 材质与表面

| 维度 | 参数 |
|---|---|
| 主材质 | 聚合物黏土（polymer clay）/ 软胶（soft vinyl），**不是**毛绒、**不是**陶瓷 |
| 光泽 | 哑光至半哑光，轻微次表面散射（SSS）让边缘透出暖光 |
| 表面细节 | 可见轻微指纹压痕、指腹抹痕、接缝线；无贴图纹理 |
| 边缘 | 全部圆角倒边（rounded bevel），禁止锐角、尖刺、硬折线 |
| 重量感 | 看起来"实心、压手"，不是充气感 |

**关键英文词**
```
soft polymer clay material, smooth matte surface with subtle fingerprint marks,
rounded beveled edges, no sharp corners, solid handmade clay texture,
soft subsurface scattering on edges
```

---

## 2. 比例与体型

- 头身比 **1:1 到 1:1.5**（头几乎等于身体）
- 身体 = 一个圆球/水滴形；四肢 = 短粗小圆柱，**手是圆球状肉球**（避免手指问题）
- 手脚长度 ≈ 头宽的 1/3
- 眼睛占脸部宽度 40–50%，位置偏下（幼态）
- 眼睛形式：**黑豆豆眼 + 高光点**，或**弯月眼**（笑）——不要用写实的眼球虹膜

**关键英文词**
```
chibi proportions, head-body ratio 1:1, round ball body, short stubby limbs,
round mitten hands without visible fingers, big glossy bean eyes with highlight dots,
low-set eyes for babyish look
```

---

## 3. 配色系统

规则：**主体高饱和暖色 + 背景低饱和浅色**，饱和度差拉开主体。

| 用途 | 色值 | 说明 |
|---|---|---|
| 背景常用 | `#F5EFE6` 米白 / `#FCE8E8` 淡粉 / `#E8F0F7` 淡蓝 / `#EAF3EA` 淡绿 | 单一纯色或极简渐变 |
| 描边 | 无外描边（黏土风靠光影分离，不靠黑边） | 少数情况用同色系深一度勾边 |
| 阴影 | `#000000` 10–15% 透明的柔和接触阴影 | 不要纯黑硬阴影 |
| 腮红 | `#FF9AA2` 30% 透明，圆形贴于眼下 | 增加软萌度 |
| 高光 | 白色 60% 透明的窄条，在头顶与左肩 | |

**每个生肖的固定主色见 `zodiac-characters.md`，一套内不混用他人配色。**

---

## 4. 打光

```
warm studio three-point lighting, soft key light from upper left 45°,
gentle fill light, subtle rim light on shoulder, soft contact shadow beneath,
global illumination, no harsh specular highlights
```
- 色温偏暖（约 4500K）
- 阴影柔和、边缘虚化
- 禁止强反光、禁止金属高光、禁止戏剧性明暗对比

---

## 5. 镜头与构图

```
three-quarter front view, slight 15-degree high angle, centered composition,
subject fills 75% of frame, clean negative space around, square 1:1
```
- 表情包一律**正面或 3/4 侧**，不要全侧面、不要背面（认不出情绪）
- 主体占 70–80%，四周留白供后期加文字
- 背景允许极简微场景（一张桌、一个沙发角），但**不抢主体**

---

## 6. 表情设计语言

情绪靠三件套同步表达，缺一个就会"表情不到位"：

| 元素 | 变化方式 |
|---|---|
| 眼睛 | 豆豆眼（平静）/ 弯月（开心）/ 竖线（无语）/ 螺旋蚊香眼（晕）/ 泪汪汪高光大眼（委屈）/ 白眼（不屑） |
| 嘴 | 小 o（惊讶）/ 波浪线（纠结）/ 大开口（哭/笑）/ 一字（无语）/ 下弯（委屈） |
| 眉 | 八字（委屈）/ 倒八（生气）/ 上扬（得意）/ 平（冷漠） |

**漫画效果符号**（放在头顶或身侧，同材质）：
汗滴 💧 / 怒气十字 ‼ / 惊叹号 ❗ / 问号 ❓ / 爱心 ❤ / ZZZ / 火焰 🔥 / 闪电 ⚡ / 黑线（无语）/ 星星眼 ✨

**分寸感**：负面情绪也要可爱化。生气 = 鼓腮帮 + 皱眉 + 小怒气符号，**不是**狰狞咆哮。

---

## 7. 通用负向提示词（必带）

```
realistic photography, photorealistic, human face, human skin, horror, creepy, gore,
extra limbs, extra fingers, deformed hands, mutated body, asymmetric eyes, cross-eyed,
text, letters, watermark, logo, signature, artist name, brand mark,
blurry, lowres, jpeg artifacts, noise, oversaturated, dark background, busy background,
sharp spikes, metallic gloss, plastic glossy sheen, fur texture, ceramic glaze,
multiple characters, split panel, comic frame
```

中文图生模型补充：`文字、水印、签名、多人、九宫格、边框、写实照片、恐怖、金属反光`

---

## 8. 画风一致性锁定

同一套表情包，以下 5 项必须逐字一致，一张都不能改：
1. 材质句（soft polymer clay material…）
2. 打光句（warm studio three-point lighting…）
3. 镜头句（three-quarter front view…）
4. 背景色（整套用同一个，或同一色系的 2–3 个）
5. 负向提示词

**变化的只有**：生肖物种、配色、服装道具、动作表情、微场景。
