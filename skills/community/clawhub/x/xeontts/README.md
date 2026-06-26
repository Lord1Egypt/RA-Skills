# Xeon TTS Skill

基于 OpenVINO Qwen3-TTS Base/Custom 模型的本地语音合成技能，为 OpenClaw 的 QQBOT 提供两类工作流：

- 音色克隆：用户先声明要克隆音色，再上传 3 到 5 秒参考音频，随后用 Base 模型生成目标语音
- 风格化 TTS：用户直接要求“用某种语气朗读一段话”，系统调用 Custom 模型生成音频并落盘

这个 skill 刻意不占用 xeon_asr 的端口或全局音频配置：

- Flask TTS 服务：5002
- Node 工作流网关：9002
- OpenClaw 配置写入：`channels.qqbot.xeonTts`

它不会覆盖 `tools.media.audio`，也不会改动 `channels.qqbot.stt`，因此可以和已安装的 xeonasr 共存。

## 架构

双服务架构：

| 服务 | 端口 | 类型 | 作用 |
|------|------|------|------|
| Flask TTS | 5002 | Python | 加载 Base/Custom OpenVINO TTS 模型并执行推理 |
| TTS Workflow | 9002 | Node.js | 维护 QQBOT 会话状态、校验时长、保存输出、分流 clone/custom 请求 |

## 模型与能力

默认配置使用两套模型：

- Base：`qwen3_tts_0.6b_base_openvino`，用于音色克隆
- Custom：`qwen3_tts_0.6b_custom_openvino`，用于常规 TTS 和指定语气生成

时长约束默认值：

- 参考音频：必须在 3 到 5 秒之间
- Base 克隆输出：最多约 20 秒
- Custom 输出：最多约 30 秒
- 参考音频和生成结果：默认只保留 7 天，之后自动清理

如果用户文本里显式要求超过最大时长，或根据文本长度估算会超过上限，skill 会直接拒绝并提示拆分内容。

## 快速开始

### 1. 安装 skill

```bash
clawhub install xeontts
cd "$HOME/.openclaw/workspace/skills/xeontts"
bash install.sh
```

如果你是从源码目录运行：

```bash
cd /path/to/xeon_tts
bash install.sh
```

### 2. 模型下载

安装脚本现在默认会尝试从这两个 Hugging Face 仓库下载模型：

```bash
aurora2035/Qwen3-TTS-12Hz-0.6B-Base-OpenVINO-INT8
aurora2035/Qwen3-TTS-12Hz-0.6B-CustomVoice-OpenVINO-INT8
```

如果后续你要切换到别的仓库，再在安装前覆盖这些环境变量：

```bash
export BASE_MODEL_REPO=your-org/Qwen3-TTS-12Hz-0.6B-Base-OpenVINO-INT8
export CUSTOM_MODEL_REPO=your-org/Qwen3-TTS-12Hz-0.6B-CustomVoice-OpenVINO-INT8
bash install.sh
```

现在 `xdp-tts-service` 已经发布到 PyPI，安装脚本默认直接执行：

```bash
pip install xdp-tts-service
```

只有在你需要测试本地 wheel 或私有包时，才需要覆盖安装源：

```bash
export XDP_TTS_PIP_SPEC=/absolute/path/to/xdp_tts_service-0.1.0-py3-none-any.whl
bash install.sh
```

### 3. Base 模型是否还需要原始 checkpoint

如果你上传的是用当前最新版转换脚本导出的 `Qwen3-TTS-12Hz-0.6B-Base-OpenVINO-INT8`，并且导出目录里已经包含 processor 相关文件以及 `speech_tokenizer/` 子目录，那么默认不再需要单独上传原始 Base checkpoint。

只有两种情况还需要额外提供 `BASE_CHECKPOINT_PATH`：

- 你上传的是较早期导出的 Base OV 目录，里面缺少 processor 或 speech tokenizer 权重
- 你后续发现某些机器上 Base voice clone 仍然需要旧的 fallback tokenizer 路径

也就是说，按你现在的发布计划，优先只上传 `Qwen3-TTS-12Hz-0.6B-Base-OpenVINO-INT8` 是合理的。

## OpenClaw / QQBOT 工作流

### 1. 音色克隆

用户在 QQBOT 中说：

- `我要克隆音色`
- `帮我克隆我的声音`

工作流会这样运行：

1. xeontts 识别为 clone 任务，不走 xeonasr
2. Bot 回复：请上传 3 到 5 秒参考音频
3. 如果机器上同时安装了 xeonasr，QQBOT 的语音消息会先到 9001；ASR 会识别当前会话处于音色克隆流程，并把这段音频转交给 xeontts
4. xeontts 优先用 `ffprobe` 校验时长；如果机器上没有可用的 `ffprobe`，对 WAV 文件会自动回退到读取 WAV 头部信息来校验时长
5. 如果时长不合规，立即返回错误
6. 如果合规，保存参考音频到本地 `references/`
7. Bot 再要求用户发送要朗读的文本
8. 使用 Base 模型生成音频，并把 wav 文件落盘到 `outputs/`

系统会明确告知用户：参考音频和生成结果默认只保留 7 天，之后会自动清理。

