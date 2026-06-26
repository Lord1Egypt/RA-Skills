---
name: senseaudio-let-claw-talk-universal
summary: 在 macOS 和 Windows 上启动一个持续监听的 SenseAudio 语音助手，用同一套技能逻辑实现免手打多轮语音对话。
description: 当用户希望把 AudioClaw 变成一个持续监听、开口就说、停顿就回答的本机语音助手时使用。这个 skill 支持 macOS 和 Windows 两个平台：优先尝试 Python 录音链路，macOS 上再提供原生 Swift 录音兜底；用户语音通过 SenseAudio ASR 转文字，再发给 audioclaw agent，并用 SenseAudio TTS 或系统语音读回结果。它保留可选的 WeSpeaker 后台服务和流式 TTS，但默认导出配置会尽量减少平台专属依赖。适合免手打问答、桌面语音助理、连续语音控制和原型演示。
user-invocable: true
metadata: {"openclaw":{"emoji":"🎙️","primaryEnv":"SENSEAUDIO_API_KEY","requires":{"bins":["python3"],"env":["SENSEAUDIO_API_KEY"]},"skillKey":"senseaudio-let-claw-talk-universal"}}
---

# SenseAudio-Let-Claw-Talk-Universal

当用户想要下面这些能力时，使用这个 skill：

- 一直开着麦克风，开口就能和 AudioClaw 对话
- 不想切换到专门的 CLI 或 TUI，只要功能能跑
- 想在本机做持续语音问答、语音助手、免手打交互
- 想继续使用已经调通的 SenseAudio ASR 和 TTS
- 想在 macOS 和 Windows 上复用同一套语音助手逻辑
- 想按需开启 WeSpeaker 声纹验证，把后台模型常驻起来减少冷启动

高优先级触发说法：

- 打开持续语音助手
- 开启持续监听语音模式
- 打开免手打语音模式
- 进入本机语音助手模式
- 帮我打开一直监听的语音助手
- 用 `$senseaudio-let-claw-talk-universal` 启动语音助手

不适合：

- 只想转写单条语音
- 只想把一段文字转成语音
- 想做飞书消息内的一次性语音收发

## Default behavior

这个 skill 默认：

- 在 macOS 和 Windows 上都使用同一套持续监听主循环
- 默认优先使用 `auto` 录音后端：
  - 如果 `numpy + sounddevice + webrtcvad` 可用，就走 Python 录音
  - 如果在 macOS 上且 Python 录音不可用，就回退到原生 Swift 录音器
- 导出的默认配置不会依赖 WeSpeaker、流式 TTS、状态音这些可选能力
- 用当前 skill 内置的 SenseAudio ASR 客户端做语音识别
- 用 `audioclaw agent` 跑对话
- 用当前 skill 内置的 SenseAudio TTS 客户端做语音播报，或用系统语音做本地兜底
- 导出的默认设置会先关闭 SenseAudio 流式 TTS，优先走整段播报，减少对 `miniaudio` 和流式链路调优的依赖
- 如果用户后面想启用流式 TTS，可以再手动打开
- 当前 skill 内置了常用音色目录和克隆音色登记，不依赖其他语音 skill
- 默认关闭状态提示音，减少平台差异和额外依赖
- 如果用户手动打开状态提示音，每次重新进入监听前，会先播一个轻提示音，告诉用户现在开始收音
- 默认启动时会先做一次自检：
  - 检查 Python 解释器
  - 检查录音后端依赖
  - 检查 ASR / TTS API key
  - 检查当前音色是否真的可用
- 默认唤醒词是 `贾维斯`
- 默认睡眠词是 `贾维斯休息`
- 默认唤醒保持时间是 `90` 秒
- 默认启动后会先处于休眠状态，不会直接进入可对话态
- 休眠态默认会先走单独的唤醒识别模型，当前默认是 `sense-asr-deepthink`
- 如果想改成更轻的唤醒模型，可以手动指定 `--wake-asr-model sense-asr-lite`
- 默认语速是 `1.25`
- 导出的默认设置不会自动开启 WeSpeaker
- 导出的默认设置也不会默认开启流式 TTS
- 默认支持“播报时被新语音打断”
- 默认把打断敏感度调得更稳：
  - `interrupt grace = 1.2s`
  - `interrupt min speech = 0.35s`
  - `interrupt threshold = -16dB`
- 默认会多等一点静音再判断你说完了：
  - `silence seconds = 1.6s`
