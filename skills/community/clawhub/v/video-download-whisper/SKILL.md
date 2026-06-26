---
name: video-download
description: 下载无法直接访问的视频网站内容（如B站、YouTube等），提取音频后用Whisper转录成文字。适用场景：用户要求分析某个视频内容，但链接被封锁无法直接访问；需要获取视频完整文字稿进行深度分析。
metadata: {"openclaw":{"emoji":"🎬","requires":{"bins":["yt-dlp","ffmpeg","whisper"]},"os":["darwin","linux","win32"]}}
---

# 视频下载与转录工作流

## 适用场景

- 视频链接被封锁（如b23.tv短链接）
- 无法直接访问视频页面获取内容
- 需要获取视频完整文字稿进行深度分析
- **无需翻墙即可下载YouTube等被限制的平台**

## 支持的平台

### 🌏 中国平台
| 平台 | 说明 | 命令示例 |
|------|------|----------|
| **B站/哔哩哔哩** | 视频、番剧、音频、收藏夹 | `yt-dlp "https://www.bilibili.com/video/BVxxx"` |
| **抖音/Douyin** | 短视频 | `yt-dlp "https://www.douyin.com/video/xxx"` |
| **小红书/XiaoHongShu** | 图文/视频笔记 | `yt-dlp "https://www.xiaohongshu.com/explore/xxx"` |
| **快手** | 短视频 | `yt-dlp "https://www.kuaishou.com/short-video/xxx"` |
| **微博视频** | 微博视频 | `yt-dlp "https://weibo.com/xxx"` |
| **美拍/Meipai** | 视频 | `yt-dlp "https://www.meipai.com/media/xxx"` |
| **爱奇艺** | iQiyi视频 | `yt-dlp "https://www.iq.com/play/xxx"` |
| **优酷** | Youku视频 | `yt-dlp "https://v.youku.com/v_show/id_xxx"` |
| **百度视频** | BaiduVideo | `yt-dlp "https://video.baidu.com/v/xxx"` |

### 🌍 国际平台
| 平台 | 说明 | 命令示例 |
|------|------|----------|
| **YouTube** | 视频/Shorts/直播 | `yt-dlp "https://www.youtube.com/watch?v=xxx"` |
| **TikTok** | 短视频 | `yt-dlp "https://www.tiktok.com/@user/video/xxx"` |
| **Twitter/X** | 视频 | `yt-dlp "https://twitter.com/user/status/xxx"` |
| **Instagram** | Reels/视频 | `yt-dlp "https://www.instagram.com/reel/xxx"` |
| **Facebook** | 视频 | `yt-dlp "https://www.facebook.com/user/videos/xxx"` |
| **Reddit** | 视频/直播 | `yt-dlp "https://www.reddit.com/r/subreddit/comments/xxx"` |
| **Vimeo** | 视频 | `yt-dlp "https://vimeo.com/xxx"` |
| **Twitch** | 直播/录像 | `yt-dlp "https://www.twitch.tv/videos/xxx"` |

### 📊 短视频平台
- **抖音/快手/小红书** - 国内三大短视频平台
- **TikTok** - 国际版抖音
- **YouTube Shorts** - YouTube短视频
- **Instagram Reels** - Instagram短视频

**总计支持：1858+ 个平台**

## 工作流程

```
获取视频链接
    ↓
解析为直链 (curl -sI 获取重定向URL)
    ↓
下载视频 (yt-dlp)
    ↓
提取音频 (ffmpeg)
    ↓
转录为文字 (Whisper)
    ↓
输出文字稿
```

## 第一步：解析视频直链

### B站短链接解析

```bash
# 获取B站直链（BV号）
curl -sI "https://b23.tv/短链接" 2>/dev/null | grep -i location

# 获取完整视频信息（包含cid）
curl -s "https://api.bilibili.com/x/web-interface/view?bvid=BV号"
```

### 获取所有视频的BV号

```bash
for bv in BV1xxx BV2xxx; do
  echo "=== $bv ==="
  curl -sI "https://b23.tv/短链接" | grep -i location
done
```

## 第二步：下载视频

### 通用下载命令

```bash
# 直接下载任意平台视频
yt-dlp -o "/tmp/video.mp4" "视频URL"

# 下载并指定格式
yt-dlp -f "best" -o "/tmp/video.mp4" "视频URL"
```

### 各平台下载示例

```bash
# B站视频
yt-dlp -o "/tmp/bilibili.mp4" "https://www.bilibili.com/video/BV1xxx"

# YouTube视频
yt-dlp -o "/tmp/youtube.mp4" "https://www.youtube.com/watch?v=xxx"

# YouTube Shorts
yt-dlp -o "/tmp/shorts.mp4" "https://www.youtube.com/shorts/xxx"

# TikTok视频
yt-dlp -o "/tmp/tiktok.mp4" "https://www.tiktok.com/@user/video/xxx"

# 抖音视频
yt-dlp -o "/tmp/douyin.mp4" "https://www.douyin.com/video/xxx"

# 小红书笔记
yt-dlp -o "/tmp/xhs.mp4" "https://www.xiaohongshu.com/explore/xxx"
```

