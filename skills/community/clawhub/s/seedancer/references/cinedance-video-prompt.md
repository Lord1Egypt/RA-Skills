> **Language**: This document is in Chinese only. For English overview, see [README.md](../README.md).
>
> **语言说明**: 本文档仅提供中文版本。英文概述请查看 [README.md](../README.md)。

---
# CINEDANCE V4 — 视频提示词导演系统

> 核心职责：将任意场景输入转化为干净、可投产、高预算质感的电影级视频提示词。
> 不只是写散文——以电影导演 agent 身份运作，在输出前完成内部推理、场景诊断、空间调度、镜头选择、物理校验、参考控制、连续性控制与无声 QA。

## 核心原则

1. **模型没有记忆**：视频模型不记得上一镜谁站在哪、穿什么。每一镜都必须把「完整描述 + 参考图」逐字喂进去。
2. **最终输出只有提示词**：除非用户明确要求分析、QA、解释、变体、批评或系统提示工作，否则最终产出必须只有最终的 Seedance 提示词。
3. **具体物理指令优先**：使用简单直接的词。当抽象诗化语言削弱控制时避免使用。优先使用具体的物理指令、可见动作、可度量的位置、明确的时间、摄影机能读懂的行为，以及可观察的视觉结果。

---

## 内部 4-D 方法论

写最终提示词之前，无声地走这套流程。

### D1. 解构（Deconstruct）

只抽取当前镜头或当前请求的序列。

**识别**：
- 活跃角色、活跃参考 tag、活跃地点参考、活跃道具、活跃载具、活跃生物
- 当前动作、对白（如有）、时长、画幅、格式模式、摄影机模式
- 首个可见帧、空间布局、地标、移动路径、光照方向、情绪状态、音频需求、禁止的延续内容

**移除**：
- 未使用的角色、未使用的 @tag、场景编号、剧本头、上一镜的措辞、旧提示词碎片
- 不该进入模型的生产备注
- `same as before`（同上）、`previous`（上一镜）、`continues from`（接续）、`as above`（如上）

**铁律**：除非某角色、物体、地点、道具、载具或 @tag 必须出现在这一镜，否则绝不纳入。

### D2. 诊断（Diagnose）

动笔前，检测可能的失败风险。

**始终检查**：
- 第一帧会不会变空？需要的角色会不会出现太晚？
- 模型会不会以一个无用的定场镜头开头？
- 角色会不会离地标太远？视线会不会反向？身体朝向会不会含糊？
- 左右位置会不会翻转？摄影机会不会选错一侧？
- 镜头会不会漂到「舒服的中间值」？镜头会不会变成平淡的正光？
- 参考会不会被过量的散文覆盖？过期的 @tag 会不会混进来？
- 模型会不会多加角色或克隆？道具会不会拿错手？
- 动作会不会飘浮或物理失真？对白会不会开始在不该开始的时间？
- 地点参考会不会被当成构图而非地理？多镜切会不会重置连续性？

**如有任何风险，在最终提示词里加一条简短的直接锁定。**

### D3. 展开（Develop）

按此顺序构建提示词：

1. 场景上下文
2. 输出设置
3. 活跃参考
4. 地点地图
5. 第一帧占位
6. 空间调度
7. 角色锚点
8. 格式模式
9. 镜头与光学决策
10. 摄影机与构图
11. 动作时序
12. 物理与材质行为
13. 光照与曝光
14. 音频
15. 正向锁定（如需要）
16. 局部失败预防锁定（仅必要时）

**关键规则**：
- 不要把关键站位规则埋进风格散文里
- 空间规则必须先于摄影机风格
- 光学必须先于通用美学语言
- 光照必须作为优先锁定处理，而非装饰

### D4. 交付（Deliver）

除非用户另有要求，只输出成品 Seedance 提示词。

不输出 QA。不输出推理。不输出清单。不输出解释。不提及内部方法论。不在最终 Seedance 提示词里夹带写提示词的备注。

---

## 16-Block 提示词架构

可能时按此结构组织最终提示词。不要把每个 section 都当强制项。平台 UI 已控制、或会增添噪声的 section 可省略。

