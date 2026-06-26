---
name: qwen-image-edit
description: |
  千问图像生成与编辑助手。支持文生图、图像编辑（增删改元素 / 修改文字 / 风格迁移）、多图融合。擅长复杂中文文字渲染，可生成海报、封面、展板、宣传图等商用素材。触发词：生成图片、画图、做海报、P图、改图、修图、抠图、换背景、加文字、融合图片。

homepage: https://help.aliyun.com/zh/model-studio/text-to-image
---

# Qwen Image

  千问图像生成与编辑助手。支持文生图、图像编辑（增删改元素 / 修改文字 / 风格迁移）、多图融合。擅长复杂中文文字渲染，可生成海报、封面、展板、宣传图等商用素材。触发词：生成图片、画图、做海报、P图、改图、修图、抠图、换背景、加文字、融合图片。
Generate and edit images using Alibaba Cloud's Qwen Image API (千问图像).
  Qwen Image AI generation & editing assistant. Supports text-to-image, image editing (add/remove/change elements, modify text, style transfer), and multi-image fusion. Excels at complex Chinese text rendering, produces commercial assets like posters, covers, banners, and promotional graphics. Triggers: generate image, image editing, text-to-image, poster design, make a poster, photo editing, image fusion.

使用阿里云千问图像 API 生成与编辑图像。
  千问图像 AI 生成与编辑助手。支持文生图、图像编辑（增删改元素、修改文字、风格迁移）以及多图融合。擅长复杂中文文字渲染，可生成海报、封面、展板、宣传图等商用素材。触发词：生成图片、画图、做海报、P图、改图、修图、抠图、换背景、加文字、融合图片。



## Usage
## 用法

### Text-to-Image
### 文生图

Generate an image (returns URL only):
生成图像（仅返回 URL）：
```bash
python {baseDir}/scripts/generate_image.py --prompt "一只橘猫坐在窗台上晒太阳"
```

Generate and save locally:
生成并保存到本地：
```bash
python {baseDir}/scripts/generate_image.py --prompt "a beautiful sunset over mountains" --filename sunset.png
```

With custom size:
自定义尺寸生成：
```bash
python {baseDir}/scripts/generate_image.py --prompt "城市夜景" --size "2688*1536" --filename city.png
```

Generate multiple images:
生成多张图像：
```bash
python {baseDir}/scripts/generate_image.py --prompt "水彩风格的花卉" --n 4 --filename flower.png
```

### Image Editing
### 图像编辑

Single image editing:
单图编辑：
```bash
python {baseDir}/scripts/generate_image.py --images photo.png --prompt "在画面左下角加一只猫" --filename edited.png
```

Multi-image fusion (up to 3 images):
多图融合（最多 3 张图像）：
```bash
python {baseDir}/scripts/generate_image.py --images bg.png style.png --prompt "将图二的风格应用到图一" --filename fused.png
```

Edit with a URL input:
通过 URL 输入进行编辑：
```bash
python {baseDir}/scripts/generate_image.py --images https://example.com/photo.jpg --prompt "remove the text on the wall" --filename cleaned.png
```

Use dedicated edit model:
使用专用编辑模型：
```bash
python {baseDir}/scripts/generate_image.py --images input.png --prompt "把天空改成星空" -m qwen-image-edit-max --filename starry.png
```

## API Key
## API 密钥

Obtain the API key in the following order:
按以下优先级获取 API 密钥：

1. `--api-key` command line argument
2. `DASHSCOPE_API_KEY` environment variable
3. Get your API key from: https://dashscope.console.aliyun.com/

1. `--api-key` 命令行参数
2. `DASHSCOPE_API_KEY` 环境变量
3. 从以下地址获取 API 密钥：https://dashscope.console.aliyun.com/

## Models
## 模型

| Model | Mode | Description |
|---|---|---|
| `qwen-image-2.0-pro` | generate + edit (default) | Best text rendering & realism |
| `qwen-image-2.0` | generate + edit | Faster, balanced quality |
| `qwen-image-edit-max` | edit | Strongest editing: industrial design, geometry, character consistency |
| `qwen-image-edit-plus` | edit | Multi-output & custom resolution |
| `qwen-image-edit` | edit | Basic single-image editing |

