---
name: tukeli-visual-api
description: 调用图可丽（Tukeli）视觉处理 API，实现通用抠图、人脸变清晰、AI背景更换三项能力。支持文件上传、图片URL两种输入方式，返回二进制流或Base64编码结果。AI背景更换为异步接口，需先提交任务再查询结果。
risk: safe
source: community
date_added: '2026-03-16'
author: tukeli
tags:
- image-processing
- background-removal
- face-enhance
- ai-background
- api
tools:
- claude-code
- cursor
- codex-cli
---

# 图可丽视觉 API — 图像处理工具集

## 概述

通过图可丽（Tukeli）REST API 实现三项核心图像处理能力：

1. **通用抠图（Image Matting）** — 自动识别图像中主体轮廓，与背景分离，返回透明 PNG；支持人像、物体、头像等多种类型
2. **人脸变清晰（Face Clear）** — AI 增强人脸清晰度，将模糊低质量人脸照片转为高清图
3. **AI背景更换（AI Background）** — 根据文字描述自动对图片透明区域进行 AI 扩展生成新背景（异步接口）

> **注意**：图可丽 API 的请求域名为 `https://picupapi.tukeli.net`，与图可丽官网域名不同，请勿混淆。

## 适用场景

- 用户需要去除图片背景时
- 用户需要提升人脸照片清晰度时
- 用户需要为已抠图的图片生成 AI 背景时
- 用户提到"抠图"、"去背景"、"人像分割"等相关话题时
- 用户提到"人脸增强"、"照片变清晰"等相关话题时
- 用户提到"AI换背景"、"背景生成"等相关话题时

## 不适用场景

- 任务与图像处理无关
- 用户需要生成全新图片（非处理现有图片）
- 用户需要视频处理（请使用其他工具）

## 工作原理

通过图可丽 API 对图片进行 AI 处理。每次调用消耗点数（积分）：
- 抠图：图片 15M 以下消耗 1 点，15M~25M 消耗 2 点
- 人脸变清晰：每次消耗 2 点
- AI背景更换：按分辨率计费（≤512×512 消耗 3 点，≤1024×1024 消耗 6 点，≤1920×1080 消耗 12 点）

## 三种 API 对比

| 场景 | 推荐 API |
|------|---------|
| 去除商品/人物/动物背景 | **通用抠图**（mattingType=6）|
| 提取人像（发丝级精度） | **通用抠图**（mattingType=1）|
| 提取头像/头部区域 | **通用抠图**（mattingType=3）|
| 模糊人脸照片变高清 | **人脸变清晰**（mattingType=18）|
| 为透明图片生成 AI 背景 | **AI背景更换**（异步接口）|

## 快速开始

1. 前往 https://www.tukeli.net 注册账号
2. 获取 API Key（登录后在账户设置中获取）
3. 在 `.env` 文件中配置：`TUKELI_API_KEY=你的密钥`
4. 安装依赖：`pip install -r scripts/requirements.txt`
5. 运行脚本：`python scripts/tukeli.py --api matting --image photo.jpg`

完整配置说明见 `references/setup-guide.md`。

## 1. 调用模式

| 命令参数 | 功能 | 接口 |
|---------|------|------|
| `--api matting` | 通用抠图（文件上传，返回二进制） | `POST /api/v1/matting?mattingType=6` |
| `--api matting --base64` | 通用抠图（文件上传，返回Base64） | `POST /api/v1/matting2?mattingType=6` |
| `--api matting --url` | 通用抠图（图片URL，返回Base64） | `GET /api/v1/mattingByUrl?mattingType=6` |
| `--api face-clear` | 人脸变清晰（文件上传，返回二进制） | `POST /api/v1/matting?mattingType=18` |
| `--api face-clear --base64` | 人脸变清晰（文件上传，返回Base64） | `POST /api/v1/matting2?mattingType=18` |
| `--api face-clear --url` | 人脸变清晰（图片URL，返回Base64） | `GET /api/v1/mattingByUrl?mattingType=18` |
| `--api ai-bg --submit` | AI背景更换（提交任务） | `POST /api/v1/paintAsync` |
| `--api ai-bg --query` | AI背景更换（查询结果） | `GET /api/v1/getPaintResult` |

