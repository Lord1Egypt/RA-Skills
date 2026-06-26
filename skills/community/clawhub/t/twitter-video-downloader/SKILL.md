---
name: twitter-video-downloader
description: 推特视频下载器 - 下载 Twitter/X 视频、GIF 和音频（MP4/MP3），支持 1080p、2K、4K、8K 高清下载。适用于需要保存推特视频、提取音频的用户。⚠️ 中国大陆用户需要使用代理。
version: 1.0.1
metadata:
  openclaw:
    emoji: "🐦"
    requires:
      bins: ["yt-dlp", "ffmpeg"]
---

# 🐦 推特视频下载器

专为中文用户打造的 Twitter/X 视频下载工具。支持下载高清视频、GIF、音频，提供批量下载功能。

## ⚠️ 中国大陆用户须知

**Twitter/X 在中国大陆被封锁，必须使用代理才能下载！**

使用前请确保您已开启代理工具（如 Clash、V2RayN、Shadowsocks 等）。

## ✨ 功能特性

- ✅ 下载 Twitter/X 视频（MP4 格式）
- ✅ 下载 GIF（自动转为 MP4）
- ✅ 提取音频（MP3 格式）
- ✅ 多清晰度支持：360p、480p、720p、1080p、2K、4K、8K
- ✅ 批量下载多个视频
- ✅ 查看视频信息（标题、作者、播放量等）

## 🚀 使用方法

### 基础下载（海外用户）

```bash
# 下载最佳质量
clawhub run twitter-video-downloader -- "https://x.com/user/status/1234567890"

# 下载指定清晰度
clawhub run twitter-video-downloader -- "URL" --quality 1080

# 仅下载音频 MP3
clawhub run twitter-video-downloader -- "URL" --audio-only
```

### 中国大陆用户（必须使用代理）

```bash
# 使用 HTTP 代理（Clash 默认端口）
clawhub run twitter-video-downloader -- \
  "https://x.com/user/status/1234567890" \
  --proxy http://127.0.0.1:7890

# 使用 SOCKS5 代理
clawhub run twitter-video-downloader -- \
  "https://x.com/user/status/1234567890" \
  --proxy socks5://127.0.0.1:1080
```

### 批量下载

```bash
clawhub run twitter-video-downloader -- \
  --proxy http://127.0.0.1:7890 \
  "https://x.com/user1/status/123" \
  "https://x.com/user2/status/456" \
  "https://x.com/user3/status/789"
```

### 查看视频信息

```bash
clawhub run twitter-video-downloader -- info "https://x.com/user/status/123"

# 带代理
clawhub run twitter-video-downloader -- info "https://x.com/user/status/123" --proxy http://127.0.0.1:7890
```

## 🔧 常用代理配置

| 代理工具 | HTTP 代理地址 | SOCKS5 代理地址 |
|---------|--------------|----------------|
| Clash | http://127.0.0.1:7890 | socks5://127.0.0.1:7890 |
| Clash Verge | http://127.0.0.1:7897 | socks5://127.0.0.1:7897 |
| V2RayN | http://127.0.0.1:10809 | socks5://127.0.0.1:10808 |
| Shadowsocks | - | socks5://127.0.0.1:1080 |
| Surge | http://127.0.0.1:6152 | socks5://127.0.0.1:6153 |

## 📁 下载位置

- **视频**：`~/Downloads/twitter-videos/`
- **音频**：`~/Downloads/twitter-audio/`

## 🔗 支持的链接格式

- `https://twitter.com/username/status/1234567890`
- `https://x.com/username/status/1234567890`
- `https://mobile.twitter.com/username/status/1234567890`

## ⚡ 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `--quality, -q` | 视频清晰度：best, 1080, 720, 480, 360 | `-q 1080` |
| `--audio-only, -a` | 仅下载音频 MP3 | `-a` |
| `--proxy, -p` | 代理地址（大陆用户必填） | `-p http://127.0.0.1:7890` |
| `--output, -o` | 自定义输出目录 | `-o /path/to/download` |

## 🛠️ 安装依赖

此工具需要 `yt-dlp` 和 `ffmpeg`，OpenClaw 会自动检查并提示安装。

## ❓ 常见问题

**Q: 下载失败怎么办？**  
A: 请检查代理是否开启，使用 `--proxy` 参数指定代理地址。

**Q: 如何确认代理正常工作？**  
A: 在终端运行 `curl -x http://127.0.0.1:7890 https://x.com -I`，如果返回 200 说明代理正常。

**Q: 下载的视频在哪里？**  
A: 默认保存在 `~/Downloads/twitter-videos/` 目录。

**Q: 支持下载私密账号的视频吗？**  
A: 不支持。只能下载公开账号的公开推文视频。

## 📝 示例场景

```bash
# 场景 1：下载马斯克的一条推文视频
clawhub run twitter-video-downloader -- \
  "https://x.com/elonmusk/status/1234567890" \
  --proxy http://127.0.0.1:7890

# 场景 2：下载为 1080p 高清
clawhub run twitter-video-downloader -- \
  "https://x.com/user/status/123" \
  --proxy http://127.0.0.1:7890 \
  --quality 1080

# 场景 3：只提取音频
clawhub run twitter-video-downloader -- \
  "https://x.com/user/status/123" \
  --proxy http://127.0.0.1:7890 \
  --audio-only
```

## ⚠️ 免责声明

- 请遵守当地法律法规
- 仅下载您有权下载的内容
- 尊重原创作者的版权

---

**Made with ❤️ for Chinese users**
