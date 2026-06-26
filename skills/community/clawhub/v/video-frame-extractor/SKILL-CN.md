```md
---
name: video-frame-extractor
description: 当需要从视频文件中提取帧时，应使用此技能，例如从视频生成关键帧序列、按时间间隔创建视频缩略图，或为分析准备视频帧。触发场景包括诸如“从视频提取帧”、“每 N 秒采样一帧”、“为视频分析提取关键帧”或“生成视频缩略图序列”等请求。
---

# 视频帧提取器

## 概述

此技能指导 LLM 代理使用 FFmpeg 从视频文件中提取帧。它提供了完整的视频帧提取工作流，包括环境设置、参数配置和命令执行。

**主要方法：FFmpeg**（快速且可靠）
**备用方法：OpenCV**（当 FFmpeg 不可用时）

## 工作流

### 步骤 1：验证 FFmpeg 是否已安装

在提取帧之前，先检查 FFmpeg 是否已安装：

```bash
ffmpeg -version
```

如果 FFmpeg 未安装，请参阅下方的 **FFmpeg 安装** 部分。

### 步骤 2：确定提取参数

在提取帧之前，LLM 必须与用户确认以下参数：

| 参数 | 说明 | 示例 |
|-----------|-------------|---------|
| **output_path** | 保存提取帧的目录 | 默认路径 `./tmp/video_name/frames` |
| **frame_rate** | 每秒提取的帧数 | `0.25`（每 4 秒 1 帧） |
| **scale** | 短边缩放目标像素值（可选） | `640`（短边 → 640px） |

**参数计算指南：**
- 若要每 X 秒提取 1 帧：`frame_rate = 1/X`
- 示例：每 4 秒 1 帧 → `frame_rate = 0.25`
- 示例：每 10 秒 1 帧 → `frame_rate = 0.1`
- 示例：每秒 1 帧 → `frame_rate = 1`

### 步骤 3：执行 FFmpeg 命令

生成并执行 FFmpeg 命令：

**基础命令（不缩放）：**
```bash
ffmpeg -hide_banner -loglevel error -i "{video_path}" -vf "fps={frame_rate}" -fps_mode vfr -q:v 2 -f image2 "{output_path}/%06d.jpg"
```

**带短边缩放（推荐用于分析）：**
```bash
ffmpeg -hide_banner -loglevel error -thread_queue_size 512 -i "{video_path}" -vf "fps={frame_rate},scale='if(gt(iw,ih),-2,{scale}):if(gt(iw,ih),{scale},-2)':flags=lanczos" -fps_mode vfr -q:v 2 -f image2 -atomic_writing 1 "{output_path}/%06d.jpg"
```

**参数说明：**
| 标志 | 用途 |
|------|---------|
| `-hide_banner` | 隐藏构建信息 |
| `-loglevel error` | 安静模式，仅显示错误 |
| `-thread_queue_size 512` | 为大文件增大线程队列 |
| `-vf "fps={rate}"` | 设置帧提取速率 |
| `-fps_mode vfr` | 可变帧率模式（跳过重复帧） |
| `-q:v 2` | JPEG 质量（1-31，值越小质量越高） |
| `-atomic_writing 1` | 原子写入文件（防止损坏） |
| `%06d.jpg` | 顺序命名：000001.jpg、000002.jpg... |

### 步骤 4：验证输出

提取完成后，验证输出：
- 统计帧数：`ls {output_path}/*.jpg | wc -l`
- 检查帧文件大小：`ls -lh {output_path}/*.jpg | head -5`

## FFmpeg 安装

### Windows

**选项 1：winget（推荐）**
```powershell
winget install ffmpeg
```

**选项 2：Chocolatey**
```powershell
choco install ffmpeg
```

**选项 3：手动下载**
1. 从以下地址下载：https://www.gyan.dev/ffmpeg/builds/
2. 解压到一个固定位置（例如：`C:\tools\ffmpeg`）
3. 添加到 PATH：`setx PATH "$PATH;C:\tools\ffmpeg\bin`
4. 重启终端

**验证安装：**
```powershell
ffmpeg -version
```

### Linux（Ubuntu/Debian）

```bash
sudo apt update
sudo apt install ffmpeg
```

**验证安装：**
```bash
ffmpeg -version
```

### Linux（CentOS/RHEL/Fedora）

```bash
sudo dnf install ffmpeg
```

### macOS

```bash
brew install ffmpeg
```

## 常见使用场景

### 每 4 秒提取 1 帧，并缩放到 640px
```
frame_rate = 0.25
scale = 640
```

### 每 10 秒提取 1 帧，保持原始尺寸
```
frame_rate = 0.1
scale = 0 (no resize)
```

### 对一个 10 分钟视频按每秒 1 帧提取（共 600 帧）
```
frame_rate = 1
video_duration = 600 seconds
expected_frames = 600
```

## 输出目录结构

提取的帧按顺序命名保存：
```
output_path/
├── 000001.jpg
├── 000002.jpg
├── 000003.jpg
└── ...
```

顺序命名（`%06d`）可确保无论原始帧编号如何，帧始终按时间顺序排列。

## 错误处理

| 错误 | 解决方案 |
|-------|----------|
| `ffmpeg: command not found` | 先安装 FFmpeg |
| `No such file or directory` | 检查 video_path 是否正确 |
| `Permission denied` | 检查 output_path 的写入权限 |
| `Output directory not empty` | 清空目录或使用其他输出路径 |

## 说明

- FFmpeg 在帧提取方面比 OpenCV **快得多**（10-100 倍）
- scale 过滤器使用 `-2` 而不是 `-1`，以确保尺寸可被 2 整除（更好的编解码器兼容性）
- `-fps_mode vfr`（可变帧率）在定位时会跳过重复帧
- 使用 `-q:v 2` 可获得高质量 JPEG（范围 1-31，默认值 31）
```