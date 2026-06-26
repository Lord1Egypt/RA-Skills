# 镜头语言、光学参数与视觉风格词汇表（Camera Language, Optics & Visual Style Glossary）

在 Seedance 2.0 提示词中使用以下术语，实现精确的电影级控制。

> **Seedance 2.0 术语说明**：Seedance 2.0 没有内置摄影机、镜头、光圈或色调预设，所有术语均为**提示词风格引导词（Prompt Style Anchors）**，通过语义引导模型生成方向。

---

## 实测有效性标记体系（Effectiveness Markers）

本文件使用三级标记体系标注每个术语在 Seedance 2.0 中的实测有效性：

| 标记 | 含义 | 适用范围 |
|------|------|---------|
| ✅ 实测有效（Tested & Effective） | 社区多人次测试验证，对输出有明显影响 | 景别、运镜、景深、焦距、光线类型、色彩分级 |
| ⚠️ 部分有效（Partially Effective） | 部分场景有效，建议配合视觉描述兜底 | 快门角度（Shutter Angle）、肌肉级微表情 |
| 💡 风格锚定（Style Anchor） | 作为整体美学方向引导，非精确参数 | UE5/Lumen/PBR/Ray Tracing 等渲染术语、摄影机美学 |

**使用建议**：💡 风格锚定术语必须搭配具体视觉描述（双保险）才能发挥最佳效果。

---

## 焦距与光学选择（Focal Length & Optics）

| 焦距 | 名称 | 用途 | 提示词写法 | 有效性 |
|---|---|---|---|---|
| **14-24mm** | 超广角（Ultra Wide Angle） | 宏大叙事、环境全景、空间压迫感、夸张透视 | `14mm 超广角仰拍，建筑线条向中心汇聚产生压迫感` | ✅ |
| **24-35mm** | 广角（Wide Angle） | 环境建立镜头、群像场景、动作场面 | `24mm 广角建立环境，前景人物与背景空间层次分明` | ✅ |
| **35-50mm** | 标准（Standard / Normal） | 自然透视、日常场景、对话场面 | `35mm 标准镜头，自然透视感，观众视角平视` | ✅ |
| **50-85mm** | 中长焦（Medium Telephoto） | 半身肖像、情感表达、人物与环境的关系 | `50mm 中景，人物半身入画，背景适度虚化` | ✅ |
| **85-135mm** | 长焦（Telephoto） | 肖像特写、压缩背景、聚焦情绪、分离主体 | `85mm 长焦特写，背景压缩为色块，主体从环境中剥离` | ✅ |
| **135mm+** | 超长焦（Super Telephoto） | 极远距离拍摄、极端背景压缩、偷窥视角 | `200mm 超长焦，极浅景深，背景完全虚化为散景` | ✅ |

### 特殊镜头（Specialty Lenses）

| 类型 | 效果 | 提示词写法 | 有效性 |
|---|---|---|---|
| **变形镜头（Anamorphic Lens）** ✅ | 横向椭圆形光斑、宽银幕视野、边缘色差 | `变形镜头，横向椭圆光斑，宽银幕光学畸变` | ✅ |
| **微距镜头（Macro Lens）** ✅ | 极浅景深、微观纹理清晰可见 | `微距镜头，极浅景深，昆虫翅膀纹理和复眼反光清晰可见` | ✅ |
| **移轴镜头（Tilt-Shift Lens）** ✅ | 选择性焦平面、微缩模型效果 | `移轴镜头，水平焦平面，城市呈现微缩模型感` | ✅ |
| **鱼眼镜头（Fisheye Lens）** ✅ | 极端桶形畸变、180° 视野 | `鱼眼镜头，极端桶形畸变，走廊线条弯曲向边缘` | ✅ |

---

## 景别（Shot Size / Framing）

