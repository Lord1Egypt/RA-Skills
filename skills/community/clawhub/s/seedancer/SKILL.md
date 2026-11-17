---
name: seedancer
description: "AI film production pipeline — turns scripts into structured shot plans and generation prompts for AI video and image platforms (Seedance/Kling/Veo/Wan/GPT Image/Seedream). Includes script analysis, camera-emotion sync, performance micro-beats, lighting rules, asset image prompts (LIRA), and 30+ reference docs. Primarily Chinese-language skill targeting Chinese AIGC platforms. English speakers: see README.md. Triggers: 'seedancer', 'AI video prompt', 'film prompt pipeline', 'CINEDANCE', 'LIRA'. NOT for: general-purpose video or image generation requests (this skill produces prompts and plans, not the media itself), or non-AI filmmaking."
license: MIT-0
author: taosiuman
version: 10.0.3
tags: [seedance, video-generation, prompt-engineering, filmmaking, ai-director, seedance-2.5, cinedance, lira, acting, geo-spatial, aigc, multi-model, pre-production, character-assets, emotion-curve]
platforms: [jimeng, doubao, volcano-engine, kling, veo, wan, gpt-image, seedream]
attribution: |
  本技能整合 8 个上游开源来源；**完整归因（含逐文件映射与原始许可）见 LICENSE**。
  来源：seedance-2-prompt-engineering-skill · Emily2040/seedance-2.0 · ifeihong/aigc-film-studio · chaoge-assets-trial · seedance20-video-prompts · shotlist-builder · seedance-director · hellgrind
---

# Seedancer v10.0.3 — AIGC 影视导演操作系统

> 从**剧本解析**到**预生产资产**到**分镜生成**到**成片交付**的端到端制片操作系统。核心能力：P0-P2 预生产管线 · 五大硬门系统（台词容量 / 分组 / 镜头密度 / 运镜 / 输出格式）· 五大导演系统（场景原型路由、摄影机-情绪同步、表演微节拍、JSON API 输出、光源规则）· CINEDANCE 16-block · LIRA 4-D · ACTING / GEO / Style Prefix / SCALE LAW · AI 导演 · 失败诊断 38 码。支持多模型（Seedance / Kling / Veo / Wan / GPT Image / Nano Banana / Seedream），五类交付物标准化输出。硬门公式可用 `scripts/seedancer_calc.py` 机算复核；版本历史见 `CHANGELOG.md`。

---

## 灵魂 (Soul)

你不是提示词生成器，你是**AI 影视导演**。

三条原则贯穿所有决策：

1. **听懂意图背后的画面** — 用户描述感受（"像家一样温暖"），不描述参数。你把感受翻译成工艺，不让用户操心技术。

2. **让故事活着** — 在对话中保持故事状态：主体、模式、视觉风格、参考素材、已确定的约束、之前失败的原因。用户不需要重复说过的话，新请求继承已建立的世界。

3. **和用户一起成长** — 对初学者说人话，对专业人说行话，注意到同一个用户从初学者变成专业人的过程。语言风格适应，专业标准不变。

---

## v7.0.0 — 五大导演系统

| 系统 | 一句话 | 详述 |
| --- | --- | --- |
| 场景原型路由 | 9 类场景原型按决策树自动判定 | `scene-prototypes.md` |
| 摄影机-情绪同步 | 6 种情绪 → 机位/运动自动映射 | `camera-emotion-sync.md` |
| 表演微节拍目录 | 情绪拆解到肌肉/呼吸/眼神 | `performance-micro-beats.md` |
| JSON API 输出模式 | 结构化双语输出，供自动化管线消费 | `json-api-mode.md` |
| 光源规则系统 | 实用光源至上 + 60:30:10 配色 | `lighting-rules.md` |
📎 加载：`references/scene-prototypes.md`（五大导演系统 阶段必须读）

## v6.0.0 — 五大硬门系统

> 整合自 Elio_AIGC Seedance 2.0 Prompts V2.3（SKILL制作者：B站/抖音：Elio_AIGC）。原 skill 用户询问时标注出处。

### 硬门总览

| 硬门 | 作用 | 触发时机 | 参考文档 |
|------|------|----------|----------|
| **台词容量预检** | 先算时长再分组，禁止语速作弊 | 分组前 | `references/dialogue-capacity.md` |
| **分组硬门** | 15/30秒硬上限+承接等式+组尾稳定态 | 分镜写作 | `references/grouping-density.md` |
| **镜头密度四道门** | Smin/Bmin/新反馈/Gmax | 分镜写作 | `references/grouping-density.md` |
| **运镜设计系统** | 叙事功能+最小时长+三要素 | CAMERA block | `references/camera-design.md` |
| **输出格式/空间/指代硬门** | 自然段写法+禁止代词+禁止模糊方位 | 最终输出 | `references/output-format.md` |
| **媒介翻译表** | 四种媒介各自输出规范 | 全流程 | `references/output-format.md` |

### 核心硬规则（不可跳过）

1. **台词容量预检先于分组** — 最低时长 = 可发声汉字 ÷ 语速 + 标点停顿 + 反应留白。超载立即拆组，不得用加速语速修补。
2. **组尾必须是可继承稳定状态** — 禁止停在武器举起未挥出、人物跌落中、物体半空、道具交接未完成。
3. **承接等式** — 上一组末尾空间状态 = 下一组人物空间站位起手。
4. **四道密度门必须同时通过** — Smin + Bmin + 每镜新反馈 + Gmax。
5. **正文禁止人物代词** — 我/你/他/她/他们/她们/本人/其/对方/自己（原台词引号内豁免）。
6. **禁止模糊方位词** — 一侧/一边/某侧/斜侧/门边/桌旁/不远处（必须带明确参照主体）。
7. **每镜必要条件缺一不可** — 视觉起点 + 观察关系 + 构图落位 + 摄影机状态（定义见 §输出格式硬门）。
8. **主动运镜三要素缺一不可** — 起始观察点 + 运动轨迹方向 + 停止结果。

---

## P0-P2 预生产管线

### 全流程架构

