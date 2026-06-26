---
name: yq-gif-sticker-generator
description: "Q版表情包生成器：将用户照片（人物、宠物、物品、Logo/Icon）转换为4个经典动作的Q版GIF动态表情包，带中文配文，支持在线展示和下载。关键词：表情包、sticker、GIF、Q版、动图"
version: 1.0.0
---

# Q版GIF动图表情包生成器

## Overview
将用户上传的一张照片（人物、宠物、物品、Logo/Icon）转换成一套包含4个经典动作、带有中文配文的高质量 GIF 表情包，并提供在线展示页面。整个流程分三步：静态图生成 → 动态视频生成 → GIF转换与交付。

## 4款经典表情包配置表

| 序号 | 动作 | 配文 | 文件名标识 |
|------|------|------|------------|
| 1 | 开心挥手 | 嗨~ | hi |
| 2 | 大笑捧腹 | 哈哈哈 | laugh |
| 3 | 哭泣流泪 | 呜呜呜 | cry |
| 4 | 比心爱心 | 爱你哦 | love |

## Workflow

### Step 1: 静态图生成与配文 (sticker-generator)

**目标**: 生成4张带有不同动作和中文配文的静态 Q 版图片。

#### 1.1 分析原图主体 (images_understand)
使用 `images_understand` 深度分析用户上传的照片，识别主体类型：
- **人物**: 提取面部特征、发型、服饰等
- **动物/宠物**: 提取品种、毛色、体型等
- **物品**: 提取形状、颜色、特征等
- **Icon/Logo**: 提取形状和配色，后续将其转化为保持原有形状和配色的 3D 玩具/公仔形象

#### 1.2 批量生成带字图片 (edit_images)
直接基于用户上传的照片，**并发**调用 `edit_images` 生成4张不同的图片。

**Prompt 策略：**
使用高质量的英文 Prompt，强调以下关键要素：
- **Pop Mart 盲盒风格 (Pop Mart style)**
- **3D 渲染 (C4D/Octane)**，高级质感
- **干净白色背景 (Clean white background)**
- **黑字白边 (Black text with white outline)**，确保清晰可读

```python
edit_images(
    image_edit_items=[
        {
            "prompt": "3D cute Q-version cartoon style, Pop Mart blind box style, chibi character, big head, waving happily, greeting warmly. Clean white background, minimalist, high quality 3D render, C4D, octane render. Text rendering: Clear, legible Chinese text '嗨~' written at the bottom. Text style: Black text with thick white outline, bold cute font, floating in front of the character. No spelling errors, no blur, sharp details.",
            "base_image_file": "<用户上传的图片>",
            "output_file": "imgs/sticker_01_hi.png"
        },
        {
            "prompt": "3D cute Q-version cartoon style, Pop Mart blind box style, chibi character, big head, laughing out loud, holding belly. Clean white background, minimalist, high quality 3D render, C4D, octane render. Text rendering: Clear, legible Chinese text '哈哈哈' written at the bottom. Text style: Black text with thick white outline, bold cute font, floating in front of the character. No spelling errors, no blur, sharp details.",
            "base_image_file": "<用户上传的图片>",
            "output_file": "imgs/sticker_02_laugh.png"
        },
        {
            "prompt": "3D cute Q-version cartoon style, Pop Mart blind box style, chibi character, big head, crying, tears flowing. Clean white background, minimalist, high quality 3D render, C4D, octane render. Text rendering: Clear, legible Chinese text '呜呜呜' written at the bottom. Text style: Black text with thick white outline, bold cute font, floating in front of the character. No spelling errors, no blur, sharp details.",
            "base_image_file": "<用户上传的图片>",
            "output_file": "imgs/sticker_03_cry.png"
        },
        {
            "prompt": "3D cute Q-version cartoon style, Pop Mart blind box style, chibi character, big head, making heart shape with hands, love hearts around. Clean white background, minimalist, high quality 3D render, C4D, octane render. Text rendering: Clear, legible Chinese text '爱你哦' written at the bottom. Text style: Black text with thick white outline, bold cute font, floating in front of the character. No spelling errors, no blur, sharp details.",
            "base_image_file": "<用户上传的图片>",
            "output_file": "imgs/sticker_04_love.png"
        }
    ]
)
```

**输出**: 4张带字图片路径：
- `imgs/sticker_01_hi.png`
- `imgs/sticker_02_laugh.png`
- `imgs/sticker_03_cry.png`
- `imgs/sticker_04_love.png`

---

### Step 2: 动态视频生成 (sticker-animator)

**目标**: 将4张静态图片转换为动态短视频。

#### 关键配置
- **并发执行**: 必须使用 `batch_image_to_video` 进行并发生成，严禁串行调用。
- **极速模式**: 视频时长强制限制为 **1秒** (duration=1)，仅生成关键动作，大幅减少等待时间。
- **文字保护**: Prompt 中需强调 **"保持文字清晰"**，防止视频生成过程中文字变形。

```python
batch_image_to_video(
    count=4,
    image_file_list=[
        "imgs/sticker_01_hi.png",
        "imgs/sticker_02_laugh.png",
        "imgs/sticker_03_cry.png",
        "imgs/sticker_04_love.png"
    ],
    output_file_list=[
        "videos/sticker_01_hi.mp4",
        "videos/sticker_02_laugh.mp4",
        "videos/sticker_03_cry.mp4",
        "videos/sticker_04_love.mp4"
    ],
    prompt_list=[
        "Q版卡通人物开心挥手，热情打招呼，动作夸张可爱，保持文字清晰，High Quality, 1s loop",
        "Q版卡通人物大笑捧腹，笑得前仰后合，保持文字清晰，High Quality, 1s loop",
        "Q版卡通人物哭泣流泪，擦眼泪，保持文字清晰，High Quality, 1s loop",
        "Q版卡通人物双手比心，发射爱心，保持文字清晰，High Quality, 1s loop"
    ],
    # 强制所有视频时长为 1秒，确保快速生成
    duration_list=[1, 1, 1, 1],
    resolution_list=["768P"] * 4
)
```