| 术语 | 画面范围 | 典型用途 | 有效性 |
|---|---|---|---|
| **极特写（ECU / Extreme Close-up）** | 眼睛、手部或微小细节填满画面 | 情绪高潮、关键道具细节 | ✅ |
| **特写（CU / Close-up）** | 面部或单个物体，紧凑构图 | 角色表情、重要反应 | ✅ |
| **中近景（MCU / Medium Close-up）** | 头部和肩膀 | 对话场景、表情加肢体语言 | ✅ |
| **中景（MS / Medium Shot）** | 腰部以上 | 日常交互、手势表达 | ✅ |
| **中全景（MFS / Medium Full Shot）** | 膝盖以上 | 全身动作的局部展现 | ✅ |
| **全景（FS / Full Shot）** | 全身，从头到脚 | 完整角色动作、姿态展示 | ✅ |
| **远景（WS / Wide Shot）** | 主体加上大量环境 | 角色与环境的关系 | ✅ |
| **极远景（EWS / Extreme Wide Shot）** | 广阔景观，主体很小 | 建立镜头、规模感、孤独感 | ✅ |
| **双人镜头（Two-Shot）** | 两个主体同框 | 对话、对抗、亲密关系 | ✅ |
| **过肩镜头（OTS / Over-the-Shoulder）** | 从一个主体肩膀后方拍另一个 | 对话中强调听者反应 | ✅ |
| **主观视角（POV / Point of View）** | 镜头充当角色的眼睛 | 沉浸式体验、恐怖/悬疑 | ✅ |

---

## 镜头运动（Camera Movement）

| 术语 | 运动方式 | 情绪效果 | 有效性 |
|---|---|---|---|
| **推镜头（Push-in / Dolly-in）** | 镜头向主体靠近 | 紧张感增加、聚焦注意力 | ✅ |
| **拉镜头（Pull-back / Dolly-out）** | 镜头远离主体 | 展现规模、孤独感、揭示环境 | ✅ |
| **轨道镜头（Dolly Shot）** | 沿轨道平滑横向或前后移动 | 平滑流畅、专业电影感 | ✅ |
| **横移（Trucking / Lateral Dolly）** | 镜头水平滑动 | 跟随平行运动、展示空间关系 | ✅ |
| **摇镜头（Pan）** | 镜头绕轴水平旋转 | 环顾场景、跟随水平运动 | ✅ |
| **俯仰镜头（Tilt）** | 镜头绕轴垂直旋转 | 从脚到头揭示、展示高度 | ✅ |
| **摇臂/升降（Crane / Boom Shot）** | 镜头垂直升降 | 规模揭示、场景转换 | ✅ |
| **环绕（Arc / Orbit Shot）** | 镜头绕主体画弧运动 | 戏剧性展示主体、360° 审视 | ✅ |
| **跟拍/跟踪（Tracking / Follow Shot）** | 镜头跟随运动的主体 | 沉浸感、动作参与感 | ✅ |
| **手持（Handheld）** | 轻微有机抖动 | 纪实感、紧张不安、真实感 | ✅ |
| **稳定器（Steadicam / Gimbal Shot）** | 平滑漂浮运动穿越空间 | 优雅流畅、梦境感 | ✅ |
| **甩镜头（Whip Pan）** | 极快水平旋转 | 能量转换、场景切换 | ✅ |
| **变焦（Zoom）** | 镜头焦距变化（非物理移动） | 快速聚焦、复古风格 | ✅ |
| **推变焦/眩晕镜头（Dolly Zoom / Vertigo Effect）** | 镜头后移同时变焦拉近（或反向） | 空间扭曲感、角色内心失衡 | ✅ |

---

## 镜头角度（Camera Angle）

| 术语 | 说明 | 情绪效果 | 有效性 |
|---|---|---|---|
| **平视（Eye-level）** | 中性、自然视角 | 客观、平等、日常 | ✅ |
| **仰拍（Low Angle）** | 镜头从下往上拍主体 | 力量感、英雄感、威胁感 | ✅ |
| **俯拍（High Angle）** | 镜头从上往下拍主体 | 脆弱感、渺小感、被审视 | ✅ |
| **鸟瞰/俯视（Bird's Eye / Top-down）** | 正上方垂直向下 | 全局概览、上帝视角、战术视角 | ✅ |
| **荷兰角/倾斜（Dutch Angle / Canted Angle）** | 镜头绕轴倾斜 | 不安、紧张、混乱、疯狂 | ✅ |
| **虫视（Worm's Eye View）** | 极低位，贴地仰拍 | 极端压迫感、宏伟感 | ✅ |

---

## 焦点与景深（Focus & Depth of Field）

