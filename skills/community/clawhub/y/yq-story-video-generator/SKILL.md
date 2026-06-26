---
name: yq-story-video-generator
description: "从图片或文字描述自动生成完整视频故事。支持灵活输入（1-N张图片/纯文字/混合），可选时长和风格。关键词：故事视频、视频生成、图片转视频、文字转视频、story video、video generation"
version: 1.0.0
---

# 故事视频生成助手

## Overview

视频故事生成专家，从用户提供的图片或文字描述自动生成完整的视频故事。支持灵活输入（1-N张图片、纯文字、混合模式），可选时长和风格。完整流程包括：脚本生成 → 主体参考图 → 首帧图片 → 视频片段 → 背景音乐 → 最终合成。

## 交互规则

核心原则：内容简洁，不啰嗦

- 凡是有选项的问答，用 genui-form-wizard 展示
- 检测用户对话语言，所有输出跟随用户语言
- 展示选项时，只用用户语言，不要中英双语
- 提问/引导时只问必要的，克制的礼貌，禁止"您好"、"好的"、"我来帮您"

视频/文件输出规则：
- 生成的视频/文件必须用以下格式输出才能在对话中显示：
  ```
  <deliver_assets>
  <item>
  <path>视频或文件路径</path>
  </item>
  </deliver_assets>
  ```
- 每个文件一个 `<item>` 块，多个文件放在同一个 `<deliver_assets>` 内

## 输入模式

| 模式 | 输入 | 处理方式 |
|------|------|----------|
| 图片模式 | 1-N 张图片 | AI 自动识别角色，执行图片分析与脚本生成 |
| 文字模式 | 纯文字描述 | 执行文字转脚本生成 |
| 混合模式 | 图片 + 文字补充 | 图片为主，文字作为补充说明 |

**不再强制要求 3 张特定类型图片。**
- 用户扔 1 张图也能生成
- 用户只说一句话也能生成
- 用户不分类，AI 自动判断

## 可选参数

### 时长选项
用 genui-form-wizard 展示：
- 24秒（4段 x 6秒）— 短片
- 48秒（8段 x 6秒）— 标准（默认）
- 72秒（12段 x 6秒）— 长片

### 风格选项（纯文字模式时展示）
用 genui-form-wizard 展示：
- 吉卜力（温馨治愈）
- 赛博朋克（科幻未来）
- 写实（自然真实）
- 水彩（艺术手绘）
- 像素（复古游戏）
- 动漫（日式动画）
- 油画（古典艺术）
- 极简（简洁现代）
- AI 推荐（根据内容自动选择）

## 关键约束

| 参数 | 值 |
|------|-----|
| 每段时长 | 6秒（固定） |
| 视频分辨率 | 768P (统一) |
| 背景音乐 | 无歌词纯音乐，时长=视频总时长 |

### 默认参数

| 参数 | 默认值 |
|------|--------|
| segment_duration | 6 |
| default_duration | 48 |
| default_segments | 8 |
| video_resolution | "768P" |
| bgm_style | "instrumental, no vocals" |

## 环境依赖

本任务需要 FFmpeg。在执行前检查并安装：

```bash
# 检查 FFmpeg
if ! command -v ffmpeg &> /dev/null; then
  # 根据系统安装
  if [[ "$OSTYPE" == "darwin"* ]]; then
    brew install ffmpeg
  elif [[ -f /etc/debian_version ]]; then
    sudo apt-get update && sudo apt-get install -y ffmpeg
  elif [[ -f /etc/redhat-release ]]; then
    sudo yum install -y ffmpeg
  fi
fi
```

## 目录结构

```
output/
├── story_script.json       # 故事脚本
├── subject_reference.png   # 主体参考图（一致性锚点）
├── frames/                 # 首帧图片
├── videos/                 # 视频片段
├── bgm.mp3                 # 背景音乐
├── merged/                 # 合成中间文件
└── final_video.mp4         # 最终视频
```

## Workflow

### Step 0: 环境检查与收集输入
1. 检查 FFmpeg 是否可用，不可用则安装
2. 接收用户的图片/文字
3. 如果用户未指定时长，询问或使用默认 48 秒
4. 如果纯文字且未指定风格，展示风格选项

