# YouTube Transcriber

> 🎯 一键转录 YouTube 视频，自动生成带时间戳的文字稿

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Node 14+](https://img.shields.io/badge/node-14+-green.svg)](https://nodejs.org/)

---

## 🚀 快速开始

### 方法 1：OpenClaw（推荐）

```bash
# OpenClaw 自动从 GitHub 安装
/openclaw install youtube-transcribe

# 直接使用
/youtube-transcribe "https://youtube.com/watch?v=VIDEO_ID"
```

### 方法 2：直接从 GitHub（NPX）

```bash
npx github:BODYsuperman/Youtube-Transcriber-Skill "https://youtube.com/watch?v=VIDEO_ID"
```

### 方法 3：Python（手动安装）

```bash
git clone https://github.com/BODYsuperman/Youtube-Transcriber-Skill.git
cd Youtube-Transcriber-Skill
./install.sh
python3 transcribe.py "URL"
```

---

## 📖 详细使用方法

### URL 参数说明

**URL 就是 YouTube 视频的链接地址**

#### 支持的 URL 格式

| 格式 | 示例 | 说明 |
|------|------|------|
| **标准格式** | `https://youtube.com/watch?v=jNQXAC9IVRw` | 最常用的格式 |
| **短链接** | `https://youtu.be/jNQXAC9IVRw` | YouTube 短链接 |
| **手机版** | `https://m.youtube.com/watch?v=VIDEO_ID` | 移动版 YouTube |
| **带时间戳** | `https://youtube.com/watch?v=VIDEO_ID&t=30s` | 从 30 秒开始 |
| **带播放列表** | `https://youtube.com/watch?v=VIDEO_ID&list=PLxxx` | 播放列表中的视频 |

**所有格式都支持！工具会自动提取视频 ID。**

---

### 语言参数

| 代码 | 语言 | 使用示例 |
|------|------|---------|
| `auto` | 自动检测（默认） | `npx ... "URL"` |
| `zh` | 中文 | `npx ... "URL" zh` |
| `en` | 英文 | `npx ... "URL" en` |
| `ja` | 日文 | `npx ... "URL" ja` |
| `ko` | 韩文 | `npx ... "URL" ko` |
| `es` | 西班牙文 | `npx ... "URL" es` |
| `fr` | 法文 | `npx ... "URL" fr` |

---

### 完整命令格式

```bash
npx github:BODYsuperman/Youtube-Transcriber-Skill <YouTube 视频链接> [语言代码]
```

| 参数 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| **URL** | YouTube 视频链接 | ✅ 必填 | - |
| **语言** | 转录语言代码 | ❌ 可选 | `auto` |

---

## 💡 实际操作步骤

### 步骤 1：找到想转录的视频

在 YouTube 上找到视频，复制地址栏的 URL：

```
https://www.youtube.com/watch?v=jNQXAC9IVRw
```

### 步骤 2：运行命令

```bash
npx github:BODYsuperman/Youtube-Transcriber-Skill "https://www.youtube.com/watch?v=jNQXAC9IVRw"
```

### 步骤 3：等待完成

```
📺 URL: https://www.youtube.com/watch?v=jNQXAC9IVRw
🌐 Language: auto

[1/3] 下载音频...
✅ 下载成功

[2/3] 转录中...
✅ 转录完成！语言：en

[3/3] 生成总结...

============================================================
# 视频转录总结

**URL:** https://www.youtube.com/watch?v=jNQXAC9IVRw
**语言:** en
**行数:** 4

## 转录内容

[0.00s -> 4.00s]  Alright, so here we are, one of the elephants.
[4.00s -> 12.00s]  The cool thing about these guys is that they have really long trunks.
[12.00s -> 14.00s]  And that's cool.
[14.00s -> 19.00s]  And that's pretty much all there is to say.
============================================================
```

---

## 📝 更多使用例子

### 例子 1：转录英文视频

```bash
npx github:BODYsuperman/Youtube-Transcriber-Skill "https://youtube.com/watch?v=jNQXAC9IVRw" en
```

### 例子 2：转录中文视频

```bash
npx github:BODYsuperman/Youtube-Transcriber-Skill "https://youtube.com/watch?v=9uDH8z-HZKs" zh
```

### 例子 3：自动检测语言

```bash
npx github:BODYsuperman/Youtube-Transcriber-Skill "https://youtube.com/watch?v=VIDEO_ID"
```

### 例子 4：使用短链接

```bash
npx github:BODYsuperman/Youtube-Transcriber-Skill "https://youtu.be/VIDEO_ID"
```

### 例子 5：批量处理（创建脚本）

```bash
# 创建 batch.sh
cat > batch.sh << 'EOF'
#!/bin/bash
for url in "$@"; do
    echo "Processing: $url"
    npx github:BODYsuperman/Youtube-Transcriber-Skill "$url" zh
done
EOF

chmod +x batch.sh

# 使用
./batch.sh "URL1" "URL2" "URL3"
```

---

## 📦 系统要求

| 要求 | 最低版本 | 检查命令 |
|------|---------|---------|
| **Node.js** | >= 14.0.0 | `node --version` |
| **Python** | >= 3.8.0 | `python3 --version` |
| **npm** | >= 6.0.0 | `npm --version` |

---

## 🔧 安装依赖（仅方法 3 需要）

### 自动安装（推荐）

```bash
./install.sh
```

### 手动安装

```bash
pip3 install -r requirements.txt
```

### 验证安装

```bash
python3 -m yt_dlp --version
python3 -c "from faster_whisper import WhisperModel; print('Whisper OK!')"
```

---

## 🔍 常见问题

### Q1: 下载失败（403 错误）

```
ERROR: unable to download video data: HTTP Error 403: Forbidden
```

**解决方案：**

```bash
# 使用代理
npx github:BODYsuperman/Youtube-Transcriber-Skill "URL" -p "http://proxy:port"

# 或设置环境变量
export HTTP_PROXY="http://proxy:port"
export HTTPS_PROXY="http://proxy:port"
npx github:BODYsuperman/Youtube-Transcriber-Skill "URL"
```

---

### Q2: 转录太慢

**解决方案：**

1. 使用更小的模型（修改 `transcribe.py` 中的 `WhisperModel('tiny')`）
2. 使用更好的 CPU/GPU
3. 检查网络连接

---

### Q3: 内存不足

```
Killed
```

**解决方案：**

```bash
# 使用 tiny 模型（仅需 100MB 内存）
# 修改 transcribe.py 第 15 行：
model = WhisperModel('tiny', device='cpu', compute_type='int8')
```

---

### Q4: 找不到 Python

```
python3: command not found
```

**解决方案：**

```bash
# Ubuntu/Debian
sudo apt-get install -y python3 python3-pip

# macOS
brew install python

# Windows
# 下载安装：https://www.python.org/downloads/
```

---

### Q5: 找不到 Node.js

```
npx: command not found
```

**解决方案：**

```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# macOS
brew install node

# Windows
# 下载安装：https://nodejs.org/
```

---

## 📊 性能基准

**40 分钟视频转录时间：**

| 模型 | NAS (4 核) | 本地电脑 (8 核) | 内存 |
|------|-----------|---------------|------|
| `tiny` | 24 分钟 | 10 分钟 | 100MB |
| `base` | 45 分钟 | 20 分钟 | 500MB |
| `small` | 90 分钟 | 40 分钟 | 1GB |

---

## 📁 文件结构

```
Youtube-Transcriber-Skill/
├── README.md           # 使用说明
├── package.json        # npm 配置
├── requirements.txt    # Python 依赖
├── install.sh          # 自动安装脚本
├── transcribe.py       # Python 主脚本
└── bin/
    └── transcribe.js   # NPX 入口
```

---

## 🙏 感谢

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube 下载工具
- [faster-whisper](https://github.com/guillaumekln/faster-whisper) - Whisper 语音识别
- [OpenAI Whisper](https://github.com/openai/whisper) - 原始 Whisper 模型

---

## 📬 反馈与支持

遇到问题？欢迎反馈：
- **Issues:** https://github.com/BODYsuperman/Youtube-Transcriber-Skill/issues
- **Discussions:** https://github.com/BODYsuperman/Youtube-Transcriber-Skill/discussions

---

**⭐ 如果这个项目对你有帮助，请给个 Star！**

---

## 📜 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件
