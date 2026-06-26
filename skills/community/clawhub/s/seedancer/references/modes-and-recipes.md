# 模式说明与交互笔记（Mode Reference & Interaction Notes）— 即梦 Seedance 2.0 / Seedancer

> **v2.2.0 升级说明**：本文件所有电影专业术语采用"中文（English）"中英对照格式，与 SKILL.md v2.2.0 及 references/camera-and-styles.md 保持一致。

---

## 模式选择（Mode Selection）

### 1) 纯文本模式（Text-to-Video）
没有参考素材时使用。提示词必须承载所有视觉引导：风格（Style）、色调（Color Tone）、角色描述（Character Description）、镜头（Camera Shot）、时间线节拍（Timeline Beats）。

适用场景：
- 原创角色/生物概念设计（Original Character / Creature Concept Design）
- IP 安全的抽象场景（IP-Safe Abstract Scenes）
- 快速概念验证（Quick Concept Validation）

最佳实践：
- 开头声明比例（Aspect Ratio）、时长（Duration）、帧率（Frame Rate）和风格（Style）
- 角色/生物使用完全原创名称和独特特征
- 所有动作用五维度节拍描述（Five-dimension Beat Description）
- 提示词控制在 200 字以内（过长会生成失败）

### 2) 首帧模式（Image-to-Video）
上传单张首帧图片（或首帧+尾帧）加文本提示词。模型从首帧出发生成动画。

适用场景：
- 已有概念图/分镜图需要动画化（Concept Art / Storyboard to Animation）
- 口播视频（上传角色照片 + 音频）（Talking Head Video）
- 产品展示（上传产品照片）（Product Showcase）

关键技巧：
- 首帧构图决定最终画面的起点，确保主体位置合理
- 尾帧可选上传，模型会自动生成中间过渡动作（Interpolation）
- 首尾帧主体位置和姿态需合理衔接（Seamless Pose Transition）

### 3) 全参考模式（Reference-to-Video）
同时上传图片和视频、音频进行多模态控制。赋予创作者对表演（Performance）、光影（Lighting）、运镜（Camera Movement）的调度权。

适用场景：
- 需要精确复刻某段运镜或动作（Precise Camera/Action Replication）
- 角色一致性（Character Consistency）要求高的多镜头序列
- 音乐节拍同步（Music Beat Sync）
- 复杂多资产场景（Complex Multi-asset Scenes）

### 4) 视频延长模式（Extend / Video Extension）
上传已有视频作为 `@视频1`，写 `延长 @视频1 X 秒`。模型从原视频结尾继续生成。

⚠️ **关键规则**：
- 生成时长选择 = **新增片段的时长（Extension Duration）**，不是最终总时长（Total Duration）
- 提示词中需包含连续性描述（Continuity Description）（角色从上一段结尾动作直接过渡到新动作）
- 交接帧（Handoff Frame）需稳定姿态、清晰构图

### 5) 视频编辑模式（Edit / Video Editing）
对已有视频的指定片段、角色、动作或剧情进行定向修改。

适用场景：
- 替换视频中某个角色（Character Replacement）
- 修改特定动作或特效（Action / VFX Modification）
- 调整场景元素（Scene Element Adjustment）

---

## @asset 引用模式（@asset Reference Pattern）

始终在提示词正文之前映射素材，减少错误：

```text
素材映射（Asset Mapping）：
- @图片1 = 首帧（First Frame） / 角色身份锚定（Character Identity Anchor）
- @图片2 = 环境风格参考（Environment Style Reference）
- @视频1 = 运动 + 镜头参考（Motion + Camera Reference）
- @音频1 = 音乐节奏 / 台词音频（Music Rhythm / Dialogue Audio）
```

在 12 个文件限制内，按影响力排序使用：
1. 核心视觉风格（Core Visual Style）（2-3 张图）
2. 角色/主体参考（Character / Subject Reference）（1-3 张图）
3. 动作/镜头参考（Motion / Camera Reference）（1 段视频）
4. 音频基础（Audio Foundation）（1 段音频）
5. 支持细节（Supporting Details）（剩余插槽）

---

## 可充分利用的控制能力（Available Control Capabilities）

Seedance 2.0 擅长：
- **多镜头叙事（Multi-shot Narrative）**：自动生连贯的多镜头序列，角色/场景/氛围全程一致
- **音画同步（Audio-visual Sync）**：原生双声道立体声，含背景音乐/环境音效/口型同步（8+ 语言）
- **物理仿真（Physics Simulation）**：高级模式适合运动、碰撞场景（基础/可选）
- **角色一致性（Character Consistency）**：跨镜头保持面部特征、发型、配饰完全一致
- **运镜复刻（Camera Movement Replication）**：准确复制推拉变焦（Push-pull Zoom）、跟踪镜头（Tracking Shot）和机械臂多角度跟拍（Robotic Arm Multi-angle Tracking）
- **视频延长（Video Extension）**：将片段链式连接超过 15 秒限制
- **视频编辑（Video Editing）**：对指定片段/角色/动作/剧情进行定向修改

