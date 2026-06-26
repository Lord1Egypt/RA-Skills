# 🎙️ Whisper GPU 音频转字幕

使用本地 Whisper 模型将音频文件转录为 SRT 字幕，**完全免费**，无需联网，支持 GPU 加速。

## ✨ 主要特性

- **完全免费** — 本地运行，替代剪映付费字幕功能
- **GPU 加速** — 自动检测并使用 Intel XPU / NVIDIA CUDA / AMD ROCm / Apple Metal
- **智能适配** — 自动选择最优运行参数（如 Intel XPU 自动关闭 FP16）
- **高精度** — 支持 Whisper Turbo 模型，速度与精度兼顾

## 📦 适用场景

- 自媒体视频制作（YouTube、B站、抖音等）
- 会议录音转文字
- 播客/课程内容转字幕
- 直播回放整理

## 🚀 快速开始

### 安装依赖

```bash
pip install openai-whisper
```

根据你的硬件安装对应的 PyTorch 版本：

```bash
# Intel GPU
pip install torch==2.10.0+xpu

# NVIDIA GPU
pip install torch --index-url https://download.pytorch.org/whl/cu121

# CPU
pip install torch
```

### 使用方法

安装此 Skill 后，直接告诉 AI：

```
把 xxx.mp3 转成 SRT 字幕文件
```

或者指定路径：

```
把 /path/to/audio.mp3 转成 SRT 字幕
```

### 高级用法

```
把 xxx.mp3 用 large-v3-turbo 模型转成英文字幕
把 xxx.mp3 转成字幕，语言是日语
```

## 🎬 字幕文件支持平台

生成的 `.srt` 字幕文件可以在以下平台直接使用：

### 视频剪辑软件
| 软件 | 支持情况 |
|------|---------|
| **剪映** | ✅ 完美支持，导入后可编辑样式 |
| **Adobe Premiere Pro** | ✅ 原生支持 |
| **DaVinci Resolve** | ✅ 原生支持 |
| **Final Cut Pro** | ✅ 原生支持（通过插件） |
| **CapCut (电脑版)** | ✅ 完美支持 |

### 播放器
| 播放器 | 支持情况 |
|--------|---------|
| **PotPlayer** | ✅ 自动加载同名 SRT 文件 |
| **VLC Media Player** | ✅ 自动加载同名 SRT 文件 |
| **IINA (macOS)** | ✅ 自动加载同名 SRT 文件 |
| **MPV** | ✅ 自动加载同名 SRT 文件 |
| **QQ影音** | ✅ 自动加载同名 SRT 文件 |

### 在线平台
| 平台 | 支持情况 | 注意事项 |
|------|---------|---------|
| **B站** | ✅ 上传时选择「字幕」 | 支持 SRT 格式直接上传 |
| **YouTube** | ✅ 创作者工作室 | 支持字幕轨道上传 |
| **抖音** | ✅ 需通过剪映处理 | 不能直接上传 SRT，需通过剪映导入 |
| **视频号** | ⚠️ 需转换 | 可能需要转换格式 |
| **西瓜视频** | ✅ 类似 B 站 | 支持 SRT 格式 |

### 字幕编辑工具
| 工具 | 用途 |
|------|------|
| **Subtitle Edit** | 专业字幕编辑，支持 SRT |
| **Aegisub** | 动画字幕制作 |
| **Arctime** | 国产字幕编辑软件 |
| **Notepad++** | 简单文本编辑 |

> 💡 **提示**：大多数平台会自动加载与视频文件同名的 `.srt` 文件，无需手动导入。例如 `video.mp4` 会自动加载 `video.srt`。

## 🖥️ 支持的 GPU 加速

| 设备 | 加速方式 | FP16 | 备注 |
|------|---------|------|------|
| Intel Arc 系列 | XPU | ❌ 自动关闭 | 需要 PyTorch XPU 版本 |
| NVIDIA 显卡 | CUDA | ✅ 自动开启 | 推荐 RTX 30/40 系列 |
| AMD 显卡 | ROCm | ✅ 自动开启 | Linux 下支持最佳 |
| Apple M1/M2/M3 | Metal | ✅ 自动开启 | macOS 原生支持 |
| 无 GPU | CPU | ❌ 自动关闭 | 兜底选项 |

## 📊 支持的 Whisper 模型

| 模型 | 大小 | 速度 | 精度 | 推荐场景 |
|------|------|------|------|---------|
| `tiny` | 39M | 极快 | 低 | 快速预览 |
| `base` | 74M | 快 | 中 | 日常使用 |
| `small` | 244M | 中 | 中 | 平衡选择 |
| `medium` | 769M | 慢 | 高 | 高质量需求 |
| `turbo` | 809M | 中 | 高 | ✅ **默认推荐** |
| `large-v3` | 1550M | 最慢 | 最高 | 专业需求 |
| `large-v3-turbo` | 1550M | 慢 | 最高 | 专业需求 |

## ⚙️ 执行方式

AI 会调用项目目录中的 `scripts/transcribe.py` 脚本执行转录，脚本会：

1. 自动检测可用 GPU 设备并选择最优加速方式
2. 加载 Whisper 模型（默认 `turbo`）
3. 将音频转录为 SRT 格式字幕
4. 输出文件保存在与音频同目录

## 📝 注意事项

- 首次运行会自动下载模型文件（turbo 约 1.5GB）
- 模型默认缓存在 `~/.cache/whisper`，可用软链接/Junction 指向其他磁盘
- Intel XPU 需要 Intel Arc 独显 + 对应版本 PyTorch
- 国内用户：如模型下载失败，可手动从镜像站下载后放入 `~/.cache/whisper/`

## 🔧 环境要求

- Python 3.8+
- PyTorch（对应你的硬件版本）
- openai-whisper

## 📄 License

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**English Version**: [README.md](README.md) - Complete documentation in English
