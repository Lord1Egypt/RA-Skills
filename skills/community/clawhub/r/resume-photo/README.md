# 🪪 Resume Photo · 简历照生成器

把一张**生活照**变成**高端专业简历照** —— 换纯色背景、上商务正装、柔光补光、端正姿态，保留你的五官与身份特征，输出可直接打印和投简历的高清人像。

## 特点

- **保身份**：严格保留脸型、五官、年龄、肤色，不做换脸式"美化"。
- **不过度美颜**：保留皮肤纹理与衣物细节，拒绝磨皮瘦脸失真。
- **场景预设**：应届 / 金融 / 互联网 / 政务 / 学术 / 海外申请，各有背景与服装搭配。
- **标准尺寸**：一寸、二寸、大一寸、小二寸、美签 2x2 一键裁切（自带脚本）。
- **多版本**：一次生成多张备选，挑到满意为止。

## 依赖

- 至少一个**已配置凭证**且支持参考图编辑的 provider：Google / OpenAI / OpenRouter / fal / xAI / MiniMax。
- 凭证：`openclaw models auth paste-api-key`（`OPENAI_API_KEY` / `GEMINI_API_KEY` / `OPENROUTER_API_KEY` / `FAL_KEY` / `XAI_API_KEY`），或 `openclaw models auth login` 用订阅 OAuth。
- 模型优先级（自动挑）：`google/gemini-3.1-flash-image` → `openai/gpt-image-2` → OpenRouter Gemini → fal nano-banana → Grok Imagine → MiniMax。
- 标准尺寸裁切脚本需要 `magick` / `convert` / `ffmpeg` / `sips` 之一（macOS 自带 `sips`）。

## 用法

直接说人话即可：

> "把这张照片做成简历照，浅灰背景，二寸。"
> "转成银行求职的证件照。"
> "给我三个背景颜色的版本。"

## 文件

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 主流程说明 |
| `references/prompt-template.md` | 提示词模板（中英双版 + 负向约束） |
| `references/presets.md` | 背景 / 服装 / 尺寸预设 |
| `scripts/generate_resume_photo.sh` | 一键：挑最佳模型 → 参考图编辑 → 落盘 |
| `scripts/pick_image_model.py` | 按优先级挑选最佳可用生图模型 |
| `scripts/resize_photo.sh` | 标准证件照尺寸裁剪 |
| `examples.md` | 用法示例 |

## 许可

MIT
