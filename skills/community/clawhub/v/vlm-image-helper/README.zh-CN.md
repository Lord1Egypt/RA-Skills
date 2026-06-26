# vlm-image-helper

[English](README.md) | [中文](README.zh-CN.md)

> 面向 VLM 和 OCR 工作流的视觉检查辅助工具。

`vlm-image-helper` 帮助代理协助视觉模型在重新分析前更清晰地查看图片。它不是通用图片编辑器——它是解决阻碍 OCR 或视觉理解的歧义的针对性视觉辅助工具。

## Problem

视觉模型经常遇到无法自信地阅读文字或区分相似字符的情况：

- **字符混淆**：无法区分 `O` 和 `0`、`I` 和 `l` 或 `1`、`B` 和 `8`
- **方向问题**：文字侧向、倒置或倾斜
- **分辨率限制**：小字或远处细节无法阅读
- **对比度问题**：褪色的扫描件、暗照片、过曝的截图
- **部分可见**：图片只有某个区域重要，但其余部分造成干扰

当模型说"我无法自信地阅读这段文字"或"图片不清晰"时，它需要的是更清晰的视图——而不是完整的图片编辑。

## Solution

`vlm-image-helper` 提供**语义化预设**，让代理可以用自然语言描述区域：

- 说**"左上角"**而不是猜测像素坐标
- 说**"中间"**而不是计算百分比
- 说**"x2"**而不是计算缩放因子

代理用自然语言思考；skill 负责翻译成精确操作。

## What You Get

- **语义化裁剪预设**：`top-left`、`center`、`bottom-right`、`left-half` 等
- **语义化缩放预设**：`x2`、`x3`、`x4`
- **旋转**：任意角度，处理倾斜文字
- **增强**：自动增强、对比度、锐度，提升可读性
- **格式转换**：文件路径 ↔ base64，便于重新输入
- **最小化编辑**：只做消除歧义所需的最小变换

## How It Works

```text
1. 模型发现图片中的模糊区域
2. 代理选择语义预设（如"右下角"）
3. 脚本应用最小变换
4. 代理将处理后的图片重新输入进行再分析
5. 模型确认，或代理迭代使用更紧凑的裁剪
```

## Core Capabilities

| 能力 | 描述 |
|------|------|
| **语义化裁剪** | `--crop-preset top-left`、`center`、`bottom-right` 等 |
| **语义化缩放** | `--scale-preset x2`、`x3`、`x4` |
| **旋转** | `--rotate 90`、`--rotate -15`，任意角度 |
| **增强** | `--auto-enhance`、`--contrast 1.5`、`--sharpness 2.0` |
| **管道** | 一条命令链式组合多个操作 |
| **透传** | 无需编辑，直接将文件转换为 base64 |

## 安装

**前置依赖：**
```bash
pip install Pillow
# 或
uv pip install Pillow
```

**安装 skill：**
```bash
# 克隆仓库
git clone https://github.com/your-org/vlm-image-helper.git

# 复制到 skills 目录
# macOS / Linux
cp -r vlm-image-helper/* ~/.claude/skills/vlm-image-helper/

# Windows (PowerShell)
Copy-Item -Recurse vlm-image-helper/* $env:USERPROFILE\.claude\skills\vlm-image-helper\
```

## 快速示例

```bash
# 旋转侧向文字
python scripts/image_helper.py image.png --rotate 90 -o rotated.png

# 裁剪右下角象限并放大 3 倍
python scripts/image_helper.py image.png --crop-preset bottom-right --scale-preset x3 -o detail.png

# 增强低对比度文字
python scripts/image_helper.py image.png --auto-enhance -o enhanced.png

# 将文件转换为 base64 用于重新输入
python scripts/image_helper.py image.png --base64

# 完整管道：旋转、裁剪中间、放大 2 倍、输出 base64
python scripts/image_helper.py screenshot.png --rotate 5 --crop-preset center --scale-preset x2 --base64
```

## 何时使用

- 模型无法自信地阅读图片中的文字
- 模型无法区分相似字符（`O/0`、`I/l/1`）
- 模型表示图片不清晰或质量低
- 图片只有某个区域相关
- 模型需要二次分析更清晰的视图

## 何时不使用

- 通用图片编辑（裁剪、调整大小、美化滤镜）
- 批量图片处理
- 图片格式转换（除非是为了重新输入视觉模型）

## Repository Structure

```text
vlm-image-helper/
|-- SKILL.md                 # 核心工作流和决策指南
|-- README.md
|-- scripts/
|   `-- image_helper.py      # 主 CLI 工具
|-- references/
|   |-- cli-reference.md     # 完整 CLI 文档
|   `-- presets.md           # 预设表和选择启发式
`-- agents/
    `-- openai.yaml          # OpenAI 兼容的 agent 配置
```

## License

本项目采用 [MIT License](LICENSE) 授权。
