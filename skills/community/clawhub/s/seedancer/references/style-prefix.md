> **Language**: This document is in Chinese only. For English overview, see [README.md](../README.md).
>
> **语言说明**: 本文档仅提供中文版本。英文概述请查看 [README.md](../README.md)。

---
# Style Prefix

> **逐字粘贴到每个视频提示词的 STYLE block 末尾。** Style Prefix 锁定全局视觉风格，确保跨镜头风格一致性。

---

## 核心原则

### 三条根条款（不可删除）

无论使用哪种变体，这三条**绝不能省略**：

1. **Skin** — 毛孔级真实感，防止塑料脸
2. **Acting** — 湿润活眼 + 眼神光，防止死脸
3. **Continuity** — 无身份漂移，防止换脸

这三条是活人感与跨镜头一致性的底线。

---

## 标准 Style Prefix（电影感原版）

```
Style: Photorealistic — no 3D render, no game engine, no game-cutscene aesthetic.
Cinematography: floating immersive camera that lives with the actors; natural motivated light;
painterly composed frames, strong silhouettes against the light.
Lighting: Natural light only — contre-jour backlight, camera on shadow side, atmospheric haze
throughout. Key light from sky and windows only.
Color: 60:30:10 — dominant / secondary / accent.
Camera: Physical cine lens. 180° shutter motion blur.
Skin: Pore-level realism — vellus hair, asymmetric moles, capillary flush, pore-shadow matching
on-set light.
Acting: Hollywood — micro-pauses before reactions, precise eye-line, wet living eyes with
catch-lights, visible breath and chest rise.
Physics: Gravity and inertia respected — mass has real weight, correct contact shadows. No
floating props.
Composition: Rule of thirds + golden ratio. Every person moving from frame one.
Continuity: Characters, props, environment identical across every cut. No identity drift.
Technical: 24fps smooth motion. 8K detail. No jitter.
Audio: Environmental SFX only. No music. No subtitles.
```

### 技术标签收尾

```
Photorealistic. NON-IP. [画幅]. [时长]s. SFX only. NO CGI. Cinematic.
```

---

## 变体 1：竖屏短视频降格版

适用于 9:16 竖屏短视频。去掉 IMAX/8K，保留三条根条款。

```
Style: Photorealistic — no 3D render, no game engine, no game-cutscene aesthetic.
Cinematography: tight vertical portrait framing; natural motivated light from practical sources;
subject fills 60% of frame vertically.
Lighting: Natural motivated light from in-scene practical sources — dominant warm key from window
or overhead, soft ambient fill from room bounce, rim light on character's back; no flat front fill,
no beauty light; shadows fall naturally with visible depth.
Color: 60:30:10 — dominant / secondary / accent.
Camera: Physical lens. Natural motion blur.
Skin: Pore-level realism — vellus hair, asymmetric moles, capillary flush, pore-shadow matching
on-set light.
Acting: Hollywood — micro-pauses before reactions, precise eye-line, wet living eyes with
catch-lights, visible breath and chest rise.
Physics: Gravity and inertia respected — mass has real weight, correct contact shadows. No
floating props.
Composition: Vertical rule of thirds; subject at left-third or right-third; eyes at upper-third
line.
Continuity: Characters, props, environment identical across every cut. No identity drift.
Technical: High detail. No jitter.
Audio: Environmental SFX only. No music. No subtitles.
```

**关键差异**：
- 去掉 `IMAX`、`8K`（竖屏不需要电影级宏大感）
- `tight vertical portrait framing`（竖屏肖像构图）
- `subject fills 60% of frame vertically`（主体占画面 60% 垂直高度）
- `Vertical rule of thirds`（竖屏三分法）
- `eyes at upper-third line`（眼睛在上三分线）

---

## 变体 2：漫画风格变体

适用于漫剧。保留三条根条款，切换为漫画风格渲染。

```
Style: Manga aesthetic — clean line work, flat color cells, cel-shaded rendering, stylized
proportions, dramatic screen tones for shadows.
Cinematography: dynamic panel-style framing; bold silhouettes; speed lines for motion.
Lighting: High-contrast cel shading — hard shadow edges, minimal mid-tones, dramatic backlight
rim.
Color: Saturated palette with deliberate color coding (e.g., warm tones for protagonist, cool
tones for antagonist). 60:30:10 — dominant / secondary / accent.
Camera: Stylized lens effects — speed lines, impact frames, Dutch angle for tension.
Skin: Stylized manga skin — smooth cel shading, minimal pore detail, but retain asymmetric facial
features and catch-lights in eyes.
Acting: Exaggerated physical commitment — large gestures, clear body language, but retain
micro-pauses and eye-life. Wet living eyes with catch-lights (non-negotiable).
Physics: Stylized physics — exaggerated motion, but mass still has weight and correct contact
shadows. No floating props.
Composition: Panel-style framing; strong diagonals; subject at dynamic angles.
Continuity: Characters, props, environment identical across every cut. No identity drift.
Technical: Clean line work. 24fps smooth motion. No jitter.
Audio: Environmental SFX only. No music. No subtitles.
```

**关键差异**：
- `Manga aesthetic`（漫画美学）
- `cel-shaded rendering`（赛璐璐渲染）
- `stylized proportions`（风格化比例）
- `Exaggerated physical commitment`（夸张肢体动作）
- **但保留**：`Wet living eyes with catch-lights`、`No identity drift`、`mass still has weight`

---

## 变体 3：亮调平台风

适用于广告/品牌片/明亮风格的短视频。