---

## 导演交互流程（Director Interaction Flow）

### 第一次交互（收到剧本/想法后）
向导演确认以下变量：

1. **视觉风格基调（Visual Style Tone）**：全局美学倾向
   - 示例选项：高反差纪实（High-contrast Documentary）/ 复古科幻（Retro Sci-fi）/ 现代极简（Modern Minimalist）/ 水墨国风（Ink-wash Chinese Style）/ 赛博朋克（Cyberpunk）
   
2. **时长策略（Duration Strategy）**：叙事节奏倾向
   - 动作快切（Quick Action Cuts）（短镜头组接）vs 长镜头叙事（Long Take Narrative）（一镜到底 / Single Continuous Shot）
   
3. **超自然规律（Supernatural Rules）**：特殊能量或物理现象的视觉表现
   - 示例：法术粒子密度（Spell Particle Density）/ 能量颜色（Energy Color）/ 重力异常表现方式（Gravity Anomaly Visuals）
   
4. **生成模式（Generation Mode）**：根据用户素材情况选择
   - 纯文本（Text-to-Video）/ 首帧（Image-to-Video）/ 全参考（Reference-to-Video）

### 后续交互（输出初版提示词后）
- 导演可针对任一维度要求调整（如"把光影改暗一点"、"节奏再快一些"）
- 根据反馈修改后重新输出

---

## 对白与音效设计（Dialogue & Sound Design）

当提示词包含角色台词或音效时，将其作为视觉方向的**独立层级（Independent Layer）**：

```text
[时间段（Time Segment）]：[视觉动作和镜头（Visual Action & Camera）]
对白（角色名，情绪）（Dialogue: Character Name, Emotion）："台词"
音效（Sound Effect）：[环境/效果描述]
```

最佳实践：
- 每 3-5 秒时间段最多一条对白
- 情绪显式标记（Explicit Emotion Tags）：`冰冷（Cold）`、`绝望（Desperate）`、`欢快（Cheerful）`、`耳语（Whisper）`
- 音效单独描述：脚步声（Footsteps）、环境嗡鸣（Ambient Hum）、配乐高潮（Score Climax）、寂静（Silence）
- 结尾音频收束（Audio Resolution）：`配乐淡出（Score Fade Out）`、`环境风声（Ambient Wind）`、`寂静（Silence）`
- 口播视频必须开启口型同步（Lip Sync），确保音频清晰无杂音

---

## 多段工作流（Multi-segment Workflow）— 超过 15 秒

### 路径一：视频延长接力（Video Extension Relay）— 推荐新手
1. 开头声明 **总时长（Total Duration）** 和 **分段数量（Segment Count）**
2. 第一段：正常生成，结束于**干净的交接帧（Clean Handoff Frame）**
3. 第二段及之后：上传上一段作为 `@视频1`，使用 `延长 @视频1 X 秒`
4. 每段末尾包含 **交接帧描述（Handoff Frame Description）**
5. 向前传递：身份（Identity）、服装（Costume）、光照（Lighting）、镜头风格（Camera Style）、场景连续性（Scene Continuity）

### 路径二：分段独立生成 + 剪辑拼接（Independent Generation + Edit Assembly）— 高级，质量更可控
1. 所有段落共用同一套角色图和场景图
2. 每段独立生成，使用统一的 prompt 模板
3. 最后编辑软件中拼接，可添加过渡效果（Transition Effects）✅

---

## 一镜到底/连续镜头技巧（Long Take / Continuous Shot Tips）

- `@图片1` 作为首帧（First Frame）（主角/开场构图）
- 额外图片作为 **场景路标点（Scene Landmarks）** — 镜头经过的地点、角色或道具
- 将提示词写成一条连续摄像机路径（Continuous Camera Path），按顺序经过每个路标点
- 明确注明：`无剪辑（No Cuts）、单镜头连续拍摄（Single Continuous Take）、一镜到底（Long Take）` ✅
- 15 秒配合 3-5 个路标点效果最佳

---

## 产品展示技巧（Product Showcase Tips）

