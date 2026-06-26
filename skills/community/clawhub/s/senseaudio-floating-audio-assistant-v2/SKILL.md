---
name: senseaudio-floating-audio-assistant
description: Use when the user wants to open, stop, configure, debug, or package the SenseAudio floating audio assistant in AudioClaw, including system-audio subtitles, bilingual ASR/translation, recent-project organization, copied-text TTS, music generation, or macOS audio routing.
metadata: {"openclaw":{"emoji":"🎧","primaryEnv":"SENSEAUDIO_API_KEY","requires":{"bins":["bash","python3","swiftc","SwitchAudioSource"],"env":["SENSEAUDIO_API_KEY","AUDIOCLAW_ASR_API_KEY"]},"install":[{"kind":"brew","formula":"switchaudio-osx","bins":["SwitchAudioSource"]}],"os":["macos"],"skillKey":"senseaudio-floating-audio-assistant"}}
---

# SenseAudio 浮窗音频助手

使用这个 skill 来启动和维护 SenseAudio 浮窗音频助手。

高优先级触发说法：

- 打开实时字幕
- 开启系统音频字幕
- 打开双语同传
- 启动字幕浮窗
- 打开听视频字幕助手
- 打开浮窗音频助手
- 打开最近项目
- 打开音乐工坊
- 用 `$senseaudio-floating-audio-assistant`

## Default Behavior

默认启动 macOS 原生悬浮窗：

- 采集系统播放音频，不依赖麦克风
- 自动进入字幕音频路由模式，并在停止时恢复原音频输出和音量
- 使用本地 `sherpa-onnx` 输出低延迟快速字幕
- 使用 SenseAudio 输出更准确的最终 ASR
- 可在 ASR 面板选择快速识别语言和 SenseAudio 目标翻译语言
- 可显示并区分“快速 ASR / SenseAudio ASR / SenseAudio 翻译”
- 保存最近项目，支持重命名、查看原文、多模板整理、自定义模板编辑和模板文件导入
- 复制文本后支持 SenseAudio TTS 朗读和音色选择
- 音乐工坊使用 SenseAudio 音乐生成接口，保留生成历史并支持播放/暂停/重命名

## Main Commands

启动浮窗：

```bash
bash "{baseDir}/scripts/start-senseaudio-floating-audio-assistant.sh"
```

停止浮窗并恢复系统音频：

```bash
bash "{baseDir}/scripts/stop-senseaudio-floating-audio-assistant.sh"
```

查看运行状态：

```bash
bash "{baseDir}/scripts/status-senseaudio-floating-audio-assistant.sh"
```

检查系统音频链路和基础依赖：

```bash
bash "{baseDir}/scripts/check-senseaudio-floating-audio-assistant-setup.sh"
```

打开最近项目/历史记录目录：

```bash
bash "{baseDir}/scripts/open-senseaudio-floating-audio-assistant-runs.sh"
```

打开 Audio MIDI Setup：

```bash
bash "{baseDir}/scripts/open_audio_midi_setup.sh"
```

运行自检：

```bash
bash "{baseDir}/scripts/doctor-senseaudio-floating-audio-assistant.sh"
python3 "{baseDir}/scripts/senseaudio_api_smoke.py"
```

如果需要真实调用 SenseAudio 做一条极小 TTS 探针，再运行：

```bash
python3 "{baseDir}/scripts/senseaudio_api_smoke.py" --live-tts
```

## Action Flow

如果用户说“打开实时字幕”“开启双语同传”“启动浮窗字幕”“打开音乐工坊”“查看最近项目”，不要只返回命令，也不要假装状态已经切换。优先直接执行启动脚本：

```bash
bash "{baseDir}/scripts/start-senseaudio-floating-audio-assistant.sh"
```

如果用户说“关掉字幕”“停止实时字幕”“恢复电脑声音”，优先执行：

```bash
bash "{baseDir}/scripts/stop-senseaudio-floating-audio-assistant.sh"
```

## Requirements

这个 skill 伴随 AudioClaw 使用，默认当前环境已经有可调用的 `audioclaw agent`。实时字幕、翻译、TTS 和音乐生成使用 SenseAudio；最近项目的“整理/关键信息提取/模板处理”必须交给 AudioClaw agent，不要用本地假结果兜底。