| 术语 | 效果 | 提示词写法 | 有效性 |
|---|---|---|---|
| **浅景深（Shallow DOF / Shallow Depth of Field）** | 背景虚化，主体突出 | `浅景深，背景化为柔和散景，主体清晰锐利` | ✅ |
| **深焦（Deep Focus）** | 全部清晰对焦，分层构图 | `深焦，前景人物与背景建筑均清晰可见` | ✅ |
| **变焦/跟焦（Rack Focus）** | 焦点从前景转移到背景（或反向） | `焦点从前景的手部缓慢转移至背景中的人物` | ✅ |
| **分裂屈光（Split Diopter）** | 两个平面同时对焦 | `分裂屈光，前景脸部与背景门框同时清晰` | ✅ |
| **散景（Bokeh）** | 柔和圆形背景光斑 | `背景散景呈六边形光斑，暖色环境光` | ✅ |

---

## 转场（Transition）

| 术语 | 说明 | 使用场景 | 有效性 |
|---|---|---|---|
| **切（Cut）** | 镜头之间瞬时切换 | 常规剪辑、节奏切换 | ✅ |
| **叠化（Dissolve）** | 两个镜头之间逐渐融合 | 时间流逝、梦境过渡 | ✅ |
| **淡入淡出（Fade In / Fade Out）** | 逐渐过渡到纯色（黑/白） | 场景开始/结束 | ✅ |
| **划像（Wipe）** | 一个镜头滑过另一个 | 风格化转场、复古感 | ✅ |
| **匹配剪辑（Match Cut）** | 基于相似形状或运动的剪辑 | 主题关联、时空跳跃 | ✅ |
| **猛切（Smash Cut）** | 突然剪辑制造冲击或对比 | 惊吓、反差、节奏突变 | ✅ |
| **甩镜转场（Whip Transition）** | 快速摇镜连接两个场景 | 动作片转场、能量延续 | ✅ |

---

## 节奏术语（Pacing / Temporal Terms）

| 术语 | 效果 | 提示词写法 | 有效性 |
|---|---|---|---|
| **慢动作/升格（Slow Motion / Slow-mo）** | 减速播放制造戏剧感 | `慢动作，60fps 感，水滴悬浮在空中` | ✅ |
| **延时（Time-lapse）** | 压缩时间，云/人群快速移动 | `延时摄影，云层快速翻涌，光影在地面扫过` | ✅ |
| **变速（Speed Ramp）** | 镜头内从慢到快（或反向）过渡 | `变速：子弹时间慢动作突然加速至正常速度` | ✅ |
| **定格（Freeze Frame）** | 单帧保持为静态图像 | `定格在角色跃起的最高点，画面暂停 2 秒` | ✅ |
| **快剪（Quick Cuts）** | 快速镜头切换制造能量感 | `快剪：每 0.5 秒切换一次视角，节奏紧张` | ✅ |
| **长镜头（Long Take）** | 无剪辑的长镜头 | `一镜到底 15 秒，无剪辑，连续跟拍` | ✅ |

---

## 视觉风格（Visual Style）

### 灯光方案（Lighting Setup）

| 术语 | 效果 | 适用场景 | 有效性 |
|---|---|---|---|
| **主光（Key Light）** | 主要光源，决定基调 | 所有场景的基础 | ✅ |
| **轮廓光/背光（Rim Light / Backlight）** | 边缘光将主体与背景分离 | 角色引入、戏剧性揭示 | ✅ |
| **补光（Fill Light）** | 柔化主光产生的阴影 | 减少对比度、柔和面部 | ✅ |
| **英雄光效（Hero Lighting）** | 戏剧性，产品广告风格，强烈高光 | 产品展示、英雄登场 | ✅ |
| **体积光（Volumetric Light / God Rays）** | 大气中可见的光束（上帝光/丁达尔效应） | 森林、教堂、尘埃空间 | ✅ |
| **霓虹光（Neon Lighting）** | 彩色人造光源，赛博朋克美学 | 城市夜景、科幻 | ✅ |
| **黄金时刻（Golden Hour）** | 温暖的低角度自然日光 | 浪漫、怀旧、史诗感 | ✅ |
| **蓝色时刻（Blue Hour）** | 冷色暮光环境光 | 孤独、宁静、科幻前奏 | ✅ |
| **钨丝暖光（Tungsten Warm Light）** | 室内橙暖色实用光 | 温馨室内、复古氛围 | ✅ |
| **明暗对比法（Chiaroscuro）** | 明暗区域高对比度 | 戏剧张力、黑色电影、恐怖 | ✅ |
| **伦勃朗光（Rembrandt Lighting）** | 面部三角形高光区 | 肖像、戏剧性面部特写 | ✅ |
| **蝴蝶光（Butterfly / Paramount Lighting）** | 鼻下方对称蝴蝶形阴影 | 美容、时尚、女性肖像 | ✅ |

