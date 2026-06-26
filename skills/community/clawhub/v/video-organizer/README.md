# Video Organizer - 视频文件批量重命名和整理工具

一个简单但强大的视频文件批量重命名和整理工具，帮助你快速整理混乱的视频文件夹！

## 功能特性
- ✅ 自动识别视频文件格式（mp4, avi, mov, mkv, flv, wmv, webm 等）
- ✅ 按时间整理（文件修改时间）
- ✅ 按格式/扩展名整理
- ✅ 按分辨率整理（720p, 1080p, 4K 等，计划中）
- ✅ 批量重命名（支持多种命名模式、正则表达式）
- ✅ 预览模式（先看效果再执行）
- ✅ 撤销操作（安全可靠）

## 安装

### 方法一：通过 clawhub 安装
```bash
clawhub install video-organizer
```

### 方法二：作为 Python 脚本运行
```bash
# 克隆或下载项目
git clone <repo-url>
cd video-organizer
```

## 快速开始

### 1. 按时间整理视频
```bash
python3 video_organizer.py organize ./videos --by date --output ./organized
```

这会将视频按照修改时间整理到这样的文件夹结构中：
```
organized/
├── 2026/
│   ├── 03/
│   │   ├── video1.mp4
│   │   └── video2.mp4
│   └── 04/
└── 2025/
```

### 2. 按格式整理视频
```bash
python3 video_organizer.py organize ./videos --by format --output ./organized
```

这会将视频按照扩展名整理：
```
organized/
├── mp4/
│   ├── video1.mp4
│   └── video2.mp4
├── avi/
│   └── video3.avi
└── mkv/
    └── video4.mkv
```

### 3. 批量重命名视频
```bash
python3 video_organizer.py rename ./videos --pattern "video_{001}.mp4"
```

### 4. 预览模式（不实际执行，先看效果）
```bash
python3 video_organizer.py organize ./videos --by date --preview
```

### 5. 撤销操作
```bash
python3 video_organizer.py undo ./organized
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

### 命名模式变量
- `{001}` - 三位序号（自动补零）
- `{01}` - 两位序号
- `{1}` - 一位序号
- `{YYYY}` - 四位年份
- `{MM}` - 两位月份
- `{DD}` - 两位日期
- `{original}` - 原始文件名（不含扩展名）
- `{ext}` - 原始扩展名

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
| m4v, mpg, mpeg, 3gp, ogv, ts | 其他常见视频格式 |

## 示例场景

### 场景 1：整理下载的视频
```bash
# 按时间整理下载文件夹里的视频
python3 video_organizer.py organize ~/Downloads --by date --output ~/Videos/Organized
```

### 场景 2：批量重命名视频
```bash
# 将视频重命名为 video_001.mp4, video_002.mp4...
python3 video_organizer.py rename ./videos --pattern "video_{001}.mp4"
```

### 场景 3：先预览，再执行
```bash
# 第一步：预览
python3 video_organizer.py organize ./videos --by format --preview

# 第二步：确认没问题后执行
python3 video_organizer.py organize ./videos --by format --output ./organized
```

## 安全性
- 工具默认使用复制而非移动（整理时），原文件不会被删除
- 执行前会自动保存备份
- 支持一键撤销操作
- 建议先用 --preview 预览效果

## 故障排除

### 问题：权限不足
**解决方法**：确保你有文件的读写权限

### 问题：撤销失败
**原因**：备份文件可能被删除或修改
**解决方法**：确保在同一目录下执行，且备份文件未被删除

## 开发计划
- [ ] 按分辨率整理（720p, 1080p, 4K 等）
- [ ] 视频元数据读取（时长、编码等）
- [ ] 配置文件支持
- [ ] GUI 界面（可选）

## 贡献
欢迎提交 Issue 和 Pull Request！

## 许可证
MIT License

---

**Video Organizer** - 让视频整理变得简单！🎬
