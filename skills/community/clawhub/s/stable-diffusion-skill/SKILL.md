---
name: stable-diffusion
description: "Complete Stable Diffusion WebUI integration skill. Supports txt2img, img2img, inpainting, ControlNet, LoRA, model switching, upscaling, and more via SD WebUI API. Use when user wants to generate images with Stable Diffusion, edit images, apply styles, use ControlNet, or manage SD models."
description_zh: "完整的 Stable Diffusion 图像生成 Skill，支持文生图、图生图、局部重绘、ControlNet、LoRA、模型切换、超分辨率放大等全套功能，通过 SD WebUI API 调用本地部署实例。"
description_en: "Full Stable Diffusion integration: txt2img, img2img, inpainting, ControlNet, LoRA, upscaling via local SD WebUI API."
version: "1.0.0"
homepage: https://github.com/AUTOMATIC1111/stable-diffusion-webui
allowed-tools: Bash, Read, Write, Edit
metadata:
  clawdbot:
    emoji: 🎨
    requires:
      bins:
        - python
      env:
        - SD_WEBUI_URL
      pip:
        - requests
        - Pillow
    setup:
      - "确保本地已启动 Stable Diffusion WebUI（带 --api 参数）"
      - "默认地址：http://127.0.0.1:7860"
      - "安装依赖：pip install requests Pillow"
---

# 🎨 Stable Diffusion Skill

通过本地部署的 **Stable Diffusion WebUI API** 实现完整的 AI 图像生成与编辑能力。

> **前提条件**：需要本地安装并启动 SD WebUI（AUTOMATIC1111 版本），启动时加上 `--api` 参数。
> 默认 URL：`http://127.0.0.1:7860`（可通过环境变量 `SD_WEBUI_URL` 修改）

---

## 🚀 快速开始

### 检查连接状态
```bash
python ${CLAUDE_SKILL_DIR}/sd_client.py --action status
```

### 第一次使用流程
1. 确认 SD WebUI 已运行（`--api` 模式）
2. 检查连接：`python ${CLAUDE_SKILL_DIR}/sd_client.py --action status`
3. 查看可用模型：`python ${CLAUDE_SKILL_DIR}/sd_client.py --action list-models`
4. 生成第一张图！

---

## 📋 功能速查表

| 功能 | 命令关键词 | 说明 |
|------|-----------|------|
| 文生图 | txt2img / 生成图片 / 画 | 从文字描述生成图像 |
| 图生图 | img2img / 图片风格化 | 基于参考图生成新图 |
| 局部重绘 | inpaint / 修图 / 重绘 | 修改图片特定区域 |
| ControlNet | controlnet / 姿势控制 | 精确控制图像结构 |
| 超分辨率 | upscale / 放大 / 高清 | 放大图片并增强细节 |
| 模型管理 | 换模型 / 加载模型 | 切换检查点/LoRA |
| 批量生成 | 批量 / batch | 一次生成多张变体 |
| 提示词工具 | 优化提示词 / 翻译 | 将中文描述转为 SD 提示词 |

---

## 🖼️ 文生图（txt2img）

### 基本用法
用户说："帮我画一张..."、"生成一张..."、"txt2img..."

**参数收集流程**：
1. 如果用户没提供详细参数，先询问关键信息：
   - 描述（正向提示词）
   - 风格偏好（写实/动漫/油画等）
   - 尺寸（512x512 / 768x768 / 512x768 等）
2. 将中文描述智能转换为 SD 提示词（见提示词转换规则）
3. 调用 API 生成

**执行命令**：
```bash
python ${CLAUDE_SKILL_DIR}/sd_client.py --action txt2img \
  --prompt "1girl, beautiful, masterpiece, best quality" \
  --negative-prompt "ugly, bad anatomy, blurry" \
  --width 512 --height 768 \
  --steps 20 --cfg-scale 7 \
  --sampler "DPM++ 2M Karras" \
  --seed -1 \
  --output-dir "./sd_output"
```

**常用参数说明**：
| 参数 | 默认值 | 说明 |
|------|-------|------|
| `--steps` | 20 | 采样步数（推荐 20-30） |
| `--cfg-scale` | 7 | 提示词遵从度（1-30，推荐 5-12） |
| `--sampler` | DPM++ 2M Karras | 采样器 |
| `--seed` | -1 | 随机种子（-1=随机） |
| `--width/height` | 512x512 | 图像尺寸（需为 8 的倍数） |
| `--batch-size` | 1 | 每批生成数量 |
| `--n-iter` | 1 | 批次数量 |

---

## 🔄 图生图（img2img）

用户说："把这张图片..."、"参考这张图风格化..."、"img2img..."