- 默认会把回复整理成更简短、更口语化、更适合直接念出来的表达
- 默认会尽量借鉴更自然的陪伴式交互风格：
  - 短句
  - 少解释
  - 少套话
  - 被插话后优先顺着用户这句往下接
- 默认会从 `~/.audioclaw/workspace/state/voiceclaw_preferences.json` 读取已记住的用户偏好
- 默认不会开启 WeSpeaker 声纹验证
- 如果开启 WeSpeaker：
  - 会自动拉起后台常驻服务并预热模型
  - 默认模型是 `chinese`
  - 默认阈值是 `0.72`
  - 后台状态和样本会保存在 `~/.audioclaw/workspace/state/wespeaker`
  - 用户级 WeSpeaker 环境默认应放在 `~/.audioclaw/workspace/tools/wespeaker/.venv`
  - 如果用户环境还没准备好，先看 `references/wespeaker_user_setup.md`

## 环境要求

### macOS 最小跑通环境

- 已安装商汤输入法 AudioClaw，并且能找到 CLI：
  - `/Applications/商汤输入法AudioClaw.app/Contents/Resources/claws/picoclaw/audioclaw-darwin-arm64`
  - 或 `/Applications/商汤输入法AudioClaw.app/Contents/Resources/claws/picoclaw/audioclaw-darwin-amd64`
- 有可用的 `python3`
- 已通过用户级凭据文件提供 SenseAudio key：
  - `~/.audioclaw/workspace/state/senseaudio_credentials.json`
- 如果没有安装 `numpy + sounddevice + webrtcvad`，当前 skill 会优先回退到 macOS 原生 Swift 录音器
- 使用原生 Swift 录音器时，建议本机有可用的命令行开发工具：
  - `xcode-select --install`

### Windows 最小跑通环境

- 已安装 Windows 版 AudioClaw，并且能找到内部 CLI：
  - `C:\Program Files\AudioClaw\resources\claws\picoclaw\audioclaw.exe`
- 已安装真实可用的 Python，推荐：
  - `Python 3.11 x64`
  - 或 `Python 3.12 x64`
- Windows 不建议把 `C:\Users\<用户名>\AppData\Local\Microsoft\WindowsApps\python.exe` 当成真实 Python
- 当前 Windows 版最小录音链路需要：
  - `numpy`
  - `sounddevice`
  - `webrtcvad`
  - `setuptools`
- 用户级凭据文件需要存在：
  - `C:\Users\<用户名>\.audioclaw\workspace\state\senseaudio_credentials.json`

推荐安装命令：

```powershell
py -3 -m pip install --upgrade pip setuptools
py -3 -m pip install numpy sounddevice webrtcvad
```

### 完整版服务环境

如果你想把这套 skill 开成更完整的桌面语音服务，建议补齐这些可选能力。

macOS / Windows 通用可选项：

- 可选流式 TTS：
  - `miniaudio`
- 可选 WeSpeaker 声纹验证：
  - 建议单独准备用户级虚拟环境
  - 不要塞进 skill 包
- 用户级共享凭据：
  - `~/.audioclaw/workspace/state/senseaudio_credentials.json`
  - 或 `C:\Users\<用户名>\.audioclaw\workspace\state\senseaudio_credentials.json`

WeSpeaker 完整环境建议：

- 推荐独立 Python 版本：
  - `Python 3.11`
- 推荐用户级环境目录：
  - macOS / Linux: `~/.audioclaw/workspace/tools/wespeaker/.venv`
  - Windows: `C:\Users\<用户名>\.audioclaw\workspace\tools\wespeaker\.venv`
- 典型依赖：
  - `torch`
  - `torchaudio`
  - `soundfile`
  - `PyYAML`
  - `requests`
  - `onnxruntime`
  - `s3prl`
  - `openai-whisper`
  - `peft`
  - `wespeaker`

说明：

- 当前导出包默认关闭 WeSpeaker
- 当前导出包默认关闭 SenseAudio 流式 TTS
- 这两项属于完整版增强能力，不影响最小跑通链路
- Windows 上如果说“录入我的声音”后明显卡很久，优先检查：
  - `C:\Users\<用户名>\.audioclaw\workspace\state\wespeaker\service.log`
  - 以及 `voiceclaw_runtime.log`

## 日志与排障

当前 skill 现在保留了 3 组用户级日志/状态文件：

- 运行时状态：
  - `~/.audioclaw/workspace/state/voiceclaw_runtime_state.json`