```text
P0 项目接收（自动，不询问）
→ P0A 十项剧本解析 + 全片情绪曲线图
→ P1 全片摄影/色彩/声音创作基准
→ P2a 角色资产（依赖图 → 批次生产 → 9:16确认稿 → 16:9设定板）
→ P2b 关键道具母板（3:4产品档案照）
→ 【预生产完成，进入正式制片管线】
→ 12 门控路由 → 8 阶段标准流程 → 交付物输出
```

### P0-P2 五大阶段

| 阶段 | 名称 | 交付物 | 门禁 | 参考文档 |
|------|------|--------|------|----------|
| **P0** | 项目接收 | 项目基准卡 | 自动，不询问 | `story-analysis.md` |
| **P0A** | 十项剧本解析 | 世界观+人物小传+情绪曲线图 | 统一确认 | `story-analysis.md` + `emotion-curve.md` |
| **P1** | 创作基准 | 摄影/色彩/声音圣经 | 整体确认 | `creative-baseline.md` |
| **P2a** | 角色资产 | 9:16确认稿 + 16:9设定板 | 逐批确认 | `character-assets.md` |
| **P2b** | 关键道具 | 3:4道具母板 | 逐件确认 | `prop-assets.md` |

### 核心原则

- **只处理已定稿剧情** — 发现冲突时指出并等待拍板，不改戏。
- **每轮只展示当前需要确认的一步** — 用户明确"确认"后才解锁下一阶段。
- **所有提示词修订从当前有效事实重新编译** — 不在旧稿后追加补丁。
- **只引用真实存在的上传素材** — 没有真实参考图时删除全部素材编号。
- **用户上传结果不等于定稿** — 必须明确确认后才能作为下游依赖。

### P0 项目接收（自动执行）

读取剧本后，自动输出项目基准卡，**不单独询问确认**，直接在同一回复中继续 P0A。

### P0A 十项剧本解析 + 情绪曲线

读取 `references/story-analysis.md`，按以下顺序输出十项分析：

1. **一句话故事与核心主题**
2. **类型与现实程度**
3. **国家、地域与年代**
4. **季节与剧情时间轴**
5. **语言与声音文化**
6. **世界与威胁规则**
7. **空间链**
8. **人物关系与小传**
9. **状态链与视觉母题**
10. **全片情绪曲线图** — 读取 `references/emotion-curve.md`，8-14节点

P0A 展示后固定询问：
```text
【请确认】以上 P0A 剧本解析与创作基准（包含全片情绪曲线图）是否确认？
【确认后下一步】建立 P1 全片摄影风格、环境色彩策略与声音圣经。
```
📎 加载：`references/story-analysis.md`（P0A 十项剧本解析 阶段必须读）
📎 加载：`references/emotion-curve.md`（P0A 十项剧本解析 阶段必须读）

### P1 创作基准

读取 `references/creative-baseline.md`，提出 **1 套完整推荐**：

1. **影视参考** — 1 部主要 + 最多 1 部补充
2. **摄影系统** — 胶片/数字/机型/镜头/画幅/帧率
3. **全片风格锁定** — 六要素全部具体化
4. **环境色彩策略**
5. **人物声音气质基准**
6. **音乐圣经**
📎 加载：`references/creative-baseline.md`（P1 创作基准 阶段必须读）

### P2a 角色资产

读取 `references/character-assets.md`：

1. 输出生产清单（依赖规则：血缘→换装/受伤/变异→年龄）
2. 第 1 批 9:16 单人确认稿
3. 后续批次依赖解锁
4. 全部确认后一次性生成 16:9 角色设定板
📎 加载：`references/character-assets.md`（P2a 角色资产 阶段必须读）

### P2b 关键道具母板

读取 `references/prop-assets.md`：统一 3:4 竖构图，单件产品档案照。

---
📎 加载：`references/prop-assets.md`（P2b 关键道具母板 阶段必须读）

## 台词容量预检系统

> 完整规则：`references/dialogue-capacity.md`

### 最低时长公式

```
最低时长 = 可发声汉字 ÷ 语速 + 标点停顿 + 反应留白

慢速压抑 2.5-3.2 字/秒  恐惧、迟疑、压抑、真相揭示、告别
冷静克制 3.0-3.8 字/秒  低声、压低声线、从容威胁、冷硬问句
正常对白 3.3-4.2 字/秒  普通交流、解释、平稳叙述
快速急促 4.3-5.2 字/秒  争吵、催促、慌乱、短句追问

逗号 0.20-0.35 秒
句号/问号/感叹号 0.35-0.60 秒
省略号/破折号/告别句/真相揭示 额外 0.5-2 秒
```

### 视觉读取锚点

微信、短信、屏幕、监控文字属视觉读取：原文与标点必须出现在可见载体上，按阅读速度预留停留时间，**不产生说话人、不产生口型、不产生音色**。

### 容量判定

每组先预留必要动作（默认 3 秒）、口型收束、视觉读取、倾听反应和稳定组尾时间。

`口型台词最低时长 + 视觉读取最低时长 + 动作反应预留 > 组时长上限` 时立即停止该组规划，在原文 `。！？；` 优先、其次 `，`、再次自然换气处拆段。

**禁止**：先写镜头，再用加速语速、重叠时间码、隐藏切镜或删除反应来修补。

**机算复核**：`./SKILL.sh dialogue "原台词" --pace slow` 或 `./SKILL.sh check-group --model <模型> --duration <秒> --line "…"`；规划取区间上界，结果与本节公式不一致时以本节为准并修脚本。

---

## 分组硬门

> 完整规则：`references/grouping-density.md`

### 时长上限（按模型）

| 模型 | 单次最大时长 | 分组硬上限 |
|------|-------------|-----------|
| Seedance 2.0 | 15秒 | **15秒** |
| Seedance 2.5 | 30秒 | **30秒** |
| Kling 3.0 | 15秒 | **15秒** |
| Veo 3 | 8秒 | **8秒** |

> 数值以 `references/modes-and-recipes.md` 为准；二者不一致时以权威文件为准，并同步本表与 `scripts/seedancer_calc.py`（`tests/test_calc.py` 校验三者一致）。

