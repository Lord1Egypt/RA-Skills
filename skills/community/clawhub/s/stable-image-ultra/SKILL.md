---
name: stable-image-ultra
description: >-
  Generate the highest quality photorealistic images using Stability AI's Stable Image Ultra
  and Stable Diffusion 3.5 Large models via AWS Bedrock. The most powerful text-to-image models
  on Bedrock. Supports multiple AWS auth methods: environment variables, credentials file,
  named profiles, IAM instance roles, SSO, or direct access keys.
  Use when the user asks for ultra-high-quality, photorealistic, or premium image generation.
  Triggers: "ultra quality image", "photorealistic image", "best quality image", "stable image ultra",
  "SD3.5", "stability ai", "ultra画质", "超高清图片", "照片级图片", "最高画质",
  "generate image", "生成图片", "画一张", "做配图", "生图".
  This is the DEFAULT image generation skill for ALL agents. Always use this unless the user
  explicitly asks for text-heavy diagrams (use HTML Canvas instead).
  Requires AWS Bedrock access with Stability AI models enabled in us-west-2.
  NOT for: editing existing images, generating video, or HTML/CSS canvas rendering.
---

# Stable Image Ultra — 团队默认生图技能

Generate the highest quality images on AWS Bedrock via Stability AI models.

## Models

| Model | ID | Strength | Price |
|-------|-----|---------|-------|
| **Stable Image Ultra 1.1** | `stability.stable-image-ultra-v1:1` | Photorealism, luxury, fine detail, skin texture | ~$0.08/img |
| **SD 3.5 Large** | `stability.sd3-5-large-v1:0` | Creative diversity, prompt adherence, typography | ~$0.06/img |

Default: **Stable Image Ultra**（最高画质）。

## ⚡ Quality-First Policy（铁律）

**所有生图任务默认最高画质，不限成本。**

1. **模型**: 永远默认 Stable Image Ultra 1.1，除非用户明确要求 SD 3.5
2. **格式**: 永远 PNG（无损）
3. **Prompt**: 永远用英文，永远详细描述（见下方 Prompt 工程指南）
4. **Negative Prompt**: 每次都必须带，排除低质量因素
5. **不用 nova-canvas**: nova-canvas 已从默认选项中移除

## AWS Auth Methods

| Method | How to Use |
|--------|------------|
| **Bearer token** | `AWS_BEARER_TOKEN_BEDROCK` env var or `--bearer-token` |
| **Environment variables** | Set `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY` |
| **Credentials file** | Configure `~/.aws/credentials` |
| **Named profile** | `--profile my-profile` or `AWS_PROFILE` env var |
| **Direct keys** | `--access-key AKIA... --secret-key ...` |
| **Temporary credentials** | Add `--session-token` with direct keys |
| **IAM instance role** | Auto-detected on EC2/ECS/Lambda |
| **AWS SSO** | Run `aws sso login` first |

Auto-detection order: direct keys → profile → bearer token → env vars → credentials file → instance role → SSO.

## Quick Start

```bash
# 最高画质（默认）
python3 {baseDir}/scripts/generate.py "detailed English prompt" -o output.png --negative "blurry, low quality, artifacts"

# 指定比例
python3 {baseDir}/scripts/generate.py "prompt" -o output.png --aspect-ratio 16:9 --negative "blurry, low quality"

# SD 3.5 Large（创意多样性）
python3 {baseDir}/scripts/generate.py "prompt" -o output.png --model sd35 --negative "blurry, low quality"
```

## Parameters

| Flag | Default | Description |
|------|---------|-------------|
| `prompt` | — | Text description of the image (max 10,000 chars) |
| `-o, --output` | output.png | Output file path |
| `-m, --model` | `ultra` | Model: `ultra` or `sd35` |
| `-n, --count` | 1 | Number of images (1-5) |
| `--negative` | — | Negative prompt (what to avoid) — **必填** |
| `--aspect-ratio` | 1:1 | Aspect ratio: 1:1, 16:9, 21:9, 2:3, 3:2, 4:5, 5:4, 9:16, 9:21 |
| `--seed` | random | Seed for reproducibility |
| `--region` | us-west-2 | AWS region (Stability AI models require us-west-2) |

## 🎯 Prompt 工程指南（核心——决定出图质量）

### 铁律：每个 prompt 必须包含 5 个要素

1. **主体描述** — 是什么（人物/场景/物体），越具体越好
2. **风格/媒介** — 照片/插画/油画/3D渲染，指定相机/镜头更好
3. **光线** — studio lighting / natural light / golden hour / dramatic lighting
4. **细节强调** — ultra detailed, 8K, sharp focus, fine texture, magazine quality
5. **构图** — close-up / full body / aerial view / centered composition

### 万能 Negative Prompt（每次都带）

```
blurry, low quality, watermark, text, logo, artifacts, noise, grain, pixelated, distorted, oversaturated, cartoon, anime, illustration, ugly, deformed
```