```
Style: Photorealistic — no 3D render, no game engine, no game-cutscene aesthetic. Clean modern
digital capture.
Cinematography: bright, airy framing; high-key lighting; soft shadows; optimistic tone.
Lighting: High-key natural light — dominant key from large soft source (window or sky), minimal
shadow contrast, bright ambient fill. No dark moody shadows.
Color: High-key palette — 60% light tones (white, cream, pastel), 30% mid-tones, 10% accent
color. Bright, optimistic, clean.
Camera: Physical lens. Shallow depth of field for subject isolation. Smooth motion.
Skin: Pore-level realism — vellus hair, asymmetric moles, capillary flush, but bright and clean.
No dark shadows on face.
Acting: Natural, relaxed, approachable — micro-expressions, genuine smiles, open body language.
Wet living eyes with catch-lights (non-negotiable).
Physics: Gravity and inertia respected — mass has real weight, correct contact shadows. No
floating props.
Composition: Rule of thirds; subject centered or at third; clean negative space.
Continuity: Characters, props, environment identical across every cut. No identity drift.
Technical: 24fps smooth motion. High detail. No jitter.
Audio: Environmental SFX only. No music. No subtitles.
```

**关键差异**：
- `bright, airy framing`（明亮、通透的构图）
- `high-key lighting`（高调光）
- `High-key palette`（高调配色）
- `Natural, relaxed, approachable`（自然、放松、亲和的表演）

---

## 三条根条款详解

### 1. Skin（皮肤）

```
Skin: Pore-level realism — vellus hair, asymmetric moles, capillary flush, pore-shadow matching
on-set light.
```

**为什么不能删**：防止塑料脸。没有这条，模型会输出光滑、对称、无毛孔的塑料皮肤。

**效果**：
- `vellus hair`（汗毛）— 皮肤表面有细微毛发
- `asymmetric moles`（不对称的痣）— 打破完美对称
- `capillary flush`（毛细血管潮红）— 皮肤有血色
- `pore-shadow matching on-set light`（毛孔阴影匹配场景光）— 毛孔有真实阴影

### 2. Acting（表演）

```
Acting: Hollywood — micro-pauses before reactions, precise eye-line, wet living eyes with
catch-lights, visible breath and chest rise.
```

**为什么不能删**：防止死脸。没有这条，模型会输出玻璃珠般的死眼。

**效果**：
- `micro-pauses before reactions`（反应前的微停顿）— 思考的痕迹
- `precise eye-line`（精确视线）— 眼睛看向具体目标
- `wet living eyes with catch-lights`（湿润活眼 + 眼神光）— 眼睛有生命
- `visible breath and chest rise`（可见呼吸和胸腔起伏）— 身体有生命

### 3. Continuity（连续性）

```
Continuity: Characters, props, environment identical across every cut. No identity drift.
```

**为什么不能删**：防止换脸。没有这条，模型会在每个镜头重新生成角色外观。

**效果**：
- `identical across every cut`（每个切完全一致）
- `No identity drift`（无身份漂移）— 脸、体型、服装、道具、环境都一致

---

## 使用规则

### 1. 逐字粘贴

Style Prefix 必须**逐字粘贴**到每个视频提示词的 `STYLE` block。绝不缩写、绝不改写。

```
STYLE
[粘贴完整的 Style Prefix]
```

### 2. 选择合适变体

根据项目类型选择变体：
- 横屏电影/短剧 → 标准版
- 竖屏短视频 → 竖屏降格版
- 漫剧 → 漫画风格变体
- 广告/品牌片 → 亮调平台风

### 3. 技术标签收尾

Style Prefix 之后，追加技术标签：

```
Photorealistic. NON-IP. [画幅]. [时长]s. SFX only. NO CGI. Cinematic.
```

**参数**：
- `[画幅]` — `16:9` 或 `9:16`
- `[时长]` — 镜头时长（秒）

**技术标签始终英文**。

### 4. `SFX only. No music.` 是强制的

音乐属于后期，生成版配乐只会碍剪辑。

---

## 与 CINEDANCE 的关系

Style Prefix 是 CINEDANCE 16-block 中 `STYLE` block 的核心内容。

```
STYLE
[粘贴完整的 Style Prefix]

QUALITY
8K detail, pore-level skin, no jitter, no flicker; faces stay exactly their references at every
distance.

POSITIVE CONSTRAINTS
[计数与禁令]

Photorealistic. NON-IP. [画幅]. [时长]s. SFX only. NO CGI. Cinematic.
```

---

## 常见错误

| 错误 | 后果 | 修正 |
|---|---|---|
| 删掉 Skin 条款 | 塑料脸 | 保留三条根条款 |
| 删掉 Acting 条款 | 死脸 | 保留三条根条款 |
| 删掉 Continuity 条款 | 换脸 | 保留三条根条款 |
| 每镜改写 Style Prefix | 风格漂移 | 逐字粘贴，不改写 |
| 在 Style Prefix 里写音乐 | 模型自创配乐 | `SFX only. No music.` 是强制的 |
| 不写技术标签 | 缺少约束 | 始终追加技术标签 |

---

## 检查清单

每镜提示词发出前检查：

- [ ] STYLE block 已逐字粘贴 Style Prefix
- [ ] 三条根条款都在（Skin / Acting / Continuity）
- [ ] 选择了合适变体（标准/竖屏/漫画/亮调）
- [ ] 技术标签已追加（Photorealistic. NON-IP. [画幅]. [时长]s. SFX only. NO CGI. Cinematic.）
- [ ] 没有写音乐（`SFX only. No music.`）
- [ ] 技术标签始终英文

---

**参考**：完整 16-block 架构详见 `references/cinedance-video-prompt.md`；表演系统详见 `references/acting-performance.md`；质检关详见 `references/qa-checklists.md`。
