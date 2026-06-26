# Gemini 4 格漫画出图规范

当用户要为小红书内容生成 `4格漫画`、`插画分镜`、`Gemini 配图提示词` 时，读取本文件。

目标不是写一句“万能提示词”，而是稳定产出同一账号能长期复用的漫画视觉系统。

如果用户还没有角色卡和画风卡，先回到 `persona-visual-bootstrap.md` 做初始化，再使用本文件。

如果用户当前的重点是“别被一眼看成 AIGC”，先不要默认走纯 AI 漫画，优先判断是否应改成：

- 真人实拍 + 手工标注
- 真人截图 + 插画点缀
- 真人照片转插画的混合方案

## 核心判断

Gemini 出图不稳定，通常不是因为“模型不行”，而是因为每次都在重新定义这 4 件事：

- 主角是谁
- 画风是什么
- 页面结构是什么
- 这一篇到底讲哪一个冲突

所以不要直接从“单条剧情提示词”开始。先固定 `角色卡 + 画风卡 + 页面模板`，再写每一篇的剧情分镜。

## 官方能力要点

基于 Google 官方文档，以下做法更稳：

- 提示词应尽量具体、清晰、避免模糊目标
- 图像生成和编辑任务适合多轮迭代，而不是每次完全从零生成
- 图像提示词可拆成 `主体 + 场景/背景 + 风格 + 构图/镜头`

对这个技能的实际含义是：

- 优先做“固定参考图 + 轻编辑”而不是每次重新抽卡
- 优先做“固定 2x2 四格布局”而不是每次临时描述版式
- 优先做“低变量提示词”而不是堆砌一大串随机风格词

## 推荐工作流

### 第一步：先做角色母版

不要一上来就做 4 格漫画。先生成一张 `角色母版图`，作为后续每次出图的身份锚点。

角色母版至少固定这些内容：

- 年龄感：`90后男性`
- 发型：短发、黑发、不过度夸张
- 脸型：普通亚洲男性、偏写实或半写实
- 体型：轻微肉感或正在减脂中的普通身材
- 穿搭：固定一套日常装，例如 `灰色连帽卫衣 + 黑色运动裤 + 白色运动鞋`
- 标志物：电脑、体重秤、哑铃、水杯这类重复出现的物件

角色母版的作用是让后续每一篇都在“同一个人”的基础上变化，而不是重新生成陌生人。

### 第二步：再做画风母版

画风要少而稳，不要每次改。

推荐固定这几项：

- 风格：温和、干净、治愈、轻喜剧、半扁平漫画风
- 线条：干净、细线、不要太厚重
- 配色：低饱和暖灰、米白、浅蓝、浅绿
- 光感：柔和室内光
- 版式：固定 `2x2` 四格，留白干净，格子间距统一

不要每次追加新的画风词，比如这次“日漫”、下次“美漫”、再下次“像素风”。这会直接破坏连续性。

### 第三步：每篇只换剧情，不换系统

每次真正变化的，只应该是：

- 这一篇的主题冲突
- 每一格发生的动作
- 少量场景元素

人物、衣服、画风、比例、布局、色彩，尽量都不要变。

## 小红书最稳的 4 格公式

默认优先使用这个结构：

1. `问题`
   例如：今天又拖到凌晨 2 点，还没运动
2. `尝试`
   例如：打开 AI，让它给我一个 15 分钟在家计划
3. `执行`
   例如：真的只做了 3 个动作，但开始了
4. `结果 / 反思`
   例如：没逆袭，但起码把今天拉回来了

这套结构特别适合：

- AI 健身计划
- 自救叙事
- 执行复盘
- 工作流展示的轻剧情化表达

## 常见翻车点

如果生成结果看起来“很傻”，通常不是故事不对，而是画面语言太像低配宣传海报。最常见的原因有：

- 每一格都把意思写死在图里，像教程截图，不像漫画
- 同一格里塞太多动作，尤其把多个训练动作硬挤进一个画面
- AI 屏幕画得太具体，像“AI 神谕机”，很假
- 主角表情太用力，像励志广告，不像普通人
- 字幕太满、太直白，缺少留白和情绪