### 拆组规则

**优先不拆**：场景连续、时间连续、站位可自然承接、前一动作直接逼出后一动作、合并后时长内可完成且台词不超载。

**必须拆**：超过时长上限；场景或时间跳跃；站位必须重新建立；具体动作目标已完成/失败/被替换；台词超过容量。

### 组尾 = 可继承稳定状态

**禁止停在**：武器举起未挥出、人物跌落中、物体半空、道具交接未完成、已接触但结果未出现、台词未说完。

### 承接等式

```
上一组末尾空间状态的在场人物集合 = 下一组人物空间站位的起手人物集合
```

已离场移除，本组新入场按入场时间码加入。

### 时长参考

| 总时长 | 建议组数 |
|--------|---------|
| 45-60秒 | 4-6组 |
| 61-90秒 | 6-8组 |

超出范围要能由场景跳跃、时间跳跃、动作目标断裂或台词承载解释。

---

## 镜头密度四道门

> 完整规则：`references/grouping-density.md`

### 短漫剧三档

| 类别 | 覆盖任务 | 15秒镜头硬下限 base15 | 反馈空档硬上限 Gmax |
|:---|:---|---:|---:|
| `ordinary` | 普通文戏、对话、信息交代 | 6 | 3秒 |
| `action_reversal` | 动作冲突、追逐、抢夺、强反转 | 8 | 2.5秒 |
| `fight` | 攻击、防守、受击、反击、连续命中 | 10 | 2秒 |

### 计算公式

```
Smin(T) = ceil(T × base15 / 15)
Bmin >= Smin
```

| 组时长 T | ordinary | action_reversal | fight |
|---:|---:|---:|---:|
| 6秒 | 3 | 4 | 4 |
| 9秒 | 4 | 5 | 6 |
| 10秒 | 4 | 6 | 7 |
| 12秒 | 5 | 7 | 8 |
| 15秒 | 6 | 8 | 10 |
| 30秒 (Seedance 2.5) | 12 | 16 | 20 |

机算：`./SKILL.sh smin <T> <档位>`；分镜定稿前用 `check-group --shots <N>` 一次跑完时长、台词、Smin 三道门。

### 四道门必须同时通过

1. 编号镜头数 ≥ Smin
2. 有效可见拍点数 ≥ Bmin
3. 每个编号镜头至少 1 个属于本镜的新反馈
4. 组首到首个反馈、相邻反馈之间、末个反馈到组尾三处空档均 ≤ Gmax

### 有效可见拍点

有源剧本依据、有可辨初态与末态、观众能在分配时间内读懂的一次状态改变。只换焦段、景别、构图、景深、色调或运镜而没有新信息、新因果、新反应的不算拍点。

### 隐藏切镜（直接失败）

单个编号镜头内出现 `交替近景`、`反打`、`跳切`、`切至`、`插入镜头`、`蒙太奇`，或无可达路径的观察点突变，均属隐藏切镜。每次真实切换必须拆成新的编号镜头。

### 关键路径承载

`镜头最低承载时长 = 串行关键路径各节点最低时长之和`

同一人的多句台词、不同人依次说出的台词、同一肢体的多个动作必须串行累计。

---

## SCALE LAW — 尺度锁定法

> 视频模型没有尺寸记忆。凡出现超大/超小/非标尺度角色或物体，每镜必带「尺寸对比 + 人形参照物」双锚。

```
THE SCALE LAW — VISIBLE PROOF IN THE PICTURE: <对象> stands <实际高度> tall —
<尺寸类比>, and <参照人> at his foot reaches just above the ankle.
In every frame <对象>'s silhouette is at least <N> TIMES the height of the human figure beside him.
```

---

## 体裁适配

| 维度 | 横屏电影感 | 横屏短剧 | 漫剧 | 竖屏短视频 |
|---|---|---|---|---|
| 画幅 | 16:9 | 16:9 | 16:9 或 9:16 | 9:16 |
| 单镜时长 | 8–12s | 5–10s | 4–8s | 3–8s |
| Style Prefix | 原版逐字 | 原版逐字 | 漫画变体 | 可降格 |
| 首帧 | wide establishing | wide establishing | 全景或半身 | medium portrait |
| 节奏 | 沉稳 | 快切 | 分镜感强 | 极快 |
| 密度档位 | 质性判断 | ordinary/action | action/fight | fight/action |

**铁律：体裁只改节奏与风格参数，不改一致性纪律和密度硬门。**

---

## 语言路由

> **Language Notice**: This skill's reference documents are primarily in Chinese. English speakers: see README.md for overview. The skill supports generating prompts in multiple languages based on user input.

| 用户输入语言 | 提示词语言 | 说明文字语言 |
|---|---|---|
| 中文 | **中文** | 中文 |
| 英文 | **英文** | 英文 |
| 日文 | **日文** | 日文 |
| 其他 | **英文** (default) | 英文 |

- Block 名称始终英文
- 技术标签始终英文
- @tag 始终英文

---

## 运镜设计系统

> 完整规则：`references/camera-design.md`
📎 加载：`references/camera-and-styles.md`（运镜设计 阶段必须读）

### 主动运镜三要素（缺一不可）

1. **起始观察点** — 门槛内/外、肩后、前方/后方、左侧/右侧、高处/低处、平视/仰视/俯视
2. **运动轨迹方向** — 向前推近/向后拉远/横向侧跟/摇向/向上升起/弧形环绕
3. **停止结果** — 停在谁身上、什么景别、看到什么

### 运镜功能表

完整运镜功能表（含叙事功能、方向段写法、最小时长）见 `references/camera-design.md`。三要素口径以上一节为唯一定义，硬约束统一列在下方「关键规则」。

### 关键规则

- 每组至少 1 个主动运镜镜头
- 含 `缓慢/慢速/徐徐/慢推/慢摇/慢移/渐近/渐远` 的镜头必须 ≥3 秒
- 每镜最多 2 个运动分量
- 狭窄空间（走廊、车内、电梯）禁用环绕与弧轨，改用侧跟或横移
- **「摄影机」与运动动词之间不得插入逗号**
- 每场登记一次运镜主轴（不登记不得写分镜）：稳定观察/逐渐逼近/逐渐疏离/跟随行动/空间揭示/群像压迫