```bash
python ${CLAUDE_SKILL_DIR}/sd_client.py --action img2img \
  --init-image "/path/to/image.png" \
  --prompt "oil painting style, detailed" \
  --denoising-strength 0.75 \
  --steps 20 --cfg-scale 7 \
  --output-dir "./sd_output"
```

**去噪强度（denoising-strength）指南**：
- `0.1-0.3`：轻微修改，保留原图 70-90%
- `0.4-0.6`：中度变化，半保留原始构图
- `0.7-0.9`：大幅改变，保留基本构图
- `1.0`：完全重新生成

---

## 🖌️ 局部重绘（Inpainting）

用户说："把这张图的...改成..."、"修改图片中的..."

```bash
python ${CLAUDE_SKILL_DIR}/sd_client.py --action inpaint \
  --init-image "/path/to/image.png" \
  --mask-image "/path/to/mask.png" \
  --prompt "new content for masked area" \
  --inpainting-fill 1 \
  --denoising-strength 0.85 \
  --output-dir "./sd_output"
```

**蒙版填充模式**：
- `0`：填充（fill）
- `1`：原始（original）
- `2`：潜空间噪声（latent noise）
- `3`：潜空间无（latent nothing）

---

## 🎛️ ControlNet 控制

用户说："参考这个姿势..."、"用 ControlNet..."、"保持构图生成..."

```bash
python ${CLAUDE_SKILL_DIR}/sd_client.py --action txt2img-controlnet \
  --prompt "beautiful girl, detailed" \
  --control-image "/path/to/pose.png" \
  --control-module "openpose" \
  --control-model "control_v11p_sd15_openpose" \
  --control-weight 1.0 \
  --output-dir "./sd_output"
```

**常用 ControlNet 模块**：
| 模块 | 用途 |
|------|------|
| `openpose` | 人体姿势控制 |
| `canny` | 边缘线条控制 |
| `depth` | 深度图控制 |
| `normal` | 法线图控制 |
| `scribble` | 手绘草图控制 |
| `seg` | 语义分割控制 |
| `tile` | 细节增强/高清修复 |
| `lineart` | 线稿上色控制 |

---

## 🔍 超分辨率放大（Upscaling）

用户说："放大这张图..."、"高清化..."、"超分..."

```bash
python ${CLAUDE_SKILL_DIR}/sd_client.py --action upscale \
  --image "/path/to/image.png" \
  --upscaler "R-ESRGAN 4x+" \
  --scale 2 \
  --output-dir "./sd_output"
```

**可用放大算法**（需 SD WebUI 中已安装）：
- `Latent`（潜空间放大，适合动漫）
- `R-ESRGAN 4x+`（通用高质量）
- `R-ESRGAN 4x+ Anime6B`（动漫专用）
- `ESRGAN_4x`（经典ESRGAN）
- `SwinIR 4x`（写实图像）

---

## 📦 模型管理

### 查看可用模型
```bash
python ${CLAUDE_SKILL_DIR}/sd_client.py --action list-models
python ${CLAUDE_SKILL_DIR}/sd_client.py --action list-samplers
python ${CLAUDE_SKILL_DIR}/sd_client.py --action list-upscalers
python ${CLAUDE_SKILL_DIR}/sd_client.py --action list-loras
python ${CLAUDE_SKILL_DIR}/sd_client.py --action list-vaes
```

### 切换检查点模型
```bash
python ${CLAUDE_SKILL_DIR}/sd_client.py --action switch-model \
  --model-name "realisticVisionV60B1_v60B1VAE.safetensors"
```

### 在提示词中使用 LoRA
在 prompt 中加入 `<lora:模型名:权重>` 语法：
```
1girl, beautiful, <lora:koreanDollLikeness_v15:0.8>, masterpiece
```

---

## 🎨 高清修复（Hires Fix）

在 txt2img 中启用 Hires Fix 生成高清大图：

```bash
python ${CLAUDE_SKILL_DIR}/sd_client.py --action txt2img \
  --prompt "landscape, detailed" \
  --width 512 --height 512 \
  --enable-hr \
  --hr-scale 2 \
  --hr-upscaler "R-ESRGAN 4x+" \
  --hr-steps 15 \
  --denoising-strength 0.5 \
  --output-dir "./sd_output"
```

---

## 💡 提示词转换规则

当用户用中文描述时，按以下规则转换为 SD 提示词：

### 标准质量词（始终添加）
**正向**（推荐加入）：
```
masterpiece, best quality, ultra-detailed, high resolution
```

**负向**（推荐加入）：
```
(worst quality:2), (low quality:2), blurry, ugly, bad anatomy, bad hands, 
extra limbs, deformed, mutated, poorly drawn face, text, watermark
```