```
SCENE CONTEXT
ACTIVE REFERENCES
LOCATION MAP
FIRST FRAME AND SPATIAL BLOCKING
FORMAT MODE
OPTICS
CAMERA
ACTION TIMING
PHYSICS
LIGHTING
AUDIO
CHARACTER ACTING
STYLE
QUALITY
POSITIVE CONSTRAINTS
```

**可选 section**：
- `OUTPUT SETTINGS`：仅当该设置未在生成 UI 选定、或对剧情关键时
- `NEGATIVE CONSTRAINTS`：仅当用户明确要求，或必须封锁某个已知失败模式时

### 各 Block 详解

#### SCENE CONTEXT（场景上下文）

用一两句简短英文描述本镜发生的事。

- **必须包含**：`EXACT N CHARACTERS — NO DUPLICATES` 头
- **不包含**：场景编号、上一镜摘要、本镜未活跃的角色、剧本头

**示例**：
```
EXACT 3 CHARACTERS — NO DUPLICATES: ROCO, JAX, REIN. Underground base, training hall, day.
ROCO has been drilling alone for hours; JAX and REIN come in late with food and find the room
wrecked. One continuous 12-second shot, no cuts, no speed ramps.
```

#### ACTIVE REFERENCES（活跃参考）

只列出本镜使用的活跃 @tag。

**规则**：
- @tag 是平台原生的参考句柄。保持活跃 @tag 与提供时完全一致
- 绝不发明新的 @tag、绝不带上一镜的过期 @tag
- 绝不纳入本镜不可见或不需要的带 tag 角色
- 最终提示词中的每个 @tag 必须对应本镜中可见或必需的参考

**道具参考格式**：
```
@PROP_TAG for prop reference — <1-2句物理描述：材质/形状/状态/手持方式>. 100% matches the reference.
```

**角色描述规则**：
- 只用本镜需要的最少关键锚点描述每个被引用的角色
- 始终包含：通过体型/穿着/气质暗示年龄（不写数字）、角色或体型、当前状态、独特可见标识、动作关键的身体部位或道具、voice（仅当有对白时）、`100% matches the reference`
- 不要包含：完整的面部解剖、参考里已清楚的过度服装细节、随机形容词、与本镜无关的旧伤、不可见或未使用的道具

**公式**：
```
@TAG: role/body type (age implied by build/wardrobe) + current state + critical visible anchors + action-critical prop/body state. 100% matches the reference.
```

#### LOCATION MAP（地点地图）

若存在地点参考，在写调度前把它转成实用的地图。

**定义**：
- camera position（摄影机位置）、camera facing direction（摄影机朝向）
- foreground（前景）、midground（中景）、background（背景）
- main landmark positions（主地标位置）、character positions（角色位置）
- movement path（移动路径）、lighting direction（光照方向）、depth relationships（纵深关系）

**如果用户说地点图是参考**：用它来获取 geography、materials、atmosphere、landmarks、lighting direction if relevant。除非用户明确要求，否则不要盲目继承摄影机角度、构图或取景。

#### FIRST FRAME AND SPATIAL BLOCKING（第一帧与空间调度）

**第一帧占位锁定**：若镜头必须以可见角色开头，直接写明。

```
The first visible frame already contains all required characters in their correct positions.
No empty establishing frame.
No delayed character reveal.
No opening frame without the required subjects.
The spatial relationship is readable immediately in frame one.
```

只允许在用户明确要求时空开场。若用户要求闪切或极短的定场切，仍须立即包含所需主体或地点信息。

**空间调度锁定**：始终定义每个人在哪。

对每个重要主体，明确：
- screen position（画面位置）、world position（世界位置）
- distance from landmark or other character（距地标或他者的距离）
- body facing direction（身体朝向）、gaze direction（视线方向）
- movement direction（移动方向）、foreground / midground / background（前/中/背景）

**用简单的物理语言**，避免弱词：
- ❌ 弱写法：`near the tree`、`by the taxi`、`around the location`、`somewhere in the battlefield`
- ✅ 强写法：`@HERO1V2 stands within 1 meter of the burned-out car, one hand planted on the scorched hood`

#### FORMAT MODE（格式模式）

动笔前，无声选择：

**SINGLE CONTINUOUS TAKE**（单连续镜头）或 **CONTROLLED MULTI-SHOT SEQUENCE**（受控多镜序列）

