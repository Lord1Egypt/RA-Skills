---
name: gemini-image-gen
description: >-
  Generate, edit, and compose images using Gemini models. Activate when user asks to generate images, draw, create logos/posters/icons/banners, edit/modify photos, combine images, or any image creation task.
  画图、生成图片、做图、P图、修图、合成图、做logo、做海报、做图标、做封面、品牌视觉、Nano Banana、Banana。

metadata:
  openclaw:
    emoji: "🎨"
    category: creative
    homepage: "https://github.com/wangyan/wangyan-skills"
    requires:
      bins:
        - python3
        - uv
    permissions:
      - messaging
    tags:
      - image-generation
      - image-editing
      - image-composition
      - text-to-image
      - logo-design
      - poster-design
      - brand-visual
      - gemini
      - nano-banana
      - nano-banana-pro
      - openai-compatible

---

# Gemini Image Generator

通过 `Nano Banana` 实现文生图、图片编辑与多图合成，支持 OpenAI 兼容和 Google 原生两种 API 格式，可自定义端点和密钥。

---

## 📦 安装依赖

本技能需要 `python3` 和 `uv` 环境。

### 安装 Python 3

```bash
# macOS
brew install python3

# Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip

#CentOS/RHEL
sudo yum install python3 python3-pip
```

### 安装 uv

`uv` 是一个极速的 Python 包管理器，用于运行脚本和管理依赖。

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# 使用 pip
pip install uv

# 确保 `uv` 在 PATH 中可用
uv --version
```

---

## 📦 安装技能

### 使用 skills CLI 安装（推荐）

```bash
# github 镜像源
npx skills add https://github.com/wangyan/wangyan-skills/tree/main/skills/gemini-image-gen

# gitcode 镜像源 (推荐国内用户使用)
npx skills add https://gitcode.com/wang_yan/wangyan-skills.git
```

### 使用 Clawhub CLI 安装

```bash
# 使用 Clawhub CLI 安装
npx clawhub@latest install wangyan-gemini-image-gen

# 使用腾讯 skillhub 安装 (推荐国内用户使用)
curl -fsSL https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/install/install.sh | bash  -s -- --no-skills
skillhub install wangyan-gemini-image-gen
```

---

## ⚙️ 环境变量

运行时需要提供 `GEMINI_API_KEY` 和 `GEMINI_BASE_URL`，可以通过命令行参数、环境变量或 `.env` 文件提供。

```json
{
  "skills": {
    "entries": {
      "gemini-image-gen": {
        "enabled": true,
        "apiKey": "your-api-key",
        "env": {
          "GEMINI_API_KEY": "your-api-key",
          "GEMINI_BASE_URL": "https://api.example.com/v1",
          "GEMINI_MODEL": "gemini-3.1-flash-image-preview",
          "GEMINI_API_FORMAT": "openai",
          "GEMINI_TIMEOUT": "300",
          "GEMINI_RESOLUTION": "1K",
          "GEMINI_OUTPUT_DIR": "output/images"
        }
      }
    }
  }
}
```

### 🔧 配置优先级

配置按以下优先级加载（高优先级覆盖低优先级）：

```
命令行参数 > 环境变量 > 技能目录 .env 
```

### 📄 .env 文件配置

你也可以使用 `.env` 文件来配置参数，支持以下位置（按优先级排序）：

| 位置 | 优先级 | 说明 |
|------|--------|------|
| `技能目录/.env` | 最高 | 技能本地配置，推荐 |
| `~/.openclaw/.env` | 中 | 全局配置，所有技能共享 |
| `/workspace/.env` | 最低 | 沙箱环境配置 |

**创建 `.env` 文件：**

```bash
cd ~/.openclaw/skills/gemini-image-gen
cp .env.example .env

# 编辑 .env 填入你的配置
nano .env
```

**示例 `.env` 文件：**

```bash
# 必填配置
GEMINI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GEMINI_BASE_URL=https://api.example.com/v1

