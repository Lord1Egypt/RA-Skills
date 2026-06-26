---
name: soap-cut-video
version: 1.0.0
description: "生成肥皂/蜡块切割 ASMR 解压短视频。支持文字描述直接出片，或将实物图片转为切割动效。聚焦整齐切片、截面颜色暴露、粉末掉落的瞬间爽感，配合切割 ASMR 声效。"

tags: [ASMR, 解压, 治愈, 手工感, 短视频, video]

metadata:
  openclaw:
    emoji: "🧼"
    requires:
      bins: [node]

user-invocable: true
---

# 肥皂 / 蜡块切割视频生成

三个爆点让这类视频停留率极高：

- **截面颜色**：渐变蜡、分层彩皂、大理石纹切开的那一刀，颜色比整块更漂亮
- **切面工整**：波浪刀、方块连切、一刀到底，每一帧都是构图
- **声音上头**：蜡的绵密闷响、皂的酥脆碎裂，ASMR 完播率直接拉满

文字描述或一张实物图，直接出片。

**依赖**：本目录 `scripts/video_gen.js` + 运行环境需设置 `WERYAI_API_KEY` + Node.js 18+。不依赖其他 Cursor 技能。

---

## 默认参数

| 参数 | 值 |
|------|----|
| 比例 | 9:16（固定，抖音/快手竖版） |
| 时长 | 5s（短，爆点瞬间） |
| 音频 | 开启（切割 ASMR 是核心） |
| 风格 | 微距俯拍特写，冷白无缝背景，慢动作切片，切面工整清晰可见 |
| 循环衔接 | 否（默认；开启时在 prompt 末尾追加循环关键词） |

---

## 文字描述直接生成切割视频

描述切割对象和切法，构建 prompt 直接出片。适合批量测试不同材质和刀具组合的视觉效果，或快速产出特定解压风格的内容。

说明切割对象（彩色肥皂 / 渐变蜡块 / 分层手工皂 / 大理石纹蜡）和切法（波浪刀 / 方块连切 / 斜切一刀 / 线切细丝），视角偏好可选（俯拍 / 平视 / 45° 斜切追踪）。

收到描述后，根据材质硬度、颜色分布和切法特征构建 prompt，重点强化截面颜色暴露的瞬间、粉末或薄片飞散的弧线、刀刃推进时材质形变的质感。确认参数后执行 `node {baseDir}/scripts/video_gen.js wait --json '…'`（字段与参数表一致），解析 stdout 返回链接。

**生成前确认参数：**

> 即将使用以下参数生成，确认后开始（可直接回复"确认"或告知修改项）：
> - model：（请告知，或由你指定）
> - aspect_ratio：9:16
> - duration：5s
> - generate_audio：true
> - 循环衔接：否（回复"循环"可开启，将在 prompt 末尾追加 `seamless loop` 关键词）

**参数配置：**

| 参数 | 值 |
|------|----|
| aspect_ratio | 9:16 |
| duration | 5 |
| generate_audio | true |

**Prompt 参考（渐变蜡块波浪刀切）：**
> Extreme close-up macro shot, top-down overhead angle, a chunky pastel gradient wax block layered in soft pink-lilac-sky-blue sitting on a cold white marble slab, a wavy-edge palette knife presses slowly downward in 120fps slow motion, the blade splits the wax revealing a breathtaking swirled cross-section of pastel gradient colors, thin wavy shavings curl and tumble away from the perfect cut edge, cold diffused studio light makes the wax surface slightly translucent and glowing, fine wax dust floats in the air backlit by the white light, ASMR dense satisfying crunch-and-squeak of wavy blade through dense wax, minimal white seamless background, no distractions