- 运行时事件日志：
  - `~/.audioclaw/workspace/state/voiceclaw_runtime.log`
- agent 原始错误日志：
  - `~/.audioclaw/workspace/state/voiceclaw_agent_error.log`

Windows 上对应路径是：

- `C:\Users\<用户名>\.audioclaw\workspace\state\voiceclaw_runtime_state.json`
- `C:\Users\<用户名>\.audioclaw\workspace\state\voiceclaw_runtime.log`
- `C:\Users\<用户名>\.audioclaw\workspace\state\voiceclaw_agent_error.log`

如果你遇到“聊着聊着突然听不到我说话了”，优先看：

- `voiceclaw_runtime.log`

常见判断方式：

- 如果里面反复出现 `capture_no_speech`
  - 更像是麦克风/VAD 没起录，先查录音环境和阈值
- 如果反复出现 `asr_empty`
  - 更像是录到了声音，但 ASR 没给出有效文本
- 如果反复出现 `wake_blocked`
  - 更像是当前还在休眠态，没有命中唤醒词
- 如果出现 `agent_error`
  - 再去看 `voiceclaw_agent_error.log`

## Main command

默认最推荐直接用启动器，它会优先选择已经装好依赖的那套 Python，并带上更少依赖的默认参数：

```bash
bash "{baseDir}/scripts/start_senseaudio_let_claw_talk_universal.sh"
```

Windows 可以直接运行：

```powershell
py -3 "{baseDir}\scripts\start_senseaudio_let_claw_talk_universal.py"
```

说明：

- Windows 端需要真实可用的 Python 解释器
- 推荐优先使用 `py -3`
- 如果系统里只有 `C:\Users\<用户名>\AppData\Local\Microsoft\WindowsApps\python.exe` 这种应用商店别名，启动器会直接提示你安装 Python，或手动设置 `VOICECLAW_PYTHON_BIN`
- 不建议把真实 SenseAudio key 写进 skill 包本身。更稳的做法是写到用户级文件：
  - `C:\Users\<用户名>\.audioclaw\workspace\state\senseaudio_credentials.json`
  - 或用当前 skill 自带脚本写入：
    `py -3 "{baseDir}\scripts\configure_senseaudio_credentials.py" --api-key "你的sk-..."`

如果要手动指定 Python，再用 SenseAudio TTS：

```bash
python3 "{baseDir}/scripts/run_continuous_voice_assistant.py" \
  --tts-mode senseaudio \
  --capture-backend auto \
  --no-senseaudio-streaming-tts \
  --voice-id male_0004_a \
  --emotion calm \
  --tts-speed 1.25
```

如果只想快速试运行，也可以先用系统播报：

```bash
python3 "{baseDir}/scripts/run_continuous_voice_assistant.py" \
  --tts-mode system
```

默认启动后，先说：

```text
贾维斯
```

再继续提问。

如果想让它立刻回到休眠，可以说：

```text
贾维斯休息
```

如果想让它记住你的偏好，可以直接说：

```text
记住不要打断我
记住语速 1.1
记住多等一下再截断
记住以后更简短一点
记住以后展开一点
记住当前偏好
清除偏好
```

如果想查看当前状态，可以直接说：

```text
当前设置
```

如果想开启或使用 WeSpeaker，可直接说：

```text
开启 WeSpeaker 声纹验证
录入我的声音
重录我的声音
查看 WeSpeaker 状态
关闭 WeSpeaker 声纹验证
关闭只听我模式
启动后台声纹
停止后台声纹
```

说明：

- 说 `录入我的声音` 后，现在默认只录 1 句来建档
- skill 会直接给出一条可照读的示例句，用户从下一句开始照读即可
- 开启后，后台会常驻预热，后续验证会更快
- 当前 WeSpeaker 是可选能力，不开就不会影响原来的持续语音助手流程
- 当前 skill 会优先过滤与最近播报内容高度相似的回录，避免把刚说过的话再次当成新的用户输入
- 如果上一轮播报被用户打断，当前 skill 不会额外加模型，也不会做复杂规则判断。
  它只会把“上一轮回答播报到一半被打断了”这件事，用一句很轻的上下文告诉现有 agent，
  让下一轮更自然地接话，避免重新铺垫上一整段。

如果想换音色，也可以直接说：

