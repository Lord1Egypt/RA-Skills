---
name: turbo-whisper-local-stt
description: |
  当用户想要**音频转文字**、**语音转文本**、**转录录音**、**生成字幕**、**会议录音转文字**、**语音笔记转文本**、**本地转录音频**时自动触发。
  使用本地 Faster-Whisper（large-v3-ct2 等模型）进行高性能、中文优先的音频转文字，完全离线、隐私安全，支持 wav/mp3/m4a 等格式和整个音频文件夹。
  特别适合长音频（内置 VAD 分段）、会议/访谈/视频字幕等中文场景，输出结构化结果（完整文本 + 分段 + 时间戳）。

  【重要约束】仅处理音频文件或音频文件夹，其他文件（如视频、图片、纯文本）一律不触发此技能。

  常见触发口语（越多越好）：
  - “帮我把这个音频转成文字”
  - “语音转文本 这个录音.mp3”
  - “转录这个会议录音”
  - “生成这个视频的字幕” （如果用户提供音频提取后的文件）
  - “本地转录音频 文件夹路径”
  - “把这个语音笔记转文字”
  - “音频转文字 会议.wav”
  - “帮我转录这段录音”
  - “语音识别 这个 m4a 文件”
  - “离线转文字” / “本地 STT”
metadata:
  openclaw:
    requires:
      bins:
        - python
    user-invocable: true
---

# Turbo-Whisper-Local-STT

**功能**：本地高性能音频转文本工具，使用 Faster-Whisper large-v3-ct2 模型。支持中文优先、长音频 VAD 分段、GPU 加速（int8_float16），完全离线隐私安全。特别适合会议录音、语音笔记、视频字幕等中文音频场景。

### 触发时机（Triggers）
- 用户提供音频文件（.wav、.mp3、.m4a 等）或音频文件夹路径，并表达转文字、转录、生成字幕等意图。
- 用户说“帮我转录”“语音转文本”“音频转文字”等口语。
- 支持单个文件或整个文件夹批量处理。

### 支持的模型（推荐顺序）
1. **faster-whisper-base-ct2** → 默认推荐（低配设备 / 追求极速）
2. **faster-whisper-large-v3-ct2** → 高精度需求 / 会议转录
3. **faster-whisper-large-v3-turbo-ct2** → 性能与精度的平衡点

## 参数提取指南
当决定调用此技能时，请从用户消息中准确提取以下参数：

1. **`<音频路径>`** (必填): 用户提供的音频文件路径或文件夹路径（支持相对/绝对路径）。
2. **`<输出目录>`** (选填): 用户指定的输出文件夹。若未指定，默认在输入文件同级目录生成 `[源文件名].json` 和 `.txt`。
3. **`<language>`** (选填): 明确指定语言时使用（如 `zh`、`en`），默认自动检测但优先中文。
4. **`<model_path>`** (选填): 用户指定特定模型路径。
5. **`<output>`** (选填): 输出格式（`json` 或 `text`），默认两者都生成。
6. 其他可选参数（如 `--beam_size`、`--separator`）根据用户需求添加。

### 执行步骤
1. **解析路径**：识别用户的音频文件或文件夹路径。
2. **默认目标**：若未指定输出路径，默认在输入同级创建 `[源文件名].json/.txt` 文件。
3. **调用命令**：使用以下兼容性命令启动脚本（优先 `python3`，失败则 `python`）。脚本会自动创建虚拟环境、检测 GPU 并安装对应版本。

   ```bash
   (python3 scripts/transcribe.py --audio_path "<音频路径>" [--output_dir "<输出目录>"] [--language <zh/en>] [--model_path "<模型路径>"] [--output <json/text>] [--beam_size 5] [--separator " "]) || (python scripts/transcribe.py --audio_path "<音频路径>" [--output_dir "<输出目录>"] [--language <zh/en>] [--model_path "<模型路径>"] [--output <json/text>] [--beam_size 5] [--separator " "])