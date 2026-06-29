# AI绘画提示词优化器 - 详细内容参考

## 艺术风格库

| 风格 | 关键词 | 特点 | 适用场景 |
|------|--------|------|---------|
| 真人写真 | photorealistic, 8k, detailed skin texture, raw photo | 接近照片的真实感 | 人物肖像、产品展示 |
| 证件照 | professional portrait, clean background, studio lighting | 专业证件照 | 简历、简历头像 |
| 动漫 | anime style, manga style, cel shading, anime screenshot | 日系动漫画风 | 头像、二次元内容 |
| 厚涂油画 | oil painting, impasto technique, detailed brushwork | 厚重的笔触感 | 艺术创作、人物画 |
| 水彩 | watercolor painting, soft edges, translucent washes | 水彩通透感 | 插画、封面 |
| 3D渲染 | 3d render, Pixar style, octane render, octane ray tracing | CGI质感 | 游戏素材、产品图 |
| 赛博朋克 | cyberpunk, neon lights, futuristic, holographic | 科技感霓虹 | 概念设计、头像 |
| 像素艺术 | pixel art, pixelated, 8-bit, pixel-style | 复古像素风 | 游戏素材、头像 |
| 水墨国风 | Chinese ink painting, sumi-e, traditional Chinese art | 国风水墨 | 古风内容、艺术 |
| 吉卜力 | Studio Ghibli style, Hayao Miyazaki, anime background | 吉卜力动画风 | 插画、风景 |
| 电影感 | cinematic lighting, film grain, movie still, film photography | 电影截图感 | 封面、概念图 |
| 蒸汽朋克 | steampunk, Victorian era, brass and copper, gears | 蒸汽机械风 | 概念设计 |
| 复古胶片 | vintage film, Kodak portra, analog photography | 复古胶片感 | 写真、人文 |
| 玻璃彩窗 | stained glass, cathedral window, light through glass | 玻璃彩窗效果 | 艺术、头像 |
| 浮世绘 | ukiyo-e, Japanese woodblock print style | 日本浮世绘 | 艺术、插画 |

## 构图设计

### 景别体系

| 景别 | 英文关键词 | 取景范围 | 适用场景 |
|------|-----------|---------|---------|
| 大特写 | extreme close-up, detail shot | 眼睛/嘴唇等局部 | 情绪表达、细节展示 |
| 特写 | close-up, face focus | 面部/头部 | 表情、人物头像 |
| 近景 | close-up portrait, bust | 头部到腰部 | 上半身、强调服装 |
| 中景 | medium shot, waist up | 腰部到膝盖 | 姿态、动作展示 |
| 中全景 | cowboy shot, 3/4 view | 大腿到头部 | 平衡人物与环境 |
| 全景 | full body shot, wide shot | 全身 | 完整姿态、场景 |
| 环境人像 | environmental portrait | 人物+背景 | 叙事、场景交代 |
| 远景 | long shot, establishing shot | 人物极小 | 场景展示、氛围 |

### 构图法则

| 法则 | 关键词 | 效果 | 适用场景 |
|------|--------|------|---------|
| 三分法 | rule of thirds | 平衡美感 | 通用构图 |
| 黄金分割 | golden ratio, golden spiral | 自然美感 | 人像、风光 |
| 对称构图 | symmetrical, centered, mirror | 庄重正式 | 建筑、正面人像 |
| 对角线 | diagonal, leading lines | 动感张力 | 动态场景 |
| 俯视 | bird's eye view, overhead | 全貌掌控 | 场景、桌面 |
| 仰视 | worm's eye view, low angle | 气势宏大 | 建筑、人物 |
| 框架构图 | frame within frame, doorway | 聚焦引导 | 叙事感 |
| 留白 | negative space, minimal | 简洁意境 | 艺术感、极简 |

## 氛围关键词库

### 光照类型

```
自然光 Natural:
- sunlight, golden hour, magic hour
- soft window light, diffused light
- overcast daylight, soft ambient
- moonlight, starlight

人造光 Artificial:
- studio light, soft box lighting
- neon lights, LED strips
- candle light, warm glow
- fairy lights, bokeh lights

特殊光 Special:
- rim light, backlight, edge lighting
- volumetric light, god rays
- dramatic chiaroscuro
- lens flare, light leaks
```

### 情绪氛围