### 安装依赖

```bash
# yt-dlp 安装
pip3 install yt-dlp

# ffmpeg 安装 (macOS)
brew install ffmpeg

# Whisper 安装
pip3 install -U openai-whisper
```

### 下载B站视频

```bash
# 下载视频到指定目录
yt-dlp -o "/tmp/video.mp4" "https://www.bilibili.com/video/BV号"

# 下载并自动合并音视频
yt-dlp -f "bv+ba" -o "/tmp/video.mp4" "https://www.bilibili.com/video/BV号"
```

### 常用选项

| 选项 | 说明 |
|------|------|
| `-o path` | 输出路径 |
| `--cookies-from-browser` | 使用浏览器cookies（会员内容） |
| `-f format` | 指定格式 |

## 第三步：提取音频

```bash
# 提取 wav 格式（Whisper推荐）
ffmpeg -i /tmp/video.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 /tmp/audio.wav -y

# 提取 mp3 格式（体积更小）
ffmpeg -i /tmp/video.mp4 -vn -acodec libmp3lame -ar 16000 -ac 1 /tmp/audio.mp3 -y
```

## 第四步：Whisper转录

```bash
# 使用base模型（快速）
whisper /tmp/audio.wav --model base --output_format txt --output_dir /tmp

# 使用medium模型（更准确，中文推荐）
whisper /tmp/audio.wav --model medium --output_format txt --output_dir /tmp

# 输出到指定文件
whisper /tmp/audio.wav --model medium --output_format txt --output_dir ~/workspace
```

### 模型选择

| 模型 | 速度 | 准确率 | 适用场景 |
|------|------|---------|----------|
| tiny | 最快 | 最低 | 快速测试 |
| base | 快 | 中等 | 一般用途 |
| small | 中等 | 较高 | 中文推荐 |
| medium | 慢 | 高 | 重要内容 |
| large | 最慢 | 最高 | 精度要求极高 |

### Whisper路径

由于安装位置可能不在PATH中，使用完整路径：

```bash
# Python 3.9 用户
/Users/yanghaohan/Library/Python/3.9/bin/whisper

# 或添加到PATH
export PATH="/Users/yanghaohan/Library/Python/3.9/bin:$PATH"
```

## 第五步：处理结果

转录完成后，文字稿会保存在指定目录的 `.txt` 文件中。

查看结果：

```bash
cat /tmp/audio.txt
```

## 完整执行示例

```bash
# 1. 解析BV号
BV=$(curl -sI "https://b23.tv/短链接" | grep -i location | grep -oE 'BV[a-zA-Z0-9]+' | head -1)
echo "BV号: $BV"

# 2. 下载视频
yt-dlp -o "/tmp/video.mp4" "https://www.bilibili.com/video/$BV"

# 3. 提取音频
ffmpeg -i /tmp/video.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 /tmp/audio.wav -y

# 4. 转录
whisper /tmp/audio.wav --model medium --output_format txt --output_dir /tmp

# 5. 查看结果
cat /tmp/audio.txt
```

## 脚本使用

```bash
# 添加执行权限
chmod +x ~/.openclaw/workspace/skills/video-download/scripts/*.sh

# 第一步：下载B站视频并提取音频
~/.openclaw/workspace/skills/video-download/scripts/bilibili-download.sh "b23.tv/xxx" /tmp

# 第二步：转录
~/.openclaw/workspace/skills/video-download/scripts/transcribe.sh /tmp/audio_BVxxx.wav small /tmp
```

## 注意事项

1. **B站视频可能没有字幕** - 需要通过Whisper转录
2. **会员内容** - 需要提供cookies或cookies-from-browser选项
3. **下载速度** - 取决于网络状况，通常5-10分钟完成一期视频
4. **Whisper模型** - 首次使用会下载模型（约139MB），medium模型需要约3GB磁盘空间

## 故障排除

### yt-dlp下载失败

```bash
# 更新到最新版本
pip3 install -U yt-dlp

# 使用cookies（如果有）
yt-dlp --cookies /path/to/cookies.txt "URL"
```

### Whisper模型校验失败

```bash
# 删除损坏的模型缓存
rm -rf ~/.cache/whisper/*

# 重新下载
whisper /tmp/audio.wav --model base
```

### Python版本问题

```bash
# 检查Python版本
python3 --version

# Whisper需要Python 3.10+
# 如果版本过低，考虑使用Docker或其他环境
```
