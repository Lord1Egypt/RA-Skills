# Video Downloader Skill

## 安装依赖

使用前需要安装 `yt-dlp`:

```bash
# 方法 1: 系统包 (推荐)
sudo apt-get install yt-dlp

# 方法 2: pip
pip install yt-dlp

# 方法 3: 直接下载二进制
sudo curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp
sudo chmod a+rx /usr/local/bin/yt-dlp
```

## 使用方法

发送视频链接给八戒，例如:
- https://www.bilibili.com/video/BV1xx411c7mD
- https://www.youtube.com/watch?v=xxxxx
- https://v.douyin.com/xxxxx
- https://www.tiktok.com/@user/video/xxxxx

视频会自动下载到 `~/.openclaw/workspace/downloads/` 目录