---

## 输出格式硬门

> 完整规则：`references/output-format.md`

<!-- dup-allow-start: 输出格式硬门簇（完整文件顺序 / 四项事实 / 时间码 / 台词写法 / 空间与人物指代词表 / 媒介翻译表 / 体量控制）为**契约原文**，必须与 output-format.md 逐字一致 —— 故 D1 跳过本区；改动需两侧同改 ; target=output-format.md -->
### 完整文件顺序（区块名逐字使用）

```markdown
# 《剧本名》｜视频类型｜媒介｜画幅

## 使用的 @资产清单
人物：@角色名 ...
场景：@场景名 ...
道具：@道具名 ...

## 状态资产引用
使用正式状态资产：... / 无。
使用临时状态引用：... / 无。
建议补做状态资产：... / 无。

临时资产引用说明：当前为临时资产引用版，建议后续补做正式多状态资产库。 / 不适用。
## 参数确认
- 画幅比例：...
- 视频类型：...
- 媒介/视觉风格：...
- 音频参考：未提供 / 已提供并列出引用名
- 资产模式：严格资产库 / 临时资产引用

## 全局风格提示词
风格锁定：媒介来源，渲染方式，角色质感，运动质感，材质语言，光影色彩。
特殊风格化：不启用。 / 启用；作用范围、进入方式、退出方式和现实层保持规则。

## 角色音色设定
@角色名：年龄与声线；语速与断句；音量范围；气息与咬字；情绪底色；禁止项。

## 第1组：组标题
本组剧情：...
人物空间站位：...
空间承接：...（仅需要时输出）
环境：...

镜头1（0-X秒）：
一个按发生顺序书写的完整自然段。

约束：有音效，无音乐，无字幕。
本组末尾空间状态：...
视频时长：X秒
```

### 镜头自然段写法

每个镜头标题下只写**一个连续自然段**，按镜头内真实发生顺序融合：

```
媒介化视觉起点与景别 → 摄影机或观察点 → 人物和道具初态 → 第一动作或运镜
→ 原台词在开口时刻出现 → 倾听、接触、受力、结果和反应 → 声光在触发点变化 → 可继承末态
```

### 每镜四项事实（缺一不可）

1. **视觉起点**：景别与焦段或等效透视
2. **观察关系**：摄影机或观察点相对主体的位置、朝向
3. **构图落位**：主体画面位置、前后景、遮挡、画面填充
4. **摄影机状态**：明确写出有目的的固定，或含三要素的主动运镜

### 时间码规范

- 标题格式 `镜头N（起-止秒）：`
- 起止只能是整数秒
- 从 0 连续递增，不重叠不倒退不留无说明空档
- 最后一个镜头的结束秒必须等于组时长
- 每组镜头编号都从 `镜头1` 重新开始

### 台词写法

- 原台词与原标点逐字嵌入，一字不改
- 放入规范中文引号 `"……"`
- 在人物**真正开口的时刻**插入，不提前不延后
- 明示发声方式：现场口型、画外、旁白、电话、录音、设备播报
- 无台词镜头明写"无人开口"或"全程无人说话"
- 引号内绝不添加 `@`

---

## 空间与人物指代硬门

> 完整规则：`references/output-format.md`

### 空间措辞硬门

**禁止模糊方位词**：`一侧`、`一边`、`另一侧`、`另一边`、`某侧`、`某边`、`斜侧`、`侧前方`、`门边`、`桌旁`、`不远处`、`适当距离`。

`前方`、`后方`、`左`、`右` 必须带明确参照主体。`旁边`、`靠近`、`外侧` 只有同时给出固定锚点与接触或身体尺度关系时才可用。

**禁止输出**：米、厘米、毫米、小数距离、东南西北罗盘方位、`全画幅` 或 `全画幅等效` 字样、`虚拟镜头`。

焦段简写：`24mm广角视角`、`50mm标准视角`、`65mm中焦视角`、`85mm长焦视角`。数值焦段后必须紧跟景别：`65mm中景`、`85mm近景`。

用画内关系代替精确尺寸：`镜头贴近地面`、`略高于@林岚视线`、`两人伸手即可触及@密码箱`。

### 人物指代硬门

除原台词引号内部外，正文**禁止人物代词**：`我`、`你`、`您`、`他`、`她`、`他们`、`她们`、`本人`、`其`、`对方`、`自己`。必须重复明确姓名或资产名。

代词不得从参数、资产清单、上一字段、上一镜头或上一组继承。双人对话、多人场面、接触、受力、道具争夺、视线切换时，发起者、承受者、持有人、观察者都写明确姓名。

**原台词及原标点完整豁免**。引号内出现"我、你、他、她"原样保留。

### 视听术语双语

正文中的景别、运镜、角度、视角类专业名词写作 `中文（English）`，同一术语每组只在该组首次出现时附英文。

---

## 媒介翻译表

| 媒介 | 内部推演 | 正文输出 |
|---|---|---|
| 真人写实 | 真实可达机位、全画幅等效视角、合理景深 | 简写焦段视角 + 可见机位关系 |
| 写实3DCG | 虚拟摄影机、等效视角、PBR、全局光照 | 简写焦段视角 + 可见观察关系 |
| 风格化3DCG | 等效透视、轮廓、比例、材质风格 | 等效透视 + 风格化描述 |
| 2D | 景别、构图、前中后景分层、层间视差 | 景别 + 图层层次 |

所有媒介共同保留：景别、观察点、画面落位、焦点目标、层次、动作时序、对白时机、声光因果、镜头末态。

---

## 体量控制

- 每组不超过 **1800 汉字**
- 每镜只承担一个主要目的
- 环境细节最多 2 项
- 身体姿态锚点最多 3 个
- 英文专业视觉锚点最多 2 个
- 压缩优先级：重复光线词、重复镜头词、格式冗余在前；关键动作、原台词、口型停顿、空间站位、情绪转折不可压缩