**Prompt 参考（分层彩色肥皂方块连切）：**
> Eye-level tight medium shot angled slightly downward, a thick rectangular handcrafted soap bar in vivid stacked layers of coral-mint-gold-white sitting on white ceramic tile, a sharp straight cleaver pushes rhythmically through the bar making 6 successive clean slices, each slab drops and fans out in perfect formation to reveal parallel color layers in cross-section, fine chalky soap powder dusts the surface with each cut, warm diffused side lighting casts soft shadows that accentuate each slab's thickness, satisfying dense crumbly ASMR squeak of blade through compressed soap, dark matte background for maximum color contrast

**Prompt 参考（大理石纹蜡一刀斜切）：**
> Dutch angle close-up shot at 30 degrees, a cylindrical white-grey-black marbled wax pillar resting on dark slate surface, a single razor-sharp knife blade enters from the upper-right corner and slices diagonally in one continuous slow push at 60fps, the two halves gradually separate revealing an intricate marbled interior cross-section with swirling grey veins against cream white, the cut face catches cold rim lighting from behind creating a crisp white highlight along the perfect edge, a faint shower of wax micro-particles scatter in the air, deep ASMR low thud of blade through dense wax, minimal dark background

**预期效果：** 切片截面颜色/纹理在慢动作中清晰暴露，切割声与视觉节奏吻合，爽感集中在刀刃推进的 1-2 秒内，适合竖版平台无限刷看。

---

## 实物图片转切割动效

上传一张肥皂或蜡块实物图，生成以该物体为主体的切割动效视频。适合将产品图或现有素材二次利用，快速产出对应的解压内容。

提供图片 URL（必须是可公开访问的 HTTPS 地址）和期望切法（整切一刀 / 多刀连切 / 波浪刀切 / 线切细丝）。识别图片中材质颜色和纹理分布后，生成与原图风格一致的切割动效。

**生成前确认参数：**

> 即将使用以下参数生成，确认后开始（可直接回复"确认"或告知修改项）：
> - model：（请告知，或由你指定）
> - aspect_ratio：9:16
> - duration：5s
> - generate_audio：true
> - image：（你提供的图片 URL）
> - 循环衔接：否（回复"循环"可开启）

**参数配置：**

| 参数 | 值 |
|------|----|
| aspect_ratio | 9:16 |
| duration | 5 |
| generate_audio | true |
| image | 用户提供的图片 URL |

**Prompt 参考（图片实物切割动效）：**
> Close-up macro shot matching the angle of the provided image, a sharp knife blade enters the frame from the top and presses through the soap or wax block in a single slow deliberate cut at 120fps, slicing cleanly from one edge to the other, the two halves slowly separate revealing the internal color layers and texture of the block matching the original object, fine powder particles float upward backlit by cold white studio light, the cut surface catches a clean highlight along the freshly exposed edge, deep satisfying ASMR crunch of blade through dense material, white seamless studio background

**预期效果：** 切割过程与图片原始颜色和纹理保持视觉一致，截面暴露效果与实物材质匹配，声效和慢动作节奏强化爽感。

---

## 使用技巧

### Prompt 增强方向

- **强化截面暴露**：`the cut face reveals`, `cross-section exposed`, `interior color layers emerge`, `split apart revealing`
- **切割质感差异**：蜡用 `dense satisfying crunch`；皂用 `crumbly chalky squeak`；硬质蜡用 `deep low thud`
- **粉末/碎屑飞散**：`fine dust floats in backlit air`, `thin shavings curl away`, `micro-particles scatter`
- **开启循环衔接**时，在 prompt 末尾追加：`seamless loop, first and last frame identical, perfectly looping`

### 常见问题

- 图片 URL 必须是 HTTPS 公网可访问地址，本地路径或私有链接会报错，建议先上传到图床
- 若想突出颜色反差，在 prompt 中明确背景色（深色背景衬托亮色皂块，白色背景适合渐变蜡）
- 方块连切场景建议在 prompt 中指定切片数量（如 `6 successive slices`），避免生成单刀效果

> **注意**：`aspect_ratio` 参数不是所有模型都支持，若调用时报错 1002，尝试去掉该参数后重试。