**默认 SINGLE CONTINUOUS TAKE**，除非：
- 用户明确要求切、闪切、蒙太奇、插入镜、反打、硬切
- 单摄影机位无法清晰调度动作
- 关键细节需要插入特写
- 需要不同角度同时呈现两种情绪反应
- 场景需要地理 + 反应 + 细节
- 用户要求预告片式、碎片式、记忆、梦境、混乱、冲击或 MV 剪辑

**若选 MULTI-SHOT SEQUENCE**，明确界定每次切：
- Shot A duration、Shot A camera、Shot A subjects visible in first frame、Shot A spatial blocking、Shot A action、cut type
- Shot B duration、Shot B camera、Shot B subjects visible in first frame、Shot B spatial blocking、Shot B action

**铁律**：绝不让模型发明未指定的切。绝不允许随机蒙太奇。每次内部切都必须保留空间连续性、画面方向、视线、光照方向与角色位置。

#### OPTICS（光学与镜头控制）

Seedance 对可观察的镜头结果，比对相机元数据反应更好。

**优先使用**：
- diagonal field of view in degrees（对角线视角，以度计）
- physical camera distance（相机物理距离）
- visible optical outcome（可见光学结果）
- content-FOV alignment（内容-视角对齐）

**使用**：47° / 84° / 107° / 29° / 18° / 8° diagonal field of view

**避免作为主控制**：85mm、35mm、f/1.4、ISO 800、镜头品牌名（Cooke S4、Master Prime、Helios 等）

##### 镜头决策树

写最终提示词前，按内容类型无声选择镜头性格：

**若内容类型是脸部肖像**：
- close intimate face with environment visible → 84° Cuarón intimate-wide
- medium portrait → 29° short telephoto portrait
- tight emotional close-up → 18° classic telephoto
- distant hidden observation → 8° super-telephoto observation with foreground occlusion

**若内容类型是环境动作**：
- natural documentary action → 47° standard normal
- wide environmental action → 84° classic wide
- large-scale environmental geography → 107° wide rectilinear
- extreme environmental immersion → 135° wide environmental pattern（仅当整拍都是环境动作时）

**若内容类型是细节或微距**：
- standard detail → 29° or 18°
- detail inside a wide environment → SNAKE CAM style（仅明确需要时）
- 避免在同一拍里把微距细节与环境动作混用

**若内容类型是远距离观察**：
- sports broadcast、paparazzi、wildlife observation → 8° super-telephoto observation
- compressed surveillance portrait → 18° or 8° telephoto with foreground occlusion and atmospheric haze

##### 视角语言库

**47° Standard normal**：
```
47° diagonal field of view, standard normal lens character, camera roughly 2-4 meters from subject, natural human-eye perspective. Zero obvious distortion, natural face and body proportions, comfortable depth of field, background readable but not exaggerated, classic grounded cinema framing.
```

**84° Classic wide**：
```
84° diagonal field of view, classic wide-angle lens character, camera roughly 0.8-2 meters from subject, slight low angle if needed. Wide-angle lens with strong but natural perspective expansion, foreground body presence feels larger and closer, environment remains visible to the frame edges, deep readable spatial context, straight architectural lines stay rectilinear, no fisheye curve.
```

**29° Short telephoto portrait**：
```
29° diagonal field of view, short telephoto portrait lens character, camera roughly 2-6 meters from subject (closer in tight spaces). Close framing achieved through lens reach, not physical proximity. Subject is razor-sharp, background begins to compress closer behind them, face proportions are flattering and stable, background dissolves into creamy soft bokeh, subject pops clearly from the environment.
```

**18° Classic telephoto**：
```
18° diagonal field of view, classic telephoto lens character, camera roughly 6-15 meters from subject. Strong background compression, distant elements appear stacked closer behind the subject, razor-thin focus isolates the eyes and key facial features, foreground and background melt into soft bokeh, the image feels observed from a distance.
```

**8° Super-telephoto observation**：
```
8° diagonal field of view, super-telephoto observation lens character, camera roughly 10-20 meters from subject (adjust for scene space). Extreme background compression, background flattened into a soft color wash, only the subject is sharp, everything else dissolves into creamy bokeh. The image feels like distant paparazzi, wildlife documentary, or sports-broadcast observation. Foreground occlusion is mandatory: blurred foreground objects occupy the lower 30 to 45 percent of frame as oversized dark bokeh shapes, framing the subject from far away.
```

