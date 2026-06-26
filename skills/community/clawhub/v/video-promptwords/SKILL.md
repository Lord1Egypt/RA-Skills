# Video Prompting Skill

AI 视频生成提示词工程指南——覆盖 Sora、Runway Gen-3/4、Kling、Seedance 2.0、Veo 2、Hailuo、Pika 等主流模型。

---

## 1. 视频提示词核心结构

一个高质量的视频提示词通常包含以下维度（不必每个都写，但越多越精确）：

```
[主体] + [动作/运动] + [场景/环境] + [镜头语言] + [光影氛围] + [风格/美学] + [技术参数]
```

### 各维度详解

| 维度 | 说明 | 示例 |
|------|------|------|
| **主体** | 谁/什么，外貌穿着细节 | A woman in a red silk dress, mid-30s, short black hair |
| **动作/运动** | 主体在做什么，怎么动 | slowly walking forward, turning her head to the left |
| **场景/环境** | 在哪里，周围有什么 | in a dimly lit Tokyo alley at night, neon signs reflecting in puddles |
| **镜头语言** | 摄影机怎么拍（最关键！） | tracking shot, low angle, slow dolly in, drone aerial |
| **光影氛围** | 光线、色调、氛围感 | golden hour lighting, volumetric fog, cinematic warm tones |
| **风格/美学** | 艺术风格、电影参考 | Wes Anderson style, film grain, anamorphic lens, 35mm |
| **技术参数** | 帧率、分辨率、时长等 | 4K, 60fps, 16:9, slow motion 120fps |

---

## 2. 镜头语言词汇表（最实用的部分）

### 运镜方式

| 英文术语 | 中文 | 效果描述 |
|----------|------|----------|
| **Static shot** | 固定镜头 | 摄影机不动，画面静止，适合展现场景 |
| **Pan** | 水平摇镜 | 摄影机左右转动，水平扫视场景 |
| **Tilt** | 垂直摇镜 | 摄影机上下转动，展示高低 |
| **Dolly in/out** | 推拉镜头 | 摄影机物理前后移动，靠近/远离主体 |
| **Truck** | 横移镜头 | 摄影机左右平移 |
| **Tracking shot** | 跟踪镜头 | 摄影机跟随主体移动 |
| **Crane shot** | 摇臂镜头 | 大幅度上下运动，从高到低或反之 |
| **Drone shot / Aerial** | 无人机/航拍 | 俯瞰大场景 |
| **Handheld** | 手持摄影 | 有轻微晃动，纪实感 |
| **Steadicam** | 稳定器 | 流畅移动但不晃 |
| **Whip pan** | 快速摇镜 | 快速转场，动感强 |
| **Orbit / 360°** | 环绕镜头 | 绕主体旋转 |
| **Push-in** | 缓慢推近 | 制造紧张感或亲密感 |
| **Pull-back reveal** | 后拉揭示 | 从细节开始，后拉揭示大场景 |
| **Rack focus** | 焦点转换 | 前景模糊→后景清晰，或反之 |
| **Zoom in/out** | 变焦 | 不移动摄影机，光学放大/缩小 |

### 拍摄角度

| 英文术语 | 中文 | 效果 |
|----------|------|------|
| **Eye level** | 平视 | 自然、客观 |
| **Low angle** | 仰拍 | 主体显得强大、威严 |
| **High angle** | 俯拍 | 主体显得渺小、脆弱 |
| **Bird's eye** | 鸟瞰 | 从正上方俯视 |
| **Worm's eye** | 虫眼视角 | 从地面极低角度仰视 |
| **Dutch angle / Tilted** | 倾斜构图 | 不安、紧张、疯狂 |
| **Over-the-shoulder** | 过肩镜头 | 对话场景，增加代入感 |
| **POV** | 第一人称 | 观众视角，沉浸感 |

### 景别

| 英文术语 | 中文 | 描述 |
|----------|------|------|
| **Extreme close-up (ECU)** | 极近景 | 只拍眼睛/嘴巴等局部 |
| **Close-up (CU)** | 近景 | 头部+肩部 |
| **Medium close-up (MCU)** | 中近景 | 胸部以上 |
| **Medium shot (MS)** | 中景 | 腰部以上 |
| **Medium full shot (MFS)** | 中全景 | 膝盖以上 |
| **Full shot (FS)** | 全景 | 全身 |
| **Wide shot (WS)** | 远景 | 主体+大量环境 |
| **Extreme wide shot (EWS)** | 大远景 | 主体很小，以环境为主 |
| **Establishing shot** | 建置镜头 | 交代场景位置 |

---

## 3. 光影氛围词汇

