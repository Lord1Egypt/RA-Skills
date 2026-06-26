---
name: xiaomi-any2speech
description: >
  声音世界模型（Speech World Model）：不只是 TTS，而是理解场景、角色、情绪并自主规划表达的语音大模型。
  原生支持长文+多人、中英双语，也支持上传参考音频进行音色克隆（Voice Prompt / voice cloning），内置高能创作模板，将任意内容转为播客/有声书/相声/Rap/广播剧等，单次最长 ~10 分钟，输出 WAV。
  涵盖单人TTS、VoiceDesigner音色定制、参考音频克隆、多人人物对话合成、长文有声化、Instruct TTS 的超集。
  A Speech World Model: beyond TTS — understands scenes, characters, and emotions to autonomously plan expressive speech.
  Native long-form & multi-speaker synthesis in Chinese/English, and supports reference-audio voice cloning (Voice Prompt), up to ~10 min per pass.
  触发意图：用我的声音/用这个音色/参考这段录音/克隆声音/模仿声音、做成播客/相声/辩论/有声书/Rap/新闻/脱口秀/电台/课程/广播剧/评书/讲故事、朗读/念出来/转语音/TTS/生成音频/做个语音版/配音、变成能听的/用XX腔念、发语音/做成XX发给我、用模板/选模板/有什么模板。
  English: make a podcast/audiobook/debate/rap/news/stand-up/story/radio drama, read aloud/TTS/generate audio/voice over/narrate/dub/mimic voice/clone voice/use my voice/use this voice sample, make it listenable, send as voice.
---

# Any2Speech

所有能力通过同一套 API 完成，由 `instruction` 字段决定最终形态。内置免费公开 Key，无需注册。

**运行环境**：需要 `curl` 和 `python3`（用于 JSON 解析）；飞书发送可选需要 `ffmpeg`/`ffprobe`。

```bash
BASE=https://miplus-tts-public.ai.xiaomi.com
API_KEY=${API_KEY:-sk-anytospeech-pub-free}
```

## Step 1 · 确认输入

| 用户给了什么 | source_type | curl 参数 |
|---|---|---|
| 文字内容 | `text` | `-F "source_type=text" -F "text=内容"` |
| 网页链接 | `url` | `-F "source_type=url" -F "url=链接"` |
| 本地文件 | `file` | `-F "source_type=file" -F "file=@/路径/文件"` |
| 参考音色文件 + 文字 | → **VP 流程** | 跳到 Step 3-VP |
| 参考音色文件 + 选模板 | → **VP 模板** | 跳到 VP 模板章节（不需要文字） |

**来源缺失时**：停下来问"请提供文字内容、网页链接或文件路径"，不要猜测或用空值执行。

**文件路径安全**：仅接受用户在当前对话中明确提供的路径。不要自行扫描目录或猜测文件；不要读取 `~/.ssh`、`~/.env`、`~/.config` 等敏感路径。

**VP 判断**：用户提供了参考音色文件（wav/mp3/m4a/flac/ogg/webm），或说了"用我的声音"、"克隆音色"、"参考这段录音"等 → 走 **Step 3-VP**。用户说了"用模板"或指定模板名 → 走 **VP 模板**（不需要文字）。VP 的一步式和两步式需要 `text`，模板不需要。

## Step 2 · 构造 instruction

`instruction` 控制合成形态。选择逻辑：用户明确描述了风格 → 直接用；只说"帮我读" → 留空（单人朗读）；说了场景没细节 → 从下表取最近的；英文输入 → 加 `English` 关键词。

| 场景 | 中文 instruction | English instruction |
|---|---|---|
| 两人播客 | `两人播客，一人理性分析，一人感性追问，偶尔插嘴，5分钟内` | `Two-host podcast, one analytical, one curious, with interruptions, under 5 min` |
| 相声 | `传统相声，甲逗哏（语速快、北京腔），乙捧哏（沉稳正经），至少两个包袱` | — |
| 新闻播报 | `CCTV 新闻联播风格，先播导语，再逐条播报，结尾有总结语` | `CNN anchor style, lead-in then item-by-item, closing summary` |
| 辩论 | `正反双方，正方激情澎湃，反方逻辑冷静，各做30秒总结陈词` | `Pro vs Con, pro passionate, con logical, 30s closing each` |
| Rap | `押韵，节奏感强，两人 battle，明显停顿和连读节奏` | `Rhyming rap battle, two performers, strong rhythm` |
| 脱口秀 | `单人独白，幽默有深度，有停顿节奏感，偶尔自嘲` | `Solo monologue, witty and deep, rhythmic pauses` |
| 有声书 | `第三人称叙述，情绪随剧情起伏，遇到对话切换人物语气` | `Third-person narration, emotion follows plot, voice-switch for dialogue` |
| 情感电台 | `深夜电台，低沉磁性男声，语速缓慢` | `Late-night radio, deep magnetic male voice, slow pace` |
| 单人 TTS | `女声，职业干练，语速偏快` | `Female, professional tone, slightly fast` |

