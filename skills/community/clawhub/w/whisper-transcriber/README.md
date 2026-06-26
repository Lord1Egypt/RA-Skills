# 🎤 Whisper Transcriber

**离线语音转文字技能** - 基于 Whisper.cpp 的高精度语音识别

---

## ⚡ 快速开始

### 一键安装

```bash
# 运行安装脚本（交互式选择模型）
# 默认会把模型下载到 ./assets/models（仓库通过 .gitignore 忽略大模型文件）
./scripts/install.sh

# 或直接指定模型
./scripts/install.sh base
```

### 使用示例

```bash
# 转写单个文件
./scripts/transcribe.sh voice.ogg

# 使用 large 模型（更高精度）
./scripts/transcribe.sh voice.ogg -m large

# 批量转写目录
./scripts/transcribe.sh ./recordings/ -b

# 输出 SRT 字幕
./scripts/transcribe.sh meeting.ogg -s

# 查看帮助
./scripts/transcribe.sh --help
```

---

## 📦 安装说明

### 前置要求

- macOS / Linux：bash + 包管理器（brew/apt/dnf/yum/pacman/zypper）
- Windows：推荐 **WSL2**（本项目在 WSL 下最稳）
- 500MB+ 可用磁盘空间（取决于模型大小）

### Windows（推荐路径：WSL2）

1. 安装 WSL2（Ubuntu 即可）并进入 WSL
2. 在 WSL 里运行：

```bash
bash ./scripts/install.sh
bash ./scripts/transcribe.sh voice.ogg
```

> 说明：原生 Windows 环境下 whisper-cli 的安装来源不统一，公开发布时容易踩坑；因此本 skill 默认建议 WSL2。

### 手动安装（如果 install.sh 自动安装失败）

macOS：
```bash
brew install whisper-cpp ffmpeg
```

Linux（包名可能随发行版不同而不同）：
```bash
# 示例（Debian/Ubuntu）
sudo apt-get update -y
sudo apt-get install -y ffmpeg
# whisper-cli/whisper.cpp 请按发行版包名安装
```

---

## 📖 完整文档

详细文档请查看 [`SKILL.md`](./SKILL.md)

---

## 🎯 功能特性

- ✅ 支持多种音频格式（OGG、WAV、MP3、FLAC、M4A 等）
- ✅ 离线运行，隐私安全
- ✅ Apple Silicon Metal GPU 加速
- ✅ 中文识别优化
- ✅ 自动语言检测
- ✅ 时间戳输出
- ✅ 多模型精度可选
- ✅ 批量处理支持
- ✅ 多种输出格式（TXT、SRT、JSON）

---

## 📊 模型对比

| 模型 | 大小 | 速度 | 精度 | 推荐场景 |
|------|------|------|------|----------|
| `tiny` | 75 MB | ⚡⚡⚡ | ⭐⭐ | 快速测试 |
| `base` | 142 MB | ⚡⚡ | ⭐⭐⭐ | 日常使用 ⭐ |
| `small` | 466 MB | ⚡ | ⭐⭐⭐⭐ | 高精度需求 |
| `medium` | 1.5 GB | 🐌 | ⭐⭐⭐⭐⭐ | 专业场景 |
| `large` | 2.9 GB | 🐌🐌 | ⭐⭐⭐⭐⭐ | 最佳精度 |

---

## 🔧 常用命令

```bash
# 查看帮助
./scripts/transcribe.sh --help

# 查看版本
whisper-cli --version

# 测试转写
./scripts/test.sh

# 清理临时文件
# 现在默认每次运行会使用 mktemp 创建独立临时目录并在退出时自动清理
# 如需自定义临时目录根路径：export WHISPER_TEMP_DIR=/tmp
# (一般不需要手动 rm -rf)
```

---

## 🐛 故障排除

### 问题：找不到 whisper-cli

```bash
# 检查是否安装
which whisper-cli

# 重新安装
brew reinstall whisper-cpp
```

### 问题：模型下载慢

```bash
# 使用镜像（如果有）
# 或手动下载后放到 ./assets/models/（推荐默认）
```

### 问题：识别不准确

1. 换用更大的模型（`-m large`）
2. 确保音频质量（16kHz 以上）
3. 指定正确的语言（`-l zh`）

---

## 📝 更新日志

### v1.0.0 (2026-03-06)
- 初始版本发布
- 支持 whisper-cpp 所有模型
- 自动化安装脚本
- 批量处理支持
- 多种输出格式

---

## 📄 许可证

MIT License

---

## 🔗 相关资源

- [Whisper.cpp GitHub](https://github.com/ggml-org/whisper.cpp)
- [模型下载](https://huggingface.co/ggerganov/whisper.cpp)
- [OpenClaw 技能系统](https://docs.openclaw.ai/skills)