### Step 1: 生成故事脚本
根据输入模式选择：
- 有图片 → 执行 **图片分析与脚本生成**（参见下方详细说明）
- 纯文字 → 执行 **文字转脚本生成**（参见下方详细说明）
- 输出: `output/story_script.json`

### Step 1.5: 主体参考图生成
- 基于脚本的 `analysis.subject` 生成主体参考图
- 支持：人物/动物/物体/场景 等各类主体
- 作为后续所有帧的视觉一致性锚点
- 输出: `output/subject_reference.png`
- **【重要】此步骤是视觉一致性的关键**
- 详见下方「主体参考图生成」章节

### Step 2: 首帧图片生成（串联）
- 基于脚本的 visual_desc **串联**生成首帧图片
- 每帧使用：主体参考图 + 上一帧 作为双重参考
- **必须按顺序逐帧生成，不能并行**
- 输出: `output/frames/frame_01.png` - `frame_N.png`
- 详见下方「首帧图片生成」章节

### Step 3: 视频片段生成
- 从首帧图片生成视频片段
- 统一参数: duration=6, resolution=768P
- 输出: `output/videos/segment_01.mp4` - `segment_N.mp4`
- 详见下方「视频片段生成」章节

### Step 4: 背景音乐生成（可与 Step 3 并行）
- 根据故事情绪生成无歌词背景音乐
- 音乐时长 = 视频总时长
- 输出: `output/bgm.mp3`
- 详见下方「背景音乐生成」章节

### Step 5: 视频拼接与音乐合成
- 拼接所有视频片段
- 叠加背景音乐
- 输出: `output/final_video.mp4`
- 详见下方「视频拼接与音乐合成」章节

### 完成提示
所有步骤完成后，向用户报告：
- 最终视频路径
- 视频时长
- 使用的风格

使用 `<deliver_assets>` 格式输出最终视频。

## 执行原则

1. **输入灵活**: 1张图/N张图/纯文字/混合，都能处理
2. **全自动执行**: 确认输入后，自动完成全部步骤
3. **并行处理**: Step 3 和 Step 4 可并行
4. **错误重试**: 单个资源生成失败时自动重试一次

---

## 图片分析与脚本生成（Step 1 - 图片模式）

### 功能描述

使用 `images_understand` 工具分析用户提供的图片，自动识别每张图的角色（主体/场景/风格/混合），生成故事脚本。

### 输入要求

- 1-N 张图片（不限数量，不强制分类）
- 可选：用户的补充说明

### 执行步骤

#### 1. 创建输出目录

```bash
mkdir -p output/frames output/videos output/merged
```

#### 2. 分析图片并生成脚本

使用 `images_understand` 工具，传入以下 prompt：

```
你是一位资深分镜导演。请基于提供的图片创作一个由 {segment_count} 个镜头组成的连贯视频脚本。

【关键任务 0：图片角色识别】
首先分析每张图片，判断其角色：
- 主体图：包含明确的角色/物体/人物
- 场景图：以环境/背景为主
- 风格图：体现特定艺术风格/色调
- 混合图：同时包含多种元素

如果只有1张图，从中提取所有元素（主体+场景+风格）。
如果有多张图，综合分析它们的关系。

【关键任务 1：主体特征锁定】
从图片中提取主角的不少于3个核心视觉特征（如：毛色纹理、眼睛颜色、配饰、体型特征）。
**约束**：在生成的每一段 `visual_desc` 中，必须强制重复描述这些特征，防止角色长相漂移。
(错误示例: "猫跑了...")
(正确示例: "同一只棕色虎斑缅因猫（黄绿眼、耳尖黑毛）向右奔跑...")

【关键任务 2：视觉连续性设计】
- **动作衔接**: Segment N 的结尾动作必须为 Segment N+1 开头动作做铺垫。
- **环境渐变**: 场景切换时必须保留上一场景的元素作为锚点。
- **动作量化**: 必须明确动作的速度（慢/快）、方向（向左/向右/逼近镜头）和幅度。

【输出要求】
生成严格的JSON格式：

{
  "analysis": {
    "subject": "主体详细特征（必须非常具体，用于后续锁定）",
    "scene": "环境特征锚点",
    "style": "光影与画风定义",
    "image_roles": ["图1: 主体+场景", "图2: 风格", ...]
  },
  "story_script": [
    {
      "segment_id": 1,
      "visual_desc": "[镜头类型+风格定义] + [主体完整特征复述] + [具体的环境位置] + [量化的动作描述]。[光影描述]。"
    },
    ... (共 {segment_count} 段)
  ]
}

**特别指令**:
1. `visual_desc` 是给AI绘画模型看的，必须包含英文单词提示 (如: Cinematic shot, Ghibli style)。
2. 确保最后一段有完美的结局感。
3. 即使只有1张图，也要创作完整的故事弧线。
```

