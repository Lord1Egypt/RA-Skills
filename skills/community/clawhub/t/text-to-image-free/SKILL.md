---
name: text-to-image-free
description: >
  Free AI text-to-image generation.
  Turn text descriptions into images. No API key required.
  Supports multiple models via Pollinations.ai free API.
version: 1.3.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
        - python3
    emoji: "🎨"
    homepage: https://clawhub.ai/BusTes01/text-to-image-free
    models:
      - sana
      - flux
      - turbo
      - dreamshaper
---

# 🎨 Text-to-Image Free

A free AI image generation tool. User provides a text description, and the agent generates a corresponding image. **No API key required**, zero cost. Powered by Pollinations.ai free API.

## Usage

User says: "generate an image: a Shiba Inu on a beach drinking coconut water"

The agent performs the following workflow:

### Step 1: Extract Prompt

Extract the image description from user input.

Trigger keywords: "generate", "create an image", "draw", "make a picture"

### Step 2: Set Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| width | 1024 | Image width in px |
| height | 768 | Image height in px |
| model | `sana` | `sana` / `flux` / `turbo` / `dreamshaper` |
| nologo | true | Remove watermark |
| seed | random | Fixed integer for reproducible results |

User can override:
```
"Generate: cyberpunk Shanghai night view, width 1920 height 1080, use flux model"
"Generate another, use seed=42 for consistent style"
```

### Step 3: Call API

Use `exec` to run curl against Pollinations.ai:

```bash
PROMPT="<your text description>"
WIDTH=1024
HEIGHT=768
SEED=""  # optional: "42"

curl -s --max-time 180 \
  "https://image.pollinations.ai/prompt/$(python3 -c "import urllib.parse; print(urllib.parse.quote('$PROMPT'))")?width=$WIDTH&height=$HEIGHT&nologo=true${SEED:+&seed=$SEED}" \
  -o /tmp/generated_image.jpg
```

### Step 4: Return Result

Return the generated image file to the user.

## Model Selection

| Model | Features | Speed |
|-------|----------|-------|
| `sana` (default) | Latest efficient model, balanced style & detail | Fast |
| `flux` | Higher quality, richer detail | Moderate |
| `turbo` | Fastest generation, good for previews | Fastest |
| `dreamshaper` | Artistic / dream-like style | Medium |

> As of May 2026, Pollinations.ai default model has been switched to **Sana**. Older models like `stable-diffusion` are deprecated. Sana offers better speed-quality balance.

## Examples

```
User: "Generate: cyberpunk Shanghai night, neon lights, flying cars"
→ Agent calls API → returns image ✓

User: "Generate: an orange cat wearing an astronaut helmet, cartoon style, use flux model"
→ Agent calls API → returns image ✓
```

## Notes

- Free API has queue limits: one request at a time
- Generation takes ~15-60 seconds (Sana is faster than predecessors)
- English prompts yield best results
- Use `seed` parameter (e.g., `&seed=42`) for reproducible results
- Non-commercial use only (Pollinations.ai free tier limitation)

---

# 🎨 文生图（免费）

一个免费的AI图片生成工具。用户输入描述性文字，即可生成对应的图片。**无需任何API Key**，零成本使用。基于 Pollinations.ai 免费API。

## 使用方法

用户说："画一张图：一只柴犬在沙滩上喝椰子水"

Agent 执行以下流程：

### 第一步：提取提示词

从用户输入中提取图片描述文本。

关键词触发："画一张图"/"生成图片"/"画"/"create"/"generate"

### 第二步：调整参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| width | 1024 | 图片宽度 |
| height | 768 | 图片高度 |
| model | `sana` | `sana` / `flux` / `turbo` / `dreamshaper` |
| 无水印 | 是 | 默认去除水印 |
| seed | 随机 | 固定值可复现相同结果 |

用户可指定参数：
```
"画一张图：赛博朋克上海夜景，宽1920高1080，使用flux模型"
"再生成一次，用seed=42保持风格一致"
```

### 第三步：调用API

使用 `exec` 运行 curl 命令调用 Pollinations.ai：

```bash
PROMPT="<图片描述文字>"
WIDTH=1024
HEIGHT=768
SEED=""  # 可选："42"

curl -s --max-time 180 \
  "https://image.pollinations.ai/prompt/$(python3 -c "import urllib.parse; print(urllib.parse.quote('$PROMPT'))")?width=$WIDTH&height=$HEIGHT&nologo=true${SEED:+&seed=$SEED}" \
  -o /tmp/generated_image.jpg
```

### 第四步：返回结果

将生成的图片文件返回给用户。

## 模型选择

| 模型 | 特点 | 速度 |
|------|------|------|
| `sana`（默认） | 最新高效模型，通用风格，细节出色 | 快 |
| `flux` | 更高质量，细节丰富 | 稍慢 |
| `turbo` | 极速生成，适合快速预览 | 最快 |
| `dreamshaper` | 偏向艺术/梦幻风格 | 中等 |

> 2026年5月更新：Pollinations.ai 已将默认模型切换为 **Sana**，前代模型（如stable-diffusion）已下线。Sana在速度和画质间取得更好平衡。

## 示例

```
用户：「画一张图：赛博朋克上海夜景，霓虹灯，飞行汽车」
→ Agent 调用API → 返回图片 ✓

用户：「画一张图：一只橘猫戴着宇航员头盔，卡通风格，使用flux模型」
→ Agent 调用API → 返回图片 ✓
```

## 注意事项

- 免费API有队列限制，一次只能处理一个请求
- 生成时间约15-60秒（Sana模型较前代更快）
- 建议使用英文提示词获得最佳效果，中文也支持
- 支持 `seed` 参数（如 `&seed=42`）获得可复现结果
- 仅限非商业用途（Pollinations.ai免费层限制）