**可叠加控制**：语种（`英文`/`中英混合`）、音色（`声音醇厚磁性`）、情绪弧线（`开场铺垫，中段碰撞，结尾升华`）、互动（`允许插话`）、环境音（`加观众笑声`）、时长（`10分钟内`）、口音（`东北腔`/`British accent`）。建议核心控制点 ≤ 5 个。

## Step 3 · 选接口并执行

**默认走同步**，切异步条件：504 超时 / 文件输入 / 文本超 1000 字。

### 同步

```bash
OUTPUT=output_$(date +%s).wav
curl -X POST "$BASE/v1/audio/generate" \
  -H "Authorization: Bearer $API_KEY" \
  -F "source_type=text" \
  -F "text=内容" \
  -F "instruction=风格描述" \
  --max-time 600 \
  --output "$OUTPUT"
echo "✓ 保存至 $OUTPUT"
```

### 异步（504 / 文件 / 长文本）

```bash
OUTPUT=output_$(date +%s).wav
JOB=$(curl -s -X POST "$BASE/v1/audio/jobs" \
  -H "Authorization: Bearer $API_KEY" \
  -F "source_type=text" \
  -F "text=内容" \
  -F "instruction=两人播客，一人理性分析，一人感性追问，5分钟内" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['job_id'])")
echo "已提交: $JOB"

for i in $(seq 1 60); do
  STATUS=$(curl -s -H "Authorization: Bearer $API_KEY" \
    "$BASE/v1/audio/jobs/$JOB" \
    | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")
  [ "$STATUS" = "done" ]   && break
  [ "$STATUS" = "failed" ] && echo "生成失败" && exit 1
  sleep 10
done
[ "$STATUS" != "done" ] && echo "轮询超时" && exit 1

curl -s -H "Authorization: Bearer $API_KEY" \
  "$BASE/v1/audio/jobs/$JOB/download" --output "$OUTPUT"
echo "✓ 保存至 $OUTPUT"
```

## Step 3-VP · 参考音频克隆（Voice Prompt）

VP 接口与标准接口共用同一个 `$BASE` 和 `$API_KEY`。

**默认走一步式**——Agent 场景下一次调用最简洁。仅当用户明确要求"先看脚本"或"指定谁演谁"时才用两步式。

**多人角色与参考音频的对应关系**：如果需要确认“每个说话人用哪段参考音频”，优先走两步式 `think -> synthesize`。先用 `think` 拿到 `speakers` 和 `script_lines`，向用户确认角色列表，再按 `voice_file_{角色名}` 精确上传；不要只依赖上传顺序。多文件在字段名不匹配时按上传顺序兜底。

**单文件行为差异**：一步式（`generate`/`jobs`）传 1 个参考音频时，服务端自动注入单人朗读提示，强制生成单角色脚本；两步式 `synthesize` 无此限制，单文件会被复制给所有角色。因此多人场景只有 1 个参考音频时，应走两步式。

### 一步式（默认）

一次调用完成规划 + 合成。单人传一个 `voice_file_角色名`，多人传多个。

```bash
OUTPUT=vp_$(date +%s).wav
curl -X POST "$BASE/v1/audio/vp/generate" \
  -H "Authorization: Bearer $API_KEY" \
  -F "source_type=text" \
  -F "text=要合成的文本内容" \
  -F "instruction=两人播客，一人理性分析，一人感性追问" \
  -F "voice_file_主持人A=@/path/to/host_a.wav" \
  -F "voice_file_主持人B=@/path/to/host_b.mp3" \
  -F "denoise=1" \
  --max-time 600 \
  --output "$OUTPUT"
```

