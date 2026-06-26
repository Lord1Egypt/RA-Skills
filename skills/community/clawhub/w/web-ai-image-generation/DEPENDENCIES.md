# Python 依赖与安装说明

本文件说明运行 Web AI 生图 skill 所需的 Python、浏览器和系统环境依赖。

## Python 版本

建议使用：

- Python 3.10+

## Python 包依赖

依赖文件：`requirements.txt`

包含：

- `playwright`：浏览器自动化。
- `Pillow`：图片格式处理，可用于后续扩展或统一转码。

安装：

```bash
python -m pip install -r requirements.txt
```

## Playwright 浏览器依赖

安装 Chromium：

```bash
python -m playwright install chromium
```

如需安装系统依赖，可执行：

```bash
python -m playwright install-deps chromium
```

## 系统浏览器

脚本默认优先尝试使用：

```text
/usr/bin/google-chrome
```

如果不存在，会回退到 Playwright 自带 Chromium。

也可以通过参数指定 Chrome 路径：

```bash
python scripts/ai_image_playwright.py \
  --platform gemini \
  --prompt "一张科技感短视频封面" \
  --chrome-path /path/to/google-chrome
```

## 桌面环境要求

当前实现使用 `headless=False`，需要可用桌面环境。

Linux 下通常需要有效的 `DISPLAY`。如果在服务器环境运行，可以考虑使用 `xvfb`：

```bash
xvfb-run -a python scripts/ai_image_playwright.py \
  --platform chatgpt \
  --prompt "一张电影海报风格的 AI 封面"
```

## 登录态目录

默认 profile 和输出目录位于当前 skill 文件夹下：

```text
skills/web-ai-image-generation/.runtime/profile
skills/web-ai-image-generation/.runtime/output
```

首次运行时需要在弹出的浏览器中登录 Gemini 或 ChatGPT。之后会复用 `.runtime/profile` 中保存的登录状态。

也可以指定独立 profile：

```bash
python scripts/ai_image_playwright.py \
  --platform gemini \
  --prompt "一张竖屏短视频封面" \
  --profile-dir ./.runtime/gemini-profile
```

## 快速验证

Gemini：

```bash
python scripts/ai_image_playwright.py \
  --platform gemini \
  --prompt "一张竖屏 3:4 的短视频封面，主题是 AI 自动剪辑" \
  --output-dir ./output
```

ChatGPT：

```bash
python scripts/ai_image_playwright.py \
  --platform chatgpt \
  --prompt "一张竖屏 3:4 的短视频封面，主题是 AI 自动剪辑" \
  --output-dir ./output
```

输出文件会保存到 `--output-dir` 指定目录。