### 色彩搭配（Color Palette）

| 术语 | 效果 | 情绪联想 | 有效性 |
|---|---|---|---|
| **暖色调（Warm Tone）** | 红、橙、金 | 能量、激情、温暖、怀旧 | ✅ |
| **冷色调（Cool Tone）** | 蓝、银、青 | 冷静、科技、忧郁、疏离 | ✅ |
| **低饱和/柔和（Desaturated / Muted）** | 低饱和度 | 写实、苍凉、复古、纪实 | ✅ |
| **高饱和/鲜艳（Vibrant / Saturated）** | 冲击力色彩 | 动画、奇幻、广告、活力 | ✅ |
| **单色（Monochromatic）** | 单一色相的明暗变化 | 极致风格化、压抑、专注 | ✅ |
| **互补/青橙对比（Complementary / Teal & Orange）** | 两种对立色（经典电影配色） | 商业大片标准配色 | ✅ |
| **粉彩（Pastel）** | 柔和浅色调 | 温柔、奇幻、治愈、梦幻 | ✅ |
| **高反差黑白（High-contrast B&W）** | 纯黑与纯白，无灰度过渡 | 极端风格化、noir、艺术电影 | ✅ |

### 美术/渲染风格（Art / Rendering Style）

| 术语 | 效果 | 适用场景 | 有效性 |
|---|---|---|---|
| **照片级写实（Photorealistic）** | 与真实拍摄难以区分 | 产品广告、写实剧情 | ✅ |
| **赛璐璐/卡通渲染（Cel-shading）** | 平涂色块加硬边轮廓线 | 动画、二次元、游戏 CG | ✅ |
| **水彩（Watercolor）** | 柔和渗透、纸张纹理、有机边缘 | 唯美、治愈、文艺 | ✅ |
| **水墨写意（Ink-wash / Sumi-e）** | 中日毛笔水墨美学 | 国风、武侠、仙侠 | ✅ |
| **3D CGI 渲染（3D CGI Rendering）** | 干净 CG，准确材质和光照 | 科幻、产品展示、教育 | ✅ |
| **定格动画（Stop-motion）** | 逐帧物理动画质感 | 趣味、手工感、怀旧 | ✅ |
| **像素风（Pixel Art）** | 复古低分辨率方块美学 | 游戏感、复古、趣味 | ✅ |
| **油画（Oil Painting）** | 厚重纹理，可见笔触 | 艺术感、史诗、古典 | ✅ |
| **日式动画（Anime Style）** | 日本动画风格，表情丰富 | 二次元、奇幻、青春 | ✅ |
| **混合媒介（Mixed Media）** | 单件作品中融合多种视觉风格 | 实验性、创意广告 | ✅ |

### 胶片颗粒与质感（Film Grain & Texture）

| 术语 | 效果 | 适用场景 | 有效性 |
|---|---|---|---|
| **35mm 胶片颗粒（35mm Film Grain）** ✅ | 有机纹理，经典电影感 | 剧情片、文艺片 | ✅ |
| **16mm 胶片颗粒（16mm Film Grain）** ✅ | 更粗颗粒，独立电影/复古外观 | 独立电影、纪录片 | ✅ |
| **干净数字（Clean Digital）** | 无颗粒，锐利现代外观 | 商业广告、科技产品 | ✅ |
| **VHS/模拟（VHS / Analog）** | 扫描线、色彩溢出、复古失真 | 80年代复古、恐怖、实验 | ✅ |
| **IMAX 清晰度（IMAX Clarity）** | 超锐利，大画幅电影细节 | 史诗大片、自然纪录片 | ✅ |

---

## 物理描述术语库（Physical Description Vocabulary）

用于五维度标准中的"物理表现（Physical Performance）"维度。

### 材质触感（Material Texture）