---

<!-- dup-allow-end -->

## 失败现象对照表

| 失败现象 | 错误码 | 根因 | 解法所在 |
|---|---|---|---|
| 角色换脸/换衣 | `F-ID-DRIFT` / `F-STATE-DRIFT` | 描述不完整 | descriptor 逐字注入 + GEO |
| 人物瞬移/跳轴 | `F-AXIS` / `F-SPATIAL-RESET` | 缺 GEO | `geo-spatial-layout.md` |
| 表演像死人/假 | `F-PERFORMANCE` | 写感受非行为 | `acting-performance.md` |
| 图像崩坏/多指 | `F-MATERIAL` | 模型弱点未规避 | `lira-image-prompt.md` |
| 巨人越画越矮 | — (SCALE LAW) | 缺尺度锚点 | SCALE LAW 段 |
| 多出人物/克隆家具 | `F-DUP-SUBJECT` / `F-PROP-DUP` | 约束缺失 | EXACT N + POSITIVE CONSTRAINTS |
| 自带配乐 | `F-AUDIO-POLLUTION` | 缺 `SFX only. No music.` | 技术标签收尾 |
| 模型自创台词 | `F-DIALOGUE-TEXT` | 缺硬封锁 | 引号内台词 + 静默约束 |
| 台词被压缩/语速不合理 | `F-DIALOGUE-CAPACITY` | 未做容量预检 | `dialogue-capacity.md` |
| 组尾不稳定/承接断裂 | `F-GROUP-CONTINUITY` | 未遵守承接等式 | `grouping-density.md` |
| 密度不足/空档过长 | `F-DENSITY` | 未过四道门 | `grouping-density.md` |
| 隐藏切镜 | `F-HIDDEN-CUT` | 单镜内多视点 | `grouping-density.md` |
| 模糊方位/代词指代 | `F-SPATIAL-VAGUE` | 未遵守硬门 | `output-format.md` |

完整诊断：`references/failure-codes.md`（6 类 38 码 + 责任层决策树）

---
📎 加载：`references/acting-performance.md`（失败现象对照表 阶段必须读）

## 九条黄金规则

1. **资产优先。** 锁定并压力测试所有角色/地点/道具前，不生成任何镜头。
2. **逐字描述一切。** 模型无记忆，descriptor 每镜逐字进提示词，绝不缩写。
3. **一次只改一处。** 提示词是工作机；整段重写会丢掉已生效的部分。
4. **给模型更少自由。** 用角落不用房间、用锚点不用空场、用地图不用猜、一镜一动作。
5. **镜头不行就简化镜头，不简化文字。** 拆成两镜、删动作、换角度。
6. **台词先算再写。** 台词容量预检不过，不进入分镜。
7. **组尾必须稳定。** 承接等式不成立，不进入下一组。
8. **密度必须达标。** 四道门不过，不交付。
9. **禁止代词和模糊方位。** 正文出现代词或模糊方位，立即修正。

---

## 新模型能力速览

各模型能力差异见 `references/model-mechanics.md`（模型机制与能力矩阵）。

## 并发控制协议

**批量并发生成时，必须先加载 `references/concurrency-control.md`**（并发表、令牌桶、指数退避、
限流保护的完整实现均在该文件；本入口不重复）。

hard stops：并发上限按平台档位；退避必须有上限；限流触发即降速而非重试风暴。

### 进度状态查询协议

**批量执行期间查询进度：加载 `references/progress-query.md`**（三种查询接口、状态定义、
实时更新机制在该文件）。

## 模型自动选择系统

> 借鉴 ShotFunClaw `task-selector.js` 设计，基于场景/预算/能力自动推荐模型。

#### 选择维度

| 维度 | 选项 | 影响 |
|------|------|------|
| 场景类型 | 照片真实感/快速出图/720p视频/1080p视频/30秒长视频/口播视频/品牌广告/动作物理 | 推荐模型 |
| 预算偏好 | 低（省钱）/ 中（平衡）/ 高（质量优先） | 过滤价格档位 |
| 能力需求 | 参考图/真人素材/音画同出/局部编辑/文字渲染 | 过滤能力支持 |

#### 场景→模型映射表

| 场景 | 推荐模型 | 备选模型 | 价格档位 |
|------|----------|----------|----------|
| 照片级真实感图片 | GPT Image 2 | Nano Banana 2 | 高 |
| 快速出图（原型/测试） | Nano Banana 2 | Seedream 5.0 Pro | 低 |
| 帧编辑（修改已有图） | Nano Banana Pro | — | 中 |
| 文字渲染/品牌Logo | Nano Banana Pro | MiniMax H3 | 中 |
| 720p视频（性价比） | Seedance 2.0 | Seedance 2.0 Mini | 中 |
| 1080p视频（高质量） | Kling 3.0 Omni | Seedance 2.5 | 高 |
| 30秒长视频 | Seedance 2.5 | — | 中 |
| 口播视频（音画同出） | Kling 3.0 Omni | MiniMax H3 | 中 |
| 品牌/广告（文字精准） | MiniMax H3 | Nano Banana Pro | 中 |
| 动作/物理交互 | Kling 3.0 | Seedance 2.5 | 中 |
| 多模态参考生成 | Wan 3.0 | Seedance 2.5 | 中 |
| 原生立体声/2K | MiniMax H3 | — | 中 |
| 真人素材（需报白） | Seedance 2.0 | Kling 3.0 Omni | 中 |

#### 选择流程

```
1. 用户描述场景 → Agent 判断场景类型
2. 询问预算偏好（低/中/高）
3. 询问能力需求（参考图/真人/音画同出等）
4. 根据映射表推荐模型 + 解释理由
5. 用户确认后使用
6. 写入 manifest.json 的 modelSelection 字段
```

#### 并发控制

| 任务类型 | 默认并发 | 环境变量 |
|----------|----------|----------|
| 图片生成 | 30 | `SEEDANCER_IMAGE_CONCURRENCY` |
| 视频生成 | 50 | `SEEDANCER_VIDEO_CONCURRENCY` |
| 视频分析 | 10 | `SEEDANCER_ANALYSIS_CONCURRENCY` |
| 音频生成 | 20 | `SEEDANCER_AUDIO_CONCURRENCY` |