> 单人场景只需一个 `voice_file_主播=@ref.wav`。异步版用 `$BASE/v1/audio/vp/jobs` 提交，轮询方式与标准异步相同（加 `voice_file_*` 和可选 `denoise` 字段）。

### 两步式（用户要求预览脚本 / 指定角色映射 / 多次合成时使用）

**第一步 think**：LLM 规划，返回角色列表 + 可编辑脚本。

```bash
THINK=$(curl -s -X POST "$BASE/v1/audio/vp/think" \
  -H "Authorization: Bearer $API_KEY" \
  -F "source_type=text" \
  -F "text=要合成的文本内容" \
  -F "instruction=两人播客")
REQ_ID=$(echo "$THINK" | python3 -c "import sys,json; print(json.load(sys.stdin)['req_id'])")
echo "$THINK" | python3 -c "import sys,json; d=json.load(sys.stdin); print('speakers:', d['speakers']); [print(f\"  {l['speaker']}: {l['text']}\") for l in d['script_lines']]"
```

返回 `speakers`（如 `["主持人A","主持人B"]`）和 `script_lines`（`[{"speaker":"..","text":".."},...]`）。向用户展示脚本和角色列表，确认后进入第二步。

**第二步 synthesize**：上传参考音频合成。`voice_file_` 后缀必须与 `speakers` 中的角色名完全一致。同一 `req_id` 可多次调用，换音色或改脚本。

```bash
OUTPUT=vp_$(date +%s).wav
curl -X POST "$BASE/v1/audio/vp/synthesize" \
  -H "Authorization: Bearer $API_KEY" \
  -F "req_id=$REQ_ID" \
  -F "voice_file_主持人A=@/path/to/host_a.wav" \
  -F "voice_file_主持人B=@/path/to/host_b.webm" \
  -F "denoise=1" \
  --max-time 3600 \
  --output "$OUTPUT"
```

编辑脚本时加 `script_lines_json` 字段（JSON 字符串）：

```bash
curl -X POST "$BASE/v1/audio/vp/synthesize" \
  -H "Authorization: Bearer $API_KEY" \
  -F "req_id=$REQ_ID" \
  -F 'script_lines_json=[{"speaker":"主持人A","text":"修改后的台词"},{"speaker":"主持人B","text":"另一句"}]' \
  -F "voice_file_主持人A=@host_a.wav" \
  -F "voice_file_主持人B=@host_b.wav" \
  --max-time 3600 \
  --output "vp_edited.wav"
```

### VP 参数速查

| 参数 | 接口 | 说明 |
|---|---|---|
| `voice_file_{角色名}` | synthesize / generate / jobs | 参考音频（wav/mp3/m4a/flac/ogg/webm），5~20s 清晰人声最佳，超 20s 自动裁切 |
| `denoise` | synthesize / generate / jobs | `1`=显式开启降噪，`0`=显式关闭；未传时跟随服务端 `VP_DENOISE` 配置，当前部署默认关闭。参考音频环境嘈杂时建议显式传 `1` |
| `req_id` | synthesize | 来自 think 返回值 |
| `script_lines_json` | synthesize | 可选，编辑后脚本 `[{"speaker":"..","text":".."},...]` |

> 降噪预览（不合成，仅试听降噪效果）：`curl -X POST "$BASE/v1/audio/vp/denoise" -H "Authorization: Bearer $API_KEY" -F "voice_file=@ref.webm" --output denoised.wav`。当前返回标准 WAV，采样率为 48kHz。

### VP 模板（预置脚本，不需要输入文本）

列出模板 → prepare 选用 → synthesize 合成，与两步式共用 synthesize。

```bash
# 列出模板（返回 title / speakers / voice_count / sentence_count）
curl -s -H "Authorization: Bearer $API_KEY" "$BASE/v1/audio/vp/templates" \
  | python3 -c "import sys,json; [print(f\"{t['title']}（{t['voice_count']}人，{t['sentence_count']}句）\") for t in json.load(sys.stdin)['templates']]"

# prepare（用 title 标识，需 URL encode；不需要 text）
# 返回 req_id / speakers / summary / sentence_count / script_lines
TITLE="罗永浩、王自如的世纪骂战"
ENCODED=$(python3 -c "import sys,urllib.parse; print(urllib.parse.quote(sys.argv[1]))" "$TITLE")
PREP=$(curl -s -X POST "$BASE/v1/audio/vp/templates/$ENCODED/prepare" \
  -H "Authorization: Bearer $API_KEY")
REQ_ID=$(echo "$PREP" | python3 -c "import sys,json; print(json.load(sys.stdin)['req_id'])")
echo "$PREP" | python3 -c "import sys,json; d=json.load(sys.stdin); print('speakers:', d['speakers'])"

# synthesize（同两步式）
OUTPUT=vp_$(date +%s).wav
curl -X POST "$BASE/v1/audio/vp/synthesize" \
  -H "Authorization: Bearer $API_KEY" \
  -F "req_id=$REQ_ID" \
  -F "voice_file_主持人=@host.wav" \
  -F "voice_file_嘉宾=@guest.wav" \
  --max-time 3600 \
  --output "$OUTPUT"
```