| 情绪 | 光影关键词 | 色调关键词 | 示例场景 |
|------|-----------|-----------|---------|
| 温暖治愈 | warm sunlight, golden glow | warm tones, orange, amber | 阳光、咖啡、窗边 |
| 清新自然 | soft daylight, morning light | pastel colors, light palette | 户外、春天 |
| 神秘阴暗 | dramatic shadows, low key | dark tones, desaturated | 夜景、森林 |
| 浪漫唯美 | soft romantic light, candle | rose, pink, soft warm | 约会、求婚 |
| 冷酷科技 | cold blue light, harsh | blue, cyan, metallic | 科技、未来 |
| 复古怀旧 | vintage light, film grain | sepia, faded, warm | 回忆、胶片 |
| 梦幻飘渺 | ethereal glow, soft focus | pastel, luminous, glow | 仙境、幻想 |
| 激烈动感 | dramatic lighting, lens flare | high contrast, vivid | 动作、运动 |

## Midjourney 参数详解

### 参数速查表

| 参数 | 格式 | 可选值 | 说明 | 默认值 |
|------|------|--------|------|--------|
| --ar | --ar 16:9 | 1:1, 4:3, 16:9, 9:16, 3:2, 2:3, 5:4 | 宽高比 | 1:1 |
| --v | --v 6 | 5.2, 6, 6.1 | 版本号 | 6 |
| --s | --s 250 | 0-1000 | 风格化程度 | 250 |
| --q | --q 1 | 0.25, 0.5, 1, 2 | 质量(渲染时间) | 1 |
| --style | --style raw | raw, cute, expressive, scenic | 风格预设 | - |
| --stylize | --stylize 250 | 同--s | 风格化(完整写法) | - |
| --chaos | --chaos 20 | 0-100 | 结果变化度 | 0 |
| --weird | --weird 250 | 0-3000 | 古怪程度 | 0 |
| --tile | --tile | - | 生成无缝纹理 | - |
| --pan | --pan | - | 扩展画面 | - |
| --zoom | --zoom 2 | 1.5, 2 | 缩放 | - |
| --repeat | --repeat 4 | 1-40 | 生成数量 | 1 |

### 版本特性

```
V6 (最新):
- 更强的文字生成能力
- 更准确的prompt遵循
- 更真实的照片质感
- 支持 --style raw 获得更少风格化

V5.2:
- 更好的细节渲染
- 改进的美学评分
- --style参数支持

V6.1:
- 更快的生成速度
- 更强的连贯性
- 细节改进
```

### 组合示例

```
人物肖像：
a portrait of [描述] --ar 3:4 --v 6 --s 200 --style raw

全身像：
a full body shot of [描述] --ar 2:3 --v 6 --s 250

风景：
[场景描述], epic landscape --ar 16:9 --v 6 --s 100

动漫风：
[主体描述], anime style --ar 1:1 --v 6 --s 750

高细节：
[详细描述], 8k, highly detailed, masterpiece --ar 4:3 --v 6 --q 2
```

## Stable Diffusion 权重语法

### 基础权重

```
(关键词)       默认权重 1.1
(关键词:1.5)   正向增强 1.5倍
[关键词:0.7]   负向减弱 0.7倍
((关键词))     权重 1.1×1.1=1.21
(((关键词)))   权重 1.1³≈1.33

混合语法：
[关键词1|关键词2]  交替混合
(keyword1:0.7, keyword2:1.3)  逗号分隔不同权重
```

### Lora调用

```
<lora:名称:权重>
示例：
<lora:hanfu_v1:0.8>  调用权重0.8的汉服Lora
<lora:add_detail:1>   添加细节Lora

常用Lora标签：
<lora:detail:0.6>     增加细节
<lora:pose:0.7>       姿态控制
<lora:face:0.8>       脸部美化
```

### 常用提示词模板

```
正向必备：
(masterpiece:1.3), (best quality:1.2), (high quality:1.1), 
(ultra detailed:1.1), (absurdres:1.1), (8k:1.1), (detailed:1.1)

人物正向：
1girl, beautiful detailed face, detailed eyes, long flowing hair, 
perfect anatomy, detailed hands, detailed fingers, detailed skin

通用负向：
lowres, bad anatomy, bad hands, text, error, missing fingers, 
extra digit, fewer digits, cropped, worst quality, low quality, 
normal quality, jpeg artifacts, signature, watermark, username, 
blurry, deformed, ugly, disfigured, mutated

人物负向：
bad anatomy, bad proportions, bad hands, bad fingers, extra limbs, 
distorted face, deformed eyes, asymmetric eyes,萧手脚, missing limbs

风格负向：
low quality, blurry, pixelated, jpeg artifacts, watermark, logo
```

### 采样器推荐