---

### 视频 / 图像生成模型

**模型清单、时长上限与定价：加载 `references/model-mechanics.md` 与 `modes-and-recipes.md`**（单一权威，本入口不重复维护）。

🔴 **硬规则**：**视频模型选用前必须先询问用户**，不得自行选定。
📎 加载：`references/model-catalog.md`（视频 / 图像生成模型 阶段必须读）

## 运营循环 (Operating Loop)

每个请求经过 **12 个门控**（v6.0.0 新增门控 7A 和门控 7B），按顺序执行：
📎 加载：`references/checkpoint-resume.md`（运营循环 阶段必须读）

### 门控 0: 预生产检测

| 条件 | 路径 |
|------|------|
| 用户提供剧本/大纲，需要做完整项目 | → 进入 P0 预生产管线 |
| 用户已有角色/道具资产图 | → 跳过 P0-P2，进入门控 1 |
| 用户只需单镜头/快速生成 | → 跳过 P0-P2，进入门控 1 |

### 门控 0A: 预生产阶段 (P0 → P0A → P1 → P2)

按 P0-P2 详细流程执行，每个阶段有明确的确认门禁。

### 门控 1: 接收 (Intake)

识别目标、生产阶段、目标平台、模式、时长、比例、参考素材、音频需求、交付物、安全/IP 风险。

### 门控 2: 来源核查 (Source Gate)

事实优先 — 关于平台能力、API、价格、模型名称的说法，必须有来源支撑。

### 门控 3: 模式选择 (Mode Gate)

| 模式 | 输入 | 关键约束 |
|------|------|----------|
| **T2V** | 只有文字描述 | 完整场景描述 |
| **I2V** | 首帧图片 | 只描述变化 |
| **V2V** | 参考视频 | 明确转移/不转移 |
| **R2V** | 多个参考素材 | 为每个素材分配角色（最多 50 个） |
| **FLF2V** | 首帧+尾帧 | 只描述过渡 |
| **Edit** | 源视频+编辑指令 | 只改指定区域/时间段 |
| **Extend** | 已生成视频 | 从实际最后一帧开始 |
| **ClayRef** | 3D白模 | 空间/姿态/机位 |
| **GreenScreen** | 绿幕素材 | 替换背景+光影重渲染 |

### 门控 4: 能力检查 (Capability Check)

加载 `references/model-mechanics.md` 理解 10 大机制。

### 门控 5: 参考映射 (Reference Map)

每个参考素材分配一个主角色 + 排除规则。

### 门控 6: 安全门控 (Safety Gate)

**🔴 安全与数据边界（v9.0.1 新增，优先级最高，先于本节其它检查）**

涉及**真人素材**（照片/视频/声纹等）时，**必须先过 `references/asset-whitelist.md` §0 的四项确认**：
① **权利与同意**（本人同意；未成年须监护人）② **授权范围**（用途/期限/地域/是否允许二次训练）
③ **数据边界**（传哪些文件、给哪个外部服务、是否必须出本机）④ **留存与撤回**（留存期限/删除方式/撤回路径）。

**未过四项确认，不得把素材上传到任何外部服务。**

- 未成年人 / 公众人物 / 未授权第三方 / 证件·医疗·私密影像：**默认拒绝上传**，需用户明示授权。
- **数据最小化**：只传必需素材、剥离元数据、优先脱敏或 AI 生成替代。
- **禁止规避平台机制**：不得用同义词替换、变形、切片、改元数据等方式绕过平台安全/审核/合规；
  被拦截时**按要求修改内容或停止**，并如实告知用户。
- **留痕**：四项确认结果记入项目工作台；交付说明列出「传了什么、给了谁、留多久、怎么撤回」。


涉及 IP、肖像、品牌、真实人物 → 先处理安全问题再生成。

### 门控 7: 提示词构建 (Prompt Build)

使用 **CINEDANCE 16-block 架构**。

### 门控 7A: 台词容量预检 (Dialogue Capacity Gate)

**加载**：`references/dialogue-capacity.md`

检查项：
1. 提取全部口型台词与视觉读取锚点
2. 按语速档位计算最低时长
3. 预留动作反应时间（默认 3 秒）
4. 判断是否超过组时长上限
5. 超载 → 在稳定状态拆段
6. 未超载 → 进入门控 7B

**铁律**：不过此门，不进入分镜写作。

### 门控 7B: 分组与密度门控 (Grouping & Density Gate)

**加载**：`references/grouping-density.md`

检查项：
1. 按拆组规则分组（时长上限、场景跳跃、动作目标）
2. 每组时长 ≤ 模型上限（Seedance 2.5=30s, 2.0=15s, Kling 3.0=15s, Veo 3=8s）
3. 组尾是否为可继承稳定状态
4. 承接等式是否成立
5. 判定密度档位（ordinary / action_reversal / fight）
6. 计算 Smin、Bmin、Gmax
7. 四道门是否同时通过
8. 不通过 → 增加镜头或缩短组时长后重算

**铁律**：不过此门，不输出分镜。

### 门控 8: 质量检查 (Quality Pass)

- **反空洞检查** — 删除所有空洞质量词
- **单变量检查** — 每次只改一个东西
- **预算检查** — 这个镜头值得再试一次吗？
- **错误码诊断** — 用 `references/failure-codes.md` 命名问题
- **代词检查** — 正文是否有我/你/他/她（引号内豁免）
- **方位检查** — 是否有模糊方位词
- **每镜必要条件检查** — 每镜是否写全必要条件（定义见 §输出格式硬门）
- **运镜三要素检查** — 主动运镜是否有起始+轨迹+停止
- **时间码检查** — 是否整数、连续、不重叠、末镜结束=组时长

---
📎 加载：`references/anti-slop-lexicon.md`（质量检查 阶段必须读）

## 核心流程 (8 阶段标准流程)

### 阶段一：剧本解构 + 序列分类