# 可选配置
GEMINI_MODEL=gemini-3.1-flash-image-preview
GEMINI_API_FORMAT=openai
GEMINI_TIMEOUT=300
GEMINI_RESOLUTION=1K
GEMINI_OUTPUT_DIR=output/images
```

| 参数 | 环境变量 | 说明 |
|------|---------|------|
| `--prompt` / `-p` | - | 图片描述或编辑指令（**必填**） |
| `--filename` / `-f` | - | 输出文件名（**必填**） |
| `--api-key` / `-k` | `GEMINI_API_KEY` | API 密钥（运行时必填，可由命令行、环境变量或 `.env` 提供） |
| `--base-url` / `-b` | `GEMINI_BASE_URL` | API 端点 URL（运行时必填，可由命令行、环境变量或 `.env` 提供） |
| `--model` / `-m` | `GEMINI_MODEL` | 模型名称（默认自动轮询） |
| `--api-format` / `-F` | `GEMINI_API_FORMAT` | `openai`（默认）或 `google` |
| `--timeout` / `-t` | `GEMINI_TIMEOUT` | 超时秒数（默认 300） |
| `--resolution` / `-r` | `GEMINI_RESOLUTION` | `1K`（默认）、`2K`、`4K` |
| `--output-dir` / `-o` | `GEMINI_OUTPUT_DIR` | 输出目录（默认 `output/images`） |
| `--input-image` / `-i` | - | 输入图片路径（可重复，最多 14 张） |
| `--aspect-ratio` / `-a` | - | 宽高比（`1:1`、`16:9`、`9:16`、`4:3`、`3:4`、`3:2`、`2:3`） |
| `--quality` | - | 图片质量（`standard` 默认、`hd`） |
| `--style` | - | 风格（`natural` 默认、`vivid`） |
| `--no-timestamp` | - | 不自动添加时间戳前缀 |
| `--verbose` / `-v` | - | 输出详细调试信息 |

---

## 🚀 使用方法

> ⚠️ **重要**：脚本必须在**工作区目录**下运行，不要 `cd` 到技能目录。输出路径 `output/images` 是相对于工作目录的。

> 📤 **图片发送**：脚本成功后会输出 `IMAGE_PATH: /absolute/path/to/image.png`，agent 从输出中提取路径，然后调用 `message(action=send, media=<path>)` 发送给用户。**不依赖 `MEDIA:` 行机制**。

### 生成图片

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "图片描述" --filename "output.png"
```

### 编辑图片（单图）

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "编辑指令" --filename "edited.png" -i "/path/input.png" --resolution 2K
```

### 合成多张图片（最多 14 张）

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "合成指令" --filename "composed.png" -i img1.png -i img2.png -i img3.png
```

### 自定义端点

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "描述" --filename "output.png" \
  --base-url "https://example.com/v1" --api-key "sk-xxx" --model "gemini-3.1-flash-image-preview"
```

### 使用 Google 原生格式

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "描述" --filename "output.png" --api-format google
```

### 发送图片给用户（必须步骤）

脚本执行完成后，从输出中提取 `IMAGE_PATH:` 行的路径，然后调用：

```
message(action=send, channel=<channel>, media=<image_path>)
```

---

## 🤖 模型自动轮询

脚本内置模型自动轮询机制，当首选模型不可用时，会自动尝试备选模型：

**轮询顺序：**
1. `gemini-3.1-flash-image-preview`（默认首选）
2. `gemini-3-pro-image-preview`（备选1）
3. `gemini-2.5-flash-image`（备选2）

**触发条件：**
- 模型返回 404/400 错误
- 模型返回 "model not found" / "not available" / "not supported" 等错误

**自定义模型：**
如果通过 `--model` 指定了自定义模型，脚本会先尝试该模型，失败后再按上述顺序轮询。

---

## 📝 注意事项

- 文件名使用时间戳格式：`yyyy-mm-dd-hh-mm-ss-name.png`
- 图片生成成功后，脚本输出 `IMAGE_PATH: /absolute/path/to/image.png`
- agent 必须从输出中提取路径，调用 `message(action=send, media=<path>)` 发送图片
- **不要使用 `MEDIA:` 行机制**，在飞书等渠道不可靠

## 🔐 权限依赖

本技能发送图片依赖 **Messaging 权限**（`message` 工具）。

使用前请确认 OpenClaw 已配置消息渠道（如飞书、Telegram 等），否则图片只会保存到本地，无法发送给用户。
