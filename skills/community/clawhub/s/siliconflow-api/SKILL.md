---
name: siliconflow-api
description: SiliconFlow（硅基流动）AI 生成能力集成。支持文生图、图生图、文生视频、图生视频、文字转语音。当用户需要生成图片、视频、语音时使用此技能。首次使用需运行 setup 配置自己的 API Key（在 siliconflow.cn 注册获取）。国内支付方式（微信/支付宝），无需海外银行卡。
---

# SiliconFlow API

硅基流动 AI 生成平台，支持多种生成模型，国内直接使用。

## 配置（首次使用必须配置）

1. 注册 [siliconflow.cn](https://siliconflow.cn) 获取 API Key
2. 运行配置命令输入 Key：
```bash
bash scripts/sf_api.sh setup
```
⚠️ API Key 保存在本地 `.sf-config.json`，不会泄露到技能包中。

## 可用命令

| 功能 | 命令 | 说明 |
|------|------|------|
| 文生图 | `t2i <提示词> [尺寸] [模型] [输出路径]` | 默认1024x1024，模型Kwai-Kolors/Kolors |
| 图生图 | `i2i <图片路径> <提示词> [输出路径]` | 编辑已有图片 |
| 文生视频 | `t2v <提示词> [时长] [输出路径]` | 默认5秒，Wan2.2模型 |
| 图生视频 | `i2v <图片路径> <提示词> [时长] [输出路径]` | 上传图片生成视频 |
| 查询视频 | `vs <任务ID> [输出路径]` | 异步任务状态查询 |
| 文字转语音 | `tts <文本> [音色] [输出路径]` | CosyVoice2 |
| 列出模型 | `models` | 查看可用模型列表 |

## 快速开始

脚本在 `scripts/sf_api.sh`，所有命令通过它执行。

```bash
cd ~/.openclaw/workspace/skills/siliconflow-api

# 文生图
bash scripts/sf_api.sh t2i "一个穿深蓝色西装的老板坐在办公室，自信微笑，4K写实"

# 图生图（用老板照片生成成熟版）
bash scripts/sf_api.sh i2i /root/.openclaw/workspace/assets/laoban-photo.jpg "成熟稳重企业家风格，深蓝色西装，办公室背景"

# 文生视频
bash scripts/sf_api.sh t2v "一个穿西装的商人在办公室微笑" 5

# 图生视频（用老板照片生成视频）
bash scripts/sf_api.sh i2v /root/.openclaw/workspace/assets/laoban-photo.jpg "微笑看向镜头，轻轻点头" 5

# 语音生成
bash scripts/sf_api.sh tts "你好，我是做软件开发的，这是我们公司的产品"
```

## 图片生成

### 推荐模型
- `Kwai-Kolors/Kolors`（默认）— 中文理解好，写实风格强
- `Qwen/Qwen-Image` — 通义千问，质量高

### 常用尺寸
- `1024x1024`（默认方图）
- `1216x832`（横图，适合16:9）
- `832x1216`（竖图，适合9:16手机）

### 提示词技巧
- 中文提示词效果更好
- 加 `4K`, `写实`, `电影级` 等词提升画质
- 加 `浅景深`, `柔和自然光` 等摄影术语

## 视频生成

### 模型
- `Wan-AI/Wan2.2-T2V-A14B` — 文生视频
- `Wan-AI/Wan2.2-I2V-A14B` — 图生视频（上传参考图）

### 注意
- 视频生成是异步任务，提交后需轮询等待
- 生成时间约2-10分钟（排队+推理）
- 视频最长15秒
- 输出格式为 MP4

## 语音合成

### 模型
- `FunAudioLLM/CosyVoice2-0.5B` — 中文语音合成

### 音色选项
- 中文男声
- 中文女声

## 注意事项

- 所有生成都会消耗账户余额
- 图片生成约0.1-0.3元/次
- 视频生成较贵，约0.5-2元/次
- 语音合成约0.01元/次
- 生成结果保存在 `/tmp/` 目录，用完后清理