必需设备和系统依赖：

- macOS 桌面环境，原生浮窗由 Swift/AppKit 实现。
- `BlackHole 2ch`：作为系统输出音频的虚拟采集设备。
- `Multi-Output Device`：在 Audio MIDI Setup 中创建，包含真实扬声器/耳机和 `BlackHole 2ch`。
- `SwitchAudioSource`：来自 `switchaudio-osx`，用于启动时切换到多输出设备、停止时恢复原输出。
- `swiftc`：来自 Xcode Command Line Tools，用于编译原生浮窗。
- `python3` 和 `bash`：用于实时 ASR runner、诊断脚本和包装脚本。
- 可访问 SenseAudio API 的网络环境。

常用安装和打开方式：

```bash
xcode-select --install
brew install switchaudio-osx
bash "{baseDir}/scripts/open_audio_midi_setup.sh"
```

如果没有 Homebrew，手动安装 `switchaudio-osx` 后确保 `SwitchAudioSource` 在 `PATH` 中即可。

## Configuration

凭据由当前 AudioClaw workspace 或运行环境提供，上传包内不携带任何本地凭据、密钥值或环境变量样板。

运行时需要可用的 SenseAudio API key；`SENSEAUDIO_API_KEY` 是首选名称，`AUDIOCLAW_ASR_API_KEY` 作为兼容名称保留。不要把 API key 打印到聊天里；检查脚本只报告是否存在。

音频路由配置：

- 在 Audio MIDI Setup 里创建 `Multi-Output Device`。
- 设备名可以是系统默认的 `Multi-Output Device` 或中文 `多输出设备`，启动脚本会优先查找这两个名称。
- 勾选当前实际听音设备，例如耳机、显示器音频或扬声器。
- 同时勾选 `BlackHole 2ch`。
- 启动脚本会尝试切换到多输出设备；停止脚本会恢复原输出和音量。

外部参数和运行态输入：

- 快速 ASR 的源语言。
- SenseAudio ASR/翻译的目标语言。
- 复制文本朗读的 TTS 音色。
- 音乐工坊的提示词、风格参数、历史歌曲名称和播放状态。
- 最近项目整理模板，可选择预设模板、编辑自定义模板或导入模板文件。
- AudioClaw agent 接收所选模板和保存的 SenseAudio ASR 原文，返回整理结果；skill 本身不保存额外 agent 密钥。

## Health Check

为了便于维护和排障，这个 skill 内置了轻量诊断入口和可复用预设：

- `scripts/senseaudio_api_smoke.py`: 输出当前 SenseAudio API 配置摘要，包含 ASR WebSocket、TTS 和音乐生成入口；默认不消耗额度，`--live-tts` 才真实调用。
- `scripts/doctor-senseaudio-floating-audio-assistant.sh`: 本地健康检查入口，用来确认 manifest、启动脚本、诊断 JSON 和预设文件仍然可用。
- `runtime/realtime_interpreter/`: 浮窗 UI、音频采集、SenseAudio runner、TTS、音乐生成和 AudioClaw agent 整理的纯文本运行时源码。
- `presets/`: 整理模板和音乐生成参数样板，不包含真实密钥或环境变量内容。
- `references/quickstart.md`: 精简启动流程。
- `references/operator_notes.md`: 面向使用者的安装、配置和启动摘要。
- `references/senseaudio_integration.md`: SenseAudio 接入说明。
- `references/troubleshooting.md`: 常见失败路径。

## Troubleshooting

没有字幕时，按顺序检查：

1. 运行 `check-senseaudio-floating-audio-assistant-setup.sh`
2. 确认 macOS 当前输出是 `多输出设备` / `Multi-Output Device`
3. 播放一段真实音频后重新开始 ASR
4. 如果 SenseAudio 连接失败，先确认 AudioClaw 运行环境是否注入了 SenseAudio 凭据，再看实时并发配额
5. 如果停止后电脑没声音，运行停止脚本恢复音频路由

“整理”功能依赖 `audioclaw agent` 的文本模型配置。若 AudioClaw 后端模型不返回，实时字幕、ASR、翻译、TTS 和音乐工坊仍可用，但整理会等待真实 AudioClaw 结果；不要伪造本地兜底结果。