| 模型 | 模式 | 说明 |
|---|---|---|
| `qwen-image-2.0-pro` | 生成 + 编辑（默认） | 最佳文字渲染与写实效果 |
| `qwen-image-2.0` | 生成 + 编辑 | 更快速，质量均衡 |
| `qwen-image-edit-max` | 编辑 | 最强编辑能力：工业设计、几何精度、角色一致性 |
| `qwen-image-edit-plus` | 编辑 | 多输出与自定义分辨率 |
| `qwen-image-edit` | 编辑 | 基础单图编辑 |

## Options
## 参数选项

**`--images` / `-i`** — Input image(s) for editing (1-3 local paths or URLs). Omit for text-to-image.
**`--images` / `-i`** — 用于编辑的输入图像（1-3 个本地路径或 URL）。文生图时无需指定。

**`--size` / `-s`** — Output resolution `WxH`. Omit to auto-match input image ratio.
**`--size` / `-s`** — 输出分辨率 `宽x高`。省略时自动匹配输入图像比例。
- qwen-image-2.0 series (512x512 ~ 2048x2048):
- qwen-image-2.0 系列（512x512 ~ 2048x2048）：
  - `2048*2048` — 1:1 (default when generating) / 1:1（生成时默认）
  - `2688*1536` — 16:9
  - `1536*2688` — 9:16
  - `2368*1728` — 4:3
  - `1728*2368` — 3:4
- Edit models (width & height each in [512, 2048]):
- 编辑模型（宽高各在 [512, 2048] 范围内）：
  - `1024*1024`, `1536*1024`, `1024*1536`, `1280*960`, `720*1280`, etc.

**`--n`** — Number of output images (1-6, default: 1). Not supported on `qwen-image-edit`.
**`--n`** — 输出图像数量（1-6，默认：1）。`qwen-image-edit` 模型不支持。

**`--negative-prompt` / `-n`** — Elements to avoid (default: common AI artifacts).
**`--negative-prompt` / `-n`** — 需要避免的元素（默认：常见 AI 伪影）。

**`--no-prompt-extend`** — Disable automatic prompt enhancement (enabled by default).
**`--no-prompt-extend`** — 禁用自动提示词增强（默认启用）。

**`--seed`** — Random seed [0, 2147483647] for reproducible results.
**`--seed`** — 随机种子 [0, 2147483647]，用于生成可复现的结果。

**`--watermark`** — Add "Qwen-Image" watermark to the output.
**`--watermark`** — 在输出图像上添加"Qwen-Image"水印。

**`--region`** — `beijing` (default) or `singapore`. Singapore requires `--workspace-id`.
**`--region`** — `beijing`（默认）或 `singapore`。新加坡区域需要 `--workspace-id`。

**`--no-verify-ssl`** — Disable SSL verification (use behind corporate proxy).
**`--no-verify-ssl`** — 禁用 SSL 验证（在企业代理网络后使用）。

## Workflow
## 工作流程

1. If the user provides images, pass them via `--images` (local paths or URLs).
2. Execute `generate_image.py` with the user's prompt and options.
3. Parse the output for lines starting with `MEDIA_URL:`.
4. Display each image using markdown: `![Generated Image](URL)`.
5. Do NOT download or save the image unless the user specifically requests it (use `--filename`).

1. 如果用户提供了图像，通过 `--images` 参数传入（本地路径或 URL）。
2. 使用用户的提示词和选项执行 `generate_image.py`。
3. 解析输出中以 `MEDIA_URL:` 开头的行。
4. 使用 markdown 格式展示每张图像：`![生成图像](URL)`。
5. 除非用户明确要求，否则不要下载或保存图像（使用 `--filename` 指定保存）。

## Notes
## 注意事项

- Supports both Chinese and English prompts.
- Image editing accepts local files (auto Base64-encoded, max 10MB) or URLs (http/https/oss).
- Output images are PNG format. Image URLs expire in 24 hours.
- `qwen-image-edit` model does not support `--size` or `--no-prompt-extend`.
- Default negative prompt helps avoid common AI artifacts (distorted limbs, low quality, etc.).
- Beijing and Singapore regions have independent API keys and endpoints — do not mix.

- 支持中英文提示词。
- 图像编辑支持本地文件（自动 Base64 编码，最大 10MB）或 URL（http/https/oss）。
- 输出图像为 PNG 格式。图像 URL 在 24 小时后过期。
- `qwen-image-edit` 模型不支持 `--size` 和 `--no-prompt-extend` 参数。
- 默认的反向提示词有助于避免常见 AI 伪影（肢体扭曲、低质量等）。
- 北京和新加坡区域拥有独立的 API 密钥和端点——请勿混用。
