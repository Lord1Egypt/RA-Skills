---
name: video-organizer
description: 视频文件批量重命名和整理工具，支持按时间、格式、分辨率等方式整理视频，批量重命名，预览模式和撤销功能！
---

# Video Organizer - 视频文件批量重命名和整理工具

## 功能特性
- ✅ 自动识别视频文件格式（mp4, avi, mov, mkv, flv, wmv, webm 等）
- ✅ 按时间整理（文件修改时间）
- ✅ 按格式/扩展名整理
- ✅ 按分辨率整理（720p, 1080p, 4K 等，可选）
- ✅ 批量重命名（支持多种命名模式、正则表达式）
- ✅ 预览模式（先看效果再执行）
- ✅ 撤销操作（安全可靠）

## 安装
```bash
# 方法一：通过 clawhub 安装
clawhub install video-organizer

# 方法二：作为 Python 脚本运行
git clone <repo-url>
cd video-organizer
```

## 快速开始

### 1. 按时间整理视频
```bash
video-organizer organize ./videos --by date --output ./organized
```

### 2. 按格式整理视频
```bash
video-organizer organize ./videos --by format --output ./organized
```

### 3. 批量重命名视频
```bash
video-organizer rename ./videos --pattern "video_{001}.mp4"
```

### 4. 预览模式
```bash
video-organizer organize ./videos --by date --preview
```

### 5. 撤销操作
```bash
video-organizer undo ./organized
```

## 详细使用说明

### organize 命令参数
- `directory`：（必需）要整理的视频目录
- `--by`：整理方式，可选 `date`（按时间，默认）或 `format`（按格式）
- `--output`：输出目录，默认在输入目录下创建 `organized` 文件夹
- `--preview`：预览模式，只显示方案不实际执行

### rename 命令参数
- `directory`：（必需）要重命名的视频目录
- `--pattern`：（必需）命名模式
- `--regex`：正则表达式替换
- `--preview`：预览模式

### 支持的视频格式
| 格式 | 说明 |
|-----|------|
| mp4 | MP4 视频 |
| avi | AVI 视频 |
| mov | QuickTime 视频 |
| mkv | Matroska 视频 |
| flv | Flash 视频 |
| wmv | Windows Media 视频 |
| webm | WebM 视频 |

## 示例场景

### 场景 1：整理下载的视频
```bash
# 按时间整理下载文件夹里的视频
video-organizer organize ~/Downloads --by date --output ~/Videos/Organized
```

### 场景 2：批量重命名视频
```bash
# 将视频重命名为 video_001.mp4, video_002.mp4...
video-organizer rename ./videos --pattern "video_{001}.mp4"
```

### 场景 3：先预览，再执行
```bash
# 第一步：预览
video-organizer organize ./videos --by format --preview

# 第二步：确认没问题后执行
video-organizer organize ./videos --by format --output ./organized
```

## 注意事项
- 确保有文件的读写权限
- 建议先用 --preview 预览效果
- 大量文件整理可能需要一些时间
- 整理前建议先备份原文件

## 更新日志
### v1.0.0 (2026-03-06)
- 初始版本发布
- 支持按时间/格式整理
- 支持批量重命名
- 支持预览模式
- 支持撤销操作