### 风格映射
| 中文 | 英文提示词 |
|------|-----------|
| 写实/真实 | photorealistic, ultra realistic, RAW photo |
| 动漫/二次元 | anime style, 2d, cel shading |
| 油画 | oil painting, painterly |
| 水彩 | watercolor, soft colors |
| 赛博朋克 | cyberpunk, neon lights, futuristic |
| 古风/国风 | chinese traditional art, hanfu, ink wash |
| 皮克斯风 | pixar style, 3d render, cartoon |

### 翻译辅助工具
```bash
python ${CLAUDE_SKILL_DIR}/prompt_helper.py \
  --translate "美丽的中国女孩，穿着汉服，站在樱花树下" \
  --style "anime"
```

---

## 📊 工作流示例

### 示例 1：生成动漫风格人物
用户："画一个穿着汉服的古风美女"

```bash
# 步骤1：检查模型
python ${CLAUDE_SKILL_DIR}/sd_client.py --action list-models

# 步骤2：生成图像
python ${CLAUDE_SKILL_DIR}/sd_client.py --action txt2img \
  --prompt "1girl, beautiful chinese girl, hanfu, traditional chinese clothing, cherry blossom, long hair, masterpiece, best quality, anime style" \
  --negative-prompt "(worst quality:2), (low quality:2), bad anatomy, ugly" \
  --width 512 --height 768 \
  --steps 25 --cfg-scale 7.5 \
  --sampler "DPM++ 2M Karras" \
  --output-dir "./sd_output"
```

### 示例 2：风格化照片
用户："把这张照片变成油画风格"

```bash
python ${CLAUDE_SKILL_DIR}/sd_client.py --action img2img \
  --init-image "photo.jpg" \
  --prompt "oil painting, impressionist style, masterpiece, detailed brushwork" \
  --negative-prompt "photo, realistic, blurry" \
  --denoising-strength 0.65 \
  --steps 25 --cfg-scale 8 \
  --output-dir "./sd_output"
```

### 示例 3：批量生成变体
用户："同一个主题生成4张不同变体"

```bash
python ${CLAUDE_SKILL_DIR}/sd_client.py --action txt2img \
  --prompt "fantasy landscape, magical forest" \
  --batch-size 4 \
  --seed -1 \
  --output-dir "./sd_output"
```

---

## ⚙️ 配置说明

### 环境变量
| 变量 | 默认值 | 说明 |
|------|-------|------|
| `SD_WEBUI_URL` | `http://127.0.0.1:7860` | SD WebUI 地址 |
| `SD_OUTPUT_DIR` | `./sd_output` | 默认输出目录 |
| `SD_TIMEOUT` | `300` | 请求超时（秒） |

### 推荐采样器
| 采样器 | 适用场景 |
|--------|---------|
| DPM++ 2M Karras | 通用最佳（推荐） |
| DPM++ SDE Karras | 细节丰富 |
| Euler a | 快速多样 |
| DDIM | 高一致性 |
| UniPC | 快速高质量 |

---

## 🔧 故障排除

**连接失败**：
- 确认 SD WebUI 已启动并带有 `--api` 参数
- 检查端口是否正确（默认 7860）
- 若使用远程服务器，检查 `SD_WEBUI_URL`

**生成超时**：
- 增大 `SD_TIMEOUT` 环境变量
- 减少步数（`--steps`）
- 降低图像尺寸

**CUDA 内存不足**：
- 降低图像分辨率
- 减少 batch size
- 在 SD WebUI 启动时添加 `--medvram` 或 `--lowvram`

---

## 📁 工具文件说明

| 文件 | 功能 |
|------|------|
| `sd_client.py` | 主 API 客户端（所有功能入口） |
| `prompt_helper.py` | 提示词优化与中文翻译工具 |
| `image_utils.py` | 图像预处理工具（Base64编解码等） |

---

## ⚖️ 免责声明

> **English:**
> This skill is not affiliated with, endorsed by, or connected to AUTOMATIC1111 or the Stable Diffusion project in any way. It is a third-party integration tool that requires users to install SD WebUI independently. The user is solely responsible for ensuring their use of Stable Diffusion complies with applicable laws, terms of service, and licensing requirements. Generated images are subject to users' own responsibility and must comply with all relevant copyright and usage policies.

> **中文：**
> 本 Skill 与 AUTOMATIC1111 或 Stable Diffusion 项目没有任何隶属、认可或关联关系。它是一个第三方集成工具，需要用户自行安装 SD WebUI。用户全权负责确保其使用 Stable Diffusion 符合适用法律、服务条款和许可要求。生成的图片由用户自行承担责任。

---

## 📜 许可证

- 本 Skill 采用 **MIT-0 License** 开源（完全开放，无需署名）
- 本 Skill 不包含 Stable Diffusion 任何源码
- 使用本 Skill 需遵守 SD WebUI 的 **AGPL-3.0** 许可证



