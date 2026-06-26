# 视频转笔记 — AI 工作流参考

本文件为 AI 提供详细的技术参考。

---

## 依赖安装流程

AI 在首次使用时检测环境，然后**列出缺失项并征得用户同意后再安装**。

### 检查脚本

```bash
#!/bin/bash
# 检测脚本（仅检测，不安装）
MISSING=""

python3 --version >/dev/null 2>&1 || MISSING="$MISSING python3"
ffmpeg -version >/dev/null 2>&1 || MISSING="$MISSING ffmpeg"
python3 -c "import whisper" >/dev/null 2>&1 || MISSING="$MISSING whisper"

if [ -n "$MISSING" ]; then
  echo "缺失依赖:$MISSING"
  echo "需要用户确认后才能安装"
fi
```

> ⚡ **执行安装前必须做的事：**
> 1. 告诉用户具体缺失哪些工具/包（如 "python3, ffmpeg, openai-whisper"）
> 2. 展示完整安装命令（如 `brew install python3 ffmpeg && pip3 install openai-whisper`）
> 3. 等待用户确认后再执行

### 跨平台安装命令

| 平台 | Python3 | ffmpeg | openai-whisper |
|------|---------|--------|----------------|
| **macOS** | `brew install python3` | `brew install ffmpeg` | `pip3 install openai-whisper` |
| **Ubuntu/Debian** | `apt install python3` | `apt install ffmpeg` | `pip3 install openai-whisper` |
| **Windows** | [python.org](https://python.org) 下载 | `winget install ffmpeg` | `pip install openai-whisper` |

### yt-dlp（网络视频需要）

```bash
pip3 install yt-dlp
```

---

## 转写参数详解

### `transcribe.py` 完整参数

```
usage: transcribe.py [-h] [--model {tiny,tiny.en,base,base.en,small,small.en,medium,medium.en,large,turbo}] [--language LANGUAGE] [--output-dir OUTPUT_DIR] [--device DEVICE] [--max-files MAX_FILES] videos [videos ...]
```

### 模型详情

| 模型 | 大小 | 速度(相对) | 中文精度 | 推荐场景 |
|------|------|-----------|---------|---------|
| tiny | ~75MB | 1x | ⭐⭐ | 快速预览 |
| base | ~150MB | 2x | ⭐⭐⭐ | 日常推荐 |
| small | ~460MB | 4x | ⭐⭐⭐⭐ | 精度优先 |
| medium | ~1.5GB | 8x | ⭐⭐⭐⭐⭐ | 重要内容 |
| large | ~3GB | 16x | ⭐⭐⭐⭐⭐⭐ | 极致精度 |
| turbo | ~1.5GB | 4x | ⭐⭐⭐⭐⭐ | ⭐ 长视频首选 |

> **性能实测参考（MacBook Air M2, CPU）：**
> - base 模型：约实时 1x（10分钟视频 ≈ 10分钟转写）
> - turbo 模型：约实时 2x
> - 首次运行会自动下载模型文件（后续复用缓存）

### 输出格式

```
[00:00 -> 00:15] 大家好，今天我们来聊...
[00:15 -> 00:30] 首先我们来介绍一下核心概念...
[00:30 -> 00:45] 这里需要注意的一个点是...
```

输出文件：`<视频名>.txt`（与视频同目录）

---

## 已知问题 & 处理

| 问题 | 原因 | AI 处理 |
|------|------|---------|
| 转写很慢 | CPU 模式，模型太大 | 改用 `--model base` 或 `turbo` |
| 中文识别不准 | 未指定语言 | 加 `--language zh` |
| 下载失败 | 平台限制/网络问题 | 告知用户，建议本地下载 |
| 文件格式不支持 | 奇怪的视频格式 | 先用 ffmpeg 转码为 mp4 |
| 内存不足 | 视频太大 | 先压缩或用更小模型 |
| GPU 不可用 | 无 CUDA | 默认 CPU 模式 |
