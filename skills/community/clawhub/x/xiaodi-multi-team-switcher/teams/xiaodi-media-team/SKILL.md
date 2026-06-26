---
name: xiaodi-media-team
description: 多媒体处理团队 - 视频剪辑/压缩、图片处理、音频转码、字幕生成
version: 1.0.0
author: xiaodi
homepage: https://github.com/openclaw/xiaodi-media-team
metadata:
  openclaw:
    emoji: 🎬
    requires:
      bins: [ffmpeg, convert]
    install:
      - id: ffmpeg
        kind: apt
        formula: ffmpeg
        bins: [ffmpeg, ffprobe]
        label: Install ffmpeg
      - id: imagemagick
        kind: apt
        formula: imagemagick
        bins: [convert, identify]
        label: Install ImageMagick
---

# 🎬 小弟多媒体团队

专业的多媒体处理团队，提供视频剪辑、图片处理、音频转码、字幕生成等服务。

## 📋 团队成员

| 角色 | 图标 | 功能 | 工具 |
|------|------|------|------|
| 视频剪辑师 | 🎬 | 视频剪辑/压缩/转码 | ffmpeg |
| 视频创作师 | 🎥 | AI视频生成 | Runway/Pika/可灵/Sora/即梦 |
| 字幕生成器 | 📝 | 自动生成字幕 | whisper + ffmpeg |
| 图片处理师 | 🖼️ | 图片压缩/转换/缩放 | ImageMagick |
| AI绘图师 | 🎨 | AI生成图片 | DALL-E / SD |
| 音频处理师 | 🎵 | 音频转码/提取 | ffmpeg |
| 质量检查员 | 📊 | 检查文件质量 | ffprobe + identify |

---

## 🚀 快速开始

### 视频压缩

```
压缩这个视频 /path/to/video.mp4
```

```bash
{baseDir}/scripts/video_compress.sh /path/to/video.mp4 --output /tmp/compressed.mp4
```

### 视频提取帧

```
提取视频第10秒的帧 /path/to/video.mp4
```

```bash
{baseDir}/scripts/video_frame.sh /path/to/video.mp4 --time 00:00:10 --output /tmp/frame.jpg
```

### 图片压缩

```
压缩这张图片 /path/to/image.png
```

```bash
{baseDir}/scripts/image_compress.sh /path/to/image.png --output /tmp/compressed.jpg
```

### 音频提取

```
从视频中提取音频 /path/to/video.mp4
```

```bash
{baseDir}/scripts/audio_extract.sh /path/to/video.mp4 --output /tmp/audio.mp3
```

### 字幕生成

```
给这个视频生成字幕 /path/to/video.mp4
```

```bash
{baseDir}/scripts/subtitle_gen.sh /path/to/video.mp4 --output /tmp/subtitle.srt
```

### AI视频生成

```
生成一个视频：猫咪在阳光下打盹
```

```bash
{baseDir}/scripts/video_gen.sh "猫咪在阳光下打盹" --provider kling
```

**支持的平台**：
- `kling` - 可灵AI (快手) 🇨🇳 推荐
- `runway` - Runway Gen-3 🌍
- `pika` - Pika Labs 🌍
- `sora` - OpenAI Sora 🌍
- `jiming` - 即梦AI (字节) 🇨🇳

---

## 📁 支持的格式

### 视频
- 输入: mp4, avi, mov, mkv, webm, flv
- 输出: mp4 (默认), webm, mov

### 图片
- 输入: jpg, jpeg, png, gif, webp, bmp
- 输出: jpg (默认), png, webp

### 音频
- 输入: mp3, wav, aac, flac, ogg, m4a
- 输出: mp3 (默认), wav, aac

### 字幕
- 输出: srt (默认), vtt, ass

---

## ⚙️ 配置

配置文件: `{baseDir}/config.json`

```json
{
  "settings": {
    "max_file_size_mb": 500,
    "output_dir": "/tmp/xiaodi-media",
    "cleanup_temp": true
  }
}
```

---

## 🔄 工作流

### video_compress (视频压缩)
1. 质量检查员检查视频
2. 视频剪辑师压缩
3. 质量检查员验证输出

### video_create (视频生成)
1. 视频创作师调用AI平台生成视频
2. 质量检查员验证输出

### video_subtitle (字幕生成)
1. 字幕生成器提取音频并生成字幕
2. 视频剪辑师嵌入字幕
3. 质量检查员验证输出

### image_batch (图片批量处理)
1. 图片处理师处理图片
2. 质量检查员验证输出

### audio_extract (音频提取)
1. 音频处理师提取音频
2. 质量检查员验证输出

---

## 📝 使用示例

### 压缩视频到 50MB 以内
```
把这个视频压缩到 50MB 以内 /path/to/video.mp4
```

### 批量压缩图片
```
批量压缩这个文件夹的图片 /path/to/images/
```

### 提取视频片段
```
提取视频第 1 分钟到 2 分钟的片段 /path/to/video.mp4
```

### 转换图片格式
```
把这张 PNG 转成 JPG /path/to/image.png
```

---

## 🔧 技术规格

| 操作 | 工具 | 默认参数 |
|------|------|---------|
| 视频编码 | ffmpeg libx264 | CRF 23, preset medium |
| 音频编码 | ffmpeg aac | 192kbps |
| 图片质量 | ImageMagick | 85% |
| 字幕模型 | whisper medium | 中文优化 |

---

## ⚠️ 注意事项

1. 大文件处理需要较长时间，请耐心等待
2. 临时文件会自动清理
3. 输出文件默认保存在 `/tmp/xiaodi-media/`

---

*团队成员: 视频剪辑师 🎬 | 字幕生成器 📝 | 图片处理师 🖼️ | AI绘图师 🎨 | 音频处理师 🎵 | 质量检查员 📊*