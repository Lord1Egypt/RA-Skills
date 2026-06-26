---
name: douyin-transcribe
description: 全自动抖音视频下载 + 语音转文字管道。当用户发送抖音链接并要求转写文字、提取字幕、语音转文本时使用。触发词包括"抖音转写"、"抖音文字"、"抖音转文本"、"抖音字幕"、"douyin transcribe"。
---

# Douyin Video Transcribe Skill

全自动抖音视频下载 + 语音转文字管道。

## 功能

输入抖音链接 → 自动解析直链 → 下载视频 → 提取音频 → 本地语音转文字 → 输出文稿

## 依赖安装（首次需要）

```bash
# 1. 安装 coli（语音转文字引擎）
npm install -g @marswave/coli

# 2. 安装 sensevoice 模型（首次自动下载，约60MB，需代理访问GitHub）
# 模型下载后保存在 ~/.coli/models/

# 3. ffmpeg（音频处理，系统已有）

# 4. Node.js（用于视频URL拦截脚本）
```

## 使用方法

### 基本用法（仅转写，不上传飞书）

```
python3 ~/.openclaw/skills/douyin-transcribe/scripts/transcribe.py \
  --url "https://v.douyin.com/xxxxx"
```

### 指定输出目录

```
python3 ~/.openclaw/skills/douyin-transcribe/scripts/transcribe.py \
  --url "https://v.douyin.com/xxxxx" \
  --output-dir /tmp/my_videos
```

### 完整用法（转写 + 上传飞书）

```
python3 ~/.openclaw/skills/douyin-transcribe/scripts/transcribe.py \
  --url "https://v.douyin.com/xxxxx" \
  --folder-token 飞书云盘文件夹token \
  --space-id 飞书知识库space_id
```

### 参数说明

| 参数 | 说明 |
|------|------|
| `--url, -u` | 抖音视频链接（必填） |
| `--output-dir, -o` | 临时文件目录，默认 /tmp |
| `--folder-token, -f` | 飞书云盘文件夹 token |
| `--space-id, -s` | 飞书知识库 space ID |
| `--no-feishu` | 跳过飞书上传统步 |
| `--cleanup` | 完成后删除本地临时文件（视频+音频）|

## 输出

- 终端打印完整转录文本
- 本地保存 `transcript.txt` 到 `--output-dir`
- 视频/音频本地文件在 `--output-dir`（除非指定 `--cleanup`）

## 技术流程

```
抖音链接
  └─→ Node.js (puppeteer-core + Chrome)
  │     └─→ 打开 hellotik.app
  │     └─→ 填入链接，点击解析
  │     └─→ 拦截网络请求，获取CDN直链
  └─→ curl 下载视频（直链）
  └─→ ffmpeg 提取音频（WAV 16kHz单声道）
  └─→ coli asr --model sensevoice（本地ASR，约1-3分钟）
  └─→ 输出转录文本 + 可选飞书上传统步
```

## 模型说明

- **sensevoice**：阿里开源多语言ASR，支持中文/英文/日语/韩语/粤语，约60MB
- 本地运行，无需API Key，完全离线
- Intel Celeron J1900 上处理 1分钟音频约需 1-2 分钟

## 飞书上传说明

如需上传到飞书，需要在调用时传入 `--folder-token` 和 `--space-id`。

当前已配置：
- 视频素材库 folder_token: `RCIDfArx5lgZTIdO1SAcDU37n0e`
- 视频文案库 space_id: `7622229283829763274`

## 常见问题

**Q: 提示"无法获取视频直链"**  
A: CDN链接有时效（几分钟），多试几次即可。或 hellotik 解析失败，稍后重试。

**Q: 转写时间太长**  
A: sensevoice 模型较大，处理速度依赖CPU。可改用 `whisper-tiny` 模型（更快但仅英文）。

**Q: 视频很短/没有声音**  
A: 部分抖音视频是纯音乐或图片，语音转写会失败或输出很短。
