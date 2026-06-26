---
name: senseaudio-songmaker
description: Generate a complete song from a text description — AI writes lyrics then composes music. Use when users want to create a song, turn a description into audio, or generate background music. Triggers on "帮我写一首关于夏天的流行歌曲", "用这段歌词生成一首摇滚歌曲", "生成一首纯音乐背景曲", "AI 作词作曲", "作曲", "写歌", "给我生成一首歌".
metadata:
  openclaw:
    requires:
      env:
        - SENSEAUDIO_API_KEY
      bins:
        - curl
        - jq
    primaryEnv: SENSEAUDIO_API_KEY
    homepage: https://senseaudio.cn
compatibility:
  required_credentials:
    - name: SENSEAUDIO_API_KEY
      description: API key from https://senseaudio.cn/platform/api-key
      env_var: SENSEAUDIO_API_KEY
---

# SenseAudio Songmaker

Two-step song creation: generate lyrics → compose music. If the user already has lyrics, skip to Step 2.

## Workflow

```
用户描述 → [Step 1] 生成歌词 → 用户确认/修改 → [Step 2] 生成歌曲 → 返回链接
                                ↑ 用户自带歌词时跳过 Step 1
```

---

## Step 1: Generate Lyrics

**Skip this step if the user provides their own lyrics.**

```bash
LYRICS_RESP=$(curl -s -X POST "https://api.senseaudio.cn/v1/song/lyrics/create" \
  -H "Authorization: Bearer $SENSEAUDIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"prompt\": \"<USER_PROMPT>\", \"provider\": \"sensesong\"}")

TASK_ID=$(echo $LYRICS_RESP | jq -r '.task_id // empty')
```

If `task_id` is present, poll until done:

```bash
while true; do
  POLL=$(curl -s "https://api.senseaudio.cn/v1/song/lyrics/pending/$TASK_ID" \
    -H "Authorization: Bearer $SENSEAUDIO_API_KEY")
  STATUS=$(echo $POLL | jq -r '.status')
  { [ "$STATUS" = "SUCCESS" ] || [ "$STATUS" = "FAILED" ]; } && break
  sleep 3
done
LYRICS=$(echo $POLL | jq -r '.response.data[0].text')
```

If no `task_id` (sync response), read directly:

```bash
LYRICS=$(echo $LYRICS_RESP | jq -r '.data[0].text')
```

**Show the lyrics to the user and ask for confirmation or edits before proceeding.**

### Lyrics Format

The API uses structured section tags separated by ` ; `:

```
[intro-medium] ; [verse] 第一段歌词内容 ; [chorus] 副歌内容 ; [bridge] 桥段 ; [outro-short]
```

Common tags: `[intro-short]` `[intro-medium]` `[verse]` `[chorus]` `[bridge]` `[outro-short]` `[outro-medium]` `[inst-short]`

If the user provides plain lyrics without tags, wrap them: `[verse] <lyrics> ; [chorus] <chorus>`

---

## Step 2: Generate Song

Build the request body from user preferences:

| User says | Parameter |
|-----------|-----------|
| 男声 / 男歌手 | `"vocal_gender": "m"` |
| 女声 / 女歌手 | `"vocal_gender": "f"` |
| 纯音乐 / 无人声 | `"instrumental": true` (omit lyrics) |
| 风格描述（摇滚/流行/古风…） | `"style": "<描述>"` |
| 不要某种风格 | `"negative_tags": "<描述>"` |

```bash
SONG_RESP=$(curl -s -X POST "https://api.senseaudio.cn/v1/song/music/create" \
  -H "Authorization: Bearer $SENSEAUDIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"sensesong\",
    \"lyrics\": \"<LYRICS>\",
    \"title\": \"<TITLE>\",
    \"vocal_gender\": \"<f|m>\",
    \"style\": \"<STYLE>\"
  }")

SONG_TASK=$(echo $SONG_RESP | jq -r '.task_id')
```

Song generation always returns a `task_id`. Poll until done (may take 30–120s):

```bash
while true; do
  POLL=$(curl -s "https://api.senseaudio.cn/v1/song/music/pending/$SONG_TASK" \
    -H "Authorization: Bearer $SENSEAUDIO_API_KEY")
  STATUS=$(echo $POLL | jq -r '.status')
  { [ "$STATUS" = "SUCCESS" ] || [ "$STATUS" = "FAILED" ]; } && break
  echo "生成中... ($STATUS)"
  sleep 5
done
```

---

## Output

On SUCCESS, extract and display:

```bash
echo $POLL | jq -r '.response.data[0] | "标题：\(.title)\n时长：\(.duration) 秒\n音频：\(.audio_url)\n封面：\(.cover_url)"'
```

Example output:
```
标题：夏日物语
时长：187 秒
音频：https://cdn.senseaudio.cn/songs/xxx.mp3
封面：https://cdn.senseaudio.cn/covers/xxx.jpg
```

On FAILED, report the status and suggest retrying with a different style or simpler lyrics.
