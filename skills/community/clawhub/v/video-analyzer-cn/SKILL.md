---
name: video-analyzer
description: >
  视频内容分析工具。支持B站、抖音、今日头条视频链接。
  发送视频URL → 自动下载 → 抽帧 → 本地AI逐帧识别 → 综合总结。
  使用本地minicpm-v模型，无需云端API。
triggers:
  - 视频/分析/b站/抖音/头条/bilibili/douyin/toutiao/video
---

# Video Analyzer — 视频内容分析

## 支持平台

| 平台 | URL特征 | 下载方式 |
|------|---------|---------|
| B站 | b23.tv / bilibili.com | yt-dlp 直接下载 |
| 抖音 | v.douyin.com / douyin.com | 浏览器提取URL → Python带Referer下载 |
| 今日头条 | m.toutiao.com / toutiao.com | yt-dlp 指定格式下载 |

## 完整流程

```
URL → 识别平台 → 下载视频 → ffmpeg抽帧 → minicpm-v逐帧识别 → 综合总结
```

## 使用方式

用户发送视频链接，agent 自动执行以下步骤：

### Step 1: 识别平台并下载

读取 `references/download.md` 获取各平台下载脚本。

### Step 2: 抽帧

```bash
# 设置ffmpeg路径
$env:Path = "D:\AI\ffmpeg;$env:Path"

# 抽帧（每N秒一帧，根据视频长度调整）
# 短视频(<60s): fps=1/3 (每3秒一帧)
# 中视频(1-5min): fps=1/5 (每5秒一帧)  
# 长视频(>5min): fps=1/10 (每10秒一帧)
ffmpeg -i <video.mp4> -vf "fps=1/5,scale=640:-1" -q:v 3 <output_dir>/frame_%03d.jpg -y
```

**关键参数**：
- `scale=640:-1` 缩小分辨率，原图会超时
- `-q:v 3` JPEG质量（1最好，31最差，3够用）
- 帧数控制在 5-30 帧之间最佳

### Step 3: 逐帧识别

读取 `references/analyze.py` 脚本，用 minicpm-v 逐帧识别。

### Step 4: 综合总结

收集所有帧的描述，综合输出视频内容总结。

## 环境依赖

| 工具 | 路径 | 用途 |
|------|------|------|
| ffmpeg | `D:\AI\ffmpeg\` | 视频抽帧 |
| yt-dlp | 系统PATH | B站/头条下载 |
| minicpm-v | ollama本地 | 图片识别 |
| Python | 系统PATH | 抖音下载+分析脚本 |
| Chrome | 系统安装 | 抖音视频URL提取 |

## 临时文件

所有临时文件存放在 `C:\Users\39535\.openclaw\workspace\tmp\`：
- 视频文件: `*.mp4`
- 抽帧图片: `frame_*.jpg` / `dy_frame_*.jpg` / `tt_frame_*.jpg`
- 分析脚本: `analyze_*.py` / `douyin_download*.py`

分析完成后可清理临时文件。

## 注意事项

- 抖音需要Chrome浏览器打开页面提取视频URL（需浏览器MCP）
- 抖音视频URL有时效性，提取后需立即下载
- Chrome v20 cookies加密问题，不能用 `--cookies-from-browser chrome`
- 长视频帧数多时处理时间较长（每帧约20-30秒）
- 内存紧张时优先清理其他进程