| 类别（Category） | 描述词汇（Descriptors） |
|---|---|
| **金属（Metal）** | 冷硬（cold, rigid）、反光（reflective）、共振微颤（resonant tremor）、氧化斑驳（oxidized patina）、镜面抛光（mirror polish） |
| **布料（Fabric / Cloth）** | 飘逸（flowing）、垂坠（draping）、褶皱堆积（fold accumulation）、纤维纹理（fiber texture）、透光薄纱（translucent gauze） |
| **皮肤（Skin）** | 毛孔可见（visible pores）、汗珠滚动（rolling sweat beads）、受力皱褶（stress wrinkles）、温度色差（thermal color shift） |
| **石材（Stone）** | 粗糙颗粒（rough granular）、风化裂纹（weathered cracks）、苔藓附着（moss coverage）、冷色调（cool tone） |
| **玻璃（Glass）** | 透明折射（transparent refraction）、指纹油污（fingerprint smudges）、边缘光穿透（edge light penetration）、碎裂放射纹（radial fracture pattern） |
| **液体（Liquid）** | 黏稠度（viscosity）、表面张力（surface tension）、飞溅轨迹（splash trajectory）、折射变形（refractive distortion） |

### 运动物理（Motion Physics）

| 类别（Category） | 描述词汇（Descriptors） |
|---|---|
| **惯性（Inertia）** | 启动迟缓（sluggish start）、制动前倾（braking lean）、甩动余波（swing residual）、重心转移（center-of-gravity shift） |
| **阻力（Drag / Resistance）** | 空气阻力拖尾（air drag trail）、水中减速（water deceleration）、泥土陷落（soil sinking） |
| **弹性（Elasticity）** | 反弹回弹（rebound bounce）、压缩蓄能（compression energy storage）、弹簧震颤（spring oscillation） |
| **重力（Gravity）** | 自由落体加速（free-fall acceleration）、抛物线轨迹（parabolic trajectory）、落地缓冲（landing cushion） |
| **碰撞（Collision / Impact）** | 冲击波扩散（shockwave propagation）、碎片飞溅（debris scatter）、接触凹陷（contact deformation）、震动传递（vibration transfer） |

### 流体与粒子（Fluids & Particles）

| 类别（Category） | 描述词汇（Descriptors） |
|---|---|
| **烟雾（Smoke）** | 低密度飘散（low-density drift）、浓烟翻滚（dense smoke billow）、螺旋上升（spiral rise）、涡流扩散（vortex diffusion） |
| **火焰（Flame / Fire）** | 内焰蓝白外焰橙黄（blue-white inner / orange-yellow outer flame）、热浪扭曲空气（heat haze distortion）、火星飞溅（spark scatter） |
| **水流（Water Flow）** | 层流平滑（laminar smooth flow）、湍流漩涡（turbulent vortex）、水花飞溅（water splash）、涟漪扩散（ripple diffusion） |
| **能量粒子（Energy Particles）** | 光点螺旋上升（light spiral ascent）、星尘飘散（stardust drift）、脉冲闪烁（pulse flicker）、轨迹拖尾（trail afterglow） |
| **灰尘（Dust / Particulate）** | 悬浮丁达尔光束（suspended Tyndall beam）、脚步扬起（footstep kick-up）、沉降飘落（settling drift） |

---

## 快门角度情绪映射表（Shutter Angle Emotion Mapping）

快门角度是摄影机的物理参数，控制每帧曝光时间占帧间隔的比例。在 AI 视频生成中，模型可能不直接理解技术参数，**必须**用视觉翻译作为双保险。

> **有效性：⚠️ 部分有效** — 快门角度在部分场景有效，建议配合视觉描述兜底。

