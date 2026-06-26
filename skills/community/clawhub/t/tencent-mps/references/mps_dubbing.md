# 语音合成与音色复刻参数与示例 — `mps_dubbing.py`

**功能**：AI 语音合成与音色复刻，适用于有声书、播客、音视频配音等场景。
支持中、英、日、韩等 40+ 语种，可复刻真实人声音色，也可使用系统预设音色。

> ⚠️ 职责是**语音合成与音色复刻**，不涉及字幕、水印等画面处理。画面擦除请用 `mps_erase.py`；字幕生成请用 `mps_subtitle.py`。

## 运行模式

| 模式 | 接口 | 说明 |
|------|------|------|
| `clone` | SyncDubbing（同步） | 传入克隆音频，返回音色 ID（VoiceId）。建议音频时长 10~20 秒，单人清晰语音 |
| `tts` | SyncDubbing（同步） | 传入文本 + 音色 ID，返回合成 WAV 音频。文本 ≤ 2000 字符走同步接口，超出**自动切换**为 `async-tts` |
| `async-tts` | ProcessMedia（异步） | 长文本转语音，异步合成输出到 COS |
| `async-sts` | ProcessMedia（异步） | 语音转语音，对输入音视频做音色替换，异步输出到 COS |

## 参数说明

### 通用参数

| 参数 | 说明 |
|------|------|
| `--mode` | 运行模式（必填）：`clone` / `tts` / `async-tts` / `async-sts` |
| `--voice-id` | 音色 ID（系统音色或 `clone` 模式返回的自定义音色）。`tts` / `async-tts` / `async-sts` 使用 |
| `--verbose` / `-v` | 输出详细信息（含完整请求参数和响应） |
| `--dry-run` | 仅打印请求参数，不实际调用 API |
| `--region` | MPS 服务区域（优先读取 `TENCENTCLOUD_API_REGION` 环境变量，默认 `ap-guangzhou`）。同步模式可省略 |

### 文本参数（`tts` / `async-tts`）

| 参数 | 说明 |
|------|------|
| `--text` | 合成文本。`tts` 模式 ≤ 2000 字符走同步；超出自动切换为异步（无需手动改 `--mode`） |
| `--text-lang` | 文本语言（默认 `zh` 中文）。如 `en` / `ja` / `ko` / `fr` 等 |

### 克隆音频参数（`clone` 同步模式）

| 参数 | 说明 |
|------|------|
| `--audio-file` | 本地克隆音频文件路径（支持 WAV / MP3 / MP4 等）。建议时长 10~20 秒，单人清晰语音 |
| `--audio-url` | 克隆音频 URL（`--audio-file` 为空时使用） |
| `--audio-lang` | 克隆音频语言（默认 `zh`） |
| `--time-ranges` | 指定音频的克隆时间范围，格式 `start,end`（秒，如 `5.2,20`）。可多次指定 |

### 异步模式克隆视频参数（`async-tts` / `async-sts`）

| 参数 | 说明 |
|------|------|
| `--clone-video-url` | 克隆音色的视频/音频 URL（要求时长 ≥ 5 秒，单人说话人） |
| `--clone-video-lang` | 克隆视频/音频的语言（默认 `zh`） |
| `--src-lang` | 源视频/音频的语言（`async-sts` 使用） |

### 异步任务输入源（`async-tts` / `async-sts`）

| 参数 | 说明 |
|------|------|
| `--url` | 输入视频/音频 URL。`async-tts` 可不填（填任意可访问链接作占位）；`async-sts` 必填 |
| `--cos-input-bucket` | 输入 COS Bucket 名称（与 `--cos-input-key` 配合使用） |
| `--cos-input-region` | 输入 COS Bucket 区域 |
| `--cos-input-key` | 输入 COS 对象 Key（如 `/input/video.mp4`） |

### 音频质量参数（可选）

| 参数 | 说明 |
|------|------|
| `--sample-rate` | 输出采样率。支持：`8000` / `16000` / `22050` / `32000` / `44100`（默认 `16000`）。`async-sts` 不支持 |
| `--pitch` | 音调，取值范围 `[-12, 12]`，默认 `0`（原音色） |
| `--duration` | 合成音频目标时长（秒，如 `5.2`）。仅同步模式有效 |

### 同步任务输出（`clone` / `tts`）

| 参数 | 说明 |
|------|------|
| `--output` / `-o` | 合成音频本地保存路径（如 `/tmp/output.wav`）。不指定时自动生成文件名保存到当前目录 |
| `--output-url` | 请求接口返回音频 URL（有效期 24 小时）而非 base64 数据 |

### 异步任务输出配置（`async-tts` / `async-sts`）

