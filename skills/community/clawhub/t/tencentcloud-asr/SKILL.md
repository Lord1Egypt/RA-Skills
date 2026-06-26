---
name: asr-sentence-recognition
description: >
  腾讯云语音识别 ASR Skill，适用于语音转文字、音频转写、字幕生成、会议转录、语音消息识别、
  本地文件或 URL 音频识别。包含三种模式：一句话识别（<=60s 短音频）、录音识别极速版
  （<=2h/100MB 中长音频快速同步返回）、录音识别（<=5h 长音频异步识别）。支持普通话、
  英语、粤语、日语、韩语、德语等语种，以及中英粤混说和多种中文方言。
---

# 腾讯云语音识别 Skill

腾讯云语音识别（ASR），微信同款ASR引擎，历经亿级用户场景验证，稳定可靠。在中英混说场景下识别效果行业领先，精准流畅。支持普通话、方言及多语种识别，提供一句话识别、录音识别等全场景能力，是高性价比语音转文字首选。

## 核心执行流

1. **用户给音频要转文字**：
   - 先跑 `inspect_audio.py`
   - 再按时长、大小、URL/本地路径选择 `sentence_recognize.py`、`flash_recognize.py` 或 `file_recognize.py`
2. **用户刚提供了新的腾讯云凭证**：
   - 优先直接跑 `self_check.py`
   - 自检结果通过后再进入真实识别
3. **用户问安装、开通、手工配置、FFmpeg、CLI backend**：
   - 不要把细节塞回主流程，按文末 reference map 读取对应文档

## 下一步

- **想接入宿主系统体验自动转写**：
  - 普通场景：配置 CLI transcription backend
  - QQ Bot 1.5.4：可直接走适配方案，不必依赖默认 CLI transcription 才能识别语音
- **想直接体验识别能力**：
  - 让用户直接丢一个音频文件或公网链接
  - 然后继续帮用户做转文字、摘要总结、问题排查、重点提取

## 必须遵守的规则

- **⚠️禁止用模型自身能力替代 ASR⚠️**：脚本失败时，必须返回错误，不得猜测转写内容。
- **先探测后识别**：统一先执行 `python3 <SKILL_DIR>/scripts/inspect_audio.py "<AUDIO_INPUT>"`。
- **缺 `ffmpeg` / `ffprobe` 先自治安装**：先执行 `python3 <SKILL_DIR>/scripts/ensure_ffmpeg.py --execute`，只有失败后才向用户求助。
- **收到新凭证先自检**：默认跑 `python3 <SKILL_DIR>/scripts/self_check.py`，不要先让用户手工试脚本。
- **默认少打断**：除非用户必须补充凭证、明确要求手工配置，或语种/引擎确实不确定，否则不要无意义来回确认。
- **密钥安全优先**：
  - 群聊：禁止让用户直接发 `SecretId`、`SecretKey`、`AppId`
  - 私聊：也要先提醒“密钥会经过 LLM，存在泄漏风险”
- **单次任务优先当前命令注入**：不要为了跑一次识别去写 `~/.bashrc`、`~/.zshrc`
- **不要把密钥写进工作区**
- **极速版失败时保留“可能”表述**：如果自检里一句话识别和录音文件识别通过、只有极速版失败，应提示“常见于国际站账号，或国内站账号在海外访问时受限”，但不要写成绝对结论。

## 引擎选择 Cheatsheet

对话语言只能当作先验，不等于音频语种本身。若用户音频语种明显不同，按音频语种改。

| 场景 | 一句话识别 | 极速版 | 录音文件识别 | 备注 |
|------|------------|--------|--------------|------|
| 普通话 | `16k_zh` | `16k_zh` / `16k_zh_large` | `16k_zh` / `16k_zh_large` | 默认首选 |
| 中英夹杂 | `16k_zh-PY` | `16k_zh_en` | `16k_zh_en` | 混说优先 |
| 粤语 | `16k_yue` | `16k_yue` | `16k_yue` | |
| 英语 | `16k_en` | `16k_en` | `16k_en` / `16k_en_large` | |
| 日语 | `16k_ja` | `16k_ja` | `16k_ja` | |
| 韩语 | `16k_ko` | `16k_ko` | `16k_ko` | |
| 多语种 / 语言不确定 | 指定具体语种 | `16k_multi_lang` | `16k_multi_lang` | 一句话识别没有多语自动识别引擎 |