| 快门角度 | 物理含义 | 视觉效果 | 情绪映射 | 提示词写法（双保险） | 有效性 |
|---|---|---|---|---|---|
| **45°** | 极短曝光（1/8 帧周期） | 每帧几乎无运动模糊，动作呈现逐帧跳跃的碎裂感 | 紧张、恐惧、抽搐、生理痛觉、碎裂感、噩梦 | `45°窄快门（Narrow Shutter Angle）——画面呈现逐帧跳跃的碎裂感（staccato fragmentation），每个微动作都有锐利的抽搐感，强化生理痛觉` | ⚠️ |
| **90°** | 短曝光（1/4 帧周期） | 运动轨迹有轻微拖影但主体仍保持锐利 | 压迫、动态、不安、能量蓄积 | `90°快门——运动轨迹带轻微拖影（slight motion trail）但主体依然锐利，画面充满压迫性的动态感（oppressive dynamism）` | ⚠️ |
| **180°** | 标准曝光（1/2 帧周期） | 自然的运动模糊，最接近人眼感知 | 凝重、日常、流畅、自然、沉静 | `180°标准快门（Standard Shutter）——自然的运动模糊（natural motion blur），画面流畅沉稳，接近人眼感知的真实感` | ⚠️ |
| **360°** | 全帧曝光 | 极度柔滑的拖影，所有运动都带长残影 | 梦幻、回忆、超现实、迷离、恍惚 | `360°全曝光快门（Full-frame Exposure Shutter）——所有运动都留下柔和的长拖影（soft long trail），画面如梦境般迷离恍惚（dreamlike haze）` | ⚠️ |

### 快门角度递进策略（Shutter Angle Progression Strategies）

在时间片分镜中，快门角度可以随情绪递进而变化：

```
递进模式 A：恐惧→倔强（从碎裂到凝重）
45° → 90° → 180°
适用：角色从被动受虐到主动反抗的情绪弧线

递进模式 B：平静→爆发→收束
180° → 45° → 180°
适用：日常场景中突发事件打破平衡再恢复

递进模式 C：现实→回忆→现实
180° → 360° → 180°
适用：闪回/梦境插入
```

---

## 渲染风格锚定词库（Rendering Style Anchors）

渲染风格术语作为视觉风格的「锚定词（Anchor Words）」，帮助模型定位整体美学方向。注意：这些术语不会像真实渲染引擎那样精确执行，但能有效影响生成方向。**必须**搭配视觉翻译使用。

### 超写实/CGI 渲染（Hyperrealistic / CGI Rendering）

> 以下术语标记为 💡 风格锚定——作为整体美学方向引导，非精确渲染参数。

| 锚定词 | 视觉翻译（双保险） | 适用场景 | 有效性 |
|---|---|---|---|
| **UE5 超写实（UE5 Hyperrealistic）** 💡 | 游戏引擎级超写实渲染，皮肤有真实的毛孔纹理和次表面散射（Subsurface Scattering），金属反射环境光，阴影边缘锐利但暗部不死黑 | 科幻、奇幻、产品展示 | 💡 |
| **Lumen 全局光照（Lumen Global Illumination）** 💡 | 光线在空间中自然反弹，室内角落有柔和的环境光补充，不会出现死黑区域，间接光照颜色会染到附近表面 | 室内场景、复杂光照环境 | 💡 |
| **PBR 材质（PBR / Physically Based Rendering Materials）** 💡 | 物理准确渲染——金属真的像金属、石头真的像石头、布料有真实的纤维质感和褶皱规律 | 需要材质可信度的场景 | 💡 |
| **8K 贴图（8K Texture Mapping）** 💡 | 极致细节——皮肤毛孔清晰可见，布料编织纹理可辨，石材风化痕迹历历在目 | 极特写/微距场景 | 💡 |
| **光线追踪（Ray Tracing）** 💡 | 真实光线追踪——玻璃折射准确，水面反射清晰，金属高光锐利，全局阴影柔和 | 有玻璃/水面/金属的场景 | 💡 |

### 摄影机美学（Camera Aesthetics）

> 以下术语标记为 ✅ 实测有效——社区测试验证对整体画面质感有明显影响。

| 锚定词 | 视觉翻译（双保险） | 适用场景 | 有效性 |
|---|---|---|---|
| **ARRI Alexa 35 美学（ARRI Alexa 35 Aesthetic）** ✅ | 电影级数字摄影机画质——肤色还原自然，动态范围极宽，暗部噪点极低，画面有「电影感」的厚重质地 | 所有需要电影质感的场景 | ✅ |
| **35mm 胶片质感（35mm Film Quality）** ✅ | 有机颗粒感，高光有柔和的溢出（halation），暗部有轻微的颗粒噪点，色彩有化学染色的温暖感 | 文艺片/复古/怀旧 | ✅ |
| **胶片颗粒感（Film Grain Texture）** ✅ | 化学胶片特有的有机颗粒纹理，赋予画面温暖的模拟质感 | 所有需要胶片感的场景 | ✅ |
| **变形宽银幕美学（Anamorphic Aesthetic）** ✅ | 横向椭圆形散景光斑，画面边缘有轻微拉伸畸变，水平光晕（lens flare），宽银幕视野 | 史诗/科幻/艺术片 | ✅ |