| 参数 | 说明 |
|------|------|
| `--output-bucket` | 输出 COS Bucket 名称（默认取 `TENCENTCLOUD_COS_BUCKET` 环境变量） |
| `--output-region` | 输出 COS Bucket 区域（默认取 `TENCENTCLOUD_COS_REGION` 环境变量） |
| `--output-dir` | 输出目录（默认 `/output/dubbing/`），以 `/` 开头和结尾 |
| `--output-pattern` | 输出文件名前缀，支持占位符 `{taskType}`、`{timestamp}` |
| `--no-wait` | 仅提交任务，不等待结果（默认自动轮询直到完成） |
| `--poll-interval` | 轮询间隔（秒），默认 `10` |
| `--max-wait` | 最长等待时间（秒），默认 `3600`（1 小时） |
| `--download-dir` | 异步任务完成后自动下载结果到指定本地目录 |
| `--notify-url` | 任务完成回调 URL（可选） |
| `--resource-id` | 资源 ID（默认使用账号主资源 ID） |

## 支持语种（`--text-lang` / `--audio-lang` / `--src-lang` / `--clone-video-lang`）

| 代码 | 语言 | 代码 | 语言 | 代码 | 语言 |
|------|------|------|------|------|------|
| `zh` | 中文 | `en` | 英语 | `ja` | 日语 |
| `ko` | 韩语 | `de` | 德语 | `fr` | 法语 |
| `es` | 西班牙语 | `it` | 意大利语 | `ru` | 俄语 |
| `pt` | 葡萄牙语 | `ar` | 阿拉伯语 | `hi` | 印地语 |
| `th` | 泰语 | `vi` | 越南语 | `id` | 印尼语 |
| `ms` | 马来语 | `tr` | 土耳其语 | `nl` | 荷兰语 |
| `pl` | 波兰语 | `sv` | 瑞典语 | `fi` | 芬兰语 |
| `yue` | 粤语 | `he` | 希伯来语 | `fa` | 波斯语 |

> 完整列表（40+ 种）见 `mps_dubbing.py` 中的 `SUPPORTED_LANGS` 字典。

## 强制规则

> ⚠️ **优先级说明**：以下规则按优先级从高到低排列，遇到多条规则同时匹配时，**优先使用编号更靠前的规则**。

- **【最高优先 - 模式选择】先判断任务类型**：
  - ✅ 需要"获取音色 ID"→ 使用 `--mode clone`，**必须**指定 `--audio-file` 或 `--audio-url`
  - ✅ 需要"文本转语音（短文本 ≤ 2000 字符）且需要等待结果"→ 使用 `--mode tts`，**必须**指定 `--voice-id`
  - ✅ 需要"文本转语音（短文本 ≤ 2000 字符）且用户说不等结果/先拿任务ID"→ 使用 `--mode async-tts`（同步 `tts` 模式无 TaskId 概念，`--no-wait` 在 `tts` 下报错）
  - ✅ 需要"文本转语音（长文本 > 2000 字符）"→ 直接使用 `--mode tts`，脚本**自动切换**为异步（无需手动写 `async-tts`）
  - ✅ 需要"对已有音视频文件做音色替换"→ 使用 `--mode async-sts`，**必须**指定 `--url` 或 COS 输入，且必须指定 `--voice-id` 或 `--clone-video-url`

- **VoiceId 必须使用完整的加密 base64 格式**：正确格式如 `v1_Pi1pR9Q9UHqVOrQ0YpZFwL+Q/...`（约 80+ 字符）。文档示例中截短的 ID（如 `s1_2GSzVAf00hl`）**无效**，会报 `decode encrypt voiceId failed`。应通过 `--mode clone` 获取真实 VoiceId 后再使用。

- **`async-tts` 的 `--url` 参数须为可正常访问的链接**：该参数仅作占位（TextToSpeech 不依赖输入文件内容），但若 URL 返回 404，任务会直接失败。建议填写自己 COS bucket 中已存在的任意文件 URL。

- **`--output-dir` 以 `/` 开头和结尾**：API 强制要求，脚本会自动补尾部 `/`，但建议显式指定，如 `--output-dir /output/dubbing/`。

- **异步模式必须配置 COS Bucket**：`async-tts` / `async-sts` 的输出文件写入 COS，必须通过 `--output-bucket` 或 `TENCENTCLOUD_COS_BUCKET` 环境变量指定输出 Bucket。

- **`async-only` 参数禁止用于同步模式**：`--clone-video-url`、`--output-dir`、`--no-wait`、`--download-dir` 等参数在 `clone` / `tts` 模式下会报错，仅 `async-tts` / `async-sts` 可用。

## 典型工作流

```
1. 音色复刻流程（先 clone，再 tts）：
   clone → 返回 VoiceId → tts --voice-id <VoiceId>

2. 直接使用系统音色：
   tts --voice-id <系统音色ID> --text "..."

3. 长文本合成（自动切换异步）：
   tts --text "超过2000字的长文本..." --voice-id <VoiceId>
   （脚本自动切换为 async-tts，无需手动指定）

4. 音视频音色替换：
   async-sts --url <视频URL> --voice-id <VoiceId>
```

## 示例命令