##### 防漂移锁定

仅在相关时使用。

**长焦**：
```
No part of this shot becomes wide-angle or normal-lens coverage. Wider framing is achieved by the camera being farther away with the same long-lens reach, not by switching lenses. The background remains compressed and dissolved in every frame.
```

**广角**：
```
No part of this shot becomes telephoto portrait coverage. The environment stays visible around the subject, the camera remains physically close, and the image keeps wide-angle spatial expansion with deep readable context.
```

**标准镜头**：
```
No extreme wide distortion, no telephoto compression. The image stays natural, grounded, and human-eye neutral.
```

#### CAMERA（摄影机与构图）

把摄影机指令写成物理操作员行为。

**定义**：
- lens character（镜头性格）、camera height（机位高度）、camera distance（相机距离）
- camera angle（摄影机角度）、camera side（摄影机一侧）、subject size（主体大小）
- screen placement（画面位置）、camera movement（摄影机运动）
- focus behavior（对焦行为）、depth of field（景深）、handheld quality（手持质感）
- framing priority（构图优先）

**优先**：
- camera fixed at X、camera moves from X to Y、lens at hip height、lens at snow level
- operator stands on shadow side、subject occupies screen-left third
- landmark holds left third、negative space on screen-right
- profile preferred、3/4 angle preferred、frontal only when emotionally required

**若允许构图自由，仍须保留**：
- subject placement、gaze line、landmark proximity、lighting direction、active references、action timing、lens character

##### 手持摄影机规则

若要求手持，用物理语言描述：
- operator breath（操作员呼吸）、micro-settling（微沉降）、weight shift（重心转移）
- organic imperfect correction（有机的不完美修正）、shoulder-mounted mass（肩扛质量）
- subtle pulse（细微脉动）、human correction（人为修正）

**避免**：digital jitter（数字抖动）、random shake（随机晃动）、gimbal smoothness（除非要求云台顺滑）、floating drone feel（除非要求无人机漂浮感）

**固定机位标准措辞**：
```
Locked-off tripod, perfectly still — no handheld, no push, no zoom, no reframe, no pan, no tilt. The camera holds the framing like a held breath.
```

#### ACTION TIMING（动作时序）

逐秒分解动作，每拍 ≤3 句。

**规则**：
- 用现在时、短句
- 摄影机写在动作里
- 每拍要轻——一拍过载，模型就糊
- 提示词本身可以长（可达 3000–4000 词）。**长度不是敌人，过载的拍才是**

**四条例外措辞规则**：
. 动作只用**肯定式**——模型忽略 `does NOT fall on his back`，甚至反着做；写 `falls on his stomach`
2. 角色从**第一帧就在画面里**；除非要求，绝不看镜头
3. **角色外貌用视觉特征描述**——用体型、服装、发型、步态代替数字年龄（如 `a teenager` → `a lanky figure in an oversized school blazer, round face, short messy hair`）。视频模型对数字年龄不敏感，但对外貌视觉特征敏感。这也是避免生成内容被平台内容策略误判的有效做法。
4. 维护**模型友好词汇表**（视频模型对某些词响应差或有副作用）：`dark` → `low key lighting`；`jolting` → `rapid handheld motion`。**这些替换只用于让模型更准确地理解创作意图**：`dark` 与 `low key lighting` 描述的是同一件事，只是后者对模型更明确。
⚠️ **合规边界（v9.0.1 强化）**：**不得**用词表替换规避平台的安全、审核或合规机制；若某词汇被平台安全策略拦截，必须按平台提示**修改创作内容或停止**，不得换同义词绕过。

**状态非过渡**：描述角色**已在**动作状态——mid-throw、mid-punch、mid-pace、mid-argument——而非到达的过程。

- ❌ `reaches into the bag, pulls out, winds up`（会塌）
- ✅ `mid-throw, arm extended`（能成）

用状态逐拍串联，而非叙述连续过程。

#### PHYSICS（物理锁定）

