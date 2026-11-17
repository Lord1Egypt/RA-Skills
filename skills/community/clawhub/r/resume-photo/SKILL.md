---
name: resume-photo
description: "把生活照一键转为高端专业简历照/证件照：纯色背景、商务正装、柔光、标准尺寸。Use for 简历照、求职照、证件照、职业头像、resume photo, headshot, ID photo."
metadata: {"openclaw":{"emoji":"🪪","os":["darwin","linux"],"requires":{"bins":["python3"]}}}
homepage: https://clawhub.ai/skills/resume-photo
license: MIT
---

# Resume Photo · 简历照生成器

把用户提供的**生活照**转成**高端专业简历照**：保留五官与身份特征、自然微笑、纯色简约背景、商务正装、端正姿态、明亮干净、高清且**不过度美颜**。

## 前提条件（先检查，再动手）

需要一个**已配置凭证**且**支持参考图编辑**的图像生成 provider。最快判断：

```bash
bash {baseDir}/scripts/generate_resume_photo.sh --list
```

- 输出 `provider/model`（如 `google/gemini-3.1-flash-image`）→ 可用，继续。
- 输出 `NONE` → 停止并告知用户如何配置凭证；**绝不用文字假装已生成图片**。

### 模型优先级（脚本自动按此挑选）

| 优先级 | provider | 默认模型 | 说明 |
|--------|----------|----------|------|
| 1 | Google | `google/gemini-3.1-flash-image` | 人脸保真最好、编辑便宜 |
| 2 | OpenAI | `openai/gpt-image-2` | 画质最强（API key 或 Codex OAuth） |
| 3 | OpenRouter | `google/gemini-3.1-flash-image-preview` | 一个 key 走多模型 |
| 4 | fal | `fal-ai/nano-banana` 系列 | 便宜快 |
| 5 | xAI | `xai/grok-imagine-image` | 备选 |
| 6 | MiniMax | `minimax/image-01` | 备选 |

固定默认模型 / 配置回退：

```bash
openclaw models set-image google/gemini-3.1-flash-image
openclaw models image-fallbacks add openai/gpt-image-2
```

### 配置凭证（二者其一）

```bash
openclaw models auth paste-api-key   # OpenAI / Google / OpenRouter / fal 的 API key
openclaw models auth login           # 或用 ChatGPT/Codex 订阅 OAuth 登录
```

> **DeepSeek V4 不能生图。** DeepSeek 官方 API 全部模型的 `output_modalities` 均为 `["text"]`；`deepseek-flash` 只支持图片**输入**（读图），不产出图片。本 skill 里 LLM（含 DeepSeek V4）负责**撰写与审校提示词**，出图交给上面的图像模型。

## 主流程

### 1. 收集输入

需要：**原图路径**（用户上传的图片路径或 URL）。可选：性别/发型呈现、背景色、服装风格、尺寸规格、输出格式、生成张数。

- 用户未给路径 → 只问这一件事，其余用默认值。
- 默认值：背景浅蓝、白衬衫/浅色合体系西装、温和微笑、3:4 竖版、2K、JPEG、1 张。
- 完成判据：拿到本地存在的图片路径（或 URL），且各项参数已确定或取默认值。

### 2. 构造编辑提示词

按 [references/prompt-template.md](references/prompt-template.md) 填充变量，生成最终 prompt。风格与尺寸预设见 [references/presets.md](references/presets.md)。

- 用户说"换成灰色背景/西装配领带/中式正装/银行岗"→ 覆盖对应变量。
- 保留原图的 **性别、年龄、脸型、五官、肤色、发际线**；只做提示词里的允许改动。
- 完成判据：prompt 含"保留身份特征"与"禁止过度美颜"两条硬约束，且背景/服装/表情三段已实例化。

### 3. 生成（edit 模式）

**首选：一条命令跑完整链路**（自动挑最佳模型 → 以原图编辑 → 落盘）：