---

## 错误处理

| 接口 | 错误 | 处置 |
|---|---|---|
| 标准 generate | 504 | 切 `/v1/audio/jobs` 异步重试 |
| 标准 generate | 502/500 | 等 30s 重试 1 次，仍失败告知用户 |
| VP generate（一步式） | 504 | 切 `/v1/audio/vp/jobs` 异步重试 |
| VP synthesize（两步式/模板） | 504/502 | **用同一个 `req_id` 重试 synthesize**（间隔 60s，最多 3 次）。不要切 `vp/jobs`——一步式会重新规划角色名，导致 `voice_file_` 字段名不匹配、按上传顺序兜底搞反音色 |
| 所有接口 | 422 | 检查参数后重试 1 次 |
| 所有接口 | 429 | 等 30s 后重试 1 次 |

**VP 合成必须等到完成**：长脚本（50+ 句）合成耗时可能超过 10 分钟，504 通常是暂时性超时而非永久失败。Agent 必须坚持用同一个 `req_id` 重试直到成功，**禁止自行拆分/截断 annotation 句子、禁止建议用户缩短内容**——VP 合成依赖完整上下文做韵律规划，拆分会破坏节奏和衔接。

## Step 4 · 交付结果

- 告知文件路径和大致时长（有 ffprobe 则 `ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$OUTPUT"`，无则按文本长度估算）
- 支持音频播放的环境尝试内联播放
- 不要主动执行用户未请求的操作（发飞书、上传云端等）
- 失败时给出原因和建议（简化文本 / 稍后重试）

## 飞书语音发送（可选）

**仅当用户明确说"发给我"/"发飞书"/"发到群里"时执行。**

前置：`FEISHU_TENANT_TOKEN`（或 `APP_ID` + `APP_SECRET`）、`CHAT_ID`、可选 `ffmpeg`/`ffprobe`。

```bash
[ -z "$FEISHU_TENANT_TOKEN" ] && FEISHU_TENANT_TOKEN=$(curl -s -X POST \
  "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['tenant_access_token'])")
ffmpeg -y -i "$OUTPUT" -c:a libopus -b:a 32k output.opus 2>/dev/null && UPLOAD=output.opus || UPLOAD="$OUTPUT"
DURATION_MS=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$OUTPUT" | awk '{printf "%d",$1*1000}')
FILE_KEY=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/files" \
  -H "Authorization: Bearer $FEISHU_TENANT_TOKEN" \
  -F "file=@$UPLOAD" -F "file_type=opus" -F "file_name=tts.opus" -F "duration=$DURATION_MS" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['file_key'])")
curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id" \
  -H "Authorization: Bearer $FEISHU_TENANT_TOKEN" -H "Content-Type: application/json" \
  -d "{\"receive_id\":\"$CHAT_ID\",\"msg_type\":\"audio\",\"content\":\"{\\\"file_key\\\":\\\"$FILE_KEY\\\"}\"}"
```

## 注意事项

- **文本长度**：建议 50~5000 字；超 1000 字自动走异步
- **文件大小**：> 20MB 建议先压缩；支持 `txt` `md` `pdf` `docx` `csv` `json` `html` + 常见音视频
- **频率**：公共 Key 有并发限制，间隔 ≥ 3s，429 则等 30s 重试，批量请串行
- **耗时参考**：短文本 10–30s / 长文 30s–3min / 多人节目 1–10min
- **输出**：生成接口默认返回 WAV（24kHz）；`/v1/audio/vp/denoise` 降噪预览当前返回 WAV（48kHz）。建议用时间戳命名避免覆盖
- **说话人**：建议 ≤ 4 人，人数越多控制难度越高