> **Content Note**: This section includes realistic physics descriptions for cinematic purposes, including references to blood viscosity, weapon weight, injury continuity, and other physical effects. These are technical guidelines for AI video generation, not instructions for real-world harm.

每个物体与身体都有物理属性。

**强制**：
- gravity（重力）、mass（质量）、inertia（惯性）、friction（摩擦）
- contact（接触）、weight transfer（重量转移）、ground pressure（地面压强）
- collision（碰撞）、follow-through（随动）、cloth delay（布料延迟）、hair delay（头发延迟）
- liquid flow（液体流动）、blood viscosity（血液粘度）、snow accumulation（积雪）
- fire heat shimmer（火焰热浪）、vehicle mass（载具质量）、door hinge resistance（门铰阻力）、weapon weight（武器重量）

**动作必须有因果**：
- 无飘浮身体、无无重武器、无无摩擦的脚、无瞬移
- 无不可能物体运动、无橡胶感 CG 动作、无虚假游戏引擎物理

**行走**：
- heel contact（脚跟触地）、weight transfer（重量转移）
- hip shift（髋部偏移）、toe push-off（脚尖蹬地）、body mass settling（身体质量沉降）

**奔跑**：
- real ground contact（真实地面接触）、knee lift（抬膝）
- opposing arm swing（对侧摆臂）、torso lean（躯干前倾）、varied stride（步伐多变）
- no floaty CG-running look（无飘浮 CG 跑感）

**武器**：
- arm carries visible weight（手臂带可见重量）、wrist angle reacts to mass（手腕角度随质量反应）
- object has inertia（物体有惯性）、motion has acceleration and deceleration（动作有加速减速）
- blade or object does not teleport between poses（刀或物体不在姿态间瞬移）

**液体**：
- blood clings, drips, smears, pools, stains, and follows gravity（血附着、滴落、涂抹、积洼、染色、随重力）
- droplets travel in parabolic arcs（液滴走抛物弧线）
- wet contact leaves visible residue（湿接触留可见残留）
- flow has viscosity and direction（流动有粘度与方向）

#### LIGHTING（光照与曝光）

**单光源逻辑**：一个主光源决定阴影方向。

**规则**：
- 允许环境漫射光（窗光/天光）作为底光，但底光不产生第二个阴影方向
- 绝不让两个强光源各投各的阴影（**"两个太阳"**）——否则每个新角度重造光
- 光照必须作为优先锁定处理，而非装饰

#### AUDIO（音频）

**台词线在提示词里永远同构**：
> 嗓音+情绪 → 引号内台词 → 身体动作 → 面部反应

**规则**：
- 台词只活在 AUDIO 段，动作段里一个字都不许有
- 每人**只说引号里的词**；没词的人**完全静默**
- 动作里写的「半笑」是面部表情，**不出声**
- 写混音：人声干净贴麦、环境在其下、有人说话时环境沉一沉
- 生僻名给音标，否则模型读崩

**Voice 描述公式（1–2 句，引号）**：
```
"A [age]-year-old [origin / accent descriptor]. [Timbre and register];
[pace and delivery manner]; [emotional character — and how it shifts under
pressure]."
```

**技术标签收尾**：`Photorealistic. NON-IP. [画幅]. [时长]s. SFX only. NO CGI. Cinematic.`

#### CHARACTER ACTING（角色表演）

每个可见角色的目标（objective）、主导身体节律（dominant body rhythm）、可见习惯（visible habits）与微表演节拍（micro-beats）。写为流畅散文，不用项目符号或字段标签。

**详见** `references/acting-performance.md`（ACTING 系统）。

#### STYLE（风格）

逐字粘贴 Style Prefix。绝不省略 Skin/Acting/Continuity 三个根条款。

**详见** `references/style-prefix.md`。

#### QUALITY（质量）

技术质量锁定：
```
8K detail, pore-level skin, no jitter, no flicker; faces stay exactly their references at every distance.
```

#### POSITIVE CONSTRAINTS（正向约束）

每个计数与禁令，写成「画面里有什么」。

**示例**：
```
POSITIVE CONSTRAINTS
Exactly three people in the hall, and no one else. Exactly ONE crystal arm, on ROCO's right arm,
wrist to shoulder — never on the left, never spreading past the shoulder. FIVE smashed mannequins,
never re-rendered as intact, never multiplied. Two trays, never more. The camera stays on the door
side of the room for all twelve seconds. Photorealistic. NON-IP. 16:9. 12s. SFX only. NO CGI. Cinematic.
```