| 英文术语 | 中文 | 效果 |
|----------|------|------|
| **Golden hour** | 黄金时刻 | 日出/日落暖光，电影感最强 |
| **Blue hour** | 蓝色时刻 | 日出前/日落后冷蓝调 |
| **Overcast / Diffused** | 阴天/漫射光 | 柔和无硬阴影 |
| **Hard light** | 硬光 | 强烈阴影，戏剧感 |
| **Volumetric lighting** | 体积光 | 光束穿过雾/烟，丁达尔效应 |
| **Backlighting / Rim light** | 逆光/轮廓光 | 主体边缘发光 |
| **Chiaroscuro** | 明暗对比 | 强烈光影对比，伦勃朗光 |
| **Neon lighting** | 霓虹灯 | 赛博朋克/都市夜景 |
| **Practical lighting** | 实用光源 | 画面内的灯/蜡烛/屏幕照亮 |
| **Lens flare** | 镜头光晕 | 光线直射镜头产生光晕 |
| **Silhouette** | 剪影 | 主体全黑，背景亮 |
| **Film noir** | 黑色电影 | 高对比黑白，硬阴影 |

---

## 4. 风格美学词汇

| 关键词 | 风格 |
|--------|------|
| **Cinematic** | 电影感（万能修饰词） |
| **Documentary / Verité** | 纪录片风格，手持晃动 |
| **Film grain** | 胶片颗粒感 |
| **Anamorphic** | 变形宽银幕，横向光晕 |
| **35mm / 16mm / 8mm** | 不同胶片质感 |
| **VHS / Found footage** | 录像带/伪纪录片 |
| **Stop motion** | 定格动画 |
| **Anime / Ghibli** | 日式动画/吉卜力 |
| **Cyberpunk** | 赛博朋克 |
| **Vaporwave** | 蒸汽波 |
| **Oil painting / Watercolor** | 油画/水彩风格 |
| **Photorealistic** | 照片写实 |
| **Hyperrealistic** | 超写实 |
| **Wes Anderson** | 韦斯·安德森（对称、马卡龙色） |
| **David Fincher** | 大卫·芬奇（冷色调、暗沉） |
| **Christopher Nolan** | 诺兰（IMAX、宏大、时空） |
| **Terrence Malick** | 马利克（自然光、诗意、慢镜） |
| **Blade Runner style** | 银翼杀手（霓虹+雨+暗调） |

---

## 5. 运动与动态描述技巧

视频和图片最大的区别就是**运动**。描述运动要具体：

### ❌ 模糊
> A person walking

### ✅ 具体
> A woman in a flowing white dress walking slowly through a sunlit wheat field, her dress catching the wind, camera tracking alongside her at eye level

### 运动描述要素
- **速度**: slowly, gradually, rapidly, suddenly
- **方向**: from left to right, toward the camera, away into the distance
- **节奏**: with a pause, continuously, in bursts
- **主体内部运动**: hair blowing, clothes rippling, eyes darting
- **环境运动**: leaves falling, rain pouring, smoke rising, water rippling
- **摄影机运动**: (见第2节)

### 常用运动句式
```
- The camera slowly dollies in as [subject] [action]
- [Subject] enters from the left, [action], then exits right
- Starting from a close-up of [detail], the camera pulls back to reveal [scene]
- A low-angle tracking shot following [subject] as [action]
- Time-lapse of [scene] over [duration], showing [change]
- Slow motion at 120fps: [action] with [detail visible]
```

---

## 6. 各平台特性与提示词适配

### Sora (OpenAI)
- 擅长：物理真实感、复杂运动、长镜头
- 提示词风格：自然语言叙述，像在描述电影场景
- 长度：可以很长，细节越多越好
- 特殊：理解时间和因果关系，可以描述"先...然后..."
```
例：A stylish woman walks down a Tokyo street filled with warm glowing neon and animated city signage. She wears a black leather jacket, red dress, and boots, carrying a black purse. She walks casually but confidently. Many pedestrians walk about. The street is damp and reflective, creating a mirror effect of the colorful lights. Cinematic, 4K.
```

### Runway Gen-3/4
- 擅长：风格化、艺术化、快速迭代
- 提示词风格：简洁有力，关键词组合
- 建议：强调运镜和风格，主体描述清晰
```
例：Cinematic tracking shot, a dancer in red leaping through fog, volumetric lighting, anamorphic lens flare, slow motion
```

### Kling (快手)
- 擅长：人像、中国风、口型同步
- 提示词风格：中英文皆可，偏叙述性
- 建议：描述具体动作和表情变化
```
例：一位穿着汉服的年轻女子站在烟雨蒙蒙的江南水乡石桥上，手持油纸伞，微风轻拂衣袖，镜头缓慢推近，光影柔和
```

