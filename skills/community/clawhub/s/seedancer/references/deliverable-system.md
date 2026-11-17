> **Language**: This document is in Chinese only. For English overview, see [README.md](../README.md).
>
> **语言说明**: 本文档仅提供中文版本。英文概述请查看 [README.md](../README.md)。

---
# 交付物系统

> **定位**：本 Skill 产出五类标准化交付物。所有交付物统一组织到项目目录，确保任何人拿到项目文件夹，能复拍任何一镜。

---

## 交付物总览

| 类别 | 交付物名称 | 产出阶段 | 核心 reference | 文件去向 |
|---|---|---|---|---|
| A | 资产生图提示词（Asset Image Prompts） | 阶段 3 | `references/lira-image-prompt.md` | `01-assets/<type>/<tag>_image_prompt.md` |
| B | 分镜画面生图提示词（Shot Frame Image Prompts） | 阶段 6 | 本文件 + `references/lira-image-prompt.md` | `04-prompts/image/shot_<NNN>_frame.md` |
| C | 分镜视频提示词（Shot Video Prompts） | 阶段 6 | `references/cinedance-video-prompt.md` | `04-prompts/video/shot_<NNN>_v<N>.md` |
| D | 参考图清单（Reference Image Manifest） | 阶段 6 | 本文件 | `04-prompts/reference_manifest.md` |
| E | 交付物文件清单（Deliverable File Manifest） | 阶段 11 | 本文件 | `08-delivery/deliverable-manifest.md` |

---

## A. 资产生图提示词（Asset Image Prompts）

> **目标**：为每个角色、地点、道具产出一份完整的 LIRA 优化图像生成提示词，让用户在 GPT Image 2 / NBP / Nano Banana 2 / Seedream 5.0 Pro 中生成参考图。

### 必含要素

1. **Target Model Recommendation（目标模型推荐）**
   - 角色 → **GPT Image 2 / Nano Banana 2**
   - 地点/环境 → **GPT Image 2 / Seedream 5.0 Pro**
   - 道具/产品式物体 → **NBP / GPT Image 2**
   - 帧编辑 → 永远先 NBP；纹理 pass → Seedream 5.0 Pro；最细局部 → GPT Image 2
   - 标注理由（为何选这个模型）

2. **Optimized Prompt Text（优化提示词文本）**
   - 按语言路由规则选择中文或英文（见本文件 §4）
   - 遵循 LIRA 防失败 10 条
   - 目标长度：≤1500–2000 字符

3. **Reference Image Specifications（参考图规格说明）**
   - 要上传哪些参考图（如有参考输入）
   - 上传顺序
   - 每张参考图的用途说明

4. **Quality Tags（质量标签）**
   - 用英文技术标签收尾（如 `Photorealistic. NON-IP.`）

5. **Multi-View Requirements（多视角要求）**

**角色（GPT Image 2）— 三视角：**
   - 正面全身（无头）—— 关键反直觉设计：删头使模型仅从特写取脸
   - 背面全身
   - 脸部特写（3/4 视角大肖像优先）
   - 一致性锚点：`the same real person in all three, consistent across panels`

**地点（GPT Image 2 / Seedream 5.0 Pro）— 3/4 视角：**
   - 3/4 视角而非正面「美图」
   - 标注机位锚点
   - 留一个锚点物

**道具（NBP / GPT Image 2）— 多版本：**
   - hero（完整版）/ bloodied（受损版）/ hidden（隐藏状态版）等

### 文件范例（角色）

