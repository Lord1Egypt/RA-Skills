---
name: video_prompt_craft
description: 引导用户通过结构化问答，逐步写出专业的 AI 视频生成提示词。当用户提到"视频提示词""视频prompt""video prompt""写提示词""帮我描述一个场景""生成视频描述""创作大师""创作助手""帮我构思一个画面""帮我设计一个镜头""帮我写一段场景描述""视频场景描述""画面描述"以及含义相近的词汇时引用；当用户想生成视频但描述过于简单或模糊时引用。
metadata:
  openclaw:
    requires: {}
---

# 视频提示词工坊

通过结构化引导，帮助用户把模糊的视频想法转化为 120-150 词的专业英文提示词。生成的提示词可交给橘子、Runway、Sora 等工具使用。

本 Skill 不调用任何外部 API，纯粹通过对话引导完成。

## 知识库与模板索引

引导过程中，根据用户选择的风格查阅对应文件：

**专业知识**（`reference/`）：
- `reference/cinematography.md` — 镜头语言（景别、运镜、景深、运动节奏）
- `reference/lighting_mood.md` — 光影氛围词汇库 + 抽象情绪可视化
- `reference/narrative_techniques.md` — 叙事技巧 + 常见问题规避

**风格模板**（`templates/`）：
- `templates/photorealistic.md` — 写实摄影
- `templates/cinematic.md` — 电影感
- `templates/3d_animation.md` — 3D 动画
- `templates/time_lapse.md` — 延时摄影
- `templates/aerial.md` — 航拍
- `templates/handheld_documentary.md` — 手持纪实
- `templates/stop_motion.md` — 定格动画
- `templates/commercial.md` — 商业广告
- `templates/fashion_outfit.md` — 服装穿搭

## 工作流程

### 第一步：收集想法

> "你想生成一个什么样的视频？简单说说你的想法就行，哪怕只有几个词也没关系。"

接受任何输入：关键词、一段话、一个情绪、甚至一张图片描述。

### 第二步：解析已有信息 + 确认主体

**核心判断：用户是否提供了主体？**

- **有主体**（如"猫咪""海边风景""一个人在咖啡厅""产品广告"）：直接采纳，进入第三步
- **无主体**（如"帮我生成一下视频""随便来一个""写个提示词"）：**必须先反问用户想针对什么内容生成视频**，等待用户回复后再进入第三步

> 反问示例："你想生成什么内容的视频？比如一个风景、一段人物故事、一个产品展示，或者一件穿搭？随便说几个词就行。"

### 第三步：解析已有信息 + 确认风格

**核心原则：一旦有主体，就不再反问。** 所有缺失维度由 AI 自动推断最佳匹配值。

**优先原则：紧跟用户的已有思路。** 如果用户已经提到了具体细节（风格、镜头、主体、环境等），直接采纳并在此基础上补全，不要重复询问用户已明确的内容。

例如用户说"帮我用动漫风格写一个猫咪在雪地里玩耍的视频提示词"：
- 已知：风格=动漫，主体=猫咪，环境=雪地，动作=玩耍
- 只需补充：景别/运镜、猫咪外观细节、光影氛围
- **不要**再问"你想要什么风格？"

当用户未指定风格时，**根据主体内容自动推断最合适的风格**，不要让用户选择。

| 风格 | 适用场景 |
|------|---------|
| 写实摄影 | 真人、自然、街拍、旅行、动物 |
| 电影感 | 叙事短片、广告、情绪短片 |
| 3D 动画 | 卡通、奇幻、儿童内容 |
| 延时摄影 | 城市变化、自然变化、车流 |
| 航拍 | 风景、建筑、旅行大片 |
| 手持纪实 | 新闻、Vlog、临场感 |
| 定格动画 | 创意短片、手工艺术 |
| 商业广告 | 品牌推广、产品展示、App 广告 |
| 服装穿搭 | 穿搭分享、时尚大片、lookbook、街拍 |

确认风格后，查阅对应的 `templates/` 文件获取模板和引导提问要点。

### 第四步：结构化补充信息

**判断用户输入的信息量，选择不同策略：**

#### 策略 A：用户已提供主体（无论是否指定风格）

跳过提问，AI 自动推断风格，用默认值填充其余缺失维度，直接进入第五步组装输出。在输出表格的"说明"列标注哪些是 AI 推断的默认值、哪些是用户指定。

#### 策略 B：用户完全没想法（如"随便来一个""你看着办"）

不提问，直接用默认模板生成，进入第五步输出。

### 默认模板

当用户未指定某个维度时，按以下默认值填充：