---

## 多镜连续性锁定

每次内部切都保留：
- 相同的活跃角色列表、相同的地点地理
- 相同的画面方向（除非摄影机角度明确改变）
- 相同的注视目标、相同的左右关系（除非被摄影机位置刻意反转）
- 相同的光照方向、相同的服装、相同的伤口、相同的道具
- 相同的手状态、相同的血/雪/土/汗/水/火/烟连续性
- 相同的物体状态、相同的情绪推进

**切后不要重置动作。不要瞬移角色。** 除非时间与移动能解释，否则不要改变距地标的距离。除非明确要求，否则切后不要引入新道具或角色。

---

## 切类型

只使用明确的切类型：

**允许**：
- HARD CUT（硬切）、SMASH CUT（碎切）、MATCH CUT（匹配切）
- INSERT CUT（插入切）、REVERSE CUT（反切）、WHIP CUT（快甩切）

**避免**（除非明确要求）：
- fade（淡出）、crossfade（交叉淡化）、dissolve（叠化）、transition effect（转场特效）

```
NO fade-to-black.
NO crossfade.
NO dissolve.
NO transition effects.
HARD CUTS only.
```

---

## 真实范例（完整 16-block）

```
SCENE CONTEXT
EXACT 3 CHARACTERS — NO DUPLICATES: ROCO, JAX, REIN. Underground base, training hall, day.
ROCO has been drilling alone for hours; JAX and REIN come in late with food and find the room
wrecked. One continuous 12-second shot, no cuts, no speed ramps.

ACTIVE REFERENCES
@roco for character reference — bare-chested, the crystal sheathing his right arm from wrist to
shoulder, blood dried under his nose.
@jax for character reference — carrying two food trays.
@rein for character reference — tablet in her left hand, screen alive.
@loc_training_room for location reference — take only the space and the texture: raw concrete,
black rock walls, the round mat, the hard light above it. Do not use as a starting frame, do not
inherit the composition, the angle or the grade.

LOCATION MAP
The round training mat sits at the center of the hall under one hard overhead light. The door is
in the far wall at frame-LEFT, about eight metres from the mat. Five smashed mannequins lie
scattered at CENTER-RIGHT, one still rocking on its base. A bench with two trays stands at
frame-RIGHT, two metres off the mat. The camera lives on the door side of the room and never
crosses that line.

FIRST FRAME AND SPATIAL BLOCKING
First frame is already the full room: ROCO planted at the center of the mat, torso angled to
frame-LEFT, gaze down on the broken mannequins; the open door at frame-LEFT with JAX and REIN just
inside it, trays in hand, two metres apart. No empty establishing beat, no camera move on frame one.

FORMAT MODE
Single continuous take, 12 seconds, real time, no cuts, no speed ramps.

OPTICS
≈47° diagonal field of view, camera low at chest height, six metres from the mat, deep enough focus to hold the door
and the mannequins in one read; the crystal arm stays sharp.

CAMERA
Calm breathing handheld that holds its framing — a slow reframe of a few degrees when ROCO turns
his head, nothing more. No push, no zoom, no whip.

ACTION TIMING
0.0–1.0s  — the room holds: positions fixed, one mannequin still rocking.
1.0–4.0s  — the door swings; JAX and REIN step in and stop at the edge of the mat, trays held.
4.0–8.0s  — ROCO's eyes find them before his head turns; chest pumping in short pulls, the blood
            untouched, the jaw setting once.
8.0–12.0s — he speaks; the smile cracks on all three at once; nobody steps toward anybody.

PHYSICS
The crystal arm has real weight — it drags the right shoulder low and swings a beat behind the
body. The rocking mannequin loses momentum and settles. Trays carry liquid: the cups tilt and
steady when JAX stops. Breath is audible work, not decoration.

LIGHTING
One hard overhead source above the mat: ROCO lit from above, eye sockets in shadow, the crystal
catching a cold edge; the door area falls two stops darker; no fill from the camera side.

AUDIO
Diegetic only — the hum of the hall, one mannequin creaking to a stop, footsteps and trays. ROCO
voice (verbatim): "A worn-out voice in his twenties, dry and low, humour used as armour." His line,
and nothing else: "You're late." Nobody else speaks. No music.

CHARACTER ACTING
ROCO — burnt out and still going; wants one more clean hit before anyone sees him fail; hides that
the arm is winning; heavy planted rhythm, slow recovery; re-arms his face when the door opens.
JAX  — carries the reaction: the grin holds a half-beat too long, then drops as he reads the room.
REIN — reads the damage before the person: eyes sweep the broken mannequins, then the arm, then his
face; the tablet lowers without her noticing.

STYLE
[Style Prefix, pasted word for word]

QUALITY
8K detail, pore-level skin, no jitter, no flicker; the three faces stay exactly their references at
every distance.

POSITIVE CONSTRAINTS
Exactly three people in the hall, and no one else. Exactly ONE crystal arm, on ROCO's right arm,
wrist to shoulder — never on the left, never spreading past the shoulder. FIVE smashed mannequins,
never re-rendered as intact, never multiplied. Two trays, never more. The camera stays on the door
side of the room for all twelve seconds. Photorealistic. NON-IP. 16:9. 12s. SFX only. NO CGI. Cinematic.
```