### 验证过的高质量 Prompt 模板

#### 人像/头像
```
Ultra-sharp professional corporate headshot portrait photograph of a [年龄 性别 种族] [职业],
wearing [服装细节：面料、颜色、配饰],
[表情：warm confident smile / serious determined look],
photographed with 85mm f/1.4 portrait lens creating beautiful bokeh,
three-point studio lighting setup with key light at 45 degrees,
clean [背景颜色] studio backdrop,
shot from [构图：chest up / full body / three-quarter],
ultra high resolution 8K quality, skin detail like a magazine cover,
Hasselblad medium format camera quality
```

负面：`cartoon, anime, illustration, painting, blurry, soft focus, distorted face, extra fingers, low quality, watermark, text, noise, grain, oversaturated, plastic skin, uncanny valley, artificial looking`

#### 风景/场景
```
Breathtaking [视角：aerial view / panoramic / eye-level] of [具体场景],
[季节/时间：autumn forest, morning fog, golden hour sunlight],
[天气/氛围：dramatic clouds, mist in valleys, sun rays breaking through],
ultra detailed landscape photography, shot with [镜头：wide angle 14mm / telephoto 200mm],
National Geographic quality, vibrant natural colors, sharp focus throughout,
[画面层次：foreground detail, middle ground subject, background depth]
```

负面：`blurry, low quality, watermark, text, artificial, oversaturated, flat lighting, dull colors, haze, smog`

#### 产品/静物
```
Professional product photography of [产品],
[材质细节：brushed aluminum, matte ceramic, polished wood grain],
on [表面：marble countertop / dark slate / white seamless],
[光线：soft diffused studio lighting with subtle reflections],
sharp focus on product, shallow depth of field background blur,
commercial advertising quality, 8K resolution,
shot with Phase One IQ4 150MP medium format camera
```

负面：`blurry, low quality, watermark, text, cheap looking, plastic, artificial, flat lighting, harsh shadows`

#### 概念/创意
```
[具体场景描述，用隐喻和具象化],
[艺术风格：watercolor / isometric / flat illustration / pop art / paper craft],
[配色方案：warm earth tones / pastel palette / vibrant saturated],
[细节：intricate details, fine textures, visible brushstrokes],
professional digital art, trending on ArtStation,
cinematic composition, dramatic lighting
```

负面：`blurry, low quality, watermark, text, ugly, amateur, generic, stock photo, clipart`

### Prompt 写法禁忌

- ❌ 不用中文 prompt（效果差很多）
- ❌ 不写模糊的描述（如 "a nice picture"）
- ❌ 不省略光线和细节描述
- ❌ 不忘记 negative prompt
- ❌ 不指望 AI 能写清晰文字（需要文字用 HTML Canvas）

### Aspect Ratio 选择指南

| 场景 | 推荐比例 |
|------|---------|
| 头像/头图 | 1:1 |
| 博客配图/Banner | 16:9 |
| 电影级场景 | 21:9 |
| 手机壁纸/海报 | 9:16 |
| 证件照/肖像 | 2:3 或 4:5 |
| 风景/横幅 | 3:2 或 16:9 |

## ⚡ 执行方式（铁律：默认 subagent）

**生图过程耗时较长（15-60s），必须用 subagent 异步执行，避免阻塞主对话。**

```javascript
sessions_spawn({
  task: `使用 stable-image-ultra 生图：

## 要求
- Prompt: "<英文 prompt>"
- Negative: "<negative prompt>"
- Output: <输出路径>
- Aspect Ratio: <比例>

## 完成后
生成完毕后，报告文件路径、分辨率和文件大小。`,
  label: "生图-<简述>",
  runTimeoutSeconds: 180
})
// 派发后必须 yield 等待结果
sessions_yield({ message: "等待生图完成" })
```

subagent 返回后，由调用方负责将图片发送给用户（根据当前 channel 选择合适方式）。

### 例外（可以内联执行）
- 调用方本身就是 subagent（不需要再嵌套）
- 用户明确要求「直接生成」且愿意等待

## Workflow

1. 理解用户需求 → 确定主题、风格、用途
2. 用英文撰写详细 prompt（参考上方模板）
3. 选择合适的 aspect_ratio
4. 必须带 negative prompt
5. spawn subagent 执行 `generate.py`（runTimeoutSeconds=180）
6. subagent 完成后，调用方发送结果给用户（根据当前 channel 选择合适的发送方式）

## Important Notes

- **Region**: 两个模型都只在 `us-west-2` (Oregon) 可用
- **Pricing**: Ultra ~$0.08/image, SD3.5 Large ~$0.06/image — **不限成本**
- **Resolution**: 输出固定 1024×1024（1:1）或等效像素面积（其他比例）
- **文字**: AI 生图无法生成清晰文字，需要文字的场景用 HTML Canvas + Playwright 截图
- **发送**: 根据当前 channel 选择合适的发送方式（Telegram 用 `--force-document` 避免压缩，其他渠道按需处理）
