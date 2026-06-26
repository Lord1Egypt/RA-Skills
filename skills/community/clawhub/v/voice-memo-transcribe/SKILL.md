---
name: voice-memo-transcribe
description: >
  Transcribe Apple Voice Memos recordings to text, organize content, and save to Apple Notes.
  Workflow: iPhone Voice Memos → iCloud sync → Mac Voice Memos DB → transcribe → Apple Notes → iCloud sync back to iPhone.
  Requires macOS with iCloud-enabled Voice Memos. Uses faster-whisper for AI transcription with auto device detection.
  Triggers on: "语音备忘录", "录音转文字", "voice memo", "transcribe recording", "录音整理", "录音笔记".
license: MIT-0
---

# Voice Memo Transcribe / 语音备忘录转写

Transcribe Apple Voice Memos on Mac and save organized notes to Apple Notes — syncing back to iPhone via iCloud.

将 iPhone 语音备忘录通过 iCloud 同步到 Mac 后，AI 转写为文字，整理内容，并存入 Mac 备忘录，再通过 iCloud 同步回 iPhone。

```
iPhone 录音 → iCloud 同步 → Mac 语音备忘录 → AI 转写 → 整理 → Mac 备忘录 → iCloud → iPhone 备忘录
```

## Prerequisites / 前置条件

1. **macOS** with Voice Memos app / 运行语音备忘录的 Mac
2. **iCloud sync** enabled for both Voice Memos and Notes (System Settings → Apple ID → iCloud) / 已启用语音备忘录和备忘录的 iCloud 同步
3. **Full Disk Access** granted to terminal app (System Settings → Privacy & Security → Full Disk Access) / 终端已获取「完全磁盘访问权限」
4. **ffmpeg** — `brew install ffmpeg`
5. **uv** — `brew install uv`

## Database & File Paths / 数据库与文件路径

- Database / 数据库: `~/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings/CloudRecordings.db`
- Audio files / 音频文件: `~/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings/`

## Workflow / 工作流程

### Step 1: List Voice Memos / 列出语音备忘录

```bash
python3 scripts/list_memos.py [options]
```

| Option | Description / 说明 | Default / 默认 |
|--------|-------------|---------|
| `--limit N` | Number of results / 返回数量 | 20 |
| `--offset N` | Pagination offset / 分页偏移 | 0 |
| `--search TERM` | Search by title / 按标题搜索 | — |
| `--after YYYY-MM-DD` | Filter after date / 起始日期 | — |
| `--before YYYY-MM-DD` | Filter before date / 截止日期 | — |
| `--json` | JSON output / JSON 格式输出 | off |

Present results as numbered list: title, date, duration. Ask user which to transcribe.

以编号列表展示：标题、日期、时长。询问用户要转写哪些。

**Error "Database not found" / 报错"数据库未找到"** → Enable iCloud sync for Voice Memos, or grant Full Disk Access. / 启用语音备忘录的 iCloud 同步，或授予完全磁盘访问权限。

### Step 2: Check Built-in Transcript / 检查内置转写

Some Voice Memos have Apple's embedded transcripts (tsrp atom):

部分语音备忘录包含 Apple 自动生成的转写文本（tsrp atom）：

```bash
python3 scripts/extract_transcript.py "<PATH>.m4a"
```

If transcript found → skip to Step 4. If `"no embedded transcript"` → proceed to AI transcription.

如果找到转写文本 → 跳到第 4 步。如果显示 `"no embedded transcript"` → 进入 AI 转写。

### Step 3: AI Transcription / AI 转写

```bash
uv run --with faster-whisper python3 scripts/transcribe.py "<AUDIO_PATH>" [options]
```

| Option | Description / 说明 | Default / 默认 |
|--------|-------------|---------|
| `--model` | tiny/base/small/medium/large-v3 | base |
| `--language` | zh, en, ja, etc. | auto-detect / 自动检测 |
| `--output PATH` | Save transcript to file / 保存到文件 | stdout / 标准输出 |
| `--device` | cpu/coreml/mps | auto-detect / 自动检测 |

**Model guide (15 min audio, Apple Silicon M1) / 模型参考（15 分钟音频，Apple Silicon M1）：**
| Model | Time / 耗时 | RAM / 内存 | Quality / 质量 |
|--------|------|-----|---------|
| base   | ~2 min | 1.5 GB | Good / 良好 |
| small  | ~5 min | 2 GB | Better / 较好 |
| medium | ~10 min | 5 GB | Very good / 很好 |

**Tip / 提示：** Start with `base` for preview, re-run with `small` or `medium` for final output. / 先用 `base` 快速预览，再用 `small` 或 `medium` 获取最终结果。

### Step 4: Organize Content / 整理内容

1. Read transcript, identify topics, speakers, key moments / 阅读转写文本，识别话题、发言者、关键时刻
2. Create structured summary with timestamps / 创建带时间戳的结构化摘要
3. Ask user for context corrections if unclear (relationships, names, topic labels) / 如有疑问，向用户确认（人物关系、姓名、话题标签）
4. Misidentified speakers/names make notes worse — always confirm / 错误的发言者识别会降低笔记质量——务必确认

### Step 5: Save to Apple Notes / 保存到备忘录

```bash
# Write content to temp file / 将内容写入临时文件
python3 -c "
content = open('/dev/stdin').read()
with open('/tmp/note_content.txt', 'w') as f:
    f.write(content)
" <<< "$NOTE_BODY"

# Create note in a specific folder / 在指定文件夹创建备忘录
osascript -e '
tell application "Notes"
    tell folder "<FOLDER_NAME>"
        set noteTitle to "<TITLE>"
        set noteBody to do shell script "cat /tmp/note_content.txt"
        make new note with properties {name:noteTitle, body:noteBody}
    end tell
end tell
'
```

Omit `tell folder` block to use the default Notes folder. The note syncs to iPhone via iCloud automatically.

去掉 `tell folder` 部分可使用默认文件夹。备忘录会通过 iCloud 自动同步到 iPhone。

## Batch Processing / 批量处理

1. List memos → user selects multiple / 列出录音 → 用户选择多条
2. Transcribe one at a time (avoids memory pressure) / 逐条转写（避免内存压力）
3. Present each for review / 逐条展示供审阅
4. Save to Notes individually or batch at end / 逐条保存或最后批量保存

## Tips / 注意事项

- For long recordings (>30 min), warn about processing time / 长录音（>30 分钟）需提醒处理时间
- Auto device detection prefers CoreML (Apple Silicon) > MPS > CPU / 设备自动检测优先级：CoreML > MPS > CPU
- If faster-whisper OOMs, fall back to smaller model / 内存不足时回退到更小的模型
- If no Apple transcript exists, suggest user open the memo on iPhone to trigger auto-transcription / 无内置转写时，建议用户在 iPhone 上打开录音触发自动转写
- Clean up `/tmp/note_content.txt` after use / 使用后清理临时文件