### Seedance 2.0 (ByteDance)
- 擅长：高保真、动作流畅、角色一致性
- 提示词风格：详细描述，强调动作序列
- 特殊：支持角色参考和音频驱动

### Veo 2 (Google)
- 擅长：电影级画质、物理一致性
- 提示词风格：类似 Sora，自然叙述

### Pika
- 擅长：快速生成、风格化、特效
- 提示词风格：简短有力

### Hailuo (MiniMax)
- 擅长：中文场景理解、自然运动
- 提示词风格：中文叙述效果好

---

## 7. 提示词模板（可直接套用）

### 🎬 电影叙事型
```
[Shot type] of [subject] [action] in [setting]. [Camera movement] as [secondary action]. [Lighting] lighting, [style/aesthetic]. Cinematic, [format].
```
**示例：**
> Medium shot of a detective in a trench coat stepping through a rain-soaked alley. The camera slowly dollies in as he pauses to light a cigarette. Neon and streetlight mix in volumetric fog. Film noir style, anamorphic, 4K 24fps.

### 🌍 场景建立型
```
An establishing [shot type] of [location/scene]. [Time of day], [weather/atmosphere]. [Key movement or change over time]. [Style], [format].
```
**示例：**
> An establishing wide shot of a coastal village at dawn. Mist rolls over the harbor as fishing boats rock gently. Golden hour light breaks through clouds. Terrence Malick inspired, 35mm film grain, 16:9.

### 🎭 角色展示型
```
[Shot type] portrait of [character description]. [Action/micro-expression]. [Camera movement]. [Lighting setup], [background]. [Style reference].
```
**示例：**
> Close-up portrait of an elderly man with weathered skin and kind eyes. He slowly smiles, deep wrinkles creasing. Camera slowly pushes in. Soft window light from the left, blurred bookshelf behind. Wes Anderson palette, 85mm lens, shallow depth of field.

### 🏃 动作运动型
```
[Shot type + camera movement] following [subject] as [action sequence]. [Speed/tempo]. [Environment interaction]. [Lighting], [style].
```
**示例：**
> Low-angle tracking shot following a parkour athlete as they vault over rooftops at sunset. Rapid cuts between angles. Wind whips their hoodie. Golden backlight, lens flare. Action cinema style, 60fps, 4K.

### 🎨 风格艺术型
```
[Subject] [action] in [style] style. [Color palette], [texture], [camera/staging]. [Mood/atmosphere].
```
**示例：**
> A cat walking across a rooftop in Studio Ghibli style. Soft watercolor sky, warm earth tones, gentle wind animation. Dreamlike and peaceful.

### 📱 UGC/短视频型
```
[POV/type], [person] [action], [setting]. [Natural/authentic detail]. [Casual framing].
```
**示例：**
> Selfie-style POV, a young woman trying a street food stall at a night market, steam rising, neon reflections on her face. Authentic, unstaged, iPhone quality.

---

## 8. 高级技巧

### 时间叙事
视频可以描述时间流逝：
```
- "Starting with X, the scene transitions to Y as Z happens"
- "Time-lapse: clouds race overhead as..."
- "The camera holds as the sun sets, transitioning from golden hour to blue hour"
```

### 多主体协调
```
Two figures approach each other from opposite sides of the frame, meeting in the center. Camera orbits slowly around them.
```

### 物理交互
```
Water splashes against rocks as waves crash. Droplets catch the light in slow motion.
```

### 情绪曲线
```
The scene begins calm and still, then builds energy as the wind picks up, culminating in a dramatic reveal as the clouds part.
```

### 避免的坑
1. **别堆关键词**——视频模型需要自然连贯的描述
2. **别矛盾**——"fast-paced static shot" 自相矛盾
3. **别忽略运动**——视频最重要的就是动，不写运动就是活的照片
4. **别过度限制**——给 AI 留创造空间，别每个像素都规定
5. **注意模型限制**——10秒视频别写3分钟的故事

---

## 9. 推荐学习资源

### GitHub 仓库
- **awesome-prompt-engineering** — 跨模态提示工程合集（含视频部分）
- 各模型的 prompt vault（Seedance/Sora/Grok 等）— 搜索 `seedance prompt vault` / `sora prompt library`
- **AI filmmaking pipeline** 仓库 — 多阶段视频制作流程

### 官方指南
- OpenAI Sora 提示词指南
- Runway Prompting Guide
- Kling 官方提示词文档

### 社区
- r/aivideo (Reddit)
- Civitai 视频模型提示词分享
- X/Twitter 上各模型官方账号的展示案例

---

*最后更新：2025-05-10*