```text
列出音色
有哪些音色
换成温柔御姐
切换到 male_0018_a
记住默认音色是 温柔御姐
以后都用 male_0004_a
注册克隆音色 vc-123456 叫 我的声音
```

如果某个音色当前无权限或暂时不可用，skill 会优先保留当前可用音色，或者自动切到一个能正常播报的兜底音色。

一键启动：

- 运行：

```bash
bash "{baseDir}/scripts/start_senseaudio_let_claw_talk_universal.sh"
```

如果要让 AudioClaw / OpenClaw 直接拉起这个长期语音模式，优先运行：

```bash
python3 "{baseDir}/scripts/launch_senseaudio_let_claw_talk_universal.py"
```

在 Windows 工具侧，优先运行：

```powershell
py -3 "{baseDir}\scripts\launch_senseaudio_let_claw_talk_universal.py"
```

原因：

- 持续监听属于长期麦克风进程
- 不适合用 `exec + nohup + &` 在工具调用后台硬挂
- 更稳的做法是让 skill 直接打开一个新的终端窗口承载会话
- 这个启动器会按平台自动选择：
  - macOS：Terminal + `osascript`
  - Windows：Python + `CREATE_NEW_CONSOLE`
  - Linux：常见 terminal emulator

## Trigger-to-action rule

如果用户是在 AudioClaw / OpenClaw 里直接说：

- “打开持续语音助手”
- “开启持续监听语音模式”
- “打开免手打语音模式”
- “进入本机语音助手模式”
- “打开本机语音助手”

不要只返回命令，也不要改用 `nohup` 后台启动。
也不要只回复“好，已进入。你直接说。”这类假状态切换。

优先直接执行：

```bash
python3 "{baseDir}/scripts/launch_senseaudio_let_claw_talk_universal.py"
```

如果当前运行环境是 Windows，优先执行：

```powershell
py -3 "{baseDir}\scripts\launch_senseaudio_let_claw_talk_universal.py"
```

不要在工具侧直接执行长期入口；工具调用更适合用 `launch_*.py`，它会拉起新终端后立刻返回 `opened_terminal`。

如果用户还补了偏好，再把参数附上，例如：

- 唤醒词：`--wake-phrase "贾维斯"`
- 打断播报：`--interrupt-playback`
- 调试：`--debug`

这两个入口默认等价于：

- `--tts-mode senseaudio`
- `--capture-backend auto`
- `--voice-id male_0004_a`
- `--emotion calm`
- `--tts-speed 1.25`
- `--no-senseaudio-streaming-tts`
- `--speaker-verification-backend none`
- `--no-status-sounds`

如果需要改默认值，可以在启动前设置：

```bash
export VOICECLAW_TTS_MODE=system
export VOICECLAW_VOICE_ID=male_0018_a
export VOICECLAW_EMOTION=warm
export VOICECLAW_TTS_SPEED=1.25
export VOICECLAW_SENSEAUDIO_STREAMING_TTS=0
export VOICECLAW_SENSEAUDIO_STREAMING_BACKEND=auto
export VOICECLAW_WAKE_PHRASE=贾维斯
export VOICECLAW_SLEEP_PHRASE=贾维斯休息
export VOICECLAW_STATUS_SOUNDS=0
export VOICECLAW_SPEAKER_BACKEND=none
export VOICECLAW_WESPEAKER_THRESHOLD=0.72
export VOICECLAW_WESPEAKER_PYTHON=$HOME/.audioclaw/workspace/tools/wespeaker/.venv/bin/python
export VOICECLAW_EXTRA_ARGS='--wake-phrase 贾维斯 --sleep-phrase 贾维斯休息 --interrupt-playback'
```

如果想把流式模式升级成 `miniaudio` 的 MP3 解码播放，可选安装：

```bash
python3 -m pip install --user miniaudio
```

然后保持：

```bash
export VOICECLAW_SENSEAUDIO_STREAMING_BACKEND=auto
```

如果想强制只用这条后端，也可以显式传：

```bash
python3 "{baseDir}/scripts/run_continuous_voice_assistant.py" \
  --tts-mode senseaudio \
  --senseaudio-streaming-tts \
  --senseaudio-streaming-backend miniaudio
```

如果要启用唤醒词：

```bash
python3 "{baseDir}/scripts/run_continuous_voice_assistant.py" \
  --tts-mode senseaudio \
  --wake-phrase "贾维斯" \
  --sleep-phrase "贾维斯休息" \
  --wake-sticky-seconds 90
```