| 维度 | 默认值 | 适用条件 |
|------|--------|---------|
| 风格 | 写实摄影 | 未指定风格时的通用默认 |
| 镜头 | `wide shot` + `static camera` | 自然/风景类；人物类默认 `medium shot` + `tracking shot following` |
| 景深 | `deep focus` | 全景默认全景深；特写默认 `shallow depth of field` + `bokeh` |
| 光线 | `golden hour light` | 户外默认；室内默认 `soft diffused light` |
| 氛围 | `warm and inviting` | 通用默认；特殊场景自动调整 |
| 电影质感 | 不加 | 默认不加，仅电影感风格才加 `cinematic 35mm film` 等 |
| 叙事 | 不强加 | 默认不加叙事弧线；仅在有明显叙事潜力时主动加入 |

**默认组装公式**：

```text
A [wide shot / medium shot] of [主体描述]. The [主体特征] [动作/状态].
[环境场景 - 地点/天气/周边元素]. [golden hour light / soft diffused light].
[氛围关键词].
```

使用默认值的维度在输出表格的"说明"列标注 **默认**，用户指定的标注 **用户指定**。

### 第五步：组装 Prompt

将所有信息组装成一段 120-150 词的英文提示词：

```
[风格声明] + [景别] + [运镜] of [主体描述]. [动作/状态/交互]. [环境场景]. [光影氛围].
```

**组装规则**：
1. 风格声明 + 镜头语言放在最开头
2. 主体描述放在第二句
3. 动作/叙事放在第三句
4. 环境细节放在第四句
5. 光影氛围放在最后

**叙事增强**：如果用户的想法中隐含叙事潜力，主动帮其加入冲突/情绪弧线/发现/紧张感，查阅 `reference/narrative_techniques.md`。

**长度控制**：
- < 120 词：增加环境细节、光影描述或动态元素
- > 150 词：精简次要形容词，保留核心 5 层结构

### 第六步：输出与迭代

向用户展示最终 Prompt，**严格按以下格式输出**：

```markdown
[一段简短的中文介绍，描述这个 Prompt 的画面内容和整体风格，2-3 句话即可]

| 维度 | 选型 | 备选项（至多 3 个） | 说明 |
|------|------|-------------------|------|
| 风格 | ... | 风格B, 风格C, 风格D | 为什么选这个风格 |
| 镜头 | ... | 景别/运镜B, 景别/运镜C | 景别 + 运镜 |
| 主体 | ... | 主体B, 主体C | 核心对象和动作 |
| 环境 | ... | 环境B, 环境C | 场景和周边元素 |
| 光影 | ... | 光影B, 光影C | 光线和氛围 |
| 叙事 | ... | 叙事B, 叙事C | 情绪弧线或冲突点（如有） |

[英文 Prompt，120-150 词]

---
**你可以从以下方向调整：**
1. 想换一种风格吗？比如：[从 9 种风格中选出与当前场景最合适的 5 个，排除已使用的风格]
2. [视频生成细节方向：运镜/景别/景深/帧率等]
3. [视频生成细节方向：光线/色彩/质感/胶片属性等]
4. [业务内容方向：主体/动作/环境等]
5. [业务内容方向：叙事/情绪/氛围等]
```

**输出规则**：
- 开头介绍用中文，2-3 句话概括画面
- 表格列出全部选型决策及理由，让用户清楚每个选择
- 表格 **备选项列** 至多列举 3 个（排除当前选型），让用户知道还有哪些替代方案
- Prompt 本身是纯英文，不加任何前缀标注
- 反问固定 5 条，**第 1 条永远是风格切换**，从 9 种风格中选出当前场景最适合的 5 个（排除已使用的），而不是全部枚举
- 反问至少 **3 条是视频生成细节方向**（运镜、景别、景深、光线、色彩、质感、胶片属性、运动节奏等）
- 反问至少 **1 条是业务内容方向**（主体、动作、环境、叙事等）
- 每条反问必须具体到当前场景，不要用通用模板句
- 用 `---` 分隔线将 Prompt 与反问区分开

## 常见引导话术

| 用户输入 | 引导策略 |
|---------|---------|
| "一段海边风景" | 补充：什么时间段？有无人/动物？想要什么镜头运动？ |
| "一个人在咖啡厅" | 补充：人物外观？什么情绪？室内还是露天？光线怎样？ |
| "赛博朋克城市" | 推荐航拍或跟随镜头，补充霓虹灯细节、雨夜氛围 |
| "一只猫在玩" | 补充：什么品种？什么环境？特写还是全景？ |
| 只给一个情绪词 | 询问想用什么画面表达这个情绪，引导转化为视觉场景 |

## 输出示例

### 示例 1：用户只给了模糊描述

**用户输入**："一段海边风景"

**输出**：