**输出**: 4个1秒短视频路径：
- `videos/sticker_01_hi.mp4`
- `videos/sticker_02_laugh.mp4`
- `videos/sticker_03_cry.mp4`
- `videos/sticker_04_love.mp4`

---

### Step 3: 格式转换与交付 (sticker-converter)

**目标**: 将视频转换为 GIF 动图并提供展示与下载。

#### 3.1 批量转换 MP4 → GIF (Bash)
调用 Python 转换脚本，将视频批量转换为 GIF。

```bash
python3 cookbook/script/convert_mp4_to_gif.py -i videos -o gifs --fps 10 --width 240
```

#### 3.2 生成 HTML 展示页 (Bash)
调用脚本生成包含所有 GIF 的 index.html 页面。

```bash
python3 cookbook/script/generate_html.py
```

#### 3.3 部署与交付 (deploy)
将生成的 GIF 和 HTML 页面打包部署，提供在线预览链接。

```python
deploy(
    dist_dir="gifs",
    project_name="my-q-stickers",
    project_type="Others"
)
```

#### 3.4 输出交付格式
直接在对话中返回一个包含 GIF 视窗路径的 Markdown 表格：

| 表情 | 配文 | GIF 路径 |
|------|------|----------|
| 开心挥手 | 嗨~ | gifs/sticker_01_hi.gif |
| 大笑捧腹 | 哈哈哈 | gifs/sticker_02_laugh.gif |
| 哭泣流泪 | 呜呜呜 | gifs/sticker_03_cry.gif |
| 比心爱心 | 爱你哦 | gifs/sticker_04_love.gif |

**必须包含以下提示文案**: "如果需要下载， 请点击表格里面的 GIF 路径， 到视窗的右上角进行下载"

---

## 主体识别与Q版化规则

### 人物
- 提取面部特征（脸型、发型、肤色、五官）、服饰特征
- Q版化时保留核心辨识度（发型、服装颜色等）

### 动物/宠物
- 提取品种、毛色、体型、标志性特征（如花纹、耳朵形状）
- Q版化时放大可爱特征（大眼睛、圆脸）

### 物品
- 提取形状、颜色、纹理
- Q版化时添加拟人化元素（表情、四肢）

### Icon/Logo (CRITICAL)
- **必须**将其转化为保持原有形状和配色的 3D 玩具/公仔形象
- 不可改变 Logo 的核心配色方案和基本形状
- 添加Q版五官和四肢进行拟人化

## 执行原则

1. **主体一致 (Subject Consistency)**: 无论是人像、宠物还是抽象的 Logo/Icon，必须准确识别并在 Q 版化中保留核心视觉特征（配色、形状）。
2. **一步到位**: 直接利用 AI 模型生成带字图片，使用英文 Prompt 确保准确率。
3. **并发生成**: 视频生成必须使用 `batch_image_to_video` 并发执行，严禁串行调用。
4. **完整交付**: 最终必须提供 GIF 格式的视窗路径表格，并附带强制的下载引导文案。

## 工具使用清单

| 步骤 | 工具 | 必须/可选 |
|------|------|-----------|
| 分析原图 | `images_understand` | 必须 |
| 生成静态图 | `edit_images` | 必须 |
| 生成视频 | `batch_image_to_video` | 必须 |
| 转换GIF | `bash` (python3 convert_mp4_to_gif.py) | 必须 |
| 生成展示页 | `bash` (python3 generate_html.py) | 必须 |
| 部署 | `deploy` | 必须 |

## 文件与输出约定

### 目录结构
```
├── imgs/
│   ├── sticker_01_hi.png
│   ├── sticker_02_laugh.png
│   ├── sticker_03_cry.png
│   └── sticker_04_love.png
├── videos/
│   ├── sticker_01_hi.mp4
│   ├── sticker_02_laugh.mp4
│   ├── sticker_03_cry.mp4
│   └── sticker_04_love.mp4
└── gifs/
    ├── sticker_01_hi.gif
    ├── sticker_02_laugh.gif
    ├── sticker_03_cry.gif
    └── sticker_04_love.gif
```

### 命名规则
- 文件名格式: `sticker_{序号}_{标识}.{ext}`
- 序号: 01-04
- 标识: hi, laugh, cry, love

## Common Mistakes to Avoid

1. **串行生成视频**: 必须使用 `batch_image_to_video` 并发生成，不要逐个调用。
2. **遗漏文字保护**: 视频生成 Prompt 必须包含 "保持文字清晰" / "Keep text clear and stable"。
3. **视频时长过长**: 强制使用 duration=1（1秒），不要使用更长时长。
4. **忘记下载引导**: 最终输出必须包含 "如果需要下载， 请点击表格里面的 GIF 路径， 到视窗的右上角进行下载"。
5. **Logo/Icon 处理错误**: Logo 类主体必须转化为3D玩具/公仔形象，保持原有形状和配色。
6. **使用中文 Prompt 生成图片**: 静态图生成必须使用英文 Prompt，中文仅出现在配文文字中。
7. **遗漏主体分析**: 必须先用 `images_understand` 分析原图，再进行生成。