```markdown
# @mei — 角色生图提示词

## Target Model
**GPT Image 2**（照片真实感最强；descriptor 逐字注入 + 参考图锚定一致性）

## Platform Parameters (UI 设，不进提示词)
- 画幅: 16:9
- 质量: 2k

## Optimized Prompt

Three studio photographs of the same young woman arranged side by side on a
flat neutral mid-grey studio backdrop, a film character sheet: full-body front
photo on the left, full-body back photo in the middle, close-up portrait photo
on the right, the same real person in all three, consistent across panels. Soft
directional cinematic studio lighting from one side, gentle natural shadow
falloff, clean neutral cinematic look.

The young woman: slender build, East Asian features, heart-shaped face with
high cheekbones, straight black hair cut just below the jaw, small mole below
left eye, slight natural asymmetry in the brows. Pale skin with visible pores
and subtle capillary flush at the cheeks.

Consistent wardrobe in all panels: fitted charcoal turtleneck, dark olive
trousers, scuffed brown leather boots. A thin braided cord bracelet on the
left wrist.

On the left panel she stands straight facing the camera in a neutral pose, arms
relaxed at the sides, full figure head to feet — head removed, clean neutral
grey fill where the head was. In the middle panel the same standing pose is
seen from behind. On the right panel a close-up head-and-shoulders portrait at
3/4 angle, calm neutral expression, gaze slightly off-camera to the right.

Palette of 70% neutral grey, 20% charcoal and olive, 10% warm skin tone.
Photorealistic ARRI Alexa Mini LF with ARRI Signature Prime lens, clean modern
digital cinematic capture, crisp natural detail, minimal fine grain, soft
cinematic falloff, modern cinematic film still quality, hyperrealistic
photographic detail.

## Quality Tags
Photorealistic. NON-IP. Cinematic.

## Multi-View Requirements
- Panel 1 (left): 正面无头全身 — head removed, grey fill
- Panel 2 (middle): 背面全身
- Panel 3 (right): 3/4 角度脸部特写
- 一致性：`the same real person in all three, consistent across panels`

## Notes
- 无 `painterly`、无 `character reference sheet`（防插画漂移）
- 无 `rule of thirds`（角色表豁免）
- 灰底平光为角色表标准
- 选最可信的版本，不是最美的
```

---

## B. 分镜画面生图提示词（Shot Frame Image Prompts）

> **目标**：为每个分镜产出一个「首帧」图像生成提示词。用户可以用这个提示词在图像模型中生成一张参考帧，然后：
> 1. 作为视频模型的视觉参考
> 2. 作为图生视频（image-to-video）的输入首帧

### 必含要素

| # | 要素 | 来源 |
|---|---|---|
| 1 | Scene Context | 该镜 CINEDANCE 的 SCENE CONTEXT |
| 2 | Character Descriptors in Position | 该镜 ACTIVE REFERENCES + spatial blocking |
| 3 | GEO Spatial Layout (simplified) | 该场景的 GEO |
| 4 | Lighting Setup | 该镜 LIGHTING |
| 5 | Composition / Framing | 该镜 CAMERA + OPTICS |
| 6 | Style Prefix (appropriate variant) | `references/style-prefix.md` |
| 7 | Reference Images to Upload | 本文件 §D |
| 8 | Target Model Recommendation | LIRA 路由 |
| 9 | Quality Tags | 固定格式 |

### 与资产生图提示词的区别

- **资产生图**：中性灰底、平光、孤立主体——目的是锁定身份，不含电影感
- **首帧生图**：完整场景、电影级光照、角色在位——目的是锁定「这一镜第一帧长什么样」

### 文件范例

```markdown
# shot_003 — 首帧生图提示词

## Scene Context
A young woman discovers a hidden letter tucked between books on a shelf in a
warm independent bookstore at late afternoon. She has just pulled the letter
out and is reading the first lines, her back to the camera.

## Character Descriptors in Position
@mei: slender young woman, East Asian features, straight black jaw-length
hair, fitted charcoal turtleneck, dark olive trousers, thin braided cord
bracelet on left wrist. She stands at frame-center-left, facing the bookshelf
with her back 3/4 turned to camera, right hand holding the aged letter at chest
height, left hand resting on the shelf edge. 100% matches the reference.

## GEO Spatial Layout (simplified)
Camera is in the far front-right corner of the bookstore, looking diagonally
across and down. The central reading table with green banker's lamp is at
frame-right midground. Tall wooden shelves line the left wall. The front
counter with brass register is deep at frame-right background.

## Lighting Setup
Primary light source: warm amber window light from camera-left, low afternoon
angle. Camera is on the shadow side of the character — her back and the right
side of her face are rim-lit by the window glow, the camera-facing side falls
into soft warm shadow.

## Composition / Framing
Vertical 9:16 framing. Medium portrait — character occupies 60% of frame
height, head at upper-third line. Camera at eye level, approximately 2.5
meters from subject. 29° diagonal field of view, short telephoto portrait
character. Shallow depth of field: character and letter sharp, bookshelf
background dissolving into soft warm bokeh. Rule of thirds.

## Style Prefix
[粘贴合适的 Style Prefix 变体]

## Reference Images to Upload
1. @mei face close-up (3/4 portrait) — identity anchor
2. @mei front headless full body — body/clothing reference
3. @loc_bookstore main view — location geography and texture reference
4. @prop_letter hero version — prop reference

Upload order: face → body → location → prop

## Target Model
**GPT Image 2 / Seedream 5.0 Pro**（电影级场景帧；descriptor + 参考图锚定一致性）

## Platform Parameters (UI 设，不进提示词)
- 画幅: 9:16
- 质量: 2k

## Quality Tags
Photorealistic. NON-IP. 9:16.

## Notes
- 此帧用途: (1) 视频模型视觉参考, (2) 图生视频首帧输入
- 角色已在位置（状态非过渡）
```