如果要默认开启 WeSpeaker 声纹验证：

```bash
python3 "{baseDir}/scripts/run_continuous_voice_assistant.py" \
  --tts-mode senseaudio \
  --speaker-verification-backend wespeaker \
  --wespeaker-python "$HOME/.audioclaw/workspace/tools/wespeaker/.venv/bin/python" \
  --wespeaker-threshold 0.8
```

如果用户环境还没装好，先按这个文件准备：

```text
{baseDir}/references/wespeaker_user_setup.md
```

如果要关闭默认唤醒词：

```bash
python3 "{baseDir}/scripts/run_continuous_voice_assistant.py" \
  --tts-mode senseaudio \
  --no-wake-phrase
```

如果要关闭默认睡眠词：

```bash
python3 "{baseDir}/scripts/run_continuous_voice_assistant.py" \
  --tts-mode senseaudio \
  --no-sleep-phrase
```

如果要启用播报打断：

```bash
python3 "{baseDir}/scripts/run_continuous_voice_assistant.py" \
  --tts-mode senseaudio \
  --interrupt-playback
```

如果想临时关闭默认打断：

```bash
python3 "{baseDir}/scripts/run_continuous_voice_assistant.py" \
  --tts-mode senseaudio \
  --no-interrupt-playback
```

## What to adjust

如果用户说“容易误触发”或“环境噪音太大”，优先调这些参数：

- `--speech-threshold-db -18`
- `--silence-seconds 1.6`
- `--vad-mode 3`

如果用户想只测一轮，可以加：

```bash
--once
```

如果用户想用现成音频文件做链路验证，可以加：

```bash
--input-file /absolute/path/to/file.m4a --once
```

如果用户说“想先叫一声再开始对话”，优先加：

```bash
--wake-phrase "贾维斯"
```

如果用户明确说“不需要唤醒词”或“直接开口就听”，优先加：

```bash
--no-wake-phrase
```

如果用户说“播报时我还想插话”，优先加：

```bash
--interrupt-playback
```

## Exit behavior

持续模式里：

- 用户说“退出”“停止”“结束”会主动退出
- 用户说“`贾维斯休息`”会主动进入休眠，但不会退出程序
- 或按 `Ctrl+C` 退出
- 如果开启了唤醒词，只有命中唤醒词或仍在唤醒窗口内时，当前这轮语音才会被送去对话

## Runtime notes

- 默认会复用 `~/.audioclaw/workspace/state/senseaudio_credentials.json` 里的 `SENSEAUDIO_API_KEY`
- 默认会把已记住的用户偏好保存在 `~/.audioclaw/workspace/state/voiceclaw_preferences.json`
- 默认会把当前运行状态摘要保存在 `~/.audioclaw/workspace/state/voiceclaw_runtime_state.json`
- `run_continuous_voice_assistant.py` 现在自带当前 skill 内部的 SenseAudio ASR、SenseAudio TTS 和常用音色目录，不再依赖其他语音 skill
- 如果用户只要“实现功能”，不要再额外引导去做 TUI；直接启动这个 skill 的持续监听脚本
- 如果用户在意误触发，建议先不开 `--interrupt-playback`，先把阈值和唤醒词调顺
- 如果用户觉得播报被自己声音或外放误打断，优先加 `--no-interrupt-playback`，或调大 `--interrupt-grace-seconds`

## Resources

- `scripts/run_continuous_voice_assistant.py`
  - 主入口，负责持续监听、ASR、agent 调用和语音播报
- `scripts/local_senseaudio_asr.py`
  - 当前 skill 内置的 SenseAudio ASR 客户端
- `scripts/local_senseaudio_tts.py`
  - 当前 skill 内置的 SenseAudio TTS 客户端
- `scripts/local_voice_catalog.py`
  - 当前 skill 内置的常用音色目录和克隆音色登记
- `scripts/start_senseaudio_let_claw_talk_universal.sh`
  - macOS / Linux 命令行短入口
- `scripts/start_senseaudio_let_claw_talk_universal.py`
  - 跨平台长期运行入口，负责设置默认环境并启动语音助手主循环
- `scripts/launch_senseaudio_let_claw_talk_universal.py`
  - 给 AudioClaw / OpenClaw 调用的跨平台稳定启动器，会按平台打开新的终端窗口并接管长期语音会话；Windows 端不再依赖 bat/ps1
- `scripts/macos_mic_capture.swift`
  - macOS 麦克风录音兜底实现
