# 🐦 推特视频下载器 (Twitter Video Downloader)

专为**中国大陆用户**优化的 Twitter/X 视频下载工具。

仿照 [SaveTwitter.net](https://savetwitter.net) 开发，基于强大的 `yt-dlp` 引擎。

---

## ⚠️ 重要提示

**中国大陆用户必须使用代理！**

Twitter/X 在中国大陆被封锁，直接使用会连接失败。请先开启您的代理工具（Clash、V2RayN、Shadowsocks 等）。

---

## ✨ 功能特性

- 🎬 下载 Twitter/X 视频（MP4 格式，高清）
- 🎞️ 下载 GIF（自动转为 MP4）
- 🎵 提取音频（MP3 格式）
- 📺 支持多种清晰度：360p / 480p / 720p / 1080p / 2K / 4K / 8K
- 📦 批量下载多个视频
- ℹ️ 查看视频信息（标题、作者、播放量、点赞数）
- 🌐 代理支持（专为中国大陆用户设计）

---

## 🚀 快速开始

### 1. 基础下载（海外用户）

```bash
./scripts/download.sh "https://x.com/user/status/1234567890"
```

### 2. 中国大陆用户（带代理）

```bash
# Clash 用户（默认端口 7890）
./scripts/download.sh \
  "https://x.com/user/status/1234567890" \
  --proxy http://127.0.0.1:7890

# V2RayN 用户
./scripts/download.sh \
  "https://x.com/user/status/1234567890" \
  --proxy http://127.0.0.1:10809
```

### 3. 下载指定清晰度

```bash
./scripts/download.sh "URL" --quality 1080 --proxy http://127.0.0.1:7890
```

### 4. 仅下载音频（MP3）

```bash
./scripts/download.sh "URL" --audio-only --proxy http://127.0.0.1:7890
```

### 5. 批量下载

```bash
./scripts/batch-download.sh \
  --proxy http://127.0.0.1:7890 \
  "https://x.com/user1/status/123" \
  "https://x.com/user2/status/456"
```

### 6. 查看视频信息

```bash
./scripts/info.sh "https://x.com/user/status/123" --proxy http://127.0.0.1:7890
```

---

## 🔧 代理配置参考

| 代理工具 | HTTP 代理 | SOCKS5 代理 |
|---------|-----------|-------------|
| **Clash** | `http://127.0.0.1:7890` | `socks5://127.0.0.1:7890` |
| **Clash Verge** | `http://127.0.0.1:7897` | `socks5://127.0.0.1:7897` |
| **V2RayN** | `http://127.0.0.1:10809` | `socks5://127.0.0.1:10808` |
| **Shadowsocks** | - | `socks5://127.0.0.1:1080` |
| **Surge** | `http://127.0.0.1:6152` | `socks5://127.0.0.1:6153` |

---

## 📦 安装依赖

此工具需要以下依赖：

```bash
# Ubuntu/Debian
sudo apt install yt-dlp ffmpeg

# macOS
brew install yt-dlp ffmpeg

# 或使用 pip
pip install yt-dlp
```

---

## 📁 输出目录

下载的文件会自动保存到：

- **视频**：`~/Downloads/twitter-videos/`
- **音频**：`~/Downloads/twitter-audio/`

---

## 🔗 支持的链接格式

- `https://twitter.com/username/status/1234567890`
- `https://x.com/username/status/1234567890`
- `https://mobile.twitter.com/username/status/1234567890`

支持短链接 `t.co` 自动解析。

---

## 📋 命令参数

### download.sh

| 参数 | 简写 | 说明 | 示例 |
|------|------|------|------|
| `--quality` | `-q` | 视频清晰度 | `-q 1080` |
| `--audio-only` | `-a` | 仅下载音频 | `-a` |
| `--proxy` | `-p` | 代理地址（大陆必填） | `-p http://127.0.0.1:7890` |
| `--output` | `-o` | 自定义输出目录 | `-o /path/to/dir` |
| `--help` | `-h` | 显示帮助 | `-h` |

### batch-download.sh

| 参数 | 简写 | 说明 |
|------|------|------|
| `--proxy` | `-p` | 代理地址 |

### info.sh

| 参数 | 说明 |
|------|------|
| `--proxy` | 代理地址 |

---

## ❓ 常见问题

### Q: 提示 "Unable to download JSON metadata" 怎么办？

**A**: 说明您在中国大陆且没有使用代理。请添加 `--proxy` 参数：

```bash
./download.sh "URL" --proxy http://127.0.0.1:7890
```

### Q: 如何确认代理正常工作？

**A**: 在终端运行：

```bash
curl -x http://127.0.0.1:7890 https://x.com -I
```

如果返回 `HTTP/2 200`，说明代理正常。

### Q: 下载的视频在哪里？

**A**: 默认保存在用户目录的 `Downloads/twitter-videos/` 文件夹中。

### Q: 支持下载私密账号的视频吗？

**A**: 不支持。本工具只能下载**公开账号**的**公开推文**视频。

### Q: 为什么下载的 GIF 是 MP4 格式？

**A**: Twitter 上的 GIF 实际上是以视频格式存储的，下载后会保持 MP4 格式，兼容性更好。

### Q: 如何更新 yt-dlp？

**A**: 

```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade yt-dlp

# 或使用官方更新
yt-dlp -U
```

---

## 💡 使用示例

### 示例 1：下载马斯克推文视频

```bash
./scripts/download.sh \
  "https://x.com/elonmusk/status/1234567890" \
  --proxy http://127.0.0.1:7890
```

### 示例 2：下载高清 4K 视频

```bash
./scripts/download.sh \
  "https://x.com/user/status/123" \
  --proxy http://127.0.0.1:7890 \
  --quality best
```

### 示例 3：下载音频制作铃声

```bash
./scripts/download.sh \
  "https://x.com/user/status/123" \
  --proxy http://127.0.0.1:7890 \
  --audio-only
```

### 示例 4：批量下载收藏的视频

```bash
./scripts/batch-download.sh \
  --proxy http://127.0.0.1:7890 \
  "https://x.com/user1/status/111" \
  "https://x.com/user2/status/222" \
  "https://x.com/user3/status/333"
```

---

## ⚠️ 免责声明

1. 本工具仅供学习和个人使用
2. 请遵守当地法律法规
3. 尊重原创作者的版权和知识产权
4. 请勿用于下载受版权保护的内容
5. 使用本工具产生的任何法律责任由用户自行承担

---

## 🔗 相关链接

- 项目主页：[ClawHub](https://clawhub.ai)
- 灵感来源：[SaveTwitter.net](https://savetwitter.net)
- 底层工具：[yt-dlp](https://github.com/yt-dlp/yt-dlp)

---

**Made with ❤️ for Chinese users**  
**专为中文用户打造 🇨🇳**