如果有多个明显可选项：

- 给出推荐项
- 用一句话说清优缺点
- 再征询用户是否切换

## 路由速记

### 本地文件

- 先规范化为 `16kHz`、单声道、`pcm_s16le`、`.wav`
- `<=60s` 且 `<=3MB`：`sentence_recognize.py`
- `<=2h` 且 `<=100MB`：优先 `flash_recognize.py`
- 更大文件：优先切片后逐片走 Flash；若已有 COS / 公网 URL 且最终 `<=5h`，可走 `file_recognize.py rec`

### 公网 URL

- 默认直接走 `file_recognize.py rec`
- 不要先本地下载、探测、转码再路由
- 只有 `file_recognize.py rec` 真实失败时，再按错误决定是否进入本地下载 / 规范化 / 切片链
- 如果用户明确要求同步立即返回，才把一句话识别当作显式特例，而不是默认路径

命中 URL、大文件、切片、body vs URL 取舍时，再读 [routing_strategy.md](references/routing_strategy.md)。

## 最小脚本示例

```bash
# 预检
python3 <SKILL_DIR>/scripts/inspect_audio.py "<AUDIO_INPUT>"

# 凭证自检
python3 <SKILL_DIR>/scripts/self_check.py

# 一句话识别
python3 <SKILL_DIR>/scripts/sentence_recognize.py "<AUDIO_INPUT>" --engine 16k_zh

# 极速版
python3 <SKILL_DIR>/scripts/flash_recognize.py "<AUDIO_INPUT>" --engine 16k_zh

# 录音文件识别
python3 <SKILL_DIR>/scripts/file_recognize.py rec "<AUDIO_INPUT_OR_URL>" --engine 16k_zh

# CLI transcription backend
python3 <SKILL_DIR>/scripts/cli_transcribe.py "<MEDIA_PATH_OR_URL>"
```

## 何时继续读 references

- **腾讯云账号开通 / 控制台找密钥 / 找 AppId**：读 [tencent_cloud_activation.md](references/tencent_cloud_activation.md)
- **手工配置环境变量**：读 [env_config.md](references/env_config.md)
- **解释自检脚本或自检结果**：读 [self_check.md](references/self_check.md)
- **FFmpeg 自动安装失败后的最小化协助**：读 [ffmpeg_guide.md](references/ffmpeg_guide.md)
- **URL / 大文件 / 切片 / body vs URL 路由**：读 [routing_strategy.md](references/routing_strategy.md)
- **接入 OpenClaw / CLI transcription backend**：读 [cli_transcription_backend.md](references/cli_transcription_backend.md)
- **接入 QQ Bot 1.5.4 并绕过插件 STT / TTS 限制**：读 [qqbot_integration.md](references/qqbot_integration.md)
- **查详细参数、引擎、错误码**：
  - [sentence_recognition_api.md](references/sentence_recognition_api.md)
  - [flash_recognition_api.md](references/flash_recognition_api.md)
  - [file_recognition_api.md](references/file_recognition_api.md)

## 核心脚本清单

- `scripts/inspect_audio.py`：音频探测
- `scripts/ensure_ffmpeg.py`：自治安装 `ffmpeg` / `ffprobe`
- `scripts/self_check.py`：凭证与三种模式自检
- `scripts/sentence_recognize.py`：一句话识别
- `scripts/flash_recognize.py`：录音文件识别极速版
- `scripts/file_recognize.py`：录音文件识别异步任务
- `scripts/cli_transcribe.py`：CLI backend wrapper