## 反傻气规则

想让 4 格漫画更像小红书会收藏的内容，默认加这些约束：

- 图里尽量不直接写完整中文句子，文案后期自己加
- 每一格只保留一个核心动作
- 不把“AI”画成发光神秘大脑，只让它作为屏幕上的普通工具存在
- 主角不要太热血，宁可有点累、有点迟疑
- 第 3 格不要同时出现 3 个训练动作，最多只画一个动作瞬间
- 第 4 格优先画“松一口气”而不是“成功逆袭”

## 降低 AIGC 感的规则

如果用户担心“内容被认定成 AI 生成了”，本文件不应用来追求规避识别，而应优先降低批量 AIGC 质感。

优先做这些事：

- 不要整篇整图都交给 AI
- 让真人照片、真实截图、打卡记录、表格截图进入内容主体
- 漫画只做补充，不做全篇唯一视觉材料
- 同一周内不要连续多篇都用同一套纯 AI 漫画
- 图上的中文尽量后期手工添加
- 每篇图都加入一点具体生活证据，而不是完全抽象场景

## 更像真人的分镜原则

如果要讲“AI 给我做了 15 分钟在家训练”，更自然的分镜通常是：

1. 人卡住了
2. 人提出一个很小的请求
3. 人真的开始动了
4. 人没有逆袭，只是没彻底断掉

注意这里的重点不是“训练动作多专业”，而是“这个人终于从静止变成了行动”。

## 什么时候不要让 Gemini 直接写字

如果你想要稳定和统一，小红书图上的大段中文文案尽量后期自己加。

更稳的做法：

- 让 Gemini 只生成图
- 对话框或字幕条可以留空，或者只放极短英文占位
- 最终在 Canva、Figma 或其他工具里统一加中文

这样做的原因不是官方限制，而是实际生产里更容易保持：

- 字体统一
- 文案不出错
- 版面更像一个账号体系

这是我基于官方“提示词清晰、结构稳定、多轮编辑更合适”的信息做出的实务推断。

## Gemini 4 格漫画提示词结构

每次都按同一骨架写，不要自由发挥。

### 固定骨架

1. 任务定义
2. 角色一致性
3. 画风一致性
4. 页面布局
5. 四格剧情
6. 输出限制

### 主提示词模板

```text
Create a clean 2x2 four-panel comic page for a Xiaohongshu-style social post.

Main character consistency:
- Chinese male in his 30s
- short black hair
- ordinary face, slightly tired but gentle expression
- medium build, currently on a fitness journey
- wearing a gray hoodie, black joggers, white sneakers
- recurring props: laptop, dumbbell, water bottle, body scale

Art style consistency:
- soft semi-flat comic illustration
- clean thin linework
- warm neutral indoor lighting
- low saturation palette with beige, gray, muted blue, muted green
- emotionally relatable, lightly humorous, not exaggerated

Page layout:
- exactly four equal panels
- 2x2 grid
- clean white gutters
- consistent character appearance across all panels
- no extra panels, no collage chaos, no watermark

Panel 1:
- [问题场景]

Panel 2:
- [AI 或方法介入]

Panel 3:
- [实际执行动作]

Panel 4:
- [结果、感受或反思]

Output constraints:
- keep the same character in all four panels
- keep the same outfit unless explicitly changed
- prioritize clear storytelling over visual complexity
- leave room for later text overlay
- do not add dense Chinese text inside the image
```

## 角色母版提示词

先单独生成一张角色母版，再开始系列内容。

```text
Create a character reference illustration for a recurring Xiaohongshu comic protagonist.

He is a Chinese male in his 30s, in a career transition period, rebuilding his routine with AI and fitness.
Short black hair, ordinary friendly face, slightly tired eyes, medium build, realistic proportions.
He wears a gray hoodie, black joggers, white sneakers.
Props around him: laptop, water bottle, dumbbell, body scale.

Style:
- soft semi-flat comic illustration
- clean thin linework
- low saturation cozy palette
- simple neutral indoor background

Make this image look like a clean reference sheet for future comic use.
Keep the character centered, full body visible, no dense text, no extra characters.
```