| 采样器 | 特点 | 适用场景 |
|--------|------|---------|
| DPM++ 2M Karras | 平衡速度与质量 | 通用推荐 |
| DPM++ SDE Karras | 细节丰富 | 写实人物 |
| Euler a | 快速，适合动漫 | 动漫风格 |
| DDIM | 快速收敛 | 迭代优化 |
| PLMS | 稳定 | 标准输出 |
| Heun | 细节好，速度慢 | 高质量需求 |

## 完整示例库

### 示例1：电商产品图
```
用户：生成一个护肤品精华液的电商主图，白底，有光泽感

【提示词】
skincare serum bottle, transparent glass bottle with golden liquid inside, 
elegant pump cap, minimalist white background, soft studio lighting, 
product photography, high-end cosmetic packaging, subtle reflection, 
clean and pure atmosphere, 8k, professional photography, commercial 
product shot --ar 1:1 --v 6 --q 2

【变体 - 精华特写】
close-up of serum droplet, golden liquid, glass bottle, soft bokeh 
background, product photography, luxurious skincare, detailed texture 
--ar 1:1 --v 6 --s 100
```

### 示例2：游戏角色立绘
```
用户：画一个手持魔杖的法师女性，暗黑风格

【提示词】
dark fantasy female mage, flowing black robes with silver embroidery, 
holding ornate magical staff with glowing crystal, pointed wizard hat, 
mysterious dark eyes, ethereal dark magic aura, ancient stone ruins 
background, dramatic rim lighting, intricate details, dark and moody 
atmosphere, digital art, highly detailed --ar 2:3 --v 6 --s 400

【负向提示词】
cartoon, anime, bright colors, cheerful, happy, low quality, 
blurry, bad anatomy, extra limbs, deformed

【变体 - 全身立绘】
full body shot, dark sorceress, powerful stance, magical effects, 
floating runes, dark purple and blue magical energy, epic pose, 
detailed costume design --ar 2:3 --v 6 --s 300
```

### 示例3：建筑场景
```
用户：生成一个未来城市的概念图，科幻风格

【提示词】
futuristic cyberpunk cityscape, towering skyscrapers with holographic 
billboards, flying vehicles in the sky, neon-lit streets below, 
dystopian atmosphere, massive megastructure, concept art, wide angle 
view, cinematic composition, volumetric fog, dramatic lighting, 
sci-fi architecture, Blade Runner inspired --ar 16:9 --v 6 --s 500

【变体 - 城市夜景】
night view of futuristic metropolis, millions of lights, dense urban 
sprawl, aerial perspective, reflective wet streets, constant motion, 
urban density, technological civilization, epic scale --ar 16:9 --v 6
```

### 示例4：儿童插画
```
用户：画一个可爱的小兔子在森林里采蘑菇

【提示词】
cute cartoon bunny rabbit, wearing small red bow tie, holding tiny 
basket, picking colorful mushrooms in magical forest, soft green moss, 
dappled sunlight, children's book illustration style, kawaii, pastel 
colors, adorable expression, heartwarming scene --ar 4:3 --v 6 --s 600

【变体 - 简化可爱风】
chibi cute bunny, big sparkling eyes, tiny mushroom hat, happy smile, 
simple clean background, flat illustration style, pastel palette, 
sticker art style --ar 1:1 --v 6 --s 800
```

## 常见问题解决

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 手部畸形 | AI手部理解弱 | 添加"perfect hands"，使用负向"bad hands" |
| 多人失控 | 多人细节难控制 | 改为单人像，或详细描述每个人 |
| 风格偏离 | 描述不够具体 | 添加更多风格参考词 |
| 文字错误 | MJ文字能力有限 | 简单文字，--v 6改善 |
| 比例失调 | 人物身体比例怪 | 添加"perfect anatomy"、"normal proportions" |
| 画面模糊 | 细节不够/质量低 | 添加"8k, detailed"，使用--q 2 |
| 动漫不达标 | 风格不纯 | 添加明确风格词"anime screenshot, manga style" |

## 平台选择决策树

```
用户需求是什么？
├── 高质量写实照片/艺术
│   ├── 需要精细控制 → Stable Diffusion + ControlNet
│   ├── 追求最高质量 → Midjourney v6
│   └── 快速简单 → DALL-E 3
├── 动漫/二次元
│   ├── 需要风格一致性 → Stable Diffusion + LoRA
│   ├── 追求画面精美 → Midjourney + anime style
│   └── 需要批量 → Stable Diffusion
├── 概念设计/插画
│   ├── 电影感 → Midjourney
│   ├── 扁平插画 → DALL-E / Midjourney
│   └── 精细控制 → Stable Diffusion
└── 产品/电商图
    ├── 白底产品 → Midjourney + 抠图
    └── 场景产品 → Midjourney / SD
```