```bash
RESUME_PHOTO_AGENT=<agentId> bash {baseDir}/scripts/generate_resume_photo.sh \
  "<原图绝对路径>" "<输出路径,如 ~/Desktop/简历照/2026-10-16-简历照.jpg>" "[提示词文件]"
```

- 第 3 个参数可省略（脚本内置默认中文提示词）；要覆盖就把第 2 步的提示词写进临时文件传进去。
- 脚本已适配几何差异：`openai/*` 用 `--size 1024x1536`，其余用 `--aspect-ratio 3:4 --resolution 2K`。
- 多 agent 环境必须给 `RESUME_PHOTO_AGENT`，否则可能选错凭证。

**备选：`image_generate` 工具**（该工具已加载时，可异步出图并自动带回会话）：

```
image_generate(
  prompt: <第 2 步的提示词>,
  image: "<原图绝对路径>",
  aspectRatio: "3:4",          // 证件照竖版；方版头像用 "1:1"
  resolution: "2K",            // 需要打印可上 "4K"
  quality: "high",
  outputFormat: "jpeg",
  filename: "resume-photo"
)
```

- 想要多张备选：`count: 2`（1–4）；同一提示词不要重复调用。
- 完成判据：拿到生成图片的本地路径（脚本会打印 `已输出: <路径>`）。

### 4. 落盘与标准尺寸（可选）

- 把成品存到用户目录，例如 `~/Desktop/简历照/`，文件名带日期。
- 需要证件照规格（一寸/二寸/美签）时：

```bash
bash {baseDir}/scripts/resize_photo.sh <生成图路径> 二寸 <输出路径>
```

优先用 `magick`/`convert`，其次 `ffmpeg`，macOS 兜底 `sips`；脚本中心裁剪，不拉伸变形。

- 完成判据：输出文件存在，尺寸等于目标规格。

### 5. 交付

- 用 `MEDIA:<绝对路径>` 把成品发给用户（每张一行），配 1–2 句说明改了什么。
- 若生成了多张，全部附上并让用户挑选。
- 完成判据：用户拿到图片文件，而非只有文字描述。

## 硬性约束

- **不得改变身份**：脸型、五官比例、年龄、性别呈现、肤色基调必须与原图一致。
- **禁止失真美颜**：不磨皮到塑料感、不瘦脸、不大眼、不换脸、不改变脸宽。
- **禁止杂物**：背景无文字、无水印、无 logo、无装饰；服装无花纹/亮色/logo。
- **不伪造他人**：只处理用户本人提供的照片；拒绝把真人照片改成他人或用于冒充。
- 输出为人像照片，不生成证件上的文字/编号/防伪元素。

## 故障排查

| 现象 | 处理 |
|------|------|
| 工具里没有 `image_generate` | 无可用 provider，按"前提条件"第 3 步提示用户配置 |
| 身份被改变 / 像换脸 | 降低改动幅度，强化"保留五官与脸型"约束后重试一次 |
| 背景仍有杂物 | 明确写入"纯色 ${背景}，无任何文字、水印、物体" |
| 输出被过度美颜 | 加入"保留皮肤纹理、毛孔、自然肤色，禁磨皮/瘦脸" |
| 生成超时 | 设置 `image_generate` 的 `timeoutMs`（如 300000）后重试一次 |

## 参考

- [scripts/generate_resume_photo.sh](scripts/generate_resume_photo.sh) — 一条命令：选模型 → 编辑 → 落盘
- [scripts/pick_image_model.py](scripts/pick_image_model.py) — 按优先级挑选最佳可用模型（`--list` 可单独调用）
- [references/prompt-template.md](references/prompt-template.md) — 可填充的提示词模板（中英双版 + 负向约束）
- [references/presets.md](references/presets.md) — 背景/服装/尺寸预设表
- [examples.md](examples.md) — 实际用法示例
- [README.md](README.md) — 项目说明