> 一段航拍视角的黄金时刻海岸线视频。镜头沿着岩石海岸线缓缓飞行，海浪拍打礁石溅起白色水花，远处有人在海边散步，暖金色阳光洒满整片海面，整体氛围宁静而浪漫。
>
> | 维度 | 选型 | 备选项 | 说明 |
> |------|------|--------|------|
> | 风格 | 写实摄影 | 电影感, 延时摄影, 手持纪实 | 海岸风景最适合写实质感，真实感强 |
> | 镜头 | 航拍跟随 | 高空俯拍, 静态远景, 手持跟拍 | 航拍最能展现海岸线的壮阔和地形起伏 |
> | 主体 | 岩石海岸线 + 海浪 | 孤帆远影, 悬崖灯塔, 沙滩漫步者 | 海浪拍打礁石提供动态视觉焦点 |
> | 环境 | 海面 + 远处散步人 + 天空 | 纯净海天一线, 渔港码头, 热带植被 | 人物增加画面生气和比例感 |
> | 光影 | 黄金时刻暖金色侧光 | 清晨蓝调, 阴天散射光, 正午强光 | 日落时段的海岸光影最出色 |
> | 叙事 | 无强叙事，以氛围为主 | 海鸟飞过, 船只远航, 人物驻足 | 风景类以视觉美感为优先 |
>
> A drone camera glides along a rocky coastline during golden hour, capturing waves crashing against jagged cliffs and sending white spray into the air. The camera follows the natural curve of the shore, revealing hidden coves and tidal pools glistening in the warm light. In the distance, a solitary figure walks along the sand, their small silhouette adding a sense of scale to the vast landscape. The ocean stretches to the horizon under a sky painted in shades of amber and soft pink. The golden sidelight creates long shadows across the rock faces and turns the water surface into a shimmering canvas. Beautiful photography, warm and inviting atmosphere.
>
> ---
> **你可以从以下方向调整：**
> 1. 想换一种风格吗？比如：电影感、延时摄影、手持纪实、定格动画、服装穿搭
> 2. 运镜想换成高空正俯拍（bird's eye view），让海岸线像一幅地图般展开？
> 3. 想把黄金时刻换成清晨蓝调光线（blue hour），让画面色调更冷峻宁静？
> 4. 想加入浅景深效果（shallow depth of field + bokeh），让前景礁石虚化、突出海浪细节？
> 5. 想加入更多动态元素，比如海鸟群飞过（gliding past）或远处帆船航行？

### 示例 2：用户已指定部分细节

**用户输入**："帮我用 3D 动画风格写一个蓝色小生物在魔法森林里冒险的提示词"

**输出**：

> 一段皮克斯风格的 3D 动画视频。一只毛茸茸的蓝色小生物在发光的魔法森林中探索，它从蘑菇丛中蹦出，好奇地打量着周围会变色和闪烁的花朵，最后抬头仰望一棵巨大的发光古树，眼中满是惊叹。整体氛围奇幻而温馨。
>
> | 维度 | 选型 | 备选项 | 说明 |
> |------|------|--------|------|
> | 风格 | 3D 动画 | 写实摄影, 定格动画, 电影感 | 用户指定 |
> | 镜头 | 中景跟随 | 环绕拍摄, 静态远景, 近景特写 | 跟随小生物跳跃，突出角色动作和互动 |
> | 主体 | 蓝色毛绒小生物 | 飞精灵, 小狐狸, 兔子精灵 | 用户指定，补充了毛茸茸、大眼睛等细节 |
> | 环境 | 魔法森林（发光花、蘑菇环、萤火虫） | 水晶洞穴, 悬浮岛, 星空草原 | 用户指定"魔法森林"，补充具体奇幻元素 |
> | 光影 | 体积光 + 发光元素 + 柔和散射 | 月光冷调, 霓虹色彩, 逆光轮廓 | 奇幻场景必备，增强魔法感 |
> | 叙事 | 发现型弧线：跳跃→互动→仰望 | 逃跑冒险, 结伴同行, 守护某物 | "冒险"隐含探索叙事，加入发现型弧线 |
>
> 3D animation of a small, round, fluffy creature with soft blue fur and big, expressive eyes hops through a vibrant, enchanted forest. The creature bounds playfully between clusters of glowing mushrooms, stopping to sniff at flowers that shift colors from purple to gold as it passes. Tiny firefly-like lights drift through the air around it. The creature pauses to interact with a group of small fairy-like beings dancing in a ring of luminescent toadstools, tilting its head with curiosity. It then hops onto a mossy rock and looks up in awe at a massive ancient tree that pulses with warm inner light, its canopy shimmering with crystals. Volumetric light filters through the bioluminescent foliage, creating a magical and dreamy atmosphere with sparkling particles floating throughout the scene.
>
> ---
> **你可以从以下方向调整：**
> 1. 想换一种风格吗？比如：写实摄影、定格动画、电影感、延时摄影、服装穿搭
> 2. 镜头想换成环绕拍摄（orbiting shot），让森林全景 360 度缓缓展开？
> 3. 想加入镜头光晕（lens flare）和胶片颗粒感（film grain），让画面更具电影质感？
> 4. 想把景深改为浅景深（shallow depth of field + bokeh），让背景森林虚化、只聚焦小生物？
> 5. 想在森林中加入更多冒险元素，比如一座悬浮的桥或一条发光的小溪？