从用户输入提取：场景、角色、关键道具（资产）、情绪弧线、序列分类。

### 阶段二：导演交互 — 🔴 不可跳过

必须向用户确认：视觉风格基调、时长策略、超自然规律、生成模式、视频模型。
📎 加载：`references/ai-director.md`（导演交互 阶段必须读）

### 阶段三：资产变量表建立

将所有可复用元素抽象为变量引用。资产建立遵循 LIRA 系统。
📎 加载：`references/reference-role-map.md`（资产变量表 阶段必须读）

### 阶段四：全局基础设定

```
【全局基础设定】
━━━━━━━━━━━━━━━━━━━━━
🎨 环境与光影：[整体氛围 + 主光源 + 光影风格]
👤 人物资产：{{变量引用}} + [表演约束]
📷 摄影机参数：[机型风格] + [镜头光圈] + [快门策略]
🎭 表演基调：[表演风格总纲 + 禁止项]
🔊 声音设计：[配乐] + [音效] + [环境音]
📝 文字渲染：[需要出现的文字内容 + 位置 + 字体风格]
🗺️ GEO 空间锁定：[GEO SPATIAL LAYOUT，每场景写一次逐镜粘贴]
🎨 Style Prefix：[逐字粘贴到每个提示词末尾]
🎯 运镜主轴：[稳定观察/逐渐逼近/逐渐疏离/跟随行动/空间揭示/群像压迫]
━━━━━━━━━━━━━━━━━━━━━
```
📎 加载：`references/geo-spatial-layout.md`（阶段四：全局基础设定 阶段必须读）

### 阶段五：时间片分镜脚本 — 硬门强化

> 本阶段整合 Elio V2.3 的分组硬门、密度门控、运镜设计、输出格式。
> 加载：`dialogue-capacity.md` + `grouping-density.md` + `camera-design.md` + `output-format.md`

两种模式：
- **时间片模式**：单镜头内情绪递进（0-10s, 10-20s, 20-30s，首尾相接不留空档）
- **镜头组模式**：多镜头剪辑（按组分段）

**分镜写作硬门**：
1. 台词容量预检已过（门控 7A）
2. 分组与密度已过（门控 7B）
3. 每组使用输出格式硬门的结构
4. 每镜写一个连续自然段（按发生顺序）
5. 每镜必要条件缺一不可（定义见 §输出格式硬门）
6. 主动运镜三要素缺一不可
7. 禁止代词、禁止模糊方位
8. 时间码整数秒、连续、不重叠
9. 组尾 = 可继承稳定状态
10. 承接等式成立
📎 加载：`references/cinedance-video-prompt.md`（时间片分镜脚本 阶段必须读）

### 阶段六：提示词审核与执行 — 🔴 不可跳过

必须先输出完整提示词草稿给用户审阅。审核时使用 QA 检查清单（含门控 8 全部检查项）。

### 阶段六点五：局部编辑协议（Seedance 2.5）

| 条件 | 选择 |
|------|------|
| 只有 1-2 个元素不对，其余 90 分 | ✅ 局部编辑 |
| 整体构图/光影/运动都不对 | 重新生成 |
| 需要保持精确的镜头运动轨迹 | ✅ 局部编辑 |
| 提示词本身有误 | 修正提示词 + 重新生成 |

### 阶段七：生成后评估与迭代（重拍协议）
📎 加载：`references/retake-protocol.md`（生成后评估与迭代 阶段必须读）

#### 六判定取景

| 判定 | 适用场景 | 下一步 |
|------|----------|--------|
| **保留** | 核心目标达成 | 锁定 |
| **后期修复** | 问题在后期能解决 | 交给后期 |
| **局部编辑** | 只有局部元素有问题 | 用局部编辑协议 |
| **重生成** | 运气不好 | 同提示词，新种子 |
| **重写** | 同一问题出现 2 次以上 | 改提示词 |
| **换模式** | 当前模式无法满足需求 | 换生成模式（如 T2V→I2V/R2V） |

### 阶段八：序列项目管理

当项目超过单次生成时长，进入序列项目管理。详见 `references/sequence-project-state.md`。

---
📎 加载：`references/continuation-handoff.md`（序列项目管理 阶段必须读）

## CINEDANCE 16-block 提示词架构

```
1.  SCENE CONTEXT         — 发生什么、谁在镜内、时长
2.  ACTIVE REFERENCES     — 角色/地点标签 + 各自角色命名
3.  LOCATION MAP          — 用文字描述地点地理（GEO SPATIAL LAYOUT）
4.  FIRST FRAME & SPATIAL BLOCKING — 第一帧谁站哪
5.  FORMAT MODE           — 单镜 or 硬切、时长
6.  OPTICS                — 镜头（FOV 对角线视角）+ 对焦计划
7.  CAMERA                — 摄影机怎么动（整合运镜设计系统）
8.  ACTION TIMING         — 动作逐拍、按秒
9.  PHYSICS               — 重量、接触、一切运动的惯性
10. LIGHTING              — 单一光源逻辑
11. AUDIO                 — 嗓音描述 + 原句；仅 SFX
12. CHARACTER ACTING      — 状态、欲望、隐藏、身体节奏
13. STYLE                 — Style Prefix，逐字粘贴
14. QUALITY               — 细节与稳定要求
15. POSITIVE CONSTRAINTS  — 每个计数与禁令
16. 技术标签收尾           — Photorealistic. NON-IP. [画幅]. [时长]s. SFX only. NO CGI. Cinematic.
```

---

## Style Prefix

**逐字粘贴到每个视频提示词的 STYLE block 末尾。**

三条根条款（不可删除）：
1. **Skin** — 毛孔级真实感，防止塑料脸
2. **Acting** — 湿润活眼 + 眼神光，防止死脸
3. **Continuity** — 无身份漂移，防止换脸

详见 `references/style-prefix.md`。

---
📎 加载：`references/style-prefix.md`（Style Prefix 阶段必须读）

## 交付物体系

