---
name: visual-muse
description: "ComfyUI 图像生成工坊 — 用自然语言描述需求，自动生成高质量 AI 图片。支持 SDXL/Flux 多模型、风格模板自动匹配、批量生成、质量评分。说「画一张图」即可触发。"
version: 1.0.0
metadata: { "openclaw": { "emoji": "🎨", "requires": { "bins": ["python3", "curl"], "env": ["COMFYUI_API_URL"] }, "primaryEnv": "COMFYUI_API_URL" } }
---

# Visual Muse — AI 视觉缪斯

通过自然语言对话生成 AI 图片的完整技能包。

## 它能做什么

- 你说中文需求 → 自动生成英文 prompt → 调用本地 ComfyUI → 出图
- 自动匹配风格模板（电影感/动漫/写实/概念艺术/水彩）
- 支持批量生成 + 质量评分 + 迭代优化
- 记录你的审美偏好，越用越懂你

## 前置条件

1. macOS（Apple Silicon）或 Linux + NVIDIA GPU
2. ComfyUI 已安装并运行（API 端口 8188）
3. 至少一个 SDXL checkpoint 模型

## 快速开始

安装后执行 setup 脚本：

```bash
bash ~/.openclaw/workspace/skills/creative-workshop/scripts/setup.sh
```

它会检查 ComfyUI 是否安装、模型是否就位，并引导你完成配置。

## 使用方式

直接对 OpenClaw 说：

- "画一张赛博朋克猫在雨夜街道"
- "动漫风格，女孩在樱花树下"
- "写实照片，城市天际线黄昏"
- "出4张不同风格的猫"

## 包含的子技能

| 技能 | 功能 |
|------|------|
| prompt-agent | 中文→英文prompt，自动匹配风格模板 |
| workflow-agent | 选择模型和参数，组装 ComfyUI 工作流 |
| render-agent | 调用 ComfyUI API 执行生成 |
| critic-agent | 多维评分 + 问题诊断 + 改进建议 |
| memory-agent | 记录审美偏好，越用越准 |

## 支持的模型

开箱即用支持任何 SDXL checkpoint，推荐：
- DreamShaper XL（万能型）
- Juggernaut XL（电影写实）
- Animagine XL（动漫）

## 配置

环境变量 `COMFYUI_API_URL` 默认值 `http://host.docker.internal:8188`（Docker 环境）或 `http://127.0.0.1:8188`（本地环境）。

## 图片输出位置

生成的图片保存在 ComfyUI 的 output 目录下的 `creative_workshop/` 子文件夹。
