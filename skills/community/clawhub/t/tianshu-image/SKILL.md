---
name: tianshu-image
description: >
  使用阿里云通义万相 (DashScope) 生成图片。Use when: 用户需要根据文字描述生成图片；用户说「画一张」「生成图片」「文生图」。
  NOT for: 图片编辑、风格迁移、其他非文生图场景。
metadata:
  openclaw:
    primaryEnv: DASHSCOPE_API_KEY
    requires:
      env:
        - DASHSCOPE_API_KEY
---

# 天树文生图 (tianshu-image)

使用阿里云通义万相 API 根据文字描述生成图片，Node.js 实现，无需 Python/uv。

## When to Run

- 用户说「画一张」「生成图片」「文生图」「根据这段描述生成图」
- 用户提供图片描述，需要 AI 生成对应图片

## 前置配置

在 `~/.openclaw/openclaw.json` 的 `skills.entries.tianshu-image` 中配置，或设置环境变量：

- `DASHSCOPE_API_KEY` - 阿里云 DashScope API Key（从 https://dashscope.console.aliyun.com/ 获取）
- 或 `models.providers.bailian.apiKey`（若已配置百炼）

## Workflow

1. 确认用户需要生成图片
2. 执行脚本：
   ```
   node ~/.openclaw/skills/tianshu-image/scripts/generate_image.js --prompt "描述" [--size 1664*928]
   ```
3. 脚本输出 `MEDIA_URL: <url>` 或 `MEDIA: <本地路径>`
4. 用 Markdown 展示图片：`![生成的图片](URL)`

## 参数

- `--prompt` / `-p`：图片描述（必填）
- `--size` / `-s`：尺寸，默认 `1664*928`。可选：`1024*1024`、`720*1280`、`1280*720`
- `--model` / `-m`：模型，默认 `qwen-image-max`。可选：`qwen-image-turbo`、`qwen-image-plus-2026-01-09`
- `--filename` / `-f`：保存到本地文件路径（可选）
- `--negative-prompt`：负向提示词
- `--no-prompt-extend`：禁用自动提示词增强
- `--watermark`：添加水印

## Output

- 未指定 `--filename` 时输出 `MEDIA_URL: <url>`，直接展示 URL
- 指定 `--filename` 时输出 `MEDIA: <本地路径>`，表示已保存到本地
