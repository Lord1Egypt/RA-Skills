---
name: whisper-transcriber
description: "Offline speech-to-text (ASR) using whisper.cpp (whisper-cli) + ffmpeg. Supports batch transcription, timestamps, SRT/TXT/JSON outputs, and model download. Cross-platform: macOS/Linux; Windows via WSL2 (recommended)."
metadata:
  openclaw:
    emoji: "🎤"
    i18n:
      default: "zh"
      supported: ["zh", "en"]
    requires:
      bins: ["ffmpeg", "whisper-cli"]
---

# 🎤 Whisper Transcriber（离线语音转文字）

基于 **whisper.cpp / whisper-cli** 的离线语音识别技能。

## 快速使用

- 安装依赖（跨平台自动检测）：

```bash
bash <SKILL_DIR>/scripts/install.sh
```

- 转写一个音频文件：

```bash
bash <SKILL_DIR>/scripts/transcribe.sh voice.ogg
```

- 批量转写目录 + 输出 SRT：

```bash
bash <SKILL_DIR>/scripts/transcribe.sh ./recordings -b -s
```

## 跨平台说明（Windows 推荐 WSL2）

- macOS / Linux：使用 `scripts/install.sh`
- Windows：**推荐 WSL2（Ubuntu）**，在 WSL 内按 Linux 方式运行本 skill（最稳）

WSL 内安装/使用：

```bash
bash <SKILL_DIR>/scripts/install.sh
bash <SKILL_DIR>/scripts/transcribe.sh voice.ogg
```

> 说明：原生 Windows 环境下 whisper-cli 的安装来源/包名不统一，公开发布时容易造成安装失败；因此本 skill 默认建议 WSL2。

## 可配置项（环境变量）

无需改脚本，直接用环境变量覆盖默认值：

- `WHISPER_DEFAULT_MODEL`（默认 base）
- `WHISPER_DEFAULT_LANG`（默认 zh）
- `WHISPER_MODEL_DIR`（默认 `<SKILL_DIR>/assets/models`）
- `WHISPER_MODEL_DIR_USER`（默认同 `WHISPER_MODEL_DIR`，**自动下载的默认目录**；如你想把模型放到别处再覆盖此变量）
- `WHISPER_TEMP_DIR`（默认 `${TMPDIR:-/tmp}`；每次运行会在其下 mktemp 创建独立临时目录并自动清理）

## 目录结构

- `scripts/transcribe.sh`：主转写脚本（支持批量、SRT/TXT/JSON）
- `scripts/install.sh`：跨平台安装依赖 + 可选下载模型
- `scripts/install.ps1`：Windows（非 WSL）best-effort 安装/下载（不作为默认推荐路径）
- `assets/models/`：模型默认下载/存放位置（仓库通过 `.gitignore` 忽略大模型文件，避免提交/发布）
- `config.json`：默认配置（发布/维护用，脚本通过环境变量覆盖即可）

> 需要更细的用法/参数说明：直接运行 `bash <SKILL_DIR>/scripts/transcribe.sh --help`。