#### 3. 保存脚本

将生成的JSON保存到 `output/story_script.json`

### 不同图片数量的处理策略

| 图片数量 | 处理方式 |
|---------|----------|
| 1 张 | 从单图提取所有元素，AI 扩展场景变化 |
| 2 张 | AI 判断角色关系（如：主体+场景，或两个场景等） |
| 3 张 | 经典模式：尝试识别为主体/场景/风格 |
| 4+ 张 | 综合分析，可能作为故事的多个场景节点 |

### 脚本输出格式（图片模式）

```json
{
  "analysis": {
    "subject": "...",
    "scene": "...",
    "style": "...",
    "image_roles": ["..."]
  },
  "story_script": [
    {
      "segment_id": 1,
      "visual_desc": "..."
    }
  ],
  "input_mode": "image",
  "image_count": N
}
```

### 注意事项

1. **主体特征锁定**: visual_desc 中必须重复主体的核心特征
2. **动作连贯性**: 每段结尾要为下一段开头做铺垫
3. **英文提示词**: visual_desc 需包含英文风格提示词
4. **JSON格式**: 输出必须是有效的JSON格式
5. **灵活适配**: 不论图片数量，都要生成完整可用的脚本

---

## 文字转脚本生成（Step 1 - 文字模式）

### 功能描述

当用户只提供文字描述（无图片）时，使用 LLM 生成故事脚本，输出格式与图片模式完全一致。

### 输入要求

- 用户的故事描述/主题（必须）
- 风格选择（可选）：
  - 预设风格：吉卜力 / 赛博朋克 / 写实 / 水彩 / 像素 / 动漫 / 油画 / 极简
  - 自定义描述：用户自己描述的风格
  - 不指定：AI 根据主题推荐

### 执行步骤

#### 1. 创建输出目录

```bash
mkdir -p output/frames output/videos output/merged
```

#### 2. 确定风格

如果用户未指定风格，根据主题推荐：

| 主题类型 | 推荐风格 |
|---------|----------|
| 童话/奇幻 | 吉卜力、水彩 |
| 科幻/未来 | 赛博朋克、极简 |
| 日常/温馨 | 写实、动漫 |
| 冒险/动作 | 动漫、写实 |
| 自然/风景 | 油画、写实 |
| 复古/怀旧 | 像素、油画 |

#### 3. 生成脚本

使用 LLM 生成脚本，prompt：

```
你是一位资深分镜导演。请基于用户描述创作一个由 {segment_count} 个镜头组成的连贯视频脚本。

【用户描述】
{user_description}

【视觉风格】
{style_description}

【关键任务 1：主体设计与锁定】
首先，根据用户描述设计主角/主体的具体视觉形象，提取不少于3个核心视觉特征。
**约束**：在生成的每一段 `visual_desc` 中，必须强制重复描述这些特征，防止角色长相漂移。

【关键任务 2：视觉连续性设计】
- **动作衔接**: Segment N 的结尾动作必须为 Segment N+1 开头动作做铺垫。
- **环境渐变**: 场景切换时必须保留上一场景的元素作为锚点。
- **动作量化**: 必须明确动作的速度（慢/快）、方向（向左/向右/逼近镜头）和幅度。

【输出要求】
生成严格的JSON格式：

{
  "analysis": {
    "subject": "主体详细特征（必须非常具体，用于后续锁定）",
    "scene": "主要环境特征",
    "style": "{style_name} 风格：光影与画风定义"
  },
  "story_script": [
    {
      "segment_id": 1,
      "visual_desc": "[镜头类型+风格定义] + [主体完整特征复述] + [具体的环境位置] + [量化的动作描述]。[光影描述]。"
    },
    ... (共 {segment_count} 段)
  ]
}

**特别指令**:
1. `visual_desc` 是给AI绘画模型看的，必须包含英文单词提示。
2. 风格关键词必须出现在每段 visual_desc 中。
3. 确保最后一段有完美的结局感。
```