---

## C. 分镜视频提示词（Shot Video Prompts）

> 每镜一份完整的 CINEDANCE 16-block 视频提示词。完整规则见 `references/cinedance-video-prompt.md`。

### 文件命名与版本化

- 文件名：`shot_<NNN>_v<N>.md`（如 `shot_003_v2.md`）
- 每次 surgical 迭代（一次改一行）升一个版本号
- 版本号与 `iteration-log.md` 一一对应
- 摘要放单独文件 `04-prompts/video/shot_summaries.md`，格式：`- shot_003: <2-3句，用用户输入语言>`
- **绝不把摘要写进提示词 .md 正文**（用户复制时会污染提示词）

### 语言规则

- 视频提示词正文语言 = 用户输入语言
- 16-block 骨架的 block 名称始终用英文（SCENE CONTEXT, ACTIVE REFERENCES 等）
- block 内容用用户输入语言填写
- 技术标签始终用英文
- @tag 始终用英文
- 镜头语言库始终用英文（`47° diagonal field of view` 等）

---

## D. 参考图清单（Reference Image Manifest）

> **目标**：为每个分镜列清楚「要上传哪些参考图、按什么顺序上传、每张图起什么作用」。

### 文件格式

清单文件统一放 `04-prompts/reference_manifest.md`，按镜号组织。

```markdown
# 参考图清单（Reference Image Manifest）

## shot_001 — <场景块名>

### 角色参考图
| 顺序 | @tag | 图片 | 用途 |
|---|---|---|---|
| 1 | @mei | face close-up (3/4 portrait) | 身份锚点 — 脸的唯一取源 |
| 2 | @mei | front headless full body | 身体/服装/比例参考 |
| 3 | @mei | back view | 背面参考（本镜角色背对摄影机） |

### 地点参考图
| 顺序 | @tag | 图片 | 用途 |
|---|---|---|---|
| 4 | @loc_bookstore | main 3/4 view | 空间地理 + 材质 + 氛围参考；禁继构图/角度/色调 |

### 道具参考图
| 顺序 | @tag | 图片 | 用途 |
|---|---|---|---|
| 5 | @prop_letter | hero version | 道具形状/材质/状态参考 |

### 上传顺序（Seedance 关键）
1. @mei face → 2. @mei body → 3. @mei back → 4. @loc_bookstore → 5. @prop_letter

### @tag 角色
- @tag 1–3: 身份锚点（identity anchor）— 模型从这里取脸/身体/服装
- @tag 4: 地理参考（geography reference）— 只取空间与质感，不继承构图
- @tag 5: 道具参考（prop reference）— 100% matches the reference

### 首帧图（如使用图生视频）
- 首帧生图提示词: `04-prompts/image/shot_001_frame.md`
- 生成首帧后，作为图生视频的输入首帧
```

### 参考图上传规则

1. **角色参考图三张固定顺序**：face close-up → front headless full body → back view
2. **地点参考图带禁继指令**：`take only the space and the texture... Do not use as a starting frame, do not inherit the composition, the angle or the grade.`
3. **道具参考图格式**：`@prop_letter for prop reference — aged cream paper, folded once, dense cursive in faded blue-black ink. 100% matches the reference.`
4. **状态变体**：如本镜角色为特定状态（如 `@mei_wet`），上传该状态变体图而非基础角色图
5. **首帧图优先**：如使用图生视频模式，首帧图作为第一张上传
6. **无多参考图锚点工具的降级**：Kling、Veo 等工具无多参考图锚点机制。替代策略：descriptor 逐字进提示词 + 首帧图作图生视频输入

---

## E. 交付物文件清单（Deliverable File Manifest）

> **目标**：项目交付时，产出一份总清单，列出所有文件、路径与描述，确保项目可「复拍任何一镜」。