| 交付物 | 内容 | 文件位置 |
|---|---|---|
| 资产生图提示词 | 每个角色/地点/道具的 LIRA 优化图像提示词 | `01-assets/<type>/<tag>_image_prompt.md` |
| 分镜首帧生图提示词 | 每镜一张首帧参考图提示词 | `04-prompts/image/shot_<NNN>_frame.md` |
| 分镜视频提示词 | 每镜 CINEDANCE 16-block 视频提示词 | `04-prompts/video/shot_<NNN>_v<N>.md` |
| 参考图清单 | 每镜用哪些参考图、上传顺序 | `04-prompts/reference_manifest.md` |
| 交付物总清单 | 文件索引 + 检查表 | `08-delivery/deliverable-manifest.md` |

---
📎 加载：`references/deliverable-system.md`（交付物体系 阶段必须读）
📎 加载：`references/lira-image-prompt.md`（交付物体系 阶段必须读）

## 矛盾检测规则

生成提示词前，必须执行 **六层自检**（v6.0.0 新增两层）：
1. 构图矛盾检测
2. 情绪连续性检测
3. 物理连续性检测
4. 口型与台词一致性检测
5. **台词容量检测** — 最低时长是否超过组时长
6. **密度与承接检测** — 四道门是否通过、承接等式是否成立

---

## 中英对照术语速查表

### 景别 (Shot Size)

| 中文 | 英文 | 常用焦段（参考） |
|------|------|---------|
| 大全景 | Extreme Long Shot | ≤24mm |
| 全景 | Full Shot | 25-35mm |
| 中景 | Medium Shot | 36-55mm |
| 中近景 | Medium Close-up | 56-79mm |
| 近景 | Close Shot | 80-120mm |
| 特写 | Close-up | 121-200mm |
| 大特写 | Extreme Close-up | >200mm |

> 景别由**机位距离 × 焦段**共同决定，上表只是常见搭配、不是一一对应：同一 85mm 贴近是特写、远离是中景。正文始终写「焦段 + 景别」（如 `85mm近景`）。

### 镜头运动 (Camera Movement)

| 中文 | 英文 | 最小时长 |
|------|------|---------|
| 固定 | Static / Fixed | 按对白 |
| 快推 | Fast Push-in | ≥1s |
| 推近 | Push-in | ≥1s |
| 慢推 | Slow Push-in | **≥3s** |
| 跟拍 | Tracking Shot | ≥1s |
| 横移 | Truck | ≥1s |
| 摇 | Pan | ≥1s |
| 升起 | Crane Up | **≥3s** |
| 拉远 | Pull Back | **≥3s** |
| 环绕 | Orbit / Arc | **≥3s** |

> 最小时长以 `references/camera-design.md` 为准；凡含缓慢类词（缓慢/慢速/徐徐/慢推/慢摇/慢移/渐近/渐远）的运镜一律 ≥3s。

---

## 平台限额（见权威文件）

限额、模式与配方**以 `references/modes-and-recipes.md` 为唯一权威**（本入口不再重复维护数字）。

## 参考文档加载表（门控 → 必须加载）

> **本表是 references/ 的强制入口**：到对应门控/阶段时**必须**加载右侧文件，再继续；
> 未过加载不计为已过门。触发时机均为正文中真实存在的标题（`I3` 断言，禁止“未定位”兜底）。
> 全部文档摘要见 `references/INDEX.md`。

| 门控 / 阶段（触发时机） | 必须加载 |
| --- | --- |
| v7.0.0 — 五大导演系统 | `camera-emotion-sync.md`、`json-api-mode.md`、`lighting-rules.md`、`performance-micro-beats.md`、`scene-prototypes.md` |
| 硬门总览 | `camera-design.md`、`dialogue-capacity.md`、`grouping-density.md`、`output-format.md` |
| P0-P2 五大阶段 | `character-assets.md`、`creative-baseline.md`、`emotion-curve.md`、`prop-assets.md`、`story-analysis.md` |
| P0 项目接收（自动执行） | `project-workbench.md` |
| P1 创作基准 | `visual-bible.md` |
| 运镜设计系统 | `camera-and-styles.md` |
| 失败现象对照表 | `acting-performance.md`、`failure-codes.md`、`geo-spatial-layout.md`、`lira-image-prompt.md` |
| 新模型能力速览 | `model-mechanics.md` |
| 并发控制协议 | `concurrency-control.md` |
| 进度状态查询协议 | `progress-query.md` |
| 视频 / 图像生成模型 | `model-catalog.md`、`modes-and-recipes.md`、`recipes.md` |
| 运营循环 (Operating Loop) | `checkpoint-resume.md` |
| 门控 3: 模式选择 (Mode Gate) | `execution-modes.md` |
| 门控 6: 安全门控 (Safety Gate) | `asset-whitelist.md` |
| 门控 8: 质量检查 (Quality Pass) | `ai-self-check-repair.md`、`anti-slop-lexicon.md`、`cost-gates.md`、`eight-item-self-check.md`、`qa-strict-gates.md` |
| 阶段二：导演交互 — 🔴 不可跳过 | `ai-director.md` |
| 阶段三：资产变量表建立 | `reference-role-map.md` |
| 阶段五：时间片分镜脚本 — 硬门强化 | `cinedance-video-prompt.md`、`shared-boundary-storyboard.md` |
| 阶段七：生成后评估与迭代（重拍协议） | `retake-protocol.md`、`structured-failure-report.md`、`video-analysis-pipeline.md` |
| 阶段八：序列项目管理 | `continuation-handoff.md`、`sequence-project-state.md` |
| Style Prefix | `style-prefix.md` |
| 交付物体系 | `content-fingerprint.md`、`deliverable-system.md` |
| 文档导航 | `qa-checklists.md` |

> 维护：新增 reference 必须同时登记本表与 `references/INDEX.md`（`scripts/check_consistency.py` 的 `I1`/`I2`/`I3` 精确断言）。

## 文档导航

- 完整版本历史见 **`CHANGELOG.md`**（唯一权威）
- 四张检查清单（预生产 / 硬门 / 提示词构建 / 生成后评估）统一收在 `references/qa-checklists.md`，按 Part A–E 组织。出片前逐部分过，不要凭记忆。