#### 4. 保存脚本

将生成的JSON保存到 `output/story_script.json`

### 脚本输出格式（文字模式）

```json
{
  "analysis": {
    "subject": "...",
    "scene": "...",
    "style": "..."
  },
  "story_script": [
    {
      "segment_id": 1,
      "visual_desc": "..."
    }
  ],
  "input_mode": "text",
  "style_used": "吉卜力"
}
```

### 注意事项

1. **主体一致性**: 即使没有图片，也要在首段设计具体的主体形象，后续段落严格复述
2. **风格锚定**: 每段 visual_desc 必须包含风格关键词
3. **JSON格式**: 输出必须是有效的JSON格式
4. **与图片模式兼容**: 输出格式完全一致，后续步骤可无缝衔接

---

## 主体参考图生成（Step 1.5）

### 功能描述

在首帧生成之前，先生成一张高质量的"主体参考图"，作为整个视频中视觉一致性的锚点。所有后续帧都会以这张参考图作为主体参考。

**支持的主体类型：**
- 人物角色（人类、动漫人物等）
- 动物角色（猫、狗、奇幻生物等）
- 物体/产品（汽车、建筑、道具等）
- 场景/地点（城市、森林、室内等）

### 输入要求

- `output/story_script.json` 中的 `analysis.subject`（主体特征描述）
- 可选：用户提供的主体参考图片

### 执行步骤

#### 1. 读取角色特征

从 `output/story_script.json` 读取 `analysis.subject`，提取角色的核心视觉特征。

#### 2. 判断主体类型

根据 `analysis.subject` 判断主体类型：

| 类型 | 判断依据 | 参考图特点 |
|------|---------|-----------|
| 人物/动物 | 描述中有生物特征 | 正面照，中性姿态 |
| 物体/产品 | 描述中有物品特征 | 3/4视角，展示细节 |
| 场景/地点 | 描述中以环境为主 | 全景或标准视角 |

#### 3. 构建参考图 Prompt

参考图的目的是生成一张**标准化的主体展示图**，便于后续帧参考。

**Prompt 结构：**
```
Character reference sheet, [角色详细特征描述],
front-facing view, neutral pose, centered composition,
clean background, studio lighting, high detail,
consistent character design, reference image for animation,
same character as will appear throughout the video,
stable face, preserve features, detailed facial features,
high quality, 8k resolution
```

**示例：**
```
Character reference sheet, a brown tabby Maine Coon cat with yellow-green eyes,
black ear tips, fluffy fur, medium build,
front-facing view, neutral pose, centered composition,
clean background, studio lighting, high detail,
consistent character design, reference image for animation,
same character as will appear throughout the video,
stable face, preserve features, detailed facial features,
high quality, 8k resolution
```

#### 4. 生成参考图

使用 `gen_images` 工具。

**有用户参考图模式：**
```json
{
  "prompt": "[参考图 prompt]",
  "output_file": "output/subject_reference.png",
  "reference_files": ["用户提供的参考图片"],
  "aspect_ratio": "1:1",
  "resolution": "2K"
}
```

**纯文字模式：**
```json
{
  "prompt": "[参考图 prompt，含风格关键词]",
  "output_file": "output/subject_reference.png",
  "aspect_ratio": "1:1",
  "resolution": "2K"
}
```

#### 5. 保存路径

参考图保存到 `output/subject_reference.png`

### 参考图规范

#### 人物/动物类
| 要素 | 要求 |
|------|------|
| 视角 | 正面（front-facing） |
| 姿态 | 中性站姿/坐姿 |
| 背景 | 干净简洁 |
| 光照 | 均匀工作室光照 |

#### 物体/产品类
| 要素 | 要求 |
|------|------|
| 视角 | 3/4视角，展示细节 |
| 背景 | 干净简洁 |
| 光照 | 产品摄影光照 |

#### 场景/地点类
| 要素 | 要求 |
|------|------|
| 视角 | 全景或标准建立镜头 |
| 构图 | 展示环境特征 |
| 光照 | 符合场景氛围 |

### 一致性关键词

根据主体类型选择合适的稳定性关键词：

**人物/动物：**
```
stable appearance, preserve features, consistent character design,
same character throughout, detailed features,
reference image for animation
```

**物体/产品：**
```
stable appearance, preserve details, consistent product design,
same object throughout, detailed features,
reference image for animation
```

