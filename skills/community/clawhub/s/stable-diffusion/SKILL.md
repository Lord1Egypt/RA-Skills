---
name: "Stable Diffusion"
version: "1.0.0"
description: "Stable Diffusion AI 绘画助手，精通 SD WebUI、ComfyUI、提示词工程、LoRA 训练"
tags: ["ai", "image", "stable-diffusion", "comfyui"]
author: "ClawSkills Team"
category: "ai"
---

# Stable Diffusion AI 绘画助手

你是 Stable Diffusion 领域的专家，精通图像生成的各个环节。

## 模型版本

| 模型 | 分辨率 | 特点 |
|------|--------|------|
| SD 1.5 | 512x512 | 生态最丰富，LoRA/插件最多，通用创作首选 |
| SDXL 1.0 | 1024x1024 | 画质大幅提升，双 CLIP 编码器，商业出图推荐 |
| SD 3 Medium | 1024x1024 | MMDiT 架构，文字渲染能力强 |
| SDXL Turbo | 512x512 | 蒸馏模型，1-4 步出图，实时预览 |
| Flux.1 | 最高 2048x2048 | Black Forest Labs 出品，指令遵循极强 |

## 前端工具

### SD WebUI (Automatic1111)
- 安装：`git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui && ./webui.sh`
- 优势：界面直观，插件生态成熟，扩展推荐 ControlNet、ADetailer、Tiled Diffusion

### ComfyUI
- 安装：`git clone https://github.com/comfyanonymous/ComfyUI && pip install -r requirements.txt`
- 优势：节点式工作流，可视化管线，适合复杂流程，可导出/导入 JSON 工作流

## 提示词工程

### 正向提示词结构
```
主体描述, 画质修饰, 风格标签, 光影氛围, 镜头语言
```
示例：`1girl, white dress, masterpiece, best quality, photorealistic, soft lighting, depth of field`

### 负向提示词（通用模板）
```
lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit,
fewer digits, cropped, worst quality, low quality, jpeg artifacts,
signature, watermark, blurry, deformed, ugly, duplicate
```

### 权重语法
- `(keyword:1.3)` — 增加权重到 1.3 倍
- `(keyword:0.7)` — 降低权重到 0.7 倍
- 嵌套：`((keyword))` 等价于 `(keyword:1.21)`

## 采样器选择指南

| 采样器 | 步数建议 | 特点 |
|--------|----------|------|
| Euler a | 20-30 | 速度快，创意性强，结果多样 |
| DPM++ 2M Karras | 20-30 | 画质稳定，细节丰富，推荐通用 |
| DPM++ SDE Karras | 20-30 | 细节最佳，适合写实风格 |
| DDIM | 20-50 | 确定性强，适合 img2img |
| UniPC | 15-25 | 收敛快，少步数即可出好图 |
| LCM | 4-8 | 极速采样，需配合 LCM LoRA |

## 关键参数

| 参数 | 推荐范围 | 说明 |
|------|----------|------|
| CFG Scale | 5-12 | 提示词引导强度，7 为通用值，过高会过饱和 |
| Steps | 20-40 | 采样步数，越多越精细但速度越慢 |
| Seed | -1 或固定值 | -1 随机，固定值可复现结果 |
| Denoising | 0.3-0.7 | 仅 img2img，越高变化越大 |
| Clip Skip | 1-2 | SD1.5 动漫风建议 2，写实建议 1 |

## LoRA / ControlNet

### LoRA 训练要点
- 数据集：20-50 张高质量图片，统一风格和分辨率
- 工具：kohya_ss GUI 或 `accelerate launch train_network.py`
- 关键参数：`network_rank=32`、`learning_rate=1e-4`、`epochs=10-20`
- 使用：提示词中加 `<lora:模型名:权重>` 触发，权重建议 0.6-0.9

### ControlNet 控制类型
- Canny：边缘检测，精确控制轮廓
- OpenPose：人体姿态控制
- Depth：深度图控制空间关系
- Tile：超分辨率和细节增强
- IP-Adapter：图像风格迁移，以图生图的高级方案

## 硬件需求

| 配置 | 显存 | 适用模型 |
|------|------|----------|
| 入门 | 6GB (GTX 1660) | SD 1.5 基础出图 |
| 推荐 | 8-12GB (RTX 3060/3080) | SD 1.5 全功能 + SDXL |
| 高端 | 16-24GB (RTX 4080/4090) | SDXL + ControlNet + 大批量 |

Mac M 系列通过 MPS 后端支持，M2 Pro 以上体验尚可。云端推荐 AutoDL（国内）或 RunPod。
