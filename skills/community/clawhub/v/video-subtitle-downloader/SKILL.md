# Video Subtitle Downloader - 视频字幕下载器

## 简介

一键下载 YouTube/B站 等平台的视频字幕/CC字幕，并自动生成时间轴索引。

**适用场景**：学习笔记、外语翻译、内容审核、视频搬运

## 功能特性

- ✅ 支持 YouTube、B站、Twitter 等1000+平台
- ✅ 下载字幕（自动字幕 + 手动字幕）
- ✅ 生成 SRT/JSON/TXT 格式
- ✅ 视频时长超过30分钟自动分段
- ✅ 支持GPU加速转录

## 使用方式

### 触发词
- "下载字幕"
- "提取视频文字"
- "视频转文字"

### 输入
- 视频URL或视频ID
- 期望的输出格式（srt/json/txt）

### 输出
- 字幕文件路径
- 字幕总时长
- 字幕条数统计

## 技术栈

- **yt-dlp**：视频下载 + 字幕提取
- **faster-whisper**：GPU加速语音转文字
- **Python**：核心处理脚本

## 安装依赖

```bash
pip install yt-dlp faster-whisper
```

## 使用示例

```bash
# 下载YouTube字幕
python scripts/download_subtitle.py "https://www.youtube.com/watch?v=xxx" --format srt

# 批量下载
python scripts/batch_download.py urls.txt --format json
```

## 定价策略

| 版本 | 价格 | 说明 |
|------|------|------|
| 免费版 | ¥0 | 每月5个视频 |
| 专业版 | ¥19/月 | 无限使用 + GPU加速 |
| 企业版 | ¥99/月 | API接口 + 批量处理 |

## 竞品对比

| 功能 | 本技能 | 竞品A | 竞品B |
|------|--------|-------|-------|
| 平台数 | 1000+ | 50+ | 20+ |
| 中文支持 | ✅ | ❌ | ✅ |
| GPU加速 | ✅ | ❌ | ❌ |
| 价格 | ¥19/月 | ¥50/月 | ¥30/月 |

## 更新日志

- v1.0 (2026-04-04)：首发版本