**场景/地点：**
```
stable atmosphere, preserve environment style, consistent location design,
same environment throughout, detailed features,
reference image for animation
```

### 注意事项

1. **简洁背景**：参考图背景要干净，避免干扰主体特征提取
2. **合适视角**：根据主体类型选择最佳展示视角
3. **高细节**：主体细节要清晰，便于后续复现
4. **单主体**：一张参考图只包含一个主要主体
5. **多主体场景**：如果故事有多个主要主体，为每个主体生成独立参考图

---

## 首帧图片生成（Step 2）

### 功能描述

使用 `gen_images` 工具，基于故事脚本中的 visual_desc **串联生成**首帧图片。
- 每一帧都以**主体参考图**作为角色参考
- 同时以**上一帧**作为连续性参考
- 确保角色外观在整个视频中保持一致

### 角色一致性策略

```
主体参考图 ──────────────────────────────────────────────────┐
     │                                                      │
     ▼                                                      ▼
  frame_01 ──→ frame_02 ──→ frame_03 ──→ ... ──→ frame_N
              (上一帧)     (上一帧)            (上一帧)
```

**双重参考机制：**
1. **主体参考图**：保证主体视觉一致（角色/物体/场景特征）
2. **上一帧**：保证动作/构图/光照连续性

### 执行步骤

#### 1. 读取输入

- 从 `output/story_script.json` 读取 analysis 和 story_script
- 确认 `output/subject_reference.png` 存在

#### 2. 串联生成（逐帧）

**必须按顺序逐帧生成，不能并行：**

##### Frame 1（第一帧）
```json
{
  "prompt": "[visual_desc_1] + [一致性关键词]",
  "output_file": "output/frames/frame_01.png",
  "reference_files": ["output/subject_reference.png"],
  "aspect_ratio": "16:9",
  "resolution": "2K"
}
```

##### Frame 2-N（后续帧）
```json
{
  "prompt": "[visual_desc_N] + [一致性关键词]",
  "output_file": "output/frames/frame_0N.png",
  "reference_files": [
    "output/subject_reference.png",
    "output/frames/frame_0{N-1}.png"
  ],
  "aspect_ratio": "16:9",
  "resolution": "2K"
}
```

### Prompt 构建规则

每个 prompt 必须包含：

```
[风格描述: analysis.style].
[场景描述: analysis.scene].
[主体描述: analysis.subject].
[该段 visual_desc].
same subject as reference image, stable appearance, preserve features,
consistent design, consistent lighting style,
high quality, cinematic shot, detailed texture, 8k resolution.
```

**一致性关键词（根据主体类型选择）：**

人物/动物：
```
same character as reference image,
stable appearance, preserve features,
consistent character design,
same outfit as reference,
consistent lighting style
```

物体/产品：
```
same object as reference image,
stable appearance, preserve details,
consistent product design,
consistent lighting style
```

场景/地点：
```
same environment as reference image,
stable atmosphere, preserve style,
consistent location design,
consistent lighting style
```

### 参数要求

| 参数 | 值 | 说明 |
|------|-----|------|
| reference_files[0] | subject_reference.png | 主体参考图（必须） |
| reference_files[1] | 上一帧（frame 2+ 时） | 连续性参考 |
| aspect_ratio | "16:9" | 视频标准比例 |
| resolution | "2K" | 保证画质 |

### 生成顺序（严格执行）

```
1. 生成 frame_01（仅用主体参考图）
2. 等待 frame_01 完成
3. 生成 frame_02（用主体参考图 + frame_01）
4. 等待 frame_02 完成
5. 生成 frame_03（用主体参考图 + frame_02）
...
N. 生成 frame_N（用主体参考图 + frame_{N-1}）
```

**禁止并行生成**，必须等上一帧完成后再生成下一帧。

### 风格强化关键词

| 风格 | 强化关键词 |
|------|-----------|
| 吉卜力 | Ghibli style, soft lighting, hand-drawn animation, whimsical |
| 赛博朋克 | Cyberpunk, neon lights, futuristic city, dark atmosphere |
| 写实 | Photorealistic, natural lighting, detailed textures |
| 水彩 | Watercolor painting, soft edges, artistic, pastel colors |
| 像素 | Pixel art, 8-bit style, retro gaming aesthetic |
| 动漫 | Anime style, vibrant colors, expressive |
| 油画 | Oil painting style, rich textures, classical art |
| 极简 | Minimalist, clean lines, simple shapes |

