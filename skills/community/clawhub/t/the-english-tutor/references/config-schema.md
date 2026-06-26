# English Tutor · 完整配置参考

## 配置存储

用户配置统一保存在 `~/.openclaw/english-tutor/config.json`，由 `scripts/config_manager.py` 管理。

**首次由陪练助手通过对话引导创建，无需手动编辑。**

---

## config.json 字段说明

### 基础配置

| 字段 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `setup_complete` | ✅ | `false` | 首次设置是否完成 |
| `word_list_path` | ✅ | `""` | 单词表 JSON 文件路径 |
| `daily_words` | ✅ | `5` | 每日练习单词数量（建议 5-15）|
| `schedule_times` | ✅ | `["08:00"]` | 每日推送时间（上海时区）|

### LLM 模型配置 🤖

| 字段 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `llm_provider` | ✅ | `"openclaw"` | 模型提供商：`openclaw` / `minimax` / `openai` |
| `llm_model` | 否 | `""` | 指定模型 ID（留空用默认）|

> 选择 `openclaw` 时使用系统默认 LLM，无需额外配置。

### 飞书语音配置 📢

| 字段 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `feishu_app_id` | ✅ | `""` | 飞书应用 App ID |
| `feishu_app_secret` | ✅ | `""` | 飞书应用 App Secret |
| `feishu_bot_token` | 否 | `""` | 飞书 Bot Token（可选）|
| `feishu_user_open_id` | ✅ | `""` | 接收消息的用户 Open ID |

### TTS 语音合成 🔊

| 字段 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `tts_provider` | 否 | `"minimax"` | TTS 方案：`minimax` / `piper` / `espeak` |
| `minimax_api_key` | minimax时 | `""` | MiniMax API Key |

> MiniMax TTS 有 API Key 时推荐音色：`male-qn-qingse`（男声）、`female-tianmei`（女声）；无 Key 时静默跳过，可配 Piper 本地兜底

### 多维表格（可选）

| 字段 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `bitable_app_token` | 否 | `""` | 飞书多维表格 App Token |
| `bitable_words_table_id` | 否 | `""` | words 表 ID |
| `bitable_chat_table_id` | 否 | `""` | chat_log 表 ID |

### Piper 本地 TTS（可选）

| 字段 | 必填 | 说明 |
|------|------|------|
| `piper_bin` | piper时 | piper 二进制路径 |
| `piper_model` | piper时 | .onnx 模型文件路径 |

---

## 飞书 audio 消息发送流程

每日练习第一步，通过 `scripts/feishu_voice.py` 实现：

```
1. TTS 合成 mp3
   - minimax: POST /v1/t2a_v2 → hex audio → 解码为 mp3
   - piper:   piper CLI → WAV
   
2. ffmpeg 转 opus
   ffmpeg -i input.mp3 -ar 16000 -ac 1 -acodec libopus -b:a 128k output.opus

3. 上传获取 file_key
   POST /open-apis/im/v1/files
   Content-Type: multipart/form-data; boundary=...
   body: file_type=opus, file=opus二进制

4. 发送 audio 消息
   POST /open-apis/im/v1/messages?receive_id_type=open_id
   {
     "receive_id": "<user_open_id>",
     "msg_type": "audio",
     "content": "{\"file_key\": \"<file_key>\"}"
   }
```

**使用示例：**
```bash
# 使用配置发送语音
python3 scripts/feishu_voice.py "Good morning! Today's vocabulary: commute, subway, transfer."

# 使用配置（指定路径）
python3 scripts/feishu_voice.py "Hello!" --config /path/to/config.json

# 仅合成，不发送（调试用）
python3 scripts/feishu_voice.py "Hello!" --dry-run
```

---

## TTS_PROVIDER 配置

### minimax（默认，云端，音质最好）

```env
TTS_PROVIDER=minimax
MINIMAX_API_KEY=sk-your-key
MINIMAX_TTS_MODEL=speech-2.8-hd
MINIMAX_TTS_VOICE_ID=male-qn-qingse
MINIMAX_TTS_SPEED=1.05
```

### piper（本地，高质量，离线）

**下载主程序（Linux x86_64）：**
```bash
curl -L https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_amd64.tar.gz \
  -o /tmp/piper.tar.gz && tar xf /tmp/piper.tar.gz -C /tmp
```

**下载英语模型（Lessac Medium，音质好，速度快）：**
```bash
curl -L "https://hf-mirror.com/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx" \
  -o /tmp/en_US-lessac-medium.onnx
```

```env
TTS_PROVIDER=piper
PIPER_BIN=/tmp/piper/piper_phonemize
PIPER_MODEL=/tmp/en_US-lessac-medium.onnx
```

**测试：**
```bash
echo "Hello world" | /tmp/piper/piper_phonemize \
  --model /tmp/en_US-lessac-medium.onnx \
  --input-file /dev/stdin -w /tmp/test.wav
```

### espeak-ng（系统级，完全离线）

```bash
sudo apt-get install espeak-ng
```

```env
TTS_PROVIDER=espeak
ESPEAK_VOICE=en-us
```

---

## ASR_PROVIDER 配置

### local（默认，推荐，完全离线）

```bash
pip install --user --break-system-packages numpy sherpa-onnx
bash scripts/download_model.sh
```

### assemblyai / openai（云端）

```env
ASR_PROVIDER=assemblyai
ASR_API_KEY=your-key
```

---

## 多维表格表结构（可选）

**表 1：单词表（words）**

| 字段名 | 类型 | 说明 |
|--------|------|------|
| word | 文本 | 英文单词 |
| pronunciation | 文本 | 音标 |
| meaning | 文本 | 中文释义 |
| example | 文本 | 例句 |
| mastery | 数字 | 掌握程度 0-5 |
| review_count | 数字 | 复习次数 |
| last_review | 日期时间 | 最近复习时间 |
| next_review | 日期时间 | 下次复习时间 |
| user_id | 文本 | 用户 ID |

**表 2：对话记录（chat_log）**

| 字段名 | 类型 | 说明 |
|--------|------|------|
| user_id | 文本 | 用户 ID |
| role | 单选 | `ai` 或 `user` |
| text | 文本 | 对话内容 |
| voice_url | 文本 | 语音 URL（可选）|
| created_at | 日期时间 | 创建时间 |
