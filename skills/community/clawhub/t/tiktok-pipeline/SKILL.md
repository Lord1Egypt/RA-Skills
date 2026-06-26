---
name: tikhub
description: TikHub API 多平台数据爬取工具，支持抖音/TikTok/B站等。当用户提到：(1) 爬取抖音/TikTok/B站视频或评论；(2) 获取用户信息/粉丝列表；(3) 批量下载无水印视频；(4) 抖音链接转文字（下载→音频→Whisper pipeline）；(5) 调用 TikHub API。
---

# TikHub API Skill (v4)

基于 TikHub API 的多平台数据爬取工具。

## 实测经验（重要）

| 经验 | 说明 |
|------|------|
| **视频下载必须用付费端点** | 免费 `web/fetch_video_high_quality_play_url` 返回空，用 `app/v3/fetch_video_high_quality_play_url` |
| **视频直链需带请求头** | 带 `Referer: https://www.douyin.com/` + `User-Agent`，否则 403 |
| **国内用户换域名** | 用 `api.tikhub.dev` 代替 `api.tikhub.io`（不需要代理）|
| **API Key 暴露后重置** | https://user.tikhub.io 控制台重新生成 |
| **转写首选 mlx-whisper** | Apple Silicon GPU 加速，14分钟音频仅需40秒 |

## 环境准备

```bash
pip install requests openai-whisper mlx-whisper  # mlx-whisper 支持 Apple GPU
brew install ffmpeg                              # 音频提取需要
```

**API Key**: https://user.tikhub.io 获取

## 核心函数

```python
from tikhub import (
    set_api_key,                # 设置 API Key
    get_video_info,             # 视频信息（免费）
    get_video_info_by_url,      # 分享链接→视频信息（免费）
    parse_aweme_id,            # 从 URL 解析 aweme_id
    get_high_quality_url,      # 获取无水印直链（付费）
    download_video,            # 下载视频（付费）
    batch_download,             # 批量下载
    get_all_comments,          # 全量评论（免费）
    get_user_videos,           # 用户视频列表
    extract_audio,             # 视频→音频（ffmpeg）
    mlx_whisper_transcribe,     # ★ Apple GPU 转写（首选，40秒/small）
    whisper_transcribe,         # CPU Whisper（备用，openai-whisper）
    full_pipeline_douyin_to_text,  # 一键 pipeline
    check_balance,              # 查询余额
)
```

## 常用调用

```python
# 设置 Key（国内用 use_china_domain=True）
set_api_key("your_key", use_china_domain=True)

# ============ 视频信息（免费）============
info = get_video_info("7618502770185833766")
desc = info["data"]["aweme_detail"]["desc"]
author = info["data"]["aweme_detail"]["author"]["nickname"]

# 从抖音 URL 直接解析
aweme_id = parse_aweme_id("https://v.douyin.com/xxxxx")

# ============ 评论（免费）============
comments = get_all_comments("7618502770185833766", max_count=100)
for c in comments:
    print(c["text"], c["user"]["nickname"])

# ============ 视频下载（付费，需余额）============
# 先查余额
balance = check_balance()
print(balance["user_data"]["balance"])  # 余额

# 下载视频
path = download_video("7618502770185833766", output_dir="./downloads")

# ============ 完整 pipeline（下载→音频→转写）============
# GPU 加速版（推荐，Apple Silicon）
```python
text_path = full_pipeline_douyin_to_text(
    "7618502770185833766",
    use_gpu=True,          # 用 mlx-whisper（Apple GPU，40秒/small）
)
print(open(text_path).read())
```

CPU 备用版（无 Apple GPU 时）：
```python
text_path = full_pipeline_douyin_to_text(
    "7618502770185833766",
    use_gpu=False,         # 用 openai-whisper（CPU，较慢）
    whisper_model="small"
)
```

# ============ 单独调用 GPU 转写（已有音频文件）============
```python
from tikhub import mlx_whisper_transcribe
text = mlx_whisper_transcribe(
    "/path/to/audio.wav",
    model_size="small",   # small 速度最快，medium 精度更高
    language="zh"         # 中文
)
print(text)
```

## aweme_id 解析

从链接提取（支持以下格式）：
- `https://v.douyin.com/xxxxx` → 需用 `get_video_info_by_url` 获取
- `https://www.douyin.com/video/7618502770185833766` → 直接提取
- `https://www.douyin.com/jingxuan?modal_id=7618502770185833766` → 从 modal_id 提取

```python
aweme_id = parse_aweme_id("https://www.douyin.com/jingxuan?modal_id=7618502770185833766")
# → "7618502770185833766"
```

## 批量 CLI 用法

```bash
# 查询余额
python batch.py balance --api-key YOUR_KEY

# 批量下载
python batch.py download --api-key YOUR_KEY --aweme-ids 7618502770185833766,7618502770185833767

# 采集评论
python batch.py comments --api-key YOUR_KEY --aweme-id 7618502770185833766 --max 100

# 完整 pipeline（URL 文件，每行一个链接）
python batch.py pipeline --api-key YOUR_KEY --urls urls.txt
```

## 端点速查

| 功能 | 端点 | 免费/付费 |
|------|------|-----------|
| 视频信息 | `/douyin/web/fetch_one_video` | 免费 |
| 评论列表 | `/douyin/web/fetch_video_comments` | 免费 |
| 无水印直链 | `/douyin/app/v3/fetch_video_high_quality_play_url` | **付费** |
| 用户信息 | `/douyin/web/fetch_user_profile_by_uid` | 免费 |
| 用户视频列表 | `/douyin/web/fetch_user_post_videos` | 免费 |
| B站视频信息 | `/bilibili/web/fetch_one_video` | 免费 |

## 完整 Pipeline 输出示例

```
Step 1: 下载视频 → 252MB MP4
Step 2: 提取音频 → 27MB WAV (16kHz mono)
Step 3: mlx-whisper 转写 → 文字稿（Apple GPU，small 模型 14分钟音频约 40秒）
```

## 注意事项

- **频率限制**：免费额度用完会 429，批量加 `time.sleep`
- **视频下载计费**：每次调用付费端点都会被计费，注意余额
- **转写速度**：mlx-whisper（Apple GPU）> openai-whisper small（CPU）> openai-whisper medium（CPU）
- **faster-whisper 不支持 Apple MPS**：不要用！
- **API 文档**：https://api.tikhub.io/docs（Swagger UI）