### 注意事项

1. **串联生成**：必须按顺序逐帧生成，等上一帧完成后再生成下一帧
2. **双重参考**：每帧都用主体参考图 + 上一帧作为 reference
3. **主体锚定**：prompt 中必须包含一致性关键词（根据主体类型选择）
4. **比例锁定**：必须使用 16:9 比例
5. **特征复述**：prompt 中必须包含主体的完整特征描述

### 性能说明

由于串联生成，总耗时 = 单帧耗时 × 帧数。
这是保证角色一致性的必要代价，不可用并行替代。

---

## 视频片段生成（Step 3）

### 功能描述

使用 `gen_videos` 工具，从首帧图片生成视频片段。片段数量由 `story_script.json` 中的 segment_count 决定。

### 执行步骤

#### 1. 读取故事脚本

从 `output/story_script.json` 读取 story_script 数据，获取 segment_count。

#### 2. 调用 gen_videos 生成视频

由于 gen_videos 每次最多 5 个请求，需根据 segment_count 分批生成。

**分批策略：**
- 4 段 → 1 批
- 8 段 → 2 批（5 + 3）
- 12 段 → 3 批（5 + 5 + 2）

**请求格式：**
```json
{
  "video_requests": [
    {
      "prompt": "[该段的 visual_desc，添加动态描述]",
      "output_file": "output/videos/segment_01.mp4",
      "image_file": "output/frames/frame_01.png",
      "reference_type": "first_frame",
      "duration": 6,
      "resolution": "768P"
    }
  ]
}
```

### 参数要求（严格执行）

| 参数 | 值 | 说明 |
|------|-----|------|
| duration | 6 | 每段固定 6 秒 |
| resolution | "768P" | 统一分辨率 |
| reference_type | "first_frame" | 以首帧为起始 |

### 注意事项

1. **时长统一**: 所有视频必须是 6 秒
2. **分辨率统一**: 所有视频必须是 768P，确保拼接无缝
3. **分批生成**: gen_videos 每次最多 5 个，超过需分批
4. **动态描述**: prompt 中应添加动作相关描述增强视频动态效果
5. **数量灵活**: 根据 segment_count 生成对应数量，不写死

---

## 背景音乐生成（Step 4）

### 功能描述

使用音乐生成工具生成一首无歌词的背景音乐(BGM)，时长等于视频总时长。

### 执行步骤

#### 1. 分析故事情绪

从 `story_script.json` 的 `visual_desc` 中提取整体情绪基调：
- 温馨/治愈 → 轻柔钢琴、acoustic
- 冒险/动作 → 激昂管弦、epic orchestral
- 神秘/奇幻 → 空灵电子、ambient
- 欢快/童趣 → 活泼旋律、playful
- 史诗/宏大 → 交响乐、cinematic

#### 2. 构建音乐生成 prompt

```
[情绪基调] + [音乐类型] + instrumental, no vocals, no lyrics + [时长要求]
```

示例：
```
Warm and heartfelt acoustic guitar melody, gentle piano accompaniment,
cinematic film score style, emotional and touching,
instrumental only, no vocals, no lyrics,
suitable for storytelling video, 48 seconds duration
```

#### 3. 调用音乐生成工具

使用 `gen_music` 工具，参数：
- duration: 视频总时长（如 48 秒）
- style: instrumental / no vocals
- prompt: 基于情绪分析构建的 prompt

#### 4. 保存输出

保存到 `output/bgm.mp3`

### 音乐风格映射

| 视频类型 | 推荐音乐风格 |
|---------|-------------|
| 温馨故事 | soft piano, acoustic guitar, warm strings |
| 冒险动作 | epic orchestral, drums, brass |
| 童话奇幻 | magical bells, harp, ethereal synth |
| 日常治愈 | lo-fi, jazz piano, ambient |
| 史诗叙事 | cinematic orchestra, choir (humming) |
| 自然风景 | ambient, nature sounds, peaceful |

### 注意事项

1. **无歌词**: prompt 必须强调 instrumental, no vocals, no lyrics
2. **时长精确**: BGM 时长必须等于视频总时长
3. **情绪统一**: 音乐风格需与视频整体情绪匹配
4. **循环友好**: 如果时长较长，可考虑 loopable 风格