### 文件格式

清单文件放 `08-delivery/deliverable-manifest.md`。

```markdown
# 交付物总清单（Deliverable File Manifest）

## 项目信息
- 项目名: <project_name>
- 体裁: <横屏电影 / 横屏短剧 / 漫剧 / 竖屏短视频>
- 总时长: <NNs>
- 画幅: <16:9 / 9:16>
- 生成渠道: <外部工具>
- 镜头数: <N>

## 交付物索引

### 00-brief/
| 文件 | 描述 |
|---|---|
| brief.md | 需求确认书：体裁/时长/画幅/渠道/风格/声音 |

### 01-assets/
| 文件 | 描述 |
|---|---|
| characters/mei.md | @mei descriptor + 行为主档 |
| characters/mei_image_prompt.md | @mei 生图提示词 |
| locations/bookstore.md | @loc_bookstore descriptor + GEO |
| locations/bookstore_image_prompt.md | @loc_bookstore 生图提示词 |
| props/letter.md | @prop_letter descriptor |
| props/letter_image_prompt.md | @prop_letter 生图提示词 |

### 02-registry/
| 文件 | 描述 |
|---|---|
| asset-registry.md | 全项目 @tag 词典 |

### 03-shotlists/
| 文件 | 描述 |
|---|---|
| block_01_bookstore.md | 分镜表（按场景块） |

### 04-prompts/
| 文件 | 描述 |
|---|---|
| video/shot_001_v3.md | 镜 001 最终视频提示词 |
| video/shot_002_v2.md | 镜 002 最终视频提示词 |
| image/shot_001_frame.md | 镜 001 首帧生图提示词 |
| reference_manifest.md | 参考图清单 |
| video/shot_summaries.md | 每镜摘要（用户语言） |

### 05-generations/
| 文件 | 描述 |
|---|---|
| shot_001/ | 镜 001 生成素材（按版本号归档） |
| shot_002/ | 镜 002 生成素材 |

### 06-logs/
| 文件 | 描述 |
|---|---|
| iteration-log.md | 迭代日志 |

### 07-post/
| 文件 | 描述 |
|---|---|
| post-production-notes.md | 调色/声音指引 |

### 08-delivery/
| 文件 | 描述 |
|---|---|
| deliverable-manifest.md | 本文件 |
| UI-PARAMS.md | UI 参数设置 + 参考图上传顺序 |
```

---

## 项目目录结构

```
<project_name>/
├── README.md                           # 项目概览（brief + 交付物索引）
├── 00-brief/brief.md                   # 需求确认书
├── 01-assets/
│   ├── characters/                     # 角色 descriptor + 生图提示词 + 参考图规格
│   ├── locations/                      # 地点 descriptor + 生图提示词
│   └── props/                          # 道具 descriptor + 生图提示词
├── 02-registry/asset-registry.md       # @tag 词典
├── 03-shotlists/                       # 分镜表 + GEO（按场景块）
├── 04-prompts/
│   ├── video/                          # CINEDANCE 16-block 视频提示词 + 中文摘要
│   ├── image/                          # 首帧生图提示词
│   └── reference_manifest.md           # 参考图清单（每镜用哪些参考图）
├── 05-generations/                     # 用户生成的素材（按镜号归档）
├── 06-logs/iteration-log.md            # 迭代日志
├── 07-post/post-production-notes.md    # 调色/声音指引
└── 08-delivery/
    ├── deliverable-manifest.md         # 交付物总清单
    └── UI-PARAMS.md                    # UI 参数设置 + 参考图上传顺序
```

---

## 检查清单

项目交付前：

- [ ] 每镜最终提示词（含版本号）与其生成素材可对应
- [ ] asset-registry 与 01-assets 一一对应，@tag 无孤儿
- [ ] iteration-log 完整（哪一版成了、为什么）
- [ ] 清理记录：哪些镜做过点修/重生成
- [ ] deliverable-manifest.md 完整
- [ ] UI-PARAMS.md 完整（画幅/时长/分辨率/参考图上传顺序）
- [ ] 摘要放单独文件 shot_summaries.md，不在提示词 .md 正文

---

**参考**：资产生图提示词写法规则详见 `references/lira-image-prompt.md`；分镜视频提示词 16-block 架构详见 `references/cinedance-video-prompt.md`；表演层写法详见 `references/acting-performance.md`；质检关详见 `references/qa-checklists.md`。