- 将产品照片绑定为 `@图片1`，作为身份锚定（Identity Anchor）
- 技巧：**360° 旋转（360° Spin）**、**3D 爆炸视图（3D Exploded View）**、**重组卡合（Reassembly Snap）**、**英雄光效（Hero Lighting）** ✅
- 指定材质渲染（Material Rendering）✅：`玻璃反射（Glass Reflection）` ✅、`金属光泽（Metallic Sheen）` ✅、`哑光质感（Matte Texture）`、`半透明辉光（Translucent Glow）`
- 背景保持干净：影棚渐变（Studio Gradient）、中性表面（Neutral Surface）或情境化生活场景（Lifestyle Context）

---

## 口播视频批量工作流（Talking Head Video Batch Workflow）

适合系列内容（如每天一条知识分享）：
1. 建立统一角色档案（Unified Character Profile）（多角度照片：正面/侧面/表情特写）
2. 写标准 prompt 模板，每段仅替换动作描述和音频
3. 使用视频延长功能（Video Extension）接力生成，或使用分段独立生成 + 统一参考
4. 每段控制在 10-13 秒（别卡满 15 秒，留余量给转场 / Transition）

---

## 常见陷阱（Common Pitfalls）

- 文件过多但未明确每个素材的角色
- 遗漏身份（Identity）/服装（Costume）/道具（Props）的连续性（Continuity）指令
- 混淆目标总时长（Total Duration）与延长时间（Extension Duration）
- 请求可能被政策拦截的写实人脸（即梦平台）
- 使用系列名、角色名或品牌近似词（触发审核拒绝）
- 过于接近可识别的标志性特征
- 从参考图中保留品牌 Logo 或商标而未明确去除
- 不为可推断的 IP 引用添加负面约束（Negative Constraints）
- 提示词超过 200 字导致生成失败
- 首尾帧主体位置和姿态不合理导致衔接断裂

---

## 快速验证清单（Quick Verification Checklist）

- [ ] 文件数量和大小限制已遵守（总≤12，图片≤9，视频≤3，音频≤3）
- [ ] 混合文件总数 ≤ 12
- [ ] 时长（Duration）在 4 到 15 秒之间
- [ ] 每个参考素材都有明确的 `@asset` 角色（Asset Role）
- [ ] 提示词包含五维度信息（Five Dimensions）：镜头（Camera）/ 物理（Physics）/ 情感（Emotion）/ 光影（Lighting）/ 节奏（Pacing）
- [ ] 必要时包含负面约束（Negative Constraints）
- [ ] 提示词和素材描述中无系列名、角色名、品牌名
- [ ] 负面约束明确列出所有可推断的 IP 引用（IP References）
- [ ] 角色/生物使用完全原创的名称和独特视觉特征（Original Name & Visual Features）
- [ ] 对白（Dialogue）和音效（Sound Effects）作为视觉动作的独立层级写入
- [ ] 多段视频有明确的交接帧描述（Handoff Frame Description）
- [ ] 镜头术语（Camera Terms）与 `camera-and-styles.md` 词汇表一致
- [ ] 提示词总长度 ≤ 200 字

---

## 🆕 时间片模式（Time-Slice Mode）— v2.1 新增

### 概述（Overview）

时间片模式（Time-Slice Mode）是为**单镜头内情绪复杂递进（Complex Emotion Progression within Single Shot）**场景设计的提示词结构。与 Shot-by-Shot 模式不同，它不切割镜头，而是按时间轴分段描述同一连续镜头内的情绪演变。

### 适用场景（Use Cases）

- ✅ 单镜头内情绪多次转变（Multiple Emotion Shifts in Single Shot）（如恐惧→倔强→决绝）
- ✅ 微表情表演（Micro-expression Performance ⚠️）需要精确时间控制
- ✅ 摄影机参数需要随情绪变化（Camera Parameters Emotion Sync）（如快门角度递进 / Shutter Angle Progression ⚠️）
- ✅ 台词嵌入表演节奏中（Dialogue Embedded in Performance Rhythm）
- ❌ 多镜头剪辑（Multi-shot Editing）（用 Shot-by-Shot 模式）
- ❌ 需要明显场景切换（Scene Change Required）（用多段工作流 / Multi-segment Workflow）

### 结构组成（Structure）

```
【全局基础设定（Global Base Setup）】        ← 统领所有时间片
  ├─ 🎨 环境与光影（Environment & Lighting）
  ├─ 👤 人物资产（Character Asset）
  ├─ 📷 摄影机全局参数（Camera Global Parameters）
  ├─ 🎭 表演基调（Performance Tone）
  └─ 🔊 声音设计（Sound Design）

【资产变量表（Asset Variable Table）】       ← 可复用元素的变量定义

【时间片分镜脚本（Time-Slice Storyboard）】 ← 按时间轴分段
  ├─ 🎬 0-Xs（情绪锚点 / Emotion Anchor：A·B）
  ├─ 🎬 X-Ys（情绪锚点 / Emotion Anchor：C·D）
  └─ 🎬 Y-Zs（情绪锚点 / Emotion Anchor：E·F）
```