## 2. 使用示例

```bash
# 通用抠图 — 上传文件，保存为 PNG
python scripts/tukeli.py --api matting --image product.jpg --output out.png

# 通用抠图 — 传入图片URL，获取Base64
python scripts/tukeli.py --api matting --url "https://example.com/photo.jpg"

# 通用抠图 — 裁剪空白区域，添加白色背景
python scripts/tukeli.py --api matting --image photo.jpg --crop --bgcolor FFFFFF

# 人像抠图（发丝级精度）
python scripts/tukeli.py --api matting --matting-type 1 --image portrait.jpg --output face.png

# 人脸变清晰 — 上传文件，保存高清图
python scripts/tukeli.py --api face-clear --image blurry.jpg --output hd.png

# 人脸变清晰 — 获取Base64
python scripts/tukeli.py --api face-clear --image blurry.jpg --base64

# AI背景更换 — 提交任务（需先抠图得到透明PNG）
python scripts/tukeli.py --api ai-bg --submit --image-url "https://example.com/transparent.png" --text "美丽的海滩背景"

# AI背景更换 — 查询任务结果
python scripts/tukeli.py --api ai-bg --query --task-id 375593109065861
```

## 3. 通用参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--api` | 选择API：`matting`、`face-clear`、`ai-bg` | 必填 |
| `--image` | 本地图片文件路径 | — |
| `--url` | 图片URL（使用URL模式时替代--image） | — |
| `--output` | 输出文件路径 | `data/outputs/` |
| `--base64` | 返回Base64 JSON而非二进制流 | false |
| `--crop` | 裁剪空白区域（仅matting） | false |
| `--bgcolor` | 背景颜色，十六进制（如FFFFFF） | — |
| `--output-format` | 输出格式：png、webp、jpg_75等 | png |
| `--matting-type` | 抠图类型：1人像、2物体、3头像、6通用（仅matting） | 6 |
| `--face-analysis` | 返回人脸关键点（仅matting --base64） | false |

## 4. AI背景更换专属参数

| 参数 | 说明 |
|------|------|
| `--submit` | 提交任务模式 |
| `--query` | 查询结果模式 |
| `--image-url` | 输入图片URL（提交任务时使用） |
| `--image-base64` | 输入图片Base64（提交任务时使用） |
| `--text` | 背景描述文字（提交任务时使用） |
| `--task-id` | 任务ID（查询结果时使用） |

## 5. 输出说明

图片保存在 `data/outputs/` 目录，命名格式：`{api}_{timestamp}.png`

元数据保存在 `.meta.json` 文件，包含：API类型、参数、处理时间、文件大小。

## 与其他工具集成

- **图片编辑**：先用通用抠图，再用AI背景更换生成新背景
- **头像生成**：人像抠图（mattingType=1）→ 裁剪 → 生成头像
- **照片修复**：人脸变清晰 → 通用抠图 → AI背景更换

## 限制与配额

- 支持格式：PNG、JPG、JPEG、BMP、GIF（抠图）；PNG、JPG、JPEG、BMP、WEBP（人脸变清晰）
- 最大分辨率：4096×4096 像素
- 最大文件大小：25 MB（抠图），15 MB（人脸变清晰）
- 积分消耗：
  - 抠图：15M以下 1点/张，15M~25M 2点/张
  - 人脸变清晰：2点/张
  - AI背景更换：3~12点/次（按分辨率）

## 文件说明

| 文件 | 用途 |
|------|------|
| `references/setup-guide.md` | 初始配置、API Key获取、故障排查 |
| `references/api-reference.md` | 完整接口文档、参数说明、响应格式、错误码 |
| `scripts/tukeli.py` | 主调用脚本 |
| `scripts/config.py` | 配置管理（API Key、端点、限制） |
| `scripts/requirements.txt` | Python依赖 |