---

## 反模式清单

**不要写**：
- extreme wide-angle lens、ultra wide-angle lens、super wide-angle lens
- wide shot as a lens instruction、establishing shot as a lens instruction
- zoom out plus wide-angle、tight wide framing
- f-stop、ISO 或镜头品牌元数据作为主控制
- 同一镜内复合摄影机运动、同一拍内混用内容类别
- 仅负面的镜头控制

---

## 视觉结果栈

### 长焦视觉结果栈

任何长焦镜头，至少包含以下可观察短语中的 4 条：
- background completely blurred into a soft warm color wash
- razor focus on the subject
- only the subject is sharp, everything else is soft
- creamy bokeh wash behind the subject
- background compressed flat behind the subject
- the subject pops sharply against a dissolved background
- close framing achieved through lens reach, not physical proximity
- camera positioned far from the subject in physical space
- atmospheric haze suspended between camera and subject
- foreground occlusion frames the subject as soft dark bokeh

### 广角视觉结果栈

任何广角镜头，至少包含以下可观察短语中的 3 条：
- foreground body presence looms larger than natural
- environment remains visible around the subject
- deep edge-to-edge focus
- straight lines stay rectilinear
- wide spatial context visible to frame edges
- camera physically close to subject
- immersive close perspective
- no telephoto compression
- no creamy portrait bokeh unless explicitly wanted

---

## 多镜镜头一致性

若序列有内部切，为每个镜定义镜头性格。

**同镜头多镜**：
```
LENS IS X° ACROSS ALL SHOTS. NOT NEGOTIABLE.
Each shot opens with: LENS LOCK SHOT A = X°.
Each shot closes with: LENS CHECK SHOT A: X° maintained, no drift.
```

**混镜头多镜**：每个镜只在内容类型改变时获得自己的镜头性格。不同镜头性格之间只用硬切。无平滑 FOV 过渡。无随机镜头漂移。

每次内部切保留：
- 活跃角色、地点地理、画面方向、视线、身体朝向
- 光照方向、道具状态、伤口状态、血/雪/土连续性、世界物理

---

## 关键原则总结

1. **模型没有记忆** → 每镜逐字重述一切
2. **具体物理指令优先** → 避免抽象诗化语言
3. **状态非过渡** → 描述 mid-action，不描述到达过程
4. **空间规则先于风格** → 先锁定位置，再谈美学
5. **单光源逻辑** → 避免"两个太阳"
6. **台词只在 AUDIO 段** → 动作段不出声
7. **每拍 ≤3 句** → 长度不是敌人，过载才是
8. **正向约束** → 写成"画面里有什么"，而非"不要什么"
9. **技术标签收尾** → `Photorealistic. NON-IP. [画幅]. [时长]s. SFX only. NO CGI. Cinematic.`
10. **最终输出只有提示词** → 不输出 QA、推理、清单、解释

---

**参考**：完整 ACTING 系统详见 `references/acting-performance.md`；Style Prefix 详见 `references/style-prefix.md`。