### 与 Shot-by-Shot 模式的对比（Comparison with Shot-by-Shot Mode）

| 维度（Dimension） | 时间片模式（Time-Slice Mode） | Shot-by-Shot 模式（Shot-by-Shot Mode） |
|------|-----------|------------------|
| 镜头数（Shot Count） | 单镜头连续（Single Continuous Shot） | 多镜头剪辑（Multi-shot Editing） |
| 分段依据（Segmentation Basis） | 时间轴（Timeline）（0-6s, 7-15s） | 镜头 ID（Shot ID）（Shot 1, Shot 2） |
| 情绪表达（Emotion Expression） | 在同一镜头内演变（Evolution within Single Shot） | 每个镜头有独立情绪（Independent Emotion per Shot） |
| 摄影机（Camera） | 可描述参数递进（如快门变化）（Parameter Progression） | 每个镜头独立参数（Independent Parameters per Shot） |
| 适用（Best For） | 表演特写（Performance Close-up）、情绪戏（Emotional Scenes） | 动作剪辑（Action Editing）、场景转换（Scene Transitions） |

### 关键规则（Key Rules）

1. **时间片连续（Continuous Time-slices）**：0-6s → 7-15s（不要漏掉第 6 秒）
2. **情绪锚点必写（Emotion Anchor Required）**：每段必须有 `（情绪锚点 / Emotion Anchor：A·B）`
3. **双保险描述（Dual-insurance Description）**：技术参数后必须跟视觉翻译（Visual Translation）
4. **矛盾检测（Contradiction Check）**：全局设定与时间片之间不能有逻辑矛盾

### 全局基础设定说明（Global Base Setup Description）

全局基础设定（Global Base Setup）在所有时间片之前建立，统领整段视频的视觉基调（Visual Tone）：

| 层（Layer） | 作用（Function） | 示例 |
|----|------|------|
| 🎨 环境与光影（Environment & Lighting） | 锁定整体氛围（Atmosphere）、光源类型（Light Source Type）、渲染风格（Rendering Style） | 「极寒幽暗体育馆，高对比度顶光（Top-down Spotlight）✅，UE5 超写实（UE5 Hyperrealistic 💡）」 |
| 👤 人物资产（Character Asset） | 引用资产变量，添加表演约束（Performance Constraints） | `{{人物 1}}` + 「画面内只出现面部（Face Only in Frame）」 |
| 📷 摄影机全局参数（Camera Global Parameters） | 机型（Camera Model）、光圈（Aperture）、快门递进策略（Shutter Progression Strategy ⚠️） | 「ARRI Alexa 35 ✅, T1.5 大光圈（Large Aperture）✅, 45°→90°→180° 递进（Progression）」 |
| 🎭 表演基调（Performance Tone） | 表演风格总纲 + 禁止项 | 「拒绝夸张大喊，力量向内收缩（Reject Exaggeration, Internalize Power）」 |
| 🔊 声音设计（Sound Design） | 配乐（Score）/音效（SFX）/口型（Lip Sync）需求 | 「无配乐（No Score）、仅有自然音效（Natural SFX Only）」 |

### 情绪锚点速查（Emotion Anchor Quick Reference）

情绪锚点（Emotion Anchor）是两个关键词，作为语义锚帮助模型锁定该时间段的情绪基调：

- 恐惧·挣扎（Fear · Struggle）
- 偏执·倔强（Obsession · Stubbornness）
- 决绝·爆发（Resolve · Eruption）
- 宁静·空洞（Serenity · Emptiness）
- 隐忍·克制（Endurance · Restraint）
- 温柔·眷恋（Tenderness · Attachment）
- 迷失·游移（Lost · Wandering）

完整速查见 `camera-and-styles.md` 情绪锚点关键词速查表（Emotion Anchor Keywords Quick Reference）。

### 时间片模式快速验证清单（Time-Slice Mode Quick Checklist）

- [ ] 全局基础设定（Global Base Setup）完整（环境 / Environment / 人物 / Character / 摄影机 / Camera / 表演 / Performance / 声音 / Sound）
- [ ] 资产变量表（Asset Variable Table）已建立
- [ ] 每个时间片有情绪锚点（Emotion Anchor per Time-slice）
- [ ] 时间片连续无间隙（Continuous Time-slices, No Gaps）
- [ ] 技术参数有视觉翻译兜底（Visual Translation for Technical Parameters）
- [ ] 全局与时间片无逻辑矛盾（No Logical Contradictions between Global and Time-slices）
- [ ] 台词嵌入时间片内（Dialogue Embedded in Time-slice）（非独立 tag / Not Independent Tag）