### 风格化渲染（Stylized Rendering）

| 锚定词 | 视觉翻译（双保险） | 适用场景 | 有效性 |
|---|---|---|---|
| **赛璐璐渲染（Cel-shading / Toon Rendering）** | 日本动画式平涂着色，色块之间有清晰的硬边轮廓线，阴影是纯色块而非渐变 | 二次元/动画风格 | ✅ |
| **次表面散射（SSS / Subsurface Scattering）** | 光线穿透皮肤表面后在内部散射，使皮肤呈现温暖的半透明质感，耳朵边缘透光泛红 | 人物特写、角色肖像 | ✅ |
| **色调映射（Tone Mapping）** | 高动态范围画面被压缩到可显示范围，亮部不死白暗部不死黑，保留最大细节 | 大光比场景 | ✅ |
| **色彩分级（Color Grading）** | 电影级色彩调整——暗部偏青、高光偏暖、中间调饱和度精确控制 | 所有电影感场景 | ✅ |

### 物理摄影机模拟（Physical Camera Simulation）

| 锚定词 | 视觉翻译（双保险） | 适用场景 | 有效性 |
|---|---|---|---|
| **ARRI Alexa 35 摄影机（ARRI Alexa 35 Camera）** ✅ | 电影级数字摄影机画质——肤色还原自然，动态范围极宽，暗部噪点极低，画面有「电影感」的厚重质地 | 所有需要电影质感的场景 | ✅ |
| **RED V-Raptor 摄影机（RED V-Raptor Camera）** ✅ | 8K 超高分辨率摄影机——极致锐利，细节纤毫毕现，适合大画幅后期裁切 | 需要极致细节的场景 | ✅ |
| **胶片质感模拟（Film Texture Simulation）** ✅ | 有机颗粒感，高光有柔和的溢出（halation），暗部有轻微的颗粒噪点，色彩有化学染色的温暖感 | 文艺片/复古/怀旧 | ✅ |
| **变形宽银幕模拟（Anamorphic Widescreen Simulation）** ✅ | 横向椭圆形散景光斑，画面边缘有轻微拉伸畸变，水平光晕（lens flare），宽银幕视野 | 史诗/科幻/艺术片 | ✅ |

---

## 情绪锚点关键词速查表（Emotion Anchor Keywords Quick Reference）

每个时间片必须配一个两词情绪锚点，作为语义锚帮助模型锁定情绪基调。以下是常用组合：

| 情绪弧线（Emotion Arc） | 时间片 1（Slice 1） | 时间片 2（Slice 2） | 时间片 3（Slice 3） |
|---|---|---|---|
| 恐惧→反抗（Fear → Rebellion） | 恐惧·挣扎（Fear · Struggle） | 偏执·倔强（Obsession · Stubbornness） | 决绝·爆发（Resolve · Eruption） |
| 平静→崩溃（Calm → Breakdown） | 宁静·空洞（Serenity · Emptiness） | 裂痕·不安（Fracture · Unease） | 崩塌·绝望（Collapse · Despair） |
| 压抑→释放（Suppression → Release） | 隐忍·克制（Endurance · Restraint） | 裂隙·涌动（Rift · Surge） | 宣泄·释然（Catharsis · Relief） |
| 迷茫→觉醒（Confusion → Awakening） | 迷失·游移（Lost · Wandering） | 触动·聚焦（Touched · Focus） | 觉醒·坚定（Awakening · Determination） |
| 爱→失去（Love → Loss） | 温柔·眷恋（Tenderness · Attachment） | 撕裂·不舍（Torn · Reluctance） | 空洞·接受（Hollow · Acceptance） |
| 紧张→舒缓（Tension → Relief） | 紧绷·警觉（Tense · Alert） | 对峙·蓄力（Confrontation · Charging） | 释然·平静（Relief · Calm） |
| 孤独→连接（Loneliness → Connection） | 疏离·封闭（Alienation · Closure） | 试探·犹疑（Probing · Hesitation） | 敞开·温暖（Openness · Warmth） |

**使用方式**：放在时间片标题中，如 `🎬 0-6s（情绪锚点：恐惧·挣扎 / Fear · Struggle）`