```bash
# ── 音色复刻（clone）─────────────────────────────────────────────────────────

# 传入本地音频文件复刻音色（建议 10~20 秒，单人清晰语音）
python scripts/mps_dubbing.py --mode clone --audio-file /path/to/voice.wav

# 传入音频 URL 复刻音色
python scripts/mps_dubbing.py --mode clone --audio-url https://example.com/voice.wav

# 传入音频 URL，指定音频语言
python scripts/mps_dubbing.py --mode clone \
    --audio-url https://example.com/voice.mp4 --audio-lang en

# ── 短文本语音合成（tts）─────────────────────────────────────────────────────

# 最简调用（使用系统音色）
python scripts/mps_dubbing.py --mode tts \
    --text "您好，欢迎使用腾讯云语音合成服务！" \
    --voice-id "v1_Pi1pR9Q9UHqVOrQ0YpZFwL+Q/..."

# 指定输出文件路径
python scripts/mps_dubbing.py --mode tts \
    --text "Hello, welcome!" \
    --voice-id "v1_Pi1pR9Q9UHqVOrQ0YpZFwL+Q/..." \
    --output /tmp/output.wav

# 调整采样率和音调
python scripts/mps_dubbing.py --mode tts \
    --text "您好" \
    --voice-id "v1_Pi1pR9Q9UHqVOrQ0YpZFwL+Q/..." \
    --sample-rate 44100 --pitch 2 --output /tmp/out.wav

# 英文合成
python scripts/mps_dubbing.py --mode tts \
    --text "Artificial intelligence changes the world." \
    --voice-id "v1_Pi1pR9Q9UHqVOrQ0YpZFwL+Q/..." \
    --text-lang en

# 长文本自动切换为异步（无需手动改 --mode）
python scripts/mps_dubbing.py --mode tts \
    --text "这是一段超过 2000 字符的超长文本..." \
    --voice-id "v1_Pi1pR9Q9UHqVOrQ0YpZFwL+Q/..." \
    --download-dir ./output/

# ── 先复刻音色，再合成语音 ────────────────────────────────────────────────────

# 第一步：复刻音色，记录返回的 VoiceId
python scripts/mps_dubbing.py --mode clone --audio-file voice.wav

# 第二步：用拿到的 VoiceId 合成
python scripts/mps_dubbing.py --mode tts \
    --text "您好，这是复刻的声音" \
    --voice-id "v1_<上一步返回的VoiceId>"

# ── 长文本转语音（async-tts）─────────────────────────────────────────────────

# 指定音色 ID，输出结果到 COS，完成后下载到本地
python scripts/mps_dubbing.py --mode async-tts \
    --text "这是一段超长的文本，适合使用异步接口处理..." \
    --voice-id "v1_Pi1pR9Q9UHqVOrQ0YpZFwL+Q/..." \
    --url "https://<bucket>.cos.ap-guangzhou.myqcloud.com/input/placeholder.wav" \
    --output-dir /output/tts/ \
    --download-dir ./output/

# 使用 COS 文件作为输入，克隆视频指定音色
python scripts/mps_dubbing.py --mode async-tts \
    --text "长文本..." \
    --clone-video-url https://example.com/train.mp4 \
    --cos-input-key /input/placeholder.wav \
    --output-dir /output/tts/

# 仅提交任务，不等待（后续手动查询）
python scripts/mps_dubbing.py --mode async-tts \
    --text "长文本..." \
    --voice-id "v1_Pi1pR9Q9UHqVOrQ0YpZFwL+Q/..." \
    --url "https://example.com/any_accessible.mp4" \
    --no-wait

# ── 语音转语音（async-sts）───────────────────────────────────────────────────

# 对视频做音色替换（使用指定音色 ID）
python scripts/mps_dubbing.py --mode async-sts \
    --url https://example.com/video.mp4 \
    --voice-id "v1_Pi1pR9Q9UHqVOrQ0YpZFwL+Q/..." \
    --output-dir /output/sts/ \
    --download-dir ./output/

# 对视频做音色替换（现场克隆音色，指定克隆源视频）
python scripts/mps_dubbing.py --mode async-sts \
    --url https://example.com/video.mp4 \
    --clone-video-url https://example.com/train.mp4 \
    --output-dir /output/sts/

# 使用 COS 输入文件
python scripts/mps_dubbing.py --mode async-sts \
    --cos-input-key /input/video.mp4 \
    --voice-id "v1_Pi1pR9Q9UHqVOrQ0YpZFwL+Q/..." \
    --output-dir /output/sts/ \
    --download-dir ./output/

# ── 其他 ──────────────────────────────────────────────────────────────────────

# 查询已有任务结果
python scripts/mps_get_video_task.py --task-id 2600011633-WorkflowTask-xxxxx --verbose

# 查询任务并下载结果到本地
python scripts/mps_get_video_task.py --task-id 2600011633-WorkflowTask-xxxxx --download-dir ./output/

# Dry Run（只打印请求参数，不调用 API）
python scripts/mps_dubbing.py --mode tts \
    --text "您好" --voice-id "v1_xxx..." --dry-run
```
