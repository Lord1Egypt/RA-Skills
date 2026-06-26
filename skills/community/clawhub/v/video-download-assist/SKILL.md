---
name: video-downloader
description: 下载 B 站、抖音、TikTok、YouTube 等平台视频。当用户分享视频链接时自动下载并保存。Triggers on: 视频链接、"download this video"、"帮我下载视频"、"下载这个"、发视频链接、bilibili.com、douyin.com、tiktok.com、youtube.com
---

# Video Downloader - 视频下载器

一键下载全网主流平台视频，自动保存到本地。基于 yt-dlp 构建，支持 1800+ 视频网站。

## 🎯 支持平台

| 平台 | 域名示例 | 备注 |
|------|----------|------|
| Bilibili | bilibili.com, b23.tv | 支持 4K、弹幕 (需额外配置) |
| 抖音 | douyin.com, iesdouyin.com | 支持无水印下载 |
| TikTok | tiktok.com | 支持无水印下载 |
| YouTube | youtube.com, youtu.be | 支持 8K、HDR、60fps |
| 其他 | 1800+ 网站 | 完整列表见 yt-dlp 文档 |

## 📦 安装依赖

### 方法 1: 系统包管理器 (推荐)

```bash
# Ubuntu/Debian
sudo apt-get install yt-dlp

# macOS (Homebrew)
brew install yt-dlp

# Windows (Scoop)
scoop install yt-dlp
```

### 方法 2: 直接下载最新版

```bash
# 下载二进制文件
sudo curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp
sudo chmod a+rx /usr/local/bin/yt-dlp

# 验证安装
yt-dlp --version
```

### 方法 3: pip 安装

```bash
pip install yt-dlp
```

## 🚀 快速使用

### 基础用法

用户发送视频链接，自动下载：

```
用户：https://www.bilibili.com/video/BV1xx411c7mD
助手：[自动下载并返回文件路径]
```

### 手动调用脚本

```bash
python ~/.openclaw/workspace/skills/video-downloader/scripts/download_video.py <视频链接>
```

### 输出目录

视频默认保存到：`~/.openclaw/workspace/downloads/`

文件名格式：`平台名_视频标题.mp4`

## 📋 完整示例

### 示例 1: 下载 B 站视频

```
用户：https://www.bilibili.com/video/BV1mjAYzhEYg/

执行：
~/.local/bin/yt-dlp -o "~/.openclaw/workspace/downloads/%(extractor)s_%(title)s.%(ext)s" https://www.bilibili.com/video/BV1mjAYzhEYg/

返回：
✅ 下载完成！
文件：/home/zxy/.openclaw/workspace/downloads/BiliBili_视频标题.mp4
大小：31MB
```

### 示例 2: 下载抖音视频

```
用户：帮我把这个抖音视频下载下来 https://v.douyin.com/xxxxx

执行：
~/.local/bin/yt-dlp -o "~/.openclaw/workspace/downloads/%(extractor)s_%(title)s.%(ext)s" https://v.douyin.com/xxxxx

返回：
✅ 抖音视频已下载
文件路径：~/.openclaw/workspace/downloads/Douyin_视频标题.mp4
```

### 示例 3: 下载 YouTube 视频

```
用户：https://www.youtube.com/watch?v=xxxxx

执行：
~/.local/bin/yt-dlp -o "~/.openclaw/workspace/downloads/%(extractor)s_%(title)s.%(ext)s" https://www.youtube.com/watch?v=xxxxx

返回：
✅ YouTube 视频已下载
```

## 🔧 高级配置

### 选择画质

```bash
# 最高画质 (默认)
yt-dlp <URL>

# 限制为 1080p
yt-dlp -f "best[height<=1080]" <URL>

# 限制为 720p (节省空间)
yt-dlp -f "best[height<=720]" <URL>

# 只下载音频 (转 MP3)
yt-dlp -x --audio-format mp3 <URL>
```

### 批量下载

```bash
# 下载整个播放列表
yt-dlp -o "~/.openclaw/workspace/downloads/%(playlist)s/%(title)s.%(ext)s" <播放列表链接>

# 下载频道所有视频
yt-dlp -o "~/.openclaw/workspace/downloads/%(uploader)s/%(title)s.%(ext)s" <频道链接>
```

### 下载字幕

```bash
# 自动下载字幕
yt-dlp --write-sub --sub-lang zh-Hans <URL>

# 嵌入字幕到视频
yt-dlp --embed-subs <URL>
```

## ⚠️ 常见问题

### Q: 提示 "Requested format is not available"

**原因：** 某些视频需要大会员才能下载高画质

**解决：**
```bash
# 降低画质要求
yt-dlp -f "best[height<=720]" <URL>

# 或使用默认格式
yt-dlp <URL>
```

### Q: 下载速度慢

**解决：**
```bash
# 限制并发连接数
yt-dlp --concurrent-fragments 4 <URL>

# 使用代理 (如果需要)
yt-dlp --proxy http://proxy:port <URL>
```

### Q: 需要登录才能下载

**解决：** 从浏览器导出 cookies

```bash
# 从 Chrome 导出 cookies
yt-dlp --cookies-from-browser chrome <URL>

# 或使用 cookies 文件
yt-dlp --cookies cookies.txt <URL>
```

### Q: 视频文件名乱码

**解决：** 脚本已处理中文编码，确保系统 locale 支持 UTF-8

```bash
# 检查 locale
locale

# 如需要，设置 UTF-8
export LANG=en_US.UTF-8
```

## 📁 文件结构

```
video-downloader/
├── SKILL.md              # 技能说明文件
├── scripts/
│   └── download_video.py # 下载脚本 (可选，直接用 yt-dlp 更简单)
├── references/
│   └── README.md         # 详细安装和使用指南
└── README.md             # 快速入门指南
```

## 🔐 安全说明

- 仅下载用户明确请求的视频
- 尊重版权，不要传播受保护内容
- 部分平台可能有下载限制，请遵守平台规则

## 📝 更新日志

- v1.0.0 - 初始版本
  - 支持 Bilibili、抖音、TikTok、YouTube
  - 自动检测平台并下载
  - 中文文件名支持
  - 默认 1080p 画质

## 🙏 致谢

核心依赖：
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - 152k+ stars 的万能下载器
- [Douyin_TikTok_Download_API](https://github.com/Evil0ctal/Douyin_TikTok_Download_API) - 抖音/TikTok 专用 API

## 📄 许可证

本 Skill 遵循 MIT 许可证。yt-dlp 遵循 Unlicense。