## 单篇 4 格漫画模板

把下面这些变量替换掉即可：

- `[主题]`
- `[问题场景]`
- `[方法介入]`
- `[执行动作]`
- `[结果反思]`

```text
Create a Xiaohongshu-style 2x2 four-panel comic about [主题].

Use the same recurring protagonist:
- Chinese male in his 30s
- short black hair
- medium build
- gray hoodie, black joggers, white sneakers
- same face and body proportions in all panels

Visual style:
- soft semi-flat comic
- clean thin lines
- muted warm palette
- minimal cozy indoor scenes
- emotionally relatable and grounded

Layout:
- exactly four equal panels in a 2x2 grid
- clean white gutters
- strong visual continuity

Panel 1: [问题场景]
Panel 2: [方法介入]
Panel 3: [执行动作]
Panel 4: [结果反思]

Constraints:
- no extra characters unless specified
- no dense Chinese text
- no dramatic manga effects
- keep it simple, clear, and story-driven
- leave negative space for later captions
```

## 工作流展示类 4 格漫画模板

适合讲 OpenClaw、自动化追踪、复盘闭环。

```text
Create a Xiaohongshu-style 2x2 four-panel comic showing a personal AI fitness workflow.

Recurring protagonist:
- Chinese male in his 30s
- short black hair
- gray hoodie, black joggers, white sneakers
- same appearance across all panels

Style:
- soft modern comic illustration
- clean thin linework
- muted beige, gray, blue, green palette
- neat desk, laptop, scale, dumbbell as recurring objects

Layout:
- exactly four equal panels
- clear 2x2 comic page
- simple readable storytelling

Panel 1: the protagonist feels overwhelmed by messy routine and inconsistent workouts
Panel 2: he logs weight, workout completion, and mood into a simple tracking system
Panel 3: an AI workflow summarizes the day and generates tomorrow's plan on the laptop screen
Panel 4: he follows a smaller, clearer plan and feels less chaotic

Constraints:
- do not add complex UI text
- suggest the workflow visually instead of filling the screen with tiny words
- keep the emotional tone grounded and calm
- no exaggerated transformation
```

## 失败后的纠偏提示词

### 1. 人物漂了

补这段：

```text
Use the same recurring protagonist in all panels.
Do not change his hairstyle, face shape, outfit, age impression, or body type.
He must clearly look like the same person from panel 1 to panel 4.
```

### 2. 版式乱了

补这段：

```text
The output must be a clean 2x2 four-panel comic page.
Exactly four equal panels, no extra mini-panels, no collage layout, no chaotic composition.
```

### 3. 画风飘了

补这段：

```text
Keep the illustration style soft, semi-flat, clean, muted, and cozy.
Do not switch to anime action style, realistic photography, 3D rendering, or exaggerated cartoon style.
```

### 4. 画面信息太多

补这段：

```text
Simplify the scene.
Focus on one clear action per panel.
Use minimal background details and preserve empty space for later text overlay.
```

## 更稳的生产建议

如果你要长期做一个账号，推荐这样跑：

1. 先做 `角色母版`
2. 再做 `画风母版`
3. 每篇先写 4 格脚本
4. 用固定模板生成
5. 如果第一版不稳，不重写整段提示词，只补“纠偏段”
6. 把最终稳定的一版沉淀成账号专用母提示词

## OpenClaw 在配图任务中的默认输出

如果用户要配图，默认输出：

- 这一组图要讲的核心冲突
- 视觉目标
- 人物一致性设定卡
- 画风一致性设定卡
- 四格脚本
- Gemini 主提示词
- 纠偏提示词
- 图上文案建议
- 封面建议

## 适合触发本文件的请求

- `帮我把这篇内容配成 4 格漫画`
- `给我一个 Gemini 稳定出图提示词`
- `我想做长期连载漫画，帮我固定主角和画风`
- `帮我把 OpenClaw 工作流画成漫画`