---

## 视频拼接与音乐合成（Step 5）

### 功能描述

使用 FFmpeg 将所有视频片段拼接成完整视频，再叠加背景音乐(BGM)，输出最终视频。

### 输入要求

- 视频片段: `output/videos/segment_01.mp4` - `segment_N.mp4`
- 背景音乐: `output/bgm.mp3`
- 片段数量从 `output/story_script.json` 获取

### 执行步骤

#### 步骤1: 获取片段数量

从 `output/story_script.json` 读取 segment_count，或扫描 `output/videos/` 目录获取实际片段数。

#### 步骤2: 统一视频分辨率

将每个视频片段强制缩放至统一分辨率 1280x720 (16:9)：

```bash
# 动态获取片段数量
segment_count=$(ls output/videos/segment_*.mp4 | wc -l)

for i in $(seq -w 1 $segment_count); do
  ffmpeg -y -i output/videos/segment_${i}.mp4 \
         -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2" \
         -c:v libx264 -preset fast -crf 23 \
         -an \
         output/merged/scaled_${i}.mp4
done
```

#### 步骤3: 创建拼接列表

```bash
rm -f output/merged/filelist.txt
for i in $(seq -w 1 $segment_count); do
  echo "file 'scaled_${i}.mp4'" >> output/merged/filelist.txt
done
```

#### 步骤4: 拼接视频（无音频）

```bash
ffmpeg -y -f concat -safe 0 -i output/merged/filelist.txt \
       -c copy output/merged/video_only.mp4
```

#### 步骤5: 叠加背景音乐

```bash
ffmpeg -y -i output/merged/video_only.mp4 \
       -i output/bgm.mp3 \
       -c:v copy -c:a aac \
       -map 0:v:0 -map 1:a:0 \
       -shortest \
       output/final_video.mp4
```

#### 步骤6: 验证输出

```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 output/final_video.mp4
```

预期输出 = segment_count x 6 秒（允许微小误差）。

### FFmpeg参数说明

| 参数 | 说明 |
|------|------|
| `-vf "scale=1280:720"` | 强制缩放至720p |
| `-c:v libx264` | 使用H.264编码 |
| `-an` | 移除音频轨道（步骤2） |
| `-f concat` | 使用concat模式拼接 |
| `-map 0:v:0` | 使用第一个输入的视频轨道 |
| `-map 1:a:0` | 使用第二个输入的音频轨道 |
| `-shortest` | 以较短的流为准 |

### 注意事项

1. **分辨率统一**: 使用scale滤镜确保所有片段为1280x720
2. **先拼后叠**: 先拼接视频，再叠加完整BGM，避免音频断裂
3. **BGM时长**: BGM应等于视频总时长，使用 -shortest 确保同步
4. **中间文件保留**: merged目录保留便于调试
5. **数量灵活**: 根据实际片段数量处理，不写死

---

## 工具依赖

| 工具 | 用途 | 使用步骤 |
|------|------|---------|
| `images_understand` | 分析用户图片 | Step 1（图片模式） |
| `gen_images` | 生成主体参考图和首帧图片 | Step 1.5, Step 2 |
| `gen_videos` | 从首帧生成视频片段 | Step 3 |
| `gen_music` | 生成背景音乐 | Step 4 |
| `terminal` | 执行 FFmpeg 命令 | Step 0, Step 5 |

## Common Mistakes to Avoid

1. **并行生成首帧**: 首帧必须串联生成，禁止并行，否则角色一致性无法保证
2. **遗漏主体特征复述**: 每段 visual_desc 必须重复主体核心特征，防止角色漂移
3. **忘记一致性关键词**: prompt 中必须包含对应主体类型的一致性关键词
4. **比例不一致**: 参考图 1:1，首帧 16:9，视频 768P，不可混用
5. **BGM有歌词**: 必须强调 instrumental, no vocals, no lyrics
6. **直接调用工具**: 禁止跳过脚本生成步骤直接生成图片/视频
7. **gen_videos 超限**: 每次最多 5 个请求，超过需分批
8. **跳过主体参考图**: Step 1.5 是视觉一致性的关键，不可跳过
9. **未创建输出目录**: 执行前必须 `mkdir -p output/frames output/videos output/merged`
10. **未检查 FFmpeg**: 拼接前必须确认 FFmpeg 可用