这里的关键点是：ASR 仍然会删除自己的临时文件，但删除前已经把参考音频转交给 TTS 侧保存，所以不会再出现“文件被 ASR 清理导致音色克隆拿不到参考音频”的问题。

注意：默认使用 `voice_clone_xvector` 路径，原因是它对参考音频容错更高，但仍然使用的是 Base 模型。

如果后续你发现某个旧导出 Base 模型在目标机上无法完成 voice clone，再补一个原始 Base checkpoint 即可，不影响当前的开源默认方案。

说明：

- `ffprobe` 是 FFmpeg 工具链里的媒体探测工具，用来读取音频时长、编码、采样率等元数据
- 这里优先使用它，是因为它对 mp3、m4a、wav 等多种格式都更稳定
- 当前源码已经对 WAV 做了无 `ffprobe` 回退，所以它不是 WAV 场景的硬依赖；但如果你希望发布包开箱支持更多参考音频格式，仍建议目标机安装 FFmpeg

### 2. 指定语气生成

用户在 QQBOT 中说：

- `用开心的语气朗读：今天是个好日子`
- `生成语音：请提醒我下午三点开会`

工作流会这样运行：

1. 如果用户提到具体语气，就将其转成 `instruct_text`
2. 如果没有提到，默认按 `普通` 语气
3. 调用 Custom 模型生成音频
4. 将音频落盘到 `outputs/`
5. 回复用户保存路径，并明确告知文件默认只保留 7 天

## 文件清理策略

当前默认启用按天自动清理：

- `references/` 下的参考音频，默认保留 7 天
- `outputs/` 下的生成结果，默认保留 7 天
- 超过保留期的文件会在服务启动时和每次新保存文件后自动清理

安装脚本会先从 `config.example.json` 生成本地 `config.json`，其中默认已经包含 `fileRetentionDays`。

如果你要调整保留期，可以在本地生成的 `config.json` 里修改 `fileRetentionDays`。完整示例如下：

```json
{
  "port": 9002,
  "flaskTtsUrl": "http://127.0.0.1:5002/api/tts/synthesize",
  "flaskHealthUrl": "http://127.0.0.1:5002/api/health",
  "cloneModel": "qwen3_tts_0.6b_base_openvino",
  "cloneMode": "voice_clone_xvector",
  "customModel": "qwen3_tts_0.6b_custom_openvino",
  "defaultSpeaker": "Vivian",
  "defaultLanguage": "Chinese",
  "minReferenceDurationSec": 3,
  "maxReferenceDurationSec": 5,
  "maxCloneOutputSeconds": 20,
  "maxCustomOutputSeconds": 30,
  "estimatedCharsPerSecond": 4,
  "fileRetentionDays": 7,
  "outputDir": "./outputs",
  "referencesDir": "./references",
  "runtimeDir": "./runtime",
  "sessionStateFile": "./runtime/session_state.json",
  "openclawSession": "default"
}
```

## 管理命令

```bash
cd "$HOME/.openclaw/workspace/skills/xeontts"

bash start_all.sh
bash stop_tts.sh
bash self_check.sh

curl http://127.0.0.1:5002/api/health
curl http://127.0.0.1:9002/health
```

## 主要接口

### 工作流意图入口

```bash
curl -X POST http://127.0.0.1:9002/api/workflow/message \
  -H 'Content-Type: application/json' \
  -d '{"sessionId":"default","userId":"qq-1001","text":"我要克隆音色"}'
```

### 上传参考音频

```bash
curl -X POST http://127.0.0.1:9002/api/workflow/reference-audio \
  -F sessionId=default \
  -F userId=qq-1001 \
  -F file=@sample.wav
```

### 继续克隆文本

```bash
curl -X POST http://127.0.0.1:9002/api/workflow/message \
  -H 'Content-Type: application/json' \
  -d '{"sessionId":"default","userId":"qq-1001","text":"请用我的音色说，今天下班早点休息。"}'
```

### 自定义语气生成

```bash
curl -X POST http://127.0.0.1:9002/api/tts/custom-speak \
  -H 'Content-Type: application/json' \
  -d '{"text":"欢迎使用 Xeon TTS","style":"开心","speakerId":"Vivian"}'
```

## 目录结构

```text
xeon_tts/
├── install.sh
├── setup_env.sh
├── configure_openclaw_integration.sh
├── install_systemd_services.sh
├── start_tts_service.sh
├── start_all.sh
├── stop_tts.sh
├── self_check.sh
├── server.js
├── config.example.json
├── tts_config.example.json
├── SKILL.md
└── README.md
```

## 发布清理

开源时不要提交这些本机运行产物：

- `venv/`
- `node_modules/`
- `runtime/`
- `outputs/`
- `references/`
- `config.json`
- `tts_config.json`
- `*.log`
- `*.pid`

## 注意事项

- 这个 skill 只处理 TTS 和音色克隆，不处理转写
- 如果用户说的是“识别语音”“转文字”，应该交给 xeonasr
- 如果机器上没有可用的 `ffprobe`，WAV 参考音频仍可通过内置回退逻辑完成时长校验；若要稳定支持更多参考音频格式，仍建议安装 `ffmpeg`
- Base 模型仍建议使用干净、单人声、较少背景噪声的参考音频
