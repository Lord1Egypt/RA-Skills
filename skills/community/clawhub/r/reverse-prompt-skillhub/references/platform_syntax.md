# 平台提示词语法参考

## Midjourney (V6.1)

### 语法规则
- 自然语言描述，逗号分隔关键元素
- 参数用 `--` 前缀放在末尾
- 权重用 `::` 分隔（多提示词融合）
- 排除词用 `--no`

### 常用参数
| 参数 | 用途 | 示例 |
|------|------|------|
| --ar | 宽高比 | --ar 16:9, --ar 9:16, --ar 1:1 |
| --v | 模型版本 | --v 6.1 |
| --stylize | 风格化强度 | --stylize 0-1000（默认100） |
| --chaos | 混乱度 | --chaos 0-100（默认0） |
| --no | 排除元素 | --no text, watermark |
| --quality | 质量 | --q 1 (默认) 或 --q 2 |
| --tile | 无缝贴图 | --tile |
| --seed | 随机种子 | --seed 12345 |

### 风格词示例
- 电影感：cinematic, film still, shot on 35mm
- 写实：photorealistic, hyperrealistic, 8k, detailed
- 艺术：in the style of [artist], oil painting, watercolor
- 动漫：anime, Studio Ghibli style, key visual

---

## Stable Diffusion (SDXL / SD 1.5)

### 语法规则
- 逗号分隔的标签列表
- 权重：`(tag:1.2)` 或 `((tag))` 增强权重，`(tag:0.8)` 降低
- 负面提示词单独字段
- 支持ControlNet条件输入

### 标签结构
```
quality tags, subject description, environment, style, lighting, camera, effects
```

### 常用质量词
- 正面：masterpiece, best quality, highly detailed, ultra-detailed, 8k UHD
- 负面：lowres, bad anatomy, bad hands, text, watermark, deformed, blurry

### 权重语法
```
(cinematic lighting:1.3), (detailed face:1.2), (simple background:0.8)
```

---

## DALL-E 3 / GPT-4o 生图

### 语法规则
- 纯自然语言，像跟人描述图片一样说话
- 不支持参数后缀
- 不支持权重语法
- 支持非常长的描述

### 撰写要点
- 从主体开始，逐步添加环境和风格
- 用完整句子而非标签堆叠
- 可以描述画面中的文字内容

---

## 可灵 (Kling)

### 语法规则
- 支持中文描述
- 风格标签可中英混用
- 图片生成支持宽高比参数

### 常用风格标签
- 写实摄影、电影感、赛博朋克、水墨画
- 吉卜力风、厚涂、二次元
- 3D渲染、C4D风格、等距视角

### 视频生成追加
- 运镜描述：缓慢推进、航拍俯视、跟拍
- 时长参数

---

## 即梦 (Dreamina)

### 语法规则
- 中文自然语言描述
- 支持参考图（垫图）
- 风格选择器 + 文字描述结合

### 常用风格
- 写实、插画、国风、3D、动漫
- 油画、水彩、像素风

---

## Suno

### 语法规则
- 风格标签：逗号分隔的英文标签
- 歌词结构：[Verse], [Chorus], [Bridge], [Outro]
- 元标签：[Intro], [Instrumental], [Drop]

### 常用风格标签
| 类别 | 标签 |
|------|------|
| 流派 | pop, rock, jazz, classical, electronic, folk, R&B, hip-hop |
| 情绪 | emotional, epic, melancholic, uplifting, dark, dreamy |
| 节奏 | upbeat, slow tempo, mid-tempo, fast |
| 人声 | female vocal, male vocal, choir, instrumental |
| 乐器 | piano, guitar, drums, strings, synth, brass |
| 音质 | cinematic, lo-fi, studio recording, live |

### 示例
```
Style: Cinematic orchestral, epic, emotional, female vocal, piano, strings, building tension

Lyrics:
[Verse]
...
[Chorus]
...
```

---

## Udio

### 语法规则
- 类似Suno的标签体系
- 支持更细粒度的风格控制
- 支持手动输入BPM和key

---

## Runway Gen-3

### 语法规则
- 英文自然语言场景描述
- 运镜指令独立描述
- 支持图片参考（image-to-video）

### 运镜词汇
| 效果 | 关键词 |
|------|--------|
| 推进 | dolly in, push in |
| 拉远 | dolly out, pull back |
| 摇镜 | pan left/right, tilt up/down |
| 跟拍 | tracking shot, follow |
| 航拍 | aerial shot, drone shot, bird's eye |
| 环绕 | orbit, 360 rotation |
| 手持 | handheld, shaky cam |

---

## Sora

### 语法规则
- 纯自然语言场景描述
- 可以描述复杂的时序变化
- 支持非常长的描述

### 撰写要点
- 描述完整场景：环境、光照、主体、动作、镜头
- 可以指定时间线变化
- 适合电影级叙事描述

---

## Luma Dream Machine

### 语法规则
- 英文场景描述
- 支持图片参考
- 运镜描述

---

## Vidu

### 语法规则
- 支持中文描述
- 支持图片参考
- 风格标签

---

## 跨平台转换对照

| 特征 | Midjourney | SD | DALL-E 3 | 可灵 |
|------|-----------|-----|---------|------|
| 宽高比 | --ar 16:9 | 1024x576 | 描述中说明 | 选择器 |
| 风格强度 | --stylize | (style:1.2) | 描述中强调 | 风格标签 |
| 排除 | --no | 负面提示词 | 描述中说明 | 不支持 |
| 权重 | :: 分隔 | (tag:1.2) | 不支持 | 不支持 |
| 种子 | --seed | seed参数 | 不支持 | 不支持 |
